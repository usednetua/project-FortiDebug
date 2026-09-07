#!/usr/bin/env python3
"""Generate RELEASE_NOTES.md from CHANGELOG.md for a given version.

Usage (from repo root):
  python scripts/generate_release_notes.py              # latest versioned section
  python scripts/generate_release_notes.py 0.18.2
  python scripts/generate_release_notes.py v0.18.2
  python scripts/generate_release_notes.py --tag v0.18.2
  python scripts/generate_release_notes.py 0.18.2 --check   # exit 1 if missing section

Writes: RELEASE_NOTES.md (repo root)
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHANGELOG = ROOT / "CHANGELOG.md"
OUT = ROOT / "RELEASE_NOTES.md"

SECTION_RE = re.compile(
    r"^## \[([^\]]+)\](?:\s+[—–-]\s+(\d{4}-\d{2}-\d{2}))?(?:\s+[—–-]\s+(.+))?\s*$"
)
H3_RE = re.compile(r"^###\s+(.+)\s*$")


def normalize_version(raw: str | None) -> str | None:
    if not raw:
        return None
    s = raw.strip()
    if s.lower().startswith("v") and s[1:2].isdigit():
        s = s[1:]
    return s


def parse_sections(text: str) -> list[dict]:
    lines = text.splitlines()
    sections: list[dict] = []
    i = 0
    while i < len(lines):
        m = SECTION_RE.match(lines[i])
        if not m:
            i += 1
            continue
        ver, sec_date, extra = m.group(1), m.group(2), m.group(3)
        body: list[str] = []
        i += 1
        while i < len(lines) and not SECTION_RE.match(lines[i]):
            body.append(lines[i])
            i += 1
        while body and not body[-1].strip():
            body.pop()
        while body and not body[0].strip():
            body.pop(0)
        body = [ln for ln in body if ln.strip() not in ("---", "***", "___")]
        sections.append(
            {
                "version": ver,
                "date": sec_date,
                "extra": (extra or "").strip(),
                "body_lines": body,
            }
        )
    return sections


def split_categories(body_lines: list[str]) -> dict[str, list[str]]:
    cats: dict[str, list[str]] = {}
    current: str | None = None
    for line in body_lines:
        h = H3_RE.match(line)
        if h:
            current = h.group(1).strip()
            cats.setdefault(current, [])
            continue
        if current is None:
            continue
        cats[current].append(line)
    out: dict[str, list[str]] = {}
    for k, v in cats.items():
        if "\n".join(v).strip():
            out[k] = v
    return out


def bullets_preview(cats: dict[str, list[str]], limit: int = 8) -> list[str]:
    """Top-level changelog bullets for Highlights (skip nested '  - ')."""
    found: list[str] = []
    for _name, lines in cats.items():
        for line in lines:
            if line.startswith("- "):
                found.append(line.strip())
                if len(found) >= limit:
                    return found
    return found


def render(
    version: str,
    sec_date: str | None,
    extra: str,
    cats: dict[str, list[str]],
    tag: str | None = None,
) -> str:
    tag = tag or f"v{version}"
    day = sec_date or date.today().isoformat()
    title_extra = f" — {extra}" if extra else ""

    parts: list[str] = [
        f"# FortiDebug Builder {version}{title_extra}",
        "",
        f"**Дата:** {day}  ",
        f"**Tag:** {tag}",
        "",
        "## Highlights",
        "",
    ]
    preview = bullets_preview(cats)
    if preview:
        for b in preview[:6]:
            parts.append(b)
    else:
        parts.append("- Див. секції нижче.")
    parts.append("")

    order = ["Added", "Changed", "Fixed", "Removed", "Deprecated", "Security"]
    seen = set()
    for name in order:
        if name in cats:
            seen.add(name)
            parts.append(f"## {name}")
            parts.append("")
            parts.extend(cats[name])
            if parts[-1].strip():
                parts.append("")
    for name, lines in cats.items():
        if name in seen:
            continue
        parts.append(f"## {name}")
        parts.append("")
        parts.extend(lines)
        if parts[-1].strip():
            parts.append("")

    parts.extend(
        [
            "## Install",
            "",
            "- **Windows EXE:** вкладення `FortiDebugBuilder.exe` у цьому GitHub Release",
            "- **З вихідників:**",
            "",
            "```bash",
            "pip install -r requirements.txt",
            "python src/main.py",
            "```",
            "",
            "## Full changelog",
            "",
            f"Див. [CHANGELOG.md](CHANGELOG.md) — секція `[{version}]`.",
            "",
        ]
    )
    return "\n".join(parts).rstrip() + "\n"


def pick_section(sections: list[dict], version: str | None) -> dict:
    versioned = [s for s in sections if s["version"].lower() != "unreleased"]
    if not versioned and not version:
        raise SystemExit("No versioned sections in CHANGELOG.md")
    if version is None:
        return versioned[0]
    target = version.lower()
    for s in sections:
        if s["version"].lower() == target:
            return s
    known = ", ".join(s["version"] for s in sections[:12])
    raise SystemExit(f"Section [{version}] not found in CHANGELOG.md. Known: {known}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Generate RELEASE_NOTES.md from CHANGELOG.md")
    p.add_argument(
        "version",
        nargs="?",
        help="Version (0.18.2 or v0.18.2). Default: latest versioned section",
    )
    p.add_argument("--tag", help="Override tag label (default v<version>)")
    p.add_argument(
        "--check",
        action="store_true",
        help="Only verify section exists; do not write file",
    )
    p.add_argument(
        "-o",
        "--output",
        type=Path,
        default=OUT,
        help="Output path (default: RELEASE_NOTES.md)",
    )
    args = p.parse_args(argv)

    if not CHANGELOG.is_file():
        print(f"ERROR: {CHANGELOG} not found", file=sys.stderr)
        return 2

    text = CHANGELOG.read_text(encoding="utf-8")
    sections = parse_sections(text)
    if not sections:
        print("ERROR: no ## [version] sections parsed", file=sys.stderr)
        return 2

    ver = normalize_version(args.version)
    if args.tag and not ver:
        ver = normalize_version(args.tag)

    try:
        sec = pick_section(sections, ver)
    except SystemExit as e:
        print(str(e), file=sys.stderr)
        return 1

    if sec["version"].lower() == "unreleased":
        print(
            "ERROR: refusing to publish [Unreleased] as release notes; "
            "move entries to ## [X.Y.Z] first",
            file=sys.stderr,
        )
        return 1

    if args.check:
        print(f"OK: section [{sec['version']}] found")
        return 0

    cats = split_categories(sec["body_lines"])
    tag = args.tag or f"v{sec['version']}"
    if tag and not tag.startswith("v"):
        tag = f"v{tag}" if tag[0].isdigit() else tag

    content = render(
        version=sec["version"],
        sec_date=sec["date"],
        extra=sec["extra"],
        cats=cats,
        tag=tag,
    )
    out_path = args.output if args.output.is_absolute() else ROOT / args.output
    out_path.write_text(content, encoding="utf-8")
    print(f"Wrote {out_path} for [{sec['version']}] ({len(content)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
