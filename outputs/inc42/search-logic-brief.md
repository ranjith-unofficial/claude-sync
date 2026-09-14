# DataLabs Search: Logic Brief

**15 Sep 2026** · Existing logic vs new logic, why the existing one fails, why each new step exists, latency, impact.

---

## 1. In one line

Today's search is a **filter**: any name containing the typed letters qualifies, and being the exact answer earns nothing. The new logic is a **ranker**: it grades how well each name matches and puts the best match first.

---

## 2. Existing logic (DataLabs search today)

Observed from the live endpoint on 9 and 14 Sep. We tested behaviour; we have not seen the code.

| # | What it does today | Why it fails | Proof |
|---|---|---|---|
| 1 | Spell-corrects the query, then sends the **whole query as one text filter** (or routes it to an investor or sector filter) | Multi-word and spaced queries often match nothing | `iifl finance`, `matter motor`, `of business` → no results. All three companies exist |
| 2 | A name qualifies if the letters appear **anywhere** in it, even mid-word | Fragments rank with or above real names | `ola` → Manam Chocolate, Prolance, then Ola |
| 3 | **No ranking by match quality.** Order did not follow alphabet, name length, starts-with, record age, funding or prominence | The exact answer gets buried | `cred` → CRED 11th of 15 |
| 4 | Query cleaning is inconsistent | Same intent, different results | `cred.` → CRED 1st; `cred` → 11th |
| 5 | Investor-like queries go to an investor filter; some queries reach no filter at all | No result rows shown | `apax`, `sequioa`, `speciale`, `ultravio` → no rows |
| 6 | No alias or legal-name mapping | Old or legal names miss | `eternal limited`, `kiranakart` → not Zomato / Zepto |
| 7 | Returns max 15 rows, `count` always 0, errors look like empty results | Truncation invisible, failures look like "nothing found" | `count: 0` on every query |
| 8 | Fires on every keystroke | Late replies overwrite newer ones; results flicker | Same query flips between results and none |

**Latency today:** 1.5 s typical, 2.0 s worst (22 queries, 14 Sep). Up to 3.6 s seen on 9 Sep. Empty query takes 3.2 s. inc42.com's search on the same API host answers in 0.37 s.

---

## 3. New logic (14 steps in 5 stages)

| Stage | Steps | What happens | Runs where |
|---|---|---|---|
| **A. Prepare** | 1. Clean query | Build 3 forms: as typed · cleaned (lowercase, no accents, no end punctuation, legal suffixes removed) · squashed (no spaces, `'`, `&`, `-`, `.`) | In memory |
| | 2. Stop empty / short | Empty → return instantly. Under 3 letters → "type at least 3 characters" | In memory |
| | 3. Alias lookup | Known old or legal name → rewrite to main record | One table lookup |
| **B. Search** | 4. One search, all types | One index with a `type` field (companies, investors, people, industries, reports) | One search call |
| | 5. Match ladder | Each name gets only its **best** level: exact 10 · squashed exact 9 · whole word 7 · squashed starts-with 6 · starts-with 5 · typo 2 · sounds-like 1 · description 0.5. All words must match first; if nothing, retry with any word | Same call (retry only if empty) |
| **C. Score** | 6. Score | Match level × word-count factor × quality score (quality computed in advance at each data sync) | Same call |
| | 7. No per-type divide | Scores stay comparable across types | Nothing to run |
| | 10. Type weight | Company 1.0 · Investor 0.9 · Person 0.8 · Industry 0.6 · Report 0.5. Tie-breaker only | On returned rows |
| **D. Tidy** | 8. Pin exact | Exact or squashed-exact name → rank 1, never cut | On returned rows |
| | 9. Remove duplicates | Collapse on canonical ID | On returned rows |
| | 11–12. Cap and sort | 5 companies / 3 investors / 3 people / 2 industries / 2 reports, after pin and dedupe. Ties broken by ID. Show 10 | On returned rows |
| **E. Return** | 13. Honest response | True `count`, type on every row, error ≠ "no results" | API |
| | 14. Client | Wait 400 ms after typing, cancel old request, ignore late replies | App / web |

**Guards:** sounds-like only for words of 5+ letters, never on its own. Squashed levels only for one-word queries (otherwise `third wave` drops to 2nd).

