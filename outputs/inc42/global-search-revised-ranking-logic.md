# Global Search — Revised Ranking Logic

**Version 1.0 · 10 September 2026**
**Status:** implement this. It replaces three sections of the Global Search PRD (Ankit Srivastava / Ritvik Sethi, shared by Ashish): *Relevance & Ranking*, *Fuzzy Search Improvement*, and *Unified Multi-Index Search Query*.

Modal UX, Entity vs Analytical routing, default state, tiers, and Ask DataLabs are unchanged. This document is only how **entity search must retrieve, score, and return results**.

**Verified against:** ~70 live queries on both production endpoints (9 Sep) plus a re-runnable simulation of the PRD formula on 4,905 live documents (8 Sep). Simulation of this logic: **20 / 22 at rank 1** (21 with investor quality populated). Ashish’s PRD as written: **16 / 22**.

---

## 1. What this is for

DataLabs search today (`header/global-search-v2`) treats a query as a filter: if the characters appear anywhere in a name, the record enters one undifferentiated bucket. Being the exact answer earns nothing.

Live, `cred` returns CRED at **rank 11 of 15**. `ola` returns Manam Chocolate, then Prolance, then Ola. `cred.` returns CRED at rank 1. Same intent, different universe.

This logic makes search a ranker. The exact answer is first. Close variants of the same intent return the same result set.

Worked example after this logic, `cred`:

| Rank | Entity | Ladder | × length | × quality | Score |
|---|---|---|---|---|---|
| **1** | **CRED** | exact 10.0 | 1.000 | 0.78 | **7.80** |
| 2 | CredR | squash prefix 6.0 | 1.000 | 0.61 | 3.69 |
| 3 | Credilio | squash prefix 6.0 | 1.000 | 0.61 | 3.69 |

A 2.1× margin. A partial match cannot reach the exact ladder, so prominence cannot close the gap. CRED is then **pinned** at rank 1 so this is a rule, not a scoring outcome.

---

## 2. Pipeline

Every query runs these steps in this order. None are optional.

```
1. Normalise the query          → raw, normalised, squashed
2. Empty / too-short short-circuit
3. Alias lookup                 → rewrite to canonical name if hit
4. Retrieve candidates          → match any ladder field
5. Score each candidate         → best ladder × length norm × quality
6. Pin exact / squash-exact     → force rank 1, exempt from floor and caps
7. Deduplicate                  → canonical id, before size caps
8. Sort remaining               → score desc, then stable id
9. Apply size cap               → after pin and dedup
10. Return                      → true total in `count`, type label on every row
```

If step 4 returns nothing, retry once with OR semantics (step 4b). If that also returns nothing, return a true empty state, not an error.

---

## 3. Query normalisation (canonical, before anything else)

Two queries that normalise to the same string **must return byte-identical results**.

Build three forms of both the query and every indexed name:

| Form | How |
|---|---|
| `raw` | as typed / as stored |
| `normalised` | trim → collapse internal whitespace to one space → lowercase → fold diacritics to ASCII → strip leading and trailing punctuation |
| `squashed` | `normalised` with spaces, apostrophes, ampersands, hyphens and periods removed |

Also strip legal suffixes when building the matching forms (section 11). Match form against form. Never match raw query against a processed name, or the reverse.

This is what makes `cred` and `cred.`, `cafe` and `café`, `byju's` and `byjus`, `ofbusiness` and `of business`, `l&t` and `l t` the same query.

**Empty / whitespace-only:** return immediately. No ES call. No error. (Live DataLabs spends 3,268 ms on `""`.)

**Minimum length:** 3 characters after normalisation, stated in the API contract. The UI must say “type at least 3 characters”, not “no results”.

---

## 4. Match ladder

Every candidate scores on the ladders below. **Only the single highest applies** (`best_fields`). Ladders never add.

