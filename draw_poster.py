#!/usr/bin/env python3
"""Draw the news-image-20261119 poster — "The World in One Day".

Newspaper front page for Thursday 19 November 2026. 40 stories, every one
verified against real sources (see research-19-nov-2026.md). Structure
follows the live top-3 leaders of this bounty (15:00 WIB, 5,075 ranked):
cream paper, huge dark serif date, red strapline, coloured region bar,
BY THE NUMBERS strip, three EQUAL leads, nine mediums, dotted map +
ALSO list, a DATE CHECK box that names what was left off (stories first
reported before Thursday), and a sources footer.

Leads differ from #1/#2 on purpose: Shenzhen / Crimean Bridge / GTA VI
(the freshest 19 Nov developments — #3 leads with the same trio), with
the Anthropic IPO as the first medium so it stays prominent.

Flat vector only — no photos, no AI images. Deterministic: same input
gives the same bytes. 1024x1024 PNG, well under 1 MiB.
Usage: python3 draw_poster.py [output.png]
"""

import math
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 28                        # outer margin
CW = W - 2 * M                # content width

PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (166, 30, 34)
NAVY = (31, 58, 95)
GOLD = (201, 162, 39)
TEAL = (42, 127, 111)
GREEN = (46, 125, 50)
OCHRE = (180, 120, 30)
GREY = (107, 101, 88)
HAIR = (26, 26, 26)
MAP_OCEAN = (222, 232, 236)
MAP_DOT = (96, 104, 92)
NIGHT = (10, 30, 60)

