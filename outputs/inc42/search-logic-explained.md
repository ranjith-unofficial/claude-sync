# DataLabs Search: Every Piece of the Logic, Explained

**15 Sep 2026** · Companion to `search-logic-brief.md`. That brief says *what* changes. This document explains *what each term means, how it works, and why it is there*, with examples.

How to read: Part 1 gives the basic ideas. Part 2 explains today's logic. Part 3 walks through all 14 new steps, one by one. Part 4 follows real queries end to end. Part 5 lists open decisions I found while writing this.

---

## Part 1. Basic ideas you need first

### 1.1 What any search does

Every search does two jobs:

| Job | Question it answers | Example for `cred` |
|---|---|---|
| **Find** | Which records are possible answers? | CRED, CredR, Credilio, CreditVidya... |
| **Order** | Which one goes first? | CRED first, because it is exactly what was typed |

Today's DataLabs search does the first job loosely and the second job barely at all. The new logic does both deliberately.

### 1.2 Words used in this document

| Term | Plain meaning |
|---|---|
| **Record** | One thing that can be found: one company, one investor, one person |
| **Type** | The kind of record. There are 5 types (below) |
| **Index** | The searchable copy of the database, built for fast lookup. Like the index at the back of a book: you don't read every page, you jump to the right one |
| **Field** | One piece of a record: name, description, funding, and so on |
| **Score** | A number given to each found record. Higher score = shown higher |
| **Query** | What the user typed |

### 1.3 The 5 types

| Type | What it is | Example |
|---|---|---|
| **Company** | A startup or business profile | CRED, Zomato, OfBusiness |
| **Investor** | A VC fund, angel network, PE firm | Peak XV Partners, Apax Partners |
| **Person** | A founder or executive | Aman Gupta, Deepinder Goyal |
| **Industry** | A sector or sub-sector | Fintech, Green Hydrogen |
| **Report** | A DataLabs report | A funding report |

The same query can match several types. `cred` matches CRED the company and CRED listed as an investor. `aman gupta` matches a person and possibly a company. Search has to decide how to order a company against an investor against a person. That is the reason several steps exist.

---

## Part 2. Today's logic (existing), explained

Observed from outside by sending real queries on 9 and 14 Sep. We have not seen the code.

### 2.1 How it works today

1. **Spell-correct.** If the query looks misspelt, it is replaced with a known word. `zomto` becomes `zomato`, `flipcart` becomes `flipkart`. *This part works.*
2. **Decide a filter.** The query is turned into a filter: usually "company name contains X", sometimes "investor name contains X" or "sector = X".
3. **Contains anywhere.** A record passes if the typed letters appear **anywhere in its name**, including in the middle of a word.
4. **Return up to 15.** Passing records come back in an order that follows no rule we could find.

### 2.2 Why that fails

**"Filter, not ranker."** A filter only asks *yes or no: does this name contain `cred`?* CredR says yes. InCred says yes (in-**cred**). OkCredit says yes (ok-**cred**-it). CRED says yes. All four get the same "yes". Nothing says CRED is a *better* yes. So CRED lands 11th.

**"Contains anywhere."** `ola` is inside Choc**ola**te and Pr**ola**nce. Both pass, and both appear above Ola.

**"Whole query as one filter."** `iifl finance` is sent as one piece of text. For reasons not visible from outside, this returns nothing, even though IIFL Finance exists. Same for `matter motor` and `of business`.

**"Routed to a different filter."** `apax` becomes "investor filter = apax". The user sees a filtered investor list, not a search result.

**No memory of other names.** Zomato's legal name is Eternal Limited. Search doesn't know that, so `eternal limited` misses.

**Every keystroke is a search.** Typing `cred` fires `c`, `cr`, `cre`, `cred`. If the reply for `cre` arrives after the reply for `cred`, the screen shows results for `cre`. Results flicker.

**Speed.** 1.5 s typical, 2.0 s worst (14 Sep). An empty query takes 3.2 s.

---

## Part 3. New logic, step by step

The 14 steps fall into 5 stages:

