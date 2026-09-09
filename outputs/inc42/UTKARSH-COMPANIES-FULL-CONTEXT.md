# Utkarsh × Companies — full context pack (for Claude)

**Compiled:** 10 Sep 2026 IST · **Owner:** Ranjith / Product Manager  
**Scope for further logic:** Companies section only (Discover vs Browse, rails, tags, cards).  
**Safety:** This file is additive. Nothing was deleted from existing notes.

---

## 1. Source discussions (read these)

| When | What | Link / path |
|---|---|---|
| 9 Sep ~7:40–8:40 PM IST | Design review — Discover vs Browse split, freshness | https://notes.wisprflow.ai/shared/c7L16n7CW-x2RBrpWNvKSBlNGxSKXiKR5REctRtsFpU · meeting `975a26fb-2073-4fe5-b608-6b468c299bba` · local extract `/workspace/inc42-handover/_740pm_transcript.txt` (Companies block ~L274–384) |
| 8 Sep ~8:30–9:30 PM IST | Product review — company filters/tags, card fallback hierarchy | https://notes.wisprflow.ai/shared/DTaRM87dcU4OIcdOWYmtkDtG2SAiV7pSkRpzMXkH50Y |
| 9 Sep 12:30 IST | Product & Data Sync — tags, profitable, IPO, top-10→top-3 | https://notes.wisprflow.ai/shared/8AUasqKEdb7ASoQcXtJVIYqQH_AFQxtBiM0V_gEeARk |
| 8 Sep Slack | Ranjith → Utkarsh: company hierarchy + Claude artifact | DM thread on One Inc42 / company page |
| 8 Sep ~11:58 PM | Ranjith → Satya (+Utkarsh) MOM: article/company card design feedback | Group DM |
| 9 Sep Slack | Prapti: company tags inventory + editorial series defs + cadence | DM Prapti |

Prior IA (Companies sectional home + browse-all already framed):  
- `app-info-hierarchy-brief.md`  
- `CLAUDE-HANDOFF-app-info-hierarchy.md`  
- Working lock draft: `companies-discover-vs-browse.md`

---

## 2. What Ranjith showed / proposed to Utkarsh

### Early hierarchy (8 Sep Slack)
Company screen shelves proposed:
1. Recently Funded  
2. Just Launched  
3. Early Fundraisers  
4. Profitable Startups  
5. Unicorns  

Claude artifact shared: company page data preview (a316a3a8…).

### Themes on Discover (9 Sep design review screen-share)
Ranjith framed a **generic / Discover** page for “must know” themes, e.g.:
- Profitable Startups  
- 30 Startups To Watch  
- AI Startups  
- IPO Pipeline  

And a separate **Browse all ~70k** page = existing Explore companies, with quick filters (Unicorn, Recently Funded, Fintech, etc.).

**Ranjith’s instinct (later):** move Recently Funded off Discover into Browse as a quick filter.  
**Utkarsh’s pushback (treat as lock):** Recently Funded (and “in the news” style rails) should stay on **Discover**, or the feed stays static and recirculates the same ~20 companies.

---

## 3. Utkarsh locks / pushbacks (Companies)

### 3.1 Discover vs Browse split
- **Discover (NEW):** curated / happening / discovery — must stay **fresh**.  
- **Browse / All companies (EXISTING Explore companies tab):** full database + quick filters.  
- Entry to Browse must stay findable (hierarchy concern; OK for now, revisit later).  
- Hypothetically later: explicit toggles “Discover companies” / “All companies” (food for thought).

### 3.2 Freshness > static editorial heroes
- Primary Discover interest: **Recently Funded**, **In the News**, latest rounds — keeps feed alive.  
- Challenge with only regular curated lists: same ~20 companies recirculate.  
- **30 Startups To Watch:** fine as *manually dynamic* — every month new edition; for **first ~1 week** after launch, that tag becomes higher / more prominent.  
- Build a **calendar** with Marketing + Data (later): series launches (e.g. manufacturing startups) → that tag prominent for next few days.  
- **Recently Funded is always prominent** — “that always works.”  
- Static information gets boring.

### 3.3 Seasonal / filings
- From ~Oct–Nov (filings season): **new financials** / companies whose financials are coming out / growth-stage filings can be a dynamic Discover section.  
- Also around quarter ends for listed companies’ earnings.

### 3.4 Company filters & tagging (8 Sep review)
- IPO pipeline needs **manual tagging**; DataLabs lacks full dataset; Enterprise team has tracker. Deferred good-to-have.  
- Editorial tags planned: Minicon, Soonicorn, Unicorn, hot early-stage, hot AI.  
- **Profitable startups** filter capped ~**60** by design (>10cr revenue, >90% margin) so corporates don’t dominate (Prapti logic). Utkarsh asked why count is low; Ranjith explained.  
- **Just Launched** value prop **needs to be vetted**.  
- Utkarsh also asked about **IPO pipeline and Listed**.

