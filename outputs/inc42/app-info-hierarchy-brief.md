# App info hierarchy — News vs Companies (brief)

**Date:** 7 Sep 2026 · **Owner:** Ranjith · **Status:** high-level approach for agreement  
**Sources:** [Design review Wispr](https://notes.wisprflow.ai/shared/k869WCco8davBiYW672f3VgrBtAxTzPNgQ-_rWUqbOY) · usage called in-room (Watchlist ~15%, Streak ~20–25%) · prior Brief landing work (44% Brief-tab never-open; card1→card2 ~45%)

---

## 1. What locked today

| Decision | Implication |
|---|---|
| Explore → **News** + **Companies** (separate bottom tabs) | Article and company jobs are different; stop forcing one feed |
| Bottom bar ≈ **4 tabs** | News · Companies · *(Streak or Brief — see open)* · **Profile** last |
| **Watchlist → Profile** | Low usage (~15%); don’t spend a primary tab |
| **Streak stays top-level for now** (~20–25%) | Revisit after News/Companies prove themselves |
| Companies = **sectional home** + **browse-all** filter page | Discovery first; database second |
| Search = **global**, more prominent on Companies; **not** a fifth tab | Same search brain; different default ranking/hints per tab |
| Design order | Article → News home → Companies home → Company profile (UI only) → **Brief last** |
| Company profile | **UI refresh this round**; UX revamp = v3. No web-view shell |

---

## 2. Recommended mental model

Think **two consumption modes**, one identity:

- **News** = “What’s happening in the ecosystem?” (stories, briefs-as-stories, FOMO).  
- **Companies** = “Who should I track?” (entities, funding, launches, watchlist entry points).  
- **Profile** = “My stuff + settings” (watchlist, saved, account).  
- **Brief** = morning ritual surface (time-boxed, not a third content index). Keep it distinct from News home so Brief doesn’t become “another Explore.”

Do **not** rebuild a unified Explore that mixes story cards and company chips in one infinite list. Cross-links are fine (story → company; company → related news).

---

## 3. What lives where

### News home

**Job:** scan and open stories fast.

| Include | Exclude / defer |
|---|---|
| Hero / top story (desc = **first summary bullet**, not truncated lede) | Company database sections |
| Story feed (sectors as **short display tags**; try one variant with quieter tags) | Full watchlist management |
| Entry to **article detail** (readability: tighter line-height / spacing) | Deep company filters |
| Light “companies mentioned” chips → Companies / profile | Streak as the page hero (Streak can badge elsewhere) |

**Search on News:** global search, default bias to **stories**; recent queries.

### Companies home

**Job:** browse entities by moment, then drill.

| Include | Exclude / defer |
|---|---|
| **Sections** e.g. Recently funded · Just launched · (optional: trending / in news) | Long story cards as the primary unit |
| **Browse all** → filter page (sector, stage, etc.) | Full v3 company UX |
| Strong **search** (default bias to **companies**) | Watchlist as a top section that duplicates Profile (show “Watchlist” row → Profile) |
| Paths into **company profile** (UI-only this round) | Web-view company pages |

### Profile

| Include | Notes |
|---|---|
| **Watchlist** (primary home for follows) | Matches ~15% usage; still must be 1 tap from Companies via “Watchlist” |
| Saved / bookmarks if separate from watchlist | Keep labels clear vs company follows |
| Account, preferences, notifications | |
| Optional: Streak summary if Streak tab later drops | |

### Brief

| Include | Notes |
|---|---|
| Time-boxed daily pack (existing Brief product) | Design **after** News/Companies so it doesn’t regress into a story index |
| FOMO / live-room patterns already explored in draft Figma | Avoid “three named stories as a library” |

**Open product call:** whether the 4th tab is **Streak** or **Brief** for v2 marketing launch (15 Sep). Usage favors keeping Streak visible short-term; Brief has a known open-rate problem and is last in the design queue. Recommendation: **ship News + Companies + Streak + Profile** for the 15 Sep cut; treat Brief as overlay / deep link / next tab experiment so Brief redesign isn’t on the critical path of the Explore split.

---

## 4. Search, tags, onboarding

| Area | Approach |
|---|---|
| **Search** | One global entry. Placeholder and ranking **context-aware** (News vs Companies). No Search tab. |
| **Tags** | Familiar tag affordance on cards; **short display names** for long sectors (need 2–3 naming options). Quiet-tag variant as A/B later. |
| **Onboarding** | Interest/sector (One Inc42: must ask) should seed **both** News ranking and Companies sections (e.g. default sector strip). Don’t onboarding-only for articles. |
| **Cross-promo** | From News story → company profile; from company → “News about this company.” Supports QIA cross-surface story without merging tabs. |

---

## 5. Success signals (lightweight)

| Surface | Early signal |
|---|---|
| News | Story opens / session; tag tap rate |
| Companies | Section click-through; browse-all use; search→company profile |
| Profile | Watchlist open rate (expect rise once Findability = Profile tab) |
| Brief | Only after its redesign: open rate vs today’s ~44% never-open on Brief tab |

---

## 6. Ask (stop here)

Agree / amend:

1. **Strict split:** News = stories; Companies = sectional entities + browse-all; no hybrid Explore.  
2. **Watchlist only under Profile**, with a Companies shortcut row.  
3. **15 Sep tab set:** News · Companies · Streak · Profile; **Brief not blocking** the Explore split.  
4. **Search** global + context bias; short sector **display names** required before polish.

**Out of scope until you say go:** full wire inventory, Asana tickets, copy deck, v3 company UX, Brief FOMO variant build.
