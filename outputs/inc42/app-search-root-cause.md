# Inc42 App — Search: Root Cause & Revised Approach

**Investigated:** 30 Aug 2026 · **Method:** live API replay + PostHog behavioural data (11–30 Aug, `@inc42.com` and emulator traffic excluded)
**Supersedes the diagnosis in** `app-search-defects.md` (23 Aug) — that doc blamed index coverage. The dominant cause is different.

---

## Headline

Search is not mainly failing because content is missing. It is failing because **the same query returns different answers seconds apart**.

When a user repeats the exact same query, the result count flips between zero and non-zero:

| Scope | Repeated identical queries | Flipped between 0 and >0 | Share |
|---|---|---|---|
| Articles | 12 | 9 | **75.0%** |
| Companies | 91 | 52 | **57.1%** |

A search index does not behave this way. Dropped, timed-out and rate-limited responses are being rendered as "no results".

### One real user, 13 seconds (25 Aug)

| Time | Query | Results |
|---|---|---|
| 17:51:59 | `ship` | 5 |
| 17:52:02 | `shipr` | 5 |
| 17:52:04 | `shipro` | **0** |
| 17:52:06 | `shipr` | **0** ← same query, 4s earlier returned 5 |
| 17:52:06 | `ship` | **0** ← same query, 7s earlier returned 5 |
| 17:52:07 | `ship r` | 5 |
| 17:52:11 | `ship ro` | 2 |
| 17:52:12 | `ship roc` | **0** |

The user was looking for Shiprocket. Inc42 has 522 articles matching "shiprocket". They gave up.

---

## Evidence that this is request flooding, not missing content

`search_performed` fires **on every keystroke** — so every character typed is a live API call.

**Zero-result rate by how fast the user was typing, holding query length constant:**

| Query length | Typed fast (<400ms gap) | Typed slowly (>1500ms gap) | Ratio |
|---|---|---|---|
| 4 chars | **81.8%** zero (n=22) | 9.1% zero (n=77) | **9.0×** |
| 5 chars | 36.7% (n=30) | 18.0% (n=50) | 2.0× |
| 6 chars | 34.4% (n=32) | 14.6% (n=48) | 2.4× |
| 7 chars | 42.9% (n=28) | 30.8% (n=26) | 1.4× |
| 8 chars | 48.0% (n=25) | 37.5% (n=24) | 1.3× |

Same query length, same content behind it — only the typing speed differs. Rows for 9+ chars have n=3–12 and are noise.

**The backing API rate-limits by IP and the penalty is long-lived.** In testing, a burst of 25 back-to-back requests returned **25× HTTP 429**, after which every request from that IP — including from a normal browser session on the same connection — was refused for **over 20 minutes continuously**. This is not a short cooldown; a client that trips the limit is locked out well beyond a single session. (This block was induced by deliberately abnormal load — but an app firing one request per keystroke, across users sharing office or carrier NAT, is exposed to exactly this.)

---

## Current approach, as actually implemented

| Layer | What it is | Source |
|---|---|---|
| Company / person / investor search | `POST https://datalabs-api.inc42.com/header/global-search` body `{"keyword": "..."}` | `inc42.com/wp-content/themes/inc42/js/main.min.js` |
| Company list + filters | `POST https://datalabs-api.inc42.com/company/new-search` body `{filter:{}, from, size, sort, sortby, search_url, is_inc42}` | same file |
| Article search (website) | Plain WordPress search (`?s=` / `wp-json/wp/v2/search`). The `ais-SearchBox` / `#inc-algolia-search-box` Algolia markup is dead leftover — no Algolia request fires. | live network capture |
| Relevance ordering | Done **in the browser** — JS re-sorts the API response with `name.toLowerCase().includes(query)` then alphabetically | `main.min.js` |

**Observed limits:** `global-search` returns at most 20 companies + 10 people + 20 investors. The app caps at **25 companies / 5 articles** (PostHog `result_count` max).

### What works

- **Exact company names are fine.** 50 entities were extracted from 300 recent Inc42 articles and independently confirmed present in DataLabs via the factsheet API; **48 of 50 return at rank 1**.
- Single-token typos on long distinctive names work: `zomatoo` → Zomato (rank 1), `zomto` → Zomato (rank 1).

### What does not work

**1. Multi-word queries collapse.** Tokens are OR'd with no phrase boost and no minimum-match, so the result cap fills with junk:

