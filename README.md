# FortiDebug Builder (Windows)

GUI для складання CLI-команд діагностики FortiGate.

**Версія:** 0.5.0

## Можливості

Recipes, Sessions, Ping/Traceroute, Sniffer, Flows, Network, Policy Lookup, VPN (IKE version-aware + SSL), App Debug, DHCP, SD-WAN, Auth/FSSO, UTM/IPS, **Wireless/CAPWAP**, **Hardware/NPU**, System Top, HA, Routing, TAC, SSH Logger, Saved, Settings, About.

Глобально: FortiOS 6.0–8.0, safety-блоки, tooltips, config persist, scrollable UI.

## Встановлення

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

## Збірка .exe

```bash
python scripts/generate_icon.py
pyinstaller build.spec
```

## Документація

- `doc/PLAN.md`, `RELEASE_2_PLAN.md`, `RELEASE_3_PLAN.md`, `RELEASE_4_PLAN.md`
- `CHANGELOG.md`
