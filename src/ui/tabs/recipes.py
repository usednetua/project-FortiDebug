"""Recipes / Workflows — one-click incident playbooks."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab
from core.fortios_version import (
    DEFAULT_VERSION,
    ike_log_filter_clear,
    ike_filter_remote_peer,
    ike_filter_name,
)
from core.safety import preamble, epilogue


class RecipesTab(BaseTab):
    RECIPES = [
        "Traffic not passing",
        "VPN down / rekey",
        "High CPU",
        "Policy / NAT check",
        "HA out-of-sync",
        "DNS issues",
    ]

    def __init__(self, master, on_change=None, get_version=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self.get_version = get_version or (lambda: DEFAULT_VERSION)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(
            self, text="Recipes / Workflows", font=ctk.CTkFont(size=18, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 12))

        ctk.CTkLabel(self, text="Scenario").grid(row=1, column=0, sticky="w", padx=10, pady=4)
        self.recipe = ctk.CTkOptionMenu(
            self, values=self.RECIPES, command=lambda _: self.notify_change()
        )
        self.recipe.set(self.RECIPES[0])
        self.recipe.grid(row=1, column=1, sticky="ew", padx=10, pady=4)

        ctk.CTkLabel(self, text="Source IP").grid(row=2, column=0, sticky="w", padx=10, pady=4)
        self.src = ctk.CTkEntry(self, placeholder_text="optional")
        self.src.grid(row=2, column=1, sticky="ew", padx=10, pady=4)
        self.src.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Destination IP").grid(row=3, column=0, sticky="w", padx=10, pady=4)
        self.dst = ctk.CTkEntry(self, placeholder_text="optional")
        self.dst.grid(row=3, column=1, sticky="ew", padx=10, pady=4)
        self.dst.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Port").grid(row=4, column=0, sticky="w", padx=10, pady=4)
        self.port = ctk.CTkEntry(self, placeholder_text="optional")
        self.port.grid(row=4, column=1, sticky="ew", padx=10, pady=4)
        self.port.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Peer / Phase1 (VPN)").grid(row=5, column=0, sticky="w", padx=10, pady=4)
        self.peer = ctk.CTkEntry(self, placeholder_text="remote IP or phase1 name")
        self.peer.grid(row=5, column=1, sticky="ew", padx=10, pady=4)
        self.peer.bind("<KeyRelease>", self.notify_change)

        note = ctk.CTkLabel(
            self,
            text="Готовий набір команд під типові інциденти. Заповни поля → Copy.",
            text_color="gray",
            wraplength=480,
        )
        note.grid(row=6, column=0, columnspan=2, sticky="w", padx=10, pady=12)

    def generate_commands(self) -> str:
        name = self.recipe.get()
        src = self.src.get().strip()
        dst = self.dst.get().strip()
        port = self.port.get().strip()
        peer = self.peer.get().strip()
        version = self.get_version()

        if name == "Traffic not passing":
            return self._traffic_not_passing(src, dst, port)
        if name == "VPN down / rekey":
            return self._vpn_down(version, peer)
        if name == "High CPU":
            return self._high_cpu()
        if name == "Policy / NAT check":
            return self._policy_nat(src, dst, port)
        if name == "HA out-of-sync":
            return self._ha_sync()
        if name == "DNS issues":
            return self._dns(src, dst)
        return "# select a recipe"

    def _traffic_not_passing(self, src: str, dst: str, port: str) -> str:
        lines = ["# === Recipe: Traffic not passing ===", ""]
        lines.append("# 1) Session table")
        lines.append("diagnose sys session filter clear")
        if src:
            lines.append(f"diagnose sys session filter src {src}")
        if dst:
            lines.append(f"diagnose sys session filter dst {dst}")
        if port:
            lines.append(f"diagnose sys session filter dport {port}")
        lines.append("diagnose sys session list")
        lines.append("")
        lines.append("# 2) Debug flow")
        lines.extend(preamble(reset=True, clear_flow_filter=True, timestamps=True))
        if src:
            lines.append(f"diagnose debug flow filter saddr {src}")
        if dst:
            lines.append(f"diagnose debug flow filter daddr {dst}")
        if port:
            lines.append(f"diagnose debug flow filter port {port}")
        lines.append("diagnose debug flow show function-name enable")
        lines.append("diagnose debug flow show iprope enable")
        lines.append("diagnose debug flow show console enable")
        lines.append("diagnose debug enable")
        lines.append("diagnose debug flow trace start 200")
        lines.extend(epilogue(stop=True))
        lines.append("")
        lines.append("# 3) Sniffer (optional)")
        filt_parts = []
        if src:
            filt_parts.append(f"host {src}")
        if dst:
            filt_parts.append(f"host {dst}")
        if port:
            filt_parts.append(f"port {port}")
        filt = " and ".join(filt_parts) if filt_parts else ""
        if filt:
            lines.append(f"diagnose sniffer packet any '{filt}' 4 0 l")
        else:
            lines.append("diagnose sniffer packet any '' 4 0 l")
        return "\n".join(lines)

    def _vpn_down(self, version, peer: str) -> str:
        lines = ["# === Recipe: VPN down / rekey ===", ""]
        lines.append("diagnose vpn ike gateway list")
        lines.append("diagnose vpn tunnel list")
        lines.append("")
        lines.extend(preamble(reset=True, timestamps=True))
        lines.append(ike_log_filter_clear(version))
        if peer:
            # peer can be IP or phase1 name
            if any(c.isdigit() for c in peer) and "." in peer:
                lines.append(ike_filter_remote_peer(version, peer))
            else:
                lines.append(ike_filter_name(version, peer))
        lines.append("diagnose debug application ike -1")
        lines.append("diagnose debug enable")
        lines.extend(epilogue(stop=True))
        return "\n".join(lines)

    def _high_cpu(self) -> str:
        return "\n".join(
            [
                "# === Recipe: High CPU ===",
                "",
                "get system performance status",
                "diagnose sys top 5 20",
                "diagnose sys top-mem",
                "diagnose debug crashlog read",
                "diagnose hardware cpuinfo",
                "diagnose sys session full-stat",
            ]
        )

    def _policy_nat(self, src: str, dst: str, port: str) -> str:
        lines = ["# === Recipe: Policy / NAT check ===", ""]
        lines.append("# Sessions")
        lines.append("diagnose sys session filter clear")
        if src:
            lines.append(f"diagnose sys session filter src {src}")
        if dst:
            lines.append(f"diagnose sys session filter dst {dst}")
        if port:
            lines.append(f"diagnose sys session filter dport {port}")
        lines.append("diagnose sys session list")
        lines.append("")
        lines.append("# Flow with iprope")
        lines.extend(preamble(reset=True, clear_flow_filter=True, timestamps=True))
        if src:
            lines.append(f"diagnose debug flow filter saddr {src}")
        if dst:
            lines.append(f"diagnose debug flow filter daddr {dst}")
        if port:
            lines.append(f"diagnose debug flow filter port {port}")
        lines.append("diagnose debug flow show function-name enable")
        lines.append("diagnose debug flow show iprope enable")
        lines.append("diagnose debug flow show console enable")
        lines.append("diagnose debug enable")
        lines.append("diagnose debug flow trace start 100")
        lines.extend(epilogue(stop=True))
        return "\n".join(lines)

    def _ha_sync(self) -> str:
        lines = [
            "# === Recipe: HA out-of-sync ===",
            "",
            "get system ha status",
            "diagnose sys ha status",
            "diagnose sys ha checksum cluster",
            "diagnose sys ha checksum global",
            "diagnose sys ha checksum root",
            "",
        ]
        lines.extend(preamble(reset=True, timestamps=True))
        lines.append("diagnose debug application hasync -1")
        lines.append("diagnose debug enable")
        lines.extend(epilogue(stop=True))
        return "\n".join(lines)

    def _dns(self, src: str, dst: str) -> str:
        lines = ["# === Recipe: DNS issues ===", ""]
        lines.append("diagnose sys session filter clear")
        lines.append("diagnose sys session filter dport 53")
        if src:
            lines.append(f"diagnose sys session filter src {src}")
        if dst:
            lines.append(f"diagnose sys session filter dst {dst}")
        lines.append("diagnose sys session list")
        lines.append("")
        lines.extend(preamble(reset=True, timestamps=True))
        lines.append("diagnose debug application dnsproxy -1")
        lines.append("diagnose debug enable")
        lines.extend(epilogue(stop=True))
        lines.append("")
        lines.append("# Sniffer DNS")
        lines.append("diagnose sniffer packet any 'port 53' 4 0 l")
        return "\n".join(lines)
