"""SD-WAN diagnostics — FortiOS-aware (virtual-wan-link / sdwan / service4)."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab
from core.fortios_version import (
    DEFAULT_VERSION,
    version_banner,
    sdwan_cmd,
    sdwan_service_cmd,
    sdwan_version_note,
)
from ui.widgets.tooltip import tip


class SdwanTab(BaseTab):
    def __init__(self, master, on_change=None, get_version=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self.get_version = get_version or (lambda: DEFAULT_VERSION)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(self, text="SD-WAN", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 12))

        note = ctk.CTkLabel(
            self,
            text="Префікс залежить від FortiOS (селектор зліва): virtual-wan-link на 6.x, sdwan на 7+.",
            text_color="gray",
            wraplength=480,
        )
        note.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 8))

        self.health = ctk.CTkCheckBox(
            self, text="health-check", command=self.notify_change
        )
        self.health.select()
        self.health.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=3)
        tip(self.health, "… health-check")

        self.service = ctk.CTkCheckBox(
            self, text="service / service4", command=self.notify_change
        )
        self.service.select()
        self.service.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=3)
        tip(self.service, "≥7.4.4: service4; раніше: service")

        self.member = ctk.CTkCheckBox(
            self, text="member", command=self.notify_change
        )
        self.member.select()
        self.member.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.zone = ctk.CTkCheckBox(
            self, text="zone", command=self.notify_change
        )
        self.zone.grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.neighbor = ctk.CTkCheckBox(
            self, text="neighbor", command=self.notify_change
        )
        self.neighbor.grid(row=6, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.service_sla = ctk.CTkCheckBox(
            self, text="sla-log", command=self.notify_change
        )
        self.service_sla.grid(row=7, column=0, columnspan=2, sticky="w", padx=10, pady=3)
        tip(self.service_sla, "… sla-log (не service-sla-log)")

        self.ver_hint = ctk.CTkLabel(self, text="", text_color="gray", wraplength=480)
        self.ver_hint.grid(row=8, column=0, columnspan=2, sticky="w", padx=10, pady=6)

    def generate_commands(self) -> str:
        version = self.get_version()
        note = sdwan_version_note(version)
        self.ver_hint.configure(text=f"FortiOS {version.value}: {note}")

        lines = [version_banner(version, note), ""]

        if self.health.get():
            lines.append(sdwan_cmd(version, "health-check"))
        if self.service.get():
            lines.append(sdwan_service_cmd(version))
        if self.member.get():
            lines.append(sdwan_cmd(version, "member"))
        if self.zone.get():
            lines.append(sdwan_cmd(version, "zone"))
        if self.neighbor.get():
            lines.append(sdwan_cmd(version, "neighbor"))
        if self.service_sla.get():
            lines.append(sdwan_cmd(version, "sla-log"))

        if len(lines) <= 2:
            return "\n".join(lines[:1] + ["", "# select options"])
        return "\n".join(lines)
