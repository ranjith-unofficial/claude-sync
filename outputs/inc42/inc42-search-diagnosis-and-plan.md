# Inc42 Search — Diagnosis & Implementation Plan

**Date:** 30 Aug 2026 · **Revised: 6 Sep 2026** · **Scope:** all three search surfaces — the app, Inc42 Media (articles), DataLabs (companies/people/investors)
**Method:** live API replay against ground truth pulled from outside the system (real Inc42 articles, real user queries from PostHog), plus behavioural data from PostHog App (146258) and DataLabs (66351). The 6 Sep revision adds a live re-test of the production APIs **and of the real user-facing search pages**.
**Supersedes:** the coverage-based diagnosis in `app-search-defects.md` (23 Aug) and expands `app-search-root-cause.md` (30 Aug).

> **What changed on 6 Sep.** Ranjith's two open symptoms (`cred` misses CRED; results full of junk) were reproduced and root-caused — they are **one** bug, and it is DataLabs-only. Separately, driving the real inc42.com search page showed that **article search returns nothing at all** for every query, which no prior version of this document caught. And the v1-vs-v2 comparison inverted: v2 is *not* strictly better, so the "migrate everything to v2" recommendation is now conditional. See **C4–C8**.
>
> Nothing has been fixed since 30 Aug — every multi-word failure in this document's own regression set still returns zero.

---

## 0. CORRECTIONS after Ranjith's review (30 Aug) and the live re-test (6 Sep)

Three things in the first version of this document were wrong or overstated (C1–C3). Five more were added or corrected on 6 Sep (C4–C8). All are corrected here and in place below.

### C1. There is a **fourth** search system — `global-search-v2` *(originally titled "and it is the good one" — see C4)*

My testing hit `POST /header/global-search` (v1), which inc42.com's header uses. **DataLabs uses `POST /header/global-search-v2`**, a different endpoint with a different response shape (`results[]` with `entity_type`, plus `did_you_mean` and `applied_filters`). That is why my report said `lava mobile` returns "Vaca Mobiles" while the DataLabs UI showed "No results found" — **two different engines, same query.** Ranjith's screenshots were right; my report described the wrong endpoint for that surface.

Measured side by side:

| Query | v1 — inc42.com header | v2 — DataLabs |
|---|---|---|
| `zomato` | 11 rows: Zomato, Zocalo, Zosito | **1: Zomato** |
| `zomto` | 2: Zomato, TOMTO LEMON | **Zomato + `did_you_mean:"zomato"`** |
| `zomatoo` | 4: Zomato, GoMaxoo, Somato Publications | **Zomato + `did_you_mean:"zomato"`** |
| `shipr` | 13: Shippr, Shiproute, Shiprocket | **Shiprocket rank 1** |
| `airbound` | 11: Airbound, Airborne, Abound | **1: Airbound** |
| `fintech` | 20: MyLead FinTech, Spay Fintech… | **`Fintech (INDUSTRY)` + filter `{company:{sector:["Fintech"]}}`** |
| `green hydrogen` | 20: Hydrogen Gentech, Silver Hydrogen Peroxide | **filter `{sector:["Energy"], sub_1:["Hydrogen"]}`** |
| `iifl finance` | 20 rows of noise | **0** |
| `wagh bakri` | 20 rows of noise | **0** |
| `lava mobile` | 20 rows of noise | **0** |
| `tbotek` | 7: JBTEK, Design Totke | **0** |

### Worked example — `airbound`, reproduced end to end

Ranjith's screenshot of `inc42.com/#inc-search-popup` shows Profiles: **Airbound, Abound, Airborne, Airmount Logistics** + "Show More". Reproduced exactly:

| Step | Output |
|---|---|
| v1 API raw order (11 companies) | Airbound, Airborne, Abound, HireBound, Airmount Logistics, Around Always, Wizbound Technologies, Inbound Aerospace, Inbound WebHub, All Around Polymer, Around the Globe Repz |
| After `main.min.js` re-sort (substring match first, then alphabetical) | **Airbound, Abound, Airborne, Airmount Logistics**, All Around Polymer, Around Always, … |
| What the UI shows | exactly those four, then "Show More" — **matches the screenshot** |
| **v2, same query** | **`Airbound` — one result, nothing else** |

Two things this proves:

1. The browser-side re-sort in `main.min.js` is **real and load-bearing** — it is the only reason Airbound ranks first at all, since the API returned Airborne second. It is compensating for the server's ranking. An earlier version of this document recommended simply deleting it; that would make v1 *worse*. It should be removed only as part of moving to v2, which returns correct order from the server.
2. Every one of the three wrong profiles a user sees — Abound, Airborne, Airmount Logistics — disappears on v2. The noise is a v1 artefact, not a data problem.

**v2 already does most of what §9 proposed building** — typo correction with `did_you_mean`, entity typing, and topic-to-sector resolution (`fintech` → a sector filter, `green hydrogen` → Energy/Hydrogen). It is live, and inc42.com is not using it.

> **Qualified by C4 (6 Sep).** True of v2's *architecture*, and the table above still reproduces. But the table is a favourable sample: across a 30-query regression set v2 returns **nothing at all 50% of the time**, misses exact names v1 gets at rank 1, and is **4× slower**. "v2 is much better" was too strong — it is better at the hard queries and worse at the easy ones.

**v2's most visible defect:** it passes the *entire* query string as a single `company_search` value — `{"company":{"company_search":["iifl finance"]}}` — so any multi-word query needs an exact full-name match or returns nothing. No tokenisation, no partial phrase match. That behaviour explains every "No results found" screenshot: `iifl finance`, `wagh bakri`, `lava mobile`. It also explains why run-together `tbotek` fails.

> **Superseded in part by C4/C5 (6 Sep).** This was written as v2's *one* defect. It is one of **three**: (a) no tokenisation — this paragraph; (b) **no exact-match boost**, which is why `cred` misses CRED and `ola` ranks 3rd — the symptom Ranjith actually reported; (c) **no recall fallback**, which is why single tokens like `apax`, `birdeye` and `speciale` return zero on v2 while v1 answers them. Defect (b) is the higher-value fix.

### C2. The rate-limit lockout was self-inflicted and is not a user-facing problem

I induced it with deliberately abnormal parallel load (hundreds of requests, 6 threads). **Ranjith could not reproduce it manually, and normal use will not hit it.** It should not have been presented as a live severity. The verified fact is narrow: the endpoint has an IP-level limit that, once tripped by abuse-level traffic, locks out the whole `datalabs-api` host for ~30 minutes. That is worth knowing for load-testing and for any server-side batch job — it is **not** an explanation for what users are seeing. Demoted from root cause #1.

### C3. The typing-speed table is a correlation, not a demonstrated cause

The numbers are real — they come from PostHog, not from an assumption — and the pattern survives splitting by scope:

| Scope | Fast (<400ms gap) | Slow (>1500ms gap) |
|---|---|---|
| Articles | 60.7% zero (n=28) | 35.1% zero (n=74) |
| Companies | 40.0% zero (n=110) | 17.8% zero (n=191) |

But **the causal story I attached to it (rate limiting) is not supported**, and one person typing at two speeds cannot reproduce a population-level correlation — Ranjith tried and correctly saw no difference. There is also an unresolved confound: fast keystrokes are mid-word fragments of a longer intended word, and slow ones are more often complete words, so the two groups differ in content, not only in timing. Treat the table as a signal worth explaining, not as evidence for a mechanism.