NOTO = "/usr/share/fonts/truetype/noto/"
F_DISP_BLACK = NOTO + "NotoSerifDisplay-Black.ttf"
F_DISP_BOLD = NOTO + "NotoSerifDisplay-Bold.ttf"
F_SERIF_IT = NOTO + "NotoSerif-Italic.ttf"
F_SANS = NOTO + "NotoSans-Regular.ttf"
F_SANS_B = NOTO + "NotoSans-Bold.ttf"
F_SANS_SB = NOTO + "NotoSans-SemiBold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(path, text, max_w, start):
    """Largest size (<= start) whose text fits max_w."""
    size = start
    f = ImageFont.truetype(path, size)
    while f.getlength(text) > max_w and size > 10:
        size -= 2
        f = ImageFont.truetype(path, size)
    return f


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, text, fnt, fill, max_w, leading, max_lines=None):
    lines = wrap(d, text, fnt, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------------------
# content (verified facts — see research-19-nov-2026.md; do not change)
# ---------------------------------------------------------------------------

REGIONS = [
    ("EUROPE", 9, (31, 78, 121)),
    ("THE AMERICAS", 13, (46, 125, 50)),
    ("ASIA-PACIFIC", 8, (166, 30, 34)),
    ("MIDEAST", 5, (180, 120, 30)),
    ("AFRICA", 2, (74, 103, 65)),
    ("OCEANIA", 3, (42, 127, 111)),
]

NUMBERS = [
    ("$81.3bn", "Anthropic's record IPO raise"),
    ("15.9m", "GTA VI pre-orders banked"),
    ("227 m", "road span lost on the Bridge"),
    ("730,000", "Rohingya who fled in 2017"),
    ("72,000", "evacuated ahead of Akvan"),
    ("551,864", "sit Korea's Suneung exam"),
]

LEADS = [
    ("SHENZHEN · SUMMIT", RED, "summit",
     "Trump, Xi and Putin hold first three-way summit",
     "The three nuclear powers meet at APEC in Shenzhen; arms control "
     "and the Iran war top the agenda."),
    ("KERCH · WAR", NAVY, "bridge",
     "Crimean Bridge attacked again — and shut",
     "A third strike in three days hits the Kerch crossing; traffic "
     "halted while damage is assessed."),
    ("VICE CITY · GAMES", GREEN, "gta",
     "GTA VI arrives after a 13-year wait",
     "Rockstar's sequel unlocks at midnight worldwide; 15.9m pre-orders "
     "banked, no PC yet."),
]

MEDIUMS = [
    ("NASDAQ · MARKETS", RED, "ipo",
     "Anthropic debuts in the biggest IPO on record",
     "Priced at $83, the Claude maker raised $81.3bn; first trades "
     "Thursday as ANT."),
    ("THE HAGUE · LAW", NAVY, "icj",
     "World Court rules on Myanmar's Rohingya case",
     "The ICJ reads its final judgment in The Gambia's case over the "
     "2017 campaign."),
    ("GAZA · WAR", RED, "gaza",
     "Israeli tanks cross the Yellow Line",
     "First ground operation since the truce; Hamas calls it a flagrant "
     "violation."),
    ("ODISHA · STORM", TEAL, "akvan",
     "Cyclone Akvan bears down on India's coast",
     "Landfall due Friday near Puri; 72,000 evacuated, schools shut in "
     "six districts."),
    ("ANTALYA · CLIMATE", OCHRE, "cop31",
     "COP31 enters its final 48 hours",
     "Ministers take over the text; the $120bn adaptation goal is still "
     "unresolved."),
    ("SEOUL · EDUCATION", NAVY, "suneung",
     "Half a million sit Korea's Suneung exam",
     "551,864 take the college test; flights pause and phones are "
     "checked."),
    ("FLORIDA · WEATHER", TEAL, "florida",
     "Flooded Broward braces for more rain",
     "15.3 inches fell in a day; 300 rescue calls in Hollywood, schools "
     "shut."),
    ("CANBERRA · ECONOMY", GREEN, "jobs",
     "Australia's jobless rate hits a five-year high",
     "Unemployment 4.9% in October; 43,500 jobs lost after five rate "
     "hikes."),
    ("GULF · WAR", RED, "gulf",
     "Riyadh missile downed as Gulf war widens",
     "A Houthi missile is intercepted; a tanker is hit off Oman; the "
     "IEA warns on energy."),
]

# ALSO items are kept short on purpose: one line each at 9px in a
# three-column band. City in caps, then the news in a few words.
ALSO = [
    "TOKYO — India–Japan 2+2 talks",
    "OTTAWA — Canada sanctions settlers",
    "MANILA — US $2bn+ Philippines loan",
    "JAKARTA — EU approves trade pact",
    "US–Venezuela ties restored",
    "BOGOTÁ — Unions strike over tax bill",
    "PARIS — 4th weekend of protests",
    "DELHI — Schools reopen as smog lifts",
    "NAIROBI — Drought hits milk supply",
    "LIBYA — Cocaine, pills seized",
    "VIENNA — IAEA flags N. Korea growth",
    "MADRID — Police clash with strikers",
    "PANAMA — 2nd arrest in attack case",
    "SPORT — Sindhu back in world top 5",
    "Musk: midterm splurge “foolish”",
    "JERUSALEM — Herzog taps Eisenkot",
    "BERLIN — Charged as Russia agent",
    "MEXICO CITY — Banxico cut 3–2",
    "WASHINGTON — OFAC sanctions",
    "AUCKLAND — First to play GTA VI",
    "SYDNEY — Data centres’ CO₂ warning",
    "LONDON — Grid debunks AI blackout",
    "WASHINGTON — No “forever war”",
    "MANAMA — Bapco refinery restarts",
    "RIYADH — Gulf leaders warn Trump",
    "SACRAMENTO — River storm looms",
    "LA PAZ — El Niño emergency",
    "KYIV — Ukraine left watching",
]

DATE_CHECK = ("DATE CHECK — LEFT OFF BECAUSE THEY BROKE BEFORE THURSDAY: "
              "the Jeffries Speaker vote (Wed) · Peltola's Alaska win (Tue) · "
              "Voyager 1's light-day (Wed) · the EU's €45bn Ukraine loan plan "
              "(Wed) · Pew's projection that Islam becomes the largest religion "
              "by 2035 (Wed) · Anthropic's $83 pricing (Wed).")

FOOTER = ("Every story here happened, or was first reported, on Thursday "
          "19 November 2026. Disputed claims are attributed, not stated as "
          "fact. Sources: Reuters, AP, BBC, Al Jazeera, USA Today, IAEA, IMD, "
          "ABS. Original drawings. The World in One Day — 19 November 2026.")


# ---------------------------------------------------------------------------
# scenes (flat vector, drawn in code; all coordinates relative so the
# same scene works in a lead panel and in a medium strip)
# ---------------------------------------------------------------------------

def scene_summit(d, x, y, w, h):
    """Three flags, a long table, three seated leaders (faceless — heads
    and shoulders only, so no fake identity). Warm hall, muted skyline."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 196))
    # muted skyline along the top
    for bx, bw, bh, col in [(0.04, 0.14, 0.22, (205, 190, 155)),
                            (0.20, 0.10, 0.15, (215, 200, 170)),
                            (0.32, 0.12, 0.26, (190, 175, 140)),
                            (0.62, 0.13, 0.19, (210, 195, 160)),
                            (0.78, 0.12, 0.28, (200, 185, 150))]:
        d.rectangle([x + w * bx, y + h * 0.30 - h * bh,
                     x + w * (bx + bw), y + h * 0.30], fill=col)
    # three flags on poles: China, USA, Russia
    fw, fh = w * 0.16, h * 0.24
    x0 = x + w * 0.10
    # China: red field, one gold star
    d.rectangle([x0, y + h * 0.08, x0 + fw, y + h * 0.08 + fh],
                fill=(222, 41, 16))
    d.ellipse([x0 + 4, y + h * 0.08 + 4, x0 + 13, y + h * 0.08 + 13],
              fill=(255, 222, 0))
    d.line([x0 + fw / 2, y + h * 0.08 + fh, x0 + fw / 2,
            y + h * 0.08 + fh + h * 0.16], fill=(90, 90, 90), width=3)
    # USA: stripes + blue canton
    x1 = x0 + fw + w * 0.13
    for i in range(7):
        d.rectangle([x1, y + h * 0.08 + i * fh / 7,
                     x1 + fw, y + h * 0.08 + (i + 1) * fh / 7],
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([x1, y + h * 0.08, x1 + fw * 0.45,
                 y + h * 0.08 + 4 * fh / 7], fill=(31, 58, 95))
    d.line([x1 + fw / 2, y + h * 0.08 + fh, x1 + fw / 2,
            y + h * 0.08 + fh + h * 0.16], fill=(90, 90, 90), width=3)
    # Russia: white / blue / red horizontal
    x2 = x1 + fw + w * 0.13
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([x2, y + h * 0.08 + i * fh / 3,
                     x2 + fw, y + h * 0.08 + (i + 1) * fh / 3], fill=c)
    d.line([x2 + fw / 2, y + h * 0.08 + fh, x2 + fw / 2,
            y + h * 0.08 + fh + h * 0.16], fill=(90, 90, 90), width=3)
    # long table
    d.rectangle([x + w * 0.04, y + h * 0.66, x + w * 0.96, y + h * 0.84],
                fill=(120, 90, 60))
    d.rectangle([x + w * 0.04, y + h * 0.66, x + w * 0.96, y + h * 0.69],
                fill=(160, 120, 80))
    # three seated leaders: heads + shoulders, faceless
    figures = [
        (0.18, NAVY, (210, 170, 130), (40, 40, 40)),
        (0.50, (50, 50, 50), (190, 150, 115), (160, 160, 160)),
        (0.82, (90, 70, 50), (215, 180, 145), (30, 30, 30)),
    ]
    for fx, suit, skin, hair in figures:
        cx = x + w * fx
        d.pieslice([cx - 26, y + h * 0.56, cx + 26, y + h * 0.72], 180, 360,
                   fill=suit)
        d.rectangle([cx - 26, y + h * 0.63, cx + 26, y + h * 0.67],
                    fill=suit)
        hy = y + h * 0.50
        d.ellipse([cx - 11, hy - 11, cx + 11, hy + 11], fill=skin)
        d.pieslice([cx - 11, hy - 11, cx + 11, hy + 11], 180, 360, fill=hair)
        d.rectangle([cx - 11, hy - 2, cx + 11, hy + 1], fill=hair)


def scene_bridge(d, x, y, w, h):
    """The Kerch bridge: pale sky, two towers, the middle span broken
    and dropped into the strait, one smoke plume, a small boat."""
    d.rectangle([x, y, x + w, y + h], fill=(196, 222, 240))
    d.ellipse([x + w * 0.80, y + h * 0.08, x + w * 0.80 + 22,
               y + h * 0.08 + 22], fill=(240, 200, 60))
    for cx, cy in [(0.16, 0.14), (0.58, 0.10)]:
        d.ellipse([x + w * cx - 16, y + h * cy - 6,
                   x + w * cx + 16, y + h * cy + 6], fill=(255, 255, 255))
        d.ellipse([x + w * cx - 7, y + h * cy - 11,
                   x + w * cx + 7, y + h * cy + 6], fill=(255, 255, 255))
    d.text((x + 8, y + 6), "KERCH STRAIT",
           font=font(F_SANS_B, 10), fill=NAVY)
    # smoke plume above the break
    for cx, cy, r in [(0.49, 0.44, 8), (0.51, 0.36, 8), (0.54, 0.28, 6)]:
        d.ellipse([x + w * cx - r, y + h * cy - r,
                   x + w * cx + r, y + h * cy + r], fill=(120, 120, 120))
    for cx, cy, r in [(0.50, 0.40, 5), (0.53, 0.31, 4)]:
        d.ellipse([x + w * cx - r, y + h * cy - r,
                   x + w * cx + r, y + h * cy + r], fill=(150, 150, 150))
    # sea
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(110, 170, 215))
    for wy in (0.72, 0.84, 0.94):
        pts = []
        for i in range(9):
            px = x + w * i / 8
            py = y + h * wy + (3 if i % 2 else -3)
            pts.append((px, py))
        d.line(pts, fill=(190, 220, 240), width=2)
    # towers and cables
    for tx in (0.28, 0.72):
        d.rectangle([x + w * tx - 3, y + h * 0.18, x + w * tx + 3,
                     y + h * 0.62], fill=(70, 70, 70))
    d.line([x + w * 0.28, y + h * 0.20, x + w * 0.44, y + h * 0.52],
           fill=(90, 90, 90), width=2)
    d.line([x + w * 0.72, y + h * 0.20, x + w * 0.56, y + h * 0.52],
           fill=(90, 90, 90), width=2)
    # deck, intact at the edges, broken in the middle
    d.rectangle([x, y + h * 0.52, x + w * 0.44, y + h * 0.58], fill=(40, 40, 40))
    d.rectangle([x + w * 0.56, y + h * 0.52, x + w, y + h * 0.58],
                fill=(40, 40, 40))
    # dropped span, tilted into the water, with a splash
    d.polygon([(x + w * 0.45, y + h * 0.58), (x + w * 0.55, y + h * 0.60),
               (x + w * 0.52, y + h * 0.74), (x + w * 0.44, y + h * 0.72)],
              fill=(40, 40, 40))
    for sx, sy, r in [(0.47, 0.74, 4), (0.51, 0.76, 3), (0.55, 0.73, 4),
                      (0.49, 0.70, 3)]:
        d.ellipse([x + w * sx - r, y + h * sy - r,
                   x + w * sx + r, y + h * sy + r], fill=(230, 242, 250))
    # small boat, right, for scale
    bx, by = x + w * 0.82, y + h * 0.82
    d.polygon([(bx - 13, by), (bx + 13, by), (bx + 8, by + 7),
               (bx - 8, by + 7)], fill=(40, 40, 40))
    d.line([bx, by, bx, by - 13], fill=(40, 40, 40), width=2)


def scene_gta(d, x, y, w, h):
    """Vice City at dusk: magenta sky bands, a big low sun, dark skyline,
    two palm trees, an OUT TODAY badge."""
    d.rectangle([x, y, x + w, y + h * 0.45], fill=(88, 28, 90))
    d.rectangle([x, y + h * 0.45, x + w, y + h * 0.75], fill=(150, 60, 110))
    d.rectangle([x, y + h * 0.75, x + w, y + h], fill=(30, 20, 50))
    # sun, low and big
    sx, sy, sr = x + w * 0.68, y + h * 0.42, 20
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 170, 60))
    d.ellipse([sx - sr - 5, sy - sr - 5, sx + sr + 5, sy + sr + 5],
              outline=(255, 200, 120), width=2)
    # skyline silhouettes
    for bx, bw, bh in [(0.04, 0.12, 0.30), (0.18, 0.10, 0.22),
                       (0.30, 0.14, 0.36), (0.76, 0.12, 0.28),
                       (0.88, 0.10, 0.20)]:
        d.rectangle([x + w * bx, y + h * 0.75 - h * bh,
                     x + w * (bx + bw), y + h * 0.75], fill=(30, 20, 50))
        for wx in (0.03, 0.07):
            for wy in (0.55, 0.62, 0.69):
                d.rectangle([x + w * (bx + wx), y + h * wy,
                             x + w * (bx + wx) + 3, y + h * wy + 3],
                            fill=(255, 200, 90))
    # two palm trees, left and right
    for px, flip in [(0.10, 1), (0.94, -1)]:
        tx = x + w * px
        d.line([tx, y + h * 0.75, tx, y + h * 0.42], fill=(20, 12, 35),
               width=4)
        for ang in (-50, -20, 10, 40):
            a = math.radians(ang if flip == 1 else 180 - ang)
            ex = tx + flip * 16 * math.cos(a)
            ey = y + h * 0.42 + 16 * math.sin(a)
            d.line([tx, y + h * 0.42, ex, ey], fill=(20, 12, 35), width=3)
    # OUT TODAY badge
    bw = 74
    d.rectangle([x + 8, y + 8, x + 8 + bw, y + 24], fill=GOLD)
    d.text((x + 13, y + 10), "OUT TODAY", font=font(F_SANS_B, 10),
           fill=(20, 20, 20))


def scene_ipo(d, x, y, w, h):
    """A dark trading board: candlesticks climbing, a gold trend line,
    ANT $83 in the corner. (No NASDAQ label — the kicker says it, and
    the rising candles would collide with it.)"""
    d.rectangle([x, y, x + w, y + h], fill=(12, 42, 28))
    d.text((x + 8, y + 6), "ANT  $83", font=font(F_SANS_B, 15),
           fill=(255, 255, 255))
    # candlesticks, rising left to right; tops kept below 0.34 so the
    # label row stays clear
    base = y + h * 0.88
    tops = [0.64, 0.60, 0.68, 0.52, 0.56, 0.44, 0.48, 0.36, 0.34, 0.34]
    cw = w / len(tops)
    for i, t in enumerate(tops):
        cx = x + cw * (i + 0.5)
        top = y + h * t
        col = (60, 200, 110) if i % 3 else (220, 70, 60)
        d.line([cx, top - 6, cx, base], fill=col, width=2)
        d.rectangle([cx - 5, top, cx + 5, base - h * 0.06], fill=col)
    # gold trend line over the tops
    pts = []
    for i, t in enumerate(tops):
        pts.append((x + cw * (i + 0.5), y + h * t - 4))
    d.line(pts, fill=GOLD, width=3, joint="curve")
    # arrowhead at the end
    ex, ey = pts[-1]
    d.polygon([(ex, ey - 8), (ex + 10, ey + 2), (ex - 2, ey + 6)],
              fill=GOLD)


def scene_icj(d, x, y, w, h):
    """The Peace Palace in miniature: a blue sky band, darker stone,
    a pediment, four columns, steps. The building must read at a
    glance — pale-on-pale washes out at thumbnail size."""
    d.rectangle([x, y, x + w, y + h], fill=(150, 180, 205))
    d.rectangle([x, y + h * 0.78, x + w, y + h], fill=(110, 100, 80))
    bx, by, bw = x + w * 0.12, y + h * 0.30, w * 0.76
    # pediment
    d.polygon([(bx, by + h * 0.12), (bx + bw / 2, by - h * 0.12),
               (bx + bw, by + h * 0.12)], fill=(60, 52, 40))
    d.rectangle([bx, by + h * 0.12, bx + bw, by + h * 0.16],
                fill=(60, 52, 40))
    # columns — white with a dark outline so they stand off the stone
    for i in range(4):
        cx = bx + w * 0.08 + i * (bw - w * 0.16) / 3
        d.rectangle([cx - 4, by + h * 0.16, cx + 4, by + h * 0.48],
                    fill=(245, 240, 225), outline=(70, 60, 45))
    # door + steps
    d.rectangle([x + w * 0.46, by + h * 0.34, x + w * 0.54, by + h * 0.48],
                fill=(50, 40, 30))
    for i in range(3):
        d.rectangle([x + w * 0.10, y + h * (0.78 - i * 0.04),
                     x + w * 0.90, y + h * (0.82 - i * 0.04)],
                    fill=(140, 130, 108))


def scene_gaza(d, x, y, w, h):
    """Sand, a dashed yellow ceasefire line, a tank crossing it,
    a thin smoke column."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 200, 150))
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(190, 165, 110))
    # smoke, right
    for cx, cy, r in [(0.82, 0.30, 7), (0.84, 0.20, 6), (0.86, 0.12, 5)]:
        d.ellipse([x + w * cx - r, y + h * cy - r,
                   x + w * cx + r, y + h * cy + r], fill=(140, 130, 115))
    # the Yellow Line: dashed, horizontal
    for i in range(10):
        sx = x + w * i / 10
        d.line([sx + 2, y + h * 0.62, sx + w / 10 - 2, y + h * 0.62],
               fill=(255, 220, 0), width=4)
    d.text((x + 8, y + 6), "YELLOW LINE", font=font(F_SANS_B, 10),
           fill=(120, 90, 20))
    # tank, crossing the line, left of centre
    tx, ty = x + w * 0.34, y + h * 0.52
    d.rectangle([tx - 22, ty, tx + 22, ty + 12], fill=(60, 60, 55))
    d.rectangle([tx - 10, ty - 9, tx + 12, ty], fill=(60, 60, 55))
    d.line([tx + 12, ty - 5, tx + 30, ty - 8], fill=(60, 60, 55), width=4)
    for wx in (-18, -6, 6, 18):
        d.ellipse([tx + wx - 4, ty + 12, tx + wx + 4, ty + 20],
                  fill=(40, 40, 35))


