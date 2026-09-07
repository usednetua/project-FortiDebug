# FortiDebug Builder — Scrollable dropdowns (mouse wheel)

**Цільова версія:** 0.18.2  
**Старт:** 2026-09-07

---

## Статус (таблиця кроків)

| # | Крок | Стан | Пріоритет | Примітки |
|---|------|------|-----------|----------|
| 1 | Vendor CTkScrollableDropdown (Akascape, MIT) | ⬜ Todo | P0 | `src/ui/widgets/ctk_scrollable_dropdown.py` |
| 2 | Helper `attach_scrollable_menu()` | ⬜ Todo | P0 | set + user command; configure values |
| 3 | Підключити до Recipes (85) | ⬜ Todo | P0 | головний біль |
| 4 | Підключити до інших довгих OptionMenu/ComboBox | ⬜ Todo | P0 | daemons, protocols, presets, shells… |
| 5 | CHANGELOG + INDEX | ⬜ Todo | P0 | |
| 6 | Regression: select value, command fires, lang/theme menus | ⬜ Todo | P0 | |

---

## Контекст

Standard CustomTkinter `CTkOptionMenu` / `CTkComboBox` dropdown **не підтримує нормальний scroll колесом миші** для довгих списків (відомі issues #2135, #1610, #1990). Рекомендоване рішення спільноти — **CTkScrollableDropdown** (Akascape).

## Підхід

1. Vendor одного файлу (без pip-залежності), MIT license, attribution у header.
2. Helper:
   ```python
   def attach_scrollable_menu(widget, values=None, command=None, height=280, **kwargs):
       vals = list(values) if values is not None else list(widget.cget("values") or [])
       def _on_select(v):
           try:
               widget.set(v)
           except Exception:
               pass
           if command:
               command(v)
       dd = CTkScrollableDropdown(widget, values=vals, command=_on_select, height=height, justify="left", **kwargs)
       widget._scrollable_dropdown = dd
       return dd
   ```
3. Після `configure(values=…)` на widget — також `widget._scrollable_dropdown.configure(values=…)`.

## Не чіпати

- Числові короткі списки (verbose 1–6) — можна теж підключити для єдності, але не обов’язково.
- FortiOS version menu (8 пунктів) — ок з native або з scrollable.

---

*Оновлено: 2026-09-07*
