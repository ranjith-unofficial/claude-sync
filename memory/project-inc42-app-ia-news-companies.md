---
name: project-inc42-app-ia-news-companies
description: "App IA after the 7 Sep design review (Explore splits into News + Companies) — measured filter behaviour, News section supply, Companies section order, and four in-room figures corrected. Delivered 8 Sep 2026 for the 9 Sep design gate"
metadata: 
  node_type: memory
  type: project
  originSessionId: 18bf6b04-1f4f-4757-a2bb-cdae01167126
  modified: 2026-09-11T08:22:16.541Z
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

## Update 8 Sep (evening) — structure locked with Ranjith, built in Figma
Ranjith overruled two of my calls, correctly, by applying the anti-duplication rule to my own
answer: **no companies in the News ring** (Companies is its own tab) and **no "companies in
today's news" shelf** (that concept already lives in Brief). Resolved structure:

- Bottom nav: **Brief · News · Companies · You** (he proposed "For you"; I flagged that in every
  news app For You is a personalised feed and the *first* tab — and it collides with Brief's
  "Recommended for you" section. Rename unresolved.)
- Streak is a **header icon**, not a tab. That closes the old 4th-tab question.
- **Ring = sectors**, live sectors only (24-48h), interest-ordered, red ring = new since last
  visit. A fixed sector list runs empty (AI 50% of weekdays, DeepTech 39%, Fintech 18%).
- **Tab strip = development tags only**, ordered by supply. In-Depth comes OUT of the strip
  (it is a format, not a tag) and becomes a shelf.
- **Newsletters (AI Shift, Markets, Checkout) are shelves on News home**, peers of Funding and
  In-Depth. No wrapper, no "From Inc42" heading, no cover/issue format. They are saved rules
  over existing fields: Markets = `company_type = Listed Startup` (85% covered, 18/week, 3+ in
  93% of weeks) · Checkout = ecom/D2C/QC/retail/logistics (18/week) · **AI Shift = AI/deeptech
  (3/week, below 3 in 40% of weeks — the thin one, and the one Ranjith is most excited about)**.
  Rejected putting them in Brief: Brief's identity is "then it ends".
- **Tab ≠ shelf**: a tab is a filtered archive that goes back in time so it is never empty and
  supply thresholds do not apply; a shelf is a promise about now and needs 2-3 items nearly
  every weekday. Funding is the only thing that is both, and its shelf's View all opens the
  same page the tab opens.

**Built in Figma** (file `dAsaTgNj0xh25w2OGaurZo` "App - Draft Screen", page `Referencing`
476:2, y=18700, below the round-4 work): News full scroll `649:2`, Companies full scroll
`651:2`, decision note `652:2`. Seat confirmed **Inc42 / Full / pro**, writes work on this file.

**Filed in Asana 11 Sep 2026** as subtasks of "V2 - Dev Task" (gid 1218172204712996, Inc42 App), all
assigned to Ritvik with descriptions: Brief Page, Brief Completion page, Company Explore page,
Company Explore logic, Company Detail page, Article Detail page, Profile page, Merge Watchlist
into Profile section, Streak page redesign, Attribution. ⚠️ The older open subtask "Revamp - Bottom
navigation bar" still specifies the **3-tab Brief / Explore / Watchlist** nav, which contradicts
this 4-tab lock. Flagged to Ranjith, not edited.

**Open for Prapti, not design:** do the newsletters contain original writing, or are they
curated from published articles? A rule-built AI Shift is only honest if curated.
