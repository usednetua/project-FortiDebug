# FortiDebug Builder — Release 6 Plan

**Цільова версія:** 0.7.0  
**Старт:** 2026-09-06  
**Закрито:** 2026-09-06  
**Тема спринту:** відкриті (публічні) рецепти / playbooks + global VDOM mode

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
| 10 | **VDOM-aware** (field → global switch) | ✅ Done | P1 | sidebar switch + wrap |
| 11 | Regression «не зламай!» | ✅ Done | P0 | `vd=""` optional |
| 12 | Тести (pytest) | ✅ Done | P1 | `test_recipes_r6`, `test_vdom` |
| 13 | README + bump 0.7.0 + INDEX | ✅ Done | P0 | 2026-09-06 |

**Playbooks: 49.** Global VDOM mode у sidebar.

---

## Критерії готовності Release 6

- [x] Мінімум 3 P0 recipes у UI і в dispatch  
- [x] P1: ≥2 з 5 (+ VDOM)  
- [x] Helpers без breaking change  
- [x] Тести R6 / vdom  
- [x] README + version 0.7.0  

---

## Backlog → 0.8.x (Release 7)

1. Restore stubs з `artifacts/recipes_final.py` (повні тіла original playbooks)  
2. P2 recipes: RIP, IS-IS, SSL web-mode, IoC pack, Automation Stitch, Cloud SDN  
3. VDOM name→index mapping у Settings  
4. Не обгортати global-only команди при VDOM ON  
5. Тег `v0.7.0` + CI Release (за бажанням)

---

*Закрито: 2026-09-06*