| Field | Fires when | Weight | Notes |
|---|---|---|---|
| `name.exact` | `normalised(query) == normalised(name)` | **10.0** | keyword |
| `name.squash_exact` | `squashed(query) == squashed(name)` | **9.0** | keyword. **Single-token queries only.** On multi-token queries this field is not searched — otherwise `third wave` is demoted |
| `name.token` | a query token equals a complete word of the name | **7.0** | not in the original PRD. Without it, `ola` and the `ola` inside Chocolate are indistinguishable |
| `name.squash_prefix` | squashed name starts with squashed query, query length ≥ 4 | **6.0** | **Single-token queries only**, same reason |
| `name.prefix` | name begins with the query | **5.0** | edge n-gram, min 2 / max 15, **index-side** |
| `name.fuzzy` | within ES AUTO edit distance | **2.0** | 0 edits ≤2 chars, 1 edit 3–5, 2 edits 6+. Name/title only, never description |
| `name.phonetic` | Double Metaphone key matches | **1.0** | cannot qualify a document on its own (section 10) |
| `description` | term appears in the description | **0.5** | never above a name match |

`name.token`, `name.squash_exact` and `name.squash_prefix` are additions to the PRD. They are the difference between CRED at rank 1 and CRED at rank 11.

---

## 5. Score

```
text_relevance  =  best ladder weight  ×  field_length_norm
RAW             =  text_relevance      ×  quality_score
final_score     =  RAW                 ×  type_weight
```

- **Field length norm** = `1 / sqrt(word_count(name))`. ES applies this automatically. One word keeps 1.000, two words 0.707, three words 0.577.
- **Quality score** = `_quality_score` (0.1–1.0), computed at **index time**, never at query time. Formula in section 14, unchanged from the PRD except for the exact-match exemption in section 6.
- **Type weight** is applied only after text relevance. It breaks near-ties. It must not let a weak company match beat a strong investor match.

### Do not normalise per index

The PRD divides each index’s scores by that index’s maximum. That makes every index’s top hit equal 1.0, so leading rows sort purely by type weight.

Measured on `apax`:

| Entity | RAW | After per-index normalisation |
|---|---|---|
| Apax Partners (investor, exact token) | 2.722 | 0.900 |
| Apaxon Technologies (company, partial prefix) | 2.121 | **1.000** |

The weaker match wins. That is also why `credit` can return an industry row and a person above Credit Suisse.

**Required:** one index with a `type` field. Scores are then natively comparable, `_msearch` and the client-side merge both disappear, and the 200 ms target gets easier.

If a single index is not possible in this phase, normalise against a **fixed constant of 10.0** (the exact-ladder weight), never against the per-index maximum.

Type weights, used only after that:

| Type | Weight |
|---|---|
| Company | 1.0 |
| Investor | 0.9 |
| Person | 0.8 |
| Industry | 0.6 |
| Report | 0.5 |

---

## 6. Exact match is pinned to rank 1

Scoring alone does not guarantee this. Simulation: an exact match wins only while quality > **0.42**. A shut-down company at 0.36 loses rank 1 to a larger partial match. A thin profile below 0.42 is dropped by the relevance floor entirely.

So this is a deterministic rule, not a scoring outcome:

1. If `normalised(name) == normalised(query)` **or** `squashed(name) == squashed(query)`, that record is placed at rank 1.
2. An exact match is **exempt from the relevance floor** and from every per-type size cap. It can never be filtered or truncated out.
3. If several records match exactly, order those among themselves by quality, then by a stable identifier so the order never flaps.
4. A shut-down or acquired exact match still ranks 1. Status is a **label on the card**, never a ranking penalty that costs position 1.

This is why CRED is first for `cred`, not CredR.

---

## 7. Multi-word queries

`minimum_should_match: 100%` on any query with two or more tokens.

Elasticsearch defaults to OR. Live consequence: `iifl finance` ranks IIFL Finance **6th**, behind CapitalXB, Avail and Arthan Finance, and the per-type cap of 5 then cuts it off.

If the AND pass returns nothing, retry once as OR. Do not OR on the first pass.

Token matching is **order independent**. `finance iifl` must return IIFL Finance. An optional phrase bonus may lift the original order, but the reversed order must still retrieve the record.

---

## 8. Retrieve, then cap — never the reverse

Per-type size caps (5 companies / 3 investors / 3 people / 2 industries / 2 reports) apply **after** pin and dedup.

An exact match that would have sat at position 6 of an index must still appear.

Modal display cap remains 10, configurable.

---

## 9. Deduplicate before display

Collapse on canonical identifier **before** applying size caps.

Live: `aman gupta` returns the same person three times in six rows. `cred` on the main-site endpoint returns CredR at rank 4 and rank 6. Duplicates consume result slots.

