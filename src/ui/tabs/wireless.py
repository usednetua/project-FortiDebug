"""Wireless / CAPWAP diagnostics (FortiAP managed by FortiGate).

Commands verified against Fortinet docs (stable wlac -c wtp|sta|vap across 6.4–7.6).
Always respect global FortiOS selector for banners / future syntax forks.
"""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab
from core.fortios_version import (
    DEFAULT_VERSION,
    version_banner,
    wireless_version_note,
)
from core.safety import preamble, epilogue
from ui.widgets.tooltip import tip


class WirelessTab(BaseTab):
    def __init__(self, master, on_change=None, get_version=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self.get_version = get_version or (lambda: DEFAULT_VERSION)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(
            self, text="Wireless / CAPWAP", font=ctk.CTkFont(size=18, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 8))

        note = ctk.CTkLabel(
            self,
            text="Потрібен wireless-controller / FortiAP. Синтаксис залежить від FortiOS (селектор зліва).",
            text_color="gray",
            wraplength=480,
        )
        note.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 8))

        self.wtp = ctk.CTkCheckBox(
            self, text="wlac -c wtp (managed APs)", command=self.notify_change
        )
        self.wtp.select()
        self.wtp.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=3)
        tip(self.wtp, "diagnose wireless-controller wlac -c wtp")

        self.sta = ctk.CTkCheckBox(
            self, text="wlac -c sta (clients)", command=self.notify_change
        )
        self.sta.select()
        self.sta.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.vap = ctk.CTkCheckBox(
            self, text="wlac -c vap (SSIDs)", command=self.notify_change
        )
        self.vap.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        self.wtp_status = ctk.CTkCheckBox(
            self, text="get wireless-controller wtp-status", command=self.notify_change
        )
        self.wtp_status.grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        ctk.CTkLabel(self, text="STA MAC (filter)").grid(row=6, column=0, sticky="w", padx=10, pady=4)
        self.sta_mac = ctk.CTkEntry(self, placeholder_text="aa:bb:cc:dd:ee:ff")
        self.sta_mac.grid(row=6, column=1, sticky="ew", padx=10, pady=4)
        self.sta_mac.bind("<KeyRelease>", self.notify_change)
        tip(self.sta_mac, "diagnose wireless-controller wlac sta_filter <mac> 1")

        self.cw_acd = ctk.CTkCheckBox(
            self, text="Live CAPWAP debug (cw_acd -1)", command=self.notify_change
        )
        self.cw_acd.grid(row=7, column=0, columnspan=2, sticky="w", padx=10, pady=3)
        tip(self.cw_acd, "diagnose debug application cw_acd -1 — шумно")

        self.timestamps = ctk.CTkCheckBox(
            self, text="Console timestamps", command=self.notify_change
        )
        self.timestamps.select()
        self.timestamps.grid(row=8, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.stop_block = ctk.CTkCheckBox(
            self, text="Append stop-debug block", command=self.notify_change
        )
        self.stop_block.select()
        self.stop_block.grid(row=9, column=0, columnspan=2, sticky="w", padx=10, pady=4)

        self.ver_hint = ctk.CTkLabel(self, text="", text_color="gray", wraplength=480, justify="left")
        self.ver_hint.grid(row=10, column=0, columnspan=2, sticky="w", padx=10, pady=6)

        self.grid_columnconfigure(1, weight=1)

    def generate_commands(self) -> str:
        version = self.get_version()
        note = wireless_version_note(version)
        self.ver_hint.configure(text=f"FortiOS {version.value}: {note}")

        lines = [version_banner(version, note), ""]

        if self.wtp.get():
            lines.append("diagnose wireless-controller wlac -c wtp")
        if self.sta.get():
            lines.append("diagnose wireless-controller wlac -c sta")
        if self.vap.get():
            lines.append("diagnose wireless-controller wlac -c vap")
        if self.wtp_status.get():
            lines.append("get wireless-controller wtp-status")

        mac = self.sta_mac.get().strip()
        if mac:
            lines.append(f"diagnose wireless-controller wlac sta_filter {mac} 1")

        if self.cw_acd.get():
            lines.extend(preamble(reset=True, timestamps=bool(self.timestamps.get())))
            lines.append("diagnose debug application cw_acd -1")
            lines.append("diagnose debug enable")
            lines.extend(epilogue(stop=bool(self.stop_block.get())))

        body = [ln for ln in lines[2:] if ln or ln == ""]
        if not any(ln and not ln.startswith("#") for ln in lines):
            return "\n".join(lines[:1] + ["", "# select options"])
        return "\n".join(lines)
