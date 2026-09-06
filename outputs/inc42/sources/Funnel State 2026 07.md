# Datalabs: State of the Funnel

**Date**: 2026-07-30 **Window**: PostHog Jun 1 to Jul 29 2026 (weekly headline \= Jul 20 to 26\) · Razorpay and Metorik launch (Apr 22\) to date **Sources**: PostHog project 66351 (direct API), Razorpay payments, Metorik order and subscription snapshots, GSC **Companion docs**: `analytics/august-mop-2026.md` (the plan) · `analytics/pro-trial-funnel-analysis-2026-07.md` (trial deep-dive) · `tools/weekly-brief/METHODOLOGY.md` (how these numbers must be measured)

This is the diagnostic. It states where the business actually is at each step of the funnel and what the analysis concluded. The August plan is a separate document and contains only the actions.

---

## The funnel end to end

Weekly steady state, using the week of Jul 20 to 26 where the metric is weekly, and launch-to-date where the metric is cumulative.

| Step | Volume | Conversion from previous | Health |
| :---- | :---- | :---- | :---- |
| Sessions (pageview-bearing) | 25,947 | — | 🟡 spiky, not trending |
| Registrations | **524 people** | 2.02% | 🟢 strongest week on record |
| Entered onboarding | 377 | 71.9% | 🔴 **28.1% never enter** |
| Completed onboarding | 329 | 87.1% of those who enter | 🟡 |
| Activated (v3) | 371 | 77.5% of onboarded | ⚪ metric is not meaningful, see §4 |
| Hit a Pro lock | \~106 | \~20% of registrants | 🟡 |
| Clicked upgrade | 39 | 36.8% | 🔴 |
| Reached checkout | 27 | 69.2% | 🔴 |
| Started trial (mandate created) | **20** | 74.1% | 🟢 tripled since June |
| Trial converts to paid | 25.4% | — | 🟡 flat since launch |
| Survives to month 2 | 52.2% | — | 🔴 |
| Survives to month 3 | 23.1% | — | 🔴 |

**Compounded: roughly 3% of real trials reach a third charge.** 37 of 48 paying subscriptions have exactly one successful charge.

**The shape of the problem**: acquisition is working and improving, the middle is leaky but ordinary, and the bottom is broken by mechanics rather than by demand. Trials tripled without MRR following, because trials die at the day-7 debit.

---

## 1\. Traffic and awareness

**Current state**: 25,947 pageview-bearing sessions in the week, 22,859 users, 21,129 of them new.

| Channel | Sessions | Share |
| :---- | :---- | :---- |
| Organic Search | 11,774 | 45.4% |
| Direct | 11,571 | 44.6% |
| Referral | 1,900 | 7.3% |
| AI Search | 389 | 1.5% |
| Email | 198 | 0.8% |
| Organic Social | 72 | 0.3% |

**Traffic is spiky, not trending.** Eight-week session series: 13.6K, 14.5K, 14.9K, 14.3K, 21.1K, 30.2K, 20.2K, 25.9K. The week's headline "+28.5% WoW" is measured off a trough; against the Jul 6 peak this week is **down 14%**.

**The news.google.com spike was noise.** It ran 0 to 50 to 1,225 sessions over three weeks, peaked Jul 23 at 1,009, and decayed to 4/day within five days. Quality: **95.9% bounce, 10 seconds average duration, 1.02 pageviews per session**, against 40.2% / 149s / 1.73 for the rest of the site. It produced **1 to 2 registrations in 91 days**. It contributed roughly 7.6% of this week's sessions, so it inflated the headline while adding nothing.

**AI search is growing steadily**: 254 → 297 → 333 → 327 → 333 → 351 → 345 → 389 sessions over eight weeks, \+53%, near-monotonic. Assistant mix is ChatGPT 79%, then Perplexity, Gemini, Claude, Copilot.

**Takeaway**: the only durable growth in traffic is Google organic. Direct is 44.6% of sessions but averages 1.39 pageviews and converts at 0.47%, so it is a residual bucket (returning, untagged, bot), not a channel. Weekly session deltas should not be read as trend without checking the 8-week series.

---

## 2\. Acquisition and registration

**Current state**: 524 registrations in the week (540 events; the event fires more than once for some people).

### Attribution was wrong by roughly 10x

For five weeks the brief reported registrations as **98.1% Direct** and the team concluded SEO-to-signup was unmeasurable. That was a query defect, not a tracking gap.

The brief read `person.properties['$initial_referring_domain']` **on the `Registered` event**. PostHog resolves person properties as of event time, and `Registered` fires at the instant of identification, before the person profile is written, so the property is NULL for **518 of 524** registrants. NULL was then mapped to "Direct".

| Channel | Registrants | Share | Previously reported |
| :---- | :---- | :---- | :---- |
| **Organic Search** | **352** | **67.2%** | \~1% |
| Referral (95 of 96 \= inc42.com) | 96 | 18.3% | \~1% |
| **Direct** | **54** | **10.3%** | **98.1%** |
| AI Search | 21 | 4.0% | 0 |

Verified three independent ways (event-level `$referring_domain`, `session.$entry_referring_domain`, post-identify `argMax` of the person property), all agreeing within a few units. **Fixed, and the fix is retroactive across all history.**

### Channel efficiency

| Channel | Sessions | Regs | Session → reg | Activated | Session → activated |
| :---- | :---- | :---- | :---- | :---- | :---- |
| AI Search | 389 | 21 | **5.40%** | 14 | **3.60%** |
| Referral | 1,900 | 96 | **5.05%** | 46 | 2.42% |
| Organic Search | 11,774 | 352 | 2.99% | 211 | 1.79% |
| Direct | 11,571 | 54 | **0.47%** | 33 | 0.29% |
| **Total** | **25,947** | **524** | **2.02%** | 305 | 1.18% |

