# Changelog

Усі значущі зміни проекту FortiDebug Builder (Windows).

Формат базується на [Keep a Changelog](https://keepachangelog.com/).

---

## [0.9.0] — 2026-09-06 — Release 8

### Added
- **VDOM name→index map** (Settings): `name=index` → `config.json` `vdom_map`
  - `resolve_vd_index` для Sessions / Flows / Recipes `filter vd`
  - default `root=0`
- **Recipes +2 (51 total)** — `recipe_r8.py`:
  - RIP neighbor / routes
  - SSL VPN web-mode
- `normalize_vdom_map` / `vdom_map_to_text`
- `doc/RELEASE_8_PLAN.md`

### Changed
- About / README → **0.9.0**

### Backlog → 1.0.x
- IS-IS, IoC pack, Automation Stitch, Cloud SDN

---

## [0.8.0] — 2026-09-06 — Release 7

### Added
- Restore 24 stubs; global-scope VDOM carve-out; тести

---

## [0.7.0] — 2026-09-06 — Release 6

### Added
- Recipes +7 (49) + глобальний VDOM mode

---

## [0.5.2] — 2026-09-05

### Added
- CI / Release Windows EXE

---

## [0.1.0] — 2026-09-03

### Added
- Базові модулі, FortiOS selector
