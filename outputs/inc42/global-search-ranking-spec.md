# Global Search: Required Behaviour Specification

**Version 2.0, 9 September 2026.** An addition to the Global Search PRD (Entity and Analytical intents, ES backed unified modal). It specifies how search must **behave**, covering ranking, matching, query handling, failure states and non functional limits.

**Method.** Approximately 70 distinct queries were run against both live endpoints (`header/global-search-v2`, used by DataLabs and by logged out company pages, and `header/global-search`, used by the main site header) on 9 September 2026. Ranking claims are additionally checked against a re-runnable simulation of the PRD's own scoring formula over a 4,905 document corpus (2,581 companies, 1,465 people, 847 investors) pulled from the live API. Every "today" column below is an observed result, not an inference.

---

## 1. Summary of what is wrong today

Three independent defect classes, not one.

| Class | Symptom | Example |
|---|---|---|
| **A. Ranking** | The exact answer is returned but buried | `cred` returns CRED at **11 of 15** |
| **B. Recall** | The record exists but the query returns nothing at all | `matter` returns **0**, while the company Matter is rank 1 on the other endpoint |
| **C. Consistency** | The same intent typed slightly differently returns a different universe | `cred` ranks CRED 11th, `cred.` ranks it **1st** |

Class B is the most severe and is not currently named in the PRD. On the test set, **5 valid queries for records that demonstrably exist returned zero results.**

---

## 2. Core diagnosis

The current engine asks one question: do these characters appear anywhere in this name. CredR, InCred, OkCredit and CRED all answer yes and enter one undifferentiated bucket, which is then emitted in an order that correlates with nothing measurable. Ruled out as the sort key by testing: alphabetical, name length, prefix match, match position, record age, funding, prominence.

**Search is behaving as a filter, not as a ranking. Being the exact answer earns a record nothing.**

Supporting evidence:

| Query | Result today | What it proves |
|---|---|---|
| `ola` | Manam Choc**ola**te, Pr**ola**nce, then Ola | Mid word fragments rank above whole word matches |
| `credit` | Fintech (industry), **Prerit Rathi (a person)**, then Credit Suisse | Approximate matches score at least as high as literal ones |
| `rocket` | Shiprocket, Rocketlane, then Rocket | A company named exactly Rocket ranks third for its own name |
| `startup` | Startuppz, StartupXY, then Startup | Same pattern, and it reproduces on both endpoints |

---

## 3. Ranking rules

### Rule 0. Query normalisation is canonical and happens before anything else

Two queries that normalise to the same string **must return byte identical results.**

Normalisation order: trim, collapse internal whitespace, lowercase, fold diacritics to ASCII, strip leading and trailing punctuation, and additionally build a "squashed" form with all spaces, apostrophes, ampersands, hyphens and periods removed.

Both the query and the indexed name are stored in all three forms (raw, normalised, squashed) and matched form against form.

Verified failures this fixes:

| Pair | Today | |
|---|---|---|
| `cred` vs `cred.` | CRED at **11** vs CRED at **1** | Trailing punctuation silently changes the ranking path |
| `ola` vs `ola.` | Ola at **3** vs Ola at **1** | Same |
| `cafe` vs `café` | 15 results vs 3 results, **completely disjoint sets** | Diacritics are not folded, on either endpoint |
| `byju's` vs `byjus` | 1 result vs **0 results** | Apostrophe is mandatory today |
| `ofbusiness` vs `of business` | 1 result vs **0 results** | Spacing is mandatory today |
| `l&t` vs `l t` | L&T Technology Services vs **Canvera Digital Technologies** | Ampersand is mandatory today |

### Rule 1. Match strength is graded, and only the highest ladder counts

Every candidate scores on the following ladders. Only the single highest applies (`best_fields`). Ladders never add.

| Ladder | Fires when | Weight |
|---|---|---|
| `name.exact` | normalised query equals the normalised full name | **10.0** |
| `name.squash_exact` | squashed query equals the squashed name | **9.0** |
| `name.token` | a query token equals a complete word of the name | **7.0** |
| `name.squash_prefix` | squashed name starts with the squashed query, minimum 4 characters | **6.0** |
| `name.prefix` | name begins with the query (edge n-gram, 2 to 15) | **5.0** |
| `name.fuzzy` | within edit distance AUTO | **2.0** |
| `name.phonetic` | phonetic key matches | **1.0** |
| `description` | term appears in the description | **0.5** |