```
A. PREPARE        1 Clean the query  →  2 Stop empty/short  →  3 Alias lookup
B. SEARCH         4 One search across all types  →  5 Match ladder
C. SCORE          6 Score  →  7 No per-type divide  →  10 Type weight
D. TIDY           8 Pin exact  →  9 Remove duplicates  →  11 Caps  →  12 Stable sort
E. RETURN         13 Honest response  →  14 Client waits, drops late replies
```

(Step numbers follow the build spec. Type weight, step 10, is explained with scoring because it is part of the score.)

---

### Stage A. Prepare the query

#### Step 1. Clean the query

**What:** Before searching, turn the query into three versions. Do the same to every name in the index, once, when the index is built.

| Version | How it is made | `BYJU'S` becomes | `Of Business` becomes | `Café Coffee Day` becomes |
|---|---|---|---|---|
| **As typed** | Unchanged | `BYJU'S` | `Of Business` | `Café Coffee Day` |
| **Cleaned** | Lowercase · remove accents (é → e) · remove punctuation at start and end · collapse double spaces | `byju's` | `of business` | `cafe coffee day` |
| **Squashed** | Cleaned, then remove all spaces, apostrophes, `&`, hyphens and dots | `byjus` | `ofbusiness` | `cafecoffeeday` |

**Legal suffixes** are also removed from names when building the cleaned and squashed versions: Limited, Ltd, Pvt, Private, Inc, LLP, LLC, Technologies, Technology, Ventures, Venture, Works, Holdings, Group, India, International. So `Matter Motor Works` is also findable as `matter motor` and `matter`.

**Why:** users type the same thing many ways. Search must treat them as one.

| These must give identical results | Today |
|---|---|
| `cred` · `CRED` · `cred.` | `cred.` puts CRED 1st, `cred` puts it 11th |
| `byjus` · `byju's` | 0 results vs 1 result |
| `ofbusiness` · `of business` · `of-business` | 1 result vs 0 vs 0 |
| `cafe` · `café` | Two completely different result sets |
| `l&t` · `l t` | L&T vs an unrelated company |

**Where the "squashed" version is used:** in the match ladder (step 5), to catch spacing and punctuation differences. Explained there.

#### Step 2. Stop empty or very short queries

**What:** If the cleaned query is empty, return nothing immediately, without searching. If it is 1 or 2 characters, show "Type at least 3 characters" instead of "No results".

**Why:** an empty query costs 3.2 s today for nothing. And "No results" after typing `cr` wrongly tells the user the company doesn't exist.

#### Step 3. Alias lookup

**What:** A small table of other names for the same record. If the query matches an alias, replace it with the main name before searching.

| User types | Search actually runs |
|---|---|
| `eternal limited`, `eternal` | Zomato |
| `kiranakart` | Zepto |
| `bundl technologies` | Swiggy |
| `ani technologies` | Ola |
| `sequoia`, `sequoia capital` | Peak XV Partners |

**How the table is built:** start from the legal-name field DataLabs already has, then hand-check the top 200 brands.

**Why:** no matching rule can guess that "Eternal Limited" means Zomato. The letters have nothing in common. Only a table knows.

---

### Stage B. Search

#### Step 4. One search across all types

**What:** Keep all 5 types (companies, investors, people, industries, reports) in **one index**, with a label on each record saying its type. Run **one** search.

**The alternative, and why we avoid it:** keep 5 separate indexes, search each one separately, then merge the 5 lists. The problem: each index scores on its own scale. A score of 3 in the company index and a score of 3 in the investor index don't mean the same thing. So the merge has to invent a way to compare them, and that is where it goes wrong (see step 7).

**Also:** limits like "5 companies, 3 investors" must not be applied at this stage. If they are, a correct answer sitting 6th among companies is thrown away before ordering even happens. Limits come later, in step 11.

#### Step 5. The match ladder

This is the core. Every record that could match gets checked against 8 levels, from strongest to weakest. **A record gets only its single best level.** Levels never add up.

