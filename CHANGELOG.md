# Changelog

Усі значущі зміни проекту FortiDebug Builder (Windows).

Формат базується на [Keep a Changelog](https://keepachangelog.com/).

---

## [0.7.0] — 2026-09-06 — Release 6

### Added
- **Recipes +7 (49 total)** — `src/ui/tabs/recipe_r6.py` (`RecipeR6Mixin`):
  - **P0:** ADVPN / Shortcut tunnels; SIP / VoIP / ALG; Application Control / ISDB
  - **P1:** Email filter / Antispam; File filter / DLP; Transparent mode / Bridging; Modem / LTE / PPP
- **Глобальний перемикач VDOM** (sidebar, поруч із FortiOS):
  - Switch **VDOM mode** + поле імені VDOM (default `root`)
  - **ON:** preview → `config vdom` / `edit <name>` … `end` / `end`
  - **OFF:** без multi-VDOM контексту
  - Sessions / Flows / Recipes: `filter vd` через `resolve_vd_index`
  - Persist: `vdom_enabled`, `vdom_name` у config.json
- `src/core/vdom.py`, `tests/test_vdom.py`, `tests/test_recipes_r6.py`
- План: `doc/RELEASE_6_PLAN.md`

### Changed
- `_session_block` / `_flow_block` — optional `vd` (backward-compatible)
- Export bundle header включає стан VDOM mode
- About / README version **0.7.0**

---

## [Unreleased] — Release 5

### Added
- **Індекс документації** (`doc/INDEX.md`)
- **Кодекс впровадження** (`doc/CODEX_IMPLEMENTATION.md`)
- **Recipes**: 42 playbooks (+10), mixins `recipe_extra` / `recipe_impl`
- Export bundle, sidebar search, SSL/SD-WAN recipes

### Changed
- `AGENTS.md`: обов’язок актуалізувати `doc/INDEX.md`

---

## [0.5.2] — 2026-09-05

### Added
- **CI / Release**: GitHub Actions — збірка `FortiDebugBuilder.exe` + Release на тег `v*`

### Changed
- `.gitignore`: `build.spec` у репозиторії
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