`name.token`, `name.squash_exact` and `name.squash_prefix` are additions to the current PRD. Without `name.token`, a whole word match and a mid word fragment are indistinguishable, which is the direct cause of `ola` returning Manam Chocolate first.

### Rule 2. Two multipliers after the ladder

```
RAW  =  best ladder score  ×  field length norm  ×  quality score
```

- **Field length norm** = `1 / sqrt(number of words in the name)`. Applied automatically by Elasticsearch. One word keeps 1.000, two words 0.707, three words 0.577.
- **Quality score** = the 0.1 to 1.0 prominence value from the PRD's `function_score`, computed at index time and never at query time.

Worked example, `cred`, from the simulation:

| Rank | Entity | Best ladder | × length | × quality | RAW |
|---|---|---|---|---|---|
| **1** | **CRED** | **exact 10.0** | 1.000 | 0.78 | **7.80** |
| 2 | CredR | squash prefix 6.0 | 1.000 | 0.61 | 3.69 |
| 3 | Credilio | squash prefix 6.0 | 1.000 | 0.61 | 3.69 |
| 4 | CredAble | squash prefix 6.0 | 1.000 | 0.61 | 3.69 |

A 2.1x margin. A partial match cannot reach the exact ladder, so prominence cannot close the gap.

### Rule 3. An exact name match is pinned to rank 1

**This must be a deterministic rule, not a scoring outcome.**

Scoring alone does not guarantee it. The simulation locates the break even point: an exact match wins only while its quality score exceeds **0.42**.

| Case | Quality | Outcome |
|---|---|---|
| Active company | 0.50 to 0.78 | Wins. 41 of 41 tested |
| **Shut down company** | **0.36** | **Loses rank 1 to a larger partial match** |
| **Thin profile with the relevance floor active** | **below 0.42** | **Removed from results entirely, not merely demoted** |

Required:

1. If `normalise(name) == normalise(query)`, or `squash(name) == squash(query)`, that record is placed at rank 1.
2. An exact match is **exempt from the relevance floor** and from every per type size cap. It can never be filtered or truncated out.
3. If several records match exactly, order those among themselves by quality score, then by a stable identifier so the order never flaps.

### Rule 4. All query tokens must match on multi word queries

`minimum_should_match: 100%`, with a retry as OR only when the strict pass returns nothing.

Without it Elasticsearch defaults to OR: `iifl finance` currently returns IIFL Finance at rank **6**, behind CapitalXB, Avail and Arthan Finance, and the per type size cap of 5 cuts it off entirely.

### Rule 5. Word order must not matter

`finance iifl` currently returns IIFL Seed Ventures, IIFL Special Opportunities Fund and IIFL Securities, and never IIFL Finance. Token matching must be order independent, with an optional phrase bonus when the order does match.

### Rule 6. One index with a `type` field, not per index normalisation

The PRD normalises each index by dividing by the top score **within that index**. That makes the leading row of every index normalise to exactly 1.000, so leading rows sort purely by type weight and never by match quality.

Measured on `apax`:

| Entity | RAW | After per index normalisation |
|---|---|---|
| Apax Partners (investor, exact token) | 2.722 | 0.900 |
| Apaxon Technologies (company, partial prefix) | 2.121 | **1.000** |

The weaker match wins. This is the mechanism behind `credit` returning an industry row and a person above Credit Suisse.

Required: a single index carrying a `type` field, or failing that, normalisation against a fixed constant (10.0) rather than the per index maximum. A single index also removes the client side merge step and helps the latency target.

### Rule 7. Phonetic matching needs a length guard

Phonetic matching must not qualify a record on its own, and must not fire on query tokens shorter than 5 characters. Without the guard, `credit` matches a person named Prerit and `sequoia` matches unrelated records above the intended one.

### Rule 8. Legal suffixes are stripped for matching

`Limited`, `Ltd`, `Pvt`, `Private`, `Inc`, `LLP`, `Technologies`, `Ventures`, `Works` and similar suffixes are removed when building the matching forms, and the stripped form is matched at the `name.token` ladder.

