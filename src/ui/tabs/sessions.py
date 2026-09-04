"""Diagnose Sessions tab — IPv4/IPv6, clear, full-stat."""

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
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 12))

        self.ipv6 = ctk.CTkCheckBox(self, text="IPv6 (session6)", command=self.notify_change)
        self.ipv6.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=4)

        ctk.CTkLabel(self, text="Source IP").grid(row=2, column=0, sticky="w", padx=10, pady=4)
        self.src_ip = ctk.CTkEntry(self, placeholder_text="10.1.1.10")
        self.src_ip.grid(row=2, column=1, sticky="ew", padx=10, pady=4)
        self.src_ip.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Destination IP").grid(row=3, column=0, sticky="w", padx=10, pady=4)
        self.dst_ip = ctk.CTkEntry(self, placeholder_text="8.8.8.8")
        self.dst_ip.grid(row=3, column=1, sticky="ew", padx=10, pady=4)
        self.dst_ip.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Source Port").grid(row=4, column=0, sticky="w", padx=10, pady=4)
        self.src_port = ctk.CTkEntry(self, placeholder_text="")
        self.src_port.grid(row=4, column=1, sticky="ew", padx=10, pady=4)
        self.src_port.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Destination Port").grid(row=5, column=0, sticky="w", padx=10, pady=4)
        self.dst_port = ctk.CTkEntry(self, placeholder_text="")
        self.dst_port.grid(row=5, column=1, sticky="ew", padx=10, pady=4)
        self.dst_port.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Protocol").grid(row=6, column=0, sticky="w", padx=10, pady=4)
        self.proto = ctk.CTkOptionMenu(
            self, values=list(self.PROTOCOLS.keys()), command=lambda _: self.notify_change()
        )
        self.proto.set("Any")
        self.proto.grid(row=6, column=1, sticky="ew", padx=10, pady=4)

        ctk.CTkLabel(self, text="VDOM index").grid(row=7, column=0, sticky="w", padx=10, pady=4)
        self.vdom = ctk.CTkEntry(self, placeholder_text="(optional)")
        self.vdom.grid(row=7, column=1, sticky="ew", padx=10, pady=4)
        self.vdom.bind("<KeyRelease>", self.notify_change)

        self.negate = ctk.CTkCheckBox(self, text="Negate filter", command=self.notify_change)
        self.negate.grid(row=8, column=0, columnspan=2, sticky="w", padx=10, pady=6)

        self.include_stats = ctk.CTkCheckBox(
            self, text="Include session stats", command=self.notify_change
        )
        self.include_stats.grid(row=9, column=0, columnspan=2, sticky="w", padx=10, pady=4)

        self.full_stat = ctk.CTkCheckBox(
            self, text="Include full-stat (conserve thresholds)", command=self.notify_change
        )
        self.full_stat.grid(row=10, column=0, columnspan=2, sticky="w", padx=10, pady=4)

        self.append_list = ctk.CTkCheckBox(
            self, text="Append session list", command=self.notify_change
        )
        self.append_list.select()
        self.append_list.grid(row=11, column=0, columnspan=2, sticky="w", padx=10, pady=4)

        self.clear_matched = ctk.CTkCheckBox(
            self, text="Clear matched sessions (after list)", command=self.notify_change
        )
        self.clear_matched.grid(row=12, column=0, columnspan=2, sticky="w", padx=10, pady=4)

    def generate_commands(self) -> str:
        pfx = "diagnose sys session6" if self.ipv6.get() else "diagnose sys session"
        lines = [f"{pfx} filter clear"]

        src = self.src_ip.get().strip()
        if src:
            lines.append(f"{pfx} filter src {src}")

        dst = self.dst_ip.get().strip()
        if dst:
            lines.append(f"{pfx} filter dst {dst}")

        sport = self.src_port.get().strip()
        if sport:
            lines.append(f"{pfx} filter sport {sport}")

        dport = self.dst_port.get().strip()
        if dport:
            lines.append(f"{pfx} filter dport {dport}")

        proto_val = self.PROTOCOLS.get(self.proto.get())
        if proto_val is not None:
            lines.append(f"{pfx} filter proto {proto_val}")

        vdom = self.vdom.get().strip()
        if vdom:
            lines.append(f"{pfx} filter vd {vdom}")

        if self.negate.get():
            lines.append(f"{pfx} filter negate enable")

        if self.include_stats.get():
            lines.append(f"{pfx} stat")

        if self.full_stat.get():
            lines.append("diagnose sys session full-stat")

        if self.append_list.get():
            lines.append(f"{pfx} list")

        if self.clear_matched.get():
            lines.append(f"{pfx} clear")

        return "\n".join(lines)
