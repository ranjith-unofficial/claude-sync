# The brief page: four sections

Working spec, 6 September 2026. Owner: Ranjith.

This document covers the four sections that make up the brief page, in the order the reader
meets them:

1. The brief card
2. Past briefs
3. Companies in today's brief
4. Recommended for you

For each section it records what the section promises, what data actually exists to keep
that promise, how the section behaves when the data is missing, and what is still open.

Every figure here is measured, not estimated. Where something has not been measured, it says so.

---

## Method

All coverage figures come from a 90 day corpus of **1,179 articles published 6 June to
4 September 2026**, covering 91 days and 65 weekdays, pulled from the WordPress REST API
with ACF fields. Company data comes from checking all **443 tagged company slugs** against
their DataLabs pages on inc42.com/company/{slug} on 6 September 2026.

Brief level figures come from simulating the real brief through its locked windows and caps
across **84 brief days and 9 reader personas, so 756 briefs**.

Two words are used precisely throughout:

- **Article weighted** means weighted by how often Inc42 writes about a company. A company
  written about 18 times counts 18 times. This is the right lens for anything the reader sees.
- **Company weighted** means each company counted once. This is the right lens for a data
  backfill task.

Source files are in `~/ClaudeDocs/inc42/brief-data/`.

---

## A note that applies to all four sections

The brief page is not a feed. Each section makes a promise in its heading, and the reader
learns that promise within about three days of use. A section that changes its name, appears
on some days and not others, or shows an empty state, breaks the promise and costs more than
the missing content was worth.

So the rule across all four sections is the same: **the section is fixed, the rows degrade.**

---

## 1. The brief card

### What it is

The entry point on the home screen. It stands for the whole brief and has to be worth tapping
before the reader has seen anything inside.

### What data exists

| Field | Coverage | Verdict |
|---|---|---|
| `summary`, three bullets | **93%** | The most reliable content asset Inc42 has |
| `development_tag` | 85% | Usable as a row eyebrow |
| `companies` | 73% | Enough for the watchlist hook |
| `sector` | **58%** | Currently the card's eyebrow, blank on 42% of stories |

Within the summary, bullet 1 repeats the headline. Its median overlap with the headline is
50% of words, and only 11% of bullet 1s add a number the headline does not already have.
**Bullet 2 is the only line a headline cannot carry.** It is the interpretation line, and it
is forward looking on 27% of articles against 8% for bullet 1.

56% of articles have no "so what" line in any bullet. The cause is visible in the CMS:
`user_needs` is set to "Inform Me" on 715 of 750 articles, or 95%. Inc42 publishes news of
record, so a why it matters line cannot be promised per story.

### What does not work

Two of the three stat tiles in the current design are uncomputable on real data:

| Tile | Reality |
|---|---|
| "₹2,900 Cr moved today" | Median ₹239 Cr, and **₹0 on 14% of weekdays** |
| "3 IPO filings" | Median 0, and **zero on 59% of weekdays** |
| "6 sectors" | Median 6, never zero, but carries no reader value |

Tiles that never hit zero: distinct companies (median 13), story types (median 6), biggest
single transaction (median ₹3,371 Cr).

There is a trap in any money tile. The first implementation surfaced total addressable market
and cumulative tracker numbers rather than money that actually moved, and **11 of the top 12
picks were false**, including a cumulative unicorn valuation and a 2030 government export
target. Any money extraction has to exclude market sizing language, cumulative trackers,
multi company roundups, and income statement figures.

### The real defect

The card's hero company appears in its own three teaser rows **only 28% of the time**, because
the rows are sorted by recency. The card announces one story and then shows three unrelated
ones. This is a ranking problem, not a summary problem, and no card treatment fixes it.

### Decided

- The card leads with the summary, not the sector eyebrow.
- No aggregate money tile until the filters above are applied.
- Row ordering must follow the hero.

### Open

- Whether bullet 2 alone can carry the card, given it exists on 93% of articles but is only
  forward looking on 27%.

---

## 2. Past briefs

### What it is

The archive. Every brief the reader has and has not opened, so a missed day does not feel like
a lost day. This is the section that makes the streak mean something, because a streak with no
way to see what you missed is only a punishment.