**What does survive without a causal claim** is the non-determinism: the same user, same scope, same query string, repeated within seconds, returns 0 one time and >0 another — 57.1% of repeated company queries and 75.0% of repeated article queries. The `shipr → 5 → 0` sequence is a direct observation, not an inference. The most likely cause is a **client-side response race** — per-keystroke requests resolving out of order and a stale response overwriting a good one — which matches the "race condition" already logged as a live bug in the 26 Aug v2 scoping sync. It is not the rate limiter.

**The fix does not change:** debounce plus cancel in-flight requests kills a response race and request flooding alike.

---

## 0b. CORRECTIONS from the live re-test (6 Sep 2026)

### C4. v1 vs v2 is a recall/precision trade-off — **v2 is not simply "the good one"**

C1 concluded v2 was better on every axis and that its only real defect was multi-word tokenisation. Re-measured 6 Sep over a 30-query regression set drawn from Appendix A and Appendix B:

| | v1 `/header/global-search` | v2 `/header/global-search-v2` |
|---|---|---|
| Hard zeros on the shared subset | 1/15 | **15/30 (50%)** |
| `cred` → CRED | **rank 1** | **absent entirely** |
| `ola` → Ola | **rank 1** | rank 3 (behind Manam Chocolate, Prolance) |
| `navi` → Navi | **rank 1** | rank 3 (behind Navixel, Navigatio Asia) |
| `speciale`, `apax`, `ultravio`, `taga motors`, `birdeye`, `youtube`, `trancxn` | returns rows | **0** |
| `zomto` (typo) → Zomato | noisy | **rank 1 + `did_you_mean`** |
| `fintech` / `green hydrogen` | name-substring noise | **resolves to a sector filter** |
| `peak xv` | noise | **investor + portfolio companies** |
| Latency p50 | **390ms** | **1,558ms** (p90 1,741ms, max 3,347ms) |

**v2 has the better architecture — typed entities, `did_you_mean`, topic→sector resolution — but worse retrieval:** no recall fallback, no exact-match boost, and 4× the latency. Migrating to v2 as-is trades one failure class for another, and would **regress `cred` on inc42.com, where it currently works**.

This is the same two-engines-one-query confusion as C1: Ranjith's `cred` complaint is a **DataLabs-only** symptom. The identical query on inc42.com returns CRED at rank 1.

§9.0 items 3 and 4 (migrate inc42.com and the app onto v2) are rewritten below as **conditional** on fixing v2's recall and latency first.

### C5. `cred` root cause — no exact-match boost, not a coverage gap

Ranjith's symptom (1) from 4 Sep, reproduced and explained:

| Check | Finding |
|---|---|
| Is CRED indexed? | **Yes** — `object_id C-2623`, slug `cred`, name exactly `CRED`, Fintech, Bengaluru, 2018 |
| How it was found | Returns correctly via `fintech` (sector) and `peak xv` (portfolio) — just never via its own name |
| Companies matching "cred" | **175** (`company/new-search`, `company_search:["cred"]` → `count: 175`) |
| What v2 returns for `cred` | 15 rows: CredR, InCred Holdings, InCred, Credgenics, OkCredit, CredAble, Altum Credo, Credlix… — **CRED absent** |

v2 substring-matches, caps at 15, and has no exact-match boost and no relevance floor, so the exact answer never surfaces above 175 competitors.

**Ranjith's symptom (1) and symptom (2) are the same defect.** "Exact word misses" and "too many irrelevant results" are two faces of one missing ranking rule. Fixing it fixes both.

This also narrows C1's claim that v2's "single defect" is passing the whole query as one `company_search` value. That is **one of three**: (a) no tokenisation, (b) no exact-match boost, (c) no recall fallback when the phrase match fails. (b) is the one users actually report.

### C6. The server is deterministic — the non-determinism is confirmed client-side

| Test | Result |
|---|---|
| 6× identical `green hydrogen` (v2) | n=2 every time |
| 8× identical `shipr` (v2) | n=3 every time |
| 8× identical `shipr` (v1) | identical every time |

Confirms C3's revised position: the 57–75% flip-flop is a **client-side response race**, not a backend or rate-limit effect. **Stage 0 (§8) stands unchanged and is still the right first ship.**

### C7. Article search on inc42.com returns **nothing at all** — and §4 measures a path no user hits

This is new, and it is the most severe finding in the document.

Driving the real user-facing page — `https://inc42.com/?s=<query>` — the results container is server-rendered **empty**:

```html
<div id="relevant" class="tab-content current">
  <div id='inc-algolia-hits' class="load-result"></div>   <!-- empty -->
</div>
<div id="inc-algolia-pagination"></div>
```

Nothing ever fills it. The entire Algolia InstantSearch path is inert:

| Check | Finding |
|---|---|
| `algolia` config global on the page | **not defined anywhere** |
| `inc42-algolia-search.js`, first statement | `if ( 'undefined' === typeof algolia ) { return; }` → **bails immediately** |
| `algoliasearch` / `instantsearch` libraries | **not enqueued at all** (full script list checked) |
| `main.min.js` — 13 `algolia` references | **all show/hide UI plumbing** (`#algolia-stats`, `#search-default-box`, un-hiding `#relevant`) — **zero fetch, zero render** |
| Shipped HTML still contains | the unrendered template `{{{ data._highlightResult.post_title.value }}}` |

Verified empty for `cred`, `zomato`, `fintech`, `startup`, `funding`. **The user gets "You searched for X", a blank results area, and the "Trending On Inc42" sidebar.**

**Two corrections this forces:**

1. §1 calls the Algolia markup "dead leftover — no Algolia request fires." Accurate, but it badly understates the consequence. It is not harmless leftover: **it is the reason article search returns nothing.**
2. **§4 measures `wp-json/wp/v2/posts?search=` — an API path no user ever reaches.** Its findings are real but describe the REST API, not the product. Re-measured 6 Sep: p50 **3,899ms**, `EMS` → 16,717, `chai` → 12,949, `cred` → 10,811, `myjar` → 0. New defect visible there: date-ordering plus a continuously-updated article means **8 of 10 test queries return "Indian Startup IPO Tracker 2026" as the top hit**. §4 is relabelled accordingly.

The one Algolia call that *is* live is unrelated to article search: a hardcoded glossary lookup (index `wp_posts_glossary`, app `VZW3KNFV02`) bound to the `#keyword` box.

> **Caveat — confirm before circulating.** This is derived from the served HTML and the enqueued scripts, not from a rendered browser session. A 30-second check on inc42.com in a real browser confirms or refutes it, and should be done before this finding goes to engineering.

### C7b. What inc42.com header search actually does today

| Popup section | Backing call | Status |
|---|---|---|
| Profiles (companies / people / investors) | `POST /header/global-search` (v1) → rendered into `#global-search-profile-data` | **works** — `cred` returns CRED at rank 1 |
| Articles / stories | Algolia InstantSearch → `#inc-algolia-hits` | **dead — renders nothing** |

`main.min.js` contains **no article or post fetch of any kind** for the popup. On the main site, search finds companies but never content — for a media business, the inverse of what it should do.

### C7c. Where v2 actually lives

`global-search-v2` appears on **none** of the public pages checked — `/datalabs/`, `/company/`, `/company/zomato/`. The public `/datalabs/` marketing page itself uses **v1**. v2 is inside the **logged-in DataLabs app**, which was not reachable for this test, so v2 was measured directly at the API.

