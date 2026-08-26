# Explore page — Article & Company tab logic (state as of 27 Aug 2026)

Synthesized from: Ritvik's `explore-feed-logic.md` (the as-built reference, dated 27 Aug), the
15-slide proposal deck `inc42_App_New_Explore_Screen_proposal` (Product/Design/Data, Aug 2026),
the live prototype at `capable-platypus-044860.netlify.app`, and the 26 Aug "Improving Brief Page
Conversion" scoping call. This is v1 of a document — not a locked spec. Ritvik owns the source of
truth (`explore-feed-logic.md`); this file adds the decision trail, gaps, and cross-references
Ranjith asked for.

**Status: blocked on real data.** Every rule below was validated against ~100 companies picked
by hand, against a real base of ~75,000 (Ritvik's own confidence estimate: 30–40% baked). Nothing
here should be treated as final until the paginated companies API/curl comes back from Prapti.

---

## 1 · The problem, in one line

Explore today is a flat, chronological list with filters. Every card looks the same regardless of
what's actually in the data — a company that raised $500M last week renders identically to one
with almost no data on file. The proposal: **let the data pick the card.** Check each
record against a short list of rules; the first rule that matches decides the layout, and the
card explains *why* it looks that way (funding, hiring, financials — whichever signal is
strongest), instead of a human picking a size to make the page look varied.

Companies risk: "random is worse than same" — varying card size without a real reason teaches
users that big ≠ important, and they stop trusting the page (deck, slide 3).

---

## 2 · How the logic works (three steps)

1. **Check** — evaluate each record's own data against the rule table, top to bottom, first match
   wins. Never looks at neighboring records.
2. **Show** — the matched rule changes which layout template is used and which field leads; the
   card's underlying structure stays constant.
3. **Group** — 2+ **adjacent** records that hit the same rule collapse into one titled block
   (e.g. "Raised recently," "Moving fast"). Because classification is per-record, this is
   stateless — page 20 classifies identically to page 1, and pagination never breaks a run.

---

## 3 · Articles — signal rules (8 rules, first match wins)

| # | Signal | Condition | Source |
|---|---|---|---|
| 1 | Latest | array index < 2, page 1 only | Given (order) |
| 2 | Update | title starts `[Update]` | Given |
| 3 | Financials | tag = `What The Financials` | Given |
| 4 | Session | tag = `Session Article` | Given |
| 5 | Series | tag = `Series` | Given |
| 6 | Spot news | tag = `Spot News` | Given |
| 7 | Cross-sector | `industry.length ≥ 5` | Derived (the only rule with a threshold) |
| 8 | Standard | no match | — |

**6 of 8 rules are pure tag reads** — the newsroom's existing tags already do most of the work.
Only "Cross-sector" invents a number (≥5 industries), and it's partly a tagging artefact, not a
true editorial signal.

Treatments: Latest → hero swipe carousel; Update → row with pulsing pill; Financials/Series →
masthead band, no image; Spot news → numbered digest when 2+, else a normal row; Cross-sector →
row with industry chips; Standard → plain row. Full treatment table in Ritvik's doc §2.

---

## 4 · Companies — signal rules (9 in the build, 10 in the proposal deck — see gap below)

| # | Signal | Condition | Source |
|---|---|---|---|
| 1 | Hero | rank ≤ 3 in current sort | Given |
| 2 | Debut | 1 funding round **and** ≥$100M | Chosen |
| 3 | Round | last funding within 90 days | Chosen |
| 4 | Syndicate | ≥18 investors | Chosen |
| 5 | Debt | funding type = IPO or Debt | Given |
| 6 | Financials | P&L data present | Given |
| 7 | Momentum | headcount Δ3mo ≥25% (either direction) **or** traffic Δ3mo ≥150% (up only) | Chosen |
| 8 | Thin | no headcount and no traffic data | Given (absence) |
| 9 | Standard | no match | — |

**⚠️ Gap found 27 Aug:** the proposal deck's "Ten rules" slide includes a **"Backed by a
person"** rule (an angel investor and little else) between Growing-fast and Little-data that
does **not** appear in Ritvik's current as-built reference. Either it was cut during build, it's
planned but not yet shipped, or the reference doc is stale. **Needs a direct answer from
Ritvik** — logged as ledger item P13.

When both headcount and traffic clear the Momentum bar, the larger absolute delta wins, not the
larger percentage. Full treatment table (leads-with / secondary field per signal) in Ritvik's
doc §4.

**Every threshold above except "Given" ones is hand-picked, not statistically derived** — the
$100M floor, 90-day window, 18-investor floor, and ±25%/150% deltas were reverse-engineered from
one sample page (25 companies). Ritvik's own recommendation: replace with corpus-wide percentiles
before general availability (ledger item P4).

---

## 5 · The "Read in 30s" interaction layer

One controller, five surfaces (feed hero, feed row, feed masthead, feed digest, article/company
detail) sharing the same auto-advance mechanic: 9s per point, tap body to advance, tap play/pause
to hold, tap a segment to jump, pauses on scroll-off and resumes on return. Only one card can be
open at a time. Full spec in Ritvik's doc §8, unchanged from what's live in the prototype.

---

## 6 · What's actually blocking this (the "curl request")

Ranjith's instruction was to reach out to Prapti/Ritvik for the data before building further.
Both the proposal deck (slide 12, "Five things from the data team") and Ritvik's own doc (§13)
converge on the **same 5 concrete asks** — this is the checklist to send, not a generic "send me
the API":

1. **What does `signals_count` count?** If a typed/pre-computed signals field already exists on
   the API, the entire client-side rule table above gets replaced by reading it directly. This is
   the single highest-leverage question — start now, don't wait for the rest.
2. **Event name on session/summit articles** — today can only render "From the stage," never
   which event.
3. **Name of the series** — Series is binary yes/no today; no field carries which series.
4. **`[Update]` as its own field** (or a `last_updated_at` field) — currently a string prefix
   inside the title, not structured data.
5. **Revenue and profit as numbers**, not prose — currently they only exist inside the written
   "What The Financials" summary text.

**Plus the paginated companies API itself** (~75,000 companies, not the ~100 tested by hand) —
this is the actual curl Ranjith is waiting on, to validate every threshold in §4 against the real
base before locking anything.

**Known payload issues to raise with Prapti in the same conversation** (Ritvik's doc §12 — these
will break the rules above if not fixed at the source): empty objects returned instead of null
(`financial_profit_and_loss: {}` reads as truthy); partial objects (some companies have headcount
but no delta — null-check the field, not the container); duplicate/inconsistent key names
(`three_month_change` vs `3_month_change`); HTML-escaped names (`Beauty &amp; Personal Care`);
duplicate investors inflating `number_of_investors` (Emergent lists Khosla twice); mixed-
granularity location arrays (Delhi / India / New Delhi all in `location[]`); date-only timestamps
(no "N hours ago" possible); and at least one wrong sector tag on record (Dogsee Chew tagged
"Tea").

---

## 7 · Risks called out before launch (deck, slide 13)

- **Numbers came from one page** — the sample used to hand-pick thresholds. Fix: derive from the
  whole database, not a page.
- **Tags start to matter** — today a missing tag costs nothing; after this ships, a missing tag
  changes a story's treatment and a wrong tag actively misleads. Fix: tell the desk, track
  untagged-story volume.
- **Traffic data isn't ours** — third-party traffic deltas can jump on small sites for reasons
  unrelated to the business. Fix: exclude very small sites, or show where the number comes from.
- **On a slow news day the page will look quiet** — called out explicitly as correct behaviour,
  not a bug, worth saying before launch so it isn't reported as one.

---

## 8 · Build sequence (Ritvik's doc §14 + deck slide 14, consistent with each other)

| Step | Scope | Dependency | Estimate |
|---|---|---|---|
| 1 | Presentation layer only — client-side rules, feature-flagged, no back-end work | None | 2–3 weeks |
| 2 | Resolve `signals_count` with Data | Conversation, not a project | Start now, alongside Step 1 |
| 3 | Move rules to the server, computed off corpus-wide percentiles | After Step 1 ships and is read | After Step 1 |

**What gets measured:** taps per signal/card type · companies added to Watchlist · summary open
rate · scroll depth vs. the current plain list · share of rows that actually receive a
non-standard treatment.

This lines up with the existing `inc42-app-v2-roadmap.xlsx` items **#3** (Article + Explore card
revamp, P1) and **#6** (DataLabs filters / Explore search reliability, P0) — this document is the
detailed logic underneath those two roadmap lines, not a separate initiative.

