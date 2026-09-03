# FortiDebug Builder (Windows) — Максимально детальний покроковий план

## 1. Мета
Windows-аналог macOS FortiDebug Builder.
GUI для візуального складання CLI-команд діагностики FortiGate (Sessions, Ping, Traceroute, Sniffer, Flows, VPN, System Top, HA, Routing + Saved).

## 2. Стек
- Python 3.11+
- GUI: CustomTkinter (темна/світла тема, сучасний вигляд)
- Зберігання: SQLite (команди) + JSON (налаштування, кастомні інтерфейси)
- Clipboard: pyperclip
- Пакування: PyInstaller → один .exe
- Git + цей приватний репозиторій

Альтернатива (якщо нативність критична): C# + WPF/.NET 8.

## 3. Структура репозиторію (цільова)
```
project-FortiDebug/
├── doc/
│   └── PLAN.md
├── src/
│   ├── main.py
│   ├── app.py                  # Application class
│   ├── ui/
│   │   ├── main_window.py
│   │   ├── sidebar.py
│   │   ├── preview_panel.py
│   │   ├── tabs/
│   │   │   ├── base_tab.py
│   │   │   ├── sessions.py
│   │   │   ├── ping.py
│   │   │   ├── traceroute.py
│   │   │   ├── sniffer.py
│   │   │   ├── flows.py
│   │   │   ├── vpn.py
│   │   │   ├── system_top.py
│   │   │   ├── ha.py
│   │   │   ├── routing.py
│   │   │   └── saved.py
│   │   └── widgets/
│   │       ├── ip_entry.py
│   │       ├── port_entry.py
│   │       ├── protocol_combo.py
│   │       ├── bpf_builder.py
│   │       └── interface_selector.py
│   ├── core/
│   │   ├── command_builder.py
│   │   ├── models.py
│   │   ├── storage.py
│   │   └── validators.py
│   └── resources/
│       └── icons/
├── tests/
│   ├── test_sessions.py
│   ├── test_sniffer.py
│   └── ...
├── requirements.txt
├── .gitignore
├── README.md
└── build.spec
```

## 4. Покроковий план (детально)

### Крок 0. Підготовка середовища (0.5 дня)
1. Встановити Python 3.11+ з python.org (додати в PATH).
2. `python -m venv venv`
3. Активувати: `venv\Scripts\activate`
4. `pip install customtkinter pyperclip pyinstaller`
5. Створити `.gitignore`:
   ```
   venv/
   __pycache__/
   *.pyc
   dist/
   build/
   *.spec
   .idea/
   .vscode/
   *.db
   ```
6. Ініціалізувати структуру папок у `src/`.

### Крок 1. Точка входу + каркас вікна (1 день)
1. `main.py`:
   ```python
   import customtkinter as ctk
   from ui.main_window import MainWindow

   if __name__ == "__main__":
       ctk.set_appearance_mode("System")
       ctk.set_default_color_theme("blue")
       app = MainWindow()
       app.mainloop()
   ```
2. `MainWindow` (CTk):
   - Sidebar (ліва панель) зі списком секцій (CTkSegmentedButton або CTkOptionMenu + кнопки).
   - Центральна область: динамічний фрейм для активної вкладки.
   - Нижня панель (preview + кнопки):
     - CTkTextbox (readonly) для згенерованих команд.
     - Кнопки: Copy, Save .txt, Save for Later.
3. Перемикання вкладок через словник `self.tabs = {"sessions": SessionsTab(...), ...}`.
4. Метод `update_preview(text: str)`.

### Крок 2. Базовий клас вкладки + валідатори (0.5 дня)
1. `BaseTab(CTkFrame)`:
   - `build_ui()`
   - `generate_commands() -> str`
   - `validate() -> bool`
2. `validators.py`:
   - `is_valid_ip(s)` (IPv4/IPv6)
   - `is_valid_port(s)` (1-65535)
   - `is_valid_vdom(s)` (int)

### Крок 3. Diagnose Sessions (1 день)
Поля (сітка CTkLabel + CTkEntry/CTkComboBox/CTkCheckBox):
- Source IP, Destination IP
- Source Port, Destination Port
- Protocol: TCP(6), UDP(17), ICMP(1), GRE(47), ESP(50), Any
- VDOM index
- Negate filter
- Include session stats
- Append session list

Логіка генерації:
```
diagnose sys session filter clear
[якщо src] diagnose sys session filter src <ip>
[якщо dst] diagnose sys session filter dst <ip>
[якщо sport] diagnose sys session filter sport <port>
[якщо dport] diagnose sys session filter dport <port>
[якщо proto != Any] diagnose sys session filter proto <num>
[якщо vdom] diagnose sys session filter vd <idx>
[якщо negate] diagnose sys session filter negate enable
[якщо stats] diagnose sys session stat
[якщо list] diagnose sys session list
```

