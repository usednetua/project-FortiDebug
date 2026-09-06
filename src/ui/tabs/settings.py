"""Settings tab — theme, language, VDOM name→index map (persisted)."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab
from core.i18n import t, get_lang
from core.config import load_config, save_config
from core.vdom import normalize_vdom_map, vdom_map_to_text
from ui.widgets.tooltip import tip


class SettingsTab(BaseTab):
    def __init__(self, master, on_change=None, on_theme=None, on_lang=None, on_vdom_map=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self.on_theme = on_theme
        self.on_lang = on_lang
        self.on_vdom_map = on_vdom_map
        self._build_ui()

    def _build_ui(self):
        cfg = load_config()

        self.title_lbl = ctk.CTkLabel(
            self, text=t("settings_title"), font=ctk.CTkFont(size=18, weight="bold")
        )
        self.title_lbl.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 16))

        self.theme_lbl = ctk.CTkLabel(self, text=t("theme"))
        self.theme_lbl.grid(row=1, column=0, sticky="w", padx=10, pady=6)

        self.theme_menu = ctk.CTkOptionMenu(
            self,
            values=[t("theme_light"), t("theme_dark"), t("theme_system")],
            command=self._theme_changed,
        )
        theme = cfg.get("theme", "Dark")
        theme_map = {"Light": t("theme_light"), "Dark": t("theme_dark"), "System": t("theme_system")}
        self.theme_menu.set(theme_map.get(theme, t("theme_dark")))
        self.theme_menu.grid(row=1, column=1, sticky="ew", padx=10, pady=6)

        self.lang_lbl = ctk.CTkLabel(self, text=t("language"))
        self.lang_lbl.grid(row=2, column=0, sticky="w", padx=10, pady=6)

        self.lang_menu = ctk.CTkOptionMenu(
            self,
            values=["English", "Українська"],
            command=self._lang_changed,
        )
        self.lang_menu.set("Українська" if get_lang() == "uk" else "English")
        self.lang_menu.grid(row=2, column=1, sticky="ew", padx=10, pady=6)

        # --- VDOM map ---
        self.vdom_map_lbl = ctk.CTkLabel(
            self, text=t("vdom_map"), font=ctk.CTkFont(weight="bold")
        )
        self.vdom_map_lbl.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=(16, 4))

        self.vdom_map_hint = ctk.CTkLabel(
            self,
            text=t("vdom_map_hint"),
            text_color="gray",
            wraplength=420,
            justify="left",
        )
        self.vdom_map_hint.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 4))

        self.vdom_map_box = ctk.CTkTextbox(
            self, height=110, font=ctk.CTkFont(family="Consolas", size=13)
        )
        raw_map = cfg.get("vdom_map") or {"root": "0"}
        self.vdom_map_box.insert("1.0", vdom_map_to_text(normalize_vdom_map(raw_map)))
        self.vdom_map_box.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=4)
        tip(self.vdom_map_box, t("vdom_map_tip"))

        self.vdom_map_btn = ctk.CTkButton(
            self, text=t("vdom_map_save"), width=160, command=self._save_vdom_map
        )
        self.vdom_map_btn.grid(row=6, column=0, sticky="w", padx=10, pady=(4, 8))

        self.vdom_map_status = ctk.CTkLabel(self, text="", text_color="gray")
        self.vdom_map_status.grid(row=6, column=1, sticky="w", padx=10, pady=(4, 8))

        self.grid_columnconfigure(1, weight=1)

    def _theme_changed(self, label: str):
        mapping = {
            t("theme_light"): "Light",
            t("theme_dark"): "Dark",
            t("theme_system"): "System",
            "Light": "Light",
            "Dark": "Dark",
            "System": "System",
            "Світла": "Light",
            "Темна": "Dark",
            "Системна": "System",
        }
        mode = mapping.get(label, "Dark")
        save_config({"theme": mode})
        if self.on_theme:
            self.on_theme(mode)

    def _lang_changed(self, label: str):
        lang = "uk" if label.startswith("Укр") or label == "Ukrainian" else "en"
        save_config({"language": lang})
        if self.on_lang:
            self.on_lang(lang)

    def _save_vdom_map(self):
        text = self.vdom_map_box.get("1.0", "end-1c")
        mapping = normalize_vdom_map(text)
        if not mapping:
            mapping = {"root": "0"}
        save_config({"vdom_map": mapping})
        # normalize display
        self.vdom_map_box.delete("1.0", "end")
        self.vdom_map_box.insert("1.0", vdom_map_to_text(mapping))
        self.vdom_map_status.configure(text=t("vdom_map_saved"))
        if self.on_vdom_map:
            self.on_vdom_map(mapping)

    def refresh_labels(self):
        self.title_lbl.configure(text=t("settings_title"))
        self.theme_lbl.configure(text=t("theme"))
        self.lang_lbl.configure(text=t("language"))
        self.theme_menu.configure(
            values=[t("theme_light"), t("theme_dark"), t("theme_system")]
        )
        self.vdom_map_lbl.configure(text=t("vdom_map"))
        self.vdom_map_hint.configure(text=t("vdom_map_hint"))
        self.vdom_map_btn.configure(text=t("vdom_map_save"))

    def generate_commands(self) -> str:
        return "# Settings — no CLI output"
