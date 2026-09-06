# Inc42 North Star — metric definition

**Status:** proposed, for review with Utkarsh · **Date:** 6 September 2026 · **Owner:** Ranjith
**Scope:** definitions only — no pipeline work, no instrumentation, no product changes.

---

## 1. Why this document exists

Inc42 runs four products — Media, App, DataLabs, IP/summits — under a "One Inc42" strategy
that says they serve one person. The declared north star, **QIA**, is not usable as written:

- It is a **binary attribute flag with no gradient**. A person who read on 22 days and one
  who read once both count as 1. No screen can be optimised against it.
- Its value is **set by which form someone filled**, not by anything the product did. Only
  4.1% of Media's identified actives carry `Company Type`; on the full QIA bar the flagship
  surface produces **25 people**.
- It **cannot be computed reliably** in the systems that hold the behaviour (see §6).

The requirement is one metric, chosen now, that **does not change as the data improves** —
valid today with ~98% of Media behaviour anonymous, and still valid at FY31 scale. The
number starts small. The definition never moves.

---

## 2. The metric

> ### EP-30 — Inc42 Engaged People
> The number of **identified people** who recorded **≥2 engaged days** across any
> combination of Inc42 surfaces in a rolling 30-day window.

| Element | Definition |
|---|---|
| **Unit** | one person = one `unified_contact_id`. Never an account, session, device, or PostHog `person_id`. |
| **Engaged day** | a calendar day (IST) on which the person took ≥1 qualifying action on **any** surface. A day is a day regardless of which product. |
| **Window** | rolling 30 days, recomputed daily. The identical definition runs at 7 days for weekly cadence — one metric, two windows, never two definitions. |
| **Threshold** | **≥2 days — derived, not chosen.** See §4. |
| **Identity** | email → `unified_contact_id`. Anonymous people are never scored. |

### What earns a day — product-owned, metric-invariant

| Product | Qualifying action | Basis |
|---|---|---|
| **Media** | article read with depth — scroll ≥50% or ≥60s dwell | needs the scroll event; **interim proxy: 2+ pageviews that day** |
| **App** | brief engaged ≥60s | already Inc42's validated activation bar, vs the 7s flick |
| **DataLabs** | an active query — search run or filter applied | validated by repeat-use: Adv Filter 53%, Saved Search 52%, vs passive profile view |
| **IP / summits** | applied, registered, or attended | already unified in `silver.events` |

**Never counts:** email opens, push receipts, bare login, staff/internal, bots. A newsletter
*click* counts only via the Media action it lands on.

Each team may revise its own row without touching the metric. That is the point: **one
scoreboard, four levers.**

### Why days, not an engagement score

- **No cross-product weighting argument.** "Is a DataLabs search worth three article reads?"
  is unanswerable and would consume months of debate. A day is a day.
- **No dependency on scroll depth.** An RFV-style score needs volume; volume does not exist
  yet. Days need only identity and a date.
- **Sums natively across four products.** This is what makes it one umbrella metric rather
  than four metrics added together.
- **Cannot be inflated by pageview padding.** Ten pageviews in one day is one day.

Depth is not discarded — it lives *inside* each product's bar for earning a day, which is
where quality judgements belong.

---

## 3. Ground truth (PostHog, 6 Sep 2026, 30-day rolling, `@inc42.com` excluded)

| | Media (53557) | App (146258) | DataLabs (66351) |
|---|---|---|---|
| Behaviour in 30d | 783,809 pageviews | 106,238 events | 654,435 events |
| **Attributable to a known person** | **2.01%** | **70.32%** | **2.44%** |
| Identified actives | 1,388 | 804 | *unreliable* |
| Median per identified person | 3 pageviews | 50 events / 2 days | — |
| **≥2 engaged days (EP-30)** | **789** | **465** | *unreliable* |
| ≥3 engaged days | 530 | 282 | *unreliable* |
| PostHog → warehouse export | exists, **PAUSED** since ~29 Jul | **none** | **none** |
| Scroll / depth event | **does not exist** | — | — |

### The finding that should change planning

**Media and App have opposite problems, and nobody is currently measured on either.**

| | Scale | Identity |
|---|---|---|
| **Media** | 478K visitors | **2.01% known** — scale without identity |
| **App** | 1,133 people | **70.32% known** — identity without scale |
| **DataLabs** | 135K visitors | 2.44% known — neither |

