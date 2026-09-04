---
name: project-inc42-brief-entry-coverage
description: Brief entry card rebuilt from measured field coverage (5 Sep 2026) — one gated shell, trigger-strip ladder, 61-day backtest; row F in the draft Figma file
metadata:
  type: project
---

**Status 5 Sep 2026:** row F (y=77000) in draft file `dAsaTgNj0xh25w2OGaurZo` — four real days
(6 Aug heaviest, 20 Aug zero-AI, 13 Jul company-less rows, 21 Jun single story). Spec at
`~/ClaudeDocs/inc42/brief-entry-coverage-spec.md`. Not yet reviewed by Ranjith.

**Measured coverage (809 articles, 61 days):** no company 27%, two companies 5%, no sector 24%,
no topic 15%; AI zero on 50% of weekdays, DeepTech 39%, Team 73%, Trends 64%; <8 stories on 23%
of days; headlines with a figure 47% (Deals 82%, Financials 89%, News 31%).
Direct-match rate: Deals+Fintech 87% of days, AI-only 20%, Team-only 13%.

**Shell rule:** a slot may only promise what its field delivers ≥85% of days; otherwise it must
disappear cleanly and never announce absence. Personal line only when ≥1 direct match. Lead
kicker ladder: fit → topic·sector → sector → none. Trigger strip ladder: followed companies →
followed sectors → any company (two-company rows emit two chips) → topic counts; max 6; hidden
when empty (2 of 61 days, both single-article Sundays).

**Prior rounds rejected:** C (20 concept cards — asserted properties the ranking doesn't compute),
D (listed all 8 headlines — gave the brief away), E (entity index — blank on 27% of rows).

**Open:** affinity matrices not provided (needed for `CLOSE TO`); onboarding completion rate;
whether showing the lead headline costs card-2 reach — proposed A/B on the existing PostHog flag.
Spec defects found in the ranking logic itself are in [[project-inc42-content-personalization]]
context: ParentMultiplier scales n²; popularity measures supply not appetite; same topic+sector
ties resolve on recency only.
