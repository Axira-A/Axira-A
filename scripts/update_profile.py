#!/usr/bin/env python3
"""Generate self-hosted dynamic SVG cards for Axira-A's profile README.

- assets/forge.svg from profile-status.json
- assets/activity.svg from the GitHub REST API

The output intentionally uses plain SVG attributes + native SMIL only.  No CSS,
JavaScript, foreignObject, fonts, or third-party rendering service is required.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from collections import Counter
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USERNAME = "Axira-A"
ACTIVITY_OUT = ROOT / "assets" / "activity.svg"
FORGE_OUT = ROOT / "assets" / "forge.svg"
STATUS_FILE = ROOT / "profile-status.json"
API = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=pushed&type=owner"

BG0 = "#070b10"
BG1 = "#0d141c"
PANEL = "#0b1118"
BORDER = "#303840"
GOLD = "#c9a467"
GOLD2 = "#8f7348"
CREAM = "#eee5d3"
MUTED = "#9a9389"
DIM = "#6f7880"
SERIF = "Georgia, 'Times New Roman', serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def request_json(url: str):
    token = os.getenv("GITHUB_TOKEN", "")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Axira-A-profile-action",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)


def trunc(text: str, max_len: int) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= max_len else text[: max_len - 1].rstrip() + "…"


def shell(title: str, kicker: str, content: str, right_top: str = "", accent: str = GOLD) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320" role="img">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/></linearGradient>
  <linearGradient id="line" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GOLD2}" stop-opacity="0"/><stop offset=".5" stop-color="{GOLD}"/><stop offset="1" stop-color="{GOLD2}" stop-opacity="0"/></linearGradient>
</defs>
<rect width="1200" height="320" rx="18" fill="url(#bg)"/>
<rect x="1" y="1" width="1198" height="318" rx="17" fill="none" stroke="#3a352e"/>
<text x="44" y="45" fill="{CREAM}" font-family="{SERIF}" font-size="25" letter-spacing="3">{escape(title)}</text>
<text x="44" y="67" fill="#847b6e" font-family="{MONO}" font-size="9.5" letter-spacing="1.6">{escape(kicker)}</text>
<text x="1156" y="48" text-anchor="end" fill="#746b60" font-family="{MONO}" font-size="9.5">{escape(right_top)}</text>
<path d="M44 84 H1156" stroke="#273039"/><path d="M44 84 H220" stroke="{accent}" opacity=".65"/>
<path d="M44 84 H130" stroke="{GOLD}" stroke-width="2" opacity="0"><animate attributeName="opacity" values="0;.65;0" dur="6s" repeatCount="indefinite"/><animateTransform attributeName="transform" type="translate" values="0 0;1010 0" dur="6s" repeatCount="indefinite"/></path>
{content}
</svg>'''


def focus_panel(x: int, y: int, project: str, status: str, detail: str, accent: str) -> str:
    return f'''<g>
<rect x="{x}" y="{y}" width="544" height="82" rx="12" fill="{PANEL}" stroke="{BORDER}"/>
<rect x="{x}" y="{y}" width="4" height="82" rx="2" fill="{accent}" opacity=".85"/>
<circle cx="{x+24}" cy="{y+24}" r="4" fill="{accent}"><animate attributeName="opacity" values=".35;1;.35" dur="2.8s" repeatCount="indefinite"/></circle>
<text x="{x+38}" y="{y+28}" fill="{CREAM}" font-family="{MONO}" font-size="13" font-weight="700">{escape(project)}</text>
<text x="{x+520}" y="{y+27}" text-anchor="end" fill="{accent}" font-family="{MONO}" font-size="9.5" letter-spacing="1">{escape(status)}</text>
<text x="{x+24}" y="{y+57}" fill="{MUTED}" font-family="{MONO}" font-size="10.5">{escape(detail)}</text>
</g>'''


def generate_forge() -> None:
    try:
        data = json.loads(STATUS_FILE.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"Could not read {STATUS_FILE}: {exc}", file=sys.stderr)
        return

    focus = list(data.get("focus") or [])[:4]
    updated = str(data.get("updated") or "—")
    positions = [(44,106),(612,106),(44,204),(612,204)]
    accents = ["#d18d47", "#8d77c7", "#b9874f", "#6f9a86"]
    cards = []
    for i, item in enumerate(focus):
        cards.append(focus_panel(
            *positions[i],
            trunc(str(item.get("project") or "Unnamed"), 30),
            trunc(str(item.get("status") or "ACTIVE"), 22),
            trunc(str(item.get("detail") or ""), 72),
            accents[i],
        ))
    FORGE_OUT.write_text(shell(
        "CURRENTLY FORGING",
        "ACTIVE DEVELOPMENT FOCUS · EDIT profile-status.json TO UPDATE",
        ''.join(cards),
        f"STATUS UPDATED  {updated}",
        "#d18d47",
    ), encoding="utf-8")
    print(f"Updated {FORGE_OUT}")


def repo_panel(x: int, y: int, repo: dict, accent: str) -> str:
    name = trunc(repo.get("name") or "Unnamed", 29)
    desc = trunc(repo.get("description") or "Active public repository", 60)
    lang = repo.get("language") or "—"
    stars = int(repo.get("stargazers_count") or 0)
    pushed = (repo.get("pushed_at") or "")[:10]
    return f'''<g>
<rect x="{x}" y="{y}" width="544" height="82" rx="12" fill="{PANEL}" stroke="{BORDER}"/>
<circle cx="{x+24}" cy="{y+24}" r="4" fill="{accent}"/>
<text x="{x+38}" y="{y+29}" fill="{CREAM}" font-family="{MONO}" font-size="13" font-weight="700">{escape(name)}</text>
<text x="{x+520}" y="{y+28}" text-anchor="end" fill="{DIM}" font-family="{MONO}" font-size="9.5">★ {stars}  ·  {escape(lang)}</text>
<text x="{x+24}" y="{y+55}" fill="{MUTED}" font-family="{MONO}" font-size="10.2">{escape(desc)}</text>
<text x="{x+520}" y="{y+69}" text-anchor="end" fill="#5e6871" font-family="{MONO}" font-size="8.5">PUSHED {escape(pushed)}</text>
</g>'''


def generate_activity() -> None:
    try:
        all_repos = request_json(API)
    except Exception as exc:
        print(f"GitHub API unavailable; preserving previous activity card: {exc}", file=sys.stderr)
        return

    public = [
        r for r in all_repos
        if not r.get("private") and not r.get("fork") and r.get("name") != USERNAME
        and int(r.get("size") or 0) > 0 and not r.get("archived")
    ]
    public.sort(key=lambda r: r.get("pushed_at") or "", reverse=True)
    repos = public[:4]
    total_stars = sum(int(r.get("stargazers_count") or 0) for r in public)
    languages = Counter(r.get("language") for r in public if r.get("language"))
    primary_language = languages.most_common(1)[0][0] if languages else "—"
    last_push = (repos[0].get("pushed_at") or "")[:10] if repos else "—"
    positions = [(44,106),(612,106),(44,204),(612,204)]
    accents = ["#6f9a86", "#8d77c7", "#b9874f", "#6e8fa9"]
    if repos:
        content = ''.join(repo_panel(*positions[i], repo, accents[i]) for i, repo in enumerate(repos))
    else:
        content = f'<text x="44" y="150" fill="{MUTED}" font-family="{MONO}" font-size="13">No public repository activity yet.</text>'
    right = f"{len(public)} REPOS  ·  {total_stars} STARS  ·  {primary_language}  ·  LAST PUSH {last_push}"
    ACTIVITY_OUT.write_text(shell(
        "LATEST PUBLIC WORK",
        "SELF-HOSTED · GENERATED BY THIS PROFILE REPOSITORY'S GITHUB ACTIONS",
        content,
        right,
        "#6f9a86",
    ), encoding="utf-8")
    print(f"Updated {ACTIVITY_OUT}")


def main() -> int:
    generate_forge()
    generate_activity()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
