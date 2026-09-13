# Global Search: What Changes, in Simple Terms

**Date:** 13 Sep 2026
**Short version of:** Global Search Revised Ranking Logic (10 Sep), sent to Ashish

---

## Part 1. Ashish's logic vs our change

| # | Topic | Ashish's logic (PRD) | Our change | Example of why |
|---|---|---|---|---|
| 1 | Exact name match | Gets the highest score (10), but is still just a score. A bigger company with a partial match can beat it | Exact match is **always rank 1**. Never filtered out, never cut by limits. A shut-down company still ranks 1, with a "shut down" label | `cred` must show CRED first |
| 2 | Whole-word match | Not there. "ola" inside "Chocolate" counts the same as "Ola" | New level: a full word match scores 7, above a partial match (5) | `ola` shows Manam Chocolate above Ola today |
| 3 | Spacing, punctuation, accents | Not handled | Treated as the same query | `cred` = `cred.` = `CRED`; `byjus` = `byju's`; `ofbusiness` = `of business`; `cafe` = `café` |
| 4 | Mixing companies, investors, people | Each type scored separately. The top result of every type is reset to the same score, then sorted by type | Score all types together (one index). If not possible now, divide by a fixed 10, not by each type's top score | `apax`: Apaxon Technologies (weak match) beats Apax Partners (exact match) |
| 5 | Multi-word queries | Any one word can match | **All words** must match first. Only if nothing comes back, allow any word. Word order does not matter | `iifl finance`: IIFL Finance is 6th and gets cut. With our change it is 1st |
| 6 | Sounds-like (phonetic) match | Works on any word length, can bring a result in on its own | Only for words of 5+ letters, and only alongside another match | `sequioa` shows Zoko and SK Finance above Sequoia |
| 7 | Legal suffixes | Not handled | Ignore Limited, Ltd, Pvt, Private, Inc, LLP, LLC, Technologies, Ventures, Holdings, Group, India, etc. | `matter` = `matter motor` = Matter Motor Works |
| 8 | Aliases (old or legal names) | Left as a later edge case | **Phase 1.** Seed from the legal-name field, hand-check top 200 brands | Eternal Limited → Zomato, Kiranakart → Zepto, ANI Technologies → Ola |
| 9 | Investor quality score | Can be added later | Same phase as company quality | `sequioa`: Sequoia is 9th without it, 1st with it |
| 10 | Duplicates | Not specified | Remove duplicates before counting the top 5 | `aman gupta` shows the same person 3 times in 6 rows |
| 11 | Result limits (5 companies / 3 investors / 3 people / 2 industries / 2 reports) | Applied before merging | Same limits, applied **after** pinning the exact match and removing duplicates | An exact match at position 6 must still appear |
| 12 | Empty or very short query | Not specified | Empty query returns instantly, no search call. Minimum 3 characters, UI says "type at least 3 characters" | Empty query takes 3.2 seconds today |
| 13 | Result count | Not specified | Return the true total | Today's endpoint always returns 0 |
| 14 | Errors and timeouts | Not specified | Show as an error with retry. **Never** show as "no results" | Failed calls look like empty results today |
| 15 | Typing behaviour | Not specified | Wait 400 ms after typing stops, cancel old requests, ignore late responses | Same query flips between results and no results |

**Unchanged from Ashish's PRD:** prefix, typo (fuzzy) and description weights; type weights (Company 1.0, Investor 0.9, Person 0.8, Industry 0.6, Report 0.5); quality score formula; search modal; Ask DataLabs routing.

**Measured result (22 test queries, right answer at rank 1):**

| Version | Score |
|---|---|
| Ashish's PRD as written | 16 / 22 |
| With our changes | 20 / 22 (21 with investor quality filled in) |

---

## Part 2. Two additions to the Search scope of work

### 1. Make workflow failure: capture and retry

| | |
|---|---|
| **What** | When the Make workflow fails, the failure is recorded and the run is retried automatically |
| **Capture** | Log every failed run: time, step that failed, error message, records affected |
| **Retry** | Retry automatically a fixed number of times, with a gap between attempts |
| **If retries run out** | Alert the owner. The failed run stays visible until someone fixes it |
| **Done when** | No failed run is silently skipped. Every failure is either retried successfully or alerted |
| **To confirm** | Which Make workflow(s) this covers, retry count and gap, who gets the alert |

### 2. Logic changes and workflow enhancements

| | |
|---|---|
| **What** | Build Part 1 of this document into search |
| **Build order** | 1. Exact match at rank 1 + treat spacing/punctuation the same<br>2. Fix records that show on inc42.com search but return nothing on DataLabs (`matter`, `byjus`, `of business`)<br>3. Score all types together<br>4. Whole-word match, all-words-first, sounds-like guard, suffix stripping<br>5. Alias table, investor quality, duplicate removal<br>6. Typing wait, ignore late responses, separate error state |
| **Done when** | All test queries return the right answer at rank 1 (full list in the 10 Sep document, section 18) |
| **Rule** | Do not move other surfaces onto the DataLabs search endpoint until this passes. inc42.com search already shows CRED, Ola and Navi first |

---

## Not fixed by these changes

| Issue | Why |
|---|---|
| Article search on inc42.com | Separate workstream |
| Companies missing from the database (Wagh Bakri, Lava, TBO Tek, BirdEye) | No ranking rule finds a missing record. Data backlog |
| Search speed (target 200 ms, today ~1.8 s) | Stated as a target, not solved by ranking rules |
