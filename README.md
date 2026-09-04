# FortiDebug Builder (Windows)

GUI для складання CLI-команд діагностики FortiGate (аналог macOS FortiDebug Builder).

**Версія:** 0.4.0

## Можливості

| Модуль | Опис |
|--------|------|
| **Recipes** | Playbooks: traffic, VPN, CPU, NAT, VIP, HA, DNS |
| **Sessions** | session / session6, policy, ext-sip/dip, clear |
| **Ping / Traceroute** | exec ping/traceroute-options |
| **Sniffer** | simple + BPF JSON, IPv6 host |
| **Flows** | debug flow + iprope + IPv6 |
| **Network** | ARP, NIC, IP list, LACP, IPv6 ND |
| **Policy Lookup** | `diagnose firewall iprope lookup` |
| **VPN** | IKE (version-aware) + SSL monitor/list/debug |
| **App Debug** | Realtime + `diagnose test application` |
| **DHCP** | lease-list, sniffer 67/68, dhcprelay |
| **SD-WAN** | health-check, service, member, zone |
| **Auth / FSSO** | auth list, fsso list, authd debug |
| **System Top / HA / Routing** | top, HA, OSPF/BGP/RIB |
| **TAC / Support** | tac report, crashlog, debug cli 7 |
| **SSH Logger** | `ssh \| Tee-Object` |
| **Saved / Settings / About** | SQLite, theme, EN/UK |

Глобально: **FortiOS 6.0–8.0**, safety-блоки, tooltips.

## Встановлення

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

## Збірка .exe

```bash
pyinstaller build.spec
# або:
pyinstaller --onefile --windowed --name FortiDebugBuilder --paths src src/main.py
```

## Документація

- `doc/PLAN.md`, `doc/RELEASE_2_PLAN.md`, `doc/RELEASE_3_PLAN.md`
- `CHANGELOG.md`

## Безпека debug

```
diagnose debug disable
diagnose debug reset
```
