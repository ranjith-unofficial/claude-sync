---
name: project-inc42-content-personalization
description: "Inc42 app brief ranking engine — locked spec, brief schedule, and the data problem that breaks it"
metadata:
  node_type: memory
  type: project
  originSessionId: 9528bcb6-d611-479f-9459-97ac0adfb878
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

## Other
- Content architecture also has a 9-parent *user-facing* topic set (Fintech, Ecommerce & Consumer, AI, Enterprise & SaaS, Startup Ecosystem, Real Estate Tech, Mobility & Logistics, Climate & DeepTech, Edtech & Health) — confirm which set onboarding actually shows.
- **Streak:** tied to `brief_completed`; reward hierarchy favours identity/status over extrinsic rewards.
