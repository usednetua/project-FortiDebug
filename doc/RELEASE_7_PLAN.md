# FortiDebug Builder — Release 7 Plan

**Цільова версія:** 0.8.0  
**Старт:** 2026-09-06  
**Тема:** відновлення stub-рецептів + polish VDOM / global-only commands

---

## Статус (таблиця кроків)

| # | Крок | Стан | Пріоритет | Примітки |
|---|------|------|-----------|----------|
| 0 | План R7 + INDEX + CHANGELOG | ✅ Done | P0 | |
| 1 | Restore 24 stubs → `recipe_impl.py` | ✅ Done | P0 | з artifacts/recipes_final.py |
| 2 | Smoke: жоден recipe не повертає `pending restore` | ⬜ Todo | P0 | test_no_stubs |
| 3 | Global-only cmds без VDOM wrap (HA, system status…) | ⬜ Todo | P1 | |
| 4 | VDOM name→index optional mapping (Settings) | ⬜ Todo | P2 | |
| 5 | P2 recipes (RIP / IS-IS / SSL web-mode / …) | ⬜ Todo | P2 | backlog |
| 6 | README + bump 0.8.0 + INDEX | ⬜ Todo | P0 | кінець спринту |

---

## Критерії

- [x] Усі методи `_missing` замінені повними тілами  
- [ ] Тест: 49 recipes без «pending restore»  
- [ ] Version 0.8.0 + README  

---

*Оновлено: 2026-09-06*
