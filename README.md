# FortiDebug Builder (Windows)

GUI для складання CLI-команд діагностики FortiGate.

**Версія:** 0.7.0 (Release 6)

## Можливості

### Глобальні перемикачі (sidebar)
- **FortiOS** 6.0–8.0 — version-aware синтаксис (IKE, SD-WAN, ZTNA, …)
- **VDOM mode** — multi-VDOM: `config vdom` / `edit <name>` … `end`; Sessions/Flows `filter vd`

### Вкладки
Recipes (**49** playbooks), Sessions, Ping/Traceroute, Sniffer, Flows, Network, Policy Lookup, VPN (IKE + SSL), App Debug, DHCP, SD-WAN, Auth/FSSO, UTM/IPS, Wireless/CAPWAP, Hardware/NPU, System Top, HA, Routing, TAC, SSH Logger, Saved, Settings, About.

Safety-блоки (preamble/epilogue), tooltips, config persist, export bundle, scrollable UI.

### Recipes Release 6 (нові)
ADVPN / Shortcut · SIP / VoIP / ALG · Application Control / ISDB · Email filter · File filter / DLP · Transparent / Bridging · Modem / LTE / PPP

## Встановлення (з джерела)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

## Збірка .exe локально

```bash
pip install pyinstaller
python scripts/generate_icon.py
pyinstaller build.spec
```

Результат: `dist/FortiDebugBuilder.exe`

## Автоматичний реліз (GitHub Actions)

CI збирає Windows `.exe` і створює GitHub Release при пуші тегу:

```bash
# 1. Онови CHANGELOG.md (обов'язково перед комітом)
# 2. Закоміть зміни
git add CHANGELOG.md
git commit -m "chore: prepare vX.Y.Z"

# 3. Створи і запуш тег
git tag vX.Y.Z
git push origin main
git push origin vX.Y.Z
```

Після успішного workflow на **Releases** з’явиться `FortiDebugBuilder.exe`.

Можна також запустити workflow вручну (Actions → Build Windows EXE → Run workflow) — artifact без Release.

## Тести

```bash
pip install pytest
pytest tests/ -q
```

## Документація

Єдина точка входу: **[doc/INDEX.md](doc/INDEX.md)**

- `doc/RELEASE_6_PLAN.md` — Release 6 (0.7.0) ✅
- `doc/CODEX_IMPLEMENTATION.md` — кодекс впровадження
- `CHANGELOG.md`