The App is, by a factor of ~35, the best identification surface Inc42 owns, and its
identified users are far denser (median 50 events vs Media's 3 pageviews). **EP-30 is
computable on the App today.** It is not computable on Media at any useful resolution.

### EP-30 today

**Media 789 + App 465 = 1,254 undeduplicated.** DataLabs person data is unusable; IP is not
yet measured; cross-surface overlap is unknown. Realistic deduplicated figure: **~1,000–1,250.**

Publish that number as-is. Not 21,298. Not 2,100.

---

## 4. How the ≥2 threshold was derived

Cohort: identified Media people active in days −60 to −31 (n = 1,344). Measured forward
into the following 30 days, two ways.

| Active days, month 1 | Cohort | Returned at all | **Still engaged (≥2 days)** |
|---|---|---|---|
| 1 | 550 | 41.6% | 21.1% |
| **2** | **270** | **62.2%** | **40.7%** |
| 3 | 159 | 69.8% | 47.8% |
| 4 | 107 | 77.6% | 62.6% |
| 5 | 70 | 82.9% | 64.3% |
| 6 | 46 | 91.3% | 80.4% |
| 7 | 31 | 96.8% | 90.3% |
| 8+ | 105 | ~100% | 80–100% |

**The elbow is at 1 → 2 days.** It is the largest single-day gain under both definitions
(+20.6pp on any return, +19.6pp on still-engaged). Every subsequent day adds only ~5–8pp.
Crossing from one day to two roughly **doubles** the chance a person is still engaged next
month.

This replaces the ≥3 placeholder. Both curves agree, which is why the threshold is stated
as derived rather than chosen.

**Caveats, stated:** Media-only; uses the interim pageview proxy rather than the real depth
bar; cohort is already-identified people, so it carries survivorship; n thins above 7 days.
**The threshold must be re-derived once scroll depth exists** and once App and DataLabs
enter the same computation.

---

## 5. How EP-30 behaves under One Inc42

EP-30 is already an umbrella metric, because it is defined on the **person** — the four
products disappear inside it. They reappear in exactly two places, and neither changes the
definition:

1. **As the rule for what earns a day** — owned per product, revisable independently.
2. **As a breakdown of the same number** — EP-30 by surfaces touched:

| Cut | Meaning |
|---|---|
| EP-30 total | size of the relationship |
| **EP-30 on 2+ surfaces** | **the One Inc42 proof** — 1.6–3.4% today |
| EP-30 on 3+ surfaces | the core |

**The durability test it passes:** if Media and App merge into one surface, EP-30 is
unaffected — only the day-earning rows consolidate. Reorganising the company must never
redefine the north star.

**Qualification (role + employer) is a cut of EP-30, not a gate inside it.** Report
"% of EP-30 who are founders / investors / operators" as a relevance check and a
personalisation input. It stays out of the metric because sponsors are a byproduct, and
because a metric whose value is set by form coverage measures the form, not the business.

---

## 6. Why it must be computed in the warehouse, not PostHog

**A person-level metric cannot be computed inside PostHog.** Direct evidence from this
analysis: on DataLabs, the same 30-day window returns **199 or 2,001 identified people**,
and **200 or 767 distinct emails**, depending only on how the query is written. Cause:
person-on-events stores person properties as **event-time snapshots**, so person-level
aggregates shift with query shape. Three separate projects also mean three separate person
universes with no shared key.

Event-level counts (the identified-share figures) are stable and were reproduced across
query shapes. Person-level counts on DataLabs are not, and are marked *unreliable* above.

**Therefore:** EP-30 is defined against `contact_360.unified_contact_id` in BigQuery, where
a person is one row with one current value.

**Do not merge the PostHog projects.** The existing architecture decision — keep event
streams separate per platform, unify downstream — is correct and stands.

### What already exists and must not be rebuilt

To be **confirmed with Prapti** before anyone starts (cited from the `inc42-data-warehouse`
repo, not from a live read):

- `contact_360` — 328K unified contacts, one `unified_contact_id` across 7+ source systems.
  **The identity spine already exists.**
- **RFV engagement scoring already implemented**, with exponential recency decay and
  hot/engaged/passive/dormant tiers.
- `silver.events` — summit registrations and paid tickets, already unified. **IP is the one
  product that is already joined.**
- `company_360` — 75K companies with sector enrichment.
- Reverse ETL to Customer.io, live since Jun 2026.

**The gap is precise:** none of the warehouse's 8 sources is PostHog. It scores
registrations and purchases, never reading, searching or app use.

### Dependencies for EP-30 to become computable

1. Behaviour must reach the warehouse — Media's export exists but is paused; DataLabs and
   App have none.
2. Person resolution on `unified_contact_id`, never PostHog `person_id`.
3. Scroll depth restored, to replace the Media interim proxy.
4. `role_captured_at` to exist, before the qualification cut can be trusted to decay.
5. Threshold re-derived once all four surfaces are in the same computation.

---

## 7. Mandatory companions

Published with EP-30 every time. These are context, not alternative north stars, and may
not be dropped from a report.

1. **R30 — Reach.** Unique browsers with 2+ interactions in 30 days, anonymous included.
   **Guard-rail: EP-30 must never rise by shrinking R30.**
2. **Identified Share.** % of interactions attributable to a known person —
   **Media 2.01% · App 70.32% · DataLabs 2.44%.** This is the metric's published blind spot.

### Why this is not a vanity metric

| Test | EP-30 |
|---|---|
| Can it go down? | **Yes** — a person who stops returning leaves the count |
| Is its blind spot hidden? | **No** — Identified Share is published beside it |
| Can traffic growth inflate it? | **No** — defined on the person, not on volume |

---

## 8. What is not chased

| Not a north star | Why |
|---|---|
| Pageviews, unique visitors, cumulative registered users | can only go up; a number that cannot fall carries no information |
| MAU / DAU per product | fragments the person; rewards surface-hoarding |
| App installs | measures marketing, not the relationship |
| Newsletter subscribers | opens are not engagement |
| Session duration alone | a confused user and an engaged one look identical |
| **QIA as currently written** | binary attribute flag, no gradient, value set by form coverage |
| Revenue, subscriptions | out of focus by decision |
| Sponsor composition | byproduct, not a target |
| Any per-product north star | re-fragments what One Inc42 exists to unify |

---

## 9. Open items before this is locked

1. **Confirm the warehouse assets with Prapti** — `contact_360`, the existing RFV
   implementation, and `silver.events` are cited from memory of the repo, not a live read.
2. **Establish why the Media batch export was paused** on ~29 Jul before anyone un-pauses it.
3. **Re-derive the threshold** once scroll depth lands and App/DataLabs join the computation.
4. **Stress the definition on five named people** — one per product, one cross-surface. If
   the "engaged day" rule is ambiguous for any of them, it is not finished.
5. **Review with Utkarsh** as a proposed replacement definition for QIA — same ambition,
   keep the name if he prefers, working arithmetic underneath.
