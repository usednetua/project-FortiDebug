#!/usr/bin/env python3
"""Generate multi-size app.ico (no external deps). Run from repo root:

    python scripts/generate_icon.py
"""

from __future__ import annotations

import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "src" / "resources" / "icons" / "app.ico"


def _png_rgba(size: int) -> bytes:
    def pixel(x: int, y: int) -> tuple[int, int, int, int]:
        cx = cy = size / 2
        d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
        if d < size * 0.38:
            return (40, 120, 220, 255)
        if d < size * 0.48:
            return (20, 60, 140, 255)
        return (15, 20, 35, 0 if d > size * 0.5 else 255)

    raw = b""
    for y in range(size):
        raw += b"\x00"
        for x in range(size):
            raw += bytes(pixel(x, y))

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    ihdr = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def build_ico(sizes: list[int] | None = None) -> bytes:
    sizes = sizes or [16, 32, 48, 256]
    pngs = [_png_rgba(s) for s in sizes]
    num = len(sizes)
    header = struct.pack("<HHH", 0, 1, num)
    offset = 6 + 16 * num
    entries = b""
    body = b""
    for s, png in zip(sizes, pngs):
        w = 0 if s >= 256 else s
        h = 0 if s >= 256 else s
        entries += struct.pack("<BBBBHHII", w, h, 0, 0, 1, 32, len(png), offset)
        body += png
        offset += len(png)
    return header + entries + body


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    data = build_ico()
    OUT.write_bytes(data)
    print(f"Wrote {OUT} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
