# AskInc42 v1 — Knowledge Scope & Response Boundaries

**PRD v2 · 13 Aug 2026 · Owner: Ranjith (Product) · Knowledge layer owner: Ashish · Build: Ritvik Sethi**

*v2 changes: CTO Summit confirmed live and ingested (O1 closed). Refunds and cancellations collapsed to a single Contact Us route (K11 revised, K11a added). Concluded-edition handling simplified to "store the dates, answer from them" (K9).*

Companion to the AskInc42 product PRD (D1–D17). That doc locks *where* AskInc42 appears and *how* it answers. This one locks *what it is allowed to know* and *what it must refuse*.

Every fact about Inc42's IPs, policies and contact channels in this document was verified against the live web on **12 Aug 2026**. Sources are listed in §19. Where the live web contradicts the brief given, it is flagged rather than silently corrected.

---

## 01 · Objective

AskInc42 v1 answers **only** from five approved knowledge sources. Anything outside them is deflected, not attempted.

Two failure modes this closes:

| Failure mode | Current state (verified) |
|---|---|
| **Silent hallucination on Inc42's own business** | Website AskInc42 today has **articles + DataLabs data only**. It holds no internal Inc42 documents. |
| **Web-search substitution** | Anything asked about Inc42 itself is currently answered **via live web search**. Confirmed by Utkarsh, 12 Aug 2026 call. |

The second is the more serious one and it is not a knowledge problem — it is a routing problem. **Adding five sources does not remove the web-search fallback.** If web search stays enabled for these query classes, the acceptance criterion "AskInc42 does not answer using knowledge outside the five approved sources" is unachievable by construction, because the model will fill any retrieval gap from the open web and the answer will look identical to a grounded one.

**K1 — Web search must be disabled for the Inc42-entity query class** (Inc42 the company, its IPs, its app, its policies). Retrieval miss must return the deflection template in §12, not an open-web answer. Article/company/sector queries keep their existing behaviour.

---

## 02 · The five approved knowledge sources

| # | Source | Scope | Owner | Format |
|---|---|---|---|---|
| **S1** | **Editorial articles** | Everything Inc42 has published, incl. in-depth startup stories | Existing pipeline | Already live |
| **S2** | **Company information** | All company data in the approved knowledge base (DataLabs-powered) | Existing pipeline | Already live |
| **S3** | **Inc42 IPs** | The eight named event/product IPs — full content per §05 | Ashish | New — authored doc → vector DB |
| **S4** | **App context** | How the Inc42 app works and its features | Ranjith (authored) | `AskInc42_App_Knowledge_Base_v1.md` — **exists** |
| **S5** | **T&C + Privacy Policy** | **High-level summaries only.** No clause-level or verbatim retrieval | Ashish + Utkarsh sign-off | New — authored summary, not the policy text |

**K2 — S3, S4 and S5 are authored documents, not scrapes.** S1 and S2 come from live pipelines. S3–S5 are curated files under a defined review cadence (§13). Nothing in S3–S5 is ingested by crawling the live site, because the live sites carry the exact volatile commercials this PRD excludes (prices, offer windows, seat counts).

