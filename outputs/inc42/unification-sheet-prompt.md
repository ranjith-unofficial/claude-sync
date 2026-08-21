PROMPT — paste into a fresh session with the Google Sheet connected.
This is the ONE INC42 UNIFICATION plan ONLY — user-facing "one Inc42" features across Website, DataLabs, and App.
Engineering foundation, analytics, and Utkarsh's PostHog review are DELIBERATELY excluded (listed as separate tracks A-D at the end).

═══════════════════════════════════════════════════════════

You are updating a Google Sheet that is the **One Inc42 Unification** roadmap — making Inc42's Website, DataLabs, and App feel like ONE product (one brand to discover, one connected experience, one account & price).

**Sheet:** https://docs.google.com/spreadsheets/d/1B2r_lT0HuS5L0axnZr34FWSY0iphjoTWy7z2Jm4w17E/edit

**Task:** Create a NEW tab **"Unification Roadmap v1"**. Do NOT modify existing tabs (Plan, Inc42 Unification, Sheet5, Competitors Features comparison) — read for reference only. Anchor the scope on the existing **"Inc42 Unification"** tab (verticals: Distribution / Engagement / Sanity) and the **Competitors** tab. Model the monthly structure on **Sheet5**. When done, confirm you touched only the new tab.

───────────────────────────────────────
## CONTEXT (the "why")

Inc42 runs three surfaces (Website, DataLabs, App) for one audience, but they don't feel like one product — separate logins, no cross-linking, an assistant only on DataLabs, no shared pricing. Unification = closing those gaps.

North-star lens = QIA (Qualified Identified Actives — a known-role person in the core market, active in 30 days). The funnel is Acquisition → Activation → Engagement. The measured reality (last 30 days): both Website and DataLabs deliver value at scale but identify almost no one — **Website identifies 0.42% of visitors, DataLabs 0.16%**. The leak is identity, so a unified account + gating is the highest-leverage unification move.
(Note: the QIA/RFV measurement and the identity backend that prove this live in the separate Foundation/Analytics track below — this plan is the user-facing features.)

───────────────────────────────────────
## THE MODEL (top of the tab — effort weight by funnel stage, by month)

Based on Sheet5's weighting, with an **Acquisition/Identification** stage added (Sheet5 omits it — but that's the leak):

| Month | Design/Spec | Awareness | Acquisition | Activation | Engagement | Retention | Revenue |
|---|---|---|---|---|---|---|---|
| M0 | 0.75 | — | — | — | — | — | — |
| M1 | — | 0.30 | 0.30 | 0.20 | 0.20 | — | — |
| M2 | — | 0.20 | 0.25 | 0.25 | 0.30 | — | — |
| M3 | — | 0.05 | 0.15 | 0.30 | 0.40 | 0.10 | — |
| M4 | — | 0.05 | 0.10 | 0.15 | 0.45 | 0.25 | — |
| M5 | — | 0.05 | 0.05 | 0.10 | 0.45 | 0.25 | 0.10 |

**These weights are LOCKED — do NOT re-cut, rebalance, or "fix" them.** They are Ranjith's effort-allocation model from Sheet5 and carry a strategic decision that is his to change, not yours.

Instead, add a small **COVERAGE CHECK** block immediately under the weight table listing every month × stage cell that carries weight but has ZERO feature rows in this plan (M5 Engagement at 0.45 is one; check them all). Report the gaps as a list and stop there — do not close them by moving rows in, inventing rows, or adjusting weights. Ranjith decides what happens to each.

───────────────────────────────────────
## THE ROADMAP (main table — one row per feature)

Columns: **Month | Vertical | Funnel Stage | Feature | What we'll do | How we'll do it | Attributes to (metric it moves) | Depends on | Source | Status**
(Vertical = Distribution / Engagement / Sanity ONLY, from the Inc42 Unification tab — NEVER a funnel stage. Source = Sheet5 / Unification-tab / Competitor-gap / Strategy. Status = Not started. Leave Owner + Date blank.)

**Depends on** — where a feature row below ends with a `Depends on:` clause, put that text in this column; otherwise leave the cell blank. Blank means "nothing blocks the start", NOT "no dependency": every row whose metric is a % identified / activation number assumes Track A instrumentation is live in order to be read at all.

**MONTH 0 — DESIGN & SPEC ("spec the one-Inc42 experience")**
- Sanity | Design | Unified Login — spec & design | Design one account across media ↔ data | Product + design | Acquisition (identity) | Unification-tab | **Depends on:** Track A — Identity spine (the spec must match the canonical Auth0 distinct_id model)
- Engagement | Design | Unified navigation bar — design | One nav shared across surfaces | Design | Activation | Sheet5
- Engagement | Design | Search prominence + unified search — design | Design a visible, unified search | Design | Activation | Unification-tab + Competitor-gap
- Distribution | Design | llm.txt / AI answer-engine — prep | Draft llm.txt so LLMs cite Inc42 | Content + tech | Awareness | Competitor-gap
- Sanity | Design | Source-based Lock Modal — design + staging | Design the registration gate | Design + staging | Acquisition | Sheet5

