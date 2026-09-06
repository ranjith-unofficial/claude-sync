# Inc42 Audience Metric — Definition

**Date:** 7 September 2026 · **Owner:** Ranjith · **Status:** proposed, replaces the QIA definition (keeps the name)
**Data:** PostHog live pull, 6–7 Sep 2026, internal excluded

---

## 1. The goal

Four products — **Media, App, DataLabs, IP** — serving one person, under One Inc42.

We need one number that:
- Counts a **person**, not four users in four reports
- Works **today**, with ~98% of web behaviour anonymous
- **Never changes definition** as data improves — it starts small and grows
- Leads to **revenue**, without requiring revenue to be today's target

QIA is the right ambition. Its current arithmetic doesn't work: it's a binary flag with no gradient, its value is set by which form someone filled, and on Media it resolves to 25 people.

**This keeps the name and fixes the arithmetic.**

---

## 2. The metric — three levels

| Level | Definition |
|---|---|
| **IA** — Identified Actives | People we can name **and** who did a qualifying action in the window |
| **QIA** — Qualified Identified Actives | IA who match the **ICP of the product they used** |
| **QIA Repeat Rate** | Of QIA, the share who returned on a **2nd separate day** in the window |

> **Window = 15 days.**

### Why 15 and not 7 or 30

Measured gap between someone's 1st and 2nd active day:

| Repeat happens within | Media | App |
|---|---|---|
| ≤ 7 days | **73%** | **96%** |
| ≤ 15 days | **92%** | **~99%** |
| ≤ 30 days | 100% | 100% |

- **30 days is too slow** — 92% of the signal is already in by day 15.
- **7 days under-counts Media by 27%.** Media is a lower-frequency product by nature; a 7-day window would make our biggest identification opportunity look broken and push effort to the App, which is already 71% identified.

**Never mix windows.** Repeat rate is 37% at 7 days and 57% at 30 for the *same audience*. Switching between reports looks like a 20-point collapse that never happened.

---

## 3. How each level leads to revenue

| Level | What it is | Revenue role |
|---|---|---|
| **Reach** | Anonymous | Nothing yet. Raw material. |
| **IA** | We know who they are | **Now reachable.** Can be emailed, retargeted, invited. |
| **QIA** | They match a product's ICP | **Now sellable to.** The addressable base for DataLabs, IP, and any Media subscription. |
| **QIA Repeat** | They keep coming back | **Now likely to convert and renew.** Nobody buys something they visited once. |

**The chain:** Reach → we know them → they're the right kind of person → they have a habit → they buy.

**Where the money actually comes from:** DataLabs and IP are the two monetisable lines. Both are sold to *people*, and both have a seniority floor — a junior analyst cannot expense DataLabs, and IP is invitation-grade. **QIA is the number that says how many people we have who can actually buy.**

**Honest limit:** reader-to-payer conversion in media sits near 1.4% and is a hard category norm. QIA rising 10x does not make revenue rise 10x. But **`payers ÷ QIA` is the metric when money becomes the focus — QIA is its denominator.** Building it now is not a detour.

---

## 4. Defining "qualified" — the ICP

Qualification is **per product**, because the products have different buyers.

### How we derived it

Three cohorts compared on Media — the whole identified base, 15-day actives, and everyone who has ever paid (Plus/Pro):

| Seniority | Base | Payers | **Payer rate** | vs average |
|---|---|---|---|---|
| **Founder** | 5,276 | 109 | **2.07%** | **1.8x** |
| **CXO** | 1,472 | 26 | **1.77%** | **1.6x** |
| **Senior mgmt / VP** | 5,070 | 80 | **1.58%** | **1.4x** |
| Other | 4,729 | 43 | 0.91% | 0.8x |
| **Junior mgmt** | 5,552 | 36 | **0.65%** | **0.6x** |
| **Student** | 4,929 | 10 | **0.20%** | **0.2x** |

**A founder is 10x more likely to pay than a student, and 3x more likely than junior management.** This confirms the thesis: seniority gates purchase, and it does so steeply.

**Who's actually active on Media right now (15d, by role):** Founder 181 · Other 106 · Senior/VP 102 · Junior mgmt 98 · Student 39 · Middle mgmt 38 · CXO 36 · Investor 14.

