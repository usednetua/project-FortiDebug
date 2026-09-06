# FortiDebug Builder — Release 6 Plan

**Цільова версія:** 0.7.0  
**Старт:** 2026-09-06  
**Тема спринту:** відкриті (публічні) рецепти / playbooks, які ще не реалізовані в додатку

---

## Статус (таблиця кроків)

| # | Крок | Стан | Пріоритет | Примітки |
|---|------|------|-----------|----------|
| 0 | Gap-аналіз відкритих рецептів (огляд) | ✅ Done | P0 | 2026-09-06 |
| 1 | План Release 6 + INDEX + CHANGELOG | ✅ Done | P0 | |
| 2 | Mixin-структура (`recipe_r6.py`) | ✅ Done | P0 | `RecipeR6Mixin` |
| 3 | Recipe: **ADVPN / Shortcut tunnels** | ✅ Done | P0 | |
| 4 | Recipe: **SIP / VoIP / ALG** | ✅ Done | P0 | |
| 5 | Recipe: **Application Control / ISDB** | ✅ Done | P0 | |
| 6 | Recipe: **Email filter / Antispam** | ✅ Done | P1 | |
| 7 | Recipe: **File filter + DLP** | ✅ Done | P1 | combined |
| 8 | Recipe: **Transparent mode / Bridging** | ✅ Done | P1 | |
| 9 | Recipe: **Modem / LTE / PPP** | ✅ Done | P1 | |
| 10 | **VDOM-aware wrappers** | ✅ Done | P1 | UI field + session/flow `vd` |
| 11 | Regression «не зламай!» | ✅ Done | P0 | helpers backward-compatible (`vd=""`); headless tests |
| 12 | Тести (pytest) на нові генератори | ✅ Done | P1 | `tests/test_recipes_r6.py` |
| 13 | README + bump 0.7.0 + INDEX | ⬜ Todo | P0 | |

**Playbooks: 49** (42 + 3 P0 + 4 P1). VDOM — UI field, не окремий recipe.

---

## Критерії готовності Release 6

- [x] Мінімум 3 P0 recipes у UI і в dispatch  
- [x] P1: ≥2 з 5 (+ VDOM field)  
- [x] Helpers без breaking change (`vd` optional)  
- [x] `test_recipes_r6.py` додано  
- [ ] README + version 0.7.0  

---

## Залишок

1. **README** — згадати 49 recipes, R6 list, VDOM field  
2. **Bump 0.7.0** (about / package metadata якщо є)  
3. INDEX: після релізу статус R6 → Done / Архів  

P2 backlog (0.8.x): RIP, IS-IS, SSL web-mode, IoC pack, Automation Stitch, Cloud SDN.

---

*Оновлено: 2026-09-06*