This matters for §11: the open "which endpoint does the app call?" question should be answered in the same conversation as "which surfaces are on v2 today?"

### C8. Access notes for anyone rebuilding the regression harness

- All `datalabs-api.inc42.com` endpoints return **`403 {"error":"Unauthorized"}`** without a **`Referer: https://inc42.com/`** header. Origin and User-Agent alone are not enough.
- **v1's response key is `companies` (plural); v2 uses `results[]`.** Reading v1 for a `company` key returns an easy false negative — it looks like the engine returns nothing when it is actually returning 20 rows.
- `company/new-search` **ignores `size` and `from`** for `company_search` queries — it returns 5 rows regardless, while reporting the true match count in `count`.

---

## 1. What is actually running

There is no single search system. There are three, none of them a search engine.

| Surface | Backend | What it matches on | Latency p50 (6 Sep) |
|---|---|---|---|
| Company / person / investor — **inc42.com header** | `POST datalabs-api.inc42.com/header/global-search` (**v1**) body `{"keyword":"…"}` | Entity **name only**, fuzzy. Returns ≤20 companies + ≤10 people + ≤20 investors. Response key is `companies` (plural) | **390ms** |
| Company / person / investor — **logged-in DataLabs** | `POST datalabs-api.inc42.com/header/global-search-v2` body `{"keyword":"…"}` | Returns `results[]` with `entity_type`, plus `did_you_mean` and `applied_filters`. Typo-corrects and resolves topics to sector filters — but matches the **whole query string as one exact phrase**, with no exact-match boost and no recall fallback | **1,558ms** |
| Company list + filters | `POST datalabs-api.inc42.com/company/new-search` body `{filter,from,size,sort,sortby,search_url,is_inc42}` | Structured filters. **Ignores `size`/`from` on `company_search` — always 5 rows**, true total in `count` | 227ms |
| **Articles (Inc42 Media) — what users get** | Algolia InstantSearch into `#inc-algolia-hits` | **Nothing. The path is inert — see C7.** Every query renders an empty results area | n/a |
| Articles — the REST API (**not user-facing**) | `wp-json/wp/v2/posts?search=` / `wp/v2/search` | SQL `LIKE '%term%'` over title + body, **ordered by date** | **3,899ms** |
| Relevance ranking (v1 surfaces) | Done **in the browser** — `main.min.js` re-sorts the response with `name.toLowerCase().includes(query)` then alphabetically | — | — |

**Access requirement:** every `datalabs-api.inc42.com` endpoint 403s without a `Referer: https://inc42.com/` header (C8).

**On the Algolia markup.** The `ais-SearchBox` / `#inc-algolia-search-box` markup on inc42.com fires no Algolia request — but calling it "dead leftover" is too soft. It is the *intended* article-search implementation, left half-wired: the config global and both libraries are missing, so the results container never populates. That is the direct cause of article search returning nothing (C7). The only live Algolia call on the site is an unrelated hardcoded glossary lookup (`wp_posts_glossary`, app `VZW3KNFV02`).

---

## 2. Finding 1 — the app's zeros are mostly not real

**The same query returns different answers seconds apart.**

| Scope | Repeated identical queries | Flipped between 0 and >0 |
|---|---|---|
| Articles | 12 | **75.0%** |
| Companies | 91 | **57.1%** |

One real user, 25 Aug, 13 seconds, hunting Shiprocket:

| Time | Query | Results |
|---|---|---|
| 17:51:59 | `ship` | 5 |
| 17:52:02 | `shipr` | 5 |
| 17:52:04 | `shipro` | **0** |
| 17:52:06 | `shipr` | **0** ← returned 5 four seconds earlier |
| 17:52:06 | `ship` | **0** ← returned 5 seven seconds earlier |
| 17:52:12 | `ship roc` | **0** |

Inc42 has 522 articles matching "shiprocket". He gave up.

**Mechanism.** `search_performed` fires on every keystroke, so every character is a live API call. The backing API rate-limits by IP, and failed responses are rendered as "no results".

Zero-result rate by typing speed, **holding query length constant**:

| Query length | Typed fast (<400ms gap) | Typed slowly (>1500ms) | Ratio |
|---|---|---|---|
| 4 chars | **81.8%** (n=22) | 9.1% (n=77) | **9.0×** |
| 5 chars | 36.7% (n=30) | 18.0% (n=50) | 2.0× |
| 6 chars | 34.4% (n=32) | 14.6% (n=48) | 2.4× |
| 7 chars | 42.9% (n=28) | 30.8% (n=26) | 1.4× |
| 8 chars | 48.0% (n=25) | 37.5% (n=24) | 1.3× |

(9+ chars has n=3–12 and is noise.)

**The rate-limit penalty is a long IP lockout, not a throttle.** A burst of 25 back-to-back requests returned 25× HTTP 429; afterwards **every** endpoint on `datalabs-api.inc42.com` — `global-search`, `new-search`, `company/factsheet`, `company/tooltip`, GET and POST — was refused from that IP for **over 30 minutes continuously**, including from an ordinary Chrome session. During the lockout the DataLabs company list renders empty.

That is the real severity: one user typing fast can take down **every DataLabs-powered surface** for everyone sharing that IP — office wifi, campus, carrier NAT — and every one of them sees "no results" rather than an error.

*Caveat, stated plainly: I induced this lockout with deliberately abnormal parallel load. The thresholds are not the app's normal traffic shape. What is verified is the behaviour — host-wide, long-lived, and silent to the user.*

---

## 3. Finding 2 — multi-word queries collapse (DataLabs entity search)

Tokens are OR'd with no phrase boost and no minimum-match, so the result cap fills with noise. Measured over 716 entity names extracted from 300 recent Inc42 articles:

| Tokens in query | hit@1 | Queries saturating the 20-row cap |
|---|---|---|
| 1 | 20% | 49% |
| 2 | **4%** | 96% |
| 3 | **0%** | 98% |

| Query | What comes back | Correct answer |
|---|---|---|
| `lava mobile` | Vaca Mobiles, Celeckt Mobiles, Celkon Mobiles… | Lava — **absent from all 20 rows** |
| `iifl finance` | IIFL Securities, IFL Housing Finance, IIFL Seed Ventures… | IIFL Finance — **absent** |
| `wagh bakri` | Wagr, Waghela Infotech, Badri group… (50 rows) | Wagh Bakri — **absent** |
| `air bound` | Future Bound Tech, Beyond The Bounds, Airbound (rank 3) | demoted below noise |

The API never returns nothing for these. It returns **20 confidently wrong rows**.

**What does work:** exact names. 50 entities were extracted from articles and independently confirmed present in DataLabs via the factsheet API — **48 of 50 return at rank 1**. Single-token typos on long names work (`zomatoo`, `zomto` → Zomato rank 1).

**What does not:** run-together words. `wagh bakri` → 50 rows, `waghbakri` → **0**. Same for `tbotek` (vs `tbo tek` which works) and `myjar`.

---

## 4. Finding 3 — the article **REST API** has recall but no precision

