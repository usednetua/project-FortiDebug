"""Recipes / Workflows — incident playbooks for FortiGate debug."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab
from core.fortios_version import (
    DEFAULT_VERSION,
    ike_log_filter_clear,
    ike_filter_remote_peer,
    ike_filter_name,
    sdwan_cmd,
    sdwan_service_cmd,
    version_banner,
)
from core.safety import preamble, epilogue
from ui.widgets.tooltip import tip


class RecipesTab(BaseTab):
    RECIPES = [
        "First steps connectivity",
        "Traffic not passing",
        "VPN down / rekey",
        "Dial-up IPsec",
        "SSL VPN login fail",
        "SD-WAN member dead",
        "High CPU",
        "High memory / conserv mode",
        "Session table full",
        "Policy / NAT check",
        "VIP / port forward",
        "Local-in / admin access",
        "HA out-of-sync",
        "OSPF neighbor down",
        "BGP neighbor down",
        "Static route / RIB",
        "DHCP no lease",
        "Auth / FSSO",
        "DNS issues",
        "Webfilter / URL block",
        "IPS / UTM hit",
        "Explicit proxy",
        "Wireless AP / client",
        "LACP / aggregate",
        "Interface / link down",
        "NPU / offload check",
        "Certificate / SSL inspect",
        "FortiGuard / license",
        "Log disk / crashlog",
        "NTP / time sync",
        "IPv6 connectivity",
        "Multicast",
    ]

    def __init__(self, master, on_change=None, get_version=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self.get_version = get_version or (lambda: DEFAULT_VERSION)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(
            self, text="Recipes / Workflows", font=ctk.CTkFont(size=18, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 8))

        ctk.CTkLabel(
            self,
            text=f"{len(self.RECIPES)} playbooks — заповни поля де потрібно → Copy / Export",
            text_color="gray",
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 8))

        ctk.CTkLabel(self, text="Scenario").grid(row=2, column=0, sticky="w", padx=10, pady=4)
        self.recipe = ctk.CTkOptionMenu(
            self, values=self.RECIPES, command=lambda _: self.notify_change(), width=280
        )
        self.recipe.set(self.RECIPES[0])
        self.recipe.grid(row=2, column=1, sticky="ew", padx=10, pady=4)
        tip(self.recipe, "Типові інциденти FortiGate")

        ctk.CTkLabel(self, text="Source / Client IP").grid(row=3, column=0, sticky="w", padx=10, pady=4)
        self.src = ctk.CTkEntry(self, placeholder_text="optional")
        self.src.grid(row=3, column=1, sticky="ew", padx=10, pady=4)
        self.src.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Destination / VIP").grid(row=4, column=0, sticky="w", padx=10, pady=4)
        self.dst = ctk.CTkEntry(self, placeholder_text="optional")
        self.dst.grid(row=4, column=1, sticky="ew", padx=10, pady=4)
        self.dst.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Port").grid(row=5, column=0, sticky="w", padx=10, pady=4)
        self.port = ctk.CTkEntry(self, placeholder_text="optional")
        self.port.grid(row=5, column=1, sticky="ew", padx=10, pady=4)
        self.port.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Peer / Phase1 / Neighbor").grid(
            row=6, column=0, sticky="w", padx=10, pady=4
        )
        self.peer = ctk.CTkEntry(self, placeholder_text="IP or name")
        self.peer.grid(row=6, column=1, sticky="ew", padx=10, pady=4)
        self.peer.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Interface").grid(row=7, column=0, sticky="w", padx=10, pady=4)
        self.wan = ctk.CTkEntry(self, placeholder_text="wan1 / any / port1")
        self.wan.grid(row=7, column=1, sticky="ew", padx=10, pady=4)
        self.wan.bind("<KeyRelease>", self.notify_change)

        self.grid_columnconfigure(1, weight=1)

    def generate_commands(self) -> str:
        name = self.recipe.get()
        src = self.src.get().strip()
        dst = self.dst.get().strip()
        port = self.port.get().strip()
        peer = self.peer.get().strip()
        iface = self.wan.get().strip() or "any"
        version = self.get_version()

        dispatch = {
            "First steps connectivity": lambda: self._first_steps(src, dst, port),
            "Traffic not passing": lambda: self._traffic_not_passing(src, dst, port),
            "VPN down / rekey": lambda: self._vpn_down(version, peer),
            "Dial-up IPsec": lambda: self._dialup_ipsec(version, peer, src),
            "SSL VPN login fail": lambda: self._ssl_login_fail(src),
            "SD-WAN member dead": lambda: self._sdwan_dead(version),
            "High CPU": self._high_cpu,
            "High memory / conserv mode": self._high_memory,
            "Session table full": self._session_full,
            "Policy / NAT check": lambda: self._policy_nat(src, dst, port),
            "VIP / port forward": lambda: self._vip(src, dst, port, iface),
            "Local-in / admin access": lambda: self._local_in(src, iface),
            "HA out-of-sync": self._ha_sync,
            "OSPF neighbor down": self._ospf,
            "BGP neighbor down": lambda: self._bgp(peer),
            "Static route / RIB": lambda: self._routing(dst),
            "DHCP no lease": lambda: self._dhcp(iface),
            "Auth / FSSO": self._auth_fsso,
            "DNS issues": lambda: self._dns(src, dst),
            "Webfilter / URL block": lambda: self._webfilter(src),
            "IPS / UTM hit": lambda: self._ips_utm(src, dst),
            "Explicit proxy": lambda: self._explicit_proxy(src),
            "Wireless AP / client": self._wireless,
            "LACP / aggregate": lambda: self._lacp(iface),
            "Interface / link down": lambda: self._interface(iface),
            "NPU / offload check": self._npu,
            "Certificate / SSL inspect": self._certificate,
            "FortiGuard / license": self._fortiguard,
            "Log disk / crashlog": self._log_disk,
            "NTP / time sync": self._ntp,
            "IPv6 connectivity": lambda: self._ipv6(src, dst),
            "Multicast": lambda: self._multicast(iface),
        }
        fn = dispatch.get(name)
        return fn() if fn else "# select a recipe"

    # ----- helpers -----

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

    # ----- recipes -----

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
        lines += [
            "",
            "# 5) Policy lookup (заповни sport/proto/intf)",
            "# diagnose firewall iprope lookup <src> <sport> <dst> <dport> <proto> <intf>",
        ]
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

    def _sdwan_dead(self, version) -> str:
        return "\n".join(
            [
                version_banner(version, "SD-WAN prefix"),
                "# === Recipe: SD-WAN member dead ===",
                "",
                sdwan_cmd(version, "health-check"),
                sdwan_cmd(version, "member"),
                sdwan_service_cmd(version),
                sdwan_cmd(version, "zone"),
                "",
                "diagnose ip address list",
                "get router info routing-table all",
                "diagnose sys link-monitor status",
            ]
        )

    def _high_cpu(self) -> str:
        return "\n".join(
            [
                "# === Recipe: High CPU ===",
                "",
                "get system performance status",
                "diagnose sys top 5 30",
                "diagnose sys top-mem",
                "diagnose sys session full-stat",
                "diagnose hardware cpuinfo",
                "diagnose debug crashlog read",
                "diagnose sys mpstat 1 5",
            ]
        )

    def _high_memory(self) -> str:
        return "\n".join(
            [
                "# === Recipe: High memory / conserv mode ===",
                "",
                "get system performance status",
                "diagnose hardware meminfo",
                "diagnose sys top-mem",
                "diagnose sys session full-stat",
                "diagnose sys confcache status",
                "# conserv mode thresholds",
                "get system global | grep -i conserv",
                "diagnose sys flush app-cache",
                "# ⚠ flush only if known safe in change window",
            ]
        )

    def _session_full(self) -> str:
        return "\n".join(
            [
                "# === Recipe: Session table full ===",
                "",
                "diagnose sys session full-stat",
                "diagnose sys session stat",
                "get system performance status",
                "diagnose firewall statistic show",
                "# top talkers (filter carefully on production)",
                "diagnose sys session filter clear",
                "diagnose sys session list | grep -c proto",
            ]
        )

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

    def _ha_sync(self) -> str:
        lines = [
            "# === Recipe: HA out-of-sync ===",
            "",
            "get system ha status",
            "diagnose sys ha status",
            "diagnose sys ha checksum cluster",
            "diagnose sys ha checksum global",
            "diagnose sys ha checksum root",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        lines += ["diagnose debug application hasync -1", "diagnose debug enable"]
        lines.extend(epilogue(stop=True))
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
