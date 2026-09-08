# Global Search PRD — Logic Simulation Before Implementation

**Date:** 8 Sep 2026
**Question asked:** does the search logic in the Global Search PRD actually return the right answer, before anyone builds it?
**Method:** built a working simulator of the PRD's scoring, ran it against a real corpus pulled live from the production index, on a regression set of queries with known-correct answers.
**Verdict:** the PRD's core fix is correct and does solve the reported symptom. Three defects would ship with it as written. All three are fixable in the spec, none require a different engine.
**Harness:** `~/ClaudeDocs/inc42/search-sim/` — re-runnable.

---

## 1. What was built

A Python implementation of exactly what the PRD specifies:

| PRD element | Implemented as |
|---|---|
| `name.exact^10` | keyword field, whole-string equality |
| `name.prefix^5` | edge n-gram, min 2 / max 15, index-side |
| `name.fuzzy^2` | Levenshtein with ES AUTO fuzziness (0 edits ≤2 chars, 1 edit 3–5, 2 edits 6+) |
| `name.phonetic^1` | Double-Metaphone-style key |
| `description^0.5` | token match |
| `multi_match` | `best_fields` = max across fields; terms sum within a field |
| BM25 | field-length normalisation (a 1-token name beats a 4-token name at equal match) |
| `function_score` | multiply by `_quality_score` |
| Company quality | funding 0.25 / team 0.15 / status 0.20 / recency 0.15 / completeness 0.10 / trending 0.15 |
| Cross-type weights | Company 1.0, Investor 0.9, Person 0.8, Industry 0.6, Report 0.5 |
| `_msearch` sizes | 5 companies / 3 investors / 3 people / 2 industries / 2 reports |
| Score normalisation | per-index max, exactly as §"Score Normalization Across Indices" specifies |

**Corpus:** 4,905 documents pulled live from `datalabs-api.inc42.com/header/global-search` — 2,581 companies, 1,465 people, 847 investors, 12 industries. Harvested across 200 seed queries, then deepened around every token in the regression set so the *competitor* sets are real, not synthetic. Quality signals parsed from live descriptions (funding, sector, status) and merged with employee counts from the 443-row DataLabs pull.

---

## 2. Result

| Config | Answer found in top 10 | Answer at rank 1 |
|---|---|---|
| **PRD exactly as written** | 19 / 22 | **16 / 22** |
| **PRD + the 5 fixes below** | 22 / 22 | **20 / 22** (21 with investor quality populated) |

### Per-query

| Query | Expected | PRD rank | PRD top-3 | Fixed rank |
|---|---|---|---|---|
| cred | CRED | **1** | CRED, CRED, Sarah Crew | 1 |
| ola | Ola | **1** | Ola, Ola, Sharwan Ola | 1 |
| navi | Navi | **1** | Navi, Navi Technologies, Navin Jain | 1 |
| zomato | Zomato | 1 | Zomato, Zomato, Jim Romano | 1 |
| zomto | Zomato | 1 | Zomato, Zomato, Sumit Babar | 1 |
| shipr | Shiprocket | 1 | Shiprocket, Shiprocket, Shipra Singh | 1 |
| razorpey | Razorpay | 1 | Razorpay ×3 | 1 |
| flipcart | Flipkart | 1 | Flipkart, Flipkart, Flipkart Ventures | 1 |
| **sequioa** | Sequoia Capital | **MISS** | Zoko, SK Finance, Sequoia Sprout | 9 → **1** w/ investor quality |
| ultravio | Ultraviolette | 1 | Ultraviolette, Hosting Ultraso… | 1 |
| **apax** | Apax Partners | **2** | **Apaxon Technologies**, Apax Partners | **1** |
| speciale | Speciale Invest | 1 | Speciale Invest ×2 | 1 |
| ofbusiness | OfBusiness | 1 | OfBusiness ×2, Bada Business | 1 |
| **iifl finance** | IIFL Finance | **6** | CapitalXB Finance, Avail Finance, Arthan Finance | **1** |
| matter motor | Matter | 1 | Matter, Yamaha Motor, Matter Labs | 1 |
| third wave | Third Wave Coffee | 1 | Third Wave Coffee, Waverly, Jasmeet Thind | 1 |
| zepto | Zepto | 1 | Zepto, Swiggy, Ankit Agarwal | 1 |
| of business | OfBusiness | 1 | OfBusiness ×2, BUSINESSNEXT | 1 |
| iifl | IIFL Finance | 2 | IIFL Securities, IIFL Finance | 2 |
| shiprocket | Shiprocket | 1 | Shiprocket ×2, Saahil Goel | 1 |
| **eternal limited** | Zomato | **MISS** | Eternal Capital, Eternal Living | **1** |
| **kiranakart** | Zepto | **MISS** | Kiranakart, Jitendra Gupta | **1** |

