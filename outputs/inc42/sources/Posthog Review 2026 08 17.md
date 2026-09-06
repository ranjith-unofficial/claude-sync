# Inc42 App — PostHog Review, First Real-User Week (Aug 12–17)

**Date**: 2026-08-17 · **Project**: PostHog `Inc42 App` (146258, eu.posthog.com) · **Window**: real users from 2026-08-12 (per Utkarsh); all "fresh" numbers are the installed-since-Aug-12 cohort unless noted · **Judged against**: `event-tracking-plan.md` v1.4 (47-event dictionary), `v1-prd.md` §12 metrics, `gtm-launch-plan.md` §6 scorecard.

**Caveat on every number below**: n \= 131 fresh installers over 6 days. Directional, not conclusive. Also 34 of 168 actives since Aug 12 are pre-Aug-12 people (beta/internal) — there is currently **no way to exclude the team** from any query (see §1.4).

---

## 0\. Headline

- **\~134 new users since Aug 12** (131 fresh installers; 112 Android / 52 iOS / 4 iPadOS). "Crossed 100 real users" confirmed.  
- **D1 retention \~30–38%** by daily cohort — at or above news-app benchmarks (\~25–30%), **achieved with zero push notifications live**.  
- **The retention engine is dark**: `push_opened` has fired **twice ever, both on Jul 10**. `push_delivered` has never fired. 67% of users grant push permission at onboarding — and then never receive anything. This is the single biggest available lever and it requires no product work if the Customer.io integration is done.  
- **Completion rate is nominally at the §12 bar (41% of brief-openers) but half of all completions take \<10 seconds** (median duration: **7s**). The "5-minute brief" is mostly being flicked through, not read. The north star as instrumented flatters us.  
- **The biggest funnel cliff is the cover → brief CTA**: 99 users saw the brief cover page, 41 tapped in (41%).  
- **Explore is beating Brief**: 69% of fresh installers used Explore vs 31% who opened a brief. The archive/company browser — not the habit anchor — is currently the de-facto product.  
- **Watchlist is unused**: 98 users opened the tab, **9 added anything** (7%). The onboarding watchlist step (specced: role → sectors → topics → **watchlist**) is absent from the shipped flow — `onboarding.step_name` shows only role/sectors/topics.  
- **Two days before the D2C Summit QR moment, deep-link attribution is broken**: Singular links (`inc42.sng.link/…`) arrive with `campaign = None`. Summit installs will be unattributable unless fixed before Aug 19\.

---

## 1\. Instrumentation audit — spec (v1.4) vs production

### 1.1 Dark events — in the dictionary, never fired (all-time)

| Event | Consequence |
| :---- | :---- |
| `decode` | **The AI explainer — the positioning ("AI that explains what it means for you") — has zero telemetry.** Either Decode isn't in the shipped build or it's uninstrumented. Verify with Ranjith which; if it shipped uninstrumented, this is the \#1 gap. (`summary_expanded` — the static summary — does fire: 62 users.) |
| `interest_captured`, `locked_feature_tapped`, `watchlist_limit_hit` | The **v1 monetization dataset** — spec says "must be clean day 1" — is empty. Either gates aren't in the build or they're silent. |
| `push_delivered` | The OEM delivery trip-wire (Launch Infra A3/D5, the MoEngage decision input) cannot be evaluated. |
| `brief_fallback_shown`, `rating_prompt_shown`, `force_update_shown` | Lower stakes; confirm intentional. |

### 1.2 Off-spec events — firing but not in the dictionary

`walkthrough` (104 users — the largest unspecced surface in the app), `brief_story_rated`, `sign_in_prompt_shown`, `story_unsaved`, `company_untracked` \+ `industry_untracked` (duplicating `watchlist_entity_removed` — three events for one action), `push_priming_dismissed`, `share_initiated`, `app_installed` (spec said no custom install event), `brief_open_today` (dead since Jul 13 — remove).

The dictionary's own rule: *"If an event isn't in this doc, it doesn't get instrumented."* Reality has diverged in both directions → the plan needs a **v1.5 reconciliation pass** with eng, not silent drift.

### 1.3 Property gaps

- `onboarding.step_name`: only role/sectors/topics — **watchlist, push\_prompt, signin\_prompt steps missing** (flow shipped differently or unlogged).  
- `brief_page_opened.is_edition_switch`: null on all 871 events — not implemented.  
- `brief_opened.source`: only ever "organic" (consistent with pushes being dark — but confirm deeplink attribution wiring too).  
- `deep_link_opened` is polluted: 62 of \~150 users are `auth_callback` redirects, plus a dev IP (`192.168.1.52:8083`) — internal testing inside production data. Exclude auth callbacks at the client.  
- **Story bundle (§4.11): GOOD.** 89–100% presence of author/industry/story\_type/development\_type/slug on `card_viewed`. The editorial feedback loop is measurable today.

