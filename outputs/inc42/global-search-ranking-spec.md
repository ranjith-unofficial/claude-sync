# Global Search: Required Ranking Behaviour

**Version 1.0, 9 September 2026.** Written as an addition to the Global Search PRD (Entity + Analytical intents, ES-backed unified modal). It specifies only how results must be **ordered**, not what the modal looks like or which indexes exist.

Every number below is either measured against the live endpoints on 9 September 2026, or produced by a re-runnable simulation of the PRD's own scoring logic over a 4,905 document corpus (2,581 companies, 1,465 people, 847 investors) pulled from the live API.

---

## 1. The problem this solves

Live behaviour today on `header/global-search-v2`:

| Query | Where the exact answer ranks | What outranks it |
|---|---|---|
| `cred` | **11 of 15** | CredR, InCred Holdings, InCred, Credgenics, OkCredit, CredAble, Altum Credo, Credlix, Credit Wise Capital, Credit Fair |
| `ola` | **3** | Manam Choc**ola**te, Pr**ola**nce |
| `navi` | **3** | Navixel Solutions, Navigatio Asia DMC |
| `credit` | Credit Suisse at 3 | Fintech (industry), **Prerit Rathi (a person)** |

The same queries on `header/global-search` (v1) return the exact answer at rank 1, 10 times out of 10.

**Diagnosis.** v2 asks a single yes/no question: do these characters appear anywhere in this name. CredR, InCred, Okcredit and CRED all answer yes and enter one undifferentiated bucket, which is then emitted in an order that correlates with nothing. Tested and ruled out as the sort key: alphabetical, name length, prefix match, match position, record age, funding, prominence. The order is deterministic across repeated calls, so it is a stable score, but not a relevance score.

`credit` returning a person named Prerit above Credit Suisse confirms that approximate matches are scored at least as highly as literal ones.

**In one line: search is currently behaving as a filter, not as a ranking. Being the exact answer earns a record nothing.**

---

## 2. Required behaviour, stated as rules

### Rule 1. Match strength must be graded, not binary

Every candidate is scored on five ladders. **Only the single highest ladder counts** (`best_fields`). Ladders do not add up.

| Ladder | Fires when | Weight |
|---|---|---|
| `name.exact` | normalised query equals the normalised full name | **10.0** |
| `name.token` | a query token equals a complete word of the name | **7.0** |
| `name.squash` | punctuation and space stripped name equals or starts with the stripped query (single token queries only) | **6.0** |
| `name.prefix` | the name begins with the query (edge n-gram, 2 to 15) | **5.0** |
| `name.fuzzy` | within edit distance AUTO | **2.0** |
| `name.phonetic` | phonetic key matches | **1.0** |
| `description` | the term appears in the description | **0.5** |

`name.token` and `name.squash` are additions to the current PRD. Without `name.token`, a whole word match and a mid word fragment are indistinguishable, which is the direct cause of `ola` returning Manam Chocolate.

### Rule 2. Two multipliers, applied after the ladder

```
RAW  =  best ladder score  ×  field length norm  ×  quality score
```

- **Field length norm** = `1 / sqrt(number of words in the name)`. Elasticsearch applies this automatically. A one word name keeps 1.000, a two word name 0.707, a three word name 0.577.
- **Quality score** = the pre-computed 0.1 to 1.0 prominence value from the PRD's `function_score`. Computed at index time, never at query time.

Worked example, `cred`, from the simulation:

| Rank | Entity | Best ladder | × length | × quality | RAW |
|---|---|---|---|---|---|
| **1** | **CRED** | **exact 10.0** | 1.000 | 0.78 | **7.80** |
| 2 | CredR | squash 6.0 | 1.000 | 0.61 | 3.69 |
| 3 | Credilio | squash 6.0 | 1.000 | 0.61 | 3.69 |
| 4 | CredAble | squash 6.0 | 1.000 | 0.61 | 3.69 |

A 2.1x margin. A partial match cannot reach the exact ladder, so no amount of funding or prominence closes the gap.

### Rule 3. An exact name match is pinned to rank 1

**This is the guarantee, and it must be a deterministic rule rather than a scoring outcome.**

Scoring alone does not guarantee it. The simulation locates the exact break even point: an exact name match wins only while its quality score exceeds **0.42**. Two verified failures below that line:

| Case | Quality | Result |
|---|---|---|
| Active company | 0.50 to 0.78 | Exact match wins. 41 of 41 tested. |
| **Shut down company** | **0.36** | **Loses rank 1 to a larger partial match.** |
| **Thin profile plus relevance floor active** | **below 0.42** | **Removed from the results entirely, not merely demoted.** |

Required:

1. If `normalise(name) == normalise(query)`, that record is placed at rank 1.
2. An exact name match is **exempt from the relevance floor** and can never be filtered out.
3. If more than one record matches exactly, order those by quality score among themselves.

### Rule 4. All query tokens must match on multi word queries

Set `minimum_should_match: 100%`, with a retry as OR only when the strict pass returns nothing.

