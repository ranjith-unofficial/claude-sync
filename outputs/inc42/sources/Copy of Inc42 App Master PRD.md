# PRD Final v3

# Inc42 App — v1 PRD (Final)

Owner: Utkarsh · Status: **canonical — single source of truth for v1.** Supersedes all earlier PRD tabs in this doc (archived below this tab). Companion: Launch Infra — Final (vendors, attribution, SKAN, identity).

## 1\. The product in one page

Inc42 is India's startup-intelligence company — investigative journalism \+ proprietary Datalabs data \+ the ecosystem's network. The app is its daily intelligence habit: "Not a newsletter. Not an algorithm. Inc42's journalism, Datalabs intelligence, and AI that explains what it means for you. One app, every morning. Then it ends."

The shape of v1:

* **Brief** — a finite, personalized morning brief that ends (the habit anchor).  
* **Explore** — the 12-year archive (\~30K+ articles) \+ the Datalabs company graph (70K+) on pull.  
* **Watchlist** — the things you track \+ their movements (the wedge \+ the Datalabs on-ramp).  
* **Company profiles** — glanceable Datalabs depth, the bridge from journalism into data.

Audience (ICPs): Founder · Investor · Startup Operator · BD & Partnerships · (Other). Personalization is by ICP \+ sectors \+ watchlist.

Operating constraint (native app): unlike the website, we can't hotfix — users must update, and App Store review adds latency. So: everything tunable lives in server-side remote config (caps, cadence, ranking, copy, taxonomy, flags); a force-update / min-version gate ships in v1; and features ship as coherent, ordered bundles (§11).

### Design principles (guardrails)

* Finite before infinite — opens to the Brief; ends with a "Done for today" endpoint; no feed continuation.  
* Depth on demand — headline → Decode → full article → entity profile, each by choice.  
* Watchlist is the personalization engine, not an algorithm — explicit choices, no behavioral feed.  
* Shown, not narrated — visible "relevant because…" attribution; no covert personalization.  
* Signal-dense cards, not image-forward — the audience scans for signal.  
* The reader earns its place — must beat inc42.com mobile (faster, focused, progress, bookmark).  
* Everything is Inc42 — no external aggregation.

## 2\. Information architecture

3 bottom tabs — Brief · Explore · Watchlist. Plus two persistent top-bar affordances: a global 🔍 search and an account avatar. Neither is a tab. No hamburger / drawer.

┌───────────────────────────────────┐  
│  Inc42            🔍        ( U )  │ ← global search \+ account avatar (every screen)  
│                                   │  
│            \[ active surface \]     │  
│                                   │  
├───────────────────────────────────┤  
│    ● Brief     Explore   Watchlist│ ← 3 tabs  
└───────────────────────────────────┘

* Article reader \= a full-screen modal from any surface (not a tab).  
* Company profile \= the shared tap-target (not a tab).  
* Ask Inc42 \= a mode, not a tab (dormant in v1; §8.2).

## 3\. Onboarding & auth

Seed flow (5 quick screens): welcome → role/ICP → sector groups (7 clubbed groups, pick ≤3) → watchlist seeds (≥1 required, 3 recommended, skip-with-friction; role×interest suggestions) → success. Onboarding state is offline-tolerant, synced on auth.

ONBOARDING — 5 steps (\~45–75s)  
\[1 Welcome\] → \[2 Role\] → \[3 Sector groups\] → \[4 Watchlist\] → \[5 Done\]  
2 Role:      ○ Founder  ○ Investor  ○ Operator  ○ BD  ○ Other  
3 Groups:    pick ≤3 →  Ecommerce & D2C · Consumer · Fintech · Enterprise & SaaS  
                        AI · Deeptech · Startup Ecosystem        (7 groups)  
4 Watchlist: ≥1 (3 recommended)   🔍 search \+  \[+ Razorpay\] \[+ Fintech\] \[+ Zepto\]   \[Skip ▸\]  
5 Done:      "You're set — here's your first Brief"

Groups → sectors mapping is server-side: picking a group applies the sector boost to all its child sectors. Authoritative child mapping:

* **Ecommerce & D2C** ← Ecommerce, D2C, Logistics  
* **Consumer** ← Consumer Services, Foodtech, Media & Entertainment, Travel Tech, Edtech, Health Tech, Agritech  
* **Fintech** ← Fintech, Cryptocurrency, Web3, Digital Brokerage, Insurance Aggregators & Comparison  
* **Enterprise & SaaS** ← Enterprise Services, Enterprise Tech, Cybersecurity, Real Estate Tech  
* **AI** ← AI, AI Governance  
* **Deeptech** ← Clean/Climate Tech, Space Tech, Semiconductors, Advanced Hardware, Manufacturing Solutions, Electric Vehicles  
* **Startup Ecosystem** ← Startup Ecosystem (article-tag-only — editorial is asked NOT to tag it on companies; no company\_sector equivalent, so it boosts articles, never company results)

Travel Tech maps to Consumer only (no double-boost via Ecommerce & D2C); Web3 maps to Fintech (alongside Cryptocurrency).

There is **no "Pick Topics" step in v1 onboarding** — onboarding collects role \+ sector groups \+ watchlist seeds only. A topics step may return in v1.1 as Explore filter-defaults; nothing in v1 ranking consumes followed topics.

**Auth**: anonymous use is allowed. A soft sign-in sheet triggers only on a gated action (Follow · \~5 profile views · 3rd Saved item). It completes the pending action and merges anon local data (saves, seeds). "Continue without account" stays available; cross-device sync needs an account.

**Sign in with Apple (launch-blocking)**: the sign-in sheet offers **Apple \+ Google \+ email** on iOS. Apple App Review Guideline 4.8 requires Sign in with Apple whenever any third-party login is offered — Google-only will be rejected. Android ships Google \+ email. All flows resolve to the same Inc42 auth user ID (identity convention: Launch Infra — Final, Identity section).

## 4\. Brief (the hero)

Reference prototype (interactive, all 4 ICPs): prototype-2026-06-10.html — https://drive.google.com/file/d/1naa66aU5CdQVcp3cjOvRDuNxlsGxyMs8/view. The prototype is the reference implementation of this model; these wireframes are the spec.

A finite, relevance-ranked stack of 6–8 cards that ends. Mon–Fri daily \+ Sat weekly recap \+ Sun off. Pushed \~7–8 AM local. Editorial cards \+ Datalabs signal cards, ranked most-relevant-to-you first. No sections — a single ranked stack; signal-type tags carry type orientation per card.

Consumption model: the Brief tab's resting state is a **cover screen**; opening it enters a full-screen **swipe-up story flow** — one card per screen, swipe up for the next, ending at Done.

COVER (Brief tab resting state)             STORY FLOW (opened; 1 card \= 1 screen)  
┌───────────────────────────────────┐       ┌───────────────────────────────────┐  
│  Brief        🔍          ( U )    │       │  ✕   TODAY'S BRIEF        2 / 8   │ ← progress to a finite end  
│                                   │       │ ■ Breaking · Fintech      ⭐ 🎯    │  
│  Good morning, Utkarsh            │       │                                   │  
│  🔥 Day 6 · Regular · 42 stories  │ ←streak│ Razorpay bags $75M Series G       │  
│                                   │  (here │ • What's new: closed $75M led by  │  
│  TODAY'S EDITION — Fri 4 Jul      │   only)│   \[Investor\] at \~$9B.             │  
│  "Late-stage fintech is back:     │       │ • Why it matters: extends payments│  
│   two mega-rounds in one week."   │ ←daily │   lead as TPV scales.             │  
│                                   │  edition line (editorial-written §4.6)    │  
│  8 stories · \~5 min               │       │ • The detail: funds lending \+ intl.│  
│                                   │       │ Relevant because you track Razorpay│ ← attribution slot  
│  \[ OPEN TODAY'S BRIEF ▸ \]         │       │ ✨ Decode   💬 "How big vs peers?" │  
│                                   │       │ \[ READ FULL STORY → \]             │  
├───────────────────────────────────┤       │        ↑ swipe up for next        │  
│  ● Brief    Explore    Watchlist  │       └───────────────────────────────────┘  
└───────────────────────────────────┘

**Card anatomy** (per story screen): signal-type tag (■ Breaking / ▤ Feature / ◆ Story / ▣ Funding) · headline · byline (By \[Author\] · Inc42 — journalism-first trust signal, in v1 display) · 3-bullet body (or deterministic funding block — §4.1 templates apply as full-screen variants) · ⭐ if it's a watchlist hit · 🎯 \+ the "relevant because…" label · ✨ Decode (opens as a sheet over the story) · 💬 suggested-question chip · READ FULL STORY (→ reader modal). Swiping past a card marks it read; progress (n / 8\) is the finiteness cue.

**Cover anatomy**: greeting · streak row (cover row \+ Explore strip; §4.5) · daily edition line (§4.6) · story count \+ read time · single CTA. No feed below the fold.

**Cover rules** (the cover is the \#1 brand surface, seen by every user every morning):

* The edition line is the hook, not metadata — a real editorial promise in the Daily Brief register (e.g. "Late-stage fintech is back: two mega-rounds in one week."), not a table-of-contents label. It synthesises the day and names the most consequential item without giving it away (curiosity-gap, peer-level, no clickbait cadence — must pass the tone gate). Authoring and ownership: §4.6.  
* "Relevant to you" pre-glance: when the day's brief has ≥1 boosted card for a tracked company/sector (§4.4 stage 3), surface it on the cover — "2 stories on companies you follow." Shown only when boosted cards exist.  
* Time-accurate greeting, greeting optional. "Good morning" must match local time (or be dropped, letting the edition line lead). Never a wrong-time-of-day greeting.  
* Dry missed-day recovery line: if the user skipped a day, one factual line — "You missed Thursday. It's still here." Shown only after a skipped day; dry register, no guilt.

**Decode (✨)**: per-card AI explainer, pre-seeded with the card's facts. Soft-capped, non-blocking (never wall the most-engaged). 💬 suggested-question chips are free. Always teaser-and-routes to the full article.

**Editorial governance (manual authoring in v1)**: brief content is written by editorial, manually — the headline and the 3-bullet summary are produced alongside publishing the source article on Inc42 (same hand, same moment — no net-new daily workload). The two daily lines (§4.6) are the only net-new editorial input. The LLM's v1 jobs are ranking (§4.4 stage 2\) and Decode (live, on-demand §4.2) — not summary generation. LLM-assisted drafting of bullets is a v1.1 efficiency option, human-approved.

### 4.1 Card states (zoomed)

EDITORIAL CARD — expanded (3-bullet Smart Brevity)     FUNDING / DATALABS SIGNAL CARD (deterministic, no LLM)  
┌───────────────────────────────────┐                  ┌───────────────────────────────────┐  
│ ■ Breaking · Fintech     ⭐  🎯    │                  │ ▣ Funding · Agritech        🎯     │  
│ Razorpay bags $75M Series G        │                  │ DeHaat · Series F                  │  
│ • What's new: closed $75M led by   │                  │ $60M · Jun 2026 · led by \[Inv\]     │  
│   \[Investor\] at \~$9B.              │                  │ Total raised $200M · HQ Patna      │  
│ • Why it matters: extends payments │ ← all 3 bullets  │ Relevant because you follow Agritech│  
│   lead as TPV scales.              │   editorial-     │ ⬛ View company →                   │  
│ • Detail: funds lending \+ intl.    │   written (v1)   └───────────────────────────────────┘  
│ Relevant because you track Razorpay│  
│ ✨ Decode   💬 "How big vs peers?" │                  COLLAPSED (tail card)  
│ Read full story →                  │                  ┌───────────────────────────────────┐  
└───────────────────────────────────┘                  │ ◆ Story  Meesho's GMV pivot   ⭐ ⌄ │  
                                                         └───────────────────────────────────┘

Swipe-card templates at launch \= only these two (the editorial 3-bullet card \+ the deterministic funding/signal card), each as a full-screen template, plus the collapsed tail treatment. No other card templates at launch.

### 4.2 Decode panel (✨)

┌───────────────────────────────────┐  
│ ✨ Decode · Razorpay $75M          │  
│ ───────────────────────────────── │  
│ In plain terms: this round values  │  
│ Razorpay \~$9B and funds a lending  │  
│ push while UPI margins stay thin.  │  
│ For a fintech founder: late-stage  │  
│ payments appetite is back.         │  
│ ───────────────────────────────── │  
│ 💬 How does this compare to peers? │ ← suggested-question chips (free, uncapped)  
│ 💬 What does it mean for my sector?│  
│ Read the full report →             │ ← always teaser-and-routes to the article  
│        (8 of 10 today · soft cap)  │ ← non-blocking; never a hard wall  
└───────────────────────────────────┘

### 4.3 Completion, slow-day & weekly states

DONE FOR TODAY (endpoint)              SLOW NEWS DAY (content-scarcity fallback)   SATURDAY "THIS WEEK"  
┌──────────────────────────┐          ┌──────────────────────────┐               ┌──────────────────────────┐  
│           ✓              │          │ Quieter day in the        │               │  This week  ▓▓▓░░         │  
│      Done for today      │          │ ecosystem.                │               │ Same finite stack — the   │  
│  Caught up — 8 stories.  │          │ Today's 4 developments \+  │               │ week's biggest movements  │  
│  ⭐ 3 from your watchlist │          │ 2 evergreen reads for you.│               │ instead of the day's.     │  
│  Back tomorrow \~7:30 AM.  │          │ (rule: ≥4 editorial \+ ≥2  │               │ Same cards, Decode,       │  
│  (no feed continuation)  │          │ signals, else backfill —  │               │ endpoint. Sun \= off.      │  
└──────────────────────────┘          │ never a 2-line digest)    │               └──────────────────────────┘  
                                       └──────────────────────────┘

Slow-news-day expression \= fewer cards \+ a "This week" recap card, not signal-card padding.

### 4.4 Relevance (how the brief ranks)

The brief format is fixed for everyone; relevance changes ordering \+ labels, not which content exists (no filter bubble; editorial keeps control). Three-stage model:

1. **Editorial featured pin (manual).** Editorial marks one (or a few) story per day as Featured / Editor's Pick via the CMS Featured toggle (deployed ✅). These occupy the top card(s), most prominently, for everyone — human judgment owns the lead, not a score.  
2. **LLM daily base rank.** The LLM ranks all remaining stories in the candidate pool by newsworthiness/importance that day → the base order beneath the pinned lead(s).  
3. **Deterministic personal boost.** On top of the LLM base, a deterministic bump for stories about companies or sectors the user tracks/follows (w\_entity·tracked \+ w\_sector·sector; tracked-entity outweighs sector). Deterministic, not learned — auditable and explainable.

Rules:

* Featured pins are never demoted by the personal boost; the boost only re-orders the non-pinned pool.  
* Uniform across ICPs in v1 — personalization \= user's sectors \+ watchlist, not ICP-tuned weights (that's the v1.1 Emphasis Layer).  
* "Relevant because…" label appears only when the personal boost (stage 3\) lifted a card ("…you track Razorpay", "…you follow Fintech") — never on featured pins or pure LLM-rank position.  
* Cold-start: empty watchlist → boost from sectors only; skipped onboarding → featured pins \+ LLM base only (the general brief).  
* Boost weights are server-side \+ remote-config tunable, validated on a \~2-week concierge backtest — structure fixed here; numbers lock after data.  
* v1 \= pin \+ rank \+ boost \+ labels only. The Emphasis Layer (per-ICP lead-sentence \+ per-article-type ordering) \+ section summaries → v1.1.

**Canonical completion event: brief\_completed \= final card of the day's brief reached.** This one definition is used everywhere it appears: streak day-credit (§4.5), the completion-rate metric (§12), and SKAN conversion tier 3 — the paid-ads optimization target (Launch Infra — Final). No other definition ("most cards," time-based) is in effect.

### 4.5 Streaks

Mechanic:

* Earned on completing the daily brief (brief\_completed — final card reached), not on opening.  
* No dedicated streak push — streak nudging folds into the existing completion nudge (§8.5 \#2), inside the caps.  
* Sat recap counts toward the streak; **Sun (no brief) never breaks it**; no streak-freeze / paid-repair mechanics ever.  
* Rationale: rewards the finish (aligned with "then it ends"), never manufactures anxiety to reopen.

Reward model — two tiers of surface (full-screen milestone canvas kept from design; editorial, non-Duolingo register):

**Surface 1 — Daily (lightweight, no interruption).** On ordinary days there is no interstitial. The streak lives as:

* the cover row (§4 cover): Day N · \<tier\> · X stories · Y companies tracked — a substance counter, not just a number. Data definition: X stories \= cumulative stories read since install; Y companies tracked \= current watchlist count (live, not cumulative).  
* the Explore header strip (Figma screen 27 format): badge \+ Day N · \<tier\> \+ dot row.  
* Register is dry-but-substantive and editorial. Never gamification voice ("Amazing Start\! Think You Can Do It Tomorrow?" is off-brand — do not ship copy in that register).

**Surface 2 — Milestone full-screen** (Figma screen 26 canvas: radial burst, badge, dot row). Fires only at Day 1 · 7 · 30 · 100\. Ordinary days never trigger it. Payload in v1 \= substance counter \+ tier promotion only — no share, no unlock, no reward mechanic (those wait for the subscription/rewards layer, which slots into this same screen later).

* Day 1 — context / first-run, not celebration. Explains the streak mechanic and confirms "you've started." Sets tier Reader.  
* Day 7 — "One full week." \+ substance counter. Promotes to Regular.  
* Day 30 — "A month in." \+ substance. Promotes to Insider.  
* Day 100 — "100 days. You live here." \+ substance. Promotes to Ecosystem Native. This is the last milestone — beyond Day 100 the full-screen never fires again; the streak lives only on the daily surfaces.  
* Re-firing after a reset: if a streak breaks and the user re-reaches a milestone day, the full-screen re-fires (the moment is earned again; it re-affirms the sticky tier they already hold — it never demotes). The milestone screen is day-based, not once-per-lifetime.

**Reader tiers** (Reader → Regular → Insider → Ecosystem Native). Named as depth-in-the-ecosystem descriptors (peer-level, India-native), deliberately not league/points/gem naming. The tier is the reward.

* Tiers are **sticky** — a streak break does NOT strip your tier. The streak number is the volatile daily thing (resets on a miss); the tier is durable identity you keep once earned. An operator who travels two days is never demoted from "Insider."  
* Tier label rides both daily surfaces (cover row \+ Explore strip) between milestones.

Build note: the full-screen milestone screen is one reusable component (badge number \+ headline \+ substance line \+ tier line); the rewards/share/unlock row is a later addition to the same component, so v1 doesn't foreclose it.

### 4.6 The daily edition line (cover) & push copy ops

The cover line and the Morning Brief push line are **two separate, hand-written lines each day**.

* **Cover** \= the synthesis "why open" hook (full line, not length-capped like the push).  
* **Push** \= a dedicated hook to the push-first spec: hook in the first \~40 characters · ≤80 total · entity/tension-led, not category · tone-gate pass · never a label ("Today's top stories").  
* **No LLM in this surface** — both lines are written by editorial (same hand as the Daily Brief hook / Brief Integrity Owner); the newsletter hook may be raw reference input but is not reused verbatim.  
* **Ownership**: Marketing is accountable for both lines being populated daily and for feeding cover/push performance back to editorial; editorial writes and iterates on that feedback.

## 5\. Explore

The archive \+ company graph, on pull. Not a discovery feed (the Brief owns "today").

Layout: search bar → Today's Datalabs signals (collapsed) → content switch (Articles | Companies) → in-tab sub-navigation strip → feed → recently viewed.

**Articles** — sub-nav \= one horizontal pill strip, two groups:

\[ Latest \]\[ Funding \]\[ Features \]\[ M\&A & Policy \]\[ Startup Stories \] ┊ \[ Fintech \]\[ Edtech \]\[ AI \]\[ …17 sectors \]  
└──────────── FEEDS ────────────┘                                    └──────── INDUSTRIES ────────┘

Selecting an industry pill \= the Sector landing (§5.1). Article card \= thumbnail · \[signal-type\] chip · \[sector→\] chip · headline · byline · age · 🔖. Article filters: Sort \= Latest / Trending · Published \= Anytime / Today / This Week / This Month; tag vocabulary \= the development-tag → UI-tag mapping (Business · Funding · Controversies · IPO · Trends · Policy · People · M\&A · Financials · Venture Capital · Layoffs …) — to be grouped into 6–8 UI options (open with Ranjith); Sector \+ development-tag filters also apply on Articles.

**Companies** — sub-nav \= preset slices over Datalabs ES: Early Fundraisers · Recently Funded · Soonicorns · Just Launched · Unicorns · Watchlist, with filters Sector / Stage (Bridge · Early · Growth · Late · Public · Undisclosed · Bootstrapped) / Sort (includes Revenue; no Web Traffic). List rows (not a grid). Card: logo · name · \[status\] · \[sector→\] · \[stage\] · LAST RAISED \+ LEAD INVESTOR · EMPLOYEES band · "In 30 seconds" line (one-line static company summary — editorial/deterministic, not the live Decode explainer; §8.2) · ✨ Decode action · \[Track\].

**Search (global 🔍)** — one overlay from any screen. Companies surface first on entity match; articles below; Go to \[Sector\] → if a sector matches. Person/fund queries return coverage (articles), not entity cards (no people/investor profiles in v1).

**Reports** — deep-link rows only (📊 New report → opens web / email-gate). No in-app reader in v1.

**Today's Datalabs signals** — collapsed rail: top 3–5 market aggregates (funding/deals/sector flows/hiring). The only daily-fresh element here.

EXPLORE — ARTICLES                         EXPLORE — COMPANIES                       SEARCH OVERLAY (global 🔍)  
┌──────────────────────────┐               ┌──────────────────────────┐             ┌──────────────────────────┐  
│ Explore     🔍    ( U )  │               │ ┌────────┬─────────────┐ │             │ 🔍 razorpay           ✕  │  
│ 🔍 Search Inc42 & Datalabs│              │ │Articles│  COMPANIES  │ │             │ ── COMPANIES ──          │  
│ ▸ Today's signals      ⌄ │               │ └────────┴─────────────┘ │             │ ⬛ Razorpay·Fintech·SerG \[+\]│  
│ ┌────────┬─────────────┐ │               │ Recently Funded  Top  › │ │             │ ── Go to Fintech → ──    │  
│ │ARTICLES│  Companies  │ │               │                    \[⚲\]  │ │             │ ── ARTICLES (24) ──      │  
│ └────────┴─────────────┘ │               │ ⬛ Razorpay   ● Active   │ │             │ Razorpay bags $75M · 3h  │  
│ Latest Funding ┊ Fintech›│               │  Fintech·Pmts  Series G │ │             │ Razorpay lending · 2w    │  
│ ┌──┐■Breaking ·Fintech   │               │  $75M·Jun26·$1.4B tot   │ │             │ ── Get a synthesized     │  
│ │IM│Razorpay $75M…    🔖 │               │  Bengaluru·1k–5k   \[✓\]  │ │             │    answer → (dormant)    │  
│ └──┘Inc42 · 3h           │               │ ⬛ Mensa     ● Active    │ │             └──────────────────────────┘  
│ ┌──┐▤Feature ·Ecommerce  │               │  Ecommerce  Series D    │ │             (person/fund → coverage,  
│ │IM│Why D2C goes offline │               │  $50M·Mar26·$300M tot   │ │              not an entity card)  
│ └──┘Inc42 · 1d        🔖 │               │  Bengaluru·501–1k  \[+\]  │ │  
│        … (20/page)       │               │        … (20/page)      │ │  
└──────────────────────────┘               └──────────────────────────┘

### 5.1 Sector landing (the industry-tag destination)

┌──────────────────────────┐  
│ ‹ Explore   🔍    ( U )  │  
│ Fintech         \[+ Track\]│  
│ ₹4,200 Cr · 38 deals/30d │  
│ ┌────────┬─────────────┐ │  
│ │ARTICLES│  Companies  │ │ ← locked to Fintech  
│ └────────┴─────────────┘ │  
│ ■ Razorpay $75M…     3h  │  
│ ▤ UPI's next act…    4d  │  
│        …                 │  
└──────────────────────────┘

Any industry tap (card chip, in-article tag, Articles industry pill, Companies "By Sector", search chip) → Explore scoped to that one sector: Articles-in-sector \+ Companies-in-sector \+ a \[+ Track sector\] button. Not a heavy dashboard.

The 17 canonical sectors (shared tag\_industry / company\_sector spine; sub-sectors/colloquial terms alias up): Fintech · Edtech · Ecommerce · Health Tech · Enterprise Tech · Enterprise Services · Media & Entertainment · Advanced Hardware & Technology · Consumer Services · Clean Tech · Real Estate Tech · Travel Tech · AI · Logistics · Agritech · Foodtech · Web3.

## 6\. Watchlist

The Following \+ Saved surface — the standing set of what you track \+ what you keep. Two sub-tabs:

┌───────────────────────────────────┐  
│  Watchlist     🔍        ( U )     │  
│ ┌──────────────┬────────────────┐ │  
│ │  TRACKING    │     Saved      │ │  
│ └──────────────┴────────────────┘ │  
│  Following (8)         \[+ Add\]    │  
│  ── COMPANIES ──                  │  
│  \[M\] Meesho   Series G · 14 alerts│ → company profile  
│  \[Z\] Zepto    Series F · 6 alerts │  
│  ── SECTORS ──                    │  
│  \# Fintech            · 9 alerts  │ → Sector landing  
│  ── RECENT ALERTS ──              │  
│  · Meesho: $275M raise        2h  │  
│  · Fintech: RBI norms         1d  │  
│  See all (90-day) →               │  
└───────────────────────────────────┘

* Track only Companies \+ Sectors in v1 (people/funds need profiles, which are v1.1+). Free caps \~15 companies \+ 5 sectors; hitting a cap → soft "more depth coming — notify me," never a hard wall.  
* Track from anywhere (one tap): Brief cards, Explore rows, search, in-article tags, profile \[+ Track\]. \[+ Add\] \= Datalabs search-as-you-type.  
* Recent Alerts \= the in-app ledger of all tracked-entity movements (surfaced in the daily digest or not); last 20 in view, "See all" → 90-day rolling.  
* Saved sub-tab absorbs bookmarks (one-tap 🔖 from cards / reader). Recency-sorted, flat. Anon \= local (cap 50), merged on sign-in.  
* Monetization on-ramp dormant — cap hits \+ 🔒 depth show "coming soon" capture; no "Pro/Plus/Subscribe/₹" wording.

SAVED sub-tab                         EMPTY — TRACKING                 EMPTY — SAVED  
┌──────────────────────────┐         ┌──────────────────────────┐    ┌──────────────────────────┐  
│ ┌─────────┬───────────┐  │         │ Track what matters to     │    │ Stories you save show up  │  
│ │Tracking │   SAVED   │  │         │ your day.                 │    │ here.                     │  
│ └─────────┴───────────┘  │         │ \[+ Add\]                   │    │ Tap 🔖 on any story.      │  
│ Saved (14)               │         │ Suggested:                │    │                           │  
│ Why India's OTT… · May14 │         │  \[+ Meesho\] \[+ Fintech\]   │    │                           │  
│ 📊 State of Fintech·May12│         │  \[+ Zepto\]  \[+ AI\]        │    │                           │  
│  … (recency, flat)       │         └──────────────────────────┘    └──────────────────────────┘  
└──────────────────────────┘

## 7\. Company entity profile

The page you land on when you tap a company anywhere. A glanceable consumption view of existing Datalabs data — company profiles only in v1 (investor \+ person deferred to v1.1/v1.2+, investor first; so person/fund search → coverage).

┌─────────────────────────────────────┐  
│  ‹          \[ \+ Follow \]        ⋯    │  
│  ⬛ COMPANY NAME                      │  
│  Sector · Sub-sector · HQ            │  
│  Founded YYYY · Active · ↗ website    │  
│  ┌ Funding ──────────────────────┐   │  
│  │ $XXM total · Latest: Series B  │   │  
│  │ $25M · Mar'26 · Key inv: A,B,C │   │  
│  └────────────────────────────────┘   │  
│  ┌ People ───────────────────────┐   │  
│  │ Founder — CEO · Founder — CTO  │   │  
│  └────────────────────────────────┘   │  
│  ┌ On Inc42 ─────────────────────┐   │ ← journalism tie-back  
│  │ • \[Headline\] 3d · \[Headline\]2w │   │  
│  └────────────────────────────────┘   │  
│  \[ Ask about COMPANY \]  (dormant)     │  
└─────────────────────────────────────┘

Order: Header → Funding → People → On Inc42 → Ask-stub.

**Launch depth — what's free in the app at launch:**

* Identity, HQ, founded, status, employee band, description  
* Total funding · latest round · top 3–5 investors  
* Founders \+ key CXOs (name/title/LinkedIn); full people list \+ job\_function breakdown  
* Recent Inc42 coverage (\~5) \+ one signal stat  
* Full round-by-round funding history \+ co-investors \+ funding-by-year chart  
* Employee-growth / web-traffic trendline charts, Glassdoor detail, acquisitions  
* **Headline historical P\&L** — YoY Revenue, Total Expense, Profit/Loss (\~3–5 yr trend, numbers \+ simple bar)

**Reserved (🔒, server-side field mask — never baked into the client):** detailed financials — full balance sheet (assets/liabilities), expense line-items / individual heads, financial ratios, EBITDA margin detail, cap table, valuation history, comparisons. These remain Datalabs Pro's product (₹1,499/mo web) — the app deliberately doesn't compete with it. The P\&L headline is a deliberate, accepted partial overlap: it's the traction hook; the financial \*depth\* is the un-conceded Pro moat. The tier boundary is a remote-config flip, never an app release.

Design note: the Figma profile's full financials block is placeholder — build the profile from this real field set: keep a headline P\&L strip (YoY Revenue / Total Expense / Profit-Loss \+ simple bar), drop the balance-sheet / expense line-item / ratio / EBITDA-detail sections.

## 8\. Cross-cutting surfaces

### 8.1 Global search

Top-bar 🔍 opens the one Explore overlay from any screen; opening from an entity pre-seeds the query. (Detail §5.)

### 8.2 Decode & Ask

**Naming**: the live, on-demand AI explainer is **"Decode"** ("Decode this", "Decoded") everywhere it appears — brief cards, the Decode action on Explore article/company cards, and the profile Ask-stub. Decode is always a live LLM action the user triggers, not a pre-written line. **"Signal" is reserved for the data vocabulary only** — the ■/▤/◆/▣ signal-type tags, the "Today's Datalabs signals" rail, watchlist significance-gated signals, and the data-team's Signal Engine all keep the word; Decode names the distinct thing the AI does to journalism (intelligence applied to reporting). No existing surface is renamed.

The static one-line card summary is NOT Decode. The pre-written one-liner on Explore article/company cards is editorial/deterministic, not a live AI call — it is named **"In 30 seconds"** (provisional; alternatives: "At a glance" / "The short version"). Keeping it distinct from Decode protects the "not an aggregator" line — Inc42 doesn't just condense headlines; Decode applies intelligence on demand.

* **Decode (✨)** — live v1, soft-capped, non-blocking (§4).  
* **Ask Inc42** — a mode, not a tab. Open-ended chat deferred to v1.1; two dormant stubs keep us ready: "Ask the archive" in search, "Ask about \[entity\]" on profiles. No live LLM call in v1.

### 8.3 Article reader

Full-screen modal from any surface. Header 🔖 → Watchlist Saved. In-article entity tags → company profile; sector tags → Sector landing. Dismiss returns to origin.

ARTICLE READER (modal, slides up)  
┌──────────────────────────┐  
│ ✕              🔖    ↗   │ ← close · save(→Saved) · share  
│ Razorpay bags $75M Series G│  
│ By \[Author\] · Inc42 · 3h  │  
│ ▓▓▓▓░░░░  (read progress) │  
│ \[focus-mode body, no nav  │  
│  chrome; entity tags →    │  
│  profile, sector → landing\]│  
│ ── Related on Inc42 ──    │  
│ • \[Headline\] • \[Headline\] │  
└──────────────────────────┘

### 8.4 Account (avatar)

Top-right avatar: Preferences (role · sector groups (the same 7 clubbed groups picked in onboarding — not the 17-sector filter list, §3) · push alerts · brief time) \+ Account (email · sign out · Delete account & data). Editable role/sectors. No subscription/billing UI in v1.

┌──────────────────────────┐  
│ \[U\] Utkarsh · Founder     │  
│     Fintech, Ecommerce    │  
│ ── PREFERENCES ──         │  
│ My role        Founder ▸  │  
│ My sectors   Fintech… ▸   │  
│ Push alerts        On ▸   │  
│ Brief time    7:30 AM ▸   │  
│ ── ACCOUNT ──             │  
│ utkarsh@inc42.com         │  
│ Sign out                  │  
│ Delete account & data    │ ← Apple requirement  
└──────────────────────────┘

### 8.5 Notifications

| \# | Push | Cadence | Trigger |
| :---- | :---- | :---- | :---- |
| 1 | Morning Brief | 1×/day, \~7–8 AM local | The daily drop. Copy \= the dedicated hand-written push line (§4.6, push-first spec) — never a generic "Your Brief is ready." |
| 2 | Brief completion nudge | ≤1 same-day, non-openers/incompletes only, stops on completion | Brief state machine. Doubles as the streak nudge — no separate streak push (§4.5). |
| 3 | Breaking | ≤1×/day | Manual / Marketing (not algorithmic) |
| 4 | Watchlist digest | 1×/day, grouped | **Daily digest** of tracked-entity movements (funding, major coverage) from deterministic templates — no LLM, no real-time triggers. Real-time significance-gated alerts → v1.1. |
| 5 | Winback | ≤1×/week, lapsed only | Scheduler |

Rules:

* Significance gating (fatigue firewall): only funding / M\&A / leadership / major policy / marquee coverage make the digest; routine mentions → ledger only.  
* Grouping ("3 updates in your watchlist") · per-entity mute · per-category opt-out.  
* Quiet hours 10 PM–7 AM local (queued → morning).  
* **Brief completion \= brief\_completed \= final card reached** (single canonical definition; §4.4). Success \= completion, not open.  
* Curiosity-gap alert copy ("New update on \[Company\]" — establish relevance, don't satisfy curiosity in the banner).  
* **Customer.io constraint**: local-time send is disabled on any message carrying A/B variants or a daily rate-limit. All push A/B tests run as **two separate messages with server-side (segment) assignment** so 7–8 AM local delivery is preserved.  
* Deep-linking per type · badge \= unread Watchlist alerts · permission-denied fallback (app fully works; re-ask ≤2×, only after a value moment).  
* Tier ladder: Free \= daily watchlist digest · Plus (v1.1) \= real-time alerts \+ custom triggers · Pro (v1.1+) \= Datalabs-grade signal alerts \+ rule-builder.

SIGN-IN SHEET (soft, on a gated action)   PUSH PERMISSION (after first brief)   PUSH EXAMPLES (curiosity-gap)  
┌──────────────────────────┐             ┌──────────────────────────┐          Inc42·now  Late-stage fintech is back — today's ← Morning Brief (dedicated push line, §4.6)  
│ Save to your account?     │             │ Tomorrow's Brief at 7:30? │                     biggest raise isn't who you'd guess.  
│ Keep saves \+ follows on   │             │ \+ alerts when tracked     │          Inc42·now  3 updates in your watchlist. ← daily digest (grouped)  
│ every device.             │             │ companies move.           │          Inc42·now  Big move in the ecosystem.   ← breaking  
│ \[ Continue with Apple \]   │             │ \[ Turn on notifications \] │          Inc42·11:30 You haven't seen today's    ← completion nudge  
│ \[ Continue with Google \]  │             │ \[ Not now \]               │                     Brief yet.   (non-openers only)  
│ \[ Continue with email \]   │             │ (asked once value shown)  │  
│ Continue without account  │             └──────────────────────────┘  
└──────────────────────────┘             (iOS: Apple \+ Google \+ email — Guideline 4.8; Android: Google \+ email)

### 8.6 Monetization (dormant, Apple-safe)

v1 \= Free tier only. Plus/Pro reserved in code (feature flags), no paywall, no upgrade prompts, no "Pro/Plus/Premium/Subscribe/₹" wording. Interest capture only ("coming soon / notify me"). v1.1 activates via Apple IAP.

## 9\. Platform & infra must-haves (v1)

| Must-have | Why |
| :---- | :---- |
| **Sign in with Apple** | Apple Guideline 4.8 — mandatory when any third-party login (Google) is offered. Launch blocker. |
| In-app account deletion | Apple requirement for any login app. Launch blocker. |
| Force-update / min-version gate | Retire a broken client when a backend change ships (native-release insurance). |
| Generalized remote config | Tune caps/cadence/ranking/copy/taxonomy/flags without an app release. |
| Privacy | ATT prompt (if tracking) \+ privacy policy \+ consent. DPDP-specific consent gate is consciously deferred (Launch Infra — Final §Consent); ATT still ships at launch. |
| Content-scarcity brief fallback | Min card count \+ evergreen backfill so a slow day still reads as a brief (≥4 editorial \+ ≥2 signals or supplement/skip). |
| Deep / universal links | Email & web → app to the right screen (the launch funnel). |
| Baseline accessibility | Dynamic Type, VoiceOver labels, contrast. |
| Offline | Cached brief \+ recently-viewed readable offline; search disabled with a clear message. |
| App Store ratings prompt | After a positive moment (completed-brief streak). |

## 10\. Data sources & dependencies

| Surface | Backend |
| :---- | :---- |
| Brief | Editorial pipeline (manually authored \+ approved by editorial; §4 governance) \+ Datalabs signals |
| Articles (Explore/search) | Inc42 hybrid search (/sqlquery) — 20-query reality check pending (launch-gating; owner: Ranjith \+ tech) |
| Companies \+ profiles | Datalabs entity search (ES) \+ company-detail |
| Reports | WordPress reports API (list-only) |
| Today's signals \+ Watchlist digest | Datalabs daily aggregate (digest assembly; deterministic templates) |

## 11\. Pushed to v1.1+ (the boundary)

* **v1.1** — deepen \+ monetize alerts: **real-time significance-gated watchlist alerts** \+ custom alert triggers (Plus) \+ Pro-grade signal alerts · Emphasis Layer \+ section-level summaries · LLM-assisted bullet drafting (human-approved efficiency layer over the v1 manual authoring) · investor profiles · saved searches · in-app report reader (if gating signed off) · Plus activation · topics step as Explore filter-defaults (if adopted).  
* **v1.2** — depth \+ monetization: person profiles · Ask Inc42 goes live · Pro-tier surfacing · audio "Listen" · share-with-team · deep-link discovery.  
* Ordering logic: habit → engagement → money; investor before person; never ship monetization UI before habit; each bundle is independently coherent.

## 12\. Success metrics (v1)

D7 ≥30% · D30 ≥15% · Brief completion ≥40% (brief\_completed \= final card reached) · push opt-in ≥55% · watchlist completion ≥30% · Decode usage ≥15% of opened stories · search/DAU ≥0.3 · Datalabs profile views/DAU ≥0.2 (M1) → 0.5 (M3) · crash-free ≥99.5%.

## 13\. Launch approach & key risks

**Rollout**: (a) a 48-hour TestFlight founding-reader wave (top \~2K Daily Brief openers), then (b) a staged Play rollout (10% → 50% → 100%) gated on crash-free rate and brief-completion. Kill criteria carry into the GTM plan's calibrate phase. (There is no closed 2-week pilot.)

**Risks:**

* **Editorial production capacity** — largely absorbed, low residual risk. The brief's headline \+ 3-bullet summary are authored alongside publishing the article itself (same editorial hand, same moment) — no net-new daily workload. The net-new editorial requirement is the two daily lines (cover hook \+ push line, §4.6); mitigate with a tight template and the content-scarcity fallback. LLM-assisted drafting stays a v1.1 efficiency option, not a v1 dependency.  
* **Search backend** — the Explore hybrid search is unverified (Cloudflare-gated); the 20-query reality check is launch-gating (owner: Ranjith \+ tech).  
* **Notification delivery on India Android** — Chinese-OEM background-kill can silently drop the Morning Brief; delivery-rate by OEM is instrumented from day one with a pre-scoped escalation (Launch Infra — Final).

## Open build-time decisions

* Decode soft-cap threshold \+ Apple-safe copy  
* Personal-boost weights (concierge backtest to validate; structure fixed in §4.4)  
* Signal-stat priority \+ logo source on profiles  
* Explore sub-nav: single strip vs Feeds|Industries toggle  
* Timezone defaults for non-India users  
* "In 30 seconds" final word choice (alternatives: "At a glance" / "The short version")  
* Article-tag grouping into 6–8 UI options (with Ranjith)  
* Datalabs in-app branding chip (in review)  
* Identity-convention eng owner (Launch Infra — Final, Identity section)

# Launch Infra Final

# Inc42 App — Launch Infrastructure & Measurement (Final)

Owner: Utkarsh · Status: **final spec for build handoff.** Companion to PRD — Final: the PRD (§8.5, §9) specifies what notifications do and what native capabilities are required; this doc names the vendors and the measurement/attribution/push-delivery infra, and flags what's launch-blocking. Out of scope here (build team owns them): the non-measurement §9 native must-haves — in-app account deletion, force-update/min-version gate, ratings prompt, offline/content-scarcity fallback.

## The stack (decided)

| Layer | Vendor | Notes |
| :---- | :---- | :---- |
| Attribution / MMP | **Singular** | AppsFlyer \= named backup. Free tier: 15k paid conversions/mo, self-serve. |
| Push / CRM | **Customer.io only** | MoEngage deferred to a delivery-rate trip-wire (§D5), not dropped. |
| Ad networks at launch | **Meta \+ Google** | Apple Search Ads not at launch → Firebase Analytics is launch-blocking. |
| Product analytics | **PostHog** (mobile SDKs) | Unified web→app funnels; covers every §12 metric. |
| Crash | **Firebase Crashlytics** | Tracks the ≥99.5% crash-free target. |
| iOS attribution | **SKAN 4** — 6-tier "highest-value reached" ladder | Optimize toward brief\_completed. Schema below. |
| Web↔app identity | Canonical user\_id \= **Inc42 auth user ID**; anonymous device UUID before registration | **OPEN: eng owner** — the one unresolved point. Spec below. |
| DPDP consent gate | **Deferred** | Not legally required until enforcement (May 13 2027). ATT still ships at launch. |

The binding constraint for the launch window is the PRD's §9 "we can't hotfix" rule: several pieces must be in the submitted binary at App Store review, so a missing SDK \= a full resubmission cycle.

## Part 1 — Rationale & findings

### 1.1 Attribution / MMP

An MMP is required the moment we buy installs on ≥2 networks. Meta, Google, and Apple Search Ads each self-report installs in their own console — and each claims credit for the same install. Without a neutral MMP you cannot get: (a) cross-network deduplicated installs, (b) true blended cost-per-install by campaign in one view, (c) post-install in-app events (brief\_completed, watchlist-add, register) attributed back to the specific ad, or (d) deferred deep-link attribution (ad → install → land on the right screen). Firebase/GA4 gives in-app analytics but is not a cross-network arbiter.

**Singular** — free plan is genuinely self-serve and generous: 15k paid conversions/mo at $0 (no credit card, no sales gate), bundling the launch essentials — attribution, SKAdNetwork, deferred deep linking (Singular Links), fraud, and ad-cost/ROAS aggregation. Growth tier is $0.05/conversion (vs AppsFlyer's $0.07). Only paid conversions count, so with mostly-organic early installs on 2–3 networks we likely sit inside the free tier for weeks. Standard \~1–3 dev-day SDK integration.

Tradeoffs vs AppsFlyer (the named backup), all low-stakes for a free news app: (a) AppsFlyer's SKAN Conversion Studio is more polished — Singular hand-holds least on the pre-launch conversion-value schema (mitigation: the schema is locked below, implement early — §B1); (b) thinner India local support; (c) AppsFlyer Protect360 is the fraud benchmark (low install-fraud incentive for us). Where Singular wins: cheaper per conversion, and best-in-class cost/ROAS aggregation — pays off as the network mix widens. Singular Links fully covers the Customer.io email→app routing (OneLink equivalent).

Appendix — full MMP landscape considered:

| MMP | Free-tier reality | India / consumer fit | Pick it over AppsFlyer when… |
| :---- | :---- | :---- | :---- |
| Singular ✅ chosen | Free: 15k paid conv/mo, self-serve, incl. SKAN \+ deep linking \+ fraud; Growth $0.05/conv | Fine; India support thinner than AppsFlyer | Cheaper/conv \+ cost-ROAS aggregation that compounds as networks widen. |
| AppsFlyer (backup) | "Zero": \~12k conversions, full SKAN 4; Growth $0.07/conv | Best — local offices/support, broadest network integrations | Deeper India support \+ Protect360 fraud \+ more polished SKAN studio. |
| Kochava | Free App Analytics: \~10k conv/mo, covers paid \+ owned media, full MMP | Good; thinner India presence, less polished UI | Second free option if Singular's terms don't fit at signup. |
| Airbridge | 15k free installs, then flat $0.05/install, no contract | Works; India footprint unproven | You'll blow past free tiers fast and want a flat, contract-free rate. |
| Adjust | Thin (\~1,500 attributions/mo, 12-mo) | Fine, no cost edge | Already mid/enterprise scale; want flat predictable pricing. |
| Branch | Deep-linking free; paid attribution sales-gated (\~$199+/mo) | Deep-linking leader | Deep-linking is primary, paid attribution secondary. |
| Tenjin | No free MMP tier; from \~$200/mo | Gaming/ad-LTV heritage | Essentially never, for a news app. |
| No MMP (Firebase/GA4 \+ consoles) | Free | — | Only defensible on a single network. Firebase Dynamic Links is deprecated → no free deferred-deep-link fallback either. |

**iOS attribution mechanics (the irreversible decision).** Most iOS users deny ATT, so SKAdNetwork (SKAN 4\) is the primary iOS attribution channel. SKAN needs a conversion-value schema designed **before submission** — mapping the fine value (0–63) \+ coarse (low/med/high) to key early milestones inside measurement window 1 (D0–D2). If skipped: installs still count, but every post-install iOS event is unmeasurable, with no retroactive backfill. The schema is locked (§C2 below); engineering implements it exactly, pre-submission. AdAttributionKit (SKAN's successor) is interoperable and a fast-follow — not launch-blocking.

**Android.** Google Play Install Referrer is read automatically by the MMP/Firebase SDK on first launch. No custom work.

### 1.2 Product analytics

**PostHog** extends to the app (already on web → unified web→app funnels, one query surface). Its iOS/Android/React Native SDKs are production-grade: funnels, retention, feature flags, mobile session replay. Covers every success metric in PRD §12 (D1/D7/D30, brief-completion, onboarding/watchlist/search funnels, Decode tap-rate, push opt-in).

**Firebase/GA4** — required because we run Google App Campaigns. Google optimizes materially better on native Firebase events than on delayed MMP postbacks, and gates some features (e.g. excluding existing users) to Firebase-linked apps. So: ship the Firebase SDK and log core install/activation events to it as the Google-ads optimization layer; PostHog stays the product-analytics tool.

### 1.3 Crash & performance monitoring

**Firebase Crashlytics** — free, Firebase is already in the stack, AI crash insights, tracks crash-free ≥99.5% (PRD §12) out of the box. Sentry only if we later want unified backend+app error/trace visibility (fast-follow, §D4). Must be in the launch binary — launch-week crashes can't be captured retroactively.

### 1.4 Push & lifecycle messaging

**Plumbing (vendor-independent, LAUNCH-BLOCKING):** APNs .p8 auth key (Apple Developer → Keys; downloadable once — secure it) \+ Push Notifications & Background Modes entitlements in the app target (ship inside the binary), and a Firebase project \+ google-services.json bundled in the app for Android. Gotcha: no APNs token → FCM can't mint an iOS token. Create these artifacts first, regardless of vendor.

**Customer.io only at launch.** One tool for email \+ push \+ in-app, already wired, no new vendor onboarding inside the launch window; its RN SDK (push via FCM/APNs \+ in-app \+ local-timezone send \+ frequency caps \+ quiet hours) covers the §8.5 spec. Three knowingly-accepted gotchas to engineer around:

* **India Android OEM delivery (the real risk).** \~51% of Indian handsets are Chinese OEMs (Xiaomi/Oppo/Vivo) whose battery/background-kill breaks the FCM connection. Customer.io is bare FCM — no push-amplification fallback — so some Morning Briefs may silently not land on exactly the daily-habit devices we care about. Mitigation: instrument delivery-rate by device OEM from day one (§A3); if it dips below tolerance, MoEngage Push Amplification Plus (claims up to \+75% delivery on Xiaomi) is the pre-scoped fix (§D5).  
* **Grouped push isn't turnkey.** The daily watchlist digest's grouped notification needs custom Android notification-channel / summary-notification work on top of the SDK — not a Customer.io setting. Scoped into §B6.  
* **Local-time send has a disable condition.** Customer.io's per-user timezone send is disabled when a message also has a daily rate-limit or A/B variants. The Morning Brief push must not carry either — all push A/B tests run as **two separate messages with server-side (segment) assignment** (PRD §8.5), or the send silently reverts to fixed-UTC.

### 1.5 CDP / event pipeline / identity resolution

Defer the CDP (RudderStack) to fast-follow (weeks 4–8) — but the web↔app user\_id / distinct\_id convention is locked **now** (§C3). At launch the SDK set (PostHog \+ Singular \+ Customer.io \+ Firebase/Crashlytics) is manageable; a CDP isn't worth blocking launch. The ID convention is the load-bearing decision — it enables later identity stitching between anonymous web (PostHog) and logged-in app users. RudderStack (India-friendly, \~50–80% cheaper than Segment, event-priced) is the pick when event volume/identity pain becomes real.

### 1.6 Consent / India DPDP

DPDP Rules were notified Nov 13 2025; full consent/notice enforcement lands May 13 2027 — a calibrated grace period, so consent doesn't legally gate the launch. DPDP requires explicit consent for analytics (stricter than GDPR — no "legitimate interest" analytics). **Decision: the launch build ships without the consent gate**; tracking SDKs fire on first launch; a lightweight consent screen is scheduled well ahead of the May 2027 enforcement date (full CMP \= §D3). Accepted knowingly — a pre-deadline convenience, not a legal requirement today. **ATT (§B2) is a separate, still-required Apple prompt — unaffected by this deferral.** Revisit before Q1 2027\.

## Part 2 — Action items

🔴 \= must be in the submitted binary (non-hotfixable per PRD §9) or otherwise launch-blocking. 🟠 \= launch-required but server-side/config. ⚪ \= fast-follow.

### A. Start immediately (lead-time-critical — external dependencies)

* **A1. Create Apple APNs .p8 key \+ push entitlements, and the Firebase project.** 🔴 The vendor-independent plumbing under all push and Android analytics. Downloadable-once key (secure it); entitlements ship inside the binary. Gates everything downstream — do this first.  
* **A2. Open the Singular account (free / self-serve); request SKAN network IDs from Meta \+ Google.** 🔴 Signup needs no credit card or sales call, clears same-day. The MMP SDK and the networks' SKAdNetworkItems IDs must be in the submitted Info.plist — networks won't attribute to a build lacking their IDs. AppsFlyer is the named backup if Singular's terms surprise at signup.  
* **A3. Instrument push delivery-rate by device OEM in Customer.io from day one.** 🟠 The MoEngage trip-wire. Tag delivery/open by manufacturer (Xiaomi/Oppo/Vivo vs rest); if delivery on Chinese OEMs drops below tolerance, that's the signal to activate MoEngage Push Amplification Plus (§D5). Cheap to add now; converts a guess into a threshold.

### B. Launch-blocking build (must be in the submitted binary)

* **B1. Implement the SKAN 4 conversion-value schema (§C2).** 🔴 The irreversible one. Wire updatePostbackConversionValue() to the 6-tier ladder in the D0–D2 window; set brief\_completed as the network optimization target. Skip it and all post-install iOS measurement is lost with no backfill.  
* **B2. Ship the ATT prompt** (NSUserTrackingUsageDescription in Info.plist \+ AppTrackingTransparency). 🔴 Can't be added server-side; without it, zero consented-user iOS data.  
* **B3. Integrate the Singular SDK (iOS \+ Android)**, initialized on first launch; wire Singular Links for the deferred-deep-link \+ Customer.io email→app routing. 🔴  
* **B4. Integrate PostHog mobile SDK** as primary product analytics; define the core event taxonomy (the §12 metrics). 🔴 (SDK) / 🟠 (dashboards)  
* **B5. Integrate Firebase — Analytics \+ Crashlytics.** 🔴 Both launch-blocking: Google App Campaigns are in the launch mix, so Firebase Analytics is the Google-ads optimization layer, not optional; Crashlytics \= the ≥99.5% crash-free tracking.  
* **B6. Integrate the Customer.io RN SDK** with the notification spec (PRD §8.5): local-time Morning Brief, grouped daily watchlist digest, caps, quiet hours, deep-linking per type. 🔴 (SDK) Two build notes from §1.4: grouped push needs custom Android notification-channel/summary work; the Morning Brief push must not carry a daily rate-limit or A/B variants.  
* **B7. DPDP consent gate — deferred** (§1.6). ⚪ Skipped for the launch build. Ship a lightweight first-run consent screen well ahead of May 2027 enforcement; full CMP \= §D3. Revisit before Q1 2027\.  
* **B8. Implement the web↔app identity convention** (§C3) — canonical user\_id identify()\-ed into all four SDKs across web \+ app auth. 🟠 Cheap now, expensive to retrofit. The anonymous-device-ID minting on first open is build-time 🔴 (can't be assigned retroactively).  
* **B9. Hand the build team the consolidated "must be in the submitted binary" list** (A1, A2, B1–B6, \+ the B8 anonymous-ID minting). 🔴 Any missing SDK/entitlement \= a resubmission cycle that blows the window.

### C. Specs

**C2. SKAN conversion-value schema — "highest-value tier reached"** (Apple writes the highest milestone hit in the D0–D2 window — no strict nesting, so it tolerates that registration is optional and non-linear):

| Fine value | Milestone |
| :---- | :---- |
| 0 | Install |
| 1 | Onboarding complete (role \+ sectors \+ watchlist) |
| 2 | Brief opened |
| 3 | **Brief completed (brief\_completed \= final card reached) — the ad-optimization target** |
| 4 | Push opt-in (watchlist-add is the fallback if push-opt-in proves too sparse) — retention signal |
| 5 | Registered (optional; high value when it happens, sits at top) |

Both brief-open (2) and brief-completion (3) are on the ladder deliberately: point Meta/Google's optimization at completion, but because that event is rarer, if launch install volume falls below Apple's crowd-anonymity threshold and the fine value is suppressed, switch the network optimization target to open — a console change, no rebuild (the ladder is frozen at build time; the optimization target is not). A user who reads briefs but never registers correctly lands at 3–4. Engineering implements this exact ladder in B1, pre-submission.

**C3. Web↔app identity convention — OPEN: name the eng owner.** Canonical user\_id \= Inc42 auth user ID once known. Registration is optional on the app, so most users never have one — for them the app mints one anonymous device ID on first open (a UUID in device storage) and passes that to all four SDKs (PostHog, Customer.io, Singular, Firebase) on both web and app. Not email, not per-SDK IDs. Anonymous users are still fully measurable and still push-able — Customer.io pushes to a device-token-only anonymous profile, so the Morning Brief does not require registration. If/when a user registers, identify()/alias merges the anonymous ID → the Inc42 auth ID so pre-registration history stitches forward (PostHog \+ Customer.io both support anon→known merge). Web↔app stitching only happens for users who log in on both surfaces; anon-web ↔ anon-app can't be linked, which is expected (the MMP still attributes the install regardless of login). This is a convention, not a feature, so it needs one named owner enforcing it across both codebases — recommended: app tech lead defines the spec, web team implements their half. Not binary-blocking, but the anonymous-ID minting must be in the launch build, and it's cheapest to lock before either codebase ships tracking calls.

### D. Fast-follow (post-launch)

* **D1.** RudderStack CDP (weeks 4–8) — reduce SDK sprawl \+ own identity resolution once volume/pain is real. ⚪  
* **D2.** AdAttributionKit alongside SKAN when re-engagement / 3rd-party-store attribution matters. ⚪  
* **D3.** Full consent-management platform (CMP) ahead of the May 2027 DPDP enforcement date. ⚪  
* **D4.** Sentry if unified backend+app error/trace visibility becomes a need. ⚪  
* **D5.** MoEngage (Push Amplification Plus) — activate if the A3 delivery-rate trip-wire fires (Chinese-OEM delivery below tolerance). Pre-scoped fix, not a default. Enterprise sales-led onboarding (10-day lead) \+ MAU pricing ($5–6K/mo at 50–100K MAU) — start the conversation the moment the threshold trips, not before. ⚪

## Sources

Attribution/MMP: AppsFlyer, Kochava, Airbridge, Branch pricing pages; Singular MMP glossary; SKAN 4 schema (Aarki), SKAN 2026 (adlibrary); Play Install Referrer; Firebase Dynamic Links deprecation. Analytics: PostHog RN SDK \+ mobile replay; Firebase-for-UA (Addict, Lupu). Crash: Sentry-vs-Crashlytics (IndieAppStack), Shakebug 2026\. Push: Customer.io RN SDK \+ local-time; MoEngage Push Amplification \+ Amp+ impact; FCM/APNs setup; MoEngage (G2) \+ Customer.io pricing. CDP: RudderStack-vs-Segment (Volument). DPDP: Respectlytics, Secure Privacy.

# App PRD Final v2

# Inc42 App — v1 Product Requirements (Unified) — v2

**Owner**: Utkarsh · **Updated**: 2026-07-05 (**v2** — design-review reconciliation \+ 2026-07-05 decision batch; see §14) · **Status**: canonical — single source of truth for v1.

---

## 1\. The product in one page

**Inc42** is India's startup-intelligence company — investigative journalism \+ proprietary Datalabs data \+ the ecosystem's network. The app is its **daily intelligence habit**: *"Not a newsletter. Not an algorithm. Inc42's journalism, Datalabs intelligence, and AI that explains what it means for you. One app, every morning. Then it ends."*

**The shape of v1:**

- **Brief** — a finite, personalized morning brief that *ends* (the habit anchor).  
- **Explore** — the 12-year archive (\~30K+ articles) \+ the Datalabs company graph (70K+) on pull.  
- **Watchlist** — the things you track \+ their movements (the wedge \+ the Datalabs on-ramp).  
- **Company profiles** — glanceable Datalabs depth, the bridge from journalism into data.

**Audience (ICPs):** Founder · Investor · Startup Operator · BD & Partnerships · (Other). Personalization is by ICP \+ sectors \+ watchlist.

**Operating constraint (native app):** unlike the website, we can't hotfix — users must update, and App Store review adds latency. So: **everything tunable lives in server-side remote config** (caps, cadence, ranking, copy, taxonomy, flags); a **force-update / min-version gate** ships in v1; and features ship as **coherent, ordered bundles** (§11).

### Design principles (guardrails)

1. **Finite before infinite** — opens to the Brief; ends with a "Done for today" endpoint; no feed continuation.  
2. **Depth on demand** — headline → Decode → full article → entity profile, each by choice.  
3. **Watchlist is the personalization engine, not an algorithm** — explicit choices, no behavioral feed.  
4. **Shown, not narrated** — visible "relevant because…" attribution; no covert personalization.  
5. **Signal-dense cards, not image-forward** — the audience scans for signal.  
6. **The reader earns its place** — must beat inc42.com mobile (faster, focused, progress, bookmark).  
7. **Everything is Inc42** — no external aggregation.

---

## 2\. Information architecture

**3 bottom tabs — Brief · Explore · Watchlist.** Plus two persistent top-bar affordances: a **global 🔍 search** and an **account avatar**. Neither is a tab. **No hamburger / drawer.**

```
┌───────────────────────────────────┐
│  Inc42            🔍        ( U )  │ ← global search + account avatar (every screen)
│                                   │
│            [ active surface ]     │
│                                   │
├───────────────────────────────────┤
│    ● Brief     Explore   Watchlist│ ← 3 tabs
└───────────────────────────────────┘
```

- **Article reader** \= a full-screen modal from any surface (not a tab).  
- **Company profile** \= the shared tap-target (not a tab).  
- **Ask Inc42** \= a *mode*, not a tab (dormant in v1; §8.2).

---

## 3\. Onboarding & auth

**Seed flow (5 quick screens):** welcome → **role/ICP** → **sector groups** (**7 clubbed groups, pick ≤3** — v2, was "17 pick ≤5"; avoids choice paralysis) → **watchlist seeds** (≥1 required, 3 recommended, skip-with-friction; role×interest suggestions) → success. Onboarding state is offline-tolerant, synced on auth.

```
ONBOARDING — 5 steps (~45–75s)
[1 Welcome] → [2 Role] → [3 Sector groups] → [4 Watchlist] → [5 Done]

2 Role:      ○ Founder  ○ Investor  ○ Operator  ○ BD  ○ Other
3 Groups:    pick ≤3 →  Ecommerce & D2C · Consumer · Fintech · Enterprise & SaaS
                        AI · Deeptech · Startup Ecosystem        (7 — locked 2026-07-04)
4 Watchlist: ≥1 (3 recommended)   🔍 search +  [+ Razorpay] [+ Fintech] [+ Zepto]   [Skip ▸]
5 Done:      "You're set — here's your first Brief"
```

- **Groups → sectors mapping is server-side**: picking a group applies the sector boost to all its child sectors. **Grouping locked 2026-07-04 (Utkarsh's ruling); the team's "Clubbed Sectors" tab now reflects the 7 groups (reconciled 2026-07-05 against logic sheet `16v86Eyz…`).** Authoritative child mapping (from the sheet):  
  - **Ecommerce & D2C** ← Ecommerce, D2C, Logistics, Travel  
  - **Consumer** ← Consumer Services, Foodtech, Media & Entertainment, Travel Tech, Edtech, Health Tech, Agritech  
  - **Fintech** ← Fintech, Cryptocurrency, Digital Brokerage, Insurance Aggregators & Comparison  
  - **Enterprise & SaaS** ← Enterprise Services, Enterprise Tech, Cybersecurity, Real Estate Tech  
  - **AI** ← AI, AI Governance  
  - **Deeptech** ← Clean/Climate Tech, Space Tech, Semiconductors, Advanced Hardware, Manufacturing Solutions, Electric Vehicles  
  - **Startup Ecosystem** ← Startup Ecosystem *(article-tag-only — editorial is asked NOT to tag it on companies; no `company_sector` equivalent, so it boosts articles, never company results)*  
- **Mapping corrections (2026-07-05, from the sheet — supersede the earlier "unconfirmed defaults"):** Real Estate Tech → **Enterprise & SaaS** (not Consumer); Agritech → **Consumer** (not Deeptech); Foodtech → **Consumer** (not Ecommerce & D2C).  
- **Two sheet ambiguities to resolve with the team:** (a) **Travel** appears under *both* Ecommerce & D2C and Consumer (Travel Tech) — assign to one to avoid double-boost; (b) **Web3** is in the Companies sector-filter list but maps to no group — recommend → Fintech (alongside Cryptocurrency).  
- The team-proposed **"Pick Topics" step is NOT in v1 onboarding** pending adjudication (scoring input vs Explore filter-defaults — review doc Q1). If adopted as filter-defaults it may join later without touching the scoring formula.

**Auth:** anonymous use is allowed. A **soft sign-in sheet** triggers only on a gated action (Follow · \~5 profile views · 3rd Saved item). It completes the pending action and **merges anon local data** (saves, seeds). "Continue without account" stays available; cross-device sync needs an account.

---

## 4\. Brief (the hero)

> **Reference prototype** (interactive, all 4 ICPs): `prototype-2026-06-10.html` — [https://drive.google.com/file/d/1naa66aU5CdQVcp3cjOvRDuNxlsGxyMs8/view](https://drive.google.com/file/d/1naa66aU5CdQVcp3cjOvRDuNxlsGxyMs8/view). The prototype is the reference implementation of this model; these wireframes are the spec.

A **finite, relevance-ranked stack of 6–8 cards** that ends. Mon–Fri daily \+ Sat weekly recap \+ Sun off. Pushed \~7–8 AM local. Editorial cards \+ Datalabs signal cards, ranked most-relevant-to-you first. **No sections** — a single ranked stack (decision 2026-06-21); signal-type tags carry type orientation per card.

**Consumption model (v2, 2026-07-04 — adopted from design):** the Brief tab's **resting state is a cover screen**; opening it enters a **full-screen swipe-up story flow** — one card per screen, swipe up for the next, ending at Done. The *ranking, finiteness, and card semantics are unchanged*; only the reading gesture changed (scroll-stack → story flow).

```
COVER (Brief tab resting state)             STORY FLOW (opened; 1 card = 1 screen)
┌───────────────────────────────────┐       ┌───────────────────────────────────┐
│  Brief        🔍          ( U )    │       │  ✕   TODAY'S BRIEF        2 / 8   │ ← progress to a finite end
│                                   │       │ ■ Breaking · Fintech      ⭐ 🎯    │
│  Good morning, Utkarsh            │       │                                   │
│  🔥 Day 6 · Regular · 42 stories  │ ←streak│ Razorpay bags $75M Series G       │
│                                   │  (here │ • What's new: closed $75M led by  │
│  TODAY'S EDITION — Fri 4 Jul      │   only)│   [Investor] at ~$9B.             │
│  "Late-stage fintech is back:     │       │ • Why it matters: extends payments│
│   two mega-rounds in one week."   │ ←daily │   lead as TPV scales.             │
│                                   │  edition line (editorial-written §4.6)    │
│  8 stories · ~5 min               │       │ • The detail: funds lending + intl.│
│                                   │       │ Relevant because you track Razorpay│ ← attribution slot
│  [ OPEN TODAY'S BRIEF ▸ ]         │       │ ✨ Decode   💬 "How big vs peers?" │
│                                   │       │ [ READ FULL STORY → ]             │
├───────────────────────────────────┤       │        ↑ swipe up for next        │
│  ● Brief    Explore    Watchlist  │       └───────────────────────────────────┘
└───────────────────────────────────┘
```

**Card anatomy (per story screen):** signal-type tag (`■ Breaking / ▤ Feature / ◆ Story / ▣ Funding`) · headline · **byline (`By [Author] · Inc42`) — v1 display** (data exists; journalism-first trust signal) · 3-bullet body (or deterministic funding block — §4.1 templates apply as **full-screen variants**) · `⭐` if it's a watchlist hit · `🎯` \+ the **"relevant because…"** label · `✨ Decode` (locked name — §8.2; opens as a sheet over the story) · `💬` suggested-question chip · `READ FULL STORY` (→ reader modal). Swiping past a card marks it read; progress (`n / 8`) is the finiteness cue.

**Cover anatomy:** greeting · **streak row** (a daily streak surface — cover row \+ Explore strip; §4.5) · **daily edition line** (one editorial-authored line, "what today means" — *manually written by editorial*, same hand as the 3-bullet summaries; see §4.6) · story count \+ read time · single CTA. No feed below the fold.

**Cover improvements (v2, LOCKED 2026-07-05 — the cover is the \#1 brand surface, seen every user every morning; make it earn the position):**

1. **Edition line is the hook, not metadata.** The line above the fold must be a real editorial promise in the Daily Brief register (e.g. *"Late-stage fintech is back: two mega-rounds in one week."*), not a table-of-contents label. This is §4.6 applied to the cover — highest-leverage element on the screen.  
2. **The edition line IS the "why open" hook — one line, both jobs (LOCKED 2026-07-05, C6).** It synthesises the day *and* names the most consequential item without giving it away (curiosity-gap, peer-level, no clickbait cadence — must pass the tone gate). **Not a separate second line.** Sourced from the Daily Brief newsletter's hook (§4.6); the brief push notification reuses the same line (§8.5 \#1). Editorial-written (LLM may draft, editorial-approved).  
3. **"Relevant to you" pre-glance.** When the day's brief has ≥1 boosted card for a tracked company/sector (§4.4 stage 3), surface it on the cover: *"2 stories on companies you follow."* Makes personalization visible *before* the swipe — reinforces "not an algorithm, your choices" at first touch. Shown only when boosted cards exist.  
4. **Time-accurate greeting, greeting optional.** "Good morning" must match local time (or be dropped entirely, letting the edition line lead). Never a wrong-time-of-day greeting.  
5. **Dry missed-day recovery line.** If the user skipped a day, one factual line — *"You missed Thursday. It's still here."* — pulls lapsed opens back **without a push** (ties to the streak's Sun-safe forgiveness). Shown only after a skipped day; dry register, no guilt.

**Decode (✨):** per-card AI explainer, pre-seeded with the card's facts. **Soft-capped, non-blocking** (never wall the most-engaged). `💬` suggested-question chips are free. Always **teaser-and-routes** to the full article.

**Editorial governance (v2, 2026-07-04 — manual authoring in v1):** brief content is **written by editorial, manually** — the headline and the 3-bullet summary are produced **alongside publishing the source article on Inc42** (same hand, same moment — no net-new daily workload), and the **daily edition line** (§4.6) is the one net-new editorial input. The LLM's v1 jobs are **ranking** (§4.4 stage 2\) and **Decode** (live, on-demand §4.2) — *not* summary generation. This corrects the earlier "auto-summarize at 3 AM" model. LLM-assisted drafting of bullets is a **v1.1 efficiency option**, human-approved. *(Legacy auto-pipeline \+ cost envelope: `brief-prd.md`, now v1.1-relevant only.)*

### 4.6 The daily edition line (cover) & push copy ops

**The cover line and the Morning Brief push line are two separate, hand-written lines each day** . 

**Cover** \= the synthesis "why open" hook.   
**Push** \= a dedicated hook to the push-first spec: hook in the first \~40 characters · ≤80 total · entity/tension-led, not category · tone-gate pass · never a label ("Today's top stories"). 

No LLM in this surface — both lines are written by editorial (same hand as the Daily Brief hook / Brief Integrity Owner); the newsletter hook may be raw reference input but is not reused verbatim. 

**Ownership:** Marketing is accountable for both lines being populated daily and for feeding cover/push performance back to editorial; editorial writes and iterates on that feedback.

### 4.1 Card states (zoomed)

```
EDITORIAL CARD — expanded (3-bullet Smart Brevity)     FUNDING / DATALABS SIGNAL CARD (deterministic, no LLM)
┌───────────────────────────────────┐                  ┌───────────────────────────────────┐
│ ■ Breaking · Fintech     ⭐  🎯    │                  │ ▣ Funding · Agritech        🎯     │
│ Razorpay bags $75M Series G        │                  │ DeHaat · Series F                  │
│ • What's new: closed $75M led by   │                  │ $60M · Jun 2026 · led by [Inv]     │
│   [Investor] at ~$9B.              │                  │ Total raised $200M · HQ Patna      │
│ • Why it matters: extends payments │ ← all 3 bullets  │ Relevant because you follow Agritech│
│   lead as TPV scales.              │   editorial-     │ ⬛ View company →                   │
│ • Detail: funds lending + intl.    │   written (v1)   └───────────────────────────────────┘
│ Relevant because you track Razorpay│
│ ✨ Decode   💬 "How big vs peers?" │                  COLLAPSED (tail card)
│ Read full story →                  │                  ┌───────────────────────────────────┐
└───────────────────────────────────┘                  │ ◆ Story  Meesho's GMV pivot   ⭐ ⌄ │
                                                         └───────────────────────────────────┘
```

### 4.2 Decode panel (✨)

```
┌───────────────────────────────────┐
│ ✨ Decode · Razorpay $75M          │
│ ───────────────────────────────── │
│ In plain terms: this round values  │
│ Razorpay ~$9B and funds a lending  │
│ push while UPI margins stay thin.  │
│ For a fintech founder: late-stage  │
│ payments appetite is back.         │
│ ───────────────────────────────── │
│ 💬 How does this compare to peers? │ ← suggested-question chips (free, uncapped)
│ 💬 What does it mean for my sector?│
│ Read the full report →             │ ← always teaser-and-routes to the article
│        (8 of 10 today · soft cap)  │ ← non-blocking; never a hard wall
└───────────────────────────────────┘
```

### 4.3 Completion, slow-day & weekly states

```
DONE FOR TODAY (endpoint)              SLOW NEWS DAY (content-scarcity fallback)   SATURDAY "THIS WEEK"
┌──────────────────────────┐          ┌──────────────────────────┐               ┌──────────────────────────┐
│           ✓              │          │ Quieter day in the        │               │  This week  ▓▓▓░░         │
│      Done for today      │          │ ecosystem.                │               │ Same finite stack — the   │
│  Caught up — 8 stories.  │          │ Today's 4 developments +  │               │ week's biggest movements  │
│  ⭐ 3 from your watchlist │          │ 2 evergreen reads for you.│               │ instead of the day's.     │
│  Back tomorrow ~7:30 AM.  │          │ (rule: ≥4 editorial + ≥2  │               │ Same cards, Decode,       │
│  (no feed continuation)  │          │ signals, else backfill —  │               │ endpoint. Sun = off.      │
└──────────────────────────┘          │ never a 2-line digest)    │               └──────────────────────────┘
                                       └──────────────────────────┘
```

### 4.4 Relevance (how the brief ranks — v2 LOCKED 2026-07-04)

The brief format is **fixed for everyone**; relevance changes **ordering \+ labels**, not which content exists (no filter bubble; editorial keeps control). **Three-stage model** (revised from the 2026-06-21 formula — editorial now sets the top explicitly):

1. **Editorial featured pin (manual).** Editorial marks one (or a few) story per day as **Featured / Editor's Pick**. These occupy the **top card(s)**, most prominently, for everyone — human judgment owns the lead, not a score.  
2. **LLM daily base rank.** The LLM ranks *all remaining stories in the candidate pool* by newsworthiness/importance that day → the base order beneath the pinned lead(s). (Replaces the earlier "editorial-importance classifier base.")  
3. **Deterministic personal boost.** On top of the LLM base, a **deterministic** bump for stories about **companies or sectors the user tracks/follows** (`w_entity·tracked + w_sector·sector`; tracked-entity outweighs sector). Deterministic, not learned — auditable and explainable.  
- **Featured pins are never demoted** by the personal boost; the boost only re-orders the non-pinned pool.  
- **Uniform across ICPs in v1** — personalization \= user's sectors \+ watchlist, not ICP-tuned weights (that's the v1.1 Emphasis Layer).  
- **"Relevant because…" label** appears only when the *personal boost* (stage 3\) lifted a card ("…you track Razorpay", "…you follow Fintech") — never on featured pins or pure LLM-rank position.  
- **Cold-start:** empty watchlist → boost from sectors only; skipped onboarding → featured pins \+ LLM base only (the general brief).  
- **Boost weights are server-side \+ remote-config tunable, validated on a \~2-week concierge backtest** — *structure* locked here; *numbers* lock after data.  
- **Build need:** editorial CMS/tool needs a **"Featured" toggle** per story feeding the brief-assembly job (Q6-adjacent — confirm this exists or is built).  
- **v1 \= pin \+ rank \+ boost \+ labels only.** The **Emphasis Layer** (per-ICP lead-sentence \+ per-article-type ordering) \+ section summaries → **v1.1**.

### 4.5 Streaks (v2 — mechanic LOCKED 2026-07-04; reward model LOCKED 2026-07-05)

**Mechanic (unchanged):**

- **Earned on *completing* the daily brief** (final card reached), not on opening.  
- **No dedicated streak push** — streak nudging folds into the existing completion nudge (§8.5 \#2), inside the caps.  
- Sat recap counts toward the streak; **Sun (no brief) never breaks it**; no streak-freeze / paid-repair mechanics ever.  
- Rationale: rewards the finish (aligned with "then it ends"), never manufactures anxiety to reopen.

**Reward model — two tiers of surface (merges the Figma full-screen style with an editorial, non-Duolingo register). Reverses the earlier "kill the interstitial" call (brand-audit §2.2): we keep the design team's full-screen canvas, but re-time *when* it fires and re-voice *what* it says.**

**Surface 1 — Daily (lightweight, no interruption).** On ordinary days there is **no interstitial**. The streak lives as:

- the **cover row** (§4 cover): `Day N · <tier> · X stories · Y companies tracked` — a *substance counter*, not just a number. **Data definition (LOCKED 2026-07-05):** `X stories` \= **cumulative stories read since install**; `Y companies tracked` \= **current watchlist count** (live, not cumulative).  
- the **Explore header strip** (Figma screen 27 format, kept): badge \+ `Day N · <tier>` \+ dot row.  
- Register is dry-but-substantive and editorial. **Kill "Amazing Start\! Think You Can Do It Tomorrow?"** (off-brand gamification voice).

**Surface 2 — Milestone full-screen (Figma screen 26 canvas, kept — radial burst, badge, dot row).** Fires **only** at Day **1 · 7 · 30 · 100**. Ordinary days never trigger it (daily interruption is what reads as Duolingo; a *rare* full-screen moment reads as significant). Payload in v1 \= **substance counter \+ tier promotion only** — no share, no unlock, no reward mechanic (those wait for the subscription/rewards layer, which slots into this same screen later).

- **Day 1** — *context / first-run*, not celebration. Explains the streak mechanic and confirms "you've started." Sets tier **Reader**.  
- **Day 7** — "One full week." \+ substance counter. Promotes to **Regular**.  
- **Day 30** — "A month in." \+ substance. Promotes to **Insider**.  
- **Day 100** — "100 days. You live here." \+ substance. Promotes to **Ecosystem Native**. **This is the last milestone** — beyond Day 100 the full-screen never fires again; the streak lives only on the daily surfaces (cover row \+ Explore strip).  
- **Re-firing after a reset (LOCKED 2026-07-05):** if a streak breaks and the user re-reaches a milestone day, the full-screen **re-fires** (the moment is earned again, and it re-affirms the sticky tier they already hold — it never *demotes*). So the milestone screen is day-based, not once-per-lifetime.

**Reader tiers (Reader → Regular → Insider → Ecosystem Native).** Named as *depth-in-the-ecosystem* descriptors (peer-level, India-native), deliberately **not** league/points/gem naming. The tier is the reward.

- **Tiers are sticky — a streak break does NOT strip your tier.** The streak *number* is the volatile daily thing (resets to Day 1 on a miss); the *tier* is durable identity you keep once earned. Enforces the Sun-safe / forgiveness principle — an operator who travels two days is never demoted from "Insider."  
- Tier label rides both daily surfaces (cover row \+ Explore strip) between milestones.

**Build note:** the full-screen milestone screen is one reusable component (badge number \+ headline \+ substance line \+ tier line); the rewards/share/unlock row is a later addition to the *same* component, so v1 doesn't foreclose it.

---

## 5\. Explore

The archive \+ company graph, on pull. Not a discovery feed (the Brief owns "today").

**Layout:** search bar → *Today's Datalabs signals* (collapsed) → **content switch (Articles | Companies)** → **in-tab sub-navigation strip** → feed → recently viewed.

**Articles** — sub-nav \= one horizontal pill strip, two groups:

```
[ Latest ][ Funding ][ Features ][ M&A & Policy ][ Startup Stories ] ┊ [ Fintech ][ Edtech ][ AI ][ …17 sectors ]
└──────────── FEEDS ────────────┘                                    └──────── INDUSTRIES ────────┘
```

Selecting an industry pill \= the **Sector landing** (§5.1). Article card \= thumbnail · `[signal-type]` chip · `[sector→]` chip · headline · byline · age · 🔖. **Article filters (v2, from the team's logic sheet):** Sort \= Latest / Trending · Published \= Anytime / Today / This Week / This Month; tag vocabulary \= the development-tag → UI-tag mapping with 2026-07-04 renames (Business · Funding · Controversies · IPO · **Trends** · **Policy** · People · M\&A · Financials · **Venture Capital** · Layoffs …) — **to be grouped into 6–8 UI options** (open with Ranjith); Sector \+ development-tag filters also requested on Articles.

**Companies** — sub-nav \= preset slices over Datalabs ES (**v2 set — logic sheet \+ Utkarsh's 2026-07-04 comment rulings**): `Early Fundraisers · Recently Funded · Soonicorns · Just Launched · Unicorns · Watchlist` ("IPO-bound" dropped — no logic exists; "Tracked" renamed Watchlist), with filters **Sector / Stage (Bridge · Early · Growth · Late · Public · Undisclosed · Bootstrapped) / Sort (adds Revenue; Web Traffic removed)**. List rows (not a grid). Card (**v2 — richer, per design**): logo · name · `[status]` · `[sector→]` · `[stage]` · LAST RAISED \+ LEAD INVESTOR · EMPLOYEES band · **"In 30 seconds"** line (one-line *static* company summary — editorial/deterministic, **not** the live Decode explainer; §8.2) · `✨ Decode` action · `[Track]`.

**Search (global 🔍)** — one overlay from any screen. **Companies surface first** on entity match; articles below; `Go to [Sector] →` if a sector matches. **Person/fund queries return coverage (articles), not entity cards** (no people/investor profiles in v1).

**Reports** — **deep-link rows only** (`📊 New report → opens web / email-gate`). No in-app reader in v1.

**Today's Datalabs signals** — collapsed rail: top 3–5 market aggregates (funding/deals/sector flows/hiring). The only daily-fresh element here.

```
EXPLORE — ARTICLES                         EXPLORE — COMPANIES                       SEARCH OVERLAY (global 🔍)
┌──────────────────────────┐               ┌──────────────────────────┐             ┌──────────────────────────┐
│ Explore     🔍    ( U )  │               │ ┌────────┬─────────────┐ │             │ 🔍 razorpay           ✕  │
│ 🔍 Search Inc42 & Datalabs│              │ │Articles│  COMPANIES  │ │             │ ── COMPANIES ──          │
│ ▸ Today's signals      ⌄ │               │ └────────┴─────────────┘ │             │ ⬛ Razorpay·Fintech·SerG [+]│
│ ┌────────┬─────────────┐ │               │ Recently Funded  Top  › │ │             │ ── Go to Fintech → ──    │
│ │ARTICLES│  Companies  │ │               │                    [⚲]  │ │             │ ── ARTICLES (24) ──      │
│ └────────┴─────────────┘ │               │ ⬛ Razorpay   ● Active   │ │             │ Razorpay bags $75M · 3h  │
│ Latest Funding ┊ Fintech›│               │  Fintech·Pmts  Series G │ │             │ Razorpay lending · 2w    │
│ ┌──┐■Breaking ·Fintech   │               │  $75M·Jun26·$1.4B tot   │ │             │ ── Get a synthesized     │
│ │IM│Razorpay $75M…    🔖 │               │  Bengaluru·1k–5k   [✓]  │ │             │    answer → (dormant)    │
│ └──┘Inc42 · 3h           │               │ ⬛ Mensa     ● Active    │ │             └──────────────────────────┘
│ ┌──┐▤Feature ·Ecommerce  │               │  Ecommerce  Series D    │ │             (person/fund → coverage,
│ │IM│Why D2C goes offline │               │  $50M·Mar26·$300M tot   │ │              not an entity card)
│ └──┘Inc42 · 1d        🔖 │               │  Bengaluru·501–1k  [+]  │ │
│        … (20/page)       │               │        … (20/page)      │ │
└──────────────────────────┘               └──────────────────────────┘ │
```

### 5.1 Sector landing (the industry-tag destination)

```
┌──────────────────────────┐
│ ‹ Explore   🔍    ( U )  │
│ Fintech         [+ Track]│
│ ₹4,200 Cr · 38 deals/30d │
│ ┌────────┬─────────────┐ │
│ │ARTICLES│  Companies  │ │ ← locked to Fintech
│ └────────┴─────────────┘ │
│ ■ Razorpay $75M…     3h  │
│ ▤ UPI's next act…    4d  │
│        …                 │
└──────────────────────────┘
```

Any industry tap (card chip, in-article tag, Articles industry pill, Companies "By Sector", search chip) → **Explore scoped to that one sector**: Articles-in-sector \+ Companies-in-sector \+ a `[+ Track sector]` button. Not a heavy dashboard.

**The 17 canonical sectors** (shared `tag_industry` / `company_sector` spine; sub-sectors/colloquial terms alias up): Fintech · Edtech · Ecommerce · Health Tech · Enterprise Tech · Enterprise Services · Media & Entertainment · Advanced Hardware & Technology · Consumer Services · Clean Tech · Real Estate Tech · Travel Tech · AI · Logistics · Agritech · Foodtech · Web3.

---

## 6\. Watchlist

The **Following \+ Saved** surface — the standing set of what you track \+ what you keep. Two sub-tabs:

```
┌───────────────────────────────────┐
│  Watchlist     🔍        ( U )     │
│ ┌──────────────┬────────────────┐ │
│ │  TRACKING    │     Saved      │ │
│ └──────────────┴────────────────┘ │
│  Following (8)         [+ Add]    │
│  ── COMPANIES ──                  │
│  [M] Meesho   Series G · 14 alerts│ → company profile
│  [Z] Zepto    Series F · 6 alerts │
│  ── SECTORS ──                    │
│  # Fintech            · 9 alerts  │ → Sector landing
│  ── RECENT ALERTS ──              │
│  · Meesho: $275M raise        2h  │
│  · Fintech: RBI norms         1d  │
│  See all (90-day) →               │
└───────────────────────────────────┘
```

- **Track only Companies \+ Sectors** in v1 (people/funds need profiles, which are v1.1+). Free caps **\~15 companies \+ 5 sectors**; hitting a cap → soft "more depth coming — notify me," never a hard wall.  
- **Track from anywhere** (one tap): Brief cards, Explore rows, search, in-article tags, profile `[+ Track]`. `[+ Add]` \= Datalabs search-as-you-type.  
- **Recent Alerts** \= the in-app ledger of all tracked-entity movements (pushed \+ un-pushed); last 20 in view, "See all" → 90-day rolling.  
- **Saved** sub-tab absorbs bookmarks (one-tap 🔖 from cards / reader). Recency-sorted, flat. Anon \= local (cap 50), merged on sign-in.  
- **Monetization on-ramp dormant** — cap hits \+ 🔒 depth show "coming soon" capture; no "Pro/Plus/Subscribe/₹" wording.

```
SAVED sub-tab                         EMPTY — TRACKING                 EMPTY — SAVED
┌──────────────────────────┐         ┌──────────────────────────┐    ┌──────────────────────────┐
│ ┌─────────┬───────────┐  │         │ Track what matters to     │    │ Stories you save show up  │
│ │Tracking │   SAVED   │  │         │ your day.                 │    │ here.                     │
│ └─────────┴───────────┘  │         │ [+ Add]                   │    │ Tap 🔖 on any story.      │
│ Saved (14)               │         │ Suggested:                │    │                           │
│ Why India's OTT… · May14 │         │  [+ Meesho] [+ Fintech]   │    │                           │
│ 📊 State of Fintech·May12│         │  [+ Zepto]  [+ AI]        │    │                           │
│  … (recency, flat)       │         └──────────────────────────┘    └──────────────────────────┘
└──────────────────────────┘
```

---

## 7\. Company entity profile

The page you land on when you tap a company anywhere. A **glanceable consumption view** of existing Datalabs data — **company profiles only in v1** (investor \+ person deferred to v1.1/v1.2+, investor first; so person/fund search → coverage).

```
┌─────────────────────────────────────┐
│  ‹          [ + Follow ]        ⋯    │
│  ⬛ COMPANY NAME                      │
│  Sector · Sub-sector · HQ            │
│  Founded YYYY · Active · ↗ website    │
│  ┌ Funding ──────────────────────┐   │
│  │ $XXM total · Latest: Series B  │   │
│  │ $25M · Mar'26 · Key inv: A,B,C │   │
│  └────────────────────────────────┘   │
│  ┌ People ───────────────────────┐   │
│  │ Founder — CEO · Founder — CTO  │   │
│  └────────────────────────────────┘   │
│  ┌ On Inc42 ─────────────────────┐   │ ← journalism tie-back
│  │ • [Headline] 3d · [Headline]2w │   │
│  └────────────────────────────────┘   │
│  [ Ask about COMPANY ]  (dormant)     │
└─────────────────────────────────────┘
```

Order: **Header → Funding → People → On Inc42 → Ask-stub.**

- **Free (shown):** identity, sector/stage, HQ, founded, status, total raised, latest round, key investors, founders \+ key CXOs, employee band, recent Inc42 coverage, one signal stat.  
- **Reserved (🔒):** full funding history, cap table, MCA financials, valuation history, charts, comparisons. *(Field-level map: `premium-boundaries.md`.)*

**Launch-depth: LOCKED 2026-07-04 \= V2+ (V2 Deep \+ historical headline P\&L).** Axis \= *how much reserved data we give away free at launch to build traction*, traded against *Datalabs Pro web revenue* (₹1,499/mo — premium-boundaries rule \#2: don't compete with it). Tier boundary is always a **server-side field mask** (remote-config flip, no app release), never baked into the client. The chosen variant deliberately pulls **headline historical P\&L** (YoY Revenue / Total Expense / Profit-Loss) up into the launch tier for wow-factor, while keeping the *detailed* financial layer (balance sheet, expense line-items, ratios, cap table, valuation history) reserved as Pro's product.

| Field group (scout-db source) | V1 Glance (Free-only) | ✅ V2+ LOCKED (V2 Deep \+ P\&L) | V3 Full \= *Figma as drawn* |
| :---- | :---- | :---- | :---- |
| Identity, HQ, founded, status, employee **band**, description | ✅ | ✅ | ✅ |
| Total funding · **latest round** · top 3–5 investors | ✅ | ✅ | ✅ |
| Founders \+ key CXOs (name/title/LinkedIn) | ✅ | ✅ | ✅ |
| Recent Inc42 coverage (\~5) \+ **one** signal stat | ✅ | ✅ | ✅ |
| **Full round-by-round funding history** \+ co-investors \+ `getFundingByYear` chart | ❌ | ✅ | ✅ |
| **Employee-growth / web-traffic trendline charts**, Glassdoor detail, acquisitions | ❌ | ✅ | ✅ |
| Full people list \+ `job_function` breakdown | ❌ | ✅ | ✅ |
| **Headline historical P\&L** — **YoY Revenue, Total Expense, Profit/Loss** (\~3–5 yr trend, numbers \+ simple bar) | ❌ | ✅ **(A1 add)** | ✅ |
| **Detailed financials** — full balance sheet (assets/liabilities), **expense line-items / individual heads**, financial ratios, EBITDA margin detail, **cap table**, valuation history, comparison | ❌ | ❌ | ✅ |

- **V1 Glance** — mirrors Datalabs web *free* tier; zero cannibalization; weakest wow. Reserved fields absent from the client.  
- **✅ V2+ (LOCKED)** — V2 Deep (history, trendlines, full people) **plus** headline historical P\&L: **YoY Revenue, Total Expense, Profit/Loss** (\~3–5 yr). The financial *headline* is the traction hook; the financial *depth* (balance sheet, expense line-items, ratios, cap table) stays Pro-reserved. **Partial, deliberate Pro overlap**: P\&L headline numbers are visible in Datalabs Pro today, so this concedes a slice of Pro's surface in exchange for app wow-factor — accepted tradeoff. Cap table / full balance sheet / ratios / EBITDA detail remain the un-conceded Pro moat.  
- **V3 Full** — everything, incl. the **full financials chart \+ EBITDA/ratios the Figma profile already draws** (screen 31). **Directly cannibalizes Datalabs Pro web** (rule \#2 conflict). Not chosen.  
- **Figma vs locked scope**: the Figma profile currently draws the *full* financials block (= V3). For V2+, the design must **keep a headline P\&L strip** (YoY Revenue / Total Expense / Profit-Loss \+ simple bar) but **drop** the balance-sheet / expense line-item / ratio / EBITDA-detail sections (design-review fix B5, updated).

---

## 8\. Cross-cutting surfaces

### 8.1 Global search

Top-bar 🔍 opens the one Explore overlay from any screen; opening from an entity pre-seeds the query. (Detail §5.)

### 8.2 Decode & Ask

> **Naming (LOCKED 2026-07-05 \= Decode):** the **live, on-demand AI explainer** is **"Decode"** ("Decode this", "Decoded") everywhere it appears — brief cards, the Decode action on Explore article/company cards, and the profile Ask-stub. Decode is always a *live LLM action the user triggers*, not a pre-written line. **"Signal" is reserved for the data vocabulary only** and is *not* used for the explainer, resolving the four-way collision: the `■/▤/◆/▣` signal-type tags, the "Today's Datalabs signals" rail, watchlist "significance-gated signals," and the data-team's **Signal Engine** all keep the word; Decode names the distinct thing the AI does *to* journalism (intelligence applied to reporting). No existing surface is renamed. **The static one-line card summary is NOT Decode.** The pre-written one-liner on Explore article/company cards (the old "30-sec gist" / "30-sec snapshot") is editorial/deterministic, not a live AI call — it is named **"In 30 seconds"** (provisional; alternatives: "At a glance" / "The short version"). Keeping it distinct from Decode protects the "not an aggregator" line — Inc42 doesn't just condense headlines; Decode *applies intelligence* on demand.  
> 

- **Decode (✨)** — live v1, soft-capped, non-blocking (§4).  
- **Ask Inc42** — a **mode, not a tab**. Open-ended chat deferred to v1.1; two **dormant stubs** keep us ready: "Ask the archive" in search, "Ask about \[entity\]" on profiles. No live LLM call in v1.

### 8.3 Article reader

Full-screen modal from any surface. Header 🔖 → Watchlist Saved. In-article entity tags → company profile; sector tags → Sector landing. Dismiss returns to origin.

```
ARTICLE READER (modal, slides up)
┌──────────────────────────┐
│ ✕              🔖    ↗   │ ← close · save(→Saved) · share
│ Razorpay bags $75M Series G│
│ By [Author] · Inc42 · 3h  │
│ ▓▓▓▓░░░░  (read progress) │
│ [focus-mode body, no nav  │
│  chrome; entity tags →    │
│  profile, sector → landing]│
│ ── Related on Inc42 ──    │
│ • [Headline] • [Headline] │
└──────────────────────────┘
```

### 8.4 Account (avatar)

Top-right avatar: **Preferences** (role · **sector groups (the same 7 clubbed groups picked in onboarding — not the 17-sector filter list**, §3) · push alerts · brief time) \+ **Account** (email · sign out · **Delete account & data**). Editable role/sectors. No subscription/billing UI in v1.

```
┌──────────────────────────┐
│ [U] Utkarsh · Founder     │
│     Fintech, Ecommerce    │
│ ── PREFERENCES ──         │
│ My role        Founder ▸  │
│ My sectors   Fintech… ▸   │
│ Push alerts        On ▸   │
│ Brief time    7:30 AM ▸   │
│ ── ACCOUNT ──             │
│ utkarsh@inc42.com         │
│ Sign out                  │
│ Delete account & data    │ ← Apple requirement
└──────────────────────────┘
```

### 8.5 Notifications (merged model — LOCKED 2026-06-21)

| \# | Push | Cadence | Trigger |
| :---- | :---- | :---- | :---- |
| 1 | **Morning Brief** | 1×/day, \~7–8 AM **local** | The daily drop. **Copy \= the day's edition line** (§4.6), reused as the push — *not* a generic "Your Brief is ready." |
| 2 | **Brief completion nudge** | ≤1 same-day, **non-openers/incompletes only**, stops on completion | Brief state machine. *Doubles as the streak nudge — no separate streak push (§4.5).* |
| 3 | **Breaking** | ≤1×/day | **Manual / Marketing** (not algorithmic) |
| ~~4~~ | **~~Watchlist alerts~~** | **~~Real-time, grouped~~** | ~~Per-entity event, **significance-gated**~~ |
| 5 | **Winback** | ≤1×/week, lapsed only | Scheduler |

**Rules:**

- **Significance gating** (fatigue firewall): only funding / M\&A / leadership / major policy / marquee coverage push; routine mentions → **ledger only**.  
- **Grouping** ("3 updates in your watchlist") · **per-category caps** (Watchlist ≤\~3/day, then collapse) · **per-entity mute** · **per-category opt-out**.  
- **Quiet hours 10 PM–7 AM local** (queued → morning).  
- **Brief completion** \= reaches final card OR opens ≥60% of cards OR min reading time (success \= *completion*, not open).  
- **Morning Brief copy (LOCKED 2026-07-05):** the push text **is the day's edition line** (§4.6), sourced from the Daily Brief newsletter hook — written once, used on both the cover and the push. Never a generic "Your Brief is ready." Same tone gate; editorial-written (LLM may draft, approved).  
- **Curiosity-gap alert copy** ("New update on \[Company\]" — establish relevance, don't satisfy curiosity in the banner).  
- **Deep-linking** per type · **badge** \= unread Watchlist alerts · **permission-denied fallback** (app fully works; re-ask ≤2×, only after a value moment).  
- **Tier ladder:** Free \= real-time alerts on standard events · **Plus** (v1.1) \= custom triggers · **Pro** (v1.1+) \= Datalabs-grade signal alerts \+ rule-builder. The real-time **Signal layer is in v1** — size the build for it.

```
SIGN-IN SHEET (soft, on a gated action)   PUSH PERMISSION (after first brief)   PUSH EXAMPLES (curiosity-gap; copy A/B'd at build)
┌──────────────────────────┐             ┌──────────────────────────┐          Inc42·now  Late-stage fintech is back — today's ← Morning Brief = the edition line (§4.6)
                     biggest raise isn't who you'd guess.
│ Save to your account?     │             │ Tomorrow's Brief at 7:30? │          Inc42·now  New update on Razorpay.      ← watchlist (single)
│ Keep saves + follows on   │             │ + alerts when tracked     │          Inc42·now  3 updates in your watchlist. ← grouped (≥2)
│ every device.             │             │ companies move.           │          Inc42·now  Big move in the ecosystem.   ← breaking
│ [ Continue with Google ]  │             │ [ Turn on notifications ] │          Inc42·11:30 You haven't seen today's    ← completion nudge
│ [ Continue with email ]   │             │ [ Not now ]               │                     Brief yet.   (non-openers only)
│ Continue without account  │             │ (asked once value shown)  │
└──────────────────────────┘             └──────────────────────────┘
```

### 8.6 Monetization (dormant, Apple-safe)

v1 \= Free tier only. Plus/Pro reserved in code (feature flags), **no paywall, no upgrade prompts, no "Pro/Plus/Premium/Subscribe/₹" wording.** Interest capture only ("coming soon / notify me"). v1.1 activates via Apple IAP. *(Tiers: `premium-boundaries.md`.)*

---

## 9\. Platform & infra must-haves (v1)

| Must-have | Why |
| :---- | :---- |
| **In-app account deletion** | Apple requirement for any login app. Launch blocker. |
| **Force-update / min-version gate** | Retire a broken client when a backend change ships (native-release insurance). |
| **Generalized remote config** | Tune caps/cadence/ranking/copy/taxonomy/flags without an app release. |
| **Privacy** | ATT prompt (if tracking) \+ privacy policy \+ consent. |
| **Content-scarcity brief fallback** | Min card count \+ evergreen backfill so a slow day still reads as a brief (≥4 editorial \+ ≥2 signals or supplement/skip). |
| **Deep / universal links** | Email & web → app to the right screen (the launch funnel). |
| **Baseline accessibility** | Dynamic Type, VoiceOver labels, contrast. |
| **Offline** | Cached brief \+ recently-viewed readable offline; search disabled with a clear message. |
| **App Store ratings prompt** | After a positive moment (completed-brief streak). |

---

## 10\. Data sources & dependencies

| Surface | Backend |
| :---- | :---- |
| Brief | Editorial pipeline (manually authored \+ approved by editorial; §4.5-governance) \+ Datalabs signals |
| Articles (Explore/search) | Inc42 hybrid search (`/sqlquery`) — *Cloudflare allowlist \+ 20-query check pending (Task \#17)* |
| Companies \+ profiles | Datalabs entity search (ES) \+ company-detail |
| Reports | WordPress reports API (list-only) |
| Today's signals \+ Watchlist alerts | Datalabs daily aggregate \+ real-time Signal layer (new in v1) |

---

## 11\. Pushed to v1.1+ (the boundary)

- **v1.1 — deepen \+ monetize alerts:** custom alert triggers (Plus) \+ Pro-grade signal alerts · Emphasis Layer \+ section-level summaries · **LLM-assisted bullet drafting** (human-approved efficiency layer over the v1 manual authoring) · **investor profiles** · saved searches · in-app report reader (if gating signed off) · Plus activation. *(Bylines pulled into v1 display.)*  
- **v1.2 — depth \+ monetization:** **person profiles** · Ask Inc42 goes live · Pro-tier surfacing · audio "Listen" · share-with-team · deep-link discovery.  
- **Ordering logic:** habit → engagement → money; investor before person; never ship monetization UI before habit; each bundle is independently coherent.

---

## 12\. Success metrics (v1)

D7 ≥30% · D30 ≥15% · **Brief completion ≥40%** · push opt-in ≥55% · watchlist completion ≥30% · Decode usage ≥15% of opened stories · search/DAU ≥0.3 · Datalabs profile views/DAU ≥0.2 (M1) → 0.5 (M3) · crash-free ≥99.5%.

## 13\. Key risks to watch

1. **Editorial production capacity — largely absorbed, low residual risk.** The brief's headline \+ 3-bullet summary are authored **alongside publishing the article itself** on Inc42 (same editorial hand, same moment) — so they carry **no net-new daily workload**. The **only net-new editorial requirement is the one daily "edition line"** (§4.6, cover). Residual risk is small and scoped to that one line; mitigate with a tight template and the content-scarcity fallback. LLM-assisted drafting stays a v1.1 efficiency option, not a v1 dependency.  
2. **Search backend** — the Explore hybrid search is unverified (Cloudflare-gated); treat the 20-query check as launch-gating (Task \#17).  
3. **Notification fatigue / build size** — real-time alerts pulled into v1; significance gating \+ grouping \+ caps are the firewall, and the Signal layer enlarges the build (re-check the 2–3 week estimate).

### Design build notes (resolved 2026-07-05 — from design-review Q4/Q5/Q7)

- **Swipe-card templates at launch \= only the two already speced** (§4.1): the **editorial 3-bullet card** \+ the **deterministic funding/signal card** (no LLM), each as a full-screen template, plus the collapsed tail treatment. **No other card templates at launch** (Q4).  
- **The Figma company-profile financials are placeholder** (Q5) — build the profile from the **real free-tier / V2+ field set** (§7), not the invented fields the mockup draws.  
- **Slow-news-day (content-scarcity) expression \= fewer cards \+ a "This week" recap card**, not signal-card padding (Q7); rule ≥4 editorial \+ ≥2 signals else backfill (§4.3, §9).

### Open build-time decisions

Decode soft-cap threshold \+ Apple-safe copy · personal-boost weights (concierge-backtest, to validate) · **editorial "Featured" toggle exists/built? (§4.4)** · signal-stat priority \+ logo source on profiles · sub-nav: single strip vs Feeds|Industries toggle · timezone defaults for non-India users · **"Pick Topics" adjudication** (recommendation: keep as Explore filter, *not* an onboarding step — awaiting final call; review doc Q1) · Datalabs in-app branding chip (brand audit N4) · **logic-sheet updates the team still owes**: IPO-Bound→Soonicorns, Stage \+Public, Sort \+Revenue; resolve Travel (two groups) \+ Web3 (unmapped).

---

## 14\. Decisions log

- **2026-06-13** — People/investor profiles deferred to v1.1+ (investor first) → company profiles only; Watchlist \= Company \+ Sector; Saved → sub-tab; person search → coverage.  
- **2026-06-19** — Explore in-tab sub-navigation \+ Sector landing \+ card/chip specs.  
- **2026-06-21** — Notifications: full merged model (real-time Signal layer pulled into v1); engine: ranking+labels only (Emphasis Layer → v1.1), **pure relevance-ranked brief stack** (no sections), investor-tracking dropped; must-adds locked; native-release constraint adopted; this unified PRD made the canonical source of truth.  
- **2026-06-21 (relevance engine)** — Ranking \= **Editorial Importance base \+ Personal Relevance boost** (boost \= w\_entity·tracked \+ w\_sector·sector); **stage dropped from scoring AND onboarding** (onboarding now 5 steps); **uniform weights across ICPs** (ICP content-tilt → v1.1 Emphasis Layer); **top editorial story pinned to top 3**; weights server-side, remote-config tunable, validated on a concierge backtest before lock.  
- **2026-06-21 (detail pass)** — Full end-state \+ empty-state wireframes added across all surfaces; expanded card \= **3-bullet Smart Brevity** (all bullets editorial-written — the 2026-07-04 manual-authoring lock supersedes this earlier auto/human-edit split); **Saturday recap \= the same finite stack labeled "This week"**; notification copy \= curiosity-gap **principle only, exact templates A/B'd at build**; Brief **reference prototype** linked (`prototype-2026-06-10.html`).  
- **2026-07-04 (logic-sheet comment rulings — Utkarsh)** — Onboarding groups locked at **7** (Ecommerce & D2C · Consumer · Fintech · Enterprise & SaaS · AI · Deeptech · Startup Ecosystem); company slices: IPO-bound → **Soonicorns**, Tracked → **Watchlist**, "Unicorns"; Stage adds **Public**; Sort adds **Revenue** / drops Web Traffic; tag renames (Venture Capital / Policy / Trends); article tags to be grouped 6–8 \+ Sector/tag filters (open w/ Ranjith).  
- **2026-07-04 (v2 — design-review reconciliation, see `design-review-v1.md`)** — Brief consumption \= **cover resting state \+ full-screen swipe-story flow** (ranking/finiteness/card semantics unchanged); **streaks in v1** (completion-earned, no streak push, cover-only UI, Sun-safe); onboarding sectors \= **clubbed groups, pick ≤3**; Explore adopts the team's **company slices \+ article filters**; richer company cards \+ sector-landing stats adopted from design; nav label stays **Brief**; "Pick Topics" NOT adopted pending Q1.  
- **2026-07-04 (Utkarsh decisions A1–A5, C4)** — **Relevance engine v2** (§4.4): editorial **manual "Featured" pin** → top card(s); **LLM ranks** the rest of the candidate pool daily; **deterministic boost** for tracked company/sector stories; labels only on boosted cards (replaces the 2026-06-21 "pin most-important \+ editorial-importance base" formula). **Brief authoring is manual editorial in v1** (headline, 3 bullets, cover edition line) — LLM does ranking \+ Decode only; LLM-assisted drafting → v1.1 (§4.5-governance, §4.6). **Bylines pulled into v1 display** (§4.1). **Company-profile depth**: LOCKED \= **V2+** (V2 Deep \+ headline historical P\&L: **YoY Revenue / Total Expense / Profit-Loss**; balance sheet, expense line-items, ratios, cap table, valuation history stay Pro-reserved) — §7. Deliberate partial Pro overlap on P\&L headline accepted for wow-factor. Newsletter relationship \= **adjacency** (brand audit N3).  
- **2026-07-05 (Utkarsh)** — **AI-layer name LOCKED \= "Decode"** (§8.2); "Signal" reserved for data vocabulary only (tags / Datalabs rail / watchlist / data-team Signal Engine), no existing surface renamed. **Company-profile depth LOCKED \= V2+** (§7, above). **Cover screen** — five improvements adopted (§4 cover): editorial "why open" tension line \+ edition line as hook, time-accurate/greeting-optional, "relevant to you" pre-glance when boosted cards exist, dry missed-day recovery line; the tension line and brief notification may be **manual (editorial/marketing) or LLM-authored**. Datalabs in-app branding \= still in review.  
- **2026-07-05 (Utkarsh — streak reward model)** — LOCKED (§4.5): keep the Figma full-screen streak canvas but **re-time \+ re-voice** it (reverses brand-audit §2.2 "kill the interstitial"). Two surfaces — daily cover row \+ Explore strip (substance counter \+ tier), and a **full-screen milestone** at Day 1/7/30/100 (Day 1 \= context/first-run). **Reader tiers**: Reader → Regular → Insider → Ecosystem Native, **sticky** (streak break resets the number, never strips the tier). v1 payload \= substance \+ tier only; share/unlock deferred to the subscription/rewards layer. Kill "Amazing Start\! Think You Can Do It Tomorrow?".  
- **2026-07-05 (Utkarsh — handoff-gap rulings)** — **Editorial authoring** rides existing article publishing (no net-new daily work); **only the edition line is net-new** (§4.6, §13). **Streak substance counter**: `X stories` \= cumulative since install, `Y companies` \= current watchlist count (§4.5). **Milestone re-fire**: full-screen re-fires when a milestone day is re-reached after a reset; never demotes tier (§4.5). **Day 100 is the final milestone** — beyond it, daily surfaces only (§4.5). **Onboarding 7-groups → 17-sectors** mapping to be reconciled from the logic sheet.  
- **2026-07-05 (Utkarsh — cover line, notifications, design Qs)** — **Cover edition line consolidated to ONE line** doing both synthesis \+ "why open" hook (C6); **sourced from the Daily Brief newsletter** (Weekly Brief on Saturdays) — near-zero net-new editorial work, still N3-adjacency-safe (§4.6). **Morning Brief push copy \= that same edition line** (§8.5 \#1), not "Your Brief is ready." **Q4:** no swipe-card templates beyond the speced editorial 3-bullet \+ deterministic funding/signal cards at launch. **Q5:** Figma profile financials are placeholder — build from the real free-tier/V2+ field set. **Q7:** slow-day \= fewer cards \+ "This week" recap card (§13).  
- **2026-07-05 (Utkarsh — Decode vs static summary)** — **Decode names only the live, user-triggered AI explainer.** The pre-written one-line card summary (old "30-sec gist" / "30-sec snapshot") is editorial/deterministic and is renamed **"In 30 seconds"** (provisional — alternatives "At a glance" / "The short version"; awaiting final word choice). Corrects the earlier plan to rename gist/snapshot → Decode (§8.2, §5). Keeps Inc42 out of "headline-condenser" (Inshorts) territory.

# AskInc42 \- PRD

# AskInc42 \- PRD

*Bringing Inc42’s existing AI assistant into the app.*

01\. Why are we doing this?

AskInc42 already exists and works — live on inc42.com, inside Datalab. The app has no equivalent. That gap matters because app readers behave differently from web readers: they open the app to get through today’s brief, not to research a question they arrived with. Porting the web experience as-is — a blank chat box — fails for exactly that reason: a blank box only works when the question already exists in the reader’s head before the interface does, which is true on Datalab and untrue in the app.

The opportunity, then, isn’t “build a chatbot.” It extends a capability Inc42 has already built and proven into a surface where the same blank-box interface would fail — using content Inc42 already produces, with no new editorial production cost beyond the review step in Section 06\.

## Problem statement

Bringing the existing AskInc42 backend into a native mobile app surfaces three concrete friction points, not just the abstract UX problem above:

| FRICTION | THE PROBLEM | ADDRESSED BY |
| :---- | :---- | :---- |
| Unacceptable latency | Mobile readers expect a response in a few seconds; the backend currently hangs well past that under load. | D15, Section 06 |
| Context blindness | The backend treats every query as a cold start, ignoring which screen the reader is actually on. | D13, Section 06 |
| Hostile formatting | Long text and Markdown tables don't render usably in a native mobile chat bubble; raw links aren't tappable widgets. | D14, Section 06 |

# 02\. The JTBD framework

Two rules, and they’re both load-bearing for every placement decision in this document:

* Never show a blank box. The reader is never asked “what do you want to know” — that puts the work of forming a question back on them, in the middle of a read.  
* Every surface already implies a question. Ask should reflect the question a reader already has at that point, not invent one — the test every placement in Section 10 was run against.

| SURFACE | THE QUESTION THE READER ALREADY HAS THERE |
| :---- | :---- |
| Story card (in today's brief) | "Tell me more about this one story." |
| Article detail | Same, deeper — they're already reading the full piece. |
| Company page | "What’s happening with this company?" |
| Sector page | "What’s happening in this sector, who’s in it?" |
| Watchlist | "What’s new in what I’m tracking?" |

# 03\. How we position it

*Positioning line: “AskInc42 is the question your daily brief didn’t answer — grounded in what Inc42 has actually reported, surfaced exactly where curiosity already exists, never a blank box.”*

| MODE | DESCRIPTION |
| :---- | :---- |
| Web — research mode | A reader lands on Datalab with a question already in mind. A blank input works because the question arrived before the interface did. |
| App — consumption mode | A reader opens the app to get through the brief. No pre-formed question means Ask has to borrow intent from wherever it’s placed. |

# 04\. Why this positioning

* Trust. Grounded only in Inc42’s own reporting, not the open web — every answer stays traceable to something Inc42 actually published, which matters because this is a business/finance audience that will fact-check.  
* Editors see and can edit the AI-drafted questions when they publish — not a separate verification layer, part of the same publish action (Section 06).  
* Category precedent exists for grounded, surfaced-in-context assistants beating general chatbots: Crunchbase Scout (per-company assistant), Robinhood Cortex (per-stock digest, Gold-gated, 95% positive feedback), Arc XP’s Ask The News (Washington Post, publisher’s-own-reporting only). Full competitor scan in the Appendix.

# 05\. Locked decisions, indexed

*A fast-reference index — every decision links to the section where its full detail lives.*

| ID | DECISION | REFERENCE |
| :---- | :---- | :---- |
| D1 | Ask is visible to every reader, logged in or not; the two flows behave differently. | Section 07 |
| D2 | Chat history is persistent, user-visible, and explicitly a Terms/Privacy commitment, not just a UX choice. | Section 09 |
| D3 | Thumbs up / down on every response, feeding a defined loop back into generation. | Section 13 |
| D4 | Generation is AI-drafted at publish time; the editor sees and can edit it as part of publishing. | Section 06 |
| D5 | Five placements in v1: story card, article detail, company page, sector page, Watchlist. No dedicated tab. | Sections 10, 15 |
| D6 | Sector detail page and Watchlist's Sectors sub-tab are different surfaces with different jobs. | Section 10 |
| D7 | Watchlist uses a rotating pool of static persona messages, not per-item generation. | Section 11 |
| D8 | No paid version. Fast and Deep modes are both free to use. | Section 08 |
| D9 | Primary guardrail: Ask must not reduce brief completion, measured as a cohort comparison. | Section 11 |
| D10 | Eval review owner: Ranjith, directly. | Section 13 |
| D11 | The chatbot must be trained on app-specific knowledge, not just article/Datalab content. | Section 06 |
| D12 | If a reader closes the app before a response finishes, a push notification tells them it's ready. | Section 07 |
| D13 | Each surface's entity is the primary context for the entire thread, not just the first message — every surface behaves the same way, until the reader explicitly diverts to a different topic. | Section 06 |
| D14 | Every response is capped around 150-200 words, no Markdown tables, sources shown as tappable citation cards instead of inline links. | Section 06 |
| D15 | Latency guardrails: Fast mode targets 5s, never exceeds 10s. Deep mode never exceeds 30s. | Sections 06, 11 |
| D16 | Personas are the five real Edit Role values: Founder, Investor, Operator, BD & Partnerships, Other. | Section 06 |
| D17 | Each persona has a fixed lens \- what they're always trying to learn, independent of topic \- that combines with the topic-specific rubric to produce the actual question. | Section 06 |

# 06\. How do we generate?

When an article is published, AI drafts one title per persona using the Topic × Persona rubric below. The editor sees these titles at the same time they publish the article — same action, not a separate queue or approval step — and can edit any of them directly if the phrasing is off. Whatever’s on the article when it publishes is what ships. That’s it.

## Personas — D16, confirmed from the real onboarding screen (Edit Role)

Five values, not three — this replaces every earlier placeholder guess (Founder/Investor/Operator, or Founder/Investor/Partnership) with what the app actually asks at onboarding.

| PERSONA | AS DESCRIBED ON THE ROLE-SELECTION SCREEN |
| :---- | :---- |
| Founder | “Track startups, competitors, funding, and market opportunities.” |
| Investor | “Discover investment opportunities with trusted startup intelligence.” |
| Operator | “Stay ahead with market signals, industry trends, and company updates.” |
| BD & Partnerships | “Find companies, decision-makers, and potential business partners.” |
| Other | “Explore startup data tailored to your interests and goals.” No role-based angle — but not generic either, see D17. |

## Persona lens — D17, the pattern behind every generated question

The layer that applies regardless of topic — what each persona is always trying to learn, independent of the specific story. The Topic × Persona rubric below is this lens refined per story type: lens \+ topic-specific fact \= the actual question.

| PERSONA | LENS — WHAT THEY'RE ALWAYS TRYING TO LEARN | QUESTION PATTERN | EXAMPLE — ZEPTO'S $350M RAISE |
| :---- | :---- | :---- | :---- |
| Founder | What this means for running or growing their own company. | \[Fact\] → what strategic or operational move does this reveal? | “What's the playbook Zepto ran to close this round?” |
| Investor | Whether this changes conviction, risk, or valuation logic. | \[Fact\] → what does this signal about risk or opportunity? | “Why did investors bet $350M on Zepto right now?” |
| Operator | The broader market/industry signal, not the deal itself. | \[Fact\] → what trend or shift does this represent? | “What does this raise signal about momentum in quick-commerce?” |
| BD & Partnerships | Who's involved, and what relationship doors this opens or closes. | \[Fact\] → what partnership or collaboration angle does this create? | “Does this change who's worth approaching for a quick-commerce partnership?” |
| Other | No role to lean on — but their followed topics/sectors from onboarding are already known (same data the brief ranking engine uses). | \[Fact\] → framed through whichever followed topic/sector the story actually matches, not a role. | Reader follows Consumer & Ecommerce: “What does Zepto's raise mean for the quick-commerce names you're tracking?” |

Correction: “Other” doesn't mean unknown. Followed topics and sectors are captured at onboarding for every reader regardless of role — that's real signal, and D17's job for “Other” is to use it. The plain generic template is reserved for the actual error case: a reader with no role and no followed topics/sectors, or a generation failure with nothing to fall back on — not the normal path for an entire persona segment.

| SURFACE TYPE | MECHANISM |
| :---- | :---- |
| Company / sector — templated | Persona sets the whole question; only the entity name varies. Low risk, no review bottleneck needed — the question is supposed to be category-level (“how is \[Company\] performing”), not story-specific. |
| Article / story card — AI draft \+ editor review | Persona \+ the article’s existing Topic tag (News/Deals/Financials/Trends/Regulatory/IPO/Team/Startups — already populated by the ranking engine, no new tagging infrastructure needed) set the generation rubric. |

## Topic × Persona rubric (representative slice)

| TOPIC | PERSONA | RUBRIC — WHAT THE DRAFT MUST FIND BEFORE AN EDITOR SEES IT |
| :---- | :---- | :---- |
| Deals | Investor | The deal's specific number (size, valuation, multiple) → what it implies about investor conviction. |
| Deals | Founder | The structure or terms named → what playbook it reveals. |
| Regulatory | Founder | The specific rule or deadline named → what it forces the founder to change. |
| Regulatory | Investor | The named policy shift → whether it changes the sector's risk profile. |
| Team | Investor | The specific role or person who moved → what it signals. |

*Representative slice — the full 8-topic × persona grid follows the same logic.*

## Pipeline, step by step

1. Editor publishes an article, same as today.  
2. AI drafts one title per persona, using the rubric above, shown to the editor right there in the publish flow.  
3. Editor edits any title directly if it reads off, same as they’d fix a headline. Nothing further to approve.  
4. Article goes live with its titles attached.

## Functional spec

| SPEC ITEM | VALUE, AND WHY |
| :---- | :---- |
| Chips shown per surface | 1 on article/company/sector, 1 on story card. More than one competes for attention against the single-tap-and-done interaction this feature is built around (Section 01). |
| Character limit | \~70 characters — fits one line at the card widths already mocked up (Appendix) without wrapping. |
| Reader's persona changes after a title was drafted | Re-select the already-drafted variant matching the new persona — all personas are drafted together at publish time, so this is a lookup, not a new generation event. |

D11 — The chatbot also needs to be trained on app-specific knowledge, not just article/Datalab content: Watchlist queries (“what’s happening in my tracked companies,” Section 02\) require the model to reason over the reader’s own app state, not just published articles.

## Context resolution — how a surface’s implicit question actually reaches the model

Every surface in Section 02/10 is built on the assumption that the system already knows what the reader is looking at. Mechanically, that means each surface passes what page it is and which entity is on it — a company page passes company \= Zepto, a sector page passes sector \= Fintech.

That context is the primary frame for the entire thread, not just the seeded first question. If a reader taps the Founder chip on Zepto's company page (“How will this help me?”), every follow-up in that same conversation is still about Zepto by default — the reader doesn't have to keep repeating the company name. This is the same rule on every surface: story card, article, company, sector. Context only shifts away from the original entity when the reader explicitly asks about something else within the thread — at that point the new topic takes over as the primary frame. The exact detection logic for “explicitly asks about something else” is engineering's call, not specified here; the product rule — sticky by default, overridden only on an explicit topic change — is what's locked.

| SURFACE | WHAT GETS PASSED AUTOMATICALLY |
| :---- | :---- |
| Story card / article | The article itself. |
| Company page | The company. |
| Sector page | The sector. |
| Watchlist | Not entity-specific — the rotating message pool (D7) doesn't need this. |

## Response format

Applies to every AskInc42 response in the app, not a toggle,  mobile is the only context this ships in.

| CONSTRAINT | WHY |
| :---- | :---- |
| \~150–200 words per response | A “wall of text” doesn't render as a usable answer on a phone screen. |
| No Markdown tables — bullet points instead | Tables break native mobile UI renderers. |
| Sources as tappable citation cards, not inline links | Sources are extracted separately and rendered as cards, not left as raw links in the text — this is what makes the trust positioning in Section 04 visible, not just claimed. |

## Latency guardrails — D15

| MODE | TARGET | HARD MAX | NOTES |
| :---- | :---- | :---- | :---- |
| Fast | 5 seconds | 10 seconds | Fast mode exists specifically to feel instant — 10s is a ceiling, not a normal case. |
| Deep | — | 30 seconds | Deep mode trades speed for Datalab-grounded depth; 30s is the outer bound, not a target to hit exactly. |

*Current backend latency runs 8–25 seconds under load — already over the Fast mode ceiling. Closing that gap is an engineering dependency, not something this document solves, but Section 03's “faster than web” positioning is only true once it does.*

# 07\. How do we make it accessible?

## Logged in

5. Reader taps a chip on any placed surface (Section 10).  
6. Chat opens and auto-fires immediately — no second tap.  
7. Response streams in; thumbs up/down available once it lands.

## Logged out

8. Chip is visible and tappable — not hidden from logged-out readers.  
9. Tapping opens the chat with the question pre-filled in the composer, not sent.  
10. Message sends only when the reader hits Enter/Send themselves.

## Reader leaves before the response is ready

11. Reader sends a question, then closes the app before the response finishes.  
12. Once it’s ready, a push notification is sent: “Your AskInc42 response is ready — tap to view.”  
13. Tapping the notification opens straight into that response.

# 08\. How gated is it?

No paid version (D8). There is no gating. Fast mode and Deep mode are both free to use, for now.

# 09\. Terms & conditions, privacy policy

| ITEM | WHAT CHANGES, WHERE, AND WHY |
| :---- | :---- |
| AI disclaimer | In-product, in the chat UI itself, and in Terms of Use: “AskInc42 is AI-generated and can make mistakes — verify anything important.” Needed because the positioning (Section 04\) rests on trust. |
| Privacy Policy §7.1 / §8 | Name the AI/LLM sub-processor once identified, with a data processing agreement and retention terms on file. The live Privacy Policy §5.1 already names Ask-style features as active, but no processor is named in §7.1 or §8 today. Bringing AskInc42 into the app increases what flows through that undisclosed processor (persona, Watchlist context, chat history). |
| Account deletion — data categories | Confirm Ask chat history (D2) is explicitly covered. It’s already grouped with “Saved articles” on the existing deletion screen — confirm that grouping is accurate once app-side history exists at real volume. |
| Personalization disclosure | Role/persona data now shapes AI-generated content shown to the reader (Section 06\) — confirm existing personalization language covers this use, or write a line that does. |

# 10\. Placement

## Sector detail page vs. Watchlist’s Sectors sub-tab — two different jobs

The sector detail page is a browsable surface: open to any reader exploring that sector, listing every company in it, closer in job to a company page than to anything personal. The Watchlist Sectors sub-tab is a personal, tracked surface: it only ever shows sectors this specific reader has saved. Same word (“sector”), different reader intent — a browsing reader on the sector page is asking “what’s happening in this space broadly”; a Watchlist reader is asking “what’s new in what I’ve already decided to follow.” They need different question framing for that reason, not just different UI chrome.

| SURFACE | STATUS | NOTES |
| :---- | :---- | :---- |
| Story card | Ship | Each individual story inside today's brief. Three finalist visual treatments already mocked up on a real screenshot — see Appendix. |
| Article detail | Ship | Persona-reframed single-story question (Section 06). |
| Company detail page | Ship | Persona-templated, entity name as the only variable. |
| Sector detail page | Ship | Lists companies in that sector — see reasoning above. |
| Watchlist — Companies / Articles / Sectors | Ship | Static rotating persona messages (D7, Section 11). |
| Dedicated Ask tab | Roadmap Phase 2 | No open bottom-nav slot in v1's confirmed 3-tab IA (Brief/Explore/Watchlist). Needs proven demand from Phase 1 first (Section 15). |

# 11\. What are the fallbacks?

* Watchlist has no single story to ground a question on → a rotating pool of 3–5 static persona messages, one shown per visit so it doesn't repeat (D7).  
* Reader has no role and no followed topics/sectors → the actual generic template, reserved for this case only (D17). Not the normal path for “Other” or any other persona.  
* Reader isn't logged in → chip still shows and opens the composer; sending requires Enter (Section 07). Access isn't blocked outright.  
* Guardrail, not a numeric placement gate (D9): Ask usage must not reduce brief completion. If Ask-users complete the brief less often than non-users, that's the signal to revisit the story-card treatment.  
* Latency guardrail, Fast mode (D15): target 5 seconds, never exceeds 10\.  
* Latency guardrail, Deep mode (D15): never exceeds 30 seconds.

# 12\. How do we monitor?

| EVENT | WHAT IT TELLS US |
| :---- | :---- |
| chip\_impression | Reach — did the chip render for this reader. |
| chip\_tap | Interest, by surface — reach vs. actual taps tells us which of the five v1 placements is pulling its weight. |
| chat\_autofired / chat\_manual\_sent | Splits logged-in vs. logged-out behavior (Section 07). |
| response\_thumbs\_up / \_down | Quality signal, feeds the loop in Section 13\. |
| editorial\_edit\_rate | How often an editor changes an AI-drafted title before publishing (Section 06\) — the health check on generation quality. |
| brief\_completed, split by Ask-user vs. non-user | The D9 guardrail, directly. |

# 13\. What is the feedback loop?

14. Reader leaves a thumbs up/down on a response.  
15. Ranjith reviews the aggregate, alongside editorial\_edit\_rate from Section 12\.  
16. Patterns feed back into the generation rubric (Section 06\) if a specific Topic × Persona combination consistently underperforms.

# 14\. How do we improve the product?

* Weekly — thumbs ratio and editorial-edit-rate reviewed together.  
* Monthly — per-surface engagement reviewed against the D9 guardrail. This is what decides when Roadmap Phase 2 triggers (Section 15), not a fixed date.

# 15\. Roadmap

| PHASE | TITLE | DESCRIPTION |
| :---- | :---- | :---- |
| Phase 1 — this PRD | Five placements, no paid version | Story card, article detail, company page, sector page, Watchlist. Fast and Deep modes, both free. |
| Phase 2 | Dedicated tab | A standalone Ask tab, triggered by Phase 1 usage data (Section 14), not a fixed date. |
| Phase 3 | Paywall — direction only | No model or timing decided. Named so it isn't lost, not scoped further here. |

# Pulse PRD v2

# PRD — Inc42 Pulse (Social Intelligence)

**Version**: v2.0 — combined · **Date**: 2026-07-30 · **Status**: Draft for review **Owners**: Ranjith (product & AI) · Utkarsh (research, decisions) · Nityam (design) · Editorial (daily review \+ allowlist) **Name**: **Pulse** — the reader-facing name for Social Intelligence.

> **This document merges two PRDs written in parallel.** Ranjith's *Social Intelligence (Pulse)* v1.0 (27 Jul) supplied the product mechanics and editorial workflow; a parallel research track supplied the evidence, supply data and legal analysis. Neither superseded the other — this is the reconciliation.

---

## 1\. What we are building

**Inc42 tells readers what happened. Pulse shows what the ecosystem is saying about it.**

Readers get the news from us. They get the opinion by scrolling LinkedIn and X. **Nobody packages the opinion.** That is the opportunity.

We collect top LinkedIn and X posts from ecosystem leaders, filter them, and turn them into 1–2 line summaries — placed in two spots in the app.

This is not a new product line. `research/01-audience-and-market.md` defines the Founders JTBD as *"know what happened, what it means for me, **and how my peers are reacting**"*, and names the **"peer-reaction layer"** in its feature set; `concept-note.md` **Decision E** cut it from v1 into the **v1.1 backlog**. Pulse is that item. It is also the app's planned activation of the third positioning pillar — *"Network ACCELERATES — minimal v1 activation"* — so it completes the Journalism → Intelligence → Network hierarchy rather than inverting it.

**Not a feed.** Four independent constraints (legal, supply, overlap, comps) each rule out an infinite scrolling surface.

### 1.1 The job: status is the driver, sensemaking is the delivery

We initially modelled this as an **efficiency** job — *save people the time of scrolling*. That is incomplete, and the incompleteness has consequences.

An independent 5-model review, given our constraints but not our design, framed the driver differently: **three of five read the job as status maintenance / ambient credibility** — *knowing what the people who matter are saying, so you are not the one who missed it.* The synthesis: **"status is the emotional driver; sensemaking is the functional delivery mechanism."**

Both are true. But which one leads changes the product:

| If the job is… | Then… |
| :---- | :---- |
| **Efficiency** (time saved) | Compression is the value. Shorter is better. Names are optional. Success \= fast reads |
| **Status** (not being caught out) | **The consequence of missing** is the value. **Named voices are load-bearing** — "Nithin Kamath argued X" transfers status; "an investor said X" does not. Controversy beats consensus. **Sharing is the point**, not a vanity metric |

**Design consequences, carried through this document:**

1. **Attribution is doubly load-bearing** (§10). It is not only the legal mechanism — it is the *product value*. Stripping names to save space destroys the thing people came for.  
2. **"Most Debated" is the status-richest block** (§5.2). Knowing where the room disagrees is the sharpest status good; it should not be the block that gets cut on thin days.  
3. **Share rate is a leading indicator, not vanity** (§16) — status-driven content gets forwarded precisely to display knowledge.  
4. **Copy should signal consequence, not convenience.** "What the ecosystem is arguing about today" carries status; "your 5-minute catch-up" sells time.

### 1.2 ⚠️ This materially weakens our own disconfirming evidence

Our headline demand risk (§16) is that VOC mining across 77K posts found the pain articulated at **\~0.046%**. Under the status framing, that null is much less informative than we treated it as:

**Nobody publicly posts "I'm anxious about missing things."** Status anxiety is, by definition, the thing you conceal — especially in front of the exact professional audience whose regard is at stake. So a public-text corpus is close to the **worst possible instrument** for detecting it. The null measures our instrument, not the need.

The same applies to the persona test: **all three framings we tested led with efficiency** ("read in five minutes, not five feeds"). We concluded urgency was weak having never put a status framing in front of them.

**Honest position: down-weight the VOC null, do not reverse it.** This does not evidence demand — it removes one of the three reasons we doubted it. The premise stays `ASSUMPTION — UNVALIDATED` and the Phase-2 research gate still applies. But we should stop citing 0.046% as though it were strong disconfirmation, and **a status-led framing must be added as a fourth variant** to any future framing test.

---

## 2\. Decisions locked

| \# | Decision | Source |
| :---- | :---- | :---- |
| D1 | **Name \= Pulse** | Ranjith |
| D2 | **Tier** \= Free teaser \+ Plus/Pro depth | Utkarsh |
| D3 | **LLM synthesis \+ 100% manual editorial approval.** Nothing auto-publishes. Automation with spot-checks only once the reject rate earns it | both |
| D4 | **Editorial review owns attribution grammar \+ verification standard** (§9) | Utkarsh |
| D5 | **Conflict-of-interest runs through editorial review**, via a separate queue (§9.4) | Ranjith |
| D6 | **Story-matching is enrichment, not a gate** (§4) | Utkarsh, on overlap data |
| D7 | **Allowlist \~200 voices, with sector-level personalisation** (§11) | Utkarsh, on supply data |
| D8 | **Quote component is switchable** — synthesis stands alone; quotes render behind a flag (§13) | Utkarsh |
| D9 | **Phased cadence**: Phase 1 rides the morning Brief; Phase 2 is a dedicated **evening** edition (§7) | Utkarsh |
| D10 | **Keep our voice DB until the Signal Engine switchover**; brief the data team on all fixes at handover | Utkarsh |
| D11 | Gaming / engagement-pod detection — **not a v1 concern** | Utkarsh |
| D12 | Prioritisation vs other v1.1 items is **out of scope** — separate thread | Utkarsh |
| D13 | **Ship the pipeline in Phase 1 — but with minimum viable machinery.** Tooling starts as a sheet-backed queue, not a custom admin app (§12). **Simplify the tooling, never the controls** (§9) | Utkarsh |
| D15 | **Commercial-conflict escalation triggers on NEGATIVE/political content, not on the commercial relationship** (§9.4). Relationship is visible context that raises priority | Utkarsh |
| D14 | **Status/FOMO is the emotional driver; sensemaking is the delivery** (§1.1) — attribution, controversy and sharing are product value, not just mechanics | Utkarsh, on council input |

---

## 3\. Scope

**In scope**

- Sources: LinkedIn and X, top posts from an allowlist of ecosystem voices  
- Two surfaces: in-article Pulse \+ the Pulse section  
- LLM-assisted filtering, grouping and drafting  
- **100% editorial review before anything publishes**  
- Sector-level personalisation  
- Free-tier experience; Plus/Pro depth reserved behind flags

**Not in scope**

- First-party trending ("Saved by 500+", read counts)  
- Comments, replies, likes, DMs, user-to-user follows — **we are not building a social network**  
- Any user-generated content  
- Infinite scroll anywhere  
- Article-length write-ups  
- Following individual people (the app has no person-follow primitive — §11)  
- Discourse-convergence clustering (v1.1 upgrade — §6.2)  
- Real-time / breaking social alerts  
- Gaming detection (D11)

---

## 4\. How it works

1. **Collect** — an agent pulls top posts daily from the allowlist across LinkedIn and X.  
2. **Filter** — an LLM removes the junk: irrelevant, promotional, thin, unverified (§8).  
3. **Enrich** — attempt to match each surviving post to an Inc42 story (by company / founder / event).  
4. **Group \+ draft** — the LLM clusters and writes a 1–2 line summary.  
5. **Review** — editorial approves, edits or rejects **every single one** (§9).  
6. **Publish** — approved Pulses go out per the cadence in §7.

### ⚠️ D6 — matching is enrichment, not a gate

The original design made a story match **required**. Measured over 60 days (1,768 quality-gated posts vs 785 Inc42 articles, ±3-day window, IDF-weighted matching with samples audited by eye): **only \~13% of quality ecosystem commentary corresponds to anything Inc42 published. 86.5% is orphan.**

The orphan half is also the *more* differentiated half — commentary is 87–92% absent from our editorial, while hard news is 26–73% already covered:

| Topic | Already in Inc42 editorial |
| :---- | :---- |
| `acquisition-merger` | 73% |
| `ipo-listing` / `funding-raised` | 32–35% |
| `company-milestone` / `hiring` | 26% |
| `industry-take` | **13%** |
| `macro-policy` | **8%** |

So: **unmatched items are first-class and flow to the Pulse section. Matched items *additionally* power in-article Pulse.** Gating on a match would have discarded \~87% of the material, including everything with no editorial substitute.

---

## 5\. The two surfaces

### 5.1 In-article Pulse

**Where**: at the end of an article, below the body. **Conditional**: appears only when the story has an approved Pulse. If there's nothing, the section does not exist. **No empty state.**

- **Collapsed (default)**: 1 line **\+ a visible attribution stub**. Reads in under 10 seconds.  
- **Expanded**: full 2-line summary \+ up to 4 attributed sources, each linking to the original post. *More sources, not more prose.*

```
THE PULSE
Investors are split on the valuation.
3 voices · Nithin Kamath, +2            View more →
```

⚠️ **The collapsed state must carry attribution.** A bare synthesised line — *"Investors are split on the valuation"* with no speaker — is exactly the **orphan assertion** §10 prohibits: unattributed, it reads as Inc42's own claim about a named company, which is the liability position we're trying to avoid. The attribution stub (count \+ one or two names) is therefore **not optional chrome**; it is the thing that makes the collapsed state legally sound. It also does double duty as the reason to expand.

⚠️ **Copy constraint**: the phrase *"3 founders you follow"* **cannot be used** — the app has no person-follow primitive (§11). Pulse resolves speakers via watchlist-company affiliation and sector, so honest copy is **"3 founders at companies you track"** or **"3 voices in your sectors"**.

### 5.2 The Pulse section

**⚠️ The blocks are phase-dependent.** The original design assumed two publishes a day; Phase 1 publishes **once** (it rides the morning Brief), which makes "new since the last publish" meaningless and the end-state copy wrong. Phase-aware definitions:

| Block | Content | Count | Phase 1 (1×/day) | Phase 2 (evening) |
| :---- | :---- | :---- | :---- | :---- |
| Today's Pulse | What the ecosystem is talking about now | 5 | ✅ | ✅ |
| Moving Fast | New since the last publish | 3 | ❌ **omit** — there is no "last publish" within the day | ✅ |
| Most Debated | Stories where opinion is split | 3 | ✅ | ✅ |
| This Week | Recurring themes | 5 lines | ✅ ⚠️ needs cross-day state (§4) | ✅ |

"This Week" is a 5-line thematic summary, not 5 discrete items. So the item counts are: **Phase 1 \= 8 items \+ the weekly summary** (3 blocks); **Phase 2 \= 11 items \+ the weekly summary** (4 blocks).

End-state copy must match the actual cadence — *"That's the pulse. Updated daily."* in Phase 1, *"…twice a day"* only if we ever publish twice. Timestamped. **No infinite scroll, no pagination, no "load more."**

⚠️ **"This Week" requires state the pipeline doesn't currently produce.** §4 is a same-day pipeline; recurring-theme detection needs a rolling multi-day store of approved items. Either add that store or defer the block — **don't ship it as an empty shell.**

⚠️ **Sizing check**: at full build that is **11 items per publish** (Phase 1: 8). Measured whole-ecosystem supply is **\~24 quality-gated items/day** (top-200 allowlist: 23/day median, 12 on a 1-in-10 bad day). The section is therefore sized at roughly half of total daily supply per publish — workable, but only because (a) the section is **not** subject to the ≥3-credible-posts rule that governs in-article Pulse, and (b) sector personalisation draws from a \~200-voice pool (§11). **Both must hold or the section runs dry and reads as a broken pipeline.**

### 5.3 How they differ

|  | In-article Pulse | Pulse section |
| :---- | :---- | :---- |
| Reader intent | "Tell me more about this" | "Tell me what's happening" |
| Scope | One story | Whole ecosystem |
| Entered from | Article | Brief card (Phase 1\) → own surface (Phase 2\) |
| Source | The \~13% that matches a story | The \~87% that doesn't |

**In-article Pulse ends a story. The Pulse section starts a session.**

---

## 6\. What a Pulse looks like

### 6.1 The four buckets

Every approved post gets exactly one bucket.

| Bucket | What it is | Lines | Why that length |
| :---- | :---- | :---- | :---- |
| **Reaction** | A leader gives their view on a news event | 1 | The stance carries it |
| **Insight** | Original analysis or a pattern nobody reported | 2 | A claim needs its evidence |
| **Announcement** | News from the person themselves ("we've raised $12M") | 1 | It's a fact — nothing to summarise |
| **Debate** | The event splits opinion into two clear camps | 2 | One line per side, or it reads biased |

### 6.2 Consensus vs split

| Type | When | Output |
| :---- | :---- | :---- |
| Consensus | 3+ credible posts, one dominant view (≥65%) | 1 line \+ sources |
| Split | 3+ credible posts, no dominant view | 2 lines, one per side |

**Fewer than 3 credible posts → no in-article Pulse.** The story gets nothing. This is deliberate: *most stories yield nothing, and Pulse stays rare and therefore meaningful.* **It does not apply to the Pulse section** (§5.2).

**v1.1 upgrade**: "Debate" currently requires posts already attached to one story. Discourse-convergence clustering (spec'd as Lane 5 in the Signal Engine brief, **not built**) would let us detect *N voices converging on a theme with no shared story* — the most differentiated unit available. Ships as an upgrade to the same bucket, not a new one.

### 6.3 Hard limits

- **Max 2 lines of Inc42-written text. Always. No exceptions.**  
- Max 1 source collapsed, 4 expanded.  
- **Never quote more than \~30 words** from a post (when quotes are enabled — §13).  
- Never article-length. It's a caption, not a second story.  
- Add a line only when removing it changes the meaning.

### 6.4 Link-out (rare)

For the occasional substantive post where summarising destroys the value, editorial can flag "Link out". Output stays one line:

> An investor broke down why this round is riskier than it looks. **Read the full post →**

**Manual only. The LLM never triggers this.**

---

## 7\. Cadence & placement (D9)

### Phase 1 — Pulse rides the morning Brief

No separate Pulse publish. The section's items appear as **2–3 cards inside the existing morning Brief**, after the editorial cards. Inherits an existing daily habit, competes for no new session, and needs no new push permission.

- **Cut-off \~20:00 the previous evening.** Editorial reviews after that and approves for the morning.  
- Share of items slipping to the *following* morning (\~35h late) by cut-off:

| Cut-off | 17:00 | 19:00 | 20:00 | 21:00 |
| :---- | :---- | :---- | :---- | :---- |
| Slips | 34.9% | 23.5% | **16.2%** | 11.1% |

- **Review shift 20:00–22:00 is confirmed workable** — editorial runs rosters with people on desk until 21:00–22:00, so this sits inside an existing shift.

### Phase 2 — dedicated evening edition

Once the cards earn it, Pulse gets its own edition — **in the evening, deliberately not the morning**, so it never competes with the Brief for the same attention slot.

**Send time is a reachability decision, not a freshness one.** Freshness rises monotonically with a later send, but 20:00 is past the window where this audience is reachable:

| Publish | 18:00 | 18:30 (start) | 19:00 | 20:00 |
| :---- | :---- | :---- | :---- | :---- |
| Same-day fresh | 70.7% | **\~74%** | 76.5% | 83.8% |
| Reachability | 🟢 | 🟢 | 🟡 | 🔴 too late |

Start at **\~18:30**. The working-day block (09:00–18:00 \= **58.9%** of items) is same-day fresh in *any* evening slot, so the \~10-point sacrifice falls only on late-afternoon content. A morning edition, by contrast, would carry **\~0% of that day's content** by definition.

⚠️ **18:30 is a hypothesis, not a finding, and cannot be settled from existing data** — Inc42's newsletters all send at a fixed hour (no absolute-time variation to mine) and the app is \~2 weeks old. **Test on ship**: three arms (17:30 / 18:30 / 19:30), metric \= push-open within 2h \+ edition completion, 3–4 weeks for weekday coverage, controlling for news volume.

Editorial review for Phase 2 lands \~17:30–18:15 — end of workday.

### Graduation and thin days

- **Phase 1 → Phase 2** requires: engagement rate ≥15% of Brief-opening sessions sustained 4 weeks **and** ≥5 approved items on ≥85% of days **and** no holdout regression (§14).  
- **The evening push is earned, not scheduled**: fire only on days clearing ≥5 approved items (\~90% of days qualify). *(Threshold anchored on BD — the thinnest persona — sitting at 4 raw items on a 1-in-10 bad day. Tunable after 30 days of real reject-rate data.)*  
- **Thin-day behaviour**: on sub-threshold days the surface shows the day's items as a section, labelled honestly (*"A quieter day — 3 things worth your time"*), and no push fires. **Never an empty screen, never padded with rejected material.**

Supporting data: 10–16 raw sector-matched items/day per persona; **zero empty days across 60**; 90–98% of days clear 5 items.

**In-article Pulse is live from Phase 1\.** It is conditional and continuous — it appears whenever a story has an approved Pulse, independent of the section's publish schedule. Only the *section* is phased.

⚠️ **Editorial review load under personalisation must be settled before build.** §15 budgets \~15 min/publish, which assumes one edition. With 8 sector editions that is only true if **review happens once at the item level and assembly into sector editions is automatic**. If instead each sector edition is reviewed separately, the load is \~8× and the cost line in §15 is wrong. **Decision: review the item pool once; assembly is deterministic and unreviewed.** State it explicitly so nobody builds the other model.

---

## 8\. Filtering and categorisation

### 8.1 What gets rejected

| \# | Filter | Reject when |
| :---- | :---- | :---- |
| 1 | Not relevant | Not about the Indian startup ecosystem |
| 2 | Already covered | We've published this take in the last 7 days |
| 3 | Unverified claim | Facts with no source, rumour, or contradicts our reporting |
| 4 | Low substance | Under 15 words, congratulations, emoji-only, plain repost |
| 5 | Promotional | Self-promo, product launches, hiring posts, ads, event plugs |
| 6 | Not credible | Poster is not on the allowlist |
| 7 | Toxic | Personal attacks, harassment, unproven allegations |
| 8 | Stale | Older than 72 hours, unless the story is still running |
| 9 | Negative or political | Negative assessment of a named company, or political/regulatory controversy — **flag for escalation, don't reject** (§9.4). BrandLabs overlap surfaces as context, not a separate filter |

### 8.2 LLM behaviour rules

- Every rejection returns a reason code. **No silent drops.**  
- **Reject when uncertain.** Precision matters more than volume.  
- Confidence below 0.7 on any call → flag for human decision.  
- **Never rewrite a post to make it pass.**  
- **Never invent a name, title, company or link.** Missing stays blank.  
- Plain English. No hype words. Neutral voice — report the view, never endorse it.  
- **Never state an opinion as fact. Always attribute the stance.**

### 8.3 Bucket assignment

Poster announcing their own news → **Announcement** · Post has data/pattern/analysis not already reported → **Insight** · Story has credible posts on both sides → **Debate** · Otherwise → **Reaction**. One bucket per post. Debate is decided at story level — a single post can never be a Debate. Below 0.7 confidence, default to Reaction and flag.

### 8.4 Matching keys (enrichment — D6)

Company name and handle · founder/investor names · event type \+ date window (funding, layoff, IPO, shutdown). We match on the company or event, **not** on mentions of Inc42 — leaders post about the company, they aren't replying to us. **No match is not a rejection.**

### 8.5 Media in posts — resolved from data

Measured across 1,409 quality-gated items:

| post\_type | Share | Median engagement |
| :---- | :---- | :---- |
| tweet | 84.8% | 113 |
| image (LinkedIn) | 9.4% | 652 |
| text (LinkedIn) | 3.3% | 543 |
| video (LinkedIn) | 1.6% | 997 |

⚠️ The headline gap is **confounded by platform** — LinkedIn and X sit on different engagement scales (p90: 660 vs 51). The valid *within-LinkedIn* comparison: image **\+20%** over text, video **\+84%**.

**Conclusions**: media lifts engagement modestly for images, strongly for video — but media-carrying posts are only **\~11.8% of supply**, so it's not a big v1 lever. **19.4% of media items carry under 25 words**, i.e. the attachment is the message for \~1 in 5\.

**v1 rules**: don't display media · flag media-carrying posts · a short post with media goes to **human review**, not auto-reject.

---

## 9\. Editorial review & governance

**Nothing publishes without human approval. No exceptions, no auto-publish.** This is a **compliance control**, not a quality filter — it is how we satisfy editorial-safety and conflict-of-interest obligations, so it runs on written rules, not judgement alone.

### 9.1 Actions

**⚠️ Simplify the tooling, never the controls (D13).** The list below is the full action set. **v1 ships the first four plus the kill switch**; the rest are convenience and can wait. What cannot be trimmed is *what the review guarantees* — 100% human approval, attribution, the verification standard, and the ability to pull something live. Those are compliance, not workflow.

| Action | Effect | v1 |
| :---- | :---- | :---- |
| Approve | Publishes at the next slot | ✅ |
| Edit & approve | Edit the text or sources, then publish | ✅ |
| Reject | Killed, with a reason | ✅ |
| Hold | Keep for the next slot | ✅ |
| **Kill switch** | Remove a live Pulse from the app immediately (per Pulse and per source) | ✅ **non-negotiable** |
| Swap source | Replace a selected source | later — achievable via Edit |
| Change bucket | Override the LLM's classification | later — achievable via Edit |
| Flag "Link out" | Convert to the 1-line \+ link format | later — achievable via Edit |

### 9.2 Rejection reasons (mandatory, one required)

1 Wrong match · 2 Misread stance · 3 Not newsworthy · 4 Weak source · 5 Duplicate · 6 Legal risk · 7 Commercial conflict · 8 Source concern · 9 Tone off · 10 Editorial call (free-text note required).

All logged. **This log is the training signal for eventual automation (D3) — without it, a later automation attempt starts from zero.** Weekly: review reasons by volume, tune prompts and allowlist. **Target: rejection rate under 20% within 8 weeks.**

### 9.3 Attribution grammar (binding copy rule)

- **Reported speech only.** "X said Y" / "X argued Y" — never the app asserting Y as fact.  
- Every claim traceable to a named speaker. **No orphan assertions.**  
- The product is explicitly **"what's being said," not "what's true."** That framing must survive into UI copy.

### 9.4 Verification standard & conflicts

- **Checkable, consequential claims** (funding amounts, acquisitions, headcount, regulatory outcomes) are verified against Datalabs/editorial before publication, or **cut**. Opinion passes through as attributed opinion — that is the product.  
- **Correction path**: an item later shown false is corrected in the next edition and struck in place, to the same standard as editorial.  
- **Escalation trigger is the CONTENT, not the relationship (D15).** The second check exists for items that are **negative in assessment or political** — *"this is a down-round in disguise"*, an accusation, a policy attack. Those are what actually create exposure. A neutral or positive comment from someone who happens to work at a client company is **not** a conflict and should not carry workflow overhead.  
  - **Escalate to editorial \+ commercial sign-off when**: the item makes a **negative assessment of a named company**, or touches **political or regulatory controversy**. Never auto-rejected, never fast-tracked.  
  - **Commercial relationship is context that escalates, not the trigger.** Measured: **17 companies are both a BrandLabs client and a voice-DB employer — 56 voices, 2.0% of the DB**. Surface that as a **visible column** (near-zero cost — it's a lookup, not a workflow) so a reviewer seeing a negative item can tell instantly whether a commercial relationship is also in play. Negative \+ commercial relationship \= highest priority.  
  - Client-company voices are **never boosted** by ranking.  
  - *Already handled upstream*: `political-celebrity` is hard-dropped by the quality gate and `regional-political` voices are flagged in the voice DB, so most political content never reaches review. This escalation covers what gets through.

### 9.5 Ownership

Named owner **and named backup**, with a documented "nobody approved by cut-off" rule. A daily dependency with no alarm is how our topic classifier died silently for 12 days.

---

## 10\. Attribution

**Every third-party opinion must be attributed. No orphan quotes.** Inc42 writes the summary (byline). The opinion belongs to the person who said it (attribution). **Both appear.**

**Why it's non-negotiable**

- **Legal.** *"This is a down-round in disguise"* unattributed \= Inc42 said it, about a real company. Attributed \= we're reporting. Same sentence, completely different liability. ⚠️ Attribution solves **defamation**. It does **not** solve **copyright** — see §13.  
- **The name is the value.** "Someone thinks the burn is unsustainable" is noise. "A Series B investor thinks so" is signal.  
- **Platform terms** require credit and a link.  
- **Distribution.** Tagged people reshare — our cheapest install channel.

**Required on every source**: name · handle/profile · title and company (where known) · link to the original post · platform.

---

## 11\. Personalisation & allowlist (D7)

**Allowlist \~200 voices, personalised at sector level.**

Supply by pool size, measured over 60 days:

| Pool | Items/day (median) | Bad day (p10) | Empty days | % of supply |
| :---- | :---- | :---- | :---- | :---- |
| top 25 | 11 | 5 | 0 | 48.5% |
| top 50 | 14 | 8 | 0 | 66.1% |
| top 100 | 19 | 10 | 0 | 83.6% |
| **top 200** | **23** | **12** | **0** | **96.6%** |

Curation is clearly right — **only 248 of our 2,846 voices (8.7%) produced a single quality-gated item in 60 days.** But allowlist size and personalisation must be decided *together*: 50 voices across 8 verticals is \~6 per sector, too thin to personalise. 200 supports 8 sector editions.

**Sector, not company watchlist** — items/day per persona:

| Persona | Sector-matched | Company-watchlist |
| :---- | :---- | :---- |
| Founder | 9.47 | 1.53 |
| Operator | 11.83 | 1.32 |
| Investor | 9.47 | **0.25** |
| BD | 8.30 | **0.17** |

At sector level all four personas get ≥1 relevant item on **98.3% of days**. At company level Investors and BD see something once every 4–6 days — a per-company social feed would look broken for most users.

**No person-follow primitive.** Sectors are already collected in onboarding, so Pulse has what it needs on day 1\. A user with no sectors gets the unpersonalised national edition.

---

## 12\. Review tooling

**v1 is a sheet, not an app (D13).** A custom admin tool is the single largest new build in this PRD, and building it before the feature is validated is the wrong order. The repo already runs several sheet-driven editorial workflows (application screener, D2C L1 review, MOP) — the pattern works and editorial already knows it.

### 12.1 v1 — sheet-backed queue

| Need | v1 implementation |
| :---- | :---- |
| Review queue | Candidates written to a Google Sheet, one row per item: text, bucket, confidence, sources \+ URLs, **`is_negative_or_political` escalation flag** \+ a **`commercial_relationship` context column** (§9.4) |
| Actions | A `decision` column (approve / edit / reject / hold) \+ an `edited_text` column \+ a **mandatory `reject_reason` dropdown** carrying all 10 codes (§9.2) |
| Publish | A job reads approved rows at the cut-off and publishes. Unapproved rows simply don't ship — **fail-closed by default** |
| Kill switch | Flip a row's status \+ cache bust. Crude but immediate |
| Quote flag | A config value, not UI (§13) |
| Allowlist | The existing `voices-master.yaml`, edited in the repo |

**Cost**: a writer job \+ a reader job. Days, not weeks. **No preview** — editorial reviews text, and the render is deterministic from a fixed template.

### 12.2 What earns a real tool

Build the custom UI when one of these is true, not before:

- Daily review consistently exceeds \~30 min (the sheet is the bottleneck)  
- Reject rate is stable enough that automation is in reach and the decision log needs proper structure (§9.2)  
- Phase 2 ships and the scheduler needs to be operable by non-engineers

Then add: in-app preview (collapsed \+ expanded) · one-click actions · allowlist management UI · publish scheduler · per-source kill switch.

---

## 13\. Legal & compliance

Full analysis: `research/social-intelligence-feed-legal-review.md` (a scoping doc for counsel, **not legal advice**). **Gate 1 is open** — questions scoped, unanswered.

| Area | Position |
| :---- | :---- |
| **Platform terms** 🔴 | **LinkedIn's User Agreement prohibits scraping *and* the use of scraped data**; LinkedIn won a permanent injunction against hiQ on **breach of contract** (not CFAA). We ingest via Apify (LinkedIn) and twitterapi.io (unofficial) — **no licence, no safe harbour.** Hardest gate |
| **Copyright** 🟠 | **India's §52 fair dealing is a closed, exhaustive list** — no US-style open factor test. "Reporting current events" is enumerated and courts favour transformative use, so synthesis sits far stronger than reproduction |
| **Defamation** | All opinions attributed to a named person; Inc42 never asserts the claim (§9.3, §10) |
| **DPDP** | §3(c)(ii) excludes self-published public data. Contested by MeitY (Aug 2024\) — don't rely on it alone. Extend the existing **"Listed Individuals" notice-and-opt-out** precedent. No new personal data collected from our users |
| **Store labels** | No new data categories → Apple/Play labels unchanged. Confirm with Animesh |
| **Takedown** | Remove within 48 hrs on request; add to blocklist. **Product spec required**: suppress-vs-purge, SLA, owner |

### The format ladder — where counsel lands decides the product

| Rung | Outcome | Product |
| :---- | :---- | :---- |
| 1 | Verbatim OK | Native cards |
| 2 | Short excerpt \+ attribution | **Where the quote design sits today** |
| **3** | No verbatim — synthesis only | Strongest on all three surfaces |
| 4 | Per-voice consent | Small opt-in programme |

### D8 — the quote component is switchable

Quotes make a Pulse land, and **at our volumes with 100% editorial review, quoting inside an edited piece is ordinary journalistic practice** — publishers do it daily, and that is a materially stronger position than bulk automated reproduction. It may well clear.

But it is unresolved. So: **build synthesis-first with quotes behind a flag.** If counsel clears them, turn it on. If not, the product ships unchanged. The flag costs almost nothing now; retrofitting would be expensive.

**⚠️ Rung-4 contingency**: if counsel requires per-voice consent, this PRD does not survive contact. A consent programme across 200+ voices isn't a product, it's a partnerships operation. Explicit descope: 20–40 consenting voices as an editorial franchise. **Do not attempt §4–§7 under rung 4\.**

### Launch-blocking legal items

1. Counsel sign-off on ingestion/retention (we hold **311K+ posts with full text** — exposure independent of display, and it exists today for the internal digests).  
2. Voice opt-out mechanism — product spec.  
3. **Publisher liability / defamation** — added as counsel question \#11; neither source PRD covered it.  
4. Fix the live privacy-policy citation error: **DPDP "Section 14" → §3(c)(ii)** (§14 is *"Right to nominate"*).

---

## 14\. Cannibalisation

Following the Brief's precedent (`brief-prd.md` §13): watch for **collapse, not movement**.

**The phased cadence (§7) reduces this structurally rather than only measuring it.** Phase 1 sits *inside* the Brief, so it competes for no separate session. Phase 2 publishes in the **evening** — a different attention slot entirely. That was the main argument for a holdout, so the argument is now weaker — **but not gone**, since Phase 1 still competes for attention *within* a Brief session.

**Ship behind a feature flag with a holdout for the first 4–6 weeks.** PostHog flags are already in use for Plus/Pro tier reservation, so the mechanism exists.

⚠️ **Size the holdout with a power calculation, not a guess.** At launch DAU a 10–20% holdout may be too small to detect a 10% effect in 2 weeks — in which case the test is *designed to return "no significant difference"* regardless of truth. Compute the minimum detectable effect at actual DAU first; if the app is too small to power it, say so and lengthen the window rather than pretending the result means something.

**Rollback trigger (pre-registered)**: exposed-cohort `brief_completed` **\>10% below holdout, sustained 2 weeks and statistically distinguishable at the sized power** → pull the cards and re-scope.

**Guardrail**: article completion rate must not drop. If Pulse pulls people out of articles, it's failing.

---

## 15\. Cost envelope

| Component | Cost | Scaling |
| :---- | :---- | :---- |
| Candidate classification (existing pipeline) | \~$0.0001/post | Flat in DAU |
| Daily synthesis — **summarize-once per sector** | \~$20–60/mo | **Flat in DAU** |
| Editorial review | \~15 min/publish | Flat |
| Review tooling (v1 sheet) | one-off, days of eng | — |
| Voice corpus (scrape \+ classify) | \~$20–35/mo | Already running |

**Per-user prose generation is explicitly out** — it scales with DAU for no product gain. Follows `brief-prd.md` §14: *"\~100–1000× cheaper than the per-user prose model the simulation accidentally implied — and auditable."*

---

## 16\. Success metrics & kill criteria

> **⚠️ The demand premise is `ASSUMPTION — UNVALIDATED`.** Three independent instruments raised doubt: VOC mining across 77K posts from these same voices found the "too much noise" pain articulated at **\~0.046%** (an upper bound); *urgency* scored weakest across all three framing variants tested; and founders don't volunteer information pain. **⚠️ Both instruments are weaker than they look — see §1.2**: public text cannot detect status anxiety (people conceal it), and all three framings tested led with *efficiency*, never status. Down-weight this evidence; do not treat 0.046% as strong disconfirmation. The job appears **real but latent** — and latent jobs fail on **adoption**, not on need. Metrics are therefore adoption-weighted, and `jtbd-phase1/PHASE2-RESEARCH-BRIEF.md` is a **gate**, not a formality.

**North star**: inherits the app's — **D30 retention of weekly active users ≥15% sustained at 90 days**. A feature that engages but doesn't move retention hasn't earned a standalone surface.

**⚠️ Denominator discipline.** Cards sit after the editorial cards, and in-article Pulse sits below the body — so "engagement among those who reached it" counts only the already-engaged and flatters the feature. Two separate metrics, both denominated on **all** sessions/readers:

| Metric | Denominator |
| :---- | :---- |
| **Reach rate** | all `brief_opened` sessions / all article readers |
| **Engagement rate** | all `brief_opened` sessions / all article readers |

**30-day gates (Phase 1\)**

- Engagement rate **≥12% of all Brief-opening sessions**  
- Reach rate reported alongside — low engagement *with low reach* is a **placement** problem, not a demand verdict, and triggers repositioning before any kill call  
- No `brief_completed` regression vs holdout (§14)  
- Editorial reject rate \<40% at 30 days, tracking to **\<20% by 8 weeks**

**30-day gates (in-article Pulse)** — a separate surface with a separate denominator, and the §16 Brief-based gates do not cover it:

- Expand rate **≥15% of article readers who saw a Pulse** (`pulse_expanded` / `pulse_viewed`, surface=article)  
- Article completion rate not below holdout (§14 guardrail)  
- Fire rate reported — what share of articles carry a Pulse at all. Expected to be low by design (§6.2); **a low fire rate is not failure, a low expand rate is**

**Share rate is a primary metric, not vanity (§1.1).** If status is the driver, forwarding *is* the behaviour — people share to display knowledge. Track `pulse_shared` per surface from day one and read it as a leading indicator of product-market fit, ahead of expand rate.

**Phase 2 metrics**: Pulse expand rate · section DAU and completion · outbound taps to original posts · **share rate** · D7/D30 retention, Pulse users vs others.

**Kill**: engagement rate **\<5% of all Brief-opening sessions sustained 4 weeks with reach ≥50%** (i.e. people saw it and didn't want it) → the latent-demand hypothesis is disconfirmed. Fold the supply back into editorial; do not build Phase 2\.

---

## 17\. Instrumentation

**None of §16's metrics are measurable today** — the app's event dictionary (`event-tracking-plan.md`, 47 events) contains nothing for Pulse. These events must land in that dictionary before build; it is the single source of truth and anything not in it doesn't get instrumented.

Conventions inherited: `object_action`, past tense, snake\_case, **no dynamic event names** (variance lives in properties), explicit instrumentation only.

| Event | Fires when | Properties | Dest |
| :---- | :---- | :---- | :---- |
| `pulse_viewed` | A Pulse block enters the viewport | `surface` (article/brief\_card/section), `bucket` (reaction/insight/announcement/debate), `story_id` (null when orphan), `position`, `is_personalised` | P |
| `pulse_expanded` | "View more" tapped | `surface`, `bucket`, `story_id` | P |
| `pulse_source_tapped` | Outbound tap to an original post | `platform` (linkedin/twitter), `voice_slug`, `bucket`, `surface` | P |
| `pulse_section_opened` | Section opened | `source` (brief\_card/nav/push/deeplink), `item_count`, `is_thin_day` (bool) | P |
| `pulse_section_completed` | End state reached | `items_viewed`, `duration_sec` | P |
| `pulse_shared` | Share sheet completed | `surface`, `bucket`, `channel` | P |

**Super properties** (§5 of the tracking plan) attach automatically — no Pulse-specific additions needed.

**Push**: Phase 2's evening edition needs a **new `push_type` value — `pulse_evening`** — added to the existing enum (`morning_brief`/`nudge`/`breaking`/`watchlist_digest`/`winback`) on `push_opened`, `push_delivered` and `app_opened.push_type`. This also makes the send-time test (§7) measurable, since the three arms differ only by `variant`, which `push_opened` already carries.

**Metric → event mapping** (closing the §16 loop):

| Metric | Computed from |
| :---- | :---- |
| Reach rate | `pulse_viewed` / `brief_opened` (Phase 1\) · / article readers (in-article) |
| Engagement rate | distinct users with `pulse_expanded` or `pulse_source_tapped` / same denominator |
| Expand rate | `pulse_expanded` / `pulse_viewed` |
| Outbound taps | `pulse_source_tapped` |
| Section DAU / completion | `pulse_section_opened` · `pulse_section_completed` / `pulse_section_opened` |
| Cannibalisation (§14) | `brief_completed` split by holdout flag |
| Send-time test (§7) | `push_opened(pulse_evening)` by `variant`, within 2h |

**Editorial-side logging is separate and equally required** (§9.2): every approve / edit / reject with reason code. That's the automation training set and it lives in the admin tool, not PostHog.

---

## 18\. Tier boundaries (D2)

D2 locked **Free teaser \+ Plus/Pro depth**, but the boundary was never specified. Following `premium-boundaries.md`, whose organising principle is **who controls the trigger** — Free \= editorial-curated, Plus \= user-defined, Pro \= Datalabs-grade:

| Tier | Pulse |
| :---- | :---- |
| **Free** | Today's edition in full (all blocks, \~11–13 items) · in-article Pulse on every story that has one · sector personalisation from onboarding · outbound links to originals |
| **Plus** | **Archive** (past editions; Free is today-only) · **all sectors**, not just the user's · early access to the evening edition |
| **Pro** | **Source-level depth** — every contributing post behind an item, not just the top 4 · **voice-level tracking** ("alert me when \[voice\] weighs in on \[sector\]") · export |

Consistent with the Brief's stance that **the daily read is deliberately free** — gating today's Pulse would kill the habit this feature exists to build. Depth, history and breadth are what's paid.

**v1.1 activation**: architecture and flags only, **no paywall, no upgrade prompts, no "Pro/Plus/Subscribe/₹" wording** — matching `v1-prd.md` §473. Interest capture only ("coming soon / notify me"), which also feeds the monetisation dataset via the existing `interest_captured` event.

---

## 19\. Risks

| Risk | Mitigation |
| :---- | :---- |
| Automated collection breaches platform terms | Legal review before build (§13). May force manual or vendor-based collection |
| Review load too heavy for editorial | Filters must cut hard. Watch daily review time in week 1 |
| Most stories yield nothing | **Expected.** Only big stories clear 3 credible posts. Pulse stays rare and therefore meaningful — and the section is fed by the orphan pool (§4), not by matched stories |
| Section runs dry | Section exempt from the 3-post rule; 200-voice pool; thin-day copy defined (§7) |
| A bad quote damages credibility | Allowlist gate, 100% review, kill switch |
| Pulse section turns into a scroll | Capped blocks, explicit end state, no pagination |
| Reads like Inc42's own opinion | Attribution rules (§10), neutral-voice rules (§8.2) |
| LLM invents a quote or source | **Every source must resolve to a stored post with a working URL. No URL → cannot publish** |
| Demand is latent, adoption fails | Phase-2 research gate; ship inside the Brief first; kill criteria pre-registered (§16) |
| **Signal Engine switchover lands mid-build** (D10) | We run the voice DB until cutover. The \~1,700 edits we've made (re-tag, dedupe, NER, classifier) are the handover brief. **Risk: if cutover happens during build, the source pipeline changes underneath us** — agree a freeze window with the data team before build starts |
| Section personalisation multiplies review load | Review once at item level, assembly automatic (§7). If that model breaks, the feature is not staffable |

---

## 20\. Open items

| \# | Item | Owner |
| :---- | :---- | :---- |
| 1 | Counsel: the 10 Gate-1 questions \+ \#11 publisher liability | Utkarsh / external |
| 2 | Phase-2 user interviews — the demand gate | product/marketing |
| 3 | Voice opt-out / takedown product spec | product \+ legal |
| 4 | Negative/political escalation flag \+ commercial-relationship lookup column in the queue | eng |
| 5 | Editorial checklist (§9.3–9.4) written and signed off | editorial |
| 6 | Evening send-time test (3 arms) | product, on Phase 2 |
| 7 | Holdout power calculation at actual DAU | data |
| 8 | Confirm no clash: `concept-note.md` retained *"Inc42 Pulse"* as a v1.1 alternate **app** name | marketing |
| 9 | Signal Engine handover brief at switchover (D10) | Utkarsh / data team |
| 10 | Privacy-policy citation fix (DPDP §14 → §3(c)(ii)) | policy owner |

## 21\. Build dependencies

- Voice corpus \+ outlier detection — **exists** (`voice-monitor/`), ours until switchover (D10)  
- Editorial corpus for story-matching — **exists** (`shared/tools/editorial-corpus/`)  
- PostHog feature flags — **exists**, already used for tier reservation  
- Review tooling — **v1 \= sheet-backed queue** (writer job \+ reader job, days). Custom admin UI deferred until it earns itself (§12.2)  
- Discourse-convergence clustering — **not built**, v1.1 upgrade (§6.2)

# App V2

**Inc42 App \- v2 Scope**

**Date**: 2026-08-19 · **Owner**: Ranjith · **Status**: Draft for team alignment **Source inputs**: PostHog first-week review (2026-08-17), Aug-18 deep-linking Slack thread, event dictionary v1.4

11 workstreams. Priorities are proposed defaults. ⚠️ \= needs input before it can be scoped. Effort \= rough T-shirt (S \<2d · M 2–5d · L \>1wk).

**Su mmary table**

| Item | Type | Owner | Priority |
| :---- | :---- | :---- | :---- |
| Updated events | Instrumentation | Ranjith \+ Eng | **P0** |
| Datalabs filters | Bug/backend | ⚠️ | ⚠️ |
| AskInc42 | Feature | Ritvik | P1 |
| Dummy screen before 7am | UX | Design \+ Eng | P2 |
| Tap-again-to-exit | UX | Eng | P3 |
| Deep linking | Bug | Nityam \+ Eng | **P0** |
| Singular setup revision | Attribution | Eng \+ Marketing | **P0** |
| Brief page \- design revisit | UX/CRO | Design | P1 |
| Separating Datalabs | Architecture | ⚠️ | ⚠️ |
| Redesign Datalabs \+ article section | Design | Design | P2 |
| Sector images \+ Dark mode (Optional) | UX | Design \+ Eng | P2 |

**1\. Updated events — P0**

**Problem**: Event dictionary v1.4 has drifted from the shipped app in both directions — specced events that never fire, and live events not in the dictionary. Half the v1 metrics can't be trusted.

**Scope**

* **Fire the dark events** (in dictionary, 0 fires all-time):  
  * push\_delivered — retention/OEM-delivery trip-wire; blocks the entire CRM layer readout  
  * decode — the AI explainer; the whole "AI that explains it for you" positioning has zero telemetry  
  * interest\_captured, locked\_feature\_tapped, watchlist\_limit\_hit — v1 monetization dataset (specced "clean day 1", currently empty)  
* **Reconcile off-spec events** (firing, not in dictionary): walkthrough (104 users), brief\_story\_rated, sign\_in\_prompt\_shown, share\_initiated; dedupe the 3 untrack events (story\_unsaved \+ company\_untracked \+ industry\_untracked) into one; remove dead brief\_open\_today  
* **Property gaps**: add missing onboarding.step\_name values (watchlist / push\_prompt / signin\_prompt); implement is\_edition\_switch; exclude auth\_callback redirects from deep\_link\_opened  
* **Internal-user tagging**: is\_internal person property (@inc42.com \+ pre-Aug-12 cohort) \+ a "Internal & beta" cohort as default dashboard filter  
* **North-star fix**: adopt completed\_engaged \= brief\_completed where duration\_sec ≥ 60

**Acceptance**: dictionary v1.5 published \+ signed off by eng; every event in v1.5 either fires in prod or is explicitly deprecated; internal traffic excludable from all dashboards.

**2\. Datalabs fixes —** ⚠️ **needs input**

**Problem**: ⚠️ Not yet specified. **Need from you**: which surface, what's broken, expected vs actual behaviour, affected build/platform. **Structure once known**: bug list → root cause per bug → owner → acceptance. Placeholder until detailed.

**3\. AskInc42 — P1**

**Context**: v1 (brief-end swap \+ Watchlist/company page) shipped. Ships **before** Pulse. Owner: Ritvik Sethi.

**Scope (v2)**

* **3 stored onboarding questions** — captured at onboarding, persisted to personalize AskInc42 answers  
* Web search stays ON (Perplexity)

**Dependencies / blockers**

* Needs an **API from Anmol** — **not yet raised with him** (raise first)  
* Feature flags currently **HALTED** — unblock or route around

**Acceptance**: 3 onboarding Qs captured \+ stored; AskInc42 answers reflect stored context; API contract with Anmol agreed.

**4\. Dummy screen before 7am — P2**

**Problem**: The brief publishes 7am IST. Users opening before drop hit an empty/undefined state.

**Scope** — pick one behaviour:

* (a) Placeholder: "Today's brief drops at 7am" \+ live countdown, or  
* (b) Show yesterday's brief with a "New brief at 7am" banner

**Approach**: gate on server publish-time, not device clock (timezone safety). Handle the 6:59→7:00 transition without a manual refresh.

**Acceptance**: opening pre-7am shows the chosen state; auto-updates to today's brief at drop without app restart. ⚠️ **Decide**: (a) countdown vs (b) show-previous.

**5\. Tap-again-to-exit — P3**

**Problem**: On Android, a single back-press from the home tab exits the app — accidental exits. **Scope**: standard "Tap again to exit" toast — first back shows toast, second within \~2s exits. **Acceptance**: single back on root tab shows toast \+ stays; double-back exits; only on root (not nested screens). Low effort.

**6\. Deep linking — P0**

**Problem**: Newsletter links open in Safari instead of the app — iOS (Safari \+ in-app webviews) and some Android. Direct browser taps of inc42.com/... work; newsletter-wrapped links don't.

**Root cause**: The Customer.io click-tracker redirect breaks Universal Links / App Links — iOS checks the app association against the *first tapped domain* (the tracker), not the final URL; the tracker isn't in AASA. Android App Links need assetlinks.json \+ domain verification on the tapped domain (fails the same way).

**Scope / fix**

* Route newsletter article links through **Singular smart links** (see \#7) — carries the app-link association \+ attribution  
* Verify AASA at https://inc42.com/.well-known/apple-app-site-association — Content-Type: application/json, **no redirect**  
* Verify Android assetlinks.json at /.well-known/, autoVerify=true, domain verified  
* Server-side 301/302 only — no JS/interstitial hop  
* Don't wrap app-destined links in the CIO tracker (or register the tracker domain in AASA/assetlinks)

**Acceptance**: tap from Gmail \+ Apple Mail on iOS and Android opens the in-app article; verified on Safari and in-app webviews. Repro link: inc42.com/buzz/razorpay-launches-ai-foundation-model-vulcan… **Note**: Nityam has additional pointers — fold in.

**7\. Singular setup revision — P0**

**Problem**: Deep links arrive with campaign \= None → Summit (QR tent-card) and any campaign installs are unattributable.

**Root cause**: same as \#6 — links not routed through properly configured Singular smart links.

**Scope**

* Rebuild Singular smart-link config so campaign / source / medium populate on click  
* Wire brief\_opened.source to read the deeplink attribution (currently only ever "organic")  
* Validate the QR → preloaded-onboarding path end-to-end

**Acceptance**: a campaign smart link produces a non-null campaign in PostHog \+ Singular; Summit QR installs attributable. **Time-critical** for campaign attribution.

**8\. Brief page — design revisit — P1**

**Problem (data-backed)**:

* **Cover→brief cliff**: 99 users saw the cover, 41 tapped in (**41%** — the biggest funnel drop)  
* **Completion quality**: median completion 7s; half of "completions" \<10s — the brief is flicked, not read

**Scope**

* Treat the brief cover as a **conversion surface** — stronger/clearer CTA, or auto-advance into card 1 (kill the dead-end cover)  
* Redesign the card flow so a genuine read is the default path (pacing, dwell nudges)  
* Instrument against completed\_engaged (\#1) so we can measure the fix

**Watch-item**: Explore beats Brief today (69% vs 31%). Re-read after the cliff is fixed — if Explore still wins with a working brief entry, that's a v1.1 strategy signal, not a bug.

**Acceptance**: cover→brief conversion up from 41%; engaged-completion (≥60s) share rises; no regression in card drop-off curve.

**9\. Separating Datalabs —** ⚠️ **needs input**

**Problem / intent**: ⚠️ Split DataLabs into its own surface/section — scope undefined. **Need from you**: is this a nav split, a separate section, or a separate app? Relation to the One-Inc42 / unification direction? This gates \#10. **Structure once known**: IA change → nav model → migration of existing Datalabs content → acceptance.

**10\. Redesign Datalabs \+ article section — P2**

**Context**: Pairs with \#9 — scope depends on that decision. **Scope (provisional)**: redesign the Datalabs surface \+ the article-reading section (typography, layout, in-article actions). **Dependency**: blocked on \#9's IA decision. Design owner TBD (Satya?). **Acceptance**: TBD once \#9 is defined.

**11\. Sector images in brief card \+ Dark mode — P2**

**Scope**

* **Dark mode**: full theming pass across app surfaces  
* **Sector-based images**: brief cards show imagery keyed to the story's sector

⚠️ **Data caveat (important)**: **86% of articles currently have no sector tag** — the same gap that shelved sector personalization. Sector-based imagery will only cover \~14% of cards unless sector-tagging is fixed first.

* **Decision needed**: (a) fix sector tagging first, (b) ship with a generic fallback image for untagged cards, or (c) defer sector images and ship dark mode alone.

**Acceptance**: dark mode toggles cleanly across all screens; sector images render per the chosen fallback strategy without blank cards.

| Section | Problem Statement | Feature / Improvement | Current → Expected Impact | Additional Comment |
| ----- | ----- | ----- | ----- | ----- |
| Brief — Entry | Drop between seeing the cover and opening the brief | Cover screen clarity / entry-flow fix | 65% → 80% target | Improving trend already (42% → 75% over last 2 weeks); track weekly, not a fixed baseline |
| Brief — Card 1→2 | Unclear if Card 1 is a real cliff | Progress indicator \+ return-path fix (pending) | TBD — 45% vs 80%, conflicting reads | Reconcile before target-setting |
| Brief — Cards 2–8 | Reference only; no problem | No fix needed | 90–97% each step | No fatigue curve; confirmed twice — don't shorten the brief |
| Brief — Full article exit | Unclear if reading the full article kills the session | Return-path CTA (pending) | TBD — 6% vs 48%, conflicting reads | Reconcile; session-scoping differs between pulls |
| Brief — Repeat open | Unclear if a 2nd open helps or hurts completion | Push nudge to re-open (pending) | TBD — direction reversed (26%→50% vs 35%→27%) | Reconcile; new pull lumps all repeat opens together |
| Brief — Retention/Push | Retention collapses D1→D3; push never delivered | Fix push delivery (iOS root cause known) | D1 35% / D3 18% → push should actually fire | Confirmed twice; P0 engineering bug |
| Brief — Rate control | “Feedback \+ rating” scope may build on a dead control | Verify Rate fires before promoting/relocating | 1 user, 1 event → confirm working first | 18-user figure is July test-account noise; don't cite |
| Brief — Loader screen | Users see loader between 12 AM–6 AM before day's brief drops | Decide: countdown placeholder vs yesterday's brief \+ banner | Not yet measured | Already flagged in 19 Aug v2 scope doc; no owner/decision yet |
| Explore — Article | Half of Explore visits produce no tap | Add feed-impression instrumentation before redesigning | 50% zero-touch → not quantifiable yet | Confirmed as fast scans, not stuck users; 81s median, near-normal return |
| Explore — Article return | Reference only; no problem | No fix needed | 73% loop back to Explore | Healthy as-is |
| Explore — Company (funding→financials) | Biggest single drop in company research funnel | Company-page redesign targeting UI between sections | 70% → 85–90% target | Already scoped into redesign |
| Explore — Company (financials→people) | Secondary drop, compounds with above | Surface key\_people alongside financial data | 46% → 55–60% target | — |
| Explore — Search (zero-result) | \~1 in 3 searches return nothing | Elasticsearch/filter reliability fix | 32–33% → \<15% target | Feeds directly into company-open funnel |
| Explore — Search (rage-search) | Some users hit repeated total search failure | Same fix \+ fallback suggestions on zero-result | 16% hit 3+ zero-results → \<5% target | 86% retry rather than abandon; real intent wasted; P0 |
| Onboarding — Walkthrough | Drop concentrates at Step 1; finishing still doesn't explain Brief | Redesign Step-1 messaging for personalization/value | 81% finish; 16/27 bail at Step 1 → 90%+ target | Also improves trust in future Explore-vs-Brief comparisons |
| Errors — Explore load\_failed | Load errors on most-used surface | Root-cause investigation | 6.8% → \<2% target | Flat for 3 weeks; neither worsening nor improving |
| Errors — company\_profile/not\_found | Dead/stale company links from Explore cards | Data-integrity audit of company\_id references | 2.0% → \<0.5% target | Newly isolated; distinct from load\_failed |
| Errors — Brief load\_failed | Load errors on Brief's entry point | Check if same root cause as Explore load\_failed | 7.4% → \<2% target | Could compound the entry drop |
| Scope — Homepage banner | Use case undefined, not shipped | Defer to next phase | 0 events → N/A this cycle | Avoids mid-freeze scope creep; no data risk from deferring |

# User Interview \- Survey Questions

# **Inc42 App User Feedback Survey**

### **1\. How often do you currently open the Inc42 App?**

* Daily  
* A few times a week  
* Rarely  
* Not anymore

### **2\. How long have you been using the Inc42 App?**

* Since launch  
* Yet to use  
* Just started

### **3\. Besides the app, do you use any other Inc42 products?**

* Website / Newsletter  
* DataLabs  
* Inc42 Plus/Pro  
* Just the app

### **4\. What’s the main thing you do when you open the app?**

**Response:** Open text

### **5\. What best describes your experience with today’s Brief?**

* Opened it and read through some stories  
* Opened it but didn’t read much  
* Haven’t opened it today  
* I don’t know what this refers to

### **6\. How relevant and useful do you find the Daily Brief?**

*Show only if the user has not selected “I don’t know what this refers to” above.*

* Very useful  
* Somewhat useful  
* Not useful

### **7\. What’s your current streak?**

* Enter a number  
* 0  
* I don’t know what a streak is

### **8\. What’s the last thing you looked at on the Explore page?**

* A company profile  
* An article  
* Something else  
* Haven’t opened Explore  
* I don’t know what Explore is

### **9\. Does Explore usually show you things you’re interested in?**

*Show only if the user has not selected “Haven’t opened Explore” or “I don’t know what Explore is”.*

* Yes, often  
* Sometimes  
* Rarely  
* No, it feels repetitive

### **10\. What’s one thing about the app that has stuck with you \- good or bad?**

**Response:** Open text

### **11\. Which of the following best describes you?**

* Founder  
* Investor  
* Operator  
* BD & Partnerships  
* Other

### **12\. Would you be open to a 30–45 minute conversation about your experience with the Inc42 App?**

*As a thank-you, we’ll offer you 1 month of free DataLabs Pro.*

* Yes  
* No

### **13\. Your Name**

**Response:** Text

### **14\. WhatsApp Number**

**Response:** Phone number

# Singular Link \-Nomenclature

# **Singular Deep-Link Configuration — Inc42 Brief**

## **Overview**

This document defines the deep-link URLs to be configured in **Singular Links** for the Inc42 Brief app.

The app uses the custom URL scheme:

inc42brief://

The corresponding inbound-link mapping is handled in:

src/core/linking/mapInboundUrl.ts

These deep links can be used for:

* Navigating users who already have the app installed  
* Deferred deep linking after installation  
* Routing users to a specific Brief, article, company, Explore tab, or Watchlist

---

# **1\. Singular Link Configuration**

When creating or editing a **Singular Link**, go to:

**Link Settings → Redirects**

Under:

> **If the app is already installed, go to:**

paste the appropriate deep-link value from this document.

### **Deferred Deep Link**

If the same destination should open immediately after a user installs the app, use the **same deep-link value** in the deferred deep-link configuration.

### **Important**

The deep-link value should be pasted into the Singular dashboard **without additional encoding**.

For example:

inc42brief://article/meesho-raises-funding

Do **not** manually encode it when entering it directly into the Singular deep-link field.

URL encoding is only required when manually constructing a Singular URL using the `_dl` parameter.

---

# **2\. Deep-Link Destinations**

## **2.1 Brief — Home**

Opens the main Brief tab.

### **Deep Link**

inc42brief://brief

### **Singular `_dl` form**

YOUR-BASE?\_dl=inc42brief%3A%2F%2Fbrief

`YOUR-BASE` should be replaced with the Singular Link generated in the Singular dashboard.

Example:

https://inc42.sng.link/Axxxx/yyyy?\_dl=inc42brief%3A%2F%2Fbrief

If no `_dl` parameter is provided, the app can also open the Brief home destination according to the inbound-link handling logic.

---

# **3\. Brief Reader**

## **3.1 Open Today's Brief**

inc42brief://brief/read

This should open the Brief reader and load the appropriate/current edition.

### **Singular `_dl` form**

YOUR-BASE?\_dl=inc42brief%3A%2F%2Fbrief%2Fread

---

## **3.2 Open a Specific Brief by ID**

inc42brief://brief/read?briefId=REPLACE\_BRIEF\_ID

### **Example**

inc42brief://brief/read?briefId=12

### **Singular `_dl` form**

YOUR-BASE?\_dl=inc42brief%3A%2F%2Fbrief%2Fread%3FbriefId%3D12

Replace `12` with the actual Brief ID.

---

## **3.3 Open a Specific Brief by Date**

inc42brief://brief/read?briefDate=REPLACE\_YYYY-MM-DD

### **Example**

inc42brief://brief/read?briefDate=2026-08-25

### **Singular `_dl` form**

YOUR-BASE?\_dl=inc42brief%3A%2F%2Fbrief%2Fread%3FbriefDate%3D2026-08-25

The date must use:

YYYY-MM-DD

format.

---

# **4\. Explore — Articles**

Opens the Explore section with the **Articles** mode selected.

### **Deep Link**

inc42brief://explore?mode=articles

### **Singular `_dl` form**

YOUR-BASE?\_dl=inc42brief%3A%2F%2Fexplore%3Fmode%3Darticles

The following can also be used:

inc42brief://explore

When no mode is specified, Explore defaults to the Articles mode.

---

# **5\. Explore — Companies**

Opens the Explore section with the **Companies** mode selected.

### **Deep Link**

inc42brief://explore?mode=companies

### **Singular `_dl` form**

YOUR-BASE?\_dl=inc42brief%3A%2F%2Fexplore%3Fmode%3Dcompanies

---

# **6\. Article Detail**

Opens a specific article.

### **Deep Link**

inc42brief://article/REPLACE-ARTICLE-SLUG

Replace `REPLACE-ARTICLE-SLUG` with the article's actual slug.

### **Example**

inc42brief://article/udaan-lines-up-160-mn-financing-round-to-strengthen-balance-sheet

### **Singular `_dl` form**

YOUR-BASE?\_dl=inc42brief%3A%2F%2Farticle%2FREPLACE-ARTICLE-SLUG

### **Web URL Support**

Canonical Inc42 web article URLs can also open the corresponding article when App Links are correctly verified.

For example:

https://inc42.com/{category}/{slug}/

For Singular's custom deep-link configuration, use the `inc42brief://` scheme described above.

---

# **7\. Company Detail**

Opens a specific company profile.

### **Deep Link**

inc42brief://company/REPLACE-COMPANY-SLUG

### **Example**

inc42brief://company/meesho

### **Singular `_dl` form**

YOUR-BASE?\_dl=inc42brief%3A%2F%2Fcompany%2FREPLACE-COMPANY-SLUG

---

# **8\. Watchlist**

Opens the user's Watchlist.

### **Deep Link**

inc42brief://watchlist

### **Singular `_dl` form**

YOUR-BASE?\_dl=inc42brief%3A%2F%2Fwatchlist

---

# **9\. Quick Reference**

| Destination | Deep Link |
| ----- | ----- |
| Brief | `inc42brief://brief` |
| Brief Reader | `inc42brief://brief/read` |
| Specific Brief | `inc42brief://brief/read?briefId={id}` |
| Brief by Date | `inc42brief://brief/read?briefDate={YYYY-MM-DD}` |
| Article Explore | `inc42brief://explore?mode=articles` |
| Company Explore | `inc42brief://explore?mode=companies` |
| Article Detail | `inc42brief://article/{slug}` |
| Company Detail | `inc42brief://company/{slug}` |
| Watchlist | `inc42brief://watchlist` |

---

# **10\. Singular Configuration Checklist**

For every Singular Link:

* Create or edit the Singular Link.  
* Ensure **Deep Linking** is enabled for the link.  
* Open **Link Settings → Redirects**.  
* Configure the destination under **If the app is already installed, go to:**.  
* Paste the plain `inc42brief://...` deep link.  
* Configure the same value as the deferred deep link if post-install routing is required.  
* Do not manually URL-encode the value when entering it directly into the Singular dashboard.  
* Only URL-encode the destination when manually constructing the `_dl` query parameter.  
* Test the Singular Link with the app installed.  
* Test the same link with the app not installed to verify deferred deep linking.  
* Verify that the final destination matches the expected screen.

---

# **11\. `_dl` Encoding Reference**

When a deep link is manually appended to a Singular Link using `_dl`, the custom scheme needs to be URL-encoded.

### **Original**

inc42brief://article/meesho

### **Encoded**

inc42brief%3A%2F%2Farticle%2Fmeesho

### **Final Singular URL**

YOUR-BASE?\_dl=inc42brief%3A%2F%2Farticle%2Fmeesho

Do not apply this encoding when pasting the deep link directly into Singular's deep-link destination field.

---

# **12\. App-Side Mapping**

All inbound deep-link routes should be handled by:

src/core/linking/mapInboundUrl.ts

The mapping should recognize the following route patterns:

inc42brief://brief  
inc42brief://brief/read  
inc42brief://brief/read?briefId={id}  
inc42brief://brief/read?briefDate={date}  
inc42brief://explore?mode=articles  
inc42brief://explore?mode=companies  
inc42brief://article/{slug}  
inc42brief://company/{slug}  
inc42brief://watchlist

The app-side mapping is responsible for translating these inbound URLs into the corresponding application destinations.

---

# **13\. Recommended Testing Matrix**

Before using a Singular Link in production, test each destination in both app states.

| Destination | App Installed | App Not Installed |
| ----- | ----- | ----- |
| Brief | ✓ | ✓ |
| Brief Reader | ✓ | ✓ |
| Specific Brief | ✓ | ✓ |
| Brief by Date | ✓ | ✓ |
| Article Explore | ✓ | ✓ |
| Company Explore | ✓ | ✓ |
| Article Detail | ✓ | ✓ |
| Company Detail | ✓ | ✓ |
| Watchlist | ✓ | ✓ |

### **Test Cases**

**Installed app**

1. Open the Singular Link.  
2. Confirm the app launches.  
3. Confirm the correct screen opens.  
4. For parameterized links, verify that the correct Brief/article/company is loaded.

**Not installed**

1. Open the Singular Link.  
2. Complete the app installation.  
3. Launch the app.  
4. Complete any required onboarding flow.  
5. Confirm the deferred deep link routes the user to the intended destination.

---

# **14\. Important Implementation Notes**

### **Custom scheme**

The application deep-link scheme is:

inc42brief://

### **Singular domain**

The Singular Link domain is:

https://inc42.sng.link/

### **Deep-link parameter**

Singular uses:

\_dl

when the destination is manually appended to an existing Singular Link.

### **Encoding**

There are two different cases:

**Direct Singular dashboard configuration**

Use:

inc42brief://article/example-slug

**Manually constructing a Singular URL**

Use:

YOUR-BASE?\_dl=inc42brief%3A%2F%2Farticle%2Fexample-slug

Do not mix these two formats.

---

# **15\. Final Configuration Summary**

The canonical app deep-link routes are:

inc42brief://brief  
inc42brief://brief/read  
inc42brief://brief/read?briefId={id}  
inc42brief://brief/read?briefDate={YYYY-MM-DD}  
inc42brief://explore?mode=articles  
inc42brief://explore?mode=companies  
inc42brief://article/{slug}  
inc42brief://company/{slug}  
inc42brief://watchlist

The corresponding app-side routing implementation is:

src/core/linking/mapInboundUrl.ts

These routes should be treated as the source-of-truth deep-link patterns for configuring Singular Links and validating inbound navigation in the Inc42 Brief application.

# App V2 \- Social Intelligence

# **Inc42 App \- Social Intelligence (Pulse)**

## **Product Requirements Document**

**Owner:** Ranjith \- Product & AI  
**Version:** v1.0 (draft)  
**Date:** 27 July 2026  
**Status:** For review \- Utkarsh (tech), Nityam (design), Editorial  
**Name:** Pulse \- the reader-facing name for Social Intelligence  
**Review owner:** Editorial \- owns daily review and the allowlist

---

# **1\. What we are building**

Inc42 tells readers what happened. Pulse shows what the ecosystem is saying about it.

We collect top LinkedIn and X posts from ecosystem leaders, filter them, and turn them into 1–2 line summaries with quotes \- placed in two spots in the app.

### **The gap**

Readers get the news from us.  
They get the opinion by scrolling LinkedIn and X.  
Nobody packages the opinion. That's the opportunity.

---

# **2\. How it works \- high level**

* An agent pulls top posts from LinkedIn and X daily.  
* An LLM filters out the junk \- irrelevant, promotional, thin, unverified.  
* Surviving posts are matched to an Inc42 story (by company / founder / event).  
* The LLM groups them and writes a 1–2 line summary with quotes.  
* Editorial reviews every single one. Nothing goes live without approval.  
* Approved Pulses publish twice a day \- 11 AM and 5 PM IST.

Detail on filtering rules is in §6, on review in §7.

---

# **3\. Scope**

## **In scope**

* Sources: LinkedIn and X only \- top posts from ecosystem leaders  
* Two surfaces: in-article Pulse \+ a Pulse section  
* LLM-assisted filtering, grouping and drafting  
* 100% editorial review before anything publishes  
* Publish 2× a day

## **Not in scope**

* First-party trending ("Saved by 500+", read counts)  
* Comments, replies, likes, DMs, user-to-user follows  
* Any user-generated content  
* Infinite scroll anywhere  
* Article-length write-ups

---

# **4\. The two surfaces**

## **4.1 In-article Pulse**

**Where:** At the end of an article, below the body.

**Conditional:** Only appears when the story has an approved Pulse. If there's nothing, the section does not exist. No empty state.

**Collapsed (default):** 1 line \+ 1 quote. Reads in under 10 seconds.

### **THE PULSE**

**Investors are split on the valuation.**

> "Stretched for this growth rate."

**View more →**

**Expanded:** Full 2-line summary \+ up to 4 quotes, each linking to the original post. More quotes, not more prose.

---

## **4.2 Pulse section**

A dedicated Pulse section in the app.

| Block | Content | Count |
| ----- | ----- | ----- |
| Today's Pulse | What the ecosystem is talking about now | 5 |
| Moving Fast | New since the last publish | 3 |
| Most Debated | Stories where opinion is split | 3 |
| This Week | Recurring themes | 5 lines |

Hard stop at the bottom: **"That's the pulse. Updated twice a day."**

Timestamped. No infinite scroll, no pagination, no "load more."

Cards use the same collapsed format; tapping opens the article.

---

## **4.3 How the two differ**

|  | In-article Pulse | Pulse section |
| ----- | ----- | ----- |
| **Reader intent** | "Tell me more about this" | "Tell me what's happening" |
| **Scope** | One story | Whole ecosystem |
| **Entered from** | Article | Bottom nav |

**In-article Pulse ends a story. The Pulse section starts a session.**

---

# **5\. What a Pulse looks like**

## **5.1 The four buckets**

Every approved post gets exactly one bucket.

| Bucket | What it is | Lines | Why that length |
| ----- | ----- | ----- | ----- |
| **Reaction** | A leader gives their view on a news event | 1 | The quote carries it |
| **Insight** | Original analysis or a pattern nobody reported | 2 | A claim needs its evidence |
| **Announcement** | News from the person themselves ("we've raised $12M") | 1 | It's a fact \- nothing to summarise |
| **Debate** | The event splits opinion into two clear camps | 2 | One line per side, or it reads biased |

---

## **5.2 Consensus vs split**

| Type | When | Output |
| ----- | ----- | ----- |
| **Consensus** | 3+ credible posts, one dominant view (≥65%) | 1 line \+ quotes |
| **Split** | 3+ credible posts, no dominant view | 2 lines, one per side |

Fewer than 3 credible posts → no Pulse. The story gets nothing.

---

## **5.3 Hard limits**

* Max 2 lines of Inc42-written text. Always. No exceptions.  
* Max 1 quote collapsed, 4 expanded.  
* Never quote more than \~30 words from a post.  
* Never article-length. It's a caption, not a second story.  
* Add a line only when removing it changes the meaning.

---

## **5.4 Link-out (rare)**

For the occasional substantive post where summarising destroys the value, editorial can flag **"Link out"**.

Output stays one line:

> An investor broke down why this round is riskier than it looks.

**Read the full post →**

Manual only. The LLM never triggers this.

---

# **6\. Filtering and categorisation rules**

## **6.1 What gets rejected**

| \# | Filter | Reject when |
| ----- | ----- | ----- |
| 1 | Not relevant | Not about the Indian startup ecosystem |
| 2 | Already covered | We've published this take in the last 7 days |
| 3 | Unverified claim | Facts with no source, rumour, or contradicts our reporting |
| 4 | Low substance | Under 15 words, congratulations, emoji-only, plain repost |
| 5 | Promotional | Self-promo, product launches, hiring posts, ads, event plugs |
| 6 | Not credible | Poster is not on the allowlist |
| 7 | Toxic | Personal attacks, harassment, unproven allegations |
| 8 | Stale | Older than 72 hours, unless the story is still running |
| 9 | BrandLabs overlap | Story is already covered as sponsored content \- flag, don't reject |

---

## **6.2 LLM behaviour rules**

* Every rejection returns a reason code. No silent drops.  
* Reject when uncertain. Precision matters more than volume.  
* Confidence below 0.7 on any call → flag for human decision.  
* Never rewrite a post to make it pass.  
* Never invent a name, title, company or link. Missing stays blank.  
* Plain English. No hype words. Neutral voice \- report the view, never endorse it.  
* Never state an opinion as fact. Always attribute the stance.

---

## **6.3 How buckets are assigned**

* Poster is announcing their own news → **Announcement**  
* Post has data, a pattern or analysis not already reported → **Insight**  
* Story has credible posts on both sides → **Debate**  
* Otherwise → **Reaction**

One bucket per post. Debate is decided at story level \- a single post can never be a Debate.

Below 0.7 confidence, default to Reaction and flag.

---

## **6.4 Matching to a story**

We match on the company or event \- not on mentions of Inc42. Leaders post about the company; they aren't replying to us.

**Match keys:**

* Company name and handle  
* Founder / investor names  
* Event type \+ date window (funding, layoff, IPO, shutdown)

---

# **7\. Editorial review**

Nothing publishes without human approval. No exceptions, no auto-publish.

## **Actions available**

| Action | Effect |
| ----- | ----- |
| **Approve** | Publishes at the next slot |
| **Edit & approve** | Edit the text or quotes, then publish |
| **Swap quote** | Replace a selected quote |
| **Change bucket** | Override the LLM's classification |
| **Flag "Link out"** | Convert to the 1-line \+ link format |
| **Hold** | Keep for the next slot |
| **Reject** | Killed, with a reason |
| **Kill switch** | Remove a live Pulse from the app immediately |

## **Rejection reasons**

Reviewer must pick one. All logged and used to tune the LLM.

| \# | Reason | Use when |
| ----- | ----- | ----- |
| 1 | Wrong match | Attached to the wrong story or company |
| 2 | Misread stance | LLM got the opinion backwards |
| 3 | Not newsworthy | Valid but nobody cares |
| 4 | Weak quote | Quote doesn't stand on its own |
| 5 | Duplicate | Same take already published |
| 6 | Legal risk | Defamation, unproven claim, ongoing case |
| 7 | Commercial conflict | BrandLabs or advertiser conflict |
| 8 | Source concern | Poster no longer credible on this topic |
| 9 | Tone off | Hype, snark, or a voice that isn't ours |
| 10 | Editorial call | Anything else \- free-text note required |

### **BrandLabs items**

BrandLabs \= Inc42's sponsored content.

External opinion on a paid story is a commercial risk. These go to a separate queue with editorial \+ commercial sign-off.

Never auto-rejected, never fast-tracked.

### **Feedback loop**

Weekly: review rejection reasons by volume, tune the prompts and the allowlist.

**Target:** Rejection rate under 20% within 8 weeks.

---

# **8\. Attribution**

Every third-party opinion must be attributed. No orphan quotes.

Inc42 writes the summary (byline). The opinion belongs to the person who said it (attribution). Both appear.

## **Why it's non-negotiable**

**Legal.** "This is a down-round in disguise" unattributed \= Inc42 said it, about a real company. Attributed \= we're reporting. Same sentence, completely different liability.

**The name is the value.** "Someone thinks the burn is unsustainable" is noise. "A Series B investor thinks so" is signal.

**Copyright and platform terms** require credit and a link.

**Distribution.** Tagged people reshare \- our cheapest install channel.

## **Required on every quote**

* Name  
* Handle/profile  
* Title and company (where known)  
* Link to the original post  
* Platform

---

# **9\. Admin tool**

* Review queue \- filterable by bucket, flag and confidence  
* Preview \- shows exactly how it renders in-app, collapsed and expanded  
* Actions \- everything in §7, one click each; rejection reason mandatory  
* Allowlist management \- add/remove ecosystem voices  
* Publish scheduler \- 11 AM and 5 PM IST  
* Kill switch \- per Pulse and per source

---

# **10\. Success metrics**

| Metric | Tells us |
| ----- | ----- |
| Pulse expand rate ("View more") | Is the summary interesting enough to open? |
| Pulse section DAU and completion rate | Is it a real destination? |
| Outbound taps to original posts | Are we adding value? |
| Share rate of Pulse cards | Is the distribution loop working? |
| D7 / D30 retention, Pulse users vs others | Retention impact |

**Guardrail:** Article completion rate must not drop. If Pulse pulls people out of articles, it's failing.

---

# **11\. Legal and compliance**

| Area | Position |
| ----- | ----- |
| **Copyright** | Short excerpts only, never full posts. Always credited and linked. |
| **Platform terms** | Automated collection must be reviewed against LinkedIn and X terms before build. Open item. |
| **Defamation** | All opinions are attributed to a named person. Inc42 never asserts the claim. |
| **Personal data** | Public professional info only \- name, handle, title, company. |
| **DPDP** | No new personal data collected from our users. No new consent needed. |
| **Store labels** | No new data categories → Apple and Play labels unchanged. Confirm with Animesh. |
| **Takedown** | Remove within 48 hrs on request; add to a blocklist. |

---

# **12\. Risks**

| Risk | Mitigation |
| ----- | ----- |
| Automated collection breaches platform terms | Legal review before build. May force manual or vendor-based collection. |
| Review load is too heavy for editorial | Filters must cut hard. Watch daily review time in week 1\. |
| Most stories yield nothing | Expected. Only big stories clear 3 credible posts. Pulse stays rare and therefore meaningful. |
| A bad quote damages credibility | Allowlist gate, 100% review, kill switch. |
| Pulse section turns into a scroll | Capped blocks, explicit end state, no pagination. |
| Reads like Inc42's own opinion | Attribution rules in §8, neutral-voice rules in §6.2. |
| LLM invents a quote or source | Every quote must resolve to a stored post with a working URL. No URL → cannot publish. |

---

# **13\. Open questions**

| \# | Question | Owner |
| ----- | ----- | ----- |
| 1 | Media in posts \- how many carry images / video / PDF / carousel, and does it add value? See 13.1. | Ranjith |
| 2 | Allowlist \- 50 curated voices, or open \+ scoring? (50 curated recommended) | Ranjith |
| 4 | BrandLabs \- confirm flag-not-reject | Ranjith |

---

# **13.1 Media in posts**

We don't know how many posts carry images or attachments, and we don't know whether the written copy or the attachment carries the value. It can go either way.

**Next step:** Sample 200 posts across LinkedIn and X. Tag media type, and whether the media carries the meaning. Decide from real numbers.

**Until then:**

* Don't display media in the Pulse block.  
* Flag media-carrying posts.  
* A short post with media goes to human review instead of auto-reject.

---

# 

# 

# Brief: Title \+ Image Generation

# **Brief Title, Push Notification & Image \- Generation Logic**

Every title and push is generated \- nothing is pre-written. All generation rules are in **§02**, image logic in **§03**. Decisions are closed \- **§06**.

**Owner:** Ranjith M  
**Reviewer:** Utkarsh Agarwal  
**Date:** 27 Jul 2026  
**Status:** Draft \- for lock

---

# **01\. Agreed on the 23 Jul Call**

### **Per-user AI titles**

**Rejected** \- 500 users × 8 articles ≈ 4,000 generations/day.

### **Generation unit**

One set per sector and per topic, generated fresh daily. Same pool for everyone; only the pick is personalised.

### **Nothing pre-written**

No canned copy \- statics go blind within days and kill CTR.

### **Topics in copy**

Logic only. Never "updates from Funding" \- summarise the article.

### **Featured article**

Anchors title, push and image when editorial marks one.

---

# **02\. Title & Push Generation**

## **2.1 One Generation \= One Set**

Four fields from a single model call \- which is what stops the header and the notification contradicting each other. This is exactly what one user sees.

| Field | Where | Cap |
| ----- | ----- | ----- |
| `title` | Brief header | 60 |
| `subheader` | Line under the header | 70 |
| `push_title` | Notification headline | 32 |
| `push_body` | Notification body → Customer.io | 100 |

One set per sector and per topic that has at least one article that day \- so a day with articles in 4 sectors gives 4 sector sets, not 7\.

**Ceiling:** 7 \+ 10 \= ≤17 generations a day for the entire user base. Each user gets one.

---

## **2.2 The Four Cases**

Sector and topic behave identically. The only variable is whether an App Featured article exists that day.

| Case | Group | Featured? | Prompt Gets | Title Shape & Example |
| ----- | ----- | ----- | ----- | ----- |
| 1 | Sector | No | That sector's articles, ranked | The sector's lead story \+ a second beat if it fits. **Fintech, 20 Jul → "Paytm back in profit; Veriqus raises ₹387 Cr"** |
| 2 | Sector | Yes | Featured article \+ that sector's articles, same call | Featured story leads; sector's lead story second. **DeepTech, 11 Jul → "ideaForge raises ₹500 Cr; Zetwerk cofounder's new AI bet"** |
| 3 | Topic | No | That topic's articles, ranked. Topic name is context only \- never in the copy. | The topic group's lead story \+ a second beat. **Controversies, 23 Jul → "NCLT stays BYJU'S insolvency bidding till Aug 31"** |
| 4 | Topic | Yes | Featured article \+ that topic's articles, same call | Featured story leads; topic's lead story second. Topic still never named. **Controversies, 15 Jul → "Emergent joins the unicorn club; nuclear plant files leak"** |

The featured article always leads in **cases 2 and 4** \- it supersedes all ranking and is the first card in every brief. The push follows the same case.

**If two articles are marked featured, the most recently published one anchors.**

---

## **2.3 The Daily Pass \- 06:45 IST**

Pull the window's articles and check for an App Featured article \- that selects the case for the whole run.

* **Group by sector → one generation each.** Case 1 or 2\.  
* **Group by topic → one generation each.** Case 3 or 4\.

Cache every set against the day's brief. Nothing is regenerated at render time.

---

## **2.4 The Pick \- Per User, at Render**

Read the sectors and topics of the 8 articles this user actually gets.

**Candidates** \= sectors they follow that appear in their brief today.

* **One** → serve it.  
* **Two or more** → the higher-ranked one in §2.5.  
* **None of their followed sectors appear** → the highest-ranked sector that does, followed or not.  
* **No sector at all** → the topic set, same method.

100% of articles carry a topic, so this always resolves.

Read from the delivered articles, not onboarding alone \- otherwise the header says **"Fintech"** over a brief full of ecommerce.

---

## **2.5 Precedence Order**

Static config, ranked by publishing volume over the sampled window. Reviewed quarterly, not recalculated daily.

1 sectoro 

| Rank | Sector | Share | Rank | Topic | Share |
| ----- | ----- | ----- | ----- | ----- | ----- |
| 1 | Ecommerce & D2C | 22.0% | 1 | Funding | 24.8% |
| 2 | Fintech | 16.5% | 2 | Trending | 22.6% |
| 3 | AI | 15.7% | 3 | Financials | 19.5% |
| 4 | DeepTech | 14.2% | 4 | Controversies | 10.5% |
| 5 | Consumer | 12.6% | 5 | IPO | 7.5% |
| 6 | Enterprise & SaaS | 11.0% | 6 | M\&A | 6.8% |
| 7 | Startup Ecosystem | 7.9% | 7 | Policies | 6.0% |
| 8 | \- | — | 8 | People | 1.5% |
| 9 | — | — | 9 | New Funds | 0.8% |
| 10 | — | — | 10 | Business Intelligence | — |

### **Two Notes on These Numbers**

**Ecommerce & D2C outranks Fintech.** A user following both is served the Ecommerce title.

**The topic column is provisional.** These are the 10 agreed topics, but the export carried no topic field — only `post_id`, `title`, `slug`, `post_date`, `app_featured` and the body fields — so each topic was inferred from the headline. "Trending" absorbs anything the rules couldn't place, which is why it sits at \#2, and Business Intelligence returned nothing.

**Action:** Re-export with the `Development_Type` tag before locking.

### **Where This Misfires**

A static order ignores today's volume — 1 ecommerce story against 5 fintech ones still serves Ecommerce.

**Recommended guard:** A lower-ranked followed sector wins if it has **3 or more additional articles** in that user's brief.

---

## **2.6 Copy Rules**

### **Title & Subheader**

Use only the headlines supplied — no outside information, no numbers that aren't in them.

* Never name the sector or topic.  
* Company names exactly as the source spells them.  
* No emoji.  
* No clickbait.  
* No cliffhangers.  
* Never mention a company that isn't in the brief.  
* No article counts in the title.

### **Push**

| Rule | Instead of | Write |
| ----- | ----- | ----- |
| Lead with the fact that changes something, not the event | Paytm posts Q1 results | Paytm is profitable again |
| Close with what else is inside | …and Scapia buys back ESOPs. Read on. | …Four more fintech moves in today's brief. |
| Never end on a dead phrase | Read on · Read today · Your brief awaits | A concrete count, stake or consequence |
| One number, not three | ₹220 Cr, ₹387 Cr and 20% in one line | The sharpest number; the rest is inside |

### **Delivery**

Push copy → Customer.io as the campaign payload, keyed by group.

Title, subheader and image come from the API \- nothing hardcoded, or every copy change needs an App Store release.

**Animesh to confirm.**

---

# **03\. Image \- LOCKED**

### **App Featured Article Exists**

→ Its lead image.

Title and image agree by construction, since the same article anchors both.

### **No Featured Article**

→ The poster uploaded by the editorial team for that day.

### **Neither**

→ The default image.

This closes the title-vs-image coherence question: on featured days the featured article settles it, and on every other day a human picks the visual.

No `lead_article_id` and no image-selection logic is needed.

### **One Constraint on the Uploaded Poster**

One poster is shown to everyone that day, but titles are personalised by sector.

So the poster should be topical rather than company-specific \- a quick-commerce visual over a fintech user's Paytm headline reads as a mismatch.

If editorial does want a company-specific image, it should be the day's biggest story, since that's what most users' titles will lead with.

---

# **04\. Sampling Evidence**

**Dataset:** `p (3).csv`  
**Date Range:** 9–23 Jul 2026\. 24 Jul excluded \- the export was pulled that morning and holds one article.

### **Sample Summary**

* **133** articles  
* **83%** carried a sector  
* **4/13** days had a featured article  
* **4–16** articles per day  
* **67** title \+ push pairs

Titles as generated. Push copy rewritten to the §2.6 rules \- the sampled version closed on "Read on".

| Date · Group | Brief Title | Push |
| ----- | ----- | ----- |
| **20 Jul · Fintech \- Case 1** | Paytm back in profit; Veriqus raises ₹387 Cr | **Paytm is profitable again**₹220 Cr in Q1, and Veriqus just raised ₹387 Cr. Four more fintech moves in today's brief. |
| **11 Jul · DeepTech \- Case 2** | ideaForge raises ₹500 Cr; Zetwerk cofounder's new AI bet | **ideaForge's ₹500 Cr raise**ideaForge mops up ₹500 Cr via QIP \- and a Zetwerk cofounder just left to build in AI. |
| **22 Jul · Ecommerce \- Case 1** | Eternal's profit triples; quick-commerce war cools | **Eternal's profit nearly triples**Blinkit's EBITDA is up and its CEO says peak discounting is over. What that means, inside. |

---

# **05\. Risks & Ops**

| Risk / Ops | Details |
| ----- | ----- |
| **Featured marking window** | The flag must be set before the 06:45 run \- sets are cached after that, so a later marking has no effect on that day's brief. In the sample, featured existed on 4 of 13 days. |
| **17% have no sector** | They surface only via the topic layer. Content tagging fix is a separate P0. |
| **Topic order unverified** | Derived from headlines, not the CMS field. Re-export before locking §2.5. |
| **Volume & cost** | ≤17 generations/day on Claude Sonnet 5 ≈ $0.11/day, under $4/month. |
| **Failure path** | Retry. If it still fails, one hardcoded safety line \+ the default image \- an engineering net, not a content strategy. |

---

# **06\. Decisions Closed**

### **Image Source**

Featured article's image on featured days; editorial uploads the poster on every other day; default image if neither.

No image-selection logic.

**Reference:** §03

### **Topic Layer**

Keep cases 3 and 4 \- needed for the 17% of articles that have a topic but no sector.

**Reference:** §2.2

### **Featured Article**

Editorial marks one when the day warrants it.

Cases 2 and 4 run when one exists; cases 1 and 3 when it doesn't.

Both paths ship a complete brief.

**Reference:** §2.2

# Notification Permissions & Re-Ask Logic

# **Notification Permissions & Re-Ask Logic**

## **Objective**

Maximize notification opt-in without triggering alert fatigue. Handle first ask, re-asks after denial, and in-app preference management.

## **Notification types**

* **Brief** — daily digest. Single toggle.  
* **Alerts** — based on entities the user follows. Master toggle \+ per-entity control.

## **1\. First ask (native prompt)**

* Fires once on the **Brief page** (first screen post-auth), for both auth-completed and auth-skipped users.  
* This is the one native OS prompt. All logic below applies **only after** this first prompt has been shown.

## **2\. Permission states**

* **Granted** → no asks. User manages types in Profile \> All Notifications.  
* **Not determined** → native prompt still available.  
* **Denied** → native prompt dead on iOS (and Android after 2nd deny). Re-asks \= in-app soft-ask only.

## **3\. Re-ask triggers (post-denial, soft-ask only)**

| Type | Trigger | Copy anchor |
| ----- | ----- | ----- |
| Alerts | User **follows an entity** while permission off | "Get alerts on {entity}?" |
| Brief | User returns after **2+ day gap** while brief off | "You missed {N} briefs" |

* Soft-ask \= bottom sheet, "Turn on" / "Not now".  
* "Turn on" → `requestPermission(fallbackToSettings: true)` (native if available, else deep-link to system settings).

## **4\. Caps (apply only after first native prompt)**

* **Cooldown:** 30 days between any re-asks.  
* **Lifetime cap:** stop after **2 dismissals** (dismissal \= stronger no than a show).  
* **Suppression:** never fire if already on; never stack two asks in one session; reset on opt-in.

## **5\. Profile \> All Notifications (in-app hub)**.

* Turning off \= suppress server-side sends (no OS involvement).  
* If OS permission denied → show banner \+ deep-link to system settings.  
* Always-available entry point; no cooldown (user-initiated).

# Account deletion

# **Account Deletion**

**Owner:** Ranjith  
**Surfaces:** iOS, Android, Web, Datalabs  
**Status:** Draft for Engineering

---

# **1\. Why**

## **Background**

Both Apple and Google now require users to be able to permanently delete their account directly from within the product. In addition, India's DPDP Act requires users to be provided the right to be erased.

Today, Inc42 does not support account deletion on any platform. This blocks Google Play compliance, risks Apple App Store review, and creates a regulatory compliance gap.

| Driver | Requirement |
| ----- | ----- |
| Apple App Store Review Guideline 5.1.1(v) | Account deletion must be initiated inside the app. Deactivation-only is not sufficient. |
| Google Play (2023 onwards) | Users must be able to delete their account both from within the app and via a public web URL without reinstalling the app. |
| DPDP Act | Users have the right to request deletion of their personal data. Requests must be completed within 30 days. |

---

# **2\. Scope**

| Surface | Deliverable |
| ----- | ----- |
| iOS | Delete Account under **Settings → Account** |
| Android | Delete Account under **Settings → Account** |
| Web | Public deletion page at **inc42.com/delete-account** |
| Datalabs | User session terminated when deletion is requested |

---

# **3\. Account States**

## **States**

| State | Description |
| ----- | ----- |
| **active** | Normal account state |
| **pending\_deletion** | User has requested deletion. Account is restorable for 3 days. User is signed out everywhere. |
| **deleted** | Account and associated data have been permanently deleted. Restoration is not possible. |

## **State Transitions**

active  
    │  
    └── User confirms deletion  
            │  
            ▼  
pending\_deletion  
    │  
    ├── Login within 3 days  
    │         │  
    │         ▼  
    │      active  
    │  
    └── No login for 3 days  
              │  
              ▼  
          deleted

### **Exception**

If unauthorized access, fraud, or identity verification is required, deletion may be delayed, but must be completed within the 30-day legal limit.

> **Definition:** "3 days" means **72 hours from the deletion request (IST).**

---

# **4\. User Flows**

## **4.1 iOS / Android (Logged In)**

1. Navigate to **Settings → Account → Delete Account**  
2. User taps **Delete Account**  
3. Show confirmation dialog  
4. User confirms deletion  
5. Account state changes to **pending\_deletion**  
6. User is signed out immediately  
7. All active sessions are revoked  
8. Success message is displayed

---

## **4.2 Web (Logged In)**

URL:

**inc42.com/delete-account**

Flow:

1. User opens the page  
2. Clicks **Delete Account**  
3. Confirmation dialog is shown  
4. User confirms deletion  
5. Account moves to **pending\_deletion**  
6. User is signed out from Web and Datalabs  
7. Success message is displayed  
8. IOS and Android should also be logged out.

---

## **4.3 Web (Logged Out)**

Flow:

1. Open **inc42.com/delete-account**  
2. Display **Log in to Delete Your Account**  
3. User logs in  
4. Show confirmation dialog  
5. User confirms deletion  
6. Same flow as logged-in users

> Login serves as identity verification and satisfies Google Play's public deletion URL requirement.

---

## **4.4 Forced Sign-out (Other Devices)**

Whenever account deletion is requested, every active session is terminated.

Display:

**You've been signed out**

We signed you out because you requested to delete your Inc42 account.

If this was a mistake, sign in within 3 days to restore your account.

Signing in after 3 days will create a new account, and your previous data and history cannot be restored.

---

## **4.5 Restore Flow**

If the user signs in within 3 days:

* Account returns to **active**  
* Saved articles are restored  
* Tracked companies are restored  
* Watchlists are restored  
* User preferences are restored  
* Fire **account\_deletion\_cancelled**

---

## **4.6 Permanent Deletion**

After 72 hours:

* Permanent deletion job executes  
* Account becomes **deleted**  
* Signing in using the same email creates a brand-new account  
* Previous data cannot be recovered

---

# **5\. Session Revocation**

Immediately after an account enters **pending\_deletion**, all active sessions must be terminated.

Platforms:

* iOS  
* Android  
* Web  
* Datalabs

## **Implementation**

Invalidate the complete Auth0 session family by revoking refresh tokens.

A valid JWT continuing until expiry is not acceptable, as users would remain logged in despite requesting deletion.

## **Sign in with Apple**

For users authenticated through Sign in with Apple:

* Do **not** revoke Apple tokens when deletion is requested.  
* Revoke tokens only after permanent deletion (Day 3).  
* Revoking immediately would prevent restoration.  
* Never revoking risks Apple App Store rejection.

---

# **6\. User Copy**

## **Confirmation Dialog**

**Delete your account?**

If you continue, your account will be scheduled for deletion and you will be signed out of all devices.

You can restore your account by signing in within the next 3 days.

After 3 days, your account and data will be permanently deleted. Signing in after that will create a new account.

---

## **Success Message**

Your account has been scheduled for deletion.

You have been signed out of all devices.

Sign in within the next 3 days to restore your account. After that, your account and data will be permanently deleted and cannot be recovered.

In some cases, we may need to verify your request before completing deletion. See our Privacy Policy for more information.

---

# **7\. Customer.io & Vendor Data**

## **Events**

| Event | Trigger | Action |
| ----- | ----- | ----- |
| account\_deletion\_requested | Day 0 | Set `deletion_pending = true`, store deletion timestamp |
| account\_deletion\_cancelled | User restores | Clear `deletion_pending` |
| account\_deleted | Day 3 | Delete Customer.io person object |

## **Marketing Suppression**

As soon as:

deletion\_pending \= true

Exclude the user from:

* Newsletters  
* Marketing campaigns  
* Push notifications  
* Automated journeys

Every marketing campaign must include a filter ensuring:

deletion\_pending \!= true

to avoid contacting users who have requested deletion.

## **Third-party Data Deletion**

On permanent deletion (Day 3), instruct processors to delete user data.

| Vendor | Action |
| ----- | ----- |
| Customer.io | Delete person |
| PostHog | Delete person profile |
| Firebase Analytics | Delete user data |
| Singular | Submit deletion request |

---

# **8\. Open Decisions**

1. **Paid subscriptions**  
   * What happens when a Datalabs Pro or Team subscriber deletes their account?  
   * Terms currently state deletion does not cancel payment obligations.  
   * Decision required.  
2. **Team Admins**  
   * Can a Team administrator delete their account and leave seats orphaned?  
3. **Restore UX**  
   * Should restoration happen automatically on login?  
   * Recommendation: Automatically restore and display a confirmation toast.  
4. **Newsletter Infrastructure**  
   * Confirm whether all newsletters originate from Customer.io.  
   * If other systems exist, suppression must be implemented there as well.

---

# **9\. Acceptance Criteria**

* Delete Account is reachable within two taps from Settings.  
* Deleting from iOS signs the user out of Android, Web, and Datalabs.  
* `inc42.com/delete-account` works without requiring the mobile app.  
* Signing in within 3 days restores saved articles, tracked companies, watchlists, and preferences.  
* Signing in after 3 days creates a new, empty account.  
* Sign in with Apple tokens are revoked only after permanent deletion.  
* Users pending deletion receive no newsletters, marketing emails, or push notifications.  
* Deleted users are removed from Customer.io, PostHog, Firebase Analytics, Singular, and other configured processors.

# Feature Flag

# **AskInc42 Feature Flag Rollout Strategy (PostHog)**

## **Current PostHog Status**

### **Ground Truth**

| Check | Finding |
| ----- | ----- |
| **App SDK** | `posthog-react-native` is already integrated and live in the **Inc42 App** project (Project ID: **146258**) |
| **Data Availability** | Collecting data since **1 July 2026** with approximately **38.6K events** across **308 people** in the last 60 days |
| **Feature Flags (App Project)** | **0** feature flags currently exist in the app project |
| **Existing Flags (Organization)** | **2** legacy flags exist, but they belong to the **DataLabs Web** project (Project ID: **66351**) and are stale |

### **Summary**

The PostHog SDK is already integrated, functioning correctly, and sending events to the EU-hosted PostHog instance. No additional SDK integration work is required.

The only remaining implementation work is to create feature flags in PostHog and consume them through the existing Feature Flag APIs.

---

# **Rollout Controls Available**

PostHog already supports all rollout mechanisms needed for AskInc42.

| Rollout Capability | Supported | Recommended Usage |
| ----- | ----- | ----- |
| Percentage Rollout | ✅ | Gradual rollout (1% → 5% → 25% → 100%) |
| Sticky Bucketing | ✅ | Ensures users remain consistently in the same rollout bucket |
| Person Property Targeting | ✅ | Target users using properties like `is_registered`, `role`, `push_opt_in`, `streak_tier` |
| Cohort Targeting | ✅ | Roll out to cohorts such as "Plus Subscribers" or "7-Day Streak Users" |
| Individual Targeting | ✅ | Internal employee dogfooding using `distinct_id` |
| Geo / OS / Device Targeting | ✅ | Ship to iOS first while Android rollout follows |
| Multivariate (A/B Testing) | ✅ | Experiment with prompt variants, UI copy, or end-of-brief experiences |
| Payload / Remote Configuration | ✅ | Update prompts, copy, and configuration without shipping a new app version |

---

# **Existing User Properties Available for Targeting**

The application already sends several useful user properties to PostHog, allowing sophisticated rollout rules without additional engineering effort.

Current properties include:

* `is_registered`  
* `auth_method`  
* `role`  
* `sector_groups`  
* `topic_groups`  
* `push_opt_in`  
* `install_date`  
* `registration_date`  
* `streak_tier`  
* `current_streak`  
* `max_streak`  
* `walkthrough_status`  
* `watchlist_count`  
* `attribution_source`  
* `attribution_campaign`  
* `email`

These properties can be used immediately for audience segmentation and phased rollouts.

---

# **React Native Feature Flag Considerations**

## **1\. Feature Flags Remain Cached Indefinitely**

### **Issue**

The React Native SDK does not automatically expire cached feature flags.

A user who has not opened the app for several days or weeks may continue using an outdated flag configuration until a successful refresh occurs.

### **Recommendation**

Refresh feature flags:

* every app launch  
* every app foreground

reloadFeatureFlagsAsync()

This ensures rollout changes and kill switches propagate as soon as users reopen the app.

---

## **2\. Bucketing Can Change After Login**

### **Issue**

Percentage rollouts are based on `distinct_id`.

During authentication:

Anonymous User  
↓  
Identified User

the `distinct_id` changes.

As a result, a user who previously belonged to the rollout group may suddenly fall outside it (or vice versa).

### **Recommendation**

After calling:

identify(...)

the application should:

1. Persist feature flags across authentication.  
2. Immediately reload feature flags.

This keeps rollout behaviour predictable after login.

---

## **3\. First Launch Returns `undefined`**

### **Issue**

Feature flags are loaded asynchronously.

Before the initial `/flags` API request completes, hooks may return:

undefined

Rendering AskInc42 immediately based on a truthy flag check can therefore produce inconsistent behaviour or UI flicker.

### **Recommendation**

Use either:

* `onFeatureFlags()`  
* sensible bootstrap defaults  
* an explicit loading state

Do not render AskInc42 until feature flag evaluation has completed.

---

# **Additional Caveat**

Only approximately **19 out of 95** identified users currently have the `email` property populated.

Using email as a rollout criterion would therefore exclude most users.

For internal testing, prefer:

* `distinct_id`  
* `is_internal` (recommended dedicated property)

rather than relying on email.

---

# **Why Feature Flags Matter for AskInc42**

The mobile application is currently awaiting App Store approval.

Feature flags allow AskInc42 to be included in the launch build while remaining disabled by default.

Once Apple approves the application, the feature can be enabled entirely from PostHog without submitting another build.

This provides several operational advantages:

* Launch AskInc42 gradually after release.  
* Start with internal users only.  
* Roll out incrementally (1% → 5% → 25% → 100%).  
* Instantly disable the feature if issues arise.  
* Modify prompts and configuration remotely without shipping a new app version.  
* Run A/B experiments to optimize user engagement.

This significantly reduces deployment risk while giving the product team complete control over rollout timing and user targeting.

---

# **Recommended Rollout Plan**

| Phase | Audience | Rollout |
| ----- | ----- | ----- |
| Internal Testing | Employees (`distinct_id` / `is_internal`) | 100% |
| Pilot | Registered users | 1% |
| Early Rollout | Registered users | 5% |
| Expansion | All eligible users | 25% |
| General Availability | Entire user base | 100% |

A server-side kill switch should remain available throughout every phase to immediately disable AskInc42 if required.

# Inc42 rating prompt — placement plan

### **Inc42 rating prompt — placement plan**

**Principle:** trigger on a moment of value. Never a raw store pop-up.

**Gate:** distinct active days ≥ 2 , ≥3 briefs completed, no `app_error` this session, not a past reviewer.

**Triggers (highest signal wins):**

1. **Streak Day 7** — strongest, fires once ever. Fire after the reward celebration. Day 30/100 as fallbacks.\[streak\_updated (milestone\_day)\]  
2. **Share/Save**: \[article\_action, entity\_action\]  
3. **Article completion (\~100%)** : \[article\_completed\]

**Surface:** pop-up (bottom sheet / modal), fired only at the trigger moments — after the **streak celebration**, after a share, or at article completion. Dismissible; respect the 30-day cooldown after dismissal.

* **Rate us** → fire **native** review (stays in-app; iOS `SKStoreReviewController` / Android Play In-App Review).   
* **No Thanks** → dismiss, record it, apply cooldown.

**Never fire on:** launch, mid-read, `app_error`, no network.

**Cooldown & caps:**

* Cooldown runs off your own dialog (trackable): No Thanks → 30 → 60 → 120 days, re-trigger only on a new positive moment.  
* Tapped Rate us → treat as spent, long suppression (native gives no result signal).  
* Native lifetime cap: 3/year on iOS; Android quota undisclosed. Native \= request only, OS decides.

**Enjoying Inc42?**  
`Rate us` · `Not now` 

# Launch Infra

# Inc42 App — Launch Infrastructure & Measurement

**Date**: 2026-07-06 (decisions updated 2026-07-07) · **Status**: Research \+ action list for build handoff · **Owner**: Utkarsh **Decisions locked (2026-07-07)**: MMP \= **Singular** (AppsFlyer \= named backup) · Push/CRM \= **Customer.io only at launch** (MoEngage deferred to a delivery-rate trip-wire, D-block) · Ad networks at launch \= **Meta \+ Google** (Apple Search Ads not at launch → Firebase Analytics **is** launch-blocking) · Product analytics \= **PostHog** \+ crash \= **Firebase Crashlytics** (confirmed) · SKAN schema \= **6-tier "highest-value reached", optimize toward brief-completion** (locked, §C2) · web↔app identity \= **canonical \= Inc42 auth user ID; anonymous device ID before registration** (eng owner TBD — the one open point, §C3) · DPDP consent gate \= **deferred with a note** (§B7). **Scope**: the measurement / attribution / push-delivery / analytics infra the app needs to launch and to run paid app-install campaigns. Companion to `v1-prd.md` — the PRD (§8.5, §9) specifies *what* notifications do and *what* native capabilities are required, but names **no vendors**. This doc fills that hole and flags what's launch-blocking for the \~7–10 day window. *Out of scope here* (build team owns them): the non-measurement §9 native must-haves — in-app account deletion, force-update/min-version gate, ratings prompt, offline/content-scarcity fallback.

**The core finding**: the PRD covers capabilities, not the systems that deliver them. The single biggest gap is **attribution** — there is no way to track paid installs today, and neither Customer.io nor MoEngage is a Mobile Measurement Partner (MMP). The binding constraint for a 10-day window is the app's own §9 "we can't hotfix" rule: several pieces must be in the **submitted binary** at App Store review, so a missing SDK \= a full resubmission cycle.

---

## Part 1 — Research & Findings

### 1.1 Attribution / MMP (the "install campaign tracking" gap)

**Do we strictly need an MMP?** Yes, the moment we buy installs on ≥2 networks. Meta, Google, and Apple Search Ads each self-report installs in their own console — and each claims credit for the *same* install. Without a neutral MMP you cannot get: (a) cross-network deduplicated installs, (b) true blended cost-per-install by campaign in one view, (c) post-install in-app events (brief-completed, watchlist-add, register) attributed back to the specific ad, or (d) deferred deep-link attribution (ad → install → land on the right screen). Firebase/GA4 gives in-app analytics but is **not** a cross-network arbiter and doesn't dedup Meta vs. Google claims.

**DECIDED (2026-07-07): Singular.** Its free plan is genuinely self-serve and generous — **15k paid conversions/mo at $0** (no credit card, no sales gate at Free/Growth), and it bundles the launch essentials that matter here: attribution, SKAdNetwork, deferred deep linking (Singular Links), fraud, and ad-cost/ROAS aggregation. Growth tier is **$0.05/conversion** (vs AppsFlyer's $0.07). Only *paid* conversions count, so with mostly-organic early installs on 2–3 networks we likely sit inside the free tier for weeks. Self-serve signup → fits the 10-day window. Standard \~1–3 dev-day SDK integration.

**Why Singular over AppsFlyer (honest tradeoff).** Where Singular wins: cheaper per conversion, and best-in-class **cost/ROAS aggregation** — overkill at 2–3 networks today, but exactly what pays off as we widen the network mix later (the reason to *stay* on it). Deep linking is **no gap** — Singular Links is a full OneLink equivalent covering the Customer.io email→app routing. What we trade away, all low-stakes for a free news app: (a) AppsFlyer's **SKAN Conversion Studio** is more polished — Singular hand-holds *least* on the pre-launch conversion-value schema (mitigate: lock it early, see §B1); (b) thinner **India local support**; (c) AppsFlyer **Protect360** is the fraud benchmark (low install-fraud incentive vs gaming). **Correction to the earlier pass:** the first take under-sold Singular ("no meaningful free tier / sales-led") — that was wrong; its free tier is real and self-serve. **AppsFlyer stays the named backup.**

**Alternatives considered** (full landscape; Singular is now the decided pick):

| MMP | Free-tier reality | India / consumer fit | Pick it over AppsFlyer when… |
| :---- | :---- | :---- | :---- |
| **Singular** ✅ **CHOSEN** | Free: **15k paid conv/mo**, self-serve, incl. SKAN \+ deep linking \+ fraud; Growth **$0.05/conv** | Fine; India support thinner than AppsFlyer | **Decided.** Cheaper/conv \+ cost-ROAS aggregation that compounds as networks widen. |
| **AppsFlyer** (backup) | "Zero": \~12k conversions, full SKAN 4; Growth $0.07/conv | Best — local offices/support, broadest network integrations | **Named backup.** Deeper India support \+ Protect360 fraud \+ more polished SKAN studio. |
| **Kochava** | Free App Analytics: \~10k conv/mo, **covers paid \+ owned media**, full MMP | Good; thinner India presence, less polished UI | Second free option if Singular's terms don't fit at signup. |
| **Airbridge** | 15k free installs, then flat **$0.05/install**, no contract | Works; India footprint unproven | You'll blow past free tiers fast and want a flat, contract-free rate. |
| **Adjust** | Thin (\~1,500 attributions/mo, 12-mo) | Fine, no cost edge | Already mid/enterprise scale; want flat predictable pricing. |
| **Branch** | Deep-linking free; paid attribution sales-gated (\~$199+/mo) | Deep-linking leader | Deep-linking is primary, paid attribution secondary. |
| **Tenjin** | No free MMP tier; from \~$200/mo | Gaming/ad-LTV heritage | Essentially never, for a news app. |
| **No MMP** (Firebase/GA4 \+ consoles) | Free | — | Only defensible on a *single* network. Firebase Dynamic Links is deprecated → no free deferred-deep-link fallback either. |

**iOS attribution mechanics (the irreversible decision).** Most iOS users deny ATT, so **SKAdNetwork (SKAN 4.0) is the primary iOS attribution channel**. SKAN needs a **conversion-value schema designed before launch** — mapping the fine value (0–63) \+ coarse (low/med/high) to key early milestones inside measurement window 1 (D0–D2). The locked schema is the **6-tier "highest-value reached" ladder in §C2** (not a strict linear funnel — registration is optional, so it sits as the top *value* tier rather than a middle rung). **If skipped: installs still count, but every post-install iOS event is unmeasurable, and it cannot be backfilled retroactively.** The MMP provides schema tooling (Singular's SKAN model config; AppsFlyer's Conversion Studio is more hand-holding if we ever switch), but the *decision of what to encode is ours* and must be locked pre-submission — and because Singular guides this least, locking it early (§B1) is the one mitigation the Singular pick demands. AdAttributionKit (SKAN's successor) is interoperable and a fast-follow — not launch-blocking; Apple has announced no SKAN deprecation.

**Android.** Google [Play Install Referrer](https://developer.android.com/google/play/installreferrer) is read automatically by the MMP/Firebase SDK on first launch. No custom work.

*Sources:* [Singular — MMP](https://www.singular.net/glossary/mobile-measurement-partner-mmp/) · [AppsFlyer pricing](https://www.appsflyer.com/pricing/) · [Kochava Free App Analytics](https://www.kochava.com/product/free-app-analytics/) · [Airbridge — AppsFlyer alternatives 2026](https://www.airbridge.io/en/blog/4-best-appsflyer-alternatives-for-2026-a-deep-dive-into-costs-attribution-accuracy) · [Branch pricing](https://www.branch.io/pricing/) · [SKAN 4 conversion schema (Aarki)](https://www.aarki.com/insights/skan-4-conversion-schema-how-to-design-one-that-actually-works-step-by-step-guide/) · [SKAN 2026 (adlibrary)](https://adlibrary.com/posts/skadnetwork) · [Play Install Referrer](https://developer.android.com/google/play/installreferrer) · [Firebase Dynamic Links deprecation](https://firebase.google.com/support/dynamic-links-faq)

### 1.2 Product analytics

**Recommendation: extend PostHog to the app** (we already run it on web → unified web→app funnels, one query surface). Its iOS/Android/React Native SDKs are production-grade in 2026: funnels, retention, feature flags, mobile session replay. Covers every success metric in PRD §12 (D1/D7/D30, brief-completion, onboarding/watchlist/search funnels, Decode tap-rate, push opt-in). Amplitude/Mixpanel are more mature for heavy behavioral analysis but not worth a second analytics tool at launch.

**Firebase/GA4 — required *if* we run Google App Campaigns.** Google optimizes materially better on native Firebase events than on delayed MMP postbacks, and gates some features (e.g. excluding existing users) to Firebase-linked apps. So: ship the Firebase SDK and log core install/activation events to it as the *Google-ads optimization layer*; PostHog stays the product-analytics tool.

*Sources:* [PostHog React Native SDK](https://posthog.com/docs/libraries/react-native) · [PostHog mobile session replay](https://posthog.com/docs/session-replay/mobile) · [Firebase for UA campaigns](https://addict-mobile.com/en/integrate-firebase-effective-ua-campaigns/) · [Firebase vs MMP (Lupu)](https://medium.com/@daniel-lupu/firebase-vs-mmp-what-happened-when-i-changed-the-source-of-my-google-app-campaigns-optimization-3f99b634e8e7)

### 1.3 Crash & performance monitoring

**Recommendation: Firebase Crashlytics** — free, we're already pulling Firebase in, AI crash insights, tracks crash-free ≥99.5% (PRD §12 target) out of the box. Lower-friction than Sentry for a small team. Sentry wins only if we later want unified backend+app error/trace visibility (fast-follow). **Must be in the launch binary** — launch-week crashes can't be captured retroactively.

*Sources:* [Sentry vs Crashlytics (IndieAppStack)](https://indieappstack.com/comparisons/sentry-vs-firebase-crashlytics-mobile-apps) · [Crash reporting tools 2026 (Shakebug)](https://www.shakebug.com/blog/best-mobile-crash-reporting-tools-in-2026-honest-guide/)

### 1.4 Push & lifecycle messaging

**Plumbing (vendor-independent, LAUNCH-BLOCKING):** APNs `.p8` auth key (Apple Developer → Keys; downloadable once — secure it) \+ Push Notifications & Background Modes **entitlements in the app target** (ship *inside the binary*), and a Firebase project \+ `google-services.json` bundled in the app for Android. Gotcha: no APNs token → FCM can't mint an iOS token. Create these artifacts now regardless of vendor.

**DECIDED (2026-07-07): Customer.io only at launch.** One tool for email \+ push \+ in-app, already wired, no new vendor onboarding inside the 10-day window, and its RN SDK (push via FCM/APNs \+ in-app \+ local-timezone send \+ frequency caps \+ quiet hours) covers the §8.5 spec. MoEngage is **deferred** to a delivery-rate trip-wire (see D5), not dropped.

**What we're knowingly accepting — three gotchas to engineer around:**

- **India Android OEM delivery (the real risk).** \~51% of Indian handsets are Chinese OEMs (Xiaomi/Oppo/Vivo) whose battery/background-kill breaks the FCM connection. **Customer.io is bare FCM** — no push-amplification fallback — so some Morning Briefs silently won't land on exactly the daily-habit devices we care about. *Mitigation:* instrument delivery-rate by device OEM from day one (A3); if it dips below tolerance, [MoEngage Push Amplification](https://www.moengage.com/push-amplification/) Plus (claims up to \+75% delivery on Xiaomi) is the pre-scoped fix. Accepting this risk with eyes open, not by omission.  
- **Grouped push isn't turnkey.** The §8.5 "grouped watchlist alerts" need custom Android notification-channel / summary-notification work on top of the SDK — not a Customer.io setting. Scope it into B6.  
- **Local-time send has a disable condition.** Customer.io's per-user timezone send is disabled when a message also has a daily rate-limit **or** A/B variants. The Morning Brief edition-line push must not carry both, or it silently sends at a fixed UTC time instead of local morning.

*Sources:* [Customer.io React Native SDK](https://docs.customer.io/integrations/sdk/react-native/quick-start-guide/) · [CIO local-timezone send](https://docs.customer.io/journeys/send/timezones/match/) · [MoEngage Push Amplification](https://www.moengage.com/push-amplification/) · [Amp+ delivery impact](https://help.moengage.com/hc/en-us/articles/360039754532-Push-Amplification-Plus-and-Delivery-Impact) · [FCM iOS get-started / APNs .p8](https://firebase.google.com/docs/cloud-messaging/ios/get-started) · [MoEngage pricing (G2)](https://www.g2.com/products/moengage/pricing) · [Customer.io pricing](https://customer.io/pricing)

### 1.5 CDP / event pipeline / identity resolution

**Recommendation: defer the CDP (RudderStack) to fast-follow (weeks 4–8)** — but **lock a consistent web↔app `user_id` / `distinct_id` convention now.** At launch the SDK set (PostHog \+ Singular \+ Customer.io \+ Firebase/Crashlytics) is manageable; a CDP isn't worth blocking launch for a small team. The ID convention is the actually-load-bearing decision — it's what enables later identity stitching between anonymous web (PostHog) and logged-in app users. RudderStack (India-friendly, \~50–80% cheaper than Segment, event-priced) is the pick when event volume/identity pain becomes real.

*Sources:* [RudderStack vs Segment 2026 (Volument)](https://www.rudderstack.com/competitors/rudderstack-vs-segment/) · [RudderStack vs Segment](https://www.rudderstack.com/competitors/rudderstack-vs-segment/)

### 1.6 Consent / India DPDP

DPDP Rules were notified Nov 13 2025; full consent/notice enforcement lands **May 13 2027** — we're in a calibrated grace period, so consent doesn't legally gate the launch. **But** DPDP requires *explicit* consent for analytics (stricter than GDPR — no "legitimate interest" analytics). The research recommendation was to ship a simple first-run consent/notice screen at launch and gate the tracking SDKs behind it — but the **decision (2026-07-07) was to defer it** (§B7): the launch build ships without the gate, tracking SDKs fire on first launch, and a lightweight consent screen is scheduled well ahead of the May 2027 enforcement date (full CMP \= D3). Accepted knowingly — it's a pre-deadline convenience, not a legal requirement today. *(Note: ATT (B2) is a separate, still-required Apple prompt — unaffected by this deferral.)*

*Sources:* [DPDP mobile compliance (Respectlytics)](https://respectlytics.com/blog/india-dpdp-act-mobile-app-compliance/) · [DPDP Phase 1 timeline (Secure Privacy)](https://secureprivacy.ai/blog/india-dpdp-act-phase-1)

### 1.7 Gaps this surfaces vs. the current PRD

Beyond the three areas originally flagged (analytics, install tracking, push), the research surfaced: (1) MMP/attribution has **no home** in the PRD; (2) SKAN conversion-value schema is a **pre-submission design decision**, not a config toggle; (3) FCM/APNs plumbing is a **distinct launch-blocking prerequisite** separate from vendor choice; (4) Firebase is a **dependency of Google App Campaigns**, not optional if buying Google installs; (5) crash tooling had a target but no tool; (6) **web↔app identity** \+ the `user_id` convention needs deciding now; (7) a **DPDP consent gate**.

---

## Part 2 — Action Items

Grouped by urgency. 🔴 \= must be in the **submitted binary** (non-hotfixable per §9) or otherwise launch-blocking. 🟠 \= launch-required but server-side/config. ⚪ \= fast-follow.

### A. Start today (lead-time-critical — external dependencies)

**A1. Create Apple APNs `.p8` key \+ push entitlements, and the Firebase project.** 🔴 The vendor-independent plumbing under *all* push and Android analytics. Downloadable-once key (secure it); entitlements ship inside the binary. Gates everything downstream — do this first.

**A2. Open the Singular account (free / self-serve); request SKAN network IDs from Meta \+ Google.** 🔴 Singular signup needs no credit card or sales call, so it clears same-day. The MMP SDK and the networks' `SKAdNetworkItems` IDs must be in the submitted `Info.plist` — networks won't attribute to a build lacking their IDs. **AppsFlyer** is the named backup if Singular's terms surprise at signup.

**A3. Instrument push delivery-rate by device OEM in Customer.io from day one.** 🟠 *The MoEngage trip-wire.* This is how we know whether the accepted India-Android risk (§1.4) is actually biting. Tag delivery/open by manufacturer (Xiaomi/Oppo/Vivo vs rest); if delivery on Chinese OEMs drops below tolerance, that's the signal to activate MoEngage Push Amplification Plus (D5). Cheap to add now, and it converts a guess into a threshold.

### B. Launch-blocking build (must be in the submitted binary)

**B1. Implement the locked SKAN 4 conversion-value schema (§C2).** 🔴 *The irreversible one.* Wire `updatePostbackConversionValue()` to the 6-tier "highest-value reached" ladder (install → onboarding → brief-open → brief-completed → push-opt-in/watchlist → registered) in the D0–D2 window; set brief-completion as the network optimization target. Skip it and all post-install iOS measurement is lost with no backfill.

**B2. Ship the ATT prompt** (`NSUserTrackingUsageDescription` in Info.plist \+ `AppTrackingTransparency`). 🔴 Can't be added server-side; without it, zero consented-user iOS data.

**B3. Integrate the Singular SDK** (iOS \+ Android), initialized on first launch; wire Singular Links for the deferred-deep-link \+ Customer.io email→app routing. 🔴

**B4. Integrate PostHog mobile SDK** as primary product analytics; define the core event taxonomy (the §12 metrics). 🔴 (SDK) / 🟠 (dashboards)

**B5. Integrate Firebase — Analytics \+ Crashlytics.** 🔴 *Both launch-blocking.* Google App Campaigns **are** in the launch mix (decision C1), so Firebase Analytics is the Google-ads optimization layer, not optional. Crashlytics \= the ≥99.5% crash-free tracking. Both in the launch binary.

**B6. Integrate the Customer.io RN SDK** with the notification spec (§8.5): local-time Morning Brief, grouped watchlist alerts, caps, quiet hours, deep-linking per type. 🔴 (SDK) Two build notes from §1.4: **grouped push** needs custom Android notification-channel/summary work (not an SDK setting); and the **Morning Brief edition-line push must not carry a daily rate-limit *or* A/B variants**, or local-time send silently reverts to fixed-UTC.

**B7. First-run DPDP consent/notice gate** in front of the tracking SDKs. ⚪ **DEFERRED (2026-07-07) with a note.** Skipped for the launch build — not legally required until DPDP enforcement (May 13 2027). *Note for later:* ship a lightweight first-run consent screen well ahead of that date to avoid a retrofit; full CMP \= D3. Revisit before Q1 2027\.

**B8. Implement the web↔app identity convention** — canonical `user_id` \= Inc42 auth user ID (per C3) `identify()`\-ed into all four SDKs across web \+ app auth. 🟠 Cheap now, enables later identity stitching; expensive to retrofit. (Owner per C3.)

**B9. Hand the build team the consolidated "must be in the submitted binary" list** (A1, A2, B1–B6, \+ the B8 anonymous-device-ID minting). 🔴 Because §9's "we can't hotfix" rule means any missing SDK/entitlement \= a resubmission cycle that blows the window. (B8's `identify()` wiring is server-side/config, but the anonymous-ID *minting on first open* is build-time — can't be assigned retroactively.)

### C. Decisions log (all resolved except C3 — the one open point)

**A7. Push vendor.** ✅ **RESOLVED (2026-07-07): Customer.io only at launch; MMP \= Singular.** MoEngage deferred to the D5 delivery-rate trip-wire. No longer a blocker for B6.

**C1. Ad networks at launch.** ✅ **RESOLVED (2026-07-07): Meta \+ Google** (Apple Search Ads not at launch). Consequences locked: Meta \+ Google SKAN IDs into `Info.plist` (A2); **Firebase Analytics is launch-blocking** (B5).

**C2. SKAN conversion-value schema.** ✅ **RESOLVED (2026-07-07).** Model \= **"highest-value tier reached"** (Apple writes the highest milestone hit in the D0–D2 window — no strict nesting, so it tolerates that registration is optional and non-linear):

| Fine value | Milestone |
| :---- | :---- |
| 0 | Install |
| 1 | Onboarding complete (role \+ sectors \+ watchlist) |
| 2 | Brief opened |
| 3 | **Brief completed** — the ad-optimization target |
| 4 | Push opt-in (or watchlist-add) — retention signal |
| 5 | Registered (optional; high value when it happens, sits at top) |

Both **brief-open (2) and brief-completion (3)** are on the ladder deliberately: point Meta/Google's optimization at completion, but because that event is rarer, if launch install volume falls below Apple's crowd-anonymity threshold and the fine value is suppressed, switch the network optimization target to open — a console change, **no rebuild** (the ladder is frozen at build time; the optimization target is not). A user who reads briefs but never registers correctly lands at 3–4. **Locked: rung 4 \= push opt-in** (watchlist-add is the fallback if push-opt-in proves too sparse). Engineering implements this exact ladder in B1 pre-submission.

**C3. Web↔app identity: name the eng owner.** 🟠 **Canonical `user_id` \= Inc42 auth user ID *once known*.** Registration is optional on the app, so most users never have one — for them the app mints **one anonymous device ID** on first open (a UUID in device storage) and passes *that* to all four SDKs (PostHog, Customer.io, Singular, Firebase) on both web and app. Not email, not per-SDK IDs. Anonymous users are still fully measurable and still **push-able** — Customer.io pushes to a device-token-only anonymous profile, so the Morning Brief does **not** require registration. **If/when a user registers, `identify()`/alias merges the anonymous ID → the Inc42 auth ID** so pre-registration history stitches forward (PostHog \+ Customer.io both support anon→known merge). Web↔app stitching only happens for users who log in on both surfaces; anon-web ↔ anon-app can't be linked, which is expected (the MMP still attributes the install regardless of login). This is a convention, not a feature, so it needs one named owner enforcing it across both codebases — recommend **app tech lead defines the spec, web team implements their half**. Confirm the owner; not binary-blocking, but the anonymous-ID minting must be in the launch build (can't be assigned retroactively) and it's cheapest to lock before either codebase ships tracking calls.

### D. Fast-follow (post-launch)

**D1. RudderStack CDP** (weeks 4–8) — reduce SDK sprawl \+ own identity resolution once volume/pain is real. ⚪ **D2. AdAttributionKit** alongside SKAN when re-engagement/3rd-party-store attribution matters. ⚪ **D3. Full consent-management platform (CMP)** ahead of the May 2027 DPDP enforcement date. ⚪ **D4. Sentry** if unified backend+app error/trace visibility becomes a need. ⚪ **D5. MoEngage (Push Amplification Plus)** — activate *if* the A3 delivery-rate trip-wire fires (Chinese-OEM delivery below tolerance). Pre-scoped fix, not a default. Enterprise sales-led onboarding (~~10-day lead) \+ MAU pricing (~~$5–6K/mo at 50–100K MAU), so start the conversation the moment the threshold trips, not before. ⚪

---

## Consolidated sources

Attribution/MMP: AppsFlyer, Kochava, Airbridge, Branch pricing pages; Singular MMP glossary; SKAN 4 schema (Aarki), SKAN 2026 (adlibrary); Play Install Referrer; Firebase Dynamic Links deprecation. Analytics: PostHog RN SDK \+ mobile replay; Firebase-for-UA (Addict, Lupu). Crash: Sentry-vs-Crashlytics (IndieAppStack), Shakebug 2026\. Push: Customer.io RN SDK \+ local-time; MoEngage Push Amplification \+ Amp+ impact; FCM/APNs setup; MoEngage (G2) \+ Customer.io pricing. CDP: RudderStack-vs-Segment (Volument). DPDP: Respectlytics, Secure Privacy. *(Inline links in each section above.)*

# App Store Submission Checklist

## Submission workstream (Ranjith \+ Animesh) — critical path

Submission is the longest-lead GTM item. Start **now** (T-9); everything in Phase 0 depends on approved builds.

### 2.1 Apple App Store

- [ ] App Store Connect listing: name, subtitle, keywords, description, screenshots, preview video — **blocked on the GTM copy pack (§7), which is currently unowned**  
- [ ] Privacy nutrition labels (declare PostHog, Singular, Customer.io, Firebase data types)  
- [ ] ATT prompt \+ purpose string (required — Singular attribution)  
- [ ] **Sign in with Apple** (Guideline 4.8 — mandatory since Google login is offered; launch-blocking build item)  
- [ ] In-app account deletion (mandate; already a v1 must-add)  
- [ ] Age rating questionnaire, export-compliance declaration  
- [ ] App Review notes \+ demo account (reviewer must reach the brief without a real Inc42 account)  
- [ ] TestFlight **external** testing build (its own beta review, \~24–48h) — needed for the founding-reader wave  
- [ ] Apple-safe copy sweep: no "Pro/Premium/Subscribe/₹" anywhere in binary or listing (locked constraint)  
- [ ] Submit for review with a **3–5 day buffer incl. one rejection cycle**  
- [ ] Apple **featuring nomination** via App Store Connect — submit at launch; realistic payoff is v1.1+ (6–18 months), zero cost to ask

### 2.2 Google Play

- [ ] Play Console listing (same copy-pack dependency)  
- [ ] Data-safety form (mirror the Apple nutrition labels)  
- [ ] Content rating questionnaire, target API level check  
- [ ] App signing \+ pre-launch report (run it — free device-lab crash pass)  
- [ ] **Staged rollout configured: 10% → 50% → 100%** (the Android release mechanism for Phases 1–2)  
- [ ] Play **pre-registration: skip** (decided — payoff doesn't justify setup for our timeline)

### 2.3 Cross-store gates before "Ready for sale"

- Task \#17 search reality-check **passed** (Ranjith \+ tech run internally — note shared)  
- Singular SKAN schema live \+ Meta/Google SKAN app IDs registered (Launch Infra A2/B1)  
- Crashlytics \+ PostHog \+ Customer.io verified on release builds (B4–B6)  
- Deep/universal links resolving (needed for Smart App Banner \+ push routing)

# Article Ranking Logic — Personalized Daily Brief

# **Article Ranking Logic — Personalized Daily Brief**

## **Inputs**

**From the user (2 signals):**

* **Followed Topics** — a set of Development\_Type categories  
* **Followed Sectors** — a set of parent sectors

**From each article:**

* Development\_Type → mapped to a behavioral topic name  
* Company\_Industries → mapped to a parent sector  
* Published timestamp

**Fixed data tables :**

* Topic popularity — *see definition below*  
* Sector popularity — *see definition below*

**Weights:** `W_topic = 1.0`, `W_sector = 0.6`, `W_pop = 0.15`

## **What "popularity" means**

Both are **audience-size measures** taken from the last-90-day co-read study — how many unique readers each category pulls, expressed on a 0–1 scale.

* **Topic popularity** \= the total unique readers of a topic (Development\_Type), divided by the readership of the single biggest topic. The biggest topic anchors the scale at 1.0 and everything else is a fraction of it. From your data: **News \= 1.000** (282,720 readers), Deals \= 0.759 (214,509 readers), Financials \= 0.252 (71,128 readers), Trends \= 0.164 (46,228 readers), Regulatory \= 0.123 (34,714 readers), IPO \= 0.116 (32,778 readers), Team \= 0.092 (25,903 readers), Startups \= 0.023 (6,630 readers).  
* **Sector popularity** \= the same thing for sectors — a sector's total unique readers divided by the biggest sector's readership. From your data: **Consumer \= 1.0** (121,253 readers), Fintech \= 0.75 (91,064), Ecommerce & D2C \= 0.69, DeepTech \= 0.64, Enterprise & SaaS \= 0.52, Startup Ecosystem \= 0.50, AI \= 0.23 (27,451).

In plain terms: popularity is *"how widely read is this kind of story, across all users."* It's a **crowd-level prior**, independent of the individual — it captures broad importance so that (a) a no-preference user gets the generally-most-read stories first, and (b) among articles that tie on personal relevance, the one in a more-read category edges ahead. It is normalized only so it sits on the same 0–1 scale as the affinity terms and can be blended with a small weight.

## **Score**

TopicAff  \= 1.0                              if article's topic ∈ followed topics  
          \= max( affinity\[t → article's topic\] for t in followed topics )   otherwise  
          \= 0                                if user set no topics, or article has no topic

SectorAff \= Σ (ParentMultiplier × ParentAffinity)

where, for each unique parent sector represented in the article:

ParentAffinity \= 1.0                         if parent sector ∈ followed sectors  
               \= max( affinity\[s → parent sector\] for s in followed sectors ) otherwise  
               \= 0                           if user set no sectors

ParentMultiplier \= 1                         if only one unique parent sector is represented  
                 \= number of unique parent sectors represented in the article, if more than one

Pop       \= ½ · topicPopularity \+ ½ · sectorPopularity

score     \= 1.0·TopicAff \+ 0.6·SectorAff \+ 0.15·Pop

## **Ranking (per day)**

Sort the day's articles by the key below, top to bottom:

1\.  score              (higher first)  
2\.  published\_time      (more recent first)

## **Tie-breaker logic**

Because `score` is a pure function of (topic, sector) for a given user, two articles with the same topic **and** the same sector always score identically. Ties resolve in strict order:

1. **Score** — the primary sort. Distinct scores never tie.  
2. **Recency** — if scores are equal, the newer article ranks higher. This is the meaningful tie-breaker and resolves the vast majority of same-score cases, since two articles wont share an exact publish time.

## **Editorial Override**

**Editorial Override**

The editorial team can assign an optional **App Featured Article** flag (`Yes`/`No`) to any article. If no value is selected, it is treated as **No** by default.

* **Yes:** The article overrides all ranking rules and is placed before all non-editorial articles. Score, affinity, popularity, and all other ranking rules are ignored.  
* **No (or not selected):** The article follows the standard ranking logic.

If multiple articles have **App Featured Article \= Yes**, they are ranked by **published\_time** (more recent first). After all editorially prioritized articles are placed, the remaining articles are ranked using the standard scoring logic.

**Sector Category Map** (parent category → child sectors)

**Ecommerce & D2C** \--\> Ecommerce, D2C, Logistics

**Consumer** \--\> Consumer Services, Foodtech, Media & Entertainment, Travel Tech, Edtech, Health Tech, Agritech

**Fintech** \--\> Fintech, Cryptocurrency, Digital Brokerage, Insurance Aggregators & Comparison Platform, Web3

**Enterprise & SaaS** \--\> Enterprise Services, Enterprise Tech, Cybersecurity, Real Estate Tech

**AI** \--\> AI, AI Governance

**DeepTech** \--\> Clean Tech / Climate Tech, Space Tech, Semiconductors, Advanced Hardware & Technology, Manufacturing Solutions, Electric Vehicles

**Startup Ecosystem** \--\> Startup Ecosystem

**Dev Tags Map** (parent category → child dev tags)

**News \--\>** Business Updates, Cohort Launches, Controversies

**Deals \--\>** Startup Funding & Investments, Fund Launches, Startup Mergers & Acquisitions

**Trends \--\>** Industry Trends, Business Models & Strategy

**IPO \--\>** Startup IPO

**Regulatory \--\>** Government & Policies

**Team \--\>** People & Culture, Startup Layoffs

**Startups \--\>** Startup Discovery

**Financials \--\>** Startup Financials 

## **Edge cases (all handled by the same formula)**

| Situation | Behavior |
| ----- | ----- |
| User set only sectors | `TopicAff = 0` for all → ranks on sector \+ popularity |
| User set only topics | `SectorAff = 0` for all → ranks on topic \+ popularity |
| User set neither | both affinities 0 → ranks on **popularity**, then recency |
| Article has no Development\_Type | `TopicAff = 0`, still ranked via sector \+ popularity |
| Article has no industry | `SectorAff = 0`, still ranked via topic \+ popularity |
| Article matches nothing | low score, sits in the tail by popularity/recency — still shown |
| Followed category absent that day | no effect; other articles rank normally |
| Article has multiple child tags from the same parent  | Count the parent only once. Multiple child tags that map to the same parent do not increase the affinity contribution (multiplier \= **1**).  |
| Article has child tags from multiple different parents  | Calculate the affinity for each unique parent and multiply that component by the number of unique parent categories represented. For example, if the article maps to **2** unique parent categories, the corresponding affinity contribution is multiplied by **2**; if it maps to **3** parents, it is multiplied by **3**.  |

# Streak and Rewards

# **Streak & Rewards**

## **1\. Objective**

The streak system exists to **reward users and give them a sense of gratification for consistently completing briefs.**

* The behaviour we want to reward is **consistency** (coming back and completing a brief each day).  
* The gratification we give in return is **rewards and badges**, unlocked as the streak grows.

---

## **2\. Key Definitions**

| Term | Meaning |
| ----- | ----- |
| **Brief** | The daily piece of content / task a user completes. |
| **Completion (Active day)** | A day counts as "active" the moment the user completes **at least one** brief that day. |
| **Streak** | The number of **consecutive calendar days** on which the user has completed at least one brief. |
| **Milestone** | A specific streak day-count (e.g. Day 1, Day 7…) that unlocks a reward and/or badge. |
| **Reader Level**  | User progression tied to milestone days: **Day 1 → Reader**, **Day 7 → Regular**, **Day 30 → Insider**, **Day 100 → Ecosystem Native**. Levels are unlocked once at their respective milestones.  |

---

## **3\. How the Streak Works — Core Rules**

**Rule 1 — One count per day (no matter how many times they complete).** Completing a brief moves the streak forward by exactly **\+1 for that calendar day**. It does not matter how many briefs the user finishes, or how many times they open the app that day — the streak increases by **1 per day only**.

**Rule 2 — Consecutive days continue the streak.** If the user was active yesterday and is active again today, today's count \= yesterday's count \+ 1\. The streak keeps growing as long as there are no gaps.

**Rule 3 — A missed day breaks the streak → resets to 0\.** If a full calendar day passes with **no completed brief**, the streak is broken and the counter resets to **0**.

**Rule 4 — Restart from 1\.** After a reset, the next time the user completes a brief, the streak begins again from **1** as a brand-new streak.

> **Current-day clarification (for implementation):** The streak stays "alive" as long as the user completes a brief either **today or yesterday**. The break only registers once a full calendar day ends with no completion — at that point the counter shows **0** until the user completes a brief again.

---

## **5\. Rewards Logic**

Currently, we will display series of logos blurred and coming soon on top of that:

---

## **6\. Badges (from the current design)**

Badges follow the same one-time, milestone-based logic as rewards. Once unlocked they are **permanent**. A badge is earned only once and cannot be re-earned.

* If the streak resets and the user climbs back to a badge day they already have, the badge is not re-awarded.

---

## **7\. Calendar View**

The calendar gives the user a visual month-by-month record of their activity.

**States shown on each date:**

| State | How it's shown | Meaning |
| ----- | ----- | ----- |
| **Active** | Marked (red / filled indicator) | User completed a brief that day. |
| **Today** | Outlined marker | The current date. |
| **Missed / inactive** | Greyed / unmarked (as per design) | No brief completed that day. |

**Behaviour:**

* A date is marked **Active as soon as** the user completes their first brief on that day.  
* Missed days remain unmarked, visually showing where the streak broke.  
* The calendar also surfaces a **monthly summary**: the count of active days this month and the **% of days active** in the month.  
1. 

# App PRD Final

# Inc42 App — v1 Product Requirements (Unified)

**Owner**: Utkarsh · **Updated**: 2026-06-21 · **Status**: canonical — single source of truth for v1.

> **How to use this doc.** This is the **one** reference the team builds v1 from. It supersedes the older per-surface PRDs (`brief-prd.md`, `explore-prd.md`, `watchlist-prd.md`, `entity-profile-prd.md`, `misc-features-prd.md`) and the concept docs — those are retained only as deep-reference for backend depth, linked inline. Where anything conflicts, **this doc wins.** Changelog at the end (§14).

---

## 1\. The product in one page

**Inc42** is India's startup-intelligence company — investigative journalism \+ proprietary Datalabs data \+ the ecosystem's network. The app is its **daily intelligence habit**: *"Not a newsletter. Not an algorithm. Inc42's journalism, Datalabs intelligence, and AI that explains what it means for you. One app, every morning. Then it ends."*

**The shape of v1:**

- **Brief** — a finite, personalized morning brief that *ends* (the habit anchor).  
- **Explore** — the 12-year archive (\~30K+ articles) \+ the Datalabs company graph (70K+) on pull.  
- **Watchlist** — the things you track \+ their movements (the wedge \+ the Datalabs on-ramp).  
- **Company profiles** — glanceable Datalabs depth, the bridge from journalism into data.

**Audience (ICPs):** Founder · Investor · Startup Operator · BD & Partnerships · (Other). Personalization is by ICP \+ sectors \+ watchlist.

**Operating constraint (native app):** unlike the website, we can't hotfix — users must update, and App Store review adds latency. So: **everything tunable lives in server-side remote config** (caps, cadence, ranking, copy, taxonomy, flags); a **force-update / min-version gate** ships in v1; and features ship as **coherent, ordered bundles** (§11).

### Design principles (guardrails)

1. **Finite before infinite** — opens to the Brief; ends with a "Done for today" endpoint; no feed continuation.  
2. **Depth on demand** — headline → Decode → full article → entity profile, each by choice.  
3. **Watchlist is the personalization engine, not an algorithm** — explicit choices, no behavioral feed.  
4. **Shown, not narrated** — visible "relevant because…" attribution; no covert personalization.  
5. **Signal-dense cards, not image-forward** — the audience scans for signal.  
6. **The reader earns its place** — must beat inc42.com mobile (faster, focused, progress, bookmark).  
7. **Everything is Inc42** — no external aggregation.

---

## 2\. Information architecture

**3 bottom tabs — Brief · Explore · Watchlist.** Plus two persistent top-bar affordances: a **global 🔍 search** and an **account avatar**. Neither is a tab. **No hamburger / drawer.**

```
┌───────────────────────────────────┐
│  Inc42            🔍        ( U )  │ ← global search + account avatar (every screen)
│                                   │
│            [ active surface ]     │
│                                   │
├───────────────────────────────────┤
│    ● Brief     Explore   Watchlist│ ← 3 tabs
└───────────────────────────────────┘
```

- **Article reader** \= a full-screen modal from any surface (not a tab).  
- **Company profile** \= the shared tap-target (not a tab).  
- **Ask Inc42** \= a *mode*, not a tab (dormant in v1; §8.2).

---

## 3\. Onboarding & auth

**Seed flow (5 quick screens):** welcome → **role/ICP** → **sectors** (the 17, pick ≤5) → **watchlist seeds** (≥1 required, 3 recommended, skip-with-friction; role×interest suggestions) → success. Onboarding state is offline-tolerant, synced on auth.

```
ONBOARDING — 5 steps (~45–75s)
[1 Welcome] → [2 Role] → [3 Categories] → [4 Topics] → [5 Sign in]

2 Role:       ○ Founder  ○ Investor  ○ Operator  ○ BD  ○ Other
3 Categories: pick ≤3  (parent-only select; children shown, not tappable)
      ☐ Consumer & Commerce   Ecommerce · Foodtech · Consumer Services · Media & Ent. · Travel Tech
      ☐ Fintech & Web3        Fintech · Web3
      ☐ Enterprise & SaaS     Enterprise Tech · Enterprise Services
      ☐ DeepTech & AI         AI · Advanced Hardware & Technology
      ☐ Industrials & Infra   Logistics · Clean Tech · Agritech · Real Estate Tech
      ☐ Health & Learning     Health Tech · Edtech
4 Topics:     pick ≥1 (3 recommended)                             [Skip ▸]
      [Business Intelligence] [Funding] [Controversies] [IPO] [Trending]
      [Policies] [People] [M&A] [Financials] [New Funds]
5 Sign in:    Continue with Google · Continue with Apple · email

```

**Auth:** anonymous use is allowed. A **soft sign-in sheet** triggers only on a gated action (Follow · \~5 profile views · 3rd Saved item). It completes the pending action and **merges anon local data** (saves, seeds). "Continue without account" stays available; cross-device sync needs an account.

---

## 4\. Brief (the hero)

> **Reference prototype** (interactive, all 4 ICPs): `prototype-2026-06-10.html` — [https://drive.google.com/file/d/1naa66aU5CdQVcp3cjOvRDuNxlsGxyMs8/view](https://drive.google.com/file/d/1naa66aU5CdQVcp3cjOvRDuNxlsGxyMs8/view). The prototype is the reference implementation of this model; these wireframes are the spec.

A finite, relevance-ranked set of 6–8 cards that ends. Mon–Fri daily \+ Sat weekly recap \+ Sun off. Pushed \~7–8 AM local. Editorial cards \+ Datalabs signal cards, ranked most-relevant-to-you first. No sections — a single ranked sequence (decision 2026-06-21); signal-type tags carry type orientation per card.

**Cover, then cards.** The Brief opens on a cover screen, not the stack: greeting · streak · day-strip · a one-line summary of the day · focus chips · "Open Today's Brief." Tapping in enters the card sequence. Cover copy \+ layout is still to be decided; the summary line can be AI-generated.

**Full-screen swipe cards.** Inside the Brief, cards are full-screen and advanced by swipe (swipe up → next story), one card at a time — not a scroll-stack of collapsed tail cards. Each card is image-optional, signal-dense, and routes to the full article.

- COVER (TBD — copy/layout not final)          CARD (full-screen, swipe up \= next)  
- ┌───────────────────────────────┐            ┌───────────────────────────────┐  
- │ Good Morning        🔥12  (U)  │            │ ‹ Today's Brief    Tue 24 Jun │  
- │ S S M \[T\] W T F   ← day-strip  │            │ ▓▓▓░░░░░  ← progress           │  
- │ ─────────────────────────────  │            │ \[image — optional\]             │  
- │ \[one-line summary of the day\]  │ ← AI-gen   │ ■ Breaking · Fintech    ⭐ 🎯  │  
- │ 8 stories · \~5 min             │            │ Razorpay bags $75M Series G    │  
- │ Sectors in focus:              │            │ • What's new …                 │  
- │ \[Funding\]\[AI\]\[Policy\] \+2       │            │ • Why it matters …             │  
- │ \[ Open Today's Brief    → \]    │            │ • Detail …                     │  
- └───────────────────────────────┘            │ Relevant because you track     │  
-                                               │ Razorpay                       │  
-                                               │ Read full story →              │  
-                                               │ ↑ Swipe up for the next story  │  
                                                └───────────────────────────────┘

Card anatomy: signal-type tag (`▣ Funding / ◈ New Funds / ⇄ M&A / ▲ IPO / ◆ People / ✕ Startup Layoffs / ◉ Trending / ⬡ Cohort Launches / ⬢ Startup Discovery / ⚠ Controversies / ■ Business Intelligence / ⬚ Business Models & Strategy / ₹ Financials / § Policies)`

) · headline · Smart Brevity body (3-bullet editorial, or deterministic funding one-liner) · ⭐ if it's a watchlist hit · 🎯 relevance chip \+ a "relevant because…" label · Read-full-story route. (Decode removed from v1 scope.)

Editorial governance: summarize-once at \~3 AM → 3-tier validation → editorial approve gate (\~6–7 AM) → app pulls. (Full pipeline \+ cost envelope: brief-prd.md.)

**Streak.** A consecutive-day engagement counter shown on the cover and at completion. Minimal in v1 — mechanics (what counts as a day, grace/reset, timezone) TBD; treat as display-only until defined.

**4.1 Card states (zoomed)**

- EDITORIAL CARD — full-screen (3-bullet Smart Brevity)   FUNDING / DATALABS SIGNAL CARD (deterministic, no LLM)  
- ┌───────────────────────────────────┐                  ┌───────────────────────────────────┐  
- │ ■ Breaking · Fintech     ⭐  🎯    │                  │ ▣ Funding · Agritech        🎯     │  
- │ Razorpay bags $75M Series G        │                  │ DeHaat · Series F                  │  
- │ • What's new: closed $75M led by   │                  │ $60M · Jun 2026 · led by \[Inv\]     │  
- │   \[Investor\] at \~$9B.              │                  │ Total raised $200M · HQ Patna      │  
- │ • Why it matters: extends payments │ ← bullet-2:      │ Relevant because you follow Agritech│  
- │   lead as TPV scales.              │   auto in v1,    │ ⬛ View company →                   │  
- │ • Detail: funds lending \+ intl.    │   human-edit v1.1│ Read full story →                  │  
- │ Relevant because you track Razorpay│                  └───────────────────────────────────┘  
- │ Read full story →                  │  
- │ ↑ Swipe up for the next story      │  
  └───────────────────────────────────┘

**4.2 Completion, slow-day & weekly states**

- DONE FOR TODAY (endpoint \+ streak)     SLOW NEWS DAY (content-scarcity fallback)   SATURDAY "THIS WEEK"  
- ┌──────────────────────────┐          ┌──────────────────────────┐               ┌──────────────────────────┐  
- │      🔥 12 Day Streak     │          │ Quieter day in the        │               │  This week  ▓▓▓░░         │  
- │      Done for today       │          │ ecosystem.                │               │ Same finite set — the     │  
- │  Caught up — 8 stories.   │          │ Today's 4 developments \+  │               │ week's biggest movements  │  
- │  ⭐ 3 from your watchlist  │          │ 2 evergreen reads for you.│               │ instead of the day's.     │  
- │  Back tomorrow \~7:30 AM.   │          │ (rule: ≥4 editorial \+ ≥2  │               │ Same cards, endpoint.     │  
- │  \[ Continue with Explore \]│          │ signals, else backfill —  │               │ Sun \= off.                │  
- │  (no feed continuation)   │          │ never a 2-line digest)    │               └──────────────────────────┘  
  └──────────────────────────┘          └──────────────────────────┘

Completion state carries the streak (minimal, per above) and routes to Explore rather than continuing a feed. Completion \= reaches final card OR opens ≥60% of cards OR min reading time (§8.5).

**4.3 Relevance (how the brief ranks — summary)**

Full logic \+ tier tables \+ tie-breaks live in the ranking sheet: [Unified App Concept](https://docs.google.com/document/d/1eT472QdzWOg_ChvvmoO3cX5CnL2sqToR5jU8-GvMxzw/edit?tab=t.gjwukq86vny4)  This is the summary; where they differ, the sheet wins.

The brief content set is identical for all users; relevance changes ranking \+ labels only, not which content exists (no filter bubble; editorial keeps control).

Final Score \= Editorial Importance (base) \+ Personal Relevance (boost).

* **Editorial Importance (EI)** — a 5-tier significance scale (Tier 1 ecosystem-defining → Tier 5 niche), each tier mapping to a configurable default score (50/40/30/20/10). Fine-grained within-tier ordering is handled by the separate scoring layer. Keeps major stories high for everyone.  
* **Personal Relevance boost \= Wₑ·(entity matches) \+ Wₜ·(topic matches) \+ Wₛ·(sector matches).** Entity outweighs topic outweighs sector (Wₑ \> Wₜ \> Wₛ; starting config 25/20/15). Topics are a live v1 ranking signal (from onboarding step 4).  
* **Full-Match Primacy** — a story matching *every* signal the user provided is promoted above all others, ordered within that priority group by total Personal Relevance. Applies to any user with ≥1 signal.  
* **Editorial Pin** — the day's highest-EI story is guaranteed a top-3 slot, even against the full-match group.  
* **"Relevant because…" label** appears only when the boost lifted the card (Boost \= Final Score − EI \> 0); entity reason shown over sector when both match.  
* **Cold-start** — apply whichever signals exist; unset signals contribute zero. Skipped onboarding → EI only (the standard editorial brief).  
* Weights \+ pin position \+ label threshold are server-side, remote-config tunable, validated on a \~2-week concierge backtest before they lock. Structure locked here; numbers lock after data.

v1 \= ranking \+ labels only. Per-ICP lead-sentences \+ per-article-type ordering \+ section-level summaries → v1.1 Emphasis Layer.

- 

---

## 5\. Explore

The archive \+ company graph, on pull. Not a discovery feed (the Brief owns "today").

Layout: search bar → content switch (Articles | Companies) → in-tab pill strip \+ filter button → feed 

Each tab (Articles, Companies) has a horizontal pill strip for quick slices and a dedicated filter button opening a bottom-sheet for deeper filtering. The bottom sheet also opens on overscroll — swiping past the end of the pill strip triggers it (the filter button is the primary, always-visible affordance; overscroll is a shortcut).

**Articles** — pill strip (single horizontal group): Latest · Funding · Controversies · Trending · Policies · In-depth · Startup Stories.

Articles filter sheet (multi-select within each group):

* **Sort by:** Latest · Trending  
* **Published:** Anytime · Today · This Week · This Month  
* **Development type:** the 10-type spine (Funding · New Funds · M\&A · IPO · People · Startup Layoffs · Trending · Cohort Launches · Startup Discovery · Controversies · Business Intelligence · Business Models & Strategy · Financials · Policies · In-depth · Startup Stories.)

Article card \= thumbnail · \[signal-type\] chip · \[sector→\] chip · headline · byline · age · 🔖.

**Companies** — pill strip: Recently Funded · IPO-bound · Just Launched · Early Fundraisers · Unicorn Startups  · Tracked. List rows (not a grid).

Companies filter sheet (multi-select within each group):

* **Sector (the 17):** Fintech · Edtech · Ecommerce · Health Tech · Enterprise Tech · Enterprise Services · Media & Entertainment · Advanced Hardware & Technology · Consumer Services · Clean Tech · Real Estate Tech · Travel Tech · AI · Logistics · Agritech · Foodtech · Web3  
* **Stage:** Bridge · Early · Growth · Late · Undisclosed · Bootstrapped  
* **Sort by:** Total Funding (High→Low) · Founding Year (Recent First) · Founding Year (Oldest First) · Headcount Change (High→Low) · Headcount Change (Low→High) · Web Traffic (High→Low) · Web Traffic (Low→High)

Company card \= logo · name · \[status\] · \[sector→\] · \[stage\] · last round \+ total raised · HQ \+ employee band · \[Track\].  

**Today's Datalabs signals** — collapsed rail: top 3–5 market aggregates (funding/deals/sector flows/hiring). The only daily-fresh element here.

```
EXPLORE — ARTICLES                          EXPLORE — COMPANIES
┌───────────────────────────────────┐       ┌───────────────────────────────────┐
│  🌐 Explore      🔍   🔥12   ( U ) │       │  🌐 Explore      🔍   🔥12   ( U ) │
│  🔍 Search Inc42 & Datalabs        │       │  🔍 Search Inc42 & Datalabs        │
│ ┌─────────┬─────────────────────┐  │       │ ┌─────────┬─────────────────────┐  │
│ │ ARTICLES│      Companies      │  │       │ │ Articles│      COMPANIES      │  │
│ └─────────┴─────────────────────┘  │       │ └─────────┴─────────────────────┘  │
│ ‹ Latest Funding IPO Trending … ⚲ │       │ ‹ Recently IPO-bound Just… ⚲ │
│   └──── overscroll ⟶ opens ⚲ ────┘ │       │   └──── overscroll ⟶ opens ⚲ ────┘ │
│ ┌──┐ ▣ Funding · Fintech      🔖  │       │ ⬛ Razorpay            ● Active    │
│ │IM│ Razorpay bags $75M Series G  │       │  Fintech · Payments   Growth      │
│ └──┘ Inc42 · 3h                   │       │  $75M · Jun26 · $1.4B total       │
│ ┌──┐ § Policy · Ecommerce     🔖  │       │  Bengaluru · 1k–5k        [ ✓ ]   │
│ │IM│ RBI tightens PA norms        │       │ ─────────────────────────────────  │
│ └──┘ Inc42 · 1d                   │       │ ⬛ Mensa Brands        ● Active    │
│ ┌──┐ ▲ IPO · Consumer         🔖  │       │  Ecommerce            Late        │
│ │IM│ Zomato files updated DRHP    │       │  $50M · Mar26 · $300M total       │
│ └──┘ Inc42 · 2d                   │       │  Bengaluru · 501–1k       [ + ]   │
│         … (20 / page)             │       │         … (20 / page)             │
│ ── Recently viewed ──             │       │ ── Recently viewed ──             │
└───────────────────────────────────┘       └───────────────────────────────────┘
   ⚲ = filter button (always visible)          ⚲ = filter button (always visible)
   overscroll past strip end = same sheet       overscroll past strip end = same sheet


ARTICLES FILTER (bottom sheet · multi-select)   COMPANIES FILTER (bottom sheet · multi-select)
┌───────────────────────────────────┐       ┌───────────────────────────────────┐
│ ══                                 │       │ ══                                 │
│ Filter Articles                 ✕  │       │ Filter Companies                ✕  │
│ ───────────────────────────────── │       │ ───────────────────────────────── │
│ Sort by                            │       │ Sector                             │
│ [ Latest ] [ Trending ]            │       │ [Fintech][Edtech][Ecommerce]       │
│ Published                          │       │ [Health Tech][Enterprise Tech]     │
│ [Anytime][Today][This Week]        │       │ [Enterprise Services][AI][Web3]    │
│ [This Month]                       │       │ [Media & Ent.][Consumer Services]  │
│ Development type                   │       │ [Adv. Hardware & Tech][Clean Tech] │
│ [Funding][Fund Launch][M&A][IPO]   │       │ [Real Estate Tech][Travel Tech]    │
│ [People][Controversy][Policy]      │       │ [Logistics][Agritech][Foodtech]    │
│ [Financials][Business]             │       │ Stage                              │
│ Categories                         │       │ [Bridge][Early][Growth][Late]      │
│ [Consumer & Commerce]              │       │ [Undisclosed][Bootstrapped]        │
│ [Fintech & Web3][Enterprise & SaaS]│       │ Sort by                            │
│ [DeepTech & AI][Industrials&Infra] │       │ [Total Funding: High→Low]          │
│ [Health & Learning]                │       │ [Founding Year: Recent First]      │
│ ───────────────────────────────── │       │ [Founding Year: Oldest First]      │
│ [   Reset   ]      [   Apply   ]   │       │ [Headcount Change: High→Low]       │
└───────────────────────────────────┘       │ [Headcount Change: Low→High]       │
                                             │ [Web Traffic: High→Low]            │
                                             │ [Web Traffic: Low→High]            │
                                             │ ───────────────────────────────── │
                                             │ [   Reset   ]      [   Apply   ]   │
                                             └───────────────────────────────────┘

```

### 5.1 Sector landing (the industry-tag destination)

```
┌──────────────────────────┐
│ ‹ Explore   🔍    ( U )  │
│ Fintech         [+ Track]│
│ ₹4,200 Cr · 38 deals/30d │
│ ┌────────┬─────────────┐ │
│ │ARTICLES│  Companies  │ │ ← locked to Fintech
│ └────────┴─────────────┘ │
│ ■ Razorpay $75M…     3h  │
│ ▤ UPI's next act…    4d  │
│        …                 │
└──────────────────────────┘
```

Any industry tap (card chip, in-article tag, Articles industry pill, Companies "By Sector", search chip) → **Explore scoped to that one sector**: Articles-in-sector \+ Companies-in-sector \+ a `[+ Track sector]` button. Not a heavy dashboard.

**The 17 canonical sectors** (shared `tag_industry` / `company_sector` spine; sub-sectors/colloquial terms alias up): Fintech · Edtech · Ecommerce · Health Tech · Enterprise Tech · Enterprise Services · Media & Entertainment · Advanced Hardware & Technology · Consumer Services · Clean Tech · Real Estate Tech · Travel Tech · AI · Logistics · Agritech · Foodtech · Web3.

---

## 6\. Watchlist

The **Following \+ Saved** surface — the standing set of what you track \+ what you keep. Two sub-tabs:

```
┌───────────────────────────────────┐
│  Watchlist     🔍        ( U )     │
│ ┌──────────────┬────────────────┐ │
│ │  TRACKING    │     Saved      │ │
│ └──────────────┴────────────────┘ │
│  Following (8)         [+ Add]    │
│  ── COMPANIES ──                  │
│  [M] Meesho   Series G · 14 alerts│ → company profile
│  [Z] Zepto    Series F · 6 alerts │
│  ── SECTORS ──                    │
│  # Fintech            · 9 alerts  │ → Sector landing
│  ── RECENT ALERTS ──              │
│  · Meesho: $275M raise        2h  │
│  · Fintech: RBI norms         1d  │
│  See all (90-day) →               │
└───────────────────────────────────┘
```

- **Track only Companies \+ Sectors** in v1 (people/funds need profiles, which are v1.1+). Free caps **\~15 companies \+ 5 sectors**; hitting a cap → soft "more depth coming — notify me," never a hard wall.  
- **Track from anywhere** (one tap): Brief cards, Explore rows, search, in-article tags, profile `[+ Track]`. `[+ Add]` \= Datalabs search-as-you-type.  
- **Recent Alerts** \= the in-app ledger of all tracked-entity movements (pushed \+ un-pushed); last 20 in view, "See all" → 90-day rolling.  
- **Saved** sub-tab absorbs bookmarks (one-tap 🔖 from cards / reader). Recency-sorted, flat. Anon \= local (cap 50), merged on sign-in.  
- **Monetization on-ramp dormant** — cap hits \+ 🔒 depth show "coming soon" capture; no "Pro/Plus/Subscribe/₹" wording.

```
SAVED sub-tab                         EMPTY — TRACKING                 EMPTY — SAVED
┌──────────────────────────┐         ┌──────────────────────────┐    ┌──────────────────────────┐
│ ┌─────────┬───────────┐  │         │ Track what matters to     │    │ Stories you save show up  │
│ │Tracking │   SAVED   │  │         │ your day.                 │    │ here.                     │
│ └─────────┴───────────┘  │         │ [+ Add]                   │    │ Tap 🔖 on any story.      │
│ Saved (14)               │         │ Suggested:                │    │                           │
│ Why India's OTT… · May14 │         │  [+ Meesho] [+ Fintech]   │    │                           │
│ 📊 State of Fintech·May12│         │  [+ Zepto]  [+ AI]        │    │                           │
│  … (recency, flat)       │         └──────────────────────────┘    └──────────────────────────┘
└──────────────────────────┘
```

---

## 7\. Company entity profile

The page you land on when you tap a company anywhere. A **glanceable consumption view** of existing Datalabs data — **company profiles only in v1** (investor \+ person deferred to v1.1/v1.2+, investor first; so person/fund search → coverage).

```
┌─────────────────────────────────────┐
│  ‹          [ + Follow ]        ⋯    │
│  ⬛ COMPANY NAME                      │
│  Sector · Sub-sector · HQ            │
│  Founded YYYY · Active · ↗ website    │
│  ┌ Funding ──────────────────────┐   │
│  │ $XXM total · Latest: Series B  │   │
│  │ $25M · Mar'26 · Key inv: A,B,C │   │
│  └────────────────────────────────┘   │
│  ┌ People ───────────────────────┐   │
│  │ Founder — CEO · Founder — CTO  │   │
│  └────────────────────────────────┘   │
│  ┌ On Inc42 ─────────────────────┐   │ ← journalism tie-back
│  │ • [Headline] 3d · [Headline]2w │   │
│  └────────────────────────────────┘   │
│  [ Ask about COMPANY ]  (dormant)     │
└─────────────────────────────────────┘
```

Order: **Header → Funding → People → On Inc42 → Ask-stub.**

- **Free (shown):** identity, sector/stage, HQ, founded, status, total raised, latest round, key investors, founders \+ key CXOs, employee band, recent Inc42 coverage, one signal stat.  
- **Reserved (🔒, omitted — not teased):** full funding history, cap table, MCA financials, valuation history, charts, comparisons. *(Field-level map: `premium-boundaries.md`.)*

---

## 8\. Cross-cutting surfaces

### 8.1 Global search

Top-bar 🔍 opens the one Explore overlay from any screen; opening from an entity pre-seeds the query. (Detail §5.)

### 8.2 Decode & Ask

- **Decode (✨)** — live v1, soft-capped, non-blocking (§4).  
- **Ask Inc42** — a **mode, not a tab**. Open-ended chat deferred to v1.1; two **dormant stubs** keep us ready: "Ask the archive" in search, "Ask about \[entity\]" on profiles. No live LLM call in v1.

### 8.3 Article reader

Full-screen modal from any surface. Header 🔖 → Watchlist Saved. In-article entity tags → company profile; sector tags → Sector landing. Dismiss returns to origin.

```
ARTICLE READER (modal, slides up)
┌──────────────────────────┐
│ ✕              🔖    ↗   │ ← close · save(→Saved) · share
│ Razorpay bags $75M Series G│
│ By [Author] · Inc42 · 3h  │
│ ▓▓▓▓░░░░  (read progress) │
│ [focus-mode body, no nav  │
│  chrome; entity tags →    │
│  profile, sector → landing]│
│ ── Related on Inc42 ──    │
│ • [Headline] • [Headline] │
└──────────────────────────┘
```

### 8.4 Account (avatar)

Top-right avatar: **Preferences** (role · sectors (17) · push alerts · brief time) \+ **Account** (email · sign out · **Delete account & data**). Editable role/sectors. No subscription/billing UI in v1.

```
┌──────────────────────────┐
│ [U] Utkarsh · Founder     │
│     Fintech, Ecommerce    │
│ ── PREFERENCES ──         │
│ My role        Founder ▸  │
│ My sectors   Fintech… ▸   │
│ Push alerts        On ▸   │
│ Brief time    7:30 AM ▸   │
│ ── ACCOUNT ──             │
│ utkarsh@inc42.com         │
│ Sign out                  │
│ Delete account & data    │ ← Apple requirement
└──────────────────────────┘
```

### 8.5 Notifications (merged model — LOCKED 2026-06-21)

| \# | Push | Cadence | Trigger |
| :---- | :---- | :---- | :---- |
| 1 | **Morning Brief** | 1×/day, \~7–8 AM **local** | The daily drop |
| 2 | **Brief completion nudge** | ≤1 same-day, **non-openers/incompletes only**, stops on completion | Brief state machine |
| 3 | **Breaking** | ≤1×/day | **Manual / editorial** (not algorithmic) |
| 4 | **Watchlist alerts** | **Real-time, grouped** | Per-entity event, **significance-gated** |
| 5 | **Winback** | ≤1×/week, lapsed only | Scheduler |

**Rules:**

- **Significance gating** (fatigue firewall): only funding / M\&A / leadership / major policy / marquee coverage push; routine mentions → **ledger only**.  
- **Grouping** ("3 updates in your watchlist") · **per-category caps** (Watchlist ≤\~3/day, then collapse) · **per-entity mute** · **per-category opt-out**.  
- **Quiet hours 10 PM–7 AM local** (queued → morning).  
- **Brief completion** \= reaches final card OR opens ≥60% of cards OR min reading time (success \= *completion*, not open).  
- **Curiosity-gap alert copy** ("New update on \[Company\]" — establish relevance, don't satisfy curiosity in the banner).  
- **Deep-linking** per type · **badge** \= unread Watchlist alerts · **permission-denied fallback** (app fully works; re-ask ≤2×, only after a value moment).  
- **Tier ladder:** Free \= real-time alerts on standard events · **Plus** (v1.1) \= custom triggers · **Pro** (v1.1+) \= Datalabs-grade signal alerts \+ rule-builder. The real-time **Signal layer is in v1** — size the build for it.

```
SIGN-IN SHEET (soft, on a gated action)   PUSH PERMISSION (after first brief)   PUSH EXAMPLES (curiosity-gap; copy A/B'd at build)
┌──────────────────────────┐             ┌──────────────────────────┐          Inc42·now  Your Brief is ready.
│ Save to your account?     │             │ Tomorrow's Brief at 7:30? │          Inc42·now  New update on Razorpay.      ← watchlist (single)
│ Keep saves + follows on   │             │ + alerts when tracked     │          Inc42·now  3 updates in your watchlist. ← grouped (≥2)
│ every device.             │             │ companies move.           │          Inc42·now  Big move in the ecosystem.   ← breaking
│ [ Continue with Google ]  │             │ [ Turn on notifications ] │          Inc42·11:30 You haven't seen today's    ← completion nudge
│ [ Continue with email ]   │             │ [ Not now ]               │                     Brief yet.   (non-openers only)
│ Continue without account  │             │ (asked once value shown)  │
└──────────────────────────┘             └──────────────────────────┘
```

### 8.6 Monetization (dormant, Apple-safe)

v1 \= Free tier only. Plus/Pro reserved in code (feature flags), **no paywall, no upgrade prompts, no "Pro/Plus/Premium/Subscribe/₹" wording.** Interest capture only ("coming soon / notify me"). v1.1 activates via Apple IAP. *(Tiers: `premium-boundaries.md`.)*

---

## 9\. Platform & infra must-haves (v1)

| Must-have | Why |
| :---- | :---- |
| **In-app account deletion** | Apple requirement for any login app. Launch blocker. |
| **Force-update / min-version gate** | Retire a broken client when a backend change ships (native-release insurance). |
| **Generalized remote config** | Tune caps/cadence/ranking/copy/taxonomy/flags without an app release. |
| **Privacy** | ATT prompt (if tracking) \+ privacy policy \+ consent. |
| **Content-scarcity brief fallback** | Min card count \+ evergreen backfill so a slow day still reads as a brief (≥4 editorial \+ ≥2 signals or supplement/skip). |
| **Deep / universal links** | Email & web → app to the right screen (the launch funnel). |
| **Baseline accessibility** | Dynamic Type, VoiceOver labels, contrast. |
| **Offline** | Cached brief \+ recently-viewed readable offline; search disabled with a clear message. |
| **App Store ratings prompt** | After a positive moment (completed-brief streak). |

---

## 10\. Data sources & dependencies

| Surface | Backend |
| :---- | :---- |
| Brief | Editorial pipeline (generate-once 3 AM, validated, approved) \+ Datalabs signals |
| Articles (Explore/search) | Inc42 hybrid search (`/sqlquery`) — *Cloudflare allowlist \+ 20-query check pending (Task \#17)* |
| Companies \+ profiles | Datalabs entity search (ES) \+ company-detail |
| Reports | WordPress reports API (list-only) |
| Today's signals \+ Watchlist alerts | Datalabs daily aggregate \+ real-time Signal layer (new in v1) |

---

## 11\. Pushed to v1.1+ (the boundary)

- **v1.1 — deepen \+ monetize alerts:** custom alert triggers (Plus) \+ Pro-grade signal alerts · Emphasis Layer \+ section-level summaries · human-edited bullet-2 \+ bylines · **investor profiles** · saved searches · in-app report reader (if gating signed off) · Plus activation.  
- **v1.2 — depth \+ monetization:** **person profiles** · Ask Inc42 goes live · Pro-tier surfacing · audio "Listen" · share-with-team · deep-link discovery.  
- **Ordering logic:** habit → engagement → money; investor before person; never ship monetization UI before habit; each bundle is independently coherent.

---

## 12\. Success metrics (v1)

D7 ≥30% · D30 ≥15% · **Brief completion ≥40%** · push opt-in ≥55% · watchlist completion ≥30% · Decode usage ≥15% of opened stories · search/DAU ≥0.3 · Datalabs profile views/DAU ≥0.2 (M1) → 0.5 (M3) · crash-free ≥99.5%.

## 13\. Key risks to watch

1. **Editorial trust** — automated brief summaries on a journalism masthead; mitigate with the validation pipeline \+ human approval gate \+ content-scarcity fallback.  
2. **Search backend** — the Explore hybrid search is unverified (Cloudflare-gated); treat the 20-query check as launch-gating (Task \#17).  
3. **Notification fatigue / build size** — real-time alerts pulled into v1; significance gating \+ grouping \+ caps are the firewall, and the Signal layer enlarges the build (re-check the 2–3 week estimate).

### Open build-time decisions

Decode soft-cap threshold \+ Apple-safe copy · brief content-scarcity exact thresholds · relevance scoring weights (companion spec, to validate) · signal-stat priority \+ logo source on profiles · sub-nav: single strip vs Feeds|Industries toggle · timezone defaults for non-India users.

---

## 14\. Decisions log

- **2026-06-13** — People/investor profiles deferred to v1.1+ (investor first) → company profiles only; Watchlist \= Company \+ Sector; Saved → sub-tab; person search → coverage.  
- **2026-06-19** — Explore in-tab sub-navigation \+ Sector landing \+ card/chip specs.  
- **2026-06-21** — Notifications: full merged model (real-time Signal layer pulled into v1); engine: ranking+labels only (Emphasis Layer → v1.1), **pure relevance-ranked brief stack** (no sections), investor-tracking dropped; must-adds locked; native-release constraint adopted; this unified PRD made the canonical source of truth.  
- **2026-06-21 (relevance engine)** — Ranking \= **Editorial Importance base \+ Personal Relevance boost** (boost \= w\_entity·tracked \+ w\_sector·sector); **stage dropped from scoring AND onboarding** (onboarding now 5 steps); **uniform weights across ICPs** (ICP content-tilt → v1.1 Emphasis Layer); **top editorial story pinned to top 3**; weights server-side, remote-config tunable, validated on a concierge backtest before lock.  
- **2026-06-21 (detail pass)** — Full end-state \+ empty-state wireframes added across all surfaces; expanded card \= **3-bullet Smart Brevity** (bullet-2 auto v1 / human-edit v1.1); **Saturday recap \= the same finite stack labeled "This week"**; notification copy \= curiosity-gap **principle only, exact templates A/B'd at build**; Brief **reference prototype** linked (`prototype-2026-06-10.html`).

# Brief\_Personalization\_logic

## **Personalized Brief Ranking Logic (v1)**

### **Objective**

Personalize the order of cards within the Brief while preserving editorial judgment and preventing filter bubbles.

The Brief content set remains identical for all users. Personalization only affects ranking and relevance labeling, not content inclusion or exclusion.

Editorial teams retain full control over story selection and overall narrative structure.

---

## **Principles**

### **Editorial Importance**

Editorial importance remains the secondary ranking signal.

It does not replace Personalization ranking.

### **Personalization as a Boost**

Personalization acts as a primary ranking signal that elevates stories based on a user's selected sectors and Topics

### **No Filter Bubble**

Users should continue to see important stories outside their stated interests.

Personalization improves relevance without narrowing exposure.

---

## **Ranking Formula**

For every story:

**Final Score \= Editorial Importance \+ Personal Relevance**

Where:

**Personal Relevance \=Topic Boost \+ Sector Boost**

Expanded form:

**Final Score \= EI \+ (Wₜ × Topic Match Count) \+ (Wₛ × Σ matched-parent weights)**

---

## **Editorial Importance (EI)**

EI is not a manually assigned 10-50 score. Every story is assigned one of five tiers based on its significance to the startup ecosystem. Each tier maps to a configurable default EI score used by the ranking engine; fine-grained ordering *within* a tier is handled by your separate scoring layer, not by this framework.

| Tier | Description | Default EI Score |
| ----- | ----- | ----- |
| Tier 1 | Ecosystem Defining | 50 |
| Tier 2 | Major Industry Event | 40 |
| Tier 3 | Important Startup Update | 30 |
| Tier 4 | Contextual / Feature Story | 20 |
| Tier 5 | Niche / Supplemental | 10 |

### **Universal rules**

**Missing Development\_Type.** If Development\_Type is blank, the story defaults to **Tier 5**. 

**Currency conversion.** Convert ₹ figures using a live FX rate at scoring time. **Snapshot the rate used and store it with the story's score** (e.g. "scored at $1 \= ₹84.6, \[timestamp\]"), so the tier is reproducible after the fact 

**Sector Category Map** (parent category → child sectors)

**Ecommerce & Consumer** → Ecommerce, Consumer Services, Foodtech, Media & Entertainment  
**Fintech** → Fintech, Cryptocurrency, Digital Brokerage, Insurance Aggregators & Comparison Platform  
**Enterprise & SaaS** → Enterprise Services, Enterprise Tech, Cybersecurity  
**AI** → AI, AI Governance  
**Mobility & Logistics** → Logistics, Travel Tech, Electric Vehicles  
**Climate & DeepTech** → Clean Tech, Space Tech, Semiconductors, Advanced Hardware & Technology, Manufacturing Solutions  
**Edtech & Health** → Edtech, Health Tech, Agritech  
**Startup Ecosystem** → Startup Ecosystem  
**Real Estate Tech** → Real Estate Tech

**Universal Rule — Full-Match Primacy**

**1\. Qualification.** A story is *fully matched* for a user if it matches **every personalization signal the user has provided.**

* User set two → story must match both.  
* **User set one → story must match that one.** A single-signal user is fully matched by any story carrying that signal.  
* User set none → Full-Match does not apply; rank on Final Score

Fully-matched stories are promoted to a **priority group** that ranks **above all other stories**, regardless of Editorial Importance.

**2\. Ordering within the priority group.** Rank fully-matched stories against each other by **total Personal Relevance** (Topic \+ Sector boosts, summed — this is where "multiple Topics" counts: more matched Topics= higher Topic Boost \= higher rank). Editorial Importance is **not** used at this stage.

**3\. If Personal Relevance ties** within the group, resolve by the General Tie-Break cascade: Topic Boost → Sector Boost → EI → Recency → Story ID. (EI re-enters only here, as a late tiebreaker.)

**4\. Editorial floor preserved.** The Editorial Pin still fires: the day's highest-EI story is guaranteed a top-3 position. If the priority group fills positions 1–2, the pinned editorial story takes position 3; if the group is larger, the pinned story still claims one top-3 slot, displacing the lowest-relevance full-match story from the top 3\.

**5\. Non-fully-matched stories** rank below the priority group by Final Score (EI \+ Personal Relevance) as normal.

---

# **Funding**

*(development tag: Startup Funding & Investments)*

* Tier 2 — round ≥ $40M, OR creates a unicorn, OR led by a top-tier global investor into an already-prominent company.  
* Tier 3 — $15M–$40M. The core of Series A/B coverage — significant but not category-shaping.  
* Tier 4 — $5M–$15M. Small growth / large seed rounds. Undisclosed rounds into a growth-stage or otherwise prominent/recognizable company default here (not T5) — the deal is real, only the number is withheld.  
* Tier 5 — \< $5M confirmed, OR seed/pre-seed, OR undisclosed rounds into early-stage / non-prominent companies.

  # **Venture Capital**

*(development tag: Fund Launches)*

* Tier 2 — fund corpus ≥ ₹1,500 Cr (\~$180M), OR launched by a top-tier India/global VC regardless of size  
* Tier 3 — ₹500 Cr–₹1,500 Cr, OR the first close of a large (₹1,000 Cr+ target) fund,  
* Tier 4 — ₹100 Cr–₹500 Cr — the bulk of sector-specific, micro-VC, and continuation funds.  
* Tier 5 — sub-₹100 Cr funds, angel networks, micro-funds

  # **M\&A**

*(development tag: Startup Mergers & Acquisitions)*

* Tier 1 — sector-restructuring. The deal materially changes the competitive structure of an entire major sector. Concrete criteria — meets any: • combines two of the top / major / recognizable players in a major sector; OR • creates a post-deal entity with clear market leadership in a major category; OR • removes a major independent player from the market (a top / major / recognizable company absorbed by a larger strategic/corporate). Rarely fires by design — reserved for deals that redraw a sector's map, not merely a large purchase.  
* Tier 2 — major deal. Meets any: • disclosed value ≥ $50M; OR • creates or cements a top / major / recognizable position in a defined category (without restructuring the whole sector); OR • a top-50 startup/unicorn or a large corporate/listed/global company is a principal party in a control transaction.  
* Tier 3 — significant deal. Meets any: • disclosed value $15M–$50M; OR • a controlling/majority stake taken by a recognizable acquirer in a named company, value undisclosed; OR • a strategic bolt-on between two recognizable companies.  
* Tier 4 — routine deal. Meets any: • disclosed value $2M–$15M; OR • an undisclosed deal between lesser-known or early-stage companies where neither party is prominent.  
* Tier 5 — minor deal. Acquihires, talent-only buys, sub-$2M deals, or undisclosed micro-deals with no recognizable party.

  # **IPO**

*(development tag: Startup IPO)*

* Tier 1 — issuer valuation/market cap ≥ $5B  
* Tier 2 — IPO events (the first time each occurs): DRHP filing, IPO open, and the listing/debut announcement itself. The debut is a T2 event only on the story that first reports the shares beginning to trade.  
* Tier 3 — in-progress subscription updates during the open window ("Day 1 / Day 2 subscribed X%").  
* Tier 4 — post-listing performance and routine progress notes: listing-day price movement, "shares trade at X% discount/premium," first-session close, and incremental "IPO to open on \[date\]" / price-band-set scheduling notes.  
* Tier 5 — small issuers (sub-₹500 Cr issue size)

  # **People**

*(development tag: People & Culture)*

* Tier 2 — founder/CEO-level move at a startup valued ≥$500M OR any company/entity of comparable scale (large corporate, listed major, global player)  
* Tier 3 — CXO-level (COO/CTO/CFO/CBO) appointments or exits at a recognized company  
* Tier 4 — other senior appointments — board members, independent/non-executive directors, advisory or venture-partner roles, and non-CXO leadership hires at a recognized company;  
* Tier 5 — mid-level hires, small-company HR news

  # **Layoffs**

*(development tag: Startup Layoffs)*

* Tier 2 — Any confirmed layoff round at a startup valued ≥$500M OR any company/entity of comparable scale (large corporate, listed major, global player) regardless of headcount percentage, OR layoffs signal a sector-wide pattern (multiple companies, same week)  
* Tier 3 — layoffs at any named, recognizable startup below the Tier 2 bar  
* Tier 5 — small-scale or unconfirmed layoffs at obscure/early-stage companies

  # **Trends**

*(development tag: Industry Trends)*

* Tier 4 — default; this category is inherently analysis/commentary  
* Tier 3 — only if built on hard aggregate data with a real signal, not a templated weekly roundup  
* Tier 5 — recurring low-effort roundups (stock movers, "stocks to watch")

  # **Cohort Launches**

*(development tag: Cohort Launches)*

* Tier 4 — cohort run by a globally recognized accelerator (YC, Google for Startups) or major corporate program  
* Tier 5 — default; structurally a niche category

  # **Startup Discovery**

*(development tag: Startup Discovery)*

* Tier 5 — default; definitionally early-stage, limited-impact coverage

  # **Controversies**

*(development tag: Controversies)*

* Tier 2 — involves a startup valued ≥$500M OR any company/entity of comparable scale (large corporate, listed major, global player) AND the controversy has regulatory action, active litigation, or demonstrated large-scale user/financial harm  
* Tier 3 — recognizable company, but contained in scope (lawsuits, PR disputes, isolated incidents)  
* Tier 5 — social-media disputes with no material business consequence

  # **News** 

*(development tag: Business Updates)*

* Tier 2 — a move by a startup valued ≥$500M OR any company/entity of comparable scale (large corporate, listed major, global player) that materially affects competitor strategy or category dynamics (e.g. pricing shifts, platform lock-in, major distribution tie-up)  
* Tier 3 — earned, not default. Requires BOTH: (a) a named, recognizable company, AND (b) a material move — a real market expansion, a meaningful partnership/tie-up, a competitively-relevant product launch, or a regulatory approval that opens a new business line.  
* Tier 4 — default. Everything that doesn't clear the T3 test: routine certifications, minor product updates, incremental feature launches, small tie-ups, "recognizable company did a normal thing" news.

  # **Business Model & Strategy**

*(development tag: Business Models & Strategy)*

* Tier 4 — no exceptions. If a story here contains hard news (a number, a launch, a deal), it's mistagged — move it to Business Intelligence or Funding

  # **Financials**

*(development tag: Startup Financials)*

* Tier 3 — prominence AND a development. Results from a listed company, unicorn, or IPO-bound company (DRHP filed / IPO announced) that also carry a material development — any of: • ≥2x YoY change in profit, revenue, or loss; OR • return to profitability, swing into loss, or first reported profit; OR • a notable revenue/scale milestone (e.g. crossing a major revenue mark, first ₹1,000 Cr year).  
* Tier 4 — routine results. Either: • a listed / unicorn / IPO-bound company's results with no material development (in-line growth, ordinary quarterly, single-digit or modest YoY movement) — the "prominent, but nothing happened" case; OR • routine results at smaller / less-prominent companies.  
* Tier 5 — obscure-company financials, stock-price-movement commentary tied to results

  # **Policy**

*(development tag: Government & Policies)*

* Tier 1 — nationwide, cross-sector policy (Budget changes, RBI-wide rules, SEBI frameworks, landmark AI/data policy)  
* Tier 2 — sector-specific or single-major-company regulatory action (a court ruling on one platform, a ministerial statement with near-term policy weight)  
* Tier 3 — routine enforcement (single-company fines, narrow rulings, compliance tightening)  
* Tier 4 — routine government/regulator data releases and administrative updates with no new policy change: monthly transaction/registration statistics, periodic reports, status notifications, and procedural clarifications.  
* Tier 5 — narrow, low-impact tweaks (single-vehicle-category incentives, hyper-local rules)

---

## **Sector Match**

Sector Boost \= Wₛ × Σ (weight of each distinct parent category the story matches from the user's selected parents)  
Sector Match Count represents the number of distinct parent categories (from the user's selected parents) that the story's child tags roll up to.

Example

User follows: Fintech, AI

Story child tags: Fintech, AI

Sector Match Count \= 2 

Where each matched parent contributes weight **1**, except **Startup Ecosystem \= 0.5**.

* Edge case 1 (child tags, same parent): dedupe → count parent once.  
* Edge case 2 (child tags, different parents): each distinct matched parent adds its weight.  
* Example: matches Fintech \+ AI \+ Startup Ecosystem → 1 \+ 1 \+ 0.5 \= 2.5 → Sector Boost \= Wₛ × 2.5.

**Sector Category Map** (parent category → child sectors)

**Ecommerce & D2C →** Ecommerce, D2C, Logistics

**Consumer →** Consumer Services, Foodtech, Media & Entertainment, Travel Tech, Edtech, Health Tech, Agritech

**Fintech →** Fintech, Cryptocurrency, Digital Brokerage, Insurance Aggregators & Comparison Platform, Web3

**Enterprise & SaaS →** Enterprise Services, Enterprise Tech, Cybersecurity, Real Estate Tech

**AI →** AI, AI Governance

**DeepTech →** Clean Tech / Climate Tech, Space Tech, Semiconductors, Advanced Hardware & Technology, Manufacturing Solutions, Electric Vehicles

**Startup Ecosystem →** Startup Ecosystem

---

## **Weight Hierarchy**

### **Requirement**

Wₜ \> Wₛ 

Example starting configuration:

| Weight | Value |
| ----- | ----- |
|  |  |
| Wₜ | 20 |
| Wₛ | 15 |

Final values will be determined after concierge- validation and controlled experimentation.

Weights remain configurable via Remote Config.

---

## **Example Calculation**

> **User Profile**  
>  Sector Match \= Fintech (1 full parent) → Sector Boost \= Wₛ × 1 \= 15  
>  Preferred Topics: Funding & Investment

> **Story:** "Razorpay raises $75M"

> **Scores**  
>  Editorial Importance \= **40** (Startup Funding & Investments, ≥$40M → Tier 2 → EI 40 on the new 10–50 scale)  
>  Topic Match \= 1 (Funding & Investment) → Topic Boost \= Wₜ × 1 \= **20**  
>  Sector Match \= 1 (Fintech) → Sector Boost \= Wₛ × 1 \= **15**  
>  Personal Relevance \= 20 \+ 15 \= **35**  
>  **Final Score \= 40 \+ 35 \= 75**

---

### **Another Story**

National startup funding slowdown

Editorial Importance \= 50

Sector Match \= 0

Personal Relevance \= 0

Final Score \= 50

---

## **Relevance Label Logic**

The "Relevant because..." label should only appear when personalization materially influenced ranking.

### **Formula**

Boost \= Final Score − Editorial Importance

### **Conditions**

If Boost \> 0:

Display relevance label.

Examples:

* Relevant because you follow Fintech

If Boost \= 0:

Do not display any relevance label.

The story reached its position due to editorial importance alone.

---

### **Cold Start Logic**

Apply whichever signals the user has provided. Any signal the user has not set contributes zero.

**User Selected Topics And/Or Sectors But No Watchlist**  
 Use:  
 Final Score \= EI \+ Topic Boost \+ Sector Boost  
 *(Entity Boost \= 0\. Whichever of topic/sector the user set applies; the other is 0.)*

**User Selected Topics Only**  
 Use:  
 Final Score \= EI \+ Topic Boost

**User Selected Sectors Only**  
 Use:  
 Final Score \= EI \+ Sector Boost

**User Skipped Onboarding**  
 Use:  
 Final Score \= EI  
 No personalization is applied. The user receives the standard editorial Brief.

> **Note:** Full-Match applies to any user with at least one provided signal — including single-topic or single-sector cold-start users. Only users who skipped onboarding entirely rank on plain Final Score.

---

## **Remote Configuration**

 The following parameters must be configurable without app releases:

* Topic weight (Wₜ)  
* Sector weight (Wₛ)  
* Startup Ecosystem parent weight (default 0.5)  
* Relevance label threshold

---

## **Tie-Break Rules**

**1\. General Ranking Tie-Break** When Final Score is equal, resolve in this order:

1. Topic Boost  
2. Sector Boost  
3. Sector Boost composition — prefer the story matching more full-weight (non–Startup Ecosystem) parents  
4. EI  
5. Recency (published\_at, descending)  
6. Story ID (ascending)

No random tie-breaks. Steps 5–6 guarantee full determinism.

**3\. Relevance Label Tie-Break** If a story qualifies for a label via both Topic Match and Sector Match:

* Display the Topic-based reason. Topic always outranks sector (consistent with Wₜ \> Wₛ).

# Old PRDs

# App PRD v1

# Inc42 Brief — Product Concept

**Status**: Concept locked · 2026-05-17  
---

## TL;DR

**Inc42 Brief** is a unified mobile app for India-1 professionals — founders, investors, operators, and BD & partnerships leaders who need to stay sharp on India's startup economy.

The **Morning Brief** is the spine: a finite, push-delivered, segment-filtered, watchlist-ranked daily brief of 6–8 items. It arrives at 7–8 AM IST, runs through what moved, and ends. No infinite scroll. The brief is the door.

Behind it: a full **article reader**, a **discovery feed**, **Datalabs entity profiles**, **search**, **watchlist**, and **bookmarks**. These exist so a single morning touchpoint can become a full content relationship — but they're pull-only. The app opens to the brief, not the feed.

**Everything is Inc42**: no third-party news aggregation. Every item in the brief is either Inc42 editorial or Datalabs structured data. The "Because you track: \[X\]" attribution on every personalized card is always Inc42's own signal.

**v1.0 is free, no paywall, no monetization.** Premium boundaries are architected from day one but not activated. The goal of v1.0 is to prove daily habit, cross-segment resonance, and that a single app can carry both the brief and the deeper reading session.

---

## 1\. Positioning — TBD

---

## 2\. Audience

Four segments. Founders and Investors at full depth. Operators and BD & Partnerships as lighter-touch modes on the same spine.

| Segment | Mode | Depth | What it surfaces |
| :---- | :---- | :---- | :---- |
| **Founders** | Default | Primary | Sector \+ stage news, capital \+ policy signal, talent and hiring moves |
| **Investors** | Watchlist mode | Primary | Portfolio company news, peer-fund moves, deal-flow signals, thesis-relevant developments |
| **Operators** | Role-context mode | Lighter | Function-relevant talent moves, tooling shifts, competitive-set news |
| **BD & Partnerships** | Saved-search mode | Lighter | Client/prospect company news, service-line trends, partnership signals |

**Cadence by segment** — this is a design rule, not just a scheduling choice:

| Segment | Decision cadence | Push frequency |
| :---- | :---- | :---- |
| Founders | Same hour, not same week | High (must-know breaking) |
| Investors | Same hour, not same week | High (watchlist \+ deal alerts) |
| Operators | Same day, not same week | Daily digest |
| BD & Partnerships | Same week, not same month | Weekly batch |

**Operators v1.0 scope**: comp/ESOP signal requires separate data infrastructure — deferred to v1.1. v1.0 Operators mode draws from news-derivable signals only.

---

## 3\. Hero Jobs

**Unified spine**:

> *When something moves in the Indian startup economy that affects my decisions today, I want a finite, decodable brief on what happened and what it means for my context, without leaving my phone, so I can act on the right information in the cadence appropriate to my role.*

**Secondary job** (Explore tab):

> *When I have 10–15 minutes and want to go deeper on something — a company I track, a sector moving, a story I caught a headline on — I want to read it fully, find related context, and save it for reference, without switching to a browser.*

**Per-segment hero jobs** (persona-validated across tests \#2, \#3):

*Founders*: When something moves that affects my decisions — a competitor's raise, a regulatory shift in my sector, a talent signal — I want a decodable brief so I can decide in the same hour whether to act, share, or ignore.

*Investors*: When a portfolio company surfaces in news, a peer fund moves in my thesis area, or a deal closes in my sector — I want a brief on what happened and what it means for my watchlist, so I can respond to founders, angels, LPs, and peers in the same hour.

*Operators*: When something moves in my function or my company's competitive set — a senior talent move, tooling shift, policy signal — I want a brief so I can act with the right context inside my organization the same day.

*BD & Partnerships*: When a client or prospect company makes news or a partnership opportunity opens — I want a brief so I can act on the opportunity the same week.

---

## 4\. Information Architecture

**4 bottom tabs**: **Brief / Explore / Watchlist / Profile**

Tab label "Brief" is locked (consistent with the app name; resolves implicitly via the name decision). "Today" was tested as an alternative tab label paired with "Inc42 Today" as a name candidate — Today lost on both fronts.

**Explore — reframed as an archive surface, not a discovery feed**. The Council critiqued "Explore is structurally hollow at 11.3 articles/day" — that critique was right *if* we were building a daily-discovery feed of leftover articles. It's wrong for what we're actually building.

**Why Explore has real depth**: Inc42 has been publishing since 2014\. The archive is approximately **25,000–45,000 articles**. The Datalabs entity model covers 70,000+ companies, founders, and funds. The "3–5 leftover articles after today's brief" framing dramatically undersells what's in this tab. Five of six user journeys through Explore are archive-driven (search, topic browse, reports/longform, recent, recently viewed); only the "Today's Datalabs signals" strip is daily-fresh.

**Tab name**: **Explore** (locked — most familiar pattern across apps; the archive-surface reframe resolves the Council's "hollow" concern without needing a renamed tab). Fallback alternatives if Explore reads off in pilot: Library (collection register), then Sections (newsroom register).

| Tab | Contents | Default state |
| :---- | :---- | :---- |
| **Brief** | Morning Brief (6–8 items) \+ Datalabs signal cards | App opens here. Full-screen brief. No feed continuation after the last card. |
| **Explore** | Inc42's editorial archive (\~30K+ articles, searchable \+ browsable) \+ **Datalabs entity universe** (\~70K companies/founders/funds, browsable by sector/stage/recency) \+ Datalabs daily signals (aggregate funding/deals/hiring) \+ Full-text search across both \+ Recently viewed | Pull-only. Requires deliberate tab switch. |
| **Watchlist** | Tracked entities \+ alert history \+ setup wizard. Tapping an entity → opens its full **Datalabs entity profile** (v1.0 includes profiles; see §8). | Personalization engine. Drives brief ranking \+ push tier 1\. |
| **Profile** | Role \+ segment settings \+ push preferences \+ bookmarks \+ account management | Settings and persistence. |

**Article reader**: slides up as a full-screen modal from any brief card, library article card, entity profile coverage section, or search result. Accessible from every surface — not its own tab.

**Datalabs entity profile**: full v1.0 surface (no longer deferred to v1.1). Accessible from Watchlist entity tap, Explore Companies browse, brief Datalabs signal card tap, search result entity tap, and entity-tag tap inside an article. See §6 for wireframe.

**Ask Inc42** *(stretch goal, v1.1 if not in v1.0)*: if capacity permits, embedded contextually at article footers, brief card footers, and entity profiles with pre-seeded question suggestions. Not a standalone tab — contextual placement only, pre-loaded with article or entity context.

### What's in the Explore tab — detailed

Layout (top to bottom):

1. **Persistent search bar** — full-text search across the Inc42 corpus \+ Datalabs entity model. Entity results surface first when the query matches an entity; article results below.  
     
2. **Today's Datalabs signals** (collapsed by default, expand to view) — top 3–5 aggregate signals of the day: total funding raised, deals closed, sector flows, hiring movements. Each tappable to a deeper view (list of deals, list of hires). *Optional sub-toggle: All (market aggregates) / My watchlist (signals for tracked entities only).*  
     
3. **Content-type switch** (top-level tabs within Explore): **Articles / Companies / Reports**  
     
   - **Articles** *(default)*: chronological feed of Inc42's editorial corpus. Filter bar below: All / Breaking / Features / Stories \+ optional topic chips (user's onboarding sectors) \+ optional "★ My watchlist" chip (filters to articles mentioning tracked entities).  
   - **Companies**: entity card grid from the Datalabs entity model. Filter by sector / stage / region / recency of funding. Sort by Recently funded / Most-followed / A–Z. Tap entity → full Datalabs entity profile.  
   - **Reports**: Inc42's deep dives, Datalabs reports, special projects. Tap → article reader (or report reader for multi-page reports).

   

4. **Article feed** *(when Articles tab is active)*: chronological by default. Cards use the same format as Brief cards but **without** "Because you track" attribution — Explore is not personalized at card level. Users opt into entity-level personalization via Watchlist or the "★ My watchlist" filter chip.  
     
5. **Recently viewed** *(bottom of scroll)*: last 10 items the user opened across articles \+ entity profiles. Lightweight history; gives a re-entry point.

**What's NOT in Explore**: a daily-refreshed discovery feed of "what's new today" — that's the Brief's job. Explore is for going beyond the day, not duplicating it.

**Why this matters**: when a user finishes the Brief and taps Explore, they're looking for *something specific* (search), *the broader corpus* (browse Articles or Companies), or *aggregate market signals* (today's Datalabs signals). The archive depth means Explore has real reasons to come back beyond "see today's news" — search, sector deep-dives, company research, report reading.

---

## 5\. Content Model

### Publication volume

Inc42 publishes **11.3 articles/day** on average (WordPress REST API audit, 30-day window, 338 articles total).

| Content type | Avg/day | Brief eligible |
| :---- | :---- | :---- |
| Breaking News | 9.3 | Yes |
| Feature/Longform | 1.5 | Yes |
| Startup Stories | 0.5 | Yes |
| Resources | 0.0 | No |

With 11.3 brief-eligible articles/day, the brief is a **filtering problem, not a supply problem**. The brief selects the right \~4 from the daily editorial pool and supplements with Datalabs watchlist signals.

### Brief composition

| Slot | Source | Personalization | Count |
| :---- | :---- | :---- | :---- |
| Top editorial | Inc42 editorial pool | Segment-ranked, watchlist-boosted | 3–4 |
| Datalabs watchlist signals | Entity events (funding, hiring, deals) for tracked entities not in today's editorial | Watchlist-matched | 2–3 |
| Archive pull | Inc42 last 7 days, unread by user | Relevance-ranked | 0–1 |
| **Total** |  |  | **6–8** |

**Ranking logic**: editorial articles scored by (segment relevance weight × watchlist entity match boost × recency decay). Datalabs signal cards fill gaps — entities on the user's watchlist that didn't appear in today's editorial but had a fundable event, hiring change, or deal signal.

### Cadence

| Day | Brief type |
| :---- | :---- |
| Mon–Thu | Full daily brief (peak editorial volume: 13–15/day) |
| Fri | Full daily brief (\~11/day) |
| Sat | **Weekly recap brief** — top 5–7 stories of the week \+ Datalabs week-in-numbers (aggregate funding, deals, sector signals). Light editorial effort: pull from week's highlights. |
| Sun | **Off** — no brief pushed. App available for Explore. Sun averages 2.5 articles/day — not enough for a credible brief. |

Pushing a weak brief on Sunday trains users to ignore pushes. Scarcity signals respect for the user's time.

---

## 6\. Screen States

All wireframes use a consistent phone frame. Tab bar shows which tab is active (shown in brackets).

---

### Today / Brief tab — Morning Mode

The primary experience. App opens here every day.

```
┌────────────────────────────┐
│ 7:32 AM        Fri, May 16 │
├────────────────────────────┤
│  TODAY'S BRIEF  ●●○○○○○○  │
│  2 of 8 stories            │
│                            │
│  ┌──────────────────────┐  │
│  │ ■ BREAKING NEWS      │  │
│  │                      │  │
│  │ Meesho raises $275M  │  │
│  │ Series G at $4.9B    │  │
│  │ valuation            │  │
│  │                      │  │
│  │ "This matters for D2C│  │
│  │ founders: new floor  │  │
│  │ for Series E+ vals…" │  │
│  │              ▸ More  │  │
│  │                      │  │
│  │ Because you track:   │  │
│  │ Meesho               │  │
│  └──────────────────────┘  │
│                            │
│  ┌──────────────────────┐  │
│  │ [D] DATALABS SIGNAL  │  │
│  │                      │  │
│  │ Zepto: 200 new dark  │  │
│  │ stores in Apr · Q-   │  │
│  │ Commerce · May 2026  │  │
│  │                      │  │
│  │ Because you track:   │  │
│  │ Zepto                │  │
│  └──────────────────────┘  │
│                            │
│  ↓ scroll for 6 more       │
│                            │
├────────────────────────────┤
│ [Brief]  Explore  ☆  ≡   │
└────────────────────────────┘
```

- **Progress dots** (●●○○○○○○): stories read vs total. Not a percentage — shows the brief is finite and countable.  
- **Brief cards scroll vertically** — swipe or scroll to read all 8\. No horizontal swipe; no infinite scroll.  
- **Datalabs signal cards** have distinct visual treatment (lighter background or border) — signals "structured data, not an article."  
- **Tab bar**: Today is active.

---

### Brief card — editorial item (zoomed in)

```
┌──────────────────────────────────────┐
│ ■ BREAKING NEWS           2h ago     │
│                                      │
│ Meesho raises $275M Series G at      │
│ $4.9B valuation                      │
│                                      │
│ By Pooja Sareen · Inc42              │
│                                      │
│ "This matters for D2C founders:      │
│ a new valuation floor for Series E+  │
│ companies in social commerce…"       │
│                                  ▸   │
│                                      │
│ Because you track: Meesho       ⊘    │
└──────────────────────────────────────┘
```

- **AI decode snippet**: 1 sentence (outcome-oriented: "This matters for…", not "This article says…"). Tapping ▸ expands to 3–4 bullet decode. Only present if Ask Inc42 is in scope; omit if deferred.  
- **"Because you track"**: shown only on cards where watchlist boosted the ranking. Top editorial picks not influenced by watchlist carry no attribution line.  
- **Dismiss (⊘)** *(Council-driven addition)*: long-press the card or tap the ⊘ icon to mark "not interested." Surfaces a quick reason chooser ("Not in my sector / Already read / Not interested in \[entity\]"). Feeds personalization signal — the only per-card action added to v1.0 beyond what already exists (Track via entity tap → watchlist; bookmark in reader; share in reader). Other Council-suggested actions (Track deeper / Share internally / Note for later) are already covered by existing affordances.  
- **Tap anywhere on card**: opens Article Reader.

---

### Datalabs signal card (zoomed in)

```
┌──────────────────────────────────────┐
│ [D] DATALABS  ·  Funding Signal      │
│                                      │
│ Zepto  added 200 new dark stores     │
│ in April FY26                        │
│ Q-Commerce · May 15, 2026            │
│                                      │
│ Revenue implication: ₹~180 Cr        │
│ monthly run-rate expansion           │
│                                      │
│ Because you track: Zepto             │
└──────────────────────────────────────┘
```

- **\[D\] tag \+ distinct background**: signals "this is Datalabs structured data, not an Inc42 editorial article."  
- **No AI decode on signal cards**: the structured data is the signal — no prose decode needed.  
- **Tap**: opens Datalabs entity profile for the company.

---

### Brief completion — "Done for today"

After the last card, the brief ends. No feed continuation.

```
┌────────────────────────────┐
│ 7:41 AM        Fri, May 16 │
├────────────────────────────┤
│                            │
│                            │
│      ✓                     │
│   Done for today.          │
│                            │
│   You read all 8 stories   │
│   in today's brief.        │
│                            │
│   Next brief: tomorrow     │
│   morning at 7:30 AM.      │
│                            │
│   ─────────────────────    │
│                            │
│   Want to go deeper?       │
│   [ Open Explore ]         │
│   (tap to switch tabs)     │
│                            │
│   Or come back tomorrow.   │
│                            │
│                            │
│                            │
├────────────────────────────┤
│ [Brief]  Explore  ☆  ≡   │
└────────────────────────────┘
```

- **"Open Explore" is an opt-in action** — not an automatic continuation. The user must actively tap to switch.  
- **No "keep reading" link** that scrolls straight into a feed. The break is deliberate.

---

### Explore tab — Articles view (default)

```
┌────────────────────────────┐
│ 9:41                LIBRARY│
├────────────────────────────┤
│  ┌──────────────────────┐  │
│  │ 🔍 Search Inc42…     │  │
│  └──────────────────────┘  │
│                            │
│  TODAY'S SIGNALS       ▾   │
│  ┌──────────────────────┐  │
│  │ ₹423 Cr raised today │  │
│  │ across 12 deals      │  │
│  └──────────────────────┘  │
│  ┌──────────────────────┐  │
│  │ Fintech leads sector │  │
│  │ activity (5 deals)   │  │
│  └──────────────────────┘  │
│     (3 more, scroll →)     │
│                            │
│  [Articles] Companies Reports│
│                            │
│  [All] Breaking Features   │
│  Stories  ↓ Recent         │
│  [D2C][Fintech]  [★Watchlist]│
│                            │
│  ┌──────────────────────┐  │
│  │ ■ BREAKING NEWS  3h  │  │
│  │ Cabinet clears new   │  │
│  │ semiconductor policy │  │
│  │ By Shishir · Inc42   │  │
│  └──────────────────────┘  │
│                            │
│  ┌──────────────────────┐  │
│  │ ▤ FEATURE        5h  │  │
│  │ Why India's OTT      │  │
│  │ market is splitting  │  │
│  │ By Nikhil · Inc42    │  │
│  └──────────────────────┘  │
│                            │
│  (scroll for archive ↓)    │
│                            │
├────────────────────────────┤
│  Brief  [Explore]  ☆  ≡   │
└────────────────────────────┘
```

- **Top-level content-type switch** (Articles / Companies / Reports): determines what kind of cards the feed below shows.  
- **Today's signals strip** (collapsible): 3–5 aggregate Datalabs signals. Always visible across all three content types.  
- **Filter bar** (Articles view): content-type chips \+ topic chips \+ opt-in "★ My watchlist" chip.  
- **Feed**: chronological by default. Same card format as Brief cards, no "Because you track" attribution (Explore is not personalized at card level).  
- **Archive depth**: scroll back loads progressively older articles; for deep archive, search is the right tool.

---

### Explore tab — Companies view

```
┌────────────────────────────┐
│ 9:41                LIBRARY│
├────────────────────────────┤
│  ┌──────────────────────┐  │
│  │ 🔍 Search Inc42…     │  │
│  └──────────────────────┘  │
│                            │
│  TODAY'S SIGNALS       ▾   │
│  (collapsed)               │
│                            │
│  Articles [Companies] Reports│
│                            │
│  [All sectors▾] [Stage▾]   │
│  ↓ Recently funded         │
│                            │
│  ┌──────────────────────┐  │
│  │ [M] Meesho   ✓ Track │  │
│  │ E-commerce · Series G│  │
│  │ $275M · May 2026     │  │
│  └──────────────────────┘  │
│                            │
│  ┌──────────────────────┐  │
│  │ [Z] Zepto   ✓ Track  │  │
│  │ Q-Commerce · Series G│  │
│  │ $340M · Mar 2026     │  │
│  └──────────────────────┘  │
│                            │
│  ┌──────────────────────┐  │
│  │ [R] Razorpay   [+]   │  │
│  │ Fintech · Series F   │  │
│  │ $375M · Dec 2025     │  │
│  └──────────────────────┘  │
│                            │
│  ┌──────────────────────┐  │
│  │ [P] Pocket FM   [+]  │  │
│  │ Audio · Series D     │  │
│  │ $103M · Mar 2024     │  │
│  └──────────────────────┘  │
│                            │
│  (scroll for more ↓)       │
│                            │
├────────────────────────────┤
│  Brief  [Explore]  ☆  ≡   │
└────────────────────────────┘
```

- **Filter row**: sector dropdown (multi-select), stage dropdown, region (optional).  
- **Sort options**: **Recently funded \+ largest rounds** *(default)* / Most-followed / A–Z. The default is a composite — entities ranked by a score combining recency and round size (a $100M raise 1 week ago outranks a $5M raise 1 day ago). Surfaces what's meaningfully moving without dropping fresh activity. Avoids hidden algorithmic personalization (no "trending in your sector").  
- **Entity cards**: logo, name, sector, latest funding round, funding amount \+ date. Tracked-state shown inline (✓ Tracking for tracked entities; \[+\] for untracked).  
- **Tap entity** → opens full Datalabs entity profile (wireframe below).  
- **Tap track button** → adds/removes from watchlist without leaving Explore.

---

### Explore tab — Reports view

Same layout pattern as Articles view, filtered to Inc42's reports \+ Datalabs reports \+ deep-dive features. Cards are larger (reports often have a hero image \+ multi-section structure). Tap → report reader (or article reader for single-piece reports). Filter by topic/sector \+ report type (Sector report / Funding report / Trend analysis).

---

### Search active state

---

### Search — active state

```
┌────────────────────────────┐
│ 9:41                    ╳  │
├────────────────────────────┤
│  ┌──────────────────────┐  │
│  │ 🔍  zepto___________ │  │
│  └──────────────────────┘  │
│                            │
│  ENTITY                    │
│  ┌──────────────────────┐  │
│  │  [Z]  Zepto          │  │
│  │  Q-Commerce · Ser. G │  │
│  │  Last funded: $340M  │  │
│  │                [Track]  │
│  └──────────────────────┘  │
│                            │
│  ARTICLES  (24 results)    │
│  ┌──────────────────────┐  │
│  │ Zepto added 200 dark │  │
│  │ stores in Apr FY26   │  │
│  │ Breaking · 2h ago    │  │
│  └──────────────────────┘  │
│  ┌──────────────────────┐  │
│  │ Can Zepto beat       │  │
│  │ Blinkit in Tier 2?   │  │
│  │ Feature · 3 days ago │  │
│  └──────────────────────┘  │
│  ┌──────────────────────┐  │
│  │ Zepto dark store     │  │
│  │ economics, explained │  │
│  │ Report · 2 weeks ago │  │
│  └──────────────────────┘  │
│                            │
├────────────────────────────┤
│  Brief  [Explore]  ☆  ≡  │
└────────────────────────────┘
```

- **Entity result surfaces first** when the query matches a Datalabs entity — gives the user a one-tap path to the profile \+ track.  
- **Article results** ranked by recency. Tap opens Article Reader.  
- **\[Track\]**: adds entity directly from search without visiting the profile.

---

### Article Reader

```
┌────────────────────────────┐
│ ←  Inc42       🔖  ↗  ╳  │
├────────────────────────────┤
│ ▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░ │
│                            │
│  BREAKING NEWS · May 16    │
│                            │
│  Meesho raises $275M       │
│  Series G at $4.9B val     │
│                            │
│  Pooja Sareen · Inc42      │
│  May 16, 2026 · 4 min read │
│  ──────────────────────    │
│                            │
│  Meesho has closed a $275  │
│  million Series G round at │
│  a valuation of $4.9       │
│  billion, backed by        │
│  SoftBank, General         │
│  Atlantic and Fidelity…    │
│                            │
│  The raise comes as social │
│  commerce sees a new wave  │
│  of institutional interest │
│  following Meesho's return │
│  to profitability in FY25… │
│                            │
│  [full article continues]  │
│                            │
│  ──────────────────────    │
│  RELATED STORIES           │
│  · Meesho's FY26 revenue   │
│    breakdown · Feature     │
│  · Social commerce raises  │
│    in 2026 · Brief         │
│                            │
├────────────────────────────┤
│  Brief  [Explore]  ☆  ≡  │
└────────────────────────────┘
```

- **Progress bar** (▓▓▓░░░): thin top bar showing reading completion.  
- **🔖 bookmark**: one-tap, in header, saves to Profile → Bookmarks.  
- **↗ share**: native iOS/Android share sheet.  
- **╳ close**: returns to wherever the reader was opened from (brief, feed, search).  
- **Related stories**: 2–3 articles from Inc42 on the same company or topic, editorial-tag-driven. Shown at the end of the article — not as a sidebar.  
- **No comments section** in v1.0.  
- Gate v1.0 launch on: reader loads faster than inc42.com mobile \+ usability test ≥8/10 vs web baseline.

---

### Watchlist tab

```
┌────────────────────────────┐
│ 9:41           WATCHLIST   │
├────────────────────────────┤
│  TRACKING (12)     [+ Add] │
│                            │
│  Companies                 │
│  ┌──────────────────────┐  │
│  │ [M] Meesho   Ser. G  │  │
│  │ E-Commerce · 14 alerts│ │
│  └──────────────────────┘  │
│  ┌──────────────────────┐  │
│  │ [Z] Zepto   Ser. G   │  │
│  │ Q-Commerce · 8 alerts│  │
│  └──────────────────────┘  │
│  ┌──────────────────────┐  │
│  │ [B] Bhavish Aggarwal │  │
│  │ Founder, Ola · 3 alts│  │
│  └──────────────────────┘  │
│                            │
│  Sectors                   │
│  ┌──────────────────────┐  │
│  │ D2C            21 ▸  │  │
│  └──────────────────────┘  │
│  ┌──────────────────────┐  │
│  │ Fintech        17 ▸  │  │
│  └──────────────────────┘  │
│                            │
│  RECENT ALERTS             │
│  · Meesho: $275M raise     │
│    2h ago                  │
│  · Zepto: 200 new stores   │
│    2h ago                  │
│  · D2C: Nykaa FY26 results │
│    Yesterday               │
│                            │
├────────────────────────────┤
│  Brief  Explore  [☆]  ≡  │
└────────────────────────────┘
```

- **\[+ Add\]** opens the entity search (same as Watchlist seed in onboarding — Datalabs search-as-you-type).  
- **Alert count** on each entity row. Tap entity → opens the full **Datalabs entity profile** (wireframe below) — v1.0 includes profiles.  
- **Recent alerts** section: last 3 watchlist-triggered signals, regardless of whether they appeared in the brief.

---

### Datalabs entity profile *(v1.0)*

*Restored to v1.0 scope per user discretion (against Council's cut recommendation), to preserve the investor-segment differentiation at launch. Subject to eng-leadership timeline confirmation at the build planning call.*

```
┌────────────────────────────┐
│ ←              [+ Track]   │
├────────────────────────────┤
│                            │
│  [M]  Meesho               │
│  Social Commerce · Ser. G  │
│  Founded 2015 · Bengaluru  │
│  meesho.com · LinkedIn · X │
│                            │
│  ──────────────────────    │
│  FUNDING (full history)    │
│  $275M Series G · May 2026 │
│  SoftBank · General Atl.   │
│                            │
│  $300M Series F · Jun 2024 │
│  SoftBank · Prosus         │
│                            │
│  $570M Series E · Sep 2021 │
│  Fidelity · B Capital      │
│  See all 8 rounds →        │
│                            │
│  ──────────────────────    │
│  COMPANY                   │
│  Employees       15,000+   │
│  Stage           Series G  │
│                            │
│  ──────────────────────    │
│  KEY PEOPLE                │
│  Vidit Aatrey · CEO        │
│  Sanjeev Barnwal · CTO     │
│  Past: IIT-D · InMobi      │
│                            │
│  ──────────────────────    │
│  SIGNALS                   │
│  Employee growth: +18% YoY │
│  Hiring velocity: 87/mo    │
│  Traffic trend: +12% MoM   │
│                            │
│  ──────────────────────    │
│  SIMILAR COMPANIES         │
│  Snapdeal · Limeroad · Roposo│
│                            │
│  ──────────────────────    │
│  FINANCIALS / MCA       🔒 │
│  P&L · Balance sheet ·     │
│  Revenue · Cash flow       │
│                            │
│  CAPTABLE & VALUATIONS  🔒 │
│                            │
│  ENHANCED SIGNALS       🔒 │
│  Competitive intel ·       │
│  Tech stack · Cap est.     │
│                            │
│  ──────────────────────    │
│  INC42 COVERAGE  (24)      │
│  · Meesho raises $275M     │
│    Series G · 2h ago       │
│  · Meesho FY26 revenue     │
│    breakdown · 6d ago      │
│  · Can Meesho beat Amazon  │
│    in Bharat? · 18d ago    │
│  See all 24 →              │
│                            │
├────────────────────────────┤
│  Brief  Explore  [☆]  ≡   │
└────────────────────────────┘
```

- **\[+ Track\]** in the header: primary CTA. Adds entity to watchlist; affects brief ranking \+ push tier 1\. Shows \[✓ Tracking\] for tracked entities.  
- **Coverage section**: Inc42 editorial only. Shows 3 most recent articles with this entity \+ "See all" link. Tap → Article Reader.

**v1.0 field-level free/🔒 split** *(mirrors Datalabs web tier — see `datalabs-gtm/strategy/current/free-pro-feature-matrix-apr-2026.md`)*:

| Field | App v1.0 | Datalabs web equivalent |
| :---- | :---- | :---- |
| Sector, sub-sector, location, founded year | ✅ Free | Anonymous |
| Website, social links | ✅ Free | Anonymous |
| Company description | ✅ Free | Anonymous |
| **Full funding round history** (all rounds, dates, amounts, stages, investors, leads) | ✅ Free | Anonymous |
| Key people — names \+ titles | ✅ Free | Anonymous |
| Key people — education \+ work history | ✅ Free | Registered Free |
| Employee count band | ✅ Free | Registered Free |
| **Signals** — funding recency, last round date, employee growth %, hiring velocity, traffic trend, app reviews | ✅ Free | Registered Free |
| Similar companies | ✅ Free | Registered Free |
| Financials / MCA (P\&L, balance sheet, revenue, cash flow) | 🔒 *(no public tier name in v1.0 UI)* | Pro only |
| Captable & Valuations | 🔒 *(no public tier name in v1.0 UI)* | Pro only |
| Enhanced signals (cap table estimates, tech stack, competitive intel) | 🔒 *(no public tier name in v1.0 UI)* | Pro only |
| Person & Investor profiles — full portfolio, co-investors, thesis | ✅ Free | Registered Free |

**Why mirror Datalabs web tier**: a Datalabs free user on the web and an Inc42 Brief app user should see the same depth on the same entity. Inconsistency would break trust ("the app is stingier than the website"). Pro-only fields stay Pro-only.

**Gating UX in v1.0** (Apple-safe — see §10 for compliance reasoning): 🔒 fields are visible (so users see the depth that exists) but tapping them surfaces a generic **"Deeper Datalabs depth is coming — notify me when ready"** bottom sheet. **No mention of "Pro," "Premium," "Subscribe," or pricing in v1.0** to avoid App Store rejection risk. This is feature-interest capture, not subscription marketing. v1.1 activates the conversion path with Apple IAP.

**v1.0 deliberately out of scope from Datalabs web**: credits-based actions (basic profile export, full profile export, contact reveals, MCA downloads). These are web-workflow features, not consumption features. They stay on the web for v1.0.

---

### Profile tab

```
┌────────────────────────────┐
│ 9:41                       │
├────────────────────────────┤
│  [U]  Utkarsh              │
│  Founder · D2C, Fintech    │
│                            │
│  ──────────────────────    │
│  BOOKMARKS  (14)           │
│  ┌──────────────────────┐  │
│  │ Why India's OTT      │  │
│  │ market is splitting  │  │
│  │ Feature · May 14     │  │
│  └──────────────────────┘  │
│  ┌──────────────────────┐  │
│  │ Zepto dark store     │  │
│  │ economics, explained │  │
│  │ Report · May 12      │  │
│  └──────────────────────┘  │
│                            │
│  ──────────────────────    │
│  PREFERENCES               │
│  My role        Founder ▸  │
│  My sectors   D2C, SaaS ▸  │
│  Push alerts      On   ▸   │
│  Brief time    7:30 AM ▸   │
│                            │
│  ──────────────────────    │
│  ACCOUNT                   │
│  utkarsh@inc42.com         │
│  Sign out                  │
│                            │
├────────────────────────────┤
│  Brief  Explore  ☆  [≡]  │
└────────────────────────────┘
```

- **Bookmarks**: all saved articles, recency-sorted. Tap → Article Reader.  
- **Preferences**: role and sectors are editable post-onboarding — users aren't locked into their initial setup choices.  
- **Brief time**: user can shift the morning push delivery window (e.g., 7 AM vs 8 AM vs 9 AM).

---

### Push permission bottom sheet (post-first-brief)

Appears after the user reads their first brief (scrolls to last card or spends \>60 seconds).

```
┌────────────────────────────┐
│  (brief cards dimmed       │
│   behind the sheet)        │
│                            │
│                            │
│                            │
│                            │
│                            │
├────────────────────────────┤
│                            │
│  Get notified when         │
│  something moves for       │
│  Meesho or Zepto.          │
│                            │
│  ┌──────────────────────┐  │
│  │  Turn on notifications│  │
│  └──────────────────────┘  │
│                            │
│         Not now            │
│                            │
└────────────────────────────┘
```

- **Uses actual entity names** from the user's watchlist — makes the ask specific, not generic.  
- **"Not now"**: dismisses the sheet. Not prompted again for 7 days.  
- This pre-permission screen precedes the native iOS OS dialog — improving opt-in rate vs asking the OS dialog cold.

---

## 7\. Onboarding and Auth

### Philosophy

Show value before asking for anything. Get the user to see what the brief looks like before they've done any work. Then ask for just enough to personalize the first brief (role \+ 3 entity seeds minimum). Then authenticate to save preferences. Then deliver the first brief. Push permission comes after the first brief — not before.

**Why push permission is last**: iOS push opt-in averages 43.9%. Pre-permission screens that demonstrate value first get \~30% higher opt-in. A push ask before the user has experienced a single brief is a wasted ask.

### 6-step flow (with wireframes)

---

**Step 1 — Value primer**

```
┌────────────────────────────┐
│           Inc42            │
├────────────────────────────┤
│                            │
│  Your morning brief for    │
│  India's startup economy.  │
│                            │
│  ┌──────────────────────┐  │
│  │  SAMPLE BRIEF        │  │
│  │                      │  │
│  │ ■ Meesho raises $275M│  │
│  │   Series G · 2h ago  │  │
│  │                      │  │
│  │ ■ Cabinet clears new │  │
│  │   semicon policy     │  │
│  │                      │  │
│  │ [D] Zepto: 200 new   │  │
│  │   dark stores in Apr │  │
│  │                      │  │
│  │   + 5 more stories   │  │
│  └──────────────────────┘  │
│                            │
│  Your version will be      │
│  personalized for your     │
│  sector and the companies  │
│  you track.                │
│                            │
│  ┌──────────────────────┐  │
│  │   Build my brief →   │  │
│  └──────────────────────┘  │
│                            │
└────────────────────────────┘
```

No input required. Pure show-don't-tell. Establishes what the app is before asking the user to do any work.

---

**Step 2 — Role**

```
┌────────────────────────────┐
│    Inc42        ○●○○○      │
├────────────────────────────┤
│                            │
│  What best describes       │
│  your role?                │
│                            │
│  ┌──────────────────────┐  │
│  │  Founder             │  │
│  │  Building a startup  │  │
│  └──────────────────────┘  │
│  ┌──────────────────────┐  │
│  │  Investor            │  │
│  │  VC, angel, family   │  │
│  │  office              │  │
│  └──────────────────────┘  │
│  ┌──────────────────────┐  │
│  │  Operator            │  │
│  │  Product, marketing, │  │
│  │  ops at a startup    │  │
│  └──────────────────────┘  │
│  ┌──────────────────────┐  │
│  │  BD & Partnerships   │  │
│  │  Sales, partnerships,│  │
│  │  biz dev             │  │
│  └──────────────────────┘  │
│  ┌──────────────────────┐  │
│  │  Something else      │  │
│  └──────────────────────┘  │
│                            │
│           Skip →           │
└────────────────────────────┘
```

Five options — not four. See the "Something else" path below. Skip defaults to Founder mode.

---

**Step 2b — "Something else" sub-screen** *(shown only if "Something else" is selected)*

```
┌────────────────────────────┐
│  ←   Inc42      ○●○○○     │
├────────────────────────────┤
│                            │
│  How would you describe    │
│  your role? (optional)     │
│                            │
│  ┌──────────────────────┐  │
│  │  e.g. Journalist,    │  │
│  │  Analyst, Consultant │  │
│  │  [________________]  │  │
│  └──────────────────────┘  │
│                            │
│  What do you follow most?  │
│  (pick up to 3)            │
│                            │
│  ┌───────┐ ┌────────┐ ┌──┐ │
│  │Funding│ │  M&A   │ │✓ │ │
│  └───────┘ └────────┘ └──┘ │
│  ┌──────┐ ┌────────┐ ┌───┐ │
│  │Policy│ │Sectors │ │IPO│ │
│  └──────┘ └────────┘ └───┘ │
│  ┌──────────┐ ┌──────────┐ │
│  │Regulatory│ │ Deeptech │ │
│  └──────────┘ └──────────┘ │
│                            │
│  You'll get the same       │
│  personalized brief —      │
│  ranked by your topics and │
│  companies you track.      │
│                            │
│  ┌──────────────────────┐  │
│  │      Continue →      │  │
│  └──────────────────────┘  │
└────────────────────────────┘
```

**"Something else" handling**: for users who don't fit the four defined segments (journalists, analysts, consultants, researchers, government officials, service providers, students). They get:

- Optional free-text role description (stored for future segmentation research — not used to change the brief in v1.0)  
- Topic-interest multi-select (same chips as Step 3, shown here instead)  
- Brief personalized by topic chips \+ watchlist seeds — same algorithm as the four segments, just without a segment-specific filter mode  
- The note "You'll get the same personalized brief" sets the right expectation

"Something else" users skip Step 3 (topics already collected) and go straight to Step 4 (watchlist seed).

---

**Step 3 — Topics** *(skipped for "Something else" users — topics collected in Step 2b)*

```
┌────────────────────────────┐
│    Inc42        ○○●○○      │
├────────────────────────────┤
│                            │
│  Which sectors do you      │
│  follow?  (up to 5)        │
│                            │
│  ┌──────┐ ┌───────┐ ┌───┐  │
│  │✓ D2C │ │Fintech│ │ EV│  │
│  └──────┘ └───────┘ └───┘  │
│  ┌──────┐ ┌───────┐ ┌────┐ │
│  │ SaaS │ │EdTech │ │Health│
│  └──────┘ └───────┘ └────┘ │
│  ┌───────┐ ┌──────┐ ┌────┐ │
│  │Gaming │ │Retail│ │Deep│ │
│  └───────┘ └──────┘ └────┘ │
│  ┌──────────┐ ┌──────────┐ │
│  │ AgriTech │ │Logistics │ │
│  └──────────┘ └──────────┘ │
│                            │
│  1 of 5 selected           │
│                            │
│  ┌──────────────────────┐  │
│  │      Continue →      │  │
│  └──────────────────────┘  │
│           Skip             │
└────────────────────────────┘
```

Role-adaptive chips: Investors see sectors \+ deal stages. Operators see function areas (Product, Marketing, Engineering, Finance).

---

**Step 4 — Watchlist seed** *(1 required, 3 recommended)*

```
┌────────────────────────────┐
│    Inc42        ○○○●○      │
├────────────────────────────┤
│                            │
│  Track companies and       │
│  founders you care about.  │
│                            │
│  ┌──────────────────────┐  │
│  │ 🔍 Search companies…  │  │
│  └──────────────────────┘  │
│                            │
│  ┌──────────────────────┐  │
│  │ [M] Meesho     ✓  ╳  │  │
│  └──────────────────────┘  │
│                            │
│  ●○○  1 added · 3 recommended│
│                            │
│  SUGGESTED FOR YOU         │
│  ┌──────────────────────┐  │
│  │ [Z] Zepto         [+]│  │
│  └──────────────────────┘  │
│  ┌──────────────────────┐  │
│  │ [R] Razorpay     [+] │  │
│  └──────────────────────┘  │
│  ┌──────────────────────┐  │
│  │ [K] Khatabook    [+] │  │
│  └──────────────────────┘  │
│  ┌──────────────────────┐  │
│  │ [S] Shiprocket   [+] │  │
│  └──────────────────────┘  │
│                            │
│  ┌──────────────────────┐  │
│  │      Continue →      │  │
│  └──────────────────────┘  │
│ Skip — get a general brief │
└────────────────────────────┘
```

- **Soft gate** (Council revision): 1 entity required to proceed; 3 recommended for best personalization. Forced 3-seed gates have been shown to drop completion 15–25% at this funnel step without proportional retention benefit — users who voluntarily add 3 seeds are already more engaged than those forced to.  
- **Search-as-you-type** from Datalabs entity model (70K+ companies, founders, funds).  
- **Suggested entities**: role-adaptive. Founders see peer-stage \+ peer-sector companies. Investors see sector-relevant companies. "Something else" users see top-followed entities in their selected topics.  
- **"Skip — get a general brief"**: visible as a small secondary action. Users who skip get a brief ranked purely by their role \+ topic selections from Steps 2–3, no watchlist boost. Triggers a stronger in-app nudge to add entities after Day 1\.  
- **Track skip rate in pilot**: if skip rate \>30% AND skipped-users retention \<50% of non-skipped users at D30 → consider strengthening the recommendation (more aggressive suggestion engine, not a hard gate).

---

**Step 5 — Auth**

```
┌────────────────────────────┐
│    Inc42        ○○○○●      │
├────────────────────────────┤
│                            │
│  Save your setup.          │
│                            │
│  Sign in to get your       │
│  personalized brief        │
│  across devices.           │
│                            │
│  ┌──────────────────────┐  │
│  │  Sign in with Apple  │  │
│  └──────────────────────┘  │
│  ┌──────────────────────┐  │
│  │  Sign in with Google │  │
│  └──────────────────────┘  │
│  ┌──────────────────────┐  │
│  │ Continue with LinkedIn│  │
│  └──────────────────────┘  │
│  ┌──────────────────────┐  │
│  │  Phone (OTP)         │  │
│  └──────────────────────┘  │
│                            │
│   Continue without account │
│                            │
│  By continuing you agree   │
│  to our Terms & Privacy.   │
│                            │
└────────────────────────────┘
```

- **Position B** (after setup, before first brief): user has psychological sunk cost from 3-seed setup and is motivated to save it.  
- **Sign in with Apple**: required on iOS when any social sign-in option is offered (App Store mandate).  
- **"Continue without account"**: small text link below primary buttons — available but not prominent. Local storage preserves onboarding choices for Session 1; cross-device sync requires account.  
- **No email \+ password**: reduces friction and security surface in v1.0.

---

**Step 6 — First brief (earned)**

```
┌────────────────────────────┐
│ 7:32 AM        Fri, May 16 │
├────────────────────────────┤
│  YOUR BRIEF   ●○○○○○○○    │
│  Personalized for Founder  │
│  Tracking: Meesho, Zepto…  │
│                            │
│  ┌──────────────────────┐  │
│  │ ■ BREAKING NEWS      │  │
│  │                      │  │
│  │ Meesho raises $275M  │  │
│  │ Series G at $4.9B    │  │
│  │ valuation            │  │
│  │                      │  │
│  │ "This matters for D2C│  │
│  │ founders: a new val  │  │
│  │ floor for Series E+  │  │
│  │ companies…"  ▸ More  │  │
│  │                      │  │
│  │ Because you track:   │  │
│  │ Meesho               │  │
│  └──────────────────────┘  │
│                            │
│  ┌──────────────────────┐  │
│  │   + 7 more stories   │  │
│  └──────────────────────┘  │
│                            │
├────────────────────────────┤
│ [Brief]  Explore  ☆   ≡  │
└────────────────────────────┘
```

Delivered immediately after auth. Full-screen Morning Mode. Subtitle "Personalized for \[Role\] · tracking \[entity1\], \[entity2\]…" is the only onboarding reminder — no overlays, no tutorial tooltips. The brief IS the onboarding.

---

### Push permission — post-first-brief

See the Push permission bottom sheet wireframe in §6. Triggered after the user scrolls to the last brief card or spends \>60 seconds reading.

---

## 8\. Feature Scope

### v1.0 hard scope — 7 features

*(Datalabs Entity Profiles restored to v1.0 per user discretion — preserves investor-segment differentiation at launch. Council had recommended cutting this to v1.1; trade-off accepted in exchange for stronger Datalabs visibility at launch and a fuller Explore/Companies surface. Subject to eng-leadership timeline confirmation at the build planning call.)*

| \# | Feature | What it does |
| :---- | :---- | :---- |
| 1 | **Morning Brief** | 6–8 item finite daily brief. Mon–Fri daily \+ Sat weekly recap \+ Sun off. Segment-filtered, watchlist-ranked. Editorial items \+ Datalabs signal cards. "Because you track: \[X\]" on every watchlist-attributed card. Per-card **Dismiss** ("not interested in this") action surfaces personalization signal. Brief ends — no infinite scroll below the last card. |
| 2 | **Push tiers** | Must-know stream (breaking deals, policy; segment-tiered cadence) \+ brief push (7–8 AM daily). Hard cap 3/day. "Because you track X" attribution on all watchlist pushes. Push permission asked post-first-brief. |
| 3 | **Article Reader** | Full in-app article reading. Progress bar, bookmark, share, related stories at end. Not a deep-link to inc42.com. |
| 4 | **Explore \+ Search** | Three-way content-type switch (Articles / Companies / Reports). Articles: Inc42 corpus archive (filter bar \+ topic chips \+ opt-in watchlist filter). Companies: Datalabs entity universe browse (sector/stage/region filters \+ sort). Reports: deep dives \+ Datalabs reports. Today's Datalabs signals strip (daily aggregates) at top. Full-text search across articles \+ Datalabs entities. Recently viewed at bottom. Pull-only — user navigates here deliberately. |
| 5 | **Watchlist \+ Progressive Profiling** | 6-step onboarding (§7 above; 1 required / 3 recommended on seed step). In-product: add/remove entities anytime via search. Drives brief ranking \+ push tier 1\. Tap entity → opens full Datalabs entity profile (feature \#7). |
| 6 | **Bookmarks** | Single-tap save from brief cards, library cards, article reader. Persisted to account (or local storage for anon users). Accessible from Profile tab. |
| 7 | **Datalabs Entity Profiles** | Per-entity profile pages: sector, stage, latest funding round, key investors, employee/revenue bands, Inc42 coverage section. Free-tier fields visible; deeper fields (full funding history, captable, exec movements, granular revenue) shown with 🔒 \+ "Premium" tag but **conversion path dormant in v1.0** (no paywall, no Plus signup). Tier-flag is rendered, monetization is not yet activated. \~70K entities covered (companies, founders, funds). Accessible from Watchlist tap, Explore Companies browse, brief Datalabs signal cards, search results, and in-article entity tags. |

### v1.1 stretch goals \+ deferred features

| Feature | Origin | Condition |
| :---- | :---- | :---- |
| **Premium activation on Datalabs profiles** | v1.0 ships profile UI with 🔒 gates; v1.1 activates conversion path | The deepest profile fields (full funding history, captable, exec movements, granular revenue) are already gated visually in v1.0 but the upgrade flow is dormant. v1.1 activates the conversion path (paywall flow, Plus subscription, payment). Premium-boundaries doc to define the exact tier mapping before build kickoff. |
| **Audio — "Listen to today's Brief"** | Always v1.0 stretch | Single TTS-narrated track of the daily brief. One generation/day, cached, background playback, lock-screen controls, variable speed (1.0×–2.0×). \~$0.03/day operating cost. **Council favored promoting this to v1.0** if any stretch ships — reinforces morning ritual; less category risk than partial AI. Decision at build planning. |
| **Ask Inc42 (contextual AI)** | Always v1.0 stretch | Embedded at article footers \+ brief card footers \+ entity profiles. Pre-seeded question suggestions. Rate-capped at 10/day on free tier. *Not* a standalone tab. **Council split on this** — viable but less differentiating than Audio. If AI decode snippet on brief cards is already in v1.0, contextual Ask is a depth extension of an existing feature. |
| **Social curation** | v1.1+ | Curated signal from what India's founders, investors, and ecosystem leaders are discussing. Requires separate social signal pipeline — not in scope for v1.0. |
| **Soft Plus waitlist** *(consider for v1.0)* | Council-flagged opportunity | 3 of 5 council members recommend a lightweight "Inc42 Brief Plus — coming soon" CTA in Profile \+ on premium-adjacent surfaces (e.g., a tappable 🔒 field on entity profiles). Costs \~2 hours of build; captures qualified leads \+ signals roadmap. Not a paywall. Decision at build planning. |

### Explicitly out of v1.0

- Third-party news aggregation (no ET/Mint/external sources — ever)  
- In-app community / discussion threads  
- Peer reaction layer  
- Comp/ESOP signal for Operators  
- Full Signal-style real-time alerting (v1.1 — especially for full-time VC use case)  
- Tiered Plus/Pro monetization (boundaries architected, not activated)  
- Long-form deep dives as a distinct format — stays on web  
- Hard identity verification

---

## 9\. Design Principles

Seven principles from competitive research (FT Edit, Bloomberg, Particle, MoneyControl):

**1\. Finite before infinite** — the app opens to the Morning Brief, not the feed. Discovery (Explore tab) requires a deliberate tab switch. The brief ends with a "Done for today" state, not a continuation. *FT Edit's lesson*: finite framing is a product differentiator, not a limitation.

**2\. Depth on demand — 4 levels of progressive disclosure** — every brief card supports four layers, accessed by choice:

- Headline (always visible)  
- AI decode (tap to expand)  
- Full article (Article Reader modal)  
- Entity layer (Datalabs profile from entity name in article or card)

**3\. Watchlist is the personalization engine, not the algorithm** — no algorithmic feed in v1.0. Personalization is watchlist-driven (explicit entity choices) \+ segment-weighted (role \+ sector at onboarding). The user always understands why a card is in their brief. *Bloomberg's model*: explicit watchlist, not behavioral inference.

**4\. Visible attribution on every personalized card** — "Because you track: \[Company\]" appears only on cards where the user's watchlist influenced ranking. Cards in the brief as top editorial (not watchlist-boosted) don't carry this line. The distinction tells the user both what's personalized and what's considered universally important.

**5\. Signal-dense cards, not image-forward** — the Inc42 audience is scanning for signals, not stories. Brief cards are scannable in 2 seconds: headline \+ category \+ decode snippet \+ attribution. The article reader can be image-forward; the cards should be tight. *Contrast with Particle*: Particle's beautiful image-forward cards work for general news; professional audiences scan faster with text-dense signal cards.

**6\. The article reader must earn its place** — if the in-app reader isn't materially better than inc42.com in Safari, users will bypass the app for reading. "Better" means: faster load, focus mode (no navigation chrome), progress tracking, one-tap bookmark, related articles surfaced at end. Gate v1.0 launch on a reader usability test (≥8/10 from 5 representative users vs the inc42.com mobile baseline).

**7\. Everything is Inc42** — no "3 sources ▾" on cards, no aggregation from external publishers. The "Because you track: \[X\]" attribution replaces the aggregator's "Reuters \+ FT \+ NYT" line. Inc42's value is not that it aggregates — it's that it's the original source and the intelligence layer over it.

---

## 10\. Monetization — Free v1.0, Apple-Safe Feature-Interest Capture

**v1.0 launch**: free, no paywall, no active subscription, no purchase flow.

### Apple App Store compliance — load-bearing constraint

The app cannot promote external paid subscriptions or imply a coming paid product in ways that would trigger App Store rejection. Apple Guideline 3.1.1 (in-app purchase requirement) and 3.1.3 (multiplatform services) constrain how we can talk about future paid features in v1.0. The general rule: **do not name a specific paid tier or product, do not show pricing, do not link to external checkout, do not promote subscription**.

This shapes the v1.0 waitlist design materially: it cannot be a "subscribe to Inc42 Pro" waitlist. It must be **feature interest capture** — collecting signal about which capabilities users want, framed as product feedback rather than pre-purchase. The lead-gen value is preserved (we still know which users want deeper Datalabs); the framing is shifted to stay safely within App Store guidelines.

### The two surfaces, Apple-safe copy

**Trigger 1 — 🔒 field on entity profile** (Financials / Captable / Enhanced Signals):

Tap any 🔒 field → bottom sheet:

```
┌────────────────────────────┐
│         (profile dimmed)   │
│                            │
├────────────────────────────┤
│                            │
│  Deeper Datalabs depth     │
│  is coming.                │
│                            │
│  Financials, captable, and │
│  enhanced signals are part │
│  of what we're building    │
│  next.                     │
│                            │
│  ┌──────────────────────┐  │
│  │  Notify me when ready│  │
│  └──────────────────────┘  │
│                            │
│         Not now            │
│                            │
└────────────────────────────┘
```

**Trigger 2 — Profile tab "Coming soon" row** (renamed from "Upgrade"; reframed as product roadmap):

```
┌──────────────────────────────┐
│  COMING SOON                 │
│  Deeper Datalabs depth,      │
│  advanced alerts, and more.  │
│                  Notify me → │
└──────────────────────────────┘
```

That's the only two surfaces. No upgrade prompts on brief cards, article cards, or Explore feed. No paywall flow, no payment integration, **no mention of "Pro," "Plus," "Premium," "Subscribe," "Pay," "₹/mo," or any specific product name**.

### Banned vocabulary in v1.0 surfaces

The following words and phrases are not used anywhere in the v1.0 UI:

- "Inc42 Pro" / "Inc42 Plus" / "Datalabs Pro" *(as in-app product names)*  
- "Premium" / "Subscribe" / "Subscription" / "Paid"  
- "Unlock with \[tier\]" / "Upgrade for \[features\]"  
- Any price disclosure (₹1,499/mo etc.)  
- Any link to external checkout (web subscription page)

### Allowed framing in v1.0 surfaces

- "Coming soon"  
- "We're building" / "Coming next"  
- "Notify me when ready"  
- "More depth coming" / "Deeper Datalabs"  
- 🔒 icon as visual treatment *(common pattern across apps; not a payment signal on its own)*  
- Generic "more features" language

### Tier-flag architecture (unchanged, but private)

Every v1.0 feature/field still ships with a `tier` flag in the data model (`free` / `plus` / `pro`). The flag is private — used for rendering 🔒 visual treatment, but no public UI mentions tier names. v1.1+ activation makes the tier flags meaningful in the UX (paywall flow, pricing, sign-in entitlement check).

### v1.1 activation — Apple IAP required for in-app subscription

When monetization activates in v1.1+:

- **The in-app subscription must use Apple In-App Purchase (IAP) for iOS**, not external web checkout. This is Apple's hard requirement. Plan pricing accordingly (Apple takes 15–30%; the in-app price may differ from web).  
- **The web Datalabs Pro subscription continues separately**. Users who subscribed via the web sign in to the app and get their entitlements via the reader-app exception (App Store Guideline 3.1.3(b)). This is allowed.  
- **No external-link entitlement** for v1.1 unless we've evaluated the 27% Apple take \+ linking requirements; default to pure IAP for simplicity.  
- **Combined Pro/Plus brand** for the in-app tier is still TBD at v1.1 activation — could be "Inc42 Pro" (single brand, simpler), "Datalabs Pro" (continuity with web), or a new app-specific brand. Decide at v1.1 design phase.

### Why this framing protects the v1.0 launch

Three reasons the Apple-safe approach is the right v1.0 design:

1. **App Store review risk is asymmetric**: a single rejection delays launch by 1–4 weeks for resubmission. The cost of saying "Inc42 Pro coming soon" with pricing is far higher than the small lead-gen lift from naming the tier.  
2. **Lead-gen value is preserved**: users who tap "Notify me" on Financials/Captable still surface their high-intent signal. The waitlist queue still works. Only the framing changes.  
3. **Cross-product reader-rule is preserved**: when a web Datalabs Pro user installs the app, their entitlements work (they sign in, app honors). v1.0 doesn't need to mention this explicitly — it just works.

### Lead capture mechanics (unchanged)

For both surfaces, "Notify me" creates a single record per user:

- User ID (or anon device ID for "Continue without account")  
- Source (`field_lock_financials` / `field_lock_captable` / `field_lock_enhanced_signals` / `profile_row`)  
- Timestamp  
- Email (existing if authed; prompted in an expanded bottom sheet if anonymous)

Source tagging lets v1.1 segment the waitlist: `source=field_lock_*` users are high-intent (tapped a specific field); `source=profile_row` users are general-interest. Different conversion offers when monetization activates.

### Full spec ownership

`premium-boundaries.md` to update before build kickoff with:

- The seven-feature v1.0 \+ free/🔒 field map (per §6)  
- The Apple-safe feature-interest capture mechanics (copy, triggers, dismiss cadence)  
- The v1.1 IAP commitment \+ reader-rule entitlement bridge to web Pro

---

## 11\. Success Metrics \+ Behavioral Validation Gates

### North-star metric

**D30 retention of weekly active users.**

A user is *retained at D30* if they had ≥1 session in days 0–30 AND ≥1 session in days 21–30 (recency filter removes dabblers).

**Target**: ≥15% D30 retention sustained at the 90-day checkpoint.

Benchmark: FT Edit's retention curve — publicly cited as a retention breakthrough in financial-content apps. News/content apps are at the lower end of the industry distribution. Sticky exceptions (Bloomberg, FT, MoneyControl) earn retention through habitual push cadence, personalization, paywall lock-in, and cross-surface integration. Inc42's equivalent: push discipline \+ watchlist personalization \+ finite framing.

---

### Pre-launch baselines (pilot cohort, \~50–200 users)

Run for 2 weeks minimum before public launch. If these miss, fix before launching — don't launch with broken activation.

| Metric | Target |
| :---- | :---- |
| Pilot install rate (% of invitees who install) | ≥60% |
| Onboarding completion (Steps 1→6) | ≥80% |
| Watchlist completion (≥3 seeds added) | ≥40% |
| Push opt-in (system permission granted) | ≥60% |
| Day 1 return rate | ≥70% |
| Crash-free session rate | ≥99% |

---

### 30-day post-launch thresholds

| Metric | Pass | Soft-fail | Hard-fail |
| :---- | :---- | :---- | :---- |
| **D7 retention** (≥1 session in days 4–7) | ≥30% | 20–30% | \<20% |
| **D30 retention** (per north-star definition) | ≥15% | 10–15% | \<10% |
| **Push opt-in rate** | ≥55% | 40–55% | \<40% |
| **Watchlist completion** (≥3 seeds at onboarding) | ≥30% | 20–30% | \<20% |
| **Brief completion** (≥3 of 6–8 cards opened per session) | ≥40% | 25–40% | \<25% |
| **Article reader sessions per DAU** | ≥0.5 | 0.3–0.5 | \<0.3 |
| **Datalabs entity profile views per DAU** *(restored to v1.0)* | ≥0.3 | 0.15–0.3 | \<0.15 |
| **Explore Companies browse engagement** (% of Explore sessions that switch to Companies tab) | ≥15% | 8–15% | \<8% |
| **Bookmark rate** (≥1 bookmark per 5 brief sessions) | ≥20% | 10–20% | \<10% |
| **Dismiss rate per brief session** *(Council-driven addition)* | 1–3 per session | \<1 or \>5 | \>7 (signal noise) |
| **Onboarding completion** (Steps 1→6, with new soft seed gate) | ≥75% | 60–75% | \<60% |
| **Crash-free session rate** | ≥99.5% | 99–99.5% | \<99% |
| **Push CTR** | 3–7% | 1–3% | \<1% |

**Pass on all** → continue to 60-day checkpoint with no scope changes. **Any soft-fail** → diagnose \+ iterate; decision at 60-day checkpoint. **Any hard-fail** → see kill criteria below.

---

### 60-day checkpoint

| Metric | Pass | Soft-fail | Hard-fail |
| :---- | :---- | :---- | :---- |
| **D60 retention** (≥1 session in days 51–60) | ≥10% | 7–10% | \<7% |
| **Explore-to-brief ratio** (% of sessions with both a brief read AND an Explore visit) | ≥20% | 10–20% | \<10% |
| **Search queries per DAU** | ≥0.3 | 0.1–0.3 | \<0.1 |
| **"Continue without account" → full auth conversion** (% of anon users who create account within 7 days) | ≥50% | 30–50% | \<30% |
| **Watchlist depth growth** (% of users with ≥5 seeds, up from ≥3 at onboarding) | ≥40% | 25–40% | \<25% |
| **Push fatigue** (% of users who muted ≥1 alert tier) | ≤15% | 15–25% | \>25% |
| **Article reader sessions per DAU** (updated target) | ≥1.0 | 0.5–1.0 | \<0.5 |

**Pass on all** → on track for 90-day go. **Soft-fail** → calibrate before 90-day. **Hard-fail on push fatigue** → reduce default push cadence by 33%, re-test.

---

### 90-day go / no-go

The decisive checkpoint. Outcome determines v2 commissioning, Plus tier activation, and v1.1 sequencing.

| Metric | Pass (v2 go) | Re-scope | Kill |
| :---- | :---- | :---- | :---- |
| **D30 retention sustained** (rolling 30-day window) | ≥15% | 10–15% | \<10% |
| **Push opt-in sustained** (new \+ existing users) | ≥55% | 40–55% | \<40% |
| **D90 retention** (≥1 session in days 81–90) | ≥7% | 4–7% | \<4% |
| **MAU growth** (month-over-month) | Positive | Flat | Negative |

**Pass on all** → green-light v2 \+ Plus tier activation review. **Re-scope** (1–2 metrics in range) → 30-day v1.1 fix cycle on specific metric; re-evaluate at 120-day. **Kill** (any 1+ metric in kill range) → halt v2 work; deep architectural review; consider Signal pivot or sunset.

---

### Counter-metrics (must NOT degrade during rollout)

These track cannibalization of Inc42's existing owned channels.

| Counter-metric | Acceptable | Trigger |
| :---- | :---- | :---- |
| **Newsletter open rate** (Inc42 editorial) | ≥90% of pre-launch baseline; \-10% tolerable at 90 days | \<80% baseline at 90 days → app is cannibalizing newsletter |
| **Web sessions** (inc42.com) | ≥95% of pre-launch baseline | \<90% baseline at 90 days → SEO traffic erosion |
| **Plus subscription pace** (existing Inc42 Plus on web) | Stable or growing | Decline → brand/pricing confusion (app is free, Plus exists on web) |
| **Datalabs Pro revenue** | Stable or growing | Decline \>5% sustained → app leaking premium-like features for free |

---

### Pivot signals

| Signal | v1.1 action |
| :---- | :---- |
| **Investor segment retention \>30% above Founder retention at 90 days** | Accelerate Signal layer: full real-time alerting \+ investor workflows |
| **Brief-only sessions \>60% of active users at Day 60** | Two options: (a) investigate Explore/Reader friction, or (b) accept Brief-only as the winning product and deprioritize Explore in v1.1 |
| **Tap-to-decode usage \>30% of stories** *(if Ask Inc42 in v1.0)* | Expand Scout action set (add `landscape`, `compare` actions) |
| **"Listen to today's Brief" usage \>40% WAU at 60 days** *(if audio in v1.0)* | Fast-track per-story audio narration in v1.1 |
| **Watchlist completion \>60% at onboarding** | Consider expanding free-tier watchlist depth before Plus activation |
| **Push fatigue (mute rate) \>15%** | Reduce default cadence; test "because you track X" attribution copy variants |
| **Operator segment retention \<8% at 90 days** | Cut Operators-mode polish from v1.1; reallocate to Founders \+ Investors deepening |
| **BD segment retention \<5% at 90 days** | Cut BD-mode polish from v1.1; consider separate B2B service-provider product |

---

### Kill criteria (explicit triggers)

1. **D30 retention \<10% sustained for 4+ weeks** → halt new feature work; investigate hero-job dilution ("nice but unnecessary" failure mode)  
2. **Push opt-in \<40% AND watchlist completion \<20% simultaneously** → onboarding flow is failing; redesign before any v1.1 work  
3. **Newsletter open rate \<80% AND web sessions \<90% simultaneously** → app is net-cannibalizing existing channels; halt and reassess strategic value  
4. **Datalabs Pro revenue decline \>5% sustained** → premium boundary bleed; revisit `premium-boundaries.md` and tighten free tier  
5. **≥3 of 4 segments fail D30 retention 10%** → product-market fit is segment-specific; consider Signal pivot for Investors, sunset for others

Kill ≠ shutdown. Kill \= halt new investment \+ decide between Signal pivot, segment-specific re-scope, or sunset.

---

### Reporting cadence

| Frequency | Audience | Format |
| :---- | :---- | :---- |
| **Weekly** (during 90-day window) | Eng \+ product \+ Utkarsh | Dashboard refresh; flag any metric crossing soft-fail threshold |
| **30-day, 60-day, 90-day** | Leadership \+ co-founders | Decision memo: pass / soft-fail / hard-fail per metric \+ recommended action |
| **Quarterly post-90** | All stakeholders | Metric trends, pivot signals, v1.1 \+ v1.2 sequencing |

Dashboards: PostHog (or Amplitude — eng leadership choice). Decision memos: markdown docs in `inc42-app/post-launch/`.

---

## 12\. Design Risks

**Risk 1: Two modes → no strong identity**

The app is finite (Morning Brief) and open-ended (Explore). If it can't be described in one sentence, the App Store listing fails and word-of-mouth fails.

*Mitigation*: the positioning test (E / A / F) is specifically designed to find a single sentence that holds for a unified product. "One app, every morning" in Option E is the clearest single-line positioning tested so far. Tab naming ("Today" vs "Brief") matters here — resolve in the test.

**Risk 2: Article Reader doesn't earn its place**

If the in-app Reader isn't materially better than inc42.com on mobile Safari, users will deep-link out. A mediocre reader is worse than no reader — it damages trust in the app's native experience.

*Mitigation*: gate v1.0 launch on a Reader usability test against the inc42.com mobile baseline. If it fails, ship deep-links instead — that's acceptable degradation.

**Risk 3: "Nice but unnecessary" — weak daily habit**

The Morning Brief must be good enough to open every morning. If it isn't, the app falls into the standard 75%-lost-in-3-days retention curve. The app's engineering and design cannot compensate for weak editorial curation.

*Mitigation*: push discipline (3/day cap \+ "because you track X") \+ watchlist personalization \+ finite framing \+ behavioral validation gates at 30 / 60 / 90 days.

**Risk 4: Explore cannibalises the brief's finiteness**

If the Explore tab is easily accessible and algorithmically compelling, users bypass the brief and go straight to the feed. The brief's core promise evaporates.

*Mitigation*: app opens to the brief; Explore requires tab switch; brief ends with "Done for today" state; no "Keep reading" shortcut from the brief end state to the feed.

**Risk 5: Auth friction kills onboarding completion**

Moving auth to Position B (after setup screens) means users who drop during auth have already added watchlist seeds — and those preferences are lost. "Continue without account" preserves the session locally but cross-device sync is gone.

*Mitigation*: "Continue without account" must work well for Session 1 with a non-intrusive "Save your setup" prompt surfaced after Day 1 brief. Local storage of onboarding preferences until account creation removes the sting. Soft seed gate (1 required, 3 recommended) reduces sunk-cost loss if user drops at auth.

**Risk 6: Editorial operations quality is the true execution risk** *(Council-flagged, high consensus)*

The concept assumes a high-functioning daily curation \+ tagging \+ ranking pipeline. Most media organizations fail to sustain this consistently. If entity tagging is inconsistent, "Because you track" attribution becomes noisy and trust collapses fast. If Saturday recap quality is weak, users learn pushes are skippable. If watchlist suggestions are poor, onboarding feels fake-personalized. The product's success is more dependent on editorial operational excellence than on any UX decision.

*Mitigation*: run a 2–3 week **concierge pilot** in parallel with v1.0 build (Council Priority 1 recommendation). 50–100 users, real editorial curation of 6–8 items daily, real entity tagging, real watchlist-ranked output, real push cadence — using internal tools, not the production app. Validates the operational assumption while engineering builds. Define explicit editorial quality thresholds: ≥4 editorial articles \+ ≥2 Datalabs signals required for a brief to ship; below that → brief delayed, supplemented with archive pull, or skipped (no weak briefs).

**Risk 7: Product stops at consumption, doesn't help the user act** *(Council-flagged, medium consensus)*

Every persona hero job ends with "so I can decide / share / ignore" — but the product surfaces are read, save, search, track. No share-with-team affordance, no note-for-later beyond bookmark, no CRM/calendar handoff. The brief informs but doesn't close the loop.

*Mitigation*: v1.0 adds **Dismiss** as the one new action affordance (per-card "not interested" with reason chooser → personalization signal). Share is in the article reader (native share sheet). Bookmark \= note-for-later. Other action affordances (Share with team templated, Track-as-decision, calendar handoff) are deferred to v1.1+ to keep v1.0 scope tight.

**Risk 8: App Store rejection if monetization framing is too aggressive in v1.0**

Apple App Store Guidelines (3.1.1 IAP requirement; 3.1.3 multiplatform services; 3.1.5 external link entitlement) restrict how apps can promote paid subscriptions — especially external (non-IAP) ones. The original combined-waitlist design ("Inc42 Plus/Pro — coming soon; deeper Datalabs at ₹1,499/mo") would likely trigger rejection: it names a specific paid product, hints at pricing, and could be read as promoting an external subscription.

A single rejection delays launch by 1–4 weeks for resubmission and damages timeline confidence with eng leadership.

*Mitigation*: §10 redesigns the waitlist as **feature-interest capture** with Apple-safe copy. Banned vocabulary in v1.0 UI: "Pro," "Plus," "Premium," "Subscribe," "Paid," "Unlock with \[tier\]," pricing, external links. Allowed framing: "Coming soon," "Deeper Datalabs depth," "Notify me when ready," generic 🔒 visual. Lead-gen value preserved; framing shifted to product-feedback register. v1.1 activation uses Apple IAP for in-app subscription; reader-rule exception (3.1.3(b)) covers users who subscribed to Datalabs Pro via web.

*Pre-submission checklist before App Store review*: (1) no banned vocabulary in any v1.0 surface, (2) no external checkout links anywhere, (3) all 🔒 taps go to the feature-interest sheet, never to a purchase flow, (4) screenshots and App Store description follow same framing.

---

**Risk 9: Datalabs Entity Profiles in v1.0 — mostly de-risked, two residual concerns**

The original Council concern was a 4–8 week timeline add \+ data-pipeline readiness for profiles. Both are materially smaller risks than first estimated:

- **Timeline**: \~2–3 weeks of AI-accelerated build, not 4–8 weeks. The Datalabs web product is already live on Next.js with the full profile UI shipped (April 2026 free-default launch). Translation to the app is mostly mobile-shell work \+ responsive adaptation, not net-new UI/data design.  
- **Data pipeline**: not a concern. The web is already serving the free-tier data fields we're mirroring to the app (sector, stage, full funding history, key people, signals, similar companies). Head coverage of the top entities is clean by definition — the web product depends on it.  
- **Entity tagging discipline**: Inc42's editorial team already follows a strong taxonomy with multiple tag dimensions, and the data team recently completed a tagging audit. The "Because you track" attribution \+ Explore Companies browse \+ entity profile coverage section all run on existing, audited tagging infrastructure.

**Two residual concerns to address at build planning:**

1. **Free/🔒 field split must match Datalabs web tier exactly** — Datalabs Free users on the web and Inc42 Brief app users on the same entity must see identical depth. The field-level mapping in §6 captures this; needs Datalabs team sign-off before build kickoff.  
2. **Combined Plus/Pro waitlist mechanics** — the bottom-sheet trigger from 🔒 fields and the Profile tab row need design \+ copy decisions. Low effort, but a v1.0 build item.

---

## 13\. Open Decisions

### Locked (2026-05-16, full 9-persona test \+ LLM Council review)

- ✅ **App name**: Inc42 Brief  
- ✅ **Primary tab label**: "Brief"  
- ✅ **Positioning copy**: Option F — *"Not a newsletter. Not an algorithm. Inc42's journalism, Datalabs intelligence, and AI that explains what it means for you. One app, every morning. Then it ends."*  
- ✅ **Structural copy preservation**: "Then it ends." retained across all marketing surfaces (App Store, onboarding, web hero, ad creative)  
- ✅ **Variants for specific contexts**: Option I reserved for PR/media-trade-press; Option E reserved for formal corporate decks; Inc42 Briefing reserved as brand-portfolio asset for v1.1+ institutional contexts  
- ✅ **Watchlist seed gate softened** (Council): from "3 required" to "1 required, 3 recommended" with skip-to-general-brief path  
- ✅ **Explore → Explore** (Council \+ archive-depth reframe): tab name locked to Explore; framing is "archive surface for \~30K+ articles \+ \~70K entities \+ daily Datalabs signals" — not a leftover-articles feed. Fallback names if Explore reads off in market: Sections → Explore.  
- ✅ **Per-card Dismiss** added (Council): one new action affordance for personalization signal; other actions covered by existing affordances  
- ✅ **Explore content-type switch**: Articles / Companies / Reports at top level (driven by Datalabs profiles being in v1.0)  
- ✅ **Datalabs Entity Profiles in v1.0** (2026-05-17): 7 features total. Field-level free/🔒 split **mirrors Datalabs web tier** (the canonical reference is `datalabs-gtm/strategy/current/free-pro-feature-matrix-apr-2026.md`). All Datalabs-Free fields visible in app; Datalabs-Pro-only fields shown with 🔒 \+ dormant conversion path. Datalabs web is already on Next.js with profiles live → translation to app is \~2–3 weeks of AI-accelerated build.  
- ✅ **Combined Inc42 Plus/Pro waitlist — Apple-safe feature-interest capture** (2026-05-17): replaces standalone "Brief Plus waitlist". Bottom-sheet trigger from 🔒 fields \+ single Profile-tab "Coming soon" row. **No banned vocabulary in v1.0 UI** ("Pro," "Plus," "Premium," "Subscribe," pricing — all out). Lead-gen value preserved; framing shifted to product-feedback register to avoid App Store rejection risk. Full copy spec in §10.  
- ✅ **v1.1 monetization activation \= Apple IAP** (2026-05-17): when paid features activate, in-app subscription uses Apple In-App Purchase (not external web checkout). Web Datalabs Pro subscribers' entitlements honored via reader-rule exception (App Store Guideline 3.1.3(b)). No external-link entitlement in v1.1 unless explicitly evaluated.  
- ✅ **Companies sort default** \= Recently funded \+ largest rounds (composite ranking by recency × round size). No hidden personalization.  
- ✅ **Tab name \= Explore** (user preference, 2026-05-17): most familiar pattern across apps; the archive-surface reframe (not a daily-discovery feed) resolves the Council "hollow" concern without a renamed tab. Fallbacks if pilot signals otherwise: Library, then Sections.

### Pending build planning call

- [ ] **Free/🔒 field split sign-off from Datalabs team**: confirm the app's field map (in §6) mirrors the Datalabs web tier exactly — same depth on the same entity across web and app for a Free user. The mirror is the principle; sign-off is the action.  
- [ ] **App Store pre-submission review**: before submitting v1.0 to App Store review, walk the checklist in Risk 8 — no banned vocabulary, no external checkout links, no purchase flow, screenshots \+ App Store description follow same Apple-safe framing as the in-app surfaces.  
- [ ] **Ask Inc42 in v1.0**: contextual embed at article footer \+ entity profiles — fit in v1.0 build window or defer to v1.1?  
- [ ] **Audio in v1.0**: "Listen to today's Brief" — confirmed feasible (\~$0.03/day); capacity-dependent  
- [ ] **Native vs cross-platform**: eng-leadership call  
- [ ] **Article Reader tech approach**: web-view wrapper vs native vs React Native (note: Datalabs is already Next.js — web-view wrapping for profile pages is the path-of-least-resistance and worth testing first)

### Pending separate work

- [ ] **Concierge pilot of Morning Brief workflow** *(Council Priority 1\)*: 2–3 weeks, 50–100 users, manual editorial curation \+ entity tagging \+ watchlist ranking \+ push cadence using internal tools. **Runs in parallel with v1.0 build**, not as a pre-build gate. Validates the operational assumption while engineering builds. Findings feed v1.0 launch readiness check.  
- [ ] **Investor-tuned F variant**: run a 3-persona quick test (3 Investor personas) on *"Not a newsletter. Not an algorithm. Inc42's journalism, Datalabs intelligence, and AI that explains what each deal means for your portfolio. One app, every morning. Then it ends."* before committing to investor-acquisition channels (LinkedIn ads to VCs, LP communications)  
- [ ] **Brief vs Briefing brand-portfolio note**: 1-page doc defining when each is used (Brief \= product name; Briefing \= institutional voice in copy for v1.1+ Pro tier, B2B outreach, PR-to-trade-press)  
- [ ] **Premium boundaries for unified app**: `premium-boundaries.md` needs an update for Article Reader, Search, Explore, and (now v1.1) Datalabs Entity Profile tier decisions  
- [ ] **Saturday weekly recap workflow**: confirm editorial team's curation process and capacity for the Sat brief format before committing to the model  
- [ ] **Editorial quality threshold rules**: explicit "minimum brief quality" rules — e.g., ≥4 editorial articles \+ ≥2 Datalabs signals required to ship; below threshold → delay / supplement / skip. Prevents "weak brief on slow days" failure mode.

### Parked for future session

- [ ] **Creative name re-exploration**: Brief is locked for v1.0; the creative-naming brainstorm (Crux / Lore / Chai / others) is parked. Revisit if a name change makes strategic sense post-launch or if the audience signals dissatisfaction with "Brief" specifically. Brainstorm and pattern analysis preserved in `brainstorm-name-and-positioning.md`.

---

## 14\. What's Needed to Commit to Build

### From co-founders / leadership

- [ ] Concept sign-off (yes / no / needs-discussion)  
- [ ] 9-persona positioning test authorization  
- [ ] Pilot cohort identification (50–200 users across segments for pre-launch baselines)  
- [ ] Build commitment \+ timeline authorization (post-concept lock)

### From eng leadership

- [ ] Native vs cross-platform stack decision  
- [ ] Build cost/time estimate for 7 features \+ 4-tab IA  
- [ ] Stretch goal scope confirmation (Ask Inc42 \+ Audio — in v1.0 or v1.1?)  
- [ ] Article Reader tech approach sign-off  
- [ ] Instrumentation review of event taxonomy in `success-metrics-and-kill-criteria.md`

### From editorial (Pooja \+ pilot editors: Vinai, Nikhil, Shishir)

- [ ] **Run the concierge pilot in parallel with build** *(Council Priority 1\)*: 2–3 weeks, 50–100 users, real curation \+ tagging \+ ranking \+ push using internal tools — validates the operational pipeline while engineering builds  
- [ ] Brief curation rhythm commit — daily 6–8 stories, segment-personalized, by 7 AM IST  
- [ ] Saturday weekly recap format — curation process for the week-in-review brief  
- [ ] Push-tier curation criteria — must-know vs nice-to-know rules per segment  
- [ ] Article → entity tagging discipline for watchlist personalization quality  
- [ ] **Editorial quality thresholds**: define "minimum viable brief" rules (≥4 editorial \+ ≥2 Datalabs signals to ship; below \= delay / supplement / skip)

### From Datalabs team

- [ ] **Field map sign-off**: confirm app v1.0 free/🔒 split (§6) matches Datalabs web tier exactly. Reference: `datalabs-gtm/strategy/current/free-pro-feature-matrix-apr-2026.md` (April 2026 launch matrix).  
- [ ] **App-side API access**: web is on Next.js with profiles live; confirm the same data layer is reachable from the app (web-view wrap is the path-of-least-resistance, but native fetches need API endpoint exposure).  
- [ ] **Deal trigger latency SLA for push tier 1** (signal → push within X minutes).  
- [ ] **v1.1 conversion-path activation plan**: when profiles' 🔒 fields unlock to a Datalabs Pro paywall in the app — coordinate sequencing with `datalabs-gtm/` Pro tier app-side roadmap.

*(Note: entity tagging discipline and head-entity coverage are NOT open items — Inc42 editorial already follows a strong multi-taxonomy tagging system, and the data team recently completed a tagging audit. Both are pre-validated.)*

### From Ask Inc42 team — only if Ask in v1.0

- [ ] Inc42 Scout `ask` action API for contextual article footer embed  
- [ ] Cost economics review at the planned rate-cap (10 decode-taps/day free tier)

---

## 15\. Validation Evidence

### Research

- `research/01-audience-and-market.md` — audience JTBD synthesis, 4 segments  
- `research/02-adjacent-products.md` — competitive teardown: Bloomberg, FT Edit, MoneyControl, Particle, Crunchbase, LinkedIn  
- `research/03-ecosystem-inventory.md` — Inc42 surface inventory \+ feature-to-surface mapping  
- `research/content-volume-audit-30d-actual.md` — WordPress REST API audit: 338 articles / 30 days \= 11.3/day

### Persona tests (6 rounds)

| Test | What it validated |
| :---- | :---- |
| 2026-05-inc42-app-concept | Sub-brand name, positioning baseline |
| 2026-05-inc42-brief-rewrite | Positioning Candidate A (Differentiation 8.56 vs 4.33 baseline) |
| 2026-05-inc42-brief-segment-hero-jobs | Per-segment hero jobs (Investors 8.03, Operators 7.65, BD 7.90) |
| 2026-05-inc42-app-version-shootout | 4-way head-to-head: Brief wins consensus as spine |
| 2026-05-inc42-app-unified-positioning | 3-persona quick test: Option E wins (8.24/10, unanimous); Option D (platform framing) eliminated (5.23/10) |
| **2026-05-inc42-app-full-test** | **Full 9-persona test: Option F wins (7.89/10) and overtakes E at full depth. Inc42 Brief locked as the name. Inc42 Briefing reserved as institutional brand-portfolio asset.** |

### LLM Council (2 rounds)

- `council-synthesis-2026-05-10.md` — Brief-only product pass: 5/5 unanimous: Brief is v1.0 spine. 7 strategic decisions resolved.  
- **`council-synthesis-2026-05-16-unified.md`** — Unified concept pass: 5/5 responded. High-consensus findings drove scope cuts (Datalabs Profiles → v1.1), gate softening (3-seed → 1-required-3-recommended), tab reframing (Explore → Explore), and per-card Dismiss action. Highest-leverage recommendation: run concierge pilot in parallel with build to validate editorial operations.

### Build-prep docs

- `premium-boundaries.md` — per-feature Free/Plus/Pro tier map (needs update for unified app)  
- `watchlist-activation-flow.md` — original onboarding spec (§7 of this doc is the evolved version)  
- `success-metrics-and-kill-criteria.md` — pass/soft-fail/hard-fail thresholds \+ kill criteria \+ unified-app additions

---

*Concept locked 2026-05-16: F \+ Inc42 Brief \+ "Brief" tab label. Build planning call is the remaining gate. All prior versions preserved in `v1.0-concept.md` and `concept-note.md`. Creative name re-exploration parked — preserved in `brainstorm-name-and-positioning.md`.*

# Brief Tab

# PRD — Inc42 Brief (the daily intelligence brief feature)

**Status**: Final draft for sign-off · 2026-06-11 · author: Claude (for Utkarsh)   
**Feature owner**: Utkarsh (product)

**Prototype:** [https://drive.google.com/file/d/1naa66aU5CdQVcp3cjOvRDuNxlsGxyMs8/view](https://drive.google.com/file/d/1naa66aU5CdQVcp3cjOvRDuNxlsGxyMs8/view)  
**App Master Dashboard Sheet: [ Inc42 App Master Dashboard](https://docs.google.com/spreadsheets/d/16v86EyzAqKkCojnHy-cOgutNClSo_TyGF5ca3A3kJkM/edit?usp=sharing)**

---

## 1\. What the Brief is

A finite, personalized, \~90-second daily intelligence brief — 6–8 cards/day per user, four ICPs (Founder, Operator, Investor, BD), with an explicit endpoint. Each card triages one signal (a funding round or an editorial story) into a glanceable unit; tapping a card opens the full article with the summary pinned on top. It is the **front door** of the unified Inc42 app — the highest-confidence, habit-forming surface that routes into Explore, Datalabs profiles, and Ask.

**Hero job**: *"In 90 seconds each morning, tell me what changed in my corner of India's startup economy — accurately enough that I act on it, and pointed enough that I tap to go deeper."*

**Not**: an infinite feed, a newsletter re-render, a per-user-generated prose product, or a chat-first interface.

---

## 2\. Decisions locked in this PRD (your calls, 2026-06-11)

These four were the genuinely-open items (`brief-intelligence-layer.md` §10). Now decided:

| \# | Decision | Locked choice | Consequence for build |
| :---- | :---- | :---- | :---- |
| 1 | **v1 ICP launch scope** | **All 4 ICPs at launch** (Founder \+ Operator \+ Investor \+ BD) | 4 ranking/section configs \+ 4 serendipity policies tuned pre-launch; onboarding must segment users into one ICP upfront. Max coverage from day one. |
| 2 | **Editorial human-edit SLA** | **Fully automated v1, human-edit fast-follow** | Ship 100% generated bullets at launch; the 3-tier validator carries accuracy. Human-edit of bullet-2 on top cards lands in v1.1 once editorial throughput is confirmed. Accepts flatter voice \+ more causation-claim exposure early → the validator \+ listed-co hold (below) must be airtight at launch. |
| 3 | **Cannibalization appetite** | **Accept it — Brief is the front door** | Brief is meant to become the primary morning surface. Newsletter/Datalabs-feed engagement migrating is acceptable, even intended. Still instrument the overlap (counter-metrics §13) — accept ≠ blind. |
| 4 | **💬 suggested-question chip behavior** | **Opens Ask pre-seeded, but free (not capped)** | Tapping a curated suggested-question fires it into Decode/Ask, pre-filled and answerable, and does **not** count against the Decode soft-cap. Only free-text Decode counts. Cost controlled via the curated question set \+ teaser-and-route system prompt. |

   
Decision \#2 raises the stakes on the trust layer — with no human in the loop at launch, the deterministic Pass-1 gate \+ the listed-company causation hold (§7, §12) are the only things standing between a generated bullet and the Inc42 masthead. They are launch-blocking, not P2.

---

## 3\. Scope

### In (v1)

- Daily brief generation for all 4 ICPs, 6–8 cards/ICP/day.  
- Hybrid card bodies: editorial \= 3-bullet Smart Brevity (generate-once, validated); funding \= deterministic strip (no LLM).  
- Deterministic personalization: ICP-based ranking \+ section order, ⭐ watchlist hits, 🎯 relevance chip, per-followed-sector stat band.  
- Collapsed/expanded consumption model with read-tracking \+ finite endpoint card.  
- Per-card Decode (✨) \+ the 💬 suggested-question chip \+ brief-level Ask.  
- 1 serendipity slot ("Editor's Pick") per brief, per-ICP rules.  
- 3-tier validation pipeline \+ explicit fallbacks.  
- Editorial publishing gate (6am generate → approve → app pulls).

### Out (v1 — explicitly deferred)

- Human-written bullet-2 (→ v1.1, per decision \#2).  
- "Listen to today's Brief" audio (v1.0 stretch, not committed).  
- Per-story audio narration (v1.1).  
- Transactional payments / paid-subscription UI (Apple constraint — "Coming soon"/"Notify me" only; gated features labeled 🔒).  
- Real-time push alerting beyond the daily brief drop (v1.1 Signal layer).

---

## 4\. Consumption model (UX)

The brief is a **vertical stack of cards** with a finite end. Proven shape: Axios completion behavior, Inshorts (100M users / \~15 opens-month India), FT Edit retention.

- **Lead 1–2 cards open by default** (expanded depth) — the brief opens already showing substance, not a wall of headlines.  
- **Tail cards collapse** to: headline \+ `Signal-Type` tag \+ ⭐ (if hit) \+ 🎯 relevance chip \+ one line (the "what's new" line or the deterministic funding one-liner) \+ a `⌄` affordance.  
- **Tap a collapsed card → expands** to full anatomy AND auto-marks it read; progress advances.  
- **Sticky progress bar**: "N of 7" — completion is the habit reward infinite scroll denies.  
- **Tapping the card body (not a chip) → opens the full article** with the summary pinned on top (CTA Model A, §6).  
- **Hard stop at the endpoint card** — never silently extends into infinite scroll.

The interactive prototype (`prototype-2026-06-10.html`) is the reference implementation of this model across all 4 ICPs.

---

## 5\. Card anatomy (LOCKED)

```
N. Headline                         `Signal-Type`   ⭐ watchlist
   🎯 [deterministic relevance chip — why this card is in YOUR brief]
   • What's new      — hard news (generate-once, validated)
   • Why it matters  — item-level significance, NOT per-user  (✎ = human-edited, v1.1)
   • The detail      — one concrete fact from the article body a headline-only reader wouldn't know
   📊 [deterministic funding strip — funding cards only]
   ↳ 📊 [entity] on Datalabs   ·   💬 [story-specific suggested question]
```

- **Funding cards** → deterministic strip only (`📊 Company · ₹Cr ($M) · Stage · Sector · Lead/backers`), **no LLM bullets**. Grounded and free. Collapsed line uses `fundingOneLiner` — asserts "led by" **only** when explicit `lead_investors` exists, else neutral "backed by X, Y and others" (accuracy fix made this session).  
- **Editorial cards** → 3 generate-once bullets, grounded in the **real article body** (the `focusBody` window — for multi-story roundups, only the ±280-char slice about this card's entity), run through the validator before shipping.  
- **`Signal-Type` tag** reuses the Datalabs taxonomy (Funding & Investment, Competitive & Intelligence, M\&A & Strategic, Org & Team, Sector & Trend, Regulatory…); also drives the emergent content-type sections.  
- **🎯 relevance chip** (deterministic, §8): watchlist company → "\[co\] is on your watchlist"; watchlist investor in round → "\[inv\] (your watchlist) is in this round"; sector match → "\[sector\] · matches your focus"; else omitted.

### Bullet-2 ("why it matters") — the brand-value \+ risk field

Highest-brand-value AND highest-risk field. **v1 \= LLM-from-structured-fields with a tight, opinionated prompt** (seeded from the article lede), the **strictest validation tier**, and **no style instructions** to the summarizer (style instructions yield parody). **Human-edit on top cards is v1.1** (decision \#2). Content-type schemas — funding / policy / org / competitive / **investigation** ("What happened / Why it matters / What Inc42 found") — run under the one engine, not a single mold.

---

## 6\. CTA model (Model A — LOCKED)

**No "Read" button.** Tapping the card body opens the full article with the summary pinned on top. Two chips carry the cross-product routing:

- **`📊 [entity] on Datalabs`** — Intelligence/wider context, deterministic (entity nav → Datalabs profile, or `📊 [sector] tracker` / `📊 Open in Datalabs` fallback).  
- **`💬 [story-specific suggested question]`** — Network/Ask. An LLM-suggested, story-specific follow-up (≤12 words, Perplexity-style), generated in the same summarize-once batch (the 4th field of the schema). Per decision \#4: tapping opens Ask **pre-seeded \+ free** (not counted against the Decode cap).

CTA chip taps `stopPropagation` so they don't trigger the card-body article open.

---

## 7\. Intelligence layer (LOCKED — `brief-intelligence-layer.md` §2)

**Summarize-once-per-item \+ deterministic rank; generation only on-demand.** Cost is flat in DAU (\~$10–40/mo for item summaries \+ funding band) vs \~$20K/mo-at-50K-DAU for per-user prose — and summarize-once is the only model that lets you run ONE validation/human-spot-check pass per item before it ships to all users. Per-user generation makes review structurally impossible.

### Summarize-once schema (4 fields, grounded in real article body)

```
{ cards: [ { i, whatsNew, whyItMatters, detail, suggestedQuestion } ] }
```

- `detail` \= one concrete fact from the article body a headline-only reader wouldn't know.  
- `suggestedQuestion` \= sharp, story-specific follow-up ≤12 words.  
- Generation runs once per item at 3am (model `anthropic/claude-sonnet-4.6` in the sim; final model is an eng choice). Prompt-caching cuts cost \~59–60%.

### 3-tier validator (LOCKED — Council, §8.1)

Prompt-level "only use these facts" is documented to be insufficient (Maynez et al. ACL 2020; reproduced live in the sim — injected Rainmatter/Lightspeed). So:

```
Pass 1 — Deterministic hard gate (ALL items, free):
  entity allowlist (from FULL structured fields, not truncated display) · numeric/unit/currency range ·
  date/tense sanity · relationship-schema check vs structured fields ·
  banned-claim lexicon ("led the round","acquired","fraud","probe","confirmed" unless in source) ·
  provenance/source-span mapping
Pass 2 — Selective LLM NLI/entailment judge (high-risk items only, ~$15-60/mo):
  "does the summary assert any relationship/causation/quote/temporal claim NOT entailed by structured fields?"
  Triggers: regulatory/legal/allegation/layoffs/people-moves · any quote ·
  any "why it matters" with inference/causation/comparison/prediction · investigative/exclusive originals
Pass 3 — Mandatory human review: red-category (investigations, allegations, market-moving listed-co claims)
```

Two zero-cost structural rules: **(a) ban direct quotes in generated bullets** (quotes live only on tap-through); **(b) explicit fallback on validation failure** — editorial item → headline \+ standfirst \+ open-article; funding item → deterministic strip only. **No silent retries** that bypass policy.

With decision \#2 (no human-edit at launch), Pass-1 \+ Pass-2 are the live trust layer for the whole brief; Pass-3 human review of red-category items is non-negotiable even in the otherwise-automated v1.

---

## 8\. Personalization (LOCKED — shown, not narrated, §3)

Deterministic, free, un-fakeable — never per-user prose:

- **Selection** — the brief *is* personalized by which 6–8 of \~20 items it shows.  
- **Ranking \+ section order by ICP mode** — Operators lead with Analysis & Features; Founders/Investors/BD with Funding & Deals.  
- **⭐ watchlist hits** \+ **🎯 relevance chip** \+ **per-followed-sector stat band** (everyone also sees the shared deterministic market numbers — an anti-bubble floor).  
- **Zero-hit watchlist fallback** (§9.5): never render empty — degrade to "⭐ Trending in your sector" / "Highly read by \[your ICP\]".

The *personal* angle that used to be narrated is now available **on demand** via Decode. Topic-subscription beats algorithmic personalization for premium audiences (myFT, 44% of digital subs).

---

## 9\. Serendipity (LOCKED — §8.2)

**1 default slot (\~12–15%)**, labeled **"Editor's Pick" \+ one-line rationale**, placed *after* the core-relevance band, never displacing top-ranked cards, **tracked separately** (skip/hide/save/CTR/next-day-retention). Per ICP:

- **Founders: 0–1** — cross-ICP must have a regulatory/talent/investor-pattern angle that *transfers* (not a random raise).  
- **Operators: 1** — must be **sector/macro-level, not company-level** ("quick-commerce GMV hit ₹X" \= signal; "Zepto raised X" \= noise).  
- **Investors: 1** — cross-sector by job function.  
- **BD: 1** — by saved-search/lead relevance.

The shared funding band is NOT a serendipity slot — it's a fixed factual floor, not counted against the 6–8.

---

## 10\. Ask integration (LOCKED — §5)

- **Per-card Decode (✨)** — opens an answer pre-seeded with that card's structured context (grounded by construction). **Soft cap \+ conversion prompt** ("8 of 10 — unlock unlimited with Brief Pro"), NOT a hard 10/day wall (§9.3 — a hard wall hits the most-engaged users at peak intent).  
- **💬 suggested-question chip** — pre-seeded \+ **free/uncapped** (decision \#4).  
- **Brief-level chat** — "summarize today in a line", "skip funding, what's the talent news?".  
- **Decode system prompt must teaser-and-route** ("…read the full report") to limit article-traffic cannibalization (§9.2) — even though we accept cannibalization strategically (decision \#3), Decode shouldn't *replace* the article, it should *route* to it.

Ask is a secondary, optional affordance — never the path to consume the brief. Recognition is cheaper than recall.

---

## 11\. Editorial governance & publishing gate (LOCKED — §8.4)

Quality ownership cannot be distributed. RACI:

- **Editorial** — quality bar, content-type style rules, exception classes, signal-label standards, **publishability veto**. Single **Brief Integrity Owner** (senior editorial) appointed.  
- **Datalabs** — summarization pipeline, validators, taxonomy, source mapping, model tuning, versioning \+ rollback.  
- **App** — ranking, personalization, serendipity execution, endpoint, UX, analytics. *Does not own language quality.*

**Publishing gate**: Datalabs generates \~20 candidate cards by 7 am → editorial reviews/edits red-category \+ Pass-3 items in CMS → "approve" by 8 am → app pulls the approved payload. Weekly 30-min quality review (editorial \+ Datalabs \+ app PM), one scorecard, one taxonomy owner, escalation to Utkarsh.

Note: in automated-v1 (decision \#2), the 8 am gate still applies — editorial's job at launch is the **Pass-3 red-category review \+ publishability veto**, not editing every bullet. The bullet-2 human-edit workflow layers on in v1.1.

---

## 12\. Risk (launch-blocking — §9)

1. **India IT Rules 2021 / SEBI exposure.** A wrong causation claim about a named/listed company can touch SEBI false-market-information \+ defamation — Inc42 is a publisher, not a mere intermediary here. **Hard rule: any causation claim about a listed company is held from publication until human review.** Validate trigger rules with counsel (the one genuinely-open item that is NOT ours to decide).  
2. **Stale-cache risk.** Summarize-once \+ cache → an afternoon reader could see a figure the CMS already corrected. **Cache-invalidation webhook**: material article update → auto re-summarize \+ re-validate \+ show "updated" state; version \+ rollback.  
3. **Taxonomy drift.** Reused Datalabs signal-tags will drift from editorial standards → editorial veto on taxonomy \+ change-log/diff review.

---

## 14\. Cost envelope

| Component | Cost | Scaling |
| :---- | :---- | :---- |
| Item summaries (summarize-once, \~20/day) \+ funding band | \~$10–40/mo | **Flat in DAU** |
| Pass-2 NLI judge (high-risk items only) | \~$15–60/mo | Flat (per-item, not per-user) |
| Decode / Ask (on-demand) | \~$0.04/invocation | Self-limiting, soft-capped |
| 💬 suggested-question taps | folded into summarize-once batch (generation) \+ on-demand answer | Free at tap (decision \#4) |

\~100–1000× cheaper than the per-user prose model the simulation accidentally implied — *and* auditable.

---

## 15\. Success metrics (per `success-metrics-and-kill-criteria.md`)

**North-star**: D30 retention of weekly active users — **≥15% sustained at 90-day** (FT Edit benchmark).

Brief-specific gates (30-day): **Brief completion** (% sessions where user tapped into ≥3 of 8–12 stories) ≥40% pass / 25–40% soft / \<25% hard · D7 ret ≥30% · D30 ret ≥15% · push opt-in ≥55% · watchlist completion ≥30% · crash-free ≥99.5%.

60-day Brief-relevant: Decode usage ≥15% of opened stories · cross-product surfacing (decode → Datalabs/Ask) ≥20%.

**Kill** (locked): D30 \<10% sustained 4+ wks → halt \+ hero-job-dilution review. Counter-metric: newsletter \<80% AND web \<90% baseline → net-cannibalization halt (the one place decision \#3's "accept" has a floor).

Instrument from day 0 (PostHog, shared user IDs): `brief_session_started/_story_opened/_session_completed`, `decode_tapped/_returned/_rate_capped`, `suggested_question_tapped`, watchlist \+ push \+ counter-metric events.

---

# Explore PRD

# Inc42 App — Explore PRD (team share)

**Owner**: Utkarsh · **Updated**: 2026-06-19 · **Status**: for team review *Simplified, share-ready version. Full build detail (backend contracts, SLOs, ranking model, telemetry) lives in `explore-prd.md`.*

---

## 1\. What Explore is

The app's **archive \+ browse surface** — the counterpart to the daily Brief. Where the Brief is finite, curated, and pushed each morning, Explore is **deep, on-demand, and pull-only**: \~30K Inc42 articles (12-year archive) \+ the Datalabs company graph (70K+ companies), reached by **search** and **browse**.

It is a **retrieval** surface, not a feed. No algorithmic "what's new today" — that's the Brief's job. Explore is for going *beyond* today.

---

## 2\. Where it sits (IA)

- **3 bottom tabs**: Brief · **Explore** · Watchlist.  
- **Global 🔍 search** and **account avatar** live on the top bar of every screen — neither is a tab. No hamburger menu.

**Explore layout (top → bottom):**

1. Search bar  
2. *Today's Datalabs signals* rail (collapsed)  
3. **Content switch**: Articles | Companies  
4. **Sub-navigation strip** (horizontal scroll) — slices the corpus  
5. The feed (cards)  
6. Recently viewed

---

## 3\. Articles tab

**Sub-nav strip** \= one horizontal-scroll pill bar with two groups:

```
[ Latest ] [ Funding ] [ Features ] [ M&A & Policy ] [ Startup Stories ] ┊ [ Fintech ] [ Edtech ] [ Ecommerce ] [ AI ] [ … 17 sectors ]
└────────────── FEEDS (editorial streams) ─────────────┘            └──────── INDUSTRIES (the 17 sectors) ────────┘
```

- **Feeds** \= editorial streams. **Industries** \= the 17 Datalabs sectors. One selection at a time.  
- Selecting an **industry** pill opens the **Sector landing** (§6) — same as tapping a sector tag anywhere.  
- Default \= `Latest`, chronological.

**Article card (light list-row):**

```
┌───┐ ■ Breaking   · Fintech            chips = [signal-type] [sector→]
│IMG│ Razorpay bags $75M Series G       tap row    → Article Reader
└───┘ Inc42 · 3h                    🔖   tap sector → Sector landing
```

Fields: thumbnail · signal-type chip (Breaking/Feature/Story/Report) · **sector chip (tappable)** · headline · byline · age · 🔖 save.

---

## 4\. Companies tab

The 70K-company graph is too big for one flat list, so it's organized by **preset slices**:

```
[ Recently Funded ] [ Top Funded ] [ By Stage ] [ By Sector ] [ Most Tracked ]
```

- **Recently Funded** (default) · **Top Funded** · **By Stage** (Seed/Series A/B…) · **By Sector** (drills into a sector landing) · **Most Tracked** (app's own follow counts).  
- Secondary filters (sector, stage, type, status, region, founded year) in a Filters sheet.

**Company card (list-row):**

```
⬛ Razorpay        ● Active             chips = [status] [sector→] [stage]
   Fintech · Payments   Series G        tap row    → company profile
   Last: $75M · Jun 2026 · $1.4B total  tap sector → Sector landing
   Bengaluru · 1k–5k          [ ✓ ]     [Track] toggles watchlist
```

Fields: logo · name · status chip · **sector chip (tappable)** · stage chip · last round \+ total raised · HQ \+ employee band · Track.

---

## 5\. Search (global)

Opens the same overlay from the top-bar 🔍 anywhere. **Companies surface first** on an entity match; articles below; a `Go to [Sector] →` chip if a sector matches. Person/fund names return **coverage (articles)** — there are no people/investor profiles in v1 (see surfaces PRD).

```
🔍 razorpay
─────────────────────────────
COMPANIES
⬛ Razorpay · Fintech · Series G   [+]
─────────────────────────────
Go to Fintech →
─────────────────────────────
ARTICLES (24)
 Razorpay bags $75M Series G · 3h
 Razorpay's lending pivot     · 2w
─────────────────────────────
Get a synthesized answer →  (dormant — future "Ask")
```

---

## 6\. Sector landing (where an industry tag goes)

Tapping any **industry** — a card's sector chip, an in-article tag, an Articles industry pill, the Companies "By Sector" slice, or a search chip — lands here. It's **Explore scoped to one sector** (not a heavy dashboard):

```
‹ Explore
Fintech                       [+ Track]
₹4,200 Cr · 38 deals · last 30d
┌────────────┬───────────────┐
│  ARTICLES  │   Companies   │   ← locked to Fintech
└────────────┴───────────────┘
■ Breaking  Razorpay bags $75M…   3h
▤ Feature   UPI's next act…       4d
   …
```

\= the Articles \+ Companies lists pre-filtered to that sector \+ a **Track sector** button. Taxonomy \= the 17 sectors; sub-sectors/colloquial terms (SaaS, D2C, Quick-Commerce) alias up to their parent.

---

## 7\. Reports

**Not a reading surface in v1.** Reports are desktop/PDF-shaped. They appear as **deep-link rows** in Brief and Explore (`📊 New report: State of Indian Fintech 2026 →`) that open on web or trigger the email-gate. No in-app reader.

---

## 8\. Today's Datalabs signals

A collapsed rail at the top: top 3–5 market aggregates of the day (funding raised, deals, sector flows, hiring). Tappable to detail. Optional `All / My watchlist` toggle. The only daily-fresh element in Explore.

---

## 9\. The 17 sectors (canonical taxonomy)

Fintech · Edtech · Ecommerce · Health Tech · Enterprise Tech · Enterprise Services · Media & Entertainment · Advanced Hardware & Technology · Consumer Services · Clean Tech · Real Estate Tech · Travel Tech · AI · Logistics · Agritech · Foodtech · Web3

*Shared spine for Inc42 editorial (`tag_industry`) and Datalabs (`company_sector`).*

---

## 10\. Data sources (one line each)

| Surface | Backend |
| :---- | :---- |
| Articles | Inc42 hybrid search (`/sqlquery`) |
| Companies \+ profiles | Datalabs entity search (ES) |
| Reports | WordPress reports API (list-only) |
| Today's signals | Datalabs daily aggregate feed |

---

## 11\. Not in v1 (deferred)

- Algorithmic discovery feed (Brief owns "today").  
- In-app report reader.  
- Conversational "Ask the archive" (dormant hook only).  
- People / investor profiles → company profiles only (see surfaces PRD).  
- Saved searches / search alerts.  
- In-app paywall (tier flags exist, conversion dormant).

---

## 12\. Success signals

- Search queries / DAU ≥ 0.3  
- Sessions touching both Brief \+ Explore ≥ 20%  
- Companies browse engagement ≥ 15%  
- Datalabs profile views / DAU ≥ 0.2 (M1) → 0.5 (M3)

# Other Surfaces

# Inc42 App — Surfaces PRD: Watchlist · Profile · Shared (team share)

**Owner**: Utkarsh · **Updated**: 2026-06-19 · **Status**: for team review *Simplified, share-ready. Combines what were three docs (Watchlist, Entity Profile, Misc). Full build detail lives in `watchlist-prd.md`, `entity-profile-prd.md`, `misc-features-prd.md`.*

**IA reminder**: 3 bottom tabs (Brief · Explore · Watchlist) \+ global 🔍 \+ account avatar. No hamburger. Free tier only at launch — Plus/Pro reserved in code, **no paywall, no pricing words anywhere** (App Store-safe).

---

# PART A — Watchlist

## A1. What it is

The **Following \+ Saved** surface — the standing set of what a user tracks, plus the stories they keep. It's the app's reason to exist beyond a newsletter: the Brief says what moved *today*; Watchlist is what *you* told the app to care about, and its latest movements. It's also the natural Datalabs-Pro on-ramp.

Not a live ticker, not a second Brief. Event-driven: you open it to check "did anything happen to what I track?"

## A2. Two sub-tabs

```
┌──────────────────────────────┐
│  Watchlist        🔍    ( U ) │
│ ┌──────────────┬───────────┐ │
│ │  TRACKING    │   Saved   │ │   ← segmented control
│ └──────────────┴───────────┘ │
│  Following (8)       [+ Add] │
│  ── COMPANIES ─────────────  │
│  [M] Meesho   Series G       │   → company profile
│      Ecommerce · 14 alerts   │
│  [Z] Zepto    Series F       │
│      Ecommerce · 6 alerts    │
│  ── SECTORS ───────────────  │
│  # Fintech         9 alerts  │   → Sector landing
│  ────────────────────────    │
│  RECENT ALERTS               │
│  · Meesho: $275M raise   2h  │
│  · Fintech: RBI norms    1d  │
│  See all (90-day) →          │
└──────────────────────────────┘
```

```
SAVED sub-tab
┌──────────────────────────────┐
│  Saved (14)                  │
│  Why India's OTT market…May14│  → Article Reader
│  📊 State of Fintech 2026·May12│ → report deep-link
└──────────────────────────────┘
```

## A3. What you can track (v1)

Two types only: **Companies** and **Sectors/Topics**. *People and funds/investors are NOT trackable in v1* — a tracked row must open a profile, and v1 only ships company profiles (see Part B). They return in v1.1+, **investor before people**.

- Free caps: **\~15 companies \+ 5 sectors** (\~20 total). Hitting a cap shows a soft "more depth coming — notify me," never a hard wall.  
- Track from anywhere (one tap): Brief cards, Explore rows, search results, in-article tags, profile `[+ Track]`.  
- `[+ Add]` opens Datalabs search-as-you-type.

## A4. Recent alerts

Chronological list of movements for tracked entities (funding, hires, policy, coverage). Independent of the Brief. Shows **last 20**, "See all" → **90-day** rolling history. Each tier-1 push ("because you track X") lands here.

## A5. Saved

Absorbs bookmarks (the old Profile tab is gone). One-tap 🔖 from Brief cards, Explore rows, and the reader. Recency-sorted, flat (no folders v1). Anon users: saved locally (cap 50), merged on sign-in; gentle sign-in nudge after the 3rd save.

## A6. Empty states

```
TRACKING (empty)                 SAVED (empty)
Track what matters to your day.  Stories you save show up here.
[+ Add]                          Tap 🔖 on any story to keep it.
Suggested: [+Meesho] [+Fintech]
```

## A7. Monetization on-ramp (dormant)

Watchlist is the upsell surface, but v1 only **captures interest** — cap hits and 🔒 depth show a "coming soon — notify me" sheet. No "Pro/Plus/Subscribe/₹" wording. v1.1 activates the real path.

---

# PART B — Company Entity Profile

## B1. What it is

The page you land on when you tap a company anywhere. A **glanceable consumption view** of Datalabs data — not Datalabs Web in a phone frame. Shortlisted from the existing Datalabs company profile (no new data).

**v1 \= company profiles only.** Investor and person profiles are deferred to v1.1/v1.2+ (investor first). That's why person/fund search returns coverage, not a profile.

## B2. Anatomy

```
┌─────────────────────────────────────┐
│  ‹            [ + Follow ]      ⋯    │
│  ⬛ COMPANY NAME                      │
│  Sector · Sub-sector · HQ city       │
│  Founded YYYY · Active · ↗ website    │
│  ┌── Funding ───────────────────────┐│
│  │ $XXM raised total                ││
│  │ Latest: Series B · $25M · Mar'26 ││
│  │ Key investors: A, B, C           ││
│  └──────────────────────────────────┘│
│  ┌── People ────────────────────────┐│
│  │ Founder — CEO        in          ││
│  │ Founder — CTO        in          ││
│  └──────────────────────────────────┘│
│  ┌── On Inc42 ──────────────────────┐│  ← editorial tie-back
│  │ • [Headline]              3d     ││
│  │ • [Headline]              2w     ││
│  └──────────────────────────────────┘│
│  [ Ask about COMPANY ]  (dormant)    │
└─────────────────────────────────────┘
```

Order: **Header → Funding → People → On Inc42 → Ask-stub.** Closes the Intelligence→Journalism loop on every profile.

## B3. Free vs reserved

- **Free (shown)**: identity, sector/stage, HQ, founded, status, total raised, latest round, key investors, founders \+ key CXOs, employee band, recent Inc42 coverage, one signal stat.  
- **Reserved (🔒, omitted in v1 — not teased)**: full funding history, cap table, MCA financials, valuation history, trendline charts, comparisons.

Rule of thumb: *who / what / when \= free; how-much / structured depth \= later.* No lock overlays or upsell copy at launch.

## B4. Reach

From Watchlist company rows, Explore → Companies, Brief signal cards, global search, in-article company tags — all resolve to one canonical profile by company slug.

---

# PART C — Shared surfaces

## C1. Account (avatar)

Top-right avatar, every screen. Low-frequency housekeeping:

```
[U] Utkarsh — Founder · Fintech, Ecommerce
PREFERENCES
  My role        Founder ▸
  My sectors     Fintech … ▸   (the 17)
  Push alerts    On ▸
  Brief time     7:30 AM ▸
ACCOUNT
  utkarsh@inc42.com
  Sign out
```

Editable role/sectors. No subscription/billing UI in v1.

## C2. Global search

The top-bar 🔍 opens the **one** Explore search overlay from any screen (Brief, Explore, Watchlist, reader, profile). Opening it from an entity pre-seeds the query (tap 🔍 on a Meesho card → "Meesho"). Detail in the Explore PRD.

## C3. Decode & Ask

- **Decode (✨)** — live in v1. Per-card AI explainer, pre-seeded with the card's facts. **Soft-capped, non-blocking** (capture interest, never wall the most-engaged users). Suggested-question chips are free. Always routes to the full article.  
- **Ask Inc42** — a *mode, not a tab*. Open-ended chat is deferred to v1.1. Two dormant stubs keep us ready: "Ask the archive" in search, "Ask about \[entity\]" on profiles. No live LLM call in v1.

## C4. Article reader

Full-screen modal that slides up from any surface. Header 🔖 saves to Watchlist → Saved. In-article entity tags open company profiles; sector tags open Sector landings. Dismiss returns to where you were.

## C5. Auth & notifications

- **Sign-in**: soft sheet triggered by a gated action (Follow, \~5 profile views, 3rd save). Completes the pending action and merges anon local data. "Continue without account" stays available.  
- **Push permission**: asked *after* the first brief is read (value first), not on cold launch.  
- **Notification prefs** (via avatar): brief push \+ time, alert tiers (must-know / digest, capped 3/day), watchlist alerts on/off.

---

## Open items

- Apply the simplified Watchlist cap (\~15 companies \+ 5 sectors) to `premium-boundaries.md` at build.  
- Decode soft-cap threshold \+ Apple-safe prompt copy — set at build.  
- Company profile: signal-stat priority \+ logo source — confirm at build.  
- Investor profile (v1.1) lands before person profile.

# WIP

# Inc42 First-Open Walkthrough

# **PRD — Inc42 First-Open Virtual Tour**

**Owner:** \[Mohit Bhaler\] · **Status:** Draft v0.2 · **Last updated:** 6 Jul 2026 **One-liner:** A dismissible, 4-stop spotlight tour on the home screen that dims the UI, highlights one area at a time, and introduces Brief, Streak, Explore, and Watchlist.

---

## **1\. Problem**

New users finish auth and preference selection, land on home, and don't know what the brief is, how the streak works, or what Explore and Watchlist are for. A short guided tour orients them to the four core areas in one pass.

## **2\. Goal**

In the first session, walk every new user through the four key areas of the app so they know what each one does before they start using it.

## **3\. Success metrics**

| Metric | Type | Definition |
| ----- | ----- | ----- |
| Tour completion | **Primary** | % of new users who reach "Done" (stop 4\) |
| Skip rate \+ skip-by-step | Secondary | % who exit early, and at which stop |
| Step drop-off | Secondary | View → advance rate per stop |
| First-brief-open (downstream) | Guardrail | % who open a brief in session 1 |
| Reached-streak-screen (downstream) | Guardrail | % who hit the streak screen in session 1 |

## **4\. Scope**

3-stop spotlight tour on the home screen; dim scrim \+ single spotlight per stop; Next \+ Skip per stop; first-open-only trigger; iOS \+ Android.

## **5\. Trigger & entry conditions**

* Fires once, on **first app open after auth \+ preference selection are complete**.  
* Runs entirely as an overlay on the **home screen**. It does not navigate anywhere.  
* Never re-triggers automatically once the tour is completed or skipped.

  ## **6\. The tour**

Four stops, all on the home screen. Each stop dims the full screen and spotlights one region. The underlying UI is **inert** during the tour — the only tappable controls are **Next** and **Skip**.

| \# | Stop | Spotlight \`target | Copy (draft) | Button |
| ----- | ----- | ----- | ----- | ----- |
| 1 | Brief | Today's Edition card+ weekly day row | "Your personalized daily brief, based on your preferences. Tap any day to catch up on past ones." | Next |
| 2 |  |  |  |  |
| 3 | Explore | Explore nav icon | "Browse the wider ecosystem: articles, sectors, and companies across Inc42." | Next |
| 4 | Watchlist | Watchlist nav icon | "Your tracked companies, saved articles, and saved sectors, all in one place. " | Done |

## **7\. Interaction spec**

* **Scrim:** full-screen dark overlay (\~65% opacity). The spotlight target sits at full brightness inside a cutout with a small padding radius around it.  
* **Controls:** every stop shows **Skip** (persistent) and **Next**. Stop 4's primary button reads **Done**.  
* Card content (structure): **Heading:** the stop name (Brief, Streak, Explore, Watchlist) **Copy:** one line below it **Buttons:** Skip and Next (Done on the last)  
* **Advance:** strictly via **Next**. No gestures, no tapping the real element.  
* **Skip:** exits the **entire** tour immediately and marks it seen.  
* **Underlying UI:** non-interactive for the tour's duration; it's shown for context only.

  ## **8\. Behavior rules**

* Completing (Done) or skipping marks the tour **seen**; it never auto-replays.  
* No nagging: a user who skips is not re-prompted in-session or later.

  ## **9\. Edge cases**

| Case | Behavior |
| ----- | ----- |
|  |  |
| App backgrounded mid-tour | Resume at the last un-advanced stop. |
| Small screens / nav layout shifts | Spotlight \+ tooltip must fit; tooltip flips to avoid clipping. |
| Reinstall / returning user | Treat "seen" as server-side if available so it doesn't replay.  |

# FAQ's

## **qInc42 App FAQs**

## **Streak FAQs**

### **What is a streak?**

A streak is the number of consecutive days you've completed your daily Brief. Each day you finish the current day's Brief, your streak increases by one.

### **How do I maintain my streak?**

Simply complete the day's Brief. Only the latest daily Brief counts towards your streak.

### **Do older briefs or articles count?**

No. Reading previous days' Briefs or individual articles won't increase your streak. Only completing the current day's Brief counts.

### **When does my streak reset?**

If you miss a day's Brief, your streak resets. The next time you complete a Brief, you'll start a new streak from Day 1\.

### **What are reader levels?**

Reader Levels recognise your long-term consistency. As your streak reaches key milestones, you'll unlock new levels. Once unlocked, a Reader Level is permanent, even if your streak resets later.

### **What are badges?**

Badges celebrate important streak milestones. Each badge can only be earned once and remains part of your profile permanently.

### **Are there rewards?**

Rewards are coming soon. Until then, maintaining your streak helps you unlock Reader Levels and earn achievement badges.

### **What does the calendar show?**

The calendar gives you a monthly view of your activity. Completed Briefs are marked, today's date is highlighted, and missed days remain blank so you can easily track your reading habit.

# **General FAQs**

### **What is the Inc42 app?**

The Inc42 app helps you stay updated on India's startup ecosystem with a personalized daily Brief, the complete Inc42 article archive, and company insights, all in one place.

### **Is the app free?**

Yes. All features currently available in the Inc42 app are free to use.

### **How do I sign in?**

You can sign in using Apple, Google, or your email address. If you already have an Inc42 account on the website, use the same credentials to access your account in the app.

### **What is the Daily Brief?**

The Daily Brief is a personalised roundup of the most important startup news, funding announcements, company updates, and ecosystem trends, curated to match your interests.

### **How is my Brief personalised?**

Your Brief is created using the preferences you choose during onboarding, including your role, the sectors you follow, and the topics you're interested in.

**When will I receive my Brief?**

A new Brief is available every morning, so you can catch up on the day's most important startup news.

### **What happens after I finish the Brief?**

Once you've completed all the stories, you'll see a "Done for Today" screen. That's your signal that you've finished today's Brief. A new one will be available the next day. You can also browse Explore tab to know more. 

### **How do I follow a company or sector?**

Tap Track or the \+ icon on a company or sector. You can do this from your Brief, Search, Explore, or a Company page.

### **Where can I see everything I follow?**

Open the Watchlist tab to view all the companies and sectors you're tracking, along with their latest updates.

### **How do I save articles for later?**

Tap the Bookmark icon on any article. You can find all your saved stories in the Saved section within the Watchlist tab.

### **Will I receive updates about companies I follow?**

Yes. If there's important news about a company or sector you track, it will be included in your Daily Brief.

### **What is Explore?**

Explore gives you access to the complete Inc42 content library, including articles, company profiles, and startup data beyond your daily Brief.

### **Can I search for companies or articles?**

Yes. Use the Search icon to quickly find companies, articles, sectors, and other content available in the app.

### **Where does the company information come from?**

Company profiles are powered by Inc42 Datalabs and include information such as funding history, company overview, leadership, and other publicly available business data.

**Contact & Privacy**

**How is my data handled?** We follow a strict privacy policy to keep your data safe. Open **Privacy Policy** under About on your Profile to read it in full.

**How do I get in touch?** Tap **Contact Us** under About, or email the Inc42 team at \[email address\], and we'll get back to you.

# Inc42 App Analytics PRD

**Inc42 App Analytics PRD**

June 2026

 

# **Table of Contents**

Table of Contents................................................. 1

1\. Purpose............................................................ 1

2\. Global Properties, Identity & Sessions............. 1

2.1 Standard Properties (sent with every event).......................................................................... 1

2.2 Identity Resolution...................................... 1

2.3 Sessions..................................................... 1

Event: session\_started.................................. 1

Event: session\_ended................................... 1

3\. Event Documentation Standard & Completion Definitions............................................................. 1

3.1 Naming & Documentation Convention....... 1

3.2 Completion Definitions (the core v1 gap)... 1

4\. Onboarding....................................................... 1

Event: onboarding\_started............................ 1

Event: onboarding\_step\_viewed................... 1

Event: onboarding\_step\_completed............. 1

Event: onboarding\_step\_skipped................. 1

Event: onboarding\_abandoned..................... 1

Event: onboarding\_role\_selected................. 1

Event: onboarding\_sectors\_selected........... 1

Event: onboarding\_completed...................... 1

5\. App Open & Sessions...................................... 1

6\. Brief.................................................................. 1

Event: brief\_loaded....................................... 1

Event: brief\_card\_viewed.............................. 1

Event: brief\_card\_expanded......................... 1

Event: brief\_article\_opened.......................... 1

Event: brief\_story\_saved.............................. 1

Event: brief\_session\_ended................................. 1

7\. Articles.............................................................. 1

Event: article\_opened................................... 1

Event: article\_completed............................... 1

Event: article\_saved...................................... 1

Event: article\_shared.................................... 1

8\. Search.............................................................. 1

Event: search\_executed............................... 1

Event: search\_result\_clicked........................ 1

9\. Company Profiles............................................. 1

Event: company\_profile\_viewed................... 1

Event: company\_related\_article\_clicked...... 1

10\. Watchlist (Unified).......................................... 1

Event: watchlist\_entity\_added...................... 1

Event: watchlist\_entity\_removed.................. 1

Event: watchlist\_opened............................... 1

Event: watchlist\_alert\_opened...................... 1

11\. Notifications.................................................... 1

Event: notification\_permission\_requested.... 1

Event: notification\_permission\_granted / notification\_permission\_denied.................... 1

Event: push\_received................................... 1

Event: push\_opened..................................... 1

12\. Installs & Attribution........................................ 1

13\. Core Business Metrics Dashboard................ 1

13.1 Habit Metrics............................................. 1

13.2 Personalization Metrics............................ 1

13.3 Intelligence Metrics................................... 1

13.4 Retention Metrics...................................... 1

14\. Key Product Hypotheses to Validate............. 1

15\. Privacy & Data Governance........................... 1

15.1 Search Query Handling............................ 1

15.2 General PII Minimization.......................... 1

16\. Open Items for Engineering Sign-off.............. 1

 

 

# **1\. Purpose**

The analytics framework exists to answer four core business questions:

•        Habit Formation — Are users building a daily Brief consumption habit?

•        Personalization — Does Watchlist-driven personalization improve engagement and retention?

•        Intelligence Discovery — Are users moving beyond headlines into deeper startup intelligence?

•        Retention — Which behaviors predict long-term retention and product success?

The analytics system prioritizes meaningful user actions over UI interactions.

**Measurement Principles**

•        One canonical event per real-world user action. If two surfaces produce the same underlying action (e.g., following a company), they emit the same event with a different source value — never two differently named events.

•        Every rate metric states its unit explicitly: distinct users, distinct sessions, or raw events. These are not interchangeable and must never be silently mixed within one formula.

•        Funnel/reach metrics that have a natural dimension (step, card position, search) are computed per-dimension, never as an aggregate sum, so they cannot exceed 100%.

•        Any metric whose denominator is not a client-side event (e.g., installs, alerts\_sent) must name its actual data source and the join key used to connect it to client analytics.

# **2\. Global Properties, Identity & Sessions**

## **2.1 Standard Properties (sent with every event)**

Every event in this document inherits the following properties automatically. They are not re-listed under each individual event.

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| event\_name | string | Canonical event identifier, e.g. brief\_card\_viewed |
| event\_id | UUID | Unique ID per event instance; used for client-side retry de-duplication |
| timestamp | ISO 8601 (UTC) | Client-generated event time |
| user\_id | string, nullable | Stitched identity once authenticated; null pre-login |
| anonymous\_id | string | Persistent device/install-level ID, assigned at first open |
| session\_id | string | Identifies the current session (see 2.3) |
| platform | enum: ios, android, web | Client platform |
| app\_version | string | Semantic app version, e.g. 4.2.1 |
| os\_version | string | Device OS version |
| device\_id | string (hashed) | Hashed device identifier; never raw IDFA/GAID in the analytics warehouse |
| network\_type | enum: wifi, cellular, offline\_queued | Connectivity at send time; offline\_queued flags events that were queued and sent late |

## **2.2 Identity Resolution**

•        anonymous\_id is assigned on first app open and persisted in local storage; it is the only identity available during pre-login onboarding.

•        On signup or login, the client fires an alias/identify call mapping anonymous\_id → user\_id.

•        The analytics warehouse must perform identity stitching so pre-login onboarding events and post-login events merge into one user timeline. Without this, onboarding personalization (H6) and D1/D7/D30 retention cannot be joined to the same user.

•        Retention (D1/D7/D30) is computed from first session — anonymous or authenticated — not from signup, unless a metric explicitly says “post-signup retention.”

## **2.3 Sessions**

### **Event: session\_started**

**Trigger:** App enters the foreground and either (a) it is a cold start, or (b) more than 30 minutes have elapsed since the last recorded activity.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| session\_id | UUID | New ID generated for this session |
| entry\_source | enum: push, deep\_link, icon, widget | What brought the user into this session |
| is\_first\_session | boolean | True only for a device's very first session |

**Why**

Defines the boundary every DAU/WAU/MAU and per-session metric depends on.

**Questions Answered**

•        How many distinct users are active per day/week/month?

•        What share of sessions originate from notifications vs. organic opens?

 

### **Event: session\_ended**

**Trigger:** App is backgrounded and the 30-minute inactivity timeout has elapsed (computed retroactively), or the OS signals app termination.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| session\_id | UUID | Matches the session\_started event |
| session\_duration\_seconds | integer | Wall-clock duration of the session |
| screens\_viewed | integer | Count of distinct screens viewed in the session |

**Why**

Closes the session record so duration and depth can be computed.

**Questions Answered**

•        How long are typical sessions?

•        Do longer sessions correlate with retention?

 

**DAU / WAU / MAU definition:** Distinct stitched identities (anonymous\_id pre-login, user\_id post-login, deduplicated via 2.2) with ≥ 1 session\_started in the period. This definition is referenced by every “.../DAU” metric in Section 13\.

 

# **3\. Event Documentation Standard & Completion Definitions**

## **3.1 Naming & Documentation Convention**

•        Naming: object\_verb\_pastparticiple (e.g. brief\_card\_viewed, watchlist\_entity\_added).

•        Every event below documents: Trigger, Properties (or an explicit “None”), Why, Questions Answered, and Metrics (or an explicit “None”) — no event is allowed to silently omit a section.

•        Every metric formula states its unit (distinct users / distinct sessions / raw events) and, where the underlying event has a natural dimension (step\_name, card\_position, search\_id), states that the metric is computed per-dimension.

## **3.2 Completion Definitions**

**article\_completed**

Fires when EITHER of the following is true, whichever happens first, provided the app has not been continuously backgrounded for more than 5 seconds during the read (to exclude false positives from a phone being put down):

•        scroll\_depth\_pct \= 100%

New properties added to article\_completed: scroll\_depth\_pct, active\_time\_seconds, estimated\_read\_seconds.

**brief\_session\_ended**

Fires once per brief\_date per user, with a completion\_type property distinguishing how it was reached:

•        completion\_type \= "full" when cards\_viewed.

•        completion\_type \= "exited" when the user explicitly leaves the Brief screen

New properties added to brief\_session\_ended: completion\_type, scroll\_depth\_pct. Brief Completion Rate (Section 13\) is reported for completion\_type \= "full" specifically, with an “any completion” variant reported alongside for context.

# **4\. Onboarding**

### **Event: onboarding\_started**

**Trigger:** User enters the onboarding flow, for the first time or after a prior abandonment.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| source | enum: organic, paid, referral, deep\_link | Acquisition source |
| is\_reentry | boolean | True if the user previously abandoned onboarding and is starting again |

**Why**

Starting point for all onboarding funnels.

**Questions Answered**

•        How many users enter onboarding?

•        How many complete onboarding?

**Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Onboarding Start Rate | distinct users with onboarding\_started / installs | installs is MMP-sourced, not a client event — see Section 12 |

 

### **Event: onboarding\_step\_viewed**

**Trigger:** User views a given onboarding step.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| step\_name | enum: welcome, role, sectors, watchlist, success | Which step was viewed |
| step\_index | integer | Position of this step in the flow |

**Why**

Measures progression and drop-off.

**Questions Answered**

•        Which screen loses users?

•        Are users reaching Watchlist setup?

**Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Step Reach Rate (per step) | users reaching step\_viewed{step\_name} / users with onboarding\_started | Computed independently per step\_name — never summed across steps, so each value is bounded at 100% |

 

### **Event: onboarding\_step\_completed**

**Trigger:** User successfully completes a given onboarding step.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| step\_name | enum | Which step was completed |
| step\_index | integer | Position of this step in the flow |
| time\_on\_step\_seconds | integer | Time spent on the step before completing it |

**Why**

Measures successful progression.

**Questions Answered**

•        Which onboarding step creates friction?

**Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Step Completion Rate (per step) | step\_completed{step\_name} / step\_viewed{step\_name} | Per step\_name |

 

### **Event: onboarding\_step\_skipped**

**Trigger:** User explicitly taps “skip” on a step.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| step\_name | enum | Which step was skipped |
| step\_index | integer | Position of this step in the flow |

**Why**

Critical because onboarding is skippable.

**Questions Answered**

•        What information are users unwilling to provide?

•        Is Watchlist setup perceived as too much effort?

**Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Skip Rate (per step) | step\_skipped{step\_name} / step\_viewed{step\_name} | Per step\_name |

 

### **Event: onboarding\_abandoned**

**Trigger:** User exits the app or navigates away from onboarding without completing or explicitly skipping the final step, and does not return within 24 hours.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| last\_step\_viewed\_name | enum | Last step the user saw before abandoning |
| last\_step\_viewed\_index | integer | Position of the Last step the user saw before abandoning |
| time\_in\_onboarding\_seconds | integer | Total time spent before abandoning |

**Questions Answered**

•        At which step do we lose users silently, with no explicit skip action?

•        How many onboarding starts never resolve into either completion or an explicit skip?

**Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Abandonment Rate | onboarding\_abandoned / onboarding\_started | Distinct users |

 

### **Event: onboarding\_role\_selected**

**Trigger:** User selects their role on the role step.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| role | string | Selected role |
| step\_name | enum |  |
| step\_index | integer |  |

**Why**

Defines ICP.

**Questions Answered**

•        Which ICPs are most common?

•        Which ICPs retain best?

 

### **Event: onboarding\_sectors\_selected**

**Trigger:** User selects one or more sectors of interest.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| sector\_count | integer | Number of sectors selected |
| selected\_sectors | array\<string\> | Which sectors were selected |
| step\_name | enum |  |
| step\_index | integer |  |

**Why**

Measures personalization depth.

**Questions Answered**

•        Which sectors are most popular?

•        Does more personalization improve engagement?

 

### **Event: onboarding\_completed**

**Trigger:** User reaches the final “success” step of onboarding.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| role\_selected | string | Role chosen during onboarding |
| sector\_count | integer | Sectors selected |
| watchlist\_count | integer | Entities added to Watchlist during onboarding |
| selected\_sectors | array\<string\> | Which sectors were selected |
| completion\_time\_seconds | integer | Total time to complete onboarding |

**Why**

Measures onboarding quality.

**Questions Answered**

•        Does onboarding quality predict retention? (H6)

**Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Onboarding Completion Rate | onboarding\_completed / onboarding\_started | Distinct users |

 

***Note:** Watchlist additions made during onboarding are captured by the unified watchlist\_entity\_added event with source \= onboarding (Section 10).*

 

# **5\. App Open & Sessions**

Defined in full in Section 2.3, since identity and session boundaries needed to be established before any other event could be discussed precisely. This section exists in the Table of Contents as the canonical pointer: session\_started and session\_ended are the foundation for DAU/WAU/MAU and for every per-session metric in this document.

**See:** Section 2.3 for event definitions; Section 13 for how DAU/WAU/MAU are computed from them.

### **Event: explore\_opened**

**Trigger:** User opens the Watchlist screen.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| entry\_source | string | New |

### **Event: explore\_content\_type\_switched**

**Trigger:** Fires when user toggles between Articles and Companies in Explore.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| switched\_to | enum: articles, companies | Direction of switch |

### **Event: explore\_filter\_applied**

**Trigger:** Fires when user taps any sub-nav pill (Latest, Funding, Features, M\&A, Startup Stories, or any of the 17 sector pills). This is the primary way users express content intent in Explore — without it you're blind to what people actually want to read.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| filter\_label | string | Exact pill tapped (e.g. "Fintech", "Funding") |
| content\_type | Enum: articles, companies | Which toggle was active |

# **6\. Brief**

### **Event: brief\_loaded**

**Trigger:** The daily Brief screen finishes loading for the user.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| brief\_date | date | Editorial date of the Brief shown |
| card\_count | integer | Total cards in this Brief |
| watchlist\_card\_count | integer | Cards matching the user's Watchlist |
| editorial\_card\_count | integer | Editorially curated cards |
| signal\_card\_count | integer | Algorithmic/signal-driven cards |

**Why**

Starting point of the daily habit.

**Questions Answered**

•        How many users access the Brief?

•        Does personalization impact engagement?

**Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Brief Open Rate | distinct users with brief\_loaded / DAU | Distinct users in both numerator and denominator |

 

### **Event: brief\_card\_viewed**

**Trigger:** A Brief card becomes visible on screen (impression).

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| card\_id | string |   |
| article\_id | string |   |
| card\_position | integer | Position within the Brief |
|  |  |  |
|  |  |  |
| is\_watchlist\_hit | boolean | Whether this card matched a tracked entity |
| is\_sector\_hit | boolean | Whether this card matched a tracked sector |

**Why**

Measures exposure.

**Questions Answered**

•        Which positions get viewed?

•        Are users reaching the end?

**Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Card Reach Rate (per position) | users viewing card\_viewed{card\_position=N} / users with brief\_loaded | Computed per card\_position; monotonically non-increasing as N grows, never exceeds 100% |

 

### **Event: brief\_card\_expanded**

**Trigger:** User taps to expand a card's summary.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| article\_id | string |   |
| card\_id | string |   |
| card\_position | integer |   |
| is\_watchlist\_hit | boolean | Whether this card matched a tracked entity |
| is\_sector\_hit | boolean | Whether this card matched a tracked sector |

**Why**

Represents active interest.

**Questions Answered**

•        Which stories generate curiosity?

•        Do watchlist stories outperform editorial stories? (H2)

**Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Expansion Rate | card\_expanded / card\_viewed | Raw events; segment by is\_watchlist\_hit for H2 |

 

### **Event: brief\_article\_opened**

**Trigger:** User taps through from a Brief card into the full article.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| article\_id | string |   |
| card\_id | string |   |
| card\_position | integer |   |
| is\_watchlist\_hit | boolean | Whether this card matched a tracked entity |
| is\_sector\_hit | boolean | Whether this card matched a tracked sector |

**Why**

Measures transition from summary to deep reading.

**Questions Answered**

•        Which Brief stories drive reading?

•        What content types create depth?

**Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Brief Article CTR | article\_opened / card\_viewed | Raw events; segment by is\_watchlist\_hit for H2 |

 

### **Event: brief\_story\_saved**

**Trigger:** User saves a story directly from the Brief.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| article\_id | string |   |
| card\_type | string |   |

**Why**

Strong value signal.

**Questions Answered**

•        Which content is worth revisiting?

**Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Save Rate | brief\_story\_saved / card\_viewed | Raw events |

**FIX:** v1 had no Metrics section for this event despite calling it a “strong value signal.”

 

### **Event: `brief_session_ended`** 

**Trigger:** See Section 3.2 for the full completion definition.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| cards\_viewed | integer |   |
| brief\_date | date | Editorial date of the Brief shown |
| card\_count | integer |  |
| cards\_expanded\_id | Integer \<array\> |   |
| cards\_expanded\_count | integer |  |
| session\_duration\_seconds | integer |   |
| is\_watchlist\_hit | boolean |  |
| is\_sector\_hit | boolean |  |
| completion\_type | enum: full, exited | How completion was reached — see Section 3.2 |
| scroll\_depth\_pct | number | Final scroll depth at completion |

**Why**

Primary product success metric.

**Questions Answered**

•        Are users completing the habit?

•        Does completion predict retention? (H3)

**Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Brief Completion Rate | distinct users with brief\_session\_ended{completion\_type=full} / distinct users with brief\_loaded | Report “full” completion as the primary metric; report “full \+ exited” as a secondary “any engagement” variant |

# **7\. Articles**

### **Event: article\_opened**

**Trigger:** User opens a full article from any surface.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| article\_id | string |   |
| article\_type | string |   |
| source | enum: brief, explore, search, profile, notification |   |
| tags | array\<string\> |   |

**Why**

Measures content consumption.

**Questions Answered**

•        Which surfaces drive reading?

 

### **Event: article\_completed**

**Trigger:** See Section 3.2 for the full completion definition (scroll depth or active time threshold).

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| article\_id | string |   |
| article\_type | string |  |
| read\_time | integer |   |
| tags  | array\<string\> |  |
| source | string |   |
| scroll\_depth\_pct | number | New — required by the Section 3.2 completion definition |
| active\_time\_seconds | number | New — excludes time the app was backgrounded |
|  |  |  |

**Why**

Measures actual consumption, not just opens.

**Questions Answered**

•        Are users reading or merely opening?

**Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Article Completion Rate | article\_completed / article\_opened | Raw events |

 

### **Event: article\_saved**

**Trigger:** User saves an article for later.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| article\_id | string |   |
| source | string |   |
| article\_type  | string |  |
| tags | array\<string\> |  |
| scroll\_depth\_pct  | number |  |
| time\_since\_opened\_seconds  | number |  |
| is\_completed  | boolean  |  |
|  |  |  |
|  |  |  |

**Why**

Measures perceived value.

**Questions Answered**

•        Which content is worth revisiting outside the Brief?

**Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Save Rate | article\_saved / article\_opened | Raw events |

 

### **Event: article\_shared**

**Trigger:** User shares an article to an external destination.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| article\_id | string |   |
| source | string |   |
| article\_type  | string |  |
| tags | array\<string\> |  |
| destination  | string |  |
| scroll\_depth\_pct  | number |  |
| time\_since\_opened\_seconds  | number |  |
| is\_completed  | boolean  |  |

**Why**

Measures advocacy and distribution.

**Questions Answered**

•        What content drives organic distribution?

**Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Share Rate | article\_shared / article\_opened | Raw events |

# **8\. Search**

### **Event: search\_executed**

**Trigger:** User submits a search query.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| search\_id | UUID | New — join key to search\_result\_clicked, enabling per-query success measurement |
| query\_length | integer |   |
| query | string | Raw query text. Access-restricted; see Section 15 for redaction and retention policy. Only query\_length and a derived query\_category reach the main analytics warehouse. |
| result\_count | integer |   |
| has\_results  | boolean |  |

**Why**

Strong indicator of intent.

**Questions Answered**

•        How often do users actively seek intelligence? (H4)

**Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Search Usage Rate | distinct users\_who\_searched / DAU | Distinct users |

 

### **Event: search\_result\_clicked**

**Trigger:** User taps a search result.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| search\_id | UUID | New — links this click back to its originating search\_executed event |
| query | string | Raw query text. Access-restricted; see Section 15 for redaction and retention policy. Only query\_length and a derived query\_category reach the main analytics warehouse. |
| result\_type | enum: company, article, sector |   |
| result\_position | integer |   |
| result\_id  | UUID |  |

**Why**

Measures search quality.

**Questions Answered**

•        Are users finding useful results?

**Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Search Success Rate | distinct search\_id with ≥ 1 result\_clicked / distinct search\_id with search\_executed | Computed per search, not as a daily aggregate — enables analysis of which queries succeed, supporting H4 |


# **9\. Company Profiles**

### **Event: company\_profile\_viewed**

**Trigger:** User views a company profile / Datalabs page.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| company\_id | string |   |
| sector | string |   |
| stage | string |   |
| source | string |   |

**Why**

Measures movement into startup intelligence.

**Questions Answered**

•        Is journalism driving Datalabs exploration?

**Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Profile Views / DAU | company\_profile\_viewed events / DAU | Numerator is raw events (one user can view multiple profiles); denominator is distinct users |

 

### **Event: company\_related\_article\_clicked**

**Trigger:** User clicks an article recommended from a company profile.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| article\_id | string | New |
| company\_id | string | New |

**Why**

Measures the bridge between data and journalism.

**Questions Answered**

•        Are profiles generating content consumption?

**Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Profile→Article CTR | company\_related\_article\_clicked / company\_profile\_viewed | Raw events |

 

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Follow Conversion Rate | watchlist\_entity\_added{entity\_type=company, source=profile} / company\_profile\_viewed | Raw events. Replaces the broken v1 formula. |

 

# **10\. Watchlist (Unified)**

### **Event: watchlist\_entity\_added**

**Trigger:** User adds any entity (company, sector, person, or topic) to their Watchlist, from any surface.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| entity\_type | enum: company, sector, person, topic |   |
| entity\_id | string |   |
| entity\_name | string |   |
| source | enum: onboarding, brief, profile, search, notification | New — makes this one event usable everywhere instead of duplicating it per surface |
| position | integer, nullable | Populated only when added from a suggested/ranked list, e.g. onboarding suggestions |

**Questions Answered**

•        What drives Watchlist adoption?

•        Which suggested entities perform best?

•        Which surfaces create follows?

**Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Watchlist Adoption Rate | distinct users\_with\_watchlist / DAU | Distinct users |
| Adds per Source | watchlist\_entity\_added grouped by source | Raw events, segmented |

 

### **Event: watchlist\_entity\_removed**

**Trigger:** User removes an entity from their Watchlist.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| entity\_type | enum | New  |
| entity\_id | string | New |
| entity\_name | string |   |
| source | string | New — surface the removal happened from |
| days\_since\_added | integer | New — enables “how long before abandonment” analysis |

**Why**

Measures personalization churn.

**Questions Answered**

•        What entities are being abandoned?

•        How long do users keep entities before abandoning them?

 

### **Event: watchlist\_opened**

**Trigger:** User opens the Watchlist screen.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| entry\_source | string | New |

**Why**

Measures engagement with the personalization layer.

**Questions Answered**

•        Are users revisiting tracked entities?

**Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Watchlist Revisit Rate | watchlist\_opened / DAU, among users\_with\_watchlist | Distinct users in denominator |

 

### **Event: watchlist\_alert\_opened**

**Trigger:** User opens a Watchlist alert/notification.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| alert\_type | string |   |
| alert\_id | string | New — join key to the backend notification dispatch log |

**Why**

Measures effectiveness of the alert system.

**Questions Answered**

•        Are alerts driving re-engagement?

**Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Alert Open Rate | alert\_opened / alerts\_sent | alerts\_sent is not a client event — it is a backend record from the notification dispatch service, joined via alert\_id |

 

# **11\. Notifications**

### **Event: notification\_permission\_requested**

**Trigger:** App prompts the user for push notification permission.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| trigger\_context | enum: onboarding, first\_brief, manual\_settings | New event |

**Why**

Push effectiveness cannot be evaluated without knowing the opt-in funnel.

**Questions Answered**

•        When do we ask for permission, and does that timing matter?

 

### **Event: notification\_permission\_granted / notification\_permission\_denied**

**Trigger:** User responds to the OS permission prompt.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| trigger\_context | string | Matches the preceding request event |

**Why**

Defines the addressable audience for all push metrics.

**Questions Answered**

•        What share of users can even receive notifications?

**Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Push Opt-in Rate | notification\_permission\_granted / notification\_permission\_requested | Distinct users |

**FIX:** New events, paired with notification\_permission\_requested above.

 

### **Event: push\_received**

**Trigger:** Device receives a push notification.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| notification\_type | enum: morning\_brief, watchlist\_alert, breaking\_news, completion\_nudge, winback |   |
| alert\_id | string, nullable | New — for watchlist\_alert type, joins to the backend dispatch log |

**Why**

Establishes the denominator for push engagement.

 

***Note:** iOS delivery receipts are unreliable when the app is fully killed (the OS does not always wake the app to log push\_received). Treat any push\_received-based denominator as a likely undercount, not a data-quality bug — cross-check against the backend dispatch log's sent count where precision matters.*

### **Event: push\_opened**

**Trigger:** User taps a push notification.

**Properties**

| Property | Type / Values | Description |
| :---- | :---- | :---- |
| notification\_type | string |   |
| alert\_id | string, nullable | New |

**Why**

Measures notification effectiveness.

**Questions Answered**

•        Which notification types drive engagement?

**Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Push CTR | push\_opened / push\_received | Raw events; report alongside the backend dispatch “sent” count given the push\_received caveat above |

 

 

# **12\. Installs & Attribution**

***Note:** New section. v1 used “installs” as a metric denominator (Onboarding Start Rate) without ever defining where that number comes from.*

•        installs is not a client analytics event. It is sourced from the Mobile Measurement Partner (MMP — e.g. AppsFlyer or Adjust) install log.

•        Join key: the device-level attribution identifier (IDFA/GAID where available, otherwise probabilistic matching) is mapped to anonymous\_id at first open via the MMP SDK callback.

•        Any metric whose denominator is “% of installs that...” (e.g. Onboarding Start Rate) must use this MMP-joined install count, not a client-side proxy.

 

# **13\. Core Business Metrics Dashboard**

Every metric below states its unit (distinct users, distinct sessions, or raw events) explicitly — v1 left this ambiguous for several metrics, most notably Brief Open Rate.

## **13.1 Habit Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| DAU / WAU / MAU | distinct stitched user identities with ≥ 1 session\_started in the period | Distinct users — see Section 2.3 |
| Brief Open Rate | distinct users with brief\_loaded / DAU | Distinct users / distinct users |
| Brief Completion Rate | distinct users with brief\_session\_ended{completion\_type=full} / distinct users with brief\_loaded | Distinct users / distinct users — see Section 3.2 |
| Article Completion Rate | article\_completed / article\_opened | Raw events / raw events (a user opens many articles per day) |

## **13.2 Personalization Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Watchlist Adoption Rate | distinct users\_with\_watchlist / DAU | Distinct users |
| Average Watchlist Size | mean count of active (non-removed) entities, per user\_with\_watchlist | User-level average |
| Average Sector Count | mean sector\_count from onboarding\_sectors\_selected, per user | User-level average |
| Follow Conversion Rate | watchlist\_entity\_added{entity\_type=company, source=profile} / company\_profile\_viewed | Raw events — see Section 9 fix |

## **13.3 Intelligence Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| Search Usage Rate | distinct users\_who\_searched / DAU | Distinct users |
| Company Profile Views / DAU | company\_profile\_viewed events / DAU | Raw events / distinct users |
| Profile → Follow Conversion | same formula as Follow Conversion Rate above | Raw events |
| Search Success Rate | distinct search\_id with ≥ 1 click / distinct search\_id with a search | Per-search, not daily aggregate — see Section 8 fix |

## **13.4 Retention Metrics**

| Metric | Formula | Notes |
| :---- | :---- | :---- |
| D1 / D7 / D30 Retention | % of users with a first session\_started on day 0 who have ≥ 1 session\_started on day N | Distinct stitched users |

**Segmented by**

•        Role

•        Sector Count

•        Watchlist Size

•        Brief Completion Frequency (0–1, 2–3, 4–5 Briefs/week — see H3)

 

# **14\. Key Product Hypotheses to Validate**

| \# | Hypothesis | Measured via |
| :---- | :---- | :---- |
| H1 | Users with larger watchlists have higher Brief completion rates. | Average Watchlist Size vs. Brief Completion Rate (Section 13.1–13.2) |
| H2 | Watchlist-hit stories outperform editorial-only stories. | Expansion Rate, Brief Article CTR, and Article Completion Rate, each segmented by is\_watchlist\_hit |
| H3 | Brief completion predicts retention. | D7/D30 Retention segmented by Brief Completion Frequency buckets (0–1, 2–3, 4–5 Briefs/week) |
| H4 | Search users retain better than non-search users. | D7/D30 Retention segmented by users\_who\_searched vs. not |
| H5 | Company profile exploration increases likelihood of following companies and returning to the app. | Follow Conversion Rate and subsequent session\_started recency, segmented by company\_profile\_viewed activity |
| H6 | Higher onboarding personalization leads to stronger long-term engagement and retention. | sector\_count and watchlist\_count from onboarding\_completed vs. D7/D30 Retention and Brief Completion Rate |

 

# **15\. Privacy & Data Governance**

***Note:** New section. v1 stored raw free-text search queries with no redaction or retention policy — a PII and compliance risk, particularly under India's DPDP Act.*

## **15.1 Search Query Handling**

•        The main analytics warehouse receives only query\_length and a derived query\_category (e.g. company, sector, person, other — produced by a lightweight classifier), never the raw query text.

•        Raw query text is routed to a separate, access-controlled operational store with a 90-day retention limit, used only for search-relevance tuning by the search team.

•        Raw queries are purged on user account deletion requests, consistent with DPDP Act 2023 / GDPR data-subject erasure requirements.

## **15.2 General PII Minimization**

•        device\_id is hashed before it reaches analytics; raw IDFA/GAID values never enter the warehouse (see Section 2.1).

•        user\_id is an internal surrogate key — raw email or phone number is never used as an event property.

•        Tables joinable to user\_id are restricted to need-to-know roles; the raw search-query store is additionally restricted to the search/relevance team only.

 

# **16\. Open Items for Engineering Sign-off**

This PRD makes specific recommendations throughout (thresholds, timeouts, retention windows) so that engineering has a concrete starting point. The following still need explicit sign-off before build:

•        Session timeout window — recommended 30 minutes (Section 2.3).

•        Article completion thresholds 

•        Brief completion threshold .

•        Search query retention period and the query\_category classifier approach (Section 15.1).

•        Identity-stitching provider/method — e.g. Segment, Amplitude, or an in-house solution (Section 2.2).

•        Alert dispatch log schema and the alert\_id join key, to be confirmed with the backend notifications team (Sections 10–11).

•        MMP integration details for the installs/attribution join (Section 12).

•        Whether monetization/subscription events are in scope for this analytics system or deferred to a separate addendum — currently out of scope for v2.

•        Whether “explore” (referenced as an article\_opened source value) gets its own event section via a dedicated Explore PRD, or is folded into this document in a future revision.

  

# Inc42 App Growth & GTM Strategy

# **Inc42 App Growth & GTM Strategy**

## **Objective**

Increase Inc42 App adoption by converting existing Inc42 audience across owned channels into active app users.

The primary opportunity is not acquiring new audiences but converting users who already engage with Inc42 content through the website, newsletters, social media, events, and email communication.

---

# **Core Value Proposition**

Rather than positioning the app as another way to consume Inc42 content, position it as a startup intelligence platform.

Key messaging pillars:

* Track startups you care about  
* Get daily startup intelligence in minutes  
* Get real-time startup updates  
* Never miss funding rounds and major developments  
* Follow sectors, companies, and investors

Every acquisition surface should communicate one or more of these benefits rather than simply asking users to download the app.

---

# **Primary Growth Channels**

## **1\. Website (Highest Priority)**

The website is expected to be the largest source of app acquisition.

### **Mobile Web**

#### **Continue on App Banner**

Introduce a Reddit-style sticky bottom banner on mobile web.  
![][image1]

Trigger:

* On opening the article  
* 30% article scroll depth  
* OR 45+ seconds spent on page

Examples:

* Track this company on the Inc42 App  
* Get future updates on this startup  
* Follow funding developments in real time

---

#### **Article-End CTA**

Contextual CTAs based on article category.

AI Articles:

* Try Inc42 AI Bot  
* Unlock AI features on the Inc42 App

When users click on this, show a banner that says: This feature is exclusively available on the Inc42 App — absolutely free.  
![][image2]

Funding Articles:

* Track this startup on the Inc42 App

AI Articles:

* Get AI startup alerts

Fintech Articles:

* Follow India's fintech ecosystem

D2C Articles:

* Track leading consumer startups

---

#### **Homepage Promotion**

Persistent app promotion strip.  
![][image3]

Example:

Download the Inc42 App • Startup Alerts • Daily Briefings • Company Tracking

---

## **2\. Newsletter**

Newsletter subscribers represent a highly engaged audience already familiar with the Inc42 brand.

### **Newsletter Header Placement**

Placed before the first story.

Example:

Get real-time startup alerts and daily intelligence on the Inc42 App.

---

### **Newsletter Footer Placement**

Placed after the final story.

Example:

Continue tracking today's biggest startup developments on the Inc42 App.

---

### **Dedicated App Discovery Section**

Weekly recurring section showcasing:

* Most tracked startups  
* Trending companies  
* Top startup sectors  
* Popular watchlists

Purpose:  
Create curiosity and FOMO around app-exclusive experiences.

---

## **3\. Social Media**

Leverage existing social reach to continuously promote app adoption.

### **Carousel Posts**

Final slide includes:

Track startups, sectors, and investors on the Inc42 App.

---

### **Funding News Posts**

Include messaging such as:

Track this company and future funding updates on the Inc42 App.

---

### **Reels and Videos**

End screen should include:

Download the Inc42 App

Track startups in real time

---

### **Static Creatives**

Subtle app branding integrated into:

* LinkedIn posts  
* Instagram posts  
* Twitter/X creatives

---

## **4\. Events**

Events attract some of the highest-intent startup audiences.

### **Registration Flow**

App promotion included in:

* Registration pages  
* Confirmation emails  
* Event reminders

---

### **Venue Entry**

QR code-based app download promotion.

Potential future use cases:

* Event agenda  
* Speaker details  
* Session schedules  
* Networking

---

### **On-Ground Branding**

Include app messaging on:

* Event screens  
* Stage banners  
* Standees  
* Registration desks

---

### **Post-Event Follow-Up**

Use app as the destination for:

* Session recordings  
* Event highlights  
* Speaker summaries  
* Startup reports

---

## **5\. Direct Email Marketing**

Leverage existing email database.

### **Audience Segments**

* Newsletter subscribers  
* Event attendees  
* Registered website users  
* Dormant app users

---

### **Campaign Types**

#### **Startup Intelligence Campaign**

Example:

You've read 10 startup stories this month.

Track startups and get real-time updates on the Inc42 App.

---

#### **Weekly Trending Startups**

Showcase:

* Most followed startups  
* Trending sectors  
* Major funding rounds

Drive users into the app.

---

#### **Founder Campaigns**

Following startup coverage or funding announcements:

Subject:

Your company is being tracked on Inc42

Potential messaging:

* Number of followers  
* Profile views  
* Engagement growth

Encourage founders to share their startup profile.

# Ask In42

# **PRD: Ask42 Mobile Optimization (v1.0)**

## **Goal**

Optimize the desktop-first Ask42 backend for a native mobile app experience by addressing latency bottlenecks, context awareness, and response formatting constraints.

---

# **1\. Problem Statement**

Ask42 was designed for a desktop web interface. As we embed it into a native mobile app (iOS/Android), three critical friction points emerge:

### **1.1 Unacceptable Latency**

Mobile users expect responses in **\<3 seconds**. Currently, n8n webhook overhead and keep-alive byte hacks cause tools to hang for up to **8–25 seconds**.

### **1.2 Context Blindness**

Mobile apps have highly specific screens (e.g., viewing a specific Company Profile). The bot currently treats every query as a cold start, ignoring the user's current screen context.

### **1.3 Hostile Formatting**

The LLM generates massive "walls of text" (up to 900 words) and complex Markdown tables that break native mobile UI renderers. Citations are embedded as raw text links rather than tappable mobile widgets.

---

# **2\. Core Pillars of Improvement**

## **Pillar 1: Latency & Infrastructure Overhaul**

We must eliminate architectural middlemen that inflate response times.

### **1.1 Deprecate n8n for DB Lookups**

**Current State**

* `db_query` and other tools hit n8n webhooks, which then query the MySQL database.

**Solution**

* Rewrite the tool handlers in the FastAPI backend (`ask_agent/tools.py`) to connect directly to the MySQL/ScoutDB database via SQLAlchemy/asyncpg.  
* Eliminate the n8n HTTP hop entirely.

---

### **1.2 Fix the Timeout Reset Bug**

**Current State**

* n8n keeps connections alive by sending space characters ( ) every few seconds.  
* This bypasses standard HTTP timeouts (such as `httpx`), causing the backend to hang indefinitely on a dead tool.

**Solution**

* Replace `httpx` timeouts with a strict `asyncio.wait_for(timeout=TOOL_HARD_TIMEOUT)` wrapper in the agent loop.  
* Ensure the hard timeout is enforced regardless of keep-alive bytes.

---

## **Pillar 2: Context-Aware Query Resolution**

Mobile UI relies heavily on contextual floating action buttons (FABs). When a user asks *"What's happening?"* while on Zepto's page, the bot must know they mean Zepto.

### **2.1 Entry Point Context Injection**

Adopt the exact specifications from the [**Context-Aware PRD**]().

**Request Payload**

{  
  "entry\_point": "company",  
  "context\_entity": "zepto"  
}

**Behavior**

* The mobile app sends the contextual metadata in the `/query/stream` payload.  
* `analyzer.py` determines whether the query is referential (e.g., *"Summarize this"*).  
* If relevant, the context entity is injected into the prompt.  
* If the user explicitly overrides the context (e.g., *"Tell me about Swiggy"*), the page context is ignored.

---

## **Pillar 3: Mobile-Friendly Responses & UI**

We must enforce strict limits on the LLM's output and shift complex formatting to the frontend via structured JSON.

### **3.1 Mobile Mode (Text Limits & Formatting)**

Introduce an `is_mobile: bool` flag in the API request.

When `is_mobile=True`, modify `prompt.py` to:

* Cut word count limits by **50%** (Target: **150–200 words**).  
* Explicitly instruct the LLM:  
  * Do **not** use Markdown tables for comparisons.  
  * Format comparisons as bullet points.

---

### **3.2 Native Citation Widgets**

**Current State**

* The LLM currently hallucinates markdown links or adds `(Datalabs)` within the response text.

**Solution**

* Strictly enforce the backend `extract_sources_and_entities()` logic.  
* Extract all URLs, articles, and company links into the `sources` JSON array sent via SSE.  
* The mobile UI will render these sources as horizontal swipeable cards (widgets) at the bottom of the chat bubble, completely replacing in-text hyperlinks.

# Context-Aware PRD

# **PRD: Context-Aware Query Resolution for Ask42**

**Status:** Implementation Ready (pending article fetch endpoint URL)

**Scope:** Query interpretation only — no new tools, no new retrieval logic, no new response templates.

---

# **1\. Problem**

Every Ask42 query is treated as a cold-start query today. When a user is on Zepto's company page and asks *"What's happening?"*, the assistant has no way to know they mean Zepto. It defaults to a generic interpretation.

This breaks two classes of user behaviour that are increasingly common as Ask42 gets embedded across multiple product surfaces.

### **1.1 Referential Queries**

Queries such as:

* "How is it doing?"  
* "Summarize this"  
* "What does this mean for them?"

### **1.2 Contextual Follow-ups**

The user is already reading about a company or article and wants to go deeper without restating the context.

At the same time, blindly injecting the current page entity into every query creates a different failure mode:

> "Compare Blinkit and Instamart"

asked from Zepto's page should **not** involve Zepto.

---

# **2\. Goal**

Make Ask42 context-aware for referential and ambiguous queries, while ensuring explicit user intent always wins over page context.

### **Out of Scope**

* New retrieval logic or data sources  
* New response templates or formatting changes  
* Changes to any tool handlers  
* Prompt restructuring

---

# **3\. Surfaces That Send Context**

Ask42 is embedded across multiple surfaces. Each sends an optional context payload with the query.

| Surface | Entry Point | Context Payload |
| ----- | ----- | ----- |
| Company page | `company` | `contextEntity: "zepto"` (slug) |
| Article page | `article` | `articleId: "abc123"` |
| Brief page | `brief` | `articleId: "brief-xyz"` (treated as article) |
| Investor page *(future)* | `investor` | `contextEntity: "sequoia-capital-india"` |
| Sector page *(future)* | `sector` | `contextEntity: "fintech"` |
| Homepage / Global | *(none)* | No context payload |

---

# **4\. Context Resolution Logic**

The GPT-4.1-nano analyzer—which already runs on every query—makes the context relevance decision within the same classifier call, adding **zero latency**.

### **Use Page Context If**

* Query uses pronouns referring to no explicit entity (`it`, `they`, `this company`)  
* Query uses vague temporal references (`what's happening`, `lately`, `these days`)  
* Query has no named entity but the page context provides one  
* Query explicitly references the current page (`summarize this`, `why does this matter`)

### **Ignore Page Context If**

* Query names specific entities different from the page context  
* Query asks about a sector, trend, or topic unrelated to the page entity  
* Query is fully self-contained and interpretable without context  
* When in doubt → ignore

### **Priority Order**

Always resolve context in the following order:

1. Explicit user entities and intent  
2. Conversation history  
3. Page context

---

# **5\. Analyzer Output Changes**

The analyzer JSON gains two new fields.

{

  "mode": "fast",

  "query\_type": "summarize",

  "entities": \[\],

  "enrichment\_slugs": \[\],

  "result\_limit": 10,

  "context\_used": true,

  "requires\_article\_fetch": true

}

### **New Fields**

| Field | Type | Description |
| ----- | ----- | ----- |
| `context_used` | `bool` | Whether page context is relevant to this query |
| `requires_article_fetch` | `bool` | True only when `query_type == "summarize"` and entry point is article/brief |

### **New Query Type**

| Type | When | Behavior |
| ----- | ----- | ----- |
| `summarize` | Query asks to summarize/explain the current article or page | Fetch article content → inject → Claude summarizes. No agent tool calls. |

---

# **6\. Execution Paths**

## **Path A — Summarize (Article / Brief Entry Points Only)**

Request:

{query: "summarize this", entryPoint: "article", articleId: "abc123"}

        │

        ▼

Analyzer

query\_type \= "summarize"

context\_used \= true

requires\_article\_fetch \= true

        │

        ▼

Pre-fetch Phase

Check session cache using articleId

Cache hit

    → Use cached condensed article

Cache miss

    → Fetch article by ID

    → Condense:

        • Title

        • Date

        • Key entities

        • First 3 paragraphs

    → Store in session

        │

        ▼

Inject condensed article into system prompt

        │

        ▼

Claude synthesizes summary

(No agent tool calls.

No enrichment prefetch.)

---

## **Path B — Normal Query with Context Enrichment**

Request:

{query: "how is it doing?",

 entryPoint: "company",

 contextEntity: "zepto"}

        │

        ▼

Analyzer

query\_type \= "company"

context\_used \= true

entities \= \["zepto"\]

        │

        ▼

Pre-fetch Phase

"zepto"

↓

Added to enrichment\_slugs

↓

Existing enrichment pipeline runs

↓

ES profile \+ financials loaded

        │

        ▼

Normal agent loop

Claude already has Zepto enrichment context

---

## **Path C — Context Ignored**

Request:

{query: "compare Blinkit and Instamart",

 entryPoint: "company",

 contextEntity: "zepto"}

        │

        ▼

Analyzer

context\_used \= false

        │

        ▼

Everything behaves exactly as today.

Zepto is never referenced.

---

# **7\. Multi-Turn Behaviour**

The session-level article cache ensures an article is fetched at most once per conversation, regardless of how many follow-up questions are asked.

| Turn | Query | Analyzer | Behavior |
| ----- | ----- | ----- | ----- |
| 1 | "summarize this" | `context_used=true`, `summarize` | Fetch article → Store in session → Summarize |
| 2 | "compare Blinkit and Instamart" | `context_used=false` | Normal query, article not injected |
| 3 | "what's the author's main argument?" | `context_used=true` | Read from session (no re-fetch) → Inject → Answer |

---

# **8\. Request Schema Changes**

New optional fields are added to `QueryRequest`.

All are optional and fully backward compatible.

class QueryRequest(BaseModel):

    chatInput: str \= ""

    query: str \= ""

    mode: str \= ""

    session\_id: str \= ""

    bypass\_cache: bool \= False

    conversation\_history: list\[dict\] \= \[\]

    entity\_hints: list\[str\] \= \[\]

    \# New — Page Context

    entry\_point: str \= ""        \# "company" | "article" | "brief" | "investor" | "sector" | ""

    context\_entity: str \= ""     \# slug for company/investor/sector entry points

    article\_id: str \= ""         \# article/brief ID

Existing callers that do not send these fields experience **zero behavior change**.

---

# **9\. Cache Key Changes**

When `context_used == true`, include the context entity or article ID in the cache key.

### **Current**

cache\_key \= hash(normalized\_query)

### **Updated**

cache\_key \= hash(normalized\_query \+ ":" \+ context\_entity\_or\_article\_id)

    if context\_used else hash(normalized\_query)

This ensures identical queries from different pages receive different cache entries.

Example:

* "What's happening?" on Zepto  
* "What's happening?" on Swiggy

These now generate separate cache keys.

---

# **10\. Files Changed**

| File | Changes | Approx. Scope |
| ----- | ----- | ----- |
| `server.py` | Accept new request fields, trigger article fetch, seed enrichment slug, inject article block | \~40 lines |
| `analyzer.py` | Append page context, parse new JSON fields, extend `AnalyzerResult` | \~25 lines |
| `session.py` | Add `article_cache: dict[str, str]` | \~10 lines |
| `cache.py` | Include context in cache key | \~5 lines |
| `prompt.py` | Add optional `page_context_block` parameter | \~5 lines |
| `ask_agent/article_context.py` *(new)* | `fetch_article_by_id()` \+ `condense_article()` | \~50 lines |

### **Files Not Modified**

* `tools.py`  
* `agent.py`  
* `enrichment.py`  
* `analytics.py`  
* `fallback.py`  
* `validation.py`  
* `charts.py`  
* All tool definitions  
* All tool handlers

---

# **11\. Article Condensation**

The condensed article injected into the prompt contains:

* Title  
* Publication date  
* Key entities mentioned (companies, people)  
* First 2–3 paragraphs of the body  
* Target size: **under 800 characters**

This keeps the additional context lightweight while remaining within the prompt budget.

---

# **12\. What Is Not Changing**

| Concern | Decision |
| ----- | ----- |
| Tool set | No new tools. `article_context.py` is an internal utility, not an agent tool. |
| Agent loop | Unchanged for Paths B and C. Path A bypasses it and is the only new execution path. |
| Enrichment logic | Unchanged. The page entity is simply added to the existing enrichment slug pipeline. |
| Response formatting | Unchanged. No new templates or response sections. |
| Session memory | Existing conversation memory remains unchanged. Only `article_cache` is added. |

---

# **13\. Open Item**

### **Article Fetch Endpoint**

`fetch_article_by_id(article_id)` requires:

* Endpoint URL  
* Expected response schema (title, body, date, author)  
* Required authentication headers

All remaining implementation work can proceed independently. The `article_context.py` module will remain stubbed until the endpoint is finalized.

# My Inc42 Relevance Engine

# **My Inc42 Relevance and Emphasis Engine (V1)**

## **Objective**

Help users identify what matters most in the startup ecosystem through relevance-based prioritization.

The Brief structure remains fixed for all users.

Relevance influences:

* Summary generation  
* Content ranking  
* Recommended reads  
* DataLabs signals

# **Founder**

### **What stage is your startup currently in?**

Options:

* Idea / MVP  
* Pre-Seed  
* Seed  
* Series A  
* Series B/C  
* Series D+/Pre-IPO  
* Listed Company

{  
Mapping:  
**Early Stage Startups**

* Idea/MVP  
* Pre-Seed  
* Seed

**Growth Stage Startup**

* Series A  
* Series B/C

**Late Stage Startups**

* Series D+  
* Pre-IPO

**Listed Startups**

* Listed Company

}

### **Which industry are you building in?**

Multi-select.:

* Ecommerce  
* Media & Entertainment  
* Fintech  
* Edtech  
* Travel Tech  
* Agritech  
* Health Tech  
* Clean Tech  
* Logistics  
* Real Estate Tech  
* Consumer Services  
* Foodtech  
* Enterprise Services  
* Enterprise Tech  
* Web3  
* Advanced Hardware & Technology  
* AI

### **What are your top priorities right now?**

Select up to 3\.

* Capital & Fundraising  
* Growth & Market Expansion  
* Product & Technology  
* People & Organization  
* Partnerships & Ecosystem  
* Business Performance  
* Regulatory & Legal  
* Operations  
* Competitive Intelligence  
* Exit & Liquidity

### **Which companies do you want to track?**

Search \+ Select

Examples:

* Razorpay  
* Zepto  
* Zomato  
* Postman

### **Which industries do you want to track?**

Multi-select

Examples:

* Fintech  
* SaaS  
* AI  
* Quick Commerce

# **Investor**

### **What type of investor are you?**

* Angel Investor  
* Micro VC  
* VC Fund  
* Family Office  
* Corporate VC  
* PE Fund  
* Scout

### **Which stages do you invest in?**

Multi-select

* Idea / MVP  
* Pre-Seed  
* Seed  
* Series A  
* Series B/C  
* Series D+/Pre-IPO  
* Listed Company

### **Which sectors do you invest in?**

Multi-select

Same industry list.

### **Which companies do you want to monitor?**

Search \+ Select

### **Which industries do you want to track?**

Multi-select

# **Startup Operator**

(PM, Growth, Product, Marketing, Strategy, etc.)

### **What best describes your role?**

* Product  
* Growth  
* Marketing  
* Operations  
* Strategy  
* Data  
* Design  
* Engineering

### **Which industry do you work in?**

Multi-select

### **Which companies do you want to track?**

Search \+ Select

### **Which industries do you want to track?**

Multi-select

# **BD & Partnerships**

### **Which industry do you work in?**

Multi-select

### **Which companies do you want to track?**

Search \+ Select

### **Which industries do you want to track?**

Multi-select

# **Others**

### **What best describes your role?**

—--

### **Which companies do you want to track?**

Search \+ Select

### **Which industries do you want to track?**

Multi-select

# **Relevance Scoring**

Every content item receives:

Relevance Score \=  
Industry Match \+  
Stage Match \+  
Focus Match \+  
Tracked Entity Match 

The score determines emphasis in the summary

# **Brief Structure**

## **1\. Industry Pulse**

Purpose:  
Provide ecosystem orientation.

Input:

* Breaking News  
* Industry Developments  
* Reports  
* Editorial Analysis

### **Personalization Logic**

The underlying content remains unchanged.

The interpretation and ranking change.

### **Example**

Label:

Relevant because you operate in AI.

Summary:

AI infrastructure and enterprise software continue attracting investor attention while adoption expands across industries.

### **Story Cards**

Headline

Summary

Article CTA

Relevance Label

Examples:

Relevant because you operate in fintech.

Relevant because you are a Seed-stage founder.

Relevant because you track OpenAI.

## **2\. Funding Intelligence**

Purpose:  
Explain capital movement across the ecosystem.

### **Components**

Funding Climate

Key Deals

Active Investors

### **Funding Climate**

AI-generated overview.

Example:

Relevant because fundraising is your current focus.

Seed-stage activity remained strong this week with increased participation from AI-focused investors.

### **Key Deal Cards**

Company

Sector

Stage

Amount Raised

Investors

Use of Funds

Relevance Label

Example:

Relevant because you are a Seed-stage founder.

### **Active Investor Cards**

Investor Name

Recent Activity

Relevance Label

Example:

Relevant because fundraising is your current focus.

## **3\. DataLabs Signals**

Purpose:  
Track entities the user cares about.

Visible only to logged-in users.

### **Input**

Tracked Companies

Tracked Investors

Tracked Sectors

### **Signal Types**

Funding Event

Acquisition

Partnership

Leadership Change

Product Launch

Hiring Activity

### **Signal Card**

Entity

Signal

Impact Summary

Relevance Label

Example:

Relevant because you track OpenAI.

OpenAI launches enterprise pricing model.

## **4\. Suggested Reads**

Purpose:  
Surface relevant content from the editorial pool.

### **Recommended For You**

Based on:

* Industry  
* Stage  
* Focus Area  
* Tracked Companies

Example:

Relevant because fundraising is your current focus.

Fundraising Lessons From Recent Seed Founders.

# **Daily Brief Generation Workflow**

## **Step 1**

Fetch all brief-eligible content.

Approx. 11 articles/day.

## **Step 2**

Content Enrichment

Generate metadata:

* Industry  
* Companies  
* Topics  
* ICP  
* Funding Stage  
* Focus Areas

## **Step 3**

Calculate Relevance Scores

Apply scoring model.

## **Step 4**

Generate Section Summaries

Modify emphasis based on user profile.

## **Step 5**

Rank Content

Rank stories within sections.

Do not change section order.

## **Step 6**

Generate Recommendations

Create Suggested Reads section.

## **Step 7**

Inject Relevance Labels

Every personalized item must explain why it appears.

Examples:

Relevant because you track OpenAI.

Relevant because you are building in fintech.

Relevant because fundraising is your current focus.

Relevant because you are a Seed-stage founder.

---

# **Design Principles**

1. Fixed Brief Structure

Every user sees the same section order.

---

2. Relevance Over Personalization

Do not create different products for different users.

Prioritize what matters.

---

3. Interpretation Over Filtering

The goal is not to hide content.

The goal is to explain and prioritize content.

---

4. Explainability

Every personalized recommendation must include a reason.

Users should always understand why something appears.

---

# **Layer 2: Emphasis**

## **Purpose**

Determine which information should receive prominence within an article for a specific ICP.

The goal is not to change facts or generate interpretation.

The goal is to change information hierarchy.

Different users should notice different aspects of the same article.

---

## **Inputs**

* ICP

---

## **Outputs**

* Lead sentence  
* Information ordering  
* Highlighted metrics  
* Highlighted entities  
* Highlighted quotes  
* Highlighted facts

---

## **Rules**

Never change:

* Facts  
* Numbers  
* Events  
* Entities

Only change:

* What appears first  
* What receives emphasis  
* What receives less prominence

This is information-level personalization.

Not interpretation.

---

# **Founder Emphasis Framework**

## **Core Principle**

Treat every article as a case study in company building.

Question:

"What can another founder learn from how this company is being built, operated, scaled, defended, or improved?"

---

## **Prioritize**

### **Execution**

Examples:

* Product launches  
* Operational improvements  
* Strategic decisions  
* Cost reductions  
* Process changes

---

### **Growth**

Examples:

* Revenue growth  
* Customer growth  
* Market expansion  
* Distribution expansion

---

### **Product**

Examples:

* New products  
* Product strategy  
* Technology investments

---

### **Operations**

Examples:

* Hiring  
* Layoffs  
* Efficiency improvements  
* Supply chain decisions

---

### **Strategy**

Examples:

* Acquisitions  
* Expansion plans  
* Market entry  
* Positioning changes

---

### **Compliance**

Examples:

* Regulatory requirements  
* Policy impact  
* Legal obligations

---

## **Deprioritize**

* Secondary share sales  
* Investor liquidity  
* Investor ownership changes  
* Capital market mechanics

Unless central to the article.

---

# **Investor Emphasis Framework**

## **Core Principle**

Treat every article as a signal for evaluating a company, market, or investment opportunity.

Question:

"What does this development reveal about investment attractiveness, risk, or future returns?"

---

## **Prioritize**

### **Capital Flows**

Examples:

* Funding amount  
* Investor participation  
* Debt raised  
* Capital allocation

---

### **Market Position**

Examples:

* Market leadership  
* Competitive advantage  
* Expansion  
* Consolidation

---

### **Financial Performance**

Examples:

* Revenue  
* Profitability  
* Margins  
* Cash efficiency

---

### **Risk**

Examples:

* Regulatory risk  
* Legal issues  
* Governance concerns  
* Operational challenges

---

### **Liquidity**

Examples:

* IPO filings  
* Secondary transactions  
* Exits  
* Share sales

---

### **Sector Signals**

Examples:

* Government support  
* Regulatory changes  
* Infrastructure investment  
* Market shifts

---

## **Deprioritize**

* Product feature details  
* Minor operational decisions  
* Tactical execution details

Unless central to the article.

---

# **Information Ordering Rules**

## **Funding Article**

Founder Order:

1. Why capital is being raised  
2. What the company plans to build  
3. Growth plans  
4. Funding amount  
5. Investors

Investor Order:

1. Funding amount  
2. Investors  
3. Capital raised  
4. Company progress  
5. Use of funds

---

## **Financial Results Article**

Founder Order:

1. Revenue growth  
2. Profitability improvement  
3. Efficiency improvements  
4. Business decisions  
5. Market reaction

Investor Order:

1. Profitability  
2. Revenue  
3. Margins  
4. Growth quality  
5. Market implications

---

## **Acquisition Article**

Founder Order:

1. Strategic rationale  
2. Capability gained  
3. Expansion opportunity  
4. Acquisition details

Investor Order:

1. Market position impact  
2. Consolidation impact  
3. Competitive advantage  
4. Acquisition details

---

## **Policy / Regulation Article**

Founder Order:

1. Operational impact  
2. Compliance requirements  
3. Business changes required  
4. Effective timeline

Investor Order:

1. Portfolio impact  
2. Sector impact  
3. Regulatory risk  
4. Effective timeline

---

# **Lead Sentence Selection**

The lead sentence should contain the information most relevant to the ICP.

Example:

Article:

"Startup raises $20M. Revenue grows 150%. Expansion planned."

Founder Lead:

"The company plans to use fresh capital to accelerate expansion following 150% revenue growth."

Investor Lead:

"The company secured a $20M round after reporting 150% revenue growth."

Same facts.

Different emphasis.

---

# **Emphasis Guardrails**

Do not:

* Add interpretation  
* Add recommendations  
* Add predictions  
* Add trends  
* Add assumptions

Emphasis changes salience.

Interpretation changes meaning.

The Emphasis Layer must only change salience.

# Onboarding Flow

# **MyInc42 V1 Onboarding Flow**

## **First-Time User**

### **Step 1: Welcome Screen**

Headline:

Startup Intelligence In Under 5 Minutes

Subtext:

Get a quick overview of everything happening across the Indian startup ecosystem.

Why this step:  
We keep the first screen lightweight and frictionless so users can reach the core product value as quickly as possible. At this stage, data and light personalization are the priority, capturing a name and role gives us enough context to tailor the experience without creating onboarding fatigue. By avoiding login requirements, we reduce drop-off and let users experience the product's value before asking for any commitment.

What's your name?

What best describes you?

* Founder  
* Investor  
* Startup Operator  
* BD & Partnerships  
* Other

CTA:

Show My Brief

No login required.

---

## **Step 2: Guided Introduction**

User lands directly inside the Brief.

A lightweight walkthrough introduces the core sections.

### **Screen 1**

Industry Pulse

Understand the most important developments across the startup ecosystem.

---

### **Screen 2**

Funding Intelligence

Track funding activity, investors, and capital flows.

---

### **Screen 3**

Suggested Reads

Discover the most important stories and insights from across the ecosystem.

---

### **Screen 4**

Complete Today's Brief

Click Complete once you've finished reading today's brief.

Completing the brief unlocks your Day 1 streak.

CTA:

Complete Brief

---

## **Step 3: Personalization Prompt**

Triggered after user completes the Brief.

Headline:

Make This Brief Relevant To You

Subtext:

Track your industry, startup stage and companies you care about to receive a more relevant brief.

CTA:

Personalize My Brief

Secondary CTA:

Maybe Later

---

## **Step 4: Login**

Options:

* Continue with Google  
* Continue with Email

---

## **Step 5: Relevance Setup**

### **Founder**

#### **What stage is your startup currently in?**

* Idea / MVP  
* Pre-Seed  
* Seed  
* Series A  
* Series B/C  
* Series D+/Pre-IPO  
* Listed Company

Internal Mapping:

Early Stage Startups

* Idea/MVP  
* Pre-Seed  
* Seed

Growth Stage Startups

* Series A  
* Series B/C

Late Stage Startups

* Series D+  
* Pre-IPO

Listed Startups

* Listed Company

---

#### **Which industry best describes your startup?**

Multi-select

* Ecommerce  
* Media & Entertainment  
* Fintech  
* Edtech  
* Travel Tech  
* Agritech  
* Health Tech  
* Clean Tech  
* Logistics  
* Real Estate Tech  
* Consumer Services  
* Foodtech  
* Enterprise Services  
* Enterprise Tech  
* Web3  
* Advanced Hardware & Technology  
* AI

---

#### **Which companies do you want to track?**

Search \+ Select

Examples:

* Razorpay  
* Zepto  
* Zomato  
* Postman

Optional

---

#### **Which other industries do you want to track?**

Multi-select

Optional

Examples:

* AI  
* Fintech  
* Enterprise Tech  
* SaaS

---

### **Investor**

#### **What type of investor are you?**

* Angel Investor  
* Micro VC  
* VC Fund  
* Family Office  
* Corporate VC  
* PE Fund  
* Scout

---

#### **Which stages do you invest in?**

Multi-select

* Idea / MVP  
* Pre-Seed  
* Seed  
* Series A  
* Series B/C  
* Series D+/Pre-IPO  
* Listed Company

---

#### **Which sectors do you invest in?**

Multi-select

Same industry list.

---

#### **Which companies do you want to monitor?**

Search \+ Select

Optional

---

#### **Which other industries do you want to track?**

Multi-select

Optional

---

### **Startup Operator**

#### **What best describes your role?**

* Product  
* Growth  
* Marketing  
* Operations  
* Strategy  
* Data  
* Design  
* Engineering

---

#### **Which industry do you work in?**

Multi-select

---

#### **Which companies do you want to track?**

Search \+ Select

Optional

---

#### **Which other industries do you want to track?**

Multi-select

Optional

---

### **BD & Partnerships**

#### **Which industry do you work in?**

Multi-select

---

#### **Which companies do you want to track?**

Search \+ Select

Optional

---

#### **Which other industries do you want to track?**

Multi-select

Optional

---

### **Other**

#### **What best describes your role?**

Free text or predefined categories.

---

#### **Which companies do you want to track?**

Search \+ Select

Optional

---

#### **Which industries do you want to track?**

Multi-select

Optional

---

## **Step 6: Personalization Success Screen**

Headline:

Your Personalized Brief Is Ready

Subtext:

We'll prioritize stories based on your profile, industry and tracked companies.

CTA:

View My Personalized Brief

---

## **Returning User Flow**

Open App

↓

Personalized Brief Loads Directly

↓

User Completes Brief

↓

Streak Updated

↓

New Personalized Brief Generated Next Day

# Notifications

# **Notification Strategy PRD**

## **Inc42 Brief**

### **Objective**

Notifications exist to achieve two goals:

1. Ensure users consume the Daily Brief.  
2. Deliver time-sensitive alerts.

The Daily Brief is the primary habit-forming mechanism.

Alerts are a secondary real-time information layer.

The two systems operate independently.

---

# **Notification Architecture**

Notification System  
│  
├── Brief Notifications  
│  
└── Alert Notifications

---

# **PART 1: BRIEF NOTIFICATIONS**

## **Core Principle**

Success is not:

User opened notification.

Success is:

User completed today's Brief.

All Brief notifications are optimized toward Brief completion.

---

# **Brief State Machine**

User receives today's Brief.

Possible states:

STATE 1  
Brief Not Opened

↓

STATE 2  
Brief Opened But Not Completed

↓

STATE 3  
Brief Completed

↓

Stop All Brief Notifications

---

# **State Definitions**

## **Brief Opened**

User enters Brief.

At least one card viewed.

---

## **Brief Completed**

User has consumed the Brief.

Completion Criteria:

* Reaches final card

OR

* Opens 60%+ of cards

OR

* Spends predefined minimum reading time

Any condition marks Brief as completed.

---

# **Notification Flow**

## **Scenario A**

User does not open Brief.

### **Notification 1**

Time:  
Morning

Purpose:  
New Brief Available

Template:

Title:  
Your Brief is Ready

Body:  
Today's startup developments are waiting.

CTA:  
Read Brief

↓

No Open

↓

### **Notification 2**

Time:  
\+4 hours

Purpose:  
Reminder

Template:

Title:  
You Haven't Seen Today's Brief Yet

Body:  
The biggest startup developments today are still unread.

CTA:  
Open Brief

↓

No Open

↓

### **Notification 3**

Time:  
Evening

Purpose:  
Last Reminder

Template:

Title:  
Before Today's News Gets Old

Body:  
Catch up on today's startup developments in a few minutes.

CTA:  
Read Brief

↓

No Open

↓

Stop

Wait for next day's Brief.

---

# **Scenario B**

User Opens Brief But Does Not Complete

### **Notification 1**

Morning Brief

↓

User Opens

↓

User Leaves Before Completion

↓

### **Notification 2**

Time:  
3-4 hours later

Purpose:  
Resume Consumption

Template:

Title:  
Finish Today's Brief

Body:  
You're partway through today's startup developments.

CTA:  
Continue Reading

↓

If completed

Stop

↓

If not completed

No further Brief notifications.

Only one reminder.

---

# **Scenario C**

User Completes Brief

Morning Brief

↓

User Completes

↓

No More Brief Notifications

---

# **Brief Notification Logic**

Maximum Brief Notifications Per Day:

Not Opened:  
3

Opened But Incomplete:  
2

Completed:  
1

---

# **Notification Schedule**

07:30 AM  
Primary Brief Notification

11:30 AM  
Non-Open Reminder

06:00 PM  
Final Reminder

Incomplete Reminder:  
3-4 hours after abandonment

---

# **PART 2: WATCHLIST ALERTS**

## **Goal**

Notify users whenever a tracked company appears in a newly published article.

Alerts are driven entirely by the watchlist.

No watchlist match \= No alert.

---

# **Alert Flow**

User Tracks Company

↓

Inc42 Publishes Article

↓

Company Mentioned

↓

Push Notification Sent

↓

User Opens Article

OR

User Ignores Article

↓

No Reminder

No Follow-up

No Second Push

---

# **Alert Rules**

Every new article can generate one alert.

Each article generates only one notification.

No reminder notifications.

No completion reminders.

No recovery notifications.

---

# **Alert Templates**

Most notification systems make a mistake by putting the answer inside the notification.

If the notification already says:

> Meesho raises $275M at $4.9B valuation

the user has already consumed 80% of the information.

The notification should create enough context to establish relevance but not enough to satisfy curiosity.

For v1, I'd standardize around a single generic framework.

### **Generic Template**

Title:  
New Update On \[Company\]

Body:  
A new development involving \[Company\] has been reported.

CTA:  
Read Update

# **Notification Settings**

Users can control:

Daily Brief  
ON/OFF

Watchlist Alerts  
ON/OFF

Brief Delivery Time  
User Selectable

---

# **Notification Center**

Store:

* Brief Notifications  
* Watchlist Alerts

For 30 days.

Each item includes:

* Title  
* Timestamp  
* Read Status  
* Article Link

---

# **Analytics**

## **Brief Funnel**

Brief Sent

↓

Brief Opened

↓

Brief Completed

Track:

* Open Rate  
* Completion Rate  
* Reminder Recovery Rate

---

## **Alert Funnel**

Alert Sent

↓

Article Opened

Track:

* Alert Open Rate  
* CTR  
* Time To Open

---

# **Success Metrics**

Brief Open Rate

> 25%

Brief Completion Rate

> 40%

Reminder Recovery Rate

> 15%

Alert Open Rate

> 20%

Watchlist Alert CTR

> 15%

Notification Disable Rate  
\<15%

# Interpretation Layer Framework

# **Interpretation Layer Framework**

## **Assumption**

Available Inputs:

* Current article  
* Daily brief (\~11 articles)  
* User ICP (Founder, Investor)  
* User Industry  
* User Stage  
* Tracked companies  
* Tracked sectors

Unavailable Inputs:

* Historical article database  
* Long-term ecosystem trends  
* External market intelligence database

# **Architecture**

Raw Articles  
↓  
Article Classification  
↓  
Relevance Layer  
(Which articles should receive attention?)  
↓  
Emphasis Layer  
(What information should be emphasized?)  
↓  
L0 Summary  
(What happened?)  
↓  
Interpretation Layer  
L1 → Immediate Significance  
L2 → Ecosystem Connection  
L3 → Future Implications  
L4 → Suggested Actions

---

# **Layer 1: Relevance**

## **Question**

Which articles should receive more attention?

## **Inputs**

* Industry  
* Stage  
* Tracked Companies  
* Tracked Sectors

## **Output**

* Ordering

## **Example**

User:

Fintech Founder

Articles:

* RBI Lending Regulation  
* Healthtech Funding  
* Edtech Acquisition

Result:

RBI article ranks highest.

---

# **Layer 2: Emphasis**

## **Question**

Within an article, what information should be highlighted?

## **Inputs**

* ICP

## **Output**

* Lead sentence  
* Highlighted metrics  
* Highlighted entities  
* Information ordering

## **Example**

Article:

Startup raises $20M.  
Revenue grows 150%.  
Expansion planned.

Founder:

* Revenue growth  
* Expansion  
* Operating milestones

Investor:

* Round size  
* Investor participation  
* Capital raised

Important:

Facts do not change.

Only information hierarchy changes.

---

# **Layer Definitions**

## **L0 — What Happened?**

Question:  
What happened?

Personalization:  
❌ No

Example:

Article:  
Zepto filed its UDRHP and initiated the IPO process.

Output:  
Zepto filed its UDRHP and initiated the IPO process.

Confidence:  
100%

---

## **L1 — Immediate Significance** 

Question:  
What does this development mean right now? 

Personalization:  
✅ Yes

Source:  
Directly from article

Example:

Article:  
Meesho loss narrows 88%

Founder:  
Shows ability to improve unit economics while scaling.

Investor:  
Shows progress towards profitability and sustainable returns.

Confidence:  
High

---

## **L2 — Connecting The Dots**

Question:  
How does this relate to broader developments?

Personalization:  
✅ Yes

Source:  
Current article \+ supporting evidence

Example:

Article:  
Meta partners Reliance for data center

Founder:  
Growing infrastructure may improve access to AI compute.

Investor:  
Large players continue investing in Indian digital infrastructure.

Confidence:  
Medium

Condition:  
Only generate if article itself provides enough context

---

## **L3 — Future Implications**

Question:  
What could happen because of this?

Personalization:  
✅ Yes

Source:  
Inference

Example:

Article:  
New gaming regulation announced

Founder:  
Compliance costs may increase.

Investor:  
Portfolio companies may face margin pressure.

Confidence:  
Low-Medium

Condition:  
Only for policy/regulatory articles.

---

## **L4 — Suggested Actions**

Question:  
What should I do?

Personalization:  
✅ Completely

Source:  
Advice

Example:

Article:  
New gaming regulation announced

Founder:  
Review compliance requirements.

Investor:  
Assess exposure across gaming portfolio.

Confidence:  
Variable

Condition:  
Avoid in V1

L1 and L3 can sound similar.

The cleanest distinction is:

### **L1 \= Present Impact**

What does this development mean **right now**?

### **L3 \= Future Impact**

What could happen **because of this**?

---

# **Article Type Matrix**

| Article Type | L0 | L1 | L2 | L3 | L4 |
| ----- | ----- | ----- | ----- | ----- | ----- |
| Funding | ✅ | ✅ | ❌ | ❌ | ❌ |
| Product Launch | ✅ | ✅ | ❌ | ❌ | ❌ |
| Partnership | ✅ | ✅ | ❌ | ❌ | ❌ |
| Leadership Change | ✅ | ✅ | ❌ | ❌ | ❌ |
| Secondary Sale | ✅ | ✅ | ❌ | ❌ | ❌ |
| Financial Results | ✅ | ✅ | ❌ | ❌ | ❌ |
| Acquisition | ✅ | ✅ | ❌ | ❌ | ❌ |
| Layoffs | ✅ | ✅ | ❌ | ❌ | ❌ |
| IPO Filing | ✅ | ✅ | ❌ | ❌ | ❌ |
| Government Funding | ✅ | ✅ | ❌ | ❌ | ❌ |
| Policy Change | ✅ | ✅ | ✅ | ✅ | ❌ |
| Regulation | ✅ | ✅ | ✅ | ✅ | ❌ |
| Court Ruling | ✅ | ✅ | ✅ | ✅ | ❌ |
| Startup Crisis | ✅ | ✅ | ❌ | ❌ | ❌ |

---

# **ICP Behaviour**

## **Founder Lens**

Prioritize:

* Revenue growth  
* Expansion  
* Product launches  
* Hiring  
* Customer acquisition  
* GTM  
* Operations  
* Compliance impact

Example:

Funding Article

Generic:  
Company raised $20M.

Founder:  
Capital will be used for expansion and scaling operations.

---

## **Investor Lens**

Prioritize:

* Round size  
* Valuation  
* Investors involved  
* Exits  
* Liquidity  
* Market position  
* Capital efficiency

Example:

Funding Article

Generic:  
Company raised $20M.

Investor:  
The round reflects investor conviction and extends the company's growth runway.

---

# **Different ICP Output Example**

Article:  
Meesho narrows losses by 88%

L0:  
Meesho reduced losses by 88%.

Founder L1:  
Demonstrates improved operating efficiency while maintaining scale.

Investor L1:  
Signals movement towards profitability and improved financial health.

---

Article:  
Zepto files UDRHP

L0:  
Zepto initiated IPO filing.

Founder L1:  
Highlights the operational maturity required for public markets.

Investor L1:  
Creates a potential liquidity event and public market benchmark.

---

Article:  
Gaming Regulation Introduced

L0:  
Government introduced new gaming regulation.

Founder L1:  
Companies will need to comply with updated requirements.

Investor L1:  
Regulatory changes may affect portfolio company operations.

Founder L3:  
Compliance costs may increase.

Investor L3:  
Sector risk profile may change.

---

# **Rules**

## **L0**

Never personalized.

Never infer.

Never predict.

---

## **L1**

Primary interpretation layer.

Allowed for all articles.

Can be personalized by ICP.

Must be derivable from article.

---

## **L2**

Only generate when:

* Policy article  
* Regulation article  
* Court ruling

Otherwise suppress.

---

## **L3**

Only generate when causality is obvious.

Mostly:

* Policy  
* Regulation  
* Court rulings

Suppress for:

* Funding  
* Product launches  
* Partnerships

---

## **L4**

Do not generate in V1.

Requires explicit recommendation engine.

# **Direct Causal Chain Test**

Before generating L2, L3 or L4 ask:

"If I had access only to this article, would a reasonable person arrive at this conclusion?"

If YES:

Generate.

If NO:

Suppress.

---

## **Strong Direct Causal Chain**

Policy Changes

Regulations

Court Rulings

---

## **Weak Direct Causal Chain**

Acquisitions

Layoffs

IPO Filings

Financial Results

Leadership Changes

Funding

Product Launches

Partnerships

Feature Launches

Marketing Campaigns

Awards

Reason:

The article itself does not provide enough evidence to infer future outcomes.

---

## **Founder v/s Investor**

| Founder | Investor |
| ----- | ----- |
| Building a company | Allocating capital |
| Inside the business | Outside the business |
| Wants execution insights | Wants assessment insights |
| Controls operations | Controls investment decisions |
| Asks "What can I learn?" | Asks "How should I evaluate?" |

This distinction should drive the entire emphasis and interpretation framework.

---

# **Funding Article**

### **Article**

Rivvun AI raises $7.5M

### **Weak Founder Version**

The company raised capital.

### **Better Founder Version**

The company secured capital to expand product development and enterprise adoption.

Why valuable?

Founder learns:

* Where money is going  
* What growth lever is being funded

---

### **Weak Investor Version**

The company raised capital.

### **Better Investor Version**

The round signals investor conviction in the company's approach to enterprise revenue optimization.

Why valuable?

Investor learns:

* Why investors participated  
* What investment thesis exists

---

# **Financial Results**

### **Article**

Meesho loss narrows 88%

### **Founder**

Focus:

* Efficiency  
* Revenue  
* Cost control  
* Execution

Output:

Meesho significantly improved operating efficiency while maintaining scale.

Question founder is asking:

"How did they execute?"

---

### **Investor**

Focus:

* Profitability  
* Return profile  
* IPO readiness

Output:

Meesho moved materially closer to profitability.

Question investor is asking:

"Does this improve investment quality?"

---

# **Acquisition**

### **Article**

Incuspaze acquires iKeva

### **Founder**

Focus:

* Expansion strategy  
* Market entry  
* Capability acquisition

Output:

The acquisition accelerates Incuspaze's footprint expansion.

Question:

"What strategic advantage did they gain?"

---

### **Investor**

Focus:

* Consolidation  
* Market position  
* Competitive moat

Output:

The acquisition strengthens Incuspaze's position in the coworking market.

Question:

"Does this strengthen market leadership?"

---

# **IPO Filing**

### **Article**

Zepto files UDRHP

### **Founder**

Focus:

* Operational maturity  
* Governance  
* Scaling journey

Output:

The filing reflects the operational and governance maturity required for public markets.

Question:

"What did the company achieve to get here?"

---

### **Investor**

Focus:

* Liquidity  
* Valuation  
* Market appetite

Output:

The filing moves the company closer to a potential liquidity event.

Question:

"How does this affect returns?"

---

# **Policy Article**

### **Article**

Government introduces AI regulation

### **Founder**

Focus:

* Compliance  
* Product impact  
* Operational changes

Output:

AI startups will need to incorporate additional compliance processes.

Question:

"What changes inside my company?"

---

### **Investor**

Focus:

* Risk  
* Sector attractiveness  
* Portfolio impact

Output:

The regulation introduces new considerations for evaluating AI businesses.

Question:

"How does this affect investment risk?"

# 

---

# **A Simple Test**

For every article ask:

### **Founder**

"What can I learn from this company's actions?"

### **Investor**

"What does this tell me about the quality of this company, market, or investment opportunity?"

# **Master Prompt**

# **Startup Intelligence Personalization Framework**

## **Objective**

Generate personalized startup intelligence while maintaining factual consistency across users.

Facts, numbers, entities, and events must remain identical for all users.

Only the following may change:

* Article ranking  
* Information emphasis  
* Information ordering  
* Summary framing  
* Interpretation framing

Never change the underlying facts.

---

# **Architecture**

Raw Article  
↓  
Article Classification  
(Funding, IPO, Policy, Acquisition, Financial Results, Regulation, etc.)  
↓  
Relevance Layer  
(Which articles deserve attention?)  
↓  
Emphasis Layer  
(What information should be highlighted?)  
↓  
L0 Summary  
(What happened?)  
↓  
Interpretation Layer  
L1 → Immediate Significance  
L2 → Ecosystem Connection  
L3 → Future Implications  
L4 → Suggested Actions

---

# **Layer 1: Relevance**

## **Purpose**

Determine which articles receive more attention.

## **Inputs**

* Industry  
* Stage  
* Tracked Companies  
* Tracked Sectors

## **Outputs**

* Ranking  
* Ordering  
* Priority

## **Rules**

Industry and stage determine which articles get surfaced and which get buried.

Tracked companies increase article priority.

This is article-level personalization.

No content modification occurs here.

---

# **Layer 2: Emphasis**

## **Purpose**

Determine what information receives prominence within an article.

## **Inputs**

* ICP  
* Article Type

## **Outputs**

* Lead sentence  
* Highlighted metrics  
* Highlighted entities  
* Information ordering

## **Rules**

Facts remain unchanged.

Only information hierarchy changes.

This is information-level personalization.

---

# **Founder Lens**

Treat every article as a case study in company building.

Focus on:

* Execution  
* Product  
* Growth  
* Operations  
* Expansion  
* Distribution  
* Hiring  
* Strategy  
* Compliance

Prioritize:

* Company actions over investor actions  
* Decisions over outcomes  
* Operating details over financial details

Core Question:

"What can another founder learn from how this company is being built, operated, or scaled?"

---

# **Investor Lens**

Treat every article as a signal for evaluating companies, markets, and investment opportunities.

Focus on:

* Capital flows  
* Market position  
* Competitive strength  
* Risk  
* Returns  
* Liquidity  
* Sector attractiveness  
* Valuation signals

Prioritize:

* Investor actions over company actions  
* Outcomes over decisions  
* Financial significance over operating details

Core Question:

"What does this development reveal about the attractiveness, risk, or quality of this investment opportunity?"

---

# **Interpretation Layer**

Assume:

* Current article available  
* Daily brief (\~11 articles)  
* No historical article access  
* No external ecosystem database

---

# **L0 — What Happened?**

## **Purpose**

Describe the event.

## **Rules**

* Purely factual  
* No personalization  
* No inference

Question:

"What happened?"

---

# **L1 — Immediate Significance**

## **Purpose**

Explain what changed today because of the event.

## **Rules**

* Directly supported by article  
* High confidence  
* Personalization allowed

Question:

"What does this development mean right now?"

---

# **L2 — Ecosystem Connection**

## **Purpose**

Connect the event to broader developments.

## **Rules**

Generate only when:

* Article itself contains supporting context

  Question:

"How does this relate to broader developments?"

---

# **L3 — Future Implications**

## **Purpose**

Describe what could happen because of the event.

## **Rules**

Generate only when a direct causal chain exists.

Question:

"What could happen because of this?"

---

# **L4 — Suggested Actions**

## **Purpose**

Recommend actions.

## **Rules**

Generate only when explicitly enabled.

Question:

"What should the user do?"

---

# **Direct Causal Chain Test**

Before generating L2, L3, or L4 ask:

"If I had access only to this article, would a reasonable person arrive at this conclusion?"

If yes:

Generate.

If no:

Suppress.

---

# **Strong Direct Causal Chain**

Suitable for L2 and L3:

* Policy Changes  
* Regulations  
* Court Rulings  
* Tax Changes  
* Government Mandates  
* Government Funding Programs  
* Licensing Changes  
* Import/Export Restrictions  
* Data Protection Rules

Reason:

The event itself changes the operating environment.

---

# **Medium Direct Causal Chain**

Use cautiously:

* Acquisitions  
* Layoffs  
* IPO Filings  
* Financial Results  
* Leadership Changes  
* Startup Crises

---

# **Weak Direct Causal Chain**

Avoid L2 and L3:

* Funding  
* Product Launches  
* Partnerships  
* Feature Releases  
* Marketing Campaigns  
* Awards

Reason:

The article alone does not provide enough evidence for broader conclusions.

# **Interpretation Eligibility Matrix**

Legend:

✅ \= Recommended

⚠️ \= Generate only when strong supporting evidence exists

❌ \= Suppress

| Article TypeL0L1L2L3L4 |  |  |  |  |  |
| ----- | ----- | ----- | ----- | ----- | ----- |
| Funding | ✅ | ✅ | ❌ | ❌ | ❌ |
| Product Launch | ✅ | ✅ | ❌ | ❌ | ❌ |
| Partnership | ✅ | ✅ | ❌ | ❌ | ❌ |
| Leadership Change | ✅ | ✅ | ❌ | ❌ | ❌ |
| Secondary Sale | ✅ | ✅ | ❌ | ❌ | ❌ |
| Financial Results | ✅ | ✅ | ⚠️ | ❌ | ❌ |
| Acquisition | ✅ | ✅ | ⚠️ | ❌ | ❌ |
| Layoffs | ✅ | ✅ | ⚠️ | ❌ | ❌ |
| IPO Filing | ✅ | ✅ | ⚠️ | ❌ | ❌ |
| Government Funding | ✅ | ✅ | ⚠️ | ⚠️ | ❌ |
| Policy Change | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| Regulation | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| Court Ruling | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| Startup Crisis | ✅ | ✅ | ⚠️ | ⚠️ | ❌ |

## **Article Type Rules**

### **Funding**

Allowed:

* L0  
* L1

Do Not Generate:

* L2  
* L3  
* L4

Reason:  
A funding event only proves that capital was raised. It does not prove broader market trends, investor sentiment, or future outcomes.

---

### **Product Launch**

Allowed:

* L0  
* L1

Do Not Generate:

* L2  
* L3  
* L4

Reason:  
The article confirms a product launch, not market adoption or future impact.

---

### **Partnership**

Allowed:

* L0  
* L1

Do Not Generate:

* L2  
* L3  
* L4

Reason:  
The existence of a partnership does not provide sufficient evidence for ecosystem-level conclusions.

---

### **Leadership Change**

Allowed:

* L0  
* L1

Do Not Generate:

* L2  
* L3  
* L4

Reason:  
The appointment itself is factual. Future business impact is speculative.

---

### **Secondary Sale**

Allowed:

* L0  
* L1

Do Not Generate:

* L2  
* L3  
* L4

Reason:  
A secondary transaction provides liquidity but does not establish broader market sentiment.

---

### **Financial Results**

Allowed:

* L0  
* L1

Use Caution:

* L2

Do Not Generate:

* L3  
* L4

Reason:  
Results may support broader observations only if explicitly referenced in the article.

---

### **Acquisition**

Allowed:

* L0  
* L1

Use Caution:

* L2

Do Not Generate:

* L3  
* L4

Reason:  
Some consolidation observations may be valid, but future market effects are uncertain.

---

### **Layoffs**

Allowed:

* L0  
* L1

Use Caution:

* L2

Do Not Generate:

* L3  
* L4

Reason:  
The article may indicate operational restructuring but cannot reliably predict future outcomes.

---

### **IPO Filing**

Allowed:

* L0  
* L1

Use Caution:

* L2

Do Not Generate:

* L3  
* L4

Reason:  
An IPO filing starts a process but does not indicate listing success or market reception.

---

### **Government Funding**

Allowed:

* L0  
* L1

Use Caution:

* L2  
* L3

Reason:  
Government intervention creates a causal chain but long-term ecosystem impact remains uncertain.

---

### **Policy Change**

Allowed:

* L0  
* L1  
* L2  
* L3

Use Caution:

* L4

Reason:  
Policy changes directly alter the operating environment and naturally create downstream effects.

---

### **Regulation**

Allowed:

* L0  
* L1  
* L2  
* L3

Use Caution:

* L4

Reason:  
Regulations create direct obligations and direct business consequences.

---

### **Court Ruling**

Allowed:

* L0  
* L1  
* L2  
* L3

Use Caution:

* L4

Reason:  
Court rulings often establish enforceable outcomes with clear downstream implications.

---

### **Startup Crisis**

Allowed:

* L0  
* L1

Use Caution:

* L2  
* L3

Do Not Generate:

* L4

Reason:  
Business distress may create visible consequences but future outcomes remain uncertain.

---

# **Interpretation Guardrails**

Never:

* Invent trends  
* Invent investor sentiment  
* Invent market shifts  
* Invent future outcomes  
* Generalize from a single event

When uncertain:

Suppress.

Prefer omission over speculation.

# Rough

1. **Funding & Investments** (Startup Funding & Investments, Fund Launches) \~23 articles  
2. **Company Performance & Business Updates** (Business Updates, Startup Financials, Industry Trends) \~16 articles  
3. **Corporate Actions** (Startup IPO, Startup Mergers & Acquisitions, Startup Layoffs, People & Culture, Controversies) \~15 articles  
4. **Regulation & Policy** (Government & Policies) \~3 articles

# v0\_Brief Personalization

## **Scoring & Ordering Logic — Brief Personalization**

**Context:** \~11 articles/day, all shown. Two scores total — Combined Score and Watchlist+Sector Score. Combined Score is used in **both** Step 1 and Step 2\.

---

### **Scores**

**1\. Combined Score** (used in Step 1 AND Step 2\)  
 `Combined Score = Signal Score + Watchlist(0 or 2) + Sector(0 or 2)` → range 1–10

**2\. Watchlist+Sector Score** (used in Step 3 only)  
 `watchlistHit(0 or 2) + sectorMatch(0 or 2)` → range 0–4

---

### **Signal Score table (per ICP) — base component of Combined Score**

| Signal Type | Founder | Operator | Investor | BD |
| ----- | ----- | ----- | ----- | ----- |
| Funding & Investment | 6 | 4 | 6 | 6 |
| Sector & Trend | 4 | 6 | 4 | 3 |
| Competitive & Intelligence | 3 | 6 | 3 | 5 |
| M\&A & Strategic | 2 | 1 | 5 | 2 |
| Org & Team | 5 | 3 | 2 | 4 |
| Regulatory | 1 | 2 | 1 | 1 |

---

Mapping each tag to the PRD's signal-type taxonomy (Funding & Investment, Competitive & Intelligence, M\&A & Strategic, Org & Team, Sector & Trend, Regulatory):

**Funding & Investment**

* Startup Funding & Investments  
* Fund Launches

**M\&A & Strategic**

* Startup Mergers & Acquisitions  
* Startup IPO

**Org & Team**

* People & Culture  
* Startup Layoffs

**Sector & Trend**

* Industry Trends  
* Cohort Launches  
* Startup Discovery  
* Controversies

**Competitive & Intelligence**

* Business Updates  
* Business Models & Strategy  
* Startup Financials

**Regulatory**

* Government & Policies

---

### **Step 1 — Inclusion check (NOT a 6–8 selection)**

1. Compute **Combined Score** for all \~11 candidates.  
2. **Default: include all \~11.**  
3. Watchlist guarantee: never drop a `watchlistHit = true` card.

**Output:** essentially all \~11 cards. Combined Score carries forward to Step 2\.

---

### **Step 2 — Section ordering (which section comes first, second, ...)**

Sections are ordered by **max Combined Score of the cards in that section** — not by raw Signal Score alone.

1. Group cards by `signalType`.  
2. For each section, compute a representative Combined Score (use the **highest** Combined Score among cards in that section — i.e., the section's "best card" pulls it up).  
3. Order sections by this representative score, descending.

**Practical effect:** a section that's normally low-priority for an ICP (e.g. Regulatory for a Founder, Signal Score \= 1\) can jump up the order if it contains a watchlist-hit card (+2) — e.g. representative score \= 1+2 \= 3, which could outrank a section like M\&A (Signal Score 2, no boosts \= 2).

**Output:** ordered list of non-empty sections, now influenced by watchlist/sector hits.

---

### **Step 3 — Within-section ordering (order of cards inside each section)**

1. Inside each section, sort cards by **Watchlist+Sector Score** (0–4), descending.  
2. Tie → recency, newer first.

**Output:** final order \= sections in Step 2 order, cards within each section in Step 3 order.

---

### **Worked example (Founder)**

| Card | Signal Type | Watchlist | Sector Match | Combined Score |
| ----- | ----- | ----- | ----- | ----- |
| A | Funding & Investment | No | No | 6 |
| B | Funding & Investment | No | No | 6 |
| C | Regulatory | Yes | No | 1+2 \= 3 |
| D | M\&A & Strategic | No | No | 2 |
| E | Org & Team | No | No | 5 |

**Step 2 — Section representative scores (max Combined Score per section):**

* Funding & Investment: max(6, 6\) \= 6  
* Org & Team: 5  
* Regulatory: 3 (boosted by watchlist hit on Card C)  
* M\&A & Strategic: 2

**Section order:** Funding & Investment → Org & Team → **Regulatory** → M\&A & Strategic

(Regulatory jumped above M\&A purely because Card C's watchlist hit pulled its Combined Score above M\&A's.)

**Step 3 — Within Funding & Investment** (A and B both WL+Sector \= 0): tie → recency decides A vs B order.

**Final order:** \[A, B\] → E → C → D

---

### **Summary table**

| Step | Score used | Decides |
| ----- | ----- | ----- |
| 1\. Inclusion check | Combined Score | Whether anything *ever* needs dropping (rare); watchlist cards never dropped |
| 2\. Section order | Combined Score (best card per section) | Order of sections — watchlist/sector hits can pull a section up |
| 3\. Within-section order | Watchlist+Sector Score only | Order of cards inside a section |

---

# Conversation History Arch

# **Product Requirements Document (PRD): Conversation History Fix**

---

# **1\. Executive Summary**

The Ask Datalabs Streaming Agent currently fails to handle follow-up queries (e.g., *"yeah"*, *"what about their revenue?"*) gracefully.

This is driven by two distinct bugs.

## **1.1 Core Architectural Bug (Sequencing)**

The backend's Query Analyzer classifies the user's intent **before** loading the conversation history.

Because the Analyzer is blind to the context, it flags perfectly valid follow-up queries as `out_of_scope` or `fast`. This disables background tasks such as Charts and Discovery Search, degrading the user experience.

---

## **1.2 Local Developer UI Bug (Statelessness)**

The local testing interface (`index.html`) does not generate or pass a `session_id`.

As a result, the backend treats every request as a brand-new conversation. Without history, the LLM interprets follow-up messages like *"yeah"* as unrelated input and returns the fallback response:

> "I specialize in Indian startup intelligence..."

---

# **2\. Root Cause Analysis**

## **A. Sequencing Bug (Backend)**

### **Current Execution Order (`server.py`)**

1. **Node 7 – `analyze_query`**  
   * GPT-4.1-nano classifies the query.  
   * Determines `query_type`.  
   * Extracts `entities`.  
   * Only receives the raw query (e.g., *"what about their revenue?"*).  
   * Because conversation history is unavailable, pronouns such as *"their"* cannot be resolved, resulting in `out_of_scope`.  
2. **Node 9 – Discovery / Charts**  
   * Since the query has already been classified as `out_of_scope`, these background tasks are skipped.  
3. **Node 10 – `read_session`**  
   * Conversation history is finally loaded from the session store or frontend payload.  
4. **Node 11 – `run_agent_stream`**  
   * The LLM agent executes.

   ### **Impact on Real Users (Mobile / n8n)**

Production clients already send conversation history.

As a result:

* The LLM successfully answers the follow-up question (e.g., *"Zepto's revenue is ₹X..."*).  
* However, because the Analyzer failed earlier in the pipeline, the UI never receives the supporting rich data.

Missing UI elements include:

* Charts  
* Entity Links  
* Discovery Search  
  ---

  ## **B. Statelessness Bug (Frontend `index.html`)**

The local developer interface does not implement session management.

### **Current Flow**

1. User asks:  
   "Tell me about Zepto"  
2. The server responds.  
3. The frontend does **not** save a `session_id`.  
4. User asks:  
   "yeah"  
5. The frontend sends this as a completely new request.  
6. The LLM receives **only** the word:  
   "yeah"  
7. Following Prompt Rule 132 (*"Do NOT answer queries outside the Indian startup domain"*), the LLM rejects the prompt and returns the fallback response.  
   ---

   # **3\. Proposed Solution**

Implement a two-part fix addressing both the backend sequencing issue and the local testing interface.

---

## **Fix 1: Reorder the Backend Pipeline**

Load conversation history **before** classification so the Analyzer can resolve pronouns and references.

### **Required Changes**

#### **1\. Move `read_session` (`server.py`)**

Move the session read step so it executes **before** `analyze_query()`.

---

#### **2\. Update `analyze_query` (`analyzer.py`)**

Add a new `history` parameter to the function signature.

---

#### **3\. Inject History into the Analyzer Prompt**

Modify the GPT-4.1-nano message array to include the last three conversation turns (User/Assistant pairs) immediately before the current query.

---

#### **4\. Prompt Tuning**

Extend `ANALYZER_PROMPT` with an explicit instruction:

> "If the user uses pronouns (e.g., 'their', 'it'), resolve them using the conversation history."

---

## **Fix 2: Stateful Local UI**

Enable local developers to test multi-turn conversations.

### **Required Changes**

#### **1\. Generate `session_id`**

Generate a UUID when `index.html` loads.

---

#### **2\. Include Session in Every Request**

Append the following field to every `/query/stream` POST request.

* {  
*   "session\_id": "\<uuid\>"  
* }  
    
  ---

  # **4\. Success Criteria**

  ### **1\. Feature Restoration**

Follow-up queries such as:

> "what about their revenue?"

correctly trigger:

* Chart generation  
* Discovery Search

allowing rich UI components to load for the resolved entity.

---

### **2\. Analyzer Accuracy**

The Analyzer correctly resolves entities from pronoun-heavy follow-up queries.

Example:

* "their"  
*         ↓  
* \["zepto"\]  
    
  ---

# Feature Flags

# Events

# **Inc42 App Analytics PRD (v1)**

## **Purpose**

The analytics framework exists to answer four core business questions:

### **1\. Habit Formation**

Are users building a daily Brief consumption habit?

### **2\. Personalization**

Does Watchlist-driven personalization improve engagement and retention?

### **3\. Intelligence Discovery**

Are users moving beyond headlines into deeper startup intelligence?

### **4\. Retention**

Which behaviors predict long-term retention and product success?

The analytics system should prioritize meaningful user actions over UI interactions.

---

# **Section 1: Onboarding**

## **Event: onboarding\_started**

### **Trigger**

User enters onboarding.

### **Properties**

| Property |
| ----- |
| source |
| app\_version |

### **Why**

Starting point for all onboarding funnels.

### **Questions Answered**

* How many users enter onboarding?  
* How many complete onboarding?

### **Metrics**

**Onboarding Start Rate**

onboarding\_started / installs  
---

## **Event: onboarding\_step\_viewed**

### **Properties**

| Property |
| :---- |
| step\_name |

Values:

* welcome  
* role  
* sectors  
* watchlist  
* success

### **Why**

Measures progression and drop-offs.

### **Questions Answered**

* Which screen loses users?  
* Are users reaching Watchlist setup?

### **Metrics**

**Step Reach Rate**

step\_viewed / onboarding\_started  
---

## **Event: onboarding\_step\_completed**

### **Properties**

| Property |
| :---- |
| step\_name |

### **Why**

Measures successful progression.

### **Questions Answered**

* Which onboarding step creates friction?

### **Metrics**

**Step Completion Rate**

step\_completed / step\_viewed  
---

## **Event: onboarding\_step\_skipped**

### **Properties**

| Property |
| :---- |
| step\_name |

### **Why**

Critical because onboarding is skippable.

### **Questions Answered**

* What information are users unwilling to provide?  
* Is Watchlist perceived as too much effort?

### **Metrics**

**Skip Rate**

step\_skipped / step\_viewed  
---

## **Event: onboarding\_role\_selected**

### **Properties**

| Property |
| :---- |
| role |

### **Why**

Defines ICP.

### **Questions Answered**

* Which ICPs are most common?  
* Which ICPs retain best?

---

## **Event: onboarding\_sectors\_selected**

### **Properties**

| Property |
| :---- |
| sector\_count |
| selected\_sectors |

### **Why**

Measures personalization depth.

### **Questions Answered**

* Which sectors are most popular?  
* Does more personalization improve engagement?

---

## **Event: onboarding\_watchlist\_entity\_added**

### **Properties**

| Property |
| :---- |
| entity\_type |
| entity\_id |
| entity\_name |
| position |

### **Why**

Measures recommendation effectiveness.

### **Questions Answered**

* Which suggested entities perform best?  
* Which entities drive engagement?

---

## **Event: onboarding\_completed**

### **Properties**

| Property |
| :---- |
| role\_selected |
| sector\_count |
| watchlist\_count |
| completion\_time\_seconds |

### **Why**

Measures onboarding quality.

### **Questions Answered**

* Does onboarding quality predict retention?

### **Metrics**

**Onboarding Completion Rate**

onboarding\_completed / onboarding\_started  
---

# **Section 2: Brief**

## **Event: brief\_loaded**

### **Properties**

| Property |
| :---- |
| brief\_date |
| card\_count |
| watchlist\_card\_count |
| editorial\_card\_count |
| signal\_card\_count |

### **Why**

Starting point of the daily habit.

### **Questions Answered**

* How many users access the Brief?  
* Does personalization impact engagement?

### **Metrics**

**Brief Open Rate**

brief\_loaded / DAU  
---

## **Event: brief\_card\_viewed**

### **Properties**

| Property |
| :---- |
| card\_id article\_id |
| card\_position |
| card\_type |
| sector |
| is\_watchlist\_hit |
| relevance\_reason |

### **Why**

Measures exposure.

### **Questions Answered**

* Which positions get viewed?  
* Are users reaching the end?

### **Metrics**

**Card Reach Rate**

card\_viewed / brief\_loaded  
---

## **Event: brief\_card\_expanded**

### **Properties**

| Property article\_id |
| :---- |
| card\_id |
| card\_position |
| card\_type |
| is\_watchlist\_hit |

### **Why**

Represents active interest.

### **Questions Answered**

* Which stories generate curiosity?  
* Do watchlist stories outperform editorial stories?

### **Metrics**

**Expansion Rate**

card\_expanded / card\_viewed  
---

## **Event: brief\_article\_opened**

### **Properties**

| Property |
| :---- |
| article\_id |
| card\_id |
| card\_position |
| card\_type |
| is\_watchlist\_hit |

### **Why**

Measures transition from summary to deep reading.

### **Questions Answered**

* Which Brief stories drive reading?  
* What content types create depth?

### **Metrics**

**Brief Article CTR**

article\_opened / card\_viewed  
---

## **Event: brief\_story\_saved**

### **Properties**

| Property |
| :---- |
| article\_id |
| card\_type |

### **Why**

Strong value signal.

### **Questions Answered**

* Which content is worth revisiting?

---

## **Event: brief\_session\_ended**

### **Properties**

| Property |
| :---- |
|  |
| cards\_viewed |
| cards\_expanded |
| session\_duration\_seconds |

### **Why**

Primary product success metric.

### **Questions Answered**

* Are users completing the habit?  
* Does completion predict retention?

### **Metrics**

**Brief Completion Rate**

brief\_session\_ended / brief\_loaded  
---

# **Section 3: Articles**

## **Event: article\_opened**

### **Properties**

| Property |
| :---- |
| article\_id |
| article\_type |
| source |
| tags |

Sources:

* brief  
* explore  
* search  
* profile  
* notification

### **Why**

Measures content consumption.

### **Questions Answered**

* Which surfaces drive reading?

---

## **Event: article\_completed**

### **Properties**

| Property |
| :---- |
| article\_id |
| read\_time |
| source |

### **Why**

Measures actual consumption.

### **Questions Answered**

* Are users reading or merely opening?

### **Metrics**

**Article Completion Rate**

article\_completed / article\_opened  
---

## **Event: article\_saved**

### **Properties**

| Property |
| :---- |
| article\_id |
| source |

### **Why**

Measures perceived value.

---

## **Event: article\_shared**

### **Properties**

| Property |
| :---- |
| article\_id |
| destination |

### **Why**

Measures advocacy and distribution.

---

# **Section 4: Search**

## **Event: search\_executed**

### **Properties**

| Property |
| :---- |
| query\_length query |
| result\_count |

### **Why**

Strong indicator of intent.

### **Questions Answered**

* How often do users actively seek intelligence?

### **Metrics**

**Search Usage Rate**

users\_who\_searched / DAU  
---

## **Event: search\_result\_clicked**

### **Properties**

| Property |
| :---- |
| result\_type |
| result\_position |

Values:

* company  
* article  
* sector

### **Why**

Measures search quality.

### **Questions Answered**

* Are users finding useful results?

### **Metrics**

**Search Success Rate**

search\_result\_clicked / search\_executed  
---

# **Section 5: Company Profiles**

## **Event: company\_profile\_viewed**

### **Properties**

| Property |
| :---- |
| company\_id |
| sector |
| stage |
| source |

### **Why**

Measures movement into startup intelligence.

### **Questions Answered**

* Is journalism driving Datalabs exploration?

### **Metrics**

**Profile Views / DAU**

company\_profile\_viewed / DAU  
---

## **Event: company\_tracked**

### **Properties**

| Property |
| :---- |
| company\_id |
| source |

### **Why**

Represents personalization adoption.

### **Questions Answered**

* Which surfaces create follows?

### **Metrics**

**Follow Conversion Rate**

company\_followed / profile\_viewed  
---

## **Event: company\_related\_article\_clicked**

### **Why**

Measures bridge between data and journalism.

### **Questions Answered**

* Are profiles generating content consumption?

---

# **Section 6: Watchlist**

## **Event: watchlist\_entity\_added**

### **Properties**

| Property |
| :---- |
| entity\_type |
| entity\_id |
| source |

### **Why**

Core personalization event.

### **Questions Answered**

* What drives Watchlist adoption?

### **Metrics**

**Watchlist Adoption Rate**

users\_with\_watchlist / DAU  
---

## **Event: watchlist\_entity\_removed**

### **Why**

Measures personalization churn.

### **Questions Answered**

* What entities are being abandoned?

---

## **Event: watchlist\_opened**

### **Why**

Measures engagement with personalization layer.

### **Questions Answered**

* Are users revisiting tracked entities?

---

## **Event: watchlist\_alert\_opened**

### **Properties**

| Property |
| :---- |
| alert\_type |

### **Why**

Measures effectiveness of alert system.

### **Metrics**

**Alert Open Rate**

alert\_opened / alerts\_sent  
---

# **Section 7: Notifications**

## **Event: push\_received**

### **Properties**

| Property |
| :---- |
| notification\_type |

Types:

* morning\_brief  
* watchlist\_alert  
* breaking\_news  
* completion\_nudge  
* winback

---

## **Event: push\_opened**

### **Properties**

| Property |
| :---- |
| notification\_type |

### **Why**

Measures notification effectiveness.

### **Questions Answered**

* Which notification types drive engagement?

### **Metrics**

**Push CTR**

push\_opened / push\_received  
---

# **Section 8: Core Business Metrics Dashboard**

## **Habit Metrics**

* DAU  
* WAU  
* MAU  
* Brief Open Rate  
* Brief Completion Rate  
* Article Completion Rate

---

## **Personalization Metrics**

* Watchlist Adoption Rate  
* Average Watchlist Size  
* Average Sector Count  
* Follow Conversion Rate

---

## **Intelligence Metrics**

* Search Usage Rate  
* Company Profile Views / DAU  
* Profile → Follow Conversion  
* Search Success Rate

---

## **Retention Metrics**

* D1 Retention  
* D7 Retention  
* D30 Retention

Segmented by:

* Role  
* Sector Count  
* Watchlist Size  
* Brief Completion Frequency

---

# **Key Product Hypotheses To Validate**

### **H1**

Users with larger watchlists have higher Brief completion rates.

### **H2**

Watchlist-hit stories outperform editorial-only stories.

Measured through:

* Expansion Rate  
* Article CTR  
* Completion Rate

### **H3**

Brief completion predicts retention.

Compare:

* Users completing 0–1 Briefs/week  
* Users completing 2–3 Briefs/week  
* Users completing 4–5 Briefs/week

Against:

* D7 Retention  
* D30 Retention

### **H4**

Search users retain better than non-search users.

### **H5**

Company profile exploration increases likelihood of following companies and returning to the app.

### **H6**

Higher onboarding personalization leads to stronger long-term engagement and retention.

# Privacy Policy

# **Inc42 App — Privacy Policy**

## **1\. Introduction**

Ideope Media Private Limited ("Ideope") is a technology service provider that carries out marketing, educational, and non-news content development activities. Ideope has granted an exclusive licence to Inc42 Plus Media Private Limited ("Inc42" or "Company") to operate the Inc42 mobile application for iOS and Android (the "App"). Through the App, Inc42 provides access to digital news and media content and to company and sector information, and Ideope and Inc42 (collectively, the "Inc42 Group" or "we" or "us" or "our") provide the features and functionality made available in the App (the "Services").

This Privacy Policy explains how we collect, use, disclose, store, and protect your information in connection with the App, in compliance with the Digital Personal Data Protection Act, 2023 ("DPDP Act"), the Information Technology Act, 2000 ("IT Act"), and other applicable data protection laws.

This Privacy Policy forms part of, and must be read together with, the Terms of Use for the App. By downloading, installing, or using the App, you acknowledge the practices described in this Privacy Policy. This Privacy Policy is specific to the App; your use of the Inc42 website and other Inc42 services is governed by the privacy policy applicable to those services.

## **2\. Applicability**

This Privacy Policy applies to two categories of individuals:

**2.1 App Users.** Individuals who download, browse, register for, or use the App, whether or not they create an account.

**2.2 Listed Individuals.** Business professionals whose professional information appears within the company and sector information in the App. In the App, this information is limited to **name and designation** (for example, a company's founders or key executives), sourced from publicly available records, regulatory filings, and the Inc42 Group's market intelligence data. The App does not display business contact information (such as work email, phone number, or LinkedIn profile) for these individuals. The processing of Listed Individuals' data is governed by the Contact Data Policy in addition to this Privacy Policy.

## **3\. What Information We Collect**

**3.1 Information You Provide (App Users)**

When you register or interact with the App, we may collect:

| Category | Examples |
| ----- | ----- |
| Identity Data | Name, email address, and (where provided by your sign-in method) profile information |
| Account Data | Account identifier, password or authentication token, account preferences |
| Preference Data | Professional role, sectors, and topics you select during onboarding or in settings |
| Activity Data | Articles you save, companies and sectors you track, your reading of the daily Brief, and your streaks, reader levels, and badges |
| Communication Data | Correspondence with our support team, feedback, and survey responses |

The App does not collect payment information (there are no paid subscriptions in the App), and it does not provide functionality for you to post comments or publicly submit user content.

**3.2 Information Collected Automatically**

When you use the App, including while you browse without an account, we automatically collect:

| Category | Examples |
| ----- | ----- |
| Device Information | Device type and model, operating system and version, app version, device settings, and language |
| Device Identifiers | A device-level identifier generated by the App on first open, and, where permitted, advertising identifiers (such as Apple's IDFA or the Android Advertising ID) used for measurement and attribution |
| Network Information | IP address, internet service provider, and connection information |
| Usage Information | Screens viewed, content accessed, search queries, features used, notifications interacted with, and time and duration of use |
| Approximate Location | Coarse geographic location derived from your IP address (the App does not collect precise device GPS location, and does not request location permission) |
| Referral / Attribution Information | The campaign, link, or source through which you installed or opened the App |

On Apple devices, collection of certain identifiers used for cross-app tracking is subject to Apple's App Tracking Transparency (ATT) prompt (see Section 6).

**3.3 Information About Listed Individuals**

For business professionals whose information appears in the App's company and sector pages, we hold only **name and designation (professional title and company affiliation)**, sourced from public records, regulatory filings (including MCA filings), company websites, and the Inc42 Group's market intelligence data. We do not display or process business contact data (work email, phone, or LinkedIn) for these individuals within the App.

## **4\. Legal Basis for Processing**

Under the DPDP Act, 2023 and other applicable laws, we process personal data on the following bases:

| Purpose | Legal Basis | Applicable Law |
| ----- | ----- | ----- |
| Account creation and service delivery | Consent (provided at registration) | DPDP Act, Section 6 |
| Personalization of content | Consent | DPDP Act, Section 6 |
| Analytics, measurement, and service improvement | Consent | DPDP Act, Section 6 |
| Marketing communications (if any) | Consent (opt-in) | DPDP Act, Section 6 |
| Security and fraud prevention | Certain legitimate uses | DPDP Act, Section 7 |
| Legal compliance | Compliance with law | DPDP Act, Section 7 |
| Listed Individuals' professional data (name, designation) | Publicly available data exemption | DPDP Act, Section 14 |

**Note on analytics and consent.** The DPDP Act does not provide a "legitimate interest" basis equivalent to the GDPR. Analytics and measurement technologies in the App begin operating from the moment you first open it, including while you browse without an account. We are introducing in-App consent controls for this processing in line with the DPDP Act. Until those controls are available, you can manage or limit tracking and analytics through your device settings and permission prompts (including the ATT prompt on Apple devices). Where consent is the legal basis for processing, you may withdraw it at any time.

## **5\. How We Use Your Information**

**5.1 Service Delivery.** Operating the App; delivering the daily Brief, articles, and company and sector information; enabling you to save articles and track companies and sectors; sending notifications for tracked entities; and operating streaks, reader levels, badges, and rewards.

**5.2 Personalization.** Using the preferences you provide (role, sectors, and topics) together with your activity in the App to personalize the Briefs and content shown to you.

**5.3 Communication.** Sending transactional and service messages (such as account, notification, and security messages). We will send marketing or promotional communications only with your consent, and you may withdraw that consent at any time. Even if you opt out of marketing, we may still send you administrative and service-related messages.

**5.4 Analytics and Improvement.** Understanding how the App is used, measuring engagement and the effectiveness of our marketing and install campaigns, diagnosing crashes and performance issues, and improving content, features, and user experience.

**5.5 Security and Legal.** Detecting and preventing fraud, abuse, manipulation of the Streaks and Rewards features, and unauthorised access; enforcing our Terms of Use; complying with legal obligations; and resolving disputes.

The App does not use your information to serve third-party advertising within the App, and does not use AI-generated content features.

## **6\. Mobile Identifiers, Cookies and Tracking Technologies**

The App uses device identifiers, software development kits (SDKs), and similar technologies to recognise your device, measure usage, secure the App, and support our marketing measurement. These include the device-level identifier generated on first open and, where permitted, advertising identifiers. The App does not display third-party advertising to you within the App. Where we refer to advertising identifiers or advertising attribution, these are used solely to measure the effectiveness of Inc42's own campaigns to promote the App — not to serve ads to you inside it.

On Apple devices, you may be asked, through Apple's App Tracking Transparency prompt, whether to allow tracking across other companies' apps and websites; declining may limit advertising-measurement functions but does not prevent you from using the App. You can manage tracking and notification permissions at any time through your device settings. For further detail on cookies and similar technologies, please refer to our Cookie Policy.

## **7\. Disclosure of Information to Third Parties**

**7.1 Service Providers.** We share information with third-party service providers who process it on our behalf, under data processing agreements and only as instructed by us:

| Service Provider Category | Purpose | Examples |
| ----- | ----- | ----- |
| Cloud Hosting | App backend and data hosting | Google Cloud Platform (GCP) |
| Authentication / Sign-In | Login and identity management | Auth0; Sign in with Apple; Sign in with Google |
| Product Analytics | Usage analytics and product improvement | PostHog |
| Advertising Attribution / Measurement | Install and campaign measurement | Singular |
| Crash & Performance | Crash and stability monitoring | Firebase Crashlytics |
| Ads Measurement / Analytics | Measurement for marketing campaigns | Firebase (Google Analytics for Firebase) |
| Push & Messaging | Push notifications and messaging | Customer.io |
| Content Delivery & Security | Content delivery and protection | Cloudflare |
| File Storage | Storage of images and assets | Amazon Web Services (AWS S3) |

The specific providers may change over time as our stack evolves; the current list reflects the App's launch configuration.

**7.2 Social Sharing.** When you use the App's share feature to share an article or link, information is transmitted to the third-party platform you choose to share on. Shared links may contain campaign or tracking parameters (such as UTM tags) that we use for analytics. Those third-party platforms' privacy policies govern their processing.

**7.3 Legal and Regulatory.** We may disclose your information when required by law, regulation, court order, or government request, or where we believe disclosure is necessary to protect the rights, property, or safety of the Inc42 Group, our users, or others.

**7.4 Business Transfers.** If the Inc42 Group undergoes a merger, acquisition, reorganisation, or sale of assets, your information may be transferred to the successor entity, and we will provide notice where required.

**7.5 With Your Consent.** We may share your information for any other purpose with your consent.

## **8\. Cross-Border Data Transfers**

Your data may be processed and stored in locations outside India as part of our use of global service providers.

| Provider | Location | Safeguard |
| ----- | ----- | ----- |
| Google Cloud Platform | India (primary), global | Data processing agreement |
| Auth0 | United States | Data processing agreement |
| PostHog | EU / US | Data processing agreement |
| Firebase (Google) | United States | Data processing agreement |
| Singular | United States | Data processing agreement |
| Customer.io | United States | Data processing agreement |
| AWS S3 | As per provider's infrastructure | Data processing agreement |
| Cloudflare | Global | Data processing agreement |

Where personal data is transferred outside India, we put appropriate safeguards in place, including data processing agreements with Standard Contractual Clauses where applicable, in compliance with the DPDP Act and other applicable laws.

## **9\. Your Rights as a Data Principal**

**9.1 Rights of App Users.** Under the DPDP Act, 2023, you have the rights to: access a summary of your data; correct inaccurate or incomplete data; request erasure of your data (subject to legal retention requirements); withdraw consent; nominate another person to exercise your rights in the event of death or incapacity; and lodge a grievance. You can exercise these rights by emailing grievance+datalabs@inc42.com, or, for account deletion, by using the in-App account-deletion option (Settings → Delete account & data).

**9.2 Rights of Listed Individuals.** Business professionals whose name and designation appear in the App may request to know what professional data we hold, request correction, and object to or opt out of processing. Requests may be made to grievance+datalabs@inc42.com. The opt-out process and timelines are set out in the Contact Data Policy.

**9.3 Additional Rights for EU/EEA Residents (GDPR).** If you are located in the EU or EEA, you additionally have the rights to data portability, restriction of processing, objection, and to lodge a complaint with your local supervisory authority.

We will respond to data-principal requests within 30 days of receipt; if we require additional time, we will notify you.

## **10\. Data Retention**

We retain personal data only for as long as necessary to fulfil the purposes described in this Privacy Policy, or as required by law.

| Data Category | Retention Period |
| ----- | ----- |
| Account data (active users) | Duration of the account, plus 3 years after deletion |
| Account data (inactive users) | 12 months of inactivity, after which the account may be deactivated with notice |
| Usage logs and analytics | 24 months |
| Marketing consent records | Duration of consent, plus 12 months |
| Listed Individuals' professional data | Retained while relevant and accurate; removed upon opt-out |
| Suppression list (opted-out individuals) | Indefinitely (to prevent re-addition) |
| Support records | 3 years from resolution |

Upon expiry of the retention period, data is securely deleted or anonymised. We may retain anonymised or aggregated data, which no longer identifies you, for longer periods, including indefinitely, for analytics, research, and service improvement.

## **11\. Data Security**

We implement technical and organisational measures to protect the confidentiality, integrity, and availability of your data, including encryption of data in transit (TLS) and at rest, role-based access controls on the principle of least privilege, audit logging of sensitive operations, and hosting on infrastructure with enterprise-grade security controls. No security system is impenetrable; while we strive to protect your data, we cannot guarantee absolute security. You are responsible for maintaining the confidentiality of your account credentials and for signing out when using shared devices.

## **12\. Children's Data**

The App is intended for individuals who are at least 18 years of age. Individuals under 18 may use the App only under the supervision and guidance of a parent or legal guardian, through the guardian's account. We do not knowingly collect personal data from a child without verifiable parental consent. If we become aware that we have collected such data without the required consent, we will take steps to delete it promptly. If you believe we have inadvertently collected data from a child, please contact grievance+datalabs@inc42.com.

## **13\. Data Breach Notification**

In the event of a personal data breach likely to result in a risk to the rights of Data Principals, we will notify the Data Protection Board of India within the timelines required under the DPDP Act, and will notify affected Data Principals without undue delay where the breach is likely to result in a high risk to their rights. Notifications will describe the nature of the breach, the categories of data affected, the likely consequences, and the measures taken to address it.

## **14\. Communications and Notifications**

(a) We may contact you by email, in-App message, and push notification for transactional and service purposes.

(b) **Marketing communications** will be sent only with your consent. You may withdraw consent at any time by using the unsubscribe link in any marketing email, adjusting your notification preferences, or emailing support@inc42.com.

(c) **Push notifications** are delivered subject to the notification permission on your device; you can disable them at any time in your device or App settings.

(d) Even if you opt out of marketing, we may still send you administrative, account-related, and security communications.

## **15\. Session Replay**

\<\!-- PENDING CONFIRMATION: include this section only if PostHog session replay is enabled in the App. If enabled, this disclosure must match your Apple privacy label and Google Play Data Safety form. If session replay is NOT enabled, delete this Section 15 entirely and renumber. \--\>

*\[To be confirmed — include only if session replay is enabled\] We may use session replay technology to understand how users interact with the App, identify errors and usability issues, and improve the Services. Where enabled, this technology records interactions such as taps, scrolls, and navigation within the App. This information is collected by our analytics provider and used only for the purposes described in this Privacy Policy.*

## **16\. Changes to This Privacy Policy**

We may update this Privacy Policy from time to time. If we make material changes to how we collect, use, or disclose personal data, we will notify you by posting a prominent notice in the App or through direct communication. The most recent version is indicated by the effective date below.

## **17\. Grievance Redressal & Data Protection Officer**

**Grievance Officer** Inc42 Plus Media Private Limited 59/16, Ground Floor, Gali No. 59, Kalkaji, New Delhi, South Delhi – 110019, Delhi Email: grievances\[@\]inc42.com

**Grievance Officer** Ideope Media Private Limited 59/16, 4th Floor, Jujhar Tower, R.D. Marg, Kalkaji, New Delhi – 110019, Delhi Email: grievances+ideope\[@\]inc42.com

**Data Protection Officer** Inc42 Plus Media Private Limited 59/16, Ground Floor, Gali No. 59, Kalkaji, New Delhi, South Delhi – 110019, Delhi Email: grievance+datalabs@inc42.com

The Data Protection Officer is the point of contact for data protection inquiries, data-principal requests, and complaints from Data Principals and the Data Protection Board of India.

## **18\. How to Contact Us**

General privacy queries and data-principal requests: grievance+datalabs@inc42.com Contact Data opt-out: grievance+datalabs@inc42.com (subject: "Contact Data Opt-Out Request") General support: support\[@\]inc42.com

We will undertake reasonable efforts to address your concern within 30 days.

---

*This Privacy Policy was last updated on \[DATE\].*

# ToU

# **Inc42 App — Terms of Use**

**PLEASE READ THESE TERMS OF USE CAREFULLY BEFORE DOWNLOADING, INSTALLING, OR USING THE INC42 MOBILE APPLICATION.**

These Terms of Use ("Terms") govern your download, installation, access to, and use of the Inc42 mobile application for iOS and Android (the "App"). These Terms are separate from, but consistent with, the terms of use governing the Inc42 website (www.inc42.com). Where you also use the website or other Inc42 services, those separate terms apply to that use.

This document is an electronic record in terms of the Information Technology Act, 2000 and the rules thereunder as applicable, and the amended provisions pertaining to electronic records in various statutes as amended by the Information Technology Act, 2000\. This electronic record is generated by a computer system and does not require any physical or digital signatures.

---

## **Definitions**

"**Ideope**" means Ideope Media Private Limited, a technology service provider that also carries out marketing, educational, and non-news content development activities.

"**Inc42**" or "**Company**" or "**we**" or "**us**" or "**our**" means Inc42 Plus Media Private Limited, which operates the App under an exclusive, non-transferable, non-sublicensable, non-assignable, worldwide licence from Ideope to access, use, manage, and operate the App and use Ideope's intellectual property.

"**Inc42 Group**" means Inc42 and Ideope collectively, together with their affiliates, partners, associates, or subsidiaries.

"**Suppliers**" means the third-party licensors, data providers, and service providers that supply content, data, or services used in or made available through the App.

"**App**" means the Inc42 mobile application made available for iOS and Android devices, including all updates, upgrades, and versions thereof.

"**App Store**" means the Apple App Store, the Google Play Store, or any other third-party platform through which the App is distributed.

"**Services**" means all features and functionality made available through the App, including access to digital news and media content, company and sector information, the ability to save articles, the ability to track companies and sectors and receive related notifications, and the Streaks and Rewards features.

"**Brief**" means a daily piece of content or task made available in the App for a User to complete.

"**Streaks and Rewards**" means streaks, reader levels, badges, and similar engagement indicators, together with any rewards associated with them, made available in the App, as described in Section 9\.

"**Inc42 IPR**" means all content (including articles, audios, photographs, illustrations, graphics, other visuals, videos, copy, text, software, data, datasets, company and sector information, reports, analytics, and insights), code, data and materials on or accessible through the App, the look and feel, design and organisation of the App, and the compilation of the content, code, data and materials therein, including but not limited to any copyrights, trademark rights, trade secrets, know-how, patent rights, database rights, service marks, moral rights, sui generis rights and other intellectual property and proprietary rights therein.

"**User**" or "**you**" or "**your**" means any person who accesses or uses the App, whether or not registered.

"**Registered User**" means a User who has created an account through the App as described in these Terms.

"**Data Principal**" has the meaning assigned under the Digital Personal Data Protection Act, 2023\.

---

## **1\. Acceptance of Terms**

By downloading, installing, accessing, or using the App, or by clicking "I agree" (where presented), you signify your acceptance of these Terms and of our Privacy Policy, Cookie Policy, and all other policies referenced herein, which are incorporated into these Terms by reference.

Inc42 reserves the right to amend, remove, or add to these Terms at any time at its sole and absolute discretion. Such modifications shall be effective immediately upon posting within the App or on the website. Your continued access to or use of the App after the posting of modifications constitutes your acceptance of the modified Terms.

Some features of the App may be subject to additional posted terms and conditions. Your use of those features is subject to those conditions, which are incorporated into these Terms by reference. In the event of an inconsistency, the provisions of the additional conditions shall prevail with respect to that feature.

If, at any time, you do not wish to accept these Terms, you may not access or use the App, and you should uninstall it.

## **2\. Eligibility**

You will be eligible to use the App only if you are competent to contract under the Indian Contract Act, 1872\. You represent and warrant that you are at least eighteen (18) years of age and are capable of entering, performing and adhering to these Terms. While individuals under the age of 18 may utilise the App, they shall do so only with the involvement and guidance of their parents and/or legal guardians, under such parent's or legal guardian's registered account.

## **3\. The App and Its Services**

3.1 **Content.** Through the App, Inc42 provides access to digital news and media content, and to company and sector information, on an as-is basis. Certain company and sector information available in the App is sourced from the Inc42 Group's market intelligence data. The App does not provide access to the Inc42 Datalabs subscription platform or its subscription-gated features (such as credits, contact reveals, data exports, or AI-powered tools).

3.2 **Browsing without registration.** You may browse and read content in the App without creating an account.

3.3 **Save and Track.** Registered Users may save articles for later reference and may track companies and sectors. When you track a company or sector, you may receive notifications (including push notifications) about updates relating to those companies or sectors, subject to Section 8\.

3.4 **Streaks and Rewards.** The App may offer Streaks and Rewards features, such as streaks, reader levels, badges, and, where made available, rewards, to recognise and encourage consistent engagement (for example, completing a Brief each day), as described in Section 9\.

3.5 **Personalization.** The App may ask you to provide preferences (such as your professional role, sectors, and topics of interest) and may use these, together with your activity in the App, to personalize the Briefs and other content shown to you. This processing is carried out in accordance with the Privacy Policy and applicable law, including the Digital Personal Data Protection Act, 2023\.

3.6 **Sharing.** The App may allow you to share articles or links to content using your device's sharing options and third-party applications. Links you share may contain campaign or tracking parameters (such as UTM tags) that Inc42 uses to measure engagement and for analytics purposes. You are responsible for your use of any sharing functionality and for compliance with the terms of any third-party platform on which you share.

3.7 **No user-generated content.** The App does not provide functionality for Users to post comments, upload content, or otherwise submit material for public display.

3.8 **Availability.** The Company may modify, suspend, or discontinue, temporarily or permanently, any or all of the Services (or any part thereof) at any time, with or without notice, without liability.

## **4\. Registration and Account**

4.1 **When registration is required.** Registration is required only to use the save, track, and Streaks and Rewards features. Browsing content does not require an account.

4.2 **Sign-in methods.** Registration and login are provided through Auth0 and through social login using Sign in with Apple and Sign in with Google. By registering, you authorise Inc42 and Ideope to collect and process the personal data received through your chosen sign-in method in accordance with the Privacy Policy.

4.3 **Accurate information.** You agree to provide only true, accurate, current, and complete information at registration and to keep it updated.

4.4 **Account security.** You are solely responsible for maintaining the confidentiality of your account credentials and for all activities that occur under your account. You shall immediately notify Inc42 of any known or suspected unauthorised use of your account. Inc42 will not be liable for any loss arising from unauthorised use of your account.

4.5 **One account.** You agree to maintain only one account and certify that you currently have no other account(s). If Inc42 reasonably believes an account is being shared or misused in violation of these Terms, Inc42 reserves the right to cancel access rights immediately without notice.

4.6 **Account inactivity.** Inc42 reserves the right to deactivate accounts that have been inactive for an extended period (12 months or more), with prior notice to the registered email address.

4.7 **Single Inc42 account.** Your account may form a single Inc42 identity shared across the App, the Inc42 website, and other Inc42 services (including Inc42 Datalabs). The same credentials may provide access across these services, and certain actions — such as updating your profile or deleting your account — may take effect across all of them. Your use of any other Inc42 service remains subject to the terms applicable to that service.

## **5\. Licence to Use the App**

Subject to your compliance with these Terms, Inc42 grants you a limited, non-exclusive, non-transferable, non-sublicensable, revocable licence to download, install, and use the App on a mobile device that you own or control, solely for your personal, non-commercial, and internal business use.

This licence does not grant you any right, title, or interest in the App or the Inc42 IPR, other than the limited right to use them in accordance with these Terms. All rights not expressly granted are reserved by the Inc42 Group and/or its licensors.

## **6\. Your Device and Connectivity**

You are responsible for obtaining and maintaining the mobile device, operating system, software, and internet or data connection required to download and use the App, and for ensuring your device meets the minimum technical requirements notified from time to time.

You are solely responsible for all mobile-data, telecommunications, roaming, and other charges you incur in connection with your use of the App, including in relation to downloading content or receiving notifications. Your network operator's charges are a matter between you and your operator.

If you sell, transfer, or dispose of your device, you should log out of and remove the App from that device.

## **7\. App Updates**

The App may, from time to time, automatically download and install updates, upgrades, new versions, or new features. Whether such updates install automatically may be governed by your device's operating system or App Store settings. Certain updates may be necessary for the continued use of the App.

All updates are subject to these Terms unless accompanied by separate terms, in which case those separate terms apply. Inc42 does not guarantee that the App will be compatible with all devices or operating system versions, or that it will continue to support any particular device or operating system version.

Inc42 may require you to install a minimum or current version of the App in order to continue using it, and may disable, limit, or block the functioning of older or unsupported versions. If a required update is not installed, some or all features of the App may become unavailable.

## **8\. Push Notifications**

If you track companies or sectors, use the Streaks and Rewards features, or otherwise opt in, the App may send you push notifications. Push notifications are delivered subject to the notification permission granted at the operating-system level on your device.

You may disable push notifications at any time through your device settings or, where available, within the App's settings. Disabling notifications may limit or remove the usefulness of the track and Streaks and Rewards features.

## **9\. Streaks and Rewards**

9.1 **Overview.** The App may offer Streaks and Rewards — including streaks, reader levels, badges, and, where made available, rewards — to recognise and encourage consistent engagement with the App. A day is treated as "active" when you complete at least one qualifying activity (such as a Brief) on that calendar day, and your streak reflects the number of consecutive active days. The specific rules, day-count thresholds, level names, badges, and qualifying activities are determined by Inc42, are described in the App, and may change (see Section 9.4).

9.2 **No monetary value.** Streaks, reader levels, badges, and similar features are provided solely for engagement and status purposes and have **no monetary value**. They are not virtual currency, are not your property, and cannot be redeemed, exchanged, transferred, sold, or converted into cash, credit, goods, or discounts, except as may be expressly stated for a specific reward under separate terms as described in Section 9.5.

9.3 **Streaks reset; badges and levels retained.** Streaks are based on consecutive active days and will reset (including to zero) if you miss a day or otherwise do not meet the applicable conditions; after a reset, a new streak begins from the start. Badges and reader levels, once earned, are generally retained and are not re-earned upon a subsequent streak. Inc42 does not guarantee the continuity or accuracy of any streak, level, badge, or reward.

9.4 **Changes.** Inc42 may, at its sole discretion and at any time, introduce, modify, suspend, reset, or discontinue any Streaks and Rewards feature, or change the rules, thresholds, qualifying activities, level names, badges, or rewards, without notice and without liability.

9.5 **Rewards.** Where the App offers rewards in connection with streaks, milestones, or levels, such rewards:

(a) may be introduced, changed, limited, or withdrawn at any time and are subject to availability;

(b) may be subject to separate reward-specific or promotional terms and conditions, which will be made available at the relevant time and which will prevail over this Section in the event of any conflict;

(c) may be provided, fulfilled, or sponsored by third parties, in which case the third party's terms may also apply, and Inc42 is not responsible for the third party's goods, services, or conduct; and

(d) confer no entitlement — no User has a right to any particular reward, and Inc42 does not guarantee that any reward will be offered, remain available, or be fulfilled.

9.6 **Anti-abuse.** Inc42 reserves the right to review, adjust, freeze, or forfeit any streaks, badges, levels, or rewards, and to suspend or terminate your account, where it reasonably believes you have manipulated, gamed, or abused the Streaks and Rewards features, including through automated means, multiple accounts, false or artificial completion of Briefs, or any breach of these Terms.

9.7 **No liability.** Inc42 shall have no liability for any loss of, reset of, or inability to access any streak, badge, level, or reward.

## **10\. App Store Terms**

10.1 You acknowledge that these Terms are concluded between you and Inc42 only, and not with Apple Inc. ("Apple") or Google LLC ("Google"). Inc42, not Apple or Google, is solely responsible for the App and its content.

10.2 Your use of the App must comply with the applicable App Store's terms of service and usage rules in effect at the time (including the Apple Media Services Terms and Conditions and the Google Play Terms of Service, as applicable).

10.3 Apple and Google have no obligation to furnish any maintenance or support services with respect to the App. To the maximum extent permitted by applicable law, Apple and Google have no warranty obligation with respect to the App.

10.4 Apple and Google, and their subsidiaries, are third-party beneficiaries of these Terms, and upon your acceptance of these Terms will have the right (and will be deemed to have accepted the right) to enforce these Terms against you as a third-party beneficiary thereof, in each case solely to the extent these Terms relate to your use of the App obtained through the relevant App Store.

10.5 You represent and warrant that you are not located in a country subject to a relevant government embargo, or designated as a "terrorist supporting" country, and that you are not listed on any relevant government list of prohibited or restricted parties.

## **11\. Proprietary Rights and Intellectual Property**

Except as expressly permitted herein, you do not have any right, title, or interest in or to the Inc42 IPR. Your use of the App does not grant you ownership of any content, code, data, datasets, or materials you may access on or through the App, including any company or sector information sourced from the Inc42 Group's data.

All content, data, reports, analytics, and insights accessible through the App remain the exclusive property of the Inc42 Group and/or its licensors. Access to such content through the App grants you a limited, non-exclusive, non-transferable, revocable licence to view such content for your personal, non-commercial, and internal business use only, subject to these Terms.

## **12\. Permitted Use**

You may access and view content on the App on a mobile device you own or control. Unless otherwise specifically indicated, use of the App and the Inc42 IPR is only for your personal, non-commercial, and internal business use. You shall not use the App or the Inc42 IPR, or any portion thereof, for any other purpose without Inc42's prior written approval, except as specifically permitted herein.

## **13\. Prohibited Uses**

Unless otherwise specifically indicated in these Terms or in the App, you shall NOT:

**13.1 General**

(a) Copy, reproduce, distribute, transmit, modify, perform, broadcast, transfer, create derivative works from, sell, or otherwise exploit any content, code, data, or materials of, on, or available through the App.

(b) Alter, edit, delete, remove, or otherwise change the meaning or appearance of, or repurpose, recompile, decompile, disassemble, or reverse engineer any content, code, data, or other materials in the App or the App itself, except to the extent such restriction is prohibited by applicable law.

(c) Use the App for any illegal purpose, for the facilitation of the violation of any law or regulation, or in any manner inconsistent with these Terms.

(d) Use, transfer, distribute, or dispose of any information contained in the App or the Inc42 IPR in any manner that could compete with the business of the Inc42 Group or any of its Suppliers.

(e) Engage in screen scraping, database scraping, data mining, phishing, spidering, or harvesting of email addresses or other data.

(f) Use any scraper, robot, bot, spider, automated device, program, tool, algorithm, process, or methodology to access, acquire, copy, or monitor any portion of the App or any data or content found on or accessed through it, without the prior express written consent of Inc42.

(g) Forge headers or otherwise manipulate identifiers in order to disguise the origin of any content.

(h) Attempt to gain unauthorised access to the App, any data, materials, information, computer systems, or networks connected to any server associated with the App, through hacking, password mining, or any other means.

(i) Take or attempt any action that imposes an unreasonable or disproportionately large load on the App or its infrastructure, including any denial-of-service attack.

(j) Use the App to distribute or transmit any content that is unlawful, harmful, threatening, abusive, defamatory, vulgar, obscene, or otherwise objectionable, including content that threatens the unity, integrity, defence, security, or sovereignty of India.

(k) Use any automated means, multiple or fraudulent accounts, false or artificial completion of Briefs, or any other artificial or deceptive method to accrue, inflate, or otherwise manipulate streaks, reader levels, badges, rewards, or any other Streaks and Rewards feature.

**13.2 Anti-AI Training and Data Exploitation**

(l) You shall not use any data, content, articles, company or sector information, or other material from the App for training, fine-tuning, validating, or developing any artificial intelligence model, machine learning model, large language model (LLM), natural language processing system, or any derivative technology, whether directly or through a third party. This prohibition applies regardless of the method of access (manual, API, scraping, or otherwise) and regardless of whether such use is for commercial or non-commercial purposes.

(m) You shall not use any data from the App as a substitute for, or to create a competing product or service to, the App, Inc42 Datalabs, or any of their features.

(n) You shall not build, compile, or aggregate any data obtained from the App into a database or dataset for resale, redistribution, or sublicensing to any third party.

## **14\. Feedback**

If you choose to provide any feedback, suggestions, ideas, or recommendations regarding the App (collectively, "Feedback"), you grant the Inc42 Group a perpetual, irrevocable, worldwide, royalty-free, sublicensable, and transferable licence to use, reproduce, modify, and otherwise exploit such Feedback for any purpose, without any obligation of notice, attribution, confidentiality, or compensation to you. Feedback shall not be treated as confidential.

## **15\. Data Attribution**

If you reference, cite, or display any data, statistics, charts, or insights obtained from the App in any external publication, presentation, report, or media, you must:

(a) Clearly attribute the data to "Inc42" as the source;

(b) Include a hyperlink to inc42.com where the data is displayed digitally;

(c) Not alter, misrepresent, or take data out of context in a manner that could be misleading; and

(d) Not imply endorsement, partnership, or affiliation with Inc42 unless such a relationship has been formally agreed in writing.

## **16\. Third-Party Services and Links**

16.1 The App may contain links to third-party websites or resources. We are not responsible for the content, products, or services on those websites or resources.

16.2 The App integrates with third-party services, including Auth0 for authentication and Apple and Google for social login. Your use of these integrated services may be subject to their respective terms and conditions and privacy policies.

16.3 The App uses third-party product-analytics, advertising-attribution, crash-reporting, and messaging providers that collect device and usage data to help us understand, measure, secure, and improve the App and its marketing. Such data may be collected from the moment you first open the App, including while you browse without an account. The specific providers used, and the categories of data they collect, are described in the Privacy Policy and in the App's privacy disclosures on the Apple App Store and Google Play.

## **17\. Privacy and Data Protection**

Your use of the App is also governed by our Privacy Policy, which describes how we collect, use, disclose, and protect your personal data in compliance with the Digital Personal Data Protection Act, 2023 (India), the Information Technology Act, 2000, and other applicable laws.

The App uses analytics and measurement technologies. The personal data collected, the purposes of processing, and how you may give or withdraw consent are described in the Privacy Policy and in the notices presented to you in the App. As a Data Principal under the Digital Personal Data Protection Act, 2023, you have the rights described in the Privacy Policy, including, where consent is the legal basis for processing, the right to withdraw consent at any time.

The App personalizes the Briefs and content shown to you based on preferences you provide (such as your professional role, sectors, and topics of interest) and your activity in the App. This personalization is carried out in accordance with the Privacy Policy and applicable law.

The App may generate a device-level identifier when you first open it, which is used for analytics and measurement whether or not you create an account. On Apple devices, you may be asked, through Apple's App Tracking Transparency prompt, whether to allow tracking across other companies' apps and websites; declining may limit advertising-measurement functions but does not prevent you from using the App. You can manage tracking and notification permissions at any time through your device settings.

## **18\. Intermediary Status**

In addition to hosting content created by the Inc42 Group, the App operates as an "intermediary" as defined under the Information Technology Act, 2000 and the Information Technology (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021, as amended from time to time.

## **19\. Right to Monitor and Editorial Control**

We reserve the right, but have no obligation, to monitor use of the App. We reserve the right to disclose information as necessary to satisfy any law, regulation, or government request, and to edit, refuse to display, or remove any content that is objectionable or in violation of these Terms.

## **20\. Disclaimer and Limitation of Liability**

(a) **As-is basis.** You agree that your use of the App is at your sole risk. The App, all features, content, functions, and materials are provided "AS IS" and "AS AVAILABLE," without warranty of any kind, either express or implied, including without limitation any warranties concerning availability, accuracy, correctness, completeness, usefulness, uptime, or uninterrupted access, and any warranties of title, non-infringement, merchantability, or fitness for a particular purpose. We hereby disclaim any and all such warranties.

(b) **Data accuracy.** Inc42 does not warrant the accuracy, completeness, timeliness, or reliability of any content or data available through the App, including company and sector information and financial or funding data. Such data is sourced from public records, third-party providers, and automated processes and may contain errors or be outdated.

(c) **No investment advice.** None of the information in the App constitutes a solicitation, offer, opinion, or recommendation by Inc42 to buy or sell any security, or to provide legal, tax, accounting, or investment advice regarding the profitability or suitability of any security or investment. Investments in securities are subject to market risks, and nothing in the App shall be construed as a recommendation or advisory to trade in any securities.

(d) **Third-party individuals' data.** Company profiles in the App may display limited professional information about founders, executives, and other business professionals — namely their name and designation — sourced from the Inc42 Group's market intelligence data and from public and third-party records. The App does not display business contact information (such as work email, phone number, or profile links) for such individuals. Inc42 does not guarantee the accuracy, currency, or completeness of such information. Its display and processing are governed by the Privacy Policy and, where applicable, the Contact Data Policy, under which affected individuals may exercise their rights.

(e) **Limitation of liability.** Under no circumstances shall the Inc42 Group, its Suppliers, agents, directors, officers, employees, representatives, successors, or assigns be liable for any direct, indirect, incidental, consequential, special, punitive, or exemplary damages arising from the use of or inability to use the App, even if advised of the possibility of such damages. In no event shall the Inc42 Group's total aggregate liability exceed one thousand Indian Rupees (INR 1,000).

## **21\. Indemnification**

You agree, at your own expense, to indemnify, defend, and hold harmless the Inc42 Group, its Suppliers, agents, directors, officers, employees, shareholders, representatives, successors, and assigns from and against any and all claims, damages, liabilities, costs, and expenses, including reasonable attorneys' fees, arising out of or in connection with: (a) your use of the App; (b) a violation of these Terms by you or anyone using your account; (c) any claim that your use of the App infringes any intellectual property right or privacy right; or (d) any misrepresentation or breach of warranty made by you herein.

## **22\. Termination**

(a) Inc42 reserves the right to terminate your account or your access to the App, in whole or in part, at its sole discretion, at any time without notice, if you breach these Terms, engage in prohibited activities, or for any other reason Inc42 deems appropriate.

(b) **Deletion by you.** You may delete your account at any time directly within the App, using the account-deletion option in the App's settings, or by contacting support@inc42.com. Upon deletion, your account and associated data will be handled as described in the Privacy Policy. Because your Inc42 account may be shared across the App, the Inc42 website, and other Inc42 services (see Section 4.7), deletion may affect your access to those other services. Uninstalling the App alone does not delete your account.

(c) You may also stop using the App at any time by uninstalling it. Upon termination, you must discontinue use of the App.

(d) Termination does not relieve you of any obligations incurred prior to termination.

## **23\. Trademarks**

The trademarks, logos, service marks, and trade names (collectively the "Trademarks") displayed in the App are the Inc42 Group's registered and unregistered Trademarks and may not be used without written permission. All third-party Trademarks in the App are the property of their respective owners. Nothing in the App shall be construed as granting any licence or right to use any Trademark without written permission.

## **24\. Governing Law and Jurisdiction**

These Terms shall be governed and construed in accordance with the laws of India. You agree to submit to the exclusive jurisdiction of the courts of New Delhi, India, with respect to any legal proceedings that may arise in connection with the App or from a dispute as to the interpretation or breach of these Terms.

## **25\. Grievance Redressal**

In accordance with the Information Technology Act, 2000 and the Digital Personal Data Protection Act, 2023, the details of the designated officers are provided below:

**Grievance Officer** Inc42 Plus Media Private Limited 59/16, Ground Floor, Gali No. 59, Kalkaji, New Delhi, South Delhi – 110019, Delhi Email: grievances\[@\]inc42.com

**Grievance Officer** Ideope Media Private Limited 59/16, 4th Floor, Jujhar Tower, R.D. Marg, Kalkaji, New Delhi – 110019, Delhi Email: grievances+ideope\[@\]inc42.com

**Data Protection Officer:** grievance+datalabs@inc42.com

Any complaints or concerns regarding content, breach of these Terms, or data protection matters should be taken up with the designated officer via email, signed with electronic signature.

For general Inc42 queries: support@inc42.com

## **26\. Notice of Copyright Infringement**

The Inc42 Group respects the intellectual property rights of others. If you believe that your work has been copied in a way that constitutes copyright infringement, please forward the following information to the Grievance Officer:

(a) A physical or electronic signature of a person authorised to act on behalf of the copyright owner;

(b) Identification of the copyrighted work claimed to have been infringed;

(c) Identification of the material in the App that is claimed to be infringing;

(d) Your address, telephone number, or email address;

(e) A statement of good-faith belief that the use is not authorised; and

(f) A statement, under penalty of perjury, that the information is accurate and that you are authorised to act on behalf of the copyright owner.

## **27\. Miscellaneous**

**27.1 Entire Agreement.** These Terms, together with the Privacy Policy, Cookie Policy, Contact Data Policy, and any other terms posted in the App or on the website, constitute the entire agreement between you and Inc42 with respect to the App.

**27.2 Severability.** If any provision of these Terms is found invalid or unenforceable, that provision will be enforced to the maximum extent permissible, and the other provisions will remain in full force and effect.

**27.3 Assignment.** Inc42 or Ideope may assign these Terms or any part thereof without restriction. You may not assign, transfer, or sub-licence your rights under these Terms to any third party.

**27.4 Waiver.** Any failure to enforce any provision of these Terms shall not be construed as a waiver of the right to enforce such provision in the future.

**27.5 Survival.** Provisions relating to Intellectual Property, Warranties, Indemnity, Limitation of Liability, and any other rights and obligations which by their nature should survive shall continue to apply after termination of these Terms.

**27.6 Limited Time to Claim.** Any legal action arising out of or related to the App must be initiated within one (1) year from the accruing of the cause of action; otherwise, such cause of action shall be deemed to have ceased to exist.

**27.7 Force Majeure.** Inc42 shall not be liable for any failure to perform its obligations where such failure results from circumstances beyond Inc42's reasonable control, including natural disasters, acts of government, internet disruptions, or third-party service outages.

---

**Copyright © Inc42.com. All Rights Reserved.** This Terms of Use document is subject to change without notice.

*These Terms of Use were last updated on \[DATE\].*

# sign-in bottom sheet

**1\. Save Article** *(bookmark)*

* Headline: **Sign in to save this article**  
* Subhead: Keep the articles you want to come back to in one place, your library syncs across every device.  
* Pill: ✓ We'll save this article the moment you're in

**2\. Track Company** *(star)*

* Headline: **Sign in to track {company}**   
* Subhead: Add it to your watchlist and get alerts on the latest updates.   
* Pill: ✓ We'll start tracking it the moment you're in

**3\. Track Sector** *(star)*

* Headline: **Sign in to track {sector}**   
* Subhead: **Follow the stories moving the whole sector, all in one feed.**  
* Pill: ✓ We'll start tracking it the moment you're in

**4\. Watchlist** 

* Headline: **Sign in to build your watchlist**  
* Subhead: Save articles and track the companies and sectors you care about — all in one place.  
* Pill: ✓ We'll set up your watchlist the moment you're in

**5\. Login to view streak** 

* Headline: **Sign in to keep your streak**  
* Subhead: Track your reading streak and stay on top of the market every day.  
* Pill: ✓ Your streak is saved the moment you're in 

**6\. General Login** *(app logo)*

* Headline: **Sign in to get started**   
* Subhead: Sync your saved articles, tracked companies, and streak across every device.

# New\_event\_sheet\_Changes

### **P0 — Architecture** 

1. **Create person profiles for anonymous users — BUG (For both [customer.io](http://customer.io) and posthog)**  
   * **Expected:** A person profile should be created for non logged-in users so `setPersonProperties()` updates are stored successfully.  
   * **Actual:** No person profile is created for anonymous users, so every logged-out `setPersonProperties()` call fails silently.  
   * **Not triggering for anonymous users :**   
     * `push_permission_granted` → set `push_opt_in`  
     * `push_permission_denied` → set `push_opt_in`  
     * `notification_settings_changed` → set `push_opt_in`, `push_types_enabled`  
     * `preferences_updated` → set `role`, `sector_groups`, `topic_groups`  
     * `app_installed`→ set `install_date, attribution_source, attribution_campaign`  
     * `Onboarding_completed` → set `role`, `sector_groups`, `topic_groups`  
     * `Walkthrough` → set `walkthrough_status`   
     * `push_delivered` → set `push_types_enabled`  
     * `brief_completed` → set `streak_current, streak_maxstreak_tier, briefs_completed_total, last_brief_completed_at, last_brief_opened_at`  
2. **Stop sending all properties in one bundle**  
   * **Expected:** Each `setPersonProperties()` call should send only the properties relevant to that event.  
   * **Actual:** `setPersonProperties()` call sends a large batch of unrelated properties.  
   * **List:**   
     * `push_permission_granted` → set `push_opt_in`  
     * `push_permission_denied` → set `push_opt_in`  
     * `notification_settings_changed` → set `push_opt_in`, `push_types_enabled`  
     * `preferences_updated` → set `role`, `sector_groups`, `topic_groups`  
     * `app_installed`→ set `install_date, attribution_source, attribution_campaign`  
     * `onboarding_completed` → set `role`, `sector_groups`, `topic_groups`  
     * `walkthrough` → set `walkthrough_status`   
     * `push_delivered` → set `push_types_enabled`  
     * `story_saved` → set `watchlist_count`  
     * `story_unsaved` → set `watchlist_count`  
     * `watchlist_entity_added` → set `watchlist_count,tracked_sector_count`  
     * `watchlist_entity_removed` → set `watchlist_count,tracked_sector_count`  
     * `sign_in_completed` → set `is_registered, auth_method, dnd = false,email`  
     * `register` → set `is_registered, auth_method,registration_date, register_source`  
     * `account_deleted` → set `dnd = true`  
     * `brief_completed` → set `streak_current, streak_maxstreak_tier, briefs_completed_total, last_brief_completed_at, last_brief_opened_at`  
3. **Remove email from every event payload**  
   * **Expected:** `email` should exist only as a person property, triggered by `sign_in_completed identify call`  
   * **Actual:** `email` is included in every event payload.

---

### **P1 — Missing `setPersonProperties()` calls (profile never updates)**

4. **`brief_completed`**  
   * **Expected:** `setPersonProperties()` should update `briefs_completed_total`, `last_brief_completed_at`, `last_brief_opened_at`, `streak_current`, `streak_max`, and `streak_tier`.  
     Should also trigger for anonymous users/ non-logged in users  
   * **Actual:** No `setPersonProperties()` call is made, so these profile properties never update. Not getting triggered for anonymous users/ non-logged in users  
5. **`story_saved` / `story_unsaved`**  
   * **Expected:** `setPersonProperties()` should update `watchlist_count`.  
   * **Actual:** No profile update occurs.  
6. **`watchlist_entity_added` / `watchlist_entity_removed`**  
   * **Expected:** `setPersonProperties()` should update `watchlist_count`.  
   * **Actual:** No profile update occurs.

---

### **P1 — Watchlist counting logic**

7. **`Change watchlist_size_after → watchlist_size_before in watchlist_entity_added and watchlist_entity_removed events`**   
   * **Expected:** **Expected:** The event should intentionally send `watchlist_size_before`, representing the watchlist count before the action, replacing the current `watchlist_size_after` property.   
   * **Actual:** The event currently sends `watchlist_size_after`; this should be changed to `watchlist_size_before`. This event property is present in **`watchlist_entity_added and watchlist_entity_removed events`**  
8. **`watchlist_count`**  
   * **Expected:** Should include both tracked entities(Industries/Sectors and Companies) and saved articles.  
   * **Actual:** Only tracked entities(Industries/Sectors and Companies) are counted.  
9. **`watchlist_entity_added`**  
   * **Expected:** `entity_name` should be populated for sectors, just as it is for removal events.  
   * **Actual:** `entity_name` is `null` when adding sector entities.

---

### **P2 — Wrong property values**

10. **`deep_link_opened`**  
* **Expected:** `source`, `medium`, and `content` should be populated.  
* **Actual:** These properties are missing.  
11. **`app_installed`**  
* **Expected:** The install-time `setPersonProperties()` call should set `install_date`, `attribution_source`, and `attribution_campaign`.  
* **Actual:** These properties are populated only later via `identify()`.  
12. **`search_result_tapped`**  
* **Expected:** `entity_or_story_id` should contain the article ID.  
* **Actual:** The article slug is sent instead.  
13. **`summary_expanded`**  
* **Expected:** For story cards, the property should be `story_id`. For company cards, the property should be `company_id`.  
* **Actual:** The event uses the `story_id` key even for company cards, instead of `company_id`.  
14. **`story_shared`**  
* **Expected:** `channel` should be populated as an event property, and only the `story_shared` event should be emitted.  
* **Actual:** `channel` is incorrect, and a separate "share initiated" event is also emitted.

---

### **P2 — Event not firing**

15. **`sign_in_prompt_shown`**

**Expected**  
Fires whenever an anonymous user encounters a sign-in wall.

Triggers:

* Track company  
* Track sector  
* Save article  
* Brief card  
* Streak

**Group**

* Auth

**Property Group**

* Super only

**Property**

* `source`  
  * `track_company`  
  * `track_sector`  
  * `save_article`  
  * `Brief_card`  
  * `streak`

**Actual**

* Event does not exist.

---

### **P3 — Cleanup**

16. **Remove `is_new_account` from `register`**  
* **Expected:** `is_new_account` should no longer be sent on the `register` event.  
* **Actual:** It is still included. 

### **17\. `streak_milestone_viewed` fires on non-milestone days**

**Expected**

* `streak_milestone_viewed` fires only at `streak_current` \= **1, 7, 30, 100** (ordinary days never trigger the interstitial).  
* Each milestone day maps to exactly one tier promotion:  
  * Day 1 → `reader`  
  * Day 7 → `regular`  
  * Day 30 → `insider`  
  * Day 100 → `ecosystem_native`  
* On every other day (2–6, 8–29, 31–99, 101+), the event must not fire.

**Actual**

* `streak_milestone_viewed` also fires on non-milestone days. Confirmed on live profiles where it fired on Day 2 and Day 3\.

---

### **18\. `tracked_sector_count`, `streak_current`, and `streak_max` are wrong and are not updating via `setPersonProperties()`**

**Expected**

* `tracked_sector_count` reflects the current number of distinct tracked sectors and can return to `0` when no sectors are tracked (not increment-only).  
* `streak_current` and `streak_max` always reflect the live streak values.  
* These properties are updated via `setPersonProperties()` on the events that modify them:  
  * `watchlist_entity_added` / `watchlist_entity_removed` → set `tracked_sector_count,watchlist_count`  
  * `story_saved` / `story_unsaved` → set `watchlist_count`  
  * `brief_completed` → set `streak_current`, `streak_max`, `streak_total`, `last_brief_completed_at`, `last_brief_opened_at`

**Actual**

* `tracked_sector_count` is incorrect. It holds a stale value after sectors are untracked and does not reset correctly.  
* `streak_current` and `streak_max` are also not updating correctly.

  ### **19\. Add `edition_type` to all brief-related events**

**Expected:**

* Add a new event property `edition_type` (enum) to:  
  * `brief_page_opened`  
  * `brief_opened`  
  * `card_viewed`  
  * `brief_completed`  
  * `brief_fallback_shown`  
* Allowed values (lowercase snake\_case):  
  * `weekday` — Tuesday–Saturday brief  
  * `weekend` — Monday brief covering **Saturday 7:00 AM → Monday 7:00 AM**  
  * `weekly_recap` — Sunday recap covering **Monday 7:00 AM → Sunday 7:00 AM**  
* The value must remain consistent across the entire brief session (open, card views, completion, etc.).

**Actual:**

* `edition_type` is missing from all brief-related events, making it impossible to distinguish between weekday, weekend, and weekly recap editions in analytics.

  ### **20\. Add `article_published` server-side event**

**Expected:**

* Fire a server-side `article_published` event once per article when the editorial team publishes it.  
* Send the event to:  
  * Customer.io   
  * PostHog   
* Include the **Story** property bundle  
* event properties:  
  * `story_id` (string)  
  * `title` (string)  
  * `url` (string)

**Actual:**

* No event is emitted when an article is published.

  ### **21\. Add `card_rated` event for Brief cards**

**Expected:**

* Fire a `card_rated` event whenever a user taps:  
  * 👍 More like this  
  * 👎 Less like this  
    on any brief card  
* Property groups:  
  * Super  
  * Story  
* Event properties:  
  * `rating` (enum: `more_like_this` / `less_like_this`)  
  * `story_id` (string)  
  * `position` (number, 0-based card index)  
  * `card_type` (enum: `editorial` / `signal` / `recap`)  
  * `is_boosted` (boolean)  
  * `boost_reason` (enum: `featured` / `tracked_company` / `tracked_sector` / `none`)

  * ### `edition_type` 

**Actual:**

* Story rating interactions are not tracked.

  ### **22\. Add `profile_name_updated` event**

**Expected:**

* Fire a \-side `profile_name_updated` event when a user saves changes in **Profile → Edit Profile**.  
* Fire only after a successful save.  
* Property group:  
  * Super  
* Event properties:  
  * `fields_changed` (array containing only changed fields: `first_name` and/or `last_name`)  
  * `new_first_name` (string)  
  * `new_last_name` (string)  
* On the same action, update person properties via `identify` / `setPersonProperties`:  
  * `first_name`  
  * `last_name`

**Actual:**

* Name edits are neither tracked nor reflected in person properties.

  ### **23\. Add `publishing_date` to the Story property bundle**

**Expected:**

* Add `publishing_date` to the Story property bundle.

**Actual:**

* Not captured.

  ### **24\. Add `first_name` and `last_name` person properties**

**Expected:**

* Add two person properties:  
  * `first_name` (string)  
  * `last_name` (string)  
* Populate them during `sign_in_completed`.  
* Update them whenever `profile_name_updated` is fired.

**Actual:**

* `first_name` and `last_name` person properties do not exist.

  ### **25\. Extend the `sign_in_completed` identify call**

**Expected:**

* Extend the existing `identify` / `setPersonProperties` call on `sign_in_completed`.  
* In addition to the existing properties:  
  * `is_registered`  
  * `auth_method`  
  * `dnd`  
  * `email`  
* Also set:  
  * `first_name`  
  * `last_name`  
* Values should come from the authentication provider (Google, Apple, or Email).  
* 

**Actual:**

* The current identify call only sets `is_registered`, `auth_method`, `dnd`, and `email`. `first_name` and `last_name` are never populated during sign-in.

### **26\. Reset `dnd` when a deleted user signs in on Inc42 Web or DataLabs**

**Expected:**

* When a user who previously deleted their account signs in again on any platform, the existing `identify` / `setPersonProperties` call should reset the `dnd` person property to `false`.  
* This behavior should be consistent across:  
  * Inc42 App  
  * Inc42 Website  
  * DataLabs

**Actual:**

* `dnd` is reset to `false` only when a deleted user signs in on the Inc42 App. The same update does not occur when they sign in on the Inc42 Website or DataLabs.

# Events Sheet — Consolidated Change List

# **Events Sheet — Consolidated Change List**

---

# **A. Event fixes (build is wrong; spec/sheet unchanged)**

## **1\. `brief_page_opened` — `source`**

**Expected**

* `source` reflects the true origin:  
  * `organic`  
  * `brief`  
  * `profile`  
  * `streak`  
  * `explore`  
  * `watchlist`  
  * `deeplink`  
  * `push`

**Actual**

* `source` is incorrect or not populated with the actual entry point.

**Fix**

* Populate `source` from the actual entry point.

---

## **2\. `streak_milestone_viewed` — Day 1 milestone**

**Expected**

* Fires for every milestone.  
* `milestone_day` \= `1` / `7` / `30` / `100`

**Actual**

* Does not fire for the Day 1 milestone.

**Fix**

* Ensure the event also fires for the Day 1 milestone.

---

## **3\. `profile_section_viewed` — `section` enum**

**Expected**

* `section` enum:  
  * `funding`  
  * `financial_overview`  
  * `corporate_activity`  
  * `key_people`  
  * `recent_activity`

**Actual**

* Working correctly, but an extra `overview` section is being sent.

**Fix**

* Remove `overview` from the enum.

# **B. Event restructures**

## **5\. `watchlist_entity_removed` — undo the split**

**Expected**

* A single `watchlist_entity_removed` event with:  
  * `entity_type` \= `company` / `sector`

**Actual**

* The build ships two separate events:  
  * `company_untracked`  
  * `sector_untracked`

**Fix**

* Collapse both back into `watchlist_entity_removed`.  
* (Add/remove remain separate events as defined in the sheet. This only reverses the unnecessary split.)

---

## **6\. `story_shared` — split into two events**

**Expected**

A complete share funnel:

### **`share_initiated` (new)**

* Fires on share icon tap.  
* Properties:  
  * `story_id`  
  * `source` (`brief_card` / `article_reader`)  
  * Story group

### **`story_shared` (existing)**

* Fires on share sheet completion.  
* Properties:  
  * `story_id`  
  * `channel` (`whatsapp` / `twitter` / `linkedin` / `email` / `link`)  
  * `source`  
  * Story group

**Actual**

* `channel` is captured when the share icon is tapped, before the share sheet callback returns.  
* Share intent and successful share completion cannot be distinguished.

**Fix**

* Split into the two events above.

**Unlocks**

* Share completion rate \= `story_shared ÷ share_initiated`

---

## **7\. Redefine `watchlist_count` \+ fire Identify on save/unsave**

**Expected**

* `watchlist_count` \= total of:  
  * tracked companies  
  * tracked sectors/industries  
  * saved articles  
* Updated via `identify()` on:  
  * `watchlist_entity_added`  
  * `watchlist_entity_removed`  
  * `story_saved`  
  * `story_unsaved`

**Actual**

* `story_saved` and `story_unsaved` do not perform an `Identify`, so saved articles never update `watchlist_count`.

**Fix**

* Add `watchlist_count` to the **Person Property to Update** cell.  
* Set **Identify ✓** on:  
  * `story_saved`  
  * `story_unsaved`

---

# **C. New events (not yet implemented)**

## **8\. `sign_in_prompt_shown`**

**Expected**  
Fires whenever an anonymous user encounters a sign-in wall.

Triggers:

* Track company  
* Track sector  
* Save article  
* Profile  
* Brief card

**Group**

* Auth

**Property Group**

* Super only

**Property**

* `source`  
  * `track_company`  
  * `track_sector`  
  * `save_article`  
  * `profile`  
  * `brief_card`

**Actual**

* Event does not exist.

**Fix**

* Add the event..

---

## **9\. `walkthrough` (First-Open Virtual Tour)**

**Expected**

* A single consolidated onboarding state-machine event.  
* Fires on:  
  * Next  
  * Skip  
  * Done  
* Across all three walkthrough steps.

**Properties**

* `status`  
  * `next`  
  * `skip_tour`  
  * `done`  
* `step_name`  
* `step_number` (`1–3`)

**Person Property**

* `walkthrough_status`  
  * `completed`  
  * `skipped`

**Actual**

* Event does not exist.

**Note**

* `status` and `step_name` reuse existing dictionary enums.

---

## **10\. `app_installed`**

**Expected**

* Fires once on first app launch after installation.  
* Owns install-time person properties:  
  * `install_date`  
  * `attribution_source`  
  * `attribution_campaign`  
* `Identify ✓`

**Actual**

* These person properties are currently written on `app_opened`.

**Note**

* No additional event properties are required.  
* SDK already captures app version, device, and OS.  
* Attribution remains Singular's responsibility and should not be duplicated.

---

## **11\. `app_updated`**

**Expected**

* Fires whenever the app version changes.

**Property**

* `update_type`  
  * `forced`  
  * `voluntary`

**Actual**

* Property not implemented.

**Fix**

* Add `update_type`.  
* (App version is already provided by PostHog.)

---

# **D. Property changes**

## **12\. `deep_link_opened` — replace attribution with UTM parameters**

**Expected**  
Every deep link (app shares, Customer.io emails, WhatsApp communities, website banners, paid Google/Meta campaigns) is attributable through four UTM event properties:

* `utm_source`  
* `utm_medium`  
* `utm_campaign`  
* `utm_content`

Examples:

* `utm_source`  
  * `inc42_app`  
  * `customer_io`  
  * `whatsapp`  
* `utm_medium`  
  * `app_share`  
  * `email`  
  * `social`  
  * `cpc`  
* `utm_campaign`  
  * `article_share`  
* `utm_content`  
  * `article_reader`  
  * `brief_card`

For native app shares:

* `utm_source = inc42_app`  
* `utm_medium = app_share`

These remain fixed because native share sheets do not expose the true destination.

**Actual**

* The row still uses:  
  * `attribution_source`  
  * `attribution_campaign`  
* The implementation is inconsistent.

**Fix**

* Add the four UTM event properties.  
* Remove:  
  * `attribution_source`  
  * `attribution_campaign`  
    from this event.

These person properties now belong to `app_installed` (\#10).

---

## **13\. `app_opened` — remove Identify / person-property updates**

**Expected**

* `app_opened` should not update person properties.  
* `install_date`  
* `attribution_source`  
* `attribution_campaign`

should only be written on `app_installed`.

**Actual**

* `app_opened` currently performs an `Identify` and stamps `install_date`.

**Fix**

* Remove the Identify/person-property update from `app_opened`.

---

# **E. Identify-call & person-property changes**

## **14\. `email` as a Person property**

**Expected**

* `email` (string) lives in the Person property group and flows to both PostHog person properties and Customer.io attributes.  
* Send it as:  
  * `$email` in PostHog  
  * `email` attribute in Customer.io  
* Set via `identify()` on `sign_in_completed` only.  
* Since `sign_in_completed` fires on every successful authentication (new and returning users), sending it on registration as well would be redundant.

**Actual**

* `email` is not sent to either PostHog or Customer.io.

**Fix**

* Add `email` to the Person property group and Property Dictionary.  
* Add it to the **Person Property to Update** cell on `sign_in_completed`.

---

## **15\. Add Identify trigger**

**Expected**  
The following events update their respective person properties:

* `notification_settings_changed:`role, sector\_groups, topic\_groups   
* `preferences_updated:push_opt_in, push_types_enabled`

**Actual**

* Neither event performs an `Identify`.

**Fix**

* Add `Identify ✓` to both.

---

## **16\. DND / account-deletion suppression**

**Expected**  
`dnd` (bool) suppresses all Customer.io notifications while account deletion is pending.

Updates:

* `account_deleted`  
  * `Identify ✓`  
  * `dnd = true`  
* `sign_in_completed`  
  * `Identify ✓`  
  * `dnd = false`

**Actual**

* `dnd` exists in the property dictionary but is never updated.

**Fix**

* Wire the Identify updates above.

---

## **17\. Person-property updates must also run for anonymous users**

**Expected**  
For anonymous users, these events should still update person properties on the anonymous profile so they merge cleanly after `sign_in_completed`.

Applicable events:

* `app_installed`  
* `onboarding_completed`  
* `walkthrough`  
* `push_permission_granted`  
* `push_permission_denied`  
* `push_delivered`  
* `notification_settings_changed`  
* `preferences_updated`

**Actual**

* These updates are skipped until registration.  
* Anonymous profiles remain incomplete.

**Fix**

* Apply person-property updates on the anonymous path as well:  
  * PostHog → `$set` on the anonymous `distinct_id`  
  * Customer.io → update the anonymous profile using `anonymous_id`

**Dependency**

* Depends on fixing Item \#19, otherwise duplicate-profile issues remain.

---

## **18\. Person-property synchronization (PostHog \+ Customer.io)**

**Expected**  
Every person property defined in the tracking specification is reflected and kept up to date in both PostHog and Customer.io.

**Actual**

* Except `role, sector_groups, topic_groups nothing is being triggerd`

**Verify**

* `role`  
* `sector_groups`  
* `topic_groups`  
* `watchlist_count`  
* `tracked_sector_count`  
* `push_opt_in`  
* `push_types_enabled`  
* `is_registered`  
* `auth_method`  
* `registration_date`  
* `register_source`  
* `streak_current`  
* `streak_max`  
* `streak_tier`  
* `briefs_completed_total`  
* `last_brief_completed_at`  
* `last_brief_opened_at`  
* `install_date`  
* `attribution_source`  
* `attribution_campaign`  
* `interest_features`  
* `dnd`  
* `walkthrough_status`  
* `email`

---

# **F. Identity / merge bug (engineering — not a sheet edit)**

## **19\. Customer.io anonymous → login merge is broken (the big one)**

**Expected**

* On login, Customer.io merges the anonymous profile into the identified profile, preserving all pre-login history under a single user profile.

**Actual**

* Customer.io creates a new identified profile instead of merging.  
* Confirmed by two profiles sharing the same `anonymous_id` (`0bb78212…`) but different `cio_id`s (`6f70` vs `7a7b`).  
* The app writes `anonymous_id` as an attribute on the new profile but never performs Customer.io's merge operation.

**Impact**

* Pre-login history is stranded.  
* Duplicate Customer.io profiles are created.  
* Lifecycle and attribution data become orphaned.

**Scope**

* PostHog merges the same user correctly, so identity capture is functioning there.  
* The issue is isolated to the Customer.io identify-at-login flow.  
* (Related to `sign_in_completed`, which is already flagged in the status column.)

* 

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMwAAAC0CAYAAADYU8NeAABYMUlEQVR4Xu1dB3wURfv2K/+vWAHpkF5odooogij2ghWxoaLSOySk0KsVwYKCgtgV+MBe6CBI7733FlqSu9xdyiXP/33e2T0ul6CJHdkX3t/szc7Ozs6+z7xlZjZnlS9/Lhx22OGS8VmhGQ477PCp2QGMww6Xgn8SMBkZGUhI6IaCgoJC+U2bXl3o93PPDceIEc/j6NGjRepw2GGbs7N9uOaa+khN7Y1+/ZKLnCfHx0dg+/ZteOGFZ+Hz+USmjuCKK+oUKvNjFFqfzXfffVux5xs3biD3DC+SXxz/JGDIderEYtmyJYHfq1evRHp6urLL5SpUNhRYDjsczARMkyZX4vHHH8KYMaOLnCe/8spLmubn52t61123onr18kXKkdetW/uTQAml0PMEzMGDB4vkF8clAozDDjts2AGMww6Xgh3AOOxwKdgBjMMOl4IdwDjscCn4dwNMg/oXOfwn5vr1CodtHS6ef3PAhL4Yh//8HPoOHT7JPwmYCeNfwcG9GwK/b76psf6OjKxUpGwoh76I2dOnok9KVzRudEWRc6cr79y2skjeH8VzZk4qklcct7jvVjRpXK9IfjCHvsuf4mAZ+TV48YLviuTZ/Gvea/f2VahcuUyR/FPxTwLm6ace0vSaRnUDzN8laXToSwjloYOScGDP+iL5ZNbP9Pln+gXyVi6bEzjeu3MNViyZqbx5/eJA+dDrySNHDNZ0w5ofNB08sHeRMjx+/53Rgd9fffFRIP8aAfgzQ1OK3INsA8Y+Z6frVy8oXG7rikB716ycZ9IVc3H3XTcGyrz2yrOFrrnzjmaFfvdJ7hqof8a3/wvkz/juf4UAcN+9N6PF/bcEfn8/ZwoaX3NykOJ5ll+66OtC9Qdz6LsM5abXNsDsGZ8GmO06+XtqkfKl5flzv9SUfd/q0ftUsO+5+2ZUqHBeiWSvpMy62j5tZLwk/JOAafPUw5rajQxNf4xDX0IoP9m6JZaL4ITml5T7pnbHjTc0Cvx+4vEW8vAPB343vPISDB2cVOS60Dqua3plkfxT8S03N0FSQsdCeQ0bXFykXHE8aECCCG7dwO9nhqYGjm+ynqOJnB/x/IBC1416aUiRun4u9+/brdDvrp2fKFLmsktrFHmXP8UlkYfS8Knq+y0AM/7NkUXyT8U/CZhfypdcHFvkhTj85+WqVcsVeYcOn+TfHDDBHPpyHP5zcN0rahV5Vw4Xz78rYBx2+HRnBzAOO1wKPisnJwcOO+xwydgBjMMOl4IdwDj8l2Lu0AzN+zX5ZwPmrLPOQmZmZpH8YN5Q9vK/BIc+11+Rjxw5UiSvJJydnY2vv/5a0+I4tPypmGUvvvjiIvlRUVFF8n6KH3vsMVx++eW44oorivBDDz1UpHxpuFSA6d27twIlNP9UHCp4pNBj5BeYfaP5+YF8m/JdWZrmbN+j5+zfpI0V62vK/AMd+uFAl0HIPZAWOF/cvYPzszft0N8Ffj8KsnOwrd5dRcrYHPpcfwV+7bXXNKUAnX/++bjgggvwn//8p0i5n+JLLrlE08qVKwdAwm3rHo/nDwHM3r17i+QFM+/D71SE5peUSwUYvUAA43a7i+QXx6GCZwtjzo69KPBlB/L8x9ID5wJpQQH2tOxaOE8oP8sb+G3npX/4+cm6Mlx6bXH3tY8PdB2sKcGiqQAm87MZyDtyHAW5edhQvm6h60Of63Tnf/7zn7jooosUKJdddpnmfffdd0XK/RgfOHBAAXbeeecFuHz58ti5cye8Xq8K5fLly4tcdyr+tQDDdgUDNVTjsW0EdOh1JeVSA8bm3bt3F8kL5WChO5059Ln+arx9+3b8+9//RsOGDYuc+z3Y1kYETI0aNTBv3jwsWbIE0dHROPvss4uU/ykurTlYGv7ZgHHY4TORHcA47HAp2AGMww6Xgs9Sr/dXJgYGbrzxRj2mDeq3nOtTEctPmTIlNLtENHr0aL3+96RatWqV6p7Vq1cPzSqWUlJSCtV78803F3sfRqbsfDreZcuWDSnh0KmoV69exfZpSalUVwbf6NxzzRcFCQbOx5AYWrTJBsysWbMCeYzEkEIbTKfPBswtt9yiaUJCgs4NkP71r39pal/XpUsXTW269NJLNWVbbHC2adNGv8zJ6A2/oPjBBx8E2peYmKipXd+mTZswZ84cPQ4W7s8//1zTYOG0KfQZ7N+ck7CP//GPf2g6bty4IuVI9vlGjRoF8uzzL7zwArZu3Voo78svvyxSjhQKmOBz9vHUqVOL5HG+gvR///d/hc5deeWVgd9z584NHDOyZpNdx6uvvhrIC23Hk08+GTi2+47vku/jwgsvDJyLiIjQlPnPPvusRtpsuvbaazU9dOhQII9k358Tlbm5uXpsv1cS5YCOP2nEiBGYP38+tmzZgpdeeilQ5udQ4bf+ExT8ImzAkI4dO6apLdikUMDs27cPO3aYuY9QYQsGTOvWrTX929/+FugIu97vv/9e0ypVqmhqkw0YAuzw4cN6fM011wTOM/LCbz6TeG++GPs4lIIBExkZGXSmeEEMJuaFCjnpVICxjytUqFAkrzjA2M8fnEcKFdTi7rFgwYJAXtWqVTVlZMwuw3dgU9OmTQPHwXVVqlSpSH4wYGJjYwPHpBYtWuigFUz2Pfl+bbIBQwHnlMWyZcsCgyXDyqRTAcaWkeA8EsPaS5cu1eP7779fgfW7A8Yhh35topCT09JOTjr/mckBjEMOlYJ+FmD4hf4/C/2Z2vJLiDPQfxXKyy/Apn2FTbGfQxlZOVi+zZhmP0ZlWk5Abp4xs3+N+/4YlRgwtCGpOrmsgmvKSPxt+wbdunXTmdr//ve/+ps+BP0Y2648ceIE6tSpU8jOZFQomB555BGEhYXh73//u/6mk9mkSZOA2rbBsW3bNvVrWO71118PrgL16tVTH4fLPlie1zVu3DjQ/kmTJhVqA21p/qaNP3HiRK2TdjODAHRU+Uwk2uL0hfh8tJvt+mjXM73zzjsDddIWZxtYT/PmzfU8fQSyfW/2I+/F33l5eYFnJE+bNg179uwJlKUzG3x+9erVmk+Q1axZs9DzkMqUKaP3pg1vn2vXrl2R56azv2LFCv0dWgefsVy5cppv+3wMUrB/g8tm+fLw9zvHBviCByZgyZY0PSZtO5gROFez/Seax+PWo+YE8kkb9p4I/I5r+7HmhT3xfuC8Te1emxcol53rx7UpX+jxrNX79Xxo+V+bSgwYLs6zyQYMXyQB0759e40OFUfBjmUohQLGDiQEl7UdUArQ7Nmz9TjYMQ8FTHx8vKbBdVCAqlWrFvjNsDCJyy9sp5HCQapYsWKgHMkGTHB99nFxeTbZUTebuH6JZA8opFNdbx+npqYWyQs+Dr2nTQMHDgwcd+zYMXD8Y9eF5tn9SNq4cWPgmOAJLXvhQxMwfdW+wO9gwAQLcHDe/mNmIS2Pdx52adqw16c4eMITKBcKmAY9pwZ+HzieVai+Px1gHHKoOKKA3jd8mmqIf931Vujpvxw5gHHIoVKQAxiHHCoFlRowdPJCKd9yxnP9+TjhNrOrJDplOVb0gsRSbu/JiSaS25dbbKQreCLNJnvm1ibbL7ApK+vkBrOSEu9DPya07mAK9gNOtcyHtj0n3Wz6saiXvTLiVBRcD8nuC/4dRpvYXnumnmT7FaH9xvVPpyI+S6g/YueT7KBJSYj3Le49/tg7CX1/vN6ug214+eWXiz1H4jsL/l3Sdv5SKvFdaKuO+tz8AU4es62T5u8o5GRd1HFSsc6e/TvyyQ8DTPrvveM0P7QsHfQGDRookyiMjCoxSmUvm7jtttu0k7766iu8//77gfL2NaEUExMT6FQ69nY5GzCk4hxrkg0YBg/se3Am2Sa+3OBVDldddZVG+4LrYNCCNHLkSI1QMXpGOtU9n3jiiUAen7E4gSgOMCQGRyhMDG4U1yenuqcN5OAZ++DzjMiR7OVLJD6XHdUk2eVPdQ8Sl6rYZC+3YcTObiuflxQMmOA6+O5D80Pv8VtRie8SDJiS0rfL92oExCbGyt+evjnwO9ObgwkzT/7+NYlLS/4KZC8xIv1eQvFjNGDAgNCsUlMwYE43KtEb4GjFUf63Zocc+rNTiQDjkEMOGfrDAVOco/hHULBzGryStrS0cOHC0Ky/NAVvefg59GcwM0tDJW4tN95QuL/99ttAHh/2VM5dcc5YcXnBs8jMD96LcSoqrh6SvarAph49egSOuZykdu3aesyPPdi0ePFiTYMBU1ybSZMnT9aUX1oh2asAbPrss88Cy+iDrwveFxJMofkMTNhE34VbIoIp9Ll5PZe2TJgwQd+NvVoheKafFNwWOwBgb7UgFfe8TO3IFD94QuLSJhKXytsmdOg7YISvuG0Axd0j+JhbHOz73XTTTZpn9/OfiQo/7Y9Qs2bNNFJlr9FiJIuhTa6p4hojhlH58NwYxE1bu3bt0usef/zxwNouEq9lOa7pIjHaxGU33KPBfHaSPcIHdyxfEH8zwsX0+uuvD9TF6BU3CNnX8Pddd5nvjPE362aEjfTRRx/pC+VLt8/z/gQXR0t7XRc1BT8TxGNGwbiZrGXLlnoNv2YyduxYPXfrrbdqHonRNkbLuFOSxH7hsw8bNixQhsTruJmNkTJ+miiY1qxZo8tngvuA7Q/VejZ4SXy2c845J7ARjMuJbNAwFM06uE/o3XffDQgzl9288847eszzBCcBb/c5997wfbMv2ferVq0KbPoaNGiQgtS+NvQZ+ME8tpm7bUn2Gjp7sOVGOPY162f+W2+9pV+Ksd8d+4B9z7Zy3WD37t0Ddf3RVGLAOOSQQw5gHHKoVOQAxiGHSkEOYBxyqBTkAMYhh0pBDmAccqgUdBbDqw477HDJ2AGMww6Xgh3AOOxwKdgBzC9kfkWFM/Y85pYCO59fbwwty4982Mf8PK19/MADD2jKJTtM+fVPptyfYpfhsvrgurjfhinvP3ToUP1DQsHnuZKCXyQNzuNqjODfDpeeHcD8Ak5KSgoccykQv5zDpUBc6hFalsxzNnMpip3PjVJMueSE6ZtvvqnpF198oZ9cCr02tF4uaSE4gs9zjVxoOYd/OTuAcdjhUrADGIcdLgX/oYA5MrwesvpHwZMci6xBsfD0jYFngMV9Jb9/JDyp0fD0Ex4YhayB0Safv3mdnPcOiBJmmVjN90oZ74BI+AZF6bFvuORLGV6X1S9Sy2T1k+O+kg6Wcyw3wCqTFANXqpxLidT6s3jcNxbeYVLn0FjTBmlPVv8ISaWNKZIv5bxSlzs1Uo+zkni9/O4TJXkxyEqWcsK8n1vys5LipC3Rms86mO/pHQd3b/6OlLZJ3XzGRF4vdSVHwt03XPpBjvtEKnv6RmifsV4381ieqZRxp0QIx8DLeyUL95J2JUjdcg9XsrQ1MVqfM6u3XJ8k5xOk3t7RJ7mX1NVDzncX5nWJbIs55+4mz5Ig9+kh13SPk/rroGDrPORvngX/+tmFOJ+8YSby1wlvnAn/WimzYTYK1tk8y7CcK2C5DTPkmhma+tdNt1LzO3+tnF8v5VbPxL7vvykiR78n/7GAef5KI/RDa4rgiiD1Iwt4BlKoouBLiVPh9PQTARBh8ggQsobICx8iL5JAGUjwUIAIpFgFTlZfI3TeIbEq9F4CYpABVxZTBWKMKdM/Xo6Zyv36UDgpcJaQyG+vgMPbJ07uE4PsgdIugo2CPkiEeGC4XmuEV8oO5jEBEKkAIrA8faQNfSS1wOWmAPeRZ+H9mSeC6xHB9fI5k4WlLp73EDQExgACPMI8hzynd6A8Q4oFHLaT4O3D/pFzg5gXqffzpsh9U6W+pEit3802SZ6CuA+vi9LfCkYBFFMFi9TtJlB7ybUJZJYhwAiYKO2XrG7yW65xd41D9kt3CQjmwL9JALGOIJmjrMfkjbMUMASEf80sBU2ecD6P15FnG8Csn2WAEcwEjQUgBQyBt3oW9p/JgEkbWg8eGbkp+KoNKNDy4ikcOtqmEBAUcgMC1UD9WF7SQfJ7AEd4YWoKAoGA6m20iGcI6xNh70/gUIg58hIEppwK32ACS1JqMgKP96MwUguIYPmoHUTIVLNQgPsYgddjCq6AwJNCYWQbYxWYZrS3tCKvlXpVC1BICQAKL58vJdzUk8rnMpqEz+xmfXI/NwHUh8fShkSjDViW59neLGoJtoft5m/mK0jZ1ggFvwJfwRClGspLALEfZQBS7ZPMe/NZjAbyEiCJorUS5Rphby+prye1TrwBFOvrFaFay9Vd2tgtCgWbZwIi8ASNahpJCYI8gmjDLEx5/WPsqFUb+wYNwP6mzbDptuaYO2WKARHBYrPUUbD9B7R+4C4ktX0MXR9rKUCxtA6Z2kZ4/w9fFZGj35P/WMAMq6+jtUc1igGDgoNCSeFXc8wa7VVDGBPMM5imF00h/hYeRhOOI6gZmSlECoKhMSrECkQp6xJzyUUzqp/ROlmDJRUtQEHVUVxNNzHnEgksEU4Kmphr1G4KPLYlhdqCqQEeNYwKO0d6NRPZFiPEnv7UfEYos3is52KN1qRWSYzT+1MDqMZIYB0EBoHGAYGA4mDC5ycQCFi20TL3qI1ofg429yMQ1bSUtmcRZOyPJIJGrk2NRaaAys1zBLqAx0vQ6MBk2k9QeGhuUcOoeWa0rWodNd2k/p5yTLOTQOoRjex32iF/0w8GMBtnK0gInHwBEvNe6j0BH7/0EWZ/OAV7Z32D7bNn4phooQJqnzXGJFNzS1Jsnovbb7wBiW0fEcDcf1LD2BpnzUzsn38ma5jnrhTzKxLZg2sZYaL2oMkiqS+5CjzDGiDnywHI+2YQsr9OhS+1IjzvPoy83QuQdegQPCeOwjO5iwgQbXzjT7iTjdATSAqwIXJuCH9zZCWgKHgsQ3BSOOVcqjnWfNVgBJ2U7xMuoIw1I7CW5wgtphUFhiYKhY1gs7SWtkGFVgRpaJRqKQWAgM3LUZ2mZX/6NwSSHA+IN+aammmxBuwCPg/NSb2XAYKbPhfNKTW5pL3UTCLs7l4UeAMgPodH/BcvwSv+jbt3vILAy3PqOxGQxsSin0NAZcnzsZ4smlwCIJZRcPWI1bJuYQ8HDdsco/nGtAevF7+Lfo6wS/LzvhgGiI9CM0tNrTVzkL56Bo4JHxdBP7JiFo4tnw7Xqjk4vnw2MlYJSNYYk4w+Tub66di+9CscEHDsWjsNe+T3ruVfIW/NdPhXCWDWCMs1++edwYBJ3/I9sGMx8vcsQ8HeJSjYswj5+5ZjztXxmNO4BmZfUxNzr6mN6VeEoyBtJ2bVjcb0iyphbrOGchyBeXJ+jvCselHI321dv2Mh8iQtcG1FNkeojC3w75X6dy2RMpK/ayHyd/4g6WJgj+TtXQQwX69fKsdL9Hfubimzc6nkL4J/90JJhXexnLTXtQ3e1fKy07cgX+ot2Cn521mGdZh6C3Ytlfst1vL8DXk+/+6l8B9eDrC81vWDPLt1nvXyOr3XIu0X7FiibH6bNmibtbxpG+vADqtden6RdX/Wu1jrhTwz25W1V+5/aKXpC2mflrPup9fvkb6T0d+VEI6cacPh/24o/F8PQ+5XgwWc4ch+oxVy3hJ+8zHkjH9MgeXVAAC1TaQGDLzPXI/cma/Av3m2MdE2WFpkkzjxm4NMMIvzN85Q86xg7WzVOIatIAD9HQ0GCGhUy5zhJln65vkCEBGqHXyBIuwiSP4dIqgiHNMbxmB2oxqY26gWcjIzUcByIpB+eal+nxuzryaYamBW/XD4XUeBbUagtjyfgDkN47Gm831Y0+sJzGoQg1lXxWHBbVdhplyztmsrLLqnCVa3v1fqr4XVnVpg3g31sfiRW6RcDI5+NQFrOj6I1d0expymdbC6a0tsGd5NALEYO19MkbprYFWnB7CuRyvMlvus7nQ/Fj92KxbcXF/yW+KH267EqnZyb6l3ZqM4rGx3Lxa1uA6bBnbEuk6PYO6VsVjTrRVWd2whwrtenmcxVj9xD1Z1fEjqegizrDpXd5Y2dHkIs6+K1fuxTfMa1zL50vbVnaV85weU51xVA/OurY3lbe6V/pJ+uboWlj52B1Y+dbf2RaaAe3W7+/WZZjeIk3pbYmWb+xQkBjBMCWIDcA4srmHXIHvMw8j9bjD83wpwvhsiJm5DeIc2gnf8w/CNexzZbz0m2q2+mHGijQQ07u6RJu0ar9qHPo7v7fbIm/2a+DTUPLMUGAXivCsYCA6ChcAJdfqDeS0DB0xnnNkaJkMAUyCjno7kHPEInD0cwY+K5qglXAdL2j2IvKP7MS3+QswSgaHmmdlANI7vBPIPyGh5YLXRLhzh9y7GzPpROLFsJhbefTVmXRmDnS/3x/LWd8Al6n9WvTjsePslzLwiEtMvroZDU0bj2Lxp8G77XsFTcGgFfBvnYomAZ4ZosDlyv+2vDISbL2v7EgFpDeRunY/5N16KOfWjsXlIZyx7srncU8DduDaOL/gU829pgJmXhwmoD8pgsAIzRPsR5NNqVcbOt15B2uQx0n4ZlTny7pBnPrgeWwe1F2DHYXHLa3Hi+y/x/XWXY/ql4fjhjoY4+MU4yb9O2hyB+c2vgXfTfHwndfkzNqLg2FrMlmf8Jq4clj99J6ZdEoZ9U16XtAqWPd4c0+pUQp604ficifi+6cWYI2WXPXIzjs75SDVOACgBDWoA5N++SEAQIUB5HnlfPyMm8RDki8bxJIXD92YrZI8THv84fK+3grtHuLA8TzdGzgQsXcQstc22XgSRcOdYuLqISdk+Di6CqYP4U0/LdZ1qw/Pqo8j9fAjyFr6NnGVTRRMxujZbUxM4MBrG+DFnuA9Dk6xgn5gle2lKLFaTKF9MiumXV8McaoYGkSjIPoLpl1RSwZgjo/PqhLbY+tYIHBFBP/L9NOSlH1DTBzSNODoGTCzLNKFQ7FpgTCCCkSlNlF0sFzLC7uQ1HGFZnzmfn7ZazbT8nUYLUsvlq4nDsrz2B6P9tP1LFLR6jmXUnJNrpE1slzG52MaFCiKaaTxnTKeFek816XSUNyaVEWxe/4Nei73m2QLageZnIbbMLOlLc2zKap3afmPWYc8P2ka9B+unht+7XPyRivALOHK/GQb/N0MFMKJZelaF94UbxAwTraKAeQyu3mHw0IfqGSGAidT5HA8DAzzuyaCAMdHo9xitE2VAw+haJ5YT36czWX53kHoEaFmdhDua1N1eyreTcm2kTFsp0zZafkdjW9LNReTo9+Q/FDBHXrwKviFmzoUOrka3xCH1iFPt5hyLRn7oIEsnMqpkOdqevnHGkWUYVifyLGeUYVM66HT85djdm5EfE+XJ6i0OLaNAyQwQ8D7G4We0i+c5UaiTenzBGlblMZ1ejpLmHEOtOpkp12VqWJb1RWtbOHLqXAvbxYgZo199rNAxQ9Cp0WZyUwMDDAREmnDvANNGhqc1IMG2MfjAyVxG5FgPnzMhJhBc0OAAAxNWqNujc0UmumZC1ewTUyeDIF72pwizlwLMAAmDB3zu1DBkMRjCezJqRuef5hX7TPqBk5QMArgZSFBAmKiZpxdD3XK/nnT6TZhZ+11A4hYgsA8VOKppYjWalkWwkHsQOLw22gQMJM/VUTRQJynXMQ6ZnePgbieaqJ2ceyoervYEipRpI6mAaEfyGQyYQ8/U0wk3b3KcAKeGBQoKvJmE9AykQDCkaoTQhG4JLAokhY6Rr0id1fYwapNMgeTvKBV4BRjDo5yd1llthlXNOZ0jSYrRGXZPIiNIFMooIwQ6mcdRMkIjRJrfmxOXkfqSvQmsm2Ch0BNI8kIpXD3jdHTlBKXOrTAKpbP5FGL+jtFIFAUyK0nAmBgvz0wBNRONFDo9xz6g4A+wAETQEtD2xCuBoMDk70gTTWOUjpE0hrFTpa3dGeWK1sHHBraGyTkhydC6zjGZazk3ZSYmWYaCHm1pC7utbAMHFQ4SkSZqJiDgYML7sJzO33QzQPH0jDXlCTABCLULy7u7iD/VVt5TZ3nurnGGO0erxnF1kDLUNtQ+1DLCmW1NvoLnSSn3VDS2J9xeRI5+T/5DAXNkSH0dQb2cdR8UrZOWKigEBdOBDAcbodAZfM559JLRh3MJFAQKX7KZV9HRX0Dh1rkDCo8RdhV+jnCJRsPoCCnCQIHjyMxrjPaI0mgPzQzVMBwZKbi9DAA0jyO0aiv5TXDQdheAUQPpMe9HcFEYOYKrsEUb7WGDmPMibGeC0ThZfBaW40jPugkGCptqIF4bZULBLMdJUAq3NUtPwOjSIM4lETC8D3+zXHLESQ3M+rlspo+lPXVAouaJtAYWLs1he2P1GV0KGvtZo8wARK3VkxOYPMfJTdOPHppe7E/VJuYaL/uZ2qYn+5PXsT9ZVrQEza1uUabPuko9Yma5OxrO6izXdIxSTZIlfo4xxaKQKWVcbaWsgGd76i1F5Oj35D8UMGmDuJYsApkMRw7m/AtfTIxOqHEZB+czPAIkCgpnvHWCjULLEZ4aQIUuwozgFESCJMlaR8URklojkS8uwgiKjnocRY2GUKbwWoLhSaA9Hm1eMK/rRuE0Ak6toiabLSQW+BgZUkGhQCiITdt0riaJy3uMiWlMIGlnXzNXouYVTSvVJlE6v6OTnZwLIcgIGNZPUBFMauZR2KlpqWEitT90yQz7jtqYQOU9VJuZcgHgcYJXV01EmxUHvJeuMIgybdG5J9NObROZ/ayrGNhnkapptD1qtrIf+NyWNmJbqWHYH915LlrXpOkAxOhZt2jNd1GjyLG7gwCgC00xAifWaJkuxuzKbB+pQCGYXG3kvPgvWTwWDbMj6QwGzOGhdeGRl+0ZGG/Z9WYZiy+Z5gmFlYCJMy+SWogCw3wVHJPypetoSRuatrkCIdI4o1JW16DJi/VyFKTJxkWLXF9FgaYpxtGXJoSAIHvmWLz14IPoW6cm+tSMwYZZM8TUoqlozEaaYLzWRQ3GZSMED81COr+WJvPwHCf81JcS32JUc4y+914kRYejb82ayEo7jpQ6NdBPjr3HM81ozNGdWoMagb4RVwPoigdLsLneTRd+Rpp+6RumWoez9+wjHwGgKyMo8OwTmmVcl8dJTvYLzTCrL9TnoVajGWiBytI+XEmgJp/6jNb9LRPQ9DnbRq0VrhpalxnR11ITLVZXCWiIWQCQ1S3ODCzU0N1s00w0lJhl7i41VJO4O4hmo8YRELm6RBrzjCYYHf725thoHOnz9jEKom3JtxaRo9+T/1DAcC2Z2tP9qRUEOEy5CJOz/hQUmmP9jKBT41Bg6NtQq1CIbAdXtQMXRVomjK7t4nU6800BEPC81hxDr66H1Frx6FcjHonVKwtXQz/+rhmPXmFVlBPCqglXQW9JCZqU2AikXn4JvBkupEq53pHhSI2PFuGPQ36+H89f1wR9pY6EsKrwp+1D/tGd6FWtMhKqs64qSAwLk7IxWm9iOOuMkzqqY9PcuSJc1cV5b4CFH36IfvHxUo4cK9dXgm9KqjFF1SGvgk8H9kefGnJtRHX0l/Z3Kl8e+ZlHkTP/DXQtf4G2h9eyzX3j45Cd6dblONmfpqJL+TLavp5hlfW52C62r3dEGPrUkjqlXb3CKmlen1qxpg1hpn96C/P52E+J1fk8lYSryAAQoc+SGB6GnUuXCEDCrMiYvBOuANBIWbSGmql1GClz0QTrSN9FQNOJYGGYWc53iUEmI2WdeN5EwwLahX5NuziNpNEs2550WxE5+j35jwXMoPpmsSLNLS7L50JDXUrCkY4OPc8Z4acW0SX5XLrOlI4uTRmO0AQL7XmOvlwCQpBYI7dZ1Cj1MUo1uCa6ViiHviJ43u/Hy4usiN5R4ehW4ULkbpiGzMOHkFojVjgG3SWvuwjau507wjfybix69x388M5b+CQlEamxAphaNeD35+EFAQy1h6DHmIGitbJXfIkJ7dshSQQxKSZSgBaLFCmTHBWlgr1h1iw1cdzS1rxju5F/bC/8x/cg5/AWEV4RYgGk/+h29W9oXua6jopwxuK9dm1FqKshJT4KiQKwnKO7BTBj0E3a2V/A1kfazXt1qyRgys2BLzVc2+Nb/AGSJZ/P3b18OQXA++3ay7OHIVkEv1+NGti9cgXy5o1HQriAQQCdt3EGcv252LZwgYKod2Q1zB3zhg4uCTIIpNQguAWYbgFmj3DRslHGNFN/JdryW+gDRpitAjaABBzUPuq3dGaggExgERwEjwCjQ6SAhlqFDr/lv7QhiGKxo88ZHCU7LD4M96P4BoiqHkjnnyHmWP2tGsZamey19si41EwzGkUjOWqKyTHDnBpJoxAa+1/9CZonjJDRR+lDsyoKOQe3Y8zDD4qA1UK/uFoiiPECjgrIXfUFvhg4WH+/2vwOrJ0xUwRMNEOVavB9+SyG1q0vQImCP/0IDqxbI0IVDtexI6JhGqvQoSDfmHbdI7BhxgwV8Mm9EvHynberQPr3LIPr8BE1xdbPnCWAFsFJiofr1ftxfNce0QrxSIqLQp4nGxkz3kR+dhZysjKR48lUTZYswOtRpSJ8c17Tr+n3q1kDwxrIgDNvNLpUrICelSvBu3UR0g8e0HPPN20qZk4ZNZH8Rw8oEHtXqY4ctxd5uT7RhtskzcGRbVu1rYMbXIHcea+jl2iwJAFH3vpZmDf+LdVYHEg8z1yNLfPn60CRGFEVfeJiFHjZ6S41u8weGoJE3hkXfnK/DKN0PCfH3A6gvgq1C82yzrEaLeNEp+6zoenGOhh27mCcfwJI527o3xA0beOxPeUM9mGODKings2Fib5na6rtrKt0uaeD8xNc/cu9HZxj0L0oxulU55a/1WbnXhna5THGidVjEWaChftjNBJF0y0ceUc2I233LqQfOIA8GdE93SvDf3AD/Ps3IXvRO+CCRIaZvVLW995T2DRnDjbNmgnPhMd1XsczbRRyjx1E7pFdyHj1PhGipnL9JvgPCO/fYJxkLn2ng8vIXNcweLqGqwZ0izbz79+MvH2b9J5eGXE1WrbuO2St+QqeNd8ia/U38Kz7RtJvkSf1+bXsJuQs/QjeHmHwzn9d2n0IuUf3IvPFm1TDalSOTv6kXsg7vFWu2YDMQVfoambOuOuoz+iXaBpXt4pwDaprhaSFtZz4aInVtO+z54ySZ9mo981Z+ak49vRFqsO/axVy0w8hb9cyZHWsCHevMFPu4EbtO3dPo8nUj+N8EX04hpQ5aFGDWBOYCirOvxAg1jwMTTVNu4lGYfSM8zBMdQJT2swJT2oZ+jDi7+xIOYN9mMP96kMnIOnwW7so1UTjPhcKO5e1M1LGFb7sfIaVdSm80SL64tW5pkah/2Kceg0MUBj7hgeiVmaZO+cmeMwXR7+I4Is2DjDr5DGFjAJuhZK9dGLpF2nkKNrMsehiQ46I0eYl06RgOLuXNUejUTyaJbyPMUm4stjNMC7L8VqtgyMwyxk28x7RVuTNmDEawSNYaVoyGkjn254H4nNaA4I+k0bkoo3WZd/w2RkW1v6JOxkosSZbzSrmKOPMawSMgw3rjDKCbZlZwVFFjTKynDr50RqKZzs5yavlLK1CUDDkriYaJ067cHWzVd7qM25G01UALKuTmPRzopTdHSWPfgvNMmochpnbiQ9zJptkacPrmXAml7encm6AoWVjlqkPw3wreqN+CgVMBZmjKkPNJoKlwsJwrPg1/qzjAYc9UZxa3/qvjAlHoaJgUFhU4GgyxBpwWIKjWwO4i5GC/eaTeOHmG9QE6RMjppk48r2qVUVKVIT6CT0rVYA/M01eOkPWFGwj/CpkOqLKi6YgKTgi1STRNVec3+nGMKrcv1OsEYxunNMxQPJwL0p3MwJ7ulVV3yJZ/KzUuDgNJtAspI/1Qfee8EwdphFAnesgsHitgIUAJzjdSZy3MmDV/UY9GemLNvuGCMbUMOTMfln8ljAkRUUiZ8WnZs6Gk7nsb84JqWlr5rR0L0yPSGuXpulzzrWodqFm4TN0kXfgPiE+TrT4YuIPiilJHyjPk6Pr07y9jLOvfUDzjCsCuAaNS2asKJmZlzGTlmqytYm1JjHjse1MnulPG1ZPfRPjo0Rp6FQjY9QqfFkc6Rjy1BCq5CfRtCDzN6+LQr7HhV5hVdWPoPOdEh0pKZ3ZcHG4GcmJQW85d2jdetEMVeVFVRFH1SV2ugi+vNTeAoAcbxZyD23VyA+ZApoSF6vASJa6kA+k1rkIqfExSBaB9WSm49sXnrfOR+q9eb+TbNpyMt/87iTOeeZdZbDy0ylB10VYbeZxdassOUwDBX1qxIrgxZg2adskPzJK/YeUGny24PuxHtYRfO9Ivc4+b9/TsP3b7jNz33daPyEgqYORd94aaMvJvrXawf4NuvdJlueJY/AhTsskxjCcXkMDDj2rVpV3eZkODBz89FsD9DHVJBNgdBUgM9Tc3tI+BE5bDi6MnMWoibajzxlskqUNr28mKwkYRrx0uQv9Dc5DMGzM0Z+jZYwZ4WhiMOqiSzSidFRzUdO81xHe9zsjJ+OAjMRRSIisCt/x/TiwYYO+uL1rVpuJNanD1b06MruEIT8vDx927SoOchz2yCju2b9Ww7rPNGoIV+tqmNi7pwIEOXkoEIe+R/Wq6ujPGjMGeTlebJkzS4XAnZEB38LJGNqovggx529i8fqD9ylQB9VvoPX3i68pDnY23I9UNMtCZIROf74F8nP82DpvHp69rokAIQLbFsxXoBII/kPbxVfZp1G74c2uQcajFTD/gwkqfNRySQx9R1YXx/hCeL4ZhV7RURa4RMhOyAh/yUUaNWMQ4/junXB1roKMvYf0+v0b1sM36CqNklEb5+cXqCZjiHnQFRfLaF/JOOHdw1CQm4+UCAPoRBH4/pfI/eUZ4Ydok/I4tnsP+kibu5Yti85lz0PXcmWQUL2y3Fe0/7GjyE/bjZ7VKqJ/3SvgeeF2qVMA0D7WmGJdrNUSNMe4ykI0jYcLMttTy9B34cSmMcfcbWI0RL39zJ6HqSt+CickY1SbqAZRjSIASeFuROk0sb9ddFrVrIo2Di5NKJoiBFFvMQEyjuocySc9uyLfl4W8bJ8CYt+GdTp3sY+AEdOBjnZu+n50K18evWiCeLKQFFFdXzj/XibnFZ5p1ACux6tgYkIPnW9Bdq68+HSpJx6D6l0mdedg5Refyv1itG53ejo2zpmpwJycnIhsuX+KmE/8ne/3w5+bK2aJmHQRVeGdMUZNEc9LLdG7WnWdm8l3Z6pQJwsY3d+NUZOLYPMf3oa8Y/v0Hs9c3wSuPnXxZpsnkVqLgIrS+SA1dXI8WPzBu3pNbrYHvlVfY9fy5UjbtQueT5/HuMdaWcD3I/3gfh0U9q9fL35NffQOr4yUWBmgPh0uJlMGhjS4AiPuuVOAUEn9D8/YJ/Hc9ddJ26vLs+Rj/fTvxHQL03shN0+e/ajWt/rzzwWU+3QAOS4AMu2RgeHoMeQf2YmEKpUx+IoG8L1wq9EknOEXM9RFbUITr3OsmmXm4xpRulBTI2TUMFx8KaBxdYgxPsyZvDTm8OC68A6J0XkYnaSjU2n5IjrZqNtt6atY/oFGfGhf0zmk3RtrbP/OYotnuTH6/nvQ95LaWPjhB3A9dxeO7t6Fsa0ewuHt2+BKCLOcTtri4cga3RJZqz+H6/0e4myKWXZsD8Y9+ije69IZmY9Xx6w3xmDsI4+iQIDnZVSnE0fceBxLvhLuJ8tg16rlGPvYw/CkZ4qpIC+6bWX4Pn8Wrrc7YsmkSXhL6irI9cE1/GZkdq+hS0HU37FW6Ga2D0fGgGuRM/d9ueZpEZhIZHauijcefRhjWj1oACNa8q3HHsUHCT3hfvE6vNL8LgFJPAbWrYfESDPpmicA5bcKsmaOhE9MRW9mJlw9KiJ3w0zRNMeQl3VC+qiamQM5koa3Wj2Cozt2iNBWQnqPygLYdBzcsBGHN29F7vF98pxVzWJMXTdntTfxEngXf4iszwdixptjpI5HARSYgEH3KvC8eAc8ox8RrSAmV89qAqzp0u6HxHTNhD9tJ0a3uBdvduokgLnZTGQypMzomYaUaZIxMmblc+a/C0PO0kdcxfyU3F+0i6eLBZgzeXn/wcH1TGRsADVMpH43i8vdNVrFORV10hkZijIhZXFiXfISde8+F+9R6xBIdNI5ctOhZ2hZtQ9tYjq6kSbSpOuyzASbW5ecx5o5Ajmvy/jpvOrciJh8HPW4IYrX0Tml096lprG1NewZrbPTWQIiDyfb1AbnvYzmU7ND6nCxDO9HcPfkWqk4MQdjTRnOS3CU5eiqE32xYtNHmoCEhqXlOTnKWwskGaZlYIEfzMhJYl+xvbGqgdUZ5zL73nEmWsiBhmF1LovhIJQs2ovmLFcq65q5aK1LQcHBh/eQ59b1e1xWpHXLM7NvukXpch99DkbFrHV0fB4TbZPnsqJ2GmmTNFMGBkbQqC3sZTG6VYDP2Z2byWJ08PKIE6+DB0FEbaIrlk20zN0+RiNqnOHXSUsuj2krJlmfM1jDHBpUX30WXTs1UISWq4e5Vomf9eknL5Afp6BAMBzM5TAMWTIyw5GNL55LYDgaavjURIC4Zszs76CJx5cYbfaB6ApkI1y6/FxfXrwV5mRIlOcp4EYozAJMlmU4VAS0I7fdUgCo2cwL5rUuTrBZOwuzusWbCFlnA1R76burkwgGf3N9VQ+zxop5HkbHOOtN8Mu1Oqfy/B3Yu2olelaqqCaizt7XiBZzJxY9K1fEhukz4Pmop5qlFHquRdPQrwgn96m4u4ZhUt8U9UdSanG5TA1smf+9Ruh0boTg5gLOTuE4uGmDOvxmSU2cajPXex0sgLIPTX9pP3C+jAtSub+GA4mu5o7Wb5jxfagmEtASEO4ONfQ+1ObuTmYgMQswqWU5ALFf2IYa2m+qUbi2TAY4jYyp/yL5olHcbWM0EOAS5z+T+2HO6KUxQ+qq4Gs0TL+MYi/njzCagiFljn4cybg8nxObdPb5wnROQXwSAVb2gDh890Q8ypxbHlUrVkG7+5qj2+OPoG+HpzE8uZ9qFntZPudJzGSexbpb0AIIgaah3Si141dM+Z/wFKzU1PDKqZJOnYLlnzIV/t/UQDn+XslzWkb408lyPDlwzOt4fuWnE/X3SrKes8p+OglJMdWRIr7TSqu+FVOYPxnL5NwK4cTwKuLnRGDRh+8jZ8EEuI6myfmJcp5lJmsZ+hgjbrpBrp+It1s/rr4Y78N6yOa+k+U+MehRqbze5/u33kDfWjGY88Zo5Mi7UTOOWlnD4uwTM4Do3iAN40db8zfWwtagxadmeUykGWgIZA5A1EK83lrdbUAk2kh3XFrgoiamgy9a3NXNTADrwkzOzXSOREY7AuYM1jCHB9TXkSuLX2lkKLl3vEbKfPoFTALEAEPNB2vFrI5mAgCOcmefUxYvvX0bzilTFnFR1VCubAWce855uP6KK/D6sIEYM2wQnk1NwssD+iG7d1XLtLBedCInGWl2GC2im6d4D5qFFAqO3u3OR+ZTkeIbuPDlsBfFP8iA++WW4hsc12UsH3XpCM/HqXC1Phfep85D/oGNumyEApq9eTYObtmI7157GZ8kJ2jkqyAvB77jJ3RE3/L993C1+hf8nnzRHvFY8vGHcLeqqWvbUuMjkbt3uZghZ4v9HiZ+yFFdesPARGpcDHpWq6SRJG/3CvC0PRe+J86W0wWYmJKEkbffquu9ln70iYzcl+DDzu010sZlMN6nzkVBThbmjRuDV+kP1YzGiBubwtXy3ziwbq0GKg5tWC9m5jnWjL0ZSLg9wp6g1IlfblGgtuKksU7IGs2i13DyltqfAKKJxt2qCfHGvONyGZ3pNylNVGqiTPHfCBqaYgZs3GbBWX6awNEmrNyNPg03kJ3BUbJDg+qamX1dii6drR+no5bh5KWZuDS+TbQpxwCArkSORLYAq3yFKIRXjkT5MhVx56jmeGDmdJQrXxGRVcNxbb0r0fDiy1G7SlUk3n8L1n03GTc3bmT8I2oaMY10KYcwfQU112ij6+hn8j0b5qB7hYroVb0ysue8DYhQJlavrsKX3qESelatpPMQORlpGHTFpVKuCvx+P7xbFsnIXQH9Lr4YOTsWi1DeoJGqguwcAYhbBL6ymkrPNb3OiorFioB/JKNtLQFMpGqYvB0LseiD9xVcx/fsFJOuKrKXfiz1RBnAcHcmw+q9wzDz1Zc1pJyzZyM8Yx7H1yNH4quRI5A58gYBTEetz5+Via8GD9HIGoGX1a4ivnzlJXz36ivI+mIQDqxdp2bZwY0bxISlsEdZk5hGM+vEqByreavRSQZfTprHOnFsmbVm0tX4bwq47tQwUkbX2pHjtZ+NPxhpQMG9Ml14bFLVKvRlCCaaaFxTRsCcyfMwh7laOTXeLMHXpS6RZuegtZ9fv3DJWX7dGyKjnO5l4dqzWGQLgM4++wJMTmmFvRs2Y933c7H0g9exdexQpH82BrveHopN0z9Hxva1IqQu+BdMQl7mUbm+qoDOeoEMY1IQ1AeKNpNotNf5/WDa5xwJp/bH5H4p6FTmfJw4dEDyqiMzLQ2dzy+LzwYNRPbhnWqKeJd9hq4ESc1aOqHZv0ZNpG3fhuzvRmJiUg8kEzACNDX31G4Xk6dLFRnxc1QDLPlINEzXWjrJSp/Fv38tsj4djP5X1NfQLX2aAgB94qLRo3ol48sxiMHlQF2r61zKVvFV0g8eRGJUdQGvgOql6wQwHXR1s9+fK6N2Bf1EFVcg7123Dp3LnCcAlD79cjD2r12rgDm0doNGx+zlRhoJo3bguxGQ+ggeLiXSYEKsMcmSCVz2KQcaPp85NiseLDOa/U3Tjee4BIiA6Ba0tIiBDvURyWaextXRlNM9MhpFi8aOvmewSZY2uL6uVtbZfV2dbL4dTFPMxy3L9GE4mnE3IbUQ10PRrBJ/Z1Wvq7Hs80nY8+1E7PvsLeyfMhprJ47F8WlT4V+zSpfLb5k4DjmbFyNv/ybkH9mMbNcR5LydasKmfIH0jRhV4jGXfyRY9jhfvM5Gc4SkeWaApQ4wQUYThaMwR09+/IIjamBdGR1/AzyaFqZOgpFmiwGnWSoToeVVqGgacu+OHtMEjTSmj94v1mxKo2aleUpNyC/0M8DBvmFQgyYrI1wUTI2Q0QfkJ2+NoOuGManPlRJuAif0G+3lRNQkrCslzIBCQcjoGtvKvog2z6rROEvz8rxqIMuX4XIilpfnSE8IQ7m4+qhfLQ71rr4O55ctizJiKp9z3gUoU6Ycku+9wYBBtymzH+S6jowcRutuTA1KdI0z0wga/TPaR4HU9UzfojysgYBBBKWvAGGQWUfmHcgPYtSCd3ANXSrj46pknuNcjEbUovSjGL7U6ti6ajGWj+yJLWP6Y0FqK+yaNB6fPdsH7z99Fzy7N+gcwLePXgnPB8PhX/2dzlpnaNg0SgXQLUA1H30QJ5NCxOiQhkeNkNAM4YfAvdw+wOiP+jsMiRow0S43nxmi7U6Q8SVHaiRI14NxdGU4liZgL8ucodYiILtam6d6xZnoFf0o9QNYNsZEzHoSLFEGfLrCIdKEjCnUTCnQbKOup4s2oWSd2I0yoXhqAg3RRyuoFawUdD5HL2qHaLPvnoCz7mP+ogD9O9YdYRx29oX6mgwXE5R8zhhtj2poLvaU3+sT6qJKZB1cWC0CvZ7rh0ua3YUyFavhwgur4tzzyuCC8yugbJkLsbBTQ9Uo7NNMTlJq5JH9F2n6iADRTzJZYKGWEaefftu2M3l5fxqdfgGIflDc/rMU1CxDBSj8eyw8JkgoAPqNY46sMbqy2d1HzLLEC7Fo3mzMmvQBpozshw6Na2Nhcl/sfullHH/nfWTO+wIzXxsO95ED8Gekw/dxd2TYNjiBqFG4KCsMHaumodk1SKeUAmQEySzJMWX0N4WJ4VS+ZM4nULAZ9eFcEIXLGh0VRNRI1topDSZwpNc5FSPsaudb2ku1nc5xRBtfgA41NRPB1Js+S5z6eWbgiLS2CPM6npc8fsxCd55a9+ayIT4nv6VME4orleWZXKw7KRz6VX6CWp+J2pvmLoFgnpMhZF19zO8scx6MW7sl38cv9BBsGjwhmCKxZeBN6HT7zVjxbHdsG9ENrveeh3fq2/B9MwW587+F55v34Pp0DJ558gFcID6nx/qemZpovcxEdGB7MwcjLlbV/TOScvsyBx4B1vYhZ/DEZdrQBurY61fvh/Ar9AQMgRNt/sQETTFuDKNgcFkMzQ/uXdel7JEajs4fGoElixdj87pV2LJ+DZZN/wbLv/kMO1f8gIz9e+D3upDvc+HpW2/E4A5PIffbdvB+mSAvOkwnSfUDE7pamaZGtPkeF0FFM4WCSlOEmof37MUAAYHE0ZCCSWGKNv6PXmuBjFqIWoUgUNvdAI8ayWglRqCsay3AcOW0zm9QeDWUG200EYWVk4BcPq/lIkw/cJ9QMiNSEbq1QOtlXdr2SDMgqL8XZVZj836MOhK0BBPnu3gt9wrJoOEjuBQANH2NZtPtAzSLqM1oNnKFNwMvUpf6MrqvJkL3Gq14oDE2fjwBz3Zogw87PIIRTz2OjHFDMad/T0zt2g4Lhidj20ejkTl1NLre0gSZIx8yJq4OOsapJ2AMWGLNQMPJXa6woP+igDnTl/c/U0//OJJvaC1x8GPFb6lp9vSL1nHze2XUKta2Zb8A6cWWV+Ka+tciPqIGwivGoFZEbVQoWxkXnFcW5/7nAjxy922Y/GI3rPx0LNZOeRU9WrdE7Pn/QUy58nB/0AK5U1sjc+5o5E26FzmfPozcz3og5/MUZH/WFnnTWgm3QfZbjyN/dkd43rzWmCCJNKGkHdwVqr6IZZJRM3HkVpBEWTZ8tBHYbsYXUuGjeWX9hTEKvY7k/Gtg3J6rmkx8Hp105TfKLIGliUXgUbOxbitipeYW/QVqCmo7aiTdq2OXizbzU/p3XgxYVTuqkBthp+mnvg9XCQj4dO8LHXcGD1STRxow6/4ZgtM8m34zTSePo3TDnvlwIc/FaHAmc+hVWD0iGVsHtMPi/t3xwuMtseWVZ7DsnTdx4P034P7wdbgmjcbeD19G+rTP4aXZKv6e+jCqUQkICziWNtHVAASOLtKM1onOMzpKpvthhtA/kU5SP4X+CU2NSMzucDGuuuxaNLq0AcIujEPVCyMQVy0eURWiUbN6HVx9aX1UKxOuIeWq5aqJfVwWZ59zHsqdczaqCIBiy1dFTIVqeCi2HLLHJcD9UjMcHnk9ciYOQubEcTg0cQDWDO6GPSNbYkfCxfCNaoycj+9B9vsj4ftiJk7c3xCH3roTroebwfVElDrW6i9QkBkRUo3El8vRjwJrnH2jORhajdJRkuXN0pxo4w9QO6lWijIb2BhNsoHB+umgU3vSLFKTjtcZcOhcFAWcwQoCQ51uCjzNKMtRJzCpIQgO3svy1zxc+kLT02qTmXSMNvXJeR9BS03VP9ZEK3mOPhD9K/17MQaAxuczbdAIpqU99Vy/WlgytCOmpzyJVQKcFYMT4PriPawYPQQnJo/Cro9HIWNIQ6ORLXNPgyvUYt04D8NFmVyaFGOBKcbM/zA4IAOMRskGnskaZnBdnajUL0oqYISHRCEvLx/vjBmFiqI9KperiioXhqNOWG3EVI8RzVIT9S+6DJEVaqBy2TDUjIxHlfKRKC9lyQ3j6yCqYjgqnlsJeRO7ImtcO/jG34/sV28V7XE1PK+1ge+NW5A9qTXy3r4Z2a9fh6wRzZD1ajNkj70Za7o+hDcurw3XU9foZGB+nh8nOt4Inwp1jDrRGjBQ55iOOH0LaxTm+jSe47IQahrmU6BVA3G05LWiSehnMJDA36xHNUu0MTvUFCKoKEgxxoziHnmaVzTDuDOVgGJ9vJaRM2oaC5QuhmTVLyG4IlTwOY+l0TLOmyRyPR7BQsGP1c1keo7+CbWH7mA1As1wsQZCLBONph/XrhmNx3uwzfwdo/6Sp3t5bPjyY3zU+VF80vkhzBvUCT8M74pVL/bCzglDkTllEHLfbYvcT/sIGKpoP+n6NJqcqmHYLzRBCUCzZs+sO4vU4ADnY7b3O5Od/oF0+mlny+jGv/Q1sCbysv3IdbsFNLmIqFgJVcpVQVzVGogPi0aYmGFXXlIfNcJrCYii0ahBPdE+UQKcKoiuHIvqon0ui6mF2Mph4nxej2XJ1+FEnwZIH9AF7lFNkPNGUxyd9Da874r9/LK8uDH3wDPuchxPek5e+misHHQnXrihCdLG9dQ5D6U8oMBfYD4dJILh1bVsJvytWxHouFrA0AibOvYiyAQSbXGO0KJ9eJ3+WTwdrY0D7xWnm4LhSRAQMXCg3wujNqBAS93WHzQymsPkG3DKef79TPopvWgiRZoyBBDvLeaUfriQQFDTkfXFaEBA/RkurFQNFWU0EMHI3/SBLKDo53Ppc3ExKu9n+Wk0l3zJ1eB97QG4xrRE9uj7pR8fRVrKdcjoewP2JlyL3b2aYvX0eTi0eTuGtW6F/IlJyB7/NLLfbC3v4T64nrlNBq+2yH6vkwDoSeS8J/xuK+R8IoPbuCd1pyrvzYWp/MqMzstQ23SMx84+Z/JaMv7JPkaqGJkZGItcXz5yvV7ked3IySsQMFQSMIjWuKgu4qrXRJ2oi1BD/JY6ERfjstiLEV45WkAVi7AK4Wh/96149ObrkTHmPuR92Q3rkupjcZ8bMOH+G+F+uTE8z16CZY/cjtyPWmDhuDfhfe52Ea77kP5ac7iGP4T0YVdg2k13wb1hHtLXTtPl64oaP3THpW6YopOsGiFShdte3Kn79FUo6X9YwkW7nMJr/Wk9M+8Ra3wPCqM62MwT4DwThvw1Z2PxpIr47I36mDa+NrLX/xf+Vf9F3sqzkbf6P8hbdY6mx3/4L3wb/oHcdedg7HMVkbX5v1g+vYwBMMGpAKHQx6rPo5qD4GGoWH2dWHXU9Y/fKgiMJtTPyCrwzMCgmotRSV3JLEDtXBneyUPEtG2OtP5Xw/fSHfCMaI70vk1xqO/VSEtuhKPkPo1xJKUx6lWvjOND7kY2NYpoep8AxifaPmdSInzvdxHAtEP2hE7IGf0wsj/qDB/B90ZL+N5rDX+OF/m5PmR1CNeAQFZnE3Ln8pkd/c9kDTOsHnzDxFYdfJGAxQN/tkc/K5RxbD9O7FmF8865ADFVw1C5TBUFzLV166NWWC1cHn+pmGKxiK4YJ1onXMy2SrjwgirwvXg10nu2wNpn74P/sxY43PFJ+EbUgu+52vIi43HkndtwKLmF5NWVF345cl64E95BYjdPegbpt4nwrP8a2Ud3IuvAdnj2rBXNkmfrGQUNl5R4X7vDRLNoShLsFFSOznSEaZboKEzB5Oht/BE1oZJozkTpJK2O3Iyi8WuXdJpfCMPYEbehf9KjmPjxGHz65Vy88+4XGJpyC8ZPmIRRg2/GhPHj8c77UzG4e2VMmfIZXkioiPyN52DFnH9hxIi3sG3rVjze/MYACMzf2WQ7DYD0LwPopKYx5XS5P9uuH++gtonVOSbz6VjzHLobVq7zu9OR4/YhZ+SdcL94O9J6i+/57N2iuZsic8it8I5qCd9rT4kG7yDapg2yRj2IwymNkDvtReRNex7ZXw0Q7dFDwCBAeaeD+JSiUcaLNhHQeMc+IRq/owDmYeS8LSASMGlfi1anSewZdLXRLtTkXBrT9wz2YY7Q6e9TRUDiQbY3HbmudHjdaTi+bwN2rPoKZc4uJ4ARf6RMZVwcWxuVxDyrXlH8lvAY8VuqiVlWDRfF1kBY2Qrwvj5cOre1Lq1x975PRm1+fjYKGTKS5jzfAN4XasH1fHPkjJLRcWyCjGovIffz1vj+7ntwa90aeKD57cjcOQ++tG3Iz8mUF5ZjgJJnGWfEjhzmy4vM6hOmCxAD8yFJdIDpS0SZZTz0Q+g/0Heg4DLlH52l+dU3zozkNMEYidI8zr0wUka/SExTBhXojKuvEWX23qifEm3qpCZRZ5xmHE1ahoQjFcAaJuaHD/XrOzF6rH81WT8Da1YAmD9NTpBHmetp5vEvDRBMBBn9E105INe/eAMy047gwJYDyHhWAPn8rcjs1xi+Vx6Bd2QLeJ67FycG3Cj9Sw3xlGidR5D1wv3Y2uFK5E7uq3/uL+/b4cie2AM5/0tF9se94ZvQFZ5PesL7jpjKYwVoH/cUELWV82K6zXnTHqICFPjKTFcujTmDTbL0YwdNj9DkoVwytTmYQn9bVKBDEQ8KsGfTBjkMeB56Npj3brHOy/8pr40SQPjNKZJ9f7sNwRTcpkB1BeabZ7p0hwIYpaFv+0+X63brvjRpjECqsFofAtdzep0x2xhu1lAx55koxGruWXWrBjOagdpLBZwagKsdWC/rt5cUcWKRoFIgm6CEblewvyBKM0snfAlCcw/1Z6SMOv4MvMhxztrPCz/vqUhG/wKrLwL9JoMJTdcC1RDA6N5d8WLbh5GVfkKDJ3pe67ZS/8lOHfa4+EK51iAVSla/U+Ps7NSoiBz9nvyHAiYzM7OwQNrCaqf2iwhOrfN8T22uvQqJtzRD8h0N8UrXNji6fxc2Ll2A4Y/fjZlTJ4EA2b99MxZ99xmyMtJxJO0Q8uS+6ZLmZvsK1adk38em0DYFnfcO43ehI9RkMbPpFD4xdfhJWl1GQo1AB5yCG2UigSrQJvKlAQJ+7INlAiChYLOMpUms7Q1GuINBGK1hY/tv5Gi9+m03Az6zTYHgpHaT9g3gTH2Mzpfwz7HrCgDejxpFv/MWYZYcSRvzD6wv3C+h/SGUk5ONrk0uwZZlC9HrliYY3f0JvNG7Bx6IugCvdO+ALcuXY8qoYVgi/b57/Rp0aHgJnqhdEV3uuBZeVyYWfDZRANIcrWKrY/qHYzH9vdd168S8KZ8o2Aq9D/u+1vGWoS2LyNHvyX88YEg0d+hcM7W5OCG2OzCUJP/Q9h0Ym9IRIzo9iufbtZDRrQ3GD0rAy10ex4TBKfJC2+stCgHPvk8xQlGELJPMPu95rp75oj6FXMyZt7/cebKs1m/dRG/KnwVq3tEPUpJjf7YfBXn5RZ850MYCGXX98rMAObl5unXglMLME/bIrddbxyRJZyxNM2ai/uEmfvE/xmyZIIA0gGGW0fCrnAHi9Wx/8DvQn6ZuptPfHYe3+3bD860fxCcv9seQVnfhxSdb4JMRgzDkITFzjx3DuoVz8VrC03i3fyJe6fQEnnniQUwaMRxvJnbGO4MSMTa5e+EbhJLdh1Jky7AHi8jR78l/KGAOfvsSMua/jXxvBvzC+dYylmLTbIuzrDw73/5tlw0+H8yhdQby3ZJazHOh9RS6jmUykflZf2R98xzcM56H+1tJv3sWrm+fQUq/cXjro/lom/QR0o5lipDnIj0zC7MXb8LBQydkZPZj5ab9ChqfNxs52blwiTO9aNVONTfeeH8Oduw5jKMnXPBI/xAg85ZuVQfYlZWNzTsPY/e+Y1i2YgcOHj6qAjRy3Eypxw+v1LVj9yHs2X8MqzfuwW5J9x08ofc6cjwTX89eB4r4ivcGw/2NtPe7Z5D5zTNwyXGmshx/+yzcnw8MArnFNp0q3z4OzQ8A3yL7fHD54DSY7HvZJHVlu49g2+RRReTo9+Q/FDABDcPOsUcz4TL1UxB942Dc8MQYHTU9nhx4xQzwenORJYKmPVzA8S1f94FQ2HbvO6r5bq9Xr7H/mYErX/J9yM7JRcYJDzIyPNix65jO+WzffVSu9yNNhKp6s6GIvGkoEod/pg2p1mwILr/nZZRv0Fc/mcR7ter1Ll4dPwvZMuIrKAQEew+cEAHPkbqOq4CyPVmebOT68kTQfTh+1KN5ubn5uOaB15H0/GeYu3CbiQSJhmGqz0HB8ZudlaqJjJOgbcnPz9M2mDxmmWc74fKo9qHTsGjZDn123Z3JMqpl8rVPtX5JfdKHm7cfNOf0Fie1XoEU0D6jXSRV5mTnYdeeE6av5Xq/5Mfd8AZimo1GynPfSV4+tm5Lk/fiE5BnKahVi+p7NO1jzUtXbNc2uN3Z5pnpu/A5eSx1p2f4sGHHYXkHLmzbfQTrtx6QZ/Jj6640qz2BbsCBfQeKyNHvyX8OwNjmCFOh/329Qt9ng+bPGeG3AWAJkHnJFKw8fWn6O9fq1aCXTkCZK61jlqMJxBepwmRdwzxJa9wyHOHNhluy5EezVi8j7Noh+GLWOr1u9g9bcffTb5jbWPcyP1gPD/ORmeXFhCnLcOy4G2CbRDDyWb/euwC3PDoatW8YjHwBjzRfnWFtm22usag6wyfZPLd5BgUAJYf1USitZ9S2BPrFtI/HRvgLtA+1rRRSfWY2OF/7j/mX3DZchN5trtPIIAVazrGdrNeqb96S3Uh9cY4BhNYnzwealqYf9D0Qv7kWuBXAJ8tqfWyPXsO2+837td+XHvMa02fmOqsrhA7sOYMB47DDpxs7gHHY4VKwAxiHHS4FO4Bx2OFS8FnGlXLIIYdKQg5gHHKoFOQAxiGHSkEOYBxyqBTkAMYhh0pBDmAccqgU5ADGIYdKQQ5gHHKoFOQAxiGHSkEOYBxyqBTkAMYhh0pBDmAccqgUVCLAZGRk4KyzzirEGzZs0PTn0Nlnnx2aVYjuu+++0KxflcqXLx84vvPOO4POlI5+7vP/HJo4cWJoVhGqX79+aFaJKSkpKTTrd6MRI0aEZmH48OGhWUXo+uuvLySTHo8ntMivTqV+4+vXrw8cBwuMfRyc17x588Dx//73v8BxMGCCy69Zs6ZInn08ZsyYQF5wfvBx9+78mELhvOJ+BwOmQoUKmtrnudsvNzcX1atXD5Qh/fe//w0cx8bGavpj97Cf8aGHHsLx48cD+XwODjakDz/8UNPinqVZs2aBPNKwYcM0TUxMxMaNGwuds8kGzKxZswJ9OWDAAE3tek81WAUD5m9/+5umYWFhgby2bdsWauc//vEPTYtre+hvW5Ap4KHnSC1btgwc23THHXdoOnny5EDezJkzMXr06MBvEuvJzs5Go0aNkJ6ernk1atQoVObXpMJP+BP05ZdfYuTIkXqcn5+vjd2/fz8OHDigxxS2LVu26PHDDz+MFStWFLqe+ffffz/+7//+D40bNw7kdenSRR8yPDw8kNe6devAdeedd17g2Kb27durUHXt2hUvv/yy3pt179mzRwWedQQL6pIlSzSvbt26KFOmDPr27YtDhw7pMWnQoEGoWrWqtpvEe3700Udo2rSp/s7JyQk8V79+/cxSb/lN7WvTnDlzAmXuuusurFq1Ci+88IKeY/7evXsVMAQj888991w9t23bNtxzzz0KiqlTp2oe27l48eJA3bz+tttuQ4sWLZCamoqePXsG3gXp4MGD2od8L6+++irefffdwHXPPfecpoMHD9aUQnjZZZcFriURMKyTbWD9JILdfp4ffvghYGnw9xtvvBHo52PHjmHnzp16HExs69VXX40HH3xQf7NcREQEevXqpWUJQhIHowYNGgRfin//+9+BAYBlX3vtNZQrV65QmV27duk5Aob0r3/9S9tEq4GyGjww/lpUIsDYH0pw2OEznQsBxs7kKMVP/OTl5SliObqSiWSHHT4d2ev1Yt++fcHiHiDK+u7du4tcE8pqZfACGyi8kJk0N1wuF06cOIEjR46o6ULTa/PmzWry0LT4Ldk2X0KPfw5369btF9fxS5mmWfBv+jChZX6K+QyPPfZYsflM6W/QeQ49fyrmdTSNQ/N/Kf/9xmfxv5nLi+QXx/3HTdfyofm/Jq9evToUHz9KNOND6yATbMTAWbZGoTYhCmmnpqWlKeIIEDqP9EXYwe+88w5GjRqltrXNzKfdTfs9OH/BggVqp/P4P//5D8aPH688b968wHXB6bfffhu4lhGS4Pp/6jgqKipwTMfQPqbdbf9m23v06KH2M3+/+OKLmpYtWzZQnnZ8aN3BxzZT0JguXLgwcPzPf/5T0wix0UPL16lTJ3A8YcIEdVBDy5Dj4+MDx3S8mQb3N6OHTGnz23nB7aNvxfTvf/+7phdddJEGAOzzjLTRv7F/222mL3TNNdfoMZ15pvTx7HLkf1+bilff/xL/aZqKv1+TbO5jpcHHTN//dBrm/7BQjxctWlRsOfL8BaYMj2PuH4Z/Nk7B9wt+COT1fOFDPV64cBH+0TgZg16fXKhNP8UrV64MxYMS+4xyf+mll2LcuHGhp5VC6yIvXbrUAEY/QeqQQ38x2rFjR2hWIFhF4iBRkvC12+3G9OnTMWPGjJI5/Q45dLoSXYjSEt2R4qiI0++QQ39VWr58eWhWIaI7wgDXT5EDGIccKgX9IsAwekZ70OaSEh1alrdtTPt6e4b5x4jlGGD4KapduzbOP//80OxflUrzzD+Hfuv6fw5xcvNMpl/0RmzA2MRYdfBv+7i4F8/lJQRMQkJCYNkHyz3wwAOB4yZNmgRforZlw4YNA+cZDWLKGWNG+WwgMvIRDBi7rM12XjCpfRpUZ2iZH8uziVEu5pEZJWR7Qu9p10/bOjnZRJHsc6TgPmRq/7brYVSPZD8rl4Nw6Yn926bg5yHbS3uYd/nll+vx119/HbiGqzWqVKmiUb/gvrLrsSm4bcHl2rVrV2y7g+mqq64q1CdcHXC6UVFJduiMoWDAOFQycnrLIYdKQQ5gHHKoFOQAxiGHSkEOYBxyqBTkAMYhh0pBDmAcKhUFbwE5Hdlu/8+lXwSYTQ90wP6725aM72qDfcK77za77Bw6vYhCxqUjB6bNxYayl5/WzC0r3Mbyc4DziwCzseb1SItoXGI+FNUE+6KvDa0mQJwT4EQetxeQub6HKfPtvFDiObL98JzE6927N5YtW1Zo6Tbz+MK5vN2h0hP7l5ORu76cXkQATzfm3hbK1h8GmOzRn+Dw5q2FwPHDZTdpSjW4sYYpd+jGVj8JmK1bt4Zmn3JyzQaLzdz3zX3jweWDZ59D8xwqOZUUMEdfGl/outDzP5dJh/uNLJL/c/hPB5iDkU0Cx8GAORjZ+EcB82tQKGBsKi7PoZJTSQFD2nrRLXrsXboGGZ98he0N7kG+2xM4f6DTAE1Dr9sssmEfh54LpuAyu+9sA8/ilcjeugt7WnQu9vpQ/sMBs+7qe7Cs8X1Y08ik5J2xTXHg8jv0eEf95jgU+dOA4XZi7hp06M9HJQVMcUzAeBauLJL/S5gU/JuACS1zKv7DAVNS/inABG/cCf5wHbfQUlOR+JDTpk3T7w6Q7BXP/CRSKNll+KIPHz5cpIN43l4AuGvXLi1nE79n4NBJ+iWA+bPxHwYYh84sYtDk6NGj+h21tWvX6vce+JGJ04XZZn43j2b7HxIlc+jMIwoZOXR+43TinwMUmxzAOORQKcgBjEMOlYIcwDjkUCnIAYxDDpWCHMA45FApyAGMQw6Vgn4TwHyf0huLHmuBNdOnhZ5y6DSnTZs2hWadUfSLAKPxbOFdN12NHTddhe03NizKN1yNnc2uwS7h7TcU/qtaDp1+5ADmF9CF41uhwtuPYnvT+th5XQNsFOC4jh5ByyErcdOwE3hz6mr43auQv6qxxU2UkW+WrART6MpjfhnfoT8flRQw/CtgNj/55JOhp4sl/sUze3kUPwD+Z6RfBJhybz8S4HGPNsW4L3aj0dB8NBnuE/bg2mGGcz2bDGBWXivcVPjk3zq0iSDhxh7SHOtP39n5JHZgcUv0mXLdF/+0Ho8//vhj/SCdfY7MP+swd+7cIqAMrsehklFJAMMPPNofZLQp+I/v8pgfDrTz7DQYMKHn+P750UdS586di5ThWkDyz/n4eGnoF0nLheMfRdnxD+HCtx9GuXEPo9brbZDmyceNww6g2bBjGDs/A+nedEBAgpUEDMEinJcVWpVDpwmVBDB/ZfpFgKH/kuFzo+zbLXGBAOd80TRlJDX8INbteFqA0ijA/jW/7Z8Td+i3JwcwvzLtPH4Is3esgDdzNXLcG5Cb4w0t4tBpTvQv58+ff1oyv3n9S+hXB4xDDv2VyQGMQw6VghzAOORQKcgBjEMOlYIcwDjkUCnIAYxDDpWCzqpTOxoOO+xwydgBjMMOl4IdwDjscCn4tATMPXffhkmTPkbtWlFFzp3OzGcaNmwQ4uPDlV955SV88MG7Rcqdrmy/M6Zjx45Wvvee2/HIw/efNu/ytAHMJRfHaUfXiI8ocu6vwD82APBcaN7pyMGA4W8e33PPbQ5gfktmxzZocKl2+sUXxRY5f7oyn+vjj97Hhx++hysur4X69S4KjMS1iyl/OnIwYGx2AOOww39hdgDjsMOlYAcwDjtcCv5/OBJTiU0TI/gAAAAASUVORK5CYII=>

[image2]: <data:image/png;base64,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>

[image3]: <data:image/png;base64,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>