# Changelog

Усі значущі зміни проекту FortiDebug Builder (Windows).

Формат базується на [Keep a Changelog](https://keepachangelog.com/).

---

## [Unreleased]

### Added
- **Safety-блоки** у Flows / VPN / HA / Routing:
  - `diagnose debug reset`
  - `diagnose debug flow filter clear` (Flows)
  - `diagnose debug console timestamp enable`
  - `diagnose debug info` (опційно)
  - обов’язковий stop: `diagnose debug disable` + `diagnose debug reset`
- Flows: виправлено `trace start` (було `trace-start`), додано filter clear, show function-name

### Planned (Release 2)
- Flows v2: iprope, IPv6, presets
- Recipes / Workflows
- Application Debug tab
- TAC / Support helper
- Див. `doc/RELEASE_2_PLAN.md`

---

## [0.1.0] — 2026-09-03 / 2026-09-04

### Added
- Початкова структура проекту (Python + CustomTkinter)
- **Sessions**, **Ping**, **Traceroute**, **Sniffer**, **Flows**, **VPN**, **System Top**, **HA**, **Routing**
- **SSH Logger**, **Saved Commands** (SQLite)
- Перемикач **FortiOS 6.0–8.0** + version-aware IKE syntax
- `doc/PLAN.md`, `doc/RELEASE_2_PLAN.md`

### Notes
- IKE: ≤7.2 `log-filter`+`dst-addr4`; ≥7.4.1 `log filter`+`rem-addr4`
