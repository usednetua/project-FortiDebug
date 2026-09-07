# FortiDebug Builder — Alphabetical sort of menus & list fields

**Цільова версія:** 0.18.1 (patch UX)  
**Старт:** 2026-09-07

---

## Статус (таблиця кроків)

| # | Крок | Стан | Пріоритет | Примітки |
|---|------|------|-----------|----------|
| 1 | Інвентаризація всіх CTkOptionMenu / CTkComboBox / списків | ✅ Done | P0 | main_window, recipes, tabs |
| 2 | План виключень (числові рівні, версії FortiOS) | ✅ Done | P0 | див. нижче |
| 3 | Сортувати RECIPES (алфавіт, case-insensitive) | ⬜ Todo | P0 | recipes.py |
| 4 | Сортувати sidebar NAV (за поточним label / key) | ⬜ Todo | P0 | main_window.py |
| 5 | Сортувати текстові списки у вкладках | ⬜ Todo | P0 | app_debug, sessions, sniffer, flows, system_top, hardware, policy_lookup, vpn, ssh_logger, ping… |
| 6 | Sniffer BPF presets — алфавіт після «» | ⬜ Todo | P1 | _preset_names |
| 7 | CHANGELOG [Unreleased] / 0.18.1 | ⬜ Todo | P0 | перед комітом |
| 8 | Оновити doc/INDEX.md | ⬜ Todo | P0 | |
| 9 | Regression («не зламай!»): генерація команд, default values, i18n refresh | ⬜ Todo | P0 | |

---

## Детальні кроки

### 1–2. Scope і виключення

**Сортувати (алфавіт, case-insensitive, зазвичай `sorted(..., key=str.casefold)`):**
- Список recipes (`RecipesTab.RECIPES`)
- Sidebar navigation buttons (порядок кнопок за поточним `t(key)` або стабільним key)
- Daemon list (App Debug)
- Protocol lists (Sessions, Flows, Sniffer simple, Policy lookup)
- Interface presets (Sniffer ComboBox)
- System Top variants
- NPU family (Hardware)
- BPF preset names (після порожнього пункту)
- Flows presets (порожній перший, решта alpha)
- Shell options (SSH Logger) — за текстом
- Theme / Language values — за потреби

**НЕ сортувати / зберігати логічний порядок:**
- FortiOS version menu (`VERSION_LABELS` — хронологія 6.0 → 8.0)
- Числові рівні: Verbose 1–6, IKE debug level, App Debug level
- Timestamp none / a / l (сенсовий порядок)
- DF bit: default, yes, no
- Mode Realtime / Test

### 3. Recipes

`RECIPES = sorted([...], key=str.casefold)`  
Після сортування `self.recipe.set(self.RECIPES[0])` — перший алфавітний (не обов’язково «First steps…»).

### 4. Sidebar NAV

Варіант A (простий): відсортувати `NAV_KEYS` за `key` (стабільно, незалежно від мови).  
Варіант B: будувати кнопки в порядку `sorted(NAV_KEYS, key=lambda kv: t(kv[0]).casefold())` і перебудовувати / переставляти при `_refresh_ui_labels`.

Обрано **B** для справжнього алфавіту в UI (uk/en).

### 5–6. Вкладки

У кожному місці, де `values=list(...keys())` або літерал списку текстових опцій — застосувати `sorted(..., key=str.casefold)`.  
Для dict-based (PROTOCOLS, DAEMONS, VARIANTS, PRESETS) — сортувати keys при передачі в OptionMenu; dict порядок у Py3.7+ зберігається, але UI values — sorted list.

Sniffer `_preset_names`: `return [""] + sorted(self._all_presets().keys(), key=str.casefold)`.

### 7–9. Docs & regression

- CHANGELOG: секція Changed — alphabetical menus / lists.
- INDEX: додати цей план.
- Перевірити: default `.set(...)` існує в списку після сорту; dispatch recipes не залежить від порядку; i18n refresh не ламає nav order.

---

*Оновлено: 2026-09-07*
