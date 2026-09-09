# Inc42 North Star — QIA (and what we measure)

**Status:** Working lock for Product, Data, Marketing, Lifecycle  
**Date:** 10 Sep 2026 (rev 2 — Ranjith inputs)  
**Sources:** Product & Data Sync 9 Sep 2026; User Qualification 8 Sep 2026; Ranjith North Star rewrite inputs 10 Sep 2026; Utkarsh ask for one short shared write-up  
**Rule:** One short doc. Do not spawn parallel metric briefs.  
**Supersedes:** earlier North Star draft `1LIr4MKLCOj2YV-kJqp68bHOk6n2GUFWhfBlePmSIDPY` and any QIA-15 ops framing.

---

## 1. Why this exists

Inc42 runs Media, DataLabs, and App as one audience with one person ID. Teams mixed three ideas under one label:

1. Did we **identify** them?
2. Did they get **product value early** (activation)?
3. Are they a **sellable, engaged** person in-window (QIA)?

This note locks names, the full qualifying-action list, what we ask vs enrich, windows, and how Media “3+ articles” is counted in the database.

---

## 2. Ladder

| Layer | Name | Definition | Window / shape |
|---|---|---|---|
| 0 | Reach | Seen / visited (often anonymous) | Period traffic |
| 1 | Identified | Signed up + required onboarding fields | Snapshot |
| 2 | Activated | Platform first aha after identify | Cohort from identify (typically ≤7d) |
| 3 | **IA** | Identified + ≥1 of the **10 qualifying actions** | Rolling stock (7d and 30d) |
| 4 | **QIA** | IA + **Qualified** (Senior Manager+) | **QIA-7** and **QIA-30** only |
| 5 | **QIA Core** | QIA + higher bar (VP+) | Same windows; report slice |

**No QIA-15.** Board / warehouse numbers are **QIA-7** and **QIA-30** only.

---

## 3. Identified — what we ask vs what we enrich

### 3.1 Must ask (onboarding)

| Field | Notes |
|---|---|
| Email / mobile (as today) | Identity spine |
| First name / last name (as today) | |
| **Company name** | Must ask; enrichment key |
| **Designation** (job title) | Must ask; **seniority is derived from this** |
| **Role** | Must ask as well (separate from designation) |
| **Sector** | Must ask (cannot fully enrich interest) |
| **Topic** interest | Must ask |

Persona as its own field stays deferred until activation / personalization journeys need it.

### 3.2 Derived / enriched (do not bloat the form)

**From designation**

- **Seniority band** (Senior Manager+, VP+, etc.) used for QIA / QIA Core

**From company name** (enrich, do not ask)

- Company type / nature  
- Employee count / company size  
- Industry / sector of the company (firmographic)  
- Other firmographics available from enrichment (e.g. stage / funding where present)  

Enrichment is real-time or warehouse reverse-ETL; users can correct pre-fills later if we show them. Do not ask the full firmographic set in onboarding.

**Identified bar:** required ask fields present (including company + designation + role + sector + topic). App gaps on company remain a known parity issue until the field ships everywhere.

---

## 4. Qualified (the “Q”)

Common bar across products (not three product-specific ICP tables):

| Slice | Bar |
|---|---|
| **QIA** | **Senior Manager and above** (from designation → seniority) |
| **QIA Core** | **VP and above** |

Current preference: seniority **irrespective of company type** for v1. Company-type overrides (e.g. special analyst rules) stay an open edge; do not block the North Star.

Out of QIA: below Senior Manager (junior / intern / student-style bands).

---

## 5. The 10 qualifying actions (IA / QIA Active rung)

Any **≥1** of these inside the reporting window completes the Active rung for **IA** and (with seniority) **QIA**. List is Utkarsh’s set (revised 26 Aug). Keep this list in this document; do not redefine QIA without updating this table.

| # | Qualifying action | Notes |
|---|---|---|
| 1 | Article read to **depth** | Opened **and** depth-qualified (not open-only) |
| 2 | Profile / database record view | Media / DataLabs / App |
| 3 | Search **completed** | Query submitted; “search active” / focus alone does not count |
| 4 | Advanced or filtered search | Especially DataLabs |
| 5 | Watchlist / saved search / alert | |
| 6 | Ask / AI query | DataLabs; App Ask telemetry may lag |
| 7 | App session with ≥1 **content** action | Not bare open |
| 8 | Newsletter **click** | Never email **open** |
| 9 | Event application / registration | |
| 10 | Payment or renewal | |

**Never count as a qualifying action:** email opens, push receipts, bare login, screen-arrival only (`brief_page_opened`, `explore_viewed`, `card_viewed`, etc.), staff, bots.

