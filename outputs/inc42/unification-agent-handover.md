# Unification Agent — Handover Pack

**Prepared 2 September 2026 · for a new agent joining the One Inc42 unification work**

Four parts: the prompt to give the agent, the context it needs, where the knowledge lives, and the meeting record. Part 5 is the list of traps — read it before doing any analysis.

---

# PART 1 — THE PROMPT

Copy everything between the lines into the agent's system prompt or first message.

---

You are the product-data agent for **One Inc42 unification** at Inc42, an Indian startup-media company. You work for Ranjith (Product & AI). Utkarsh is the chair of the unification track and owns the north-star metric.

## What Inc42 is

Three products that do not know each other:

| Product | What it is | Scale |
|---|---|---|
| **Media** — inc42.com | Startup journalism | ~495,000 visitors/month |
| **DataLabs** — datalabs.inc42.com | Company/funding database, freemium | ~115,000 visitors/month |
| **App** — Inc42 (Android + iOS) | Daily Brief + Explore + Watchlist | ~900 installs, launched 12 Aug 2026 |

Plus IPs/events (D2C Summit, CTO Summit, D2CX) which sell tickets and are the primary revenue line.

## The problem you are solving

Separate logins, separate identities, no shared context. A reader who follows a company on the website starts from zero in the app and again in DataLabs. Cross-surface usage is **1.6–3.4%**.

**Unification is not a design-consistency project.** Utkarsh's own definition (31 Aug): *"from a user experience, how is it consistent across all surfaces… frictionless login and onboarding."* The operational version: **one person, recognisable on any surface.**

## The north star

**QIA-30 — Qualified Identified Actives, 30 days.** A person we can name, who clears a seniority bar, who took at least one of ten qualifying actions in a rolling 30-day window.

```
QIA = arrivals × identified × qualified × active-in-window
```

Every plan row must name which multiplier it moves, or it does not belong.

Official figure: **QIA-30 = 5,470 of IA-30 = 17,464** (warehouse, re-run 26 Aug). Target 15,000 by FY28-end.

## How you must work

1. **Query live data. Never quote a number you have not verified this session.** PostHog SQL is available and current to ~4 minutes.
2. **Label every figure as measured or assumed.** Conversion rates you did not observe are assumptions — say so in the same sentence.
3. **Never compare a number across method versions.** The QIA definition has changed three times in three weeks. Each change moved the number without anyone behaving differently. Log every definitional change explicitly.
4. **Experiments over builds.** Utkarsh aligned on an experiment-led approach on 10 Aug — prove impact, do not big-bang. Every proposal needs a pre-registered kill criterion.
5. **Deliver one document, not fragments.** Ranjith works from a single consolidated artifact he can debate against. Drip-feeding tables is explicitly unwanted.
6. **Tables over prose. No paragraphs where a table works.** Crisp, PM lens, always include source links.
7. **State decisions directly. Never invent content.** If you cannot verify it, say so and mark the gap.

## What is locked — do not reopen

- Three buckets: **unified experience / App / DataLabs** (31 Aug)
- **Backtrack from QIA**, not bucket by bucket
- DataLabs scope = **free-user retention + one-time fixes only.** No new scope. No B2B pivot
- App priority: **activation first, D7 retention second**
- Web capped at **5–10% of bandwidth**
- **Third-party enrichment is now open** for evaluation (31 Aug) — previously internal-data only
- Qualification bar differs by platform: **DataLabs role+company; media and app role only** (1 Sept, Ranjith)
- Workspaces stay separate per platform; historical cross-surface stitching is impossible — accept it

## What is open — do not assume

