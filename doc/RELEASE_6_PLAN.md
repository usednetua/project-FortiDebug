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
| 10 | Recipe: **VDOM-aware wrappers** | ⬜ Todo | P1 | optional vd field |
| 11 | Regression «не зламай!» | ⬜ Todo | P0 | smoke 49 + helpers |
| 12 | Тести (pytest) на нові генератори | ⬜ Todo | P1 | |
| 13 | README + bump 0.7.0 + INDEX | ⬜ Todo | P0 | |

**Поточна кількість playbooks: 49** (42 + 3 P0 + 4 P1).

---

## Критерії готовності Release 6

- [x] Мінімум 3 P0 recipes у UI і в dispatch  
- [x] P1: щонайменше 2 з 5 (зроблено 4; лишився VDOM)  
- [ ] Жодної регресії на існуючих  
- [ ] CHANGELOG, INDEX, README оновлені (CHANGELOG/INDEX частково)  
- [ ] Теги / CI зелені (якщо pytest у workflow)

---

## Залишок

1. **VDOM** (крок 10) — optional поле / `vd` у filters  
2. **Regression** (11) — import RecipesTab, generate усі 49 без exception  
3. **pytest** (12) — unit на `_advpn` / `_sip_voip` / `_email_filter`  
4. **README + 0.7.0** (13)

P2 backlog (0.8.x): RIP, IS-IS, SSL web-mode, IoC pack, Automation Stitch, Cloud SDN.

---

*Оновлено: 2026-09-06*
