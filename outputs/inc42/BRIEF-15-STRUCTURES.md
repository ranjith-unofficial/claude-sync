# Brief entry — 15 structures, in the real screen (round 3)

6 Sep 2026. Draft file `dAsaTgNj0xh25w2OGaurZo`, page **Referencing**, rows at y = 7900 / 9400 / 10900 (below rounds 1 and 2). Header note at y = 7680.

Every screen is the actual Brief page: status bar, orange band with **Fri, 4 Sep / Good morning, Ranjith**, search + avatar, the object, "New brief every morning at 7:00 AM", bottom nav. Same eight stories on all fifteen — the real Fri 4 Sep brief (23 published 3 Sep 07:00 → 4 Sep 07:00), reader follows Fintech · Ecommerce & D2C · Deals · IPO, tracks Meesho + Zerodha.

What is different each time is the **structure**, not the skin. None reuse Satya's folder (88), issue (86 A) or band (86 D); none reuse round 2's fifteen mechanics.

| # | Structure | What it says the Brief is | Headlines printed | Link |
|---|---|---|---|---|
| 01 | Sorted by what you follow | grouped by the reader's follows; grouping is the personalisation | 1 | [572-5](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=572-5) |
| 02 | Inbox | eight unread messages, sender = company | 2 | [578-2](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=578-2) |
| 03 | Checklist | reading list, 0 / 8 ticked | 1 | [579-2](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=579-2) |
| 04 | Questions | the five questions it answers | 0 | [580-2](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=580-2) |
| 05 | Memo | TO / FROM / RE, three numbered lines, sign-off | 3 (rewritten) | [576-2](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=576-2) |
| 06 | Graph | follows in the centre, stories as nodes on solid/dashed edges | 0 | [577-2](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=577-2) |
| 07 | Route | eight stops, start → done | 1 | [581-2](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=581-2) |
| 08 | Cover | masthead, one lead, coverlines | 1 | [582-2](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=582-2) |
| 09 | Table | company / what / figure, zebra rows | 0 | [583-2](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=583-2) |
| 10 | Changelog | +3 funding rounds, +1 IPO filing… since yesterday 7 AM | 0 | [584-2](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=584-2) |
| 11 | Watchlist first | tracked companies as full rows, rest as chips | 2 | [586-2](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=586-2) |
| 12 | Threads | LAST … → NOW … per company | 3 | [587-2](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=587-2) |
| 13 | DataLabs card | lead company as a profile card, seven pills | 1 | [588-2](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=588-2) |
| 14 | Tiers | must know / should know / good to know, by impact score | 1 | [589-2](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=589-2) |
| 15 | Filter → matrix | follow chips, 23 → 8 funnel, company × follow dots | 0 | [590-2](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=590-2) |

## Rules kept on every screen
- ≤3 full headlines; the rest are company + kind + figure.
- Every story carries its reason (followed sector/topic, tracked, or "also worth knowing"). Additive framing only.
- Brand orange `#EA4B2B`; Urbanist display, Inter body, JetBrains Mono labels, Fraunces for the serif moments.
- No live counters, no time claims, no invented figures. "LAST" lines on 12 are real prior Inc42 stories.

## Needs a new field before it can ship
| Screen | New field |
|---|---|
| 04 Questions | headline → question rewrite (summariser step) |
| 12 Threads | previous appearance per company (read events or last Inc42 story — fallback exists) |
| 14 Tiers | impact score in the app ranking (exists only in the audit extract) |
| 13 DataLabs card | company stage + DataLabs slug on the article |

Everything else is layout on fields the ranking already computes. Failure behaviour is written under each screen on the canvas.

## Recommendation
If one has to go into an A/B against the live card: **15 Filter → matrix** for "is this built for me" (it shows the mechanism and gives the reader the Edit), **10 Changelog** for "what will I get" (the 24-hour diff is the clearest statement of the cut), **04 Questions** for FOMO without giving the brief away.
