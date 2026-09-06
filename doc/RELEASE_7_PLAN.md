# FortiDebug Builder — Release 7 Plan

**Цільова версія:** 0.8.0  
**Старт:** 2026-09-06  
**Тема:** відновлення stub-рецептів + polish VDOM / global-only commands

---

## Статус (таблиця кроків)

| # | Крок | Стан | Пріоритет | Примітки |
|---|------|------|-----------|----------|
| 0 | План R7 + INDEX + CHANGELOG | ✅ Done | P0 | |
| 1 | Restore 24 stubs → `recipe_impl.py` | ✅ Done | P0 | |
| 2 | Smoke: жоден recipe не `pending restore` | ✅ Done | P0 | `test_no_stubs.py` |
| 3 | Global-only cmds без VDOM wrap | ✅ Done | P1 | tabs HA/Top/HW/TAC + recipes |
| 4 | VDOM name→index optional mapping (Settings) | ⬜ Todo | P2 | |
| 5 | P2 recipes (RIP / IS-IS / SSL web-mode / …) | ⬜ Todo | P2 | backlog |
| 6 | README + bump 0.8.0 + INDEX | ⬜ Todo | P0 | кінець спринту |

---

## Global scope (step 3)

**Tabs (never wrap):** `ha`, `system_top`, `hardware`, `tac`  
**Recipes (never wrap):** HA out-of-sync, High CPU/mem, NPU, TAC healthcheck, FortiGuard, NTP, Log disk, Certificate

При VDOM ON для цих сценаріїв: банер `# GLOBAL scope` без `config vdom`.

---

## Критерії

- [x] Усі `_missing` замінені  
- [x] Тест no stubs  
- [x] Global-scope carve-out  
- [ ] Version 0.8.0 + README  

---

*Оновлено: 2026-09-06*
