"""FortiOS version helpers and syntax differences."""

from enum import Enum


class FortiOSVersion(str, Enum):
    V6_4 = "6.4"
    V7_0 = "7.0"
    V7_2 = "7.2"
    V7_4 = "7.4"
    V7_6 = "7.6"
    V8_0 = "8.0"


# Default for new installs
DEFAULT_VERSION = FortiOSVersion.V7_4

VERSION_LABELS = {
    FortiOSVersion.V6_4: "6.4.x",
    FortiOSVersion.V7_0: "7.0.x",
    FortiOSVersion.V7_2: "7.2.x",
    FortiOSVersion.V7_4: "7.4.x",
    FortiOSVersion.V7_6: "7.6.x",
    FortiOSVersion.V8_0: "8.0.x",
}


def parse_version(s: str) -> FortiOSVersion:
    s = (s or "").strip()
    for v in FortiOSVersion:
        if s.startswith(v.value) or s == VERSION_LABELS[v]:
            return v
    return DEFAULT_VERSION


def version_gte(current: FortiOSVersion, minimum: FortiOSVersion) -> bool:
    order = list(FortiOSVersion)
    return order.index(current) >= order.index(minimum)


# --- Syntax helpers ---

def ike_log_filter_cmd(version: FortiOSVersion) -> str:
    """v7.4.1+ uses space: 'diagnose vpn ike log filter'
    older uses hyphen: 'diagnose vpn ike log-filter'
    """
    if version_gte(version, FortiOSVersion.V7_4):
        return "diagnose vpn ike log filter"
    return "diagnose vpn ike log-filter"


def ike_log_filter_clear(version: FortiOSVersion) -> str:
    return f"{ike_log_filter_cmd(version)} clear"


def flow_trace_start(version: FortiOSVersion, count: str = "1000", ipv6: bool = False) -> str:
    if ipv6:
        return f"diagnose debug flow trace start6 {count}"
    return f"diagnose debug flow trace start {count}"


def session_cmd_prefix(ipv6: bool = False) -> str:
    return "diagnose sys session6" if ipv6 else "diagnose sys session"
