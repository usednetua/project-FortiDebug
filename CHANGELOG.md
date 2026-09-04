# Changelog

Усі значущі зміни проекту FortiDebug Builder (Windows).

Формат базується на [Keep a Changelog](https://keepachangelog.com/).

---

## [Unreleased]

### Added
- **Recipes / Workflows** — 6 playbooks:
  - Traffic not passing (session + flow + sniffer)
  - VPN down / rekey (version-aware IKE)
  - High CPU
  - Policy / NAT check (iprope)
  - HA out-of-sync
  - DNS issues (dnsproxy)
- **Flows v2**: iprope, IPv6, addr filter, presets
- **Safety-блоки** у Flows / VPN / HA / Routing

### Planned (Release 2)
- Application Debug tab
- TAC / Support helper
- Sessions / Sniffer enrichment
- UX polish / hotkeys
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
