"""Attach scrollable (mouse-wheel) dropdowns to CTk OptionMenu / ComboBox.

Uses vendored CTkScrollableDropdown (Akascape, MIT) because stock CustomTkinter
dropdowns do not scroll reliably with the mouse wheel on long lists.
"""

from __future__ import annotations

from typing import Callable, Optional, Sequence

import customtkinter as ctk

from ui.widgets.ctk_scrollable_dropdown import CTkScrollableDropdown


def attach_scrollable_menu(
    widget,
    values: Optional[Sequence[str]] = None,
    command: Optional[Callable[[str], None]] = None,
    height: int = 280,
    **kwargs,
) -> CTkScrollableDropdown:
    """Replace native dropdown of CTkOptionMenu/CTkComboBox with a scrollable one.

    - Selecting an item calls widget.set(value) and optional command(value).
    - If command is None, uses widget._command (CustomTkinter internal).
    - Access later via widget._scrollable_dropdown to update values:
        widget._scrollable_dropdown.configure(values=new_list)
    """
    if getattr(widget, "_scrollable_dropdown", None) is not None:
        return widget._scrollable_dropdown

    if values is None:
        try:
            values = list(widget.cget("values") or [])
        except Exception:
            values = []
    else:
        values = list(values)

    if command is None:
        command = getattr(widget, "_command", None)

    def _on_select(v: str) -> None:
        try:
            widget.set(v)
        except Exception:
            pass
        if command is not None:
            try:
                command(v)
            except TypeError:
                command()

    dd = CTkScrollableDropdown(
        widget,
        values=values,
        command=_on_select,
        height=height,
        justify="left",
        **kwargs,
    )
    try:
        widget._scrollable_dropdown = dd
    except Exception:
        pass
    return dd


def update_scrollable_values(widget, values: Sequence[str]) -> None:
    """Sync values on both the widget and its scrollable dropdown (if any)."""
    vals = list(values)
    try:
        widget.configure(values=vals)
    except Exception:
        pass
    dd = getattr(widget, "_scrollable_dropdown", None)
    if dd is not None:
        try:
            dd.configure(values=vals)
        except Exception:
            pass


def wire_scrollable_dropdowns(root, *, min_items: int = 1, height: int = 280) -> int:
    """Recursively attach scrollable dropdowns under root. Returns count attached."""
    count = 0

    def walk(w):
        nonlocal count
        try:
            children = w.winfo_children()
        except Exception:
            children = []
        for ch in children:
            walk(ch)
        if isinstance(w, (ctk.CTkOptionMenu, ctk.CTkComboBox)):
            try:
                vals = list(w.cget("values") or [])
            except Exception:
                return
            if len(vals) >= min_items:
                attach_scrollable_menu(w, values=vals, height=height)
                count += 1

    walk(root)
    return count
