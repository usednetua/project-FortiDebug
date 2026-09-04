"""UTM / IPS quick debug helpers."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab
from core.safety import preamble, epilogue
from ui.widgets.tooltip import tip


class UtmIpsTab(BaseTab):
    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(self, text="UTM / IPS", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 8))

        warn = ctk.CTkLabel(
            self,
            text="⚠ IPS/UTM debug може бути дуже «шумним» — використовуй фільтри і швидко вимикай.",
            text_color="#e67e22",
            wraplength=480,
        )
        warn.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 10))

        ctk.CTkLabel(self, text="IPS filter IP").grid(row=2, column=0, sticky="w", padx=10, pady=4)
        self.filter_ip = ctk.CTkEntry(self, placeholder_text="optional host")
        self.filter_ip.grid(row=2, column=1, sticky="ew", padx=10, pady=4)
        self.filter_ip.bind("<KeyRelease>", self.notify_change)

        self.ips_filter_list = ctk.CTkCheckBox(
            self, text="diagnose ips filter status", command=self.notify_change
        )
        self.ips_filter_list.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.ips_filter_set = ctk.CTkCheckBox(
            self, text="Set ips filter (src/dst from IP field)", command=self.notify_change
        )
        self.ips_filter_set.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=3)
        tip(self.ips_filter_set, "diagnose ips filter set src/dst … (синтаксис може відрізнятися)")

        self.ips_debug = ctk.CTkCheckBox(
            self, text="diagnose ips debug enable + all", command=self.notify_change
        )
        self.ips_debug.grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.av_stats = ctk.CTkCheckBox(
            self, text="diagnose ips av stats", command=self.notify_change
        )
        self.av_stats.grid(row=6, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.urlfilter_debug = ctk.CTkCheckBox(
            self, text="Live urlfilter debug (-1)", command=self.notify_change
        )
        self.urlfilter_debug.grid(row=7, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.timestamps = ctk.CTkCheckBox(
            self, text="Console timestamps", command=self.notify_change
        )
        self.timestamps.select()
        self.timestamps.grid(row=8, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.stop_block = ctk.CTkCheckBox(
            self, text="Append stop-debug / ips debug disable", command=self.notify_change
        )
        self.stop_block.select()
        self.stop_block.grid(row=9, column=0, columnspan=2, sticky="w", padx=10, pady=4)

        self.grid_columnconfigure(1, weight=1)

    def generate_commands(self) -> str:
        lines = []
        ip = self.filter_ip.get().strip()

        if self.ips_filter_list.get():
            lines.append("diagnose ips filter status")

        if self.ips_filter_set.get() and ip:
            lines.append(f"diagnose ips filter set src {ip}")
            lines.append(f"diagnose ips filter set dst {ip}")

        if self.av_stats.get():
            lines.append("diagnose ips av stats")

        need_live = self.ips_debug.get() or self.urlfilter_debug.get()
        if need_live:
            lines.extend(preamble(reset=True, timestamps=bool(self.timestamps.get())))
            if self.ips_debug.get():
                lines.append("diagnose ips debug enable all")
            if self.urlfilter_debug.get():
                lines.append("diagnose debug application urlfilter -1")
            lines.append("diagnose debug enable")
            if self.stop_block.get():
                lines.append("")
                lines.append("# --- stop after capture ---")
                if self.ips_debug.get():
                    lines.append("diagnose ips debug disable")
                lines.extend(epilogue(stop=True))

        return "\n".join(lines) if lines else "# select options"
