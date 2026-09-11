#!/usr/bin/env python3
"""Build the self-hosted SVG visual system for Axira-A's GitHub profile.

No third-party runtime service is required for the core visuals.  Everything here
is plain SVG + native SMIL animation, which keeps text and lines vector-sharp on
GitHub and avoids raster blur.
"""
from __future__ import annotations

from pathlib import Path
import random
from html import escape

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

BG0 = "#070b10"
BG1 = "#0b1118"
BG2 = "#111a24"
GOLD = "#c9a467"
GOLD2 = "#8f7348"
CREAM = "#eee5d3"
MUTED = "#a89f91"
BLUE = "#6e8fa9"
ORANGE = "#ff8a2a"
ORANGE2 = "#ffc05d"
GREEN = "#7fa37d"

SERIF = "Georgia, 'Times New Roman', serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def svg_open(w: int, h: int) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'


def defs(prefix: str = "x") -> str:
    return f'''<defs>
  <linearGradient id="{prefix}bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{BG0}"/><stop offset="0.55" stop-color="{BG1}"/><stop offset="1" stop-color="#090d12"/>
  </linearGradient>
  <linearGradient id="{prefix}gold" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{GOLD2}" stop-opacity="0"/><stop offset=".5" stop-color="{GOLD}"/><stop offset="1" stop-color="{GOLD2}" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="{prefix}fire" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="#fff2b0"/><stop offset=".35" stop-color="{ORANGE2}"/><stop offset=".72" stop-color="{ORANGE}"/><stop offset="1" stop-color="#c54c19" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="{prefix}glow" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="{ORANGE2}" stop-opacity=".42"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/>
  </radialGradient>
  <filter id="{prefix}blur"><feGaussianBlur stdDeviation="12"/></filter>
  <filter id="{prefix}soft"><feGaussianBlur stdDeviation="4"/></filter>
</defs>'''


def stars(w: int, h: int, seed: int = 17, count: int = 70) -> str:
    rnd = random.Random(seed)
    out = []
    for i in range(count):
        x = rnd.randint(22, w - 22)
        y = rnd.randint(16, int(h * 0.52))
        r = rnd.choice([0.6, 0.8, 1.0, 1.2])
        op = rnd.uniform(0.22, 0.72)
        if i < 10:
            out.append(
                f'<circle cx="{x}" cy="{y}" r="{r}" fill="#cbd8e3" opacity="{op:.2f}">'
                f'<animate attributeName="opacity" values="{op:.2f};{min(op+0.35,1):.2f};{op:.2f}" dur="{3+i%4}s" begin="-{i*.23:.2f}s" repeatCount="indefinite"/>'
                '</circle>'
            )
        else:
            out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#cbd8e3" opacity="{op:.2f}"/>')
    return ''.join(out)


