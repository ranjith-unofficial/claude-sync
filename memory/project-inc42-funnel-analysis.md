---
name: project-inc42-funnel-analysis
description: "INC42 product funnels + QIA reality — the identification cliff, activation defs, weekly-plan artifact"
metadata: 
  node_type: memory
  type: project
  originSessionId: d8963308-0bb1-4e90-a221-f2c4311ce0ba
---

Built a QIA-grounded weekly plan for Ranjith (Aug 2026). Artifact (updated in place): **https://claude.ai/code/artifact/dfd082a1-c773-4367-8002-e8b1548b5b01** · source `~/ClaudeDocs/inc42/inc42-weekly-plan.html`.

**QIA number is soft.** Utkarsh's "~2,100 qualified today" = 21,298 ninety-day identified actives × 9.99% (role **and** resolved company). But QIA is defined as **30-day** (not 90), so it's inflated; true QIA-30 ≈ **1,200–1,500** (est). Can't be measured cross-surface today (identity spine broken). Plan gates everything on pulling the real QIA-30 from BigQuery first. See [[project-inc42-strategy-utkarsh]].

**Per-product activation (validated where possible)** — activation = earliest action that predicts return (FT RFV / NYT habit method):
- **Website** = reads a **2nd article** (⚠ proposed, not measured — validate on proj 53557: 2nd article vs scroll≥70% vs newsletter).
- **DataLabs** = **views a company profile** (✅ data-backed: `/company/` is the #1 surface, 1,777 users/9,134 views/30d; repeat-use by action: Adv Filter 53% · Saved Search 52% > Search 44%).
- **App** = **completes a brief, engaged ≥60s** (not the 7s flick; 41% nominal completion but 7s median).

**THE finding — the identification cliff** (PostHog, 30d, internal excluded; [[reference-inc42-posthog-projects]]):
| | Website | DataLabs | Unified* |
|--|--|--|--|
| Views | 721,890 | 207,529 | 929,419 |
| Visitors | 478,249 | 135,909 | 614,158 |
| Activation | 45,510 (9.5%) | 83,647 (62%) | 129,157 |
| **Identified** | **1,986 (0.42%)** | **211 (0.16%)** | **2,197 (0.36%)** |
| Engaged 2+d | 42,622 | 2,665 | 45,287 |
| Retained | 36,635 | 1,880 | 38,515 |
| Revenue | 186 | 278* | 464 |

Both deliver value at scale then **identify almost no one** — the funnel collapses at identity, not activation. This is the one-number case for registration-gating (A2). *Unified = naïve sum (can't dedup cross-surface yet = the spine work). * DataLabs Revenue 278 > Identified 211 because payment events don't carry email (person-on-events) — the broken spine showing in data.
