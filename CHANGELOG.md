# Changelog

Усі значущі зміни проекту FortiDebug Builder (Windows).

Формат базується на [Keep a Changelog](https://keepachangelog.com/).

---

## [Unreleased]

### Added
- **UX**: dark theme за замовч., Ctrl+Enter = Copy, Ctrl+S = Save .txt, кнопка «Copy stop-debug»
- **Sessions enrichment**: IPv6, clear, full-stat
- **Sniffer enrichment**: timestamp format, presets DNS / IKE-ESP / SYN
- **TAC / Support**
- **Application Debug**
- **Recipes / Workflows** — 6 playbooks
- **Flows v2**: iprope, IPv6, presets
- **Safety-блоки**

### Planned (Release 2)
- README update / build.spec
- Див. `doc/RELEASE_2_PLAN.md`

---

## [0.1.0] — 2026-09-03 / 2026-09-04

### Added
- Структура (Python + CustomTkinter)
- Sessions, Ping, Traceroute, Sniffer, Flows, VPN, System Top, HA, Routing
- SSH Logger, Saved Commands (SQLite)
- FortiOS 6.0–8.0 + version-aware IKE
- `doc/PLAN.md`, `doc/RELEASE_2_PLAN.md`

### Notes
- IKE: ≤7.2 `log-filter`+`dst-addr4`; ≥7.4.1 `log filter`+`rem-addr4`
