# FortiDebug Builder — Release 3 Plan

**Мета:** закрити пробіли з офіційних / community FortiGate debug cheatsheet’ів  
(Fortinet CLI Troubleshooting Cheat Sheet, BOLL FOS 7.4/7.6, yuriskinfo diagnose sheet, Community Tips).

**Базова версія:** 0.3.0

---

## Статус (таблиця кроків)

| # | Крок | Стан | Пріоритет | Примітки |
|---|------|------|-----------|----------|
| 1 | Network tab (ARP, NIC, IP list) | ❌ Todo | P0 | Високий ROI, у всіх cheatsheet’ах |
| 2 | Policy lookup (iprope lookup) | ❌ Todo | P0 | Без live traffic |
| 3 | VIP / DNAT recipe + hints | ❌ Todo | P0 | Playbook у Recipes |
| 4 | SSL VPN status + monitor | ❌ Todo | P0 | Розширення VPN tab |
| 5 | diag test application (App Debug) | ❌ Todo | P1 | Поруч із realtime debug |
| 6 | DHCP diagnostics | ❌ Todo | P1 | lease-list, relay test |
| 7 | Interfaces / LACP | ❌ Todo | P1 | aggregate list/name |
| 8 | SD-WAN diagnostics | ❌ Todo | P2 | health-check, service, member |
| 9 | Auth / FSSO list | ❌ Todo | P2 | firewall auth list, fsso |
| 10 | diag debug cli 7 | ❌ Todo | P2 | GUI→CLI changes |
| 11 | UTM / IPS quick debug | ❌ Todo | P3 | filter + debug level |
| 12 | README + CHANGELOG + version bump | ❌ Todo | P0 | на фініші |

**Легенда:** ✅ Done · 🟡 Partial · ❌ Todo  
**Пріоритет:** P0 = наступна ітерація · P1 = скоро · P2/P3 = за потреби

---

## 1. Джерела (перевірені публічно)

1. Fortinet Document Library — *CLI troubleshooting cheat sheet* (FortiOS 8.0).
2. BOLL Engineering — FortiGate Cheatsheet FortiOS 7.4 / 7.6 (PDF + Community post).
3. yuriskinfo — *Fortigate debug and diagnose commands complete cheat sheet* (GitHub).
4. Fortinet Community — Technical Tips (debug flow meaning, VIP, IPv6 session/flow, app debug list).

Принципи debug (як у R2): **reset → filter → limit → enable → stop+reset**; timestamps; вузькі фільтри.

---

## 2. Детальний покроковий план

### Крок 1. Network tab (P0) — 0.5–1 день

**Файл:** `src/ui/tabs/network.py`

**UI (checkboxes + optional interface field):**

| Опція | Команда |
|-------|---------|
| ARP table (get) | `get system arp` |
| ARP table (diag) | `diagnose ip arp list` |
| Clear ARP | `execute clear system arp table` |
| Interface IP list | `diagnose ip address list` |
| NIC hardware info | `get hardware nic <if>` |
| Netlink interfaces | `diagnose netlink interface list` |
| IPv6 neighbor cache | `diagnose ipv6 neighbor-cache list` |

**Логіка:**
- Поле Interface (для NIC) — обов’язкове лише якщо увімкнено NIC info.
- Preview live update як у інших вкладках.
- Підключити в `main_window.py` + i18n ключі (`network`).

**Критерій готовності:** згенерований блок копіюється і виконується на FGT без правок.

---

### Крок 2. Policy lookup (P0) — 0.5 дня

**Файл:** `src/ui/tabs/policy_lookup.py` (або секція в Flows)

**Команда:**
```text
diagnose firewall iprope lookup <src_ip> <src_port> <dst_ip> <dst_port> <proto> <src_intf>
```

**UI поля:**
- Source IP, Source port
- Destination IP, Destination port
- Protocol (TCP/UDP/ICMP/… або номер)
- Source interface (напр. `port1`, `wan1`)

**Валідація:** `is_valid_ip` / `is_valid_port`.

**Tooltip:** «Показує, яка policy матчиться для 5-tuple + intf — без реального трафіку».

**Критерій:** коректний рядок при заповнених обов’язкових полях; підказка якщо порожньо.

---

### Крок 3. VIP / DNAT recipe (P0) — 0.5 дня

**Файл:** `src/ui/tabs/recipes.py` — новий scenario **«VIP / port forward»**

**Шаблон команд (з Community VIP tip):**
1. Sniffer: `diagnose sniffer packet <wan> 'host <client> and port <dport>' 4 0 l`
2. Flow: reset → filter saddr/dport → function-name → iprope → trace start → enable → stop block
3. Session filter dst `<vip>` / dport
4. Коментарі що шукати: `VIP-...`, `DNAT`, `iprope_in_check failed`

**Поля recipe:** client IP, VIP/public IP, port, WAN interface.

---

### Крок 4. SSL VPN у VPN tab (P0) — 0.5–1 день