AI is the most efficient channel end to end, at roughly 2x organic and 12x direct, but at 1.5% of traffic it is a trajectory bet rather than a volume lever. **AI registrations are flat at 18 to 30 per week and the reg rate has fallen from 7.1% to 5.4% as volume grew.**

**Referral is decaying**: registrations fell 136 to 96 over eight weeks, down 29%, on our best high-volume channel.

### The registration wall works only where data is specifically gated

| Entry page type | Sessions | Regs | Reg % |
| :---- | :---- | :---- | :---- |
| datalabs home | 461 | 25 | **5.42%** |
| company: financials | 2,256 | 107 | **4.74%** |
| company: captable | 2,575 | 83 | 3.22% |
| lists | 738 | 21 | 2.85% |
| person | 2,095 | 40 | 1.91% |
| industry | 1,295 | 24 | 1.85% |
| **company: other** | **13,466** | 186 | **1.38%** |
| company: funding | 1,819 | 21 | 1.15% |
| reports | 707 | 1 | **0.14%** |

**Takeaway**: generic company pages are 52% of all sessions and convert at a third the rate of financials or cap-table pages on the same underlying entity. This is the single largest volume opportunity in the funnel, and it is a product/UX difference rather than an SEO one. `/reports/` at 0.14% is functionally broken.

---

## 3\. Onboarding

**Current state**: real completion is **87.1%**, not the 100% reported for months.

The brief read `properties['state']`, a key that does not exist, so every row returned NULL and the code fell back to treating every `Datalab Onboarding` event as a completion. The real key is `Datalab Onboarding State`, and it is fully populated.

| Stage | People (week of Jul 20\) |
| :---- | :---- |
| Onboarding Step 2 | 479 |
| Onboarding Step 3 | 444 (92.7%) |
| Onboarding Completed | **417 (87.1%)** |

Stable at 85 to 91% across 14 weeks. **There is no `Onboarding Step 1` event anywhere in 90 days**, so the observed top of funnel is Step 2 and 87.1% is an upper bound.

### The larger hole: 28% never enter onboarding at all

| Cohort | Registrants | Any onboarding event | Completed |
| :---- | :---- | :---- | :---- |
| Registered 30 to 60 days ago | 1,960 | 1,399 (71.4%) | **1,222 (62.3%)** |
| Registered Jul 20 to 26 | 524 | 377 (71.9%) | 329 (62.8%) |

These are **not bounces**. Never-onboarders average **24.8 events and 6.0 pageviews on day 0**. They are on site and engaged; the flow either never fires for them or they dismiss it. They return at 7.5% versus 28.3% for completers.

**Takeaway**: 37.7% of registrants never complete onboarding, and onboarding completion is a 3.4x retention predictor. This is the cheapest large retention lever in the product.

---

## 4\. Activation

**Current state**: 77.5%, flat, and the metric does not mean what it is used for.

Activation v3 \= an onboarded user performing 5+ activation events (`Advanced Filter Applied` OR a `/company/*` pageview). In practice that is "read five company pages", which is browsing.

| Day-0 activation events | n | Week-1 return |
| :---- | :---- | :---- |
| 0 | 251 | 12.0% |
| 1 to 2 | 52 | 21.2% |
| 3 to 4 | 242 | 12.0% |
| **5 to 9** | **735 (42%)** | **19.5%** |
| 10 to 19 | 347 | 23.6% |
| 20+ | 125 | **52.0%** |

**The 5+ bar admits 69% of users, and the 5-to-9 bucket, which is 42% of the whole cohort and the bulk of what the bar admits, returns at 19.5%, below the 20.5% cohort average.** All the discriminating power sits at 20+.

Holding activation constant makes the point decisively:

| Segment | n | Week-1 return |
| :---- | :---- | :---- |
| Activated (5+) **and** used a filter on day 0 | 165 | **51.5%** |
| Activated (5+), no filter | 1,042 | **19.7%** |
| Not activated, no filter | 534 | 12.9% |

One `Advanced Filter Applied` (2.81x lift, 10% penetration) outperforms the entire five-pageview bar (1.87x, 69% penetration).

**Takeaway**: a 77.5% activation rate that is flat and does not track retention is a vanity metric. It cannot go up meaningfully and it does not tell us anything when it moves.

---

## 5\. Engagement and feature adoption

**Current state**: every high-lift feature in the product is under 15% adoption, and the highest-lift ones are under 3%.

Cohort registered 65 to 130 days ago (n \= 3,521), feature usage in first 30 days, retention measured days 31 to 60\. Base retention 7.7%.

| Feature | Adoption | Retention if used | Lift |
| :---- | :---- | :---- | :---- |
| **Saved Search** | **2.7%** | 35.1% | **5.06x** |
| Advanced Filter Clicked | 9.8% | 26.0% | 4.56x |
| Table Pagination | 11.9% | 24.3% | 4.47x |
| Table Sort | 5.9% | 28.5% | 4.46x |
| **Advanced Filter Applied** | **14.5%** | 22.5% | 4.34x |
| **Customize Columns** | **2.0%** | 29.6% | 4.08x |
| Export | 2.6% | 26.4% | 3.66x |
| Search Completed | 15.4% | 17.7% | 3.01x |
| **Report Interaction** | **18.6%** | 10.4% | **1.47x** |
| List Interaction | 3.5% | 13.7% | 1.83x |
| Edit Interaction | 1.3% | 12.8% | 1.67x |

