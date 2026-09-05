# Brief entry card — built from field coverage, not from a good day
5 Sep 2026 · draft file row F (y=77000) · four real days from the corpus

## What I assumed, and what the data says

Source: the 809-article master (5 Jun – 20 Aug 2026, 61 publishing days) from the sector-tagging
audit workbook, plus a fresh 1,179-article pull of `structure_data` from the WP API (6 Jun – 4 Sep).

| I assumed | Measured | Consequence |
|---|---|---|
| Every article has a company | **27% have none.** 67% one, 5% two, 0.1% three | The entity index in row E is blank on a third of rows. Dead. |
| One company per article | 5% carry two; **33% of days** have at least one such row | Chips must render "Beco · HUL", not pick one |
| Sector is an article field | `primary_industry` in WP is **null on 86%**. The sector the ranking uses comes from the company master, which is itself missing on 81 of 340 companies | SectorAff is 0 on ~24% of rows *after* best-effort roll-up |
| A followed sector usually has something | AI: **zero on 50% of weekdays.** DeepTech 39%. Startup Ecosystem never lands in the sector field at all | An AI follower has a *direct* match on 20% of days. "Nothing in AI today" would be the majority screen |
| Topic is near-universal | 15% have no development tag. Team zero on 73% of weekdays, Trends 64%, Regulatory 36%, Financials 32%, IPO 25% | Any slot keyed on a specific topic is optional |
| 8 stories a day | Weekday median 16, weekend median 4; **23% of days have fewer than 8** | Count must be true, never padded |
| Headlines carry numbers | 47% overall — Deals 82%, Financials 89%, IPO 56%, News 31%, Team 5% | "The Number" works on ~half of leads. Ladder tier, not a rule |

Direct-match rate by follower profile (≥1 of the 8 cards in a followed topic or sector):

| Follows | Days with ≥1 direct match |
|---|---|
| Consumer + News | 87% |
| Fintech + Deals | 87% |
| DeepTech + Regulatory | 61% |
| **AI only** | **20%** |
| **Team only** | **13%** |

Caveat: the affinity matrices (topic→topic, sector→sector from the co-read study) were not in the
spec I was given, so every simulation above sets indirect affinity to 0. In production an AI
follower is served the nearest thing at affinity > 0, so the ranking never literally has "nothing"
— which is exactly why the entry must never *say* nothing. I need the two matrices to render the
`CLOSE TO` state truthfully.

## The rule that comes out of this

**A slot may only make a promise its field can keep on ≥85% of days. Below that, the slot must
be able to disappear without leaving a hole — and it must never announce its own absence.**

So "Nothing in AI today" is disqualified twice: it names a followed thing (a <85% field) and it
announces absence.

## The shell — one card, every slot gated

Kept from the live app: orange header, greeting, streak, the brief card with hero image and date,
Past Briefs, Beyond the Brief. Changed: what the card says.

| # | Slot | Field | Coverage | Rule |
|---|---|---|---|---|
| 1 | Hero image, date, `N stories · M min` | article, count | 100% | always. N is the true count; N=1 says "1 story", CTA says "Read today's story" |
| 2 | Personal line `K of N in what you follow` | direct match | 13–87% by profile | **only when K ≥ 1.** When K = 0 the line does not exist. No substitute text |
| 3 | Lead headline | headline | 100% | always, in full. This is the one story given away |
| 3a | Lead kicker | fit → topic+sector → sector → none | 92%+ | `BECAUSE YOU FOLLOW X` if direct; else `TOPIC · SECTOR`; else whichever exists; else no kicker |
| 3b | Lead standfirst | summary bullet 1 | 93% | render if present, collapse if not |
| 4 | Trigger strip `ALSO IN TODAY'S BRIEF` | ladder, below | 97% | names and counts only. Never a predicate. Hidden when the ladder is empty |
| 5 | CTA | — | 100% | always |

### The trigger strip ladder
Fills left to right, max 6 chips, stops when full. The day decides how deep it reaches.

| Tier | Source | Chip |
|---|---|---|
| T1 | followed companies present in the brief | `Groww` (orange) |
| T2 | followed sectors present in the brief | `Fintech` (orange) |
| T3 | any company in the brief — two-company rows emit two chips | `Beco` `HUL` (grey) |
| T4 | topic counts, descending | `2 business updates` (grey) |

Why this is the hook: a core reader at 7am is scanning for *triggers* — a name they know, their
sector, a category that matters to them. Names and counts fire the trigger without spending the
story. "Swiggy · Beco · HUL · Shiprocket · Peeko" tells a D2C operator the brief is theirs today,
and tells them nothing about what happened. The predicate stays behind the tap.

### Backtest — 61 days × 4 profiles

