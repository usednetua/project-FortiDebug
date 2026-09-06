# FortiDebug Builder — Release 9 Plan

**Цільова версія:** 0.10.0  
**Старт / закрито:** 2026-09-06  
**Тема:** IS-IS + Automation Stitch + CI tags (manual)

---

## Статус

| # | Крок | Стан |
|---|------|------|
| 0 | План R9 + INDEX + CHANGELOG | ✅ |
| 1 | Recipe: IS-IS neighbor / LSP | ✅ |
| 2 | Recipe: Automation Stitch | ✅ |
| 3 | (опц.) IoC / Cloud SDN | ⬜ backlog |
| 4 | README + bump 0.10.0 | ✅ |
| 5 | Тег `v0.10.0` (CI EXE) | ⬜ вручну |

**Playbooks: 53.**

---

## CI tags (вручну)

```bash
git tag v0.9.0   # optional historical
git tag v0.10.0
git push origin v0.9.0 v0.10.0
```

Workflow `Build Windows EXE` → Release + `FortiDebugBuilder.exe`.

---

*Закрито: 2026-09-06*
