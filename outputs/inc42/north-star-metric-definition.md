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
| **Repeat Rate** | Share who returned on a **2nd separate day** in the window |

> **Window = 15 days.**

### What we optimise against — now vs later

**Today we optimise on IA and Repeat Rate of IA. We do not optimise on QIA.**

The qualified base is currently a few hundred people. At that size a single campaign or bug moves it 15%, and chasing it would produce decisions driven by noise. QIA is computed, tracked and reported from day one — it is simply not the number teams steer by yet.

**The switch is a change of focus, not of definition.** All three definitions are fixed now and never change. When the QIA base clears **~1,000 people**, the operating focus moves from IA to QIA and Repeat Rate follows it. Nothing gets redefined — we start steering by a number that was always being measured.

### Why 15 days and not 7 or 30

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
| **Repeat** | They keep coming back | **Now likely to convert and renew.** Nobody buys something they visited once. |

**The chain:** Reach → we know them → they're the right kind of person → they have a habit → they buy.

**Where the money actually comes from:** DataLabs and IP are the two monetised lines. Both are sold to *people*, and both have a floor — a junior analyst cannot expense DataLabs, and IP is senior-only by design. **QIA is the number that says how many people we have who can actually buy.**

**Honest limit:** reader-to-payer conversion in media sits near 1.4% and is a hard category norm. QIA rising 10x does not make revenue rise 10x. But **`payers ÷ QIA` is the metric when money becomes the focus — QIA is its denominator.** Building it now is not a detour.

---

## 4. Defining "qualified" — the ICP

Qualification is **per product**, because the products have different buyers. A person is Qualified if they match the ICP of the product they used.

### Evidence: Media — who actually pays

Whole identified base vs everyone who has ever paid (Plus/Pro):

| Seniority | Base | Payers | **Payer rate** | vs avg |
|---|---|---|---|---|
| **Founder** | 5,276 | 109 | **2.07%** | **1.8x** |
| **CXO** | 1,472 | 26 | **1.77%** | **1.6x** |
| **Senior mgmt / VP** | 5,070 | 80 | **1.58%** | **1.4x** |
| Other | 4,729 | 43 | 0.91% | 0.8x |
| **Junior mgmt** | 5,552 | 36 | **0.65%** | **0.6x** |
| **Student** | 4,929 | 10 | **0.20%** | **0.2x** |

**A founder is 10x more likely to pay than a student, and 3x more likely than junior management.** Seniority gates purchase, steeply.

**Who is active on Media now (15d, by role):** Founder 181 · Other 106 · Senior/VP 102 · Junior mgmt 98 · Student 39 · Middle mgmt 38 · CXO 36 · Investor 14.

### Evidence: DataLabs — a completely different buyer

Derived from `User_Profile_Fixed`, DataLabs' own computed persona field (40,411 records). This field is applied uniformly, so unlike the seniority dropdown it is not confounded by which onboarding form someone filled.

| Persona | Base | Payers | **Payer rate** | vs avg |
|---|---|---|---|---|
| **Investor** | 3,064 | 141 | **4.60%** | **2.5x** |
| **Sales & Marketing** | 6,284 | 139 | **2.21%** | **1.2x** |
| Founder/CXO | 12,206 | 208 | 1.70% | 0.9x |
| **Market Researcher** | 18,203 | 243 | **1.34%** | **0.7x** |
| Other | 653 | 0 | 0% | — |

**DataLabs is investor-first.** On Media, founders convert best. On DataLabs, investors convert at 2.5x average and founders sit *below* average.

**The uncomfortable finding: Market Researcher is DataLabs' largest segment — 46% of the classified base — and its worst-converting. The biggest audience is the wrong audience.**

### The ICP per product