---

## 6. Activation (product aha — parallel to QIA)

Activation ≠ the Active rung inside QIA. Activation = first meaningful product experience **from identify**, per surface.

| Surface | Activation | Notes |
|---|---|---|
| **App** | **Brief completion** | App-only aha |
| **Media** | **3+ distinct articles with depth** | See §7 for database rule |
| **DataLabs** | **Advanced / filtered search**, and/or **Ask M42** | Ask M42 as activation still **open** to confirm |

Chase as **% of new IDs** in the activation window (typically ≤7d from identify). Product health input; not a rename of QIA. Someone can be **QIA and not platform-activated** (e.g. newsletter click + Senior Manager+).

---

## 7. How we measure Media “3+ articles” in the database

Definition only works if instrumentation matches it.

**One qualified article (person × article)** requires:

- Stable `person_id` (identified)  
- Stable `article_id` (not raw URL with junk query params)  
- `timestamp`  
- Depth signal: `depth_pct ≥ threshold` (working target **60%**) **or** boolean `depth_qualified`  
- Prefer one qualifying row per person × article (dedupe re-opens)

**Media activated (cohort):**

```
media_activated =
  count distinct article_id
  where person is Identified
    and event is depth-qualified article read
    and timestamp in [identify_at, identify_at + 7 days]
  ≥ 3
```

Same shape in PostHog (HogQL / cohort) or warehouse SQL.

**Coverage rule:** until web scroll depth is joined to identity, treat Media Actv as **partial** (App + joined web only). Do not publish a fake-complete Media Actv. Do not fall back to “3 opens” without labeling it **interim**.

---

## 8. What QIA means (one paragraph)

**QIA** = **Identified** + **≥1 of the 10** in-window + **Senior Manager+** (seniority from designation).  

**QIA-7 / QIA-30** = rolling stock of distinct people over 7 or 30 days.  

**QIA Core** = same with **VP+**.  

**IA** = Identified + ≥1 of the 10, **no** seniority gate.

---

## 9. What we measure (scoreboard)

### Company

| Metric | Role |
|---|---|
| **QIA-7** | Primary North Star stock |
| **QIA-30** | Always labeled; warehouse / longer narrative |
| **QIA Core-7 / 30** | VP+ slice |
| **IA-7 / 30** | Broader identified-engaged stock |

### Short-term chase (QIA base still small)

1. **Identification** (ask fields complete, including role + company + designation)  
2. **Activation** per surface among new IDs  

Report QIA weekly; steer Identify + Activate until the QIA base is real, then lean on **QIA-7** growth.

### Product inputs

| Team | Primary |
|---|---|
| App | Brief completion ≤7d from identify |
| Media | 3+ distinct depth-qualified articles ≤7d from identify |
| DataLabs | Advanced search (Ask M42 once locked) ≤7d from identify |
| Marketing | Identified + Qualified volume; channels → QIA |
| Lifecycle | Repeat among QIA (secondary) |
| Warehouse | Publish QIA-7 / 30 / IA / Core with clear labels |

---

## 10. Naming hygiene

| Say | Mean |
|---|---|
| Activation | Platform first aha from identify |
| Qualifying action / IA | One of the 10 in-window |
| QIA-7 / QIA-30 | Senior Manager+ + IA stock |
| QIA Core | VP+ slice |

Prefer full phrases in meetings: **“platform activation”** vs **“QIA-7”**.

---

## 11. Open items

1. Confirm **Ask M42** as DataLabs activation yes/no.  
2. Lock **depth %** (working 60%) and ship web scroll → person join.  
3. Optional company-type seniority overrides later.  
4. Baseline benchmarks once warehouse numbers are trusted.  
5. Role field: free text vs controlled list (product/design to specify in onboarding).

---

## 12. One-line OS

**Ask company + designation + role + sector + topic → enrich firmographics and seniority → Identify → Activate per product → grow QIA-7. Report QIA-30 and Core. Never QIA-15.**

---

## Appendix — sources

- Product & Data Sync, 9 Sep 2026: https://notes.wisprflow.ai/shared/8AUasqKEdb7ASoQcXtJVIYqQH_AFQxtBiM0V_gEeARk  
- User Qualification, 8 Sep 2026: https://notes.wisprflow.ai/shared/DGV2CBC_3TADaDMJAYaW3DeBfJplNf58T1Pk_hsx-xI  
- Ten qualifying actions (Utkarsh, revised 26 Aug)  
- Ranjith rewrite inputs 10 Sep 2026 (role ask; seniority from designation; company enrichment; full 10 in-doc; Media 3+ DB rule)
