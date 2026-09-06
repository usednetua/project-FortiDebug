# Changelog

Усі значущі зміни проекту FortiDebug Builder (Windows).

Формат базується на [Keep a Changelog](https://keepachangelog.com/).

---

## [0.8.0] — 2026-09-06 — Release 7

### Added
- **Restore stubs:** 24 playbooks у `recipe_impl.py` відновлено з `artifacts/recipes_final.py`
  (Dial-up IPsec, SSL VPN, Policy/NAT, VIP, Local-in, OSPF, BGP, Routing, DHCP, Auth/FSSO,
  DNS, Webfilter, IPS/UTM, Explicit proxy, Wireless, LACP, Interface, NPU, Certificate,
  FortiGuard, Log disk, NTP, IPv6, Multicast)
- **Global-scope VDOM carve-out:** вкладки HA / System Top / Hardware / TAC і відповідні recipes
  **не** обгортаються в `config vdom` при VDOM mode ON — банер `# GLOBAL scope`
- `should_wrap_vdom()`, `GLOBAL_SCOPE_TABS`, `GLOBAL_SCOPE_RECIPES` у `core.vdom`
- `tests/test_no_stubs.py`, розширені `tests/test_vdom.py`
- `doc/RELEASE_7_PLAN.md`

### Changed
- Усі 49 recipes з повними CLI-тілами (без `# pending restore`)
- About / README → **0.8.0**

### Backlog → 0.9.x
- VDOM name→index mapping у Settings
- P2 recipes: RIP, IS-IS, SSL web-mode, IoC, Automation Stitch, Cloud SDN

---

## [0.7.0] — 2026-09-06 — Release 6

### Added
- **Recipes +7 (49 total)** + **глобальний VDOM mode** + тести

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

---

## [0.1.0] — 2026-09-03

### Added
- Базові модулі, FortiOS selector
