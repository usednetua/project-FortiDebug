"""Network diagnostics — ARP, NIC, addresses, IPv6 neighbors."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab
from ui.widgets.tooltip import tip


class NetworkTab(BaseTab):
    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(self, text="Network", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 12))

        ctk.CTkLabel(self, text="Interface (for NIC)").grid(row=1, column=0, sticky="w", padx=10, pady=4)
        self.iface = ctk.CTkEntry(self, placeholder_text="port1 / wan1")
        self.iface.grid(row=1, column=1, sticky="ew", padx=10, pady=4)
        self.iface.bind("<KeyRelease>", self.notify_change)
        tip(self.iface, "Потрібен для get hardware nic <if>")

        self.arp_get = ctk.CTkCheckBox(self, text="get system arp", command=self.notify_change)
        self.arp_get.select()
        self.arp_get.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.arp_diag = ctk.CTkCheckBox(
            self, text="diagnose ip arp list", command=self.notify_change
        )
        self.arp_diag.select()
        self.arp_diag.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.arp_clear = ctk.CTkCheckBox(
            self, text="Clear ARP table ⚠", command=self.notify_change
        )
        self.arp_clear.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=3)
        tip(self.arp_clear, "execute clear system arp table")

        self.ip_list = ctk.CTkCheckBox(
            self, text="diagnose ip address list", command=self.notify_change
        )
        self.ip_list.select()
        self.ip_list.grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.nic = ctk.CTkCheckBox(
            self, text="get hardware nic <interface>", command=self.notify_change
        )
        self.nic.grid(row=6, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.netlink = ctk.CTkCheckBox(
            self, text="diagnose netlink interface list", command=self.notify_change
        )
        self.netlink.grid(row=7, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.nd6 = ctk.CTkCheckBox(
            self, text="IPv6 neighbor-cache list", command=self.notify_change
        )
        self.nd6.grid(row=8, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.grid_columnconfigure(1, weight=1)

    def generate_commands(self) -> str:
        lines = []
        if self.arp_get.get():
            lines.append("get system arp")
        if self.arp_diag.get():
            lines.append("diagnose ip arp list")
        if self.arp_clear.get():
            lines.append("# ⚠ clears entire ARP table")
            lines.append("execute clear system arp table")
        if self.ip_list.get():
            lines.append("diagnose ip address list")
        if self.nic.get():
            iface = self.iface.get().strip()
            if iface:
                lines.append(f"get hardware nic {iface}")
            else:
                lines.append("# get hardware nic <interface> — set Interface field")
        if self.netlink.get():
            lines.append("diagnose netlink interface list")
        if self.nd6.get():
            lines.append("diagnose ipv6 neighbor-cache list")
        return "\n".join(lines) if lines else "# select options"
