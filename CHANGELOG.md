# Changelog

Усі значущі зміни проекту FortiDebug Builder (Windows).

Формат базується на [Keep a Changelog](https://keepachangelog.com/).

---

## [Unreleased] — Release 7 (0.8.0)

### Added
- **Restore stubs:** 24 playbooks у `recipe_impl.py` відновлено з `artifacts/recipes_final.py`
- **Global-scope VDOM carve-out:** вкладки HA / System Top / Hardware / TAC і recipes
  (HA, High CPU/mem, NPU, TAC, FortiGuard, NTP, Log disk, Certificate) **не** обгортаються в
  `config vdom` навіть коли VDOM mode ON — лише коментар `# GLOBAL scope`
- `should_wrap_vdom()`, `GLOBAL_SCOPE_TABS`, `GLOBAL_SCOPE_RECIPES` у `core.vdom`
- `doc/RELEASE_7_PLAN.md`, `tests/test_no_stubs.py`

### Changed
- Більше немає stub `# pending restore` у Recipes
- `wrap_vdom_context` приймає `tab_key` / `recipe_name` / `scope`

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
