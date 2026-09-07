# FortiDebug Builder 0.18.2

**Дата:** 2026-09-07  
**Tag:** v0.18.2

## Highlights

- **Скрол колесом миші у випадаючих списках** — stock CustomTkinter OptionMenu/ComboBox не скролиться на довгих списках.

## Fixed

- **Скрол колесом миші у випадаючих списках** — stock CustomTkinter OptionMenu/ComboBox не скролиться на довгих списках.
  - Vendored [CTkScrollableDropdown](https://github.com/Akascape/CTkScrollableDropdown) (MIT, Akash Bora)
  - `wire_scrollable_dropdowns()` підключає scrollable popup до всіх меню після старту (`src/main.py`)
  - Helper: `src/ui/widgets/scrollable_menu.py`

## Install

- **Windows EXE:** вкладення `FortiDebugBuilder.exe` у цьому GitHub Release
- **З вихідників:**

```bash
pip install -r requirements.txt
python src/main.py
```

## Full changelog

Див. [CHANGELOG.md](CHANGELOG.md) — секція `[0.18.2]`.
