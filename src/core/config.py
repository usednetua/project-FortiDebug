"""Persist app settings in %APPDATA%/FortiDebugBuilder/config.json."""

import json
import os
from pathlib import Path
from typing import Any, Dict


def _config_dir() -> Path:
    appdata = os.environ.get("APPDATA") or str(Path.home())
    d = Path(appdata) / "FortiDebugBuilder"
    d.mkdir(parents=True, exist_ok=True)
    return d


def config_path() -> Path:
    return _config_dir() / "config.json"


def bpf_presets_path() -> Path:
    return _config_dir() / "bpf_presets.json"


def _defaults() -> Dict[str, Any]:
    return {
        "theme": "Dark",
        "language": "uk",
        "fortios": "7.4.x",
        "vdom_enabled": False,
        "vdom_name": "root",
    }


def load_config() -> Dict[str, Any]:
    path = config_path()
    base = _defaults()
    if not path.exists():
        return base
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            base.update(data)
        return base
    except (json.JSONDecodeError, OSError):
        return base


def save_config(data: Dict[str, Any]) -> None:
    path = config_path()
    existing = load_config()
    existing.update(data)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)


def load_bpf_presets() -> Dict[str, str]:
    path = bpf_presets_path()
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def save_bpf_preset(name: str, expression: str) -> None:
    presets = load_bpf_presets()
    presets[name] = expression
    with open(bpf_presets_path(), "w", encoding="utf-8") as f:
        json.dump(presets, f, indent=2, ensure_ascii=False)


def delete_bpf_preset(name: str) -> None:
    presets = load_bpf_presets()
    if name in presets:
        del presets[name]
        with open(bpf_presets_path(), "w", encoding="utf-8") as f:
            json.dump(presets, f, indent=2, ensure_ascii=False)
