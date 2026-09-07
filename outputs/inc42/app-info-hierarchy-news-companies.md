# App information hierarchy: News and Companies

**Date:** 8 September 2026 · **Owner:** Ranjith · **For:** Satya, Prapti, Utkarsh, Ritvik
**Gate:** design EOD 9 Sep · dev 11 Sep · submit Fri/Sat · marketing launch 15 Sep

This document answers the two questions left open in the 7 Sep design review: what belongs on
News home besides stories, and what order the Companies sections should run in. Every figure
below is measured. Where something is not measured it says so.

---

## 0. Method

| Source | Scope |
|---|---|
| PostHog, project 146258 (Inc42 App) | 90 days to 8 Sep 2026. 1,397 users opened the app, 654 opened it on 2 or more days |
| Article corpus | 1,179 articles, 6 Jun to 4 Sep 2026, WordPress REST plus ACF. 65 weekdays, 26 weekend days |
| DataLabs company check | all 443 company slugs tagged in those articles, checked against inc42.com/company/{slug} |
| Funding freshness probe | 178 funding articles with a tagged company, DataLabs last_funding_date compared against the article date |

Two words used precisely: **reach** is distinct users who touched a surface. **Repeat** is users
who touched it on 2 or more separate days. Reach and repeat diverge badly on this app and most
of the disagreement in the room comes from quoting one when meaning the other.

---

## 1. What was locked on 7 Sep and stays locked

| Decision | Status |
|---|---|
| Explore splits into News and Companies as separate bottom tabs | Locked |
| Four tabs, Profile last | Locked |
| Watchlist moves under Profile | Locked |
| Companies is a sectional home plus a browse all filter page | Locked |
| Search stays global, more prominent on Companies, not a fifth tab | Locked |
| Company profile is UI only this round, UX is v3. No web view | Locked |
| Design order: article, news home, companies home, company profile, brief last | Locked |
| Hero card description is the first summary bullet | Locked |
| Short display names needed for long sector names | Locked, options in section 7 |

One decision from the room is challenged by the data and is flagged in section 3.1. One is
flagged in section 5. Everything else above is left alone.

---

## 2. What people actually filter by

This is the measured version of the point made in the room that people use development tags
more than sector.

**Articles sub tab, 90 days.** Last filter held in a session, and whether an article was opened
in that session.

| Filter | Users | Sessions | Opened an article |
|---|---|---|---|
| latest (default) | 1,021 | 2,492 | **36.9%** |
| deals | 68 | 84 | 51.2% |
| financials | 44 | 53 | 52.8% |
| startup_stories | 31 | 34 | 61.8% |
| in-depth | 21 | 35 | **77.1%** |
| trends | 21 | 22 | 63.6% |
| news | 8 | 9 | 44.4% |

**Companies sub tab, 90 days.** Same method, outcome is opening a company profile.

| Filter | Users | Sessions | Opened a company profile |
|---|---|---|---|
| all (default) | 753 | 1,117 | **21.3%** |
| recently_funded | 108 | 128 | 50.0% |
| just_launched | 35 | 41 | **73.2%** |
| ipo_bound | 33 | 39 | 48.7% |
| early_fundraisers | 21 | 22 | 40.9% |
| unicorns | 16 | 21 | 52.4% |
| soonicorns | 14 | 16 | 75.0% |
| watchlist | 5 | 8 | 62.5% |
| profitable_startups | 2 | 3 | 33.3% |

Three things follow, and they carry the rest of this document.

1. **Every named filter beats the default feed, on both sides.** Companies: 41% to 75% against
   21% for the undifferentiated list. Articles: 51% to 77% against 37% for latest. Sectioning
   is not a nice to have for power users. It is the thing that works, and the flat feed is the
   thing that does not.
2. **There is no sector filter in Explore at all.** The pill row has never contained one. So
   "people use development tags more than sector" is true, and the reason is that development
   tags are the only option present. That does not make the comparison meaningless, see 3.1.
3. **Small n on the tail.** just_launched, unicorns, soonicorns and early_fundraisers sit on 14
   to 35 users. Treat the top three as evidence and the tail as direction.

---

## 3. News home

### 3.1 The top strip: put topic on top, not sector

