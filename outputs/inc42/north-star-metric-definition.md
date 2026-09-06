# Inc42 North Star — metric definition

**Status:** decided by Ranjith, 6 Sep 2026 · for review with Utkarsh
**Scope:** definitions only — no pipeline work, no instrumentation, no product changes.

---

## 1. The decision

**Two metrics, tracked as a pair. Never one without the other.**

| | **Metric 1 — Identified Actives (IA-30)** | **Metric 2 — Repeat Rate** |
|---|---|---|
| **What** | People we know (we have their email) who did something real in a rolling 30 days | Of those people, the share who came back on a **2nd separate calendar day** |
| **Type** | Absolute count | Percentage |
| **Owner** | Growth / capture | Product |
| **Answers** | Are we turning strangers into known people? | Was what we captured real? |

Plus one **guard-rail**, published every time: **total reach**. Any IA-30 gain that came
with a reach drop does not count.

### Why two and not one blended number

- **Each has one owner and one action.** Blended, a movement could be either lever and
  nobody knows who acted.
- **They police each other.** Gate too aggressively and you capture junk registrations:
  IA-30 rises, Repeat Rate falls. The pair exposes the cheat. A single number hides it.
- **No threshold argument is needed to start measuring.**

---

## 2. Precise definitions

### "Did something real" — the activation bar, per product

Each product owns its own row. Changing a row does not change the metric.

| Product | What counts | Note |
|---|---|---|
| **Media** | article read with depth — scroll ≥50% or ≥60s dwell | scroll event does not exist yet; **interim proxy: 2+ pageviews that day** |
| **App** | brief engaged **≥60s** | not the 7-second flick — Inc42's validated activation bar |
| **DataLabs** | an **active query** — search run or filter applied | not a passive profile view — validated by repeat-use data |
| **IP / summits** | applied, registered, or attended | already unified in `silver.events` |

**Never counts:** email opens, push receipts, bare login, staff/internal, bots.

### "Repeat" = a 2nd separate calendar day, inside the same 30 days

Not a 2nd pageview. Not a 2nd session. Those happen by accident — one curious visit from a
search result produces ten pageviews. A person cannot produce two separate days by
accident: they have to leave, and then decide to come back.

**Why 2 days and not 1 or 3** — derived from the forward return curve (§4):

| Visited on… | Chance they return next month | |
|---|---|---|
| 1 day | **42%** | worse than a coin flip — most never come back |
| **2 days** | **62%** | **the flip point** |
| 3 days | 70% | only +8 more |

Going 1 → 2 days is worth **+20 points**. Every day after that is worth only +5 to +8.
The line goes at the biggest jump in the curve.

### Unit

One person = one `unified_contact_id` in the warehouse. **Never** a PostHog `person_id`
(see §5). Anonymous people are never counted in either metric — they appear only in reach.

### Window

Rolling 30 days, recomputed daily. The identical definitions run at 7 days for weekly
cadence — same definitions, two windows, never two definitions.

---

## 3. Baseline (PostHog, 6 Sep 2026, 30-day rolling, `@inc42.com` excluded)

| | Total people seen | **IA-30** | Known share **of people** | **Repeat rate** | Repeaters |
|---|---|---|---|---|---|
| **Media** (53557) | 500,661 | **1,418** | **0.28%** | **57%** | 789 |
| **App** (146258) | 1,133 | **804** | **71%** | **58%** | 465 |
| **DataLabs** (66351) | ~136,000 | *unreliable* | *unreliable* | unknown | — |
| **IP / summits** | — | unmeasured | ~100% by definition | unmeasured | — |

⚠️ **Two different measures are easy to confuse — keep them apart.** *Known share of
people* (column above) = what share of humans we can name. *Known share of behaviour* =
what share of clicks/reads we can attribute. They are not interchangeable:
Media 0.28% of people / 2.01% of behaviour · App 71% of people / 70.32% of behaviour ·
DataLabs person-level unusable, **2.44% of behaviour**.
| **Total (undeduplicated)** | | **2,222** | | **56%** | 1,254 |

