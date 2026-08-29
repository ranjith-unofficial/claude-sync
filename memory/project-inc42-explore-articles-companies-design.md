---
name: project-inc42-explore-articles-companies-design
description: "Explore tab (Articles + Companies) card-logic design direction, 27-29 Aug 2026 — competitor research, Brief-vs-Story naming resolved, Companies card-shape correction, 8+8 UI variations artifact; still mid-iteration, not yet approved by Ranjith"
metadata:
  type: project
  originSessionId: 1c442aa8-439c-4822-95e9-3864030f3bbb
  modified: 2026-08-29T07:46:04.837Z
---

Distinct from [[project-inc42-app-brief-gratification-redesign]] (that's the Brief tab / gratification-beat redesign). This thread is the **Explore tab's two sub-tabs — Articles and Companies** — specifically how each card's layout/logic should work, based on Ritvik's `explore-feed-logic.md` reference doc plus a 15-slide proposal deck, reconciled and then validated against real competitor products.

## What's locked (evidence-backed, not just asserted)

- **Naming: keep "Brief," don't rename to "Story."** This directly resolves the open question flagged in [[project-inc42-app-brief-gratification-redesign]] ("'Brief' may not land with news readers — 'story'/'quick read' floated, not decided"). Evidence: Quartz's *Daily Brief* newsletter is alive today under that name — the *Quartz Brief app* that shut down (2019) was killed by a chat-interaction gimmick, not the label (Nieman Lab post-mortem). Renaming to "Story" would actively collide with Inc42's own tag vocabulary (*Session Article*, *Spot News* already use "story" for a single piece). **The actual fix is visual, not verbal**: an Instagram/Snapchat-style segmented progress bar across the top of the Brief card, not a rename.
- **Companies Explore cards: fixed shell + dynamic lead metric, NOT structurally-different-per-signal.** Ritvik's original proposal (card height/shape changes per signal — funding vs momentum vs thin-data) has no precedent at scale in Crunchbase, Tracxn (Data Labs' direct competitor), CB Insights, Bloomberg Terminal, or LinkedIn — all of them keep one fixed card shell and only vary the lead metric + a reason chip inside it. Baymard Institute's dashboard research: inconsistent card structure measurably hurts pattern recognition — matches the "random is worse" risk the proposal deck's own slide 3 already flagged. The fully-adaptive version is only defensible as a top-3 "Hero" rail (Ritvik's signal #1, rank≤3), never the general list.
- **Articles Explore cards: the current tag-driven hero/row/masthead spec holds as-is** — 6 of 8 rules are free reads of tags the desk already sets; matches how Apple News and Inshorts mix a hero unit with plain rows in one feed. Not a novel risk like the Companies side.
- **Two gaps found comparing the proposal deck against the as-built reference doc** (not yet answered by Ritvik): (1) the deck's company-signal list has a 10th rule, "Backed by a person" (angel investor, little data else), missing from the current 9-rule build; (2) the deck links two *split* prototypes (Companies-only / Articles-only), while Ranjith's own reference link is a third, merged build — canonical URL unconfirmed.
- **The actual data blocker**, once distilled from both the deck and Ritvik's doc, is 5 concrete questions for Prapti/Ritvik (not a vague "send me an API"): what `signals_count` actually is (highest leverage, start now), event-name field on session/summit articles, a named-series field, `[Update]` as its own field, and structured (not prose) earnings numbers — plus the paginated companies API itself to validate thresholds against the real ~75,000-company base (current build tested on only ~100 by hand, self-rated 30-40% confidence).

## Deliverables produced

- `~/ClaudeDocs/inc42/inc42-explore-page-logic.md` — full signal tables, payload issues, build sequence, reconciled against the deck.
- `~/ClaudeDocs/inc42/inc42-v2-experiments-plan.md` — merges Utkarsh's confirmed brief-page A/B tests with Ritvik's company-signaling experiment into one sequenced stack.
- Task-ledger additions: 21 new rows in `~/ClaudeDocs/inc42/inc42-open-ledger-MASTER.csv` section **P** (P1-P14, the Explore-page decision items) plus additions to sections E/D — **also copied into a new tab "Open Ledger (27 Aug)"** in the Google Sheet at `docs.google.com/spreadsheets/d/1NCpTEzgEEtds0uCfqPNSS6aeFhOpKbgkL_F-cgtVPxg` (the same workbook holding App V2 Roadmap / App - Funnel Diagnostics / Dunning System tabs) — see [[reference-inc42-open-ledger-sheet]].
- Design-direction artifact (HTML, iterated 5 times): 8 full-scale UI variations each for Articles and Companies (baseline, current-spec, magazine, Axios-style, curated-blocks, data-hybrid badge, minimal-list, immersive-swipe for Articles; baseline, fixed-shell, fully-adaptive, single-score, tile-grid, trend-sparkline, ranked-table, spotlight-card for Companies), each with a recommend/consider/avoid verdict and sourced tradeoffs.

## Status — mid-iteration, not approved

Ranjith rejected the first four passes of the visual artifact as cluttered, wrongly-scaled, and "not following any design principle." Root causes found and fixed: (1) a click-to-reveal switcher hid 13 of 14 variants behind an unnoticed toggle — compounded by a real bug (stray leftover `</div>`) that broke the CSS reveal entirely, so only the plain baseline ever showed; (2) mockups were built from memory/generic patterns instead of real references. Fixed by (a) showing all variants simultaneously at full phone-mockup scale, no hidden interaction, and (b) pulling actual Dribbble references (a "Kites Design" news-app shot for card anatomy — source row + engagement row; an F1 editorial-app shot for bold stat-forward hero cards; a dark fintech watchlist app for filled-gradient trend charts and tabular right-aligned deltas) before rebuilding. See [[feedback-ui-mockup-research-first]] for the durable process lesson. **As of last update Ranjith had not yet confirmed the redesigned version is acceptable** — check before treating any of the "locked" bullets above as shipped, only as the current recommended direction.

**Why:** captures both the substantive product decisions (which are evidence-backed and durable) and the unresolved process/approval state (which is not) separately, so neither gets misread as the other.

**How to apply:** cite the "What's locked" section as the current best-evidence direction for Explore/Companies work; do not tell Ranjith the visual artifact itself is finished without first confirming with him, since as of this writing he had not signed off on the latest pass.
