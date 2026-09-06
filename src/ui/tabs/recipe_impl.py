"""Core recipe helpers and original playbooks (restored from artifacts)."""

from core.fortios_version import (
    version_banner,
    ike_log_filter_clear,
    ike_filter_remote_peer,
    ike_filter_name,
    sdwan_cmd,
    sdwan_service_cmd,
)
from core.safety import preamble, epilogue


class RecipeImplMixin:
    """Helpers + core recipes. Extended by RecipeExtraMixin / RecipeR6Mixin."""

    def _vdom_banner(self, vd: str) -> list:
        """Advisory lines when VDOM index/name is set (CLI context is operator responsibility)."""
        if not vd:
            return []
        return [
            f"# VDOM context: {vd}",
            f"# If multi-VDOM: config vdom → edit <name>  OR  session/flow filter vd <index>",
            "",
        ]

    def _sniffer(self, iface: str, src: str, dst: str, port: str, proto: str = "") -> str:
        parts = []
        if src:
            parts.append(f"host {src}")
        if dst:
            parts.append(f"host {dst}")
        if port:
            parts.append(f"port {port}")
        if proto:
            parts.append(proto)
        filt = " and ".join(parts) if parts else ""
        return f"diagnose sniffer packet {iface} '{filt}' 4 0 l"

    def _session_block(self, src: str, dst: str, port: str, vd: str = "") -> list:
        lines = ["diagnose sys session filter clear"]
        if vd:
            lines.append(f"diagnose sys session filter vd {vd}")
        if src:
            lines.append(f"diagnose sys session filter src {src}")
        if dst:
            lines.append(f"diagnose sys session filter dst {dst}")
        if port:
            lines.append(f"diagnose sys session filter dport {port}")
        lines.append("diagnose sys session list")
        return lines

    def _flow_block(self, src: str, dst: str, port: str, count: str = "100", vd: str = "") -> list:
        lines = list(preamble(reset=True, clear_flow_filter=True, timestamps=True))
        if vd:
            lines.append(f"diagnose debug flow filter vd {vd}")
        if src:
            lines.append(f"diagnose debug flow filter saddr {src}")
        if dst:
            lines.append(f"diagnose debug flow filter daddr {dst}")
        if port:
            lines.append(f"diagnose debug flow filter port {port}")
        lines += [
            "diagnose debug flow show function-name enable",
            "diagnose debug flow show iprope enable",
            "diagnose debug flow show console enable",
            "diagnose debug enable",
            f"diagnose debug flow trace start {count}",
        ]
        lines.extend(epilogue(stop=True))
        return lines

    def _first_steps(self, src: str, dst: str, port: str, vd: str = "") -> str:
        lines = self._vdom_banner(vd) + [
            "# === Recipe: First steps connectivity ===",
            "# sniffer → session → flow → routing",
            "",
            "# 1) Sniffer",
            self._sniffer("any", src, dst, port),
            "",
            "# 2) Sessions",
        ]
        lines.extend(self._session_block(src, dst, port, vd))
        lines += ["", "# 3) Debug flow"]
        lines.extend(self._flow_block(src, dst, port, vd=vd))
        lines += ["", "# 4) Routing"]
        lines.append(
            f"get router info routing-table details {dst}"
            if dst
            else "get router info routing-table all"
        )
        return "\n".join(lines)

    def _traffic_not_passing(self, src: str, dst: str, port: str, vd: str = "") -> str:
        lines = self._vdom_banner(vd) + ["# === Recipe: Traffic not passing ===", "", "# Sessions"]
        lines.extend(self._session_block(src, dst, port, vd))
        lines += ["", "# Flow"]
        lines.extend(self._flow_block(src, dst, port, "200", vd=vd))
        lines += ["", "# Sniffer", self._sniffer("any", src, dst, port)]
        return "\n".join(lines)

    def _vpn_down(self, version, peer: str) -> str:
        lines = [
            version_banner(version, "IKE filter"),
            "# === Recipe: VPN down / rekey ===",
            "",
            "diagnose vpn ike gateway list",
            "diagnose vpn tunnel list",
            "diagnose vpn ike status",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        lines.append(ike_log_filter_clear(version))
        if peer:
            if "." in peer and any(c.isdigit() for c in peer):
                lines.append(ike_filter_remote_peer(version, peer))
            else:
                lines.append(ike_filter_name(version, peer))
        lines += ["diagnose debug application ike -1", "diagnose debug enable"]
        lines.extend(epilogue(stop=True))
        return "\n".join(lines)

    def _high_cpu(self) -> str:
        return "\n".join([
            "# === Recipe: High CPU ===", "",
            "get system performance status",
            "diagnose sys top 5 30",
            "diagnose sys top-mem",
            "diagnose sys session full-stat",
            "diagnose hardware cpuinfo",
            "diagnose debug crashlog read",
            "diagnose sys mpstat 1 5",
        ])

    def _high_memory(self) -> str:
        return "\n".join([
            "# === Recipe: High memory / conserv mode ===", "",
            "get system performance status",
            "diagnose hardware meminfo",
            "diagnose sys top-mem",
            "diagnose sys session full-stat",
            "diagnose sys confcache status",
            "get system global | grep -i conserv",
        ])

    def _session_full(self) -> str:
        return "\n".join([
            "# === Recipe: Session table full ===", "",
            "diagnose sys session full-stat",
            "diagnose sys session stat",
            "get system performance status",
            "diagnose firewall statistic show",
        ])

    def _ha_sync(self) -> str:
        lines = [
            "# === Recipe: HA out-of-sync ===", "",
            "get system ha status",
            "diagnose sys ha status",
            "diagnose sys ha checksum cluster",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        lines += ["diagnose debug application hasync -1", "diagnose debug enable"]
        lines.extend(epilogue(stop=True))
        return "\n".join(lines)

    def _sdwan_dead(self, version) -> str:
        return "\n".join([
            version_banner(version, "SD-WAN prefix"),
            "# === Recipe: SD-WAN member dead ===", "",
            sdwan_cmd(version, "health-check"),
            sdwan_cmd(version, "member"),
            sdwan_service_cmd(version),
            sdwan_cmd(version, "zone"),
            "diagnose sys link-monitor status",
        ])

    def _dialup_ipsec(self, version, peer: str, client: str) -> str:
        lines = [
            version_banner(version, "IKE filter"),
            "# === Recipe: Dial-up IPsec ===",
            "",
            "diagnose vpn ike gateway list",
            "diagnose vpn tunnel list",
            "get vpn ipsec tunnel summary",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        lines.append(ike_log_filter_clear(version))
        if peer:
            if "." in peer:
                lines.append(ike_filter_remote_peer(version, peer))
            else:
                lines.append(ike_filter_name(version, peer))
        elif client:
            lines.append(ike_filter_remote_peer(version, client))
        lines += [
            "diagnose debug application ike -1",
            "diagnose debug application fnbamd -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        return "\n".join(lines)

    def _ssl_login_fail(self, client_ip: str) -> str:
        lines = [
            "# === Recipe: SSL VPN login fail ===",
            "",
            "get vpn ssl monitor",
            "diagnose vpn ssl list",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        if client_ip:
            lines.append(f"diagnose vpn ssl debug-filter src-addr4 {client_ip}")
        lines += [
            "diagnose debug application sslvpn -1",
            "diagnose debug application authd -1",
            "diagnose debug application fnbamd -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        lines += ["", "diagnose firewall auth list"]
        return "\n".join(lines)

    def _policy_nat(self, src: str, dst: str, port: str) -> str:
        lines = ["# === Recipe: Policy / NAT check ===", "", "# Sessions"]
        lines.extend(self._session_block(src, dst, port))
        lines += ["", "# Flow + iprope"]
        lines.extend(self._flow_block(src, dst, port))
        return "\n".join(lines)

    def _vip(self, client: str, vip: str, port: str, wan: str) -> str:
        lines = [
            "# === Recipe: VIP / port forward ===",
            "# Шукай: DNAT, VIP-..., policy 0 drop",
            "",
            "# Sniffer WAN",
            self._sniffer(wan, client, vip, port),
            "",
            "# Flow",
        ]
        lines.extend(self._flow_block(client, vip, port, "50"))
        lines += ["", "# Sessions"]
        lines.extend(self._session_block(client, vip, port))
        return "\n".join(lines)

    def _local_in(self, src: str, iface: str) -> str:
        lines = [
            "# === Recipe: Local-in / admin access ===",
            "",
            "diagnose firewall iprope list 100000",
            "get system interface physical",
            "diagnose ip address list",
            "",
        ]
        lines.extend(preamble(reset=True, clear_flow_filter=True, timestamps=True))
        if src:
            lines.append(f"diagnose debug flow filter saddr {src}")
        lines += [
            "diagnose debug flow show function-name enable",
            "diagnose debug flow show iprope enable",
            "diagnose debug enable",
            "diagnose debug flow trace start 50",
        ]
        lines.extend(epilogue(stop=True))
        lines += [
            "",
            self._sniffer(iface if iface != "any" else "any", src, "", "22", "tcp"),
            "# also try port 443 / 10443 for HTTPS admin",
        ]
        return "\n".join(lines)

    def _ospf(self) -> str:
        lines = [
            "# === Recipe: OSPF neighbor down ===",
            "",
            "get router info ospf status",
            "get router info ospf neighbor",
            "get router info ospf interface",
            "get router info routing-table ospf",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose ip router ospf all enable",
            "diagnose ip router ospf level info",
            "diagnose debug enable",
            "",
            "# --- after test ---",
            "diagnose debug disable",
            "diagnose ip router ospf all disable",
            "diagnose debug reset",
        ]
        return "\n".join(lines)

    def _bgp(self, neighbor: str) -> str:
        lines = [
            "# === Recipe: BGP neighbor down ===",
            "",
            "get router info bgp summary",
            "get router info bgp network",
        ]
        if neighbor:
            lines.append(f"get router info bgp neighbors {neighbor}")
            lines.append(f"get router info bgp neighbors {neighbor} routes")
            lines.append(f"get router info bgp neighbors {neighbor} advertised-routes")
        lines.append("")
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose ip router bgp all enable",
            "diagnose ip router bgp level info",
            "diagnose debug enable",
            "",
            "# --- after test ---",
            "diagnose debug disable",
            "diagnose ip router bgp all disable",
            "diagnose debug reset",
        ]
        return "\n".join(lines)

    def _routing(self, dst: str) -> str:
        lines = [
            "# === Recipe: Static route / RIB ===",
            "",
            "get router info routing-table all",
            "get router info routing-table database",
            "get router info routing-table static",
            "diagnose firewall proute list",
            "diagnose firewall proute6 list",
        ]
        if dst:
            lines.append(f"get router info routing-table details {dst}")
        return "\n".join(lines)

    def _dhcp(self, iface: str) -> str:
        lines = [
            "# === Recipe: DHCP no lease ===",
            "",
            "execute dhcp lease-list",
            f"diagnose sniffer packet {iface} 'port 67 or port 68' 4 0 l",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose debug application dhcprelay -1",
            "diagnose debug application dhcpd -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        return "\n".join(lines)

    def _auth_fsso(self) -> str:
        lines = [
            "# === Recipe: Auth / FSSO ===",
            "",
            "diagnose firewall auth list",
            "diagnose debug authd fsso list",
            "diagnose debug authd fsso server-status",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose debug application authd -1",
            "diagnose debug application fnbamd -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        return "\n".join(lines)

    def _dns(self, src: str, dst: str) -> str:
        lines = ["# === Recipe: DNS issues ===", ""]
        lines.extend(self._session_block(src, dst, "53"))
        lines.append("")
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose debug application dnsproxy -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        lines += ["", "diagnose sniffer packet any 'port 53' 4 0 l"]
        return "\n".join(lines)

    def _webfilter(self, src: str) -> str:
        lines = [
            "# === Recipe: Webfilter / URL block ===",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        if src:
            lines.append(f"# filter client {src} via flow if needed")
        lines += [
            "diagnose debug application urlfilter -1",
            "diagnose debug application ftgd -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        lines += [
            "",
            "# rating test (replace URL)",
            "# diagnose test application urlfilter 3",
        ]
        return "\n".join(lines)

    def _ips_utm(self, src: str, dst: str) -> str:
        lines = [
            "# === Recipe: IPS / UTM hit ===",
            "# ⚠ дуже шумно — коротко і з фільтром",
            "",
            "diagnose ips filter status",
            "diagnose ips av stats",
        ]
        if src:
            lines.append(f"diagnose ips filter set src {src}")
        if dst:
            lines.append(f"diagnose ips filter set dst {dst}")
        lines.append("")
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose ips debug enable all",
            "diagnose debug enable",
            "",
            "# --- stop ---",
            "diagnose ips debug disable",
        ]
        lines.extend(epilogue(stop=True))
        return "\n".join(lines)

    def _explicit_proxy(self, src: str) -> str:
        lines = [
            "# === Recipe: Explicit proxy ===",
            "",
            "diagnose wad session list",
            "diagnose wad worker policy list",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose debug application wad -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        if src:
            lines += ["", f"# client filter hint: {src}"]
        return "\n".join(lines)

    def _wireless(self) -> str:
        lines = [
            "# === Recipe: Wireless AP / client ===",
            "",
            "diagnose wireless-controller wlac -c wtp",
            "diagnose wireless-controller wlac -c sta",
            "diagnose wireless-controller wlac -c vap",
            "get wireless-controller wtp-status",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose debug application cw_acd -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        return "\n".join(lines)

    def _lacp(self, iface: str) -> str:
        lines = [
            "# === Recipe: LACP / aggregate ===",
            "",
            "diagnose netlink aggregate list",
        ]
        if iface and iface != "any":
            lines.append(f"diagnose netlink aggregate name {iface}")
            lines.append(f"get hardware nic {iface}")
        else:
            lines.append("# diagnose netlink aggregate name <agg>")
        lines += [
            "diagnose netlink interface list",
            "get system interface physical",
        ]
        return "\n".join(lines)

    def _interface(self, iface: str) -> str:
        lines = [
            "# === Recipe: Interface / link down ===",
            "",
            "get system interface physical",
            "diagnose ip address list",
            "diagnose netlink interface list",
            "diagnose hardware deviceinfo nic",
        ]
        if iface and iface != "any":
            lines.append(f"get hardware nic {iface}")
            lines.append(f"diagnose hardware deviceinfo nic {iface}")
        return "\n".join(lines)

    def _npu(self) -> str:
        return "\n".join(
            [
                "# === Recipe: NPU / offload check ===",
                "# ASIC-dependent — перевір ? на моделі",
                "",
                "diagnose hardware cpuinfo",
                "diagnose hardware meminfo",
                "get hardware npu np6 port-list",
                "diagnose npu np6 port-list",
                "diagnose npu np6 session-stats 0",
                "# session list: шукай npu / no_ofld_reason",
                "diagnose sys session filter clear",
                "diagnose sys session list",
            ]
        )

    def _certificate(self) -> str:
        return "\n".join(
            [
                "# === Recipe: Certificate / SSL inspect ===",
                "",
                "get vpn certificate local",
                "get vpn certificate ca",
                "get vpn certificate crl",
                "diagnose test application ssl 99",
                "",
                "# deep inspection issues often need flow + ssl debug",
            ]
            + list(preamble(reset=True, timestamps=True))
            + [
                "diagnose debug application ssl -1",
                "diagnose debug enable",
            ]
            + list(epilogue(stop=True))
        )

    def _fortiguard(self) -> str:
        return "\n".join(
            [
                "# === Recipe: FortiGuard / license ===",
                "",
                "get system status",
                "diagnose autoupdate status",
                "diagnose autoupdate versions",
                "get system fortiguard-service status",
                "execute update-now",
                "# DNS to FortiGuard",
                "execute ping update.fortiguard.net",
            ]
        )

    def _log_disk(self) -> str:
        return "\n".join(
            [
                "# === Recipe: Log disk / crashlog ===",
                "",
                "get system status",
                "diagnose sys logdisk usage",
                "diagnose hardware deviceinfo disk",
                "diagnose debug crashlog read",
                "execute log filter dump",
                "# storage free",
                "diagnose sys flash list",
            ]
        )

    def _ntp(self) -> str:
        return "\n".join(
            [
                "# === Recipe: NTP / time sync ===",
                "",
                "get system status",
                "diagnose sys ntp status",
                "execute time",
                "# config system ntp — перевірити servers",
            ]
        )

    def _ipv6(self, src: str, dst: str) -> str:
        lines = [
            "# === Recipe: IPv6 connectivity ===",
            "",
            "diagnose ipv6 address list",
            "diagnose ipv6 neighbor-cache list",
            "get router info6 routing-table",
            "diagnose firewall proute6 list",
            "",
            "diagnose sys session6 filter clear",
        ]
        if src:
            lines.append(f"diagnose sys session6 filter src {src}")
        if dst:
            lines.append(f"diagnose sys session6 filter dst {dst}")
        lines.append("diagnose sys session6 list")
        lines.append("")
        lines.extend(preamble(reset=True, clear_flow_filter=True, timestamps=True))
        if src:
            lines.append(f"diagnose debug flow filter saddr {src}")
        if dst:
            lines.append(f"diagnose debug flow filter daddr {dst}")
        lines += [
            "diagnose debug flow show function-name enable",
            "diagnose debug enable",
            "diagnose debug flow trace start6 50",
        ]
        lines.extend(epilogue(stop=True))
        return "\n".join(lines)

    def _multicast(self, iface: str) -> str:
        return "\n".join(
            [
                "# === Recipe: Multicast ===",
                "",
                "get router info multicast",
                "diagnose ip multicast list",
                "diagnose netlink interface list",
                f"diagnose sniffer packet {iface} 'ip multicast' 4 0 l",
            ]
        )
