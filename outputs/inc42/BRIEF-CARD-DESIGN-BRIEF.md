# Design brief — Inc42 app, the Brief entry screen

You are being asked to design one mobile screen. Read all of this before designing.
Nothing here prescribes a solution. It describes the product, the data that exists,
the behaviour observed, the constraints, and the approaches that have been rejected
and why. The design decisions are yours.

---

## 1. What Inc42 is

Inc42 is an Indian startup media company. It has two products relevant here:

- **Editorial** — a newsroom publishing startup and technology news at inc42.com.
  Roughly 16 articles on a weekday, 4 on a weekend day.
- **Inc42 DataLabs** — a startup intelligence platform at inc42.com/datalabs, with
  company, investor and industry profiles. 75,000+ startups, 3,000+ investors,
  20,000+ funding rounds, 400+ sectors. Company pages sit on the same domain at
  `inc42.com/company/{slug}`. There is a free tier (search, live signals, preview
  metrics, saved lists) and a paid tier at ₹1,499/month (full P&L, MCA filings,
  cap table, exports, verified contacts).

The mobile app went live on Google Play in August 2026 and on iOS shortly after.
It has three tabs: **Brief**, **Explore**, **Watchlist**.

---

## 2. What "the Brief" is today

Every morning at 07:00 IST the app publishes a **Brief**: a set of up to 8 news
stories selected and ordered for that specific user. The user taps through them one
at a time like a deck of cards. On finishing, a streak screen appears.

The **Brief tab's landing screen** is what you are designing. It currently contains a
card that represents today's Brief, plus some other modules. Tapping the card enters
the deck.

The cut-off is 07:00 to 07:00 — the Brief covers the previous 24 hours and does not
update during the day.

---

## 3. The problem

Two measured failures:

1. **44% of person-days that visit the Brief tab never open the Brief at all.**
   People land on this screen and leave without entering.
2. **Card 1 → card 2 advance is 45%.** Of those who do enter, over half leave at the
   first story. (There is no fatigue curve after that — cards 2 through 8 advance at
   77–87%.)

The screen you are designing is the first of those two problems.

Additionally, the product owner reports that the screen does not communicate what a
"Brief" is. Users cannot answer "what is this?" — a critique also raised in an
external app teardown.

---

## 4. The questions the screen is expected to answer

These are the product owner's words, unedited:

> What is Brief? Is this personalized? Is this everything that I need to know?
> What is inside? What is the card for me? How is it relevant for me? How do I ensure
> that I'm getting a FOMO that I should not miss reading this? How do I ensure that
> this is built for me?

And separately:

> How do we ensure this is not just an article? This is a series of news that we have
> curated for you, and you should not miss it out. That is what people should
> understand when they look into these things.

---

## 5. The ranking logic (how the 8 stories are chosen)

This is implemented. You are not being asked to change it, but the screen can only
truthfully describe what it produces.

**Inputs from the user:** a set of followed Topics, and a set of followed Sectors.
**Inputs from each article:** a Development Type (mapped to a topic), Company
Industries (mapped to a parent sector), and a published timestamp.

```
TopicAff  = 1.0  if the article's topic is in the followed topics
          = max(affinity[t -> article topic]) over followed topics, otherwise
          = 0    if the user set no topics, or the article has no topic

SectorAff = sum over each unique parent sector in the article of
            (ParentMultiplier x ParentAffinity)
  ParentAffinity   = 1.0 if that parent sector is followed
                   = max(affinity[s -> parent sector]) over followed sectors
                   = 0 if the user set no sectors
  ParentMultiplier = 1 if the article has one unique parent sector
                   = the number of unique parent sectors, if more than one

Pop   = 0.5 x topicPopularity + 0.5 x sectorPopularity
score = 1.0 x TopicAff + 0.6 x SectorAff + 0.15 x Pop
```

Sorted by score descending, then by published time descending.

**Popularity** is audience size over the last 90 days, normalised so the largest is 1.0:
- Topics: News 1.000, Deals 0.759, Financials 0.252, Trends 0.164, Regulatory 0.123,
  IPO 0.116, Team 0.092, Startups 0.023
