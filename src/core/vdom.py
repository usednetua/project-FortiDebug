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

Optional **name→index map** (Settings / config.json `vdom_map`) resolves named
VDOMs to filter vd indices.
"""

from typing import Dict, List, Optional, Set

GLOBAL_SCOPE_TABS: Set[str] = {
    "ha",
    "system_top",
    "hardware",
    "tac",
}

GLOBAL_SCOPE_RECIPES: Set[str] = {
    "HA out-of-sync",
    "NPU / offload check",
    "General TAC collect / healthcheck",
    "High CPU",
    "High memory / conserv mode",
    "Log disk / crashlog",
    "FortiGuard / license",
    "NTP / time sync",
    "Certificate / SSL inspect",
}

SCOPE_GLOBAL = "global"
SCOPE_VDOM = "vdom"

DEFAULT_VDOM_MAP: Dict[str, str] = {
    "root": "0",
}


def normalize_vdom_map(raw) -> Dict[str, str]:
    """Return {lowercase_name: index_str} from config dict or text lines."""
    out: Dict[str, str] = {}
    if isinstance(raw, dict):
        for k, v in raw.items():
            name = str(k).strip()
            idx = str(v).strip()
            if name and idx:
                out[name.lower()] = idx
        return out
    if isinstance(raw, str):
        for line in raw.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                name, idx = line.split("=", 1)
            elif ":" in line:
                name, idx = line.split(":", 1)
            else:
                continue
            name, idx = name.strip(), idx.strip()
            if name and idx:
                out[name.lower()] = idx
    return out


def vdom_map_to_text(mapping: Dict[str, str]) -> str:
    if not mapping:
        return "root=0\n"
    lines = []
    items = sorted(mapping.items(), key=lambda kv: (0 if kv[0] == "root" else 1, kv[0]))
    for name, idx in items:
        lines.append(f"{name}={idx}")
    return "\n".join(lines) + "\n"


def _load_map_from_config() -> Dict[str, str]:
    try:
        from core.config import load_config

        return normalize_vdom_map(load_config().get("vdom_map") or {})
    except Exception:
        return {}


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


def resolve_vd_index(
    vdom_mode: bool,
    vdom_name: str,
    explicit_vd: str = "",
    name_map: Optional[Dict[str, str]] = None,
) -> str:
    """Resolve filter vd index.

    Priority:
      1. explicit_vd (UI override field)
      2. if VDOM mode off → empty
      3. if name is numeric → use as index
      4. name_map (or config vdom_map) lookup
      5. DEFAULT_VDOM_MAP (root→0)
      6. empty (context edit still uses the name)
    """
    explicit = (explicit_vd or "").strip()
    if explicit:
        return explicit
    if not vdom_mode:
        return ""
    name = (vdom_name or "").strip()
    if not name:
        name = "root"
    if name.isdigit():
        return name
    merged: Dict[str, str] = dict(DEFAULT_VDOM_MAP)
    if name_map is None:
        name_map = _load_map_from_config()
    if name_map:
        merged.update({k.lower(): str(v).strip() for k, v in name_map.items() if str(v).strip()})
    return merged.get(name.lower(), "")


def vdom_banner(enabled: bool, name: str = "root", *, wrapped: bool = True) -> str:
    if not enabled:
        return "# VDOM mode: off (single / no multi-VDOM)"
    ctx = (name or "root").strip() or "root"
    if wrapped:
        return f"# VDOM mode: on — context '{ctx}'"
    return f"# VDOM mode: on — GLOBAL scope (no config vdom; active VDOM name '{ctx}' ignored)"