def scene_akvan(d, x, y, w, h):
    """A cyclone spiral over the sea, a coastline on the right,
    a red RED ALERT tag."""
    d.rectangle([x, y, x + w, y + h], fill=(178, 208, 224))
    cx, cy = x + w * 0.36, y + h * 0.52
    for r in range(22, 3, -3):
        d.arc([cx - r, cy - r, cx + r, cy + r], r * 30, r * 30 + 210,
              fill=(31, 58, 95), width=3)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(31, 58, 95))
    # coastline, right
    d.polygon([(x + w * 0.78, y), (x + w, y), (x + w, y + h),
               (x + w * 0.86, y + h), (x + w * 0.80, y + h * 0.55)],
              fill=(222, 200, 150))
    # sea lines, bottom
    for wy in (0.80, 0.90):
        pts = []
        for i in range(7):
            pts.append((x + w * i / 6,
                        y + h * wy + (3 if i % 2 else -3)))
        d.line(pts, fill=(230, 242, 250), width=2)
    # RED ALERT tag
    d.rectangle([x + w - 62, y + 6, x + w - 6, y + 22], fill=RED)
    d.text((x + w - 57, y + 8), "RED ALERT", font=font(F_SANS_B, 10),
           fill=(255, 255, 255))


def scene_cop31(d, x, y, w, h):
    """Antalya hills under a big sun; a white chip carries the $120bn
    figure the talks are stuck on."""
    d.rectangle([x, y, x + w, y + h], fill=(150, 200, 220))
    d.ellipse([x + w * 0.78, y + h * 0.08, x + w * 0.78 + 20,
               y + h * 0.08 + 20], fill=(255, 210, 80))
    for cx, cy in [(0.18, 0.16), (0.50, 0.10)]:
        d.ellipse([x + w * cx - 14, y + h * cy - 5,
                   x + w * cx + 14, y + h * cy + 5], fill=(255, 255, 255))
    # hills
    d.polygon([(x, y + h), (x, y + h * 0.62), (x + w * 0.35, y + h * 0.48),
               (x + w * 0.60, y + h * 0.66), (x + w, y + h * 0.55),
               (x + w, y + h)], fill=(90, 160, 110))
    d.polygon([(x, y + h), (x, y + h * 0.78), (x + w * 0.45, y + h * 0.68),
               (x + w, y + h * 0.80), (x + w, y + h)], fill=(50, 120, 80))
    # white chip: the unresolved figure
    d.rectangle([x + 8, y + h - 26, x + 92, y + h - 8], fill=(255, 255, 255))
    d.text((x + 13, y + h - 23), "$120bn", font=font(F_SANS_B, 12),
           fill=NAVY)
    d.text((x + 98, y + h - 21), "ANTALYA", font=font(F_SANS_B, 10),
           fill=(255, 255, 255))


