# Inc42 Audience Model — QIA, Activation, Identity

**Status:** Locked operating model for discussion and implementation  
**Date:** 8 Sep 2026  
**Owner:** Ranjith (Product) · QIA chair: Utkarsh  
**Rule:** One document. Do not spawn parallel briefs.

---

## 0. Executive lock

| Item | Lock |
|---|---|
| **Company chase** | **QIA count** (rolling **15-day** stock of distinct people) |
| **Product chase** | **Activation ≤7 days from identify**, per platform |
| **QIA (one line)** | Identified + Qualified (ICP) + ≥1 of Utkarsh’s **10** qualifying actions |
| **Activation (one line)** | Platform first aha after identify (App = Brief completion; Media = 3 article reads; DataLabs = DL aha) |
| **Never say** | “Chase QIA within 7 days” (collapses two metrics) |
| **Warehouse cousin** | **QIA-30** stays labeled separately; never mix with QIA-15 on one chart |

**This doc decides:** definitions, windows, grid labels, what we collect, who chases what.  
**Open:** exact persona table copy, exact DL activation event list, Core QIA weekly or not, scroll→PostHog join date, single dashboard owner.

---

## 1. Problem statement

Inc42 has one person across Media, DataLabs, and App, but metrics were argued as if they were the same number:

- Activation (onboarding aha) and QIA (qualified + active stock) both “felt like 7 days” because ~70% of qualifying actions happen early.
- “QIA within 7 days” made Marketing and Product fight over one number.
- Counting 3 article reads as **App** activation would dilute Brief (App’s unique aha). Ignoring in-App reads would under-credit **Media**.
- Without a shared ladder and grid, teams redefine QIA in every meeting.

**Cost of getting it wrong:** hollow signup lists sold as QIA; or over-gating so sellable people never enter the number; App Brief under-funded; payable leading indicators unclear.

**Success:** one scoreboard. Same labels in Product, Marketing, Lifecycle, and warehouse.

---

## 2. Industry practice → Inc42 implication

| Industry practice | Inc42 implication |
|---|---|
| AARRR: Activation ≠ Retention ≠ Revenue | Keep Actv and QIA as different layers |
| Multi-product suites use **product-specific** first-aha until identity+workspace unify | App / Media / DL each have their own ≤7d Actv |
| B2B “qualified” = ICP/persona, not title seniority alone | Qualified = persona fit for any Inc42 product |
| North star + input metrics | Company steers **QIA stock**; products steer **Actv% among new IDs** |
| Don’t mix cohort and stock windows | Actv = cohort from identify; QIA = rolling stock |

**Payability:** QIA (with the 10) is closer to sellable/nurturable than Identified alone. Platform Actv predicts early habit (Brief, depth, DL aha) which feeds retention and cross-sell. Neither alone is revenue; both are leading indicators.

**Devil’s advocate (industry would push back):** cheap actions in the 10 (e.g. thin session, newsletter click) can inflate QIA vs payable; 15d vs sales-cycle 30d; App Brief not required for QIA may under-invest Brief. Addressed in §11.

---

## 3. Definitions ladder

| Step | Name | Definition | Window | Denominator / type | Owner | Never counts |
|---|---|---|---|---|---|---|
| 0 | **Reach** | Seen / visited (often anonymous) | Period | Traffic | Growth / analytics | — |
| 1 | **Identified** | Email + job title + company (App may be role-only until company field exists) | Snapshot | People | Product / onboarding | Incomplete profiles as “identified” |
| 2 | **Qualified** | Passes ICP / persona for **any** Inc42 product | Snapshot | Identified | Strategy (Utkarsh) | Students/juniors as QIA if out of ICP |
| 3a | **Active (the 10)** | ≥1 of Utkarsh’s 10 qualifying actions | Rolling **15d** (stock) | People | Warehouse (Prapti) | Opens, bare login, screen-arrivals, bots |
| 3b | **Activated** | Platform **first aha** after identify | **≤7d from identify** (cohort) | New IDs that period | Each product team | Using another platform’s aha as this platform’s Actv |
| 4 | **QIA** | Identified + Qualified + ≥1 of the 10 | Rolling **15d** stock | Distinct people | **Company** | ID+ICP with zero of the 10 |
| 5 | **Engage / Repeat** | Returns / stays active among QIA | 15d (don’t mix with 7) | QIA | Lifecycle | Mixing 7/15/30 on one chart |

