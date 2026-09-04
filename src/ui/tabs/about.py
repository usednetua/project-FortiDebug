"""About tab."""

import customtkinter as ctk
import webbrowser
from ui.tabs.base_tab import BaseTab
from core.i18n import t

APP_VERSION = "0.2.1"
AUTHOR = "used.net.ua"
WEBSITE = "https://used.net.ua"


class AboutTab(BaseTab):
    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self._build_ui()

    def _build_ui(self):
        self.title_lbl = ctk.CTkLabel(
            self, text=t("about_title"), font=ctk.CTkFont(size=18, weight="bold")
        )
        self.title_lbl.grid(row=0, column=0, sticky="w", padx=10, pady=(5, 20))

        self.ver_lbl = ctk.CTkLabel(
            self, text=f"{t('version')}: {APP_VERSION}", font=ctk.CTkFont(size=14)
        )
        self.ver_lbl.grid(row=1, column=0, sticky="w", padx=10, pady=6)

        self.author_lbl = ctk.CTkLabel(
            self, text=f"{t('author')}: {AUTHOR}", font=ctk.CTkFont(size=14)
        )
        self.author_lbl.grid(row=2, column=0, sticky="w", padx=10, pady=6)

        self.web_lbl = ctk.CTkLabel(
            self, text=f"{t('website')}: {WEBSITE}", font=ctk.CTkFont(size=14)
        )
        self.web_lbl.grid(row=3, column=0, sticky="w", padx=10, pady=6)

        self.link_btn = ctk.CTkButton(
            self, text=WEBSITE, width=200, command=lambda: webbrowser.open(WEBSITE)
        )
        self.link_btn.grid(row=4, column=0, sticky="w", padx=10, pady=16)

        ctk.CTkLabel(
            self,
            text="FortiDebug Builder — Windows CLI helper for FortiGate diagnostics.",
            text_color="gray",
            wraplength=480,
        ).grid(row=5, column=0, sticky="w", padx=10, pady=8)

    def refresh_labels(self):
        self.title_lbl.configure(text=t("about_title"))
        self.ver_lbl.configure(text=f"{t('version')}: {APP_VERSION}")
        self.author_lbl.configure(text=f"{t('author')}: {AUTHOR}")
        self.web_lbl.configure(text=f"{t('website')}: {WEBSITE}")

    def generate_commands(self) -> str:
        return "# About — no CLI output"
