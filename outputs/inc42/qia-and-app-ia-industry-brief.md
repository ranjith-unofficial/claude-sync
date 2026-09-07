# QIA + App info hierarchy — industry practice → Inc42

**Date:** 7 Sep 2026 · **Status:** revised for agreement (HOLD implementation)  
**Replaces:** `qia-activation-grid-brief.md` + `app-info-hierarchy-brief.md` as the working draft  
**Sources:** Product & Data / One Inc42 / design-review Wispr (7 Sep); Ranjith audience-metric doc; industry patterns below

---

# Part A — Metrics / QIA / activation

## §0 Industry practice

**AARRR split.** Activation = “product aha” inside a short N-day window. Retention / actives are a different stage. Collapsing activation into “active this month” muddies both diagnosis and lifecycle messaging.

**Multi-product suites.** Spotify, Atlassian, marketplace-style portfolios almost always keep **product-specific activation** until identity and a shared workspace are real. A single company-wide “activated” definition too early forces CIO/CRM into an unmanageable fan-out of journeys.

**North star vs inputs.** One named north star (the sellable / ICP-qualified count). Teams steer **input metrics** (identified actives, activation conversion) until the north-star base is large enough that noise does not drive decisions. A ~1,000 person floor before steering the north star is a common rule of thumb.

**B2B “qualified”.** Clearbit / HubSpot-style qualification is **ICP / persona fit** (function + company type + seniority band where relevant), not title seniority alone. Seniority-only gates miss Sales & Marketing → data-product buyers and overweight “sounds senior” readers who never buy.

**Windows.** Never plot 7 / 15 / 30 on the same chart without labeling. Common pattern: short **SLA window** for activation (often 7d) + longer **reporting window** for actives / qualified (14–15d).

**Cross-product counting.** Customer counts as activated if **OR** across products. Per-product activation stays a **local health** metric. Re-running cold onboarding for someone already qualified on another surface is an anti-pattern.

**Backfill.** Forward cohorts (known activation state) are goal truth. Legacy “activation unknown” is reported on a separate line, never blended into the KPI used for targets.

## §1 Implication for Inc42

| Industry rule | What it means here |
|---|---|
| Product-specific activation | Media / DataLabs / App / IP each define their own aha; no One-Inc42-wide activation until identity + combined CIO workspace exist |
| North star + inputs | Keep the **QIA** name; steer **IA-15 + activation conversion** until QIA ~1,000 |
| Persona ICP, not VP+ only | Ranjith’s ICP table (Investor, Sales & Marketing, Founder/CXO, …) is the qualification axis; Media seniority alone cannot route DataLabs buyers |
| 7d SLA + 15d report | Matches One Inc42’s 7d activation lock and the metric doc’s 15d evidence (Media under-counted at 7d) |
| OR across surfaces | App-activated user on DataLabs web stays QIA; chase DataLabs activation as local ops, not a re-gate |
| Forward vs legacy | Historical unknown activation → provisional line only |

**Today’s contradictions (unchanged facts):** One Inc42 pushed unified activation + 7d; Product & Data locked product-specific + QIA needs Actv≥1; metric doc steers IA with 15d and persona ICP without an activation row in the three-level table. Industry lens resolves this toward **product-specific Actv + OR for QIA + dual windows + persona ICP**.

## §2 Recommendation (Inc42) — agree / amend

Keep **QIA** as the north-star name.

**Stack:** Reach → **IA** (email + job title + company + qualifying action in reporting window) → **Activated** (product-specific, 7d SLA) → **QIA** (Actv on ≥1 surface + ICP of any product) → **Core QIA** (proven-buyer slice, report only) · **Repeat Rate** as integrity check.

**Windows:** activation SLA **7d**; IA / QIA / Repeat reporting **15d**; warehouse QIA-30 labeled separately; never mix on one chart.

**Activation drafts (local):** App = existing early content/brief aha · DataLabs = profile / search / filter / watchlist / Ask / trial · Media interim = 2+ article opens OR newsletter click OR search (scroll restore becomes primary later; Infotude 2+ articles needs retention check) · IP = application / ticket.

**Steer now:** IA-15 + Repeat-15 + activation-leak conversion. **Report** QIA weekly with Actv gate. **CIO:** one journey per surface activation; already-QIA users get recognised / continue, not cold onboarding.

