# App IA — RAW context dump (not polished)

Compiled: 8 Sep 2026 ~01:30–02:00 IST · for handover only · quotes + facts, no recommendation prose

---

## A. MEETING INDEX

| ID | Title | When (UTC → IST) | Share | Notes |
|---|---|---|---|---|
| `2233a7e7-019b-4e7c-8121-a9345389e900` | **App UI Redesign Discussion** | 2026-09-07 13:27–14:51 UTC → **7 Sep 2026 ~18:57–20:21 IST** | https://notes.wisprflow.ai/shared/k869WCco8davBiYW672f3VgrBtAxTzPNgQ-_rWUqbOY | Primary design-review lock for News/Companies split, Watchlist→Profile, Streak keep, design order, 15 Sep launch |
| `f9514d22-ff8b-409e-8179-eae1055f1fc3` | Wispr Flow UI Redesign | 2026-09-05 08:00–09:17 UTC → **5 Sep ~13:30–14:47 IST** | https://notes.wisprflow.ai/shared/k8B5oSd13Obyv4QEt9lclLEAy-yXR5Z111vZfc5nhKE | Earlier page-level UX / explore-brief direction |
| `70d61cc3-d6e0-4e2c-b31c-f1e6e1e4b78a` | Card UI Redesign Discussion | 2026-09-04 12:20–12:43 UTC → **4 Sep ~17:50–18:13 IST** | https://notes.wisprflow.ai/shared/fdpIT1vMhEeWiI8VwIJUVvMrBe6QB5VnoQJMO4FsfNs | Card/glass critique; Brief page unreadable notes |
| `b83ed5f9-51b0-4cac-9dd9-4b604261f7da` | Brief Card Design Refresh | 2026-08-26 10:04–11:05 UTC → **26 Aug ~15:34–16:35 IST** | https://notes.wisprflow.ai/shared/UGkb6y-RjPYrZQcoQ6bCPrUkTjMWdBSUiU7Im0fxn2Q | Brief card redesign review |
| `1f7caee8-771c-4b9f-b523-21c6e0f0c018` | Optimizing Wispr Brief Design | 2026-08-27 07:53–08:11 UTC → **27 Aug ~13:23–13:41 IST** | https://notes.wisprflow.ai/shared/P97PRSJypJuh5KCwdnZJFlfzZz5vEGcCmK9ajRVXJE0 | Brief home critique |
| `2e26af56-99eb-468a-88d1-1310f756a434` | Product & Data Sync | 2026-09-04 08:00–08:30 UTC → **4 Sep ~13:30–14:00 IST** | https://notes.wisprflow.ai/shared/0qW-XD3k6pMyAVMPydoXKcUmWfruS0Rz8Om9Ay1rDVI | Attendees: Ashish, Prapti, Ranjith, Utkarsh — warehouse/QIA; not the IA nav lock |
| `fc61f3e3-643c-412f-a59a-0385cf4e46ab` | Product & Data Sync | 2026-09-02 07:00–07:30 UTC → **2 Sep ~12:30–13:00 IST** | https://notes.wisprflow.ai/shared/wlZ1q5l_KDmUhlhbL55SewhRr-t1t6u7oVDRCu-FgaU | MOP/dunning/QIA — not Explore split |

**Speaker labels in Wispr transcript are anonymous (Speaker 1 / Speaker 2).** Context: designer (Satya) + product (Ranjith); Rithvik joined late for timeline/web-view. Do not treat speaker IDs as named attribution without cross-check.

---

## B. WISPR 7 SEP — FLOW SUMMARY (machine summary, verbatim bullets)

Source: get_meeting summary for `2233a7e7-…`

### Information Architecture
- Explore split into two bottom tabs: News and Companies (4 tabs total)
  - Article and company consumption patterns are fundamentally different
- Watchlist merged into Profile (only ~15% usage); Streak stays top-level for now (~20-25% usage)
- Companies page uses sectional layout (recently funded, just launched, etc.) with 'browse all' filter page
- Search prominence to increase on Companies page; stays global, not a separate bottom tab

### Timeline & Delivery
- Design completion target: 9th EOD; dev completion 11th; submission Fri/Sat; marketing launch 15th
- Page order: news home, companies home, article detail, company profile, then brief last
- Company profile page: UI update only this round, UX revamp deferred to v3
- Web-view idea for company detail page rejected (breaks native interaction, aesthetics mismatch)

