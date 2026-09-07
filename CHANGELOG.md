# Changelog

Усі значущі зміни проекту FortiDebug Builder (Windows).

Формат базується на [Keep a Changelog](https://keepachangelog.com/).

---

## [Unreleased]

### Changed
- **Процес релізу:** обов’язок генерувати `RELEASE_NOTES.md` під кожен реліз і публікувати разом із GitHub Release (asset + body). Зафіксовано в `AGENTS.md` §3, `doc/CODEX_IMPLEMENTATION.md`, CI `build-windows.yml`.
- **README.md** — повний детальний опис програми (можливості, Recipes, модулі, встановлення, структура, обмеження, гарячі клавіші). Версія в README: 0.18.2.

---

## [0.18.2] — 2026-09-07

### Fixed
- **Скрол колесом миші у випадаючих списках** — stock CustomTkinter OptionMenu/ComboBox не скролиться на довгих списках.
  - Vendored [CTkScrollableDropdown](https://github.com/Akascape/CTkScrollableDropdown) (MIT, Akash Bora)
  - `wire_scrollable_dropdowns()` підключає scrollable popup до всіх меню після старту (`src/main.py`)
  - Helper: `src/ui/widgets/scrollable_menu.py`

---

## [0.18.1] — 2026-09-07

### Changed
- **Алфавітне сортування всіх меню та списків у UI** (case-insensitive):
  - Sidebar navigation — за поточним перекладеним label (перебудова при зміні мови)
  - Recipes (85 playbooks)
  - App Debug daemons, Sessions/Flows/Sniffer protocols, System Top variants
  - Sniffer interfaces + BPF presets, Hardware NPU family
  - Policy Lookup proto / pol_type / auth_type, SSH Logger shells
- Числові рівні (verbose, IKE, debug level) та FortiOS versions залишено в логічному порядку

---

## [0.18.0] — 2026-09-06 — Release 17

### Added
- **Logging pack +7 (85 total)** — `recipe_r17.py`:
  - Log disk full / filesystem
  - Syslog not received
  - FAZ OFTP / connectivity deep
  - Memory logging / miglogd
  - Traffic log missing
  - Event log search / filter
  - Log rate / miglogd load

### Changed
- About / README → **0.18.0**

---

## [0.17.0] — 2026-09-06 — Release 16

### Added
- WiFi / FortiAP pack (78)

---

## [0.16.0] — 2026-09-06 — Release 15

### Added
- Remote-user pack

---

## [0.15.0] — 2026-09-06 — Release 14

### Added
- LLDP / 802.1X / Captive portal

---

## [0.14.0] — 2026-09-06 — Release 13

### Added
- EVPN + WebCache/WCCP

---

## [0.13.0] — 2026-09-06 — Release 12

### Added
- GRE / VXLAN / CGNAT

---

## [0.12.0] — 2026-09-06 — Release 11

### Added
- BFD + SAML SSO

---

## [0.11.0] — 2026-09-06 — Release 10

### Added
- IoC + Cloud SDN

---

## [0.10.0] — 2026-09-06 — Release 9

### Added
- IS-IS + Automation Stitch

---

## [0.9.0] — 2026-09-06 — Release 8

### Added
- VDOM map; RIP + SSL web-mode

---

## [0.8.0] — 2026-09-06 — Release 7

### Added
- Restore stubs; global VDOM

---

## [0.7.0] — 2026-09-06 — Release 6

### Added
- Recipes +7 + VDOM mode

---

## [0.5.2] — 2026-09-05

### Added
- CI Windows EXE

---

## [0.1.0] — 2026-09-03

### Added
- Базові модулі
