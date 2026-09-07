"""Attach scrollable (mouse-wheel) dropdowns to CTk OptionMenu / ComboBox.

Uses vendored CTkScrollableDropdown (Akascape, MIT) because stock CustomTkinter
dropdowns do not scroll reliably with the mouse wheel on long lists.
"""

from __future__ import annotations

from typing import Callable, Optional, Sequence

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
    - Store return value or use widget._scrollable_dropdown to update values later:
        widget._scrollable_dropdown.configure(values=new_list)
    """
    if values is None:
        try:
            values = list(widget.cget("values") or [])
        except Exception:
            values = []
    else:
        values = list(values)

    def _on_select(v: str) -> None:
        try:
            widget.set(v)
        except Exception:
            pass
        if command is not None:
            command(v)

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