---

## 4. ICP / who is qualified

**Qualified** = persona / ICP fit for Media, DataLabs, App, or IP (table maintained in One Inc42 / strategy docs). Not “VP+ only.” Seniority alone cannot route Sales & Marketing → DataLabs.

**Core QIA** (optional report slice, not a second north star): QIA in proven-buyer segments (e.g. Media Founder/CXO/Senior; DataLabs Investor / Sales & Marketing).

**Out of QIA, still Identified:** audience that fails ICP (e.g. students/juniors) — serve content; do not sell as QIA.

*Open: paste the locked persona table from the One Inc42 definition doc into this section when Utkarsh confirms.*

---

## 5. Utkarsh’s 10 qualifying actions (Active bar inside QIA)

Revised 26 Aug. These are the **Active** bar for QIA, not the Activation definition.

| # | Action | Reachable today (approx.) |
|---|---|---|
| 1 | Article read — opened **and** read to depth | App yes; web scroll often GA4-only (join gap) |
| 2 | Profile / database record view | Media / DataLabs / App |
| 3 | Search completed (query submitted; “Search Active” does not count) | All three |
| 4 | Advanced or filtered search | DataLabs |
| 5 | Watchlist / saved search / alert | All three |
| 6 | Ask / AI query | DataLabs (App Ask telemetry gap) |
| 7 | App session with ≥1 content action | App |
| 8 | Newsletter **click** (never open) | Customer.io (often invisible to PostHog) |
| 9 | Event application / registration | Event projects |
| 10 | Payment or renewal | All |

**Never counted:** email opens, push receipts, bare login, screen-arrival events (`brief_page_opened`, `explore_viewed`, `card_viewed`), staff, bots.

**Map without redefining QIA:**

| Product aha | Maps onto the 10? | Is it Activation? |
|---|---|---|
| Brief completion | Often via #7 (content action) | **Yes — App Actv only** |
| 3 article reads | Via #1 if depth | **Yes — Media Actv only** |
| DL search / profile / Ask / pay | #3/#4/#2/#6/#10 | **Yes — DL Actv** when used as DL aha |

---

## 6. Platform activation (≤7 days from identify)

| Platform | Activation | Does not count as this platform’s Actv |
|---|---|---|
| **App** | **Brief completion** | 3 article reads |
| **Media** | **3 article reads** (web **or** in-App) | Brief completion alone |
| **DataLabs** | DL aha = instrumented DL subset of the 10 (search completed, advanced search, profile view, watchlist, Ask, pay — finalize list) | Media/App-only actions |

### Edge examples

