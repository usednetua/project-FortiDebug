# Changelog

Усі значущі зміни проекту FortiDebug Builder (Windows).

Формат базується на [Keep a Changelog](https://keepachangelog.com/).

---

## [Unreleased] — Release 7 (0.8.0)

### Added
- **Restore stubs:** 24 playbooks у `recipe_impl.py` відновлено з `artifacts/recipes_final.py`
  (Dial-up IPsec, SSL VPN, Policy/NAT, VIP, Local-in, OSPF, BGP, Routing, DHCP, Auth/FSSO,
  DNS, Webfilter, IPS/UTM, Explicit proxy, Wireless, LACP, Interface, NPU, Certificate,
  FortiGuard, Log disk, NTP, IPv6, Multicast)
- `doc/RELEASE_7_PLAN.md` — план 0.8.0

### Changed
- Більше немає stub `# pending restore` у Recipes (усі 49 з реальними тілами)

---

## [0.7.0] — 2026-09-06 — Release 6

### Added
- **Recipes +7 (49 total)** — `RecipeR6Mixin`: ADVPN, SIP/VoIP, App Control/ISDB, Email, File/DLP, Transparent, Modem/LTE
- **Глобальний VDOM mode** (sidebar) + `core.vdom` + filter vd
- `tests/test_vdom.py`, `tests/test_recipes_r6.py`

### Changed
- About / README → **0.7.0**

---

## [0.5.2] — 2026-09-05

### Added
- CI / Release: Windows EXE + GitHub Release на тег `v*`

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

## [0.1.0] — 2026-09-03

### Added
- Базові модулі, FortiOS selector
