"""VDOM mode helpers — multi-VDOM CLI context and filter syntax.

When multi-VDOM is enabled on FortiGate, most diagnose/get commands that are
VDOM-scoped should be run after:

    config vdom
    edit <vdom-name>

and closed with:

    end
    end

Session / flow filters can also use numeric VDOM index:

    diagnose sys session filter vd <index>
    diagnose debug flow filter vd <index>
"""

from typing import List, Optional, Tuple


def vdom_enter(name: str) -> List[str]:
    name = (name or "root").strip() or "root"
    return [
        "# --- multi-VDOM context ---",
        "config vdom",
        f"edit {name}",
        "",
    ]


def vdom_leave() -> List[str]:
    return [
        "",
        "# --- leave VDOM ---",
        "end",
        "end",
    ]


def wrap_vdom_context(body: str, enabled: bool, name: str = "root") -> str:
    """Wrap generated command body in config vdom / edit / end when enabled."""
    if not enabled or not (body or "").strip():
        return body
    # Avoid double-wrap if body already starts with config vdom
    stripped = body.lstrip()
    if stripped.startswith("config vdom"):
        return body
    parts = vdom_enter(name) + [body.rstrip("\n")] + vdom_leave()
    return "\n".join(parts)


def session_filter_vd_line(prefix: str, vd: str) -> Optional[str]:
    """Return 'diagnose sys session[6] filter vd X' if vd non-empty."""
    vd = (vd or "").strip()
    if not vd:
        return None
    return f"{prefix} filter vd {vd}"


def flow_filter_vd_line(filter_cmd: str, vd: str) -> Optional[str]:
    """filter_cmd e.g. 'diagnose debug flow filter' or '... filter6'."""
    vd = (vd or "").strip()
    if not vd:
        return None
    return f"{filter_cmd} vd {vd}"


def resolve_vd_index(vdom_mode: bool, vdom_name: str, explicit_vd: str = "") -> str:
    """Prefer explicit field; if VDOM mode on and name looks like index, use it.

    FortiGate filter vd expects numeric index (0 = root typically).
    If name is non-numeric, return empty for filter (context edit uses name).
    """
    explicit = (explicit_vd or "").strip()
    if explicit:
        return explicit
    if not vdom_mode:
        return ""
    name = (vdom_name or "").strip()
    if name.isdigit():
        return name
    # common convention: root → 0
    if name.lower() in ("root", ""):
        return "0"
    return ""


def vdom_banner(enabled: bool, name: str = "root") -> str:
    if not enabled:
        return "# VDOM mode: off (single / no multi-VDOM)"
    return f"# VDOM mode: on — context '{(name or 'root').strip() or 'root'}'"
