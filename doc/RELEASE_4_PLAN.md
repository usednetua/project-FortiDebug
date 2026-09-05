# FortiDebug Builder — Release 4 Plan

**Мета:** полірування продукту (іконка, tooltips, тести) + розширені діагностики з cheatsheet’ів, які ще не покриті (Wireless, NPU/hardware).

**Базова версія:** 0.4.1  
**Цільова версія:** 0.5.0

---

## Статус (таблиця кроків)

| # | Крок | Стан | Пріоритет | Примітки |
|---|------|------|-----------|----------|
| 1 | Іконка `.ico` + підключення в `build.spec` | ❌ Todo | P0 | EXE branding |
| 2 | Tooltips на всіх основних вкладках | ❌ Todo | P0 | VPN, Sniffer, Ping, HA, Routing, DHCP, SD-WAN, Auth, UTM, TAC |
| 3 | Unit-тести для Network / Policy lookup / safety generators | ❌ Todo | P0 | pytest |
| 4 | FortiOS version persist у config.json | ❌ Todo | P1 | разом із theme/lang |
| 5 | Content area scroll (довгі вкладки) | ❌ Todo | P1 | CTkScrollableFrame |
| 6 | Wireless / CAPWAP basic diagnostics | ❌ Todo | P2 | якщо є FortiAP |
| 7 | NPU / hardware quick view | ❌ Todo | P2 | npu np6/np7 summary, hardware deviceinfo |
| 8 | Recipe: «First steps connectivity» (sniffer+flow+session+route) | ❌ Todo | P1 | Community first-steps tip |
| 9 | README / CHANGELOG / About → 0.5.0 | ❌ Todo | P0 | на фініші |

**Легенда:** ✅ Done · 🟡 Partial · ❌ Todo  
**Пріоритет:** P0 = MVP R4 · P1 = бажано · P2 = за потреби

---

## 1. Контекст

R2/R3 закрили основні CLI-сценарії з офіційних і community cheatsheet’ів.  
R4 фокус:

1. **Якість релізу** — іконка, tooltips скрізь, тести, UX скролу.
2. **Нішеві, але часті** — wireless (якщо AP), NPU overview, «first steps» recipe.
3. **Persist** — пам’ятати обрану FortiOS у `%APPDATA%`.

---

## 2. Детальний покроковий план

### Крок 1. Іконка EXE (P0) — 0.5 дня

**Файли:**
- `src/resources/icons/app.ico` (16/32/48/256)
- `build.spec` — розкоментувати / додати `icon='src/resources/icons/app.ico'`

**Дії:**
1. Підготувати просту іконку (щит / CLI / «FD») у форматі multi-size `.ico`.
2. Оновити `build.spec`.
3. Перевірити збірку: `pyinstaller build.spec`.

**Критерій:** `dist/FortiDebugBuilder.exe` має власну іконку в Explorer.

---

### Крок 2. Tooltips скрізь (P0) — 0.5–1 день

Використовувати `ui.widgets.tooltip.tip`.

| Вкладка | Приклади підказок |
|---------|-------------------|
| VPN | SSL monitor, ifindex, stop-block |
| Sniffer | verbose levels, BPF Save |
| Ping / Traceroute | source, df-bit, data-size |
| HA | checksum cluster / recalculate |
| Routing | protocol-specific list |
| DHCP | lease-list vs relay debug |
| SD-WAN | health-check vs service |
| Auth | clear ⚠ |
| UTM/IPS | шумний debug |
| TAC | tac report довгий, cli 7 |

**Критерій:** ключові checkbox/entry мають hover-підказку українською або EN (залежно від i18n за бажанням — спочатку фіксовані рядки).

---

### Крок 3. Unit-тести (P0) — 0.5–1 день

**Нові / розширити:**
- `tests/test_network_cmds.py` — генерація рядків ARP/LACP (через thin helper або mock-free pure functions, якщо винесемо).
- `tests/test_policy_lookup.py` — формат `iprope lookup`.
- Існуючі: validators, safety, fortios — лишити зелені.

