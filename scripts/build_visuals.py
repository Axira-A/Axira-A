#!/usr/bin/env python3
"""Build the static vector visual system for the Axira-A GitHub profile.

The profile intentionally keeps its core visuals self-hosted. SVG text/lines stay
sharp at GitHub's responsive widths, while tiny SMIL animations provide motion
without JavaScript, canvas, or a third-party renderer.
"""
from __future__ import annotations

import json
import random
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ICONS = ASSETS / "icons"
CONFIG = ROOT / "profile-config.json"
STATUS = ROOT / "profile-status.json"
ASSETS.mkdir(exist_ok=True)
ICONS.mkdir(exist_ok=True)

BG0 = "#070b10"
BG1 = "#0b1118"
BG2 = "#111a24"
PANEL = "#0b1118"
BORDER = "#2b3540"
GOLD = "#c9a467"
GOLD2 = "#806742"
CREAM = "#efe6d4"
MUTED = "#a89f91"
DIM = "#69747e"
BLUE = "#7197b4"
GREEN = "#7da184"
ORANGE = "#f47b28"
ORANGE2 = "#ffc05d"
SERIF = "Georgia, 'Times New Roman', serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def svg_open(w: int, h: int, label: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">'
    )


def common_defs(prefix: str) -> str:
    return f'''<defs>
  <linearGradient id="{prefix}-bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{BG0}"/><stop offset=".56" stop-color="{BG1}"/><stop offset="1" stop-color="#080c11"/>
  </linearGradient>
  <linearGradient id="{prefix}-gold" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{GOLD2}" stop-opacity="0"/><stop offset=".5" stop-color="{GOLD}"/><stop offset="1" stop-color="{GOLD2}" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="{prefix}-glow" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="{ORANGE2}" stop-opacity=".42"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/>
  </radialGradient>
  <filter id="{prefix}-blur"><feGaussianBlur stdDeviation="12"/></filter>
  <filter id="{prefix}-soft"><feGaussianBlur stdDeviation="3"/></filter>
</defs>'''


def stars(w: int, h: int, seed: int = 37, count: int = 74) -> str:
    rnd = random.Random(seed)
    out: list[str] = []
    for i in range(count):
        x = rnd.randint(18, w - 18)
        y = rnd.randint(12, int(h * .56))
        r = rnd.choice([.55, .7, .85, 1.05])
        op = rnd.uniform(.18, .62)
        if i < 12:
            out.append(
                f'<circle cx="{x}" cy="{y}" r="{r}" fill="#c8d5df" opacity="{op:.2f}">'
                f'<animate attributeName="opacity" values="{op:.2f};{min(op+.28,.9):.2f};{op:.2f}" dur="{3.2+(i%5)*.7:.1f}s" begin="-{i*.31:.2f}s" repeatCount="indefinite"/>'
                '</circle>'
            )
        else:
            out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#c8d5df" opacity="{op:.2f}"/>')
    return ''.join(out)