**DataLabs payer data is confounded and excluded from this derivation.** Its payer rates correlate with *snake_case vs spaced* role values (`founder_owner_ceo` 4.33% vs `founder` 0.45%) — a form-vintage artifact, not a behavioural difference. Newer onboarding forms were used on paid flows. **Do not read DataLabs ICP off this data until the vocabularies are merged.**

### The ICP per product

| Product | Who can realistically buy | **Qualified (counts to QIA)** | Not qualified |
|---|---|---|---|
| **DataLabs** | Needs budget authority | Founder · CXO · VP/Director · Partner · Principal · **Analyst/Associate at investor or research firms** · Market researchers | Students · junior mgmt without budget |
| **IP / Summits** | Invitation-grade only | Founder · CXO · Partner · VP+ | Everyone below VP |
| **Media** (if subscribed) | Broadest — juniors possible, lower propensity | All seniority levels in-market | Students |
| **App** | Free — widest | Everyone in-market | Students |

### Naming the segments

| Name | Who | Media evidence |
|---|---|---|
| **Proven buyers** | Segments that have already paid | Founder, CXO, Senior/VP — all over-index |
| **Probable buyers** | Same profile, haven't paid yet | The 181 active founders, 102 senior, 36 CXO not yet on a plan |
| **Audience** | Qualified, but not this product's buyer | Junior mgmt for DataLabs; anyone sub-VP for IP |
| **Out of market** | Never qualifies | Students (0.2% payer rate), SEO/link-building, unusable roles |

---

## 5. Where we stand today

**15-day window, identified = has an email** (the full definition is stricter — see §6, and these will drop):

| | Media | App | DataLabs | IP |
|---|---|---|---|---|
| Total people seen (30d) | 500,661 | 1,133 | ~136,000 | — |
| Behaviour we can attribute | **2.01%** | **70.32%** | **2.44%** | — |
| **IA-15** | **998** | **733** | *unreliable* | unmeasured |
| **Repeat Rate-15** | **47.6%** | **54.7%** | unknown | unmeasured |
| Median time to 2nd day | 2 days | **1 day** | unknown | unmeasured |

**Under the full definition** (email + job title + company), Media's 30-day IA drops from 1,389 to **571**. QIA will be smaller again once ICP is applied.

**Two facts that should drive planning:**

**Repeat rate is 48% on Media and 55% on the App — close. Repeat is not the broken thing. Identification is.**

| | Scale | Identity |
|---|---|---|
| **Media** | 500,661 people | **0.28% identified** — scale without identity |
| **App** | 1,133 people | **71% identified** — identity without scale |
| **DataLabs** | ~136,000 | 2.44% of behaviour — neither |

**The arithmetic of where to spend effort** (Media):

| Lever | Move | Repeaters | Gain |
|---|---|---|---|
| Repeat rate | 48% → **100%** (impossible) | 998 | +523 |
| **Identification** | 0.28% → **1%** | 2,854 | **+2,065** |
| Identification | 0.28% → **2%** | 5,707 | **+4,918** |

**Identification beats a physically impossible repeat rate by 4x.**

---

## 6. What we collect

> **Identified = (Email or Phone) + Job Title + Company Name**

**Asked — 3 required, 1 confirmation:**

| Field | Required |
|---|---|
| Email or phone | Yes — whichever the login uses |
| **Job title** (free text) | Yes |
| **Company name** (autocomplete) | Yes |
| Seniority + Function | Pre-filled from job title, one tap to correct |

**Derived — never asked:**

| From | We get |
|---|---|
| Job title | **Seniority band, Function** |
| Company name | **Industry, Company Type, Company Size** |

Every field carries `captured_at` and `source`. **Role goes stale after 24 months** and drops out of QIA until reconfirmed — the BPA standard; without it a qualified count silently rots.

### Why company name, not industry

| Definition | People |
|---|---|
| Email + title + **Industry** | 1,384 |
| Email + title + **Company name** | **18,471** |

`Industry` has 7,106 records. `Company Name` has **73,205**, and `company_360` holds 75,000 companies. We were asking a question we can already answer.

### Why seniority is derived, not asked