- Sectors: Consumer 1.0, Fintech 0.75, Ecommerce & D2C 0.69, DeepTech 0.64,
  Enterprise & SaaS 0.52, Startup Ecosystem 0.50, AI 0.23

**Editorial override:** any article can be flagged "App Featured Article = Yes". Those
are placed above everything else, ordered by publish time. Everything else follows the
score.

**Topic map (parent -> child development tags)**
News: Business Updates, Cohort Launches, Controversies ·
Deals: Startup Funding & Investments, Fund Launches, Startup Mergers & Acquisitions ·
Trends: Industry Trends, Business Models & Strategy · IPO: Startup IPO ·
Regulatory: Government & Policies · Team: People & Culture, Startup Layoffs ·
Startups: Startup Discovery · Financials: Startup Financials

**Sector map (parent -> child sectors)**
Ecommerce & D2C: Ecommerce, D2C, Logistics ·
Consumer: Consumer Services, Foodtech, Media & Entertainment, Travel Tech, Edtech, Health Tech, Agritech ·
Fintech: Fintech, Cryptocurrency, Digital Brokerage, Insurance Aggregators, Web3 ·
Enterprise & SaaS: Enterprise Services, Enterprise Tech, Cybersecurity, Real Estate Tech ·
AI: AI, AI Governance ·
DeepTech: Clean Tech / Climate Tech, Space Tech, Semiconductors, Advanced Hardware & Technology, Manufacturing Solutions, Electric Vehicles ·
Startup Ecosystem: Startup Ecosystem

**Two known properties of this formula, stated as fact:**
- There is **no story-level importance signal**. `Pop` is a per-category constant, so
  every `Startup IPO` article scores identically on that term whether it is a ₹8,010 Cr
  filing by a late-stage company or a seed-stage company saying it may list in 12–18
  months. Two articles with the same topic and sector receive the same score and are
  separated only by recency.
- `ParentMultiplier` makes SectorAff scale as n² x average affinity, so an article
  tagged into two or three unfollowed sectors can outscore an article in the user's
  actual followed sector.

---

## 6. The content — measured, not assumed

Source: 1,179 articles from the Inc42 WordPress REST API, 6 June – 4 September 2026,
plus an 809-article editorial tagging audit (5 June – 20 August 2026).

**Files provided** (in `~/ClaudeDocs/inc42/brief-data/`):
- `articles_90d.csv` — 1,179 rows: id, date, title, url, development_type,
  primary_industry, primary_company, second_company, parent_category, story_type,
  company_type, shelf_life, user_needs, impact_score
- `days_90d.csv` — 91 rows, one per publishing day: published count, how many carry a
  company / development type / industry, and that day's Daily Brief newsletter title
- `article_summaries.json` — the 2–3 summary bullets per article that the story cards use
- `corpus90.json`, `rows809.json`, `impact.json` — the raw pulls

**Volume**
| | |
|---|---|
| Weekday median published | 16 |
| Weekend median published | 4 |
| Days publishing fewer than 8 | 23% |
| Days publishing exactly 1 | 10% |

**Field coverage — this is the constraint that has broken most attempts**
| Field | Missing |
|---|---|
| primary_company | **27% have none**; 5% have two; 0.1% have three |
| sector (after best-effort roll-up) | 24% |
| development_type | 15% |
| summary bullets | 7% |
| a currency figure in the headline | 53% (present on Deals 82%, Financials 89%, IPO 56%, News 31%, Team 5%) |
| company_type | 15% (Late Stage 23%, Listed 22%, Growth 12%, Early 12%, International 7%) |
| `sentiment__tonality` | **unusable — "Positive" on 1,178 of 1,181 articles, including every controversy and layoff** |
| shelf_life | 90% is the default "3 Days" |
| story_type | Exclusive 4%, Follow Up 6%, Series 11%, "Others" 64% |
| parent_category | News 84%, In-Depth 12%, Startup Stories 4% |

**Sector supply — % of weekdays with ZERO stories in that sector**
Ecommerce & D2C 2% · Consumer 5% · Enterprise & SaaS 14% · Fintech 18% ·
DeepTech 39% · **AI 50%** · Startup Ecosystem 100% (never populated in the sector field)