Supporting figures: Media 783,809 pageviews in 30d, 2.01% attributable to a known person;
median known reader = 3 pageviews. App 106,238 events, 70.32% attributable; median known
user = 50 events across 2 days.

### What the baseline says

**Repeat rate is 57% on Media and 58% on the App — nearly identical. Repeat rate is not
the broken thing.** Identification is: 0.28% on Media against 71% on the App.

| | Scale | Identity |
|---|---|---|
| **Media** | 500,661 people | **0.28% known** — scale without identity |
| **App** | 1,133 people | **71% known** — identity without scale |
| **DataLabs** | ~136,000 people | 2.44% of *behaviour* known; person-level unusable — neither |

The App is ~250× better at identification than Media and its users are far denser. **The
metrics are computable on the App today.** They are not computable on Media at useful
resolution.

### Where the effort goes

Sizing the two levers on Media, where the volume is:

| Lever | Move | Repeaters | Gain |
|---|---|---|---|
| Today | — | 789 | — |
| **Metric 2** | repeat rate 57% → **100%** (impossible) | 1,418 | +629 |
| **Metric 1** | identification 0.28% → **1%** | 2,854 | **+2,065** |
| Metric 1, further | 0.28% → **2%** | 5,707 | **+4,918** |

Getting identification to 1% beats a physically impossible repeat rate by 3×.
**Metric 1 is the chase. Metric 2 is the check that stops you cheating at it.**

---

## 4. How the 2-day line was derived

Cohort: known Media people active in days −60 to −31 (n = 1,344), measured forward into the
following 30 days, two different ways.

| Active days, month 1 | Cohort | Returned at all | Still engaged (2+ days again) |
|---|---|---|---|
| 1 | 550 | 41.6% | 21.1% |
| **2** | **270** | **62.2%** | **40.7%** |
| 3 | 159 | 69.8% | 47.8% |
| 4 | 107 | 77.6% | 62.6% |
| 5 | 70 | 82.9% | 64.3% |
| 6 | 46 | 91.3% | 80.4% |
| 7 | 31 | 96.8% | 90.3% |
| 8+ | 105 | ~100% | 80–100% |

The elbow is at 1 → 2 days under **both** definitions (+20.6 and +19.6 points — the largest
single-day gain in each). Two independent tests agreeing is why the line is stated as
derived from data rather than chosen.

**Caveats:** Media only; uses the interim pageview proxy, not the real depth bar; cohort is
already-identified people, so it carries survivorship; n thins above 7 days.
**Re-derive once scroll depth exists and App/DataLabs enter the same computation.**

---

## 5. Why this must be computed in the warehouse, not PostHog

**A person-level metric cannot be computed inside PostHog.** On DataLabs, the same 30-day
window returns **199 or 2,001 people**, and **200 or 767 distinct emails**, depending only
on how the query is written. Cause: person-on-events stores person properties as
**event-time snapshots**, so person-level aggregates shift with query shape. Three separate
projects also mean three separate person universes with no shared key.

Event-level counts (identified share) are stable and reproduced across query shapes.
DataLabs person-level counts are not, and are marked *unreliable* above.

**Do not merge the PostHog projects.** The existing decision — keep event streams separate
per platform, unify downstream — is correct and stands.

### What already exists and must not be rebuilt

**Confirm with Prapti before anyone starts** (cited from the `inc42-data-warehouse` repo,
not from a live read):

- `contact_360` — 328K unified contacts, one `unified_contact_id` across 7+ systems. **The
  identity spine already exists.**
- RFV engagement scoring, with exponential recency decay and hot/engaged/passive/dormant
  tiers, paid weighted 2×.
- `silver.events` — summit registrations and paid tickets, already unified. **IP is the one
  product already joined.**
- `company_360` — 75K companies. Reverse ETL to Customer.io, live since Jun 2026.

**The gap is precise: none of the warehouse's 8 sources is PostHog.** It scores
registrations and purchases, never reading, searching or app use.

### Dependencies before both metrics are computable across all four products

1. Behaviour must reach the warehouse — Media's export exists but has been **paused since
   ~29 Jul**; DataLabs and App have none. Establish why it was paused before un-pausing.
