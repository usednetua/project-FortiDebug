# FortiDebug Builder (Windows)

GUI для складання CLI-команд діагностики FortiGate.

**Версія:** 0.11.0 (Release 10)

## Можливості

### Глобальні перемикачі
- **FortiOS** 6.0–8.0 · **VDOM mode** + **VDOM map** (Settings)
- Global-scope tabs (HA / System Top / Hardware / TAC) без VDOM-wrap

### Вкладки
Recipes (**55**), Sessions, Flows, VPN, SD-WAN, Routing, TAC, …

### Recipes (виділене)
- **R8:** RIP · SSL web-mode · VDOM map
- **R9:** IS-IS · Automation Stitch
- **R10:** IoC / Threat feed · Cloud SDN connector

## Встановлення

```bash
pip install -r requirements.txt
python src/main.py
```

## CI Release

```bash
git tag v0.11.0 && git push origin v0.11.0
```

## Документація

**[doc/INDEX.md](doc/INDEX.md)** · `CHANGELOG.md`
