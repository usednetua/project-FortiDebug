# FortiDebug Builder (Windows)

GUI для складання CLI-команд діагностики FortiGate.

**Версія:** 0.12.0 (Release 11)

## Можливості

- **FortiOS** 6.0–8.0 · **VDOM mode** + **VDOM map** (Settings)
- Global-scope: HA / System Top / Hardware / TAC без VDOM-wrap
- **Recipes: 57** playbooks (BFD, SAML, IoC, Cloud SDN, IS-IS, …)

## Встановлення

```bash
pip install -r requirements.txt
python src/main.py
```

## CI Release

```bash
git tag v0.12.0 && git push origin v0.12.0
```

## Документація

**[doc/INDEX.md](doc/INDEX.md)** · `CHANGELOG.md`
