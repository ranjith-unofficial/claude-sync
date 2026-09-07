# CLAUDE HANDOFF — App Information Hierarchy (News vs Companies)

**Purpose of this file:** Context pack only. Claude already has deeper analysis and meeting memory. Use this as the seed: fill the empty sections, develop the recommendation, and produce the working artifact Ranjith will share with design (Satya) before the **9 Sep EOD design gate**.

**Created:** 8 Sep 2026 (IST) by Chief of Staff / Grok Bot from Wispr + prior briefs.  
**Do not treat as final product doc.** Audience metrics live separately (see linked Drive).  
**Local path (Mac):** `~/ClaudeDocs/inc42/CLAUDE-HANDOFF-app-info-hierarchy.md`

---

## 0. What Claude should produce (empty until you fill)

> Claude: replace each stub below. Keep tables tight. No em dashes. Decisions already made should stay decided; only reopen if data contradicts.

### 0.1 Problem statement (1 paragraph)

_TODO — Claude fill_

### 0.2 Industry practice → Inc42 implication → recommendation (one table)

| Industry practice | Inc42 implication | Recommendation |
|---|---|---|
| _TODO_ | _TODO_ | _TODO_ |

### 0.3 Final IA map (tabs, homes, what lives where)

_TODO — Claude fill; start from §3 locked proposals below_

### 0.4 Open decisions + Ranjith asks (bullet list)

_TODO_

### 0.5 Design handoff checklist for Satya (ordered screens)

_TODO — align to design order already locked_

### 0.6 Data / analysis Claude already has (paste pointers, not re-run unless needed)

_TODO — Claude: attach or cite your existing PostHog / Brief / Explore / Watchlist / Streak cuts_

### 0.7 Explicitly out of scope

_TODO_

---

## 1. Why this exists / what to solve

**Problem:** The App still forces **two different jobs** into one **Explore** surface (stories + company discovery). That blurs scan vs track, wastes nav on low-usage surfaces (Watchlist ~15%), and puts Brief redesign on the critical path of a marketing launch (15 Sep) even though Brief has a known open-rate problem (~44% Brief-tab never-open).

**What good looks like:**
- Clear **information hierarchy**: News = stories; Companies = entities; Profile = my stuff; Brief = ritual (not a third content index).
- Nav that matches usage (bury Watchlist; keep mid-habit Streak unless data says otherwise).
- Design can finish **by 9 Sep EOD** without waiting on Brief FOMO redesign.
- Onboarding interest/sector seeds **both** News and Companies (not articles-only).
- Cross-links between story ↔ company without rebuilding a hybrid Explore feed.

**Related but separate:** Company-wide **QIA / Activation** model is already locked in a different Drive doc. Do **not** reopen metric debates inside this IA file except where IA placement affects App Actv (Brief completion) or Media Actv (3 article reads in-App).

Canonical metrics doc:  
https://docs.google.com/document/d/1aqWOG2XAcoB6OZx8dPu_qEQCaPjLr9pQN0pL60-QUoU/edit

Metric locks that touch IA:
- App Activation ≤7d from identify = **Brief completion only** (not 3 article reads).
- Media Activation = **3 article reads** (web **or** in-App).
- Company chase = **QIA** (Identified + ICP + ≥1 of Utkarsh’s 10), rolling **15d stock**.
- **Engage / Repeat among QIA** is Lifecycle secondary only (Ranjith 8 Sep: too much for the company scoreboard). Do not build IA around Repeat.

---

## 2. Meeting context (raw, source-backed)

### 2.1 App UI Redesign Discussion — 7 Sep 2026

- **Wispr title:** App UI Redesign Discussion  
- **Share:** https://notes.wisprflow.ai/shared/k869WCco8davBiYW672f3VgrBtAxTzPNgQ-_rWUqbOY  
- **Owner:** Ranjith M · created ~7 Sep 2026 ~18:57 IST (UTC 13:27)

**Flow summary (compressed):**
- Font/color: Inc42 logo red as primary baseline; serif+sans combo; flatten toggle pill.
- Hero card description = **first summary bullet**, not truncated first line of article (avoids incomplete cut-off).
- Tags: keep familiar tag look; also try quieter variant; long sector names need **short display names** (e.g. Advanced Hardware and Technology, Media and Entertainment).
- Article readability: tighten line-height / paragraph spacing.
- **IA:** Explore → **News** + **Companies** (separate bottom tabs; ~4 tabs total). Article vs company consumption patterns are different.
- **Watchlist → Profile** (~15% usage). **Streak stays top-level** for now (~20–25%).
- Companies = **sectional** home (recently funded, just launched, …) + **browse all** filter page.
- Search more prominent on Companies; stays **global**, not a fifth tab.
- Timeline: design **9th EOD** → dev **11th** → submit Fri/Sat → marketing launch **15th**.
- Design order called in room: article → news home → companies home → company profile → **brief last**. (Summary also listed “news home, companies home, article detail…” — Claude: reconcile to the sequential delivery next steps which put **article page first**.)
- Company profile: **UI-only** this round; UX revamp = v3. **Reject web-view** shell.

