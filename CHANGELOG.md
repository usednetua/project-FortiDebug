# Changelog

Усі значущі зміни проекту FortiDebug Builder (Windows).

Формат базується на [Keep a Changelog](https://keepachangelog.com/).

---

## [Unreleased]

### Planned (Release 2)
- Safety-блоки (reset/clear/stop) у всіх debug-вкладках
- Flows v2: function-name, iprope, IPv6, presets
- Recipes / Workflows (типові інциденти)
- Application Debug tab
- TAC / Support helper
- Див. `doc/RELEASE_2_PLAN.md`

---

## [0.1.0] — 2026-09-03 / 2026-09-04

### Added
- Початкова структура проекту (Python + CustomTkinter)
- **Sessions** — diagnose sys session filter/list/stat
- **Ping** — exec ping-options + exec ping
- **Traceroute** — exec traceroute-options + exec traceroute
- **Sniffer** — diagnose sniffer packet (simple filter + BPF presets)
- **Flows** — diagnose debug flow (reset, filters, trace, stop block)
- **VPN / IKE** — gateway/tunnel list + live IKE debug
- **System Top** — top / top-summary / top-mem / top-io + companion snapshots
- **HA** — status, checksums, sync, hatalk/hasync debug
- **Routing** — OSPF, BGP, Static/RIB, proute, lookup
- **SSH Logger** — генерація команди ssh | Tee-Object / tee з timestamp-логом
- **Saved Commands** — SQLite persistence, search, edit, delete, Save for Later
- Глобальний **перемикач FortiOS** (6.0 → 8.0)
- Version-aware IKE syntax:
  - ≤ 7.2: `diagnose vpn ike log-filter` + `dst-addr4` / `src-addr4`
  - ≥ 7.4.1: `diagnose vpn ike log filter` + `rem-addr4` / `loc-addr4`
- `doc/PLAN.md` — детальний план розробки
- `doc/RELEASE_2_PLAN.md` — план наступного релізу (на базі Fortinet debug best practices)
- `.gitignore`, `requirements.txt`, `README.md`

### Notes
- Синтаксис IKE перевірено за Fortinet Community / Document Library (зміна з v7.4.1).
- Flow / session / sniffer синтаксис стабільний для 6.0–8.0 у межах поточного функціоналу.
