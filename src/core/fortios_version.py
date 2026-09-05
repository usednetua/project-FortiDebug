"""FortiOS version helpers and verified syntax differences.

Sources (Fortinet Community + docs):
- From FortiOS 7.4.1: 'diagnose vpn ike log-filter' -> 'diagnose vpn ike log filter'
- From 7.4.1: dst-addr4 -> rem-addr4, src-addr4 -> loc-addr4

Wireless (wlac) core list commands (-c wtp/sta/vap) are stable across 6.4–7.6;
always prefer selector notes + '?' on device for model-specific options.

NPU CLI is primarily hardware-family (np6/np7/…) rather than FortiOS minor,
but availability still depends on platform + FortiOS build.
"""

from enum import Enum


class FortiOSVersion(str, Enum):
    V6_0 = "6.0"
    V6_2 = "6.2"
    V6_4 = "6.4"
    V7_0 = "7.0"
    V7_2 = "7.2"
    V7_4 = "7.4"
    V7_6 = "7.6"
    V8_0 = "8.0"


DEFAULT_VERSION = FortiOSVersion.V7_4

VERSION_LABELS = {
    FortiOSVersion.V6_0: "6.0.x",
    FortiOSVersion.V6_2: "6.2.x",
    FortiOSVersion.V6_4: "6.4.x",
    FortiOSVersion.V7_0: "7.0.x",
    FortiOSVersion.V7_2: "7.2.x",
    FortiOSVersion.V7_4: "7.4.x",
    FortiOSVersion.V7_6: "7.6.x",
    FortiOSVersion.V8_0: "8.0.x",
}

_VERSION_ORDER = list(FortiOSVersion)


def parse_version(s: str) -> FortiOSVersion:
    s = (s or "").strip()
    for v in FortiOSVersion:
        if s.startswith(v.value) or s == VERSION_LABELS[v]:
            return v
    return DEFAULT_VERSION


def version_gte(current: FortiOSVersion, minimum: FortiOSVersion) -> bool:
    return _VERSION_ORDER.index(current) >= _VERSION_ORDER.index(minimum)


def uses_new_ike_filter_syntax(version: FortiOSVersion) -> bool:
    return version_gte(version, FortiOSVersion.V7_4)


def ike_log_filter_base(version: FortiOSVersion) -> str:
    if uses_new_ike_filter_syntax(version):
        return "diagnose vpn ike log filter"
    return "diagnose vpn ike log-filter"


def ike_log_filter_clear(version: FortiOSVersion) -> str:
    return f"{ike_log_filter_base(version)} clear"


def ike_filter_remote_peer(version: FortiOSVersion, ip: str) -> str:
    base = ike_log_filter_base(version)
    if uses_new_ike_filter_syntax(version):
        return f"{base} rem-addr4 {ip}"
    return f"{base} dst-addr4 {ip}"


def ike_filter_local_peer(version: FortiOSVersion, ip: str) -> str:
    base = ike_log_filter_base(version)
    if uses_new_ike_filter_syntax(version):
        return f"{base} loc-addr4 {ip}"
    return f"{base} src-addr4 {ip}"


def ike_filter_name(version: FortiOSVersion, name: str) -> str:
    return f"{ike_log_filter_base(version)} name {name}"


def ike_filter_interface(version: FortiOSVersion, index: str) -> str:
    """Filter by interface index (0 = all). Newer CLI may use ifindex."""
    base = ike_log_filter_base(version)
    if uses_new_ike_filter_syntax(version):
        return f"{base} ifindex {index}"
    return f"{base} interface {index}"


def flow_trace_start(count: str = "1000", ipv6: bool = False) -> str:
    if ipv6:
        return f"diagnose debug flow trace start6 {count}"
    return f"diagnose debug flow trace start {count}"


def session_prefix(ipv6: bool = False) -> str:
    return "diagnose sys session6" if ipv6 else "diagnose sys session"


def version_banner(version: FortiOSVersion, note: str = "") -> str:
    """Comment line for generated CLI — reminds operator of selected FortiOS."""
    label = VERSION_LABELS.get(version, version.value)
    extra = f" — {note}" if note else ""
    return f"# FortiOS {label}{extra}"


def wireless_version_note(version: FortiOSVersion) -> str:
    if version_gte(version, FortiOSVersion.V7_0):
        return "wlac -c/-d; перевіряй «diagnose wireless-controller wlac help»"
    return "wlac базові -c/-d; частина опцій може відрізнятись на 6.x"


def hardware_version_note(version: FortiOSVersion) -> str:
    return (
        "NPU CLI залежить від ASIC (np6/np7), не лише від FortiOS; "
        f"обрано {VERSION_LABELS.get(version, version.value)}"
    )
