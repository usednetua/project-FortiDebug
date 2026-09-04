# FortiDebug Builder (Windows)

GUI для складання CLI-команд діагностики FortiGate (аналог macOS FortiDebug Builder).

## Можливості

| Модуль | Опис |
|--------|------|
| **Recipes** | 6 готових playbooks під типові інциденти |
| **Sessions** | `diagnose sys session` / `session6`, clear, full-stat |
| **Ping / Traceroute** | exec ping/traceroute-options |
| **Sniffer** | simple + BPF, timestamp, presets |
| **Flows** | debug flow + iprope + IPv6 + presets |
| **VPN** | IKE gateway/tunnel + live debug (syntax за версією FortiOS) |
| **App Debug** | authd, dnsproxy, sslvpn, miglogd, wad, sip, … |
| **System Top** | top / top-mem / top-summary |
| **HA / Routing** | status, checksums, OSPF/BGP/RIB |
| **TAC / Support** | tac report, crashlog, support bundle |
| **SSH Logger** | `ssh \| Tee-Object` з timestamp-логом |
| **Saved Commands** | SQLite, search, edit |

Глобально: **перемикач FortiOS 6.0–8.0**, safety-блоки (reset / filter clear / stop+reset).

## Встановлення

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

## Гарячі клавіші

- `Ctrl+Enter` — Copy
- `Ctrl+S` — Save .txt

## Збірка .exe

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pyinstaller --onefile --windowed --name FortiDebugBuilder --paths src src/main.py
```

Готовий файл: `dist/FortiDebugBuilder.exe`

## Документація

- `doc/PLAN.md` — початковий план
- `doc/RELEASE_2_PLAN.md` — план Release 2
- `CHANGELOG.md` — історія змін

## Безпека debug

Завжди використовуй фільтри. Після роботи:

```
diagnose debug disable
diagnose debug reset
```