2. Person resolution on `unified_contact_id`, never PostHog `person_id`.
3. Scroll depth restored, to replace the Media interim proxy.
4. The 2-day line re-derived once all four surfaces are in the same computation.

Until then: report Media and App separately and add them, stating the double-count openly.

---

## 6. Reading the pair

| IA-30 | Repeat rate | Diagnosis |
|---|---|---|
| ↑ | ↑ | **Real growth.** The only clean win. |
| ↑ | ↓ | **Capturing junk** — gating too hard, or capturing people with no intent. |
| ↓ | ↑ | **Shrinking to look good** — the ratio trap. |
| ↓ | ↓ | Real decline. |

Plus the veto: **any IA-30 gain that arrived with a reach drop does not count.**

### Three failure modes to defend against

1. **Repeat rate is a ratio, so it can improve by getting worse.** Identify fewer, better
   people and the percentage rises. → **Never publish repeat rate without IA-30 beside it.**
2. **IA-30 can be bought by gating, at the cost of reach.** → **Reach is published
   alongside, always.** This is Utkarsh's A2 hypothesis and the guard-rail on the whole thing.
3. **"Repeat" will drift if left loose.** → Fixed as a 2nd separate calendar day. Not a
   pageview, not a session.

---

## 7. Diagnostic cuts

Published beside the pair, never folded inside either number — folding a cut into a metric
is exactly what broke QIA.

| Cut | Question it answers |
|---|---|
| By **depth** (2–3 / 4–7 / 8–14 / 15+ days) | how strong are these relationships? Media today: **423 of 789 (54%) sit at the bare minimum of 2–3 days** |
| By **surfaces touched** (1 / 2 / 3+) | is One Inc42 actually happening? 1.6–3.4% today |
| By **role** (founder / investor / operator) | are they the right people? |

**Role and employer stay outside both metrics.** A metric whose value is set by form
coverage measures the form, not the business — only 4.1% of Media's known actives carry
`Company Type`, and on the full QIA bar the flagship surface produces **25 people**.

---

## 8. Relationship to money

Not the current focus, but the pair is upstream of every revenue line, not orthogonal to it.

- Membership, event tickets and sponsorship all need the same input: people who show up
  repeatedly and are known.
- Precedent: FT's engagement threshold correlated with **10% lower cancellation**, and
  carried them to 1M subscribers. Inc42's own warehouse already weights paid users 2× in its
  RFV scoring.
- **Honest limit:** necessary, not sufficient. Reader→payer conversion in media sits near
  1.4% and is a hard category norm. IA-30 rising 10× does not make revenue rise 10×.

**When money becomes the focus, the metric will be `payers ÷ IA-30`. IA-30 is the
denominator of the future revenue metric — building it now is not a detour.**

---

## 9. What is not chased

| Not a metric | Why |
|---|---|
| Pageviews, unique visitors, cumulative registered users | can only go up; a number that cannot fall carries no information |
| MAU / DAU per product | fragments the person; rewards surface-hoarding |
| App installs | measures marketing, not the relationship |
| Newsletter subscribers | opens are not engagement |
| Session duration alone | a confused user and an engaged one look identical |
| **QIA as currently written** | binary attribute flag, no gradient, value set by form coverage |
| Revenue, subscriptions | out of focus by decision — see §8 |
| Sponsor composition | byproduct, not a target |
| Any per-product north star | re-fragments what One Inc42 exists to unify |

---

## 10. Open items before this is locked

1. **Confirm the warehouse assets with Prapti** — `contact_360`, the existing RFV
   implementation and `silver.events` are cited from repo memory, not a live read.
2. **Establish why the Media batch export was paused** on ~29 Jul before anyone un-pauses it.
3. **Fix DataLabs measurement** — its person-level data is currently unusable, so one of the
   four products has no baseline.
4. **Instrument IP/summits** — attendees hand over their name in person; it is structurally
   the highest-yield identification surface and is currently invisible.
5. **Re-derive the 2-day line** once scroll depth lands and all four surfaces are computed
   together.
6. **Review with Utkarsh** as a proposed replacement for QIA — same ambition, working
   arithmetic underneath.