| Tokens in query | hit@1 | Queries returning exactly 20 rows (cap saturated) |
|---|---|---|
| 1 | 20% | 49% |
| 2 | **4%** | 96% |
| 3 | **0%** | 98% |

Live examples:

| Query | What comes back | Correct answer |
|---|---|---|
| `lava mobile` | Vaca Mobiles, Celeckt Mobiles, Celkon Mobiles… | Lava — **absent from all 20 rows** |
| `iifl finance` | IIFL Securities, IFL Housing Finance, IIFL Seed Ventures… | IIFL Finance — **absent** |
| `wagh bakri` | Wagr, Waghela Infotech, Badri group… (50 rows) | Wagh Bakri — **absent** |
| `air bound` | Future Bound Tech, Beyond The Bounds, Airbound (rank 3) | demoted below noise |

The API never returns "nothing" for these — it returns **20 confidently wrong rows**.

**2. Run-together words fail.** `wagh bakri` → 50 rows; `waghbakri` → **0**. Same for `tbotek` (vs `tbo tek` → works), `myjar` → 0.

**3. No topic search at all.** Companies match on name only. `green hydrogen`, `carbon credit`, `deepfake`, `pharmaceutical`, `youtube` return nothing useful — despite Inc42 having 134, 159, 185 and 2,291 articles on them respectively.

**4. Article search is raw WordPress.** Measured over 30 queries:

| Property | Measured |
|---|---|
| Latency | **p50 ≈ 5.0s** (range 4.3–5.6s) |
| Ordering | By **date**, not relevance — `shipr` returns 534 matches, top hit is a generic stocks roundup, not Shiprocket |
| Typo tolerance | **None** — `myjar`, `birdeye`, `tbotek`, `humgerb`, `taga motors`, `trancxn`, `wheelse6wll` all return 0 |
| Phrase handling | None — `of business` returns **32,637** results |
| Corpus | 55,562 articles exist; the app returns at most **5** |

**5. Latency of the entity API:** p50 579ms, p90 928ms, p99 1,520ms — measured over 716 live queries.

---

## Scale of the problem

| Metric | Value |
|---|---|
| App users (11–30 Aug) | 717 |
| Users who searched | 61 (8.5%) |
| **Users who hit a zero-result search** | **29 — 47.5% of everyone who searches** |
| Completed search intents | 137 companies, 53 articles |
| Zero-result rate, companies | **19.7%** |
| Zero-result rate, articles | **35.8%** (was 27.0% on 23 Aug — getting worse) |
| Zero-result searches followed by another search attempt | 200 |

Honest note on impact: zero-result searches do **not** cause immediate abandonment — 87.0% of users engage with some content within 5 minutes afterwards, vs 94.4% after a successful search. The cost is wasted effort and eroded trust in the feature, not an immediate exit.

---

## Revised approach

### Stage 1 — Stop the bleeding (client-side only, no backend work)

| Fix | Detail |
|---|---|
| **Debounce 350ms, cancel in-flight requests** | One request per settled query instead of one per keystroke. Fixes the flooding *and* the 3× event inflation in one change. |
| **Never render a failed request as "0 results"** | Distinguish `empty` from `timeout` / `429` / `network error`. Show a retry state, not an empty state. This alone removes most of the 57–75% non-determinism. |
| **Minimum 3 characters before firing** | Matches what the website already does. |
| **Cache the last ~20 queries client-side** | Backspacing re-reads the cache instead of re-querying. |
| **Instrument it** | `search_performed` currently has **no** latency or status property. Add `latency_ms`, `http_status`, `error_type`, and fire once per completed intent. Until this lands, none of the above is verifiable. |

### Stage 2 — Fix query semantics (backend)

| Fix | Detail |
|---|---|
| **AND-first, OR-fallback** | Require all tokens to match. Only fall back to OR when AND returns nothing, and label those results "related". Fixes `lava mobile`, `iifl finance`, `matter motor`, `third wave`. |
| **Rank: exact > prefix > token > fuzzy** | A fuzzy neighbour must never outrank an exact prefix. `shipr` should return Shiprocket first, not a stocks roundup. |
| **Length-scaled fuzziness** | No fuzziness under 4 characters; edit distance 1 for 4–7; 2 for 8+. |
| **Squashed-name index field** | Index names with spaces and punctuation stripped, so `tbotek`, `waghbakri`, `ofbusiness` match. |
| **Relevance floor — stop padding** | Drop low-scoring rows rather than filling to 20/25. Three right answers beat twenty wrong ones. |
| **Move ranking server-side** | Delete the browser-side `includes()` re-sort; the engine should return results already ranked. |

