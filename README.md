# FortiDebug Builder (Windows)

**GUI для візуального складання CLI-команд діагностики FortiGate.**

Версія: **0.18.2** · Автор: [used.net.ua](https://used.net.ua) · Ліцензія: приватний репозиторій

---

## Що це

FortiDebug Builder — десктопна Windows-програма (Python + CustomTkinter), яка допомагає мережевим інженерам і TAC швидко збирати правильні `diagnose` / `exec` / `get` команди для FortiGate без запам’ятовування синтаксису під конкретну версію FortiOS.

Замість того щоб шукати в документації чи старих нотатках, ви:

1. Обираєте **сценарій** (Recipes) або **модуль** (Sessions, Sniffer, VPN, …).
2. Заповнюєте потрібні поля (IP, інтерфейс, peer, порт…).
3. Бачите готовий блок команд у preview.
4. Копіюєте в буфер, зберігаєте в `.txt` або експортуєте bundle з метаданими.

Програма **не підключається** до FortiGate і **не виконує** команди — лише генерує їх. Ви самі вставляєте результат у SSH/CLI сесію.

---

## Основні можливості

| Категорія | Опис |
|-----------|------|
| **Recipes (85 playbooks)** | Готові сценарії інцидентів: connectivity, VPN, SD-WAN, HA, routing, WiFi/FortiAP, logging, SSL/IPsec remote-user, IoC, Cloud SDN, EVPN, CGNAT тощо |
| **FortiOS 6.0–8.0** | Селектор версії змінює синтаксис (IKE filters, SD-WAN `virtual-wan-link` vs `sdwan`, service/service4…) |
| **VDOM mode** | Обгортання команд у `config vdom` / `edit <name>`; карта ім’я→індекс для `filter vd` |
| **Модулі діагностики** | Sessions, Ping, Traceroute, Sniffer (BPF), Flows, Network, Policy Lookup, VPN, App Debug, DHCP, SD-WAN, Auth/FSSO, UTM/IPS, Wireless, Hardware/NPU, System Top, HA, Routing, TAC, SSH Logger |
| **Збережені команди** | SQLite: title / category / notes, пошук, export |
| **i18n** | Українська + English |
| **UX** | Темна/світла тема, алфавітне сортування меню, scrollable dropdowns (колесо миші), пошук у навігації, гарячі клавіші |

### Recipes (короткий огляд)

- Connectivity / traffic not passing / policy & NAT / VIP  
- VPN (site-to-site, dial-up IPsec, SSL VPN login / web-mode / DTLS / realm / IP pool)  
- SD-WAN, ADVPN, BFD, link-monitor  
- Routing: static/RIB, OSPF, BGP, RIP, IS-IS, EVPN  
- HA out-of-sync, High CPU/memory, session table full  
- DHCP, Auth/FSSO/LDAP/RADIUS/SAML, Captive portal, 802.1X  
- WiFi / FortiAP (offline, associate, 802.1X, roaming, rogue/WIDS, RF)  
- Logging: disk full, syslog, FAZ OFTP, miglogd, traffic/event log  
- UTM/IPS, Webfilter, AV, App Control, DLP, DoS  
- GRE/VXLAN/CGNAT, WebCache/WCCP, LLDP/CDP, Cloud SDN, IoC/Threat feed, Automation Stitch  

Повний список — у вкладці **Recipes** (алфавітно).

### Модулі (вкладки)

- **Sessions** — filter src/dst/port/proto/vd + list/stat  
- **Ping / Traceroute** — source, interface, options  
- **Sniffer** — interface, verbose 0–6, простий фільтр або BPF builder + presets  
- **Flows** — debug flow filter + trace-start + stop-debug  
- **VPN** — IKE log-filter (версійно), phase1/phase2, status  
- **Policy Lookup** — iprope / policy match  
- **SD-WAN / Routing / HA / Hardware / Wireless** — відповідні diagnose-блоки  
- **Saved** — локальна база збережених наборів  
- **Settings** — тема, мова, VDOM map  
- **About** — версія, посилання  

---

## Вимоги

- Windows 10/11 (основна ціль; Linux/macOS — теоретично через той самий Python)  
- Python **3.11+**  
- Залежності: `customtkinter`, `pyperclip`, (для збірки) `pyinstaller`  

```text
customtkinter>=5.2.0
pyperclip>=1.8.2
pyinstaller>=6.0.0
pytest>=7.0.0
```

---

## Встановлення та запуск

### З вихідників

```bash
git clone <repo-url>
cd project-FortiDebug
python -m venv venv
# Windows:
venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

### Готовий .exe (CI)

GitHub Actions збирає Windows one-file EXE при тегу:

```bash
git tag v0.18.2
git push origin v0.18.2
```

Артефакт з’являється в Releases / Actions artifacts.

Локальна збірка:

```bash
pyinstaller build.spec
# або
pyinstaller --onefile --windowed --name FortiDebugBuilder src/main.py
```

---

## Як користуватися (коротко)

1. У sidebar оберіть **FortiOS** (наприклад 7.4.x) і за потреби увімкніть **VDOM mode** + ім’я VDOM.  
2. Відкрийте **Recipes** або потрібний модуль.  
3. Заповніть поля (необов’язкові можна лишити порожніми).  
4. У нижній панелі з’явиться згенерований блок.  
5. **Copy** (або `Ctrl+Enter`) → вставте в CLI FortiGate.  
6. **Copy stop-debug** — швидкий `diagnose debug disable` + `reset`.  
7. **Save .txt** / **Export bundle** — збереження з заголовком (версія app, FortiOS, VDOM, час).  
8. **Save for Later** — у локальну SQLite для повторного використання.  

Налаштування (тема, мова, карта VDOM) зберігаються в `%APPDATA%\FortiDebugBuilder\`.

---

## Структура репозиторію

```text
project-FortiDebug/
├── .github/workflows/build-windows.yml   # CI → Windows EXE
├── doc/                                  # Плани, CODEX, INDEX
│   ├── INDEX.md
│   ├── CODEX_IMPLEMENTATION.md
│   ├── PLAN.md
│   └── RELEASE_*.md / FEATURE_*.md
├── src/
│   ├── main.py
│   ├── core/          # config, i18n, vdom, fortios_version, storage, safety…
│   ├── ui/
│   │   ├── main_window.py
│   │   ├── tabs/      # усі вкладки + recipe_r*.py mixins
│   │   └── widgets/
│   └── resources/
├── scripts/
├── requirements.txt
├── build.spec
├── CHANGELOG.md
└── README.md
```

Розробка ведеться за **Кодексом впровадження** (`doc/CODEX_IMPLEMENTATION.md`): спочатку план у `doc/`, таблиця етапів, принцип «не зламай!», оновлення `doc/INDEX.md`.

---

## Документація

- **[doc/INDEX.md](doc/INDEX.md)** — індекс усіх планів і релізів  
- **[CHANGELOG.md](CHANGELOG.md)** — історія змін (Keep a Changelog)  
- **[doc/PLAN.md](doc/PLAN.md)** — початковий детальний план  
- **[doc/CODEX_IMPLEMENTATION.md](doc/CODEX_IMPLEMENTATION.md)** — обов’язковий процес впровадження  

---

## Гарячі клавіші

| Клавіші | Дія |
|---------|-----|
| `Ctrl+Enter` | Copy commands |
| `Ctrl+S` | Save .txt |
| `Ctrl+E` | Export bundle |

---

## Обмеження та безпека

- Програма **не виконує** команди на FortiGate і не має мережевого доступу до пристрою.  
- Згенеровані debug-команди можуть навантажувати CPU/диск — завжди майте під рукою **Copy stop-debug**.  
- Версійні відмінності синтаксису покриті для основних модулів (IKE, SD-WAN тощо); для дуже старих/нових patch-рівнів перевіряйте `help` на пристрої.  

---

## Розробка

```bash
# тести
pytest

# перед комітом — обов’язково оновити CHANGELOG.md
# при змінах у doc/ — актуалізувати doc/INDEX.md
```

Нові recipes додаються через mixin-файли `recipe_rN.py` + запис у `RecipesTab.RECIPES`.

---

## Автор

**used.net.ua** · [https://used.net.ua](https://used.net.ua)

Windows-аналог macOS FortiDebug Builder. Зворотний зв’язок і пропозиції — через issues / власника репозиторію.
