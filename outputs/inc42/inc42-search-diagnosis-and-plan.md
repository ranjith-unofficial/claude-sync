# Inc42 Search — Diagnosis & Implementation Plan

**Date:** 30 Aug 2026 · **Scope:** all three search surfaces — the app, Inc42 Media (articles), DataLabs (companies/people/investors)
**Method:** live API replay against ground truth pulled from outside the system (real Inc42 articles, real user queries from PostHog), plus behavioural data from PostHog App (146258) and DataLabs (66351).
**Supersedes:** the coverage-based diagnosis in `app-search-defects.md` (23 Aug) and expands `app-search-root-cause.md` (30 Aug).

---

## 1. What is actually running

There is no single search system. There are three, none of them a search engine.

| Surface | Backend | What it matches on |
|---|---|---|
| Company / person / investor (web + likely app) | `POST datalabs-api.inc42.com/header/global-search` body `{"keyword":"…"}` | Entity **name only**. Returns ≤20 companies + ≤10 people + ≤20 investors |
| Company list + filters | `POST datalabs-api.inc42.com/company/new-search` body `{filter,from,size,sort,sortby,search_url,is_inc42}` | Structured filters |
| Articles (Inc42 Media) | Plain **WordPress** search (`?s=` / `wp-json/wp/v2/search`) | SQL `LIKE '%term%'` over title + body, **ordered by date** |
| Relevance ranking | Done **in the browser** — `main.min.js` re-sorts the response with `name.toLowerCase().includes(query)` then alphabetically | — |

The `ais-SearchBox` / `#inc-algolia-search-box` Algolia markup on inc42.com is dead leftover. No Algolia request fires.

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

## 4. Finding 3 — Inc42 Media article search has recall but no precision

WordPress `LIKE '%term%'` matches substrings **inside words**, and orders by date. Measured across 45 queries:

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

| # | Cause | Surface | Evidence |
|---|---|---|---|
| 1 | Request-per-keystroke floods a rate-limited API; failures render as "0 results" | App | 57–75% non-determinism; 9× zero rate when typing fast |
| 2 | Multi-word queries OR-match and flood the result cap | Entity search | hit@1 20% → 4% → 0% |
| 3 | Article search is `LIKE` with no word boundaries, no relevance, 5s latency | Inc42 Media | `EMS` → 16,860; `chai` → 13,110 |
| 4 | No topic/sector/tag search anywhere | All | `fintech` is the #1 web query |
| 5 | No aliases, no run-together handling | All | `Eternal Limited`, `waghbakri`, `tbotek` |
| 6 | Search quality is unmeasurable | DataLabs, app | no result count on DataLabs; no latency anywhere |
| 7 | Genuine index gaps | Entity search | Brewnexa, Hustle Hard Ventures, Emerging Ledger, Alphavector — 58 searches, 4 users |
| 8 | Client flattens typed results, burying people behind 20 companies | Web | `main.min.js` merges companies+people+investors into one list |
| 9 | Duplicate person records consume the result cap | DataLabs data | "Aman Gupta" ×4, "Deepinder Goyal" ×2 |

Note the ordering. Every prior diagnosis started at #7.

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

### Stage 0b — three more fixes that need no search engine

| Fix | Detail | Effort |
|---|---|---|
| **Stop flattening typed results** | `main.min.js` merges companies + people + investors into one sorted list, burying the correct person behind 20 companies. Render the three arrays as three labelled groups. The API already returns them typed | S |
| **Add the 4 known missing companies** | Brewnexa, Hustle Hard Ventures, Emerging Ledger, Alphavector — 58 searches from 4 users chasing records that do not exist | XS |
| **De-duplicate the person table** | "Aman Gupta" appears 4×, "Deepinder Goyal" 2×; duplicates eat the 10-row cap | S |

### Stage 0c — alias table, ~200 rows, no engine required

Even on the current API, a lookup table mapping legal and former names to the canonical entity would fix an entire failure class: Kiranakart → Zepto, Eternal Limited → Zomato, Bundl Technologies → Swiggy, ANI Technologies → Ola, Lava International → Lava, Jar → MyJar. Seed from the DataLabs legal-name field; hand-curate the top 200 brands.

---

## 9. Revised approach — one index, one endpoint

The three-system split is the structural problem. Companies, people, investors and articles should live in **one index**, served by **one endpoint**, returning **typed, scored** results.

Corpus is small: ~75,000 companies + ~55,562 articles + people + investors. This is a small-index problem, not a big-data one.

### 9.1 Engine

**Recommend Typesense** (or Meilisearch). Both give typo tolerance, prefix matching, synonyms, faceting and field weighting as configuration rather than code, and serve sub-50ms at this corpus size. Azure AI Search is capable but the Azure credits (₹16.84L) run dry around 11 Oct 2026 — a poor home for a permanent dependency. Algolia is the zero-ops option if hosting is unwelcome; the site already has dead Algolia markup, so someone once started this.

### 9.2 Index schema

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

### 9.3 Query plan

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

### 9.4 Response shape

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

### 9.5 Ingestion

- Companies / people / investors: nightly full rebuild from the DataLabs DB (75K rows is minutes), plus webhook upserts on edit.
- Articles: WordPress `save_post` hook → upsert. Backfill all 55,562 once.
- Aliases: seed from DataLabs legal-name and former-name fields; hand-curate the top 200 brands. Start with the known misses — Lava International ↔ Lava Mobiles, Zomato ↔ Eternal, TBO Tek, IIFL Finance, Jar ↔ MyJar, Wagh Bakri.

