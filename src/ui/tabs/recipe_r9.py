"""Release 9 recipes — IS-IS, Automation Stitch."""

from core.safety import preamble, epilogue


class RecipeR9Mixin:
    """Release 9 playbooks."""

    def _isis(self) -> str:
        lines = [
            "# === Recipe: IS-IS neighbor / LSP ===",
            "# Adjacency down, missing LSP / routes, level-1 vs level-2",
            "",
            "get router info isis status",
            "get router info isis neighbors",
            "get router info isis interface",
            "get router info isis database",
            "get router info isis topology",
            "get router info routing-table isis",
            "get router info routing-table all",
            "",
            "# CLNS / ISO adjacency often uses multicast 01:80:c2:00:00:14 / 15",
            "diagnose ip address list",
            "diagnose sniffer packet any 'isis' 4 0 l",
            "# if 'isis' BPF unsupported on device:",
            "# diagnose sniffer packet any '' 4 50 l",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose ip router isis all enable",
            "diagnose ip router isis level info",
            "diagnose debug enable",
            "",
            "# --- after test ---",
            "diagnose debug disable",
            "diagnose ip router isis all disable",
            "diagnose debug reset",
        ]
        return "\n".join(lines)

    def _automation_stitch(self) -> str:
        lines = [
            "# === Recipe: Automation Stitch ===",
            "# Stitch not firing, action fail, webhook / CLI / email",
            "",
            "# config overview (read-only style via get/show on device)",
            "# show system automation-stitch",
            "# show system automation-trigger",
            "# show system automation-action",
            "",
            "diagnose automation info",
            "diagnose test application autod 1",
            "diagnose test application autod",
            "",
            "# recent stitch activity / log hints",
            "execute log filter category event",
            "execute log filter field subtype system",
            "# execute log display",
            "",
            "get system status",
            "diagnose sys top 5 15",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        lines += [
            "diagnose debug application autod -1",
            "diagnose debug enable",
        ]
        lines.extend(epilogue(stop=True))
        lines += [
            "",
            "# If stitch uses webhook: check outbound connectivity / policy",
            "# diagnose sniffer packet any 'tcp port 443' 4 0 l",
            "# For email actions: also see Email filter recipe + diagnose mailserver",
        ]
        return "\n".join(lines)
