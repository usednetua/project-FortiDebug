"""Core recipe helpers and original playbooks (subset; full set in artifacts)."""

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
    """Helpers + core recipes. Extended by RecipeExtraMixin."""

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

    def _session_block(self, src: str, dst: str, port: str) -> list:
        lines = ["diagnose sys session filter clear"]
        if src:
            lines.append(f"diagnose sys session filter src {src}")
        if dst:
            lines.append(f"diagnose sys session filter dst {dst}")
        if port:
            lines.append(f"diagnose sys session filter dport {port}")
        lines.append("diagnose sys session list")
        return lines

    def _flow_block(self, src: str, dst: str, port: str, count: str = "100") -> list:
        lines = list(preamble(reset=True, clear_flow_filter=True, timestamps=True))
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

    def _first_steps(self, src: str, dst: str, port: str) -> str:
        lines = [
            "# === Recipe: First steps connectivity ===",
            "# sniffer → session → flow → routing",
            "",
            "# 1) Sniffer",
            self._sniffer("any", src, dst, port),
            "",
            "# 2) Sessions",
        ]
        lines.extend(self._session_block(src, dst, port))
        lines += ["", "# 3) Debug flow"]
        lines.extend(self._flow_block(src, dst, port))
        lines += ["", "# 4) Routing"]
        lines.append(
            f"get router info routing-table details {dst}"
            if dst
            else "get router info routing-table all"
        )
        return "\n".join(lines)

    def _traffic_not_passing(self, src: str, dst: str, port: str) -> str:
        lines = ["# === Recipe: Traffic not passing ===", "", "# Sessions"]
        lines.extend(self._session_block(src, dst, port))
        lines += ["", "# Flow"]
        lines.extend(self._flow_block(src, dst, port, "200"))
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

    def _missing(self, name: str) -> str:
        return f"# Recipe '{name}' — full body pending restore (see artifacts/recipes_final.py)"

    def _dialup_ipsec(self, version, peer, src):
        return self._missing("Dial-up IPsec")

    def _ssl_login_fail(self, src):
        return self._missing("SSL VPN login fail")

    def _policy_nat(self, src, dst, port):
        return self._missing("Policy / NAT check")

    def _vip(self, src, dst, port, iface):
        return self._missing("VIP / port forward")

    def _local_in(self, src, iface):
        return self._missing("Local-in / admin access")

    def _ospf(self):
        return self._missing("OSPF neighbor down")

    def _bgp(self, peer):
        return self._missing("BGP neighbor down")

    def _routing(self, dst):
        return self._missing("Static route / RIB")

    def _dhcp(self, iface):
        return self._missing("DHCP no lease")

    def _auth_fsso(self):
        return self._missing("Auth / FSSO")

    def _dns(self, src, dst):
        return self._missing("DNS issues")

    def _webfilter(self, src):
        return self._missing("Webfilter / URL block")

    def _ips_utm(self, src, dst):
        return self._missing("IPS / UTM hit")

    def _explicit_proxy(self, src):
        return self._missing("Explicit proxy")

    def _wireless(self):
        return self._missing("Wireless AP / client")

    def _lacp(self, iface):
        return self._missing("LACP / aggregate")

    def _interface(self, iface):
        return self._missing("Interface / link down")

    def _npu(self):
        return self._missing("NPU / offload check")

    def _certificate(self):
        return self._missing("Certificate / SSL inspect")

    def _fortiguard(self):
        return self._missing("FortiGuard / license")

    def _log_disk(self):
        return self._missing("Log disk / crashlog")

    def _ntp(self):
        return self._missing("NTP / time sync")

    def _ipv6(self, src, dst):
        return self._missing("IPv6 connectivity")

    def _multicast(self, iface):
        return self._missing("Multicast")