`Designation` is not a job title — it's a **second seniority dropdown** (`founder`, `senior-management`, `junior-management`, `student`). We ask the same question twice into two fields. They cover different people: **merging them lifts role coverage from 34,032 to 54,725, a 61% gain with no new questions.**

The standalone dropdown must not be reused as-is — it mixes seniority, role type and life stage. The result is already visible: **192 people picked "Investor" as their seniority while working at early-stage startups.**

### What counts as a qualifying action

Utkarsh's 10 criteria, adopted as-is. Three flags:

1. **Those people-counts are all-people, not identified-only.** Web Search Completed shows 2,530 people/30d, but Media has only 1,389 identified actives in total. **Filtered to Identified, these numbers collapse.** Nobody should expect IA near 2,530.
2. **Criterion #1 contributes zero on web** — scroll is dead, so *reading an article* doesn't count on our largest surface. Media's IA is currently driven by search, newsletter clicks and registrations. **Restoring scroll changes the metric's composition, not just its size** — pre-announce it so the jump isn't read as growth.
3. **Criterion #6 (Ask/AI) is instrumented but not piped** — it can't count today.

---

## 7. Questions this will get

**"Why three numbers instead of one north star?"**
It is **one** north star — QIA. IA is its input and Repeat Rate is its quality check. Reporting QIA alone lets it be gamed: gate aggressively and QIA rises while repeat rate collapses, and nobody sees it. The three are one metric with its numerator, denominator and integrity check shown.

**"Isn't this just QIA renamed?"**
Same name, same ambition, working arithmetic. Three changes: qualification comes from **ICP fit** rather than a form field being filled; the window is **15 days** rather than 30; and repeat behaviour is measured rather than assumed.

**"Why is the number so small?"**
Because it's true. Media has 571 people meeting the full identified bar. The honest number is the one that can go down.

**"Won't gating fix identification overnight?"**
It would, and it would also destroy reach. **Total reach is published beside QIA every time. Any gain that arrives with a reach drop does not count.**

**"Students and juniors read us — are we writing them off?"**
No. They're **Identified, not Qualified for DataLabs or IP**. They still count in IA, still get served, still convert to Media subscriptions at 0.65–0.2%. They just aren't the addressable base for the two products we monetise.

---

## 8. What has to be built

**Blockers**
1. **Collapse the five email fields into one** — `email`, `Email`, `Work Email`, `work_email`, `Personal Email`. **33,981 people (27% of everyone reachable) have an address in a field that isn't `email`.** Every count is wrong until this is fixed.
2. **Merge `Designation` + `Seniority`** onto one ladder — 54,725 existing answers, plus DataLabs' snake_case vocabulary.
3. **Company name → `company_360` resolver** — 73,205 names waiting to become Industry, Type, Size.
4. **Job title normaliser** — lookup table plus LLM fallback → seniority, function.
5. **`captured_at` and `source`** on every identity field.

**Data integrity**
6. **`Phone Number` is stored as numeric**, destroying `+91` and leading zeros — 6,348 records affected.
7. **Restore Scroll Depth on Media.**

**Pipeline**
8. Media's PostHog→warehouse export **exists but has been paused since ~29 July** — find out why before un-pausing. DataLabs and App have none.
9. **Do not merge the PostHog projects.** Keep streams separate, unify downstream. **A person-level metric cannot be computed inside PostHog** — the same DataLabs window returns 199 or 2,001 people depending on query shape. It must run on `unified_contact_id` in BigQuery.
10. **IP/summits is entirely unmeasured** despite attendees handing over full details in person — structurally our highest-yield identification surface.

---

## 9. Open items

1. **Confirm with Prapti** — `contact_360` (328K contacts), `company_360` (75K companies), `silver.events` are cited from repo documentation, not a live read.
2. **Confirm App auth** — if OTP/phone-based, phone is the primary identifier, not email.
3. **Re-derive the DataLabs ICP** once role vocabularies are merged. Current payer rates are a form-vintage artifact.
4. **Ratify the per-product ICP table in §4** — a reasoned hypothesis from Media payer data, not yet validated on DataLabs or IP.
5. **Audit the 10 activation criteria** against what actually fires, filtered to identified people only.
6. **Re-derive the repeat line** once scroll depth lands.
