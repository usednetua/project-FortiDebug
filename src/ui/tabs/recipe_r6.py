"""Release 6 recipe expansion — open playbooks gap (ADVPN, SIP, App Control)."""

from core.fortios_version import (
    FortiOSVersion,
    version_gte,
    version_banner,
    sdwan_cmd,
    sdwan_service_cmd,
    ike_log_filter_clear,
    ike_filter_name,
    ike_filter_remote_peer,
)
from core.safety import preamble, epilogue


class RecipeR6Mixin:
    """P0 playbooks for Release 6: ADVPN, SIP/VoIP, Application Control / ISDB."""

    def _advpn(self, version, peer: str, iface: str, src: str, dst: str) -> str:
        lines = [
            version_banner(version, "ADVPN / Shortcut + SD-WAN"),
            "# === Recipe: ADVPN / Shortcut tunnels ===",
            "# Scope: ADVPN 1.0/2.0 with SD-WAN; verify shortcuts, health, IKE",
            "",
            "# --- IKE / tunnel status ---",
            "diagnose vpn ike gateway list",
            "diagnose vpn ike gateway summary",
            "diagnose vpn tunnel list",
            "diagnose vpn ike status",
            "",
            "# --- SD-WAN ADVPN ---",
            sdwan_cmd(version, "member"),
            sdwan_cmd(version, "health-check"),
            sdwan_service_cmd(version),
        ]
        if version_gte(version, FortiOSVersion.V7_0):
            lines += [
                sdwan_cmd(version, "advpn"),
                sdwan_cmd(version, "advpn-session"),
            ]
        else:
            lines.append(
                "# diagnose sys sdwan advpn / advpn-session — primarily 7.0+; "
                "on 6.x check virtual-wan-link + ike gateway"
            )
        lines += [
            "",
            "# --- link-monitor (often backs SD-WAN health) ---",
            "diagnose sys link-monitor status",
            "",
        ]
        if peer:
            lines.append(f"# peer / phase1 focus: {peer}")
            if "." in peer and any(c.isdigit() for c in peer):
                lines.append(f"# diagnose vpn ike gateway list | grep {peer}")
            else:
                lines.append(f"diagnose vpn ike gateway list name {peer}")

        lines.extend(preamble(reset=True, timestamps=True))
        lines.append(ike_log_filter_clear(version))
        if peer:
            if "." in peer and any(c.isdigit() for c in peer):
                lines.append(ike_filter_remote_peer(version, peer))
            else:
                lines.append(ike_filter_name(version, peer))
        lines += [
            "diagnose debug application ike -1",
            "diagnose debug application sdwan -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))

        if src or dst:
            lines += ["", "# --- optional flow for traffic over shortcut ---"]
            lines.extend(self._flow_block(src, dst, ""))

        if iface and iface != "any":
            lines += [
                "",
                f"# sniffer on overlay / underlay interface {iface}",
                self._sniffer(iface, src, dst, ""),
            ]
        return "\n".join(lines)

    def _sip_voip(self, src: str, dst: str, port: str, iface: str) -> str:
        sip_port = port or "5060"
        lines = [
            "# === Recipe: SIP / VoIP / ALG ===",
            "# One-way audio, call setup fail, missing pinholes / expected sessions",
            "",
            "# --- sessions (look for expected / pinhole UDP RTP) ---",
        ]
        lines.extend(self._session_block(src, dst, sip_port))
        lines += [
            "",
            "# broad session filter for SIP signaling",
            "diagnose sys session filter clear",
            f"diagnose sys session filter dport {sip_port}",
            "diagnose sys session list",
            "",
            "# helper / VoIP related (availability varies by version)",
            "diagnose sys session stat",
            "get system session-helper",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose debug application sip -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))

        sniffer_iface = iface if iface else "any"
        parts = [f"port {sip_port}"]
        if src:
            parts.insert(0, f"host {src}")
        if dst:
            parts.insert(0 if not src else 1, f"host {dst}")
        filt = " and ".join(parts)
        lines += [
            "",
            "# sniffer: SIP signaling",
            f"diagnose sniffer packet {sniffer_iface} '{filt}' 4 0 l",
            "",
            "# RTP is dynamic — after seeing SDP ports, re-run sniffer with those UDP ports",
            f"# diagnose sniffer packet {sniffer_iface} 'udp and port <rtp-port>' 4 0 l",
        ]
        if src or dst:
            lines += ["", "# flow for call setup"]
            lines.extend(self._flow_block(src, dst, sip_port, "150"))
        return "\n".join(lines)

    def _app_control(self, version, src: str, dst: str) -> str:
        lines = [
            version_banner(version, "Application Control / ISDB"),
            "# === Recipe: Application Control / ISDB ===",
            "# App-ctrl hits, internet-service, SD-WAN app-based steering",
            "",
            "# --- SD-WAN internet-service / app-ctrl cache ---",
        ]
        if version_gte(version, FortiOSVersion.V7_0):
            lines += [
                sdwan_cmd(version, "internet-service-app-ctrl-list"),
                "# diagnose sys sdwan internet-service-app-ctrl-list app-id <id>",
            ]
        else:
            lines.append(
                "# internet-service-app-ctrl-list — primarily 7.0+ SD-WAN; "
                "on 6.x use application control sensors + session UTM fields"
            )
        lines += [
            "",
            "# --- application / IPS related stats ---",
            "diagnose ips session list",
            "get application name status",
            "diagnose application list",
            "",
        ]
        lines.extend(self._session_block(src, dst, ""))
        lines += [""]
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose debug application ipsmonitor -1",
            "# optional: diagnose debug application urlfilter -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        if src or dst:
            lines += ["", "# flow to see app / ISDB decision"]
            lines.extend(self._flow_block(src, dst, ""))
        return "\n".join(lines)
