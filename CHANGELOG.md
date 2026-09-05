# Changelog

Усі значущі зміни проекту FortiDebug Builder (Windows).

Формат базується на [Keep a Changelog](https://keepachangelog.com/).

---

## [Unreleased] — Release 5

### Added
- **Recipes**: розширено до **42 playbooks** (+10):
  - ZTNA / Access Proxy (version-aware: `endpoint record list` → `ec-shm list` з 7.4.2+)
  - FortiAnalyzer / remote logging (`fgtlogd` test levels + OFTP debug)
  - WAD / Proxy engine (filters + category/level verbose)
  - DoS / Flood protection
  - User auth LDAP/RADIUS/TACACS (`fnbamd`/`authd` + sniffer ports)
  - General TAC collect / healthcheck (`execute tac report` + perf/crashlog)
  - ARP / Neighbor
  - Link-monitor / health-check
  - Antivirus / AV engine
  - Traffic shaping / QoS
- Export bundle, sidebar search, SSL/SD-WAN recipes

---

## [0.5.2] — 2026-09-05

### Added
- **CI / Release**: GitHub Actions workflow (`.github/workflows/build-windows.yml`) — збірка `FortiDebugBuilder.exe` на `windows-latest` і автоматичний GitHub Release при пуші тегу `v*`

### Changed
- `.gitignore`: прибрано ігнорування `*.spec`, щоб `build.spec` завжди був у репозиторії
- README: секція «Автоматичний реліз»

---

## [0.5.1] — 2026-09-05

### Added
- Tooltips, build.spec, тести IKE/SD-WAN

### Fixed
- SD-WAN / Policy Lookup version syntax

---

## [0.5.0] — 2026-09-05

### Added
- Wireless, Hardware/NPU, First steps, persist, scroll

---

## [0.4.0] — 2026-09-05

### Added
- Network, Policy Lookup, VIP, SSL, DHCP, SD-WAN, Auth, …

---

## [0.1.0] — 2026-09-03

### Added
- Базові модулі, FortiOS selector
