# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for FortiDebug Builder (Windows)
#
# Usage (from repo root, venv active):
#   python scripts/generate_icon.py
#   pyinstaller build.spec
#
# Output: dist/FortiDebugBuilder.exe

import sys
from pathlib import Path

block_cipher = None
root = Path(SPECPATH)
src = root / "src"
icon = root / "src" / "resources" / "icons" / "app.ico"

a = Analysis(
    [str(src / "main.py")],
    pathex=[str(src)],
    binaries=[],
    datas=[
        (str(src / "resources"), "resources"),
    ] if (src / "resources").exists() else [],
    hiddenimports=[
        "customtkinter",
        "pyperclip",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="FortiDebugBuilder",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(icon) if icon.exists() else None,
)
