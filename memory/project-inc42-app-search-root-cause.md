---
name: project-inc42-app-search-root-cause
description: "Inc42 search failure root cause (30 Aug 2026) + Ranjith's open symptoms for the deferred search-performance bucket (4 Sep 2026) — non-determinism from per-keystroke request flooding, not missing content; corrects the 23 Aug index-coverage diagnosis"
metadata: 
  node_type: memory
  type: project
  originSessionId: 300a6e51-1907-4a2e-97de-6fec672f48be
  modified: 2026-09-06T14:59:14.114Z
---

Investigated 30 Aug 2026 with live API replay + PostHog. **The dominant cause of app search zero-results is NOT index coverage** — this corrects `app-search-defects.md` (23 Aug), which blamed content gaps.

**Root cause: search is non-deterministic.** Same user, same query, seconds apart, flips between 0 and >0 results — 75% of repeated article queries, 57.1% of company queries. `search_performed` fires per keystroke, so every character is a live API call; failed/timed-out/429 responses render as "no results". Controlled for query length, typing fast (<400ms gap) vs slowly (>1500ms) gives up to **9x** the zero-result rate on the identical query length.

**Verified working:** exact company names resolve fine — 48/50 editorially-verified entities return at rank 1 on `POST datalabs-api.inc42.com/header/global-search {"keyword":"..."}`.

**Verified broken:**
- Multi-word queries OR-match with no phrase boost: hit@1 falls 20% (1 token) → 4% (2) → 0% (3); 96-98% of multi-word queries saturate the 20-row cap with junk. `lava mobile`, `iifl finance`, `wagh bakri` return 20 confidently wrong rows, never the right answer.
- Run-together words fail: `waghbakri`/`tbotek`/`myjar` → 0, though spaced versions work.
- No topic search — companies match on name only.
- Article search is raw WordPress: **p50 ~5.0s**, ordered by date not relevance, zero typo tolerance, app caps at 5 results against a 55,562-article corpus.
- API rate-limits by IP; penalty persists minutes (25/25 burst requests → 429).

**Scale:** 47.5% of everyone who searches (29 of 61 searchers, 717 app users) hits a zero result. Articles 35.8% zero (worse than 27% on 23 Aug), companies 19.7%. Honest caveat: it does NOT cause immediate abandonment — 87% engage with content within 5 min vs 94.4% after a good search.

**Open question:** which endpoint/index the app actually calls is UNCONFIRMED — `/header/global-search` answers many queries the app returned 0 for, so the app is likely on `/company/new-search` (size:25) plus something else for articles. Needs 10 min with Ritvik or Anmol; changes which fixes apply.

Deliverable: `~/ClaudeDocs/inc42/app-search-root-cause.md` — staged fix plan (client-side debounce/error-state first, then AND-first query semantics, then coverage + engine replacement).


**Cross-POV extension (30 Aug, same session).** Tested all three surfaces, not just the app:
- **Inc42 Media (articles)** = WordPress `LIKE '%term%'`, no word boundaries, date-ordered, p50 ~5.0s. `EMS` returns **16,860** articles (matches syst-ems/it-ems), `chai` returns **13,110** (matches chai-rman), `Accel` 9,419 (accel-erator). No aliases: `Zomato` 4,695 vs `Eternal Limited` 115; `Zepto` 1,400 vs `Zepto Pvt Ltd` 39.
- **DataLabs web** = 5,913 searches by 686 users in 30d (10x the app), and `Search Completed` carries **no result count and no latency** — failure rate is entirely unmeasurable there.
- **Biggest product gap: intent is thematic, engine is entity-only.** `fintech` is the #1 DataLabs web query (15 distinct users); `ai startups`, `series a`, `unicorns`, `health`, `solar` all in the top 70. App equivalent is the cleantech cluster (green hydrogen, carbon credit, BESS). Entity search matches name only, so all of these return nothing useful.
- **Rate-limit lockout is host-wide and long:** after tripping it, EVERY `datalabs-api.inc42.com` endpoint (global-search, new-search, factsheet, tooltip) was refused from that IP for 30+ min, from a normal browser too; the DataLabs company list renders empty. (I induced it with abnormal load — thresholds unknown, behaviour verified.)

Master deliverable: `~/ClaudeDocs/inc42/inc42-search-diagnosis-and-plan.md` — supersedes the app-only doc. Contains the Typesense index schema, query plan (AND-first, exact>prefix>token>typo, relevance floor, no token-dropping), typed grouped response shape, 4-stage rollout, and acceptance criteria.

**Replay of 57 real DataLabs web queries (30 Aug):** only 1/57 returned nothing — hard zeros are rare on the entity API; the failure is wrong answers. Four confirmed genuine index gaps absorbing 58 searches from 4 users: Brewnexa Technologies (20 searches), Hustle Hard Ventures (14), Emerging Ledger (13), Alphavector (11, the only hard zero). Legal names are separate unlinked records — Kiranakart exists on its own, Eternal Limited → Eternal Capital, Bundl Technologies → Template Bundle, ANI Technologies → Animeria Technologies (0/4 resolve). **CORRECTION: person search is NOT broken** — the API returns Aman Gupta / Tanmay Bhat / Deepinder Goyal at rank 1 of their own `person` array; the defect is that `main.min.js` flattens companies+people+investors into one list so 20 companies bury the right person. Person table has duplicates (Aman Gupta x4). Prefix loses to typo in ranking (`ultravio` → "Hosting Ultraso" above Ultraviolette).

