---
name: project-inc42-app-search-root-cause
description: "Inc42 app search failure root cause (30 Aug 2026) — non-determinism from per-keystroke request flooding, not missing content; corrects the 23 Aug index-coverage diagnosis"
metadata:
  type: project
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

Relates to [[project-inc42-app-explore-deep-dive]] (search rage-loop P0), [[project-inc42-app-analytics-audit]], [[feedback-validation-approach]].
