# FortiDebug Builder — Release 6 Plan

**Цільова версія:** 0.7.0  
**Старт:** 2026-09-06  
**Тема спринту:** відкриті (публічні) рецепти / playbooks, які ще не реалізовані в додатку

---

## Статус (таблиця кроків)

| # | Крок | Стан | Пріоритет | Примітки |
|---|------|------|-----------|----------|
| 0 | Gap-аналіз відкритих рецептів (огляд) | ✅ Done | P0 | 2026-09-06, цей спринт |
| 1 | План Release 6 + INDEX + CHANGELOG | 🔄 In progress | P0 | цей файл |
| 2 | Mixin-структура для нових recipes (`recipe_r6.py` або розширення extra) | ⬜ Todo | P0 | не ламати 42 існуючі |
| 3 | Recipe: **ADVPN / Shortcut tunnels** | ⬜ Todo | P0 | SD-WAN + IKE, version-aware |
| 4 | Recipe: **SIP / VoIP / ALG** | ⬜ Todo | P0 | pinholes, one-way audio |
| 5 | Recipe: **Application Control / ISDB** | ⬜ Todo | P0 | app-ctrl list, SD-WAN steering |
| 6 | Recipe: **Email filter / Antispam** | ⬜ Todo | P1 | smtp / emailfilter debug |
| 7 | Recipe: **File filter + DLP** | ⬜ Todo | P1 | можна об’єднати або 2 окремі |
| 8 | Recipe: **Transparent mode / Bridging** | ⬜ Todo | P1 | brctl, FDB |
| 9 | Recipe: **Modem / LTE / PPP** | ⬜ Todo | P1 | sys modem, link |
| 10 | Recipe: **VDOM-aware wrappers** (параметр vd майже всюди) | ⬜ Todo | P1 | cross-cutting |
| 11 | Regression «не зламай!» на 42 існуючих + нові | ⬜ Todo | P0 | після кожного recipe |
| 12 | Тести (pytest) на нові генератори | ⬜ Todo | P1 | |
| 13 | README + bump 0.7.0 + INDEX | ⬜ Todo | P0 | |

---

## 1. Контекст і джерела

Поточний стан: **42 playbooks** (Release 5).

Відкриті джерела gap-аналізу:
- Fortinet Document Library: Troubleshooting methodologies / scenarios, CLI Troubleshooting Cheat Sheet, Administration Guide (SD-WAN, IPsec, VoIP, UTM)
- Fortinet Community Technical Tips (ADVPN+SD-WAN, SIP ALG, routing debug, diagnose application list)
- Практичні збірки CLI (HIFENCE, handbook.fortinet.com.cn тощо)

**Уже покрито (не дублювати):** First steps, Traffic not passing, VPN/IKE, Dial-up, SSL VPN login, SD-WAN member dead, High CPU/mem, Session full, Policy/NAT, VIP, Local-in, HA, OSPF, BGP, Static/RIB, DHCP, Auth/FSSO, DNS, Webfilter, IPS/UTM, Explicit proxy, Wireless, LACP, Interface, NPU, Certificate, FortiGuard, Log disk/crashlog, NTP, IPv6, Multicast, ZTNA, FAZ, WAD, DoS, LDAP/RADIUS/TACACS, TAC collect, ARP, Link-monitor, AV, Traffic shaping/QoS.

---

## 2. Пріоритетний backlog (P0 → P2)

### P0 (обов’язково в 0.7.0)

| Назва в UI | Короткий scope | Ключові команди / блоки |
|------------|----------------|-------------------------|
| **ADVPN / Shortcut tunnels** | ADVPN 2.0, shortcut paths, SD-WAN+ADVPN health | `diagnose vpn ike gateway list/summary`, `diagnose sys sdwan advpn`, `diagnose sys sdwan advpn-session`, debug `sdwan` + `ike` + flow |
| **SIP / VoIP / ALG** | SIP ALG, pinholes, RTP, one-way audio | `diagnose debug application sip -1`, session list (expected), sniffer RTP/SIP, helper status |
| **Application Control / ISDB** | App-ctrl hits, internet-service, SD-WAN app steering | `diagnose sys sdwan internet-service-app-ctrl-list`, debug application/urlfilter, session filter |

### P1 (бажано в 0.7.0)

| Назва в UI | Scope |
|------------|--------|
| **Email filter / Antispam** | smtp / emailfilter debug + test application |
| **File filter** | blocking by type/extension |
| **DLP** | fingerprints, sensitivity, debug dlp |
| **Transparent mode / Bridging** | `diagnose netlink brctl`, bridge FDB |
| **Modem / LTE** | `diagnose sys modem`, PPP, signal |
| **VDOM parameter** | опційний `vd` / VDOM selector у більшості recipe |

### P2 (наступний спринт / 0.8.x)

- RIP / RIPng, IS-IS  
- SSL VPN web-mode / portal deep  
- IKEv2 cert / EAP specific  
- Local-out / source selection  
- Session helpers deep  
- Hardware NIC errors deep  
- miglogd / local log search  
- Automation Stitch  
- IoC collection pack  
- Cloud SDN connectors  

