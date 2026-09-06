"""Release 8 P2 recipes — RIP, SSL VPN web-mode."""

from core.safety import preamble, epilogue


class RecipeR8Mixin:
    """Release 8 playbooks (P2 backlog items)."""

    def _rip(self) -> str:
        lines = [
            "# === Recipe: RIP neighbor / routes ===",
            "# Neighbor not forming, routes missing from RIB",
            "",
            "get router info rip status",
            "get router info rip database",
            "get router info rip interface",
            "get router info routing-table rip",
            "get router info routing-table all",
            "",
            "# interface / network reachability for RIP (UDP 520)",
            "diagnose ip address list",
            "diagnose sniffer packet any 'udp port 520' 4 0 l",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose ip router rip all enable",
            "diagnose ip router rip level info",
            "diagnose debug enable",
            "",
            "# --- after test ---",
            "diagnose debug disable",
            "diagnose ip router rip all disable",
            "diagnose debug reset",
        ]
        return "\n".join(lines)

    def _ssl_web_mode(self, client_ip: str) -> str:
        lines = [
            "# === Recipe: SSL VPN web-mode ===",
            "# Portal bookmarks fail, RDP/HTTP rewrite, web mode only (not tunnel)",
            "",
            "get vpn ssl monitor",
            "diagnose vpn ssl list",
            "diagnose vpn ssl statistics",
            "",
            "# web-mode / portal related",
            "get vpn ssl settings",
            "# show vpn ssl web portal",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        if client_ip:
            lines.append(f"diagnose vpn ssl debug-filter src-addr4 {client_ip}")
        lines += [
            "diagnose debug application sslvpn -1",
            "diagnose debug application ssl -1",
            "diagnose debug application wad -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        lines += [
            "",
            "diagnose firewall auth list",
            "diagnose wad session list",
        ]
        if client_ip:
            lines += [
                "",
                f"# client {client_ip} — also check local-in / portal VIP",
                f"diagnose sniffer packet any 'host {client_ip} and (port 443 or port 10443)' 4 0 l",
            ]
        return "\n".join(lines)