**MAJOR CORRECTION (30 Aug, after Ranjith challenged the report with screenshots).** There is a FOURTH search system: `POST datalabs-api.inc42.com/header/global-search-v2`, used by DataLabs. inc42.com's header uses v1 (`/header/global-search`). Different response shape — v2 returns `results[]` with `entity_type`, plus `did_you_mean` and `applied_filters`. My report described v1 behaviour for a v2 surface, which is why it claimed `lava mobile` returns "Vaca Mobiles" while Ranjith's DataLabs screenshot showed "No results found". Both were true, of different endpoints.
**v2 is much better and already live:** `zomto`/`zomatoo` → Zomato with `did_you_mean`; `shipr` → Shiprocket rank 1; `fintech` → `Fintech (INDUSTRY)` + filter `{company:{sector:["Fintech"]}}`; `green hydrogen` → `{sector:["Energy"], sub_1:["Hydrogen"]}`. Topic-to-sector resolution — the thing I recommended building — EXISTS.
**v2's single defect:** it passes the whole query as one `company_search` value, so multi-word needs an exact full-name match → `iifl finance`, `wagh bakri`, `lava mobile`, `tbotek` all return 0. Tokenising that one field is the highest-value fix in the whole investigation.
**Revised plan: migrate inc42.com + app onto v2 and fix its tokenisation — do NOT start by building a new engine.** New infra is only clearly justified for article search (WordPress LIKE, 5s).
**Two other corrections:** (a) the rate-limit lockout was self-inflicted by my own abnormal load, is NOT reproducible in normal use, and was wrongly presented as root cause #1 — demoted; (b) the typing-speed/zero-result table is a real PostHog correlation (survives scope split: companies 40.0% fast vs 17.8% slow) but the rate-limiting cause I attached to it is unsupported, and a single user cannot reproduce a population correlation — Ranjith correctly could not. The non-determinism itself stands (57.1% companies / 75.0% articles on repeated identical queries); leading cause is a client-side response race, matching the "race condition" already logged in the 26 Aug sync.

**Ranjith's observations from 4 Sep — both now VERIFIED and root-caused on 6 Sep 2026:**
1. **Exact-word match misses** (`cred` → no CRED). **CONFIRMED, and it is DataLabs-only.**
2. **Too many irrelevant results.** **CONFIRMED — same bug as (1).**

**6 SEP 2026 LIVE RE-TEST — five findings that change the plan.** Doc refreshed in place: `~/ClaudeDocs/inc42/inc42-search-diagnosis-and-plan.md` (now dated "Revised 6 Sep", corrections C4–C8, root causes re-ranked, §9 rewritten into Tracks A/B/C).

- **ROOT CAUSE #0 (new, most severe): inc42.com article search returns NOTHING for every query.** `?s=<query>` server-renders an empty `#inc-algolia-hits`; the Algolia InstantSearch path is half-wired — the `algolia` config global is undefined, `algoliasearch`/`instantsearch` libs are not enqueued, and `inc42-algolia-search.js` bails on its first line. `main.min.js` has 13 algolia refs, ALL show/hide UI, zero fetch. Verified empty for cred/zomato/fintech/startup/funding. So the header popup finds companies (v1) but never content. **CAVEAT: derived from served HTML, not a rendered browser — needs a 30-second browser confirm before circulating.** This also means the doc's old §4 article numbers (`EMS`→16,860, 5s) describe `wp-json/wp/v2/posts?search=`, a path NO USER HITS.
- **ROOT CAUSE #1: `cred` = no exact-match boost + no relevance floor.** CRED IS indexed (`C-2623`, slug `cred`, name exactly "CRED", Fintech/Bengaluru/2018) — found via `fintech` and `peak xv` routes. 175 companies match "cred"; v2 caps at 15 and the exact answer never surfaces. Symptoms (1) and (2) are ONE bug.
- **v1 vs v2 INVERTED the 30 Aug conclusion.** v2 is NOT strictly better. v2: 15/30 hard zeros (50%), `cred`→absent, `ola`/`navi`→rank 3, p50 **1,558ms**. v1: 1/15 zeros, `cred`/`ola`/`navi`→**rank 1**, p50 **390ms**. v2 wins only on typo (`zomto`+did_you_mean), topic→sector (`fintech`, `green hydrogen`) and investor portfolio (`peak xv`). **So "migrate everything onto v2" would BREAK `cred` on inc42.com where it works today** — migration is now gated on v2 beating v1 on the regression set.
- **Server is deterministic** (6× `green hydrogen`, 8× `shipr` → identical). Confirms the 57–75% flip-flop is the client-side response race. Stage 0 unchanged.
- **Nothing has shipped since 30 Aug** — every multi-word failure still returns 0.

**Harness gotchas (cost me time):** all `datalabs-api.inc42.com` endpoints 403 without a **`Referer: https://inc42.com/`** header. **v1's response key is `companies` (plural), v2's is `results[]`** — reading v1 for `company` gives a false "returns nothing". `company/new-search` ignores `size`/`from` on `company_search` (always 5 rows; true total in `count`). Probe scripts were in the session scratchpad (`probe.py`, `regress.py`, `cmp2.py`, `art.py`) — regenerate if needed.

**Method lesson:** #0 and #1 were both only visible by driving the actual product pages; every prior audit tested endpoints and concluded the engines roughly worked. Start future search audits at the user-facing surface.

**Still open:** which endpoint the app calls; which surfaces are on v2 (it is on NO public page — `/datalabs/` itself uses v1, so v2 is the logged-in app only); whether v2's 1.5s latency is structural; whether its matcher is a tunable engine or hand-rolled SQL. Last two gate fix-vs-replace.

This bucket is its own workstream — Ranjith confirmed all four sub-tracks in scope (v2 relevance, client Stage 0, v2 latency/migration call, article search).

Relates to [[project-inc42-app-explore-deep-dive]] (search rage-loop P0), [[project-inc42-app-analytics-audit]], [[feedback-validation-approach]].