---

## 3. Детальні кроки

### 0–1. Gap-аналіз + план (поточний)
- [x] Огляд відкритих playbooks vs 42 існуючих  
- [ ] Цей `RELEASE_6_PLAN.md`  
- [ ] Оновити `doc/INDEX.md`  
- [ ] Запис у `CHANGELOG.md` [Unreleased] **перед** комітом  

### 2. Архітектура
- Новий mixin: `src/ui/tabs/recipe_r6.py` (або розширення `recipe_extra.py` якщо обсяг невеликий).  
- Підключення в `RecipesTab`: `RecipeR6Mixin, RecipeExtraMixin, RecipeImplMixin, BaseTab`.  
- Усі нові методи: `preamble` / `epilogue`, version-aware через `core.fortios_version`, tooltips.  
- Не змінювати сигнатури існуючих helpers без regression.  

### 3. ADVPN / Shortcut tunnels
**Вхідні поля (мінімум):** Phase1/gateway name (opt), member/interface, src/dst для flow.  
**Блоки команд:**
1. Status: `diagnose vpn ike gateway list`, `summary`, optional `info <name>`  
2. SD-WAN ADVPN: `diagnose sys sdwan advpn`, `advpn-session`, `member`, `health-check`  
3. Live debug (optional toggle): reset → `diagnose debug application ike -1` + `sdwan -1` + timestamp → enable  
4. Flow (optional): filter + trace-start  
5. Epilogue: disable + reset  
**Version notes:** перевірити різницю `sys sdwan` vs старі `virtual-wan-link` (у нас уже є helpers).  
**Regression:** існуючий «SD-WAN member dead» і VPN recipes.  

### 4. SIP / VoIP / ALG
**Поля:** src/dst, SIP port (5060 default), interface.  
**Блоки:**
1. Session filter + list (шукати expected / pinhole)  
2. `diagnose debug application sip -1` + enable  
3. Sniffer: SIP (udp/tcp 5060) + RTP range hint  
4. Helper / ALG status якщо доступно  
5. Epilogue  
**Regression:** session helpers, sniffer, flow.  

### 5. Application Control / ISDB
**Поля:** app name/id (opt), src/dst.  
**Блоки:**
1. `diagnose sys sdwan internet-service-app-ctrl-list` (+ filter by app-id якщо є)  
2. Session list з UTM/app info  
3. Debug application / related  
4. Optional flow  
**Regression:** IPS/UTM, Webfilter, SD-WAN.  

### 6–9. P1 recipes
- Email filter: debug `emailfilter` / `smtp`, test application.  
- File filter + DLP: можна один combined recipe «File filter / DLP» на старті, потім рознести.  
- Transparent: `diagnose netlink brctl name host root.b` (і аналоги), list bridges.  
- Modem: `get system modem` / `diagnose sys modem` + link-monitor якщо є.  
- VDOM: глобальний optional selector у RecipesTab → передавати в filter `vd` / context.  

### 10–11. Regression і тести
Після **кожного** recipe:
- [ ] Recipes tab відкривається  
- [ ] Генерація без traceback  
- [ ] Існуючі 42 назви в списку + dispatch  
- [ ] Version selector 6.4 / 7.0 / 7.2 / 7.4 / 7.6 не ламає синтаксис  
- [ ] `pytest` (нові + старі test_*)  

### 12–13. Документація і реліз
- Оновити README (кількість recipes, приклади ADVPN/SIP).  
- Bump версії 0.7.0.  
- INDEX.md — статус цього плану → Done після закриття.  

---

## 4. Критерії готовності Release 6

- [ ] Мінімум 3 P0 recipes (ADVPN, SIP, App Control) у UI і в dispatch  
- [ ] P1: щонайменше 2 з 5 (Email/File-DLP/Transparent/Modem/VDOM)  
- [ ] Жодної регресії на існуючих 42  
- [ ] CHANGELOG, INDEX, README оновлені  
- [ ] Теги / CI зелені (якщо pytest у workflow)

---

## 5. Ризики

| Ризик | Міра |
|-------|------|
| Різниця синтаксису FortiOS 6.x vs 7.x/8.x для sdwan/advpn | Використовувати існуючі `fortios_version` helpers; fallback-коментарі в output |
| Занадто довгі debug-блоки | Toggle «Include live debug» (default off для важких) |
| Роздуття `recipes.py` | Окремий mixin `recipe_r6.py` |
| Stub’и з R5 | Не чіпати, поки не буде окремого restore-завдання |

---

## 6. Порядок виконання (рекомендований)

1. Закрити крок 1 (план + INDEX + CHANGELOG) — **зараз**  
2. Mixin + каркас dispatch  
3. ADVPN → regression  
4. SIP → regression  
5. App Control → regression  
6. 1–2 P1 на вибір  
7. Тести + README + bump  

---

*Оновлено: 2026-09-06*