### Крок 4. Ping (1 день)
Опції `exec ping-options`:
- source <ip>
- interface <name>
- df-bit {yes|no}
- data-size <bytes> (за замовч. 56, для MTU 1472)
- adaptive {enable|disable}
- timeout / interval / repeat-count
+ checkbox «Show view-settings»
+ host

Генерація:
```
exec ping-options source ...
...
exec ping-options view-settings   # якщо увімкнено
exec ping <host>
```

### Крок 5. Traceroute (0.5 дня)
Аналогічно Ping:
- interface
- queries-per-hop
- max-ttl
- source
+ host

### Крок 6. Sniffer (2–3 дні) — пріоритетний складний модуль
1. InterfaceSelector:
   - CTkComboBox з пресетами (port1, port2, any, vlan100...)
   - кнопка «Add Custom» → зберігає в JSON
2. Verbose: CTkOptionMenu 0–6 з підказками.
3. Простий фільтр (якщо toggle off):
   - Host / Network / Port / Protocol + src/dst/either
4. BPF Builder (toggle on):
   - Presets: TCP SYN, TCP RST, New TCP, ICMP, ARP, VLAN, IPv6, Broadcast, Multicast
   - Snippet constructor:
     - type (host/network/port/protocol/ether host/vlan/tcp flag/icmp type/...)
     - value
     - Negate, Wrap in parens
     - Combine with AND/OR
     - Add to filter / Clear
5. Генерація:
   `diagnose sniffer packet <intf> '<bpf>' <verbose> [<count>]`

### Крок 7. Flows (1 день)
- Reset debug state (checkbox, за замовч. on)
- src/dst address, port, protocol filters
- Trace count (default 1000)
- Console timestamps
- Append stop-debug block (за замовч. on)

Команди:
```
diagnose debug reset
diagnose debug flow filter ...
diagnose debug flow show console enable
diagnose debug flow trace-start <count>
...
diagnose debug disable
```

### Крок 8. VPN (1 день)
- Phase1 name / Phase2 name / Peer IPv4
- IKE debug level (-1 за замовч.)
- Status commands + live debug block

### Крок 9. System Top + HA + Routing (2 дні)
**System Top**:
- top / top-summary / top-mem / top-io
- delay, max lines
- companion: performance status, hardware info, conserve-mode

**HA**:
- status, checksums, full dump
- force sync, reset uptime, manage unit
- hatalk / hasync debug

**Routing**:
- OSPF (status/neighbors/interfaces/LSDB/routes + live debug)
- BGP (summary, neighbor routes, advertised, network, live debug)
- Static / RIB / proute / lookup destination

### Крок 10. Saved Commands (1–1.5 дні)
1. `storage.py`:
   - SQLite: `CREATE TABLE commands (id INTEGER PRIMARY KEY, title TEXT, category TEXT, notes TEXT, command TEXT, created_at TEXT)`
2. UI:
   - Список (CTkScrollableFrame або Treeview)
   - Пошук (фільтр по title/category/notes/command)
   - Edit / Delete / Copy / Export
   - Context menu (правою кнопкою)
3. «Save for Later» з будь-якої вкладки → діалог title + notes + category.

### Крок 11. Налаштування і персистентність (0.5 дня)
- `%APPDATA%\FortiDebugBuilder\config.json`
- theme, last used tab, custom interfaces, window size/position

### Крок 12. Тестування (1.5–2 дні)
- Unit-тести генераторів (pytest)
- Ручне тестування всіх комбінацій полів
- Валідація порожніх/некоректних вводів
- Темна/світла тема
- Гарячі клавіші: Ctrl+C (copy), Ctrl+S (save txt), Ctrl+L (save later)

### Крок 13. Збірка .exe (0.5–1 день)
```bash
pyinstaller --onefile --windowed --name FortiDebugBuilder --icon=resources/icon.ico src/main.py
```
або через `build.spec`.

### Крок 14. Документація і фініш (1 день)
- README.md (українською + англійською)
- Скріншоти
- Changelog
- Ліцензія (MIT або власна)

## 5. Порядок пріоритетів (MVP → Full)
1. Каркас + Sessions + Ping + Sniffer + Preview + Copy/Save
2. Saved Commands
3. Flows + VPN
4. System Top + HA + Routing
5. Polish + .exe

## 6. Оцінка часу (один розробник)
- MVP: 6–8 робочих днів
- Повний функціонал: 12–16 робочих днів

## 7. Наступні дії прямо зараз
1. Створити `requirements.txt`
2. Створити базову структуру папок і `main.py` + `MainWindow`
3. Реалізувати Sessions як перший робочий модуль

---
Оновлено: 2026-09-03
