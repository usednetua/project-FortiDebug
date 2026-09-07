"""System Top tab — diagnose sys top variants."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab


class SystemTopTab(BaseTab):
    VARIANTS = {
        "top": "diagnose sys top",
        "top-summary": "diagnose sys top-summary",
        "top-mem": "diagnose sys top-mem",
        "top-io": "diagnose sys top-io",
    }

    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(self, text="System Top", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 15))

        ctk.CTkLabel(self, text="Variant").grid(row=1, column=0, sticky="w", padx=10, pady=4)
        variant_values = sorted(self.VARIANTS.keys(), key=str.casefold)
        self.variant = ctk.CTkOptionMenu(
            self,
            values=variant_values,
            command=lambda _: self.notify_change(),
        )
        self.variant.set("top")
        self.variant.grid(row=1, column=1, sticky="ew", padx=10, pady=4)

        ctk.CTkLabel(self, text="Refresh delay (sec)").grid(row=2, column=0, sticky="w", padx=10, pady=4)
        self.delay = ctk.CTkEntry(self, placeholder_text="5")
        self.delay.insert(0, "5")
        self.delay.grid(row=2, column=1, sticky="ew", padx=10, pady=4)
        self.delay.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Max lines").grid(row=3, column=0, sticky="w", padx=10, pady=4)
        self.max_lines = ctk.CTkEntry(self, placeholder_text="20")
        self.max_lines.insert(0, "20")
        self.max_lines.grid(row=3, column=1, sticky="ew", padx=10, pady=4)
        self.max_lines.bind("<KeyRelease>", self.notify_change)

        # Companion commands
        ctk.CTkLabel(self, text="Companion snapshots", font=ctk.CTkFont(weight="bold")).grid(
            row=4, column=0, columnspan=2, sticky="w", padx=10, pady=(12, 4)
        )

        self.perf_status = ctk.CTkCheckBox(
            self, text="get system performance status", command=self.notify_change
        )
        self.perf_status.grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.hw_cpu = ctk.CTkCheckBox(
            self, text="diagnose hardware cpuinfo", command=self.notify_change
        )
        self.hw_cpu.grid(row=6, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.hw_mem = ctk.CTkCheckBox(
            self, text="diagnose hardware meminfo", command=self.notify_change
        )
        self.hw_mem.grid(row=7, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.conserve = ctk.CTkCheckBox(
            self, text="diagnose sys session full-stat (conserve thresholds)", command=self.notify_change
        )
        self.conserve.grid(row=8, column=0, columnspan=2, sticky="w", padx=10, pady=3)

    def generate_commands(self) -> str:
        lines = []

        if self.perf_status.get():
            lines.append("get system performance status")
        if self.hw_cpu.get():
            lines.append("diagnose hardware cpuinfo")
        if self.hw_mem.get():
            lines.append("diagnose hardware meminfo")
        if self.conserve.get():
            lines.append("diagnose sys session full-stat")

        variant = self.variant.get()
        base = self.VARIANTS[variant]

        delay = self.delay.get().strip()
        max_lines = self.max_lines.get().strip()

        if variant in ("top", "top-summary"):
            # diagnose sys top <delay> <max_lines>
            args = []
            if delay:
                args.append(delay)
            if max_lines:
                args.append(max_lines)
            cmd = base + (" " + " ".join(args) if args else "")
            lines.append(cmd)
        else:
            # top-mem / top-io — one-shot, delay ignored
            lines.append(base)

        return "\n".join(lines)