### What data exists

Supply is the one thing that is never a problem here. There is **exactly one brief per day,
seven days a week**, with no gaps. A week always has seven, a month always has about thirty.
The 90 day corpus covers 84 brief days with no missing day.

Every brief already knows: its date, its story count, its read state per story, and its
completion state. These come from the brief generator and from `brief_completed`, which the
streak is already tied to.

### What is not measured

This section has had no analysis. Specifically unmeasured:

- How far back readers actually go. Nobody has looked.
- Whether an unopened brief from four days ago has any pull, or whether the archive is
  really a two day window with a long dead tail.
- Whether partially read briefs draw people back more than untouched ones.

These are answerable from PostHog once the section exists, and not before. They should not
hold up building it, but they should be instrumented from day one.

### Design consequences that follow from the data

- **Do not paginate deeply.** Seven days is a week, and a week is the unit readers think in.
  Anything past that is a "see all" affordance, not a scroll.
- **Show completion, not recency.** "6 of 8 read" is the state that brings someone back.
  A date alone does not.
- **The Sunday recap and the Monday weekend brief are structurally different** from a weekday
  brief. The Sunday recap covers Monday 7am to Saturday 7am and holds up to 10 stories drawn
  from a pool of around 70. Monday covers the weekend. Both need to look different in the
  archive or they read as duplicates of days already seen.

### Open

- Whether an unread brief expires. The brief copy currently says "This brief is only for
  today", which sits awkwardly with an archive that keeps it forever.

---

## 3. Companies in today's brief

### What it is

The companies named in the stories the reader just read, each with a number that explains why
they are in the news.

### Supply

This section is built from the **eight stories that survive the brief cap**, not from
everything published that day. That distinction halves the numbers, and earlier analysis got
it wrong by using the wrong denominator.

| | Per brief |
|---|---|
| Companies in the section | **Median 6, minimum 2** |
| With the number matched to the story | **Median 4** |
| With some number | Median 5 |
| With no DataLabs page | Median 1 |
| Sunday recap | **7 companies**, not 49 |

**30.1% of the stories that reach a brief carry no company tag at all.** That is two to three
of the eight, every day, concentrated in policy stories (93% untagged), industry analysis
(70%), roundups (50%) and In-Depth pieces (42%).

The section can effectively never be empty. Across 756 simulated briefs, **exactly one had
zero companies**, or 0.13%. It was a reader who follows only Regulatory, on the Sunday recap
of 9 August, where every story was a policy story. Fewer than three companies happens on 3.4%
of briefs overall, rising to 7% for a Regulatory only follower.

The section cannot empty by accident. It can only empty through narrow personalisation, which
is a ranking problem and is fixed by capping how monotone a brief is allowed to be.

### The data point per story type

The number to show is decided by **what the article is about**, never by the company's sector.

| What the article is about | Articles | % | Show | Have it | With fallback |
|---|---|---|---|---|---|
| Funding | 197 | 24% | Total funding raised, investor count | 78% | 82% |
| Financials | 111 | 14% | Revenue and year on year, financial year labelled | 75% | 92% |
| Analysis, In-Depth | 102 | 13% | Full profile | 66% | 91% |
| IPO | 94 | 12% | Total funding raised, revenue | 65% | 82% |
| Product, launch | 58 | 7% | Web traffic | 79% | 84% |
| Legal action | 54 | 7% | **Nothing exists** | 0% | 85% |
| Stake sale | 39 | 5% | Market cap, **not available**, using total funding | 95% | 100% |
| M&A | 39 | 5% | Total funding raised | 79% | 92% |
| Stock move | 34 | 4% | Market cap, **not available**, using revenue | 88% | 100% |
| Leadership | 27 | 3% | Headcount | 96% | 96% |
| Fund launch, VCs | 17 | 2% | **Nothing useful exists** | 0% | 65% |
| Regulatory approval | 9 | 1% | **Nothing exists** | 0% | 89% |
| Layoffs | 6 | 1% | Headcount | 83% | 100% |
| Shutdown | 6 | 1% | Headcount | 50% | 83% |
| **Total** | **810** | | | **67%** | **87%** |

