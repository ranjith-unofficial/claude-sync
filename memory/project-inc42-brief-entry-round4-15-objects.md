---
name: project-inc42-brief-entry-round4-15-objects
description: Brief entry round 4 (6 Sep 2026, late) — fifteen non-list visual objects (orbit, bento, bubbles, treemap, radar, ring, clock, skyline, bookshelf, corkboard, stamps, coverflow, mosaic, type scale, card box) with real feature images, in the real screen; unreviewed
metadata:
  type: project
---

**Built Sun 6 Sep 2026 (afternoon/evening)** on page Referencing (476:2) of draft file
`dAsaTgNj0xh25w2OGaurZo`, rows at y=12400 / 13900 / 15400, header note y=12180. Round 3
(lists, y=7900+) stays on the canvas, rejected. Doc + links: `~/ClaudeDocs/inc42/BRIEF-15-STRUCTURES.md`
(round 4 section at the bottom).

**Why:** Ranjith rejected round 3 as "I don't like this list format … very poor … never ever give me
this design … everything is a list … I cannot show the entire list … think of some as a design itself."
Only the graph (round 3 #06) "somehow" worked. Satya's folder is "much better" structurally but he is
not convinced by it either.

**The fifteen (node ids):** V01 Orbit 607:2 · V02 Bento 593:2 · V03 Bubbles 594:2 · V04 Treemap 599:2 ·
V05 Radar 596:2 · V06 Ring 608:2 · V07 Clock 609:2 · V08 Skyline 602:2 · V09 Bookshelf 603:2 ·
V10 Corkboard 604:2 · V11 Stamp sheet 610:2 · V12 Coverflow 611:2 · V13 Mosaic 612:2 ·
V14 Type scale 612:97 · V15 Card box 613:2. Same shell as round 3 (real greeting header + nav),
same Fri 4 Sep eight, sizes from impact.json where the object is "sized by importance".

**Images:** og:image of each of the 8 articles fetched with curl from inc42.com (scratchpad `img/`),
placed via `upload_assets` with `nodeIds` (24 slots, all 200). Ellipse nodes take image fills fine.
Precedents pulled from Mobbin: Finimize Daily Brief hero, Binance treemap, Acorns ring, corner tiles.

**Build lessons:** rotated text (`rotation=-90`, x = w/2-8, y = top) works for spines/narrow cells;
`arcData` ring segments and `dashPattern` perforations both fine; labels on radial objects need
side-aware placement (|cos|>0.85 → short width, small font) or they clip at the card edge — cost 3
rebuilds (orbit, ring, clock). Keep every card ≤ ~600px so the footer clears the nav at y=760.

**Status:** unreviewed. Recommendation given: V13 Mosaic / V02 Bento need no new field; V01 is the
graph with weight; V03/V04 need the impact score in prod.
Related: [[project-inc42-brief-entry-round3-15-structures]], [[feedback-design-review-ranjith]],
[[reference-figma-mcp-build-techniques]].
