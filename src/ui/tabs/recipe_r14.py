"""Release 14 recipes — LLDP/CDP, 802.1X, Captive portal."""

from core.safety import preamble, epilogue


class RecipeR14Mixin:
    """Release 14 playbooks."""

    def _lldp_cdp(self, iface: str = "") -> str:
        lines = [
            "# === Recipe: LLDP / CDP neighbors ===",
            "# Switch/peer not seen, lldp-reception off, cabling / role",
            "",
            "# Reception often enabled only on WAN-role by default",
            "# config system global / set lldp-reception enable",
            "# config system interface / edit <port> / set lldp-reception enable",
            "",
            "diagnose lldp config",
            "diagnose lldp rx neighbor",
            "diagnose lldp rx neighbor details",
            "diagnose lldp rx neighbor summary",
            "# older alias still seen on some builds:",
            "# diagnose lldprx neighbor",
            "# diagnose lldprx neighbor details",
            "",
            "diagnose user device list",
            "diagnose netlink interface list",
            "",
        ]
        if iface and iface != "any":
            lines += [
                f"# interface focus: {iface}",
                f"diagnose hardware deviceinfo nic {iface}",
                f"diagnose sniffer packet {iface} 'ether proto 0x88cc' 4 0 l",
            ]
        else:
            lines.append("diagnose sniffer packet any 'ether proto 0x88cc' 4 0 l")
        lines += [
            "",
            "# CDP is Cisco proprietary — not natively decoded like LLDP;",
            "# capture may still show ethertype 0x2000 on the wire if peer sends CDP",
            "# diagnose sniffer packet any '' 6 50 l   # then filter in Wireshark",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose debug application lldptx -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        return "\n".join(lines)

    def _dot1x(self, src: str = "", iface: str = "") -> str:
        lines = [
            "# === Recipe: 802.1X wired auth ===",
            "# Client not authorized, RADIUS reject, MAC-based vs port-based",
            "",
            "diagnose firewall auth list",
            "get system interface",
            "# show user group / show user radius",
            "",
            "# FGT as 802.1X authenticator (or supplicant on some ports)",
            "# diagnose test application fnbamd 1",
            "diagnose test application fnbamd",
            "",
        ]
        if iface and iface != "any":
            lines += [
                f"# port {iface}",
                f"diagnose hardware deviceinfo nic {iface}",
            ]
        lines.append("")
        lines.extend(preamble(reset=True, timestamps=True))
        if src:
            lines.append(f"# client {src}")
        lines += [
            "diagnose debug application fnbamd -1",
            "diagnose debug application radiusd -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        lines += [
            "",
            "# EAPOL ethertype 0x888e",
        ]
        if iface and iface != "any":
            lines.append(f"diagnose sniffer packet {iface} 'ether proto 0x888e' 4 0 l")
        else:
            lines.append("diagnose sniffer packet any 'ether proto 0x888e' 4 0 l")
        if src:
            lines.append(
                f"diagnose sniffer packet any 'host {src} and (udp port 1812 or udp port 1813)' 4 0 l"
            )
        return "\n".join(lines)

    def _captive_portal(self, src: str = "") -> str:
        lines = [
            "# === Recipe: Captive portal ===",
            "# Redirect loop, auth page not shown, session not authorized",
            "",
            "diagnose firewall auth list",
            "diagnose user device list",
            "# show user setting / captive-portal",
            "# show firewall policy  # authentication / portal enabled",
            "",
            "get system status",
            "diagnose sys session stat",
            "",
        ]
        lines.extend(self._session_block(src, "", "80"))
        lines += [
            "",
            "diagnose sys session filter clear",
            "diagnose sys session filter dport 80",
            "diagnose sys session list",
            "diagnose sys session filter clear",
            "diagnose sys session filter dport 443",
            "diagnose sys session list",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        if src:
            lines.append(f"# client {src}")
        lines += [
            "diagnose debug application fnbamd -1",
            "diagnose debug application httpsd -1",
            "diagnose debug application authd -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        if src:
            lines += [
                "",
                f"diagnose sniffer packet any 'host {src} and (port 80 or port 443)' 4 0 l",
            ]
            lines.extend(self._flow_block(src, "", "80"))
        else:
            lines += [
                "",
                "diagnose sniffer packet any 'port 80 or port 443' 4 0 l",
            ]
        return "\n".join(lines)