Verified need: `Matter Motor Works` returns 0, `matter motor` returns 0, and `matter` returns 0, while the record exists.

### Rule 9. Aliases and former names resolve to the canonical record

An alias table ships in Phase 1, not later.

| Query | Must resolve to | Today |
|---|---|---|
| `Eternal Limited`, `Eternal` | Zomato | Separate unlinked record |
| `Kiranakart` | Zepto | Separate record |
| `Bundl Technologies` | Swiggy | Separate record |
| `ANI Technologies` | Ola | Separate record |
| `Sequoia`, `Sequoia Capital` | Peak XV Partners | **0 results** |

### Rule 10. Investor quality signals cannot be deferred

With flat investor quality the intended investor ranks 9 on a typo query. With realistic investor quality it ranks 1. Investor quality is load bearing and must be populated in the same phase as company quality.

### Rule 11. Duplicate records are collapsed before display

Verified live: `aman gupta` returns the same person three times in six rows. `cred` on the main site endpoint returns CredR at both rank 4 and rank 6.

Deduplicate on canonical identifier before applying size caps, so duplicates do not consume result slots.

---

## 4. Edge case matrix

Every row was executed. "Today" is the observed v2 result unless stated.

### 4.1 Query hygiene

| # | Scenario | Example | Today | Required |
|---|---|---|---|---|
| 1 | Empty query | `""` | 0 rows, no error, **3,268 ms** | Return immediately, no network call, no error |
| 2 | Whitespace only | `"   "` | 0 rows, 3,092 ms | Treated as empty |
| 3 | Below minimum length | `c`, `cr` | 0 rows | Minimum length of 3 is acceptable, but must be **stated in the contract** and the UI must say so rather than showing "no results" |
| 4 | Uppercase | `CRED` | Same as `cred` | Correct, keep |
| 5 | Mixed case | `CrEd` | Same as `cred` | Correct, keep |
| 6 | Leading or trailing space | `" cred"`, `"cred "` | Same as `cred` | Correct, keep |
| 7 | Double internal space | `credit  card` | Returns rows | Collapse to single space before matching |
| 8 | **Trailing punctuation** | `cred.` vs `cred` | **CRED at rank 1 vs rank 11** | **Identical results. This is Rule 0** |
| 9 | Repeated punctuation | `cred!!` | CRED at rank 1 | Identical to `cred` |
| 10 | **Diacritics** | `cafe` vs `café` | **15 rows vs 3 rows, disjoint sets** | Fold to ASCII, one result set |
| 11 | **Apostrophe** | `byju's` vs `byjus` | **1 row vs 0 rows** | Both return BYJU'S |
| 12 | **Ampersand** | `l&t` vs `l t` | L&T rows vs unrelated companies | Both return the L&T entities |
| 13 | Hyphen | `of-business` | 0 rows | Same as `of business` and `ofbusiness` |
| 14 | Digits in query | `5paisa`, `1mg`, `3one4` | All resolve correctly | Keep |
| 15 | Very long query | 120 characters | 0 rows, no error | Truncate at a stated limit, no error |
| 16 | Emoji only | `🔥` | 0 rows, no error | Clean empty state |
| 17 | Markup or script string | `<script>alert(1)</script>` | 0 rows, no error, not reflected | Correct, keep, and add a regression test |
| 18 | Non Latin script | Devanagari input | 0 rows | Acceptable for v1 scope, but **state it** so it is a known limit rather than a silent failure |
| 19 | Stop word only | `the` | 0 rows | Acceptable, must render as a prompt to refine, not as a failure |
| 20 | Generic word | `startup` | Startuppz, StartupXY, then Startup | The exact name Startup must rank 1 |

### 4.2 Matching behaviour

