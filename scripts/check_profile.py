#!/usr/bin/env python3
"""Cheap sanity checks for the profile repository."""
from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
CORE_SVGS = {
    "hero.svg", "footer.svg", "tools.svg", "forge.svg", "activity.svg",
    "project-maplesadventure.svg", "project-maplesworld.svg",
    "project-rpg-menu.svg", "project-maplescore.svg", "divider.svg",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    text = README.read_text(encoding="utf-8")

    refs = set(re.findall(r'(?:src|href)=["\'](\./[^"\'#?]+)', text))
    missing = [ref for ref in sorted(refs) if not (ROOT / ref[2:]).exists()]
    if missing:
        fail("Missing local README resources: " + ", ".join(missing))

    status = json.loads((ROOT / "profile-status.json").read_text(encoding="utf-8"))
    focus = status.get("focus")
    if not isinstance(focus, list) or not 1 <= len(focus) <= 4:
        fail("profile-status.json must contain 1–4 focus items")
    for index, item in enumerate(focus, start=1):
        for key in ("project", "status", "detail"):
            if not str(item.get(key, "")).strip():
                fail(f"focus item {index} is missing {key!r}")

    assets = ROOT / "assets"
    missing_core = sorted(name for name in CORE_SVGS if not (assets / name).exists())
    if missing_core:
        fail("Missing core SVG assets: " + ", ".join(missing_core))

    for svg in assets.glob("*.svg"):
        try:
            root = ET.parse(svg).getroot()
        except ET.ParseError as exc:
            fail(f"Invalid SVG {svg.name}: {exc}")
        viewbox = root.attrib.get("viewBox")
        if not viewbox:
            fail(f"SVG {svg.name} is missing viewBox")
        if svg.stat().st_size > 250_000:
            fail(f"SVG {svg.name} is unexpectedly large ({svg.stat().st_size} bytes)")

    # Core README visuals should remain vector so GitHub can scale them sharply.
    active_rasters = re.findall(r'src=["\']\.\/assets\/[^"\']+\.(?:png|jpe?g|gif|webp)', text, re.I)
    if active_rasters:
        fail("Core README references raster assets again; keep primary UI vector-based")

    print(f"Profile checks passed: {len(refs)} local resources, {len(focus)} focus items, vector UI active.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
