"""Auth / FSSO diagnostics."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab
from core.safety import preamble, epilogue
from ui.widgets.tooltip import tip


class AuthTab(BaseTab):
    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(self, text="Auth / FSSO", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 12))

        self.auth_list = ctk.CTkCheckBox(
            self, text="diagnose firewall auth list", command=self.notify_change
        )
        self.auth_list.select()
        self.auth_list.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=3)
        tip(self.auth_list, "Список автентифікованих користувачів")

        self.auth_clear = ctk.CTkCheckBox(
            self, text="Clear auth list ⚠", command=self.notify_change
        )
        self.auth_clear.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=3)
        tip(self.auth_clear, "⚠ diagnose firewall auth clear — скидає auth-сесії")

        self.fsso = ctk.CTkCheckBox(
            self, text="diagnose debug authd fsso list", command=self.notify_change
        )
        self.fsso.select()
        self.fsso.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=3)
        tip(self.fsso, "FSSO agent / user mapping")

        self.authd_debug = ctk.CTkCheckBox(
            self, text="Live authd debug (-1)", command=self.notify_change
        )
        self.authd_debug.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=3)
        tip(self.authd_debug, "diagnose debug application authd -1 — шумно")

        self.timestamps = ctk.CTkCheckBox(
            self, text="Console timestamps", command=self.notify_change
        )
        self.timestamps.select()
        self.timestamps.grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.stop_block = ctk.CTkCheckBox(
            self, text="Append stop-debug block", command=self.notify_change
        )
        self.stop_block.select()
        self.stop_block.grid(row=6, column=0, columnspan=2, sticky="w", padx=10, pady=4)

    def generate_commands(self) -> str:
        lines = []
        if self.auth_list.get():
            lines.append("diagnose firewall auth list")
        if self.auth_clear.get():
            lines.append("# ⚠ clears authenticated users")
            lines.append("diagnose firewall auth clear")
        if self.fsso.get():
            lines.append("diagnose debug authd fsso list")
        if self.authd_debug.get():
            lines.extend(preamble(reset=True, timestamps=bool(self.timestamps.get())))
            lines.append("diagnose debug application authd -1")
            lines.append("diagnose debug enable")
            lines.extend(epilogue(stop=bool(self.stop_block.get())))
        return "\n".join(lines) if lines else "# select options"
