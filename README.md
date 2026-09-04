# FortiDebug Builder (Windows)

GUI-інструмент для візуального складання CLI-команд діагностики FortiGate.

Аналог macOS-додатку FortiDebug Builder.

## Можливості
- Diagnose Sessions
- Ping / Traceroute
- Sniffer (з BPF Builder)
- Debug Flow
- VPN IKE
- System Top / HA / Routing
- Saved Commands (SQLite)

## Встановлення
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

## Збірка .exe
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pyinstaller --onefile --windowed --name FortiDebugBuilder src/main.py
```

## Структура
Див. `doc/PLAN.md`