The room landed on sector across the top and development tags on the card below. The data
argues the opposite and this is the one recommendation worth 10 minutes of argument.

| Axis | Sector | Development tag (topic) |
|---|---|---|
| Reach, 90 days | 69 users hit a sector landing page. 41 of those came from Explore, 25 from a card tag | 193 users used at least one topic pill |
| Reach among returning users | **7.5%** (49 of 654) | Topic pills are the entire non default pill row |
| Field coverage in the corpus | **76%** after a best effort roll up. Raw primary_industry is only 14% populated | **85%** on development_type |
| Weekdays with zero stories in the biggest buckets | AI 50%, DeepTech 39%, Fintech 18%. Startup Ecosystem is never populated | News 2%, Deals 5% |
| What it does when tapped | Opens a sector landing page that 7.5% of returners have ever seen | Filters the feed in place, and that filtered feed converts about 1.5x better than latest |

Sector is the weakest navigation dimension currently measurable on the app, on the thinner
field, with the worse day to day supply. Putting it in the most valuable strip on the new
News home promotes it on the strength of a hypothesis while demoting the one dimension that
already has measured pull.

**Recommendation**

| | Put here |
|---|---|
| Top strip on News home | Topic: Latest · Deals · In-Depth · Financials · IPO. These are the pills people already use and the ones with daily supply |
| Card eyebrow | Development tag, short form. 85% coverage, so it is nearly always present |
| Sector | Keep it as the tag chip on the article card and on the article page. Keep the sector landing page. Do not make it the primary strip |
| Onboarding sector interest | Use it to reorder the topic sections and seed the Companies sections. Not as a visible sector strip |

If the sector strip ships anyway, ship it with an event on the strip itself and revisit in two
weeks with the same query. It is a cheap thing to be wrong about once, and an expensive thing
to be wrong about permanently.

### 3.2 What sections News home can actually carry

Rule for the whole page, carried over from the brief page spec: **the section is fixed, the rows
degrade.** A section that appears some days and not others breaks its own promise and costs more
than the content it was hiding.

Weekday supply, 65 weekdays:

| Candidate section | Median per weekday | Weekdays with 1 or more | With 3 or more | Verdict |
|---|---|---|---|---|
| **News** (business updates, controversies) | 5 | 98% | 86% | Permanent, full rail |
| **Deals** (funding, fund launches, M&A) | 4 | 95% | 71% | Permanent, full rail |
| **In-Depth** | 1 | 97% | 20% | Permanent, but a 1 to 2 row unit, never a rail |
| IPO | 1 | 75% | 17% | Not a permanent section. Fold into Deals |
| Financials | 1 | 62% | 26% | Not a permanent section. Fold into Deals or make it a pill only |
| Series | 1 | 78% | 15% | Pill only |
| Regulatory | 1 | 58% | 8% | Pill only |
| Startup Stories | 1 | 51% | 2% | Pill only |
| Trends | 0 | 43% | 5% | Pill only |
| Team (people, layoffs) | 0 | 32% | 5% | Do not build |

Only News, Deals and In-Depth clear the bar for a named section that is present essentially
every weekday. Everything else is a filter, not a section.

Weekends are a separate problem and must be designed, not discovered: **median 16 articles on a
weekday against 3 on a weekend day.** Every rail on this page needs a defined 1 row and 0 row
state before it ships.

### 3.3 Recommended News home, top to bottom

| Order | Unit | Source | Why |
|---|---|---|---|
| 1 | Topic strip | Latest, Deals, In-Depth, Financials, IPO | The measured navigation behaviour |
| 2 | Hero story | Top ranked story. Description is summary bullet 1 | Locked 7 Sep |
| 3 | Latest rail | Recency, current explore feed logic | 37% of sessions already open something from it |
| 4 | Deals | development_type roll up | 95% of weekdays, converts 51% |
| 5 | Companies in today's news | Companies tagged on today's stories | The only cross link between the two new tabs, and it is guaranteed fresh by construction |
| 6 | In-Depth | parent_category | 97% of weekdays, highest conversion measured at 77% |
| 7 | Continue reading | Local read state | Not instrumented today. Ship the event with the tab, build the section next cycle |