| # | Question | Owner |
|---|---|---|
| U1 | QIA window: 7, 15 or 30 days. Changes the baseline ~4× | Utkarsh |
| U2 | Should the working metric be QIA or plain identified-audience count | Utkarsh |
| U3 | Solve personalisation once across app + DataLabs, not per surface | — |
| U4 | Bucket 1's real name (the recording garbled it) | Utkarsh |
| — | Does a trial start count as a payment? 109/month at stake | Utkarsh |
| — | Do `operator` and `bd` clear the app's seniority bar? 204 vs 275 | Ranjith |
| — | Is third-party enrichment permissible under DPDP? | Legal |
| — | Which of the 10 qualifying actions actually reach the QIA computation? | Prapti |

## Your first task

Read `~/inc42-context/MASTER.md`, then `surfaces/unification/DECISIONS.md` and `OPEN.md`, then the 31 Aug meeting note. Then verify the current QIA baseline yourself before using any number in this pack.

---

# PART 2 — CONTEXT

## The finding that anchors everything

Inc42.com already hosts **75,000+ free `/company/` profile pages — and they are DataLabs data, surfaced unbranded.**

In the last 30 days they drew **889 views from 780 people: 0.13% of site pageviews**, against 426,183 people reading articles on the same domain. No Follow button. No link from an article about a company to the page about that company.

**The bridge between the worst-identifying surface and the best-identifying surface already exists, is fully built, and is invisible.**

## Current state, August 2026

| | Media | DataLabs | App |
|---|---|---|---|
| Visitors / installs | 495,041 | 114,849 | 915 |
| Engaged | 86,334 | 77,863 | 505 |
| Sign-ups | 1,515 | 2,417 | 287 |
| IA-30 | 250 | 3,672 | 418 |
| **QIA-30** | **55** | **985** | **241** |
| **Visitors per 1 QIA** | **9,001** | **117** | **3.8** |

Media supplies 81% of the people and 4% of the north star. The app supplies 0.1% of the people and 19%.

**Media's loss is entirely at engaged → identified (0.29%).** Once it identifies someone it qualifies them at 22%, close to DataLabs' 27%. The constraint is one step.

## Six-month trend

| Month | Combined visitors | Sign-ups | IA-30 | QIA-30 |
|---|---|---|---|---|
| Mar | 647,514 | 1,622 | 2,446 | 739 |
| Apr | 558,499 | 2,055 | 2,761 | 880 |
| May | 649,340 | 1,832 | 2,905 | 852 |
| Jun | 481,604 | 2,009 | 3,182 | 809 |
| Jul | 609,716 | 3,703 | 3,865 | 1,115 |
| Aug | 610,805 | 4,219 | 4,340 | 1,281 |

DataLabs went 1,056 → 985 and media 48 → 55. **The entire August step-up is the app arriving.**

## The three reactivation cohorts

| Cohort | Media | DataLabs | App | Total |
|---|---|---|---|---|
| A — signed up, no onboarding | 2,387 | 1,094 | 5 | 3,486 |
| B — qualifying action, no sign-up | 83,085 | 65,901 | 83 | ~149,000 |
| C — qualified + signed up, no onboarding | 137 | 980 | 0 | 1,117 |

**67% of media's registered users have no profile.** But media has only 250 identified actives a month, so most of cohort A is dormant — a win-back problem, not a profile-completion problem.

## Experiments, ranked by QIA gained

| # | Experiment | QIA gain | Cost | Evidence |
|---|---|---|---|---|
| 1 | **Third-party enrichment (Apollo)** — 3,059 identified actives lack role/company, 27% match | **+826** | **~₹6,000** | rate from 31 Aug call |
| 2 | Hit the 5,000 install target | +460 to +1,140 | ₹5–7.5L | measured on 870 installs |
| 3 | Gate exposure on media, role captured *in* the gate | +250 to +310 | medium build | **observed 3.55%** |
| 4 | DataLabs gate on record views | +175 | build + holdout | assumption |
| 5 | Cohort C profile completion | +75 | email only | observed 26% |
| 6 | App — convert the 322 who never authenticate | +56 | small build | assumption |
| 7 | Login-modal variants by user type/moment | +50 to +100 | low | assumption |
| 8 | Landing page redesign | +40 to +80 | design + build | assumption |
| 9 | Drive engagement (17.4% → 20%) | +30 to +50 | high | assumption |