| Level | Points | Matches when | Example query → name |
|---|---|---|---|
| 1. Exact | **10** | Cleaned query = cleaned full name | `cred` → CRED |
| 2. Squashed exact | **9** | Squashed query = squashed full name | `ofbusiness` → Of Business · `byjus` → BYJU'S |
| 3. Whole word | **7** | Every query word is a complete word in the name | `ola` → Ola Electric · `wave coffee` → Third Wave Coffee |
| 4. Squashed starts-with | **6** | Squashed name begins with squashed query (query 4+ letters) | `cred` → CredR · `ofbus` → OfBusiness |
| 5. Starts-with | **5** | A word in the name begins with the query | `shipr` → Shiprocket · `raz` → Razorpay |
| 6. Typo | **2** | Name word is within a few letter-changes of the query | `zomto` → Zomato · `razorpey` → Razorpay |
| 7. Sounds-like | **1** | Query and name word are pronounced the same | `flipcart` → Flipkart |
| 8. Description | **0.5** | Query word appears in the company's description | `quick commerce` → a company described as quick commerce |

Each level in detail:

**Level 1, Exact.** The whole cleaned query equals the whole cleaned name. Nothing more, nothing less. `cred` = CRED. `cred` ≠ CredR.

**Level 2, Squashed exact.** Same as exact, but after removing spaces and punctuation from both sides. Catches the user who types `ofbusiness` for "Of Business", or `byjus` for "BYJU'S". Scores 9, just under exact, because the user didn't type it precisely.

**Level 3, Whole word.** Each word of the query is a complete word somewhere in the name. `ola` is a whole word in "Ola Electric", but **not** in "Manam Chocolate" (there it is only part of a word). This is the level that separates Ola from Chocolate. Word order doesn't matter: `finance iifl` matches IIFL Finance.

**Level 4, Squashed starts-with.** The squashed name begins with the squashed query. `cred` → `credr` (CredR), `credilio` (Credilio). Needs at least 4 letters, otherwise `ab` would match thousands of names.

**Level 5, Starts-with.** Any word of the name begins with what was typed. Built in advance: when the index is created, every word is stored with all its beginnings (`s`, `sh`, `shi`, `ship`, `shipr`, ... up to 15 letters). So at search time, `shipr` is a direct lookup, not a scan. This is what makes search-as-you-type fast.

**Level 6, Typo.** Allows small spelling mistakes. A "letter change" means adding a letter, removing one, changing one, or swapping two neighbours.

| Query length | Letter changes allowed | Example |
|---|---|---|
| 1–2 letters | 0 | Too short to guess safely |
| 3–5 letters | 1 | `zomto` → Zomato (one letter missing) |
| 6+ letters | 2 | `razorpey` → Razorpay (one letter changed) |

Scores only 2, because a typo match is a guess.

**Level 7, Sounds-like.** Converts each word into a short **sound code** based on how it's pronounced, ignoring spelling. The standard method for this is called *Double Metaphone*. Roughly: keep the consonant sounds, drop most vowels, and treat letters that sound alike as the same (C and K, PH and F, Z and S).

- `flipkart` and `flipcart` produce the same code, so they match.
- `Sequoia` produces the code **SK**. So does **Zoko**. So does **SK** Finance.

That second example is the danger. Short codes are shared by hundreds of unrelated names. So sounds-like has **three guards**:

| Guard | Why | Example it prevents |
|---|---|---|
| Only for query words of **5+ letters** | Short words give very short codes that collide constantly | A 3-letter query matching dozens of random names |
| **Never on its own**: the record must also match at starts-with or typo | A shared sound code alone is not evidence | `sequioa` showing Zoko and SK Finance above Sequoia |
| **Last resort**: used only when normal matching found nothing | It's the weakest signal | Sounds-like results crowding out real matches |

Short names like `cred` and `ola` are **not affected**. They are found by levels 1 to 6.

**Level 8, Description.** The query word appears in the company's description text. Lowest score, so a description match never beats a name match.

**What does NOT match at all:** a query found only in the **middle** of a word. `ola` inside "Chocolate", `cred` inside "InCred". Today these are included; in the new logic they are not candidates. (See Part 5, decision 2.)

