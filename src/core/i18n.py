"""Simple EN/UK strings for UI."""

STRINGS = {
    "en": {
        "app_title": "FortiDebug Builder",
        "fortios": "FortiOS",
        "recipes": "Recipes",
        "sessions": "Sessions",
        "ping": "Ping",
        "traceroute": "Traceroute",
        "sniffer": "Sniffer",
        "flows": "Flows",
        "vpn": "VPN",
        "app_debug": "App Debug",
        "system_top": "System Top",
        "ha": "HA",
        "routing": "Routing",
        "tac": "TAC / Support",
        "ssh_logger": "SSH Logger",
        "saved": "Saved Commands",
        "settings": "Settings",
        "about": "About",
        "copy": "Copy",
        "copy_stop": "Copy stop-debug",
        "save_txt": "Save .txt",
        "save_later": "Save for Later",
        "settings_title": "Settings",
        "theme": "Theme",
        "theme_light": "Light",
        "theme_dark": "Dark",
        "theme_system": "System",
        "language": "Language",
        "lang_en": "English",
        "lang_uk": "Ukrainian",
        "about_title": "About",
        "version": "Version",
        "author": "Author",
        "website": "Website",
        "copied": "Copied",
        "copied_msg": "Commands copied to clipboard.",
        "stop_copied": "Stop-debug block copied.",
        "saved_title": "Saved",
        "empty": "Nothing to save.",
    },
    "uk": {
        "app_title": "FortiDebug Builder",
        "fortios": "FortiOS",
        "recipes": "Рецепти",
        "sessions": "Сесії",
        "ping": "Ping",
        "traceroute": "Traceroute",
        "sniffer": "Sniffer",
        "flows": "Flows",
        "vpn": "VPN",
        "app_debug": "App Debug",
        "system_top": "System Top",
        "ha": "HA",
        "routing": "Маршрутизація",
        "tac": "TAC / Support",
        "ssh_logger": "SSH Logger",
        "saved": "Збережені",
        "settings": "Налаштування",
        "about": "Про програму",
        "copy": "Копіювати",
        "copy_stop": "Стоп-debug",
        "save_txt": "Зберегти .txt",
        "save_later": "Зберегти пізніше",
        "settings_title": "Налаштування",
        "theme": "Тема",
        "theme_light": "Світла",
        "theme_dark": "Темна",
        "theme_system": "Системна",
        "language": "Мова",
        "lang_en": "English",
        "lang_uk": "Українська",
        "about_title": "Про програму",
        "version": "Версія",
        "author": "Автор",
        "website": "Сайт",
        "copied": "Скопійовано",
        "copied_msg": "Команди скопійовано в буфер.",
        "stop_copied": "Блок stop-debug скопійовано.",
        "saved_title": "Збережено",
        "empty": "Нічого зберігати.",
    },
}

_current = "uk"


def set_lang(lang: str) -> None:
    global _current
    if lang in STRINGS:
        _current = lang


def get_lang() -> str:
    return _current


def t(key: str) -> str:
    return STRINGS.get(_current, STRINGS["en"]).get(key, STRINGS["en"].get(key, key))
