# 19 November 2026 — World News in One Image

[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/ramabram46-png/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/ramabram46-png/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

A newspaper front page summing up Thursday 19 November 2026 in a single
1024×1024 image: 40 stories across 6 regions, with a dotted world map
marking where each featured story happened.

## The image

Built under the "The World in One Day" philosophy (`design-philosophy.md`):
cream paper, a huge dark serif date, a red strapline naming the three leads,
a coloured region bar, a BY THE NUMBERS strip, three EQUAL leads (never one
hero taking 60%+ of the page), nine medium stories as numbered cards
(04–12), a dotted world map with numbered dots, a 28-item "Also on Thursday
19 November" list, and a DATE CHECK box naming the big stories that were
left off because they broke before Thursday.

- **3 lead stories:** the first Trump–Xi–Putin three-way summit in Shenzhen;
  the Crimean Bridge attacked a third time in three days; GTA VI arrives
  after a 13-year wait.
- **9 medium stories:** Anthropic's record $81.3bn IPO starts trading as ANT;
  the World Court rules on Myanmar's Rohingya case; Israeli tanks cross
  Gaza's Yellow Line; Cyclone Akvan bears down on India's coast; COP31 enters
  its final 48 hours; half a million sit Korea's Suneung exam; flooded
  Broward braces for more rain; Australia's jobless rate hits a five-year
  high; a Riyadh missile is downed as the Gulf war widens.
- **28 more** in the "Also on Thursday 19 November" list, plus a map with
  numbered dots for stories 1–12.

Every featured story was checked against at least two independent news
sources (Reuters, AP, BBC, Al Jazeera, USA Today, IAEA, IMD, ABS and others)
on 19 November 2026 — see `research-19-nov-2026.md` for the sources and why
these leads. All illustrations are flat vector art drawn in code; no
AI-generated imagery, so no garbled text and no fake photos.

## How it is built

`draw_poster.py` (Python 3, Pillow, Noto fonts) draws `entry.png`
deterministically from the story list in the script. `main.ts` (Node 22,
standard library only) copies the embedded `entry.png` byte-for-byte to
`/output/entry.png` — no network, no randomness, no timestamps, so repeated
runs produce identical bytes.

```sh
python3 draw_poster.py entry.png   # regenerate the poster
node main.ts                       # write /output/entry.png
```

## Licence

MIT — see `LICENSE`.