**Enrichment is the outlier.** It converts already-identified, already-active people into qualified ones with no product change, no new traffic and no user action. Worth more than every product experiment combined, for about ₹6,000. **Blocked on DPDP review.**

**Experiment 9 ranks last and this is counterintuitive** — media's economics defeat volume interventions.

## Install sensitivity

| Installs | 27.7% (holds) | 14% (halves) | 7% (quarters) |
|---|---|---|---|
| 1,000 (current pace) | 277 | 140 | 70 |
| 3,000 | 831 | 420 | 210 |
| 4,000 | 1,108 | 560 | 280 |
| 5,000 (target) | 1,385 | 700 | 350 |

Test 500 paid installs (~₹60K) before committing ₹6L. The 27.7% is measured on self-selecting early adopters and will degrade.

## September scenarios

| Scenario | QIA-30 | vs today |
|---|---|---|
| Do nothing | ~1,281 | — |
| Enrichment only | ~2,107 | +64% |
| + cheap wins | ~2,290 | +79% |
| + installs at 14% | ~2,750 | +115% |
| Everything, mid-case | ~3,120 | +144% |

---

# PART 3 — KNOWLEDGE BASE

## Repository — the system of record

`~/inc42-context/` (GitHub `ranjith-unofficial/inc42-context`). **Always `git pull` first.**

| Path | What it holds |
|---|---|
| `MASTER.md` | Company overview, people, standing cautions |
| `surfaces/unification/DECISIONS.md` | Append-only decision log with transcript quotes |
| `surfaces/unification/OPEN.md` | Unresolved questions, re-surfaced after 7 days |
| `surfaces/unification/SPEC.md` | Current-state spec — **still a stub, needs writing** |
| `surfaces/unification/unification-sheet-prompt.md` | Prior roadmap-sheet prompt (15KB) |
| `meetings/YYYY/MM/` | Meeting notes with full transcripts |
| `ledger/open-ledger.csv` | Cross-surface open items |
| `ROUTING.yaml` | Which surface owns which keyword |

Other surfaces: `analytics`, `app-v2`, `askinc42`, `datalabs`, `dunning`, `legal`, `website`, `agent-platform`, `hiring`.

## Source documents

| Document | Where | Note |
|---|---|---|
| **One Inc42 Strategy** | Google Doc `1ta74MohxdbPD7sZmdI2A8wYACnXhCvCIYZwbcdJEaYo` | §5 has the QIA definition, revised 26 Aug. **Authoritative.** Read via `/mobilebasic` — the normal view is canvas and will not extract |
| Product Vision, Unified Product Tiers, Vision | `~/Downloads/*.md` | Downloaded 13 Aug — **stale**, verify against the live doc |
| **FY27 Plan + MOP** | `~/Downloads/PMTD MOP 2026 (1).xlsx` and Google Sheet `1qOpoELKowiYHFdOPyMEhQsnkYgqRftVJyi6YU_OjcUE` | Tabs: FY27 Plan — Engines × Tracks, Sept MOP, Aug MOP |
| Working MOP tab | "Test" sheet `1NCpTEzgEEtds0uCfqPNSS6aeFhOpKbgkL_F-cgtVPxg`, tab **Sheet15** | Ranjith's live working copy |
| Analytics master sheet | Google Sheet `1n6r5QXe-9Pq1uAWMKRe7zSgLHSejASzAq-BAqeI3L6Y` | 6 tabs. **6 known gaps as of 27 Aug, unfixed** |
| **This analysis** | https://claude.ai/code/artifact/c55a1a0a-b883-49c5-bd76-8544e8ed80dd | Complete baseline + September plan |
| App PRD | Google Doc `1RJtcNEeOjHiQK6tDxm87MZ2a4uyq0ztFqPUaSYNmyxQ` | 45 tabs, mid-rebuild and partially broken |

