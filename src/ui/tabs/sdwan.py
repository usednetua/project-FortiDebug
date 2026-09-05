"""SD-WAN diagnostics — respect FortiOS selector."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab
from core.fortios_version import DEFAULT_VERSION, version_banner
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
            text="diagnose sys sdwan … — набір підкоманд може відрізнятися за FortiOS (селектор зліва).",
            text_color="gray",
            wraplength=480,
        )
        note.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 8))

        self.health = ctk.CTkCheckBox(
            self, text="health-check status", command=self.notify_change
        )
        self.health.select()
        self.health.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=3)
        tip(self.health, "diagnose sys sdwan health-check")

        self.service = ctk.CTkCheckBox(
            self, text="service", command=self.notify_change
        )
        self.service.select()
        self.service.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=3)
        tip(self.service, "Правила SD-WAN service")

        self.member = ctk.CTkCheckBox(
            self, text="member", command=self.notify_change
        )
        self.member.select()
        self.member.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=3)
        tip(self.member, "Статус member-лінків")

        self.zone = ctk.CTkCheckBox(
            self, text="zone", command=self.notify_change
        )
        self.zone.grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.neighbor = ctk.CTkCheckBox(
            self, text="neighbor", command=self.notify_change
        )
        self.neighbor.grid(row=6, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.service_sla = ctk.CTkCheckBox(
            self, text="service-sla-log", command=self.notify_change
        )
        self.service_sla.grid(row=7, column=0, columnspan=2, sticky="w", padx=10, pady=3)
        tip(self.service_sla, "SLA log — може бути відсутній на старих 6.x")

        self.ver_hint = ctk.CTkLabel(self, text="", text_color="gray", wraplength=480)
        self.ver_hint.grid(row=8, column=0, columnspan=2, sticky="w", padx=10, pady=6)

    def generate_commands(self) -> str:
        version = self.get_version()
        self.ver_hint.configure(
            text=f"FortiOS {version.value}: перевіряй «diagnose sys sdwan ?» на пристрої"
        )
        lines = [
            version_banner(version, "перевір diagnose sys sdwan ? на FGT"),
            "",
        ]
        if self.health.get():
            lines.append("diagnose sys sdwan health-check")
        if self.service.get():
            lines.append("diagnose sys sdwan service")
        if self.member.get():
            lines.append("diagnose sys sdwan member")
        if self.zone.get():
            lines.append("diagnose sys sdwan zone")
        if self.neighbor.get():
            lines.append("diagnose sys sdwan neighbor")
        if self.service_sla.get():
            lines.append("diagnose sys sdwan service-sla-log")
        if len(lines) <= 2:
            return "\n".join(lines[:1] + ["", "# select options"])
        return "\n".join(lines)