**Rule: squashed levels (2 and 4) only for one-word queries.** For `third wave`, the squashed version is `thirdwave`. There is a separate, one-word company called **ThirdWave**. Allowing the squashed levels would let ThirdWave (short name, high level) beat Third Wave Coffee (long name, whole-word level). So for queries with 2+ words, squashed levels don't score. Measured: removing this rule drops `third wave` from 1st to 2nd.

One exception: if a name's squashed form is **identical** to a multi-word query's squashed form, that record is still allowed through the all-words rule below (it just doesn't get the 9 points). This is how `of business` still finds OfBusiness, whose name has no separate word "business".

**Rule: all words must match first.** For queries with 2+ words, a record must match **every** word.

| Query `iifl finance` | Matches `iifl`? | Matches `finance`? | Passes? |
|---|---|---|---|
| IIFL Finance | Yes | Yes | **Yes** |
| IIFL Securities | Yes | No | No |
| CapitalXB Finance | No | Yes | No |
| Avail Finance | No | Yes | No |

Without this rule, every company with "Finance" in its name floods the results. **If this strict pass finds nothing**, search runs once more allowing any word to match, so the user still sees something.

---

### Stage C. Score

#### Step 6. Score

```
Score  =  ladder points  ×  word-count factor  ×  quality score
```

**Ladder points:** from step 5 (10, 9, 7, 6, 5, 2, 1 or 0.5).

**Word-count factor:** shorter names get a small advantage when they match equally well, because a short name that matches is more likely the intended one.

| Words in name | Factor | Example |
|---|---|---|
| 1 | 1.00 | Zepto |
| 2 | 0.71 | Zepto Microwave |
| 3 | 0.58 | Third Wave Coffee |

**Quality score:** a number from 0.1 to 1.0 saying how substantial the record is. Calculated **in advance** at every data sync, never during the search, so it costs no search time.

| Type | What goes into quality (weight) |
|---|---|
| Company | Funding raised (25%) · team size (15%) · active vs shut down (20%) · how recently updated (15%) · profile completeness (10%) · trending (15%) |
| Investor | Portfolio size (30%) · number of investments (30%) · exits (20%) · trending (20%) |
| Person | Seniority (30%) · quality of their company (30%) · primary role (20%) · trending (20%) |
| Industry | Number of companies (50%) · total funding (50%) |
| Report | Recency (60%) · page count (40%) |

Why quality matters: when two records match at the same level, the bigger, more complete one should come first. Example: for `sequioa` (a typo), every candidate matches only at the typo level. With investor quality filled in, Sequoia ranks 1st. With every investor given the same flat quality, it ranks 9th, behind people named Sequeira. That is why investor quality must be built in the same phase as company quality.

**Why ladder points beat quality:** exact is 10, the next level is 9 or lower. For `cred`:

| Record | Level | Points | × words | × quality | Score |
|---|---|---|---|---|---|
| **CRED** | Exact | 10 | 1.00 | 0.78 | **7.80** |
| CredR | Squashed starts-with | 6 | 1.00 | 0.61 | 3.69 |
| Credilio | Squashed starts-with | 6 | 1.00 | 0.61 | 3.69 |

CRED is more than twice the next score. A partial match can't close that gap through quality alone.

#### Step 7. No per-type divide

**What:** don't rescale scores separately inside each type.

**The trap this avoids:** when results come from 5 separate searches (step 4's alternative), a common trick is to divide every score by the top score of its own list. That makes the **top of every list exactly 1.0**, no matter how good or bad that top match was. Then the lists are merged, and the #1s are ordered only by type weight.

Measured on `apax`:

| Record | Real score | After dividing by its list's top | × type weight | Final |
|---|---|---|---|---|
| Apax Partners (investor, whole-word match) | **2.72** | 1.00 | × 0.9 | 0.90 |
| Apaxon Technologies (company, partial match) | 2.12 | 1.00 | × 1.0 | **1.00** |

The weaker match wins, purely because it's a company. With one index and no dividing, Apax Partners (2.72 × 0.9 = 2.45) correctly beats Apaxon (2.12).

**If one index is not possible yet:** divide every score by a fixed 10 (the maximum possible), never by each list's own top.

#### Step 10. Type weight

**What:** multiply the score by a small factor based on type.

| Company | Investor | Person | Industry | Report |
|---|---|---|---|---|
| 1.0 | 0.9 | 0.8 | 0.6 | 0.5 |

**Why:** when a company and a person match equally well, most users are looking for the company. This is a **tie-breaker**, never strong enough to put a weak company above a strong investor match. That only holds if step 7 is followed.

---

### Stage D. Tidy the results

These run on the few dozen rows the search returned, not the whole database.

#### Step 8. Pin exact match to rank 1

**What:** if a record's name exactly equals the query (cleaned exact), move it to rank 1, regardless of score. It can't be removed by any limit.

**Why, when exact already scores 10:** the score also multiplies by quality. A shut-down company has low quality (status counts 20%). Simulation: an exact match keeps rank 1 by score only while its quality is above **0.42**. A shut-down company at 0.36 loses rank 1 to a large company with a partial match. The pin makes "exact is first" a guarantee, not a likely outcome. Shut-down status is shown as a label on the result, not as a lower position.

**If several records match exactly** (CRED the company and CRED the investor): order them by quality, then by ID.

#### Step 9. Remove duplicates

**What:** each real-world entity has one master ID (the "canonical ID"). If several rows share it, keep one.

**Why:** today `aman gupta` shows the same person 3 times in 6 rows. Duplicates waste the few slots the user sees.

#### Step 11. Limits per type

**What:** after pin and duplicate removal, keep at most 5 companies, 3 investors, 3 people, 2 industries, 2 reports. Show the top 10 overall.

**Why after, not before:** if limits are applied first (inside each separate search), a correct answer ranked 6th among companies is gone before ordering even starts. This is what cuts IIFL Finance today.

#### Step 12. Stable sort

**What:** sort by score. If two records have the exact same score, order them by ID.

**Why:** without a fixed tie-break, equal-score records can swap places between two identical searches. CredR and Credilio both score 3.69 for `cred`; they must appear in the same order every time.

---

### Stage E. Return the results

#### Step 13. Honest response

| What | Rule | Today |
|---|---|---|
| Result count | The true number of matches | Always 0 |
| Type label | Every row says Company / Investor / Person / Industry / Report | Mixed |
| Empty query | Instant empty reply | 3.2 s |
| Genuinely nothing found | "No results", with nearest suggestions | "No results" |
| Server error, timeout, overload | A separate error with a retry option. **Never** "No results" | Shown as "No results" |

**Why:** "No results" tells the user the company isn't on DataLabs. If the real cause was a timeout, that's a false and damaging message.

#### Step 14. Client behaviour (app and website)

| Rule | What it means | What it fixes |
|---|---|---|
| **Wait 400 ms** | Search only after the user pauses typing for 0.4 s | `cred` sends 1 request instead of 4 |
| **Cancel old request** | When a new search starts, abandon the previous one | Less wasted server load |
| **Ignore late replies** | Only show results whose query matches what's currently in the box | A slow reply for `cre` can no longer overwrite results for `cred` |

---

## Part 4. Real queries, end to end

### `cred`

| Step | What happens |
|---|---|
| 1 Clean | as typed `cred` · cleaned `cred` · squashed `cred` |
| 2 Short? | 4 letters, OK |
| 3 Alias | None |
| 4–5 Search | CRED → exact (10). CredR, Credilio, CreditVidya → squashed starts-with (6). InCred, OkCredit → `cred` only inside a word, **not matched** |
| 6 Score | CRED 7.80 · CredR 3.69 · Credilio 3.69 |
| 8 Pin | CRED is exact → rank 1 (also CRED as investor, ordered by quality) |
| 9 Dedupe | Nothing to remove |
| 11–12 | CRED, CRED (investor), CredR, Credilio, CreditVidya... |
| **Result** | **CRED 1st.** Today: 11th |

### `iifl finance`

| Step | What happens |
|---|---|
| 1 Clean | cleaned `iifl finance` · 2 words, so squashed levels off |
| 3 Alias | None |
| 5 Match | All words must match. IIFL Finance passes (exact, 10). IIFL Securities, CapitalXB Finance, Avail Finance fail the all-words rule |
| 8 Pin | IIFL Finance exact → rank 1 |
| **Result** | **IIFL Finance 1st.** Today: no results |

And `finance iifl` (reversed): not exact, but both words are whole words in IIFL Finance → level 3 (7 points), passes all-words, others filtered out → **1st**.

### `eternal limited`

| Step | What happens |
|---|---|
| 1 Clean | `eternal limited`; "limited" is a legal suffix |
| 3 Alias | Hit → search runs as `zomato` |
| 5 Match | Zomato → exact |
| 8 Pin | Rank 1 |
| **Result** | **Zomato 1st.** Today: not found |

### `apax`

| Step | What happens |
|---|---|
| 4 Search | One search, companies and investors together |
| 5 Match | Apax Partners (investor) → whole word "apax" (7). Apaxon Technologies (company) → starts-with only |
| 6–7 Score | Apax Partners 2.72 · Apaxon 2.12. No per-type divide |
| 10 Type weight | Apax Partners 2.72 × 0.9 = 2.45 · Apaxon 2.12 × 1.0 = 2.12 |
| **Result** | **Apax Partners 1st.** Today: no rows, sends to an investor filter |

### `sequioa` (typo)

| Step | What happens |
|---|---|
| 5 Match | No exact, whole-word or starts-with match. Typo level (2) matches Sequoia, and also Sequeira (a surname) |
| 5 Sounds-like | Not used: normal matching already found candidates. Zoko ("SK" sound) never enters |
| 6 Score | Everything is at level 2, so **quality decides** |
| **Result** | With investor quality filled in: **Sequoia 1st**. With flat investor quality: 9th. Today: no rows |

---

## Part 5. Open decisions found while writing this

Writing every rule out in full exposed three points the 10 Sep spec leaves ambiguous. Settle these with Ashish before build.

| # | Point | What happens | Options | My recommendation |
|---|---|---|---|---|
| 1 | **Pin on squashed exact for multi-word queries** | The 10 Sep spec pins "cleaned exact **or** squashed exact". For `third wave`, squashed `thirdwave` equals the company **ThirdWave**, so ThirdWave would be pinned above Third Wave Coffee | (a) pin squashed exact only for one-word queries · (b) pin for all | **(a).** Consequence: `of business` finds OfBusiness via matching, not a pin. In simulation it's 1st, but narrowly (1.89 vs 1.72 for Indian School of Business) |
| 2 | **Mid-word matches are dropped entirely** | `rocket` will not return Shiprocket. `cred` will not return InCred. Today both appear | (a) accept · (b) add a lowest level for mid-word matches, below description | **(a) for launch.** Fixes the `ola` → Chocolate problem cleanly. Revisit if users search brand fragments |
| 3 | **Sounds-like: last resort vs always-on with guards** | The 10 Sep spec says last resort (only when nothing else matched). The simulation ran it on every search with the two other guards | (a) last resort · (b) always, with guards | **(a).** Simpler and safer. Result is the same on the 22 test queries |

---

## Cheat sheet

| Step | One line |
|---|---|
| 1 Clean | `CRED`, `cred.`, `cred` are one query. `byju's` = `byjus` |
| 2 Stop empty | No search for empty; "type 3+ characters" for short |
| 3 Alias | Eternal Limited → Zomato |
| 4 One search | All 5 types in one index, one search, no early limits |
| 5 Ladder | Exact 10 > squashed exact 9 > whole word 7 > squashed starts-with 6 > starts-with 5 > typo 2 > sounds-like 1 > description 0.5. Best level only. All words first |
| 6 Score | Points × shorter-name factor × quality (pre-computed) |
| 7 No divide | Never rescale each type to its own top |
| 8 Pin | Exact name is always 1st |
| 9 Dedupe | One row per real entity |
| 10 Type weight | Company 1.0 > Investor 0.9 > Person 0.8 > Industry 0.6 > Report 0.5, tie-breaker |
| 11 Limits | 5/3/3/2/2, applied after pin and dedupe; show 10 |
| 12 Stable sort | Equal scores ordered by ID |
| 13 Response | True count, type labels, errors ≠ "no results" |
| 14 Client | Wait 400 ms, cancel old, ignore late replies |