| Profile | Personal line | Fit kicker | Topic kicker | No kicker | Strip ≥3 chips | Strip empty | Reached T4 |
|---|---|---|---|---|---|---|---|
| AI only | 20% | 3% | 89% | 8% | 87% | 3% | 34% |
| Team only | 13% | 0% | 92% | 8% | 87% | 3% | 38% |
| Deals + Fintech | 87% | 38% | 54% | 8% | 87% | 2% | 20% |
| No preferences | 0% | 0% | 92% | 8% | 87% | 3% | 38% |

Every row of every profile renders a complete card. The two "strip empty" days are both Sundays
with a single company-less article — and that is F4, which is still a whole card.

## The four screens (row F)

| | Day | Why it was chosen | What it proves |
|---|---|---|---|
| F1 | Thu 6 Aug — 27 published, heaviest in the corpus | Deals+Fintech follower, 8/8 direct | T2 then T3; the lead's chip is a real fit claim |
| F2 | Thu 20 Aug — zero AI articles | AI-only follower, 0/8 direct | no personal line, no empty state, kicker falls to topic, strip carries `Beco · HUL` and skips two company-less rows |
| F3 | Mon 13 Jul — 6 published, 2 with no company | IPO+Consumer, 1/6 direct | lead has no topic and no bullet: kicker uses sector alone, standfirst collapses, ladder reaches T4 |
| F4 | Sun 21 Jun — 1 article, no company, no topic, no bullet | the floor | only tier-1 fields exist, so only tier-1 slots render. Still a complete card |

## What I still cannot answer without more data
1. **The affinity matrices** — needed to render `CLOSE TO` and to know how often an AI follower's
   lead is "close" vs "popular".
2. **Onboarding completion** — if most users never set topics, the "No preferences" row above is the
   majority experience, and the personal line is a minority feature.
3. **Whether showing the lead headline costs card-2 reach.** The live card shows three headlines
   and the card-1→2 drop is ~50%. My hypothesis is that visible headlines pre-spend the deck, but it
   is a hypothesis. The PostHog flag on the brief card already exists: A = this shell (one headline),
   B = live (three). Measure card-2 reach, not opens.

---

# Row G — the Brief page in three reader states (5 Sep, after Ranjith's constraints)
Draft file row G (y=80200). One real day (Thu 20 Aug), one user (follows Ecommerce & D2C + IPO).

## Constraints taken as fixed
- Brief cut is 07:00→07:00. Nothing on the page updates intra-day. "Since this morning" is dropped.
- "Continue where you left off" already exists; card shows a progress bar and the next personalised card.
- Completion → streak screen. The card afterwards is a receipt, nothing more.
- Modules below the card change with the **day**, not with the visit. First impression is the priority.
- `brief_date` on `brief_opened` will be fixed; not a blocker.

## The two questions the first impression has to answer
1. *Is this for me?* → the **personalisation bar**: 8 segments, orange-outlined = in what you follow, grey = ecosystem. Visible before opening; the same bar carries progress in the continue state and the receipt in the done state. On a zero-match day it is simply all grey — no claim, no apology.
2. *If I finish, will I know what happened in my sector?* → the **promise line** + sub-line:
   "8 of the 14 stories Inc42 published today, picked for you." / "5 in Ecommerce & D2C and IPO, which you follow · 3 the ecosystem is reading."
   Both are 100%-coverage fields (published count, matched count, followed names present). A followed sector with nothing today is never named.

## Companies module — conveying *why*, not just *what*
Rule: **reason first, number second.** Each row = logo · company · chip (`YOU FOLLOW · ECOMMERCE` / `NEWS`) · one fact keyed to the story's development type (Deals → amount raised; Financials → the P&L line; News → the price move). Fact ladder: figure in the headline (47%) → DataLabs field → none (row still renders with the chip). Row renders only if it has a fact **or** a logo. Two-company stories emit two logos, one row. Watchlist/followed rows first. Peeko has no favicon → initial tile.

## The ending — abundance, not scarcity
"That's today. Explore →" was wrong for exactly the reason Ranjith gave: it reads as *this is all Inc42 has.* Replaced by the bridge:
"Inc42 published **14** stories today. Your brief is the 8 chosen for you. The other 6, every company profile and everything from this week are in Explore."
It states supply (true count), explains selectivity (personalisation), and points onward. On a ≤8-story day it becomes "Every story from today is in your brief."

## States
| | Card | Below the card |
|---|---|---|
| G1 unread | hero · promise · bar (0/8) · lead in full · Open | companies · yesterday (only if unread) · today's In-Depth · bridge |
| G2 continue | "Continue where you left off" · bar 3/8 · NEXT UP = company + reason, never the headline · Continue | identical |
| G3 done | ✓ Done for today · bar 8/8 · receipt line | identical |