def bonfire(cx: int, cy: int, prefix: str) -> str:
    return f'''
<ellipse cx="{cx}" cy="{cy+3}" rx="84" ry="26" fill="url(#{prefix}glow)" filter="url(#{prefix}blur)" opacity=".62">
  <animate attributeName="opacity" values=".45;.75;.5;.62" dur="4.8s" repeatCount="indefinite"/>
</ellipse>
<g opacity=".95">
  <rect x="{cx-38}" y="{cy+21}" width="76" height="7" rx="2" fill="#34271d"/>
  <path d="M{cx-27} {cy+20} L{cx+26} {cy-4}" stroke="#563b25" stroke-width="7" stroke-linecap="round"/>
  <path d="M{cx+27} {cy+20} L{cx-26} {cy-4}" stroke="#4b3321" stroke-width="7" stroke-linecap="round"/>
</g>
<path d="M{cx} {cy+17} C{cx-19} {cy+4},{cx-20} {cy-13},{cx-7} {cy-28} C{cx-6} {cy-13},{cx+2} {cy-10},{cx+7} {cy-31} C{cx+22} {cy-11},{cx+18} {cy+5},{cx} {cy+17}Z" fill="#f27022">
  <animate attributeName="d" dur="2.4s" repeatCount="indefinite" values="M{cx} {cy+17} C{cx-19} {cy+4},{cx-20} {cy-13},{cx-7} {cy-28} C{cx-6} {cy-13},{cx+2} {cy-10},{cx+7} {cy-31} C{cx+22} {cy-11},{cx+18} {cy+5},{cx} {cy+17}Z;M{cx} {cy+17} C{cx-17} {cy+3},{cx-14} {cy-17},{cx-3} {cy-37} C{cx+1} {cy-14},{cx+8} {cy-14},{cx+12} {cy-25} C{cx+21} {cy-8},{cx+16} {cy+7},{cx} {cy+17}Z;M{cx} {cy+17} C{cx-19} {cy+4},{cx-20} {cy-13},{cx-7} {cy-28} C{cx-6} {cy-13},{cx+2} {cy-10},{cx+7} {cy-31} C{cx+22} {cy-11},{cx+18} {cy+5},{cx} {cy+17}Z"/>
</path>
<path d="M{cx} {cy+16} C{cx-10} {cy+5},{cx-8} {cy-9},{cx} {cy-19} C{cx+9} {cy-7},{cx+11} {cy+5},{cx} {cy+16}Z" fill="#ffd36f">
  <animate attributeName="opacity" values=".95;.7;1;.85" dur="1.8s" repeatCount="indefinite"/>
</path>
'''+''.join(
        f'<circle cx="{cx + dx}" cy="{cy-25-dy}" r="{r}" fill="{col}" opacity="0">'
        f'<animate attributeName="cy" values="{cy-20-dy};{cy-92-dy}" dur="{dur}s" begin="-{delay}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0;.9;.7;0" dur="{dur}s" begin="-{delay}s" repeatCount="indefinite"/>'
        '</circle>'
        for dx, dy, r, col, dur, delay in [
            (-18,0,2.4,ORANGE,3.4,.2),(14,9,2.0,ORANGE2,3.0,1.1),(5,22,1.5,ORANGE,4.1,2.3),
            (-7,31,1.8,ORANGE2,3.8,.8),(26,17,1.4,ORANGE,3.7,1.8),(-28,25,1.1,ORANGE2,4.4,3.1)
        ]
    )