**Файл:** `src/ui/tabs/vpn.py`

**Додати checkboxes:**

| Опція | Команда |
|-------|---------|
| SSL monitor | `get vpn ssl monitor` |
| SSL list | `diagnose vpn ssl list` |
| SSL web/tunnel stats | `diagnose vpn ssl statistics` (якщо доступно на версії) |
| Live sslvpn debug | `diagnose debug application sslvpn <level>` + safety |

**Примітка:** realtime sslvpn debug уже частково через App Debug; у VPN — зручний status-блок.

---

### Крок 5. diag test application (P1) — 0.5 дня

**Файл:** `src/ui/tabs/app_debug.py`

**Режим:** перемикач **Realtime debug** vs **Test / status**

- Realtime: `diagnose debug application <daemon> <level>` (як зараз)
- Test: `diagnose test application <daemon> <test_level>`

Список популярних daemon + test levels (0–99 типові; підказка «див. ? на FGT»).

---

### Крок 6. DHCP (P1) — 0.5–1 день

**Файл:** `src/ui/tabs/dhcp.py`

| Опція | Команда |
|-------|---------|
| Lease list | `execute dhcp lease-list` |
| DHCP server list | `execute dhcp server list` (за наявності) |
| Relay debug | App debug `dhcprelay` / test |
| Sniffer DHCP | preset `port 67 or port 68` |

Можна як окрема вкладка або секція Network.

---

### Крок 7. Interfaces / LACP (P1) — 0.5 дня

**Розширити Network tab:**

| Опція | Команда |
|-------|---------|
| Aggregate list | `diagnose netlink aggregate list` |
| Aggregate name | `diagnose netlink aggregate name <agg>` |
| Interface transceiver (SFP) | `get system interface transceiver` (де підтримується) |

---

### Крок 8. SD-WAN (P2) — 1 день

**Файл:** `src/ui/tabs/sdwan.py`

| Опція | Команда |
|-------|---------|
| Health-check status | `diagnose sys sdwan health-check` |
| Service | `diagnose sys sdwan service` |
| Member | `diagnose sys sdwan member` |
| Zone | `diagnose sys sdwan zone` |
| Log / neighbor (за версією) | задокументувати в tooltips |

**Важливо:** перевірити синтаксис по FortiOS 7.0–8.0 (selector уже є).

---

### Крок 9. Auth / FSSO (P2) — 0.5 дня

| Опція | Команда |
|-------|---------|
| Auth list | `diagnose firewall auth list` |
| Auth clear (optional, ⚠) | `diagnose firewall auth clear` |
| FSSO list | `diagnose debug authd fsso list` |
| authd debug | вже в App Debug |

---

### Крок 10. diag debug cli (P2) — 0.25 дня

У **App Debug** або **System Top / TAC**:
```text
diagnose debug cli 7
diagnose debug enable
# ...
diagnose debug disable
diagnose debug reset
```
Підказка: показує CLI-еквівалент дій у GUI.

---

### Крок 11. UTM / IPS (P3) — 1 день (опційно)

- `diagnose ips filter` + `diagnose ips debug enable`
- Antivirus / webfilter stats
- Лише якщо є запит; інакше відкласти

---

### Крок 12. Документація і реліз (P0 на фініші)

1. Оновити `CHANGELOG.md` → **0.4.0** (або 0.3.x по етапах).
2. Оновити `README.md` (таблиця модулів).
3. About `APP_VERSION`.
4. Оновити цю таблицю статусів у `RELEASE_3_PLAN.md`.
5. За потреби: unit-тести для policy lookup / network generators.

---

## 3. Порядок реалізації (рекомендований sprint)

| Етап | Кроки | Оцінка |
|------|-------|--------|
| A | 1 Network + 2 Policy lookup | 1–1.5 дні |
| B | 3 VIP recipe + 4 SSL VPN | 1–1.5 дні |
| C | 5 test application + 6 DHCP + 7 LACP | 1.5–2 дні |
| D | 8 SD-WAN + 9 Auth (за потреби) | 1–1.5 дні |
| E | 12 Docs / version | 0.5 дня |

**MVP Release 3:** етапи A + B.  
**Full R3:** A–C + E.

---

## 4. Критерії готовності Release 3 (MVP)

- [ ] Вкладка **Network** генерує ARP / NIC / IP list.
- [ ] **Policy lookup** з валідацією полів.
- [ ] Recipe **VIP / port forward**.
- [ ] VPN: SSL monitor + list (+ optional sslvpn debug).
- [ ] CHANGELOG + README + About version оновлені.
- [ ] Статусна таблиця на початку цього файлу актуальна.

---

## 5. Поза скоупом R3

- Wireless / FortiAP deep debug
- Повний NPU / hardware suite automation
- GUI packet capture automation
- Іконка `.ico` (залишається опційно)

---

*Створено: 2026-09-05*  
*На основі аналізу публічних FortiGate debug cheatsheet’ів*