**Опційно:** винести чисті `build_*_commands(...)` у `core/cmd_builders.py` для легкого тесту без GUI.

**Критерій:** `pytest` з `src` на path проходить.

---

### Крок 4. Persist FortiOS version (P1) — 0.25 дня

**Файли:** `core/config.py`, `main_window.py`, `main.py`

- Зберігати `fortios` label у `config.json`.
- При старті — `version_menu.set(...)` з config.
- При зміні — `save_config({"fortios": label})`.

---

### Крок 5. Scrollable content (P1) — 0.5 дня

Довгі вкладки (VPN, Sessions, Recipes) обрізаються на малих екранах.

**Варіанти:**
- A) Кожну важку вкладку в `CTkScrollableFrame`.
- B) Один scroll у `content` (складніше з grid_forget).

Рекомендація: **A** для VPN, Sessions, App Debug, Recipes.

---

### Крок 6. Wireless / CAPWAP (P2) — 1 день

**Файл:** `src/ui/tabs/wireless.py`

| Опція | Команда (типові) |
|-------|------------------|
| Managed AP list | `diagnose wireless-controller wlac -c wtp` / `get wireless-controller wtp-status` |
| Client list | `diagnose wireless-controller wlac -c sta` |
| CAPWAP debug | `diagnose debug application cw_acd -1` + safety |
| RF/scan (за моделлю) | задокументувати в tooltip, що залежить від версії |

**Важливо:** перевірити синтаксис по FortiOS 7.x docs перед фінальним merge; додати примітку «доступність залежить від моделі/ліцензії».

---

### Крок 7. NPU / hardware (P2) — 0.5–1 день

**Файл:** `src/ui/tabs/hardware.py` або секція System Top / TAC

| Опція | Команда |
|-------|---------|
| CPU / mem | `diagnose hardware cpuinfo`, `meminfo` |
| deviceinfo | `diagnose hardware deviceinfo disk` / `nic` |
| NPU session / stats | `diagnose npu np6/np7 ...` — **версійно-залежно**, UI з вибором NP6/NP7 або «generic» |
| HQIP suite | `diagnose hardware test suite all` (⚠ довго, production risk) — лише з явним checkbox + warning |

Не робити повну матрицю всіх NPU команд — лише safe overview + warning.

---

### Крок 8. Recipe «First steps connectivity» (P1) — 0.5 дня

За Community tip (sniffer → flow → session → routing):

1. Sniffer host/port  
2. Session filter + list  
3. Flow з iprope  
4. `get router info routing-table details <dst>`  
5. Optional policy lookup comment  

Поля: src, dst, port (як у інших recipes).

---

### Крок 9. Документація і реліз 0.5.0 (P0)

1. CHANGELOG → `[0.5.0]`  
2. About `APP_VERSION = "0.5.0"`  
3. README — іконка, нові вкладки  
4. Оновити статус-таблицю цього файлу  

---

## 3. Порядок sprint’ів

| Етап | Кроки | Оцінка |
|------|-------|--------|
| A (MVP) | 1 icon + 2 tooltips + 3 tests + 9 docs partial | 1.5–2 дні |
| B | 4 persist + 5 scroll + 8 first-steps recipe | 1–1.5 дні |
| C | 6 wireless + 7 NPU | 1.5–2 дні |
| D | 9 final 0.5.0 | 0.25 дня |

**MVP Release 4:** етап A (+ бажано B).  
**Full R4:** A–D.

---

## 4. Критерії готовності MVP R4

- [ ] EXE з іконкою через `build.spec`
- [ ] Tooltips на ≥8 вкладках окрім уже покритих
- [ ] `pytest` зелений, + тести policy/network
- [ ] CHANGELOG / About відображають прогрес (0.5.0 на full close)

---

## 5. Поза скоупом R4

- Повна автоматизація GUI packet capture
- ZTNA deep debug
- Переписування на Qt/Electron
- CI/CD GitHub Actions (можна окремим планом)

---

*Створено: 2026-09-05*  
*База: 0.4.1, R2/R3 complete*
