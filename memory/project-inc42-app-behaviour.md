---
name: project-inc42-app-behaviour
description: "What Inc42 app users actually do — first real post-launch behavioural analysis (12–20 Aug 2026), the walkthrough confound, card-level brief drop-off, and corrections to the 17 Aug PostHog review"
metadata: 
  node_type: memory
  type: project
  originSessionId: b2024af5-d7ba-4821-944c-c16a524e5e85
  modified: 2026-08-20T13:47:14.459Z
---

Full analysis run 2026-08-20 on PostHog project **Inc42 App (146258, EU)**. Cohort: persons with `person.created_at >= 2026-08-12`, `@inc42.com` emails excluded. Artifact (republished, new URL): https://claude.ai/code/artifact/8e80f634-3f0a-4b1b-ae1b-db95d3e5a7d7 · file `~/ClaudeDocs/inc42/inc42-app-behaviour.html`.

**Base: 189 real users, 180 fired `app_installed`.** Android 111, iOS ~83.

## 🔴 The walkthrough confound — invalidates the "Explore is winning" claim
The app runs a **4-step guided tour**: step 1 `brief`, step 2 `explore_articles`, step 3 `explore_companies`, step 4 `watchlist`. **151 start it, 123 finish (81%); of the 27 who bail, 16 bail at step 1.**

Control groups: guided users (134) used Explore **100%**, brief 55%, watchlist 96%. **Tour-skippers (16) flip it: brief 63%, Explore 44%.** Users who never saw the walkthrough (38) are not a valid control — they barely used the app (5% opened a brief).

**So Explore's 82% reach and Watchlist's 74% are tour artifacts.** 48% of Explore events and 62% of watchlist events happen inside the first 10 minutes. On return visits Explore 41 vs brief 35 — near parity, not a 34-point gap. **The 17 Aug PostHog review's "Explore is beating Brief 69% vs 31%" carries the same uncorrected artifact.** Ranjith raised this hypothesis himself and it was correct.

## Brief funnel — the loss is entirely at card 1
Installed 180 → onboarding complete 150 (84%) → saw cover 156 (87%) → **entered brief 86 (48%)** → completed 33 (18%).

Card-to-card advance: **card 1→2 is 45%**, then 79 / 87 / 82 / 87 / 77 / 80%. **No fatigue curve — "the brief is too long" is not the problem.** Editions were 8 cards on 12/13/19/20 Aug and 10 cards on 14–18 Aug; edition length barely moved completion (34% vs 31%).

**What the 106 non-advancers at card 1 actually do:** 29 go BACK to the cover (15%) · 26 expand the summary · **only 19 (10%) leave the app** · 17 open the full article · 12 re-open the brief. **21% move backwards/sideways inside the app → this is a navigation problem, not disinterest.** The cover cliff and the card-1 cliff are probably the same bug.

**The full article is a one-way door.** 54 opened from brief cards: 40 read it, 7 left the app, **only 3 returned to another card (6%)**. This is the mechanism behind the 20 sessions that reached card 8 without completing — those sessions opened MORE articles (2.3/session vs 1.46 for completers). Recovering them takes session completion 33% → 51%. Fix: a return path ("back to your brief · 4 left").

**The summary is a bigger exit than the article** — 44 session exits vs 7.

**Repeat opens are the real lever:** completion 26% on first open → **50% on second**. 47 of 86 openers have only ever opened one brief.

## 🔴 Correction: median completion is 78s, NOT 7s
The 17 Aug review reported a 7-second median and concluded the brief was "mostly flicked through." On the clean post-launch cohort: **median 78s, avg 8.4 cards, 51% of completions over a minute, only 20% under 10s.** The 7s figure was distorted by pre-launch test traffic. **The brief is read far better than the team believes** — relevant before committing to Utkarsh's 20%→40% target.

## What is genuinely earned (survives the tour)
**Company data is the deepest real engagement.** 34 users generated **683 company-section views (20 each)**; funding 281 views / 8.8 per user, then financial_overview, key_people, corporate_activity. **"At a glance" on company cards: 22 users, 141 taps, 6.4 each, across 102 companies** — the most intensively used control in the app. 75–80% of company views happen outside the tour window. Ordering (funding → financials → people) is a deal-research sequence, not news reading.

Other earned surfaces: article reader (79% post-tour), 22% of article readers scroll to 100%, article opens split Explore 107 / brief 54 / deeplink 45. **Deeplink, search and company-page articles average 130–157 days old — the archive is a third of all reads.**

## Retention
D1 26–43% (blended ~33%) **with zero push ever delivered** — at/above the ~25–30% news-app median. **D3 collapses to 7–21%.** **57% of users are active on exactly one day; only 7 users (<4%) hit 5+ days.**

