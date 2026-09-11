#!/usr/bin/env python3
"""Refresh live GitHub data used by Axira-A's profile.

The workflow fetches public repository metadata and public activity, renders
self-hosted SVG cards, and rewrites one marker-delimited repository table in the
README. If GitHub API calls fail, existing generated files are preserved.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
CONFIG_FILE = ROOT / "profile-config.json"
STATUS_FILE = ROOT / "profile-status.json"
CACHE_FILE = ROOT / "data" / "live-cache.json"
README_FILE = ROOT / "README.md"
DASHBOARD = ASSETS / "dashboard.svg"
FOCUS = ASSETS / "focus.svg"
TIMELINE = ASSETS / "timeline.svg"

BG0 = "#070b10"
BG1 = "#0d141c"
PANEL = "#0b1118"
BORDER = "#2f3943"
GOLD = "#c9a467"
GOLD2 = "#806742"
CREAM = "#efe6d4"
MUTED = "#a69d8f"
DIM = "#6d7881"
GREEN = "#79a384"
BLUE = "#7197b4"
PURPLE = "#907bc0"
ORANGE = "#d78a48"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SERIF = "Georgia, 'Times New Roman', serif"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def request_json(url: str):
    token = os.getenv("GITHUB_TOKEN", "")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Axira-A-profile-refresh",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)


def maybe_json(url: str, default=None):
    try:
        return request_json(url)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return default
        raise


def trunc(text: str, length: int) -> str:
    value = " ".join(str(text or "").split())
    return value if len(value) <= length else value[: max(0, length - 1)].rstrip() + "…"


def iso_date(value: str | None) -> str:
    return (value or "")[:10] or "—"


def days_since(value: str | None) -> int | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - dt).days
    except ValueError:
        return None


def base_svg(title: str, kicker: str, height: int, content: str, right: str = "", accent: str = GOLD) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-label="{escape(title)}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/></linearGradient>
  <linearGradient id="scan" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GOLD}" stop-opacity="0"/><stop offset=".5" stop-color="{GOLD}" stop-opacity=".65"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient>
</defs>
<rect width="1200" height="{height}" rx="16" fill="url(#bg)"/>
<rect x="1" y="1" width="1198" height="{height-2}" rx="15" fill="none" stroke="#39342d"/>
<text x="38" y="40" fill="{CREAM}" font-family="{SERIF}" font-size="24" letter-spacing="2.8">{escape(title)}</text>
<text x="38" y="62" fill="#82796d" font-family="{MONO}" font-size="9.2" letter-spacing="1.4">{escape(kicker)}</text>
<text x="1162" y="43" text-anchor="end" fill="#776e62" font-family="{MONO}" font-size="9">{escape(right)}</text>
<path d="M38 79 H1162" stroke="#27313a"/><path d="M38 79 H206" stroke="{accent}" opacity=".72"/>
<rect x="38" y="78" width="92" height="2" fill="url(#scan)" opacity="0"><animate attributeName="x" values="38;1070" dur="6.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;.8;0" dur="6.5s" repeatCount="indefinite"/></rect>
{content}
</svg>'''


def card(x: int, y: int, width: int, height: int, title: str, top_right: str, line1: str, line2: str = "", accent: str = GOLD, pulse: bool = False) -> str:
    pulse_markup = ""
    if pulse:
        pulse_markup = f'<animate attributeName="opacity" values=".35;1;.35" dur="2.7s" repeatCount="indefinite"/>'
    return f'''<g>
<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="11" fill="{PANEL}" stroke="{BORDER}"/>
<rect x="{x}" y="{y}" width="4" height="{height}" rx="2" fill="{accent}" opacity=".86"/>
<circle cx="{x+22}" cy="{y+22}" r="3.8" fill="{accent}">{pulse_markup}</circle>
<text x="{x+35}" y="{y+27}" fill="{CREAM}" font-family="{MONO}" font-size="12.4" font-weight="700">{escape(title)}</text>
<text x="{x+width-18}" y="{y+26}" text-anchor="end" fill="{accent}" font-family="{MONO}" font-size="8.8" letter-spacing=".7">{escape(top_right)}</text>
<text x="{x+22}" y="{y+54}" fill="{MUTED}" font-family="{MONO}" font-size="9.6">{escape(line1)}</text>
<text x="{x+22}" y="{y+74}" fill="{DIM}" font-family="{MONO}" font-size="8.8">{escape(line2)}</text>
</g>'''


def generate_focus(status: dict) -> None:
    focus = list(status.get("focus") or [])[:4]
    positions = [(38,98),(612,98),(38,192),(612,192)]
    accents = [ORANGE, PURPLE, GREEN, BLUE]
    chunks: list[str] = []
    for i, item in enumerate(focus):
        chunks.append(card(
            *positions[i], 550, 78,
            trunc(item.get("project", "Unnamed"), 31),
            trunc(item.get("status", "ACTIVE"), 20),
            trunc(item.get("detail", ""), 77),
            "manual status · source: profile-status.json",
            accents[i], True,
        ))
    while len(chunks) < 4:
        i = len(chunks)
        chunks.append(card(*positions[i], 550, 78, "Open slot", "AVAILABLE", "Add another focus item in profile-status.json", "", DIM, False))
    updated = str(status.get("updated") or "—")
    FOCUS.write_text(base_svg(
        "CURRENTLY FORGING",
        "MANUAL ROADMAP SIGNAL · NO FAKE PERCENTAGES · EDIT ONE JSON FILE TO UPDATE",
        290,
        ''.join(chunks),
        f"STATUS UPDATED  {updated}",
        ORANGE,
    ), encoding="utf-8")


def code_repos(all_repos: list[dict], username: str) -> list[dict]:
    result = []
    for repo in all_repos:
        if repo.get("private") or repo.get("fork") or repo.get("archived"):
            continue
        if repo.get("name") == username or int(repo.get("size") or 0) <= 0:
            continue
        result.append(repo)
    result.sort(key=lambda r: r.get("pushed_at") or "", reverse=True)
    return result


def generate_dashboard(all_repos: list[dict], username: str) -> None:
    repos = code_repos(all_repos, username)
    stars = sum(int(r.get("stargazers_count") or 0) for r in repos)
    active_90 = sum(1 for r in repos if (days_since(r.get("pushed_at")) or 99999) <= 90)
    langs = Counter(str(r.get("language")) for r in repos if r.get("language"))
    lang_text = " · ".join(name for name, _ in langs.most_common(2)) or "—"
    last_push = iso_date(repos[0].get("pushed_at")) if repos else "—"
    metrics = [
        ("PUBLIC CODE REPOS", str(len(repos)), GREEN),
        ("ACTIVE · 90D", str(active_90), ORANGE),
        ("TOTAL STARS", str(stars), GOLD),
        ("TOP LANGUAGES", lang_text, BLUE),
    ]
    chunks: list[str] = []
    xs = [38, 320, 602, 884]
    for (label, value, accent), x in zip(metrics, xs):
        chunks.append(f'''<g><rect x="{x}" y="99" width="260" height="70" rx="11" fill="{PANEL}" stroke="{BORDER}"/><text x="{x+18}" y="122" fill="{DIM}" font-family="{MONO}" font-size="8.5" letter-spacing="1">{escape(label)}</text><text x="{x+18}" y="152" fill="{CREAM}" font-family="{MONO}" font-size="19" font-weight="700">{escape(value)}</text><rect x="{x+18}" y="160" width="60" height="2" fill="{accent}" opacity=".75"/></g>''')
    recent = repos[:4]
    positions = [(38,188),(612,188),(38,274),(612,274)]
    accents = [GREEN, PURPLE, ORANGE, BLUE]
    for i, repo in enumerate(recent):
        chunks.append(card(
            *positions[i], 550, 70,
            trunc(repo.get("name") or "Unnamed", 28),
            f"{repo.get('language') or '—'} · ★ {int(repo.get('stargazers_count') or 0)}",
            trunc(repo.get("description") or "Public repository", 73),
            f"pushed {iso_date(repo.get('pushed_at'))} · branch {repo.get('default_branch') or '—'}",
            accents[i], False,
        ))
    DASHBOARD.write_text(base_svg(
        "LIVE DEVELOPMENT DASHBOARD",
        "PUBLIC GITHUB DATA · SELF-HOSTED SVG · REFRESHED BY GITHUB ACTIONS",
        360,
        ''.join(chunks),
        f"LAST PUBLIC PUSH  {last_push}",
        GREEN,
    ), encoding="utf-8")


def event_rows(events: list[dict], repos: list[dict]) -> list[tuple[str,str,str,str]]:
    rows: list[tuple[str,str,str,str]] = []
    seen: set[tuple[str,str]] = set()
    for event in events:
        typ = event.get("type") or ""
        repo_name = (event.get("repo") or {}).get("name", "").split("/")[-1]
        payload = event.get("payload") or {}
        created = iso_date(event.get("created_at"))
        title = ""
        detail = ""
        if typ == "PushEvent":
            commits = payload.get("commits") or []
            title = f"PUSH · {repo_name}"
            detail = trunc((commits[-1].get("message") if commits else "Pushed commits") or "Pushed commits", 82)
        elif typ == "CreateEvent":
            ref_type = payload.get("ref_type") or "ref"
            ref = payload.get("ref") or repo_name
            title = f"CREATE · {repo_name}"
            detail = trunc(f"Created {ref_type} {ref}", 82)
        elif typ == "ReleaseEvent":
            release = payload.get("release") or {}
            title = f"RELEASE · {repo_name}"
            detail = trunc(f"Published {release.get('tag_name') or 'a release'}", 82)
        elif typ == "PullRequestEvent":
            pr = payload.get("pull_request") or {}
            title = f"PR · {repo_name}"
            detail = trunc(pr.get("title") or f"Pull request {payload.get('action') or 'updated'}", 82)
        elif typ == "IssuesEvent":
            issue = payload.get("issue") or {}
            title = f"ISSUE · {repo_name}"
            detail = trunc(issue.get("title") or "Issue updated", 82)
        if not title:
            continue
        key = (title, detail)
        if key in seen:
            continue
        seen.add(key)
        rows.append((title, detail, created, typ))
        if len(rows) >= 5:
            break
    if not rows:
        for repo in repos[:5]:
            rows.append((
                f"REPOSITORY · {repo.get('name') or 'Unnamed'}",
                trunc(repo.get("description") or "Public repository activity", 82),
                iso_date(repo.get("pushed_at")),
                "Repository",
            ))
    return rows


def generate_timeline(events: list[dict], all_repos: list[dict], username: str) -> None:
    repos = code_repos(all_repos, username)
    rows = event_rows(events, repos)
    y = 106
    chunks: list[str] = ['<path d="M64 108 V286" stroke="#313b45" stroke-width="2"/>']
    accents = [ORANGE, GREEN, PURPLE, BLUE, GOLD]
    for i, (title, detail, date, _kind) in enumerate(rows[:5]):
        yy = y + i * 38
        accent = accents[i % len(accents)]
        chunks.append(f'''<g><circle cx="64" cy="{yy}" r="5" fill="{accent}"/><circle cx="64" cy="{yy}" r="10" fill="none" stroke="{accent}" opacity=".18"/><text x="88" y="{yy+4}" fill="{CREAM}" font-family="{MONO}" font-size="11.2" font-weight="700">{escape(title)}</text><text x="370" y="{yy+4}" fill="{MUTED}" font-family="{MONO}" font-size="9.5">{escape(detail)}</text><text x="1138" y="{yy+4}" text-anchor="end" fill="{DIM}" font-family="{MONO}" font-size="9">{escape(date)}</text></g>''')
    TIMELINE.write_text(base_svg(
        "RECENT PUBLIC SIGNAL",
        "LATEST PUBLIC EVENTS · FALLS BACK TO REPOSITORY PUSHES IF EVENT DATA IS UNAVAILABLE",
        320,
        ''.join(chunks),
        "PUBLIC ACTIVITY ONLY",
        BLUE,
    ), encoding="utf-8")


def repo_details(username: str, names: list[str], all_repos: list[dict]) -> list[dict]:
    by_name = {r.get("name"): r for r in all_repos}
    details: list[dict] = []
    for name in names:
        repo = by_name.get(name)
        if repo is None:
            repo = maybe_json(f"https://api.github.com/repos/{username}/{name}", {}) or {}
        release = maybe_json(f"https://api.github.com/repos/{username}/{name}/releases/latest", None)
        details.append({
            "name": name,
            "description": repo.get("description") or "Public repository",
            "language": repo.get("language") or "—",
            "stars": int(repo.get("stargazers_count") or 0),
            "branch": repo.get("default_branch") or "—",
            "pushed": iso_date(repo.get("pushed_at")),
            "license": ((repo.get("license") or {}).get("spdx_id") or "—"),
            "release": (release or {}).get("tag_name") or "development",
        })
    return details


def render_repo_table(username: str, repos: list[dict]) -> str:
    lines = [
        "<!-- AUTO:REPOSITORIES:START -->",
        "| Repository | Stack | Channel | Branch | Last push |",
        "|---|---|---|---|---|",
    ]
    for repo in repos:
        name = repo["name"]
        link = f"https://github.com/{username}/{name}"
        release = repo.get("release") or "development"
        channel = f"`{release}`" if release != "development" else "development"
        lines.append(
            f"| **[{name}]({link})**<br><sub>{repo.get('description') or 'Public repository'}</sub> "
            f"| `{repo.get('language') or '—'}` · ★ {repo.get('stars', 0)} "
            f"| {channel} "
            f"| `{repo.get('branch') or '—'}` "
            f"| {repo.get('pushed') or '—'} |"
        )
    lines.append("<!-- AUTO:REPOSITORIES:END -->")
    return "\n".join(lines)


def rewrite_repo_table(repos: list[dict], username: str) -> None:
    text = README_FILE.read_text(encoding="utf-8")
    replacement = render_repo_table(username, repos)
    pattern = re.compile(r"<!-- AUTO:REPOSITORIES:START -->.*?<!-- AUTO:REPOSITORIES:END -->", re.S)
    if not pattern.search(text):
        raise RuntimeError("README repository markers are missing")
    new_text = pattern.sub(replacement, text, count=1)
    if new_text != text:
        README_FILE.write_text(new_text, encoding="utf-8")


def write_cache(repos: list[dict]) -> None:
    CACHE_FILE.parent.mkdir(exist_ok=True)
    payload = {
        "generated_at": datetime.now(timezone.utc).date().isoformat(),
        "repositories": repos,
    }
    CACHE_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_cached_featured() -> list[dict]:
    try:
        return list(load_json(CACHE_FILE).get("repositories") or [])
    except Exception:
        return []


def main() -> int:
    config = load_json(CONFIG_FILE)
    status = load_json(STATUS_FILE)
    username = str(config.get("username") or "Axira-A")
    featured_names = list(config.get("featured_repositories") or [])[:6]

    generate_focus(status)

    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=pushed&type=owner"
    try:
        all_repos = request_json(repos_url)
    except Exception as exc:
        print(f"GitHub repository API unavailable; preserving live cards: {exc}", file=sys.stderr)
        cached = load_cached_featured()
        if cached:
            rewrite_repo_table(cached, username)
        return 0

    generate_dashboard(all_repos, username)

    try:
        events = request_json(f"https://api.github.com/users/{username}/events/public?per_page=50")
    except Exception as exc:
        print(f"GitHub events API unavailable; using repository pushes: {exc}", file=sys.stderr)
        events = []
    generate_timeline(events, all_repos, username)

    try:
        featured = repo_details(username, featured_names, all_repos)
    except Exception as exc:
        print(f"Featured repository detail lookup partly failed: {exc}", file=sys.stderr)
        featured = load_cached_featured()
    if featured:
        write_cache(featured)
        rewrite_repo_table(featured, username)

    print("Refreshed live profile data.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