### 3.5 Card data: top-10 hierarchy → show top-3 available
**Locked mechanism (Utkarsh):**
1. One shared **priority-ordered list of ~10 metrics** (not case-by-case per section).  
2. On each card, show the **top 3 that are actually available** (skip missing; no blank slots).  
3. Uneven cards OK — can highlight what’s strong (headcount vs traffic vs funding).  
4. Detail page should hold the fuller set.  
5. “Impressive hero” among available three = later nice-to-have.

**Examples named (NOT a locked ordered list of 10):**
- Hypothetically: revenue/profit → total funding → valuation or founder/investor  
- “Should exist”: revenue, funding, employee/team size  
- Website traffic: **should not be a priority metric** (Utkarsh); monthly cadence / detail gaps  
- Coverage: even Unicorn/Soonicorn ~60–70% on revenue/profit; valuation ~28%

**Open:** Ranjith + Prapti finalize exact 1→10 + coverage % + update cadence.

### 3.6 Card UI edge cases (9 Sep, Satya/Ritvik)
Long city names (e.g. Thiruvananthapuram), undisclosed raises, decimal overflow (275.x million), headcount ranges (500–1000) making UI huge — Satya/Ritvik to handle.

---

## 4. Prapti data reality (feeds the model)

### Company tags inventory (shared 9 Sep)
- **Company Stage:** Unicorn (122), Soonicorn (141), Minicorn (60) → 323  
- **Editorial IP:** 30 Startups To Watch, Startup Watchlist, Inc42 UpNext → ~1,480+ rows (pipeline stats later ~2,108 mapped)  
- **Award:** FAST42 (2022–2026, 132)  
- **Tracker:** AI Startup Tracker (151)

### Editorial series definitions + frequency (Prapti Slack)
- **30 Startups To Watch:** monthly cohort; year+month edition; companies can recur.  
- **Startup Watchlist:** annual sector-wise Jan lists 2018–2021; **currently inactive**.  
- **Inc42 UpNext:** soonicorn/emerging profiles; preceding month’s published profiles as ingestion window.  
- Mapping: scrape inc42.com tag archive → company_uuid (exact / domain / fuzzy≥85); idempotent upserts; **pipeline frequency = monthly**.  
- App utilization inputs: Prapti said she’d figure what can be used from App POV (pending).

### Other feasibility
- IPO-bound pipeline: buildable in ~2–3 days; not fully live.  
- Listed stock movement: daily data exists; **tech sync pending**.  
- Funding data: OK for Brief/companies use.

---

## 5. Recommended lock draft (Product Manager, 10 Sep)

Full write-up: **`companies-discover-vs-browse.md`**

### Discover (NEW) — event-first
**Tier A (always live, above fold):**  
1. Recently Funded — daily  
2. In the News — daily *(gap: Media→company join)*  
3. Just Launched — only if def+data ready *(else park)*  
+ Seasonal New Financials boost  

**Tier B (calendar boost):**  
- 30 To Watch — monthly + ~7-day pin then demote  
- Series tags — N-day boost after launch  
- Profitable / IPO / AI — Discover only if membership moves; else Browse  

**Tier C:** Unicorn / Soonicorn / Minicorn → **Browse chips** by default  

### Browse (existing)
Chips: Unicorn · Soonicorn · Minicorn · Recently Funded · Sector · AI · Profitable · IPO/Listed (when ready)

### Mechanics
Query-based rails · dynamic order · dedupe across carousels · “why now” on card · optional “Updated today”

---

## 6. Open decisions for Claude / Ranjith

1. Confirm Discover vs Browse split + rail order.  
2. In the News: ship only when join exists, or placeholder?  
3. Park Just Launched for V2?  
4. IPO: Discover when tagging lands vs Browse-only until then?  
5. Finalize top-10 metric hierarchy with Prapti.  
6. Pick one editorial hero brand (30 To Watch vs UpNext) for boost calendar.  
7. Recently Funded window (30 vs 90 days).

---

## 7. Related local MD index (synced to Mac; nothing deleted)

Companies / IA / metric context useful for Claude:
- `UTKARSH-COMPANIES-FULL-CONTEXT.md` ← this file  
- `companies-discover-vs-browse.md`  
- `app-info-hierarchy-brief.md`  
- `CLAUDE-HANDOFF-app-info-hierarchy.md`  
- `_ia-context-raw.md`  
- `_wispr_design_extract.md`  
- `_wispr-actions-sep7-8.md`  
- `Inc42-North-Star-QIA.md` (metric SoT; separate from Companies UI but shared context)  
- `Inc42-Audience-Model-QIA-Activation-Identity.md`  
- `qia-and-app-ia-industry-brief.md` / `qia-and-app-info-hierarchy-brief.md` / `qia-activation-grid-brief.md`  

Transcript extract (not MD): `_740pm_transcript.txt` (Companies Discover block).

**Mac path:** `~/ClaudeDocs/inc42/`  
**Box path:** `/workspace/inc42-handover/`