**Next steps from Wispr:**
- Simulate hero with real article content (incomplete-line edges).
- Red swatch template across screens.
- 2–3 shorter naming options for long sector tags.
- Deliver designs sequentially: **article first (next day), then news home, companies home, company profile, brief last**.
- Fix article readability.
- **(Ranjith / Speaker 2) Re-share information hierarchy document covering news, companies, tags, and onboarding** ← this handoff is the seed for that.
- Submit build Fri EOD / Sat morning; test one day before submission.

### 2.2 One Inc42 session — 7 Sep 2026 (onboarding / identity feed into IA)

- **Share:** https://notes.wisprflow.ai/shared/3Az2qajH1uA3bw1PGs9baJmVzPegPKOACXWKlX-NkOs  
- Relevant to hierarchy: App combines Media + DataLabs; people on Media don’t understand DataLabs; company section exists in App but doesn’t communicate DL.
- Onboarding lock direction: ask only **job title, company name, interest/sector**; enrich the rest. Interest/sector **must** be asked (cannot enrich).
- Implication for IA: interest/sector should seed **News ranking and Companies sections**, not only article personalisation.
- QIA debate that day was unresolved in-room; **later superseded** by 8 Sep Audience Model locks (see Drive). Claude: do not revive One Inc42 QIA contradictions inside the IA doc.

### 2.3 Product & Data Wispr — 7 Sep 2026

- **Share:** https://notes.wisprflow.ai/shared/RfVfAWrzO_CNoDncsE8toJ7p--KhptrNor8RpV3oVwo  
- Used earlier for QIA×Actv grid; less IA-tab detail than design review. Claude: pull only if needed for cross-surface “already QIA → continue not cold onboarding” copy on Companies / News.

### 2.4 Weekly App Review — 24 Aug 2026 (earlier Explore→News direction)

- Local notes: `~/ClaudeDocs/inc42/` / workspace copy `ClaudeDocs/meetings/weekly-app-review.md`
- Meeting id: `d8fac763-3f4a-42a5-8fae-c77a03f1c628`
- Early decisions: rename Explore → News; Brief as feature not hero; Brief open vs completion drop-off is the redesign goal; card1→card2 drop; D7 byproduct.
- Activation language that day (Brief + 60s) is **older**; current App Actv lock = Brief completion ≤7d from identify.

### 2.5 V2 timeline (locked 7 Sep, memory)

| Gate | Date |
|---|---|
| Design EOD | 9 Sep |
| Dev | 11 Sep |
| Submit | Fri/Sat |
| Marketing launch | 15 Sep |

Scope called: brief, article, explore article, company explore and completion; Explore → News + Companies; Watchlist under Profile; logo red primary; company profile UI-only; UX → v3.

---

## 3. Proposed / provisionally locked IA (from 7 Sep briefs — NOT Ranjith-final on tab #4)

Ranjith was asked 8 Sep to lock the 4th tab (Streak vs Brief vs 5 tabs) and moved on without answering. Treat as **proposed**, not final.

| Decision | Status | Implication |
|---|---|---|
| Explore → News + Companies (separate tabs) | Strong lock from design review | Stop hybrid story+company feed |
| ~4 tabs; Profile last | Strong lock | Nav budget |
| Watchlist under Profile (~15%) | Strong lock | Shortcut row from Companies still needed |
| Streak stays top-level (~20–25%) | Proposed | Revisit after News/Companies prove out |
| 15 Sep tabs = News · Companies · Streak · Profile; Brief off Explore critical path | Proposed (recommended) | Brief still = App Actv aha; instrument completion even if not primary tab |
| Companies = sections + browse-all | Strong lock | Discovery first, DB second |
| Search global, context-biased; not a tab | Strong lock | Stronger on Companies |
| Company profile UI-only; no web-view | Strong lock | v3 UX later |
| Design order: Article → News home → Companies home → Company profile → Brief last | Strong lock | Brief not blocking Explore split |
| Hero desc = first summary bullet | Strong lock | |
| Short sector display names | Required before polish | Need 2–3 options |
| Onboarding interest/sector seeds News + Companies | Direction from One Inc42 | Must land in IA doc |

### Mental model (proposed)

- **News** = what’s happening (stories, FOMO).  
- **Companies** = who to track (entities, funding, launches).  
- **Profile** = my stuff (watchlist, saved, account).  
- **Brief** = time-boxed morning ritual; **not** another Explore. Distinct from News home.

