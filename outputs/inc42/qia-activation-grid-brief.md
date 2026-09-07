# QIA × Activation — Go-to approach + edge-case grid

**Date:** 7 Sep 2026 · **Owner:** Ranjith · **Status:** brief for agreement (stop before deeper docs)  
**Sources:** [Product & Data Wispr](https://notes.wisprflow.ai/shared/RfVfAWrzO_CNoDncsE8toJ7p--KhptrNor8RpV3oVwo) · [One Inc42 Wispr](https://notes.wisprflow.ai/shared/3Az2qajH1uA3bw1PGs9baJmVzPegPKOACXWKlX-NkOs) · [Audience metric doc](https://docs.google.com/document/d/1iwXO6icFGvPCUIi7N4WBRMev63yyLZAFBYNQ_W0z-1U/edit)

---

## 1. Contradictions to resolve (today)

| Topic | One Inc42 (AM) | Product & Data (midday) | Ranjith metric doc (7 Sep) |
|---|---|---|---|
| Activation shape | Push for **one** Inc42-wide activation (CIO cost fear) | **Product-specific** for now; no unified activation yet | Mostly silent on activation gate |
| Does QIA need activation? | QIA = qualified + identified + activated (7d, any of 10) | **Yes:** activated on **≥1 surface** to count as QIA | Three levels IA → QIA → Repeat; **no activation row** in the table |
| Window | Activation **7 days** (locked in that room) | Same 7d activation framing | **IA / QIA reporting = 15 days** (data: 92% Media / ~99% App repeats by d15) |
| What “qualified” means | Seniority-shaped language in the room | Unchanged name; activation is the new gate | **Persona / ICP fit** of any product (not VP+ only); students/juniors stay in IA |
| What we steer by | Unresolved (parked to Wednesday) | Build QIA×activated×active **grid** | **Steer IA + Repeat now**; report QIA; steer QIA when base ~**1,000** |
| Cross-product | One onboarding / one nav ambition | App-activated on DataLabs web: tweak CIO copy, don’t re-qualify as cold | Cross-promo is a **dependency** of QIA (else sellable is theoretical) |
| Infotude / Media depth | — | Tentative activation = **2+ articles**, needs retention check | Criterion #1 (read-to-depth) **dead on web** until scroll restored |
| Backfill | — | Historical activation **unknown** → backfill baseline **higher** than forward | Full identified bar (email+title+company) will **drop** today’s IA numbers |

**Marketing “QA” vs product Identified Actives:** warehouse / campaign QA often means “reachable / mailed / engaged.” Product **IA** here means named person + qualifying action in-window. Do not mix labels in the same dashboard without a subtitle.

---

## 2. Recommended go-to (aligned to current planned setup)

Keep the **QIA name**. Do **not** invent a second north-star brand.

### Stack (one person, one ID)

1. **Reach** — anyone seen (mostly anonymous). Published next to IA so gating can’t fake progress.  
2. **Identified Actives (IA)** — email + job title + company (doc §6) **and** ≥1 qualifying action in the **reporting window**. Operating focus **today**.  
3. **Activated** — product-specific first-session / early-habit gate (below). Required for QIA.  
4. **QIA** — IA who are **activated on ≥1 surface** **and** match **ICP of any Inc42 product** (persona fit table in the doc; not “VP+ only”).  
5. **Core QIA** (report line, optional steer later) — QIA in **proven-buyer** segments (Media: Founder/CXO/Senior; DataLabs: Investor / Sales & Marketing).  
6. **Repeat Rate** — integrity check on IA (and later on QIA). Never mix 7/15/30 in one chart.

### Windows (proposed reconciliation)

| Layer | Window | Why |
|---|---|---|
| **Activation** (product-specific) | **7 days** from identify / signup | Locked in One Inc42; 70%+ / 96% App activate in 7d |
| **IA / QIA / Repeat reporting** | **15 days** | Doc evidence; avoid Media looking “broken” under 7d |
| Warehouse north-star (legacy QIA-30) | Keep labeled **QIA-30 warehouse** separately | Never mix with PostHog IA-15 |

If Wednesday wants one window only, pick **15 for reporting** and keep **7 as the activation SLA** (same person can be “activated” day 3 and still sit in IA-15).

### Product-specific activation (v1)

| Surface | Activation (draft) | Notes |
|---|---|---|
| **App** | Existing App activation (brief / content action in 7d) | Already ~96% of signups in 7d |
| **DataLabs** | Any one of: company profile view, search completed, advanced/filter search, watchlist/alert, Ask (when piped), trial/pay | Align to Utkarsh’s 10 where instrumented |
| **Media / Infotude** | **Interim:** 2+ article opens **or** newsletter click **or** search completed in 7d. **Target:** restore scroll → “read to depth” becomes primary | Validate 2+ articles vs retention before locking |
| **IP** | Application started / completed or ticket purchase | Senior gate is ICP, not activation |

**Unified activation:** defer until One Inc42 identity + combined CIO workspace exist. Until then: **OR across surfaces** (“activated somewhere”), never AND.

### Operating rules

- **Steer:** IA-15 + Repeat-15 until QIA clears ~1,000.  
- **Report:** QIA every week with activation gate + ICP.  
- **CIO:** one journey per **surface activation**, not 10×4. Cross-surface: if already QIA, show “welcome back / continue” not cold onboarding.  
- **Job title** stays mandatory: Media seniority alone cannot route Sales & Marketing → DataLabs.

---

## 3. Edge-case grid — what we DO

Legend: **IA** = Identified Active · **Actv** = activated on ≥1 surface · **QIA** = Actv + ICP · **CIO** = messaging / workspace behaviour.

### A. Identity × activation × activity (primary)

| # | Identified? | Activated (≥1)? | Active in window? | ICP fit? | Count as | Operational move |
|---|---|---|---|---|---|---|
| 1 | No | — | Yes (anon) | — | **Reach only** | No CIO person journey. Grow identify (gate carefully; publish reach). |
| 2 | Yes | No | No | — | Named dormant | Win-back / complete-onboarding. **Not IA, not QIA.** |
| 3 | Yes | No | Yes | No | **IA** (audience / out-of-market) | Serve content. Students/juniors stay here. No QIA dashboards. |
| 4 | Yes | No | Yes | Yes | **IA — activation leak** | **Priority nudge:** surface-specific activation CTA. Do **not** count QIA yet. |
| 5 | Yes | Yes | No | Yes | **QIA dormant** | Lifecycle: dormant/lapsed buckets (post-7d with Animesh/Amit). Re-activation, not re-qualify. |
| 6 | Yes | Yes | Yes | Yes | **QIA (and IA)** | Full product + cross-promo to other ICP products. |
| 7 | Yes | Yes | Yes | No | **Activated IA, not QIA** | Keep serving; no “sellable” campaigns that assume ICP. |
| 8 | Yes | Unknown (legacy) | Yes | Yes | **IA + provisional QIA\* ** | \*Backfill: report **forward QIA** (known Actv) and **legacy QIA\*** separately. Never blend in one KPI. |

### B. Cross-surface edges

| Case | Count | Do |
|---|---|---|
| **App-activated, first visit DataLabs web** | Still **QIA** if ICP; Actv = yes (App) | CIO: recognised QIA state. Soft DataLabs tour / PDF incentive. **Do not** force DataLabs activation to keep QIA. Optionally track **surface-activated[DL]=false** for product ops only. |
| **Media signup, never activated** | **IA** if action+identity; **not QIA** | Activation campaign on Media (search / 2nd article / newsletter click). |
| **Activated Media only; ICP = Investor (DataLabs-shaped)** | **QIA** | Cross-promo DataLabs heavily. Function from job title required. |
| **Multi-product activated** | **QIA** once | Dedup by person. Optional badge: surfaces activated = {App, DL}. Combined workspace gets **qualified actions only**. |
| **Active on surface B, activated only on A** | Active contributes to **IA** if identified; **QIA** if Actv(A) + ICP | Do not require Actv(B). Product team may still chase Actv(B) as a **local** activation rate. |
| **Anonymous → identified mid-journey** | Stitch when possible; else start Actv clock at identify | Volume events stay in property workspaces; qualified actions → combined workspace. |
| **Infotude / Media with scroll dead** | IA/Actv under-count “readers” | Instrument interim Actv; **pre-announce** scroll restore so metric jump ≠ growth. |
| **Newsletter-only “subscriber” (no title/company)** | Not full **IA** under doc §6 | Enrichment / re-ask. Reachable in CIO but **outside IA/QIA** until fields exist. |
| **Historical unknown activation** | See row 8 | Forward metric is source of truth for goals. Legacy line for narrative only. |

### C. Quick “manager view”

| Question | Answer |
|---|---|
| North star name? | **QIA** (unchanged) |
| What teams optimise this month? | **IA-15 + Repeat-15** (+ activation conversion on leaks) |
| Who is sellable? | **QIA** (and Core QIA when we slice) |
| Unified vs per-product activation? | **Per-product definitions; OR across surfaces for QIA gate** |
| Seniority vs persona? | **Persona / ICP fit (doc table)**; seniority alone is insufficient for DataLabs routing |

---

## 4. Ask (stop here)

Agree / amend:

1. Activation = **product-specific**, QIA needs **Actv on ≥1**, reporting window **15d**, activation SLA **7d**.  
2. Steer **IA** until QIA ~1,000; always **split forward vs legacy** activation.  
3. Media interim Actv = **2+ articles OR newsletter click OR search** pending scroll + Infotude analysis.  
4. Core QIA as a **report slice**, not a second north star.

**Out of scope until you say go:** full warehouse SQL, Asana tickets, CIO journey map, Infotude retention study write-up.
