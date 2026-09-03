"""Ping tab — exec ping-options + exec ping."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab


class PingTab(BaseTab):
    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(self, text="Ping", font=ctk.CTkFont(size=18, weight="bold"))
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

        # DF bit
        ctk.CTkLabel(self, text="DF bit").grid(row=4, column=0, sticky="w", padx=10, pady=4)
        self.df_bit = ctk.CTkOptionMenu(
            self, values=["default", "yes", "no"], command=lambda _: self.notify_change()
        )
        self.df_bit.set("default")
        self.df_bit.grid(row=4, column=1, sticky="ew", padx=10, pady=4)

        # Data size
        ctk.CTkLabel(self, text="Data Size").grid(row=5, column=0, sticky="w", padx=10, pady=4)
        self.data_size = ctk.CTkEntry(self, placeholder_text="56 (1472 for MTU test)")
        self.data_size.grid(row=5, column=1, sticky="ew", padx=10, pady=4)
        self.data_size.bind("<KeyRelease>", self.notify_change)

        # Adaptive
        self.adaptive = ctk.CTkCheckBox(self, text="Adaptive ping", command=self.notify_change)
        self.adaptive.grid(row=6, column=0, columnspan=2, sticky="w", padx=10, pady=6)

        # Timeout
        ctk.CTkLabel(self, text="Timeout (sec)").grid(row=7, column=0, sticky="w", padx=10, pady=4)
        self.timeout = ctk.CTkEntry(self, placeholder_text="")
        self.timeout.grid(row=7, column=1, sticky="ew", padx=10, pady=4)
        self.timeout.bind("<KeyRelease>", self.notify_change)

        # Interval
        ctk.CTkLabel(self, text="Interval (sec)").grid(row=8, column=0, sticky="w", padx=10, pady=4)
        self.interval = ctk.CTkEntry(self, placeholder_text="")
        self.interval.grid(row=8, column=1, sticky="ew", padx=10, pady=4)
        self.interval.bind("<KeyRelease>", self.notify_change)

        # Repeat count
        ctk.CTkLabel(self, text="Repeat count").grid(row=9, column=0, sticky="w", padx=10, pady=4)
        self.repeat = ctk.CTkEntry(self, placeholder_text="")
        self.repeat.grid(row=9, column=1, sticky="ew", padx=10, pady=4)
        self.repeat.bind("<KeyRelease>", self.notify_change)

        # View settings
        self.view_settings = ctk.CTkCheckBox(
            self, text="Show view-settings", command=self.notify_change
        )
        self.view_settings.select()
        self.view_settings.grid(row=10, column=0, columnspan=2, sticky="w", padx=10, pady=8)

    def generate_commands(self) -> str:
        lines = []

        src = self.source.get().strip()
        if src:
            lines.append(f"exec ping-options source {src}")

        iface = self.interface.get().strip()
        if iface:
            lines.append(f"exec ping-options interface {iface}")

        df = self.df_bit.get()
        if df != "default":
            lines.append(f"exec ping-options df-bit {df}")

        size = self.data_size.get().strip()
        if size:
            lines.append(f"exec ping-options data-size {size}")

        if self.adaptive.get():
            lines.append("exec ping-options adaptive enable")

        timeout = self.timeout.get().strip()
        if timeout:
            lines.append(f"exec ping-options timeout {timeout}")

        interval = self.interval.get().strip()
        if interval:
            lines.append(f"exec ping-options interval {interval}")

        repeat = self.repeat.get().strip()
        if repeat:
            lines.append(f"exec ping-options repeat-count {repeat}")

        if self.view_settings.get():
            lines.append("exec ping-options view-settings")

        host = self.host.get().strip()
        if host:
            lines.append(f"exec ping {host}")
        else:
            lines.append("# specify Host / IP")

        return "\n".join(lines)