---

# Row H — eight ways to say the same deal (5 Sep)
Draft file row H (y=84000 → 92600). Each row = Entry · Continue · Done · Thank-you.
Shared content on every row (Thu 20 Aug, follows Ecommerce & D2C + IPO):

| Element | Value | Source / rule |
|---|---|---|
| Header | `INC42` + `● Day 7 · read today to keep it` | streak carries the stake; no greeting, no duplicate date |
| Title | **Your Ecommerce & IPO brief** | followed sectors present today; cap at 2 names + "+n" |
| Promise | "Every Ecommerce & D2C and IPO story from today, plus three the ecosystem is reading." | "Every" when matched ≤ 8 (100% of days for 1 sector, 91% for 2, 41% for 3); otherwise "The 8 that matter most in…" |
| Tone | ● ● ● ● ● ● ● ● + "1 funding round · 1 profit turn · 2 disputes · 4 updates" | derived from `development_type` (85%). **`sentiment__tonality` is "Positive" on 1,178/1,181 — a default, unusable** |
| Who | 6 logos (favicon service), initial tile when none resolves | row hidden below 3 |
| Button | one, black (or outlined). Orange used once per card | — |
| Continue | plain progress bar 3/8, NEXT UP = company + reason (never headline) | — |
| Done | ✓ Done for today · receipt line | streak screen already shown |
| Thank-you | DAY 8 · "That is every Ecommerce & D2C and IPO story from today." · "Inc42 read 14 so you could read 8" | closes the promise the entry made |

| # | Name | Title face | Ground | What it argues |
|---|---|---|---|---|
| H1 | MASTHEAD | Playfair Display Bold 36 | white | the paper: rules, serif, restraint |
| H2 | NEWSLETTER | Newsreader Bold 34 | cream | it is the email, in the app: issue number, thick rule |
| H3 | INK | Fraunces Black 36 | near-black | the only dark option; orange = button only |
| H4 | SANS | Manrope ExtraBold 34 | white | app-native; no dots, names as text |
| H5 | TONE FIRST | DM Sans Bold 32 | white | the day's shape leads — eight tone tiles before the title |
| H6 | COVER | Playfair Black 34 on photo | image | the only one with a picture |
| H7 | STUB | Geist Black; numeral 8 at 84 | paper card | finite and countable — the number is the object |
| H8 | LETTER | Literata Medium 28 | white | the promise *is* the title; signed by the newsroom |

Recommendation: H1 or H4 for the app (H1 if the newsletter identity should carry into the app; H4 if the app should stay sans). H7 is the strongest at "this ends". H6 is the one to test against the live card, since it is the only one that keeps an image.

---

# Row J — the one entry card, and what it does when a field is missing (5 Sep)
Draft file row J (y=93100). Six real days, one card design (H4 Sans, Manrope).

## Slot rules — measured on 61 publishing days

| Slot | Needs | Have it | Fallback 1 | Fallback 2 |
|---|---|---|---|---|
| Stake | a streak | logged-in users | "Log in to keep a streak" | — |
| Date | — | 100% | — | — |
| **Title** | ≥1 followed sector/topic present today | Ecom+IPO 80% · 3 sectors 93% · **AI-only 20%** | `Your X, Y +1 brief` when >2 | **`Today's brief`** — never names an absent sector |
| **Promise** | matched count, published count | 100% | "Every…" (matched ≤ 8) → "The 8 that matter most in…" (matched > 8) → "The eight the ecosystem is reading" (0 match) | "One story today — …" (N = 1) |
| **Who** | ≥3 resolvable logos | **~74%** of days | ≥1 company → **names as text** (13%) | nothing (5%). **Never a row of initial tiles** |
| **Tone** | ≥5 of the cards have a development type | 82% | 1–4 typed → text line only (5%) | nothing (13%) |
| Button | — | 100% | "Read today's story" when N = 1 | "Read yesterday's brief" when not ready |
| Not ready | `brief_not_ready` (real PostHog error type) | — | replaces title/promise; hands over yesterday's | — |

## The six days
| | Day | What is missing | What the card does |
|---|---|---|---|
| J1 | Thu 20 Aug, Ecom+IPO | nothing | every slot renders |
| J2 | Mon 13 Jul, Ecom+IPO | **all four logos** | names as text, promise says "one" honestly, tone line still typed |
| J3 | Thu 20 Aug, AI follower | any followed sector | title falls to Today's brief; nothing mentions AI |
| J4 | Thu 20 Aug, no prefs, logged out | stake, sector, "you" | two slots empty; card still whole |
| J5 | Sun 21 Jun | company, type, logo, 7 of 8 stories | title, promise, button — nothing else exists so nothing else renders |
| J6 | Fri 6:40 AM | the edition | says so, gives the time, offers yesterday |