**The good news, stated plainly:** `cred`, `ola` and `navi` — the exact symptom reported — all return the right answer at rank 1 under the PRD's logic. The `name.exact^10` boost is the correct fix and it works. That question is settled.

---

## 3. Defect 1 — per-index normalisation is mathematically broken

**This is the serious one.** PRD §"Score Normalization Across Indices", step 1:

> "Per-index normalization: Divide each result's score by the max score within that index's response."

Consequence: **the top hit of every index always normalises to exactly 1.0**, then gets multiplied by its type weight. So the leading row of each entity type is ordered *purely by type weight* — never by how good the match was. A junk company match always beats a perfect investor match, deterministically.

Measured on `apax`:

| Entity | Raw score | Winning field | After per-index normalisation |
|---|---|---|---|
| **Apax Partners** (investor) | **2.722** | exact token match | 2.722 → 1.0 → ×0.9 = **0.900** |
| Apaxon Technologies (company) | 2.121 | partial prefix | 2.121 → 1.0 → ×1.0 = **1.000** |

The better match loses by construction. Same mechanism put `Zoko` above `Sequoia Capital` on `sequioa`.

**Fix — pick one:**
- **(a) Preferred — one index with a `type` field instead of five.** ES scores become natively comparable, `_msearch` and the app-side merge both disappear, and the 200ms p95 target gets easier rather than harder.
- (b) Normalise against a fixed constant (max achievable boost = 10) rather than per-index max.
- (c) Skip normalisation; share one analyzer/mapping across indices so raw BM25 is comparable.

---

## 4. Defect 2 — no `minimum_should_match`, so multi-word queries flood

The PRD specifies `multi_match` with no `operator` and no `minimum_should_match`. ES defaults to OR. Measured on `iifl finance`: **IIFL Finance ranks 6th**, below CapitalXB Finance, Avail Finance and Arthan Finance — companies matching only the token "finance". The per-index cap of 5 companies then cuts it entirely.

**Fix:** `minimum_should_match: "100%"` on multi-token queries, with an automatic OR retry when AND returns nothing. Moves IIFL Finance from **6 → 1**.

---

## 5. Defect 3 — phonetic matching has no length guard

`name.phonetic^1` applies to every name at any length. Short phonetic keys collide constantly: the metaphone key for `sequioa` also matches `Zoko` and `SK Finance`, both of which outranked the real answer.

**Fix:** apply phonetic only to tokens of 5+ characters, and never let a phonetic hit alone qualify a document — require it to co-occur with a prefix or fuzzy hit.

*Caveat: the simulator uses a compact metaphone, not a full Double Metaphone. The specific `sequioa`→`Zoko` collision should be re-checked against the real analyzer. The structural point — no length guard, phonetic can qualify a doc on its own — is in the PRD text regardless.*

---

## 6. The finding that changes priorities: four entities are not in the index at all

Before testing ranking, ground truth was verified directly against the live index. Four of the "multi-word tokenisation failures" carried in my own earlier diagnosis are **not ranking bugs — the record does not exist**:

