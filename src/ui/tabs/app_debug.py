"""Application Debug — realtime debug + diagnose test application."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab
from core.safety import preamble, epilogue
from ui.widgets.tooltip import tip


class AppDebugTab(BaseTab):
    DAEMONS = {
        "authd": "Authentication / SSL VPN users / FSSO",
        "dnsproxy": "DNS proxy / resolution",
        "ike": "IPsec IKE (prefer VPN tab for filters)",
        "sslvpn": "SSL VPN daemon",
        "miglogd": "Local logging (older)",
        "fgtlogd": "FortiAnalyzer / FortiCloud log (7.2.4+)",
        "urlfilter": "Web filter",
        "wad": "Web proxy / explicit proxy",
        "sip": "SIP / VoIP",
        "fnbamd": "Certificate / RADIUS / LDAP auth",
        "eap_proxy": "EAP (IPsec XAuth / SAML related)",
        "samld": "SAML daemon",
        "dhcprelay": "DHCP relay",
        "hasync": "HA sync",
    }

    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(
            self, text="Application Debug", font=ctk.CTkFont(size=18, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 12))

        warn = ctk.CTkLabel(
            self,
            text="⚠ Realtime debug — CPU intensive. Test mode — status snapshot (safer).",
            text_color="#e67e22",
        )
        warn.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 8))

        ctk.CTkLabel(self, text="Mode").grid(row=2, column=0, sticky="w", padx=10, pady=4)
        self.mode = ctk.CTkOptionMenu(
            self,
            values=["Realtime debug", "Test / status"],
            command=lambda _: self.notify_change(),
        )
        self.mode.set("Realtime debug")
        self.mode.grid(row=2, column=1, sticky="ew", padx=10, pady=4)
        tip(self.mode, "Realtime: diagnose debug application … | Test: diagnose test application …")

        ctk.CTkLabel(self, text="Daemon").grid(row=3, column=0, sticky="w", padx=10, pady=4)
        self.daemon = ctk.CTkOptionMenu(
            self,
            values=list(self.DAEMONS.keys()),
            command=self._on_daemon,
        )
        self.daemon.set("authd")
        self.daemon.grid(row=3, column=1, sticky="ew", padx=10, pady=4)

        self.hint = ctk.CTkLabel(self, text=self.DAEMONS["authd"], text_color="gray")
        self.hint.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        ctk.CTkLabel(self, text="Level").grid(row=5, column=0, sticky="w", padx=10, pady=4)
        self.level = ctk.CTkOptionMenu(
            self,
            values=["-1 (all)", "0", "1", "2", "3", "4", "7", "99", "255"],
            command=lambda _: self.notify_change(),
        )
        self.level.set("-1 (all)")
        self.level.grid(row=5, column=1, sticky="ew", padx=10, pady=4)
        tip(self.level, "Realtime: debug level. Test: test_level (див. ? на FGT)")

        ctk.CTkLabel(self, text="Duration (min, 0=unlimited)").grid(
            row=6, column=0, sticky="w", padx=10, pady=4
        )
        self.duration = ctk.CTkEntry(self, placeholder_text="30")
        self.duration.grid(row=6, column=1, sticky="ew", padx=10, pady=4)
        self.duration.bind("<KeyRelease>", self.notify_change)

        self.reset = ctk.CTkCheckBox(self, text="Reset debug first", command=self.notify_change)
        self.reset.select()
        self.reset.grid(row=7, column=0, columnspan=2, sticky="w", padx=10, pady=4)

        self.timestamps = ctk.CTkCheckBox(
            self, text="Console timestamps", command=self.notify_change
        )
        self.timestamps.select()
        self.timestamps.grid(row=8, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.debug_info = ctk.CTkCheckBox(
            self, text="diagnose debug info", command=self.notify_change
        )
        self.debug_info.grid(row=9, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.stop_block = ctk.CTkCheckBox(
            self, text="Append stop-debug block", command=self.notify_change
        )
        self.stop_block.select()
        self.stop_block.grid(row=10, column=0, columnspan=2, sticky="w", padx=10, pady=4)

    def _on_daemon(self, name: str):
        self.hint.configure(text=self.DAEMONS.get(name, ""))
        self.notify_change()

    def generate_commands(self) -> str:
        daemon = self.daemon.get()
        level = self.level.get().split()[0]
        duration = self.duration.get().strip()
        test_mode = self.mode.get().startswith("Test")

        if test_mode:
            return f"diagnose test application {daemon} {level}"

        lines = preamble(
            reset=bool(self.reset.get()),
            timestamps=bool(self.timestamps.get()),
            debug_info=bool(self.debug_info.get()),
        )

        if duration != "":
            lines.append(f"diagnose debug duration {duration}")

        lines.append(f"diagnose debug application {daemon} {level}")
        lines.append("diagnose debug enable")
        lines.extend(epilogue(stop=bool(self.stop_block.get())))
        return "\n".join(lines)
