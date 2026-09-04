"""HA tab — with safety blocks for live debug."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab
from core.safety import preamble, epilogue


class HaTab(BaseTab):
    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(self, text="HA", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 15))

        ctk.CTkLabel(self, text="Status", font=ctk.CTkFont(weight="bold")).grid(
            row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(4, 2)
        )
        self.ha_status = ctk.CTkCheckBox(
            self, text="get system ha status + diagnose sys ha status", command=self.notify_change
        )
        self.ha_status.select()
        self.ha_status.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.checksum = ctk.CTkCheckBox(self, text="Cluster checksum", command=self.notify_change)
        self.checksum.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.global_cs = ctk.CTkCheckBox(self, text="Global checksum", command=self.notify_change)
        self.global_cs.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.root_cs = ctk.CTkCheckBox(self, text="Root checksum", command=self.notify_change)
        self.root_cs.grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.full_dump = ctk.CTkCheckBox(
            self, text="Full HA dump (group + vcluster)", command=self.notify_change
        )
        self.full_dump.grid(row=6, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        ctk.CTkLabel(self, text="Actions", font=ctk.CTkFont(weight="bold")).grid(
            row=7, column=0, columnspan=2, sticky="w", padx=10, pady=(12, 2)
        )
        self.force_sync = ctk.CTkCheckBox(
            self, text="Force full sync (ha synchronize all)", command=self.notify_change
        )
        self.force_sync.grid(row=8, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.reset_uptime = ctk.CTkCheckBox(
            self, text="Reset HA uptime (may trigger failover!)", command=self.notify_change
        )
        self.reset_uptime.grid(row=9, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        ctk.CTkLabel(self, text="Manage unit index").grid(row=10, column=0, sticky="w", padx=10, pady=4)
        self.manage_idx = ctk.CTkEntry(self, placeholder_text="0 / 1 ...")
        self.manage_idx.grid(row=10, column=1, sticky="ew", padx=10, pady=4)
        self.manage_idx.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Admin for manage").grid(row=11, column=0, sticky="w", padx=10, pady=4)
        self.manage_admin = ctk.CTkEntry(self, placeholder_text="admin (optional)")
        self.manage_admin.grid(row=11, column=1, sticky="ew", padx=10, pady=4)
        self.manage_admin.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Live debug", font=ctk.CTkFont(weight="bold")).grid(
            row=12, column=0, columnspan=2, sticky="w", padx=10, pady=(12, 2)
        )
        self.hatalk = ctk.CTkCheckBox(self, text="hatalk (heartbeat)", command=self.notify_change)
        self.hatalk.grid(row=13, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.hasync = ctk.CTkCheckBox(self, text="hasync (config sync)", command=self.notify_change)
        self.hasync.grid(row=14, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.timestamps = ctk.CTkCheckBox(
            self, text="Console timestamps", command=self.notify_change
        )
        self.timestamps.select()
        self.timestamps.grid(row=15, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.stop_debug = ctk.CTkCheckBox(
            self, text="Append stop-debug block", command=self.notify_change
        )
        self.stop_debug.select()
        self.stop_debug.grid(row=16, column=0, columnspan=2, sticky="w", padx=10, pady=4)

    def generate_commands(self) -> str:
        lines = []

        if self.ha_status.get():
            lines.append("get system ha status")
            lines.append("diagnose sys ha status")
        if self.checksum.get():
            lines.append("diagnose sys ha checksum cluster")
        if self.global_cs.get():
            lines.append("diagnose sys ha checksum global")
        if self.root_cs.get():
            lines.append("diagnose sys ha checksum root")
        if self.full_dump.get():
            lines.append("diagnose sys ha dump-by group")
            lines.append("diagnose sys ha dump-by vcluster")
        if self.force_sync.get():
            lines.append("execute ha synchronize all")
        if self.reset_uptime.get():
            lines.append("diagnose sys ha reset-uptime")

        idx = self.manage_idx.get().strip()
        if idx:
            admin = self.manage_admin.get().strip()
            lines.append(f"execute ha manage {idx}" + (f" {admin}" if admin else ""))

        if self.hatalk.get() or self.hasync.get():
            lines.extend(preamble(reset=True, timestamps=bool(self.timestamps.get())))
            if self.hatalk.get():
                lines.append("diagnose debug application hatalk -1")
            if self.hasync.get():
                lines.append("diagnose debug application hasync -1")
            lines.append("diagnose debug enable")
            lines.extend(epilogue(stop=bool(self.stop_debug.get())))

        return "\n".join(lines) if lines else "# select options"
