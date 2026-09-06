"""Release 10 recipes — IoC / threat feed, Cloud SDN connector."""

from core.safety import preamble, epilogue


class RecipeR10Mixin:
    """Release 10 playbooks."""

    def _ioc_threat_feed(self, src: str = "") -> str:
        lines = [
            "# === Recipe: IoC / Threat feed ===",
            "# External resource update fail, botnet/IoC hits, integrity collect for TAC",
            "",
            "# --- threat feed / external-resource status ---",
            "# show system external-resource",
            "diagnose test application forticron 8",
            "# execute update-external-resource <threat-feed-name>",
            "",
            "# botnet / IoC tables (names vary slightly by FortiOS)",
            "diagnose sys botnet-ip list",
            "diagnose sys botnet-domain list",
            "diagnose sys botnet-ip hit",
            "diagnose sys botnet-domain hit",
            "",
            "get system fortiguard",
            "diagnose debug rating",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose debug application forticron -1",
            "diagnose debug enable",
            "",
            "# re-trigger after enable:",
            "# diagnose test application forticron 8",
            "# execute update-external-resource <name>",
        ]
        lines.extend(epilogue(stop=True))

        lines += [
            "",
            "# --- optional: filesystem integrity (TAC IoC suspicion) ---",
            "# Run one-by-one; large output. Prefer dedicated SSH session, not GUI CLI.",
            "get system status",
            "# diagnose sys filesystem hash",
            "# diagnose sys csum /data/rootfs.gz",
            "# diagnose sys csum /bin",
            "# fnsysctl ls -la /tmp",
            "# fnsysctl ps",
            "# execute tac report",
        ]
        if src:
            lines += [
                "",
                f"# session / flow focus on suspect host {src}",
            ]
            lines.extend(self._session_block(src, "", ""))
            lines.extend(self._flow_block(src, "", ""))
        return "\n".join(lines)

    def _cloud_sdn(self) -> str:
        lines = [
            "# === Recipe: Cloud SDN connector ===",
            "# AWS / Azure / GCP / OCI / K8s dynamic address empty or stale",
            "",
            "# show system sdn-connector",
            "diagnose sys sdn status",
            "# diagnose sys sdn status <connector-name>",
            "diagnose sys sdn cache address",
            "# diagnose sys sdn cache address <connector-name>",
            "diagnose sys sdn cache service",
            "",
            "# dynamic firewall addresses from SDN",
            "# diagnose firewall dynamic list",
            "get system interface",
            "",
            "# cloud-specific test apps (use only if present on this build)",
            "# diagnose test application awsd 1",
            "# diagnose test application azd 1",
            "# diagnose test application gcpd 1",
            "# diagnose test application ocid 1",
            "# diagnose test application kubed 1",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "# enable relevant daemon only — avoid enabling all at once",
            "# diagnose debug application awsd -1",
            "# diagnose debug application azd -1",
            "# diagnose debug application gcpd -1",
            "# diagnose debug application ocid -1",
            "# diagnose debug application cloudapid -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        lines += [
            "",
            "# Outbound HTTPS to cloud API must be allowed (policy / local-out)",
            "# diagnose sniffer packet any 'tcp port 443' 4 0 l",
            "execute ping update.fortiguard.net",
        ]
        return "\n".join(lines)
