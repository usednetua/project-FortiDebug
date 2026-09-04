# Changelog

Усі значущі зміни проекту FortiDebug Builder (Windows).

Формат базується на [Keep a Changelog](https://keepachangelog.com/).

---

## [Unreleased]

### Added
- **Flows v2**:
  - `diagnose debug flow show iprope enable`
  - IPv6: `filter6` / `trace start6`
  - фільтр `addr` (будь-яка сторона)
  - Presets: Traffic denied, NAT check, Policy match
- **Safety-блоки** у Flows / VPN / HA / Routing:
  - `diagnose debug reset`
  - `diagnose debug flow filter clear`
  - timestamps, optional `diagnose debug info`
  - stop: `diagnose debug disable` + `diagnose debug reset`

### Planned (Release 2)
- Recipes / Workflows
- Application Debug tab
- TAC / Support helper
- Sessions / Sniffer enrichment
- Див. `doc/RELEASE_2_PLAN.md`

---

## [0.1.0] — 2026-09-03 / 2026-09-04

### Added
- Початкова структура (Python + CustomTkinter)
- Sessions, Ping, Traceroute, Sniffer, Flows, VPN, System Top, HA, Routing
- SSH Logger, Saved Commands (SQLite)
- Перемикач FortiOS 6.0–8.0 + version-aware IKE syntax
- `doc/PLAN.md`, `doc/RELEASE_2_PLAN.md`

### Notes
- IKE: ≤7.2 `log-filter`+`dst-addr4`; ≥7.4.1 `log filter`+`rem-addr4`