---

## 10. Phonetic matching

- Query token must be **≥ 5 characters**.
- A phonetic hit **cannot qualify a document on its own**. It must co-occur with a prefix or fuzzy hit.
- Phonetic never outranks exact, token, or prefix.

Without the guard, `credit` matches a person named Prerit, and `sequioa` matches Zoko and SK Finance above Sequoia.

Use Double Metaphone, not a compact metaphone.

---

## 11. Legal suffixes

Strip these (case-insensitive) when building `normalised` and `squashed` forms of names. The stripped form matches at the `name.token` ladder.

`Limited`, `Ltd`, `Pvt`, `Private`, `Inc`, `LLP`, `LLC`, `Technologies`, `Technology`, `Ventures`, `Venture`, `Works`, `Holdings`, `Group`, `India`, `International`.

So `matter`, `matter motor`, and `Matter Motor Works` resolve to the same record.

---

## 12. Aliases — Phase 1, not later

An alias table is queried in pipeline step 3. A hit rewrites the query to the canonical name **before** retrieval. The canonical record is what is returned.

Ship at least:

| Query | Resolves to |
|---|---|
| Eternal Limited, Eternal | Zomato |
| Kiranakart | Zepto |
| Bundl Technologies | Swiggy |
| ANI Technologies | Ola |
| Sequoia, Sequoia Capital | Peak XV Partners |
| Jar, MyJar | Jar (canonical) |

Without this table, `eternal limited` and `kiranakart` miss even with perfect ranking — they are separate unlinked records, or absent.

Seed from the DataLabs legal-name field. Hand-curate the top 200 brands in Phase 1.

---

## 13. Investor quality cannot be deferred

With flat investor quality, a typo query for Sequoia ranks the intended investor **9th**. With realistic investor quality it ranks **1st**.

Compute investor `_quality_score` in the same phase as company quality. Do not ship companies-only quality and “fill investors later”.

---

## 14. Quality scores (index time)

Unchanged from the PRD, with one override: **exact matches ignore the inactive-status penalty for ranking** (section 6). The penalty still exists for non-exact competitors.

Floor every score at 0.1. Recalculate on each index sync. Store as `_quality_score`.

**Company**

| Signal | Logic | Weight |
|---|---|---|
| Funding | 0 unfunded · 0.3 <$1M · 0.5 $1–10M · 0.7 $10–100M · 0.9 $100M–1B · 1.0 $1B+ | 0.25 |
| Team size | 0.2 1–10 · 0.4 11–50 · 0.6 51–200 · 0.8 201–1000 · 1.0 1000+ | 0.15 |
| Status | 1.0 active · 0.3 shutdown/acquired *(ignored for exact-match pin)* | 0.20 |
| Recency | 1.0 <6m · 0.8 6–12m · 0.6 1–2y · 0.4 2–5y · 0.2 older/never | 0.15 |
| Completeness | non-null key fields / key fields | 0.10 |
| Trending | top 1% = 1.0 · top 10% = 0.5 · rest = 0 | 0.15 |

**Investor** — must be populated in Phase 1

| Signal | Logic | Weight |
|---|---|---|
| Portfolio size | 0.3 1–10 · 0.5 11–50 · 0.7 51–200 · 1.0 200+ | 0.30 |
| Investment count | 0.3 1–10 · 0.5 11–50 · 0.7 51–100 · 1.0 100+ | 0.30 |
| Exits | 0.3 0 · 0.5 1–5 · 0.7 6–20 · 1.0 20+ | 0.20 |
| Trending | same as companies | 0.20 |

**Person:** seniority 0.30 · associated company quality 0.30 · primary-role flag 0.20 · trending 0.20.

**Industry:** company count 0.50 · total funding 0.50.

**Report:** recency 0.60 · page count 0.40.

Weights live as backend config, not hardcoded.

---

## 15. Index mapping

On every name (and report title):

```
name
  .exact          keyword, normalised
  .squash_exact   keyword, squashed
  .token          standard analyser, whole-token equality
  .squash_prefix  edge n-gram on the squashed form (min 4)
  .prefix         edge n-gram 2–15, index-side
  .fuzzy          standard text
  .phonetic       Double Metaphone sub-field
  .suffixless     normalised name with legal suffixes stripped
description       standard text
type              keyword   (company | investor | person | industry | report)
canonical_id      keyword
aliases           keyword array
_quality_score    float
```