| Product | **Qualified — counts to QIA** | Not qualified | Basis |
|---|---|---|---|
| **Media** | Founder · CXO · Senior Management/VP · Middle Management · Investor · Researcher · **Other (provisional)** | **Students** (0.20% payer rate) · **Junior Management** (0.65%) · undefined/unusable values | Payer gradient above — the senior ladder converts at 1.4–1.8x average; juniors at 0.6x and students at 0.2x do not clear the bar |
| **DataLabs** | Investor · Sales & Marketing · Founder/CXO · Market Researcher — **everything except "Other"** | **"Other" persona only** (653 people, **0 payers**) | Persona payer data above — all four personas convert; "Other" has never produced a single sale |
| **IP / Summits** | **Senior Manager and above**, any company type | Everyone below senior manager | Admission is senior-only by design |
| **App** | Anyone matching the **Media, DataLabs or IP** ICP | Only those matching none | The App is generic — it feeds all three |

**Note the deliberate asymmetry on "Other".** Media keeps it (4,729 people, 0.91% payer rate — half of average but non-zero). DataLabs drops it (653 people, zero sales ever). The same label means different things on the two products, and the data says so.

### The "Other" problem solves itself

"Other" is provisional on Media because we do not know what those 4,729 people actually are. **Under the new form it stops existing** — job title is free text, so there is no "Other" button to press. That leaves only two jobs:

- **New captures:** nothing to do. The category disappears at the point the new form ships.
- **Legacy base:** a one-time re-ask of everyone currently sitting on "Other". Until that runs, those people remain provisionally qualified and are reported as a separate line so the exposure is visible.

**91 of Media's 438 QIA (21%) currently rest on this provisional rule.** If "Other" were excluded tomorrow, Media QIA drops to 347.

### Naming the segments

| Name | Who |
|---|---|
| **Proven buyers** | Segments that already pay — Media: Founder, CXO, Senior/VP · DataLabs: Investor, Sales & Marketing |
| **Probable buyers** | Same profile, haven't paid yet — the 181 active Media founders, 102 senior, 36 CXO not on a plan |
| **Audience** | Identified but not qualified anywhere — junior management (0.65% on Media, cannot expense DataLabs, below the IP bar) |
| **Out of market** | Never qualifies — students (0.20% payer rate), SEO/link-building, undefined/unusable role values |

### Caveats on the derivation

- **Survivorship bias.** People who paid are people who hit a paywall, i.e. were already engaged. Part of both gradients measures engagement, not fit. Should be re-run within equally-engaged cohorts.
- **Thin cells on Media.** 304 payers with a role across six buckets; CXO (26) and Student (10) are small. Direction is sound; the multiples are not precise.
- **Mixed eras.** "Ever paid" counts a 2021 churner the same as an active subscriber.
- **DataLabs seniority is unusable** for this purpose — payer rate there tracks the *format* of the role value (`founder_owner_ceo` 4.33% vs `founder` 0.45%), a form-vintage artifact. The persona field above is used instead, and the seniority field must not be used for DataLabs ICP until vocabularies are merged.

---

## 5. Where we stand today

**15-day window, identified = has an email** (the full definition is stricter — see §6, and these numbers will drop):

| | Media | App | DataLabs | IP |
|---|---|---|---|---|
| Total people seen (30d) | 500,661 | 1,133 | ~136,000 | — |
| Behaviour we can attribute | **2.01%** | **70.32%** | **2.44%** | — |
| **IA-15** | **998** | **733** | *unreliable* | unmeasured |
| **Repeat Rate-15** | **47.6%** | **54.7%** | unknown | unmeasured |
| Median time to 2nd day | 2 days | **1 day** | unknown | unmeasured |

### QIA, with the ICP applied — Media, 30 days

| Bucket | People |
|---|---|
| Identified actives (email present) | 1,389 |
| **— of which have NO ROLE at all** | **693 (50%)** |
| Qualified — senior ladder | 385 |
| Qualified — Other (provisional) | 106 |
| Qualified — investor / researcher | 27 |
| Excluded — junior management | 101 |
| Excluded — student | 39 |
| Excluded — undefined / unusable | 31 |

**Under the full definition** (email + job title + company): IA = **570**, of which **QIA = 438**. Ninety-one of those 438 rest on the provisional "Other" rule.

