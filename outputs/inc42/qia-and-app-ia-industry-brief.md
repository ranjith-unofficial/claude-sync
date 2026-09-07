# QIA + App info hierarchy — industry practice → Inc42

**Date:** 8 Sep 2026 · **Status:** FINAL metric operating model (HOLD implementation)  
**Locks:** Ranjith FINAL via CoS 8 Sep · Windows clarification (Actv ≤7d from Identify · QIA = 15d stock) · Utkarsh 10 (26 Aug)  
**Supersedes:** drafts that (a) gated QIA on platform Actv, (b) defined QIA as ID+ICP with no Active rung, (c) renamed the goal “QIA-activated”, or (d) chased “QIA within 7 days”  
**Sources:** Ranjith FINAL + windows clarification via CoS; P&D / One Inc42 / Wispr; Utkarsh 10 (26 Aug); industry patterns

---

# Part A — Metrics / QIA / activation

## §0 Industry practice

**AARRR split.** Activation = product aha inside a short N-day window from identity. Retention / actives are a different stage. Collapsing activation into the north-star window muddies diagnosis.

**Funnel stages stay distinct.** Reach ≠ Identify ≠ Qualify ≠ Active. Anon = reach; identity fields = identify; ICP = qualify; meaningful product actions = active.

**Qualified list ≠ north star.** Chase **identified + qualified + ≥1 real action**, not a hollow named list.

**First-aha SLA ≠ north-star stock.** Platform first-aha is a **cohort clock from Identify**. The company goal is a **rolling stock** of qualified-actives. Do not force the same window on both just because many people hit an action inside 7d — that is a behavioral fact, not a metric design rule.

**North star vs inputs.** One named north star (company chase) + secondary product inputs (platform Actv). ~1,000 person floor before over-steering the north star.

**Backfill.** Forward cohorts = goal truth; legacy unknown Active reported separately.

## §1 Implication for Inc42

| Industry rule | What it means here |
|---|---|
| Reach ≠ Identified | Anon = **Reach**. Identified = email + job title + company |
| Qualified ≠ QIA | ICP alone = **Qualified** — not yet QIA |
| QIA needs real action | **QIA = Identified + Qualified (ICP) + ≥1 of Utkarsh’s 10**. **Company chase = QIA (15d stock)** |
| Platform Actv is parallel | **Product chase = platform Actv ≤7d from Identify**. **Not a QIA gate** |
| Do NOT collapse windows | **Never chase “QIA within 7 days.”** That collapses Actv into QIA |
| Don’t rename the goal | Primary = **QIA**. Do **not** rename to “QIA-activated” |
| Report shape | **QIA** primary · **platform Actv rates among new IDs** secondary · optional slices |
| Forward vs legacy | Unknown historical Active → separate line |

## §2 Recommendation (Inc42) — FINAL

Keep **QIA** as the north-star name. **Company chase = QIA (15d).** **Product chase = platform Actv ≤7d.**

### Ladder (locked)

```
Reach → Identified → Qualified → (Active via ≥1 of Utkarsh’s 10) = QIA   ← 15d rolling STOCK

         Activate ≤7d FROM IDENTIFY (per platform, parallel) → Engage/Active
```

- **Reach:** anon actives / installs / pageviews (never fold into Identified)
- **Identified:** email + job title + company
- **Qualified:** ICP / persona fit of any Inc42 product. Seniority-only is not enough.
- **Active (QIA rung):** ≥1 of the **10 actions** below (inside the **QIA window** below)
- **QIA:** Identified + Qualified (ICP) + ≥1 of 10. **Not** ID+ICP alone. **Not** platform-Actv-gated.
- **Activation ≤7d (parallel product chase):** platform first-aha, clocked **from Identify**. Per-platform flags; OR = activated somewhere. **Not** a QIA requirement.
- **Engage/Active (retention):** longer retention — separate from QIA Active rung and ≤7d Actv.

### Windows (locked — critical)

| Metric | Window | Clock / shape | Chase |
|---|---|---|---|
| **Platform Activation** | **≤7 days** | **From Identify** (cohort). Platform-specific aha | **Product chase** |
| **QIA** | **Rolling 15d STOCK** | Who is QIA now (ID + ICP + ≥1 of 10 in the stock window) | **Company chase** |
| **QIA-30** | 30d | Warehouse only — **always label** QIA-30 | Report / warehouse, not ops chase |

**Do NOT chase “QIA within 7 days.”** That collapses metrics.

**Behavioral fact ≠ window design:** ~70% doing a 10-action inside 7d is interesting behavior. It is **not** a reason to set the QIA window = 7.

**Always publish:** **QIA** (primary, 15d stock). Secondary: platform activation rates **among new IDs** (≤7d from Identify). Optional slices. Do **not** rename the goal to QIA-activated.

### The 10 actions that count as Active for QIA (Utkarsh, 26 Aug)

Any **≥1** of these completes the Active rung (with Identified + Qualified → QIA):