**The pattern is exact: every high-lift feature is a table power tool, and none of them exceeds 15% adoption.**

Dead surfaces: **Report Interaction** has the second-highest reach of any real feature (18.6%) and almost no lift (1.47x). List and Edit are dead on both axes. Ask Datalabs reaches 0.5%.

**Search is a day-0-or-never discovery**: 737 of roughly 830 first searches happen on day 0\. Only 39 people out of 1,752 (2.3%) discovered search later. Search users have been flat for 17 weeks (138 to 236 per week band) with no trend, and **26% of the search\_users goal metric is unregistered traffic** (582 logged-in vs 198 guest).

**Free-tier caps are irrelevant**: over 90 days, of 9,188 identified actives, List Interaction reached 2.5% and Saved Search 1.6%. You cannot meaningfully cap a feature 98% of users have never opened.

**Takeaway**: this is a discovery problem, not an entitlement or capability problem. The product's most retentive tools are effectively hidden.

---

## 6\. Monetisation

### The paywall funnel

| Stage | Jun 1 onward | This week |
| :---- | :---- | :---- |
| Hit a Pro lock | 801 | 106 |
| Clicked upgrade | 308 (38.5%) | 39 (36.8%) |
| Reached checkout | 162 (52.6%) | 27 (69.2%) |
| Started trial | 120 (74.1%) | 20 (74.1%) |