## Dependencies this creates
- Logo needs a **domain** per company. WP has none; DataLabs has `website`. Favicon service resolves ~85% where a domain exists. The 74% above assumes that; measure it on the real company master before committing to the logo row.
- Tone needs the development-type → up/down/flat map agreed with editorial (Deals/IPO/Financials-profit = up; Controversies/Layoffs/penalties = down; rest = flat). `sentiment__tonality` is unusable.
- Title needs the followed-sector names in the user's own vocabulary ("Ecommerce & D2C" is the taxonomy label; the onboarding chip may say something shorter).

---

# Row K — ten Brief pages (5 Sep)
Draft file row K (y=96000). Full pages, one real day (Thu 20 Aug) except K10 (Sun 21 Jun).

## Utkarsh's objection, and the data answer
"Your Ecommerce & IPO brief" is static — exciting on day one, wallpaper by day two. Correct.
**The dynamic title already exists:** the *Inc42 Daily Brief* newsletter post is published on
**62 of 65 weekdays** (~08:00) with a two-clause editorial title — "RentoMojo Files RHP, Uber India
Axes 200 Jobs & More". Every K card uses it. Weekend: none exists → the lead headline is the title (K10).
Personalisation moves out of the title into the promise line, where it is a fact, not a label.

**Timing:** the newsletter lands at 08:00, the brief at 07:00. The subject line is drafted before
08:00, so the fix is to expose the CMS draft field to the app at 07:00 — a workflow change, not a design one.

## DataLabs — how soon, and how to fast-track
The team updates a profile within 24 hours of a story. Three things follow:
1. **Never show a DataLabs number as "today's".** The company row shows the fact **from today's story**
   (headline figure / bullet) and stamps it `from today's story`. When DataLabs catches up, the stamp
   becomes `from DataLabs · updated today`. Provenance is printed, always.
2. **Fast-track = event-driven.** A Deals / IPO / Financials article publishing should open a DataLabs
   update task automatically, with the number pre-filled from the article. That turns 24h into hours
   for the stories that matter, without touching the rest of the pipeline.
3. **The table (K4) prints the caveat**: "Beco's case is from today's story — DataLabs updates tomorrow."

## Past briefs — answered, not removed
30% open them; median 2 days back; briefs stay 7 days. Four treatments:
- **7-day strip** (K1, K3, K8) — read ✓ / unread ● / today / future, one row, a legend.
- **Catch-up band** (K2) — if yesterday is unread it becomes a black band under the card; nothing else competes.
- **Three-card row** (K4, K6, K7) — Mon/Tue/Wed with state.
- **Cover carousel** (K5, K10) — for the visual layouts.

## "In-Depth" — renamed by what it costs the reader
"The 10-minute read" · "Worth ten minutes today" · "The weekend read" (K10). Never the category name.

## The ten
| # | Name | What sits under the card, in order |
|---|---|---|
| K1 | EDITION | 7-day strip · companies (reason + source) · 10-minute read · bridge |
| K2 | CATCH UP FIRST | catch-up band · companies (compact) · 10-minute read · bridge |
| K3 | CALENDAR ON TOP | strip **above** the card · companies · read · bridge |
| K4 | DATA FIRST | compact card · DataLabs table with caveat · past row · read · bridge |
| K5 | MAGAZINE | image card · big long-read cover · cover carousel · 3 companies · bridge |
| K6 | TWO CLAUSES | the title's two clauses as tappable rows · past row · companies · read · bridge |
| K7 | LIST | one-line rows for everything |
| K8 | LEDGER | continue-state card · your week (4 of 5 · 31 stories · sectors) · strip · companies · read |
| K9 | SEGMENTED | Today / Past 7 days / Companies panes; Today = card + read |
| K10 | WEEKEND | lead headline as title · weekend read · carousel · bridge |

Recommendation: **K1** as the base, **K2's band** as a conditional state on it (unread yesterday), **K10** as the
weekend variant. K6 is the one worth testing against K1 — it makes the title do the index's job.

---

# Row L — the Brief page driven by impact and continuity (5 Sep)
Draft file row L (y=99600). Three real days: Mon 8 Jun (hero), Thu 11 Jun (flat), Sun 21 Jun (weekend).

## The finding underneath everything
**The ranking formula has no story-level importance signal.** `Pop` is a category constant — every
`Startup IPO` story scores 0.116 whether it is Zepto's ₹8,010 Cr filing or a seed-stage company
saying it may list "in 12–18 months". Two articles with the same (topic, sector) score identically
and are separated only by recency. That is why nothing on the page has ever felt prominent: the
design had nothing to make prominent *with*.

