# Inc42 Audience Measurement — Metrics & Identity Definition

**Date:** 7 September 2026 · **Owner:** Ranjith · **Status:** proposed, for review with Utkarsh
**Data source:** PostHog live pull, 6 Sep 2026, 30-day rolling, internal accounts excluded

---

## 1. Goal

Inc42 runs four products — **Media, App, DataLabs, IP (summits)** — under a One Inc42 strategy that says they serve one person. We need a measurement system that:

- Treats a customer as **one person**, not four users in four reports
- Works **today**, when ~98% of website behaviour is anonymous
- **Does not change** as the data improves — the number starts small, the definition stays fixed
- Can be **acted on** by each team without fragmenting into per-product metrics
- Is **upstream of revenue**, without requiring revenue to be the current target

The declared north star, QIA, does not meet this. It is a binary attribute flag with no gradient, its value is set by which form someone filled rather than by anything the product did, and on the flagship surface it currently resolves to 25 people.

---

## 2. The two metrics

| | **Metric 1 — Identified Actives (IA-30)** | **Metric 2 — Repeat Rate** |
|---|---|---|
| **What** | Identified people who did something real in a rolling 30 days | Of those, the share who returned on a **2nd separate calendar day** |
| **Type** | Absolute count | Percentage |
| **Owner** | Growth / capture | Product |
| **Answers** | Are we turning strangers into known people? | Was what we captured real? |

**Plus one guard-rail, published every time: total reach.** Any IA-30 gain that arrives with a reach drop does not count.

### Why two and not one blended number

- **Each has one owner and one action.** Blended, a movement could be either lever and nobody knows who acted.
- **They police each other.** Gate too aggressively and you capture junk registrations: IA-30 rises, Repeat Rate falls. A single number hides that; the pair exposes it.
- **No threshold argument is needed to start measuring.**

### Reading the pair

| IA-30 | Repeat Rate | Diagnosis |
|---|---|---|
| ↑ | ↑ | **Real growth.** The only clean win. |
| ↑ | ↓ | **Capturing junk** — gating too hard, or capturing people with no intent |
| ↓ | ↑ | **Shrinking to look good** — the ratio trap |
| ↓ | ↓ | Real decline |

---

## 3. The identity ladder

| Tier | Definition |
|---|---|
| **Anonymous** | Cookie or device only. Cannot be recognised tomorrow. |
| **Reachable** | We hold an email or phone, and nothing else. |
| **Partially Identified** | Identifier + **exactly one** of {job title, company name} |
| **Identified** | **Identifier + job title + company name** |

> ### Identified = (Email **or** Phone) + Job Title + Company Name

**Every field carries two mandatory properties:**

| Property | Why |
|---|---|
| `captured_at` | A role given in 2023 is not the same asset as one given yesterday. Exists nowhere in our stack today. |
| `source` | Signup vs sign-in vs event registration vs import. You cannot fix a capture point you cannot trace. |

**Decay rule:** after **24 months** without reconfirmation, the role goes stale and the person drops out of Identified until re-asked. This is the BPA Worldwide standard — media buyers discount three-year-old qualification, and without it an Identified count silently rots.

**IA-30 = Identified ∩ active in the last 30 days.** "Identified" describes the person record. "Active" adds behaviour. Keep them separate.

---

## 4. The fields

### Asked — 3 required, 1 confirmation, 1 optional

| # | Field | Required | Format |
|---|---|---|---|
| 1 | **Email or Phone** | Yes — whichever the login uses | validated |
| 2 | **Job title** | Yes | free text with autocomplete |
| 3 | **Company name** | Yes | free text, autocomplete against `company_360` |
| 4 | Seniority + Function | Confirmation only | **pre-filled from #2**, one tap to correct |
| 5 | The other of email/phone | Optional | validated |

Sector standard is 3–5 required fields maximum. We sit at the low end while collecting more usable information than the current dropdown ever produced.

### Derived — never asked

| From | We get |
|---|---|
| **Job title** | Seniority band, Function |
| **Company name** | Industry, Company Type, Company Size |

### Stored — all three, permanently

| Field | Holds |
|---|---|
| `job_title_raw` | Exactly what the user typed. **Never overwritten.** |
| `seniority` | Derived band + `seniority_source` = `derived` / `user_corrected` / `legacy_dropdown` |
| `function` | Derived |

**Why keep the raw text:** the parser will be wrong at first. Keeping the raw means everyone can be re-derived when it improves. Derive-only throws the evidence away.

### What "did something real" means, per product