1. Article depth  
2. Profile / DB  
3. Search completed  
4. Advanced / filtered search  
5. Watchlist / alert  
6. Ask  
7. App session with ≥1 content action  
8. Newsletter click  
9. Event apply  
10. Payment  

**Never count as Active / Actv:** opens, login, screen-arrivals.

### Activation ≤7d from Identify (product chase — not a QIA gate)

| Surface | Activation (≤7d from Identify) | Notes |
|---|---|---|
| **App** | **Brief completion ONLY** | Unique App metric. Do **not** count 3 article reads as App Actv |
| **Media** | **3 article reads** | Web **or** in-App → **Media** Actv |
| **DataLabs** | DL aha from the **instrumented 10** | Local health; subset of the 10 |
| **IP** | application / ticket (draft) | Local health |

### Critical edges (locked examples)

| Case | App Actv | Media Actv | QIA? | Notes |
|---|---|---|---|---|
| ID+ICP, Brief day 2, maps to one of 10 | **Yes** | No | **Yes** | Product Actv ≠ QIA gate; Brief can satisfy a 10 |
| Newsletter click, ID+ICP, no Brief / no 3-article | No | No | **Yes** (if click is the ≥1 of 10) | **QIA without App/Media Actv** is allowed |
| ID+ICP, **0 of 10** | maybe | maybe | **No** (Qualified only) | Not company chase yet |
| ID+ICP + ≥1 of 10, no Brief / no 3-article | No | No | **Yes** | Still QIA; secondary nudge platform aha |
| Identified, ICP no (e.g. student) | maybe | maybe | **No** | Serve; never QIA |
| Anon active | — | — | No (Reach) | Identify carefully |
| Legacy Active unknown | provisional | provisional | provisional | Split forward vs legacy |

**Steer now:** grow the **15d QIA stock** (ID → ICP → ≥1 of 10). Separately improve **platform Actv ≤7d from Identify** among new IDs (Brief / 3-article / DL aha). **CIO:** journeys that land a real 10 for Qualified users; already-QIA get recognised / continue.

**Ask A (FINAL):** Confirm ladder + windows above; company chase = QIA 15d; product chase = Actv ≤7d from Identify; never “QIA in 7d”; App Actv = Brief only; Media = 3 articles web/in-App; do not rename goal; steer until ~1k QIA.

---

# Part B — App info hierarchy (News vs Companies)

## §0 Industry practice

**Content feed vs entity directory.** Separate editorial feed from entity directory; hybrid Explore mixes both and fails.

**Nav budget.** High-frequency jobs on primary tabs; bury low-usage (~15% Watchlist) under Profile; keep mid habit (Streak) visible until new tabs prove out.

**Ritual surfaces** off browse critical path until open-rate is healthy; still instrument when the ritual **is** the platform aha.

**Search.** One global entry; context-biased ranking; rarely its own tab.

## §1 Implication for Inc42

| Industry rule | What it means here |
|---|---|
| Split feed vs directory | Explore → **News** + **Companies** |
| Bury low-usage | Watchlist ~15% → **Profile** |
| Keep mid habit | Streak stays top-level |
| Ritual off nav critical path | Don’t block 15 Sep Explore split on Brief redesign |
| Brief = App Actv ≤7d from Identify | Brief completion = App product chase. **QIA** still needs ID + ICP + ≥1 of 10 in the **15d stock** |
| Global search | No Search tab · search completed / advanced search = QIA Active actions (#3–4) |

## §2 Recommendation (Inc42)

**Mental model:** News = stories · Companies = entities · Profile = my stuff · Brief = ritual **and** App ≤7d Actv aha.

**15 Sep tabs (proposed):** News · Companies · Streak · Profile. Brief via deep link / overlay — not a 4th browse tab — but **Brief completion instrumentation** must ship as App Actv ≤7d from Identify.

**Placement:** News = story feed; Companies = sections + browse-all; Profile = watchlist; Brief = pack + FOMO after redesign. In-App article reads → **Media** Actv (3-article), not App Actv. Article depth / search / watchlist / Ask / newsletter click feed the **QIA Active** rung when ID + Qualified.

**Ask B:** Confirm News/Companies split, Watchlist in Profile, 15 Sep tabs = News·Companies·Streak·Profile, Brief off Explore critical path while Brief completion = App Actv ≤7d from Identify.

---

# Combined asks (stop here)

1. **QIA = Identified + Qualified (ICP) + ≥1 of Utkarsh’s 10.** Company chase = **QIA (rolling 15d stock)**. Not hollow named list. Do not rename to QIA-activated. **Never chase QIA-within-7d.**  
2. **Product chase = platform Actv ≤7d FROM IDENTIFY:** App = Brief only · Media = 3 articles (web or in-App) · DL = instrumented-10 aha. Report Actv rates among new IDs secondary. Newsletter click can be QIA without App/Media Actv.  
3. **App IA:** News vs Companies · Watchlist in Profile · Streak kept · Brief not primary tab for 15 Sep.  
4. **QIA-30** = warehouse only, always labeled.

**Out of scope until agree:** warehouse SQL, Asana, CIO journey maps, Infotude study, Brief FOMO build, v3 company UX.
