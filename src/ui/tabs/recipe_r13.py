"""Release 13 recipes — EVPN, WebCache / WCCP."""

from core.safety import preamble, epilogue


class RecipeR13Mixin:
    """Release 13 playbooks."""

    def _evpn(self, peer: str = "") -> str:
        lines = [
            "# === Recipe: EVPN / VXLAN-EVPN ===",
            "# BGP EVPN neighbor, Type-2/3 routes, VTEP reachability",
            "",
            "get router info bgp summary",
            "get router info bgp neighbors",
            "get router info bgp network",
            "# EVPN address-family (syntax varies by FortiOS):",
            "# get router info bgp evpn",
            "# get router info bgp l2vpn evpn",
            "",
            "get system vxlan",
            "diagnose netlink brctl list",
            "diagnose netlink brctl name host root.b",
            "get system arp",
            "get router info routing-table all",
            "",
        ]
        if peer:
            lines += [
                f"# peer / VTEP {peer}",
                f"get router info bgp neighbors {peer}",
                f"diagnose sniffer packet any 'host {peer} and (tcp port 179 or udp port 4789)' 4 0 l",
                f"execute ping {peer}",
            ]
        else:
            lines.append(
                "diagnose sniffer packet any 'tcp port 179 or udp port 4789' 4 0 l"
            )
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

    def _webcache_wccp(self, src: str = "", dst: str = "") -> str:
        lines = [
            "# === Recipe: WebCache / WCCP ===",
            "# Cache miss/hit issues, WCCP assignment, transparent redirect",
            "",
            "get system status",
            "# show system wccp",
            "# show wanopt webcache",
            "# show wanopt cache-service",
            "",
            "diagnose wccp stats",
            "diagnose wccp status",
            "# diagnose test application wccpd",
            "",
            "diagnose wad worker policy list",
            "diagnose wad session list",
            "",
        ]
        lines.extend(self._session_block(src, dst, "80"))
        lines += [
            "",
            "diagnose sys session filter clear",
            "diagnose sys session filter dport 80",
            "diagnose sys session list",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose debug application wccpd -1",
            "diagnose debug application wad -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        lines += [
            "",
            "# WCCP control often GRE (proto 47) or UDP 2048 — platform dependent",
            "diagnose sniffer packet any 'proto 47 or udp port 2048 or port 80 or port 443' 4 0 l",
        ]
        if src or dst:
            lines += ["", "# flow"]
            lines.extend(self._flow_block(src, dst, "80"))
        return "\n".join(lines)
