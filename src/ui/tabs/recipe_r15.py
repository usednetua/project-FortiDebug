"""Release 15 — remote user connectivity (SSL VPN + dial-up IPsec deep dive)."""

from core.safety import preamble, epilogue


class RecipeR15Mixin:
    """Remote-access playbooks beyond login-only."""

    def _ssl_connected_no_traffic(self, src: str = "", dst: str = "", port: str = "") -> str:
        """Tunnel up, assigned IP OK, but inner traffic fails (policy/split/route)."""
        lines = [
            "# === Recipe: SSL VPN connected / no traffic ===",
            "# Login OK, tunnel up — no access to LAN / internet via tunnel",
            "# Check: ssl.root policy, split-tunnel destinations, route to pool, NAT",
            "",
            "get vpn ssl monitor",
            "diagnose vpn ssl list",
            "diagnose vpn ssl statistics",
            "get vpn ssl settings",
            "",
            "# Assigned client IP should appear here; note tunnel IP / ssl.root",
            "diagnose firewall auth list",
            "diagnose ip address list",
            "get router info routing-table all",
            "diagnose firewall proute list",
            "",
            "# Policy must have srcintf ssl.root (or ssl.<vdom>), user/group, correct dst",
            "# Split tunnel: portal destinations injected to client from policy dst",
            "# show vpn ssl web portal",
            "# show firewall policy",
            "",
        ]
        # Prefer assigned tunnel IP as src for session/flow if user put it in Source
        lines.extend(self._session_block(src, dst, port))
        lines.append("")
        lines.extend(self._flow_block(src, dst, port or "", "100"))
        lines += [
            "",
            "# Sniffer: use ASSIGNED SSL IP as host (FortiClient), not public WAN IP",
        ]
        if src and dst:
            lines.append(f"diagnose sniffer packet any 'host {src} and host {dst}' 4 0 l")
        elif src:
            lines.append(f"diagnose sniffer packet any 'host {src}' 4 0 l")
        elif dst:
            lines.append(f"diagnose sniffer packet any 'host {dst}' 4 0 l")
        else:
            lines.append("diagnose sniffer packet any 'host <assigned-ssl-ip>' 4 0 l")
        lines += [
            "",
            "# Common misses:",
            "# - no policy from ssl.root → LAN",
            "# - split tunnel dst does not include target subnet",
            "# - SSLVPN_TUNNEL_ADDR pool too wide → bad kernel routes on ssl.root",
            "# - missing route / blackhole for tunnel pool",
        ]
        return "\n".join(lines)

    def _dialup_inner_traffic(
        self, version, peer: str = "", src: str = "", dst: str = "", port: str = ""
    ) -> str:
        """IKE/XAuth up; phase2/selectors or policy block inner packets."""
        from core.fortios_version import (
            version_banner,
            ike_log_filter_clear,
            ike_filter_remote_peer,
            ike_filter_name,
        )

        lines = [
            version_banner(version, "IKE filter"),
            "# === Recipe: Dial-up IPsec up / inner traffic fail ===",
            "# Phase1/XAuth OK — no traffic to internal (selectors, policy, mode-cfg IP)",
            "",
            "diagnose vpn ike gateway list",
            "diagnose vpn tunnel list",
            "get vpn ipsec tunnel summary",
            "get vpn ipsec tunnel details",
            "",
            "# mode-cfg / internal IP assignment",
            "diagnose firewall auth list",
            "get router info routing-table all",
            "diagnose firewall proute list",
            "",
            "# Quick mode selectors must cover client↔dst; policy srcintf = tunnel",
            "# show vpn ipsec phase1-interface",
            "# show vpn ipsec phase2-interface",
            "",
        ]
        lines.extend(self._session_block(src, dst, port))
        lines.append("")
        lines.extend(self._flow_block(src, dst, port, "100"))
        lines.append("")
        lines.extend(preamble(reset=True, timestamps=True))
        lines.append(ike_log_filter_clear(version))
        if peer:
            if "." in peer and any(c.isdigit() for c in peer):
                lines.append(ike_filter_remote_peer(version, peer))
            else:
                lines.append(ike_filter_name(version, peer))
        elif src:
            lines.append(ike_filter_remote_peer(version, src))
        lines += [
            "diagnose debug application ike -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        lines += ["", "# Sniffer ESP/UDP 500/4500 on WAN + inner IP after decrypt"]
        if peer:
            lines.append(
                f"diagnose sniffer packet any 'host {peer} and (udp port 500 or udp port 4500 or proto 50)' 4 0 l"
            )
        if src and dst:
            lines.append(f"diagnose sniffer packet any 'host {src} and host {dst}' 4 0 l")
        elif src:
            lines.append(f"diagnose sniffer packet any 'host {src}' 4 0 l")
        return "\n".join(lines)

    def _ssl_realm_portal_group(self, src: str = "") -> str:
        lines = [
            "# === Recipe: SSL VPN realm / portal / group ===",
            "# Wrong portal, empty bookmarks, group not mapped, realm URL",
            "",
            "get vpn ssl settings",
            "get vpn ssl monitor",
            "diagnose vpn ssl list",
            "",
            "# Realms: /remote/login?realm=…  mapping portal ↔ group",
            "# show vpn ssl web portal",
            "# show vpn ssl web user-group-bookmark",
            "# show user group",
            "# Authentication rule order matters (first match)",
            "",
            "diagnose firewall auth list",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        if src:
            lines.append(f"diagnose vpn ssl debug-filter src-addr4 {src}")
            lines.append(f"# public client IP: {src}")
        lines += [
            "diagnose debug application sslvpn -1",
            "diagnose debug application fnbamd -1",
            "diagnose debug application authd -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        lines += [
            "",
            "# After connect: which portal/user/group?",
            "execute vpn sslvpn list",
            "diagnose vpn ssl list",
        ]
        if src:
            lines.append(
                f"diagnose sniffer packet any 'host {src} and (port 443 or port 10443)' 4 0 l"
            )
        return "\n".join(lines)

    def _ssl_dtls_mtu(self, src: str = "") -> str:
        lines = [
            "# === Recipe: SSL VPN DTLS / MTU / fragment ===",
            "# Tunnel flaps, slow apps, large packets drop, DTLS vs TLS fallback",
            "",
            "get vpn ssl settings",
            "get vpn ssl monitor",
            "diagnose vpn ssl list",
            "diagnose vpn ssl statistics",
            "",
            "# DTLS typically UDP 443; TLS TCP 443 — check which is negotiated",
            "# MTU / tcp-mss / fragment issues → path MTU, DF bit",
            "",
            "get system interface",
            "diagnose netlink interface list",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        if src:
            lines.append(f"diagnose vpn ssl debug-filter src-addr4 {src}")
        lines += [
            "diagnose debug application sslvpn -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        lines += ["", "# Capture control + tunnel"]
        if src:
            lines.append(
                f"diagnose sniffer packet any 'host {src} and (port 443 or port 10443)' 4 0 l"
            )
            lines.append(
                f"# verbose PCAP if needed: diagnose sniffer packet any 'host {src}' 6 100 l"
            )
        else:
            lines.append(
                "diagnose sniffer packet any 'port 443 or port 10443' 4 0 l"
            )
        lines += [
            "",
            "# Client-side: lower MTU on FortiClient / enable DTLS; FGT tcp-mss-adjust",
            "# config vpn ssl settings → dtls-tunnel, algorithm, idle-timeout",
        ]
        return "\n".join(lines)

    def _ssl_ip_pool(self, src: str = "") -> str:
        lines = [
            "# === Recipe: SSL VPN IP pool / wrong address ===",
            "# No IP / conflict / huge range → bogus routes on ssl.root",
            "",
            "get vpn ssl settings",
            "get vpn ssl monitor",
            "diagnose vpn ssl list",
            "",
            "# Tunnel IP range object (default SSLVPN_TUNNEL_ADDR1) must be tight",
            "# Portal IP pools must match settings — portal wins on conflict",
            "# show firewall address  # SSLVPN_TUNNEL_ADDR* / custom pools",
            "# show vpn ssl web portal",
            "",
            "diagnose ip address list",
            "get router info routing-table all",
            "diagnose ip route list",
            "",
            "# Oversized pool (e.g. 10.0.0.1–192.168.x.x) installs huge ssl.root routes",
            "# Temporary delete bad kernel route (example):",
            "# diagnose ip route delete ssl.root <net> <mask> 0.0.0.0 0",
            "# Then fix address object and reconnect clients",
            "",
            "diagnose firewall auth list",
            "diagnose firewall ippool list",
            "",
        ]
        if src:
            lines += [
                f"# client public IP {src}",
                f"diagnose sniffer packet any 'host {src} and port 443' 4 0 l",
            ]
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose debug application sslvpn -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        return "\n".join(lines)
