"""Routing tab — OSPF, BGP, Static/RIB + safety for live debug."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab
from core.safety import preamble, epilogue


class RoutingTab(BaseTab):
    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(self, text="Routing", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 12))

        ctk.CTkLabel(self, text="OSPF", font=ctk.CTkFont(weight="bold")).grid(
            row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(6, 2)
        )
        self.ospf_status = ctk.CTkCheckBox(
            self, text="Status / neighbors / interfaces", command=self.notify_change
        )
        self.ospf_status.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.ospf_lsdb = ctk.CTkCheckBox(self, text="LSDB + OSPF routes", command=self.notify_change)
        self.ospf_lsdb.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.ospf_debug = ctk.CTkCheckBox(
            self, text="Live OSPF debug (verbose)", command=self.notify_change
        )
        self.ospf_debug.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        ctk.CTkLabel(self, text="BGP", font=ctk.CTkFont(weight="bold")).grid(
            row=5, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 2)
        )
        self.bgp_summary = ctk.CTkCheckBox(self, text="BGP summary", command=self.notify_change)
        self.bgp_summary.select()
        self.bgp_summary.grid(row=6, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        ctk.CTkLabel(self, text="Neighbor IP").grid(row=7, column=0, sticky="w", padx=10, pady=3)
        self.bgp_neighbor = ctk.CTkEntry(self, placeholder_text="optional")
        self.bgp_neighbor.grid(row=7, column=1, sticky="ew", padx=10, pady=3)
        self.bgp_neighbor.bind("<KeyRelease>", self.notify_change)

        self.bgp_routes = ctk.CTkCheckBox(
            self, text="Routes / advertised-routes (needs neighbor)", command=self.notify_change
        )
        self.bgp_routes.grid(row=8, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.bgp_network = ctk.CTkCheckBox(
            self, text="Locally originated networks", command=self.notify_change
        )
        self.bgp_network.grid(row=9, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.bgp_debug = ctk.CTkCheckBox(self, text="Live BGP debug", command=self.notify_change)
        self.bgp_debug.grid(row=10, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        ctk.CTkLabel(self, text="Static / RIB", font=ctk.CTkFont(weight="bold")).grid(
            row=11, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 2)
        )
        self.static = ctk.CTkCheckBox(self, text="Static routes", command=self.notify_change)
        self.static.grid(row=12, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.rib = ctk.CTkCheckBox(self, text="Full RIB", command=self.notify_change)
        self.rib.grid(row=13, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.rib_db = ctk.CTkCheckBox(
            self, text="RIB database (incl. hidden)", command=self.notify_change
        )
        self.rib_db.grid(row=14, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.proute = ctk.CTkCheckBox(self, text="Policy routes (v4+v6)", command=self.notify_change)
        self.proute.grid(row=15, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        ctk.CTkLabel(self, text="Lookup destination IP").grid(row=16, column=0, sticky="w", padx=10, pady=3)
        self.lookup = ctk.CTkEntry(self, placeholder_text="optional")
        self.lookup.grid(row=16, column=1, sticky="ew", padx=10, pady=3)
        self.lookup.bind("<KeyRelease>", self.notify_change)

        self.timestamps = ctk.CTkCheckBox(
            self, text="Console timestamps (for live debug)", command=self.notify_change
        )
        self.timestamps.select()
        self.timestamps.grid(row=17, column=0, columnspan=2, sticky="w", padx=10, pady=4)

        self.stop_debug = ctk.CTkCheckBox(
            self, text="Append stop-debug block", command=self.notify_change
        )
        self.stop_debug.select()
        self.stop_debug.grid(row=18, column=0, columnspan=2, sticky="w", padx=10, pady=4)

    def generate_commands(self) -> str:
        lines = []

        if self.ospf_status.get():
            lines += [
                "get router info ospf status",
                "get router info ospf neighbor",
                "get router info ospf interface",
            ]
        if self.ospf_lsdb.get():
            lines += ["get router info ospf database", "get router info routing-table ospf"]

        if self.bgp_summary.get():
            lines.append("get router info bgp summary")
        neighbor = self.bgp_neighbor.get().strip()
        if self.bgp_routes.get() and neighbor:
            lines.append(f"get router info bgp neighbors {neighbor} routes")
            lines.append(f"get router info bgp neighbors {neighbor} advertised-routes")
        if self.bgp_network.get():
            lines.append("get router info bgp network")

        if self.static.get():
            lines.append("get router info routing-table static")
        if self.rib.get():
            lines.append("get router info routing-table all")
        if self.rib_db.get():
            lines.append("get router info routing-table database")
        if self.proute.get():
            lines += ["diagnose firewall proute list", "diagnose firewall proute6 list"]

        lookup = self.lookup.get().strip()
        if lookup:
            lines.append(f"get router info routing-table details {lookup}")

        if self.ospf_debug.get() or self.bgp_debug.get():
            lines.extend(preamble(reset=True, timestamps=bool(self.timestamps.get())))
            if self.ospf_debug.get():
                lines.append("diagnose ip router ospf all enable")
                lines.append("diagnose ip router ospf level info")
            if self.bgp_debug.get():
                lines.append("diagnose ip router bgp all enable")
                lines.append("diagnose ip router bgp level info")
            lines.append("diagnose debug enable")
            if self.stop_debug.get():
                lines.extend(
                    [
                        "",
                        "# --- after test: ---",
                        "diagnose debug disable",
                        "diagnose ip router ospf all disable",
                        "diagnose ip router bgp all disable",
                        "diagnose debug reset",
                    ]
                )

        return "\n".join(lines) if lines else "# select options"
