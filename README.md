# FortiDebug Builder (Windows)

GUI для складання CLI-команд діагностики FortiGate.

**Версія:** 0.8.0 (Release 7)

## Можливості

### Глобальні перемикачі (sidebar)
- **FortiOS** 6.0–8.0 — version-aware синтаксис (IKE, SD-WAN, ZTNA, …)
- **VDOM mode** — multi-VDOM: `config vdom` / `edit <name>` … `end`; Sessions/Flows `filter vd`
  - **Global scope:** HA, System Top, Hardware, TAC (і частина recipes) **не** обгортаються в VDOM-контекст

### Вкладки
Recipes (**49** playbooks, усі з повними тілами), Sessions, Ping/Traceroute, Sniffer, Flows, Network, Policy Lookup, VPN (IKE + SSL), App Debug, DHCP, SD-WAN, Auth/FSSO, UTM/IPS, Wireless/CAPWAP, Hardware/NPU, System Top, HA, Routing, TAC, SSH Logger, Saved, Settings, About.

Safety-блоки (preamble/epilogue), tooltips, config persist, export bundle, scrollable UI.

### Recipes (виділене)
- **R6:** ADVPN · SIP/VoIP · App Control/ISDB · Email · File/DLP · Transparent · Modem/LTE
- **R7:** відновлені stubs (OSPF, BGP, DHCP, Wireless, NPU, …) — більше немає `# pending restore`

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

```bash
# 1. Онови CHANGELOG.md (обов'язково перед комітом)
# 2. Закоміть зміни
git tag vX.Y.Z
git push origin main
git push origin vX.Y.Z
```

Після workflow на **Releases** з’явиться `FortiDebugBuilder.exe`.

## Тести

```bash
pip install pytest
pytest tests/ -q
```

## Документація

Єдина точка входу: **[doc/INDEX.md](doc/INDEX.md)**

- `doc/RELEASE_7_PLAN.md` — Release 7 (0.8.0) ✅
- `doc/RELEASE_6_PLAN.md` — Release 6 (0.7.0) ✅
- `doc/CODEX_IMPLEMENTATION.md`
- `CHANGELOG.md`