**The finding that matters more than the ICP rule itself:** excluding juniors and students costs 140 people. **Missing role data costs 693.** The binding constraint on QIA is not who we disqualify — it is that half of our identified actives never told us what they do. That is a capture problem, and it is 5x larger than the qualification question.

This is also why the operating focus is IA today: at 438 people, QIA moves 15% on a single campaign.

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

> **Identified = Email + Job Title + Company Name**

App login is email-OTP, so **email is the identifier across every surface.** Phone is optional enrichment and gates nothing.

**Asked — 3 required, 1 confirmation:**

| Field | Required |
|---|---|
| **Email** | Yes |
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

### Current field coverage — Media (10,473,428 person records)

| Field | Populated |
|---|---|
| Any email field | 126,849 |
| `email` specifically | 92,868 |
| **Company Name** | **73,205** |
| Seniority ∪ Designation | 54,725 |
| Industry | 7,106 |
| Company Type | 948 |
| Function | **40** |
| Interests | **40** |
| City | **7** |

**We are not missing the fields. We are missing the asking.**

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

**"Why are we steering by IA and not QIA?"**
Because the qualified base is a few hundred people and would swing 15% on a single bug. QIA is measured and reported from day one; we start steering by it when it clears ~1,000. **Definitions never change — only which one we optimise against.**

**"Why is the number so small?"**
Because it's true. Media has 571 people meeting the full identified bar. The honest number is the one that can go down.

**"Won't gating fix identification overnight?"**
It would, and it would also destroy reach. **Total reach is published beside IA every time. Any gain that arrives with a reach drop does not count.**

**"Students and juniors read us — are we writing them off?"**
They stay in **IA** — counted, served, and part of reach. They are not in **QIA**, because QIA measures the people who can actually buy. Juniors convert at 0.65% and students at 0.20%, against a senior ladder at 1.4–1.8x average; neither can expense DataLabs and both sit below the IP bar. Writing them out of the *sellable* number is not writing them out of the audience.

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
9. **Do not merge the PostHog projects.** Keep streams separate, unify downstream. **A person-level metric cannot be computed inside PostHog** — the same DataLabs window returns 199 or 2,001 people depending on query shape, because person-on-events stores properties as event-time snapshots. It must run on `unified_contact_id` in BigQuery.
10. **IP/summits is entirely unmeasured** despite attendees handing over full details in person — structurally our highest-yield identification surface. `silver.events` already holds registrations and paid tickets; it needs to be wired into the same computation.

---

## 9. What we need to confirm about `contact_360` and `company_360`

The whole metric computes against these two tables. Four things must hold for `contact_360`:

| Question | Why it decides the metric |
|---|---|
| Does `unified_contact_id` survive one person appearing in two systems under **different emails**? | If not, every cross-product count double-counts |
| Which source **wins** when role or company conflict across the 7+ inputs? | Determines whether QIA reflects the newest answer or the oldest |
| Is there a **timestamp per field**, or only per record? | Without per-field dating, the 24-month decay rule cannot be implemented |
| Does it hold **PostHog behaviour**, or only CRM/transactional data? | Per repo docs it holds neither — meaning "Active" cannot be computed there yet |

Three for `company_360`:

| Question | Why |
|---|---|
| What is the **match rate** from free-text company name to a `company_360` row? | This single number decides whether 73,205 names become ~70,000 resolved employers or ~20,000 |
| Does it carry **company type and size**, or only sector? | We need type and size; sector alone qualifies nobody |
| Does it cover **non-startup** employers — VCs, corporates, agencies, universities? | Investors are DataLabs' best-converting segment, so VC coverage is critical |

**The blunt version: if `company_360` matches well, this metric works. If it matches badly, we are back to asking people for their employer type — the field with 948 records.**

---

## 10. Remaining validation

1. **Re-run both payer gradients controlling for engagement**, to separate ICP fit from paywall exposure.
2. **Audit the 10 activation criteria** against what actually fires, filtered to identified people only.
3. **Re-derive the repeat line** once scroll depth lands and changes what counts as a qualifying action.
4. **Confirm the `contact_360` / `company_360` answers in §9** with Prapti before build starts.