Three readings of this table:

1. **Four types cover 63% of all company mentions**, and all four land between 65% and 78%.
   Build for Funding, Financials, Analysis and IPO first.
2. **Three types have no possible data point, ever.** Legal action, regulatory approval and
   business update are 8% of mentions. No field will ever exist for "got sued".
3. **Stake sale and stock move look strong but show the wrong number.** The correct figure is
   market cap, which is not on the DataLabs company page. That is 9% of mentions carrying a
   plausible looking but mismatched number. It should come from the listed company tracker.

**Headcount is the universal fallback.** It is present on 86.9% of tagged companies, article
weighted, ahead of total funding at 74.8% and revenue at 68.5%.

### Decision: show the value, not the trend

Trend deltas are dropped. Rows show the plain figure.

The supporting numbers: headcount itself is on 86.9% of tagged companies, but its 90 day trend
is on 80.6%, and web traffic's 30 day trend is on 79.1%. So a trend is missing on roughly one
row in five that has the underlying value. A trend cannot be a fixed part of the row without
either a hole or a second fallback inside an element that is already a fallback.

The tradeoff being accepted: a headcount of 681 says less than 681 down 0.7%, and the layoff
case in particular loses some of its force. Revisit if DataLabs trend coverage improves.

### The three row states

There are three, not four. Across all 367 companies with a DataLabs page, **not one has a page
carrying zero numbers**. If the page exists, it always has at least one figure.

| State | Share | What the row shows |
|---|---|---|
| 1. Matched | 71% | Name, sector, reason chip, the number that answers the chip |
| 2. Any number | 16% | Name, sector, chip, whatever profile numbers exist |
| 3. Name and chip | 13% | Name and chip only, no data line |

State 3 is almost entirely a slug mismatch problem rather than missing companies. Blinkit,
Reliance Jio, Cult.fit, Cashfree, Fibe, Atomberg and PRISM all exist in DataLabs under
different slugs. **Storing the company UUID on the article instead of a text slug takes state 3
from 13% down to about 4%, and lifts matched coverage from 71% to roughly 84%.**

Degradation happens per row. It never changes the section heading, the section's presence, or
the layout. No row ever says "no data available".

### The freshness rule

Measured against DataLabs' own `last_funding_date` for every funding story in the corpus:

| Article age | Round is in DataLabs |
|---|---|
| 0 to 2 days | **0%** |
| 3 to 7 days | 86% |
| 8 to 30 days | 74% |
| 31 to 60 days | 73% |
| 61 days and older | 82% |

Two separate problems sit inside this. There is a lag of about three days, and there is a
**permanent miss of roughly 20%** where the round never arrives at all. SUGAR Cosmetics'
article ran on 4 September against a last recorded round from July 2025, 408 days earlier.
Medulance is 871 days. Slicepay is 808 days.

The consequence: **on the morning a funding story appears in the brief, DataLabs does not
contain the round the headline is about.**

The fix does not require the sync to be repaired. **The event number comes from the article
headline**, which carries it on **91% of funding and 91% of financials headlines**, together
38% of all company mentions. DataLabs supplies context only, where a three day lag does not
matter. This removes the sync from the critical path entirely.

### Design

Five artboards in Figma, file App - Draft Screen, page Referencing, section `625:17`, built on
three real brief days with real numbers. Not yet reviewed.

---

## 4. Recommended for you

### What it is

Undecided. This section has no agreed definition, so what follows is the supply analysis that
should decide it, and three candidate definitions measured against that supply.

### What supply actually exists

Depth content is scarce:

| | Value |
|---|---|
| In-Depth plus Startup Stories | **181 of 1,179 articles, or 15%** |
| Per weekday | **Median 2, minimum 1, maximum 5** |
| Weekdays with none | **0 of 65** |
| With a real company tag | 56% |
| With a DataLabs sector | 50% |

So depth exists every single weekday, but only two pieces of it. **A section showing four or
five recommendations cannot be filled from a single day of depth content.** It needs either
several days of accumulation or a second pool.

The second pool is real and large. The brief window holds a **median of 17 articles against a
cap of 8**, leaving a **median of 9 stories published but not shown**, with none left over on
only 9 of 84 days. Deep pieces specifically sit in the window at a median of 2, with none on
only 4 of 84 days.