## Data access

| Source | ID | Status |
|---|---|---|
| PostHog — Inc42 Live (media) | 53557 | ✅ read |
| PostHog — DataLabs Live | 66351 | ✅ read |
| PostHog — Inc42 App | 146258 | ✅ read |
| PostHog — Inc42 Events | 128843 | ✅ read — holds `Application Completed` |
| PostHog — D2C Retail Summit | 177210 | ✅ read — holds ticket `Purchase` |
| GA4 — "Inc42 v4" | `a32578434p255844088` | ✅ read |
| **Customer.io** | — | ❌ **no access. Critical gap** |
| **BigQuery warehouse** | — | ❌ no access |
| PostHog write | — | ❌ `dashboard:write` / `insight:write` not granted |

**The Customer.io gap is the single biggest limitation.** Media's real identification channel is email, not login. Newsletter clicks are qualifying action #8 and are entirely invisible. Every media figure understates it.

## The ten qualifying actions (revised 26 Aug)

| # | Action | Reachable? |
|---|---|---|
| 1 | Article read — opened **and** read to depth | 🟡 app only; web scroll is in GA4, unjoinable |
| 2 | Profile / database record view | ✅ all three |
| 3 | Search completed (query submitted; `Search Active` does not count) | ✅ all three |
| 4 | **Advanced or filtered search** — the genuinely new one | ✅ DataLabs |
| 5 | Watchlist / saved search / alert | ✅ all three |
| 6 | Ask / AI query | ✅ DataLabs only — app has zero Ask telemetry |
| 7 | App session with ≥1 content action | ✅ app |
| 8 | **Newsletter click**, never an open | ❌ **Customer.io** |
| 9 | Event application / registration | ✅ two event projects |
| 10 | Payment or renewal | ✅ all |

**Never counted:** email opens, push receipts, bare login, screen-arrival events (`brief_page_opened`, `explore_viewed`, `card_viewed`), staff accounts, bots.