Push: 171 prompted, **114 granted (67%)**, and `push_delivered` has NEVER fired. The retention engine has never been switched on.

## Timing (IST)
Brief peaks 08:00–11:00 (69 opens) — validates the morning send. **Explore peaks 19:00–23:00 (335 views), nearly double.** Nothing in the product serves the evening user.

## Instrumentation defects found (add to the v1.5 dictionary pass)
- **`app_installed` under-fires ~5%** — 9 of 189 users never fired it despite all 9 completing the walkthrough and averaging 78.7 events. 8 of 9 Android. Means PostHog will always read low vs Play Console.
- **No 403 anywhere, ever** (verified all-time, unfiltered, 2026-08-20). But **`http_500` DOES exist** (company_profile, 45 events, 5 users, 23–27 Jul) — so the app *can* emit status codes and 403 is either swallowed client-side or bucketed into generic `load_failed`. Asana task filed for Ritvik: https://app.asana.com/1/176734136274/project/1202454202198945/task/1217678281874556
- All-time `error_type` values: `load_failed`, `not_found`, `http_500`, `brief_not_ready`, plus one malformed raw message string used as a type. **PostHog's taxonomy panel only showed 2 of these — it samples recent values, so always confirm with SQL.**
- Errors hit 13% of users, concentrated on the most-used surface: `load_failed` on Explore (13 users) and brief (9).
- `summary_expanded` fires on 4 surfaces via a `surface` property: `brief_card` (33 users/77 taps), `company_card` (22/141), `explore_gist` (11/35), `company_page` (6/10). **`company_page` carries `story_id` instead of `company_id` — wired wrong.** `explore_gist` shows a 28.6% same-item repeat rate (possible fire-on-collapse); brief_card and company_card do not (~2.5%).
- **`decode` has never fired** — the AI explainer that IS the positioning has zero telemetry.
- Search: companies 28.5% zero-result, **articles 42.2% zero-result with 2.2 avg results**. 17 searchers, 12 searches each.
- Sign-in is effectively mandatory: 96% start, 78% complete, only 51 net-new registers → **most sign-ins are existing Inc42/Google accounts. The app is reaching the existing audience, not a new one.**
- Dead features: rate card 1 user, story_saved 4, story_shared 5, sector_landing 4, preferences_updated 5, streak page 15.

## ✅ Corrections to earlier beliefs
- **iOS 1.0.1 IS LIVE and rolling out** — 3 users 17 Aug → 16 on 18 Aug → 27 on 19 Aug. Any item saying "blocked on build ≥41" or "awaiting Apple review of screenshots" is closed.
- Cover→brief entry is 55% (156→86), not the 41% in the 17 Aug review.
- Android is the platform: 111 vs ~83.

## Satya design sessions, 2026-08-20 (two Wispr recordings, 10:40 and 11:20)
Agreed: declutter the brief card, add a progress indicator ("4/8, tap for next"), remove the past-brief card + add "Continue where you left", editorial to rewrite the headline so it reads as a series not one article, prototype a "Personalizing for you" loader, defer dark mode and streak, explore an article-access MCP as a paid tier.

**Data check on those decisions:**
- ✅ Progress indicator, "Continue where you left", removing the past-brief card, editorial rewrite, deferring streak — all supported.
- ❌ **"Drop-off cues only meaningful at article 4-5; article 1-2 drops signal irrelevance" is wrong on both halves.** There is no drop at 4–5 (82%, 87%), and card-1 drops are navigation, not irrelevance. The cue is needed at card 1.
- ❌ **"Move Rate to the freed space"** — the rate card has 1 user in 8 days and was already flagged as a dead click on the 1 Aug QA list. Verify it fires before promoting it, and before running interviews on "rate visibility."
- ⚠️ **Hiding "Read full article"** protects completion (94% never return) but deletes 54 genuine reads. Prefer a return path.
- ⚠️ **The loader adds latency in front of the step that already loses 55%**, on a surface where 9 users hit `load_failed`. Test, don't assume.
- ⚠️ **Articles/Companies as top tabs "powered by DataLabs"** — the company-depth signal genuinely supports it; the Explore-breadth signal does not (tour artifact). Deferring until the brief-habit thesis is validated is right, **but validate it with push ON** or you are testing the brief with its engine off.
- MCP idea: §11 of [[project-inc42-strategy-utkarsh]] explicitly rules out a second product line for the demand side, and third-party data exposure needs a DPDP pass. Check both before scoping.

Related: [[project-inc42-launch]], [[project-inc42-app-acquisition]], [[project-inc42-deep-linking]], [[project-inc42-content-personalization]].