Each team owns its own row. Changing a row does not change the metric.

| Product | Qualifying action | Basis |
|---|---|---|
| **Media** | Article read with depth — scroll ≥50% or ≥60s dwell | Scroll event does not exist yet. **Interim proxy: 2+ pageviews that day.** |
| **App** | Brief engaged **≥60s** | Not the 7-second flick — our validated activation bar |
| **DataLabs** | An **active query** — search run or filter applied | Not a passive profile view — validated by repeat-use data |
| **IP / summits** | Applied, registered, or attended | Already unified in `silver.events` |

**Never counts:** email opens, push receipts, bare login, staff/internal accounts, bots.

---

## 5. Two decisions, and the evidence behind them

### 5.1 Ask company name. Do not ask industry.

| Definition | People (Media base) |
|---|---|
| Email + Job title + **Industry** | **1,384** |
| Email + Job title + **Company name** | **18,471** |

**13× more people, from data we already hold.** `Industry` has 7,106 records; `Company Name` has 73,205. We were asking a question we can already answer — company name resolves to industry, company type and company size against `company_360`.

### 5.2 Derive seniority from job title. Do not ask it cold.

**`Designation` is not a job title — it is a second seniority dropdown.** Its actual top values:

| Value | People |
|---|---|
| founder | 3,474 |
| senior-management | 3,341 |
| junior-management | 3,065 |
| other | 2,899 |
| student | 2,220 |
| Founder | 1,921 |
| VP/Senior Management | 1,640 |
| cxo / CXO | 1,521 |

We ask the same question twice, into two fields, in two casing conventions. They cover largely **different people**:

| | People |
|---|---|
| Designation only | 20,693 |
| Seniority only | 29,064 |
| Both | 4,968 |
| **Union** | **54,725** |

**Merging and normalising the two fields lifts role coverage from 34,032 to 54,725 — a 61% gain with no new questions asked.**

**Why the standalone dropdown must not be reused as-is:** it mixes three different axes — seniority (`senior-management`), role type (`founder`, `cxo`) and life stage (`student`). The consequence is already in the data: **192 people selected "Investor" as their seniority while working at early-stage startups.** Pre-filling from a typed job title anchors the answer; asking cold produces garbage.

---

## 6. Where we stand today

### Field coverage — Media person base (10,473,428 records)

| Field | Populated |
|---|---|
| Any email field | 126,849 |
| `email` specifically | 92,868 |
| **Company Name** | **73,205** |
| Seniority ∪ Designation | 54,725 |
| Industry | 7,106 |
| Phone Number | 6,348 |
| Company Type | 948 |
| Function | **40** |
| Interests | **40** |
| City | **7** |

**We are not missing the fields. We are missing the asking.**

### The identity ladder, applied

| Tier | People (Media base) |
|---|---|
| Reachable — email, nothing else | 46,158 |
| Partially Identified | 28,239 |
| **Identified** | **18,471** |

### The metrics, 30-day rolling

| | Media | App | DataLabs | IP |
|---|---|---|---|---|
| Total people seen | 500,661 | 1,133 | ~136,000 | — |
| Behaviour attributable to a known person | **2.01%** | **70.32%** | **2.44%** | — |
| Active with an identifier | 1,389 | 804 | *unreliable* | unmeasured |
| **IA-30 (Identified + active)** | **571** | needs re-measuring | *unreliable* | unmeasured |
| **Repeat Rate** | **57%** | **58%** | unknown | unmeasured |

**Two findings that should drive planning:**

**Repeat rate is 57% on Media and 58% on the App — nearly identical. Repeat rate is not the broken thing.** Identification is.

| | Scale | Identity |
|---|---|---|
| **Media** | 500,661 people | **0.28% identified** — scale without identity |
| **App** | 1,133 people | **71% identified** — identity without scale |
| **DataLabs** | ~136,000 people | 2.44% of behaviour — neither |

### Where the effort goes — the arithmetic

Sizing the two levers on Media, where the volume is:

| Lever | Move | Repeaters | Gain |
|---|---|---|---|
| Today | — | 789 | — |
| **Metric 2** | repeat rate 57% → **100%** (impossible) | 1,418 | +629 |
| **Metric 1** | identification 0.28% → **1%** | 2,854 | **+2,065** |
| Metric 1, further | 0.28% → **2%** | 5,707 | **+4,918** |

**Getting identification to 1% beats a physically impossible repeat rate by 3×. Metric 1 is the chase. Metric 2 is the check that stops us cheating at it.**

---

## 7. How the 2-day repeat line was derived

