#!/usr/bin/env python3
"""Sanity checks for the profile repository."""
from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
CONFIG = ROOT / "profile-config.json"
STATUS = ROOT / "profile-status.json"
ASSETS = ROOT / "assets"
CORE = {"hero.svg", "footer.svg", "divider.svg", "dashboard.svg", "focus.svg", "timeline.svg"}
MARKERS = ["AUTO:REPOSITORIES:START", "AUTO:REPOSITORIES:END"]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    text = README.read_text(encoding="utf-8")
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    status = json.loads(STATUS.read_text(encoding="utf-8"))

    if config.get("username") != "Axira-A":
        fail("profile-config.json username must remain Axira-A")
    projects = config.get("projects")
    if not isinstance(projects, list) or len(projects) != 4:
        fail("profile-config.json must contain exactly four portfolio projects")
    tools = config.get("tools")
    if not isinstance(tools, list) or len(tools) < 8:
        fail("profile-config.json should contain at least eight tools")

    focus = status.get("focus")
    if not isinstance(focus, list) or not 1 <= len(focus) <= 4:
        fail("profile-status.json must contain 1–4 focus items")
    for i, item in enumerate(focus, start=1):
        for key in ("project", "status", "detail"):
            if not str(item.get(key, "")).strip():
                fail(f"focus item {i} is missing {key!r}")

    for marker in MARKERS:
        if text.count(f"<!-- {marker} -->") != 1:
            fail(f"README must contain marker {marker!r} exactly once")

    refs = set(re.findall(r'(?:src|href)=["\'](\./[^"\'#?]+)', text))
    refs.update("./" + path for path in re.findall(r'\]\((?:\./)?((?:assets|data)/[^)#?]+)', text))
    missing = [ref for ref in sorted(refs) if not (ROOT / ref[2:]).exists()]
    if missing:
        fail("Missing local README resources: " + ", ".join(missing))

    missing_core = sorted(name for name in CORE if not (ASSETS / name).exists())
    if missing_core:
        fail("Missing core SVGs: " + ", ".join(missing_core))

    for svg in ASSETS.rglob("*.svg"):
        try:
            root = ET.parse(svg).getroot()
        except ET.ParseError as exc:
            fail(f"Invalid SVG {svg.relative_to(ROOT)}: {exc}")
        if not root.attrib.get("viewBox"):
            fail(f"SVG {svg.relative_to(ROOT)} has no viewBox")
        if svg.stat().st_size > 300_000:
            fail(f"SVG {svg.relative_to(ROOT)} is unexpectedly large")
        raw = svg.read_text(encoding="utf-8")
        if "<script" in raw.lower() or "foreignObject" in raw:
            fail(f"Unsafe/unsupported SVG construct in {svg.relative_to(ROOT)}")

    # Core visuals remain vector; remote badges/icons are allowed only as enhancement.
    local_rasters = re.findall(r'src=["\']\./assets/[^"\']+\.(?:png|jpe?g|gif|webp)', text, re.I)
    if local_rasters:
        fail("Primary README visuals must remain SVG/vector")

    # Prevent accidental personal contact leakage in the public README.
    if re.search(r'[\w.+-]+@[\w.-]+\.\w+', text):
        fail("README contains an email address; keep contact links intentional")

    print(
        f"Profile checks passed: {len(projects)} projects, {len(focus)} focus items, "
        f"{len(tools)} tools, {len(list(ASSETS.rglob('*.svg')))} SVG assets."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