| # | Scenario | Example | Today | Required |
|---|---|---|---|---|
| 21 | Exact full name | `cred` | Rank 11 | **Rank 1, pinned** |
| 22 | Exact name that is also a common word | `matter`, `rocket` | 0 rows / rank 3 | Rank 1 |
| 23 | Exact name of a shut down company | quality 0.36 in simulation | Loses rank 1 | Rank 1, status shown as a label, never as a ranking penalty that costs it position 1 |
| 24 | Prefix | `raz` for Razorpay | Works | Keep, below exact and whole word |
| 25 | Whole word inside a multi word name | `wave coffee` for Third Wave Coffee | Works | Keep |
| 26 | **Mid word fragment** | `ola` inside Chocolate | **Ranks 1 and 2** | Must rank strictly below every whole word and exact match |
| 27 | Suffix of a longer name | `rocket` for Shiprocket | Ranks 1, above the company named Rocket | Allowed, but strictly below the exact match |
| 28 | Run together words | `ofbusiness`, `waghbakri` | 1 row / 0 rows | Both spellings resolve through the squashed form |
| 29 | Extra space | `of business` | **0 rows** | Resolves to OfBusiness |
| 30 | **Word order reversed** | `finance iifl` | Returns three other IIFL entities, never IIFL Finance | Order independent |
| 31 | Partial multi word | `wave coffee` | Works | Keep |
| 32 | One character typo | `zomto` | Zomato rank 1 | Keep |
| 33 | Two character typo | `razorpey` | Razorpay rank 1 | Keep |
| 34 | Phonetic | `flipcart` | Flipkart rank 1 | Keep, with the Rule 7 length guard |
| 35 | Typo on a record that does not exist | `sequioa` | 0 rows | Correct behaviour, but must show "did you mean" or a clean empty state |
| 36 | Legal suffix omitted | `matter` for Matter Motor Works | 0 rows | Rank 1 via Rule 8 |
| 37 | Legal suffix included | `InCred Holdings Limited` | Works | Keep |
| 38 | Former or legal name | `Eternal Limited` | Separate record | Resolves to Zomato |
| 39 | Description only match | term in the blurb, not the name | Contributes | Keep at weight 0.5, never above a name match |
| 40 | Query matches a sector | `fintech` | Fintech industry row at rank 1 | Keep, this works well |
| 41 | Multi word sector | `green hydrogen` | Two industry rows, no companies | Should also surface companies in that sector |
| 42 | Person name | `aman gupta` | Rank 1, **duplicated three times** | Rank 1, deduplicated |
| 43 | Investor name | `peak xv partners` | Rank 1 | Keep |
| 44 | Investor portfolio spillover | `peak xv` | Ranks 2 and 3 are portfolio companies | Allowed only in a labelled section, never mixed into the entity list unlabelled |
| 45 | Same name across two types | company and person share a name | Not currently distinguishable | Both returned, ordered by match strength then type weight, each with its type label |

### 4.3 Failure and empty states

| # | Scenario | Today | Required |
|---|---|---|---|
| 46 | **True zero, record does not exist** | Renders as "No results" | Correct, and must offer the nearest suggestions |
| 47 | **False zero, record exists** | `matter`, `byjus`, `of business`, `dr reddy` all return 0 while the record is retrievable on the other endpoint | **Must not happen. This is the recall acceptance criterion** |
| 48 | **Non deterministic zero** | `3one4` returned 1 result on 5 of 6 identical calls and **0 on the sixth** | Same query must return the same result set. Any variance is a defect |
| 49 | Server error or timeout | Currently indistinguishable from zero results in the UI | Distinct error state, never rendered as "no results" |
| 50 | Rate limiting | Returns as failure | Distinct state, with a retry, never rendered as "no results" |
| 51 | Out of order responses | Search fires per keystroke, a slow earlier response can overwrite a fast later one | Debounce, and discard any response that is not for the current query string |
| 52 | Result count | **v2 returns `count: 0` on every query** while the other endpoint returns the true total (803 for `cred`) | Return the true total. Success metrics and analytics depend on it |
| 53 | Truncation | 15 rows returned with no indication more exist | Show the total and a path to the full result set |

### 4.4 Non functional

| # | Metric | Main site endpoint | DataLabs endpoint | Target |
|---|---|---|---|---|
| 54 | p50 latency, 10 query sample | **360 ms** | **1,768 ms** | 200 ms per the PRD |
| 55 | Worst observed latency | 513 ms | **3,644 ms** | Stated ceiling required |
| 56 | Empty query latency | not applicable | **3,268 ms** | 0 ms, short circuit locally |
| 57 | Exact answer at rank 1, 10 query sample | 10 of 10 | 7 of 10 | 10 of 10 |
| 58 | Determinism | stable across repeats | **1 of 3 tested queries unstable** | 100 percent stable |
| 59 | Logged out behaviour | not applicable | v2 serves logged out company pages today | Same ranking rules apply logged out |

