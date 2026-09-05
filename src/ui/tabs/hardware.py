"""Hardware / NPU overview (safe diagnostics).

NP6 commands from Fortinet Hardware Acceleration docs.
NP7 options are limited overview — full matrix is model-specific.
"""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab
from ui.widgets.tooltip import tip


class HardwareTab(BaseTab):
    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(
            self, text="Hardware / NPU", font=ctk.CTkFont(size=18, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 8))

        warn = ctk.CTkLabel(
            self,
            text="NPU команди залежать від моделі (NP6/NP7). Перевір ? на своєму FGT.",
            text_color="#e67e22",
            wraplength=480,
        )
        warn.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 8))

        self.cpu = ctk.CTkCheckBox(
            self, text="diagnose hardware cpuinfo", command=self.notify_change
        )
        self.cpu.select()
        self.cpu.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.mem = ctk.CTkCheckBox(
            self, text="diagnose hardware meminfo", command=self.notify_change
        )
        self.mem.select()
        self.mem.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        ctk.CTkLabel(self, text="NIC name").grid(row=4, column=0, sticky="w", padx=10, pady=4)
        self.nic = ctk.CTkEntry(self, placeholder_text="optional e.g. port1")
        self.nic.grid(row=4, column=1, sticky="ew", padx=10, pady=4)
        self.nic.bind("<KeyRelease>", self.notify_change)

        self.deviceinfo_nic = ctk.CTkCheckBox(
            self, text="diagnose hardware deviceinfo nic", command=self.notify_change
        )
        self.deviceinfo_nic.grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=3)
        tip(self.deviceinfo_nic, "Без імені — загальний огляд; з NIC — деталі інтерфейсу")

        ctk.CTkLabel(self, text="NPU family").grid(row=6, column=0, sticky="w", padx=10, pady=4)
        self.npu_family = ctk.CTkOptionMenu(
            self,
            values=["np6", "np7", "np6xlite", "np6lite"],
            command=lambda _: self.notify_change(),
        )
        self.npu_family.set("np6")
        self.npu_family.grid(row=6, column=1, sticky="ew", padx=10, pady=4)

        ctk.CTkLabel(self, text="NPU id").grid(row=7, column=0, sticky="w", padx=10, pady=4)
        self.npu_id = ctk.CTkEntry(self, placeholder_text="0")
        self.npu_id.insert(0, "0")
        self.npu_id.grid(row=7, column=1, sticky="ew", padx=10, pady=4)
        self.npu_id.bind("<KeyRelease>", self.notify_change)
        tip(self.npu_id, "dev_id з port-list; на single-NPU зазвичай 0")

        self.port_list = ctk.CTkCheckBox(
            self, text="port-list (get + diagnose)", command=self.notify_change
        )
        self.port_list.select()
        self.port_list.grid(row=8, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.session_stats = ctk.CTkCheckBox(
            self, text="session-stats (NP6-style)", command=self.notify_change
        )
        self.session_stats.grid(row=9, column=0, columnspan=2, sticky="w", padx=10, pady=3)
        tip(self.session_stats, "diagnose npu np6 session-stats <id>")

        self.npu_feature = ctk.CTkCheckBox(
            self, text="npu-feature", command=self.notify_change
        )
        self.npu_feature.grid(row=10, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.grid_columnconfigure(1, weight=1)

    def generate_commands(self) -> str:
        lines = []
        family = self.npu_family.get()
        npu_id = self.npu_id.get().strip() or "0"
        nic = self.nic.get().strip()

        if self.cpu.get():
            lines.append("diagnose hardware cpuinfo")
        if self.mem.get():
            lines.append("diagnose hardware meminfo")
        if self.deviceinfo_nic.get():
            if nic:
                lines.append(f"diagnose hardware deviceinfo nic {nic}")
            else:
                lines.append("diagnose hardware deviceinfo nic")

        if self.port_list.get():
            lines.append(f"get hardware npu {family} port-list")
            lines.append(f"diagnose npu {family} port-list")

        if self.session_stats.get():
            if family == "np6":
                lines.append(f"diagnose npu np6 session-stats {npu_id}")
            else:
                lines.append(
                    f"# session-stats: primarily documented for np6 — check diagnose npu {family} ?"
                )
                lines.append(f"diagnose npu {family} session-stats {npu_id}")

        if self.npu_feature.get():
            lines.append(f"diagnose npu {family} npu-feature")

        return "\n".join(lines) if lines else "# select options"
