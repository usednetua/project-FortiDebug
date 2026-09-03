"""Traceroute tab — exec traceroute-options + exec traceroute."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab


class TracerouteTab(BaseTab):
    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(self, text="Traceroute", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 15))

        # Host
        ctk.CTkLabel(self, text="Host / IP").grid(row=1, column=0, sticky="w", padx=10, pady=4)
        self.host = ctk.CTkEntry(self, placeholder_text="8.8.8.8")
        self.host.grid(row=1, column=1, sticky="ew", padx=10, pady=4)
        self.host.bind("<KeyRelease>", self.notify_change)

        # Source IP
        ctk.CTkLabel(self, text="Source IP").grid(row=2, column=0, sticky="w", padx=10, pady=4)
        self.source = ctk.CTkEntry(self, placeholder_text="(optional)")
        self.source.grid(row=2, column=1, sticky="ew", padx=10, pady=4)
        self.source.bind("<KeyRelease>", self.notify_change)

        # Interface
        ctk.CTkLabel(self, text="Egress Interface").grid(row=3, column=0, sticky="w", padx=10, pady=4)
        self.interface = ctk.CTkEntry(self, placeholder_text="port1 / wan1 ...")
        self.interface.grid(row=3, column=1, sticky="ew", padx=10, pady=4)
        self.interface.bind("<KeyRelease>", self.notify_change)

        # Queries per hop
        ctk.CTkLabel(self, text="Queries per hop").grid(row=4, column=0, sticky="w", padx=10, pady=4)
        self.queries = ctk.CTkEntry(self, placeholder_text="3")
        self.queries.grid(row=4, column=1, sticky="ew", padx=10, pady=4)
        self.queries.bind("<KeyRelease>", self.notify_change)

        # Max TTL
        ctk.CTkLabel(self, text="Max TTL").grid(row=5, column=0, sticky="w", padx=10, pady=4)
        self.max_ttl = ctk.CTkEntry(self, placeholder_text="30")
        self.max_ttl.grid(row=5, column=1, sticky="ew", padx=10, pady=4)
        self.max_ttl.bind("<KeyRelease>", self.notify_change)

        # View settings
        self.view_settings = ctk.CTkCheckBox(
            self, text="Show view-settings", command=self.notify_change
        )
        self.view_settings.select()
        self.view_settings.grid(row=6, column=0, columnspan=2, sticky="w", padx=10, pady=8)

    def generate_commands(self) -> str:
        lines = []

        src = self.source.get().strip()
        if src:
            lines.append(f"exec traceroute-options source {src}")

        iface = self.interface.get().strip()
        if iface:
            lines.append(f"exec traceroute-options interface {iface}")

        queries = self.queries.get().strip()
        if queries:
            lines.append(f"exec traceroute-options queries {queries}")

        max_ttl = self.max_ttl.get().strip()
        if max_ttl:
            lines.append(f"exec traceroute-options max-ttl {max_ttl}")

        if self.view_settings.get():
            lines.append("exec traceroute-options view-settings")

        host = self.host.get().strip()
        if host:
            lines.append(f"exec traceroute {host}")
        else:
            lines.append("# specify Host / IP")

        return "\n".join(lines)
