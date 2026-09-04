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