### Next Steps (design order variant in same summary)
- Deliver designs sequentially: **article page first (tomorrow), then news home, companies home, company profile, brief last**
- Re-share information hierarchy document covering news, companies, tags, and onboarding
- Submit app build Friday EOD / Saturday morning; test one day before submission

### Decisions Made (summary list)
- Explore tab replaced by separate News and Companies bottom tabs (4 tabs total)
- Watchlist merged into Profile; Profile moves to bottom bar as last tab
- Company profile page: UI-only update this round, UX revamp pushed to v3
- Skip web-view approach for company detail page
- (+ font/color/hero-card decisions; see summary)

**NOTE — design-order inconsistency inside same Flow Summary:** “Page order” lists news home → companies home → article → company profile → **brief last**; “Next Steps” lists **article page first**, then news home, companies home, company profile, **brief last**. Dump both; do not reconcile here.

---

## C. WISPR 7 SEP — KEY RAW QUOTES (transcript)

### C1. Explore → News + Companies (consumption different)

> Speaker 1: Assume explore as an article section. … Article as a separate section. …  
> Speaker 2: Company as a separate tab.  
> Speaker 1: हाँ। For company as a separate tab. … But मुझे ऐसा लग रहा है it becomes even more powerful.  
> Speaker 2: It's like getting data labs into a bottom bar tab. … Companies रख लो. … I think yeah, that might actually work. … उसका weight भी बढ़ता है property का.  
> Speaker 1: … जब हम explore के अंदर जैसे article और companies हैं, and the weight is coming, it's more like a sub-tabs की तरह आ रहा है। And problem क्या है कि the nature, the consumption of article और companies एकदम ही अलग है।  
> Speaker 2: बिल्कुल।  
> Speaker 1: … Universe ही different हो गया है। … even we were thinking कि क्या वो tabs रखनी चाहिए।

### C2. Single hierarchy per tab

> Speaker 1: Single hierarchy in each tab. … Single hierarchy in each tab only.  
> Speaker 2: Very simple होना चाहिए।  
> Speaker 1: क्योंकि app पे उससे ज्यादा कोई consume नहीं कर रहा।

### C3. Lock information hierarchy for News + Companies

> Speaker 1: ठीक है, तो information hierarchy is something that we have to lock then। What are we showing here? Both for this and for the companies when a new tab। … दोनों का information hierarchy we have to close।  
> Speaker 2: No, वो तो— उसका तो sorted है। Companies— company document भी भेजा है ना।  
> Speaker 1: हाँ, एक बार फिर से सारा summarize कर देना।

### C4. “No Explore anymore” / 4 tabs

> Speaker 2: Information hierarchy। And we agreed to separate। … मतलब explore is not— now there is no explore anymore। There is—  
> Speaker 1: There's no article company।  
> Speaker 2: There's news।  
> Speaker 1: There's news company। … Brief— नहीं, brief, news।  
> Speaker 2: हाँ, we have 4 tabs now।

Later (to Rithvik, near end of call):

> Speaker 2: … explore page is no more explore. We are having brief page, news, companies profile. … And for you. That is how the page is going to look like.  
> Speaker 1: Four tabs.  
> Speaker 2: Four— four different tabs is what we are going to have.  
> Speaker 1: मतलब companies को explore से break out करके अलग tab ही दे दिया। And articles भी अब है तो explore page रहेगा, essentially.  
> Speaker 2: ठीक है। And हमारा home है brief. … That still remains brief.

### C5. Watchlist ~15% → Profile (last tab)

> Speaker 1: So अब already we are at 4 items now। नहीं, 3— 4। … हाँ, 4। Washlist का कोई usage है अभी?  
> Speaker 2: नहीं, इतना नहीं है। Only 15% people are using।  
> Speaker 1: Merge them into profile and—  
> Speaker 2: I was about to say this।  
> Speaker 1: And make the profile there। … news apps में देखोगे तो everyone— almost everyone has done for you। … As the last tab। उसी में ही profile है, उसी में ही ये।  
> Speaker 2: Watchlist, जो भी वही है।  
> Speaker 1: सब कुछ वहाँ पे है।  
> Speaker 2: Then let's— हम भी ऐसे करते हैं, for you। लिख के profile, everything goes under that।

### C6. Streak ~20–25% — keep top-level for now