### 1.4 No internal-user exclusion

There is no person property, cohort, or flag marking Inc42 team members. 34 pre-Aug-12 people are mixed into every live number. **Fix**: (a) an `is_internal` person property set for @inc42.com identified users \+ the pre-Aug-12 first-seen cohort; (b) a PostHog cohort "Internal & beta" applied as a default dashboard filter.

### 1.5 Auth anomaly — verify

110 users completed sign-in since Aug 12, but only 25 fired `register` (net-new registration). Either (a) sign-in is effectively mandatory in the shipped flow (spec: optional, most users anonymous) and 85 were *existing* Inc42/Google accounts, or (b) `register` under-fires. Determines whether the anonymous-user architecture (push-able without registration) is even live.

---

## 2\. What the data says (fresh installers, Aug 12–17, n=131)

### 2.1 Activation funnel

| Step | Users | % of installs | % of prior |
| :---- | :---- | :---- | :---- |
| Installed | 131 | 100% | — |
| Onboarding completed | 97 | 74% | 74% |
| Saw brief cover (`brief_page_opened`) | 99 | 76% | — |
| **Opened brief** (cover CTA → first card) | **41** | **31%** | **41% ← the cliff** |
| Completed brief | 17 | 13% | 41% |
| Used Explore | 91 | 69% | — |
| Added ≥1 watchlist entity | 9 | 7% | — |
| Registered (net-new) | 24 | 18% | — |

Two structural reads:

1. **Cover → brief is the cliff.** 58 of 99 users who reached the brief's front door never walked through it. Candidates: CTA prominence, cover content sufficiency (headline gives away the day → no reason to enter), or users bouncing to Explore.  
2. **Explore (69%) \> Brief (31%).** The product thesis is "finite brief first, archive on pull" — behavior is inverted. Either the brief entry is broken (fix the cliff first, then re-read), or this audience genuinely wants the company graph/archive more, which would reframe v1.1 priorities.

### 2.2 Completion quality — the north-star problem

87 completions by 32 users. Duration distribution: **50 \<10s · 15 10–30s · 5 30–60s · 9 1–3min · 5 3–10min · 3 10min+**. Median 7s, mean 184s.

