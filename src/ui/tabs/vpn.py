"""VPN / IKE tab — version-aware syntax."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab
from core.fortios_version import ike_log_filter_cmd, ike_log_filter_clear, DEFAULT_VERSION


class VpnTab(BaseTab):
    def __init__(self, master, on_change=None, get_version=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self.get_version = get_version or (lambda: DEFAULT_VERSION)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(self, text="VPN / IKE", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 15))

        ctk.CTkLabel(self, text="Phase 1 / Gateway name").grid(row=1, column=0, sticky="w", padx=10, pady=4)
        self.phase1 = ctk.CTkEntry(self, placeholder_text="")
        self.phase1.grid(row=1, column=1, sticky="ew", padx=10, pady=4)
        self.phase1.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Phase 2 / Tunnel name").grid(row=2, column=0, sticky="w", padx=10, pady=4)
        self.phase2 = ctk.CTkEntry(self, placeholder_text="")
        self.phase2.grid(row=2, column=1, sticky="ew", padx=10, pady=4)
        self.phase2.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Peer IPv4").grid(row=3, column=0, sticky="w", padx=10, pady=4)
        self.peer = ctk.CTkEntry(self, placeholder_text="")
        self.peer.grid(row=3, column=1, sticky="ew", padx=10, pady=4)
        self.peer.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="IKE debug level").grid(row=4, column=0, sticky="w", padx=10, pady=4)
        self.ike_level = ctk.CTkOptionMenu(
            self,
            values=["-1 (all)", "0", "1", "2", "3", "4"],
            command=lambda _: self.notify_change(),
        )
        self.ike_level.set("-1 (all)")
        self.ike_level.grid(row=4, column=1, sticky="ew", padx=10, pady=4)

        self.show_gateway = ctk.CTkCheckBox(
            self, text="Show IKE gateway list", command=self.notify_change
        )
        self.show_gateway.select()
        self.show_gateway.grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=6)

        self.show_tunnel = ctk.CTkCheckBox(
            self, text="Show tunnel list", command=self.notify_change
        )
        self.show_tunnel.select()
        self.show_tunnel.grid(row=6, column=0, columnspan=2, sticky="w", padx=10, pady=4)

        self.live_debug = ctk.CTkCheckBox(
            self, text="Enable live IKE debug", command=self.notify_change
        )
        self.live_debug.select()
        self.live_debug.grid(row=7, column=0, columnspan=2, sticky="w", padx=10, pady=4)

        self.stop_block = ctk.CTkCheckBox(
            self, text="Append stop-debug block", command=self.notify_change
        )
        self.stop_block.select()
        self.stop_block.grid(row=8, column=0, columnspan=2, sticky="w", padx=10, pady=4)

        self.ver_hint = ctk.CTkLabel(self, text="", text_color="gray")
        self.ver_hint.grid(row=9, column=0, columnspan=2, sticky="w", padx=10, pady=6)

    def generate_commands(self) -> str:
        version = self.get_version()
        filter_cmd = ike_log_filter_cmd(version)
        self.ver_hint.configure(
            text=f"Syntax: {filter_cmd}  (FortiOS {version.value})"
        )

        lines = []

        if self.show_gateway.get():
            lines.append("diagnose vpn ike gateway list")

        if self.show_tunnel.get():
            lines.append("diagnose vpn tunnel list")

        phase1 = self.phase1.get().strip()
        phase2 = self.phase2.get().strip()
        peer = self.peer.get().strip()

        if phase1:
            lines.append(f"diagnose vpn ike gateway list name {phase1}")
        if phase2:
            lines.append(f"diagnose vpn tunnel list name {phase2}")

        if self.live_debug.get():
            lines.append("diagnose debug reset")
            lines.append(ike_log_filter_clear(version))

            if peer:
                # rem-addr4 is common; older may use different names
                lines.append(f"{filter_cmd} rem-addr4 {peer}")
            if phase1:
                lines.append(f"{filter_cmd} name {phase1}")

            level = self.ike_level.get().split()[0]
            lines.append(f"diagnose debug application ike {level}")
            lines.append("diagnose debug console timestamp enable")
            lines.append("diagnose debug enable")

            if self.stop_block.get():
                lines.append("")
                lines.append("# --- reproduce issue, then: ---")
                lines.append("diagnose debug disable")
                lines.append("diagnose debug reset")

        return "\n".join(lines) if lines else "# select options"
