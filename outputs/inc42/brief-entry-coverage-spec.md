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