Preferred: **one index**, `type` field on the document.

Synonym filter at query time for abbreviations only (`VC` ↔ Venture Capital, `PE` ↔ Private Equity, `D2C`, `SaaS`, `AI`). Brand aliases go through the alias table (section 12), not the synonym filter.

---

## 16. Query shape

Replace the PRD `_msearch` block with this. If still on five indices, run the same body against each, then merge by `final_score` using the fixed constant 10.0 — never the per-index max.

```json
{
  "size": 15,
  "query": {
    "function_score": {
      "query": {
        "bool": {
          "should": [
            { "term":  { "name.exact":        { "value": "{{normalised}}", "boost": 10 } } },
            { "term":  { "name.squash_exact": { "value": "{{squashed}}",   "boost": 9  } } },
            { "match": { "name.token":        { "query": "{{normalised}}", "operator": "and", "boost": 7 } } },
            { "prefix":{ "name.squash_exact": { "value": "{{squashed}}",   "boost": 6  } } },
            { "match": { "name.prefix":       { "query": "{{raw}}",        "boost": 5  } } },
            { "match": { "name.fuzzy":        { "query": "{{normalised}}", "fuzziness": "AUTO", "boost": 2 } } },
            { "match": { "description":       { "query": "{{normalised}}", "boost": 0.5 } } }
          ],
          "minimum_should_match": 1
        }
      },
      "functions": [
        {
          "field_value_factor": {
            "field": "_quality_score",
            "modifier": "none",
            "missing": 0.1
          }
        }
      ],
      "boost_mode": "multiply",
      "score_mode": "multiply"
    }
  }
}
```

Application-side, after ES returns:

1. Drop any row whose only hit was `name.phonetic` and whose query token is < 5 characters.
2. Pin exact / squash-exact to rank 1.
3. Dedup on `canonical_id`.
4. Multiply by type weight.
5. Sort, cap, return.

`name.squash_exact` and `name.squash_prefix` clauses are **omitted when the query has more than one token**.

If this AND-style pass is empty, retry with `"operator": "or"` and no exact pin from the retry (the pin only fires on a true exact / squash-exact hit).

Phonetic is a `should` clause on the retry only, never on the first pass, and never without a co-occurring prefix or fuzzy hit.

---

## 17. API contract

| Field | Rule |
|---|---|
| `count` | True total matching the query. Live v2 returns `count: 0` on every query. Stop that |
| `results[]` | Ordered list after pin, dedup, sort, cap |
| `entity_type` | Present on every row |
| Empty query | HTTP 200, `results: []`, `count: 0`, no ES call |
| True zero | HTTP 200, empty results, nearest suggestions if any |
| Timeout / 429 / 5xx | Distinct error. **Never** rendered as “no results” |
| Determinism | Same query, same result set. Variance is a defect |

Client (any surface using this endpoint):

- Debounce ≥ 400 ms, or fire on submit.
- Cancel in-flight requests.
- Discard any response whose query string is not the current one.
- Do not fire `search_performed` per keystroke.

---

## 18. Acceptance

### Must return the named entity at rank 1

`cred`, `ola`, `navi`, `rocket`, `startup`, `matter`, `byjus`, `byju's`, `of business`, `ofbusiness`, `iifl finance`, `finance iifl`, `wave coffee`, `third wave`, `5paisa`, `1mg`, `3one4`, `l&t`, `l t`, `cafe`, `café`, `zomato`, `zepto`, `swiggy`, `paytm`, `groww`, `meesho`, `razorpay`, `zomto`, `flipcart`, `razorpey`, `aman gupta`, `peak xv partners`.

The last seven already pass on today’s engines and are regression guards.

`CRED`, `cred`, and `cred.` must be byte-identical result sets, with CRED at rank 1.

### Must never happen

1. A mid-word fragment ranking above a whole-word match.
2. An exact name match below rank 1, or absent from the result set.
3. A person or industry row above an entity whose name matches more strongly.
4. A multi-word query returning only single-word matches while a full match exists.
5. Two queries that normalise identically returning different results.
6. The same query returning different results on repeat calls.
7. An error or timeout rendered as “no results”.
8. A duplicate record consuming a result slot.

