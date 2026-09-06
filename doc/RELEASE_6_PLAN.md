# FortiDebug Builder — Release 6 Plan

**Цільова версія:** 0.7.0  
**Старт:** 2026-09-06  
**Тема спринту:** відкриті (публічні) рецепти / playbooks, які ще не реалізовані в додатку

---

## Статус (таблиця кроків)

| # | Крок | Стан | Пріоритет | Примітки |
|---|------|------|-----------|----------|
| 0 | Gap-аналіз відкритих рецептів (огляд) | ✅ Done | P0 | 2026-09-06 |
| 1 | План Release 6 + INDEX + CHANGELOG | ✅ Done | P0 | |
| 2 | Mixin-структура (`recipe_r6.py`) | ✅ Done | P0 | `RecipeR6Mixin` |
| 3 | Recipe: **ADVPN / Shortcut tunnels** | ✅ Done | P0 | version-aware sdwan/ike |
| 4 | Recipe: **SIP / VoIP / ALG** | ✅ Done | P0 | sip debug + sniffer |
| 5 | Recipe: **Application Control / ISDB** | ✅ Done | P0 | app-ctrl-list 7.0+ |
| 6 | Recipe: **Email filter / Antispam** | ⬜ Todo | P1 | |
| 7 | Recipe: **File filter + DLP** | ⬜ Todo | P1 | |
| 8 | Recipe: **Transparent mode / Bridging** | ⬜ Todo | P1 | |
| 9 | Recipe: **Modem / LTE / PPP** | ⬜ Todo | P1 | |
| 10 | Recipe: **VDOM-aware wrappers** | ⬜ Todo | P1 | |
| 11 | Regression «не зламай!» | ⬜ Todo | P0 | smoke на 45 + helpers |
| 12 | Тести (pytest) на нові генератори | ⬜ Todo | P1 | |
| 13 | README + bump 0.7.0 + INDEX | ⬜ Todo | P0 | після P1 або якщо реліз лише P0 |

---

## 1. Контекст і джерела

Поточний стан: **45 playbooks** (42 + 3 R6 P0).

Відкриті джерела gap-аналізу:
- Fortinet Document Library: Troubleshooting methodologies / scenarios, CLI Troubleshooting Cheat Sheet, Administration Guide (SD-WAN, IPsec, VoIP, UTM)
- Fortinet Community Technical Tips (ADVPN+SD-WAN, SIP ALG, routing debug, diagnose application list)
- Практичні збірки CLI (HIFENCE, handbook.fortinet.com.cn тощо)

**Уже покрито:** First steps, Traffic not passing, VPN/IKE, Dial-up, SSL VPN login, SD-WAN member dead, High CPU/mem, Session full, Policy/NAT, VIP, Local-in, HA, OSPF, BGP, Static/RIB, DHCP, Auth/FSSO, DNS, Webfilter, IPS/UTM, Explicit proxy, Wireless, LACP, Interface, NPU, Certificate, FortiGuard, Log disk/crashlog, NTP, IPv6, Multicast, ZTNA, FAZ, WAD, DoS, LDAP/RADIUS/TACACS, TAC collect, ARP, Link-monitor, AV, Traffic shaping/QoS, **ADVPN, SIP/VoIP, App Control/ISDB**.

---

## 2. Пріоритетний backlog (P0 → P2)

### P0 — ✅ shipped у коді (2026-09-06)

| Назва в UI | Файл |
|------------|------|
| ADVPN / Shortcut tunnels | `recipe_r6._advpn` |
| SIP / VoIP / ALG | `recipe_r6._sip_voip` |
| Application Control / ISDB | `recipe_r6._app_control` |

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

## 3. Детальні кроки (коротко)

### 2–5. Виконано
- `src/ui/tabs/recipe_r6.py` + wiring у `recipes.py`  
- Helpers: існуючі `_sniffer`, `_session_block`, `_flow_block`, `sdwan_*`, `ike_*`, preamble/epilogue  

### 6–10. P1 (наступні)
- Email / File+DLP / Transparent / Modem / VDOM — той самий mixin або `_p1` методи в `recipe_r6.py`  

### 11–13. Закриття
- Regression + pytest + README / version bump  

---

## 4. Критерії готовності Release 6

- [x] Мінімум 3 P0 recipes у UI і в dispatch  
- [ ] P1: щонайменше 2 з 5  
- [ ] Жодної регресії на існуючих  
- [ ] CHANGELOG, INDEX, README оновлені  
- [ ] Теги / CI зелені (якщо pytest у workflow)

---

## 5. Ризики

| Ризик | Міра |
|-------|------|
| Синтаксис 6.x vs 7.x для sdwan/advpn | `fortios_version` helpers + коментарі-fallback |
| Довгі debug-блоки | зараз завжди з epilogue; пізніше toggle |
| Stub’и з R5 | не чіпаємо в цьому спринті |

---

*Оновлено: 2026-09-06*
