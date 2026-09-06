"""Release 17 — logging / FAZ / syslog / disk / miglogd playbooks."""

from core.safety import preamble, epilogue


class RecipeR17Mixin:
    """Logging diagnostics."""

    def _log_disk_full(self) -> str:
        return "\n".join(
            [
                "# === Recipe: Log disk full / filesystem ===",
                "# Disk full, log age, overwrite, /var/log growth",
                "",
                "get system status",
                "diagnose sys logdisk usage",
                "diagnose hardware deviceinfo disk",
                "diagnose sys flash list",
                "",
                "# Tree of log storage (7.2+)",
                "diagnose sys filesystem tree /var/log",
                "# diagnose sys filesystem last-modified-files",
                "",
                "get log disk setting",
                "# show log disk setting  # maximum-log-age, diskfull overwrite|nolog",
                "",
                "diagnose debug crashlog read",
                "execute log filter dump",
                "",
                "# Free space: delete old reports / quarantine if needed (careful)",
                "# execute log delete-all   # destructive — only if policy allows",
            ]
        )

    def _log_syslog(self, peer: str = "") -> str:
        lines = [
            "# === Recipe: Syslog not received ===",
            "# UDP/TCP 514, filter categories, reliable mode",
            "",
            "get log syslogd setting",
            "get log syslogd filter",
            "# get log syslogd2 setting  # up to syslogd4 on many builds",
            "get log setting",
            "",
            "diagnose log test",
            "",
        ]
        if peer:
            lines += [
                f"# syslog server {peer}",
                f"execute ping {peer}",
                f"execute traceroute {peer}",
                f"# execute telnet {peer} 514",
                f"diagnose sniffer packet any 'host {peer} and port 514' 4 0 l",
            ]
        else:
            lines.append("diagnose sniffer packet any 'port 514' 4 0 l")
        lines.append("")
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose debug application miglogd -1",
            "diagnose debug application fgtlogd -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        lines += [
            "",
            "# Ensure filter enables needed categories (traffic/event/utm…)",
            "# config log syslogd filter",
        ]
        return "\n".join(lines)

    def _log_faz_oftp(self, peer: str = "") -> str:
        lines = [
            "# === Recipe: FAZ OFTP / connectivity deep ===",
            "# OFTP state, cert/SN, queue, test-connectivity",
            "",
            "get log fortianalyzer setting",
            "get log fortianalyzer filter",
            "get log setting",
            "",
            "execute log fortianalyzer test-connectivity",
            "diagnose test application fgtlogd 1",
            "diagnose test application miglogd 6",
            "diagnose test application fgtlogd 4",
            "diagnose test application fgtlogd 5",
            "diagnose log kernel-stats",
            "",
            "diagnose log test",
            "",
        ]
        if peer:
            lines += [
                f"# FAZ {peer}",
                f"execute ping {peer}",
                f"execute traceroute {peer}",
                f"diagnose sniffer packet any 'host {peer} and port 514' 4 0 l",
            ]
        lines.append("")
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose debug application fgtlogd 0x100",
            "diagnose debug application miglogd -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        lines += [
            "",
            "# On FAZ: diagnose debug app oftpd … / test-connectivity from device list",
            "# Registration + matching serial in OFTP handshake",
        ]
        return "\n".join(lines)

    def _log_memory_miglogd(self) -> str:
        return "\n".join(
            [
                "# === Recipe: Memory logging / miglogd ===",
                "# RAM log buffer, miglogd stats by category",
                "",
                "get log memory setting",
                "get log memory global-setting",
                "get log setting",
                "",
                "diagnose test application miglogd 4",
                "diagnose test application miglogd 6",
                "diagnose log kernel-stats",
                "",
                "diagnose sys top 2 20",
                "diagnose sys process pidof miglogd",
                "diagnose sys process pidof fgtlogd",
                "",
                "diagnose log test",
            ]
        )

    def _log_traffic_missing(self, src: str = "", dst: str = "") -> str:
        lines = [
            "# === Recipe: Traffic log missing ===",
            "# Policy log disabled, session not logged, disk/FAZ filter",
            "",
            "get log setting",
            "get log disk filter",
            "get log memory filter",
            "get log fortianalyzer filter",
            "get log syslogd filter",
            "",
            "# Policy must have logtraffic all|utm; logtraffic-start",
            "# show firewall policy",
            "",
            "diagnose test application miglogd 4",
            "diagnose log test",
            "",
            "# Search disk traffic logs (adjust filters)",
            "execute log filter reset",
            "execute log filter device disk",
            "execute log filter category traffic",
        ]
        if src:
            lines.append(f"# execute log filter field srcip {src}")
        if dst:
            lines.append(f"# execute log filter field dstip {dst}")
        lines += [
            "execute log display",
            "",
            "# Real-time:",
            "execute log filter reset",
            "execute log filter category traffic",
            "# execute log display  # or GUI Log & Report",
        ]
        return "\n".join(lines)

    def _log_event_search(self, src: str = "") -> str:
        lines = [
            "# === Recipe: Event log search / filter ===",
            "# Admin login, system events, VPN events on disk",
            "",
            "get log eventfilter",
            "get log setting",
            "",
            "execute log filter reset",
            "execute log filter device disk",
            "execute log filter category event",
            "# execute log filter field action login",
            "execute log display",
            "",
            "diagnose log test",
            "",
        ]
        if src:
            lines += [
                f"# optional src context {src}",
                f"# execute log filter field srcip {src}",
            ]
        lines += [
            "diagnose debug crashlog read",
            "execute log filter dump",
        ]
        return "\n".join(lines)

    def _log_rate_load(self) -> str:
        return "\n".join(
            [
                "# === Recipe: Log rate / miglogd load ===",
                "# High log rate, miglogd CPU, queue drops",
                "",
                "diagnose sys top 2 30",
                "diagnose sys top-mem",
                "diagnose test application miglogd 4",
                "diagnose test application miglogd 6",
                "diagnose log kernel-stats",
                "diagnose test application fgtlogd 1",
                "",
                "get system performance status",
                "get log setting",
                "",
                "# Reduce noise: disable noisy UTM log, sampling, exclude local",
                "# config log setting → local-in-allow / local-out / neighbor-event",
                "",
                "diagnose debug crashlog read",
            ]
        )
