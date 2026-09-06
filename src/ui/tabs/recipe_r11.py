"""Release 11 recipes — BFD, SAML SSO."""

from core.safety import preamble, epilogue


class RecipeR11Mixin:
    """Release 11 playbooks."""

    def _bfd(self, peer: str = "") -> str:
        lines = [
            "# === Recipe: BFD neighbor ===",
            "# BFD session down, SD-WAN / static / BGP depend on BFD",
            "",
            "get router info bfd neighbor",
            "get router info bfd session",
            "# get router info bfd interface",
            "",
            "# often paired with static / BGP / SD-WAN",
            "get router info routing-table static",
            "get router info bgp summary",
            "",
        ]
        if peer:
            lines += [
                f"# peer focus: {peer}",
                f"# diagnose sniffer packet any 'host {peer} and udp port 3784' 4 0 l",
                f"# diagnose sniffer packet any 'host {peer} and udp port 4784' 4 0 l  # multi-hop",
            ]
        else:
            lines += [
                "diagnose sniffer packet any 'udp port 3784 or udp port 4784' 4 0 l",
            ]
        lines.append("")
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose ip router bfd all enable",
            "diagnose ip router bfd level info",
            "diagnose debug enable",
            "",
            "# --- after test ---",
            "diagnose debug disable",
            "diagnose ip router bfd all disable",
            "diagnose debug reset",
        ]
        return "\n".join(lines)

    def _saml_sso(self, src: str = "") -> str:
        lines = [
            "# === Recipe: SAML SSO / admin login ===",
            "# Admin SSO fail, SP metadata, IdP response, clock skew",
            "",
            "get system saml",
            "# show system saml",
            "get system status",
            "execute time",
            "# NTP must be OK for SAML assertions",
            "",
            "diagnose firewall auth list",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        if src:
            lines.append(f"# client / browser IP: {src}")
        lines += [
            "diagnose debug application samld -1",
            "diagnose debug application fnbamd -1",
            "diagnose debug application httpsd -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        lines += [
            "",
            "# Browser → FortiGate admin portal SSO; watch assertion errors in samld",
            "# Common: clock skew, ACS URL mismatch, cert, NameID",
        ]
        if src:
            lines.append(
                f"diagnose sniffer packet any 'host {src} and (port 443 or port 10443)' 4 0 l"
            )
        return "\n".join(lines)
