---
name: project-inc42-content-personalization
description: "Inc42 app brief ranking engine — locked spec, brief schedule, and the data problem that breaks it"
metadata:
  node_type: memory
  type: project
  originSessionId: 9528bcb6-d611-479f-9459-97ac0adfb878
  modified: 2026-08-29T07:45:11.693Z
---

Ranking + brief engine behind [[project-inc42-launch]].

## Ranking formula (LOCKED with Ranjith, 2026-07-14)
```
TopicScore  = 1.0 × (1 if article's topic ∈ followed topics else 0)   # affinity = 0, no matrix in v1
SectorScore = 0.6 × (number of matched sectors)                        # simple count, not normalized
PopScore    = 0.15 × ( ½·topicPop + ½·sectorPop )                      # sectorPop = SUM of the article's sectors
score       = TopicScore + SectorScore + PopScore
Sort: score DESC → published_at DESC.  Editorial "App Featured = Yes" pinned on top, by recency.
```
- **An article has max 1 topic; sectors can be multiple.**
- **8 topics** (popularity): News 1.000 · Deals 0.759 · Financials 0.252 · Trends 0.164 · Regulatory 0.123 · IPO 0.116 · Team 0.092 · Startups 0.023
- **7 sectors** (popularity): Consumer 1.0 · Fintech 0.75 · Ecommerce & D2C 0.69 · DeepTech 0.64 · Enterprise & SaaS 0.52 · Startup Ecosystem 0.50 · AI 0.23
- Known trade-off Ranjith accepted: because SectorScore is an unnormalized count, **3+ matched sectors can outrank a perfect topic match** (1.80 > 1.75). Fine while users follow few sectors.

## Brief schedule (LOCKED — 7 days/week, NO Sunday break; reconciled with Utkarsh)
| Day | Brief | Window (IST) | Max |
|---|---|---|---|
| Tue–Sat | Weekday | since previous brief (7AM→7AM) | 8 |
| **Sun** | Weekly Recap | **Mon 7AM → Sat 7AM** (Mon–Fri articles) | 10 |
| **Mon** | Weekend | **Sat 7AM → Mon 7AM** (Sat+Sun articles) | 9 |

⚠️ This **supersedes** the old PRD's "Mon–Fri + Sat recap + Sun off". Streak (no weekend pause now), FAQ copy, and push schedule all had to be updated.

## 🔴 Simulation findings (real data, 366 articles, Jun 13–Jul 14 2026)
Ran the scorer (`~/Downloads/inc42_brief_scorer.py`) against the BigQuery export:
1. **86% of articles have NO `Company_Industries`** → SectorScore = 0 almost always. **Sector personalization is dead.** Users pick sectors in onboarding and it changes nothing. This is a **content-tagging gap, not a code bug.**
2. **20% have no `Development_Type`** → score 0.00, ranked by recency alone.
3. **Score is effectively binary** (topic match ≈1.06, else ≈0.05) and **all matching articles tie exactly** → recency is the real ranker.
4. **Every brief is monotone** — a Deals follower gets 10 Deals articles; a no-preference user gets 10 News articles. **No diversity constraint exists.**
5. **~12 articles publish/day vs a cap of 8** → the brief shows ~70% of everything. On 31% of days it shows *everything*. Ranking only truly matters in the Sunday recap (77 → 10).
6. 8 industry values aren't in the sector map and silently score 0: Social Media, Ride Hailing, Quick Commerce, AR/VR, Kitchenware, TBD.

**Recommended P0s:** fix sector tagging (or drop sector selection from onboarding); add the missing industry values; add a per-topic diversity cap.

## 🔴 CORRECTION (2026-08-29): the "86% no sector" figure is stale / field-specific, not the current whole-picture state
Re-checked against a fresh article export (`~/Downloads/p (4).csv`, 802 articles, dated 2026-08-25) and an existing, more complete audit (`~/ClaudeDocs/inc42/inc42_sector_tagging_audit.xlsx`, 15 tabs, built 20 Aug). Real current state:
- `primary_industry` field alone: only 15.3% filled — **this matches the original 86%-missing finding almost exactly**, so that number wasn't wrong, it just got over-generalized into "sector tagging is dead" everywhere.
- The richer **`industries`** field (multi-value, likely what actually feeds `Company_Industries`/SectorScore downstream): **81.3% filled**. The audit's own "Primary Industry" column (title-case, different from the CSV's lowercase field) shows 80.3% filled (650/809) — consistent with this.
- Company tagging: 72.7% of articles have a real company (excl. `TBD` placeholders), matches the audit's 72.9%.
- Articles with BOTH a real company AND a sector/industry signal: **543/802 = 67.7% of everything published** — fully ready for any sector- or company-based feature today, not a future state.
- Fully "dark" (no company, no sector, nothing): 110-113 articles (13.7-14%) — a real, un-fixable-by-sync gap, needs actual editorial tagging.
- The audit already has a specified, ready-to-run fix (`3. Sector Fix Plan`, 337 articles) for **Bucket F: "Primary Industry present, Sector MISSING"** (178 articles) — described as "THE BIG ONE — sector column simply not synced from industry." This is a sync bug, not a tagging gap, and coverage jumps substantially in the audit's "after backfill" projection once applied.

**How to apply**: don't cite "86% of articles have no sector" as current state anymore — it's true only for the narrow `primary_industry`/`Company_Industries` field specifically. For anything checking "is there enough sector/company data to build on," use the 67.7%-fully-tagged / 81.3%-has-industries figures instead. Separately confirmed: of companies tagged on articles, **91.2% resolve to a real DataLabs company profile** (93.9% weighted by mention frequency; top-30 most-mentioned companies matched 100%) — checked via `$pageview`/`DL Page Type=Company Profile` on PostHog project 66351, so sector- and company-based app features are viable to build now, not blocked. Related: [[project-inc42-app-explore-deep-dive]].

## Other
- Content architecture also has a 9-parent *user-facing* topic set (Fintech, Ecommerce & Consumer, AI, Enterprise & SaaS, Startup Ecosystem, Real Estate Tech, Mobility & Logistics, Climate & DeepTech, Edtech & Health) — confirm which set onboarding actually shows.
- **Streak:** tied to `brief_completed`; reward hierarchy favours identity/status over extrinsic rewards.