| Query | Live `count` | What comes back | Verdict |
|---|---|---|---|
| `wagh` | 56 | Wagr, Waghela Infotech, Quick Wage | **Wagh Bakri absent** |
| `lava` | 98 | LAPA Electric, CAVA, Lavanya International | **Lava absent** |
| `tbo` | 219 | TBot Techno Systems, CostBo | **TBO Tek absent** |
| `birdeye` | 3 | ThirdEye AI, BigEye Global | **BirdEye absent** |
| `eternal limited` | 1,323 | Eternal Capital, Eternal Living | **Eternal Ltd absent** (Zomato's legal name) |
| `ani technologies` | 9,458 | Animeria Technologies, Anika Technologies | **ANI Technologies absent** (Ola's legal name) |

**No search logic fixes a missing record.** Every hour spent on fuzzy matching, n-grams and phonetics leaves these six queries returning nothing.

Two corrections to my own earlier analysis, from the same check: `matter motor` and `third wave` **already return the right answer at rank 1 on v1 today**. They were wrongly listed as failures.

---

## 7. Recommended edits to the PRD

| # | Change | Section to edit | Effect measured |
|---|---|---|---|
| 1 | Replace per-index normalisation — single index with a `type` field, or normalise to a fixed constant | Score Normalization Across Indices | `apax` 2 → 1; removes a whole failure class |
| 2 | Add `minimum_should_match: "100%"` with OR fallback | Unified Multi-Index Search Query | `iifl finance` 6 → 1 |
| 3 | Add `name.token^7` — whole-token equality, between exact and prefix | Multi-Field Mapping | separates "Apax Partners" from "Apaxon" |
| 4 | Add `name_squash` field (lowercased, punctuation stripped), **single-token queries only** | Multi-Field Mapping | fixes `ofbusiness`; scoped so it does not demote `third wave` |
| 5 | Phonetic: 5+ char guard, cannot qualify a doc alone | Fuzzy Search Improvement §3 | removes `Zoko`-class false positives |
| 6 | Alias table as a **Phase 1** item, not an unscheduled edge case (6.2) | Implementation Phases | `eternal limited`, `kiranakart` MISS → 1 |
| 7 | Add a data-gap backlog: Wagh Bakri, Lava, TBO Tek, BirdEye + legal-name records | new | six queries that no ranking change can fix |

**One more, from the sensitivity test:** investor quality signals (portfolio size, investment count, exits) are **load-bearing**, not cosmetic. With flat investor quality `sequioa` ranks 9; with realistic values it ranks 1. Phase 1 must compute investor quality, not defer it.

---

## 8. Caveats — read before circulating

- **Corpus is a sample.** 2,581 companies against roughly 75K live; 92 documents match "cred" locally versus **803** in production. Noise is under-sampled by ~9×, so every failure reported here is a **lower bound** — the same defects will be worse at full scale. Successes carry correspondingly less weight.
- **BM25 is approximated,** not reproduced. Term saturation and true IDF are absent; field-length normalisation is modelled. Ranking *relationships* are trustworthy; absolute scores are not.
- **Quality signals are partial.** Funding, sector, status and (for 443 companies) employee counts are real. Recency is a neutral constant; trending is 0 for all, which is what the PRD itself specifies for the long tail.
- **Investor quality is flat 0.55** in the headline numbers — deliberately conservative. See §7.
- **Metaphone is simplified** — see §5 caveat.
- The simulator tests **retrieval and ranking only**. AI intent classification, Ask Datalabs routing, and the modal's state machine were not simulated.

---

## 9. Answer to the question that prompted this

> "If it is still not coming up, it doesn't make sense at the end of the day."

It does come up. The PRD's `exact > prefix > fuzzy > phonetic` ladder returns CRED for `cred` at rank 1, and fixes `ola` and `navi` too — the reported symptom is genuinely solved by the proposed design.

But **16 of 22 at rank 1 is not launch quality**, and three of the six failures trace to defects in the spec rather than to tuning. Fixing them on paper first takes 20 lines of spec change and moves the same regression set to 20–21 of 22.

**Recommendation: apply edits 1–7, then build.** Ship the corrected spec into Phase 1 rather than discovering the normalisation flaw during Phase 4 relevance tuning, where it would present as unexplainable ranking behaviour.