| Case | App Actv | Media Actv | QIA? |
|---|---|---|---|
| ID+ICP, Brief complete day 2 | Yes | No | Yes if maps to a 10 (usually #7) |
| ID+ICP, 3 articles in App, no Brief | No | Yes | Yes if #1 depth |
| ID+ICP, newsletter click only | No | No | Yes if #8 visible + ICP |
| ID+ICP, none of the 10 | — | — | **No** |

---

## 7. The grid — what we call the user

| Identified | Qualified | ≥1 of 10 (15d) | Platform Actv ≤7d | **Label** | **Ops move** |
|---|---|---|---|---|---|
| No | — | — | — | Reach | Identify carefully; publish reach |
| Yes | No | No | — | Identified dormant / out-of-market | Enrich; don’t sell as QIA |
| Yes | No | Yes | — | Active audience, not QIA | Serve; no QIA campaigns |
| Yes | Yes | No | — | Qualified but not Active | Push into a real 10-action |
| Yes | Yes | Yes | No | **QIA** (not yet platform-activated) | Count QIA; product Actv nudge by ICP surface |
| Yes | Yes | Yes | Yes | **QIA + Activated** | Full path; cross-promo; continue not cold onboarding |
| Yes | Yes | Yes | Other surface only | **QIA**; local Actv gap | Soft tour on new surface; don’t strip QIA |
| Yes | Yes | Unknown legacy | — | Split forward vs legacy | Forward QIA = goal truth |

---

## 8. What information we collect

Inspired by One Inc42 / Nityam onboarding direction.

| Field | Must ask / enrich | Why |
|---|---|---|
| Email | Must (identify) | Identity spine |
| Job title | Must ask | Qualification + routing |
| Company name | Must ask (App gap today: often missing) | Qualification + enrichment |
| **Interest / sector** | Must ask (cannot fully enrich) | Seeds News + Companies; ICP assist |
| Topic interests | Optional / later | Personalisation |
| Other firmographics | Enrich from title + company | Don’t bloat onboarding |

**Onboarding rule:** collect only title, company, interest/sector; enrich the rest.  
**Identified bar:** email + title + company (document App exception until company field ships).

---

## 9. How we measure

### Default board number
**QIA count** = distinct people with Identified + Qualified + ≥1 of 10 in rolling **15 days**.

Supporting rates (not the north star): QIA / Identified; new QIAs in period.

### In a month

| Report | How |
|---|---|
| Month-end QIA stock | QIA definition on last day of month (15d lookback) |
| New QIAs in month | First time entering QIA that month |
| Activation that month | Of people who **identified in that month**, % with platform aha within **≤7d of identify** (App / Media / DL separately) |

### Marketing vs Product scorecards

| Team | Primary | Secondary |
|---|---|---|
| Company / Utkarsh | QIA 15d count | New QIAs |
| Marketing | Identified + Qualified volume; channel → QIA; #8/#9 where owned | — |
| App Product | % new IDs Brief ≤7d; Brief completions | — |
| Media Product | % new IDs 3 articles ≤7d | Depth |
| DataLabs Product | % new IDs DL aha ≤7d | — |
| Lifecycle | Repeat among QIA; win-back drop-offs | — |

---

## 10. How we chase

1. **Company scoreboard:** QIA 15d.  
2. **Product scoreboards:** platform Actv ≤7d among new IDs.  
3. **Leaks to close:** Identified without ICP · ICP without a 10 · new ID without Actv ≤7d · QIA leaving the 15d window.  
4. **CIO:** journeys by leak; already-QIA users get **continue / welcome back**, not cold onboarding.  
5. **Instrumentation:** close #8 CIO join and #1 web scroll→identity before trusting Media QIA fully.

---

## 11. Risks to payability (devil’s advocate)

| Challenge | Our answer |
|---|---|
| Cheap 10s (#7 thin session, #8 NL click) inflate QIA | Keep them in Utkarsh’s 10 for continuity; report **Core QIA** / exclude-cheap sensitivity; tighten events over time |
| 15d overstates vs sales 30d | Publish QIA-15 as product OS; QIA-30 labeled for warehouse/finance narrative |
| Brief not required for QIA under-funds App | App team KPI is Brief Actv ≤7d; company KPI stays QIA |
| In-App 3 articles as Media Actv double-counts | Correct: Media aha can happen in App shell; App Actv remains Brief-only |
| Missing CIO/GA4 → floor not truth | Call Media QIA understated until joins exist; don’t pretend completeness |
| Does this move payable? | Leading: QIA stock, Actv among new IDs, Repeat among QIA → trial/Plus/DL pay/events. Revenue stays separate.

---

## 12. Open decisions

1. Lock persona / ICP table text from One Inc42 doc with Utkarsh.  
2. Finalize DataLabs activation event list (subset of the 10).  
3. Report Core QIA weekly? Y/N.  
4. Date for web scroll depth join to identity (action #1).  
5. Single dashboard owner (Prapti + Ranjith?).  
6. App company-name field ship date (Identified parity).

---

## Appendix — sources (links only)

- Product & Data / One Inc42 / redesign Wispr notes (7 Sep)  
- One Inc42 definition doc: https://docs.google.com/document/d/1iwXO6icFGvPCUIi7N4WBRMev63yyLZAFBYNQ_W0z-1U/edit  
- Ten qualifying actions (strategy / unification notes, revised 26 Aug)  
- Chat locks 7–8 Sep 2026 (windows, App vs Media Actv, chase rules)

**Supersedes** earlier parallel QIA/IA draft briefs. Use this document only.