Cross-links OK (story → company; company → related news). Unified Explore that mixes long story cards and company chips in one infinite list = **no**.

### What lives where (proposed detail)

**News home — include:** hero/top story; story feed with short sector tags; article detail entry; light “companies mentioned” chips.  
**News — exclude:** company DB sections; full watchlist mgmt; deep company filters; Streak as page hero.

**Companies home — include:** sections (Recently funded, Just launched, optional trending/in news); browse-all filters; strong search (company bias); paths to company profile; Watchlist row → Profile.  
**Companies — exclude:** long story cards as primary unit; full v3 company UX; watchlist as duplicate top section; web-view company pages.

**Profile — include:** Watchlist (primary home); saved/bookmarks if distinct; account/prefs/notifications; optional Streak summary if Streak tab later drops.

**Brief — include:** time-boxed daily pack; FOMO/live-room patterns from draft Figma after News/Companies. Design after News/Companies so it doesn’t become a story library.

### Success signals (lightweight, proposed)

| Surface | Early signal |
|---|---|
| News | Story opens / session; tag tap rate |
| Companies | Section CTR; browse-all use; search → company profile |
| Profile | Watchlist open rate (expect rise once findable) |
| Brief | After redesign: open rate vs ~44% never-open baseline |

---

## 4. Usage / product numbers already cited in rooms (verify in Claude’s analysis)

| Signal | Figure cited | Caveat |
|---|---|---|
| Watchlist usage | ~15% | In-room call; Claude verify PostHog |
| Streak usage | ~20–25% | In-room call; Claude verify |
| Brief tab never-open | ~44% | Prior Brief landing work |
| Card1 → card2 | ~45% | Prior Brief work |
| App activate in 7d (older One Inc42 room) | ~96% of signups | Older activation definition; don’t mix with Brief-only Actv lock without care |

Claude: paste authoritative cuts here in §0.6.

---

## 5. Adjacent docs (read, don’t fork)

| Doc | Path / URL | Role |
|---|---|---|
| Audience Model (metrics) | https://docs.google.com/document/d/1aqWOG2XAcoB6OZx8dPu_qEQCaPjLr9pQN0pL60-QUoU/edit | Canonical QIA/Actv — do not spawn parallel |
| App info hierarchy brief | `~/ClaudeDocs/inc42/app-info-hierarchy-brief.md` | 7 Sep approach |
| Combined QIA+IA brief | workspace `qia-and-app-info-hierarchy-brief.md` | Older combined; QIA part partly superseded |
| Industry framing | `qia-and-app-ia-industry-brief.md` | Part B = IA industry→Inc42 |
| Brief card / UI types | `BRIEF-CARD-DESIGN-BRIEF.md`, `BRIEF-15-UI-TYPES.md` | Brief redesign later |
| One Inc42 definition | https://docs.google.com/document/d/1iwXO6icFGvPCUIi7N4WBRMev63yyLZAFBYNQ_W0z-1U/edit | Personas / ICP |
| Design Wispr | https://notes.wisprflow.ai/shared/k869WCco8davBiYW672f3VgrBtAxTzPNgQ-_rWUqbOY | Primary IA meeting |
| One Inc42 Wispr | https://notes.wisprflow.ai/shared/3Az2qajH1uA3bw1PGs9baJmVzPegPKOACXWKlX-NkOs | Onboarding / interest |
| Product & Data Wispr | https://notes.wisprflow.ai/shared/RfVfAWrzO_CNoDncsE8toJ7p--KhptrNor8RpV3oVwo | Metrics room |

**Rule:** One working IA artifact from Claude. Do not create multiple Drive drafts. Prefer one local markdown Ranjith can re-share with Satya/Prapti, then optional single Drive upload if he asks.

---

## 6. Constraints for Claude’s output

1. Tables over long prose.  
2. No em dashes.  
3. Bake decisions already strong-locked; mark only Streak vs Brief as open if still open.  
4. Separate **App Actv (Brief)** from **Media Actv (3 articles in-App)** in any success section.  
5. Include tags + onboarding interest seeding.  
6. Design order respects 9 Sep EOD gate.  
7. Leave Brief FOMO / v3 company UX / Asana ticket dump out unless Ranjith says go.  
8. If Claude’s data contradicts ~15% Watchlist or ~20–25% Streak, say so and amend tab recommendation.

---

## 7. Empty scratch for Claude

### Notes from Claude’s prior analysis

```
(paste)
```

### Alternate tab options considered

```
(paste)
```

### Sector short-name options (2–3)

```
(paste)
```

### Wire / screen inventory (optional)

```
(paste)
```

### Questions for Ranjith only

```
(paste)
```

---

**End of handoff seed.** Claude: fill §0, verify §4 with data, ship one IA recommendation file for Satya.
