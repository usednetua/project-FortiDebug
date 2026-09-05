# FortiDebug Builder (Windows)

GUI для складання CLI-команд діагностики FortiGate.

**Версія:** 0.5.1

## Можливості

Recipes, Sessions, Ping/Traceroute, Sniffer, Flows, Network, Policy Lookup (version-aware), VPN (IKE version-aware + SSL), App Debug, DHCP, SD-WAN (6.x virtual-wan-link / 7.4+ service4), Auth/FSSO, UTM/IPS, Wireless/CAPWAP, Hardware/NPU, System Top, HA, Routing, TAC, SSH Logger, Saved, Settings, About.

Глобально: FortiOS 6.0–8.0 selector, safety-блоки, tooltips, config persist, scrollable UI.

## Встановлення

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

## Збірка .exe

```bash
pip install pyinstaller
python scripts/generate_icon.py
pyinstaller build.spec
```

Результат: `dist/FortiDebugBuilder.exe`

## Тести

```bash
pip install pytest
pytest tests/ -q
```

## Документація

- `doc/PLAN.md`, `RELEASE_2_PLAN.md`, `RELEASE_3_PLAN.md`, `RELEASE_4_PLAN.md`
- `CHANGELOG.md`