def build_hero() -> str:
    w, h = 1200, 360
    p = "hero"
    s = [svg_open(w,h), defs(p), f'<rect width="{w}" height="{h}" fill="url(#{p}bg)"/>']
    s.append(stars(w,h))
    # moon
    s.append('<rect x="98" y="62" width="34" height="34" rx="2" fill="#dce6ef" opacity=".78"/>')
    s.append('<rect x="104" y="67" width="9" height="8" fill="#aab8c4" opacity=".55"/><rect x="119" y="81" width="8" height="10" fill="#aab8c4" opacity=".48"/>')
    s.append('<circle cx="115" cy="79" r="42" fill="#adc2d3" opacity=".08" filter="url(#heroblur)"><animate attributeName="opacity" values=".05;.12;.05" dur="7s" repeatCount="indefinite"/></circle>')
    # mountains
    s.append('<path d="M0 230 L90 178 153 207 222 162 289 208 360 173 438 217 524 181 606 214 682 175 760 210 842 166 924 211 1003 174 1093 206 1200 154 1200 360 0 360Z" fill="#0d151d"/>')
    s.append('<path d="M0 252 L112 211 192 239 278 201 359 246 452 216 548 250 634 219 741 246 827 209 934 243 1045 202 1200 238 1200 360 0 360Z" fill="#111c26" opacity=".9"/>')
    # fog layers
    s.append('<g opacity=".2" fill="#7890a3"><ellipse cx="130" cy="236" rx="180" ry="24"/><ellipse cx="500" cy="248" rx="240" ry="27"/><ellipse cx="960" cy="232" rx="230" ry="25"/><animateTransform attributeName="transform" type="translate" values="-35 0;35 0;-35 0" dur="18s" repeatCount="indefinite"/></g>')
    s.append('<g opacity=".12" fill="#9eb2c1"><ellipse cx="300" cy="262" rx="220" ry="20"/><ellipse cx="820" cy="256" rx="270" ry="22"/><animateTransform attributeName="transform" type="translate" values="30 0;-30 0;30 0" dur="24s" repeatCount="indefinite"/></g>')
    # aqueducts + ruins
    for base_x, mirror in [(22,1),(1178,-1)]:
        # use normal coords manually mirrored with transform around sides
        pass
    s.append('<g fill="#0a1016" stroke="#17222c" stroke-width="2">')
    # left aqueduct
    s.append('<path d="M0 249 H260 V263 H0Z"/><path d="M35 249 V217 H58 V249 M82 249 V211 H108 V249 M132 249 V223 H157 V249 M181 249 V215 H207 V249 M230 249 V226 H252 V249" fill="#0a1016"/>')
    # right
    s.append('<path d="M940 249 H1200 V263 H940Z"/><path d="M957 249 V223 H982 V249 M1008 249 V212 H1034 V249 M1060 249 V222 H1085 V249 M1111 249 V210 H1138 V249 M1164 249 V220 H1188 V249" fill="#0a1016"/>')
    # towers
    s.append('<path d="M22 248 V170 H54 V248 M28 170 V154 H35 V170 M42 170 V150 H49 V170"/><path d="M1118 248 V157 H1157 V248 M1126 157 V139 H1134 V157 M1145 157 V145 H1152 V157"/>')
    s.append('</g>')
    # warm windows
    s.append('<g fill="#f28a2d" opacity=".7"><rect x="33" y="185" width="4" height="11"/><rect x="44" y="202" width="4" height="10"/><rect x="1130" y="178" width="5" height="13"/><rect x="1143" y="191" width="5" height="12"/></g>')
    # foreground platform
    s.append('<path d="M0 284 H1200 V360 H0Z" fill="#080c11"/><path d="M0 290 H1200" stroke="#1c252d" stroke-width="2"/>')
    # stone blocks
    for x,y,ww,hh in [(0,270,54,28),(67,279,74,22),(172,266,86,35),(272,280,54,20),(906,274,74,27),(994,266,81,35),(1096,278,104,22),(349,276,44,26),(808,279,50,23)]:
        s.append(f'<rect x="{x}" y="{y}" width="{ww}" height="{hh}" rx="2" fill="#121920" stroke="#27313a"/>')
    # fire + title
    s.append(bonfire(600, 302, p))
    s.append(f'<text x="600" y="103" text-anchor="middle" fill="{CREAM}" font-family="{SERIF}" font-size="52" letter-spacing="18">AXIRA</text>')
    s.append(f'<text x="600" y="143" text-anchor="middle" fill="{MUTED}" font-family="{MONO}" font-size="13" letter-spacing="3">MINECRAFT SYSTEMS  •  WORLDS  •  MODDING</text>')
    s.append(f'<path d="M330 166 H555 M645 166 H870" stroke="{GOLD2}" stroke-width="1.5"/><path d="M600 158 l8 8 -8 8 -8 -8z" fill="none" stroke="{GOLD}"/><circle cx="600" cy="166" r="2.5" fill="{GOLD}"/>')
    # subtle scanning glint
    s.append(f'<path d="M330 166 H390" stroke="{GOLD}" stroke-width="2" opacity="0"><animate attributeName="opacity" values="0;.7;0" dur="5s" repeatCount="indefinite"/><animateTransform attributeName="transform" type="translate" values="0 0;480 0" dur="5s" repeatCount="indefinite"/></path>')
    s.append(f'<circle cx="1050" cy="326" r="4" fill="{GREEN}"><animate attributeName="opacity" values=".35;1;.35" dur="2.8s" repeatCount="indefinite"/></circle><text x="1062" y="330" fill="#6f7a82" font-family="{MONO}" font-size="10" letter-spacing="1.2">PROFILE // ACTIVE</text>')
    s.append('</svg>')
    return ''.join(s)


