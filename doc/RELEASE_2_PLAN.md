# FortiDebug Builder — Release 2 Plan

**Мета:** збагатити додаток згідно з офіційними рекомендаціями Fortinet.

---

## Статус (таблиця кроків)

| # | Крок | Стан | Примітки |
|---|------|------|----------|
| 1 | Safety-блоки | ✅ Done | |
| 2 | Flows v2 | ✅ Done | |
| 3 | Recipes / Workflows | ✅ Done | |
| 4 | Application Debug | ✅ Done | |
| 5a | Sessions enrichment | ✅ Done | policy, ext-sip/dip, duration, clear warning |
| 5b | Sniffer enrichment | ✅ Done | BPF JSON, IPv6 host, ts, presets |
| 5c | VPN enrichment | ✅ Done | interface/ifindex, status+stats |
| 6 | TAC / Support | ✅ Done | |
| 7 | UX polish | 🟡 Partial | hotkeys/theme ✅; tooltips ❌ |
| 8 | README / CHANGELOG / build | 🟡 Partial | build.spec + icon ❌ |
| — | Settings + About | ✅ Done | |
| — | Config persist | ✅ Done | theme/lang AppData |
| — | Validators IPv6 | ✅ Done | |
| — | Unit tests | ❌ Todo | |

**Легенда:** ✅ Done · 🟡 Partial · ❌ Todo

---

## Залишилось

1. Tooltips у UI
2. `build.spec` + іконка
3. Unit-тести (pytest)

---

*Оновлено: 2026-09-04*
