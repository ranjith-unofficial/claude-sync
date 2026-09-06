---
name: project-inc42-brief-entry-round3-15-structures
description: Brief entry round 3 (6 Sep 2026) — fifteen structurally different objects, each inside the real Brief page (greeting header + nav), Fri 4 Sep brief; on Referencing page y=7900+; unreviewed
metadata:
  type: project
---

**Built Sun 6 Sep 2026** on page **Referencing (476:2)** of draft file `dAsaTgNj0xh25w2OGaurZo`,
rows at y=7900 / 9400 / 10900 (x=100…2100 step 500), header note at y=7680, a note under every
screen at y+900. Rounds 1 and 2 above it were left untouched (48 nodes verified before build).
Doc with per-screen links: `~/ClaudeDocs/inc42/BRIEF-15-STRUCTURES.md`.

**Why this round:** Ranjith rejected round 2 as "when I say use different style types, you're
coming with the same design", pointed at Satya's folder round (Inc42-App-2026 file, section 88
`5177:5306`, plus 86 issue/band and 87 folder variants) as "making a lot of sense", but said
"I would not want you to come back with the same folder structure … the structure itself to be
15 different", and to put them in the actual "Hello / How are you" screen — i.e. the live Brief
page with the **Good morning, <name>** orange header (dev frame `4858:27193` in Satya's file).

**The fifteen (node ids):** 01 Sorted by follows 572:5 · 02 Inbox 578:2 · 03 Checklist 579:2 ·
04 Questions 580:2 · 05 Memo 576:2 · 06 Graph 577:2 · 07 Route 581:2 · 08 Cover 582:2 ·
09 Table 583:2 · 10 Changelog 584:2 · 11 Watchlist first 586:2 · 12 Threads 587:2 ·
13 DataLabs card 588:2 · 14 Tiers 589:2 · 15 Filter→matrix 590:2.

**Data:** real Fri 4 Sep brief (23 published 3 Sep 07:00→4 Sep 07:00, `articles_90d.csv`);
eight chosen for follows Fintech · Ecommerce & D2C · Deals · IPO, tracks Meesho + Zerodha:
slice $100 Mn at 60% cut, RentoMojo RHP, Ultrahuman $70 Mn, Meesho ₹1,650 Cr SoftBank sale,
Cradlewise $12 Mn, Zerodha SEBI nod, Cars24 FY26, BYJU'S NCLT. "LAST" lines on 12 are real
prior stories (slice 24 Aug board, RentoMojo 6 Jul SEBI nod, Meesho 24 Aug YC ₹970 Cr,
Zerodha 26 Aug FY26, BYJU'S 2 Sep Aakash/Qatar). Tiers on 14 use impact.json scores.

**Needs new fields:** 04 question rewrite; 12 previous-appearance per company; 14 impact score
in prod ranking; 13 company stage + DataLabs slug. Everything else = layout on existing fields.

**Recommendation given (unreviewed):** 15 for "built for me", 10 for "what will I get",
04 for FOMO without giving the brief away.

**Build notes:** one `use_figma` call per screen with the shell helper (SCREEN/NAV/FOOT/CTA/NOTE),
Urbanist + Inter + JetBrains Mono + Fraunces; page-level `children.length` is 0 until the page is
loaded with `setCurrentPageAsync` — always load before trusting counts. 4 of 15 needed a
collision fix after screenshot (overflow under the nav is the common failure: keep card ≤ ~620px).
Related: [[project-inc42-brief-entry-round2-15-uis]], [[feedback-design-review-ranjith]],
[[reference-figma-mcp-build-techniques]].