Item 5 is the answer to how News and Companies stay one product instead of two. It is already
specified and coverage checked in `brief-page-sections-spec.md` section 3: keep one section name
on every day, degrade the row (chip plus number, then chip plus any number, then chip plus
profile link, then chip alone), hide only at zero companies.

### 3.4 The stories versus sector collision, resolved

Raised in the room: if sectors sit in the top strip, "stories" cannot also sit above them, and
the two are different things. They are.

| Term | What it is | Where it lives |
|---|---|---|
| Brief stories | The cards inside a brief. A brief construct | Brief tab only. Never on News home |
| story_type | A CMS field: Exclusive 4%, Series 11%, Follow Up 6%, Others 64% | Not user facing. Too sparse and too Others heavy to navigate by |
| Startup Stories | A parent_category, 44 articles in 90 days | A pill, not a section |

**Resolution:** nothing called "Stories" appears on News home. The word stays inside the Brief so
it keeps one meaning in the product. The top strip is topic. This removes the collision entirely
rather than deciding which of the two wins the slot.

### 3.5 What does not go on News home

Company database sections. Full watchlist management. Deep company filters. Streak as page hero.
A second infinite feed under the sections.

---

## 4. Companies home

### 4.1 Section order

Ordered by measured demand first, conversion second, data availability third.

| Order | Section | Users, 90d | Converts to profile | Data note |
|---|---|---|---|---|
| 1 | **Recently funded** | 108 | 50.0% | Utkarsh: last round amount exists on 87% of rows, 13% undisclosed. Freshness caveat in 4.3 |
| 2 | **Just launched** | 35 | 73.2% | Highest conversion measured on the tab |
| 3 | **IPO bound** | 33 | 48.7% | Editorial supply is thin: IPO stories on 75% of weekdays, 3 or more on only 17% |
| 4 | **Soonicorns** | 14 | 75.0% | Small n. Strong conversion. Slow moving list, so it is cheap to keep |
| 5 | **Unicorns** | 16 | 52.4% | Static list. Works as browse furniture, will not drive repeat visits |
| 6 | Early fundraisers | 21 | 40.9% | Keep as a browse all filter, not a home section |
| 7 | Profitable startups | 2 | 33.3% | Cut from home. Filter only |
| 8 | Watchlist row | 5 | 62.5% | One row that deep links into Profile. Not a section |
| — | Browse all companies | — | — | Last unit on the page, opens the filter page |

**Two orderings, and the difference matters.** By demand the order is recently funded, just
launched, IPO bound. By conversion it is soonicorns, just launched, recently funded. Recently
funded wins on demand by 3x and converts at 50%, so it leads. But **just launched deserves
position 2 rather than the lower slot its raw traffic suggests**: it converts at 73%, the best on
the tab, which reads as an under exposed section rather than an unpopular one.

**Personalised section order by persona type** was raised in the room and is already written into
v3. Leave it there. The base order above should ship unpersonalised on 15 Sep so there is a
clean baseline to measure personalisation against later.

### 4.2 Browse all companies

| Question from the room | Answer |
|---|---|
| Table or non table | Non table. Cards with pills, consistent with the rest of the app |
| Which data points on the card | Three fixed: name, sector, location or last funding date. Same three on every card, no exceptions |
| What if a filtered field is missing on a card | This is the real trap. If a user filters by funding and some cards show a funding figure and others do not, the page looks broken. Rule: a card only enters a filtered result if the filtered field has a value. Enforce at query level, not at render level |
| Fallback | Per row, within a fixed card shell: if the lead metric is missing, substitute the next in a fixed priority order. Never change card height or shape per row |
| Entry from a home section | "View all" on a section opens browse all with that filter pre applied |
| Section header tap | Scrolls to the section. It is navigation, a table of contents, not a filter. Do not style it as a filter |

Card shell stays fixed and only the lead metric varies. That is what Crunchbase, Tracxn, CB
Insights and LinkedIn all do, and the structurally different per signal card has no precedent at
scale. This was already resolved in the Explore card work.

### 4.3 The data check that must happen before Recently funded ships

DataLabs `last_funding_date` was compared against the publish date of every Inc42 funding article
with a tagged company, 178 articles, 135 comparable after removing unprobed slugs and pages with
no funding date.

