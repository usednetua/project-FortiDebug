# FortiDebug Builder — Release 4 Plan

**Реліз:** **0.5.0** (+ polish)

---

## Статус (таблиця кроків)

| # | Крок | Стан | Пріоритет | Примітки |
|---|------|------|-----------|----------|
| 1 | Іконка `.ico` + `build.spec` | 🟡 Partial | P0 | `python scripts/generate_icon.py` |
| 2 | Tooltips | ✅ Done | P0 | Sniffer, Routing, SD-WAN, Ping, HA, … |
| 3 | Unit-тести Network / Policy | ✅ Done | P0 | |
| 4 | FortiOS version persist | ✅ Done | P1 | |
| 5 | Content area scroll | ✅ Done | P1 | |
| 6 | Wireless / CAPWAP | ✅ Done | P2 | + version selector |
| 7 | NPU / hardware | ✅ Done | P2 | + version selector |
| 8 | Recipe First steps | ✅ Done | P1 | |
| 9 | README / 0.5.0 | ✅ Done | P0 | |

---

## Version-aware (правило проєкту)

Глобальний селектор FortiOS обов’язковий для модулів із різним CLI (VPN/IKE, Recipes, Wireless, Hardware, SD-WAN). Нові вкладки — одразу `get_version`.

---

*Оновлено: 2026-09-05*