> Speaker 2: … eventually दो चीज़ें। One is streak, second is search।  
> Speaker 1: Streak page पे कोई पहुँच रहा है?  
> Speaker 2: हाँ, लोग आ रहे हैं। 25, 20, 25— 25% people आ रहे हैं।  
> Speaker 1: 20%।  
> Speaker 2: That's a big number। … Interesting।  
> Speaker 1: Streak is an interesting concept। तो streak भी technically speaking profile के अंदर जाना चाहिए, but हाँ, उसकी फिर prominence खत्म हो जाएगी completely। … फिर कोई नहीं use करेगा। ठीक है, for now अभी streak रखते हैं। … but we'll have to eventually start gamifying it a little।  
> Speaker 2: … once the— at least fundamentals started, then people start using, then streak can come into play।  
> Speaker 1: अभी तो वो बस है for the sake of it।

### C7. Companies = sectional + browse all; search more prominent / global

> Speaker 2: … these becomes your sections। … recently funded एक section है … It just launches your another section।  
> Speaker 1: जैसे हम article— news के लिए भी sectional कर रहे हैं।  
> …  
> Speaker 2: … इसमें एक आता है ना, browse all the companies।  
> …  
> Speaker 1: whenever you design company page, make the search little more prominent।  
> Speaker 2: Search तो वही रहेगा। अगर वो global search— … Global search versus company search … पर ठीक है, यहाँ पे तो अभी global ही रहेगा।

Also usage on search (in-room):

> Speaker 2: … people are coming from company page, they are looking for, they are using search bar। उसमें at least 16-17%। … they are coming to companies, they are browsing few companies, and they are also tapping on search and searching few companies, through which we are getting no results अभी, unfortunately।

### C8. Company profile = UI only this round; UX → v3; skip web-view

> Speaker 2: ये तो company profile पे अभी इतना time नहीं spend करेंगे। UI updation करेंगे बस। UX अभी ना छेड़ें। … इस round में। V3 में pick करो। … Company profile page में बस UI update based on जो अभी ये नई design language आई है … उसका UX अभी मत छेड़ो। … Next version में।

Web-view debate → reject:

> Speaker 2: … can we make it as a web page?  
> …  
> Speaker 1: Well, that functionality— heavy driven— that heavy functionality can't be used in web view. …  
> Speaker 2: … हमारी app की aesthetics पूरी orange है। वहाँ से वो red आएगा, वो भी बिल्कुल stitched experience लगेगा, patchy लगेगा।  
> …  
> Speaker 2: हाँ, फिर तो अभी skip the web view part।

### C9. Timeline / Brief last in delivery queue

> Speaker 2: So अभी just to summarize, 9th EOD is the design का timeline जो अभी aim कर रहे हैं। And launch— marketing launch is 15th.  
> … Friday EOD या Saturday morning is when we will have to do the submission  
> Speaker 1: … 9th, 10th, 11th.  
> Speaker 2: 11th को dev completion है।  
> …  
> Speaker 1: Brief page पे तो अभी पहुँचेंगे ही। … Brief page पे तो अभी छुआ ही नहीं है। अभी आखिरी में brief page का design होगा।  
> Speaker 2: Brief में आएगी। Brief में definitely आएगी।

(Transcript also: article page can start Kal / first half; companies work in parallel discussion — see Flow Summary next-steps for sequential design order.)

### C10. Home = Brief (hierarchical difference vs other news apps)

> Speaker 2: हमारा home brief है। इसलिए वो hierarchical difference आया। … हमारे case में ये इसलिए disconnect आ रहा है क्योंकि in our way ये different form of home है हमारा।

---

## D. PRODUCT / DATA NOTES — Brief never-open & related usage

**Primary local Product/Data artifact:** `/workspace/inc42-handover/BRIEF-CARD-DESIGN-BRIEF.md` §8  
Label in that doc: **Observed app behaviour (PostHog, 21 days, 788 users, 1,650 person-days)**

| Metric | Number |
|---|---|
| Brief-tab visits per person-day | **4.0** |
| Person-days that visited but **never opened** the Brief | **44%** |
| Person-days that completed the Brief | 25% |
| Of completers, returned to Brief tab afterwards | 85% |
| Card 1 → card 2 advance | **45%** |
| Cards 2–8 advance | 77–87% |
| Median time in a completed Brief | 78 seconds |
| Users who open full article and return to deck | 6% |
| D1 retention | 26–43%; D3 falls to 7–21% |
| Push notifications ever delivered | **zero** |
| Past briefs | 30% of users open one; median 2 days back; retained 7 days |

Also stated as problem #1 in same brief:

> **44% of person-days that visit the Brief tab never open the Brief at all.**