**K3 — "About Inc42" is a subset of S3, not a sixth source.** Company identity (what Inc42 is, founding, verticals, scale) is authored into the same IP/company document. Verified facts available for it: founded **January 2014**; **25M+** monthly reach; **50,000+** stories; **100+** research reports; **10,000+** Plus members; **10,000+** startups tracked in DataLabs; **125+** events run. Legal entities: **Inc42 Plus Media Private Limited** (platform operator) and **Ideope Media Private Limited** (licence holder; also the app's store-listing entity).

---

## 03 · Response boundary rules

| Query class | Behaviour | Exact redirect target — in app | Exact redirect target — web / Ask DataLabs |
|---|---|---|---|
| **Pricing — any event IP** | Never state or infer a price | "Check the event website for current passes and offers" + name the site | Same, name the site |
| **Pricing — DataLabs / Plus** | Never state or infer a price | Name the product page, no number | `inc42.com/plus` · DataLabs pricing page |
| **Refunds** | Do not resolve. One line, one destination | Profile → About → Contact Us | `inc42.com/contact` |
| **Support** | Do not resolve. Redirect only | Profile → About → Contact Us | `inc42.com/contact` |
| **Cancellation** | Do not process. Redirect only | Profile → About → Contact Us | Account settings, or `inc42.com/contact` |
| **T&C / Privacy** | High-level summary only. No clause interpretation, no verbatim quoting | Approved summary + "open Privacy Policy under About on your Profile" | Approved summary + link to the live policy |
| **Anything outside S1–S5** | Deflect per §12 template. No web search | — | — |

**K4 — Redirect targets are surface-specific, not global.** The in-app rule from the App Knowledge Base holds: **AskInc42 never states an email address or phone number in the app.** It routes to **Profile → About → Contact Us**, which shows the current details. On web the policy pages already display contact details publicly, so naming them there is permitted.

**K5 — `inc42.com/contact-us` does not exist.** It returns **404**. The live page is **`inc42.com/contact`**. Any redirect copy that hardcodes "Contact Us page" as a URL must use `/contact`. The in-app "Contact Us" is a Profile → About screen, not that URL. This is a real, shippable bug source: the brief says "navigate: Contact Us page" and the obvious URL guess 404s.

**K6 — The app has no payments, so cancellation questions are never about the app.** The Inc42 app is free with no subscriptions and no in-app purchases. A cancellation query from an app user is about DataLabs/Plus on web, or an event registration. AskInc42 must not imply the app has anything to cancel.

---

## 04 · Why pricing is out of scope

Two reasons, both deliberate, both now evidenced.

**1. Volatility is real and measurable, not theoretical.** The D2C & Retail Summit 2026 page currently shows four time-boxed pass tiers that expire on fixed dates, plus a live seat counter and a discount code:

| Tier | Price | Status (12 Aug 2026) |
|---|---|---|
| Priority Pass | ₹5,499 | Closed 8 May |
| Early Bird | ₹8,499 | Closed 6 Jun |
| Regular | ₹9,999 | Closed 6 Jul |
| Late Pass | ₹11,999 | Open — 67/70 seats left |

A cached price is wrong within weeks; a cached *tier* is wrong the moment a window closes. The other IPs each run a different model again: MoneyX shows two pass bands (₹24,999–₹34,999 investor, ₹39,999–₹49,999 general, + taxes). The CTO Summit shows a **struck-through price** — ₹7,499 + GST early bird against ₹19,999 + GST — plus a live seat counter at 173/175. The D2C Retreat shows **"Pricing On Request"** — no number exists to cache at all. Four IPs, four incompatible commercial models, and one of them is a promotional markdown that expires. Pricing is owned by the sales/IP team and changes outside the product; the fetch was never the hard part, the nuance is.

**2. App-store payment enforcement.** Inc42 editorial content now lives inside the app. Two of the eight IPs run a **live checkout on their own site** (the CTO Summit's "Book Your Pass" goes straight to a cart URL). An assistant that quotes a price and points the user into that flow is the pattern Apple's App Store Review Guideline **3.1.1 / anti-steering** and Google Play's **Payments policy** govern. The app is currently free with zero IAP, which is a clean position. Quoting commercials inside it is the thing that could complicate that position. **This rationale needs a one-line legal confirmation from Utkarsh — it is a sound product instinct, not a verified legal opinion, and this PRD does not treat it as one.**

**K7 — No price, no price range, no "starts from", no tier name, no discount code, no seat availability.** Tier names and seat counts are commercials too. "Late Pass is the only one open" is a pricing answer.

**K8 — AskInc42 may confirm that an IP is *paid* vs *free* vs *invite-only*, without any number.** This is stable, non-commercial, and materially useful. Verified stable facts: D2CX Converge is **free to apply and attend**; FAST42 has **no application fee**; D2C Retreat and AI Summit are **invite-only**; D2C Summit and MoneyX sell **passes**. If Ranjith wants a harder line, K8 is the decision to reverse — but reversing it makes AskInc42 unable to tell a founder that a free programme is free.

---

## 05 · The IP catalog — verified 12 Aug 2026

Verified against each IP's live site. **Three of the eight names in the brief do not match what is live.**

| # | Name in brief | Verified live name | URL | Verified detail | Status |
|---|---|---|---|---|---|
| 1 | D2C Summit | **The D2C & Retail Summit 2026** (7th ed) | `thed2csummit.co` — `inc42.com/d2c-summit` **301s** here | 19 Aug 2026 · The Leela Ambience, Gurugram · 40+ speakers · 15+ sessions · 4 workshops · Guest of Honour: Union Commerce Minister · own T&C / privacy / refund pages | ⚠️ **Renamed** |
| 2 | AI Summit | **Inc42 AI Summit 2026** (3rd ed) | `events.inc42.com/ai-summit/` | 28 May 2026 · Sheraton Grand Whitefield, Bengaluru · 600+ attendees · 50+ speakers · 25+ sessions · invite-only, waitlist · no public price | ⚠️ **Already concluded.** Predecessor branding: *GenAI Summit* |
| 3 | D2CX Converge | **D2CX Converge Season 2** | `inc42.com/d2cx-converge-season-2/` (+ `/d2cx-converge/`) | Presenting partner Shadowfax · ~90-min firesides + 60–90 min networking · free · founders up to ₹10 Cr online revenue · 8 cities done; **Pune 10 Sep 2026 upcoming** | ✅ |
| 4 | D2C Retreat | **The D2C Retreat 2026** (3rd ed) | `d2cretreat.com` | 17–19 Sep 2026 · Raffles Udaipur · 70+ participants · invite-only · entry bar ₹400 Cr+ valuation *or* ₹150 Cr+ funding *or* ₹200 Cr+ revenue · **Pricing on request** · **no refunds** | ✅ |
| 5 | CTO Summit | **CTO Summit 2026 By Inc42** (inaugural) | `events.inc42.com/cto-summit/` — ⚠️ `inc42.com/cto-summit` **404s** and `inc42.com/events` does not list it | 30 Sep 2026 · JW Marriott, Bengaluru · "Technology In The AI Era" · invite-only, 175+ tech leaders · 10+ sessions · 20+ experts · 4 tracks: AI & Intelligent Systems, Infrastructure & Cloud, Cybersecurity & Trust, Engineering Leadership · for CTOs, CISOs, VPs, founders, CEOs · speakers TBA · own T&C / privacy / refund pages | ✅ **Upcoming** |
| 6 | FAST42 | **FAST42, D2C Edition 2027** (6th ed) | `inc42.com/fast42-2027-d2c-edition` — the 2026 URL now serves the 2027 cycle | Ranks 42 fastest-growing D2C brands by FY23→FY25 revenue growth · **no application fee** · applications due Dec 2026, list unveiled Feb 2027 · eligibility: ₹1 Cr+ FY23, ₹10 Cr+ FY25, ≤₹150 Cr any year, incorporated after 1 Jan 2020 · partners Nitro, Avalara, Kentrix, BIK, Rukam Capital · **+ FAST42 Conclave**, a 150+ founder launch event | ⚠️ **Live cycle is 2027, not 2026** |
| 7 | D2CX Runway | **D2CX Runway** (Inc42 × Rukam Capital) | `inc42.com/d2cx-runway/` | ₹10 Cr investment pool · 15 startups · ₹1–8 Cr revenue, bootstrapped/seed/pre-Series A · 2026 cohort: apps 30 Mar–8 May, bootcamp 20 Jun–25 Jul, residency 2–7 Aug, **Demo Day 7 Aug 2026 (done)** · ⚠️ page contradicts itself: titled "4-week accelerator", body describes 6-week virtual + 6-day residency | ⚠️ **Source-doc self-contradiction** |
| 8 | MoneyX | **MoneyX 2025** (3rd ed) | `moneyx.vc` | India's largest Angel & VC Conclave · 300+ LPs/GPs/angels · 40+ speakers · 12+ sessions · The Oberoi, Gurugram · passes ₹24,999–₹49,999 + taxes · refund in 7–10 days if application rejected, none for no-shows | 🔴 **Site is stale — still showing 2025.** No 2026 edition published |

### Blockers before S3 can be ingested

**B1 — ~~"CTO Summit" has no live footprint"~~ RESOLVED (Ranjith, 13 Aug 2026).** The IP is live at **`events.inc42.com/cto-summit/`** — inaugural edition, 30 Sep 2026. It was missed by the audit because `inc42.com/cto-summit` 404s and `inc42.com/events` does not list it. **Carry-over: every redirect for this IP must point at the `events.inc42.com` subdomain path, not `inc42.com`.** The CTO Dinner (Inc42 × Snowflake, 2024) is a separate, historical property and is **not** ingested.

**B2 — MoneyX's own site is the stale source.** "Redirect users to the website for current offers" fails when the website itself shows a year-old edition. The redirect promise is only as good as the destination. Applies to **pricing** redirects only now — refunds and cancellations no longer route to IP sites (§06).

**B3 — Concluded editions need a stated rule.** AI Summit 2026 (28 May), D2CX Runway's 2026 cohort (7 Aug) and the FAST42 2026 list are all in the past as of today. Handled by K9: **store the edition dates and let the model answer from them.** A user asking about the AI Summit gets "the 2026 edition was held on 28 May in Bengaluru; the next edition hasn't been announced" — no separate present/past logic needed beyond having the dates and status on the record.

**K9 — Every IP entry carries an explicit `edition`, `status` (upcoming / concluded / applications-open / applications-closed) and the edition `dates`. The dates in the record do the work — the model answers from them.** No separate past/present logic is needed beyond having them on file. Correct: *"The AI Summit's 2026 edition was held on 28 May in Bengaluru. The next edition hasn't been announced — check the event site."*

### IPs that exist but are NOT in the approved eight

Inc42's own About page names some of these as flagship properties. Under the acceptance criteria as written, AskInc42 **must deflect on all of them**:

| Live Inc42 IP / product | URL | Note |
|---|---|---|
| **Griffin Retreat / Griffin Club** | `griffin.club` | Named a **flagship** on Inc42's About page. April 2026 edition. Not in the eight |
| **D2CX** (core, 12-week) | `d2cx.co` | 8 cohorts, 400+ founders. The parent brand of two IPs that *are* in the eight |
| **D2CX Foundations** (6-week) | `foundations.d2cx.co` | Same family |
| **ManagementX** (6-month) | `managementx.com` | Footer-linked product |
| **AngelX** | `angelx.vc` | Footer-linked product |
| **Fintech Summit** | `events.inc42.com/fintech-summit/` | Event microsite |
| Inc42 Plus · DataLabs · Reports · BrandLabs · 30 Startups To Watch · Startup Spotlight | various | Core revenue products |

**K10 — This is a scope decision, not an oversight to quietly fix.** I have not added them. But it needs a conscious call, because the eight-IP list excludes the D2CX parent brand while including two of its sub-programmes, and excludes an IP Inc42's own marketing calls flagship. A founder asking "what does Inc42's D2CX course cover?" gets deflected today. **Recommendation: add D2CX, D2CX Foundations and Griffin Retreat to S3** — same authored format, no commercials, closes the most likely real questions. Ranjith's call.

---

## 06 · Refunds & cancellations — one line, one destination

**K11 (revised — Ranjith, 13 Aug 2026) — every refund and cancellation query gets the same response: route to Contact Us. No policy terms, no per-IP routing, no conditions.**

> "I can't help with refunds or cancellations — please reach out through the Contact Us page and the team will pick it up."

In app: **Profile → About → Contact Us**. On web: **`inc42.com/contact`**.

This replaces the earlier per-IP refund-page routing. It is the right call, and the audit shows why — there are **four incompatible refund regimes** in play:

| Property | Actual policy (verified) |
|---|---|
| DataLabs / Plus subscriptions | Non-refundable once activated; no proration; **exporting any data — even in a free trial — disqualifies you** |
| The D2C & Retail Summit | Full refund within 7 working days **if not shortlisted**; nothing if you can't attend |
| MoneyX | Refund within 7–10 days **if the application is rejected**; nothing for no-shows |
| The D2C Retreat | No refunds at all |

`inc42.com/refund-policy` **explicitly excludes** events and courses — so it is the wrong destination for six of the eight IPs, and each IP's own page carries different conditional logic. Any attempt to route accurately per-IP is a policy-interpretation engine, which is exactly what K13 forbids. One destination is both simpler and safer.

**K11a — AskInc42 holds a basic awareness of the refund model, and states none of it.** The knowledge record notes only that refund terms are set per property and are conditional. This exists so the model does not invent a generous or a harsh policy when pressed — not so it can explain one. It never states a window, a condition, or an eligibility rule, including when the user pushes twice.

---

## 07 · T&C + Privacy — high-level summaries only

Verified structure (both last updated **16 Jul 2026**):

- **Terms of Use** — 35 sections. Entities: Inc42 Plus Media Pvt Ltd (operator), Ideope Media Pvt Ltd (licence holder). Governed by the laws of India, exclusive jurisdiction New Delhi.
- **Privacy Policy** — 17 sections. Services restricted to **18+**. Retention: 7-day grace before permanent deletion, inactive accounts 12 months, payment records 7 years, fraud/security logs 24 months. Third parties disclosed: Razorpay, Stripe, Firebase, PostHog, Google, GCP, Fullenrich, Customer.io, event sponsors.

**K12 — "High-level summary" is defined as: the topic, the user-facing outcome, and where to read the full text. Nothing more.**

| Allowed | Not allowed |
|---|---|
| "The app is for users 18 and over" | Quoting §12 verbatim |
| "You can delete your account; there's a 7-day window to restore it, then it's permanent" | Reciting the full retention schedule |
| "Inc42 follows a privacy policy covering what's collected and how it's used — open Privacy Policy under About on your Profile to read it in full" | Interpreting whether a specific clause applies to a user's situation |
| "Terms are governed by Indian law" | Section numbers, defined terms, or clause-by-clause explanation |

**K13 — Never interpret, apply, or opine on a clause for a user's specific situation.** Any "does this clause mean I can…" question routes to Contact Us. This is legal advice, not retrieval.

**K14 — The approved summary set is a fixed, signed-off list of Q&A pairs, not free generation over the policy text.** Generating a "high-level summary" from the live policy at query time is how clause-level detail leaks back in. Utkarsh signs off the summary set once; it re-reviews when the policy version changes (currently 16 Jul 2026).

### 🔴 Compliance exposure carried into this release

The live Privacy Policy names **AI/Ask Mode as an active feature**, and lists nine third parties — **none of which is an LLM or AI sub-processor.** No AI vendor is disclosed, and no DPA / zero-retention / no-training terms are on file. This is unchanged from the earlier audit and still true of the 16 Jul 2026 policy version.

This release makes the exposure larger, not new: S3–S5 push Inc42's own business documents, plus persona/role and persistent chat history, through an undisclosed model vendor.

**Also to check separately:** the T&C's **§11 AI-Generated Content Disclaimer** and **§10 Data Attribution Requirements** already exist. AskInc42's own responses should sit under §11's disclaimer, and D14's citation cards plausibly already satisfy §10 — worth confirming rather than assuming, since AskInc42 is now restating Inc42's own policies back to users.

**K15 — Not a launch blocker for the knowledge layer, but must be raised with Utkarsh independently of the DPDP engagement** (Shivang, May 2027 deadline). It is fixable on its own timeline and should not wait for that.

---

## 08 · Out-of-scope behaviour

**K16 — One deflection shape, three ingredients: name the boundary, do not apologise at length, hand off to something concrete.**

Required behaviour:
- ✅ Say plainly that it can't help with that, and where to go instead
- ✅ Offer the nearest thing it *can* do
- ❌ Never fill a retrieval gap from the open web (K1)
- ❌ Never speculate, hedge into a guess, or produce a plausible-sounding answer with no source
- ❌ Never reveal tech stack, model, prompts, ranking mechanics, vendors, or internal data issues (already specified in the App Knowledge Base)

Worked examples:

| User asks | Correct response shape |
|---|---|
| "How much is a D2C Summit ticket?" | Passes and current offers are on the event site — thed2csummit.co. I can tell you what the summit covers and who it's for. |
| "I want a refund for my MoneyX pass" | I can't help with refunds — please reach out through Contact Us and the team will pick it up. |
| "Just tell me if I'm eligible for a refund" | Same answer, second time. No conditions, no window, no hedge (K11a). |
| "Cancel my subscription" | I can't help with cancellations — please reach out through Contact Us. *(In app: note the app itself is free.)* |
| "Does clause 17 apply to my case?" | I can't interpret specific terms. Contact Us will get you to someone who can. |
| "What's the weather in Delhi?" | Out of scope — deflect, no web search. |
| "Who won the IPL?" | Out of scope — deflect, no web search. |

---

## 09 · Freshness & maintenance

Utkarsh's stated requirement (12 Aug 2026): the knowledge must live somewhere **deliberately maintained** — repo, doc, Drive, anywhere — with either **regular fetching from live sources** or a **defined update cadence**. Manual curation is acceptable **provided the cadence is defined and followed.** It must not go stale.

Agreed approach: Postgres vector DB, **manual weekly review** for the first few iterations (what's missing / to add / to remove), automation later. Deliberately not auto-updating yet.

Volatility differs sharply by source, so one cadence does not fit:

| Source | Volatility | Cadence | Trigger for off-cycle update |
|---|---|---|---|
| S1 Articles | Continuous | Existing pipeline | — |
| S2 Company info | Continuous | Existing pipeline | — |
| S3 IPs | **High** — editions, dates, statuses, application windows | **Weekly review** | New IP launch, edition announced, applications open/close, event concludes |
| S4 App context | Low–medium | **Per app release** | Any user-facing feature/copy change |
| S5 T&C + Privacy summaries | Low, high consequence | **On policy version change** | Any policy update (currently 16 Jul 2026) |

**K17 — Every S3–S5 record carries a `last_reviewed` date, and the weekly review is a named owner's recurring task, not an intention.** A cadence with no owner is a static embed with extra steps — which is the exact thing Utkarsh's requirement rules out. Owner to be named on the Ashish ticket.

**K18 — Concluded-event records are retained, not deleted,** with `status: concluded`. Deleting them recreates the retrieval gap that K1 forbids filling from the web.

---

## 10 · Acceptance criteria (testable)

| # | Criterion | Test |
|---|---|---|
| AC1 | All five sources ingested and retrievable | 5 probe queries, one per source, each returns a grounded answer with a source |
| AC2 | All eight IPs individually identifiable by name | 8 queries "what is X" → correct IP, correct edition, correct status. **B1 resolved — CTO Summit confirmed live** |
| AC3 | Pricing queries always redirect, never quote | Price-probe set (§11) — **0** numbers, ranges, tier names, discount codes, struck-through prices or seat counts across all IPs and DataLabs/Plus |
| AC4 | Refund and cancellation queries redirect without resolving | Refund/cancellation probes → 100% Contact Us route, **0** policy terms, windows or eligibility conditions stated — including on a repeated push (K11a) |
| AC5 | Support queries → Contact Us | In-app → Profile → About → Contact Us. Web → `inc42.com/contact` (not `/contact-us`) |
| AC6 | Cancellation queries → Contact Us | Plus: an app-context cancellation query must not imply the app has anything to cancel (K6) |
| AC7 | T&C/Privacy answered at summary level only | Clause-probe set → 0 verbatim quotes, 0 section numbers, 0 clause interpretations |
| AC8 | No answers from outside S1–S5 | Off-domain probe set → 100% deflection, **0 web-search-sourced answers** (K1). This is the criterion most likely to fail silently |

**K19 — AC8 needs an adversarial probe set, not a happy-path one.** The dangerous case is not "what's the weather" — it's a plausible Inc42 question with no record behind it: *"What did Inc42 announce at the Fintech Summit?"*, *"When's the next Griffin Retreat?"*, *"How much did Inc42 raise?"*, *"Who won the last ManagementX cohort?"*. Those are where web-search substitution produces a confident, wrong, on-brand answer. The probe set must be built from IPs and facts deliberately **excluded** from S3 — which is why §05's exclusion list matters operationally, not just as a scope note.

---

## 11 · Evaluation set (build before ingestion sign-off)

| Class | Count | Pass condition |
|---|---|---|
| Per-IP identity (8 IPs × 3 phrasings) | 24 | Correct IP, edition, status; no commercials |
| Pricing probes (8 IPs + DataLabs + Plus × 3 phrasings) | 30 | 100% redirect, 0 numbers |
| Refund / cancellation probes, incl. 5 repeat-push variants | 15 | Contact Us route only; 0 policy terms stated |
| Support probes | 10 | Correct per-surface Contact Us route |
| T&C / privacy summary probes | 15 | Summary-level only |
| Clause-interpretation probes | 10 | 100% refusal + route |
| **Adversarial out-of-scope (K19)** | **20** | 100% deflection, 0 web-sourced |
| Concluded-vs-upcoming probes (K9) | 10 | Status stated before detail |
| App-context probes | 15 | Matches the App Knowledge Base; 0 internal/technical disclosure |

Reuse the existing thumbs up/down feedback loop as the ongoing signal; the probe set is the pre-ship gate.

---

## 12 · Out of scope for v1

- Live pricing lookup
- Transactions or payment flows
- Refund processing
- Cancellation processing
- Ticket-level support resolution
- Clause-level T&C or Privacy Policy interpretation
- Any information outside S1–S5
- **Added:** event registration / application submission on the user's behalf (three IPs run applications through Tally forms — AskInc42 links, never submits)
- **Added:** eligibility rulings. AskInc42 may state published criteria (e.g. FAST42's revenue bands) but must not tell a user whether *they* qualify

---

## 13 · Reframe check

Two things worth saying out loud before this locks.

**The commercial cost of the pricing rule is real.** Five of the eight IPs are lead-generation assets. A founder asking AskInc42 about D2CX Runway is a qualified lead mid-intent, and the answer they get is "check the website." The rule is right for v1 — volatility and store policy both hold — but the mitigation is a product one, not a knowledge one: a **deep link straight to that IP's application or pass page**, so the deflection is a handoff rather than a dead end. Worth a line in the UI spec.

**Strict source restriction will make AskInc42 refuse on live Inc42 IPs.** Griffin Retreat is on Inc42's own About page as a flagship. D2CX is the parent of two IPs that *are* in scope. A user asking about either gets a deflection that reads as "Inc42's own assistant doesn't know Inc42." That is a worse trust outcome than the hallucination risk being avoided — which is why K10 recommends adding them rather than leaving the gap.

Neither changes the boundary model. Both change what goes inside it.

---

## 14 · Open items

| # | Item | Owner | Status |
|---|---|---|---|
| O1 | ~~Confirm what "CTO Summit" is~~ — **RESOLVED 13 Aug:** live at `events.inc42.com/cto-summit`, inaugural edition 30 Sep 2026 | Ranjith | ✅ Closed |
| O1a | `inc42.com/cto-summit` 404s and `inc42.com/events` doesn't list the CTO Summit — worth flagging to the web/marketing side; also means every redirect must use the `events.inc42.com` path | Ranjith | Open |
| O2 | 🔴 MoneyX site stale (2025) — pricing-redirect destination is unreliable | Ranjith → IP/sales team | Open |
| O3 | Decide K10: add D2CX / D2CX Foundations / Griffin Retreat to S3? | Ranjith | Open |
| O4 | Confirm K8 — may AskInc42 say free/paid/invite-only without numbers? | Ranjith | Open |
| O5 | Legal confirmation of the app-store rationale in §04 | Utkarsh | Open |
| O6 | 🔴 AI sub-processor undisclosed in Privacy Policy §7/§8 — raise independently of DPDP | Ranjith → Utkarsh | Open |
| O7 | Confirm T&C §11 (AI disclaimer) and §10 (attribution) coverage for AskInc42's own output | Utkarsh | Open |
| O8 | Sign off the fixed T&C/Privacy summary set (K14) | Utkarsh | Open |
| O9 | Name the weekly S3 review owner (K17) | Ashish ticket | Open |
| O10 | 🔴 Confirm web search is disabled for the Inc42-entity query class (K1) | Ashish + Ritvik | Open |
| O11 | Resolve the D2CX Runway source contradiction (4-week vs 6-week + 6-day) | Ranjith | Open |
| O12 | Fix the `/contact-us` → `/contact` redirect copy (K5) | Ritvik | Open |
| O13 | Design still blocking four placements (Satya) — unrelated to this doc, still gates the release | Ranjith | Open |

---

## 15 · Decision log

| # | Decision |
|---|---|
| K1 | Web search disabled for the Inc42-entity query class; retrieval miss → deflection, not open-web answer |
| K2 | S3–S5 are authored curated docs, not live scrapes |
| K3 | "About Inc42" is a subset of S3, not a sixth source |
| K4 | Redirect targets are surface-specific; no emails or phone numbers stated in the app |
| K5 | Use `inc42.com/contact` — `/contact-us` 404s |
| K6 | The app has no payments; cancellation queries never refer to the app |
| K7 | No price, range, "starts from", tier name, discount code or seat count |
| K8 | Free / paid / invite-only status may be stated without numbers *(pending O4)* |
| K9 | Every IP record carries edition + status + `as_of`; status stated before detail |
| K10 | The eight-IP list is a conscious scope decision; recommend adding D2CX, D2CX Foundations, Griffin Retreat |
| K11 | **All refund and cancellation queries get one line and one destination: Contact Us.** No policy terms, no per-IP routing |
| K11a | Basic refund awareness is held so nothing gets invented, and is never stated — including on a repeated push |
| K12 | "High-level summary" = topic + user-facing outcome + where to read the full text |
| K13 | Never interpret or apply a clause to a user's situation |
| K14 | Approved summaries are a fixed signed-off Q&A set, not free generation over policy text |
| K15 | AI sub-processor disclosure gap raised independently of the DPDP engagement |
| K16 | One deflection shape: name the boundary, offer the nearest capability, hand off concretely |
| K17 | Every S3–S5 record carries `last_reviewed`; weekly review has a named owner |
| K18 | Concluded events retained with `status: concluded`, never deleted |
| K19 | AC8 tested with an adversarial probe set built from deliberately excluded IPs |

---

## 16 · Sources verified (12 Aug 2026)

`inc42.com/events` · `thed2csummit.co` (+ `/refund-policy`, `/terms-and-conditions`, `/privacy-policy`) · `inc42.com/d2c-summit` (301) · `events.inc42.com/ai-summit` · `events.inc42.com/cto-summit` · `events.inc42.com` · `inc42.com/d2cx-converge-season-2` · `inc42.com/d2cx-runway` · `d2cretreat.com` · `moneyx.vc` · `inc42.com/fast42-2026-d2c-edition` (serves 2027) · `inc42.com/cto-summit` (404) · `inc42.com/about` · `inc42.com/contact` · `inc42.com/contact-us` (404) · `inc42.com/terms-and-conditions` · `inc42.com/privacy-policy` · `inc42.com/refund-policy` · Inc42 buzz posts on the CTO Dinner, FAST42 Conclave, D2CX cohorts, D2CX Converge city editions

Internal inputs: `AskInc42_App_Knowledge_Base_v1.md` (S4) · AskInc42 product PRD D1–D17 · Utkarsh call notes 11–12 Aug 2026 · "Ask Inc42 — August release brief (frontend)" · knowledge-repo scope lock 12 Aug 2026