**Topic supply — % of weekdays with ZERO stories in that topic**
News 2% · Deals 7% · IPO 25% · Financials 32% · Regulatory 36% ·
Trends 64% · **Team 73%** · Startups 100%

**How often a user gets a direct match** (at least 1 of their 8 in a followed topic or sector)
| Follows | Days with ≥1 match |
|---|---|
| Consumer + News | 87% |
| Fintech + Deals | 87% |
| DeepTech + Regulatory | 61% |
| **AI only** | **20%** |
| **Team only** | **13%** |

**Repeat coverage of the same company**
- 98% of weekdays contain at least one story about a company also covered in the prior
  30 days; median 3 of the 8.
- But the **top-ranked** story is such a company on only **48%** of weekdays, and a
  company seen **twice or more** on only **32%**.

**What the top story of a weekday actually is**
Startup IPO 31/65 · Funding 18/65 · M&A 11/65 · Financials 3/65 · Controversies 1/65.
By company stage: Late Stage 40, Listed 14, Growth 7, Early 4.

**The newsroom's own daily title**
Inc42 publishes a post tagged "Inc42 Daily Brief" at ~08:00 on **62 of 65 weekdays**,
never at weekends. It carries a two-clause editorial title, e.g.
*"RentoMojo Files RHP, Uber India Axes 200 Jobs & More"*,
*"Zepto's New Game Plan, Layoffs At Zomato & More"*.
**Caution:** it is not aligned to the ranking. On 11 June the title was *"ZEE5's Sports
Era Begins Tonight, Crisis Deepens At WinZO & More"* and neither story is in that day's
top eight by any ranking. On 18 June, 13 stories were published and there is no Daily
Brief post at all.

**Two example days, to design against**
- *A big day* — Monday 8 June, 12 published. Top story: "Zepto Files UDRHP, Plans
  ₹8,010 Cr Fresh Issue". Also: Aye Finance $15 Mn debt, Klassroom SME IPO approval,
  Curefoods IPO on hold, GPS Renewables ₹635 Cr, Immuneel ₹100 Cr, Kuku FM microdrama
  IPO analysis, Inc42 AI Summit round-up.
- *An ordinary day* — Thursday 11 June, 9 published, no IPO, no well-known company.
  Ethereal Machines $28.5 Mn, 4baseCare ₹38 Cr, ADIA offloads ₹1,900 Cr of Lenskart,
  Manam Chocolate $9 Mn, OneAssist AI analysis, IN-SPACe funds three spacetech
  startups, Opendoor lays off its entire 250-person India team, 3one4 Capital on AI.

---

## 7. What DataLabs can add to the screen

Company pages are free to view and carry, for example (Zepto, verified 5 Sep 2026):
sector and sub-sector, city, founded year, founders, **total funding $2.45 Bn**,
**revenue ₹4,178.3 Cr FY24, +101% YoY**, 39 investors, **employees 19,938, +6.55%
over 90 days**, **web traffic 2.44 Mn, −2.21% over 30 days**, plus full P&L, balance
sheet, cash flow and ratios, and a "Recent Stories" list linking back to editorial.

The DataLabs team updates a company profile **within 24 hours** of a story about it.
So on the day a story breaks, the profile may not yet reflect it.

Note: "DataLabs" is an internal product name. The app's audience arrives from media.

---

## 8. Observed app behaviour (PostHog, 21 days, 788 users, 1,650 person-days)

| | |
|---|---|
| Brief-tab visits per person-day | **4.0** |
| Person-days that visited but never opened the Brief | **44%** |
| Person-days that completed the Brief | 25% |
| Of completers, returned to the Brief tab afterwards | 85% |
| Card 1 → card 2 advance | 45% |
| Cards 2–8 advance | 77–87% |
| Median time in a completed Brief | 78 seconds |
| Users who open the full article and return to the deck | 6% |
| D1 retention | 26–43% · **D3 falls to 7–21%** |
| Push notifications ever delivered | **zero** — the 07:00 cue does not currently exist |
| Past briefs | 30% of users open one; median 2 days back; briefs are retained 7 days |

---

## 9. Constraints

