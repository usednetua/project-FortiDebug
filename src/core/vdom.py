"""VDOM mode helpers — multi-VDOM CLI context and filter syntax.

When multi-VDOM is enabled on FortiGate, most diagnose/get commands that are
VDOM-scoped should be run after:

    config vdom
    edit <vdom-name>

and closed with:

    end
    end

Some commands are **global-only** (HA cluster, NPU hardware, TAC report, …)
and must NOT be wrapped — they run outside any VDOM context.

Session / flow filters can also use numeric VDOM index:

    diagnose sys session filter vd <index>
    diagnose debug flow filter vd <index>
"""

from typing import List, Optional, Set

# Tabs whose output stays in global context even when VDOM mode is ON.
GLOBAL_SCOPE_TABS: Set[str] = {
    "ha",
    "system_top",
    "hardware",
    "tac",
}

# Recipe scenario names that are global-only (no config vdom wrap).
GLOBAL_SCOPE_RECIPES: Set[str] = {
    "HA out-of-sync",
    "NPU / offload check",
    "General TAC collect / healthcheck",
    "High CPU",
    "High memory / conserv mode",
    "Log disk / crashlog",
    "FortiGuard / license",
    "NTP / time sync",
    "Certificate / SSL inspect",  # cert store is global on multi-VDOM
}

SCOPE_GLOBAL = "global"
SCOPE_VDOM = "vdom"


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


def should_wrap_vdom(
    enabled: bool,
    tab_key: str = "",
    recipe_name: str = "",
    scope: str = "",
) -> bool:
    """Return True only when VDOM wrap is appropriate."""
    if not enabled:
        return False
    if (scope or "").strip().lower() == SCOPE_GLOBAL:
        return False
    if tab_key in GLOBAL_SCOPE_TABS:
        return False
    if recipe_name in GLOBAL_SCOPE_RECIPES:
        return False
    return True


def wrap_vdom_context(
    body: str,
    enabled: bool,
    name: str = "root",
    *,
    tab_key: str = "",
    recipe_name: str = "",
    scope: str = "",
) -> str:
    """Wrap generated command body in config vdom / edit / end when appropriate.

    Global-scope tabs/recipes keep the body unchanged (only a comment may be added
    by the caller).
    """
    if not should_wrap_vdom(enabled, tab_key, recipe_name, scope):
        return body
    if not (body or "").strip():
        return body
    stripped = body.lstrip()
    if stripped.startswith("config vdom"):
        return body
    parts = vdom_enter(name) + [body.rstrip("\n")] + vdom_leave()
    return "\n".join(parts)


def session_filter_vd_line(prefix: str, vd: str) -> Optional[str]:
    vd = (vd or "").strip()
    if not vd:
        return None
    return f"{prefix} filter vd {vd}"


def flow_filter_vd_line(filter_cmd: str, vd: str) -> Optional[str]:
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
    if name.lower() in ("root", ""):
        return "0"
    return ""


def vdom_banner(enabled: bool, name: str = "root", *, wrapped: bool = True) -> str:
    if not enabled:
        return "# VDOM mode: off (single / no multi-VDOM)"
    ctx = (name or "root").strip() or "root"
    if wrapped:
        return f"# VDOM mode: on — context '{ctx}'"
    return f"# VDOM mode: on — GLOBAL scope (no config vdom; active VDOM name '{ctx}' ignored)"