def scene_suneung(d, x, y, w, h):
    """An exam hall from above the back row: a wall clock, rows of
    desks with bowed heads. Tuned for the 30px medium strip — heads
    and desks stay inside it. (No SUNEUNG label: the kicker and the
    headline already say it, and the label collided with the heads.)"""
    d.rectangle([x, y, x + w, y + h], fill=(235, 228, 210))
    # wall clock, top right
    cx, cy = x + w * 0.86, y + h * 0.26
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 255, 255),
              outline=INK, width=2)
    d.line([cx, cy, cx, cy - 5], fill=INK, width=2)
    d.line([cx, cy, cx + 4, cy + 2], fill=INK, width=2)
    # three rows of desks with heads
    for r in range(3):
        ry = y + h * (0.38 + r * 0.20)
        for c in range(5):
            dx = x + w * (0.10 + c * 0.18)
            d.ellipse([dx - 6, ry - 12, dx + 6, ry - 2], fill=(230, 200, 160))
            d.pieslice([dx - 6, ry - 12, dx + 6, ry - 2], 180, 360,
                       fill=(40, 40, 40))
            d.rectangle([dx - 12, ry, dx + 12, ry + 7], fill=(160, 120, 80))
            d.rectangle([dx - 12, ry, dx + 12, ry + 2], fill=(190, 150, 105))


