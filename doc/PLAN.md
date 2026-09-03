# FortiDebug Builder (Windows) — Детальний покроковий план розробки

## 1. Мета проекту
Створити Windows-аналог macOS-додатку FortiDebug Builder.
GUI-інструмент для візуального складання CLI-команд діагностики FortiGate.

## 2. Технологічний стек (рекомендований)
- **Мова**: Python 3.11+
- **GUI**: CustomTkinter (сучасний вигляд) або PyQt6
- **Зберігання**: SQLite (saved commands) + JSON (налаштування)
- **Пакування**: PyInstaller → один .exe
- **Версіонування**: Git + GitHub (цей репозиторій)

Альтернатива: C# + WPF (.NET 8) — якщо потрібен нативний Windows-вигляд.

## 3. Структура репозиторію
```
project-FortiDebug/
├── doc/
│   └── PLAN.md                 ← цей файл
├── src/
│   ├── main.py
│   ├── ui/
│   │   ├── main_window.py
│   │   ├── tabs/
│   │   │   ├── sessions.py
│   │   │   ├── ping.py
│   │   │   ├── traceroute.py
│   │   │   ├── sniffer.py
│   │   │   ├── flows.py
│   │   │   ├── vpn.py
│   │   │   ├── system_top.py
│   │   │   ├── ha.py
│   │   │   └── routing.py
│   │   └── widgets/
│   ├── core/
│   │   ├── command_builder.py
│   │   ├── models.py
│   │   └── storage.py
│   └── resources/
├── tests/
├── requirements.txt
├── README.md
└── build.spec                   # PyInstaller
```

## 4. Покроковий план реалізації

### Крок 1. Ініціалізація проекту (1 день)
1. Створити віртуальне середовище `python -m venv venv`
2. Встановити залежності: `customtkinter`, `sqlite3` (стандарт), `pyperclip`, `pyinstaller`
3. Створити базову структуру папок
4. Написати `main.py` з порожнім вікном CustomTkinter
5. Налаштувати `.gitignore`

### Крок 2. Базовий каркас GUI (1–2 дні)
1. Головне вікно з бічною панеллю (sidebar) або вкладками (tabs)
2. Список секцій:
   - Diagnose Sessions
   - Ping
   - Traceroute
   - Sniffer
   - Flows
   - VPN
   - System Top
   - HA
   - Routing
   - Saved Commands
3. Нижня панель: кнопки **Copy**, **Save to .txt**, **Save for Later**
4. Текстове поле для попереднього перегляду згенерованих команд

### Крок 3. Модуль Diagnose Sessions (1 день)
Поля:
- Source IP / Destination IP
- Source Port / Destination Port
- Protocol (TCP/UDP/ICMP/GRE/ESP/Any)
- VDOM index
- Negate filter (checkbox)
- Include session stats
- Append session list

Генерувати:
```
diagnose sys session filter clear
diagnose sys session filter src ...
diagnose sys session filter dst ...
...
diagnose sys session list
```

### Крок 4. Модуль Ping (1 день)
Опції `exec ping-options`:
- source
- interface
- df-bit
- data-size
- adaptive
- timeout / interval / count
+ `exec ping <host>`
+ опція view-settings

### Крок 5. Модуль Traceroute (0.5 дня)
Аналогічно Ping: `exec traceroute-options` + `exec traceroute`

### Крок 6. Модуль Sniffer (2–3 дні) — найскладніший
1. Поле Interface (з пресетами + можливість додавати свої)
2. Verbose level (0–6)
3. Простий режим фільтра (Host/Network/Port/Protocol + src/dst/either)
4. BPF Builder:
   - Presets (TCP SYN, RST, ICMP, ARP, VLAN...)
   - Конструктор сніпетів
   - AND/OR, negate, parentheses
5. Генерація: `diagnose sniffer packet <intf> '<filter>' <verbose>`

### Крок 7. Модуль Flows (1 день)
- Reset debug state
- Address/Port/Protocol filters
- Trace count
- Console timestamps
- Append stop-debug block

### Крок 8. Модуль VPN (1 день)
- Phase1 / Phase2 name
- Peer IP
- IKE debug level
- Команди status + live debug

### Крок 9. System Top + HA + Routing (2 дні)
Реалізувати всі варіанти команд з оригінального додатку.

### Крок 10. Saved Commands (1 день)
- SQLite таблиця: id, title, category, notes, command, created_at
- Пошук, редагування, видалення, експорт
- Context menu

### Крок 11. Збереження налаштувань і кастомних інтерфейсів
- JSON-файл у `%APPDATA%/FortiDebugBuilder/`

### Крок 12. Тестування і полірування (2 дні)
- Перевірка всіх генераторів
- Обробка помилок вводу
- Темна/світла тема
- Гарячі клавіші (Ctrl+C, Ctrl+S)

### Крок 13. Збірка .exe (1 день)
```bash
pyinstaller --onefile --windowed --name FortiDebugBuilder build.spec
```

### Крок 14. Документація і реліз
- README.md з інструкцією
- Скріншоти
- Changelog

## 5. Порядок пріоритетів
1. Каркас + Sessions + Ping + Sniffer (MVP)
2. Saved Commands
3. Решта модулів
4. Пакування і polish

## 6. Оцінка часу
Повний MVP: 7–10 днів
Повний функціонал: 14–18 днів (один розробник)

---
*Оновлено: 2026-09-03*
