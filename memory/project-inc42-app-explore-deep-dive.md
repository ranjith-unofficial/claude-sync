---
name: project-inc42-app-explore-deep-dive
description: "Deep PostHog analysis (25-29 Aug 2026) of Explore article/company behaviour, Brief funnel reconciliation, calendar-vs-Past-Briefs entry points, behavioural segmentation, and the resulting 'Beyond Brief' homepage redesign — for the V2 freeze"
metadata:
  node_type: memory
  type: project
  originSessionId: 1bd2fc68-b479-44c7-b355-a8f9bafeb94c
  modified: 2026-08-29T07:45:57.380Z
---

Multi-day PostHog deep-dive (project 146258, EU) run 25-29 Aug 2026 to feed the V2 freeze decision. Cohort grew from 353→419→ during the session (`person.created_at >= 2026-08-12`, `@inc42.com` excluded) — treat as one growing cohort, not conflicting snapshots. Extends/corrects [[project-inc42-app-behaviour]] (20 Aug baseline).

## Explore article funnel (post-tour) — healthy, not a leak
167 opens/46 users/89 session-instances. Scroll signal on 65% of opens, avg depth 55.6%, only 6% reach ≥90%. Next action: 49% return to Explore, 35% background (same ~55% scroll depth either way — leaving isn't disengagement), 6% misclick to Brief. **73% loop back to Explore somewhere in the session, 49% open a 2nd article — NOT a one-way door**, unlike Brief's full-article exit problem.

## Explore company funnel (post-tour) — deepest genuine engagement, one real cliff
80 opens/29 users/37 sessions. 100% view ≥1 section, avg 2.95 distinct sections, 5.46 total views (real revisiting). Section reach: funding 100% → financial_overview 70% (**-30pt, the single biggest cliff in either funnel**) → key_people 46% (-24pt) → recent_activity 41% → corporate_activity 38%. 53% return to Explore after, 31% background.

## Search — the strongest quantified problem on the whole sheet
Articles 32.6% zero-result (89 searches/25 searchers), companies 31.5% (330/30). 86% of the time after a zero-result, the very next action is another search (real intent, not abandonment) — but **16% of all searchers (9 users) hit 3+ consecutive zero-results in one sitting**, worst case 28/46 zero. Hard evidence to elevate the already-flagged "investigate Elasticsearch" ticket to P0.

## Explore zero-touch sessions (50% of all Explore sessions) — NOT stuck users
Confirmed via follow-up: median 81s (vs 364s engaged), rarely search (0.7% vs 22%) or use filters (13% vs 30%), exit normally (~88% both groups background), and return at only a modest 6-7pt lower rate (55%/63% vs 61%/70% at 24h/48h). **Reads as "nothing caught the eye," not a broken interaction.** Real gap: **no feed-impression event exists** — can't tell if the feed is thin or the headlines just don't land. Don't redesign this blind; instrument first.

## Filter chips — one correction to prior notes
Real chip values (not "Latest/Top Deals/Financials/Edtech" as earlier guessed): latest/all/ipo_bound/just_launched/recently_funded/financials/soonicorns/news/deals/unicorns/early_fundraisers/startup_stories/in-depth/trends/watchlist. **`recently_funded` is the standout (52 users), 2x the next-best (`ipo_bound`, 23)** — strongest single content-preference signal found.

## Errors
explore/load_failed 6.8% (flat vs 3 weeks ago), brief/load_failed 7.4%, **company_profile/not_found 2.0% (new, untriaged, distinct from load_failed — likely stale company_id links from Explore cards)**.

## Calendar strip vs "Past Briefs" carousel — resolved, unmeasurable split (instrumentation gap)
The Brief home page has TWO entry points to a past brief: date-pill calendar strip + a "Past Briefs" card carousel. Neither `brief_opened` nor `brief_page_opened` carries any property distinguishing which was tapped — **confirmed absent, not a query limitation**. Best available (inferred, not measured) split: of ~105 total past-brief openers (current cohort), only 28 are session-linked to a calendar cover-view; the other ~77 (Ranjith's own estimate, consistent with the data) are inferred via the carousel. **Decision: keep both for this release, don't cut either on a guess — ship a `source` property on `brief_opened` (set client-side at tap time, e.g. `calendar_strip`/`past_briefs_carousel`, NOT inferred after the fact) and revisit consolidation next cycle with real data** (~100 opens/15 days gives a fast turnaround). Past-brief usage: 66/330 cover-viewers (20%) ever view a past edition; median 2 days back, real tail to 6-7 days; completion 18.6-19.5% vs 32% for today's brief (expected — "peek and leave" is real but not total, 1 in 5 still finishes).

**Sequencing of past-brief usage** (why people go there): only 14% is "finished today's brief, then browsed past" — the dominant pattern (53%) is **pure catch-up with zero same-day interaction**, plus 27% is a mid-session detour away from today's brief before finishing it (worth flagging as a distraction risk — some of these never return to finish today's brief).

## Brief funnel — three numbers hit a real definitional conflict, do not cite either version
Card 1→2 advance (45% baseline vs 80% re-pull), full-article return rate (6% vs 48%), repeat-open completion lift (26%→50% vs 35%→27%, **direction reversed**) all came back wildly different between a 20 Aug pull and a 25 Aug re-pull. Investigated: the **cover→entry number (55%→65.3%) was NOT a definitional conflict — confirmed via day-wise trend as a real, gradual improvement** (low-40s to 70s% over 12-15 days, no single shipped cause identified). The other three remain unreconciled — likely genuine query-definition mismatches (card-1 indexing, session-linkage scope, "2nd open" vs "any repeat open"), not measurement error. **Do not put these three numbers in front of Utkarsh without re-deriving them from a single consistent definition.**

## Behavioural segmentation (1,355 sessions, post-tour = 906) — the headline finding
| Persona | Sessions | 24h D1 return (first-session) |
|--|--|--|
| Explore-Articles-only | 12% | **70.0%** ← best in the whole analysis |
| Brief-only (largest cluster, 32%) | — | 49.2% |
| Multi-surface power (3+ surfaces) | 15% combined | 44.4% — LOWER despite looking "best" on paper |
| No-content-touch ("ghost", mostly a session-timeout measurement artifact) | 17% | 38.6% — lowest |

**A light, low-commitment first-session Explore taste retains better than a deep multi-surface session** (small n=20, but consistent direction). Platform splits by *session type*, not just install base: iOS skews Brief-only (168 vs 119 Android), Android skews Explore-Articles-only (91 vs 16 iOS) — not visible in earlier funnel-only work.

## "Beyond Brief" homepage redesign — design conclusion reached this session
In response to the segmentation finding, proposed adding a companies-mentioned module to the Brief home page (not gated behind brief completion — that would defeat the point). Final resolved design:
- **Don't build "sector-based" or a static "recently funded" module** — the former was wrongly thought blocked by data (see correction in [[project-inc42-content-personalization]]), the latter goes stale for daily visitors.
- **Lead with "companies mentioned in today's brief's articles"** — guaranteed fresh by construction (today's news always differs), contextually relevant, and confirmed viable: 67.7% of articles are fully company+sector tagged, 91-94% of tagged companies resolve to a real DataLabs profile.
- **Must NOT be framed as "Mentioned today"** (presupposes the user already read the brief, contradicts the requirement that non-Brief-readers see it too) — reframe as a standalone unit ("Today's Startup Movers"), and use real cards (name + one fact, e.g. funding amount) reusing the proven "at a glance" company-card format, not bare name chips (bare chips are illegible without brief context).
- Apply the same "companies mentioned" module to every past brief too (not just today's) — reuses the same mechanism, no special-casing needed for the archive.
- Known real failure mode (not hypothetical): **company name/rebrand mismatches break the DataLabs link** — Fibe (rebrand of EarlySalary) failed to match in the actual check. Needs an alias table, not better slug-guessing.
- Also flagged: reputationally-sensitive company mentions (e.g. a company named in a fraud/legal story) showing up in a positive discovery module — needs editorial/legal sign-off on an exclusion pass before shipping.
- DataLabs paywall boundary for this teaser's data depth is **unverified**, not confirmed either way — check before shipping.
- **Sequencing recommendation**: ship calendar/Past-Briefs consolidation + read/unread/started state on past-brief cards first (low risk, data-backed); ship the companies-mentioned module second (needs alias infra + source-tagging + editorial sign-off); "Beyond Brief" rotating filter-teaser last (needs a content-freshness rule from Content/DataLabs that doesn't exist yet). Don't ship all three simultaneously — can't attribute a retention change to any one cause if you do.
- Ravi Kumar's standing critique ("weekly recap = bells and whistles, must not hold homepage prominence") directly informs keeping the rotating discovery module bottom-of-page and low-prominence, and avoiding "this week" framing anywhere in copy.

Related: [[project-inc42-app-behaviour]], [[project-inc42-app-v2-scope-full]], [[project-inc42-app-ravi-critique]], [[project-inc42-content-personalization]], [[project-inc42-app-structure]].