### 9.6 Zero-result state — never a blank screen

- "Did you mean **X**?" from the top typo candidate
- Cross-type hint: "No articles — but 3 companies match"
- Trending / recently viewed as fallback
- Fire `search_no_results` with the query, so the gap list stays live instead of needing another manual audit

### 9.7 Rollout

| Stage | Scope | Risk |
|---|---|---|
| 0 | Client-side debounce, error states, instrumentation (§8) | None — ship now |
| 1 | Stand up Typesense, index companies + articles, run the regression set offline. Compare against the current API side by side. Do not ship yet | None — read-only |
| 2 | Ship behind a feature flag to the app's Explore search. Compare zero-rate and tap-through against control | Low |
| 3 | Move inc42.com header search and DataLabs global search onto the same endpoint. Retire the WordPress search path and the browser-side `includes()` re-sort | Medium |

---

## 10. Acceptance criteria

| Target | Threshold |
|---|---|
| Determinism — same query, same result count | **100%** |
| Zero-result rate, companies | < 8% |
| Zero-result rate, articles | < 12% |
| End-to-end search latency | p95 < 300ms (today: 580ms entity, ~5,000ms article) |
| Topic queries resolve | `fintech`, `green hydrogen`, `ai startups`, `series a` each return a sector/filter result |
| `search_performed` | Exactly one event per completed intent, with `latency_ms` and `http_status` |
| DataLabs `Search Completed` | Carries result count and latency |
| Regression suite in CI | The 45 real app failures + 57 real web queries + 50 verified entities |

---

## 11. Open question for engineering

**Which endpoint and index does the app actually call?** Unconfirmed from outside. The evidence says it is *not* `/header/global-search`: that endpoint returns correct rank-1 answers for `airbound`, `ofbusiness` and `speciale`, and useful rows for `iifl finance` and `shipr` — all of which the app returned 0 for. The result caps (25 companies / 5 articles, from PostHog `result_count` maxima) point at `/company/new-search` with `size:25` plus something separate for articles.

Ten minutes with Ritvik or Anmol settles it. It changes how much of §9 applies. **Stage 0 is worth shipping either way.**

---

## Appendix A — regression set, real app failures (11–30 Aug)

**Companies:** `air bound`, `airbound`, `aitmc veb`, `birdeye`, `carbon credit`, `enrission`, `evigway`, `evigwayp0`, `green hydrogen`, `humgerb`, `iifl finance`, `indiesemi`, `lava mobile`, `matter motor`, `snit hch`, `snit hll`, `speciale`, `suto`, `taga motors`, `taga motos`, `tbotek`, `tell m`, `tenacious bee collective`, `tenacious bee collr`, `third wave`, `trancxn`, `youtube`

**Articles:** `bandma`, `deepfake`, `enrission`, `harsh deodhar`, `kenvue`, `kimberly`, `lava international`, `myjar`, `ofbusiness`, `pharmaceutical`, `review.inc42@gmail.com`, `ship roc`, `shipr`, `shipro`, `tenacious bee collective`, `transxcn`, `wheelse6wll`, `wheelsey3`, `zulu`

## Appendix B — real DataLabs web queries (top 30d) to regression-test

`fintech`, `brewnexa technologies`, `hustle hard ventures`, `emerging ledger`, `ola`, `aman gupta`, `snabbit`, `alphavector`, `ai startups`, `river`, `ultra`, `alpha`, `simple energy`, `health`, `ampere`, `urban`, `series a`, `centricity`, `acko`, `flipkart`, `licious`, `safari`, `simple`, `bgauss`, `navi`, `matter`, `whistledrive`, `ultraviolette`, `zepto`, `tanmay bhat`, `solar`, `beanly`, `neysa`, `money view`, `cred`, `yubi`, `rapido`, `plum`, `zomato`, `rainmatter`, `ultravio`, `vip`, `inox`, `apax`, `sugar`, `yes madam`, `homerun`, `solarsquare`, `phonepe`, `burger`, `simple ener`, `venture`, `moengage`, `zerodha`, `h2loop`, `unicorns`, `swiggy`

Note the shape: partial words (`ultravio`, `simple ener`, `rugr`, `bg`, `pl`), generic nouns (`river`, `sugar`, `burger`, `safari`), people (`aman gupta`, `tanmay bhat`), themes (`fintech`, `ai startups`, `series a`, `unicorns`). Only a minority are clean entity lookups.

## Sources

- PostHog [Inc42 App (146258)](https://eu.posthog.com/project/146258) — `search_performed`, 11–30 Aug 2026
- PostHog [Inc42 DataLabs (66351)](https://eu.posthog.com/project/66351) — `Search Completed`, 30 days
- Live APIs: `datalabs-api.inc42.com/header/global-search`, `/company/new-search`, `/inc42/company/factsheet/`
- `https://inc42.com/wp-json/wp/v2/search` and `/posts` (55,562 articles)
- Frontend source: `https://inc42.com/wp-content/themes/inc42/js/main.min.js`
- Prior docs: `app-search-defects.md` (23 Aug), `app-search-root-cause.md` (30 Aug)