def bonfire(cx: int, cy: int, prefix: str, scale: float = 1.0) -> str:
    s = scale
    return f'''
<g transform="translate({cx} {cy}) scale({s})">
  <ellipse cx="0" cy="8" rx="96" ry="30" fill="url(#{prefix}-glow)" filter="url(#{prefix}-blur)" opacity=".55">
    <animate attributeName="opacity" values=".42;.66;.48;.58" dur="4.5s" repeatCount="indefinite"/>
  </ellipse>
  <path d="M-34 24 L28 0" stroke="#583b23" stroke-width="8" stroke-linecap="round"/>
  <path d="M34 24 L-27 1" stroke="#46301f" stroke-width="8" stroke-linecap="round"/>
  <rect x="-42" y="25" width="84" height="7" rx="2" fill="#34271d"/>
  <path fill="#ef6d21">
    <animate attributeName="d" dur="2.1s" repeatCount="indefinite"
      values="M0 20 C-19 7 -20 -15 -7 -33 C-5 -16 2 -13 8 -38 C24 -15 20 5 0 20Z;M0 20 C-17 6 -13 -19 -3 -44 C1 -18 8 -17 13 -30 C23 -10 16 8 0 20Z;M0 20 C-19 7 -20 -15 -7 -33 C-5 -16 2 -13 8 -38 C24 -15 20 5 0 20Z"/>
  </path>
  <path d="M0 19 C-11 7 -8 -10 1 -23 C11 -8 12 7 0 19Z" fill="#ffd472">
    <animate attributeName="opacity" values="1;.68;.94;.78;1" dur="1.5s" repeatCount="indefinite"/>
  </path>
  <g fill="#ff9b39">
    <circle cx="-18" cy="-20" r="2.3"><animate attributeName="cy" values="-17;-88" dur="3.1s" begin="-.4s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;.9;.55;0" dur="3.1s" begin="-.4s" repeatCount="indefinite"/></circle>
    <circle cx="14" cy="-27" r="1.8"><animate attributeName="cy" values="-20;-104" dur="3.7s" begin="-1.4s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;.8;.45;0" dur="3.7s" begin="-1.4s" repeatCount="indefinite"/></circle>
    <circle cx="3" cy="-32" r="1.5"><animate attributeName="cy" values="-27;-118" dur="4.2s" begin="-2.2s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;.85;.4;0" dur="4.2s" begin="-2.2s" repeatCount="indefinite"/></circle>
    <circle cx="27" cy="-14" r="1.2"><animate attributeName="cy" values="-14;-79" dur="3.4s" begin="-2.7s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;.7;.35;0" dur="3.4s" begin="-2.7s" repeatCount="indefinite"/></circle>
  </g>
</g>'''


