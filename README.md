# 19 November 2026 — World News in One Image

[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/ramabram46-png/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/ramabram46-png/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

A newspaper front page summing up Thursday 19 November 2026 in a single
1024×1024 image: 43 stories across 7 regions, with a dark-navy world map
marking where each featured story happened and a THE DAY IN UTC strip
telling the day as it unfolded.

## The image

Built under the "The World in One Day" philosophy (`design-philosophy.md`):
cream paper, a huge dark serif date, a red strapline naming the three leads,
a THE DAY IN UTC timeline strip, a coloured region bar, a BY THE NUMBERS
strip, three EQUAL leads (never one hero taking 60%+ of the page), ten
medium stories as numbered cards (04–13), a dark-navy world map with red
numbered pins, a 30-item "Also on Thursday 19 November" list, and a DATE
CHECK box naming the big stories that were left off because they broke
before Thursday.

- **3 lead stories:** the first Trump–Xi–Putin three-way summit in Shenzhen;
  GTA VI scores 99 on Metacritic — the joint-highest ever; Anthropic debuts
  in the biggest IPO on record ($83, $81.3bn raised).
- **10 medium stories:** the Crimean Bridge hit a third time — now the
  railway; the World Court rules on Myanmar's Rohingya case; Israeli tanks
  cross Gaza's Yellow Line; Cyclone Akvan bears down on India's coast with
  200,000 facing evacuation; COP31 enters its final 48 hours; Ukraine
  watches Shenzhen from the sidelines; APEC set to adopt the Shenzhen
  Declaration; Mélenchon could win, says France's justice minister; Earth's
  missing billion years are explained; flooded Broward braces for more rain.
- **30 more** in the "Also on Thursday 19 November" list, plus a map with
  red numbered pins for stories 1–13 and grey dots for the briefs.

Every featured story was checked against at least two independent news
sources (Reuters, AP, BBC, Al Jazeera, Nature, Sensor Tower, Metacritic,
IAEA, IMD and others) on 19 November 2026 — see
`research-19-nov-2026.md` for the sources and why these leads. All
illustrations are flat vector art drawn in code; no AI-generated imagery,
so no garbled text and no fake photos.

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