def scene_florida(d, x, y, w, h):
    """Rain over a flooded street: two houses half under water,
    a street sign, a 15.3 IN tag."""
    d.rectangle([x, y, x + w, y + h], fill=(140, 160, 175))
    # rain, diagonal strokes
    for i in range(14):
        rx = x + w * (0.04 + 0.07 * i)
        ry = y + h * (0.06 + 0.05 * (i % 3))
        d.line([rx, ry, rx - 3, ry + 10], fill=(220, 230, 240), width=2)
    # houses, half-submerged
    for hx, hw in [(0.08, 0.34), (0.54, 0.36)]:
        d.rectangle([x + w * hx, y + h * 0.42, x + w * (hx + hw),
                     y + h * 0.72], fill=(240, 235, 220))
        d.polygon([(x + w * hx - 0.02 * w, y + h * 0.42),
                   (x + w * (hx + hw / 2), y + h * 0.28),
                   (x + w * (hx + hw + 0.02), y + h * 0.42)],
                  fill=(150, 60, 50))
        d.rectangle([x + w * (hx + hw * 0.42), y + h * 0.58,
                     x + w * (hx + hw * 0.58), y + h * 0.72], fill=(60, 50, 40))
    # flood water
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(90, 130, 160))
    for wy in (0.80, 0.90):
        pts = []
        for i in range(9):
            pts.append((x + w * i / 8,
                        y + h * wy + (3 if i % 2 else -3)))
        d.line(pts, fill=(190, 220, 240), width=2)
    # 15.3 IN tag
    d.rectangle([x + w - 58, y + 6, x + w - 6, y + 22], fill=NAVY)
    d.text((x + w - 53, y + 8), "15.3 IN", font=font(F_SANS_B, 10),
           fill=(255, 255, 255))