### Stage 3 — Fix coverage

| Fix | Detail |
|---|---|
| **Alias / synonym dictionary** | Legal ↔ brand ↔ former names and tickers: Lava International ↔ Lava Mobiles, TBO Tek, IIFL Finance, Jar ↔ MyJar, Wagh Bakri. |
| **Index sector, industry and tags** | Unlocks topic search — green hydrogen, carbon credit, deepfake, pharmaceutical, defence, EMS, BESS. This is the strongest demand cluster in app search. |
| **Replace WordPress article search** | Index all 55,562 articles — title, excerpt, body, company tags — into the same engine. Removes the 5-second latency and the date-ordering. |
| **One endpoint for both types** | A single `/search` returning typed, scored results. Kill the DataLabs-API / WordPress split so the two tabs stop behaving differently. |

### Engine

Corpus is small — ~75K companies, ~56K articles. Typo tolerance, prefix matching and synonyms are out-of-the-box features in **Typesense** or **Meilisearch** (self-hosted, sub-50ms at this size). Azure AI Search is viable but note the Azure credits (₹16.84L) run dry around 11 Oct 2026, which makes it a risky home for a permanent dependency.

### Zero-result state — never show a blank screen

- "Did you mean **X**?" using the top fuzzy candidate
- Cross-scope hint: "3 companies match — switch to Companies"
- Trending / recently viewed as fallback
- Fire `search_no_results` with the query so the gap list stays live

### Acceptance criteria

| Target | Threshold |
|---|---|
| Determinism | Same query → same result count, **100%** |
| Zero-result rate, companies | < 8% |
| Zero-result rate, articles | < 12% |
| End-to-end search latency | p95 < 300ms |
| `search_performed` | Exactly one event per completed intent, carrying `latency_ms` and `http_status` |
| Regression suite | The 45 real failing queries below + the 50 verified entities, run in CI |

---

## Open question for engineering

I could not confirm from outside **which endpoint and index the app actually calls**. The evidence says it is not `/header/global-search`: that endpoint returns correct rank-1 answers for `airbound`, `ofbusiness`, `speciale` and useful rows for `iifl finance` and `shipr` — all of which the app returned 0 for. The result caps (25 companies / 5 articles) point at `/company/new-search` with `size:25` for companies plus something separate for articles.

**Ten minutes with Ritvik or Anmol resolves this**, and it changes which of Stage 2/3 applies. Stage 1 is worth doing regardless.

---

## Regression set — every query the app returned 0 for (11–30 Aug)

**Companies:** `air bound`, `airbound`, `aitmc veb`, `birdeye`, `carbon credit`, `enrission`, `evigway`, `evigwayp0`, `green hydrogen`, `humgerb`, `iifl finance`, `indiesemi`, `lava mobile`, `matter motor`, `snit hch`, `snit hll`, `speciale`, `suto`, `taga motors`, `taga motos`, `tbotek`, `tell m`, `tenacious bee collective`, `tenacious bee collr`, `third wave`, `trancxn`, `youtube`

**Articles:** `bandma`, `deepfake`, `enrission`, `harsh deodhar`, `kenvue`, `kimberly`, `lava international`, `myjar`, `ofbusiness`, `pharmaceutical`, `review.inc42@gmail.com`, `ship roc`, `shipr`, `shipro`, `tenacious bee collective`, `transxcn`, `wheelse6wll`, `wheelsey3`, `zulu`

## Sources

- PostHog project [Inc42 App (146258)](https://eu.posthog.com/project/146258) — `search_performed`, 11–30 Aug 2026
- Live API: `https://datalabs-api.inc42.com/header/global-search`, `https://datalabs-api.inc42.com/company/new-search`
- Frontend source: `https://inc42.com/wp-content/themes/inc42/js/main.min.js`
- Article corpus: `https://inc42.com/wp-json/wp/v2/posts` (55,562 posts)
- Prior doc: `~/ClaudeDocs/inc42/app-search-defects.md` (23 Aug)
