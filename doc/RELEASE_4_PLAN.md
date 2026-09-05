# FortiDebug Builder — Release 4 Plan

**Мета:** полірування продукту + розширені діагностики.

**Базова версія:** 0.4.1  
**Цільова версія:** 0.5.0

---

## Статус (таблиця кроків)

| # | Крок | Стан | Пріоритет | Примітки |
|---|------|------|-----------|----------|
| 1 | Іконка `.ico` + `build.spec` | 🟡 Partial | P0 | `scripts/generate_icon.py` + spec; запустити скрипт перед build |
| 2 | Tooltips на основних вкладках | 🟡 Partial | P0 | +Ping, HA; вже були Flows/Sessions/DHCP/… |
| 3 | Unit-тести Network / Policy lookup | ✅ Done | P0 | `cmd_builders` + `test_cmd_builders` |
| 4 | FortiOS version persist | ❌ Todo | P1 | |
| 5 | Content area scroll | ❌ Todo | P1 | |
| 6 | Wireless / CAPWAP | ❌ Todo | P2 | |
| 7 | NPU / hardware | ❌ Todo | P2 | |
| 8 | Recipe First steps connectivity | ❌ Todo | P1 | |
| 9 | README / CHANGELOG / 0.5.0 | 🟡 Partial | P0 | CHANGELOG updated |

**Легенда:** ✅ Done · 🟡 Partial · ❌ Todo

---

## Наступне

Етап B: persist FortiOS, scroll content, first-steps recipe.  
Перед EXE: `python scripts/generate_icon.py`

---

*Оновлено: 2026-09-05*