def project_icon(kind: str, x: int, y: int) -> str:
    if kind == "adventure":
        return f'''<g transform="translate({x} {y})" stroke="{GOLD}" fill="none" stroke-width="3" stroke-linecap="round">
<path d="M10 54 L54 10 M20 54 L54 20 M8 44 L20 56"/><path d="M48 9 l8 8"/><circle cx="22" cy="22" r="18" stroke="#31404d" stroke-width="1"/>
</g>'''
    if kind == "world":
        return f'''<g transform="translate({x} {y})" stroke="{GOLD}" fill="none" stroke-width="3">
<path d="M7 59 V29 H20 V18 H31 V29 H44 V13 H56 V29 H69 V59Z"/><path d="M18 59 V43 H29 V59 M45 59 V39 H56 V59"/><path d="M2 59 H74"/>
</g>'''
    if kind == "rpg":
        return f'''<g transform="translate({x} {y})" stroke="{GOLD}" fill="none" stroke-width="2.5">
<rect x="4" y="10" width="72" height="52" rx="6"/><path d="M4 25 H76 M26 25 V62"/><circle cx="15" cy="18" r="2" fill="{GOLD}"/><circle cx="22" cy="18" r="2" fill="{GOLD2}"/><path d="M34 36 H65 M34 45 H59 M34 54 H52"/>
</g>'''
    return f'''<g transform="translate({x} {y})" stroke="{GOLD}" fill="none" stroke-width="2.5">
<circle cx="12" cy="36" r="7"/><circle cx="62" cy="17" r="7"/><circle cx="62" cy="55" r="7"/><circle cx="37" cy="36" r="8"/><path d="M19 36 H29 M45 32 L55 21 M45 40 L55 51"/>
</g>'''


def project_card(filename: str, title: str, subtitle: str, status: str, chips: list[str], kind: str, accent: str) -> None:
    w,h=580,210
    p=filename.replace('.','')
    out=[svg_open(w,h), defs(p), f'<rect width="{w}" height="{h}" rx="18" fill="url(#{p}bg)"/>']
    out.append(f'<rect x="1" y="1" width="578" height="208" rx="17" fill="none" stroke="#3d352b"/><path d="M0 46 H580" stroke="#1a232c"/>')
    out.append(f'<rect x="0" y="0" width="5" height="210" rx="2" fill="{accent}" opacity=".8"/>')
    out.append(f'<circle cx="30" cy="25" r="4" fill="{accent}"><animate attributeName="opacity" values=".4;1;.4" dur="2.8s" repeatCount="indefinite"/></circle>')
    out.append(f'<text x="42" y="30" fill="#9a8c78" font-family="{MONO}" font-size="10" letter-spacing="1.6">{escape(status)}</text>')
    out.append(f'<text x="30" y="88" fill="{CREAM}" font-family="{SERIF}" font-size="28">{escape(title)}</text>')
    out.append(f'<text x="30" y="116" fill="{MUTED}" font-family="{MONO}" font-size="12" letter-spacing=".6">{escape(subtitle)}</text>')
    x=30
    for chip in chips:
        width=20+len(chip)*7.2
        out.append(f'<rect x="{x}" y="144" width="{width:.0f}" height="26" rx="13" fill="#111922" stroke="#2b3640"/><text x="{x+10}" y="161" fill="#b9b09f" font-family="{MONO}" font-size="10">{escape(chip)}</text>')
        x += width+8
    out.append(project_icon(kind, 456, 88))
    out.append(f'<path d="M452 181 H543" stroke="{accent}" opacity=".5"/><text x="543" y="194" text-anchor="end" fill="#756b5d" font-family="{MONO}" font-size="9">OPEN PROJECT  →</text>')
    out.append(f'<path d="M540 20 H559 V39" fill="none" stroke="{GOLD2}"/><path d="M21 190 H40" stroke="{GOLD2}"/>')
    out.append('</svg>')
    (ASSETS/filename).write_text(''.join(out),encoding='utf-8')