def scene_jobs(d, x, y, w, h):
    """Four falling bars and a red arrow: the jobs number, 4.9%."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    d.text((x + 8, y + 5), "4.9%", font=font(F_SANS_B, 16), fill=RED)
    # bars, descending left to right (no OCTOBER label: the bars would
    # cross it, and the kicker already says CANBERRA · ECONOMY)
    heights = [0.55, 0.48, 0.40, 0.30]
    for i, bh in enumerate(heights):
        bx = x + w * (0.42 + i * 0.13)
        d.rectangle([bx, y + h * (0.85 - bh), bx + w * 0.09, y + h * 0.85],
                    fill=RED)
    d.line([x + w * 0.40, y + h * 0.30, x + w * 0.94, y + h * 0.62],
           fill=RED, width=3)
    d.polygon([(x + w * 0.94, y + h * 0.62), (x + w * 0.86, y + h * 0.56),
               (x + w * 0.88, y + h * 0.70)], fill=RED)
    d.line([x + 8, y + h * 0.85, x + w - 8, y + h * 0.85], fill=INK, width=2)


def scene_gulf(d, x, y, w, h):
    """Night over the Gulf: stars, a gold missile trail arcing down,
    an orange interception burst, RIYADH below."""
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
    for sx, sy, r in [(0.10, 0.16, 1), (0.30, 0.10, 2), (0.55, 0.14, 1),
                      (0.75, 0.10, 1), (0.92, 0.22, 2), (0.20, 0.30, 1),
                      (0.65, 0.28, 1)]:
        d.ellipse([x + w * sx - r, y + h * sy - r,
                   x + w * sx + r, y + h * sy + r], fill=(200, 210, 225))
    # missile trail, arcing from upper right down to the burst
    pts = []
    for i in range(11):
        t = i / 10
        px = x + w * (0.88 - 0.42 * t)
        py = y + h * (0.10 + 0.42 * t * t)
        pts.append((px, py))
    d.line(pts, fill=GOLD, width=3, joint="curve")
    # interception burst
    bx, by = x + w * 0.46, y + h * 0.52
    star = []
    for i in range(12):
        ang = math.pi * i / 6
        rr = 11 if i % 2 == 0 else 5
        star.append((bx + rr * math.cos(ang), by + rr * math.sin(ang)))
    d.polygon(star, fill=(232, 106, 31))
    d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(255, 220, 120))
    # skyline, bottom
    for bx2, bw, bh in [(0.06, 0.10, 0.18), (0.18, 0.08, 0.26),
                        (0.70, 0.12, 0.22), (0.84, 0.10, 0.16)]:
        d.rectangle([x + w * bx2, y + h - h * bh,
                     x + w * (bx2 + bw), y + h], fill=(5, 15, 35))
    d.text((x + 8, y + 6), "RIYADH", font=font(F_SANS_B, 10),
           fill=(220, 228, 240))


SCENES = {"summit": scene_summit, "bridge": scene_bridge, "gta": scene_gta,
          "ipo": scene_ipo, "icj": scene_icj, "gaza": scene_gaza,
          "akvan": scene_akvan, "cop31": scene_cop31,
          "suneung": scene_suneung, "florida": scene_florida,
          "jobs": scene_jobs, "gulf": scene_gulf}


# ---------------------------------------------------------------------------
# map (dotted halftone; continents as coarse lon/lat outlines)
# ---------------------------------------------------------------------------

CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-65, 60), (-55, 52), (-65, 45), (-75, 35), (-80, 26),
     (-84, 30), (-90, 21), (-97, 26), (-105, 20), (-110, 24), (-117, 33),
     (-125, 40), (-124, 48), (-135, 58), (-150, 60), (-165, 60)],
    [(-78, 7), (-77, 4), (-80, -3), (-81, -6), (-75, -15), (-70, -18),
     (-70, -23), (-65, -25), (-57, -30), (-48, -28), (-40, -20),
     (-35, -9), (-35, -6), (-44, -3), (-50, 0), (-60, 8), (-70, 11)],
    [(-10, 37), (-9, 43), (-2, 48), (-4, 50), (2, 51), (5, 53), (8, 57),
     (10, 59), (18, 56), (21, 55), (24, 58), (28, 59), (30, 60),
     (28, 62), (24, 65), (21, 70), (30, 70), (40, 68), (45, 68),
     (55, 69), (68, 73), (75, 73), (80, 73), (100, 77), (110, 74),
     (130, 72), (150, 70), (170, 67), (178, 65), (170, 60), (162, 60),
     (158, 53), (142, 50), (140, 45), (135, 43), (130, 38), (127, 35),
     (122, 30), (120, 22), (110, 20), (105, 10), (100, 8), (98, 12),
     (95, 16), (90, 22), (85, 20), (80, 15), (77, 8), (73, 20),
     (70, 25), (66, 25), (60, 25), (57, 26), (52, 26), (50, 30),
     (48, 30), (44, 29), (42, 15), (43, 12), (40, 15), (39, 21),
     (35, 29), (34, 31), (30, 36), (27, 37), (23, 36), (19, 42),
     (14, 45), (8, 44), (3, 42), (-1, 37)],
    [(12, 35), (10, 37), (20, 32), (30, 31), (32, 31), (35, 28),
     (37, 18), (43, 11), (48, 11), (51, 12), (44, 1), (40, -5),
     (39, -10), (36, -18), (33, -26), (28, -33), (20, -35), (17, -32),
     (14, -22), (12, -18), (12, -6), (9, 4), (6, 4), (-8, 4),
     (-13, 8), (-17, 15), (-16, 20), (-15, 27), (-10, 31), (-6, 33)],
    [(113, -22), (114, -30), (115, -35), (118, -35), (124, -33),
     (129, -32), (132, -32), (136, -35), (140, -38), (145, -38),
     (150, -37), (153, -32), (153, -27), (150, -22), (146, -19),
     (142, -11), (136, -12), (132, -11), (130, -13), (126, -14),
     (122, -17), (118, -20), (114, -22)],
]


def lonlat_to_xy(lon, lat, mx, my, mw, mh):
    return (mx + (lon + 180) / 360 * mw,
            my + (85 - lat) / 145 * mh)


def _inside(px, py, poly):
    """Ray-casting point-in-polygon (poly = list of (x, y))."""
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > py) != (y2 > py):
            xin = (x2 - x1) * (py - y1) / (y2 - y1) + x1
            if px < xin:
                inside = not inside
    return inside


def draw_map(d, mx, my, mw, mh, dots):
    d.rectangle([mx, my, mx + mw, my + mh], fill=MAP_OCEAN)
    polys = [[lonlat_to_xy(lon, lat, mx, my, mw, mh) for lon, lat in poly]
             for poly in CONTINENTS]
    step = 7
    for gx in range(mx + 4, mx + mw, step):
        for gy in range(my + 4, my + mh, step):
            if any(_inside(gx, gy, p) for p in polys):
                d.ellipse([gx - 1.7, gy - 1.7, gx + 1.7, gy + 1.7],
                          fill=MAP_DOT)
    d.rectangle([mx, my, mx + mw, my + mh], outline=(120, 120, 110), width=1)
    fnum = font(F_SANS_B, 9)
    for num, (lon, lat) in dots.items():
        x, y = lonlat_to_xy(lon, lat, mx, my, mw, mh)
        rx = 12 if len(num) > 2 else 6.5
        d.ellipse([x - rx, y - 6.5, x + rx, y + 6.5], fill=RED,
                  outline=(255, 255, 255), width=1)
        tw = d.textlength(num, font=fnum)
        d.text((x - tw / 2, y - 4.5), num, font=fnum, fill=(255, 255, 255))


# ---------------------------------------------------------------------------
# build
# ---------------------------------------------------------------------------

def _num_disc(d, cx, cy, r, num, fill):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill,
              outline=(255, 255, 255), width=1)
    f = font(F_SANS_B, 11)
    tw = d.textlength(num, font=f)
    d.text((cx - tw / 2, cy - 5.5), num, font=f, fill=(255, 255, 255))


def build():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    y = 10

    # --- top band + thick rule (after the leaders' mastheads)
    fk = font(F_SANS_B, 13)
    d.text((M, y), "THE WORLD IN ONE DAY", font=fk, fill=RED)
    right = "THURSDAY'S NEWS · ONE PAGE · 40 STORIES"
    d.text((W - M - d.textlength(right, font=fk), y), right, font=fk,
           fill=INK)
    y += 18
    d.rectangle([M, y, W - M, y + 3], fill=INK)
    y += 8

    # --- masthead: huge dark serif date
    title = "Thursday 19 November 2026"
    fm = fit_font(F_DISP_BLACK, title, CW, 54)
    d.text((M, y), title, font=fm, fill=INK)
    y += 58
    # --- strapline: italic red serif, the three leads in one line
    fs = font(F_SERIF_IT, 17)
    d.text((M, y), "Three leaders meet in Shenzhen · The Bridge is hit a "
                   "third time · GTA VI finally arrives",
           font=fs, fill=RED)
    y += 22
    d.line([M, y, W - M, y], fill=HAIR, width=1)
    y += 6

    # --- region bar: widths proportional to story counts, floored so
    #     the smallest label still fits its segment
    total = sum(c for _, c, _ in REGIONS)
    widths = [max(int(CW * c / total), 60) for _, c, _ in REGIONS]
    excess = sum(widths) - CW
    if excess > 0:
        big = widths.index(max(widths))
        widths[big] -= excess
    rx = M
    fr = font(F_SANS_B, 11)
    for (name, count, col), seg in zip(REGIONS, widths):
        d.rectangle([rx, y, rx + seg - 1, y + 19], fill=col)
        label = f"{name} {count}"
        tw = d.textlength(label, font=fr)
        d.text((rx + (seg - tw) / 2, y + 3), label, font=fr,
               fill=(255, 255, 255))
        rx += seg
    y += 19 + 6

    # --- BY THE NUMBERS: six verified figures from stories on the page
    sw = (CW - 5 * 8) // 6
    fs_n = font(F_SANS_B, 17)
    fs_l = font(F_SANS, 10)
    for i, (num, lab) in enumerate(NUMBERS):
        bx = M + i * (sw + 8)
        d.rectangle([bx, y, bx + sw, y + 44], fill=(255, 255, 255),
                    outline=NAVY, width=1)
        d.text((bx + 8, y + 4), num, font=fs_n, fill=NAVY)
        draw_wrapped(d, bx + 8, y + 25, lab, fs_l, INK, sw - 16,
                     leading=11, max_lines=2)
    y += 44 + 6

    # --- three equal leads
    lead_w = (CW - 2 * 16) // 3
    panel_h = 104
    lead_bottom = 0
    for i, (kick, col, scene, head, summ) in enumerate(LEADS):
        x = M + i * (lead_w + 16)
        SCENES[scene](d, x, y, lead_w, panel_h)
        _num_disc(d, x + 13, y + panel_h + 15, 11, str(i + 1), col)
        d.text((x + 30, y + panel_h + 9), kick,
               font=font(F_SANS_B, 12), fill=col)
        fh = font(F_DISP_BOLD, 19)
        hy = draw_wrapped(d, x, y + panel_h + 31, head, fh, INK, lead_w,
                          leading=21, max_lines=2)
        sy = draw_wrapped(d, x, hy + 3, summ, font(F_SANS, 12), INK,
                          lead_w, leading=13, max_lines=2)
        lead_bottom = max(lead_bottom, sy)
    y = lead_bottom + 6
    d.line([M, y, W - M, y], fill=HAIR, width=1)
    y += 6

    # --- the day in brief: 3x3 cards, scene strip on top
    fh_b = font(F_SANS_B, 14)
    d.text((M, y), "THE DAY IN BRIEF", font=fh_b, fill=RED)
    d.text((W - M - d.textlength("STORIES 04–12", font=fr), y + 2),
           "STORIES 04–12", font=fr, fill=GREY)
    y += 18
    card_w = lead_w
    card_h = 106
    for idx, (kick, col, scene, head, summ) in enumerate(MEDIUMS):
        r, c = divmod(idx, 3)
        x = M + c * (card_w + 16)
        cy = y + r * (card_h + 6)
        d.rectangle([x, cy, x + card_w, cy + card_h],
                    fill=(255, 255, 255), outline=(200, 192, 170), width=1)
        SCENES[scene](d, x + 1, cy + 1, card_w - 2, 30)
        _num_disc(d, x + card_w - 18, cy + 46, 10, str(idx + 4), col)
        tx = x + 10
        tw = card_w - 20 - 26
        d.text((tx, cy + 35), kick, font=font(F_SANS_B, 10), fill=col)
        hy = draw_wrapped(d, tx, cy + 48, head, font(F_SANS_B, 13), INK,
                          tw, leading=14, max_lines=2)
        draw_wrapped(d, tx, hy + 2, summ, font(F_SANS, 11), INK, tw,
                     leading=11, max_lines=2)
    y += 3 * card_h + 2 * 6 + 6
    d.line([M, y, W - M, y], fill=HAIR, width=1)
    y += 6

    # --- footer band: dotted map + ALSO list
    d.text((M, y), "WHERE IT HAPPENED", font=fh_b, fill=RED)
    map_w = 380
    ax = M + map_w + 20
    d.text((ax, y), "ALSO ON THURSDAY 19 NOVEMBER — 28 MORE STORIES",
           font=fh_b, fill=RED)
    y += 16
    # dot positions are schematic where stories crowd (Gulf, Europe)
    dots = {"1": (114.1, 22.5), "2": (38.5, 46.5), "3": (174.8, -36.8),
            "4": (-74.0, 40.7), "5": (4.3, 52.1), "6": (37.0, 29.5),
            "7": (85.8, 19.8), "8": (28.5, 38.5), "9": (127.0, 37.5),
            "10": (-80.2, 26.1), "11": (149.1, -35.3), "12": (48.0, 23.5)}
    draw_map(d, M, y, map_w, 144, dots)
    d.text((M, y + 148),
           "Red numbers mark stories 1–12; positions are approximate.",
           font=font(F_SANS, 10), fill=GREY)

    acol_w = (W - M - ax - 4) // 3
    fa = font(F_SANS, 9)
    fa_b = font(F_SANS_B, 9)
    for i, item in enumerate(ALSO):
        c, r = divmod(i, 10)
        x = ax + c * (acol_w + 4)
        yy = y + r * 14
        num = str(i + 13)
        d.text((x, yy), num, font=fa_b, fill=RED)
        text = item
        while (d.textlength(text, font=fa) > acol_w - 20
               and len(text) > 8):
            text = text[:-2]
        if text != item:
            text = text[:-1] + "…"
        d.text((x + 18, yy), text, font=fa, fill=INK)
    y += 144 + 18

    # --- DATE CHECK box (what was left off, and why)
    d.rectangle([M, y, W - M, y + 30], outline=RED, width=1)
    fj = font(F_SANS_B, 10)
    draw_wrapped(d, M + 8, y + 3, DATE_CHECK, fj, RED, CW - 16,
                 leading=12, max_lines=2)
    y += 30 + 4

    # --- sources footer (wrapped, two lines)
    ff = font(F_SANS, 10)
    y = draw_wrapped(d, M, y, FOOTER, ff, GREY, CW, leading=13,
                     max_lines=2)
    y += 2
    print("final y =", y, "(canvas 1024)")
    return im


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    im = build()
    im.save(out, "PNG", optimize=True)
    print(out, im.size)
