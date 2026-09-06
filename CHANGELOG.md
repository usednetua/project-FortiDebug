# Changelog

Усі значущі зміни проекту FortiDebug Builder (Windows).

Формат базується на [Keep a Changelog](https://keepachangelog.com/).

---

## [Unreleased] — Release 6 (0.7.0)

### Added
- **План Release 6** (`doc/RELEASE_6_PLAN.md`): gap-аналіз відкритих FortiGate debug recipes
- **Recipes +7 (49 total)** — `src/ui/tabs/recipe_r6.py` (`RecipeR6Mixin`):
  - **P0:** ADVPN / Shortcut tunnels; SIP / VoIP / ALG; Application Control / ISDB
  - **P1:** Email filter / Antispam; File filter / DLP; Transparent mode / Bridging; Modem / LTE / PPP
- `RecipesTab`: MRO `RecipeR6Mixin, RecipeExtraMixin, RecipeImplMixin, BaseTab`
- Оновлено `doc/INDEX.md` — Release 6 in progress

### Changed
- Старт спринту за Кодексом впровадження (план перед кодом)

---

## [Unreleased] — Release 5

### Added
- **Індекс документації** (`doc/INDEX.md`) — навігаційний каталог усіх планів, кодексів і документів у `doc/`
- **Кодекс впровадження** (`doc/CODEX_IMPLEMENTATION.md`): обов’язковий процес перед будь-яким впровадженням
  - детальний план у `doc/` перед стартом
  - таблиця етапів / стану / приміток на початку плану
  - перевірка сумісності після кожного етапу («не зламай!»)
- **Recipes**: розширено до **42 playbooks** (+10), розбито на mixins:
  - `src/ui/tabs/recipe_extra.py` — усі 10 нових (повністю):
    - ZTNA / Access Proxy (version-aware: `endpoint record list` → `ec-shm list` з 7.4+)
    - FortiAnalyzer / remote logging (`fgtlogd` 1–5 + OFTP debug)
    - WAD / Proxy engine (filters + category/level verbose)
    - DoS / Flood protection
    - User auth LDAP/RADIUS/TACACS (`fnbamd`/`authd` + sniffer)
    - General TAC collect / healthcheck (`execute tac report`)
    - ARP / Neighbor
    - Link-monitor / health-check
    - Antivirus / AV engine
    - Traffic shaping / QoS
  - `src/ui/tabs/recipe_impl.py` — helpers + core (First steps, Traffic not passing, VPN, High CPU/mem, Session full, HA, SD-WAN)
  - Решта original playbooks — stubs (`_missing`), повний код у `artifacts/recipes_final.py` (потребує restore)
- Export bundle, sidebar search, SSL/SD-WAN recipes

### Changed
- RecipesTab: `RecipeExtraMixin, RecipeImplMixin, BaseTab`
- `AGENTS.md`: обов’язок актуалізувати `doc/INDEX.md` при кожній зміні документації

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