---

## 4. "Why so complex?"

**It is one search call.** Steps 1–3 are string cleanup and a lookup before it. Steps 8–12 are a sort over the handful of rows that come back. The heavy parts (name sub-fields, quality scores, aliases, canonical IDs) are **built once when data is indexed**, not on every search.

**Every step fixes a query that fails without it.** Simulation, switching one piece off at a time (all on = 20 / 22 right answer first):

| Switch off | Result | What breaks |
|---|---|---|
| Alias table | 18 / 22 | `eternal limited`, `kiranakart` → not found |
| One index / no per-type divide | 18 / 22 | `apax` 1 → 2, `iifl finance` 1 → 2 |
| Whole-word level | 19 / 22 | `apax` 1 → 2 (Apaxon beats Apax Partners) |
| Squashed form | 19 / 22 | `of business` → not found |
| Squashed on one-word only | 19 / 22 | `third wave` 1 → 2 |
| Sounds-like guard | 20 / 22 | `sequioa` drops out of results |
| Exact pin | 20 / 22 | Not visible on this set. Protects shut-down or thin profiles: without it, an exact match loses rank 1 once its quality falls below 0.42 |
| All words first | 20 / 22 | Top answer unchanged on this set. Its job is removing rows that match only one word (e.g. only "finance") |

Plus the steps a ranking test cannot show: stop empty queries (3.2 s wasted today), honest `count` and error states, client wait (flicker).

---

## 5. Latency

| | Today | New logic |
|---|---|---|
| Typical | 1.5 s | Target 200 ms |
| Empty query | 3.2 s | 0 ms (no call) |
| Calls per search | One per keystroke | One per typing pause |

**Why the new logic should not add delay:**
- One search call instead of separate calls per type plus a merge.
- Starts-with and squashed forms are pre-built in the index, so matching is a lookup, not a scan.
- Retry happens only when the first pass is empty.
- Post-processing touches only the rows returned (tens, not thousands).

**Cost:** a larger index (more sub-fields per name) and one full reindex.

**Not yet measured:** the new build's own latency. Measure p50 and p95 in staging before release. The 200 ms target is a goal, not a proven result.

---

## 6. Impact (22 real queries, known right answers)

| Measure | DataLabs today | New logic |
|---|---|---|
| Right answer first | 9 / 22 (41%) | **20 / 22 (91%)** |
| Right answer in top 5 | 11 / 22 (50%) | **21 / 22 (95%)** |
| "No results" for a company that exists | 9 / 22 | **0 / 22** |
| Wrong or missing | 13 / 22 | **2 / 22** (85% fewer) |

Still not first: `iifl` (IIFL Securities stays 1st; fix with an alias if wanted) and `sequioa` (9th; 1st once investor quality scores are filled).

---

## 7. Quick answers for Ashish

| Question | Answer |
|---|---|
| Why not just boost exact matches? | Fixes `cred`, `ola`, `navi` (3 queries). Leaves 9 "no results", aliases and cross-type ranking broken |
| Why one index? | Today a company's score and an investor's score can't be compared. `apax` shows a weak company match above the exact investor |
| Will it be slower? | It should be faster: one call, pre-built fields, no empty-query calls, no per-keystroke calls. Confirm in staging |
| Do we ship all 14 at once? | No. Order: (1) exact pin + cleaning · (2) fix "no results" for existing records · (3) one index · (4) match ladder, guards, suffixes · (5) aliases, investor quality, dedupe · (6) client wait and error state |
| How do we know it worked? | Run the same 22 queries (plus the 33-query acceptance list) in staging before release and in production after. Add result count and clicked position to the search event before release |

---

## 8. Limits, stated

- "New logic" numbers come from a simulation on a 4,905-record sample with ~9× fewer look-alike names than production. Expect slightly below 91% live; staging gives the true number.
- Why DataLabs returns nothing for `iifl finance`, `matter motor` and `of business` today is **not known from outside**. Needs someone with index access.
- Companies missing from the database (Wagh Bakri, Lava, TBO Tek, BirdEye) stay missing. No ranking fixes that.
- Article search on inc42.com is a separate workstream.