Cohort: identified Media people active in days −60 to −31 (n = 1,344), measured forward into the following 30 days, two independent ways.

| Active days, month 1 | Cohort | Returned at all | Still engaged (2+ days again) |
|---|---|---|---|
| 1 | 550 | **41.6%** | **21.1%** |
| **2** | **270** | **62.2%** | **40.7%** |
| 3 | 159 | 69.8% | 47.8% |
| 4 | 107 | 77.6% | 62.6% |
| 5 | 70 | 82.9% | 64.3% |
| 6 | 46 | 91.3% | 80.4% |
| 7 | 31 | 96.8% | 90.3% |

**Someone who visits once has a 42% chance of ever coming back — worse than a coin flip. Visit twice and it flips to 62%.** That single extra day is worth **+20 points**; every day after it is worth only +5 to +8.

**The line goes at the biggest jump in the curve, and both tests agree it is at 2 days.** This is derived from data, not chosen.

**Practical consequence:** the single most valuable thing any Inc42 screen can do is get a first-time identified visitor to come back a **second** time.

---

## 8. Why this will work

- **The priority argument is settled by arithmetic, not opinion.** Identification beats every alternative 3:1. Nobody has to win a debate.
- **We can start measuring next week, on the App.** 71% of app behaviour is already attributable. We do not have to wait for the warehouse to have a real number.
- **Every product owns a different lever, but nobody owns a different metric.** One scoreboard, four levers.
- **Both metrics can go down.** Registered-user counts cannot. That is the difference between a metric and a decoration.
- **It survives reorganisation.** If Media and App merge, neither metric changes — only the "did something real" rows consolidate.
- **The shape is proven.** FT built a 1M-subscriber business on a behaviour threshold derived from return data. Their engaged threshold correlated with 10% lower cancellation.
- **The biggest single fix is a join, not a data-collection project.** 73,205 free-text company names already sit in our database, waiting to become Industry, Type and Size.

---

## 9. Why it might not work

| Risk | Why it is real | Defence |
|---|---|---|
| **We gate everything and kill reach** | Identification is 90% of the chase, and the fastest way to move it is forcing login | **Reach published beside IA-30, always. A gain with a reach drop does not count.** |
| **Repeat rate improves by getting worse** | It is a ratio — identify fewer, better people and the percentage rises | **Never publish repeat rate without IA-30 next to it.** A rising % on a falling count is a loss. |
| **QIA is already locked with Utkarsh** | Two north stars is worse than one bad one | Take this as a **replacement definition**, keeping the QIA name if preferred |
| **Not yet computable across products** | Media's warehouse export is paused; App and DataLabs have none; DataLabs person data is unreliable | Report Media and App separately and add them, stating the double-count openly |
| **The numbers are small and jumpy** | At these volumes one campaign or one bug moves them 10% | Report 3-month trend, never week-on-week, until IA-30 clears ~5,000 |
| **Blind to *who* the people are** | 1,000 engaged students score the same as 1,000 engaged founders | Publish the role breakdown as a **cut** beside the metric — never inside it |
| **The 2-day line may move** | Derived from Media pageviews, not the real depth bar, because scroll depth does not exist | Re-derive once scroll lands. Expect it to shift; say so now rather than defend it later. |

---

## 10. What has to be built

**Blockers — nothing works properly without these**

1. **Collapse the five email fields into one.** `email`, `Email`, `Work Email`, `work_email`, `Personal Email`. **33,981 people — 27% of everyone reachable — have an address in a field that is not `email`.** Until fixed, "has an email" means five different things and every count is wrong.
2. **Pick one role field and normalise 54,725 existing answers** onto a single seniority ladder.
3. **Build the `company_360` resolver** — company name → Industry, Company Type, Company Size.
4. **Build the job-title normaliser** — lookup table plus LLM fallback, producing seniority and function.
5. **Add `captured_at` and `source`** to every identity field.

**Data integrity**

6. **`Phone Number` is stored as a numeric property**, which destroys `+91` and any leading zero. 6,348 numbers are already affected.
7. **Restore Scroll Depth on Media** — it is the depth bar for "did something real", and it does not exist.

**Pipeline**

8. **Media's PostHog → warehouse export exists but has been paused since ~29 July.** Establish why before un-pausing.
9. **DataLabs and App have no export at all.**
10. **Do not merge the PostHog projects.** Keep event streams separate per platform and unify downstream — the existing architecture decision is correct.

**Coverage gaps**

