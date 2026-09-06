# FortiDebug Builder (Windows)

GUI для складання CLI-команд діагностики FortiGate.

**Версія:** 0.10.0 (Release 9)

## Можливості

### Глобальні перемикачі (sidebar)
- **FortiOS** 6.0–8.0 — version-aware синтаксис
- **VDOM mode** — `config vdom` / `edit <name>`; Sessions/Flows `filter vd`
  - Global scope: HA / System Top / Hardware / TAC без wrap
  - **VDOM map** (Settings): `name=index`

### Вкладки
Recipes (**53** playbooks), Sessions, Ping/Traceroute, Sniffer, Flows, Network, Policy Lookup, VPN, App Debug, DHCP, SD-WAN, Auth/FSSO, UTM/IPS, Wireless, Hardware/NPU, System Top, HA, Routing, TAC, SSH Logger, Saved, Settings, About.

### Recipes (виділене)
- **R6–R7:** ADVPN, SIP, AppCtrl, OSPF/BGP, NPU, …
- **R8:** RIP · SSL VPN web-mode · VDOM map
- **R9:** IS-IS neighbor / LSP · Automation Stitch

## Встановлення

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

## Збірка .exe / CI Release

```bash
pyinstaller build.spec
# або:
git tag v0.10.0 && git push origin v0.10.0   # → GitHub Actions EXE + Release
```

## Тести

```bash
pip install pytest && pytest tests/ -q
```

## Документація

**[doc/INDEX.md](doc/INDEX.md)** · `CHANGELOG.md` · `doc/RELEASE_9_PLAN.md` ✅
