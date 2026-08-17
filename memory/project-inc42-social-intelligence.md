---
name: project-inc42-social-intelligence
description: "Inc42 app — \"Pulse\" (Social Intelligence) PRD v2.0 (combined, 2026-07-30) — reconciled with Utkarsh's research track; locked decisions D1-D15, phased cadence, legal gates"
metadata: 
  node_type: memory
  type: project
  originSessionId: 52399608-92e3-47c8-89fd-c3a51291e0f2
  modified: 2026-07-31T00:00:00.000Z
---

Next-phase feature for [[project-inc42-launch]]. Reader-facing name: **Pulse**. Owners: Ranjith (product & AI), Utkarsh (research, decisions), Nityam (design), Editorial (daily review + allowlist).

## PRD status (as of 2026-07-31)
Two PRDs written in parallel — Ranjith's v1.0 (27 Jul, product mechanics/editorial workflow) and Utkarsh's research track (evidence/supply/legal) — were merged into **v2.0 combined, dated 2026-07-30, "Draft for review."** Utkarsh shared this final combined version. Neither source superseded the other; it's a reconciliation, not an overwrite. Below reflects v2.0, superseding the earlier "Lane A" framing this memory previously tracked.

## The reframe that changes the product (D14, new vs earlier framing)
5-model independent review reframed the job: **status/FOMO is the emotional driver, sensemaking is the delivery mechanism** — not pure time-saving/efficiency as originally modeled. Consequences:
- Attribution is now product value, not just legal cover — "Nithin Kamath argued X" transfers status; "an investor said X" doesn't.
- "Most Debated" block is the status-richest — should not be first cut on thin days.
- Share rate (`pulse_shared`) is a **primary/leading metric**, not vanity — status content gets forwarded to display knowledge.
- ⚠️ This downweights (does not reverse) the demand-risk null: VOC mining found the "too much noise" pain at only ~0.046% of 77K posts — but public text is a poor instrument for status anxiety since people conceal it, especially to the professional audience whose regard is at stake. Demand premise stays **ASSUMPTION — UNVALIDATED**; Phase-2 research gate still applies.

## Locked decisions (D1-D15)
- D1 Name = Pulse · D2 Tier: Free teaser + Plus/Pro depth (boundary: Free = editorial-curated full daily edition + in-article Pulse; Plus = archive + all sectors; Pro = per-source depth + voice-level alerts + export)
- D3 100% manual editorial approval, nothing auto-publishes; automation only once reject-rate earns it
- D6 **Story-matching is enrichment, not a gate** — confirms this memory's earlier finding: only ~13% of quality commentary matches an Inc42 story, 86.5% is orphan. Unmatched items are first-class, flow to the Pulse section (not discarded). Orphan set is also more differentiated (87-92% absent from editorial vs hard news 26-73% already covered).
- D7 Allowlist ~**200 voices** (not 50), sector-level personalisation — needed because 50 voices ÷ 8 sectors is too thin
- D9 Phased cadence: **Phase 1** rides the morning Brief (no separate publish, cutoff ~20:00 prior evening) → **Phase 2** dedicated evening edition (~18:30 start, hypothesis not finding — needs a 3-arm send-time test)
- D13 v1 review tooling = **sheet-backed queue**, not a custom admin app — "simplify the tooling, never the controls"
- D15 Commercial-conflict escalation triggers on **negative/political content**, not on the commercial relationship itself (relationship is visible context, raises priority)
- D8 Quotes are **behind a flag** — synthesis-first ships regardless of counsel's call on quoting; quotes turn on only if cleared

## Legal (hardest gate)
Platform terms (LinkedIn scraping via Apify, unofficial X ingestion via twitterapi.io) is the **hardest legal gate** — no license, no safe harbour, LinkedIn beat hiQ on breach of contract. Copyright/defamation/DPDP positions are comparatively stronger. **Rung-4 contingency**: if counsel requires per-voice consent, this PRD doesn't survive as specced — descopes to a 20-40 voice consent-based editorial franchise instead.