> **Read this section as API behaviour, not user experience.** Everything below measures `wp-json/wp/v2/posts?search=` — a path **no user reaches**. The user-facing article search on inc42.com returns *nothing at all* (**C7**). These numbers matter for what a replacement must beat, and they describe the corpus honestly; they do not describe what a reader currently sees.
>
> **Re-measured 6 Sep:** p50 **3,899ms** (was ~5,000ms), `EMS` → **16,717**, `chai` → **12,949**, `cred` → **10,811**, `myjar` → **0**. One new defect: date-ordering plus a continuously-updated article means **8 of 10 test queries now return "Indian Startup IPO Tracker 2026" as the top hit** — including `EMS`, `chai`, `cred`, `Zomato`, `shipr` and `how much did zomato raise`.

WordPress `LIKE '%term%'` matches substrings **inside words**, and orders by date. Measured across 45 queries (30 Aug):

| Query | Articles returned | Top hit | Problem |
|---|---|---|---|
| `EMS` | **16,860** | "After OpenAI, Anthropic Says Claude…" | matches syst**ems**, it**ems**, probl**ems** |
| `chai` | **13,110** | "Sunil Mittal To Step Down As Airtel Payments Bank **Chai**rman" | matches **chai**n, **chai**rman |
| `Accel` | **9,419** | "EV Manufacturer Omega Seiki Raises…" | matches **accel**erate, **accel**erator |
| `of business` | **32,637** | — | no phrase handling |
| `shipr` | 534 | "New-Age Tech Stocks See Mixed Week" | Shiprocket not first — date order, not relevance |
| `how much did zomato raise` | 311 | "AI Startup TrueFan Raises $10 Mn…" | question queries return noise |
| `Kimberly` | 12 | "Meesho Trims Q1 Loss 54% YoY" | person queries hit body text |

**Latency: p50 ≈ 5.0 seconds** (range 4.3–6.0s) across all 45 queries. Every article search on Inc42 Media takes five seconds.

**No typo tolerance at all:** `myjar`, `birdeye`, `tbotek`, `humgerb`, `taga motors`, `trancxn`, `wheelse6wll` → 0 results each.

**No alias handling.** Zomato renamed to Eternal Ltd — `Zomato` returns 4,695 articles, `Eternal Limited` returns 115. Adding a legal suffix destroys recall: `Zepto` → 1,400, `Zepto Pvt Ltd` → **39**.

**Inc42's own IP is not findable.** `Decode` returns 388 articles, none of them about Inc42's Decode product.

---

## 5. Finding 4 — search intent is thematic, the engine is entity-only

This is the cross-surface pattern, and it is the biggest product gap.

**DataLabs web — 5,913 searches by 686 users in 30 days.** The single most common query is **`fintech` (22 searches, 15 distinct users)**. Also in the top 70: `ai startups` (9 users), `series a` (8 users), `health` (8 users), `unicorns`, `solar`, `venture`.

**App — the strongest cluster is cleantech/deeptech themes:** `green hydrogen`, `carbon credit`, `deepfake`, `pharmaceutical`, `semiconductor`, `BESS`, `defence`, `EMS`.

Entity search matches on **name only**. Every one of these returns nothing useful — while Inc42 Media has 134 articles on green hydrogen, 159 on carbon credits, 765 on pharmaceutical, 927 on semiconductors, 4,411 on quick commerce.

The demand is for a **topic and filter** experience. The engine only does name lookup.

**Also unmeasurable:** DataLabs `Search Completed` carries `Search Query`, `Search Source`, `Search Type` — and **no result count and no latency**. 5,913 searches a month with zero visibility into how many failed. The app at least has `result_count`; it has no `latency_ms` or `http_status`.

---

## 5b. Replay of real user queries — what actually breaks

57 of the most-searched real DataLabs web queries (last 30d) were replayed against the live entity API, plus 31 targeted cross-POV probes. Latency at polite pacing: **p50 398ms, p90 504ms**.

**Only 1 of 57 returned nothing.** Hard zeros are rare on this endpoint — the failure mode is wrong answers, not empty ones.

### Genuine index gaps — companies that simply are not there

| Query | Searches / users (30d) | Result |
|---|---|---|
| `brewnexa technologies` | **20 / 1 user** | Technologies33, Atishrri Technologiess… Brewnexa absent; even the bare token `brewnexa` returns only "Brewex" |
| `hustle hard ventures` | **14 / 1 user** | Hustleio, Hustlezy, Hustle Cowork — absent |
| `emerging ledger` | **13 / 1 user** | LEDGERS, Emerging Five, Emerging Coders — absent |
| `alphavector` | **11 / 1 user** | **0 rows** — the only hard zero in the set |

**58 searches from 4 users chasing companies that are not in the database.** This is the web equivalent of the `shipr` rage-loop, and it is the one place where "add missing content" is genuinely the fix.

### Legal names are separate records, not aliases — 0 of 4 resolve

| Query | Returns | Should resolve to |
|---|---|---|
| `Kiranakart` | "Kiranakart" — exists as its **own unlinked company record** | Zepto |
| `Eternal Limited` | Eternal Capital | Zomato (its actual current legal name) |
| `Bundl Technologies` | Template Bundle | Swiggy |
| `ANI Technologies` | Animeria Technologies | Ola |

### Topic queries return name-substring noise, confirming there is no sector field in the match

| Query | Top 3 |
|---|---|
| `fintech` | MyLead FinTech, Spay Fintech, Fintech Magic |
| `ai startups` | Legal Startups, Sandbox Startups, Unboxing Startups |
| `series a` | SeriesX Marketing, BEV Series, A3 Services |
| `unicorns` | Technovation Unicorns, Unicornus Maximus, Unicorn Mark |
| `green hydrogen` | Hydrogen Gentech |

It is matching the *word* in company names. It is not matching the *sector*.

### Correction — person search is not broken; the client is

An earlier read of this data suggested person search was failing. It is not. The API returns people correctly, at rank 1 of their own array:

| Query | `person` array, position 1 |
|---|---|
| `aman gupta` | **Aman Gupta** |
| `tanmay bhat` | **Tanmay Bhat** |
| `deepinder goyal` | **Deepinder Goyal** |

The defect is **presentation**: the response is 20 companies + 10 people + 20 investors, and `main.min.js` **flattens and re-sorts all three into one list**. So a user searching a person's name sees up to 20 irrelevant companies before the correct person. Typed results exist; the client throws the typing away.

This strengthens §9.4 — return typed groups and render them as groups. Do not flatten.

### Data quality: duplicate person records

`aman gupta` returns **"Aman Gupta" four times**; `deepinder goyal` returns "Deepinder Goyal" twice. The person table has duplicates, which also consume the 10-row cap.

### Ranking defects visible in real queries

| Query | Problem |
|---|---|
| `ultravio` | "Hosting Ultraso" ranks **above** "Ultraviolette Automotive" — prefix match loses to a typo match |
| `sugar` | SUGAR Cosmetics only rank 3, behind Sugar Watchers and Orange Sugar |
| `apax` | Apex, Appx, Apex — typo-matched away from Apax Partners |
| `vip` | Vipralok, VipraLabs — VIP Industries absent |
| `inox` | Maruti Inox, Inox Importers — INOX absent |

Rule 2 in §9.3 (exact > prefix > token > typo) fixes all five.

---

## 6. Scale

| Metric | App | DataLabs web |
|---|---|---|
| Searches (30d) | 190 completed intents | 5,913 |
| Users searching | 61 of 717 (8.5%) | 686 |
| **Users hitting a zero result** | **29 — 47.5% of searchers** | **unmeasurable** |
| Zero-result rate, companies | 19.7% | unmeasurable |
| Zero-result rate, articles | 35.8% (was 27.0% on 23 Aug — worsening) | unmeasurable |