Two structural losses: **493 people who hit a paywall and never clicked** (the prompt's job), and **146 who clicked and never reached checkout** (one page transition after intent is expressed, which reads as a defect rather than a persuasion problem).

*Note: this week's click-to-checkout of 69.2% is materially better than the 52.6% eight-week average. Either it is improving or it is small-sample noise at n \= 39\. Worth confirming before concluding anything.*

### Trials are the healthiest number in the business

7 to 8 per week in early June, rising to a steady **20 per week** through July. Roughly tripled. Every trial starter is `User Type = Free`; no Pro members or existing trialists leak in.

Conversion is front-loaded and immediate: **49 convert on their first lock and 37 on their second** (72% within two), and **60 of the 98 trialists matchable to a registration started the trial the same day they registered**.

### Where trials come from

| First lock page | Locks | Trials | Rate |
| :---- | :---- | :---- | :---- |
| Investor Search | 16 | 4 | **25.0%** |
| Funding Search | 10 | 2 | 20.0% |
| My Feed | 53 | 10 | 18.9% |
| Company Search | 119 | 19 | 16.0% |
| **Company Profile** | **483** | 71 | 14.7% |
| Ask Datalabs | 15 | 1 | 6.7% |
| Industry Profile | 54 | 3 | **5.6%** |
| Person Profile | 18 | 1 | 5.6% |

Company Profile carries 60% of all lock exposure at an average rate. Industry Profile is a clear misfire.

| Persona | Locks | Trials | Rate |
| :---- | :---- | :---- | :---- |
| Founder/CXO | 200 | 36 | **18.0%** |
| Investor | 128 | 19 | 15.3% |
| Sales & Marketing | 145 | 20 | 13.8% |
| **Market Researcher** | **303** | 38 | **12.2%** |

We show the most locks to the persona least likely to buy.

| Device | Locks | Trials | Rate |
| :---- | :---- | :---- | :---- |
| unresolved | 677 | 104 | 15.4% |
| **mobile** | **120** | **6** | **5.0%** |

### Payment capture at signup is healthy

Every trial mandate is a uniform **₹10 authorization**.

| Level | Result |
| :---- | :---- |
| **User level** | 264 attempted, **233 captured (88.3%)** |
| Row level | 382 authorizations, 235 captured |

Row level badly understates success because users retry. **UPI is the dominant rail** (189 users first-choosing UPI vs 73 card), and UPI-first converts at 92.1% vs card-first 80.8%. Closing that gap entirely is worth roughly 0.6 trials per week, so payment method is not the lever.

### The payment lifecycle in three stages

Mandate setup, the first charge, and subsequent renewals are separate systems that fail differently. India-specific: UPI Autopay mandates need in-app approval at the PSP, card e-mandates need AFA/OTP, and RBI requires a pre-debit notification 24h before every recurring debit. The method split therefore matters far more than it would in a card-dominant market.

#### Stage 1 — Mandate setup (the ₹10 authorization)

| Measure | Value |
| :---- | :---- |
| Customers attempting | 251 |
| **First attempt succeeds** | **199 (79.3%)** |
| Of the 52 who failed first: retried at all | 36 (69.2%) |
| **Of those who retried, succeeded** | **29 (80.6%)** |
| **Final: mandate created** | **228 (90.8%)** |
| Never created | 23 (9.2%) |

**Retry is doing heavy lifting: it converts a 79.3% first-attempt rate into 90.8% final, and 80.6% of people who retry succeed.** But 31% of those who fail never try again.

**By rail, first attempt vs final:**

| Method | Customers | 1st attempt | Final |
| :---- | :---- | :---- | :---- |
| **UPI** | 184 | **84.8%** | **92.4%** |
| Card | 65 | **66.2%** | 89.2% |
| e-mandate | 2 | 0% | 0% |

UPI is better at mandate setup on the first attempt (84.8% vs 66.2%) and is already the default choice for 73% of customers. After retries the gap narrows to 92.4% vs 89.2%, i.e. **card users mostly get there, they just take more attempts.**

**What actually fails, and what gets overcome:**

| Failure on first attempt | n | Recovered | via method switch |
| :---- | :---- | :---- | :---- |
| **Auth abandoned** (OTP / UPI approval not completed) | **24** | 54.2% | 10 |
| User cancelled at auth | 13 | 46.2% | 2 |
| Insufficient balance | 4 | 100% | 1 |
| Card tokenisation failed | 2 | 100% | 0 |
| Card 3DS disabled | 1 | 100% | 0 |

**The dominant setup failure is not a decline, it is abandonment at the authentication step** — the customer never completes the OTP or the UPI approval. Nearly half recover, and 10 of them only by switching payment method, which is a strong argument for offering the alternate rail immediately after a failed attempt.

**Setup has improved sharply, and there was a real incident:**

| Week | Captured |
| :---- | :---- |
| 2026-05-10 | low, on \~3x normal attempt volume |
| 2026-06-28 | 24/33 (72.7%) |
| 2026-07-12 | 26/35 (74.3%) |
| 2026-07-26 | 20/24 (83.3%) |

May shows a clear incident: a retry storm against a broken flow, with 31 auth abandonments that month. **Something was fixed around mid-May** and setup has been stable at \~68 to 83% since. Monthly final: **May 84.6% → June 93.1% → July 93.5%.**

#### Stage 2 — First recurring charge (the day-7 trial-to-paid conversion)

| Measure | Value |
| :---- | :---- |
| Subscriptions reaching it | 95 |
| **Captured** | **55 (57.9%)** |
| Failed | 40 (42.1%) |

| Failure | n |
| :---- | :---- |
| **Insufficient balance** | **18** |
| **Token not confirmed** (mandate never approved) | **12** |
| Mandate inactive | 3 |
| Bank declined | 2 |
| Card blocked / pre-debit notif / user cancelled | 3 |

**This is the only stage getting worse**: 73.7% (May) → 54.2% (June) → **53.8% (July)**. By method, UPI 55.4% and card 63.3% — the one place cards outperform UPI, consistent with `INSUFFICIENT_BALANCE` dominating, since UPI Autopay debits a bank account at one fixed moment with no retry.

#### Stage 3 — Second and subsequent charges (true renewals)

| Measure | Value |
| :---- | :---- |
| Subscriptions reaching it | 16 |
| Captured | 10 (62.5% of subs; 14 of 20 attempts \= 70.0%) |

Failures: insufficient balance 4, card expired 1, token not confirmed 1\. **Improving**: 55.6% (June) → 81.8% (July) at attempt level. Small n — treat directionally.

#### Is `RECURRING_TOKEN_NOT_CONFIRMED` already fixed? No.

Weekly share of recurring attempts:

| Week | Occurrences |
| :---- | :---- |
| 2026-06-07 | 2/9 (22.2%) |
| 2026-06-28 | 1/11 (9.1%) |
| 2026-07-05 | 3/16 (18.8%) |
| 2026-07-12 | 0/13 |
| **2026-07-19** | **2/15 (13.3%)** |
| 2026-07-26 | 0/13 |

**Most recent occurrence: 2026-07-21.** It is intermittent rather than trending away, and it is still live. Monthly share ran 10.5% (May) → 18.2% (June) → 7.9% (July), so it may be partially mitigated, but it has not been eliminated and should not be assumed closed.

#### End to end

| Stage | Reaching it | Succeeding | Rate |
| :---- | :---- | :---- | :---- |
| 1\. Mandate setup | 251 customers | 228 | **90.8%** |
| 2\. First charge (day-7) | 95 subscriptions | 55 | **57.9%** |
| 3\. Second charge | 16 subscriptions | 10 | **62.5%** |

Note only 95 of 228 mandate-holders have reached a first charge: the rest cancelled during the trial or are still in it.

> **Exclusion applied.** All figures in this section exclude internal and test accounts via `tools/shared/internal-emails.js` — 43 of 500 payment rows (8.6%), 13 distinct accounts, including Inc42 staff and Razorpay's own team testing the integration. **40 of the 43 were mandate-setup rows**, so Stage 1 was the most affected: first-attempt success moves 76.9% → **79.3%** and final 88.3% → **90.8%** once they are removed. The raw Razorpay file deliberately keeps these rows; exclusion is an analysis-time decision.

**Voluntary vs involuntary by stage:**

| Stage | n | Voluntary | Involuntary |
| :---- | :---- | :---- | :---- |
| Trial ended (before or at first charge) | 137 | **104 (75.9%)** | 33 (24.1%) |
| Paying customer lost (after first charge) | 12 | 4 (33.3%) | **8 (66.7%)** |

**The character flips at the first successful payment.** Before it, three quarters of exits are choices. After it, two thirds are payment failures. That boundary is the single most useful thing in this analysis: pre-payment is a value problem, post-payment is a mechanics problem, and they need different owners.

### Trial to paid, and the real leak

**25.4%** (48 paid of 189 mature), flat since launch (Apr 40%, May 25.0%, Jun 23.5%, Jul 26.7%). The Jul-2 baseline of 24.3% is confirmed and has not moved.

Decomposed:

- **50.3%** of mature trials ever reach a day-7 debit attempt; the rest cancel or expire first.  
- **57.9%** of those that reach it capture.

**First-debit capture is degrading: May 73.7% → Jun 54.2% → Jul 53.8%.**

### There is no dunning retry

**47 failed recurring charges since launch. Zero were ever followed by another attempt.** Grouping by subscription and billing cycle: 111 of 113 cycles had exactly one attempt, and the two exceptions were captured-then-captured duplicates, not retries.

**One failed debit is terminal, 100% of the time.**

This contradicts live shipped copy. `gtm/lifecycle/transactional-comms-final-v3-2026-07.md` line 344 tells customers *"Fix it in one click, or we'll retry automatically"* and line 383 cites *"the billing flow's 2 retries over 48h"*. That billing flow does not exist.

### Failure modes of lost first debits

| Mode | Share | Recoverable |
| :---- | :---- | :---- |
| INSUFFICIENT\_BALANCE | 45% | Yes, pure dunning target (20 of 22 are UPI, which debits at one fixed moment) |
| **RECURRING\_TOKEN\_NOT\_CONFIRMED** | **30%** | **Yes, it is a bug** |
| Mandate inactive or cancelled | 10% | Partly |
| BANK\_DECLINED | 5% | Low |

The mandate defect has a clean signature: **all 14 `RECURRING_TOKEN_NOT_CONFIRMED` rows are UPI, and all 14 had their ₹10 authorization captured successfully 5 to 6 days earlier.** The auth succeeds, the user sees "trial started", WooCommerce creates an active subscription, and the UPI Autopay recurring token was never confirmed. We took money and granted access against a mandate that did not exist.

### Revenue

| Measure | Value |
| :---- | :---- |
| MRR (published `cleanPaying`) | 31 active, ₹54,833 gross, ₹46,469 net |
| MRR (correcting a classification-order bug) | 37 subs, ₹65,446 gross, ₹55,463 net |
| Total collected since launch | ₹111,436 gross / ₹94,437 net |
| Net LTV per converted payer | ≈ ₹2,317 (avg 1.55 renewals) |
| **LTV forgone to failed first debits** | **≈ ₹92,665** |

**The leak has cost approximately what the entire business has earned.**

The MRR figure is disputed: `tools/metorik-fetch/index.js:61` checks `manual-renewal → comped-manual` before `hasAnyPaidOrder → paying`, mislabelling Razorpay-verified payers as comped. The classification order is verifiably wrong; the resulting number has not been changed pending a ruling.

Growth is real regardless: 10 active / ₹17.7K (May 27\) → 17 / ₹30.1K (Jul 2\) → 25 / ₹44.2K (Jul 13\) → 31 / ₹54.8K (Jul 27). **\+82% in 25 days.**

### Pricing and packaging

One price, one plan, zero discounting, zero variance: all clean-paying subscriptions bill exactly ₹1,768.82 (₹1,499 \+ 18% GST). No annual self-serve, no seats, no tiers above Pro.

**The credit add-on thesis is dead.** Zero credit top-up orders since Apr 22\. `Credit Payment` has only one instrumented stage (`Buy Credits`) and no completion stage. Three of the four advertised packs have **no purchasable SKU**. And nobody approaches the allocation: of 38 Pro members exporting in 30 days, the heaviest consumed roughly 42 of 100 credits and the median 2 to 6\. `Limit Reached` fired 8 times for 3 people in 60 days, all on the AI query cap.

**There is currently no mechanism by which an existing Pro member could spend more money.**

### The unreached power users

| Weeks active in 90d | People | Pay rate |
| :---- | :---- | :---- |
| 8+ | 49 | **14.3%** |
| 6 to 7 | 52 | 11.5% |
| 4 to 5 | 181 | 6.6% |
| 2 to 3 | 1,135 | 7.0% |
| 1 | 7,771 | 1.4% |

Frequency predicts payment at 10x. But of **257 non-paying users active 4+ weeks, only 15% have ever hit a Pro lock.** The paywall and the most engaged free users rarely meet.

---

## 7\. Retention

**Current state: flat. Not decaying, not improving.**

| Registration month | Cohort | d1 to 30 return |
| :---- | :---- | :---- |
| Feb | 409 | 28.6% |
| Mar | 1,285 | 27.7% |
| Apr | 1,660 | 29.8% |
| May | 1,764 | 27.3% |
| Jun | 1,863 | 26.4% |

d8 to 30 holds at 11 to 13%, d31 to 60 at 6 to 8%. A 1.2pp drift over five months is inside noise.

**This corrects two claims in circulation.** The brief's framing of week-1 return as "moving away from target" reads a flat series as a regression. And "WAAU compounding 535 → 571 → 586" does not survive an eight-week look: WAAU has been flat in a 490 to 586 band for nine weeks, mean 545\.

**The reported metric is also mislabelled.** The Gate-1 "Week-1 return rate" of 27.6% is computed **unbounded-horizon** over a 30-to-60-day cohort. It is baseline-matched, so it is comparable to its own 28.8% baseline, but the true **week-1-bounded** figure for the same cohort is **21.7%**. Against a target read as week-1, the position is roughly 6pp worse than reported.

### Device is the single largest retention split

| Device | n | Week-1 return | d8 to 30 |
| :---- | :---- | :---- | :---- |
| Desktop | 1,177 (67.2%) | **26.5%** | 12.4% |
| **Mobile** | **571 (32.6%)** | **8.4%** | 3.2% |

It is not an entry-page-mix artifact and it is not just the onboarding gap:

| Segment | n | Week-1 return |
| :---- | :---- | :---- |
| Desktop / Company Profile entry | 726 | 24.0% |
| **Mobile / Company Profile entry** | 447 | **7.6%** |
| Desktop / onboarding completed | 827 | **33.0%** |
| **Mobile / onboarding completed** | 242 | **12.4%** |

Mobile also onboards worse (44.1% complete vs desktop 69.1%) and effectively cannot use the retention-driving feature: **42 mobile filter users versus 575 on desktop**, against mobile being a third of registrations.

### The aha moment

**Applying an advanced filter at least twice in week 1\.** Clean dose-response, and it survives every control:

| Filters in week 1 | Retention d28 to 60 |
| :---- | :---- |
| 0 | 6.0% |
| 1 | 14.5% |
| 2 to 3 | **24.6%** |
| 10+ | **37.5%** |

Controls: holding week-1 active days at exactly 1, filter users retain 11.2% vs 3.9% (2.8x). Within desktop only, 25.4% vs 7.5% (3.4x). Both controls at once, 11.7% vs 5.1%.

Current adoption is 11.5%.

### MAU composition: 85% of the growth is inflow

| As of | MAU | Inflow | Returning stock |
| :---- | :---- | :---- | :---- |
| 2026-04-28 | 3,160 | 1,613 | 1,547 |
| 2026-06-23 | 3,432 | 2,029 | 1,403 |
| **2026-07-28** | **3,619** | **2,004** | **1,615** |

**Returning stock has not grown in three months** (band 1,356 to 1,615). Of the \+459 MAU since April 28, **\+391 (85%) is inflow**, and inflow is roughly 98% of trailing-30-day registrations, i.e. every registrant is active by construction.

Frequency confirms it: **88.9% of monthly actives are active in exactly one week of the month**, at 1.38 active days per user per month. MAU is about 4x WAU because there is essentially no week-to-week overlap.

**The 3,681 marker is not borrowed from the news.google.com spike** (that produced 2 registrations in 91 days and 4 identified users in 30 days). It came from Google organic registrations rising 159 to 321 per week over three months. But it was cleared by only 20 to 80 users on the strongest registration week on record, and a reversion to June's registration average puts MAU back to roughly 3,530.

**Takeaway**: total MAU is currently an acquisition metric wearing a retention costume.

### The dormant pool

**46,057 users dormant 30+ days**, not the \~30,000 assumed. But only **\~6,257 have meaningful prior engagement** (3+ active days plus filter or search use), of whom **1,098 are warm** (dormant 30 to 180 days).

**The reactivation lane has already failed its own kill criterion.** Site-side:

| Week | Source | Visitors | Logins | Registrations |
| :---- | :---- | :---- | :---- | :---- |
| 2026-05-18 | MoEngage | 394 | **149** | 64 |
| 2026-06-15 | Customer.io | 742 | **0** | 0 |
| 2026-06-29 | Customer.io | 786 | **3** | 0 |
| 2026-07-06 | Customer.io | 60 | 2 | 0 |

Across both Customer.io sends: 1,528 visitors, **3 logins (0.2%)** against a kill threshold of 0.8%, and only 59 of 1,566 visitors had ever registered. The list was not the dormant Datalabs base. The one send that worked (MoEngage, 37.8% login rate) has not been repeated in ten weeks, and the lane has been dark since Jul 6\.

---

## 8\. Churn

> **CORRECTED 2026-07-30.** An earlier version of this document claimed "voluntary churn is zero". **That was wrong.** It was inferred from Metorik and Razorpay alone, neither of which records *why* a subscription ended: Metorik exposes only status and dates, and Razorpay's token API returns **no status field for UPI tokens**, which are 74% of failed recurring charges. A read-only WooCommerce REST key (added 2026-07-30) settled it from order and subscription notes, which log the cause explicitly.

### The corrected picture

WooCommerce logs both voluntary paths explicitly:

- `"Razorpay mandate cancelled externally by customer (via UPI app, bank, or card issuer)"` — **91 occurrences** across the cohort. This is the path that was previously invisible: a customer killing autopay in their UPI app, which reaches our data disguised as a payment failure.  
- `"Cancellation scheduled via API. Subscription stays active until [date], then will auto-expire"` — **33 occurrences.** Cancel-at-period-end, i.e. the customer clicking cancel in the UI.

### Counted at customer level, parent-order-aware

Three things had to be fixed to get this right, each of which moved the answer:

1. A subscription whose **parent order never completed** never started. It is not churn.  
2. A first-ever charge failing and a renewal failing on an established subscriber are **different events with different fixes**.  
3. **Customers who abandoned checkout and retried successfully were being counted twice** — once as an abandonment, once as a real subscription. The unit of analysis must be the customer.

**346 subscription records resolve to 270 distinct customers.** 50 customers hold more than one subscription. **38 customers abandoned checkout and later hold a real subscription, 11 of whom went on to pay.** So 57 abandon records belong to people who did convert and are not losses at all.

| Population | Customers | Voluntary | Involuntary |
| :---- | :---- | :---- | :---- |
| Became a paying customer | **48** | — | — |
| Currently live (in trial or active) | 29 | — | — |
| **B. Started a real trial, then ended it** | **135** | **102 (75.6%)** | 33 (24.4%) |
| **C. Paying customers lost** | **12** | 4 (33.3%) | **8 (66.7%)** |
| **A. Never started** (abandon only) | **58** | — | Not churn |

Trial-to-paid at customer level: **48 of 183 \= 26.2%** (excluding the 29 still live), consistent with the 25.4% subscription-level figure.

### Payment failure is a first-charge phenomenon, not a renewal one

Decomposing all 47 failed recurring charges by whether the subscription had *ever* succeeded before:

| Failure type | Attempts | Subscriptions |
| :---- | :---- | :---- |
| **First-ever charge** (the day-7 trial-to-paid conversion) | **40** | 40 |
| **True renewal** (after ≥1 successful charge) | **7** | 7 |

**57 subscriptions have ever taken a successful recurring charge; only 7 of them later failed one.** Once a customer successfully pays once, payment keeps working roughly 88% of the time.

This is the sharpest finding in the payment analysis and it redirects the fix: **the breakage is concentrated at the very first conversion charge**, which is exactly where `RECURRING_TOKEN_NOT_CONFIRMED` sits. The absence of any dunning retry therefore matters most at first charge, not at renewal.

**The two stages have opposite characters:**

- **Trial conversion is a value problem.** Three quarters of people who end a real trial *choose* to, by cancelling or revoking the mandate. Only 34 of 138 were stopped by a payment failure.  
- **Renewal is a mechanics problem.** Two thirds of established payers who churn are lost to a failed or never-attempted charge.

**Sequence matters within each stage.** Counting any voluntary signal anywhere in a subscription's history gives 7 of 12 at renewal stage; classifying on the *first* decisive event gives 4 of 11\. The difference is subscriptions where a payment failed first and the customer cancelled afterwards, which is an involuntary churn with a voluntary epilogue. **First-cause is the honest basis and is what the table uses.**

The four voluntary renewal-stage cases: 556845 and 561306 revoked the mandate externally; 558323 and 560002 cancelled at period end.

> **Correction history for this section** (three passes, each prompted by a challenge to the previous one):  
> 

> 1. Originally claimed **"voluntary churn is zero"** — inferred from Metorik and Razorpay, neither of which records *why* a subscription ended. Wrong.  
> 2. Corrected to 224 of 300 (74.7%) voluntary at "trial stage" — but that **pooled 127 never-started subscriptions** into the churn population.  
> 3. Corrected again to customer level with **first-charge and renewal failures separated** and **abandon-then-converted customers deduped**. The table above is that version.

>   
> The voluntary percentages proved robust across passes 2 and 3 (75.4% → 75.6%; 63.6% → 66.7%), but the abandon population fell from 127 records to **58 customers** once duplicates were removed.

### What this does and does not change

- **Still true**: at the **renewal** stage involuntary churn is the majority (64%), the recurring debit captures only \~61%, and **there is still no retry** (47 failed cycles, 0 retries ever). The payment-leak fixes remain correct and cheap.  
- **No longer true**: "every paying subscriber we lost, we lost to a payment failure." And critically, the payment fixes address population **C, which is only 11 subscriptions**. The far larger population **B (138 real trials) is 75% voluntary** — a value and activation problem, not a billing one. The August plan should not expect the payment work alone to move trial-to-paid conversion much.

### Measurement gap: revocations are detected late, and nothing acts on them

The Razorpay webhook **is active**, and our integration **does** handle mandate *confirmation*: `"Razorpay mandate confirmed via webhook. Token: … Method: upi"`. Cancellation is not on that path.

Revocations surface instead through a polling reconciliation job:

| Note | Count |
| :---- | :---- |
| `[Reconciliation] Razorpay token status: paused. Monitoring.` | **263** |
| `Razorpay mandate cancelled externally by customer (via UPI app, bank, or card issuer)` | 91 |
| `[Reconciliation] Mandate cancelled at Razorpay. Token cleared.` | 3 |

None of the 91 revocation notes carries a webhook marker, and **in 0 of 91 cases did we record the revocation before the next charge failed**.

Two distinct problems, and the second is the worse one:

1. **Detection is late** — polling rather than the `token.cancelled` push.  
2. **Detection triggers nothing.** 263 paused tokens were spotted and the note literally reads *"Monitoring"*. No email, no in-app prompt, no reactivation attempt.

**73 subscriptions are currently revoked with no failed charge yet** — a live, addressable list that nobody is acting on. See August plan item A5.

### Why the earlier reading failed

`pending-cancel`, the WooCommerce status a customer-initiated cancel normally produces, is **0** across all 378 launch-cohort subscriptions. That was read as evidence of no voluntary cancellation. It is not: this store's cancel flow writes a note and schedules expiry rather than parking the subscription in `pending-cancel`, so the absence of that status means nothing here. **A negative inferred from an absent record, in a system never confirmed to write that record, is not evidence.**

### Order notes were essential

**93 `customer cancelled` notes sit on parent orders and 17 on renewal orders, with no counterpart on the subscription record.** Reading subscription notes alone would have missed 110 voluntary cancellations. Any future churn analysis must read all three sources.

### The silent-death mechanism (unchanged)

First recurring charge succeeds → `requires_manual_renewal` flips true and `next_payment_date` goes null → the subscription expires with no debit attempted. The uniform 53-to-54-day cancellation timing is now explained by a confirmed policy note: `"Auto-cancelled: subscription on-hold for 15 days (grace period: 15 days)"`, i.e. 7-day trial \+ \~30-day cycle \+ 15-day grace.

### The silent-death mechanism

First recurring charge succeeds → `requires_manual_renewal` flips true and `next_payment_date` goes null → the subscription expires one cycle later with **no debit ever attempted**. This holds for all 27 `real-trial-expired` subscriptions and all 5 expired payers, a 100% correlation. **Nine live subscriptions currently carry a broken mandate** (roughly ₹15,919/mo gross at risk), and 5 of the 25 current trials already have a detached mandate and will never be charged.

### Survival

| Milestone | Rate | n |
| :---- | :---- | :---- |
| Month 2 | **52.2%** | 12/23 |
| Month 3 | **23.1%** | 3/13 |

This supersedes the 38.5% month-2 figure in circulation, which was a local trough on 2026-07-02 (the series ran 63% → 42% → 38.5% → 47% → 50% → 52%). **The leak has moved from month 2 to month 3\.**

**All 12 post-launch churned payers churned after exactly one paid renewal.** Not one died at month 3 or later. Cohort sizes are small (n \< 20 throughout); report with sizes attached.

At the trial stage, **60 real trials (₹106,129/mo of MRR) were lost to payment mechanics** (37 with a failed recurring debit, 23 with no attempt at all) against 81 genuine voluntary trial cancels.

---

## 9\. Measurement health

The audit found that a majority of the funnel's headline numbers were wrong. Fixed items are live in `tools/weekly-brief/`.

### Fixed

| Defect | Was | Actually |
| :---- | :---- | :---- |
| Registration/activation attribution read person properties on `Registered` (fires before the profile is written) | Direct 98.1% | **Direct 10.3%, Organic 67.2%** |
| `onboardingByState` read `properties['state']`, a non-existent key | 100% completion | **87.1%** |
| `activationsBySource`: lifecycle-timing mismatch, missing 5+ threshold, double counting | Organic 271 activated vs 6 registered \= **4,516%** | reconciles exactly with the headline (371) |
| Pro Payment counted all checkout stages, and events not people | 162 payers, 30% conversion | **34 payers, 6.3%** |
| Indexing gate read UNKNOWN for four weeks while telemetry sat on disk | UNKNOWN | **PASS, tier1 98.7%** |
| Listicle alarms fired on headline WoW ignoring 8 to 10% universe churn | −26.6% "collapse" | **−10.5% like-for-like** |
| GSC click alarms fired without cross-checking GA4 | "check GSC for a broader issue" | query-demand contraction, not a ranking event |
| Registrations counted events not people | 540 | **524** |
| "Week-1 return rate" computed unbounded-horizon | 27.6% | true week-1 \= **21.7%** |

### Still open

| Defect | Consequence |
| :---- | :---- |
| **`Register Lock Interaction`**: `onLoad` and `Long Lock` dead since **2026-05-18** (a triple-fire bug May 15 to 17, then a fix that killed the impression event) | **No paywall-impression denominator.** Lock-to-register conversion and any freewall A/B readout are uncomputable. Broken 10 weeks unnoticed. Clicks did not fall; they grew 181% |
| **June identification break**: identified share of returners fell 66.5% → 51.2% simultaneously across all sources while `Login` counts held | **Gate-1 MAU is defined on `$is_identified`**, so the gate may be measured on a moving instrument. ±100 to 150 on reported MAU. One hour of frontend time settles SDK-config vs session-persistence |
| `metorik-fetch/index.js:61` classification order | Disputed MRR (31 vs 37 subs) |
| `Credit Payment` has no completion stage | Credit purchase success structurally unmeasurable |
| `Alert Interaction` semantics unknown (fires \~once per person, `Alert Status: false`, empty content on page load) | Probably a state readout, not an action. Its 3.31x "lift" is likely a proxy for having completed onboarding |
| No `Onboarding Step 1` event | 87.1% completion is an upper bound |
| `Trial Type` label reads `"7 days_without CC_50 credits"` | Factually wrong (trials do take a payment method and create a mandate) and actively misleading |
| `search_users` includes 26% guests | The 800 target measures a different population than intended |
| UserGuiding product tour stopped **2026-04-25** (766 users/month at 96% completion, then 1, 1, 0\) | A live product surface has been off for three months. Week-1 return stepped 23.8% → 21.3% in the same window (correlational only) |
| Freewall experiment `datalabs-freewall-lock` | 2.11% vs 2.09% registration across \~50k per arm. No effect, and its correct denominator is the event that broke on May 18 |

---

## 10\. What the analysis concludes

1. **The bottom of the funnel is broken by mechanics *and* by demand, with mechanics the larger share among payers.** Two thirds of paying churn (8 of 12\) is involuntary: the recurring debit captures only \~61% and there is no retry at all. But one third leaves deliberately, and at trial stage **75% of churn is a customer decision**. Fix the payment plumbing first because it is cheap and purely engineering, but do not read the trial funnel's losses as purely mechanical.  
     
2. **Acquisition is healthier than believed and measurable after all.** Organic is 67% of registrations, not 1%. AI converts best per session. The largest single volume opportunity is generic company pages, which are 52% of sessions at a third the conversion of gated pages on the same entity.  
     
3. **Retention is flat, and MAU growth is a treadmill.** Returning stock has not moved in three months; 85% of MAU growth is inflow and 89% of monthly actives show up in exactly one week. Gate targets set on total MAU measure acquisition.  
     
4. **The product has a discovery problem, not a capability problem.** Its most retentive tools (saved search, custom columns, advanced filters) sit at 2 to 15% adoption, while the widely-reached surface (reports, 18.6%) barely lifts retention at all.  
     
5. **Mobile is a third of registrations and is failing at every step**: onboarding completion 44% vs 69%, week-1 return 8.4% vs 26.5%, lock-to-trial 5.0% vs 15.4%, and 42 filter users against 575 on desktop.  
     
6. **Several of the metrics used to steer were wrong.** Attribution by 10x, onboarding completion by 13pp, activation-by-source by 45x, Pro payers by 5x. Any target set before this audit was set on a distorted picture.

---

## Confidence

**Confirmed against primary data**: all payment figures (Razorpay row-level, independently re-verified), the attribution correction (three concordant methods), the onboarding funnel, the zero-retry finding, the three charged-and-lost-access customers, the UserGuiding stop date, the Register Lock collapse, MAU composition, cohort retention curves.

**Correlational, treat as a ranking rather than effect sizes**: all feature-to-retention lifts. The one case where engagement level was controlled (activated-and-filtered 51.5% vs activated-not-filtered 19.7%) the effect survived, which supports but does not prove causality.

**Explicitly uncertain**: the UserGuiding-to-retention causal link (single correlation, no control); `Alert Interaction` semantics; the cause of the June identification break; the reactivation lane's send-side metrics (site-side visibility only); free-power-user monetisation sizing (selection-biased upper bound); `Device Type` is unresolved for 85% of records, so the mobile figure is clean but its comparator is a mixed bucket.

---

*Audits run 2026-07-29 to 30\. PostHog direct API only, never MCP. Money from Razorpay and Metorik only, never PostHog.*  
