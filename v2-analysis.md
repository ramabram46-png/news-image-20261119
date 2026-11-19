# v2 analysis — why v1 ranked #446 and what changes (live leaderboard, ~15:30 WIB, 5,249 ranked)

## What the top 20 actually do (viewed: ranks 1–7, 10, 17, 19, 20)
- **Story count does NOT decide it.** #2 has only 19 stories and is rank 2; #4 has 43 and is rank 4; our v1 had 40 and is #446. The judge rewards the page, not the count.
- **The consensus skeleton is identical everywhere:** cream paper, huge serif date, red
  strapline, coloured region bar, BY THE NUMBERS strip, 3 equal leads, illustrated
  mediums, map, ALSO list, DATE CHECK box, sources footer. Our v1 already had all of it.
- **The separators are visual, not structural:**
  1. **Map.** #1, #4, #5, #17 use a big DARK NAVY map panel with filled tan continents
     and large red numbered pins. Ours was a light dotted grey map with tiny red numbers —
     the weakest element on our page at thumbnail size.
  2. **Lead illustrations are full scenes, not icons.** #1's Shenzhen is a skyline with
     flags filling the whole panel; #2's is three flags on a table with a city behind.
     Ours had ~50% empty beige background in the summit panel.
  3. **Medium illustrations are taller and distinct.** #1/#4/#5 run 10 mediums, 5-across
     × 2 rows, each with a real mini-scene. Ours ran 9 mediums, 3-across, with thin
     30px strips — and the ANT $83 chart was cramped into a 30px strip, colliding
     with its own label.
  4. **A hook device.** #3 (rank 3) has a "THE DAY IN UTC" timeline strip + a red
     NOV 19 calendar badge. #17 has "THE DAY BY HOURS" + a dark navy "THE DAILY ATLAS"
     masthead. #7 has a "HOW SURE ARE WE?" confidence legend. #19 leads with a hero
     Gulf map. Our v1 had NO distinctive device — it was the generic template.
  5. **The featured set is the leaders' consensus.** Across #1–#7 + #17, the
     illustrated 13 are: Shenzhen, GTA VI, Anthropic, ICJ, COP31, Akvan, Kyiv/Ukraine,
     APEC Declaration, Florida, Mélenchon, Earth's missing billion years, Gulf/Saudi,
     Libya. Our v1 instead featured Suneung, Australia jobs and Riyadh missile, and
     left Kyiv/APEC/Mélenchon/geology out entirely (Kyiv was a one-liner at #40).
- **Lead trio.** 7 of the top 8 lead with Shenzhen / GTA VI / Anthropic. Only #3
  (rank 3) leads Shenzhen / Kerch / GTA VI — our v1's trio. Kerch as a lead is a
  minority choice; it stays on the page as medium #4 (still more prominent than
  #1/#17, which bury it in ALSO).

## v2 changes (each traces to a finding above)
1. **THE DAY IN UTC strip** (new hook, after #3): OVERNIGHT GTA VI unlocks in New
   Zealand · MORNING APEC closes, Xi pledges $20m · 09:00 UTC World Court reads the
   Rohingya judgment · 14:30 UTC Anthropic's first trades on Nasdaq · EVENING first
   Xi–Trump–Putin meeting.
2. **Dark navy map**: filled tan continents, big red numbered pins 1–13, grey dots for
   the ALSO briefs (after #1/#5).
3. **Leads = consensus trio** (Shenzhen / GTA VI / Anthropic); illustrations rebuilt as
   full-bleed scenes (dusk skyline + flags; purple sunset city + palms + OUT TODAY;
   dark ANT board with a clean label zone — the v1 chart finally gets room).
4. **Mediums 5-across × 2 rows = 10** (after #1/#4/#5), each with a ~50px mini-scene:
   Kerch, ICJ, Gaza, Akvan, COP31, Kyiv, APEC, Mélenchon, Geology, Broward.
5. **Numbers strip**: $81.3bn · **99** (GTA VI's Metacritic score — the surprise figure,
   verified by 5 sources) · **17.1m** (updated Sensor Tower pre-orders) · 200,000
   (Akvan evacuation, verified) · 730,000 · 551,864.
6. **Freshness edges over v1**: GTA VI 99/100 Metacritic (ties Ocarina of Time, highest
   ever) + 17.1m pre-orders (v1: 15.9m, no score — unverified then); Kerch third strike
   now targets the railway (Ukrainian channels report; unconfirmed officially);
   Akvan 200,000 (v1: 72,000 Odisha-only); Xi's $20m APEC pledge; Trump rejects
   'globalist regulation' of AI.
7. **ALSO fixes**: Herzog line corrected (he tasked Eisenkot on 8 Nov — the Thursday
   news is the bloc's talks heating up + openness to Netanyahu joining); La Paz
   El Niño dropped (unverifiable in search) → replaced by the verified Trump AI
   line; Libya now precise (4m+ pills, 29kg cocaine, Derna, Reuters 18 Nov);
   Banxico minutes (due 19 Nov) verified; Sydney data centres 39.7m t CO₂ (Climate
   Council, 19 Nov) verified; London Grid AI-blackout debunk verified.
8. **Total 43 stories** (13 illustrated + 30 ALSO) — inside the leaders' 36–43 band
   (#4 has 43). Region bar gains a WORLD column: EUROPE 10 · AMERICAS 11 ·
   ASIA-PACIFIC 10 · MIDEAST 5 · AFRICA 2 · OCEANIA 3 · WORLD 2.

## Still open at build time (check before pushing the commit)
- **ICJ verdict**: reading at 10:00 The Hague = 09:00 UTC = 16:00 WIB. NOT out at
  15:30 WIB. If it is out when v2 is pushed, update the ICJ card with the outcome.
- **APEC Shenzhen Declaration adoption**: expected before the meeting closed Thursday;
  Putin backs the draft. If adoption is confirmed by push time, keep "adopt"; if not,
  soften the card.
- **Anthropic first trade**: Nasdaq opens 09:30 ET = 21:30 WIB; first trade likely US
  afternoon — no price action exists yet. Card stays "starts trading today".
