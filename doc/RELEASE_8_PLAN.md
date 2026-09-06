# FortiDebug Builder — Release 8 Plan

**Цільова версія:** 0.9.0  
**Старт:** 2026-09-06  
**Тема:** VDOM name→index mapping + P2 recipes (опційно)

---

## Статус (таблиця кроків)

| # | Крок | Стан | Пріоритет | Примітки |
|---|------|------|-----------|----------|
| 0 | План R8 + INDEX + CHANGELOG | ✅ Done | P0 | |
| 1 | `vdom_map` у config + `resolve_vd_index` | 🔄 | P0 | name → filter vd index |
| 2 | Settings UI: редактор mapping | 🔄 | P0 | |
| 3 | Тести mapping | ⬜ | P1 | |
| 4 | P2 recipe (мінімум 1–2) | ⬜ | P2 | RIP / SSL web-mode … |
| 5 | README + bump 0.9.0 | ⬜ | P0 | кінець спринту |

---

## VDOM map

Користувач задає відповідність імен VDOM числовим індексам (як на FortiGate у `diagnose sys session filter vd`):

```
root=0
vd-LAN=1
vd-DMZ=2
```

Зберігається в `config.json` → `vdom_map: { "root": "0", ... }`.

---

*Оновлено: 2026-09-06*