| Result | Figure |
|---|---|
| Median lag | 0 days |
| DataLabs date within 7 days of the article | **79%** |
| Within 30 days, and within 90 days | 79% and 79%. Nothing lands in between, so it is synced or it is badly stale |
| More than 365 days stale | **13%** |
| Article had a company with no DataLabs funding date at all | 7 of 178 |

Worst live examples: SUGAR Cosmetics, article 4 Sep 2026, DataLabs last funding 23 Jul 2025.
Comet, article 4 Sep 2026, DataLabs 1 Jul 2024. Medulance, article 4 Sep 2026, DataLabs
16 Apr 2024. Ather Energy, article 21 Jul 2026, DataLabs 13 Aug 2024.

Utkarsh's 87% is the probability that a **funding amount exists** on a row. This is a different
question: whether the **funding date is current**. About one funding round in five that Inc42
itself reported is not reflected in the field the section will sort on.

**Consequence:** "Recently funded" sorted on `last_funding_date` will omit roughly 1 in 5 recent
rounds, including some Inc42 published on the front page the same week. Two options, and this is
a Ranjith or Prapti call, not a design call:

| Option | Effect | Cost |
|---|---|---|
| A. Sort on DataLabs `last_funding_date` as planned | Ships 9 Sep. Section is right about 79% of the time and occasionally omits a company whose funding story is live on the News tab | Zero |
| B. Union DataLabs with funding articles from the last 30 days, dedupe on company | Section matches what the app is publishing | Needs one backend join, and Anmol is already the sequential dependency |

Recommendation: **A for 15 Sep, B logged for the next release**, with the gap written down rather
than discovered by a reader who sees a funding headline on News and a 2024 date on Companies.

---

## 5. Tab set: the Streak versus Watchlist number needs one correction

The room moved Watchlist under Profile on roughly 15% usage and kept Streak top level on roughly
20 to 25%. Both figures are real. They measure different things, and the comparison as stated
does not hold.

| Surface | Users, 90d | Repeat (2+ days) | Reach among returning users | Median events per user |
|---|---|---|---|---|
| Watchlist viewed | **940** | 142 | **82.7%** | 1 |
| Watchlist entity added | 103 | 15 | 11.6% | 2 |
| Streak opened | **201** | 35 | **21.6%** | 1 |

- The 20 to 25% Streak figure is correct, on returning users. Confirmed at 21.6%.
- The 15% Watchlist figure matches **adding to a watchlist** (11.6%), not visiting the tab.
  The tab itself is visited by 82.7% of returning users, 4.7x Streak's reach.

So Watchlist is not a low traffic tab. It is a **high traffic empty tab**: 940 users opened it,
103 ever put anything in it, and the median user opens it once and never returns.

This does not reverse the decision. Moving Watchlist under Profile is still right, because a tab
that 89% of its visitors leave empty should not hold a quarter of the nav. But it changes the
reasoning and it changes what has to ship with it:

| Implication | Action |
|---|---|
| Watchlist has real pull. Burying it with no entry point loses that | Watchlist row on Companies home, plus an add control on every company card and profile |
| The problem is emptiness, not location | Profile watchlist needs a real first run state that suggests companies, not a blank list |
| Streak is the weaker of the two on every measure: 201 users against 940, 35 repeat against 142 | **Streak holding a top level tab over Watchlist is not supported by the data.** It is defensible as a deliberate bet on gamification, which is what the room said. Make that the stated reason, not usage |
| For context, the 44% brief non open figure holds | 1,119 users reached the brief page, 611 opened a brief, so 45.4% never opened one. Unchanged |

Recommendation for 15 Sep: **News, Companies, Streak, Profile**, unchanged. Streak stays on the
stated intent to gamify, with the usage claim corrected. Re-check after 30 days on the app with
the split above.

---

## 6. Search

| Decision | Detail |
|---|---|
| Stays global | One search brain, one entry point. Not a fifth tab |
| More prominent on Companies | Justified: search leads to a company profile and company search is a specific intent behaviour. 172 users searched in 90 days, 19.9% of returning users |
| How prominence increases without a new tab | Profile moves out of the header, which leaves Streak and search there. On Companies, render a full width search bar instead of an icon. On News, keep the icon |
| Ranking bias | Same index, context weighted. Companies first on the Companies tab, articles first on News |
| Blocker | Zero result rates were 31.5% on companies and 32.6% on articles. A more prominent search bar on Companies raises the number of people who meet that. **Prominence and the search fix must ship together, or prominence makes it worse** |

