"""Diagnose Sessions tab."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab


class SessionsTab(BaseTab):
    PROTOCOLS = {
        "Any": None,
        "TCP (6)": 6,
        "UDP (17)": 17,
        "ICMP (1)": 1,
        "GRE (47)": 47,
        "ESP (50)": 50,
    }

    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(self, text="Diagnose Sessions", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 15))

        # Source IP
        ctk.CTkLabel(self, text="Source IP").grid(row=1, column=0, sticky="w", padx=10, pady=4)
        self.src_ip = ctk.CTkEntry(self, placeholder_text="10.1.1.10")
        self.src_ip.grid(row=1, column=1, sticky="ew", padx=10, pady=4)
        self.src_ip.bind("<KeyRelease>", self.notify_change)

        # Destination IP
        ctk.CTkLabel(self, text="Destination IP").grid(row=2, column=0, sticky="w", padx=10, pady=4)
        self.dst_ip = ctk.CTkEntry(self, placeholder_text="8.8.8.8")
        self.dst_ip.grid(row=2, column=1, sticky="ew", padx=10, pady=4)
        self.dst_ip.bind("<KeyRelease>", self.notify_change)

        # Source Port
        ctk.CTkLabel(self, text="Source Port").grid(row=3, column=0, sticky="w", padx=10, pady=4)
        self.src_port = ctk.CTkEntry(self, placeholder_text="")
        self.src_port.grid(row=3, column=1, sticky="ew", padx=10, pady=4)
        self.src_port.bind("<KeyRelease>", self.notify_change)

        # Destination Port
        ctk.CTkLabel(self, text="Destination Port").grid(row=4, column=0, sticky="w", padx=10, pady=4)
        self.dst_port = ctk.CTkEntry(self, placeholder_text="")
        self.dst_port.grid(row=4, column=1, sticky="ew", padx=10, pady=4)
        self.dst_port.bind("<KeyRelease>", self.notify_change)

        # Protocol
        ctk.CTkLabel(self, text="Protocol").grid(row=5, column=0, sticky="w", padx=10, pady=4)
        self.proto = ctk.CTkOptionMenu(
            self, values=list(self.PROTOCOLS.keys()), command=lambda _: self.notify_change()
        )
        self.proto.set("Any")
        self.proto.grid(row=5, column=1, sticky="ew", padx=10, pady=4)

        # VDOM
        ctk.CTkLabel(self, text="VDOM index").grid(row=6, column=0, sticky="w", padx=10, pady=4)
        self.vdom = ctk.CTkEntry(self, placeholder_text="(optional)")
        self.vdom.grid(row=6, column=1, sticky="ew", padx=10, pady=4)
        self.vdom.bind("<KeyRelease>", self.notify_change)

        # Checkboxes
        self.negate = ctk.CTkCheckBox(self, text="Negate filter", command=self.notify_change)
        self.negate.grid(row=7, column=0, columnspan=2, sticky="w", padx=10, pady=6)

        self.include_stats = ctk.CTkCheckBox(self, text="Include session stats", command=self.notify_change)
        self.include_stats.grid(row=8, column=0, columnspan=2, sticky="w", padx=10, pady=4)

        self.append_list = ctk.CTkCheckBox(self, text="Append session list", command=self.notify_change)
        self.append_list.select()
        self.append_list.grid(row=9, column=0, columnspan=2, sticky="w", padx=10, pady=4)

    def generate_commands(self) -> str:
        lines = ["diagnose sys session filter clear"]

        src = self.src_ip.get().strip()
        if src:
            lines.append(f"diagnose sys session filter src {src}")

        dst = self.dst_ip.get().strip()
        if dst:
            lines.append(f"diagnose sys session filter dst {dst}")

        sport = self.src_port.get().strip()
        if sport:
            lines.append(f"diagnose sys session filter sport {sport}")

        dport = self.dst_port.get().strip()
        if dport:
            lines.append(f"diagnose sys session filter dport {dport}")

        proto_name = self.proto.get()
        proto_val = self.PROTOCOLS.get(proto_name)
        if proto_val is not None:
            lines.append(f"diagnose sys session filter proto {proto_val}")

        vdom = self.vdom.get().strip()
        if vdom:
            lines.append(f"diagnose sys session filter vd {vdom}")

        if self.negate.get():
            lines.append("diagnose sys session filter negate enable")

        if self.include_stats.get():
            lines.append("diagnose sys session stat")

        if self.append_list.get():
            lines.append("diagnose sys session list")

        return "\n".join(lines)