def build_hero(config: dict, status: dict) -> str:
    w, h = 1200, 330
    prefix = "hero"
    current = status.get("focus", [{}])[0].get("project", "MaplesAdventure")
    subtitle = config.get("headline", "Minecraft systems · worlds · modding")
    out = [svg_open(w, h, "Axira profile header"), common_defs(prefix)]
    out.append(f'<rect width="{w}" height="{h}" fill="url(#{prefix}-bg)"/>')
    out.append(stars(w, h))
    out.append('<rect x="91" y="54" width="34" height="34" rx="2" fill="#d7e2eb" opacity=".78"/><rect x="97" y="61" width="9" height="8" fill="#aebbc6" opacity=".55"/><rect x="112" y="74" width="8" height="10" fill="#aebbc6" opacity=".42"/>')
    out.append('<circle cx="108" cy="71" r="42" fill="#aec4d4" opacity=".07" filter="url(#hero-blur)"><animate attributeName="opacity" values=".05;.11;.05" dur="7s" repeatCount="indefinite"/></circle>')
    out.append('<path d="M0 218 L84 174 146 205 223 158 290 207 360 173 441 211 523 176 608 215 693 171 770 208 853 163 930 211 1015 174 1102 205 1200 151 1200 330 0 330Z" fill="#0d151d"/>')
    out.append('<path d="M0 245 L112 205 195 238 283 198 365 244 458 214 552 247 640 216 744 244 830 206 938 241 1049 200 1200 236 1200 330 0 330Z" fill="#111c26" opacity=".9"/>')
    out.append('<g opacity=".17" fill="#8398a9"><ellipse cx="120" cy="231" rx="170" ry="22"/><ellipse cx="503" cy="241" rx="235" ry="25"/><ellipse cx="963" cy="229" rx="220" ry="24"/><animateTransform attributeName="transform" type="translate" values="-34 0;34 0;-34 0" dur="18s" repeatCount="indefinite"/></g>')
    out.append('<g opacity=".1" fill="#a0b3c1"><ellipse cx="313" cy="252" rx="220" ry="19"/><ellipse cx="823" cy="248" rx="270" ry="20"/><animateTransform attributeName="transform" type="translate" values="26 0;-28 0;26 0" dur="25s" repeatCount="indefinite"/></g>')
    out.append('<g fill="#090f15" stroke="#17222c" stroke-width="2"><path d="M0 248 H258 V261 H0Z"/><path d="M34 248 V218 H58 V248 M82 248 V210 H109 V248 M132 248 V222 H158 V248 M181 248 V214 H208 V248 M230 248 V225 H252 V248"/><path d="M942 248 H1200 V261 H942Z"/><path d="M958 248 V223 H982 V248 M1007 248 V211 H1035 V248 M1060 248 V221 H1085 V248 M1111 248 V209 H1138 V248 M1164 248 V219 H1188 V248"/><path d="M22 248 V170 H54 V248 M28 170 V153 H35 V170 M42 170 V149 H49 V170"/><path d="M1117 248 V157 H1158 V248 M1125 157 V139 H1134 V157 M1145 157 V144 H1153 V157"/></g>')
    out.append('<g fill="#f18b2e" opacity=".64"><rect x="33" y="184" width="4" height="11"/><rect x="44" y="201" width="4" height="10"/><rect x="1129" y="178" width="5" height="13"/><rect x="1144" y="191" width="5" height="12"/></g>')
    out.append('<path d="M0 281 H1200 V330 H0Z" fill="#080c11"/><path d="M0 287 H1200" stroke="#1c252d" stroke-width="2"/>')
    for x,y,ww,hh in [(0,267,54,28),(66,277,74,22),(171,264,87,35),(273,278,55,20),(905,272,74,27),(994,264,81,35),(1096,276,104,22),(350,274,45,26),(808,277,51,23)]:
        out.append(f'<rect x="{x}" y="{y}" width="{ww}" height="{hh}" rx="2" fill="#121920" stroke="#27313a"/>')
    out.append(bonfire(600, 289, prefix, .88))
    out.append(f'<text x="600" y="95" text-anchor="middle" fill="{CREAM}" font-family="{SERIF}" font-size="51" letter-spacing="18">AXIRA</text>')
    out.append(f'<text x="600" y="133" text-anchor="middle" fill="{MUTED}" font-family="{MONO}" font-size="12.5" letter-spacing="2.5">MINECRAFT SYSTEMS  •  COMBAT  •  INTERFACES  •  WORLDS</text>')
    out.append(f'<path d="M323 155 H552 M648 155 H877" stroke="{GOLD2}" stroke-width="1.4"/><path d="M600 147 l8 8 -8 8 -8 -8z" fill="none" stroke="{GOLD}"/><circle cx="600" cy="155" r="2.3" fill="{GOLD}"/>')
    out.append(f'<text x="600" y="190" text-anchor="middle" fill="#78838c" font-family="{MONO}" font-size="9.5" letter-spacing="1.4">{escape(subtitle.upper())}</text>')
    out.append(f'<circle cx="930" cy="303" r="3.8" fill="{GREEN}"><animate attributeName="opacity" values=".35;1;.35" dur="2.6s" repeatCount="indefinite"/></circle><text x="942" y="307" fill="#6d7780" font-family="{MONO}" font-size="9.2" letter-spacing="1">NOW BUILDING  {escape(str(current).upper())}</text>')
    out.append('</svg>')
    return ''.join(out)


def build_footer() -> str:
    w, h = 1200, 156
    p = "foot"
    out = [svg_open(w,h,"Rest at the bonfire"), common_defs(p), f'<rect width="{w}" height="{h}" fill="url(#{p}-bg)"/>']
    out.append('<path d="M0 118 H1200" stroke="#172028"/><path d="M318 119 H520 M680 119 H882" stroke="#5f4d33"/>')
    out.append(bonfire(600, 84, p, .58))
    out.append(f'<text x="600" y="137" text-anchor="middle" fill="{GOLD}" font-family="{MONO}" font-size="10.5" letter-spacing="4">REST AT THE BONFIRE</text>')
    out.append('</svg>')
    return ''.join(out)