**"9 → 10" is not an addition.** One was split (profile/search became two), one added (#4), one deleted (community contribution).

## People

| Name | Owns |
|---|---|
| Utkarsh | Chair of unification, owns QIA, CEO-level |
| Ranjith | Product & AI — app, DataLabs product, analytics instrumentation |
| Prapti | Warehouse, data pipelines, the QIA computation |
| Ashish | Tech/infra, DataLabs backend, payments |
| Ritvik | App build |
| Satya | Design (frequently pulled to other work) |
| Nityam | Brand, acquisition, messaging |
| Animesh | Lifecycle campaigns, marketing ops |
| Anmol | APIs (AskInc42 v2 blocked on this) |

---

# PART 4 — MEETING RECORD

All notes in `~/inc42-context/meetings/2026/08/`. Full transcripts included.

## 31 Aug — App and Data Labs Alignment ⭐ most important

Ad-hoc recording, 16:19–16:47 IST, 28 min. Two speakers, identities not recorded.

**Decisions:** three-bucket restructure · backtrack from QIA · third-party enrichment opened · DataLabs narrowed to retention + one-time fixes · no B2B · DataLabs retention means **free-user** retention · newsletter on email **and** WhatsApp · personalisation deferred · involuntary-payment recovery is one-time hygiene not a recurring bucket · app priority activation then D7.

**Trigger, verbatim:** *"the whole idea of building this new MOP style was having a more unified direction… But in today's meeting also, I didn't feel that unified."*

**Data claims made in the call — none verified:** DataLabs acquires ~2,000/month organic (✅ verified 2,417) · 40–50k lifetime registrations (⚠️ PostHog shows 102,009 email distinct_ids) · free→paid 25% (❌ contradicts 48 lifetime payers and August's 11.3%) · 60–70% use personal email so enrichment hits 25–30% · Apollo ~₹1–2/profile.

## 24 Aug — Unified Data & Marketing Automation (Salesforce scoping)

*"No unified view of the user journey across assets."* Data 360 + Marketing Cloud pitched. Claimed ~5–6 lakh unique visitors/month (⚠️ PostHog reads 495k).

## 24 Aug — Weekly App Review

September target set: 5,000 installs, ~20% activation. Activation redefined as brief completed + minimum 60 seconds, measured on median.

## 24 Aug — Weekly Team Leads Sync

Cost optimisation ~20% done, targeting 30%. **One month of Azure credits left.** Sector-tagging check moved weekly → daily.

## 21 Aug — Sept planning call (FY27 lock)

⚠️ **The notetaker summary has speaker labels FLIPPED.** App is the primary acquisition surface. Web capped at 5–10% bandwidth. Workspaces stay separate. QIA-7 floated for faster loops.

## 12 Aug — QIA window revised

90 days → 30 days. Recorded in the strategy doc.

## 10–11 Aug — Unification direction aligned

Utkarsh agreed with the direction **and specifically with the experiment-led approach** — prove impact, do not big-bang. Disagreement was on numbers only, not the thesis.

---

# PART 5 — STANDING CAUTIONS

Every one of these is a mistake made in the previous analysis. Read before touching the data.

| # | Trap |
|---|---|
| 1 | **Never compare QIA across method versions.** Three definitional changes in three weeks — 9→10 actions, qualification coverage 9.99%→31.3%, per-platform bars — each moved the number with no behaviour change. The 26 Aug jump from ~2,100 to 5,470 was **entirely** DataLabs' 52,500 seniority records entering the calculation |
| 2 | **Scroll Depth is NOT dead.** It fires 675,496 events / 132,802 users a month — to **GA4**. Zero to PostHog. It is a routing problem, not an instrumentation one |
| 3 | **Routing scroll to PostHog does not unlock 133,000 people.** QIA requires identity; media identifies 1,982. It unlocks action #1 for those 1,982 only |
| 4 | **Media has no onboarding-completion event.** Only `Onboarding Started` (2,918) and `Step 1 Completed` (758). Do not count starts as completions |
| 5 | **The app has no employer/company field at all.** It cannot self-qualify. This is why the bar is role-only there |
| 6 | **`Seniority` is inconsistent** across 93,000 people — mixed casing, JSON-wrapped values, four vocabularies. Any qualification rate from PostHog is approximate |
| 7 | **Media May–June sign-ups and onboarding are a tracking break**, not performance. June reads a hard zero. Never quote as a trend |
| 8 | **DataLabs visitors swing 227k → 61k across May–June** with no campaign. Unreconciled. Do not build on it |
| 9 | **"3 in 4 app users already have accounts" is wrong.** August is ~50/50 — 287 new vs 294 existing. Every registrant also fires `sign_in_completed`, so treating them as separate populations double-counts |
| 10 | **5,470 cannot be reproduced from PostHog** (~1,285). The gap is newsletter clicks, web article reads, and cross-surface identity. Quote the official number for reporting; use PostHog for direction only |
| 11 | **Three DataLabs free→paid figures exist** — 25%, 11.3%, and 48 lifetime payers. None agree. Do not quote any |
| 12 | **`Search Active` does not count**, only `Search Completed`. Screen arrivals never count |
| 13 | **Combined totals are sums, not de-duplications.** The same person on two surfaces is counted twice until the identity spine lands |
| 14 | **Register Lock Interaction is firing again** (3,482 people in August), contrary to older notes saying it died 18 May |

---

## The one thing to fix first

`surfaces/unification/SPEC.md` is still a stub. Nine decisions are logged against a surface that has no written current-state spec. Writing it is the highest-value first deliverable — and it is also the Sept MOP gate: *"One Inc42 WRITTEN DEFINITION shipped — one login, one navigation, one value proposition; the document IS the deliverable."*
