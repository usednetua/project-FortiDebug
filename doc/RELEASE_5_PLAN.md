# FortiDebug Builder — Release 5 Plan

**Цільова версія:** 0.6.0  
**Старт:** 2026-09-05

---

## Статус (таблиця кроків)

| # | Крок | Стан | Пріоритет | Примітки |
|---|------|------|-----------|----------|
| 1 | Export bundle (.txt + meta) | ✅ Done | P0 | app/FortiOS/tab/time |
| 2 | Пошук вкладок у sidebar | ✅ Done | P0 | filter nav |
| 3 | Recipe: SSL VPN login fail | ✅ Done | P0 | sslvpn + authd |
| 4 | Recipe: SD-WAN member dead | ✅ Done | P0 | version-aware |
| 5 | Recipe: IKE / SAML extras | ⬜ Todo | P1 | опційно |
| 6 | Log filter builder | ⬜ Todo | P1 | |
| 7 | DNS / webfilter tab polish | ⬜ Todo | P2 | |
| 8 | GitHub Actions pytest | ⬜ Todo | P2 | |
| 9 | README + bump 0.6.0 | ⬜ Todo | P0 | після закриття P0/P1 |

---

## Принципи R5

- Завжди `get_version` для CLI з різницею синтаксису
- CHANGELOG перед комітом
- Таблиця статусу в плані оновлюється після кожного кроку

---

*Оновлено: 2026-09-05*
