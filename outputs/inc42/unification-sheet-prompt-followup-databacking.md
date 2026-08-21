FOLLOW-UP PROMPT — data-back the "Unification Roadmap v1" tab.

PREREQUISITE / ORDER: Run this ONLY AFTER the main Unification prompt (unification-sheet-prompt.md) has created the "Unification Roadmap v1" tab. If that tab does not exist yet, STOP and run the main prompt first.
⚠ There is a SEPARATE tab called "Roadmap v1" (the full six-track roadmap) — do NOT touch it. Edit ONLY "Unification Roadmap v1".

HARD RULES:
- Read all figures from THIS prompt — you do NOT have the dashboard file; do not go looking for it.
- Edit ONLY "Unification Roadmap v1". Leave every other tab (including "Roadmap v1"), the weight table, and all other sheets untouched.
- Do NOT insert rows between existing roadmap rows (it breaks sort/filter). Report exactly what you changed.

1) ADD ONE COLUMN, positioned immediately AFTER the "Attributes to (metric it moves)" column (i.e. before "Depends on"), titled:
   "Baseline / Target (DataLabs, Aug 2026)".
   Populate ONLY these three rows; leave the cell blank on every other row:

   • Distribution · the M1 row "llm.txt live — AI answer-engine visibility" (NOT the M0 "prep" row) →
     Baseline: Inc42 AI-citation share ~23.4% (early Aug), status "Follower" — behind Crunchbase ~28–30%, YourStory ~20–24%, Tracxn ~17%.
     Target: 28.2%.
     ⚠ The citation tracker reads 0 for the week of 10 Aug — verify before quoting the live number.

   • Sanity · the M1 row "Lock Modal LIVE — registration-gate profiles/database" →
     Baseline: ~580 registrations/week (range 498–627, Jul–Aug 2026).
     Target: to be set by the A/B holdout.

   • Sanity · the M5 row "Common / unified pricing" →
     Baseline: 83 active *paying* subscriptions (Metorik, 17 Aug 2026); ~35 Pro trials/week; ~18 payments/week.
     Target: TBD.
     Definitional note (put in the cell or an adjacent comment): "83 = currently-active PAID subscriptions. This is NOT the 278 PostHog 30-day payment-event count (event-based), nor the 1,045 lifetime Plus+Pro base used by the A1 probe (both on the Roadmap v1 tab). Three different definitions of 'paying' — do not sum or compare."

2) REFINE (do NOT replace) the DataLabs activation definition wherever it appears in the tab.
   Locked Flag 2 (search = activation) still holds — this only adds a threshold + window + onboarded precondition. Set the definition to Inc42's own tracked metric, verbatim:
   "Onboarded user who completed ≥2 search actions in the week (WAAU)."  Baseline: ~197 WAAU/week.
   Add this caveat alongside it: "WAAU is WEEKLY; QIA is rolling 30-day — ~197 WAAU/week is NOT ~197 QIA-30. Do not equate the two."

3) ADD the AI-visibility backlog as a SEPARATE block BELOW the roadmap table (never inserted between roadmap rows), titled:
   "AI-visibility backlog (from DataLabs dashboard)".
   Cross-reference it from the M1 "llm.txt live" row (e.g. append to that row's Notes / Depends-on cell: "see AI-visibility backlog below"). Block contents:
   • Deploy robots.txt allow-crawl — P0, currently BLOCKED — est. +5,000–8,000 clicks/month
   • Complete Schema markup (Organization + FAQ) — PARTIAL — est. 30–50% CTR uplift from rich snippets
   • Quick wins: add FAQ schema + freshen funding data on the top company-funding queries where Crunchbase out-cites Inc42
   • Already DONE (context only): Canonical-tag fix (+35.6% organic traffic); AI-crawling policy deployed
   Note in the block: these are DataLabs SEO/AEO execution items that SUPPORT the unification AI-visibility feature — reference only, NOT unification feature rows.

4) OPTIONAL — add a small context note on the Distribution section: DataLabs company profiles earn ~2,082 organic clicks/week, ~50K impressions, ~2% CTR, avg GSC position ~6.3.

REMINDER: figures come from this prompt only; edit ONLY "Unification Roadmap v1" (never "Roadmap v1"); weights stay locked; nothing else is touched; no rows inserted mid-table.