11. **DataLabs person-level data is unusable** — the same 30-day window returns 199 or 2,001 people depending on query shape, because person-on-events stores properties as event-time snapshots. **A person-level metric cannot be computed inside PostHog.** It must run against `unified_contact_id` in BigQuery.
12. **IP/summits is entirely unmeasured**, despite attendees handing over their details in person. Structurally our highest-yield identification surface, and currently invisible.

---

## 11. What we deliberately do not chase

| Not a metric | Why |
|---|---|
| Pageviews, unique visitors, cumulative registered users | Can only go up. A number that cannot fall carries no information. |
| MAU / DAU per product | Fragments the person; rewards surface-hoarding |
| App installs | Measures marketing, not the relationship |
| Newsletter subscribers | Opens are not engagement |
| Session duration alone | A confused user and an engaged one look identical |
| **QIA as currently written** | Binary attribute flag, no gradient, value set by form coverage |
| Revenue, subscriptions | Out of focus by decision — see §12 |
| Sponsor composition | Byproduct, not a target |
| Any per-product north star | Re-fragments what One Inc42 exists to unify |

**Also excluded from the Identified definition** (collect them, never gate on them): Industry, Company Type, Company Size — all derived. Phone, City, Function, Interests — useful, never gating. Verified work-domain email — a stricter tier if sponsors ever require it; not now.

---

## 12. Relationship to revenue

Not the current focus, but the pair is upstream of every revenue line, not orthogonal to it.

- Membership, event tickets and sponsorship all need the same input: **people who show up repeatedly and are known.**
- Precedent: FT's engagement threshold correlated with **10% lower cancellation**. Our own warehouse already weights paid users 2× in its RFV scoring — someone internally already believed engagement predicts payment.
- **Honest limit:** necessary, not sufficient. Reader-to-payer conversion in media sits near 1.4% and is a hard category norm. IA-30 rising 10× does not make revenue rise 10×.

**When money becomes the focus, the metric will be `payers ÷ IA-30`. IA-30 is the denominator of the future revenue metric — building it now is not a detour.**

---

## 13. What comparable companies collect

Verified from published sources. **Research limitation:** Crunchbase, PitchBook, Tech in Asia, Sifted, The Ken, The Information, e27, Tracxn and VCCircle are behind bot protection and their forms could not be read. This list is not padded with guesses.

| Source | What they collect |
|---|---|
| **CB Insights** | Name, job title, **job responsibilities**, contact details, company, login credentials, usage preferences, **"areas of focus and interest for your company"**, newsletter research-area interests |
| **Dealroom** | Name, email, IP, job title, company name, telephone, profile photo, **login count**, **last login date/time** |
| **Informa TechTarget** | Personal details, **social media profile details**, **professional profile details, association memberships, qualifications, company insight data**, plus usage: content interacted with, downloads, votes, questions, ratings |
| **BPA Worldwide** (B2B audit standard) | Job title, **industry/SIC**, **company size**, **purchasing/recommending authority**, **and a requalification date** |
| **Politico Pro** | Classifies by **job function**, **business decision maker**, **C-suite**, CEO |
| **Omeda** (publisher reg-wall vendor) | Name, email, company, job title, industry — **3–5 required fields max**, then progressive profiling |

**What we lack that they collect:** decision/purchase authority · company size · LinkedIn or social profile · a capture date · engagement stored on the person record (login count, downloads, ratings).

**The structural difference:** everyone else asks **few fields many times** (progressive profiling). We ask **many fields once**. That is why our form has ~20 fields and our data has three.

---

## 14. Open items before this is locked

1. **Confirm the warehouse assets with Prapti** — `contact_360` (328K unified contacts), `company_360` (75K companies), the existing RFV implementation, and `silver.events` are cited from repo documentation, not a live read.
2. **Confirm how App authentication works** — if it is OTP/phone-based, phone is the primary identifier and email becomes optional.
3. **Re-measure the App baseline** under the full Identified definition. It has role coverage but **zero** employer data, so its IA-30 will drop materially from 804.
4. **Fix DataLabs measurement** — one of four products currently has no usable baseline.
5. **Decide how `student` and `other` are treated** — roughly 13% of existing role data. Recommendation: Identified, but excluded from the in-market cut. Not discarded.
6. **Audit the 10 existing activation definitions** against what actually fires. Prior work found only 3 of 9 QIA activities were being computed; a similar gap is likely here.
7. **Re-derive the 2-day line** once scroll depth lands and all four surfaces compute together.
8. **Review with Utkarsh** as a replacement for QIA — same ambition, working arithmetic underneath.