def tool_icon(kind: str, cx: int, cy: int) -> str:
    # all icons are deliberately simplified local vectors: recognizable but not third-party logos.
    if kind == 'java':
        return f'<g transform="translate({cx-20} {cy-24})" fill="none" stroke="{GOLD}" stroke-width="2.4" stroke-linecap="round"><path d="M9 38 C20 44 33 44 42 38"/><path d="M12 31 C22 35 31 35 39 31"/><path d="M17 26 C25 29 32 29 37 26"/><path d="M26 4 C16 12 36 14 24 23"/></g>'
    if kind == 'anvil':
        return f'<g transform="translate({cx-25} {cy-22})" fill="{GOLD}"><path d="M4 5 H47 L41 15 H34 V23 H39 V30 H13 V23 H20 V15 H9Z"/><rect x="17" y="30" width="19" height="7" rx="2"/></g>'
    if kind == 'cube':
        return f'<g transform="translate({cx-23} {cy-24})" fill="none" stroke="{GOLD}" stroke-width="2.2"><path d="M23 3 L43 14 V37 L23 48 L3 37 V14Z"/><path d="M3 14 L23 25 L43 14 M23 25 V48"/><circle cx="15" cy="16" r="2" fill="{GOLD}"/><circle cx="31" cy="16" r="2" fill="{GOLD}"/></g>'
    if kind == 'gradle':
        return f'<g transform="translate({cx-25} {cy-20})" fill="{GOLD}"><path d="M5 20 C10 7 30 3 44 12 C49 15 51 23 47 28 C43 34 35 31 34 25 C29 34 18 36 7 31 C3 29 2 24 5 20Z"/><circle cx="34" cy="17" r="2.5" fill="{BG0}"/></g>'
    if kind == 'git':
        return f'<g transform="translate({cx-23} {cy-23})" fill="none" stroke="{GOLD}" stroke-width="2.5"><circle cx="10" cy="10" r="5"/><circle cx="36" cy="36" r="5"/><circle cx="36" cy="10" r="5"/><path d="M14 10 H31 M10 15 V27 C10 33 15 36 31 36"/></g>'
    if kind == 'blender':
        return f'<g transform="translate({cx-26} {cy-20})" fill="none" stroke="{GOLD}" stroke-width="3" stroke-linecap="round"><path d="M3 14 H27 L17 4 M27 14 C39 14 47 21 47 28 C47 35 40 40 31 40 C22 40 14 35 14 28 C14 22 19 17 27 14Z"/><circle cx="31" cy="28" r="7"/></g>'
    if kind == 'bench':
        return f'<g transform="translate({cx-24} {cy-23})" fill="none" stroke="{GOLD}" stroke-width="2.4"><path d="M7 8 H41 V29 H7Z"/><path d="M7 18 H41 M14 29 V41 M34 29 V41 M12 41 H36"/></g>'
    return f'<g transform="translate({cx-23} {cy-23})" fill="none" stroke="{GOLD}" stroke-width="2.5"><path d="M23 3 L42 14 V36 L23 47 L4 36 V14Z"/><path d="M23 3 V47 M4 14 L42 36 M42 14 L4 36"/></g>'