## Impact score (new, validated on 1,179 articles)
`impact = 0.40·event + 0.25·company_stage + 0.20·magnitude + 0.15·editorial`

| Term | Source | Coverage |
|---|---|---|
| event | `development_type` — IPO 1.0, M&A 0.9, Deals 0.7, Financials/Regulatory/Controversies 0.6, Trends 0.5, Team/Updates 0.3 | 85% |
| company_stage | `company_type` — Listed 1.0, Late Stage 0.85, Indian Corporate 0.7, Growth 0.6, International 0.55, Early 0.35 | 85% |
| magnitude | ₹ / $ parsed from the headline, log-scaled to ₹10,000 Cr | 47% |
| editorial | Exclusive/Investigative 1.0, In-Depth 0.7, `shelf_life` > 3 days 0.5 | 100% |

**Results:** p50 0.44, p90 0.62, max 0.84.
- **A clear hero (top ≥0.62 and ≥0.10 clear of #3) exists on 57% of weekdays.**
- **No hero on 25%** — forcing one would be a lie, so the layout changes instead.
- Impact #1 equals the most recent article on only 9% of days — it genuinely reorders.
- Ranjith's own example (IPO + Listed/Late-stage company) occurs on 52% of days.

Worked: 8 Jun Zepto UDRHP ₹8,010 Cr = 0.81, gap 0.20. 11 Jun top = 0.55, gap 0.01 → flat.

## Continuity — the personalisation that actually reads as personal
Category personalisation ("you follow Ecommerce") is a filter the user declared once. Continuity is
behavioural and specific:
- **98% of weekdays** contain at least one story about a company covered in the prior 30 days;
  **median 3 of 8**, ≥3 on 75% of days.
- Editorial already marks `Follow Up` (6%) and `Series` (11%) — **94% of weekdays carry one**.
- Zepto thread, 90 days: IPO paused (1 Aug) → warehouse sealed (11 Aug) → revenue analysis (14 Aug)
  → files UDRHP. That is a plot, and "the 4th Zepto story you have seen this month" is unmistakably
  about the reader.

## Personalisation hides big news — quantified
On weekdays publishing more than 8 stories, a story scoring ≥0.62 is cut from the personalised brief on:
Deals+Fintech **58%**, Ecom+IPO **48%**, AI-only **72%** of days. This justifies a dedicated
`Big today, not in your brief` section — additive, never competing with the brief.

## Page architecture (Ranjith's order, each section conditional)
| # | Section | Renders when | Naming decision |
|---|---|---|---|
| 0 | Masthead + contract | always | "Everything that mattered today, in five minutes." — this is how "brief" is conveyed. Not a tagline; a contract the page then keeps |
| 1 | Brief card | always | hero day → the story takes the card; flat day → the card leads with the **shape** of the day ("A day of small cheques") |
| 2 | Still following | a company thread continues (98%) | the timeline, with today's entry in orange |
| 3 | Who did what today | ≥3 companies with facts (82%) | verb-led — RAISED / FILED / PULLED / SOLD / CUT. Answers "why do I care" before the name |
| 4 | Big today, not in your brief | a ≥0.62 story was cut (48–72%) | insurance, stated as such |
| 5 | Your record | always | past briefs as a week record, not a list — feeds the streak |
| 6 | The 10-minute read | In-Depth exists (97% weekdays) | named by cost, never "In-Depth" |
| 7 | Bridge | always | true published count, points to Explore |

**The page is shorter on quiet days** (L3 has four sections, L1 has seven). Length itself signals
how big the day was — and it is honest, which the old fixed-module page was not.

## Next: Explore
The same impact score is the answer to "how do we make the feed more powerful" — sort Explore by
impact rather than recency. Not built; flagged.

---

# Row M — onboarding, and the brief as three pages (5 Sep)
Draft file row M (y=103600). Six frames: 3 onboarding + 3 brief pages.

## "Big today, not in your brief" — deleted, not reworded
Ranjith's objection was right: the section implies the brief is incomplete, and asks a question it
cannot answer (*if it is so big, why is it not in my brief?*). The fix is in the ranking, not the UI.

**Add impact as a fourth term:** `score = 1.0·TopicAff + 0.6·SectorAff + 0.15·Pop + 0.4·Impact`

Measured on 64 weekdays publishing more than 8 stories — does the day's highest-impact story make
the personalised brief?

| W_impact | Deals+Fintech | Ecom+IPO | AI only | No prefs | Followed story still #1 |
|---|---|---|---|---|---|
| **0.0 (today)** | 48% | 73% | 30% | 34% | 97% |
| **0.4** | **97%** | **100%** | **100%** | **100%** | **97%** |

At W=0.4 the biggest story of the day is in the brief essentially always, and personalisation is
untouched (a followed story still leads 97% of days). The section disappears, and the brief can
now promise *"you will always see the day's biggest story"* — which onboarding states.

## Jargon audit — every term removed or replaced
| Was | Problem | Now |
|---|---|---|
| "8 cards" | a card is not a thing readers know | **"8 stories"** |
| "DataLabs" | a product name a media reader has never met | never appears. The section says what it holds: **"filed revenue, funding history, investors and headcount"** |
| "10-minute read" | states the cost, not the reason | **the payoff**: "Understand why Cult.fit's IPO maths works · Nine minutes. You will know what the retail push costs." |
| "Big today, not in your brief" | implies the brief is incomplete | deleted (see above) |
| "In-Depth" | internal category | "One longer story" |
| "impact", "0.62" | internal | never shown |

## DataLabs, researched (inc42.com/datalabs, inc42.com/company/zepto)
- Company pages live on **inc42.com/company/{slug}** — same domain, not a separate product. Free tier
  ("Datalabs Core") already includes search, live signals and preview metrics; Pro (₹1,499/mo) adds
  full P&L, MCA docs, cap table, exports, contacts.
- The Zepto page carries, free: sector, city, founded, founders, **Total funding $2.45 Bn**,
  **Revenue ₹4,178.3 Cr FY24 +101%**, 39 investors, **Employees 19,938 +6.55% in 90d**,
  **Web traffic 2.44 Mn −2.21% in 30d**, plus full P&L / balance sheet / cash flow / ratios.
- **The four numbers a media reader understands without explanation:** revenue + YoY, loss,
  total funding, headcount + trend. "Doubled revenue, still lost ₹1,245 Cr" is a story in two numbers.
  That is the value — a number next to the news, which no other news app can do. Nobody needs to be
  told the platform's name to get it.

## Structure — three pages, one completion bar
A sticky header carries `TODAY'S BRIEF · THU 20 AUG · 0 of 8 read`, an eight-segment progress bar and
three tabs: **The brief · Companies · Deeper**. It persists on every page, so completion is always
visible and the pages never compete with it.

| Page | Job | Answers |
|---|---|---|
| **1 · The brief** | the SET, not an article | what is inside · is it everything (14→8) · why these · is it for me (continuity line) |
| **2 · Companies** | the numbers behind the names | why should I care · what does Inc42 know that others do not |
| **3 · Deeper** | the long story, the record, the rest | is there more · did I miss anything · what happens to the other six |

**Why page 1 no longer reads as an article:** the dominant object is the numbered set of eight —
lead story labelled `1 OF 8`, then rows 2–8 as verb + company + figure. A front page is one headline;
a brief is a numbered list. That is the difference, and it is now structural rather than stated.

## Onboarding (3 screens)
1. **What a brief is, shown**: 14 tiles collapse to 8. "We read everything Inc42 publishes, and keep
   what matters to you. Eight stories. Five minutes. New every morning at 7."
2. **What you follow**: sectors + story types, with the copy stating what it changes — the order, and
   the reason shown on every story.
3. **The deal**: 7 AM, expires tonight, three promises (never more than eight · you will always see
   the day's biggest story · each one tells you why it is there), and the week strip that becomes the streak.

FOMO comes from expiry and the unread count, not from invented scarcity.

## Open
- Horizontal paging vs sticky-header sections is an implementation choice; the completion bar is the
  requirement either way.
- Explore feed by impact rather than recency — same score, not yet built.

---

# Row N — one page, seven ways (5 Sep)
Draft file row N (y=107600). No onboarding, no second page, no stacked sections with headers —
one composition per variation, ~700–890px tall. Thu 8 June: 12 published, 8 in brief, 4 in IPO
which the reader follows, Zepto the 4th story about them this month.

## The seven questions, and the device that answers each
| Question | Device | Present in |
|---|---|---|
| What is a brief? | the count line "8 of the 14 Inc42 published today" + the numbered set + a dated, finite object | all |
| Is it personalised? | "Because you follow IPO" as a block label or per-row dot | all |
| Is it everything I need? | published-vs-kept arithmetic + "the day's biggest is always in" (now true — impact is a ranking term) | all |
| What is inside? | eight rows: verb/topic + company + figure | all |
| Is it relevant to me? | the four IPO rows marked; the split into yours / everyone's | N2, N5 |
| Am I going to miss out? | "expires tonight", the streak at stake, the countdown | all; N4 leads on it |
| Is it built for me? | continuity — "the 4th Zepto story you have seen this month", with the thread | all; N3 leads on it |

## The seven
| # | Name | Organising idea | Answers hardest |
|---|---|---|---|
| N1 | THE STATEMENT | the page is an account of the day — every question is a line in a table | is this everything |
| N2 | THE LIST | all eight visible, dotted where they match what you follow | what is inside |
| N3 | THE THREAD | opens on a story you have already been reading; today's instalment sits at the end of it | is it built for me |
| N4 | THE CLOCK | time-shaped — countdown to expiry, streak visibly at risk, 0 read | FOMO |
| N5 | THE SPLIT | two labelled blocks: 4 because you follow IPO / 4 the ecosystem is reading | is it personalised + is it everything |
| N6 | THE COVER | a dated, numbered edition (No. 232) with a contents strip | what is a brief (through form) |
| N7 | THE ANSWER | each question answered in one short line, in order, as the page itself | all of them, literally |

**Recommendation:** N7 for clarity of concept and N2 for daily use — N7 teaches what the brief is in
about six seconds and would work as the first-week state; N2 is the one that survives day 200.
N3's continuity block is worth folding into whichever wins, since it is the only device that reads
as genuinely personal. N4's countdown is the strongest completion pull but is a treatment, not a
layout — it can sit on top of any of the others.

---

# Row P — six structures for the whole page (5 Sep)
Draft file row P (y=111600). Full pages, ~1100–1500px. Thu 8 June.

## Four content rules fixed across all six (each is a correction)
1. **The publish count is gone.** "8 of the 14 published today" made Inc42 look small. Completeness is
   now stated as an outcome — *"Read them and you are done for the day"* / *"nothing else from today
   is needed"* — never as arithmetic.
2. **Every story carries a reason, so no row is second-class.** Highlighting four of eight made the
   other four look like filler. Now all eight are labelled: `BIGGEST TODAY` · `YOU FOLLOW IPO` ·
   `BIGGEST ROUND` · `MOST READ NOW` · `FROM OUR NEWSROOM`. Nothing is unexplained.
3. **Continuity is a marker on a row, never the page's headline.** Leading with the Zepto thread made
   the whole brief look like it was about Zepto; the "Start reading" button read as "read about Zepto".
   It now sits as one line near the CTA.
4. **Every time sentence has a subject.** "Expires tonight / tomorrow arrives at 7 AM" did not say
   what expired or what arrived. Now: *"This brief is only for today. Tomorrow's brief arrives at 7 AM."*

## The page below the brief belongs to the brief
Only two things: **the companies in it** (Zepto's filed numbers, then "+7 more companies in today's
brief") and **your week** (read/unread, seven-day retention). Not a grab bag of modules.

## The six structures
| # | Name | Borrowed from | The idea |
|---|---|---|---|
| P1 | THE DECK | pliability *Daily Sessions · 0 of 7 complete* | depth shown as a physical stack, not a list — you see there are eight without eight rows |
| P2 | THE RANKED RAIL | Apple TV *Top 10* | numerals on cards in a horizontal rail; order visible without a vertical list |
| P3 | THE PATH | Alan / Duolingo session path | the eight are a route with today's position marked; the page *is* the brief, no separate card |
| P4 | THE REMAINING | Finch *10 goals left for today* | the leading number is what is LEFT; the page empties as you read |
| P5 | THE SPREAD | magazine cover + contents | a dated, numbered edition; the contents page is the proof of completeness |
| P6 | THE BRIEFING | — | dark, dense; the reason is a left column so the eye reads WHY before WHAT |

**Recommendation:** P1 or P4. P1 makes "this is a bounded set" instantly legible and keeps the page
short; P4 makes completion the point and is the strongest daily-return mechanic — "8 stories left"
is a better pull than any countdown. P5 is the one to test if the brand should read editorial rather
than app-like. P2's rail is the weakest — a horizontal scroll hides half the set, which fights the
completeness promise.

---

# Row Q — ten pages that withhold the stories (5 Sep)
Draft file row Q (y=115800).

## The rule that generated all ten
Row P failed on one line: *"if you show everything at a glance, why would people open?"* P3–P6 listed
all eight with company and outcome, which spends the brief before it starts.

**The first screen may reveal the SIZE (eight), the SHAPE (four IPO, three rounds), WHO is in it, or
ONE sample. Never all eight with what happened.**

And "brief" is conveyed by **form, not by an explainer section** — sealed, timed, counted, ticketed,
face-down, addressed. A sealed thing gets opened; a clock says short; eight face-down cards say
finite. None of it needs a sentence that defines the product.

## Below the fold, on every one
Only two blocks, and neither leaks: **who is in it** (logos, then one company's *standing* data —
filed revenue, funding, headcount — never what they did today) and **your week**.

## The ten
| # | Name | What it reveals | What it withholds |
|---|---|---|---|
| Q1 | THE SEAL | date, eight inside, four yours | everything else |
| Q2 | THE SHAPE | today's composition — 4 IPO / 3 funding / 1 ours | every company and outcome |
| Q3 | THE FIVE MINUTES | the time, divided into eight | all content |
| Q4 | THE ONE | one story, complete, as the sample | the other seven |
| Q5 | THE QUESTIONS | three questions the brief answers | the answers |
| Q6 | THE LETTER | addressed, signed, timed; the count and your match | every story |
| Q7 | FACE DOWN | eight cards, four marked yours | all eight faces |
| Q8 | THE RING | eight empty segments, none read | all content |
| Q9 | THE PASS | edition no., 8 stops, 5 min, your two sectors printed | every story |
| Q10 | WHO MOVED | the eight companies, as logos only | every verb, figure and outcome |

## Reading
- **Q5 (Questions)** is the only structure where showing more makes you want to open more — every
  line is an open loop. It is also the only one that needs new editorial work (a question per story).
- **Q7 (Face down)** and **Q8 (Ring)** state finiteness most economically and need no new content.
- **Q10 (Who moved)** answers "is it relevant to me" fastest — you scan eight logos and know instantly.
- **Q2 (Shape)** is the only one that tells you what KIND of day it is, which is the closest thing to
  "is this everything I need to know" without a publish count.
- **Q1, Q6, Q9** carry the strongest brand form; Q6 is the most personal with zero personalisation
  machinery, since a letter addressed to you is self-evidently yours.

---

# Row S — ten cards built on an ordinary day (5 Sep)
Draft file row S (y=123800). **Thursday 11 June: nine stories, all small** — $28.5 Mn, ₹38 Cr, a
₹1,900 Cr share sale, a 250-person layoff. No famous name, no IPO. Chosen deliberately.

## Three things measured that force this
1. **Continuity cannot lead the card.** The top story is about a company the reader has seen in the
   prior 30 days on **48%** of weekdays, and seen *twice* (so "the 3rd story about them" is true) on
   only **32%**. Row R leaned on Zepto continuity in 15 of 15 cards. It renders on a third of days.
2. **The copy in row R was not achievable.** Lines like "Quick commerce just ran out of private
   money" require a daily editorial thesis nobody writes. Row S uses only fields that exist every
   day: headline, development type, company, company stage, counts, figures already in headlines,
   streak, read history.
3. **The newsroom's own title is not a clean input.** 11 June's Daily Brief title is *"ZEE5's Sports
   Era Begins Tonight, Crisis Deepens At WinZO & More"* — and **neither story is in the impact top
   eight**. 18 June (13 stories) has **no Daily Brief post at all**. So the newsletter title is a
   usable asset (S5) but it cannot be the card's spine, and where it is used the brief must be
   ordered to match it or the card contradicts the deck behind it.

## The "it looks like an article" fix
An article card is: one photo, one headline, one standfirst. Every card in row S carries the three
things an article never has —
- **a masthead** (`THE INC42 BRIEF · NO. 235`, a rule, `CHOSEN BY OUR NEWSROOM`),
- **the word brief**, used naturally and repeatedly,
- **a countable set of eight** — eight units you can count but cannot read, with the reader's own
  ones outlined.

No card in row S leads with a photo.

## The ten
| # | Name | Reason to open | Renders when |
|---|---|---|---|
| S1 | THE SHORT DAY | it is small, and that is the pitch | always; strongest on quiet days |
| S2 | THE PATTERN | the day's shape is the news — 4 rounds, 1 layoff, 1 exit | always (development_type, 85%) |
| S3 | THE PILE | two unread briefs stacked, dropping off in 7 days | when ≥1 unread |
| S4 | THE INDEX | a contents page — names and sectors, no verbs, no figures | always |
| S5 | THE NEWSROOM LINE | a person chose these, and here is their line | 62 of 65 weekdays |
| S6 | THE MONEY LINE | one computed figure | 82% of days have ≥1 figure |
| S7 | CURRENT BY 7:05 | the state you end in, not the content | always |
| S8 | YOUR STANDING | teaches the mechanic in words, once | always |
| S9 | YOUR SECTORS, TODAY | answers "is my sector covered", including the honest zero | always |
| S10 | THE EDITION | the most publication-like; masthead-forward | always |

**Reading:** S1, S2, S7 and S9 render on literally every day including Sundays and need no editorial
input. S3 is the only one where the FOMO is a visible object rather than a sentence. S10 positions
"brief" hardest but is the least personal. A shipped card is probably S2's pattern line plus S9's
sector answer inside S10's masthead frame.

## Still open
- Ordering the brief to match the newsletter title, or dropping the title from the card. Cannot ship
  S5 without resolving this.
- Whether the eight-unit counter reads as progress (it should) or as decoration.