**MONTH 1 — AWARENESS + ACQUISITION ("be found as one brand; one account")**
- Distribution | Awareness | llm.txt live — AI answer-engine visibility | Publish llm.txt | Content + tech | Awareness (only Crunchbase has it) | Competitor-gap
- Distribution | Awareness | Google Discover/preference bar · Google News indexing | Optimize "preferred source" + index | SEO/tech | Awareness | Sheet5 + Competitor-gap
- Sanity | Acquisition | Unified Login LIVE | One account across media ↔ data | Auth + FE | Acquisition → % identified | Unification-tab + Competitor-gap | **Depends on:** Track A — Identity spine (canonical Auth0 distinct_id across 3 PostHog projects + 2 Customer.io workspaces)
- Sanity | Acquisition | Lock Modal LIVE — registration-gate profiles/database | Gate identity behind registration (articles stay open) | Ship the M0 modal | Acquisition → % identified (THE cliff) | Sheet5 | **Depends on:** Track A — Restore Register-Lock instrument + Scroll Depth (MUST land in M0, or the A/B holdout on the single highest-leverage lever in this plan is unreadable) + Feature-Flag framework (to run the holdout)
- Sanity | Acquisition | Unified onboarding | Ask role + sector once, reused everywhere | Product flow | Qualified term | Sheet5 | **Depends on:** Track A — Identity spine (role/sector must persist against the canonical id, or it is captured and lost)
- Distribution | Acquisition | Newsletter signup as identity capture | Make newsletter signup a shared capture point across all three surfaces (NYT's habit anchor). NOTE: this row is the shared signup/identity capture only — the Datalabs Weekly product itself stays in Track C by decision; do not merge them. | Placement + flow | Identified + retention | Strategy

**MONTH 2 — ACTIVATION ("one connected product")**
- Engagement | Activation | AskInc42 everywhere — prominent on DataLabs + introduce in Inc42 Media | One assistant across surfaces (today: DataLabs only) | Product + backend | Activation | Sheet5 + Unification-tab
- Engagement | Activation | DataLabs cross-linking / interlinking (media ↔ data) | Link articles ↔ company/entity pages both ways | Content model + FE | Activation + cross-surface (Crunchbase strongest) | Sheet5 + Unification-tab + Competitor-gap
- Engagement | Activation | Search bar prominence + unified search | Make search visible; one search across surfaces | FE | Activation | Unification-tab + Competitor-gap
- Engagement | Activation | In-body entity card · living company pages · profiles that lead somewhere | Company card in the reading path; profiles route onward | FE | Activation → cross-surface discovery | Strategy
- Engagement | Activation | Content / news personalization | Recommend content per reader | Ranking/ML | Activation/Engagement (The Ken has it) | Unification-tab + Competitor-gap | **Depends on:** Track A — Identity spine + per-product activation events (no behavioural signal, no personalization)
- Engagement | Activation | Article & Companies card redesign | Premium visual refresh | Design | Activation | Sheet5

**MONTH 3 — ENGAGEMENT ("one community, reasons to return")**
- Engagement | Engagement | WhatsApp community | Stand up a community channel | Ops | Engagement (The Ken, Tech in Asia have it) | Unification-tab + Competitor-gap
- Engagement | Engagement | Reading progress bar · in-article TOC / navigation bar | Add progress + in-article nav | FE | Engagement (cheap edge — no rival has it) | Unification-tab + Competitor-gap
- Engagement | Engagement | Audio content format | Narrated articles/newsletters | Content | Engagement (The Ken) | Unification-tab + Competitor-gap

**MONTH 4 — ENGAGEMENT / RETENTION ("deepen & hold")**
- Engagement | Engagement | Personalization v2 + community deepening | Iterate on the M2/M3 winners | Product | Engagement/Retention | Unification-tab
- Sanity | Retention | Cross-surface saved / bookmark + follow | One saved/follow graph across surfaces. NOTE: this row ships the follow graph ONLY — Alerts on followed companies/sectors stays in Track C by explicit decision (it is a retain/membership feature, not a make-the-surfaces-feel-like-one feature, and is not in the Inc42 Unification matrix). Do not pull Alerts in. | Product | Retention | Strategy | **Depends on:** Track A — Identity spine

**MONTH 5 — SANITY / REVENUE ("one price")**
- Sanity | Revenue | Common / unified pricing | One pricing across media ↔ data | Product + billing | Revenue (Tracxn, Tech in Asia have it) | Unification-tab + Competitor-gap | **Depends on:** Track C — the A1 migration probe must read before the unified band can be set
- Sanity | Revenue | Entitlement mapping (free / T1 / T2 fences) | Define the fences behind the unified price | Product | Revenue | Strategy | **Depends on:** Track C — A1 migration probe

───────────────────────────────────────
## COMPETITOR GAPS (add as a small reference table — all map to the Inc42 Unification verticals)

| Gap (Inc42 ❌/⚠) | Vertical | Who has it | Plan slot |
|---|---|---|---|
| AI answer-engine visibility | Distribution | Crunchbase | M0→M1 llm.txt |
| Search bar prominence | Engagement | Entrackr, Crunchbase, YourStory, Tech in Asia | M0 (design) → M2 (live) |
| Unified login | Sanity | Tracxn, Tech in Asia | M1 |
| Cross-linking media↔data | Engagement | Crunchbase, DealStreetAsia, Tech in Asia | M2 |
| Content personalization | Engagement | The Ken | M2 |
| WhatsApp community | Engagement | The Ken, Tech in Asia | M3 |
| Audio content | Engagement | The Ken | M3 |
| Reading progress / in-article nav | Engagement | (nobody — cheap edge) | M3 |
| Unified pricing | Sanity | Tracxn, Tech in Asia | M5 |
| Native news app | Distribution | The Ken, YourStory, Tech in Asia | Already shipping (App) |
| Team/enterprise plans | Sanity | Tracxn, Tech in Asia, Crunchbase | ✗ DO NOT chase — DataLabs enterprise tried & killed (0/17 renewals) |

───────────────────────────────────────
## DECISIONS / FLAGS (add as notes)
1. Acquisition/Identification is its own weighted stage — 0.16–0.42% identified is the leak, not activation.
2. DataLabs activation = search/filter (an active query), not company-view (that's the SEO landing).
3. Alerts stays in Track C (membership), by decision — it is not in the Inc42 Unification matrix. M4 ships the follow graph without it; that is deliberate.
4. Unified Login creates a unified-DELETION obligation — the Delete-functionality flow in Track C must be scoped to the one account, not per-surface (DPDP).

## RULES
- Self-contained; don't invent owners/dates (leave blank).
- Keep the two ⚠ dependencies visible: Website activation ("2nd article") still needs validation; AskInc42 v2 personalization needs an API from Anmol — but that feature now sits in **Track D**, so carry the flag on the Track D listing, not on an M2 row.
- Write ONLY to the new "Unification Roadmap v1" tab; leave all other tabs untouched and say so when done.

═══════════════════════════════════════════════════════════
## ⛔ SEPARATE TRACKS — NOT part of this unification plan (do NOT add to the tab)

**A. Engineering foundation & analytics** (enables/measures unification, but is its own track):
- Singular setup (attribution)
- Identity spine — canonical Auth0 distinct_id; converge 3 PostHog projects + 2 Customer.io workspaces; promote 40,699 ICP labels
- Feature-Flag framework
- QIA-30 baseline pull + RFV engagement score
- Per-product activation events + full-funnel instrumentation (+ DataLabs referral event)
- Restore Register-Lock instrument + Scroll Depth
- V2 app release · redefine login page · collect phone number

**B. Utkarsh's recent PostHog review** (analytics hygiene, not relevant now):
- Event dictionary v1.5 reconciliation · fire dark events (push_delivered, decode, monetization) · dedupe untrack events · completed_engaged (≥60s) · is_internal tag / internal-user exclusion

**C. Membership / offering & ops** (a separate product track):
- Datalabs Weekly · Alerts · Deal Digest + report surfaces · rooms-as-membership · A1 migration probe · renewal motion + dunning · Hiring Agent · CRM use-case · Delete-functionality flow
- **App-internal brief optimisation** — moved out of the unification plan by decision. App-internal engagement is not a cross-surface "one Inc42" feature; same logic that keeps Alerts out. The app's unification touchpoints (unified login on app, AskInc42 everywhere, cross-linking) stay in the plan; its internal optimisation does not.
  - **Brief redesign** — get past card 1 (only 45% advance) and stop dumping readers into the full-article one-way door (94% never return; median completion ~78s, NOT 7s)
  - **Brief habit loop** — tune the daily return loop

**D. Parked — no home yet.** These fell out of the unification plan AND out of tracks A-C in the split. Park, don't delete — nothing is lost:
- **Turn on Morning-Brief push** — 67% opt-in is already granted and push has never once fired. Cheapest engagement win on the board.
- **AskInc42 v2 — 3 stored onboarding Qs** · ⚠ needs an API from Anmol, not yet raised with him
- Model training on app context
- Lifecycle journeys groundwork (state-based journeys)
- G8 independence firewall · Hurun list-factory formalise (trust / credential engine)
- Role + employer type + timestamp at every capture point — partly absorbed by M1 Unified onboarding; confirm the overlap before dropping it
