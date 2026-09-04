"""Recommended Fortinet debug safety preamble / epilogue.

Always: reset → clear filters → set filters → timestamp → enable → limit → stop+reset.
"""

from typing import List


def preamble(
    *,
    reset: bool = True,
    clear_flow_filter: bool = False,
    timestamps: bool = True,
    debug_info: bool = False,
) -> List[str]:
    lines: List[str] = []
    if reset:
        lines.append("diagnose debug reset")
    if clear_flow_filter:
        lines.append("diagnose debug flow filter clear")
    if debug_info:
        lines.append("diagnose debug info")
    if timestamps:
        lines.append("diagnose debug console timestamp enable")
    return lines


def epilogue(*, stop: bool = True) -> List[str]:
    if not stop:
        return []
    return [
        "",
        "# --- after test traffic: ---",
        "diagnose debug disable",
        "diagnose debug reset",
    ]