Cross-refs in handover pack (not independent measurements):
- `BRIEF-15-UI-TYPES.md` — “visits four times and leaves 44% of the time”; “78 seconds and 45% of people who opened, finish”
- `app-info-hierarchy-brief.md` / `CLAUDE-HANDOFF-app-info-hierarchy.md` cite: Watchlist ~15%, Streak ~20–25% (in-room 7 Sep), Brief 44% never-open + card1→card2 ~45% (prior Brief landing / PostHog cut)

**In-room Product usage called on 7 Sep (not the PostHog Brief cut):**
- Watchlist: **~15%** using
- Streak page reach: **~20–25%** (“25, 20, 25— 25%”)
- Company search bar: **~16–17%**

---

## E. SLACK — Ranjith / Satya / Utkarsh on Explore, News, Companies, hierarchy-adjacent

Searched: public+private via `slack_search_public_and_private` + DM reads `D0BE781KY3V` (Satya), `D0BDDK0BZD0` (Utkarsh).  
**Finding:** No Slack thread found that literally says “info hierarchy” or announces the 7 Sep News/Companies bottom-tab lock. IA lock lives primarily in Wispr 7 Sep. Slack below = prior Explore/Article/Company tab framing + Brief/Streak.

### E1. Ranjith → Satya DM — 28 Aug 2026 18:12 IST — Explore still Article Tab + Company Tab

Channel: DM `D0BE781KY3V` · ts `1787920968.187579`  
https://inc42.slack.com/archives/D0BE781KY3V/p1787920968187579

> 2. Explore page  
>    a. Generic — Currently, Tabs and header take more page which is to be optimized  
>    b. Article Tab — Listicles … Article detail page - To improve readability …  
>    c. Company Tab — Listicles - To break monotonous & make search more prominent · Company detail page - To improve readability.

(Also Brief page / completion / welcome / ratings / dark mode in same message.)

### E2. Ranjith → Satya DM — 1 Sep 2026 15:33 IST — Companies sectional / view-all path

Channel: DM `D0BE781KY3V` · ts `1788256983.663179`

> Welcome screen - button to be more intuitive  
> 2 ways to explore design page @Satya  
> 1. Currently, we can redesign the existing card and make it more intuitive, currently there is no much prominence, second inside company make search bar more visible.  
> 2. Section based Card: Recently funded and all the other pills could be sections with view all. For an example, If someone selected Unicorns, it will redirect to that section and it will have view all and clicking on view all will open a page which all the list of companies which are unicorns.  
> Default value of those card would be: Location

### E3. Ranjith → Satya — 4 Sep 2026 — Brief card redesign after Utkarsh discussion

- 19:17 IST ts `1788529657.621389`: “Had an discussion with Utkarsh, he mentioned that Brief card to be redesigned.”
- 19:51 IST feedback bullets (glass = old iOS; heading weak; drop image-colour borders at 70k scale; carousel peek; Brief page unreadable / “Brief” missing / three articles indistinguishable)

### E4. Ranjith → Satya — 28 Aug — Brief completion / Streak hero / Explore handoff (data-backed)

ts `1787907213.134429` (long prompt). Facts embedded:
- Live completion sequence: streak hero → “Explore Trending Stories” carousel → “EXPLORE MORE” CTA
- Median completion **78 seconds**, avg **8.4 cards**
- **86% of articles have no sector tag** (personalization caveat)
- Identity-over-rewards framing for streak

### E5. Ranjith → Satya — 29 Aug — Streak gratification Figma direction

ts `1788012962.355899` — Figma draft-screen link for Streak gratification direction.

### E6. Ranjith public — #tech-team-internal — 4 Sep 16:15 IST

Channel `C076FJ67BGW` · ts `1788518733.641289`

> @Satya Prusty Article title in the explore section is less readable. Can we make it more readable?

### E7. Utkarsh ↔ Ranjith DM — hierarchy-adjacent (not the tab split)

- **24 Aug** ts `1787561684.639759` (thread): Utkarsh feedback on plan — “App events piped into the warehouse. Recovers three qualifying actions at once (app session, **watchlist**, search/profile view)”
- **25 Aug** ts `1787678309.279639` Ranjith priorities: “Scope includes Brief, story cards, **Article/Explore revamp**, dark mode…”
- **1 Sep** ts `1788236355.604369` Utkarsh: brief story mix / depth stories / V2 content-led notifications for brief
- **5 Sep** ts `1788582889.418279` Utkarsh on design direction: “minus a few UX nuances, liking the big bold and clean style…” + FAST42 / Brand Extension Figma refs (reply to Ranjith’s App Draft Screen explore)

