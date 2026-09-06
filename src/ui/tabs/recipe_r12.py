"""Release 12 recipes — GRE, VXLAN, CGNAT."""

from core.safety import preamble, epilogue


class RecipeR12Mixin:
    """Release 12 playbooks."""

    def _gre_tunnel(self, peer: str = "", iface: str = "") -> str:
        tun = iface if iface and iface != "any" else ""
        lines = [
            "# === Recipe: GRE / IP-in-IP tunnel ===",
            "# Tunnel down, no route over GRE, proto 47 blocked",
            "",
            "get system interface",
            "diagnose netlink interface list",
            "diagnose ip address list",
            "get router info routing-table all",
            "",
        ]
        if tun:
            lines += [
                f"# tunnel interface focus: {tun}",
                f"diagnose hardware deviceinfo nic {tun}",
                f"diagnose sniffer packet {tun} '' 4 20 l",
            ]
        if peer:
            lines += [
                f"# remote peer {peer}",
                f"diagnose sniffer packet any 'host {peer} and (proto 47 or proto 4)' 4 0 l",
                f"execute ping {peer}",
            ]
        else:
            lines.append("diagnose sniffer packet any 'proto 47 or proto 4' 4 0 l")
        lines.append("")
        lines.extend(self._session_block("", peer, ""))
        lines.append("")
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "# GRE itself has little daemon debug; focus flow + sniffer",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        if peer:
            lines += ["", "# flow toward peer"]
            lines.extend(self._flow_block("", peer, ""))
        return "\n".join(lines)

    def _vxlan(self, peer: str = "", iface: str = "") -> str:
        lines = [
            "# === Recipe: VXLAN ===",
            "# VTEP down, no MAC learn, UDP 4789 filtered",
            "",
            "get system vxlan",
            "# show system vxlan",
            "diagnose netlink brctl list",
            "diagnose netlink brctl name host root.b",
            "get system arp",
            "diagnose ip arp list",
            "",
            "diagnose netlink interface list",
            "get router info routing-table all",
            "",
        ]
        if peer:
            lines += [
                f"# VTEP peer {peer}",
                f"diagnose sniffer packet any 'host {peer} and udp port 4789' 4 0 l",
                f"execute ping {peer}",
            ]
        else:
            lines.append("diagnose sniffer packet any 'udp port 4789' 4 0 l")
        if iface and iface != "any":
            lines += [
                f"# underlay / vxlan iface {iface}",
                f"diagnose hardware deviceinfo nic {iface}",
            ]
        lines.append("")
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose debug application lnkmtd -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        return "\n".join(lines)

    def _cgnat(self, src: str = "", dst: str = "") -> str:
        lines = [
            "# === Recipe: CGNAT / hyperscale session ===",
            "# Pool exhaustion, port block, hyperscale NP session",
            "",
            "diagnose firewall ippool list",
            "diagnose firewall ippool stats",
            "# diagnose firewall iprope list",
            "",
            "diagnose sys session stat",
            "diagnose sys session full-stat",
            "diagnose sys session list",
            "",
            "# hyperscale / NP (platform-dependent)",
            "diagnose npu np6lite session",
            "# diagnose npu np7 session",
            "get system performance status",
            "",
        ]
        lines.extend(self._session_block(src, dst, ""))
        lines.append("")
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "# CGNAT issues often visible in session + ippool only",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        if src or dst:
            lines += ["", "# flow"]
            lines.extend(self._flow_block(src, dst, ""))
        return "\n".join(lines)
