#!/usr/bin/env python3
"""FortiDebug Builder - Windows entry point."""

import customtkinter as ctk
from ui.main_window import MainWindow
from core.config import load_config
from core.i18n import set_lang
from ui.widgets.scrollable_menu import wire_scrollable_dropdowns


def main():
    cfg = load_config()
    theme = cfg.get("theme", "Dark")
    lang = cfg.get("language", "uk")
    set_lang(lang)
    ctk.set_appearance_mode(theme)
    ctk.set_default_color_theme("blue")
    app = MainWindow()
    # Stock CTk dropdowns do not scroll with mouse wheel on long lists
    wire_scrollable_dropdowns(app, min_items=1, height=300)
    app.mainloop()


if __name__ == "__main__":
    main()
