# Inc42 App — Search Defects

**Filed:** 23 Aug 2026 · **Owner (proposed):** Ritvik Sethi · **Surface:** Explore → Search (Companies + Articles)
**Data source:** PostHog project `Inc42 App` (146258, EU), events 11–23 Aug 2026, `@inc42.com` excluded

---

## Summary

In-app search fails on **19.5% of completed company searches** and **27.0% of completed article searches**. The failures are not edge cases — they include correctly spelled names of companies Inc42 actively covers.

Separately, `search_performed` fires **on every keystroke**, which has inflated every search metric reported to date by roughly 3x.

**Scale:** 27 users ran 87 completed company searches (3.2 each); 24 users ran 37 completed article searches. Search is the second-heaviest company-discovery path in the app after the unfiltered list — ahead of every filter pill.

---

## BUG 1 — `search_performed` fires per keystroke

**Severity:** High (data integrity — corrupts all search reporting)

One user typing `green hydrogen` generated **8 separate events**:

```
green → green e → green h → green hy → green hyd → green hydr → green hydro → green hydrog
```

### Impact on reported numbers

| Metric | Reported (raw) | Actual (completed intents) |
|---|---|---|
| Company searches | 277 | **87** |
| Article searches | 77 | **37** |
| Company zero-result rate | 32.5% | **19.5%** |
| Article zero-result rate | 37.7% | **27.0%** |
| Avg results returned (companies) | 13.9 | 14.7 |
| Avg results returned (articles) | 2.6 | 3.3 |

**354 recorded "searches" are really 124 real searches.**

Every prior search figure is affected, including the 42% / 28.5% zero-result rates in the 17 Aug PostHog review.

### Fix

- Fire `search_performed` on **debounce (≥400ms idle) or explicit submit**, not per character.
- Add a distinct `search_typed` event if keystroke-level telemetry is genuinely wanted — do not overload the same event name.

### Acceptance criteria

- One completed search intent produces exactly one `search_performed` event.
- Event carries: `query`, `search_scope`, `result_count`, `latency_ms`.

---

## BUG 2 — Zero-result searches

**Severity:** High (user-facing, on the app's primary lookup path)

Complete list of **completed** search intents returning 0 results, 11–23 Aug.

### 2a. Correctly spelled, real companies returning 0 — INDEX COVERAGE

| Query | Scope | Notes |
|---|---|---|
| `airbound` / `air bound` | companies | Real company, both spellings fail |
| `birdeye` | companies | Real company |
| `iifl finance` | companies | Major NBFC |
| `lava mobile` | companies | Real company |
| `lava international` | articles | Correct legal name |
| `ofbusiness` | articles | Unicorn, heavily covered by Inc42 |
| `myjar` | articles | Real company (Jar) |
| `speciale` | companies | Speciale Invest |
| `tbotek` | companies | TBO Tek — listed company |

**This is the most serious finding.** These are not typos. Either the search index is stale/partial versus the DataLabs company set, or article search is not indexing company names in body/title.

### 2b. Topic and theme searches returning 0 — NO TOPIC SEARCH

| Query | Scope |
|---|---|
| `green hydrogen` | companies |
| `carbon credit` | companies |
| `deepfake` | articles |
| `youtube` | companies |

Search appears to be **exact-entity only**. Users searching themes get nothing, even where Inc42 has extensive coverage (deepfake, carbon credits). Note the demand pattern: the strongest theme cluster in all app search is **cleantech/deeptech** — green hydrogen, carbon credit, BESS, battery, defence, EMS.

### 2c. Prefixes returning 0 — NO PREFIX MATCHING ON ARTICLES

| Query | Scope | Intended |
|---|---|---|
| `shipr` | articles | Shiprocket |
| `bandma` | articles | Bandhan / Bandma |

Company search does prefix-match (`shipr` returns 14 results under `companies`). **Article search does not.** Inconsistent behaviour between the two tabs of the same search box.

### 2d. Typos returning 0 — NO FUZZY MATCHING

| Typed | Intended |
|---|---|
| `humgerb` | HungerBox |
| `taga motors` / `taga motos` | Tata Motors |
| `trancxn` / `transxcn` | Tracxn |
| `aitmc veb` | AITMC Ventures |
| `evigway` | EV Gway |
| `suto` | (auto?) |
| `wheelse6wll` / `wheelsey3` | Wheelseye |

Single-character transpositions return nothing. No "did you mean".

### 2e. Junk input

| Query | Scope | Note |
|---|---|---|
| `review.inc42@gmail.com` | articles | Email pasted into search — likely an app-store reviewer account |

---

## Proposed fixes, in priority order

1. **Audit index coverage** — reconcile the app search index against the DataLabs company set (75K companies). Confirm `airbound`, `birdeye`, `iifl finance`, `lava`, `tbo tek`, `speciale` resolve. *Highest value: these are outright misses, not ranking problems.*
2. **Add fuzzy matching** — Levenshtein distance ≤2, or trigram similarity. Covers 2d entirely.
3. **Add prefix matching to article search** — bring it to parity with company search. Covers 2c.
4. **Add topic/keyword search over article body + tags** — covers 2b.
5. **Fix the keystroke event** — covers Bug 1.
6. **Add a real zero-result state** — currently a blank result set reads as "the app is broken". Should offer: nearest fuzzy matches, a "search the other tab" switch, and a fallback to Inc42 web search.

## Acceptance criteria

- Every one of the 27 queries listed in §2a–2d returns ≥1 relevant result, or an explicit "no match — did you mean X?" state.
- Zero-result rate on completed intents drops below 8% for companies and below 12% for articles.
- Article and company search behave identically with respect to prefix matching.
- `search_performed` fires once per completed intent.

---

## Related defects found in the same sweep (separate tickets)

| Defect | Detail |
|---|---|
| `deep_link_opened` polluted | 129 of 259 events are `onboarding/auth/callback` — the OAuth redirect, not a deep link |
| Dev traffic in production | 6 users / 717 events with `$is_emulator = True`, iOS Simulator against `192.168.1.x:8083`. Add an exclusion cohort on `$is_emulator` |
| `company_profile: not_found` | 17 events, 9 users — companies listed but whose profiles 404 |
| No filter instrumentation | No `filter_applied` event; no `results_count` on `explore_viewed`. Filter failures are currently unmeasurable |
| `decode` never fired | Zero events since launch |
| `push_delivered` never fired | 182 users granted permission; zero deliveries in 13 days |

---

## Reproduction query

```sql
-- Completed search intents (keystroke prefixes removed) with zero results
WITH q AS (
  SELECT person_id,
         properties.search_scope AS scope,
         lower(trim(toString(properties.query))) AS term,
         max(toFloat(properties.result_count)) AS res
  FROM events
  WHERE event = 'search_performed'
    AND timestamp >= '2026-08-11'
    AND length(trim(toString(properties.query))) > 1
  GROUP BY person_id, scope, term
),
grouped AS (
  SELECT person_id, scope, groupArray(term) AS terms, groupArray(res) AS resses
  FROM q GROUP BY person_id, scope
),
fin AS (
  SELECT person_id, scope,
         arrayJoin(arrayFilter(
           x -> length(arrayFilter(o -> o != x.1 AND startsWith(o, x.1), terms)) = 0,
           arrayZip(terms, resses))) AS tr
  FROM grouped
)
SELECT scope, tr.1 AS query, tr.2 AS results, count(DISTINCT person_id) AS users
FROM fin WHERE tr.2 = 0
GROUP BY scope, query, results ORDER BY scope, query;
```
