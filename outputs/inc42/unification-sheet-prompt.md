PROMPT — paste into a fresh session with the Google Sheet connected.
This is the ONE INC42 UNIFICATION plan ONLY — user-facing "one Inc42" features across Website, DataLabs, and App.
Engineering foundation, analytics, and Utkarsh's PostHog review are DELIBERATELY excluded (listed as separate tracks at the end).

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

───────────────────────────────────────
## THE ROADMAP (main table — one row per feature)

Columns: **Month | Vertical | Funnel Stage | Feature | What we'll do | How we'll do it | Attributes to (metric it moves) | Source | Status**
(Vertical = Distribution / Engagement / Sanity, from the Inc42 Unification tab. Source = Sheet5 / Unification-tab / Competitor-gap / Strategy. Status = Not started. Leave Owner + Date blank.)

**MONTH 0 — DESIGN & SPEC ("spec the one-Inc42 experience")**
- Sanity | Design | Unified Login — spec & design | Design one account across media ↔ data | Product + design | Acquisition (identity) | Unification-tab
- Engagement | Design | Unified navigation bar — design | One nav shared across surfaces | Design | Activation | Sheet5
- Engagement | Design | Search prominence + unified search — design | Design a visible, unified search | Design | Activation | Unification-tab + Competitor-gap
- Distribution | Design | llm.txt / AI answer-engine — prep | Draft llm.txt so LLMs cite Inc42 | Content + tech | Awareness | Competitor-gap
- Acquisition | Design | Source-based Lock Modal — design + staging | Design the registration gate | Design + staging | Acquisition | Sheet5

**MONTH 1 — AWARENESS + ACQUISITION ("be found as one brand; one account")**
- Distribution | Awareness | llm.txt live — AI answer-engine visibility | Publish llm.txt | Content + tech | Awareness (only Crunchbase has it) | Competitor-gap
- Distribution | Awareness | Google Discover/preference bar · Google News indexing | Optimize "preferred source" + index | SEO/tech | Awareness | Sheet5 + Competitor-gap
- Sanity | Acquisition | Unified Login LIVE | One account across media ↔ data | Auth + FE | Acquisition → % identified | Unification-tab + Competitor-gap
- Acquisition | Acquisition | Lock Modal LIVE — registration-gate profiles/database | Gate identity behind registration (articles stay open) | Ship the M0 modal | Acquisition → % identified (THE cliff) | Sheet5
- Acquisition | Acquisition | Unified onboarding | Ask role + sector once, reused everywhere | Product flow | Qualified term | Sheet5

**MONTH 2 — ACTIVATION ("one connected product")**
- Engagement | Activation | AskInc42 everywhere — prominent on DataLabs + introduce in Inc42 Media | One assistant across surfaces (today: DataLabs only) | Product + backend | Activation | Sheet5 + Unification-tab
- Engagement | Activation | DataLabs cross-linking / interlinking (media ↔ data) | Link articles ↔ company/entity pages both ways | Content model + FE | Activation + cross-surface (Crunchbase strongest) | Sheet5 + Unification-tab + Competitor-gap
- Engagement | Activation | Search bar prominence + unified search | Make search visible; one search across surfaces | FE | Activation | Unification-tab + Competitor-gap
- Engagement | Activation | In-body entity card · living company pages · profiles that lead somewhere | Company card in the reading path; profiles route onward | FE | Activation → cross-surface discovery | Strategy
- Engagement | Activation | Content / news personalization | Recommend content per reader | Ranking/ML | Activation/Engagement (The Ken has it) | Unification-tab + Competitor-gap
- Engagement | Activation | Article & Companies card redesign | Premium visual refresh | Design | Activation | Sheet5

**MONTH 3 — ENGAGEMENT ("one community, reasons to return")**
- Engagement | Engagement | WhatsApp community | Stand up a community channel | Ops | Engagement (The Ken, Tech in Asia have it) | Unification-tab + Competitor-gap
- Engagement | Engagement | Reading progress bar · in-article TOC / navigation bar | Add progress + in-article nav | FE | Engagement (cheap edge — no rival has it) | Unification-tab + Competitor-gap
- Engagement | Engagement | Audio content format | Narrated articles/newsletters | Content | Engagement (The Ken) | Unification-tab + Competitor-gap
- Engagement | Engagement | Brief habit loop (app) | Tune the daily return loop | Product | Engagement | Strategy

**MONTH 4 — ENGAGEMENT / RETENTION ("deepen & hold")**
- Engagement | Engagement | Personalization v2 + community deepening | Iterate on the M2/M3 winners | Product | Engagement/Retention | Unification-tab
- Sanity | Retention | Cross-surface saved / bookmark + follow | One saved/follow graph across surfaces | Product | Retention | Strategy

**MONTH 5 — SANITY / REVENUE ("one price")**
- Sanity | Revenue | Common / unified pricing | One pricing across media ↔ data | Product + billing | Revenue (Tracxn, Tech in Asia have it) | Unification-tab + Competitor-gap
- Sanity | Revenue | Entitlement mapping (free / T1 / T2 fences) | Define the fences behind the unified price | Product | Revenue | Strategy

───────────────────────────────────────
## COMPETITOR GAPS (add as a small reference table — all map to the Inc42 Unification verticals)

| Gap (Inc42 ❌/⚠) | Vertical | Who has it | Plan slot |
|---|---|---|---|
| AI answer-engine visibility | Distribution | Crunchbase | M0→M1 llm.txt |
| Search bar prominence | Engagement | Entrackr, Crunchbase, YourStory, Tech in Asia | M1–M2 |
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
3. Brief fix = get past card 1 (only 45% advance) + stop dumping readers into the full-article one-way door (94% never return; median completion ~78s).

## RULES
- Self-contained; don't invent owners/dates (leave blank).
- Keep the two ⚠ dependencies visible: AskInc42 v2 personalization needs an API from Anmol; Website activation ("2nd article") still needs validation.
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
