# FortiDebug Builder (Windows)

GUI для складання CLI-команд діагностики FortiGate.

**Версія:** 0.9.0 (Release 8)

## Можливості

### Глобальні перемикачі (sidebar)
- **FortiOS** 6.0–8.0 — version-aware синтаксис
- **VDOM mode** — `config vdom` / `edit <name>` … `end`; Sessions/Flows `filter vd`
  - **Global scope:** HA, System Top, Hardware, TAC без VDOM-wrap
  - **VDOM map** (Settings): `name=index` для `filter vd`

### Вкладки
Recipes (**51** playbooks), Sessions, Ping/Traceroute, Sniffer, Flows, Network, Policy Lookup, VPN, App Debug, DHCP, SD-WAN, Auth/FSSO, UTM/IPS, Wireless, Hardware/NPU, System Top, HA, Routing, TAC, SSH Logger, Saved, Settings, About.

### Recipes (виділене)
- **R6:** ADVPN · SIP · App Control · Email · File/DLP · Transparent · Modem
- **R7:** повні тіла (OSPF, BGP, NPU, …)
- **R8:** RIP neighbor · SSL VPN web-mode · VDOM name→index map

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

## CI Release

```bash
git tag vX.Y.Z
git push origin main && git push origin vX.Y.Z
```

## Тести

```bash
pip install pytest && pytest tests/ -q
```

## Документація

**[doc/INDEX.md](doc/INDEX.md)** · `CHANGELOG.md` · `doc/RELEASE_8_PLAN.md` ✅
