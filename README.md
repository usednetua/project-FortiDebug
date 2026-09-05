# FortiDebug Builder (Windows)

GUI для складання CLI-команд діагностики FortiGate.

**Версія:** 0.5.1

## Можливості

Recipes, Sessions, Ping/Traceroute, Sniffer, Flows, Network, Policy Lookup (version-aware), VPN (IKE version-aware + SSL), App Debug, DHCP, SD-WAN (6.x virtual-wan-link / 7.4+ service4), Auth/FSSO, UTM/IPS, Wireless/CAPWAP, Hardware/NPU, System Top, HA, Routing, TAC, SSH Logger, Saved, Settings, About.

Глобально: FortiOS 6.0–8.0 selector, safety-блоки, tooltips, config persist, scrollable UI.

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
git commit -m "chore: prepare v0.5.2"

# 3. Створи і запуш тег
git tag v0.5.2
git push origin main
git push origin v0.5.2
```

Після успішного workflow на сторінці **Releases** з'явиться `FortiDebugBuilder.exe`.

Можна також запустити workflow вручну (Actions → Build Windows EXE → Run workflow) — тоді буде тільки artifact без Release.

## Тести

```bash
pip install pytest
pytest tests/ -q
```

## Документація

- `doc/PLAN.md`, `RELEASE_2_PLAN.md`, `RELEASE_3_PLAN.md`, `RELEASE_4_PLAN.md`, `RELEASE_5_PLAN.md`
- `CHANGELOG.md`
