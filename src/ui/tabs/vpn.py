"""VPN / IKE + SSL VPN tab."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab
from core.fortios_version import (
    DEFAULT_VERSION,
    ike_log_filter_clear,
    ike_log_filter_base,
    ike_filter_remote_peer,
    ike_filter_name,
    ike_filter_interface,
    uses_new_ike_filter_syntax,
)
from core.safety import preamble, epilogue
from ui.widgets.tooltip import tip


class VpnTab(BaseTab):
    def __init__(self, master, on_change=None, get_version=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self.get_version = get_version or (lambda: DEFAULT_VERSION)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(self, text="VPN / IKE / SSL", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 10))

        ctk.CTkLabel(self, text="Phase 1 / Gateway name").grid(row=1, column=0, sticky="w", padx=10, pady=3)
        self.phase1 = ctk.CTkEntry(self, placeholder_text="")
        self.phase1.grid(row=1, column=1, sticky="ew", padx=10, pady=3)
        self.phase1.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Phase 2 / Tunnel name").grid(row=2, column=0, sticky="w", padx=10, pady=3)
        self.phase2 = ctk.CTkEntry(self, placeholder_text="")
        self.phase2.grid(row=2, column=1, sticky="ew", padx=10, pady=3)
        self.phase2.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Peer IPv4 (remote)").grid(row=3, column=0, sticky="w", padx=10, pady=3)
        self.peer = ctk.CTkEntry(self, placeholder_text="")
        self.peer.grid(row=3, column=1, sticky="ew", padx=10, pady=3)
        self.peer.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Interface index").grid(row=4, column=0, sticky="w", padx=10, pady=3)
        self.ifindex = ctk.CTkEntry(self, placeholder_text="optional (0=all)")
        self.ifindex.grid(row=4, column=1, sticky="ew", padx=10, pady=3)
        self.ifindex.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="IKE debug level").grid(row=5, column=0, sticky="w", padx=10, pady=3)
        self.ike_level = ctk.CTkOptionMenu(
            self,
            values=["-1 (all)", "0", "1", "2", "3", "4"],
            command=lambda _: self.notify_change(),
        )
        self.ike_level.set("-1 (all)")
        self.ike_level.grid(row=5, column=1, sticky="ew", padx=10, pady=3)

        ctk.CTkLabel(self, text="IPsec", font=ctk.CTkFont(weight="bold")).grid(
            row=6, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 2)
        )

        self.show_gateway = ctk.CTkCheckBox(
            self, text="Show IKE gateway list", command=self.notify_change
        )
        self.show_gateway.select()
        self.show_gateway.grid(row=7, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.show_tunnel = ctk.CTkCheckBox(
            self, text="Show tunnel list", command=self.notify_change
        )
        self.show_tunnel.select()
        self.show_tunnel.grid(row=8, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.show_status = ctk.CTkCheckBox(
            self, text="IKE status + tunnel stats", command=self.notify_change
        )
        self.show_status.grid(row=9, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.live_debug = ctk.CTkCheckBox(
            self, text="Enable live IKE debug", command=self.notify_change
        )
        self.live_debug.select()
        self.live_debug.grid(row=10, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        ctk.CTkLabel(self, text="SSL VPN", font=ctk.CTkFont(weight="bold")).grid(
            row=11, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 2)
        )

        self.ssl_monitor = ctk.CTkCheckBox(
            self, text="get vpn ssl monitor", command=self.notify_change
        )
        self.ssl_monitor.grid(row=12, column=0, columnspan=2, sticky="w", padx=10, pady=2)
        tip(self.ssl_monitor, "Активні SSL VPN користувачі / тунелі")

        self.ssl_list = ctk.CTkCheckBox(
            self, text="diagnose vpn ssl list", command=self.notify_change
        )
        self.ssl_list.grid(row=13, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.ssl_debug = ctk.CTkCheckBox(
            self, text="Live sslvpn debug (-1)", command=self.notify_change
        )
        self.ssl_debug.grid(row=14, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.timestamps = ctk.CTkCheckBox(
            self, text="Console timestamps", command=self.notify_change
        )
        self.timestamps.select()
        self.timestamps.grid(row=15, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.stop_block = ctk.CTkCheckBox(
            self, text="Append stop-debug block", command=self.notify_change
        )
        self.stop_block.select()
        self.stop_block.grid(row=16, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.ver_hint = ctk.CTkLabel(self, text="", text_color="gray", wraplength=480, justify="left")
        self.ver_hint.grid(row=17, column=0, columnspan=2, sticky="w", padx=10, pady=6)

    def generate_commands(self) -> str:
        version = self.get_version()
        base = ike_log_filter_base(version)
        new = uses_new_ike_filter_syntax(version)

        self.ver_hint.configure(
            text=(
                f"FortiOS {version.value}: «{base}» + rem-addr4 (з 7.4.1)"
                if new
                else f"FortiOS {version.value}: «{base}» + dst-addr4 (до 7.4.1)"
            )
        )

        lines = []
        phase1 = self.phase1.get().strip()
        phase2 = self.phase2.get().strip()
        peer = self.peer.get().strip()
        ifidx = self.ifindex.get().strip()

        if self.show_status.get():
            lines.append("diagnose vpn ike status")
            lines.append("diagnose vpn ipsec status")

        if self.show_gateway.get():
            lines.append("diagnose vpn ike gateway list")
            if phase1:
                lines.append(f"diagnose vpn ike gateway list name {phase1}")

        if self.show_tunnel.get():
            lines.append("diagnose vpn tunnel list")
            if phase2:
                lines.append(f"diagnose vpn tunnel list name {phase2}")

        if self.ssl_monitor.get():
            lines.append("get vpn ssl monitor")
        if self.ssl_list.get():
            lines.append("diagnose vpn ssl list")

        need_live = self.live_debug.get() or self.ssl_debug.get()
        if need_live:
            lines.extend(preamble(reset=True, timestamps=bool(self.timestamps.get())))
            if self.live_debug.get():
                lines.append(ike_log_filter_clear(version))
                if peer:
                    lines.append(ike_filter_remote_peer(version, peer))
                if phase1:
                    lines.append(ike_filter_name(version, phase1))
                if ifidx:
                    lines.append(ike_filter_interface(version, ifidx))
                level = self.ike_level.get().split()[0]
                lines.append(f"diagnose debug application ike {level}")
            if self.ssl_debug.get():
                lines.append("diagnose debug application sslvpn -1")
            lines.append("diagnose debug enable")
            lines.extend(epilogue(stop=bool(self.stop_block.get())))

        return "\n".join(lines) if lines else "# select options"