---

## 9 · Open items not yet resolved (send list)

All logged in `inc42-open-ledger-MASTER.csv`, section **P** (P1–P14). Highlights:

- **P2 / blocking everything below:** paginated companies API from Prapti
- **P3 / start immediately:** what `signals_count` actually is
- **P13:** reconcile the "Backed by a person" rule (deck has it, build doesn't)
- **P14:** which prototype URL is canonical — the deck links two split prototypes
  (`lustrous-bienenstitch` = Companies, `unique-speculoos` = Articles); Ranjith's own reference is
  a third, merged build (`capable-platypus`). Worth confirming with Ritvik which one is current
  before this goes in front of anyone outside the team.
- **P5–P11:** 7 editorial/product decisions (Series-vs-Session priority, streak definition,
  traffic-as-signal call, etc.) — none blocking, all cheap to resolve, listed in full in the
  ledger.

---

## 10 · What I could not verify

- Whether the 26 Aug "confirm one-card vs multi-card bet with Utkarsh" conversation (scheduled
  for "tomorrow," i.e. today, 27 Aug) has happened — nothing from today is in Wispr Flow yet. If
  it happened outside a recorded call, tell me the outcome and I'll fold it in.
- Attendees on both the dunning-events and sector-data-bug calls, and on this Ritvik session
  itself — Wispr Flow didn't capture named attendees for any of these three recordings.
