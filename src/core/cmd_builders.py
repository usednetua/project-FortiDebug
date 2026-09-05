"""Pure command builders (testable without GUI)."""

from typing import List, Optional

from core.fortios_version import FortiOSVersion, version_gte


def build_network_commands(
    *,
    arp_get: bool = False,
    arp_diag: bool = False,
    arp_clear: bool = False,
    ip_list: bool = False,
    nic_iface: Optional[str] = None,
    netlink: bool = False,
    agg_list: bool = False,
    agg_name: Optional[str] = None,
    nd6: bool = False,
) -> str:
    lines: List[str] = []
    if arp_get:
        lines.append("get system arp")
    if arp_diag:
        lines.append("diagnose ip arp list")
    if arp_clear:
        lines.append("# ⚠ clears entire ARP table")
        lines.append("execute clear system arp table")
    if ip_list:
        lines.append("diagnose ip address list")
    if nic_iface is not None:
        iface = nic_iface.strip()
        if iface:
            lines.append(f"get hardware nic {iface}")
        else:
            lines.append("# get hardware nic <interface> — set Interface field")
    if netlink:
        lines.append("diagnose netlink interface list")
    if agg_list:
        lines.append("diagnose netlink aggregate list")
    if agg_name is not None:
        name = agg_name.strip()
        if name:
            lines.append(f"diagnose netlink aggregate name {name}")
        else:
            lines.append("# diagnose netlink aggregate name <agg> — set Aggregate name")
    if nd6:
        lines.append("diagnose ipv6 neighbor-cache list")
    return "\n".join(lines) if lines else "# select options"


def build_policy_lookup(
    src: str,
    sport: str,
    dst: str,
    dport: str,
    proto: str,
    intf: str,
    *,
    version: Optional[FortiOSVersion] = None,
    pol_type: str = "",
    auth_type: str = "",
    user_or_group: str = "",
    auth_server: str = "",
) -> str:
    base = (
        f"diagnose firewall iprope lookup "
        f"{src.strip()} {sport.strip()} {dst.strip()} {dport.strip()} "
        f"{proto.strip()} {intf.strip()}"
    )
    # ≥7.4.1: optional pol_type activates extended policy-match mode
    if version is not None and version_gte(version, FortiOSVersion.V7_4):
        pt = pol_type.strip()
        if pt and pt != "(none)":
            parts = [base, pt]
            at = auth_type.strip()
            ug = user_or_group.strip()
            srv = auth_server.strip()
            if at and at != "(none)":
                parts.append(at)
                if ug:
                    parts.append(ug)
                    if srv:
                        parts.append(srv)
            return " ".join(parts)
    return base