def icon_svg(label: str, body: str, accent: str = GOLD) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64" role="img" aria-label="{escape(label)}">
<rect x="1" y="1" width="62" height="62" rx="14" fill="#0b1118" stroke="#2c3640"/>
<rect x="6" y="6" width="52" height="52" rx="10" fill="#0e151d" stroke="{accent}" stroke-opacity=".32"/>
{body}
</svg>'''


def write_icons() -> None:
    icons = {
        "project-adventure.svg": ("MaplesAdventure", f'<path d="M18 47 L45 20 M23 50 L48 25 M16 39 L25 48" stroke="{GOLD}" stroke-width="3" stroke-linecap="round"/><path d="M42 18 l6 6" stroke="{CREAM}" stroke-width="3"/><circle cx="26" cy="27" r="14" fill="none" stroke="#40505e"/>'),
        "project-world.svg": ("Maples World", f'<path d="M13 49 V29 H22 V21 H30 V29 H39 V17 H48 V29 H53 V49Z" fill="none" stroke="{GOLD}" stroke-width="2.5"/><path d="M17 49 H52" stroke="{CREAM}" stroke-width="2"/><rect x="23" y="37" width="4" height="12" fill="{ORANGE}"/><rect x="42" y="34" width="4" height="7" fill="{ORANGE2}"/>'),
        "project-menu.svg": ("RPG Menu Framework", f'<rect x="15" y="16" width="34" height="33" rx="4" fill="none" stroke="{GOLD}" stroke-width="2.4"/><path d="M21 24 H43 M21 31 H35 M21 38 H40" stroke="{CREAM}" stroke-width="2"/><circle cx="45" cy="40" r="5" fill="none" stroke="{BLUE}" stroke-width="2"/>'),
        "project-core.svg": ("MaplesCore", f'<path d="M32 13 L49 23 V42 L32 52 15 42 V23Z" fill="none" stroke="{GOLD}" stroke-width="2.6"/><path d="M32 13 V52 M15 23 L49 42 M49 23 L15 42" stroke="#8f7348" stroke-width="1.4"/><circle cx="32" cy="32" r="5" fill="{ORANGE2}" opacity=".9"/>'),
        "java.svg": ("Java 21", f'<path d="M20 42 C20 49 44 49 44 42 M22 37 H42 L39 46 H25Z" fill="none" stroke="{GOLD}" stroke-width="2.4"/><path d="M29 31 C20 24 39 25 32 17 C28 13 34 11 35 9" fill="none" stroke="{CREAM}" stroke-width="2.2" stroke-linecap="round"/>'),
        "neoforge.svg": ("NeoForge", f'<path d="M16 28 H48 L43 36 H35 V47 H29 V36 H21Z" fill="none" stroke="{GOLD}" stroke-width="2.5"/><path d="M22 24 H42" stroke="{CREAM}" stroke-width="3"/><circle cx="32" cy="18" r="4" fill="{ORANGE2}"/>'),
        "kubejs.svg": ("KubeJS", f'<path d="M32 13 L48 22 V41 L32 50 16 41 V22Z" fill="none" stroke="{GOLD}" stroke-width="2.4"/><path d="M16 22 L32 32 48 22 M32 32 V50" fill="none" stroke="#8c754f" stroke-width="2"/><text x="32" y="28" text-anchor="middle" fill="{CREAM}" font-family="{MONO}" font-size="8" font-weight="700">JS</text>'),
        "gradle.svg": ("Gradle", f'<path d="M14 35 C15 22 24 17 34 18 C43 18 50 23 50 31 C50 39 43 45 34 45 H19 C15 43 13 40 14 35Z" fill="none" stroke="{GOLD}" stroke-width="2.3"/><circle cx="38" cy="27" r="2" fill="{CREAM}"/><path d="M18 38 C24 34 31 35 35 39" stroke="#7a8e9e" stroke-width="2" fill="none"/>'),
        "git.svg": ("Git", f'<path d="M23 17 V45 M23 23 H41 V35" fill="none" stroke="{GOLD}" stroke-width="2.5"/><circle cx="23" cy="17" r="5" fill="#0e151d" stroke="{CREAM}" stroke-width="2"/><circle cx="23" cy="47" r="5" fill="#0e151d" stroke="{CREAM}" stroke-width="2"/><circle cx="41" cy="35" r="5" fill="#0e151d" stroke="{ORANGE2}" stroke-width="2"/>'),
        "actions.svg": ("GitHub Actions", f'<circle cx="20" cy="20" r="6" fill="none" stroke="{GOLD}" stroke-width="2"/><circle cx="43" cy="32" r="6" fill="none" stroke="{CREAM}" stroke-width="2"/><circle cx="22" cy="45" r="6" fill="none" stroke="{BLUE}" stroke-width="2"/><path d="M25 22 L38 29 M38 35 L27 42" stroke="#768897" stroke-width="2"/><path d="M18 17 l5 3 -5 3Z" fill="{ORANGE2}"/>'),
        "blender.svg": ("Blender", f'<path d="M16 30 H31 L39 23 M23 22 L40 22 C48 23 51 29 48 36 C45 43 35 46 27 42 C18 38 19 29 27 26" fill="none" stroke="{GOLD}" stroke-width="2.6" stroke-linecap="round"/><circle cx="36" cy="34" r="6" fill="none" stroke="{CREAM}" stroke-width="2"/>'),
        "blockbench.svg": ("Blockbench", f'<path d="M19 21 H45 V43 H19Z" fill="none" stroke="{GOLD}" stroke-width="2.3"/><path d="M19 21 L32 14 45 21 M32 14 V36 M19 43 L32 36 45 43" fill="none" stroke="{CREAM}" stroke-width="1.8"/>'),
        "unity.svg": ("Unity C sharp", f'<path d="M18 22 L31 14 47 23 45 41 31 50 17 41Z" fill="none" stroke="{GOLD}" stroke-width="2.5"/><path d="M31 14 V34 L17 41 M31 34 L45 41 M31 34 L47 23" fill="none" stroke="{CREAM}" stroke-width="1.8"/>'),
        "python.svg": ("Python", f'<path d="M20 31 C20 19 24 16 32 16 H39 C44 16 46 19 46 24 V30 H31 C25 30 22 33 22 38" fill="none" stroke="{GOLD}" stroke-width="2.5"/><path d="M44 33 C44 45 40 48 32 48 H25 C20 48 18 45 18 40 V34 H33 C39 34 42 31 42 26" fill="none" stroke="{BLUE}" stroke-width="2.5"/><circle cx="38" cy="22" r="1.8" fill="{CREAM}"/><circle cx="26" cy="42" r="1.8" fill="{CREAM}"/>'),
    }
    for filename, (label, body) in icons.items():
        (ICONS / filename).write_text(icon_svg(label, body), encoding="utf-8")


def build_divider() -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="34" viewBox="0 0 1200 34" role="img" aria-label="section divider">
<path d="M38 17 H548 M652 17 H1162" stroke="#4b4032"/><path d="M468 17 H548 M652 17 H732" stroke="{GOLD2}" opacity=".8"/><path d="M600 8 l9 9 -9 9 -9 -9z" fill="none" stroke="{GOLD}"/><circle cx="600" cy="17" r="2.5" fill="{GOLD}"/>
</svg>'''


def main() -> int:
    config = load_json(CONFIG)
    status = load_json(STATUS)
    write_icons()
    (ASSETS / "hero.svg").write_text(build_hero(config, status), encoding="utf-8")
    (ASSETS / "footer.svg").write_text(build_footer(), encoding="utf-8")
    (ASSETS / "divider.svg").write_text(build_divider(), encoding="utf-8")
    print("Built static profile visuals.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
