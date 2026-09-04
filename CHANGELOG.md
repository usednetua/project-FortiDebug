# Changelog

Усі значущі зміни проекту FortiDebug Builder (Windows).

Формат базується на [Keep a Changelog](https://keepachangelog.com/).

---

## [0.2.0] — 2026-09-04

### Added
- **Recipes / Workflows** — 6 playbooks (Traffic, VPN, High CPU, Policy/NAT, HA, DNS)
- **Application Debug** — authd, dnsproxy, ike, sslvpn, miglogd, fgtlogd, urlfilter, wad, sip, …
- **TAC / Support** — tac report, debug report, support bundle
- **Flows v2** — iprope, IPv6, addr filter, presets
- **Sessions** — IPv6 session6, clear, full-stat
- **Sniffer** — timestamp `a`/`l`, presets DNS / IKE-ESP / SYN
- **Safety-блоки** (reset / clear / timestamps / stop+reset)
- **UX** — dark theme, Ctrl+Enter Copy, Ctrl+S Save, Copy stop-debug
- Оновлений README

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