### Must be true of the contract

1. `count` is the true total.
2. Minimum query length is documented and shown in the UI.
3. Every row carries its type label.

Do not migrate remaining surfaces onto `global-search-v2` until this list passes. v1 already returns CRED / Ola / Navi at rank 1, in about a fifth of the time. Moving onto v2 before this logic ships regresses queries that work today.

---

## 19. What changed vs the PRD

| PRD as written | This logic |
|---|---|
| `name.exact^10`, `prefix^5`, `fuzzy^2`, `phonetic^1`, `description^0.5` | Same, plus `token^7`, `squash_exact^9`, `squash_prefix^6` |
| `best_fields` implied | `best_fields` explicit; ladders never add |
| Per-index divide-by-max | One index with `type`, or normalise to 10.0 |
| No `minimum_should_match` (ES defaults to OR) | AND first, OR only on empty |
| Word order unspecified | Order independent |
| Exact match is a scoring outcome | Exact match is pinned, exempt from floor and caps |
| Phonetic on every token, can qualify alone | ≥5 chars, cannot qualify alone |
| No suffix stripping | Legal suffixes stripped |
| Aliases unscheduled | Alias table in Phase 1 |
| Investor quality deferrable | Load-bearing, same phase as companies |
| Dedup unspecified | Canonical id, before caps |
| `_msearch` five indices, client merge | Single query preferred |
| `count` unspecified | True total required |

Ashish’s `exact^10` already puts CRED at rank 1 in simulation. Ship this document, not the PRD scoring section unmodified — otherwise `iifl finance`, `apax`, `finance iifl`, `cred` vs `cred.`, and aliases still fail.

---

## 20. Build order

| Order | Change | Why |
|---|---|---|
| 1 | Exact-match pin + query normalisation | Largest visible fix, smallest change. No index rebuild. CRED / Ola / Navi, plus punctuation, diacritics, apostrophes, spacing |
| 2 | Recall for records that exist on v1 and return 0 on DataLabs | `matter`, `byjus`, `of business`, `dr reddy`. Empty screen is worse than rank 11. Cause is not yet known — needs index-config access |
| 3 | Single index, or fixed-constant 10.0 normalisation | Until this lands, leading rows still sort by type |
| 4 | `name.token`, AND-first, word order, phonetic guard, suffix stripping | Remaining ranking corrections |
| 5 | Alias table, investor quality, dedup | Data. Can run in parallel with 4 |
| 6 | Debounce, discard stale responses, distinct error state | Removes perceived flakiness |

---

## 21. Out of scope of this logic

These are real bugs. Ranking does not fix them. Do not treat a green acceptance list as “search is done”.

1. **Article and content search.** Dead Algolia on inc42.com; WordPress `LIKE` matching syst-**ems** for `EMS`. Separate workstream.
2. **Analytical intent / Ask DataLabs routing.** Unchanged from the PRD; not specified here.
3. **Records not in the index.** Wagh Bakri, Lava, TBO Tek, BirdEye. No ranking rule retrieves a missing document. Data backlog, not a query change.
4. **Class B recall.** Records retrievable on `global-search` (v1) that return 0 on DataLabs v2. Required behaviour is rank 1; the retrieval bug is unsolved until someone with index access inspects it.
5. **Single-token `iifl`.** Even with this logic, IIFL Finance stays rank 2 behind IIFL Securities. The acceptance list requires `iifl finance` and `finance iifl` at rank 1, not the bare token. Resolve with an alias (`iifl` → IIFL Finance) if product wants that.
6. **v2 latency.** Target 200 ms. Live DataLabs p50 ~1,768 ms. Stated, not produced by these rules.
7. **Non-Latin / transliterated queries.** Untested. v1 scope may return 0; say so in the contract rather than failing silently.

---

## 22. Sources

- Global Search PRD, *Relevance & Ranking* / *Fuzzy Search Improvement* / *Unified Multi-Index Search Query*
- `~/ClaudeDocs/inc42/search-logic-simulation-8sep.md` (8 Sep)
- `~/ClaudeDocs/inc42/global-search-ranking-spec.md` (9 Sep)
- Live replay of both `header/global-search` and `header/global-search-v2` on 9 Sep 2026
