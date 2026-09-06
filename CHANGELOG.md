# Changelog

Усі значущі зміни проекту FortiDebug Builder (Windows).

Формат базується на [Keep a Changelog](https://keepachangelog.com/).

---

## [Unreleased] — Release 8 (0.9.0)

### Added
- **VDOM name→index map** (Settings): рядки `name=index` → `config.json` `vdom_map`
  - `resolve_vd_index` використовує карту для `filter vd` (Sessions / Flows / Recipes)
  - default `root=0`; іменовані VDOM (vd-LAN=1, …)
- `normalize_vdom_map` / `vdom_map_to_text` у `core.vdom`
- `doc/RELEASE_8_PLAN.md`

### Changed
- Settings: редактор карти + «Зберегти карту VDOM»

---

## [0.8.0] — 2026-09-06 — Release 7

### Added
- Restore 24 stubs; global-scope VDOM carve-out; тести

### Changed
- About / README → **0.8.0**

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
