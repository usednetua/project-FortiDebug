"""TAC / Support helper — commands for Fortinet support tickets."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab
from core.safety import preamble, epilogue
from ui.widgets.tooltip import tip


class TacTab(BaseTab):
    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(
            self, text="TAC / Support", font=ctk.CTkFont(size=18, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 12))

        note = ctk.CTkLabel(
            self,
            text="Набір команд для тікета Fortinet Support / baseline snapshot.",
            text_color="gray",
            wraplength=480,
        )
        note.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 10))

        self.sys_status = ctk.CTkCheckBox(
            self, text="get system status", command=self.notify_change
        )
        self.sys_status.select()
        self.sys_status.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.perf = ctk.CTkCheckBox(
            self, text="get system performance status", command=self.notify_change
        )
        self.perf.select()
        self.perf.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.crashlog = ctk.CTkCheckBox(
            self, text="diagnose debug crashlog read", command=self.notify_change
        )
        self.crashlog.select()
        self.crashlog.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.debug_report = ctk.CTkCheckBox(
            self, text="diagnose debug report", command=self.notify_change
        )
        self.debug_report.grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.tac_report = ctk.CTkCheckBox(
            self, text="execute tac report (довго, багато виводу)", command=self.notify_change
        )
        self.tac_report.select()
        self.tac_report.grid(row=6, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.ha = ctk.CTkCheckBox(
            self, text="HA status + checksum cluster", command=self.notify_change
        )
        self.ha.grid(row=7, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.vpn = ctk.CTkCheckBox(
            self, text="VPN gateway + tunnel list", command=self.notify_change
        )
        self.vpn.grid(row=8, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.routing = ctk.CTkCheckBox(
            self, text="Routing table (all)", command=self.notify_change
        )
        self.routing.grid(row=9, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.session_stat = ctk.CTkCheckBox(
            self, text="diagnose sys session full-stat", command=self.notify_change
        )
        self.session_stat.grid(row=10, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.cli7 = ctk.CTkCheckBox(
            self, text="diagnose debug cli 7 (GUI→CLI)", command=self.notify_change
        )
        self.cli7.grid(row=11, column=0, columnspan=2, sticky="w", padx=10, pady=3)
        tip(self.cli7, "Показує CLI-еквівалент дій у GUI")

        self.bundle = ctk.CTkCheckBox(
            self, text="Support bundle (усі типові команди вище)", command=self.notify_change
        )
        self.bundle.grid(row=12, column=0, columnspan=2, sticky="w", padx=10, pady=8)

    def generate_commands(self) -> str:
        if self.bundle.get():
            return self._full_bundle()

        lines = ["# === TAC / Support ===", ""]

        if self.sys_status.get():
            lines.append("get system status")
        if self.perf.get():
            lines.append("get system performance status")
        if self.crashlog.get():
            lines.append("diagnose debug crashlog read")
        if self.debug_report.get():
            lines.append("diagnose debug report")
        if self.tac_report.get():
            lines.append("execute tac report")
        if self.ha.get():
            lines.append("get system ha status")
            lines.append("diagnose sys ha checksum cluster")
        if self.vpn.get():
            lines.append("diagnose vpn ike gateway list")
            lines.append("diagnose vpn tunnel list")
        if self.routing.get():
            lines.append("get router info routing-table all")
        if self.session_stat.get():
            lines.append("diagnose sys session full-stat")
        if self.cli7.get():
            lines.extend(preamble(reset=True, timestamps=True))
            lines.append("diagnose debug cli 7")
            lines.append("diagnose debug enable")
            lines.extend(epilogue(stop=True))

        return "\n".join(lines) if len(lines) > 2 else "# select options"

    def _full_bundle(self) -> str:
        return "\n".join(
            [
                "# === Support bundle (baseline for TAC) ===",
                "",
                "get system status",
                "get system performance status",
                "diagnose debug crashlog read",
                "diagnose hardware cpuinfo",
                "diagnose hardware meminfo",
                "diagnose sys session full-stat",
                "get system ha status",
                "diagnose sys ha checksum cluster",
                "diagnose vpn ike gateway list",
                "diagnose vpn tunnel list",
                "get router info routing-table all",
                "diagnose debug report",
                "execute tac report",
            ]
        )
