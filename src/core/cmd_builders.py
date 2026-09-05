"""Pure command builders (testable without GUI)."""

from typing import Iterable, List, Optional


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
) -> str:
    return (
        f"diagnose firewall iprope lookup "
        f"{src.strip()} {sport.strip()} {dst.strip()} {dport.strip()} "
        f"{proto.strip()} {intf.strip()}"
    )
