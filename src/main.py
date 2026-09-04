#!/usr/bin/env python3
"""FortiDebug Builder - Windows entry point."""

import customtkinter as ctk
from ui.main_window import MainWindow
from core.config import load_config
from core.i18n import set_lang


def main():
    cfg = load_config()
    theme = cfg.get("theme", "Dark")
    lang = cfg.get("language", "uk")
    set_lang(lang)
    ctk.set_appearance_mode(theme)
    ctk.set_default_color_theme("blue")
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