## Kill criteria
Engagement rate <5% of all Brief-opening sessions, sustained 4 weeks, with reach ≥50% (people saw it and didn't want it) → demand hypothesis disconfirmed, fold supply back into editorial, don't build Phase 2.

**Premise:** Inc42 tells readers what happened; Pulse shows what the ecosystem is saying about it. Sources are **LinkedIn + X only**, top posts from an allowlist of ecosystem voices. First-party trending ("saved by 500+", read counts) and any social-network primitives (follows/comments/likes/UGC) are explicitly **out of scope** — not a feed.

## Product mechanics (v2.0, current)
- **Two surfaces:** in-article Pulse (conditional, only when a story has an approved Pulse — collapsed 1 line + attribution stub → expands to 2 lines + up to 4 sources) and the **Pulse section** (phase-dependent blocks: Today's Pulse, Moving Fast [Phase 2 only], Most Debated, This Week — finite, no infinite scroll/pagination).
- **Hard cap: 2 lines** of Inc42-written text, always — a caption, not a second story.
- **4 buckets:** Reaction (1 line) · Insight (2) · Announcement (1) · Debate (2, one per side).
- **Consensus vs Split** (in-article only, not the section): needs **3+ credible posts**; ≥65% one stance = consensus, else split. Under 3 posts → no in-article Pulse for that story.
- **9 reject filters** (§8.1) + **10 mandatory rejection reason codes** (§9.2), logged as the future automation training set. Filter 9 (negative/political) triggers escalation, not rejection.
- Attribution mandatory on every third-party opinion (name, handle, title, link) — now dual-purpose: legal shield **and** the product's status value (D14).

## Matching (article ↔ post) — D6, confirmed against 60-day data
Company/handle, founder/investor names, event type+date window. **Enrichment, not a gate**: only ~13% of quality-gated commentary (1,768 posts vs 785 articles, ±3-day window) matches an Inc42 story — 86.5% is orphan, and the orphan set is the *more* differentiated half (industry-take 13% already covered, macro-policy 8%, vs acquisitions 73% already covered). Unmatched items flow straight to the Pulse section rather than being discarded, and double as a **newsroom story-lead feed**.
Same failure shape as the 86% missing sector tags in [[project-inc42-content-personalization]] — a coverage gap quietly killed the original "peer-reaction-attaches-to-our-stories" design assumption.

## Resolved since the earlier draft
- **Allowlist sized at ~200 voices** (not 50) — sector-level personalisation needs ≥~6/sector at minimum and 200 clears reach for all 4 personas at ≥1 item/day on 98.3% of days (D7, §11).
- **Media in posts** — resolved from 1,409-item sample: 84.8% tweets, media (image/video/text on LinkedIn) is ~11.8% of supply but lifts engagement (image +20%, video +84% within-LinkedIn). v1 rule: flag media, don't display it; short+media posts go to human review not auto-reject (§8.5).
- **Legal/ToS positioning** confirmed: platform-terms breach (LinkedIn/X scraping) is the hardest gate; public framing must be "editorial team curates," never "an agent scrapes" (§13, carried into v2.0 unchanged).
- Publish cadence changed from the originally-floated 11AM/5PM fixed slots to the phased Brief-riding / evening-edition model (D9, see locked decisions above).

## Existing pipeline it plugs into
A working internal newsroom tool already scrapes ~916 tracked founders/investors twice daily and scores posts — see the `Social Signals Feed Logics` sheet in ~/Downloads. `feed_score = base_score + consensus boost`; `base_score = 100×editorial_relevance + signal_type(0–40) + 40·e^(−age/7) + 12·is_outlier + traction`. **Relevance dominates (0–300 of the range).** Verified against the sheet's data: the traction term is floored at 0, though the sheet's written formula omits that floor — **the doc is wrong, not the data**.
