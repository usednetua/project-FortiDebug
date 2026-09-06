# FortiDebug Builder — Release 8 Plan

**Цільова версія:** 0.9.0  
**Старт:** 2026-09-06  
**Тема:** VDOM name→index mapping + P2 recipes (опційно)

---

## Статус (таблиця кроків)

| # | Крок | Стан | Пріоритет | Примітки |
|---|------|------|-----------|----------|
| 0 | План R8 + INDEX + CHANGELOG | ✅ Done | P0 | |
| 1 | `vdom_map` у config + `resolve_vd_index` | ✅ Done | P0 | auto-load from config |
| 2 | Settings UI: редактор mapping | ✅ Done | P0 | |
| 3 | Тести mapping | ✅ Done | P1 | |
| 4 | P2 recipe (мінімум 1–2) | ⬜ Todo | P2 | RIP / SSL web-mode … |
| 5 | README + bump 0.9.0 | ⬜ Todo | P0 | |

---

## VDOM map

Settings → текст:

```
root=0
vd-LAN=1
vd-DMZ=2
```

→ `config.json` `vdom_map`. Sessions/Flows/Recipes: `filter vd` через `resolve_vd_index`.

---

*Оновлено: 2026-09-06*
