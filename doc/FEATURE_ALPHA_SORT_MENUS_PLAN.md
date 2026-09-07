# FortiDebug Builder — Alphabetical sort of menus & list fields

**Цільова версія:** 0.18.1 (patch UX)  
**Старт:** 2026-09-07

---

## Статус (таблиця кроків)

| # | Крок | Стан | Пріоритет | Примітки |
|---|------|------|-----------|----------|
| 1 | Інвентаризація всіх CTkOptionMenu / CTkComboBox / списків | ✅ Done | P0 | main_window, recipes, tabs |
| 2 | План виключень (числові рівні, версії FortiOS) | ✅ Done | P0 | див. нижче |
| 3 | Сортувати RECIPES (алфавіт, case-insensitive) | ✅ Done | P0 | recipes.py |
| 4 | Сортувати sidebar NAV (за поточним label) | ✅ Done | P0 | main_window.py — rebuild on lang |
| 5 | Сортувати текстові списки у вкладках | ✅ Done | P0 | app_debug, sessions, sniffer, flows, system_top, hardware, policy_lookup, ssh_logger |
| 6 | Sniffer BPF presets — алфавіт після «» | ✅ Done | P1 | _preset_names |
| 7 | CHANGELOG [0.18.1] | ✅ Done | P0 | |
| 8 | Оновити doc/INDEX.md | ✅ Done | P0 | |
| 9 | Regression («не зламай!»): defaults, dispatch, i18n | ✅ Done | P0 | defaults у sorted lists; versions/levels не чіпали |

---

## Детальні кроки

### 1–2. Scope і виключення

**Сортувати (алфавіт, case-insensitive, `key=str.casefold`):**
- Список recipes (`RecipesTab.RECIPES`)
- Sidebar navigation buttons (порядок за `t(key)`, rebuild при зміні мови)
- Daemon list (App Debug)
- Protocol lists (Sessions, Flows, Sniffer simple, Policy lookup)
- Interface presets (Sniffer ComboBox)
- System Top variants
- NPU family (Hardware)
- BPF preset names (після порожнього пункту)
- Flows presets (порожній перший, решта alpha)
- Shell options (SSH Logger)
- Policy type / Auth type (з `(none)` першим)

**НЕ сортувати / зберігати логічний порядок:**
- FortiOS version menu (`VERSION_LABELS` — хронологія 6.0 → 8.0)
- Числові рівні: Verbose 1–6, IKE debug level, App Debug level
- Timestamp none / a / l
- DF bit: default, yes, no
- Mode Realtime / Test

### 3–6. Реалізація

Виконано в комітах на `main` (2026-09-07).

### 7–9. Docs & regression

- CHANGELOG 0.18.1, INDEX оновлено.
- Defaults (`.set(...)`) залишаються валідними після сорту; recipe dispatch за іменем, не за індексом.

---

*Оновлено: 2026-09-07*