def build_tools() -> str:
    w,h=1200,300
    p='tools'
    tools=[
        ('Java 21','Runtime / Modding','java'),('NeoForge','Minecraft Platform','anvil'),('KubeJS','Scripting / Data','cube'),('Gradle','Build System','gradle'),
        ('Git','Version Control','git'),('Blender','Animation / 3D','blender'),('Blockbench','Voxel Modeling','bench'),('Unity / C#','Game Development','unity')]
    out=[svg_open(w,h), defs(p), f'<rect width="{w}" height="{h}" rx="18" fill="url(#{p}bg)"/>',
         '<rect x="1" y="1" width="1198" height="298" rx="17" fill="none" stroke="#3d352b"/>']
    out.append(f'<text x="44" y="48" fill="{CREAM}" font-family="{SERIF}" font-size="26" letter-spacing="3">EQUIPPED TOOLS</text><text x="1155" y="46" text-anchor="end" fill="#6d675f" font-family="{MONO}" font-size="10">LOCAL VECTOR ICONS · NO RUNTIME DEPENDENCY</text>')
    out.append(f'<path d="M44 67 H1156" stroke="#2b3138"/><path d="M44 67 H220" stroke="{GOLD2}"/>')
    start_x,start_y=44,90
    cw,ch,gx,gy=267,82,14,16
    for i,(name,desc,kind) in enumerate(tools):
        col=i%4; row=i//4; x=start_x+col*(cw+gx); y=start_y+row*(ch+gy)
        out.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="12" fill="#0d141c" stroke="#26313a"/>')
        out.append(tool_icon(kind,x+43,y+41))
        out.append(f'<text x="{x+82}" y="{y+34}" fill="{CREAM}" font-family="{MONO}" font-size="13" font-weight="700">{escape(name)}</text><text x="{x+82}" y="{y+56}" fill="#7f8a91" font-family="{MONO}" font-size="9.5">{escape(desc)}</text>')
        out.append(f'<rect x="{x+10}" y="{y+10}" width="3" height="{ch-20}" rx="1.5" fill="{GOLD2}" opacity=".5"/>')
    # animated top glint
    out.append(f'<path d="M44 67 H140" stroke="{GOLD}" stroke-width="2" opacity="0"><animate attributeName="opacity" values="0;.65;0" dur="6s" repeatCount="indefinite"/><animateTransform attributeName="transform" type="translate" values="0 0;1010 0" dur="6s" repeatCount="indefinite"/></path>')
    out.append('</svg>')
    return ''.join(out)


def build_footer() -> str:
    w,h=1200,230
    p='foot'
    out=[svg_open(w,h), defs(p), f'<rect width="{w}" height="{h}" fill="url(#{p}bg)"/>', stars(w,h,seed=9,count=25)]
    out.append('<path d="M0 177 L145 149 265 168 404 143 520 171 680 151 815 170 947 142 1064 167 1200 146 1200 230 0 230Z" fill="#0c131a"/>')
    out.append('<g opacity=".16" fill="#8aa1b1"><ellipse cx="300" cy="177" rx="220" ry="16"/><ellipse cx="840" cy="172" rx="250" ry="18"/><animateTransform attributeName="transform" type="translate" values="-20 0;20 0;-20 0" dur="20s" repeatCount="indefinite"/></g>')
    out.append(bonfire(600,165,p))
    out.append(f'<path d="M330 203 H490 M710 203 H870" stroke="{GOLD2}"/>')
    out.append(f'<text x="600" y="208" text-anchor="middle" fill="{CREAM}" font-family="{MONO}" font-size="12" letter-spacing="4">REST AT THE BONFIRE</text>')
    out.append('</svg>')
    return ''.join(out)


def main() -> int:
    (ASSETS/'hero.svg').write_text(build_hero(),encoding='utf-8')
    (ASSETS/'tools.svg').write_text(build_tools(),encoding='utf-8')
    (ASSETS/'footer.svg').write_text(build_footer(),encoding='utf-8')
    project_card('project-maplesadventure.svg','MaplesAdventure','Souls-like combat · encounters · exploration','ACTIVE DEVELOPMENT',['NeoForge 1.21.1','Combat','World Design'],'adventure','#d18d47')
    project_card('project-maplesworld.svg','Maples;World','Persistent multiplayer world & server ecosystem','SERVER PROJECT',['Economy','Progression','Create'],'world','#b9874f')
    project_card('project-rpg-menu.svg','RPG Menu Framework','Immersive inventory, equipment and RPG UI','PUBLIC REPOSITORY',['Java','UI / UX','Integrations'],'rpg','#8d77c7')
    project_card('project-maplescore.svg','MaplesCore','Shared server systems, persistence and administration','CORE SYSTEMS',['Server Authority','Data','Economy'],'core','#6f9a86')
    print('Built vector profile visuals.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