### Edge grid (operational)

| Case | Count | Do |
|---|---|---|
| Anon active | Reach only | Identify carefully; publish reach beside IA |
| Identified, not Actv, ICP yes | IA — activation leak | Priority surface CTA; not QIA yet |
| Actv ≥1 + ICP + active | **QIA** | Full product + cross-promo |
| App-Actv, first DataLabs visit | Still QIA if ICP | Soft DL tour; do not strip QIA |
| Media signup never Actv | IA if action+identity | Media activation campaign |
| Multi-product Actv | QIA once (dedup) | Optional surface badges for ops |
| Legacy Actv unknown | IA + provisional QIA\* | Split forward vs legacy lines |
| Student / junior | IA only | Serve; never QIA |
| Newsletter-only (no title/company) | Outside full IA | Enrich / re-ask |

**Ask A:** Confirm product-specific Actv, QIA needs Actv≥1 (OR), 7d/15d split, persona ICP, steer IA until ~1k, Core QIA as slice only.

---

# Part B — App info hierarchy (News vs Companies)

## §0 Industry practice

**Content feed vs entity directory.** LinkedIn separates Feed from Companies/People; news apps separate editorial from tickers/companies; marketplaces separate editorial browse from catalog. Mixing both in one infinite “Explore” is a common failure: incompatible card density, search intent, and scroll jobs.

**Nav budget.** Primary tabs = high-frequency jobs. Low-usage tools (~15%) bury under Profile / More. Mid-usage habit loops stay visible until replacement tabs prove themselves.

**Ritual surfaces** (morning brief / daily pack) should not compete with browse tabs until open-rate is healthy. Deep-link or overlay until the ritual UX is redesigned.

**Search.** One global entry; ranking and placeholder bias by context. Rarely its own bottom tab.

## §1 Implication for Inc42

| Industry rule | What it means here |
|---|---|
| Split feed vs directory | Today’s Explore → **News** + **Companies** lock is the industry-correct move |
| Bury low-usage | Watchlist ~15% → **Profile** (with a Companies shortcut), not a primary tab |
| Keep mid habit visible | Streak ~20–25% stays top-level until News/Companies prove out |
| Ritual off critical path | Brief has known never-open problem (~44% Brief-tab); don’t block 15 Sep Explore split on Brief redesign |
| Global search | Context-biased on News vs Companies; no Search tab |

Design order already matches industry: article → News home → Companies home → company profile (UI only) → Brief last.

## §2 Recommendation (Inc42) — agree / amend

**Mental model:** News = “what’s happening” (stories). Companies = “who to track” (sectional entities + browse-all). Profile = my stuff (watchlist, account). Brief = time-boxed ritual, not a third content index.

**15 Sep tab set (proposed):** News · Companies · Streak · Profile. Brief via deep link / overlay / next experiment so it does not compete with the new browse split.

**Placement**

| Surface | Include | Exclude |
|---|---|---|
| News home | Hero (first summary bullet), story feed, short display tags, → article | Company DB sections, watchlist mgmt |
| Companies home | Sections (funded / launched / …), browse-all filters, strong search, → company profile | Long story cards as primary unit; v3 company UX |
| Profile | Watchlist (canonical), saved, account | — |
| Brief | Existing pack; FOMO patterns after redesign | Competing as 4th browse tab for 15 Sep |

**Search / tags / onboarding:** one global search with context bias; short sector display names; interest/sector onboarding seeds **both** News ranking and Companies sections; story ↔ company cross-links (supports QIA cross-promo without merging tabs).

**Ask B:** Confirm strict News/Companies split, Watchlist under Profile, 15 Sep tabs = News·Companies·Streak·Profile, Brief deferred off the Explore-split critical path.

---

# Combined asks (stop here)

1. Metrics: product-specific Actv · QIA = Actv≥1 (OR) + persona ICP · 7d SLA / 15d report · steer IA until ~1k.  
2. App: News vs Companies split · Watchlist in Profile · Streak kept · Brief not blocking 15 Sep.

**Out of scope until agree:** warehouse SQL, Asana, CIO journey maps, Infotude retention study, Brief FOMO build, v3 company UX.