Honest note on impact: zero results do **not** cause immediate abandonment — 87.0% of users engage with content within 5 minutes afterwards, vs 94.4% after a successful search. The cost is wasted effort, a retry loop (200 retries in the period), and eroded trust — not an immediate exit.

---

## 7. Root causes, ranked

Re-ranked 6 Sep. The two new entries at the top (#0, #1) were both invisible to every prior version of this document.

| # | Cause | Surface | Evidence |
|---|---|---|---|
| **0** | **Article search renders nothing.** The Algolia InstantSearch path is half-wired — config global and both libraries missing — so `#inc-algolia-hits` never populates | **inc42.com** | Empty results container for `cred`, `zomato`, `fintech`, `startup`, `funding`; `main.min.js` has 13 algolia refs, all UI-only (**C7**) |
| **1** | **No exact-match boost and no relevance floor.** The exact entity loses to 175 substring competitors and never surfaces | **DataLabs (v2)** | `cred` → CRED absent despite `C-2623` existing; `ola`/`navi` → rank 3 behind noise (**C5**) — *this is Ranjith's reported symptom, both halves of it* |
| 2 | Per-keystroke requests resolve out of order; a stale response overwrites a good one and renders as "0 results" | App | 57–75% non-determinism on identical repeated queries; `shipr → 5 → 0` observed directly. Server confirmed deterministic (**C6**) |
| 3 | **v2 matches the whole query as one exact phrase with no recall fallback**, so multi-word and run-together queries return 0 | DataLabs | `iifl finance`, `wagh bakri`, `lava mobile`, `matter motor` → 0; 15/30 hard zeros on the regression set (**C4**) |
| 4 | Multi-word queries OR-match and flood the result cap | v1 entity search | hit@1 20% → 4% → 0% |
| 5 | **v2 is 4× slower than v1** — 1,558ms p50 vs 390ms — so it cannot serve typeahead as-is | DataLabs | 30-query measurement, p90 1,741ms, max 3,347ms (**C4**) |
| 6 | Article REST API is `LIKE` with no word boundaries, no relevance, ~4s latency; date-ordering lets one evergreen article top nearly every query | Inc42 Media API | `EMS` → 16,717; `chai` → 12,949; IPO Tracker tops 8/10 queries |
| 7 | No topic/sector/tag search on v1 or the app | v1, app | `fintech` is the #1 web query; v2 already solves this |
| 8 | No aliases, no run-together handling | All | `Eternal Limited`, `waghbakri`, `tbotek` |
| 9 | Search quality is unmeasurable | DataLabs, app | no result count on DataLabs; no latency anywhere |
| 10 | Genuine index gaps | Entity search | Brewnexa, Hustle Hard Ventures, Emerging Ledger, Alphavector — 58 searches, 4 users |
| 11 | Client flattens typed results, burying people behind 20 companies | Web (v1) | `main.min.js` merges companies+people+investors into one list |
| 12 | Duplicate person records consume the result cap | DataLabs data | "Aman Gupta" ×4, "Deepinder Goyal" ×2 |

Note the ordering. The 23 Aug diagnosis started at #10. The 30 Aug version started at #2 and never saw #0 or #1 — because both are only visible if you drive the actual product rather than the APIs behind it.

---

## 8. The next fix — do this first

**Ship Stage 0 this week. It is client-side only, needs no backend change, and addresses root cause #1.**

| Fix | Detail | Effort |
|---|---|---|
| Debounce 350ms + cancel in-flight requests | One request per settled query instead of one per keystroke. Fixes the flooding **and** the 3× search-metric inflation in one change | S |
| Stop rendering failures as "0 results" | Distinguish `empty` from `timeout` / `429` / network error. Show a retry state | S |
| Minimum 3 characters before firing | Matches what the website already does | XS |
| Client cache of the last ~20 queries | Backspacing reads the cache instead of re-querying | S |
| Add `latency_ms`, `http_status`, `error_type` to `search_performed`; fire once per completed intent | Until this lands, none of the above is verifiable | S |
| Add `Result Count` + `Latency` to DataLabs `Search Completed` | 5,913 searches/month currently invisible | S |

**Expected effect:** if the non-determinism analysis is right, this alone removes a large share of the 19.7% / 35.8% zero rates — because those searches were never really zero. It also tells you what the *true* zero rate is, which is what Stages 1–2 should be scoped against.

**Do not skip the instrumentation.** Right now nobody can prove whether a fix worked.

> **Reconfirmed 6 Sep.** The backend is deterministic under repeated identical queries (**C6**), so the flip-flop is unambiguously client-side. Stage 0 remains the correct first ship and needs no re-scoping.
>
> **But it is no longer the *only* "do this first".** Root cause #0 — inc42.com article search rendering nothing — is a separate, larger, and probably smaller-effort fix. It should be triaged in parallel, not queued behind Stage 0. See §8b.

### 8b. Root cause #0 — restore article search on inc42.com

Triage first, then pick one of three; effort depends entirely on why the Algolia wiring is missing.

| Step | Detail |
|---|---|
| **Confirm** | Load `inc42.com/?s=cred` in a browser with devtools open. Expect: no request to `*.algolia.net` for the results list, and an empty `#inc-algolia-hits`. **Do this before anything else** — the whole finding rests on it |
| **Then diagnose** | Was the WP Algolia plugin deactivated, did indexing lapse, or was the config global dropped in a theme deploy? The `?ver=21.94` theme bundle still ships the search JS, so this looks like a config/plugin regression rather than an intentional removal |
| **Option A — re-wire Algolia** | If the plugin and index still exist, this is a settings fix, not a build. Fastest path back to working article search |
| **Option B — point it at an existing engine** | Reuse whatever the app/DataLabs settle on, so there is one article index rather than two |
| **Option C — ship the §9.2–9.7 design** | The right long-term answer regardless; do not let it block A |

**Whichever option, add a zero-result state (§9.8) and fire a `search_no_results` event.** Article search has been returning nothing for an unknown period and nobody detected it — that is the real lesson of #0, and instrumentation is what prevents the repeat.

### Stage 0b — three more fixes that need no search engine

| Fix | Detail | Effort |
|---|---|---|
| **Stop flattening typed results** | `main.min.js` merges companies + people + investors into one sorted list, burying the correct person behind 20 companies. Render the three arrays as three labelled groups. The API already returns them typed | S |
| **Add the 4 known missing companies** | Brewnexa, Hustle Hard Ventures, Emerging Ledger, Alphavector — 58 searches from 4 users chasing records that do not exist | XS |
| **De-duplicate the person table** | "Aman Gupta" appears 4×, "Deepinder Goyal" 2×; duplicates eat the 10-row cap | S |

### Stage 0c — alias table, ~200 rows, no engine required

Even on the current API, a lookup table mapping legal and former names to the canonical entity would fix an entire failure class: Kiranakart → Zepto, Eternal Limited → Zomato, Bundl Technologies → Swiggy, ANI Technologies → Ola, Lava International → Lava, Jar → MyJar. Seed from the DataLabs legal-name field; hand-curate the top 200 brands.

---

## 9. Revised approach — **fix v2's retrieval first; migrate only once it beats v1**

**Rewritten twice: after C1 (30 Aug), and again after C4–C7 (6 Sep).** The 30 Aug version said: v2 is the good engine, migrate everything onto it, and its only defect is tokenisation. The 6 Sep measurements do not support that. v2 has the better *architecture* but **worse retrieval than v1** — 50% hard zeros, no exact-match boost, and 4× the latency. Migrating as-is would break `cred` on the main site, where it works today.

The revised stance: **fix v2's retrieval first, migrate only once it beats v1 on a regression set, and treat article search as a separate and more urgent track.**

### 9.0 The actual plan, in order

**Track A — restore what is broken (do now, independent of everything else)**

| # | Fix | Why | Effort |
|---|---|---|---|
| A1 | **Confirm and fix inc42.com article search (§8b)** | Root cause #0. Article search currently returns nothing for every query on a media site | **Triage XS; fix S–M** |
| A2 | **Client debounce + cancel in-flight + real error states (Stage 0, §8)** | Root cause #2. Backend confirmed deterministic, so this is the whole fix | S |
| A3 | **Instrument everything** — `latency_ms`, `http_status`, `error_type`, `result_count`, one event per completed intent | Nothing below is verifiable without it, and #0 went undetected for want of it | S |

**Track B — fix v2's retrieval (must land before any migration)**

| # | Fix | Why | Effort |
|---|---|---|---|
| B1 | **Exact-match boost + relevance floor** | Root cause #1 — **Ranjith's reported symptom, both halves**. `cred` → CRED, `ola` → Ola, and stop padding the cap with 175 substring matches. Rule: exact > prefix > token > typo, and drop rows below a match threshold | **S — highest value in this document** |
| B2 | **Tokenise the query** instead of passing the whole string as one `company_search` value | Fixes `iifl finance`, `wagh bakri`, `lava mobile`, `matter motor`, `third wave`. AND across tokens, then fall back to the best single-token match rather than to nothing | S |
| B3 | **Recall fallback** — never return 0 when a relaxed match exists | 15/30 hard zeros incl. single tokens (`apax`, `birdeye`, `speciale`, `ultravio`, `youtube`) that v1 answers | S |
| B4 | **Add a `name_squash` field** (lowercased, spaces and punctuation stripped) | Fixes `tbotek`, `waghbakri`, `ofbusiness` | S |
| B5 | **Get v2 under 500ms p95** | At 1,558ms p50 it cannot back a typeahead. This is a **gate**, not a nice-to-have | M |
| B6 | Alias table (Kiranakart→Zepto, Eternal→Zomato, Bundl→Swiggy, ANI→Ola) | Fixes the legal-name class | S |

**Track C — consolidate (gated on Track B passing the regression set)**

| # | Fix | Gate | Effort |
|---|---|---|---|
| C1 | Migrate inc42.com header search from v1 to v2 | **Only after v2 beats v1 on Appendix A + B.** Today it would regress `cred`, `ola`, `navi`, `speciale`, `apax` | M |
| C2 | Point the app at v2 | Same gate | M |
| C3 | Surface `did_you_mean` and `applied_filters` in the UI | None — v2 returns them today and no surface renders them. `zomto` → "Showing results for **zomato**"; `fintech` → a sector chip, not a list | S |
| C4 | Replace the article engine properly (§9.2–9.7) | After A1 restores service | L |

The ordering change that matters: **B1 was not in the 30 Aug plan at all**, and it is the fix for the symptom Ranjith actually reported. **A1 was not in any plan**, and it is the most severe defect found.

### 9.1 On replacing the engine — now a genuine decision, not a settled one

The 30 Aug version said "do not start here" on the grounds that v2 already does the hard parts. That is weaker now: **v2 fails 50% of the regression set and is 4× slower than the engine it was meant to replace.** "Fix v2" is no longer self-evidently cheaper than "stand up Typesense" — it depends on facts not visible from outside, namely why v2 is slow and how its matching is implemented.

Decide with engineering, on two questions:

| Question | If the answer is… | Then |
|---|---|---|
| Is v2's 1.5s latency structural (per-query fan-out, N+1 enrichment) or incidental (cold cache, no index)? | incidental | fix v2 — Track B is days |
| Is the matcher a tunable engine (Elastic/OpenSearch) or hand-rolled SQL? | hand-rolled SQL | B1–B3 are a rewrite; a dedicated engine is likely cheaper and better |

At this corpus size — ~75K companies + 55,562 articles — Typesense or Meilisearch serve sub-50ms, and the schema and query plan in §9.2–9.7 stand ready either way. **Article search needs new infrastructure regardless** (root cause #0 and #6): once A1 restores service, the `LIKE`-based REST path at ~4s cannot be tuned into a search engine.

### 9.2 Reference index schema (for article search, and for entity search if Track B proves insufficient)

### 9.3 Engine

**Recommend Typesense** (or Meilisearch). Both give typo tolerance, prefix matching, synonyms, faceting and field weighting as configuration rather than code, and serve sub-50ms at this corpus size. Azure AI Search is capable but the Azure credits (₹16.84L) run dry around 11 Oct 2026 — a poor home for a permanent dependency. Algolia is the zero-ops option if hosting is unwelcome; the site already has dead Algolia markup, so someone once started this.

### 9.4 Index schema

```
collection: inc42_search
  id            string
  type          enum[company, person, investor, article]   # facet
  name          string    # display name / headline
  name_squash   string    # lowercased, punctuation+spaces stripped -> "tbotek", "waghbakri"
  aliases       string[]  # legal name, former name, ticker, common abbreviations
  sectors       string[]  # facet - "fintech", "cleantech", "quick commerce"
  tags          string[]  # facet - article tags, company tags
  city          string    # facet
  stage         string    # facet - "series a", "seed"
  body          string    # article excerpt + body; company description
  published_at  int64     # sort/recency only, NEVER the primary order
  popularity    float     # funding raised, pageviews - the tiebreaker
```

### 9.5 Query plan

```
query_by         : name, aliases, name_squash, sectors, tags, body
query_by_weights : 10,   8,       8,           5,       4,    1
num_typos        : 0 for tokens <4 chars; 1 for 4-7; 2 for 8+
typo_tokens_threshold : 1     # only fall back to typo matching if exact finds nothing
prefix           : true on the last token only
drop_tokens_threshold : 0     # DO NOT silently drop tokens - this is what causes "lava mobile"
min_len_1typo=4, min_len_2typo=8
sort_by          : _text_match:desc, popularity:desc
```

The three rules that fix the observed failures:

1. **AND across tokens.** All tokens must match. Only if that yields nothing, retry with OR — and label those results "Related", visually separated. This alone fixes `lava mobile`, `iifl finance`, `matter motor`, `third wave`.
2. **Exact > prefix > token > typo, always.** A typo-neighbour must never outrank an exact prefix. `shipr` returns Shiprocket first, not a stocks roundup.
3. **Relevance floor — stop padding.** Drop rows below a `_text_match` threshold instead of filling to 20/25. Three right answers beat twenty wrong ones. This is what turns "20 confidently wrong rows" into an honest "no match — did you mean…".

Also: **word-boundary tokenisation** kills the `EMS` → 16,860 and `chai` → 13,110 problem outright, because `chai` stops matching `chairman`.

### 9.6 Response shape

```json
{ "query": "fintech",
  "groups": [
    {"type":"sector",   "total": 1,    "items":[{"name":"Fintech","companies":4210,"deeplink":"/companies?sector=fintech"}]},
    {"type":"company",  "total": 4210, "items":[ ...top 5... ]},
    {"type":"article",  "total": 765,  "items":[ ...top 5... ]},
    {"type":"investor", "total": 88,   "items":[ ...top 3... ]}
  ],
  "did_you_mean": null,
  "took_ms": 31 }
```

Typed groups solve two problems at once: the app stops needing separate Companies/Articles tabs that behave differently, and a topic query like `fintech` can resolve to **a filter, not a list** — which is what those 15 users actually wanted.

### 9.7 Ingestion

- Companies / people / investors: nightly full rebuild from the DataLabs DB (75K rows is minutes), plus webhook upserts on edit.
- Articles: WordPress `save_post` hook → upsert. Backfill all 55,562 once.
- Aliases: seed from DataLabs legal-name and former-name fields; hand-curate the top 200 brands. Start with the known misses — Lava International ↔ Lava Mobiles, Zomato ↔ Eternal, TBO Tek, IIFL Finance, Jar ↔ MyJar, Wagh Bakri.

### 9.8 Zero-result state — never a blank screen

- "Did you mean **X**?" from the top typo candidate
- Cross-type hint: "No articles — but 3 companies match"
- Trending / recently viewed as fallback
- Fire `search_no_results` with the query, so the gap list stays live instead of needing another manual audit

### 9.9 Rollout

Re-sequenced 6 Sep around Tracks A/B/C (§9.0). Stages 0 and 0a run in parallel — they touch different surfaces and neither blocks the other.

| Stage | Scope | Risk |
|---|---|---|
| **0a** | **Confirm root cause #0 in a browser, then restore inc42.com article search (§8b, Track A1)** | None to confirm; **highest user impact of anything here** |
| 0 | Client-side debounce, cancel in-flight, real error states, instrumentation (§8, Track A2–A3) | None — ship now |
| **1** | **Fix v2 retrieval: exact-match boost + relevance floor, then tokenisation, recall fallback, `name_squash` (Track B1–B4).** Re-run Appendix A + B after each | Low — server-side, behind the existing endpoint |
| **1a** | **Get v2 to p95 < 500ms (Track B5).** Gate for anything downstream | Low |
| 2 | Ship v2 behind a feature flag to the app's Explore search. Compare zero-rate and tap-through against control | Low |
| **3** | **Move inc42.com header search onto v2 — only once v2 beats v1 on the regression set.** Retire the browser-side `includes()` re-sort at the same time (it is load-bearing on v1; removing it earlier makes v1 worse — see C1) | Medium |
| 4 | Replace the article engine properly (§9.2–9.7); retire the WordPress `LIKE` path | Medium |

If Track B stalls — because v2's matcher turns out to be hand-rolled SQL or its latency is structural (§9.1) — Stage 1 becomes "stand up Typesense, index companies + articles, run the regression set offline, compare side by side, do not ship yet," and Stages 2–4 proceed against that instead. The schema and query plan in §9.2–9.7 are written for exactly that fallback.

---

## 10. Acceptance criteria

| Target | Threshold | Today (6 Sep) |
|---|---|---|
| **inc42.com article search returns results** | any non-empty result set for a valid query | **returns nothing, every query** |
| **Exact-name query returns that entity at rank 1** | 100% for the 50 verified entities | v2 fails `cred`, `ola` (r3), `navi` (r3), `sugar`, `vip`, `inox` |
| **Hard-zero rate on the Appendix A+B regression set** | < 5% | **v2 50%**, v1 7% |
| Determinism — same query, same result count | 100% | server ✅, client ❌ |
| Zero-result rate, companies | < 8% | 19.7% (app) |
| Zero-result rate, articles | < 12% | 35.8% (app); 100% (web) |
| **Entity search latency** | **p95 < 500ms** | v1 590ms, **v2 1,741ms** |
| Article search latency | p95 < 500ms | ~4,000ms (REST path) |
| **Article search top hit is query-relevant** | IPO Tracker must not top unrelated queries | tops **8 of 10** |
| Topic queries resolve | `fintech`, `green hydrogen`, `ai startups`, `series a` each return a sector/filter result | v2 ✅, v1 ❌, app ❌ |
| `search_performed` | Exactly one event per completed intent, with `latency_ms` and `http_status` | fires per keystroke, neither property |
| DataLabs `Search Completed` | Carries result count and latency | carries neither |
| Regression suite in CI | The 45 real app failures + 57 real web queries + 50 verified entities | none |

---

## 11. Open question for engineering

**Which endpoint and index does the app actually call?** Unconfirmed from outside. The evidence says it is *not* `/header/global-search`: that endpoint returns correct rank-1 answers for `airbound`, `ofbusiness` and `speciale`, and useful rows for `iifl finance` and `shipr` — all of which the app returned 0 for. The result caps (25 companies / 5 articles, from PostHog `result_count` maxima) point at `/company/new-search` with `size:25` plus something separate for articles.

Ten minutes with Ritvik or Anmol settles it. It changes how much of §9 applies. **Stage 0 is worth shipping either way.**

**Add these to the same conversation (6 Sep):**

| Question | Why it matters |
|---|---|
| Which surfaces are on v2 today? | v2 appears on **no** public page; `/datalabs/` itself uses v1 (**C7c**). "DataLabs uses v2" needs narrowing to the logged-in app |
| When did inc42.com article search stop returning results, and why? | Root cause #0. Plugin deactivated, index lapsed, or config dropped in a theme deploy? Determines whether A1 is a settings fix or a build |
| Is v2's 1.5s latency structural or incidental? | Gates the fix-vs-replace decision in §9.1 |
| Is v2's matcher a tunable engine or hand-rolled SQL? | Determines whether B1–B3 are config or a rewrite |

---

## Appendix A — regression set, real app failures (11–30 Aug), **with 6 Sep baseline**

Measured 6 Sep. `n` = rows returned. This is the pass/fail baseline for Track B.

| Query | v2 `n` | v2 top 3 | v1 `n` | v1 top 3 | Verdict |
|---|---|---|---|---|---|
| `air bound` | **0** | — | 20 | Future Bound Tech, Beyond The Bounds, **Airbound** | v2 zero, v1 buries it |
| `airbound` | 1 | **Airbound** | 11 | Airbound, Airborne, Abound | **v2 correct** |
| `birdeye` | **0** | — | 2 | ThirdEye AI, BigEye Global | both wrong |
| `carbon credit` | 15 | CreditQ, Carbon Black, Carlton D'Silva | — | — | topic query, entity engine |
| `enrission` | **0** | — | 7 | ENVISION INTELLIGENCE, Envision Professionals | both wrong |
| `green hydrogen` | 2 | Energy Generation, Renewable Energy Solutions *(sector)* | 20 | Hydrogen Gentech | **v2 resolves the topic** |
| `iifl finance` | **0** | — | 20 | IIFL Securities, IFL Housing Finance | both wrong |
| `indiesemi` | **0** | — | **0** | — | genuine gap |
| `lava mobile` | **0** | — | 20 | Vaca Mobiles, Celeckt Mobiles | both wrong |
| `matter motor` | **0** | — | 20 | **Matter**, Matters, Thinking Matter | **v1 correct at r1** |
| `speciale` | **0** | — | 12 | **Speciale Invest**, Rajasthani Special | **v1 correct at r1** |
| `taga motors` | **0** | — | 20 | **Tata Motors**, IBRIDO MOTORS | **v1 typo-corrects** |
| `tbotek` | **0** | — | 7 | JBTEK, Design Totke | both wrong — needs `name_squash` |
| `tenacious bee collective` | **0** | — | 20 | Bey Bee, Ekatra Collective | both wrong |
| `third wave` | 1 | **Third Wave Coffee** | — | — | **v2 correct** |
| `trancxn` | **0** | — | 10 | **Tracxn**, TraiCon, Tracxn labs | **v1 typo-corrects** |
| `youtube` | **0** | — | 2 | Swaps Couture, Aagaman Couture | both wrong |

**v2 hard zeros: 15/30 across this table and Appendix B's sample (50%). v1 hard zeros: 1/15.** v1 answers correctly at rank 1 for `matter motor`, `speciale`, `taga motors`, `trancxn` — all of which v2 returns nothing for. This is the evidence behind the Track C migration gate.

Not re-tested (low-signal typo fragments): `aitmc veb`, `evigway`, `evigwayp0`, `humgerb`, `snit hch`, `snit hll`, `suto`, `taga motos`, `tell m`, `tenacious bee collr`.

**Original list, companies:** `air bound`, `airbound`, `aitmc veb`, `birdeye`, `carbon credit`, `enrission`, `evigway`, `evigwayp0`, `green hydrogen`, `humgerb`, `iifl finance`, `indiesemi`, `lava mobile`, `matter motor`, `snit hch`, `snit hll`, `speciale`, `suto`, `taga motors`, `taga motos`, `tbotek`, `tell m`, `tenacious bee collective`, `tenacious bee collr`, `third wave`, `trancxn`, `youtube`

**Articles:** `bandma`, `deepfake`, `enrission`, `harsh deodhar`, `kenvue`, `kimberly`, `lava international`, `myjar`, `ofbusiness`, `pharmaceutical`, `review.inc42@gmail.com`, `ship roc`, `shipr`, `shipro`, `tenacious bee collective`, `transxcn`, `wheelse6wll`, `wheelsey3`, `zulu`

## Appendix B — real DataLabs web queries (top 30d) to regression-test

`fintech`, `brewnexa technologies`, `hustle hard ventures`, `emerging ledger`, `ola`, `aman gupta`, `snabbit`, `alphavector`, `ai startups`, `river`, `ultra`, `alpha`, `simple energy`, `health`, `ampere`, `urban`, `series a`, `centricity`, `acko`, `flipkart`, `licious`, `safari`, `simple`, `bgauss`, `navi`, `matter`, `whistledrive`, `ultraviolette`, `zepto`, `tanmay bhat`, `solar`, `beanly`, `neysa`, `money view`, `cred`, `yubi`, `rapido`, `plum`, `zomato`, `rainmatter`, `ultravio`, `vip`, `inox`, `apax`, `sugar`, `yes madam`, `homerun`, `solarsquare`, `phonepe`, `burger`, `simple ener`, `venture`, `moengage`, `zerodha`, `h2loop`, `unicorns`, `swiggy`

Note the shape: partial words (`ultravio`, `simple ener`, `rugr`, `bg`, `pl`), generic nouns (`river`, `sugar`, `burger`, `safari`), people (`aman gupta`, `tanmay bhat`), themes (`fintech`, `ai startups`, `series a`, `unicorns`). Only a minority are clean entity lookups.

### 6 Sep baseline — the exact-match failures that prove root cause #1

| Query | v2 result | v1 result | Correct answer |
|---|---|---|---|
| `cred` | CredR, InCred Holdings, InCred — **CRED absent from 15 rows** | **CRED at rank 1** | CRED (`C-2623`, indexed) |
| `ola` | Manam Chocolate, Prolance, **Ola at r3** | **Ola at rank 1** | Ola |
| `navi` | Navixel, Navigatio Asia, **Navi at r3** | **Navi at rank 1** | Navi |
| `sugar` | Sugar Watchers, Sugar Capital, Sagar A. | Sugar Watchers, Orange Sugar, SUGAR Cosmetics (r3) | SUGAR Cosmetics |
| `vip` | Gaurav Vij, Raman Vig, VIB | Vipralok, VipraLabs, Vipswallet | VIP Industries — **absent from both** |
| `inox` | INOX Renewable Solutions, EQUINOX'S DRONES, Maruti Inox | Maruti Inox, Inox Importers, Artikel Inox | INOX — **absent from both** |
| `apax` | **0** | Apex, Appx, AppX | Apax Partners — **absent from both** |
| `ultravio` | **0** | Hosting Ultraso, Ultraviolette (r2) | Ultraviolette Automotive |
| `zepto` | **Zepto** r1, Zeptoh, Zepto Microwave | — | ✅ |
| `swiggy` | **Swiggy** r1 | — | ✅ |
| `rapido` | **Rapido** r1 | — | ✅ |
| `plum` | **Plum** r1, **Plum** (dupe), Superplum | — | ✅ but duplicated |
| `yubi` | **Yubi** r1 | — | ✅ |
| `aman gupta` | **Aman Gupta** ×6 (all duplicates) | Aman Gupta r1 of `person` | ✅ but 6 dupe records |
| `fintech` | **Fintech (INDUSTRY)** + sector filter | MyLead FinTech, Spay Fintech | **v2 correct** |
| `peak xv` | **Peak XV Partners (INVESTOR)** + portfolio | — | **v2 correct** |
| `zomto` (typo) | **Zomato** + `did_you_mean` | Zomato, TOMTO LEMON | **v2 correct** |

The pattern: **v2 wins on typo, topic and investor-portfolio resolution; v1 wins on exact-name lookup.** Neither is correct on its own. Track B's job is to give v2 v1's exact-match behaviour without losing what v2 already does well.

## Sources

- PostHog [Inc42 App (146258)](https://eu.posthog.com/project/146258) — `search_performed`, 11–30 Aug 2026
- PostHog [Inc42 DataLabs (66351)](https://eu.posthog.com/project/66351) — `Search Completed`, 30 days
- Live APIs: `datalabs-api.inc42.com/header/global-search`, `/header/global-search-v2`, `/company/new-search`, `/inc42/company/factsheet/`
- `https://inc42.com/wp-json/wp/v2/search` and `/posts` (55,562 articles)
- Frontend source: `https://inc42.com/wp-content/themes/inc42/js/main.min.js`
- Prior docs: `app-search-defects.md` (23 Aug), `app-search-root-cause.md` (30 Aug)

**6 Sep revision adds:**

- Live re-test of v1 and v2 over a 30-query set drawn from Appendix A + B — result counts, ranks and latency (p50/p90/max)
- Determinism runs: 6× `green hydrogen`, 8× `shipr` on each engine
- **The real user-facing search pages**, not just the APIs: `https://inc42.com/?s=<query>` for `cred`, `zomato`, `fintech`, `startup`, `funding`; plus `/datalabs/`, `/company/`, `/company/zomato/` to locate v2
- Frontend source: `https://inc42.com/wp-content/themes/inc42/js/src/inc42-algolia-search.js` and the full enqueued-script list of the search page — the evidence for root cause #0
- Probe scripts (session scratchpad): `probe.py` (v1/v2 single queries), `regress.py` (v2 regression + latency), `cmp2.py` (v1-vs-v2 comparison), `art.py` (article REST latency/precision), `rank.py` (`new-search` paging)

**Method note.** Root cause #0 and root cause #1 were both found by driving the product, not the APIs behind it. Every prior version of this document tested endpoints and concluded the engines were roughly working. Future search audits should start from the user-facing surface and work inward.
