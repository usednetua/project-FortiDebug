"""DHCP diagnostics — leases, sniffer, relay debug."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab
from core.safety import preamble, epilogue
from ui.widgets.tooltip import tip


class DhcpTab(BaseTab):
    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(self, text="DHCP", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 12))

        ctk.CTkLabel(self, text="Interface (sniffer)").grid(row=1, column=0, sticky="w", padx=10, pady=4)
        self.iface = ctk.CTkEntry(self, placeholder_text="any / internal")
        self.iface.insert(0, "any")
        self.iface.grid(row=1, column=1, sticky="ew", padx=10, pady=4)
        self.iface.bind("<KeyRelease>", self.notify_change)
        tip(self.iface, "Інтерфейс для sniffer 67/68")

        self.leases = ctk.CTkCheckBox(
            self, text="execute dhcp lease-list", command=self.notify_change
        )
        self.leases.select()
        self.leases.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=3)
        tip(self.leases, "Список виданих DHCP lease")

        self.sniffer = ctk.CTkCheckBox(
            self, text="Sniffer ports 67/68", command=self.notify_change
        )
        self.sniffer.select()
        self.sniffer.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=3)
        tip(self.sniffer, "diagnose sniffer packet … 'port 67 or port 68'")

        self.relay_debug = ctk.CTkCheckBox(
            self, text="Live dhcprelay debug", command=self.notify_change
        )
        self.relay_debug.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=3)
        tip(self.relay_debug, "diagnose debug application dhcprelay -1")

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

        self.grid_columnconfigure(1, weight=1)

    def generate_commands(self) -> str:
        lines = []
        if self.leases.get():
            lines.append("execute dhcp lease-list")

        if self.sniffer.get():
            iface = self.iface.get().strip() or "any"
            lines.append(f"diagnose sniffer packet {iface} 'port 67 or port 68' 4 0 l")

        if self.relay_debug.get():
            lines.extend(preamble(reset=True, timestamps=bool(self.timestamps.get())))
            lines.append("diagnose debug application dhcprelay -1")
            lines.append("diagnose debug enable")
            lines.extend(epilogue(stop=bool(self.stop_block.get())))

        return "\n".join(lines) if lines else "# select options"