A 7-second "completion" of an 8-card brief is a flick-through. The §12 metric ("briefs completed/day", ≥40% completion) counts these. Nominal completion rate (41%) meets the bar; **engaged completion (≥60s) is roughly 17/87 completions — \~8 users/day**. Recommend formalizing **`completed_engaged` \= `brief_completed` with `duration_sec ≥ 60`** as the reported north star, keeping the raw count as a diagnostic. (Silent-wrongness rule applies: a number that flatters by definition is the same failure mode as one that's stale.)

Card drop-off (per-position users): 61→50→49→48→46→43→41→39 across positions 0–7. **\~64% of card-starters reach the final card, dropping \~6%/card, no single killer card.** The curve is healthy — the problem is upstream (getting into the brief) and depth (dwell), not mid-brief abandonment.

### 2.3 Retention (pre-push\!)

| Cohort | Installers | D1 returned | D1 % |
| :---- | :---- | :---- | :---- |
| Aug 11 | 26 | 8 | 31% |
| Aug 12 | 14 | 6 | 43% |
| Aug 13 | 29 | 10 | 34% |
| Aug 14 | 20 | 4 | 20% |
| Aug 15 | 15 | 5 | 33% |
| Aug 16 | 12 | 4 | 33% |

\~30–38% blended D1 with **no push at all** is above the news-app median (\~25–30%, `design-constraints.md`). D7 not yet readable (first cohort hits D7 Aug 19 — which is also Summit day, so expect contamination).

### 2.4 Push — the dark engine

- Opt-in: **75/112 prompted at onboarding \= 67% grant** (37 denied). Strong.  
- Sends: `push_opened` \= 2 events, both **Jul 10**. `push_delivered` \= 0 ever. `brief_opened.source` never \= push.  
- The entire CRM layer specced in §6 (morning-brief send, same-day nudge, winback) is inert. The Customer.io person-attribute machine (`briefs_completed_total`, `last_brief_completed_at`) has nothing to trigger.

### 2.5 Engagement depth

- `summary_expanded`: 36 of 62 card-viewers (58%) — the static summary earns its tap.  
- `article_opened`: 59 users — article-opening is as common as card-viewing, i.e., people do go deeper.  
- Saves 5 / shares 7 users — negligible, fine for week 1\.  
- Search: 16 searchers, 195 searches, **58 zero-result (30%)** — the Task \#17 search-quality concern reproduced in production. Low user count, high signal.  
- Errors: `load_failed` on **Explore** (7 users) — failures concentrated on the most-used surface; `not_found` on company profiles (4 users).

---

## 3\. Existing dashboards — verdict

| Dashboard | Verdict |
| :---- | :---- |
| **My App Dashboard** (583341, Mar) | Web template on `$pageview` — the app sends no pageviews. Dead. **Delete.** |
| **Consolidated Dashboard** (892092, Aug 12\) | Right instinct, four flaws: (1) funnels route through `sign_in_completed` mid-funnel — biases everything toward signed-in users and hides the anonymous majority the architecture was designed for; (2) the `card_viewed`×8-repeated funnel doesn't measure position drop-off (same event repeated ≠ position sequence — use a single `card_viewed` trend broken down by `position`); (3) the sign-in funnel tile is duplicated; (4) no retention, no push, no duration/quality split, no internal-user exclusion, trend tiles have no engaged-vs-raw distinction. |
| **New Dashboard** (894281, Aug 13\) | One push funnel tile. Fold into the main board. |

## 4\. Proposed: one dashboard — "Inc42 App — North Star" (replaces all three)

Default filter on every tile: **exclude "Internal & beta" cohort** (build it first — §1.4).

| Row | Tiles |
| :---- | :---- |
| **1 · North star** | Briefs completed/day (raw) · **Engaged completions/day (`duration_sec≥60`)** · completion rate (`brief_completed`/`brief_opened` users, weekly) · DAU |
| **2 · Activation** | Funnel: `app_installed → onboarding_completed → brief_page_opened → brief_opened → brief_completed` (7-day conversion window, first-time-ever) · installs/day by platform |
| **3 · Habit** | Retention: `app_installed` → returning `brief_opened` (day grid) · daily-habit readers: HogQL, users with ≥4 distinct `brief_completed` days in trailing 7 · streak-day distribution |
| **4 · Engagement** | `card_viewed` unique users by `position` (the real drop-off curve) · `summary_expanded`/`article_opened` rates · **Brief-vs-Explore DAU share** (the thesis-check tile) |
| **5 · Levers** | Push: prompted→granted funnel \+ `push_opened` trend (will read 0 until CIO goes live — that emptiness *should* be visible, per the stale-data rule) · watchlist adds/user · `register` rate · search zero-result % trend |
| **6 · Quality** | `error_shown` by type/surface · `decode` latency p50/p95 (once live) · `app_version` adoption |

**BUILT 2026-08-17**: dashboard **901039** — [https://eu.posthog.com/project/146258/dashboard/901039](https://eu.posthog.com/project/146258/dashboard/901039) (17 tiles, pinned). Every tile carries a HogQL era filter (`person.created_at >= 2026-08-12` \+ @inc42.com excluded) in lieu of a cohort — beta/internal traffic is out by construction. The three old dashboards (583341 / 892092 / 894281\) are retirement candidates, left in place pending Utkarsh/team confirmation. Weekly readout rides the existing scorecard cadence (GTM §6, owner: marketing).

## 5\. What to focus on — ranked

1. **Turn on the Morning Brief push.** Opt-in is banked (67%), retention is decent without it, the CRM layer is built and dark. Highest impact, zero product work if the Customer.io integration is complete — find out *why* it's dark (integration unfinished vs deliberately held).  
2. **Fix Summit attribution before Aug 19** (2 days): Singular deep links currently arrive `campaign=None`. The tent-card QR → D2C-preloaded onboarding moment is unmeasurable as-is.  
3. **The cover cliff** (99→41): treat the brief cover as a conversion surface. Cheapest experiments: stronger CTA, or auto-advance into card 1\.  
4. **Watchlist activation** (7%): ship the specced onboarding watchlist step. Without it the "personalization engine" and the Datalabs on-ramp are dormant, and `boost_reason`/"relevant because" have nothing to work with.  
5. **Adopt engaged-completion as the reported north star** before the number hardens in weekly scorecards. 41% completion sounds like the §12 bar is met; 7s median says otherwise.  
6. **Instrumentation punch-list with Ranjith**: `decode` (feature or telemetry missing?) · monetization events · `register` vs forced sign-in (§1.5) · dedupe untrack events · exclude `auth_callback` from `deep_link_opened` · `is_edition_switch` · internal-user tagging · dictionary v1.5 reconciliation.  
7. **Watch the Explore-first pattern** after the cover cliff is fixed. If Explore still dominates with a working brief entry, that's a strategy signal for v1.1 (archive/company graph as the wedge), not a bug.

---

*Method: direct PostHog API (HogQL), project 146258\. Queries in session scratchpad (`ph-queries*.sh`). Event inventory, funnel, retention, duration, and property-presence queries run 2026-08-17; all counts person-distinct unless labelled events.*  
