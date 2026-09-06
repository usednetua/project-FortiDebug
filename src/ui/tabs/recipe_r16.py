"""Release 16 — WiFi / FortiAP / wireless-controller playbooks."""

from core.safety import preamble, epilogue


class RecipeR16Mixin:
    """WiFi and managed FortiAP diagnostics."""

    def _wifi_ap_offline(self, peer: str = "", iface: str = "") -> str:
        """peer = FortiAP serial or IP; iface = uplink toward APs."""
        lines = [
            "# === Recipe: FortiAP offline / CAPWAP join ===",
            "# AP not managed, discovery fail, DTLS/CAPWAP down",
            "",
            "get wireless-controller status",
            "get wireless-controller wtp-status",
            "diagnose wireless-controller wlac -c wtp",
            "diagnose wireless-controller wlac -d wtp",
            "diagnose wireless-controller wlac -c ws",
            "diagnose wireless-controller wlac -c vap",
            "",
            "# Discovery: DHCP option 138 / DNS / broadcast; UDP 5246 control, 5247 data",
            "diagnose sniffer packet any 'udp port 5246 or udp port 5247' 4 0 l",
            "",
        ]
        if iface and iface != "any":
            lines += [
                f"# FAP uplink interface {iface}",
                f"diagnose hardware deviceinfo nic {iface}",
                f"diagnose sniffer packet {iface} 'udp port 5246 or udp port 5247' 4 0 l",
            ]
        if peer:
            lines += [
                f"# focus AP serial/IP: {peer}",
                f"# diagnose wireless-controller wlac plain-ctl {peer} 1",
                f"# diagnose wireless-controller wlac wtp_filter {peer} 0-<AP-IP>:5246 2",
            ]
        lines.append("")
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose debug application cw_acd 0x7f",
            "# quieter alternative: diagnose debug application cw_acd -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        lines += [
            "",
            "diagnose debug crashlog read",
            "# On FortiAP CLI (if reachable): cw_diag -c all / cfg -s / fap-tech",
        ]
        return "\n".join(lines)

    def _wifi_client_assoc(self, peer: str = "", src: str = "") -> str:
        """peer or src can hold client MAC (aa:bb:…)."""
        mac = peer if peer and ":" in peer else (src if src and ":" in src else "")
        lines = [
            "# === Recipe: WiFi client cannot associate ===",
            "# No STA entry, rejected assoc, wrong SSID/security, radio down",
            "",
            "diagnose wireless-controller wlac -c sta",
            "diagnose wireless-controller wlac -d sta",
            "diagnose wireless-controller wlac -c vap",
            "diagnose wireless-controller wlac -c wtp",
            "get wireless-controller wtp-status",
            "",
        ]
        if mac:
            lines += [
                f"# client MAC {mac}",
                f"diagnose wireless-controller wlac sta_filter {mac} 2",
                "# level 1=basic, 2=handshake detail, up to 255=very verbose",
            ]
        else:
            lines += [
                "# diagnose wireless-controller wlac sta_filter <aa:bb:cc:dd:ee:ff> 2",
            ]
        lines.append("")
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose debug application cw_acd 0x7f",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        lines += [
            "",
            "# Clear filter after test:",
            "# diagnose wireless-controller wlac sta_filter 00:00:00:00:00:00 0",
        ]
        return "\n".join(lines)

    def _wifi_wpa_enterprise(self, peer: str = "", src: str = "") -> str:
        mac = peer if peer and ":" in peer else (src if ":" in (src or "") else "")
        lines = [
            "# === Recipe: WiFi 802.1X / WPA-Enterprise ===",
            "# EAP fail, RADIUS reject, dynamic VLAN, cert issues",
            "",
            "diagnose wireless-controller wlac -c sta",
            "diagnose wireless-controller wlac -c vap",
            "diagnose firewall auth list",
            "# show user radius / show user group",
            "",
        ]
        if mac:
            lines.append(f"diagnose wireless-controller wlac sta_filter {mac} 2")
        lines.append("")
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose debug application cw_acd 0x7f",
            "diagnose debug application fnbamd -1",
            "diagnose debug application radiusd -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        lines += [
            "",
            "# RADIUS path (replace server IP)",
            "diagnose sniffer packet any 'udp port 1812 or udp port 1813' 4 0 l",
        ]
        return "\n".join(lines)

    def _wifi_assoc_no_traffic(self, src: str = "", dst: str = "", port: str = "") -> str:
        lines = [
            "# === Recipe: WiFi associated / no traffic ===",
            "# STA up, IP missing or policy/DHCP/VLAN drop after L2",
            "",
            "diagnose wireless-controller wlac -c sta",
            "diagnose wireless-controller wlac -d sta",
            "diagnose firewall auth list",
            "execute dhcp lease-list",
            "",
            "# VAP → VLAN → policy; client IP in Source if known",
            "",
        ]
        lines.extend(self._session_block(src, dst, port))
        lines.append("")
        lines.extend(self._flow_block(src, dst, port or "", "100"))
        lines += [
            "",
            "# DHCP on client VLAN",
            "diagnose sniffer packet any 'port 67 or port 68' 4 0 l",
        ]
        if src:
            lines.append(f"diagnose sniffer packet any 'host {src}' 4 0 l")
        if dst:
            lines.append(f"diagnose sniffer packet any 'host {dst}' 4 0 l")
        return "\n".join(lines)

    def _wifi_roaming(self, peer: str = "") -> str:
        mac = peer if peer and ":" in peer else ""
        lines = [
            "# === Recipe: WiFi roaming / sticky client ===",
            "# Slow roam, sticky AP, 11k/v/r, signal thresholds",
            "",
            "diagnose wireless-controller wlac -c sta",
            "diagnose wireless-controller wlac -d sta",
            "diagnose wireless-controller wlac -c wtp",
            "get wireless-controller wtp-status",
            "",
            "# Note rId / wtp / rssi while client moves",
            "",
        ]
        if mac:
            lines += [
                f"# track STA {mac}",
                f"diagnose wireless-controller wlac sta_filter {mac} 2",
            ]
        lines.append("")
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose debug application cw_acd 0x7f",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        lines += [
            "",
            "# Compare RSSI / band steering / load-balance on neighboring WTPs",
            "# Client sticky often = good RSSI on far AP + aggressive roam disabled",
        ]
        return "\n".join(lines)

    def _wifi_rogue_wids(self) -> str:
        lines = [
            "# === Recipe: Rogue AP / WIDS ===",
            "# Rogue list growth, WIDS memory, false positives",
            "",
            "diagnose wireless-controller wlac -c ap-rogue",
            "diagnose wireless-controller wlac -c stats",
            "diagnose wireless-controller wlac -d usage",
            "get wireless-controller status",
            "",
            "# Large cw_wids_* / ap_rogue trees → high cw_acd memory",
            "diagnose sys top 2 20",
            "diagnose sys top-mem",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose debug application cw_acd 0x7f",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        lines += [
            "",
            "# Review WIDS profile / on-wire vs off-wire detection",
            "# show wireless-controller wids-profile",
        ]
        return "\n".join(lines)

    def _wifi_radio_rf(self, peer: str = "") -> str:
        lines = [
            "# === Recipe: Radio RF / channel check ===",
            "# Channel plan, power, band, DAC/interferer hints",
            "",
            "get wireless-controller status",
            "get wireless-controller wtp-status",
            "diagnose wireless-controller wlac -c wtp",
            "diagnose wireless-controller wlac -c vap",
            "diagnose wireless-controller wlac -c radio",
            "# diagnose wireless-controller wlac -c rf-analysis  # if present on build",
            "",
            "# Per-AP: operating channel, tx-power, band 2.4/5/6",
            "# show wireless-controller wtp-profile",
            "# show wireless-controller vap",
            "",
        ]
        if peer:
            lines.append(f"# AP focus {peer} — compare radio vs neighbors")
        lines += [
            "diagnose wireless-controller wlac -c stats",
            "",
            "# Spectrum / interferer usually needs FortiAP local tools or analyzer",
            "# On FAP: cw_diag rfinfo / channel survey (model-dependent)",
        ]
        return "\n".join(lines)

    def _wifi_cw_acd_load(self) -> str:
        lines = [
            "# === Recipe: cw_acd / controller load ===",
            "# cw_acd 99% CPU, high mem, scale multi-process",
            "",
            "diagnose sys top 2 30",
            "diagnose sys top-mem",
            "diagnose sys process pidof cw_acd",
            "",
            "get wireless-controller status",
            "diagnose wireless-controller wlac -c stats",
            "diagnose wireless-controller wlac -d usage",
            "diagnose wireless-controller wlac -c wtp",
            "diagnose wireless-controller wlac -c ap-rogue",
            "",
            "# Scale: config wireless-controller global → acd-process-count",
            "# Temporary: fnsysctl killall cw_acd  (APs rejoin)",
            "",
            "diagnose debug crashlog read",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "# Avoid long verbose cw_acd on already overloaded box",
            "diagnose debug application cw_acd 0x1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        return "\n".join(lines)
