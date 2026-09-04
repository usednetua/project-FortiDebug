# FortiDebug Builder — Release 2 Plan

**Мета:** збагатити додаток згідно з офіційними рекомендаціями Fortinet щодо безпечного та ефективного debug.

Джерела: Fortinet Document Library (debug flow, sniffer, CLI cheat sheet), Community Technical Tips.

---

## 1. Ключові принципи Fortinet (обов’язкові)

1. **Завжди** `diagnose debug reset` + `filter clear` перед стартом.
2. **Завжди** вузький фільтр (IP/port/proto) — без фільтра debug на завантаженому пристрої = flood.
3. **Завжди** `diagnose debug console timestamp enable`.
4. **Завжди** ліміт `trace start <N>` (за замовч. 100–1000).
5. **Завжди** після роботи: `diagnose debug disable` + `diagnose debug reset`.
6. `diagnose debug disable` **не** зупиняє фоновий debug — потрібен `reset`.
7. Real-time debug — CPU-intensive; default duration 30 хв, можна `diagnose debug duration 0`.
8. Перед стартом корисно: `diagnose debug info`.

---

## 2. Що додаємо в Release 2

### 2.1. Глобальні покращення (усі вкладки з debug)
- [ ] Примусовий блок **Reset + Clear filters** (за замовч. увімкнено, не вимикати).
- [ ] Примусовий **stop-debug** блок в кінці (disable + reset).
- [ ] Опція `diagnose debug info` на початку.
- [ ] Опція `diagnose debug duration <min|0>`.
- [ ] Опція `diagnose debug console timestamp enable` (вже є в Flows — поширити).
- [ ] Попередження в UI: «Debug навантажує CPU. Використовуй фільтри».

### 2.2. Flows — розширення
- [ ] `diagnose debug flow show function-name enable`
- [ ] `diagnose debug flow show iprope enable`
- [ ] IPv6: `filter6` / `trace start6`
- [ ] Фільтр `addr` (будь-яка сторона) на додачу до saddr/daddr
- [ ] `diagnose debug flow filter clear` явно
- [ ] Preset-кнопки: «Traffic denied», «NAT check», «Policy match»

### 2.3. Sessions — розширення
- [ ] IPv6: `diagnose sys session6 filter/list`
- [ ] `diagnose sys session clear` (з підтвердженням)
- [ ] `diagnose sys session stat` / `full-stat`
- [ ] Filter: `policy`, `ext-sip`, `ext-dip`, `duration` тощо (поширені)

### 2.4. Sniffer — розширення
- [ ] Timestamp format (`a` / `l` / `none`)
- [ ] IPv6 host у простому фільтрі
- [ ] Збереження кастомних BPF у JSON (AppData)
- [ ] Preset: «SYN only», «HTTP/S», «DNS», «IKE/ESP»

### 2.5. VPN — розширення
- [ ] Сучасний синтаксис: `diagnose vpn ike log filter` (без дефіса, v7.4.1+)
- [ ] Filter: `rem-addr4`, `name`, `interface`
- [ ] `diagnose vpn ike log filter clear`
- [ ] `diagnose vpn tunnel list name <p2>`
- [ ] Phase1/Phase2 status + stats

### 2.6. Нова вкладка: **Application Debug**
Поширені демони:
- authd (authentication / SSL VPN / FSSO)
- dnsproxy
- ike (вже частково у VPN)
- sslvpn
- miglogd / fgtlogd (logging)
- urlfilter / wad (web proxy)
- sip / voip

UI: вибір daemon + level (-1 / 0..255) + filter (де є) + standard start/stop block.

### 2.7. Нова вкладка / секція: **TAC / Support**
- `execute tac report`
- `diagnose debug report`
- `get system status`
- `get system performance status`
- `diagnose debug crashlog read`
- Швидкий «Support bundle» — набір команд для тікета.

### 2.8. Нова вкладка: **Recipes / Workflows**
Готові сценарії (1 клік → повний набір команд):
1. **Traffic not passing** — session + flow + sniffer skeleton
2. **VPN down / rekey** — ike filter + tunnel list + ike debug
3. **High CPU** — sys top + performance status + crashlog
4. **Policy / NAT check** — flow з iprope + session filter
5. **HA out-of-sync** — checksum + hasync debug
6. **DNS issues** — dnsproxy debug + session dns

### 2.9. UX / якість
- [ ] Tooltips з поясненням «навіщо ця опція» (з документації)
- [ ] Валідація IP/port перед генерацією
- [ ] Кнопка «Copy stop-debug only»
- [ ] Темна тема за замовч. для «термінального» вигляду
- [ ] Гарячі клавіші: Ctrl+Enter = Copy, Ctrl+S = Save txt

### 2.10. Збірка / документація
- [ ] Оновити README з прикладами workflow
- [ ] build.spec для іконки + version
- [ ] CHANGELOG.md

---

## 3. Порядок реалізації (пріоритет)

| Етап | Що | Дні |
|------|-----|-----|
| 1 | Глобальні safety-блоки (reset/clear/stop) у всіх debug-вкладках | 1 |
| 2 | Flows v2 (function-name, iprope, IPv6, presets) | 1–2 |
| 3 | Recipes / Workflows (6 сценаріїв) | 1–2 |
| 4 | Application Debug tab | 1–2 |
| 5 | Sessions + Sniffer + VPN enrichment | 1–2 |
| 6 | TAC / Support helper | 0.5 |
| 7 | UX polish + валідація + hotkeys | 1 |
| 8 | README / CHANGELOG / build | 0.5 |

**Оцінка:** 7–11 робочих днів.

---

## 4. Критерії готовності Release 2

- Будь-який згенерований debug-блок можна безпечно вставити на production (має reset + filter + limit + stop).
- Є ≥ 5 готових Recipes під типові інциденти.
- IPv6 підтримується у Flow і Sessions.
- Application Debug покриває authd, dnsproxy, ike, sslvpn.
- Документація оновлена.

---

*Створено: 2026-09-04*  
*На основі: Fortinet docs (debug flow, sniffer, CLI cheat sheet) + Community Technical Tips*