- **Work only in the Figma file "App - Draft Screen", file key `dAsaTgNj0xh25w2OGaurZo`.**
  Never touch the live file "Inc42-App-2026" (`vKuPUMuhLos0rC1AFR5cWq`).
- Deliver **screens** — mobile, 390px wide. Not components, not a design system.
- Brand accent colour is `#EA4B2B`. The product owner has said he does not want heavy
  use of orange, and separately that the result should still feel like Inc42.
- The app's existing type is Inter. Other faces are available in Figma and may be used.
- The app has a three-tab bottom navigation: Brief, Explore, Watchlist.
- Everything on the screen must be renderable from the fields in section 6. If a design
  depends on a field, state its coverage. If it depends on new editorial work
  (a written line per day, a question per story), state that explicitly as a cost.
- The screen must still work on: a day with 1 story; a day where nothing matches what
  the user follows; a user who set no preferences; a user who is not logged in; an
  article with no company; an article with two companies; a company with no logo.

---

## 10. What has been tried and rejected, and the reason given

Every item below was built and shown. The reason is the product owner's, paraphrased
only for length. They are listed as constraints on the solution space, not as guidance
toward a particular answer.

| Approach | Reason rejected |
|---|---|
| Concept cards built on a big number, a rivalry, a verdict | They assert a property the ranking does not compute, so they only render on days the content happens to cooperate |
| Listing all 8 headlines on the screen | *"If you show everything at a glance, why would people open?"* The screen becomes a substitute for the Brief |
| An index of company names only | Blank on the 27% of articles with no company |
| Stating "8 of the 14 stories Inc42 published today" | *"You cannot say how many articles you published"* — it makes Inc42 look like it publishes very little |
| Marking only the stories that match what the user follows | *"What will happen to the non-highlighted ones?"* The unmarked rows read as filler |
| Leading with one company's history ("your 4th Zepto story") | *"It looks like it is related to Zepto only"* — the whole Brief appears to be about one company. Also measured: this can only lead on 48% of days, 32% for a "3rd story" claim |
| A section titled "Big today, not in your brief" | Implies the Brief is incomplete and invites *"if it is so big, why is it not in my brief?"* |
| A countdown timer as the lead element | *"My only focus goes on the timer"* |
| A static personalised title, e.g. "Your Ecommerce & IPO brief" | Static. Interesting on day one, wallpaper by day two |
| The words "cards", "DataLabs", "10-minute read", "In-Depth" | Internal vocabulary. A reader arriving from media does not know what any of them mean |
| "Expires tonight. Tomorrow arrives at 7 AM." | No subject — what expires, what arrives? |
| A multi-page Brief with sections and a persistent progress bar | Too much on the first screen |
| Onboarding screens | Not asked for; the screen must work on its own |
| Building every variation on the same company | Cherry-picked; not representative of what is published |
| Copy such as "Quick commerce just ran out of private money" | Requires a daily editorial thesis that nobody writes. Not producible at 07:00 every day |
| A photo + headline + standfirst layout | *"If it looks like an article card, people think it is just another article"* |
| Claiming "5 minutes" | Not believed, and not felt |
| Not using the word "brief" | The concept is never positioned. *"We want to position brief as a concept"* |
| Dense screens generally | *"If you dump too much content, eye-fitting happens and people miss it"* — but also, separately, several screens were called *"too simple"*. The stated want is a balanced screen |

One attempt not yet rejected, recorded as information rather than recommendation:
a story-level impact score was constructed from development type, company stage,
the figure in the headline, and editorial flags. On the 1,179-article corpus it
produces a clearly dominant story on 57% of weekdays and no dominant story on 25%.
Adding it to the ranking at weight 0.4 raises the rate at which the day's
highest-impact story reaches the personalised Brief from 30–73% to 97–100%, without
displacing followed topics from the lead. It is not implemented.

---

## 11. What to produce

Screen designs for the Brief tab's landing screen, in the draft Figma file. For each:

1. State which day it is designed against (use a real day from `days_90d.csv`).
2. State, field by field, what it renders and the coverage of each field used.
3. State what it does on the failure days listed in section 9.
4. State any new content or editorial work it would require, and how often.

Do not assume any data not listed in section 6. If you want a field that does not
exist, say so explicitly rather than designing as if it does.