Combining search with Ask was discussed and is explicitly out of scope for this release.

---

## 7. Tags and short display names

Long sector names that break the card, with options. Pick one column.

| Full name | Option A (shortest) | Option B (keeps the pair) | Option C |
|---|---|---|---|
| Advanced Hardware & Technology | Hardware | Hardware & Tech | Deep Hardware |
| Media & Entertainment | Media | Media & Ent | Media |
| Clean Tech / Climate Tech | Climate | Clean Tech | Climate Tech |
| Manufacturing Solutions | Manufacturing | Manufacturing | Factory Tech |
| Consumer Services | Consumer | Consumer | Consumer |
| Enterprise Services | Enterprise | Enterprise | Enterprise |

Recommendation: **Option A**, with a hard 14 character display cap and the full name kept for the
sector landing page and for search. One display name per sector, used everywhere, so a reader
learns it once.

Other tag rules confirmed in the room:

- Tags keep tag styling. Familiarity beats cleanliness here.
- Article page shows the **primary** sector only. Tertiary sector tags are appearing today and
  should not.
- Two line tags are a real case on the long names above and must be designed for, not avoided.

---

## 8. Onboarding

Interest and sector is the one field that cannot be enriched, so it has to be asked. What it
should drive:

| Surface | Use |
|---|---|
| News | Reorder the topic sections and the latest rail. Not a visible sector strip |
| Companies | Reorder the sections. A user who picked fintech sees fintech heavy rows inside Recently funded |
| Brief | Existing ranking formula, unchanged |

Do not use it for articles only. That is the gap the One Inc42 session flagged.

---

## 9. Open decisions, for Ranjith

1. **Top strip on News: topic or sector.** Section 3.1. Recommend topic. This is the only
   recommendation here that contradicts the room.
2. **Recently funded sorting: option A or B.** Section 4.3. Recommend A now, B next release.
3. **Streak justification.** Section 5. The tab can stay, but the usage argument for it does not
   hold against Watchlist and should not be repeated in the stakeholder doc.
4. **Search prominence on Companies is gated on the search fix.** Section 6. Confirm both land in
   the same build or hold the prominence change.
5. **Sector short names.** Section 7. Pick a column.

---

## 10. Design handoff checklist for Satya

In the delivery order agreed in the room.

| # | Screen | Must include |
|---|---|---|
| 1 | Article page | Readability fix: tighter line height, tighter paragraph spacing. Primary sector tag only. Two line tag case. Summary block resized |
| 2 | News home | Topic strip. Hero with description from summary bullet 1. Latest rail. Deals. Companies in today's news. In-Depth. 1 row and 0 row states for every rail. Weekend state at 3 articles |
| 3 | Companies home | Sections in the order in 4.1. Horizontal rails, not a vertical feed. Section header as navigation. Full width search bar. Watchlist row deep linking to Profile. Browse all as the last unit |
| 4 | Company profile | UI refresh only. New font, colour, radius, spacing. No UX change. No web view |
| 5 | Brief | Last. Unchanged scope this round |

Cross cutting for every screen: single primary red derived from the logo, tested on a standard
screen template across displays. Serif and sans pairing. Flatter toggle pill, depth reduced.
Floating bottom strip with four tabs.

---

## 11. Out of scope for this round

Company profile UX (v3). Personalised section ordering (v3). Brief FOMO redesign. Search and Ask
combination. Newsletter as its own News section. Continue reading section, event only this round.
Asana tickets. Web view shell, rejected.

---

## Appendix: figures that were corrected

| Claim in the room | Measured | Where |
|---|---|---|
| Watchlist about 15% | 82.7% of returning users view it, 11.6% ever add to it | 5 |
| Streak 20 to 25% | 21.6% of returning users. Correct | 5 |
| People use development tags more than sector in filters | True. Sector is not in the filter row at all, and sector landing reaches 7.5% of returning users | 2, 3.1 |
| Recently funded has 87% data | 87% is amount coverage. Date currency is 79%, and 13% is over a year stale | 4.3 |
| 44% never open the brief | 45.4% of brief page visitors never open a brief | 5 |