---

## 5. Acceptance criteria

### Must return the named entity at rank 1

`cred`, `ola`, `navi`, `rocket`, `startup`, `matter`, `byjus`, `byju's`, `of business`, `ofbusiness`, `iifl finance`, `finance iifl`, `wave coffee`, `third wave`, `5paisa`, `1mg`, `3one4`, `l&t`, `l t`, `cafe`, `café`, `zomato`, `zepto`, `swiggy`, `paytm`, `groww`, `meesho`, `razorpay`, `zomto`, `flipcart`, `razorpey`, `aman gupta`, `peak xv partners`.

The last seven currently pass and are included as regression guards.

### Must never happen

1. A mid word fragment ranking above a whole word match.
2. An exact name match below rank 1, or absent from the result set.
3. A person or industry row above an entity whose name matches more strongly.
4. A multi word query returning only single word matches while a full match exists.
5. Two queries that normalise identically returning different results.
6. The same query returning different results on repeat calls.
7. An error or timeout rendered as "no results".
8. A duplicate record consuming a result slot.

### Must be true of the contract

1. `count` returns the true total.
2. Minimum query length is documented and surfaced in the UI.
3. Every row carries its type label.

---

## 6. Data preconditions, tracked separately from ranking

No ranking rule retrieves a record that is not indexed. Verified absent or unreachable:

| Record | Status |
|---|---|
| Wagh Bakri, Lava, TBO Tek, BirdEye | Not in the index |
| Eternal Limited, ANI Technologies | Present as separate unlinked records |
| Sequoia Capital | Returns 0 on both endpoints, needs an alias to Peak XV Partners |
| Matter, BYJU'S, OfBusiness | Indexed and retrievable on the main site endpoint, **unreachable on the DataLabs endpoint** |
| Aman Gupta, CredR | Duplicate records |

---

## 7. Sequencing

| Order | Change | Reason |
|---|---|---|
| 1 | Rule 3 exact match pin, and Rule 0 query normalisation | Largest visible improvement for the smallest change. Together they fix the reported symptom and the punctuation, diacritic, apostrophe and spacing inconsistencies in one pass |
| 2 | Recall investigation for class B | Queries returning 0 for records that exist is more damaging than poor ordering, and its cause is not yet known |
| 3 | Rule 6 single index or fixed constant normalisation | Everything else is unreliable while leading rows sort by type |
| 4 | Rule 1 `name.token`, Rule 4 `minimum_should_match`, Rule 5 word order, Rule 7 phonetic guard, Rule 8 suffix stripping | The remaining ranking corrections |
| 5 | Rule 9 aliases, Rule 10 investor quality, Rule 11 deduplication | Data population, can run in parallel |
| 6 | Class C client side work: debounce, discard stale responses, distinct error state | Removes the perceived flakiness |

**Migration note.** The DataLabs endpoint is live on public pages today, including logged out company pages, and it is the surface producing the failures above. The main site endpoint returns the correct answer at rank 1 in a fifth of the time and retrieves records the DataLabs endpoint cannot reach at all. Any plan to move remaining surfaces onto the newer endpoint should be gated on it passing section 5, otherwise the move regresses queries that work correctly today.

---

## 8. Known limits of this specification

Stated so they are not mistaken for coverage.

1. **Article and content search is out of scope here.** It is a separate and more severe problem and is not addressed by any rule above.
2. **The Analytical intent path is not specified.** Only entity ranking is covered.
3. **The cause of the class B recall failures is not yet known.** The rules above define the required behaviour but not the fix, which needs someone with access to the index configuration.
4. **The punctuation path difference has no confirmed mechanism.** It is reproducible on three queries and absent on two others, which suggests two matching paths rather than one, but this needs confirmation from the implementation.
5. **Ranking figures come from a simulation of the PRD formula**, not from the production cluster. The corpus under samples competing records by roughly nine times, so reported failure counts are a lower bound.
6. **Non Latin script and transliterated queries are untested beyond a single case.**
