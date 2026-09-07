---
name: project-inc42-app-ia-news-companies
description: "App IA after the 7 Sep design review (Explore splits into News + Companies) — measured filter behaviour, News section supply, Companies section order, and four in-room figures corrected. Delivered 8 Sep 2026 for the 9 Sep design gate"
metadata:
  type: project
---

**Done 8 Sep 2026.** Answers the two questions left open by the 7 Sep App UI Redesign review
(Wispr `2233a7e7`, transcript archived at
`~/ClaudeDocs/inc42/wispr-transcripts/2026-09-07_1857_app-ui-redesign-discussion_2233a7e7.md`):
what goes on News home besides stories, and what order the Companies sections run in.
Deliverable: `~/ClaudeDocs/inc42/app-info-hierarchy-news-companies.md`. Seed context was
`CLAUDE-HANDOFF-app-info-hierarchy.md`, left unmodified.

## The measured core (PostHog project 146258, 90d to 8 Sep; 1,397 app openers, 654 returners)
**Every named filter beats the default feed on both sides.** Companies: `all` converts to a
profile 21.3%, filtered pills 41-75%. Articles: `latest` opens an article 36.9%, topic pills
51-77%. Sectioning is the thing that works; the flat feed is the thing that does not.

- **Articles pills** (users / opens-an-article): deals 68/51%, financials 44/53%,
  startup_stories 31/62%, in-depth 21/**77%**, trends 21/64%, news 8/44%.
- **Companies pills** (users / opens-a-profile): recently_funded 108/50%, just_launched 35/**73%**,
  ipo_bound 33/49%, early_fundraisers 21/41%, unicorns 16/52%, soonicorns 14/75%,
  profitable_startups 2/33%.
- **There is no sector pill in Explore at all** — so "people use development tags more than
  sector" is true and partly tautological. `sector_landing_viewed`: 69 users in 90d,
  **7.5% of returning users**, 41 via Explore + 25 via a card tag.

## Four in-room figures corrected
| Room | Measured |
|---|---|
| Watchlist ~15% | **82.7%** of returners *view* the tab (940 users); only **11.6%** ever add (103). A high-traffic EMPTY tab, median 1 visit |
| Streak 20-25% | 21.6% of returners (201 users). Correct — but Streak is weaker than Watchlist on every measure (201 vs 940 reach, 35 vs 142 repeat) |
| Recently funded "87% data" | 87% = *amount* exists. **Date currency is 79%**; 13% of DataLabs `last_funding_date` are >365d stale (SUGAR article 4 Sep 2026 vs DataLabs Jul 2025; Comet, Medulance, Ather same pattern) |
| 44% never open brief | 45.4% — 1,119 reached brief page, 611 opened one |

## Recommendations that contradict the room
1. **Top strip on News should be TOPIC, not sector.** Sector loses on reach (7.5% of returners),
   coverage (76% rolled up vs 85% development_type; raw `primary_industry` is only 14%), and
   daily supply (AI zero on 50% of weekdays, Startup Ecosystem never populated). Sector stays as
   the card tag + landing page + onboarding personalisation seed.
2. **Streak's top-level tab is a gamification bet, not a usage fact** — keep the tab, drop the
   usage argument from the stakeholder doc.

## News section supply (65 weekdays, 1,179-article corpus)
Only three clear the fixed-section bar: **News** (98% of weekdays ≥1, 86% ≥3, median 5),
**Deals** (95%/71%, median 4), **In-Depth** (97% ≥1 but only 20% ≥3 → a 1-2 row unit, never a
rail). IPO 75%/17%, Financials 62%/26%, Regulatory 58%/8%, Trends 43%, Team 32% → pills, not
sections. Weekend median is **3 articles vs 16 on a weekday**, so every rail needs a designed
1-row and 0-row state. Rule carried from the brief page spec: the section is fixed, the rows
degrade.

## Stories vs sector collision, resolved
Nothing called "Stories" goes on News home. "Brief stories" stays a Brief construct; `story_type`
is 64% "Others" and not navigable; "Startup Stories" (44 articles/90d) is a pill. Top strip is
topic, which dissolves the collision rather than picking a winner.

**Why:** the room's IA was about to promote the weakest measured navigation dimension into the
most valuable strip, and to ship a Recently-funded section that silently omits ~1 in 5 rounds
Inc42 itself reported that week.

**How to apply:** cite the pill conversion table before anyone proposes a flat feed for either
tab. Before quoting Watchlist or Streak usage, say whether you mean reach or repeat — the entire
in-room disagreement was that one word. Related: [[project-inc42-app-explore-deep-dive]],
[[project-inc42-brief-card-corpus-analysis]], [[project-inc42-brief-companies-mention-types]],
[[project-inc42-explore-articles-companies-design]], [[project-inc42-app-search-root-cause]].
