---
name: project-inc42-publishing-cadence
description: "Inc42 editorial go-live timing, 19 Aug–2 Sep 2026 — in-depth publishes in two blocks with a 4-hour empty hole, morning scheduled / evening publish-when-ready"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4388da54-7a86-42fa-aea0-cce065a9b8a3
  modified: 2026-09-03T04:41:42.842Z
---

Analysis run 2026-09-03 on 15 days of go-lives (19 Aug – 2 Sep 2026): 209 total = 179 news, 24 in-depth, 5 startups, 1 resources. Artifact: https://claude.ai/code/artifact/38404cd7-a6b5-4a5d-a755-a115bcf60b9e (file `~/ClaudeDocs/inc42/go-live-cadence.html`).

## The core finding — in-depth publishes in two blocks, not across the day
| Window (IST) | Pieces | On a round clock slot (:00/:30) |
|---|---|---|
| 06:00 – 12:30 | 12 | **10 of 12** |
| **12:30 – 16:25** | **0** — on all 15 days | — |
| 16:25 – 23:59 | 12 | **1 of 12** |

Two different processes wearing one label: a **scheduled morning release** (06:00, 07:00, 11:00 sharp) and an **evening queue draining as pieces clear** (ragged minutes: 16:25, 17:51, 19:27, 20:11, one at 23:59).

## Weekday signatures (each rests on only 2–3 observations — direction, not baseline)
| Day | News/day | In-depth/day | In-depth timing | Held |
|---|---|---|---|---|
| Mon | 15.5 | 1.0 | 06:00 sharp, the day's only piece | 2/2 |
| Tue | 17.5 | 2.0 | an 11:00-band piece | 2/2 |
| Wed | 16.3 | 1.3 | an 11:00-band piece | 3/3 |
| Thu | 13.5 | 1.5 | evening only, 18:42–19:27 | 2/2 |
| Fri | 10.5 | 2.5 | heaviest depth day, 4 of 5 after 16:00 | 2/2 |
| Sat | 8.0 | 1.5 | evening + ragged, or nothing | 1/2 |
| Sun | **0** | 1.5 | morning only (07:00–12:30), zero news all day | 2/2 |

**Two engines:** news is a weekday factory (14.8/day weekdays → 8 Sat → 0 Sun). In-depth holds ~1.6/day across all seven days, weekend included. News clock: 8% before 07:00, 12% 07:00–10:59, **80% after 11:00**.

## The finding that matters for the Brief
**In-depth published on 14 of the 15 days** — the only blank day was Sat 22 Aug. So when a brief carries no depth story, the piece almost always existed and was not picked up. **Supply is not the constraint; the cutoff and selection rule are.**

Same-day in-depth visible to a brief by cutoff time: 07:00 → 5 of 24 (21%) · 12:30 → 12 (50%) · 17:00 → 14 (58%) · 20:00 → 20 (83%). A **same-day morning brief can never see more than the morning block**, which on most days is exactly one piece. The locked 7AM→7AM brief window (see [[project-inc42-content-personalization]]) covers the full previous day, so it does see the evening block — one day late.

## Open question, not yet answered
What is the Brief's actual compile time and lookback window in the build? Needed before saying which pieces a given brief could have seen. Raised with Utkarsh 3 Sep 2026 after he flagged that recent briefs carried no depth stories and asked to revisit the story mix by publishing time and day of week.

Related: [[project-inc42-content-personalization]], [[project-inc42-morning-tape]], [[project-inc42-app-v2-scope-full]].
