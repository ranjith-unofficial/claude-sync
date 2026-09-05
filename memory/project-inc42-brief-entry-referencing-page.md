---
name: project-inc42-brief-entry-referencing-page
description: Brief entry screen round of 5 Sep 2026 built on the "Referencing" page (476:2) of the draft Figma file — four spectrum points (Paper/Balanced/App/Stack) on Wed 5 Aug, plus B on four failure days; B recommended; awaiting Ranjith's review
metadata:
  type: project
---

**Built 5 Sep 2026 (evening)** from `~/ClaudeDocs/inc42/BRIEF-CARD-DESIGN-BRIEF.md`, on page
**"Referencing" (node 476:2)** of draft file `dAsaTgNj0xh25w2OGaurZo`. Ranjith asked to draft on that
page only and edit nothing else; Page 1 child count verified unchanged (989) before and after.

**Framing he gave mid-build:** balance "editorial feel vs very modern app" — not old, not so modern
that people can't parse it. So the round is four points on that spectrum with ONE shared data contract:
- A1 Paper (x=100) editorial end, masthead + 7-row reason/company ledger — the only one adding a field
  (company, 73%).
- **B1 Balanced (x=600) — recommended**: count as object, type line, 8-segment spine (orange = followed,
  grey = ecosystem, legend gives grey a reason), personal line only when ≥1 match, one lead headline.
- C1 App (x=1100) dark focal card, 8 reason tiles.
- D1 Stack (x=1600) card stack + count badge + reason-only peek.
Row 2 (y=1400) = B on failure days: B2 ordinary Fri 10 Jul 3/8, B3 AI-only zero match, B4 logged out
no prefs, B5 one story Mon 13 Jul. Notes under every screen (y=880 / y=2280) state day, fields+coverage,
failure behaviour, editorial cost (none anywhere). Page header note at y=-330.

**Decks are simulated** with the locked formula on real days (`articles_90d.csv` + rows809 sectors,
affinity=0, newsletter/announcement posts excluded). Simulation showed the "no importance signal"
property concretely: on 8 June, Fintech+Deals ranks Zepto's ₹8,010 Cr UDRHP 8th, below a summit
thank-you post. June days have no sector data (809 audit starts 21 Jun) and no summary bullets, so
design days were moved to Aug/Jul.

**Type:** Inter UI + Fraunces headlines (Gilroy not installed). Helper JS pattern (fixed-width text with
NONE→resize→HEIGHT, y-cursor from measured heights) in the session scratchpad; one screen per
`use_figma` call worked with zero atomic failures.

**Why:** ~12 prior rows (C–S) had been rejected or unreviewed; the brief document was written to reset,
and this is the first round built against it.

**How to apply:** re-read the Referencing page before the next round — he edits frames directly.
Related: [[project-inc42-brief-entry-coverage]], [[project-inc42-brief-impact-continuity]],
[[feedback-design-review-ranjith]], [[reference-figma-mcp-build-techniques]].
