# FortiDebug Builder — Release 2 Plan

**Мета:** збагатити додаток згідно з офіційними рекомендаціями Fortinet щодо безпечного та ефективного debug.

Джерела: Fortinet Document Library (debug flow, sniffer, CLI cheat sheet), Community Technical Tips.

---

## Статус (таблиця кроків)

| # | Крок | Стан | Примітки |
|---|------|------|----------|
| 1 | Safety-блоки (reset/clear/stop/timestamps) | ✅ Done | Flows, VPN, HA, Routing, App Debug, Recipes |
| 2 | Flows v2 (iprope, IPv6, addr, presets) | ✅ Done | |
| 3 | Recipes / Workflows (6 сценаріїв) | ✅ Done | |
| 4 | Application Debug tab | ✅ Done | duration є; окремі app-фільтри — обмежено |
| 5a | Sessions enrichment | 🟡 Partial | IPv6, clear, full-stat ✅; policy/ext-sip/duration ❌ |
| 5b | Sniffer enrichment | 🟡 Partial | ts a/l, presets ✅; BPF→JSON ❌; IPv6 host у simple ❌ |
| 5c | VPN enrichment | 🟡 Partial | version-aware syntax ✅; interface filter, P1/P2 stats ❌ |
| 6 | TAC / Support | ✅ Done | |
| 7 | UX polish | 🟡 Partial | dark, hotkeys, copy-stop ✅; tooltips ❌; IP validation у UI ❌ |
| 8 | README / CHANGELOG / build | 🟡 Partial | README+CHANGELOG ✅; build.spec + icon ❌ |
| — | Settings (theme + language) | ✅ Done | додано після плану |
| — | About (version, author, site) | ✅ Done | додано після плану |

**Легенда:** ✅ Done · 🟡 Partial · ❌ Todo

---

## Залишилось (todo / partial)

1. **Sessions** — фільтри `policy`, `ext-sip`, `ext-dip`, `duration`; підтвердження перед `clear`
2. **Sniffer** — кастомні BPF у JSON (AppData); IPv6 host у simple filter
3. **VPN** — filter `interface`; Phase1/Phase2 stats
4. **UX** — tooltips; валідація IP/port у UI
5. **Збірка** — `build.spec` + іконка + version metadata
6. **Персистентність** — theme/lang у `%APPDATA%\FortiDebugBuilder\config.json`
7. **Тести** — unit-тести генераторів (pytest)

---

## Ключові принципи Fortinet

1. Завжди `diagnose debug reset` + `filter clear` перед стартом.
2. Завжди вузький фільтр (IP/port/proto).
3. Завжди timestamps.
4. Завжди ліміт `trace start <N>`.
5. Завжди після: `diagnose debug disable` + `diagnose debug reset`.
6. `disable` не зупиняє фон — потрібен `reset`.
7. Real-time debug = CPU-intensive.
8. Корисно: `diagnose debug info`.

---

*Оновлено: 2026-09-04 — статусна таблиця*
