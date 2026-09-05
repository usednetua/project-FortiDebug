"""Release 5 recipe expansion (version-aware)."""

from core.fortios_version import FortiOSVersion, version_gte, version_banner
from core.safety import preamble, epilogue


class RecipeExtraMixin:
    """New playbooks: ZTNA, FAZ, WAD, DoS, auth, TAC, ARP, link-monitor, AV, QoS."""

    def _endpoint_list_cmd(self, version) -> str:
        """diagnose endpoint record list (pre-7.4.2) → ec-shm list (≥7.4.2)."""
        if version_gte(version, FortiOSVersion.V7_4):
            return "diagnose endpoint ec-shm list"
        return "diagnose endpoint record list"

    def _ztna(self, version, src: str, dst: str) -> str:
        lines = [
            version_banner(version, "ZTNA / Access Proxy"),
            "# === Recipe: ZTNA / Access Proxy ===",
            "# Scope: FortiOS 7.0+ (ZTNA introduced in 7.0)",
            "",
            "diagnose endpoint fctems test-connectivity",
            "diagnose test application fcnacd 2",
            "execute fctems verify",
            self._endpoint_list_cmd(version),
            "diagnose firewall dynamic list",
            "diagnose test application fcnacd 7",
            "diagnose test application fcnacd 8",
            "diagnose wad worker policy list",
            "",
        ]
        if not version_gte(version, FortiOSVersion.V7_0):
            lines.insert(2, "# ⚠ ZTNA requires FortiOS 7.0+; commands may be unavailable on 6.x")
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose debug application fcnacd -1",
            "diagnose endpoint filter show-large-data yes",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        lines += ["", "# WAD (Access Proxy path)"]
        lines.extend(preamble(reset=True, timestamps=True))
        if src:
            lines.append(f"diagnose wad filter src {src}")
        if dst:
            lines.append(f"diagnose wad filter dst {dst}")
        lines += [
            "diagnose wad debug enable category all",
            "diagnose wad debug enable level verbose",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        return "\n".join(lines)

    def _faz_logging(self) -> str:
        return "\n".join(
            [
                "# === Recipe: FortiAnalyzer / remote logging ===",
                "",
                "execute log fortianalyzer test-connectivity",
                "get log fortianalyzer setting",
                "get log setting",
                "",
                "# fgtlogd status (global / per-VDOM)",
                "diagnose test application fgtlogd 1",
                "diagnose test application fgtlogd 2",
                "diagnose test application fgtlogd 3",
                "diagnose test application fgtlogd 4",
                "diagnose test application fgtlogd 5",
                "",
                "# generate test log then re-check counters",
                "diagnose test log",
                "",
                "# live OFTP / log daemon",
            ]
            + list(preamble(reset=True, timestamps=True))
            + [
                "diagnose debug application fgtlogd 255",
                "diagnose debug application miglogd 255",
                "diagnose debug enable",
            ]
            + list(epilogue(stop=True))
            + [
                "",
                "# reachability",
                "execute ping",
                "# execute traceroute <FAZ-IP>",
            ]
        )

    def _wad(self, src: str, dst: str) -> str:
        lines = [
            "# === Recipe: WAD / Proxy engine ===",
            "# High CPU on wad / explicit proxy / ZTNA access-proxy",
            "",
            "diagnose test application wad 1000",
            "diagnose test application wad 2",
            "diagnose sys top 5 30",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        if src:
            lines.append(f"diagnose wad filter src {src}")
        if dst:
            lines.append(f"diagnose wad filter dst {dst}")
        lines += [
            "diagnose wad filter list",
            "diagnose wad debug enable category all",
            "diagnose wad debug enable level verbose",
            "diagnose wad debug display pid enable",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        lines += [
            "",
            "# clear filters after test",
            "diagnose wad filter clear",
            "diagnose wad debug disable",
        ]
        return "\n".join(lines)

    def _dos(self) -> str:
        return "\n".join(
            [
                "# === Recipe: DoS / Flood protection ===",
                "",
                "diagnose firewall dos-policy list",
                "diagnose sys session full-stat",
                "diagnose sys session stat",
                "get system performance status",
                "diagnose firewall statistic show",
                "diagnose hardware deviceinfo nic",
                "",
                "# anomaly / IPS sensors that often catch floods",
                "diagnose ips anomaly list",
                "diagnose ips session list",
            ]
        )

    def _user_auth(self, client_ip: str) -> str:
        lines = [
            "# === Recipe: User auth LDAP/RADIUS/TACACS ===",
            "",
            "diagnose firewall auth list",
            "diagnose test authserver ldap",
            "diagnose test authserver radius",
            "diagnose test authserver tacacs+",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose debug application fnbamd -1",
            "diagnose debug application authd -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        if client_ip:
            lines += [
                "",
                f"diagnose sniffer packet any 'host {client_ip} and (port 389 or port 636 or port 1812 or port 49)' 4 0 l",
            ]
        else:
            lines += [
                "",
                "diagnose sniffer packet any 'port 389 or port 636 or port 1812 or port 49' 4 0 l",
            ]
        return "\n".join(lines)

    def _tac_healthcheck(self) -> str:
        return "\n".join(
            [
                "# === Recipe: General TAC collect / healthcheck ===",
                "# Run while issue is present; attach full output to TAC ticket",
                "",
                "get system status",
                "get system performance status",
                "get hardware status",
                "diagnose hardware sys memory",
                "diagnose hardware sys conserve",
                "diagnose sys top 5 30",
                "diagnose sys top-mem",
                "diagnose sys session full-stat",
                "diagnose sys session stat",
                "diagnose debug crashlog read",
                "diagnose debug config-error-log read",
                "diagnose sys flash list",
                "diagnose sys logdisk usage",
                "get system ha status",
                "diagnose sys ha status",
                "diagnose ip address list",
                "get router info routing-table all",
                "diagnose netlink interface list",
                "",
                "execute tac report",
            ]
        )

    def _arp(self, iface: str) -> str:
        lines = [
            "# === Recipe: ARP / Neighbor ===",
            "",
            "get system arp",
            "diagnose ip arp list",
            "diagnose ipv6 neighbor-cache list",
            "diagnose netlink neighbor list",
        ]
        if iface and iface != "any":
            lines.append(f"diagnose sniffer packet {iface} 'arp' 4 0 l")
        else:
            lines.append("diagnose sniffer packet any 'arp' 4 0 l")
        return "\n".join(lines)

    def _link_monitor(self) -> str:
        return "\n".join(
            [
                "# === Recipe: Link-monitor / health-check ===",
                "",
                "diagnose sys link-monitor status",
                "diagnose sys link-monitor interface",
                "get system link-monitor",
                "diagnose netlink aggregate name",
                "get system interface physical",
                "diagnose ip address list",
            ]
        )

    def _antivirus(self, src: str, dst: str) -> str:
        lines = [
            "# === Recipe: Antivirus / AV engine ===",
            "",
            "get system status",
            "diagnose antivirus statistics",
            "diagnose test application avengine 1",
            "diagnose sys scanunit stats",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose debug application scanunitd -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        if src or dst:
            lines += ["", "# session filter for suspect hosts"]
            lines.extend(self._session_block(src, dst, ""))
        return "\n".join(lines)

    def _shaper(self) -> str:
        return "\n".join(
            [
                "# === Recipe: Traffic shaping / QoS ===",
                "",
                "diagnose firewall shaper traffic-shaper list",
                "diagnose firewall shaper per-ip-shaper list",
                "diagnose sys traffic-shaper",
                "get firewall shaper traffic-shaper",
                "get firewall shaper per-ip-shaper",
                "diagnose firewall statistic show",
            ]
        )
