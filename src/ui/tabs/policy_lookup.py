"""Policy lookup — diagnose firewall iprope lookup."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab
from core.validators import is_valid_ip, is_valid_port
from ui.widgets.tooltip import tip


class PolicyLookupTab(BaseTab):
    PROTOS = {
        "TCP (6)": "6",
        "UDP (17)": "17",
        "ICMP (1)": "1",
        "Any/other": "0",
    }

    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(
            self, text="Policy Lookup", font=ctk.CTkFont(size=18, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 8))

        note = ctk.CTkLabel(
            self,
            text="iprope lookup — яка policy матчиться для 5-tuple + intf (без live traffic)",
            text_color="gray",
            wraplength=480,
        )
        note.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 10))

        ctk.CTkLabel(self, text="Source IP").grid(row=2, column=0, sticky="w", padx=10, pady=4)
        self.src = ctk.CTkEntry(self, placeholder_text="10.1.1.10")
        self.src.grid(row=2, column=1, sticky="ew", padx=10, pady=4)
        self.src.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Source port").grid(row=3, column=0, sticky="w", padx=10, pady=4)
        self.sport = ctk.CTkEntry(self, placeholder_text="12345")
        self.sport.grid(row=3, column=1, sticky="ew", padx=10, pady=4)
        self.sport.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Destination IP").grid(row=4, column=0, sticky="w", padx=10, pady=4)
        self.dst = ctk.CTkEntry(self, placeholder_text="8.8.8.8")
        self.dst.grid(row=4, column=1, sticky="ew", padx=10, pady=4)
        self.dst.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Destination port").grid(row=5, column=0, sticky="w", padx=10, pady=4)
        self.dport = ctk.CTkEntry(self, placeholder_text="443")
        self.dport.grid(row=5, column=1, sticky="ew", padx=10, pady=4)
        self.dport.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Protocol").grid(row=6, column=0, sticky="w", padx=10, pady=4)
        self.proto = ctk.CTkOptionMenu(
            self, values=list(self.PROTOS.keys()), command=lambda _: self.notify_change()
        )
        self.proto.set("TCP (6)")
        self.proto.grid(row=6, column=1, sticky="ew", padx=10, pady=4)

        ctk.CTkLabel(self, text="Source interface").grid(row=7, column=0, sticky="w", padx=10, pady=4)
        self.intf = ctk.CTkEntry(self, placeholder_text="port1 / internal")
        self.intf.grid(row=7, column=1, sticky="ew", padx=10, pady=4)
        self.intf.bind("<KeyRelease>", self.notify_change)
        tip(self.intf, "Ingress interface name as on FortiGate")

        self.warn = ctk.CTkLabel(self, text="", text_color="#e74c3c")
        self.warn.grid(row=8, column=0, columnspan=2, sticky="w", padx=10, pady=6)

        self.grid_columnconfigure(1, weight=1)

    def generate_commands(self) -> str:
        src = self.src.get().strip()
        sport = self.sport.get().strip()
        dst = self.dst.get().strip()
        dport = self.dport.get().strip()
        intf = self.intf.get().strip()
        proto = self.PROTOS.get(self.proto.get(), "6")

        errors = []
        if not src or not is_valid_ip(src):
            errors.append("Source IP")
        if not sport or not is_valid_port(sport):
            errors.append("Source port")
        if not dst or not is_valid_ip(dst):
            errors.append("Destination IP")
        if not dport or not is_valid_port(dport):
            errors.append("Destination port")
        if not intf:
            errors.append("Interface")

        if errors:
            self.warn.configure(text=f"Required / invalid: {', '.join(errors)}")
            return (
                "# diagnose firewall iprope lookup "
                "<src_ip> <src_port> <dst_ip> <dst_port> <proto> <src_intf>"
            )

        self.warn.configure(text="")
        return (
            f"diagnose firewall iprope lookup {src} {sport} {dst} {dport} {proto} {intf}"
        )
