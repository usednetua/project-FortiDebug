"""Main application window."""

import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog
import pyperclip

from ui.tabs.sessions import SessionsTab
from ui.tabs.ping import PingTab
from ui.tabs.traceroute import TracerouteTab
from ui.tabs.sniffer import SnifferTab
from ui.tabs.flows import FlowsTab
from ui.tabs.network import NetworkTab
from ui.tabs.policy_lookup import PolicyLookupTab
from ui.tabs.vpn import VpnTab
from ui.tabs.system_top import SystemTopTab
from ui.tabs.ha import HaTab
from ui.tabs.routing import RoutingTab
from ui.tabs.ssh_logger import SshLoggerTab
from ui.tabs.saved import SavedTab
from ui.tabs.recipes import RecipesTab
from ui.tabs.app_debug import AppDebugTab
from ui.tabs.tac import TacTab
from ui.tabs.settings import SettingsTab
from ui.tabs.about import AboutTab
from core.storage import save_command
from core.fortios_version import (
    FortiOSVersion,
    DEFAULT_VERSION,
    VERSION_LABELS,
    parse_version,
)
from core.i18n import t, set_lang, get_lang

STOP_DEBUG_BLOCK = "diagnose debug disable\ndiagnose debug reset"

NAV_KEYS = [
    ("recipes", "recipes"),
    ("sessions", "sessions"),
    ("ping", "ping"),
    ("traceroute", "traceroute"),
    ("sniffer", "sniffer"),
    ("flows", "flows"),
    ("network", "network"),
    ("policy_lookup", "policy_lookup"),
    ("vpn", "vpn"),
    ("app_debug", "app_debug"),
    ("system_top", "system_top"),
    ("ha", "ha"),
    ("routing", "routing"),
    ("tac", "tac"),
    ("ssh_logger", "ssh_logger"),
    ("saved", "saved"),
    ("settings", "settings"),
    ("about", "about"),
]


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        set_lang("uk")
        self.title(t("app_title"))
        self.geometry("1100x760")
        self.minsize(900, 600)

        self.fortios_version = DEFAULT_VERSION

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_rowconfigure(22, weight=1)

        self.logo = ctk.CTkLabel(
            self.sidebar, text="FortiDebug", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo.grid(row=0, column=0, padx=20, pady=(16, 4))

        self.fortios_lbl = ctk.CTkLabel(self.sidebar, text=t("fortios"), font=ctk.CTkFont(size=12))
        self.fortios_lbl.grid(row=1, column=0, padx=12, sticky="w")
        self.version_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=list(VERSION_LABELS.values()),
            command=self._on_version_change,
            width=160,
        )
        self.version_menu.set(VERSION_LABELS[DEFAULT_VERSION])
        self.version_menu.grid(row=2, column=0, padx=12, pady=(0, 8), sticky="ew")

        self.nav_buttons = {}
        for i, (key, _) in enumerate(NAV_KEYS, start=3):
            btn = ctk.CTkButton(
                self.sidebar,
                text=t(key),
                command=lambda k=key: self.show_tab(k),
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                anchor="w",
            )
            btn.grid(row=i, column=0, padx=10, pady=1, sticky="ew")
            self.nav_buttons[key] = btn

        self.content = ctk.CTkFrame(self, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        self.bottom = ctk.CTkFrame(self)
        self.bottom.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
        self.bottom.grid_columnconfigure(0, weight=1)

        self.preview = ctk.CTkTextbox(
            self.bottom, height=130, font=ctk.CTkFont(family="Consolas", size=13)
        )
        self.preview.grid(row=0, column=0, columnspan=5, sticky="ew", padx=5, pady=(5, 8))

        self.btn_copy = ctk.CTkButton(self.bottom, text=t("copy"), width=90, command=self.copy_commands)
        self.btn_copy.grid(row=1, column=0, padx=4, pady=5, sticky="w")

        self.btn_copy_stop = ctk.CTkButton(
            self.bottom, text=t("copy_stop"), width=120, command=self.copy_stop_debug
        )
        self.btn_copy_stop.grid(row=1, column=1, padx=4, pady=5, sticky="w")

        self.btn_save_txt = ctk.CTkButton(
            self.bottom, text=t("save_txt"), width=100, command=self.save_txt
        )
        self.btn_save_txt.grid(row=1, column=2, padx=4, pady=5, sticky="w")

        self.btn_save_later = ctk.CTkButton(
            self.bottom, text=t("save_later"), width=120, command=self.save_for_later
        )
        self.btn_save_later.grid(row=1, column=3, padx=4, pady=5, sticky="w")

        self.bind("<Control-Return>", lambda e: self.copy_commands())
        self.bind("<Control-s>", lambda e: self.save_txt())
        self.bind("<Control-S>", lambda e: self.save_txt())

        self.tabs = {}
        self.current_tab = None

        self.tabs["recipes"] = RecipesTab(
            self.content, on_change=self.on_tab_change, get_version=self.get_version
        )
        self.tabs["sessions"] = SessionsTab(self.content, on_change=self.on_tab_change)
        self.tabs["ping"] = PingTab(self.content, on_change=self.on_tab_change)
        self.tabs["traceroute"] = TracerouteTab(self.content, on_change=self.on_tab_change)
        self.tabs["sniffer"] = SnifferTab(self.content, on_change=self.on_tab_change)
        self.tabs["flows"] = FlowsTab(self.content, on_change=self.on_tab_change)
        self.tabs["network"] = NetworkTab(self.content, on_change=self.on_tab_change)
        self.tabs["policy_lookup"] = PolicyLookupTab(self.content, on_change=self.on_tab_change)
        self.tabs["vpn"] = VpnTab(self.content, on_change=self.on_tab_change, get_version=self.get_version)
        self.tabs["app_debug"] = AppDebugTab(self.content, on_change=self.on_tab_change)
        self.tabs["system_top"] = SystemTopTab(self.content, on_change=self.on_tab_change)
        self.tabs["ha"] = HaTab(self.content, on_change=self.on_tab_change)
        self.tabs["routing"] = RoutingTab(self.content, on_change=self.on_tab_change)
        self.tabs["tac"] = TacTab(self.content, on_change=self.on_tab_change)
        self.tabs["ssh_logger"] = SshLoggerTab(self.content, on_change=self.on_tab_change)
        self.tabs["saved"] = SavedTab(self.content, on_change=self.on_tab_change)
        self.tabs["settings"] = SettingsTab(
            self.content,
            on_change=self.on_tab_change,
            on_theme=self._set_theme,
            on_lang=self._set_lang,
        )
        self.tabs["about"] = AboutTab(self.content, on_change=self.on_tab_change)

        self.show_tab("recipes")

    def get_version(self) -> FortiOSVersion:
        return self.fortios_version

    def _on_version_change(self, label: str):
        self.fortios_version = parse_version(label)
        self.on_tab_change()

    def _set_theme(self, mode: str):
        ctk.set_appearance_mode(mode)

    def _set_lang(self, lang: str):
        set_lang(lang)
        self._refresh_ui_labels()

    def _refresh_ui_labels(self):
        self.title(t("app_title"))
        self.fortios_lbl.configure(text=t("fortios"))
        for key, btn in self.nav_buttons.items():
            btn.configure(text=t(key))
        self.btn_copy.configure(text=t("copy"))
        self.btn_copy_stop.configure(text=t("copy_stop"))
        self.btn_save_txt.configure(text=t("save_txt"))
        self.btn_save_later.configure(text=t("save_later"))
        if hasattr(self.tabs.get("settings"), "refresh_labels"):
            self.tabs["settings"].refresh_labels()
        if hasattr(self.tabs.get("about"), "refresh_labels"):
            self.tabs["about"].refresh_labels()

    def show_tab(self, key: str):
        if self.current_tab is not None:
            self.tabs[self.current_tab].grid_forget()

        for k, btn in self.nav_buttons.items():
            btn.configure(fg_color=("gray75", "gray25") if k == key else "transparent")

        tab = self.tabs[key]
        tab.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.current_tab = key

        if key == "saved" and hasattr(tab, "refresh"):
            tab.refresh()

        if hasattr(tab, "generate_commands"):
            self.on_tab_change()
        else:
            self.preview.delete("1.0", "end")

    def on_tab_change(self):
        tab = self.tabs.get(self.current_tab)
        if tab and hasattr(tab, "generate_commands"):
            cmds = tab.generate_commands()
            self.preview.delete("1.0", "end")
            self.preview.insert("1.0", cmds)

    def copy_commands(self):
        text = self.preview.get("1.0", "end-1c").strip()
        if text:
            pyperclip.copy(text)
            messagebox.showinfo(t("copied"), t("copied_msg"))

    def copy_stop_debug(self):
        pyperclip.copy(STOP_DEBUG_BLOCK)
        messagebox.showinfo(t("copied"), t("stop_copied"))

    def save_txt(self):
        text = self.preview.get("1.0", "end-1c").strip()
        if not text:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title=t("save_txt"),
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            messagebox.showinfo(t("saved_title"), path)

    def save_for_later(self):
        text = self.preview.get("1.0", "end-1c").strip()
        if not text or text.startswith("#"):
            messagebox.showwarning(t("empty"), t("empty"))
            return
        title = simpledialog.askstring(t("save_later"), "Title:")
        if not title:
            return
        category = simpledialog.askstring(t("save_later"), "Category:") or ""
        notes = simpledialog.askstring(t("save_later"), "Notes:") or ""
        save_command(title.strip(), text, category.strip(), notes.strip())
        messagebox.showinfo(t("saved_title"), title.strip())
        if "saved" in self.tabs and hasattr(self.tabs["saved"], "refresh"):
            self.tabs["saved"].refresh()