### E8. Self-DM / notes — Ranjith — 30 Aug 21:43 IST — Brief home + Explore handoff

Channel `D0BD60DFLF6` · ts `1788106417.256629`

> Thank-you / completion screen — we already have this live in Figma (streak hero → "Explore Trending Stories" carousel → Explore More CTA)…

---

## F. DECISIONS LOCKED (raw list from 7 Sep + prior data)

1. **Explore replaced** by separate bottom tabs **News** + **Companies** (≈4 tabs total). Article vs company consumption treated as different jobs.
2. **Watchlist → Profile** (last bottom tab / “for you”); Watchlist usage ~**15%**.
3. **Streak stays top-level for now**; reach ~**20–25%**; may later move under Profile after gamification / fundamentals.
4. **Companies home** = sectional (recently funded, just launched, …) + **browse all** filter page; search more prominent; **global search** (not a 5th tab).
5. **Company profile**: **UI-only** this round; **UX revamp = v3**; **no web-view** shell.
6. **Design / ship timeline:** design aim **9 Sep EOD**; **dev completion ~11th**; store submission **Fri EOD / Sat morning**; **marketing launch 15 Sep**.
7. **Brief redesign last** in design queue (not blocking Explore split for 15 Sep cut) — still home tab; “still remains brief.”
8. **Brief open-rate problem (Product/Data):** **44%** Brief-tab person-days never open; card1→card2 **~45%**; PostHog window 21d / 788 users / 1650 person-days.

---

## G. OPEN QUESTIONS (explicitly unresolved in sources)

1. **4th tab for 15 Sep cut:** Streak vs Brief as the non-News/Companies/Profile slot — room kept Streak top-level; Brief remains home; polished brief later asked Streak vs Brief for marketing launch (see `app-info-hierarchy-brief.md` open call — not re-litigated in Slack after 7 Sep).
2. **Design sequence order conflict** inside Wispr summary (article-first vs news-home-first); both end with **brief last**.
3. **News home sections:** newsletter / Markets / AI Shift / development tags as separate sections? “information hierarchy … that is what we need to know” — document to re-share.
4. **Companies filtering** direction + zero-result company search.
5. **Sector display names** for long DataLabs sector strings (2–3 shorter naming options).
6. **Whether Brief is a bottom tab vs overlay/deep-link** after News/Companies prove out (product call in later brief; not closed in Wispr transcript beyond “home is brief” + “brief design last”).
7. Slack: no post-7-Sep written confirmation of News/Companies rename in-channel yet (lock is Wispr).

---

## H. SOURCES USED (checklist)

1. Wispr `get_meeting` + transcript pages — meeting id `2233a7e7-019b-4e7c-8121-a9345389e900` (App UI Redesign Discussion, 7 Sep 2026)
2. Wispr Flow Summary / Decisions Made / Next Steps for same meeting
3. Wispr share link https://notes.wisprflow.ai/shared/k869WCco8davBiYW672f3VgrBtAxTzPNgQ-_rWUqbOY
4. Wispr search hits for related design meetings (5 Sep UI Redesign, 4 Sep Card UI, 26–27 Aug Brief)
5. Wispr Product & Data Sync meetings 2 Sep + 4 Sep (indexed; not IA nav source)
6. Local Product/Data: `/workspace/inc42-handover/BRIEF-CARD-DESIGN-BRIEF.md` §8 PostHog table (44% never-open, card1→card2 45%, etc.)
7. Local cross-refs: `BRIEF-15-UI-TYPES.md`, `app-info-hierarchy-brief.md`, `CLAUDE-HANDOFF-app-info-hierarchy.md`, `_wispr_design_extract.md`
8. Slack DM Satya↔Ranjith `D0BE781KY3V` (28 Aug Explore Article/Company tabs; 1 Sep sectional companies; 4 Sep Brief redesign; 28–29 Aug Brief/Streak prompts)
9. Slack DM Utkarsh↔Ranjith `D0BDDK0BZD0` (24 Aug watchlist in warehouse; 25 Aug Article/Explore revamp scope; 1 Sep Brief mix; 5 Sep design reaction)
10. Slack #tech-team-internal `C076FJ67BGW` 4 Sep Explore title readability (@Satya)
11. Slack search public+private (Watchlist, Streak, Explore/News/Companies phrases) — sparse on post-split IA; newsbots noise filtered out of quotes