### The finding that constrains this section

Editorial's own `shelf_life` field on depth content:

| Shelf life | Articles | Share |
|---|---|---|
| **3 days** | **110** | **61%** |
| 7 days | 29 | 16% |
| 14 days | 26 | 14% |
| 30 days | 12 | 7% |
| Evergreen | **4** | **2%** |

**Inc42's newsroom marks 61% of its own depth content as stale after three days, and only 4
pieces in 90 days as evergreen.** A "recommended for you" section built as a back catalogue is
therefore recommending content the newsroom has already declared expired.

The corresponding opportunity is in the story type field. **Series accounts for 65 of 181
depth pieces and Follow Up for another 36, so 56% of depth content is explicitly part of an
ongoing thread.** That is a much stronger hook than a back catalogue, and it is already tagged.

### Three candidate definitions

**Candidate A. Continue the thread.**
Recommend the next or previous piece in a Series or Follow Up the reader has already touched.
Supply is 56% of depth content, already tagged, no new classifier needed. It sidesteps the
shelf life problem entirely because a thread is current by definition. It requires read history,
so it is empty for a brand new reader. This is the strongest candidate.

**Candidate B. What you did not see today.**
Recommend from the median 9 stories that were published in the window but did not make the
reader's brief. Supply is excellent, present on 75 of 84 days. It needs no new data at all. The
risk is one Ranjith has already flagged in another context: it implies the brief was incomplete
and invites the question "if this matters, why was it not in my brief?". That objection killed
the "Big today, not in your brief" section, and it applies here unless the framing is clearly
about depth rather than importance.

**Candidate C. More on a company you follow.**
Recommend depth content about a company on the reader's watchlist. Supply is limited: only 56%
of depth content has a company tag and 50% has a sector, so roughly one depth piece per weekday
is addressable this way, and only if it happens to match a followed company. This is a garnish
on A or B, not a section on its own.

### Recommendation

Build **Candidate A as the primary and Candidate B as the fallback for readers with no history**.
A gives a genuine reason for the recommendation that can be stated in the row, which is the
same principle already agreed for the brief itself, where every story carries a reason chip.
B guarantees the section is never empty.

Explicitly do not build a back catalogue. The shelf life data says the newsroom would not stand
behind it.

### Open

- Whether the section shows depth content only, or any unread story.
- How many rows. Supply supports 3 comfortably, 5 only by reaching back two or three days.
- Whether it appears above or below Companies in today's brief. It is the least defined section
  and the most likely to be skipped, which argues for last.

---

## What all four sections need from outside the app

Three of these are CMS and publishing changes, not app work, and they gate sections 3 and 4.

1. **A company UUID on the article, replacing the text slug.** Lifts matched coverage from 71%
   to about 84% and fixes sector coverage at the same time. Highest value single change.
2. **A mention type classifier at publish.** Decides which number a row shows. The existing
   `development_type` cannot do this: its Business Updates bucket alone hides 64 product,
   33 stake sale, 33 stock move and 22 funding stories. Headline rules reached 93% agreement,
   so this does not need to be a model to start.
3. **The headline figure parsed and stored at publish.** Present on 91% of funding and
   financials headlines. This is what makes section 3 correct on day zero.

A fourth item, a DataLabs company API, is the long pole and should be requested now, but
sections 3 and 4 can both be built without it.

The 20% of funding rounds that never reach DataLabs is a real data quality problem and worth
reporting to that team, but it must not be a dependency for shipping any of this.

---

## Open decisions, collected

| # | Decision | Section |
|---|---|---|
| 1 | Can bullet 2 alone carry the brief card | 1 |
| 2 | Does an unread brief expire, given the "only for today" copy | 2 |
| 3 | Where market cap comes from for stake sale and stock move stories | 3 |
| 4 | Whether to exclude investors, corporates and government from the company list, about 6% of mentions | 3 |
| 5 | Definition of Recommended for you | 4 |
| 6 | Row count and position of Recommended for you | 4 |
| 7 | Whether a diversity cap is added to ranking, which removes the only zero company case | 3 |
