# FortiDebug Builder 0.18.2

**Дата:** 2026-09-07  
**Tag:** v0.18.2

## Highlights

- Скрол колесом миші у всіх довгих випадаючих списках (OptionMenu / ComboBox).
- Продовження UX-лінії 0.18.1 (алфавітне сортування меню).

## Fixed

- **Скрол колесом миші у випадаючих списках** — stock CustomTkinter OptionMenu/ComboBox не скролиться на довгих списках.
  - Vendored [CTkScrollableDropdown](https://github.com/Akascape/CTkScrollableDropdown) (MIT, Akash Bora)
  - `wire_scrollable_dropdowns()` підключає scrollable popup до всіх меню після старту (`src/main.py`)
  - Helper: `src/ui/widgets/scrollable_menu.py`

## Changed (процес, 2026-09-07)

- Обов’язок генерувати **`RELEASE_NOTES.md`** під кожен реліз і публікувати його разом із GitHub Release (EXE + нотатки + body).
- Правила зафіксовані в `AGENTS.md` §3; CI оновлено.

## Install

- **Windows EXE:** вкладення `FortiDebugBuilder.exe` у цьому Release (після CI на tag).
- **З вихідників:**

```bash
pip install -r requirements.txt
python src/main.py
```

## Full changelog

Див. [CHANGELOG.md](CHANGELOG.md) — секції `[0.18.2]`, `[0.18.1]`, `[0.18.0]`.