Without it, Elasticsearch defaults to OR: `iifl finance` currently ranks IIFL Finance **6th**, behind CapitalXB, Avail and Arthan Finance, and the per index size cap of 5 cuts it off the list entirely.

### Rule 5. One index with a `type` field, not per index normalisation

The PRD normalises each index by dividing by the top score **within that index**. This makes the leading row of every index normalise to exactly 1.000, so leading rows end up ordered purely by type weight and never by match quality.

Measured on `apax`:

| Entity | RAW | After per index normalisation |
|---|---|---|
| Apax Partners (investor, exact token) | 2.722 | 0.900 |
| Apaxon Technologies (company, partial prefix) | 2.121 | **1.000** |

The weaker match wins. This is the mechanism behind `credit` returning an industry row and a person above Credit Suisse.

Required: a single index carrying a `type` field, or failing that, normalisation against a fixed constant (10.0) rather than the per index maximum. A single index also removes the client side merge step and helps the latency target.

### Rule 6. Phonetic matching needs a length guard

Phonetic matching must not qualify a record on its own, and must not fire on query tokens shorter than 5 characters. Without the guard, `credit` matches a person named Prerit and `sequoia` matches Zoko and SK Finance above Sequoia Capital.

### Rule 7. Aliases resolve to the canonical record

Legal names and former names are currently separate unlinked records or absent. An alias table must ship in Phase 1, not later:

`Eternal Limited` to Zomato, `Kiranakart` to Zepto, `Bundl Technologies` to Swiggy, `ANI Technologies` to Ola.

### Rule 8. Investor quality signals cannot be deferred

With flat investor quality, `sequioa` returns Sequoia Capital at rank 9. With realistic investor quality it returns rank 1. Investor quality is load bearing for the ranking and has to be populated in the same phase as company quality.

---

## 3. Acceptance criteria

### Must rank 1

| Query | Expected rank 1 | v2 today |
|---|---|---|
| `cred` | CRED | 11 |
| `ola` | Ola | 3 |
| `navi` | Navi | 3 |
| `credit` | Credit Suisse or a Credit company | 3 |
| `iifl finance` | IIFL Finance | 6 |
| `zomato` `zepto` `swiggy` `paytm` `groww` `meesho` `razorpay` | the named company | 1 (already passing, must not regress) |
| `zomto` `flipcart` `razorpey` `sequioa` | the intended company, with `did_you_mean` | typo path works, keep |
| `ofbusiness` `of business` | OfBusiness | must match either spacing |
| `matter motor` `third wave` | Matter, Third Wave Coffee | already rank 1 on v1, must not regress |

### Must never happen

1. A mid word fragment match ranking above a whole word match. Test: `ola` must not return Manam Chocolate above Ola.
2. An exact name match falling below rank 1, or being absent from the result set.
3. A person or industry row outranking an entity whose name matches more strongly.
4. A multi word query returning results that match only one of its words while the full match exists.

### Non functional

| Metric | v1 today | v2 today | Target |
|---|---|---|---|
| p50 latency, 10 query sample | **360 ms** | **1,768 ms** | 200 ms per the PRD |
| Exact answer at rank 1, 10 query sample | 10 of 10 | 7 of 10 | 10 of 10 |

Measured 9 September 2026.

---

## 4. Expected outcome

Simulation of the PRD's scoring over the live corpus:

| Configuration | Rank 1 hit rate, 22 case regression set |
|---|---|
| PRD exactly as currently written | 16 of 22 |
| PRD plus the additions in this document | **20 of 22** |
| Same, with investor quality populated | **21 of 22** |

The remaining failures are missing records, not ranking failures. See section 5.

---

## 5. Items outside ranking that block the result

Verified on 8 September 2026: **Wagh Bakri, Lava, TBO Tek, BirdEye, Eternal Limited and ANI Technologies are not present in the index at all.** These are data coverage gaps. No ranking rule retrieves them, and they should be tracked separately from this specification.

Two further defects found while measuring:

1. **v2 returns `count: 0` on every query** while v1 returns the true total (803 for `cred`). Any downstream consumer reading result counts, including the PRD's own success metrics, currently receives zero.
2. **v1 returns duplicate records.** `cred` returns CredR at both rank 4 and rank 6.

---

## 6. Sequencing recommendation

| Order | Change | Reason |
|---|---|---|
| 1 | Rule 3, exact match pin | Single largest visible fix, smallest change, removes the reported symptom outright |
| 2 | Rule 5, single index or fixed constant normalisation | Everything else is unreliable while leading rows sort by type |
| 3 | Rule 1 `name.token`, Rule 4 `minimum_should_match`, Rule 6 phonetic guard | The remaining ranking corrections |
| 4 | Rule 7 aliases, Rule 8 investor quality | Data population, can run in parallel |

**Migration note.** v2 is live on public pages today, including logged out company pages, and it is the surface producing the ranking failures above. v1 currently returns the correct answer at rank 1 in a fifth of the time. Any plan to move remaining surfaces onto v2 should be gated on v2 passing the acceptance set in section 3, otherwise the move regresses queries that work correctly today.
