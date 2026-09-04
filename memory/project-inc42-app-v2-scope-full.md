---
name: project-inc42-app-v2-scope-full
description: "Full INC42 app v2 release scope reconciled from every source — Weekly App Review (24 Aug, closed), the two 20 Aug Satya design sessions, Ravi Kumar's critique, and the separate still-PROPOSED flags/feedback/ratings list — with data-check flags on which items are contradicted by behaviour data"
metadata: 
  node_type: memory
  type: project
  originSessionId: 59cedaa8-a793-4cf6-9ab8-edd7339fa0a4
  modified: 2026-09-04T06:36:28.489Z
---

Built 2026-08-24 at Ranjith's request ("everything you know — all meetings, in-person discussion, previous documents — what should be in app v2"). Two scope threads exist and are **NOT reconciled with each other** — flag this to Ranjith/Utkarsh before treating either as complete.

## Thread 1 — the "real" v2, CLOSED 2026-08-24 in Weekly App Review
Designs due Wed 26 Aug, release target 31 Aug (Utkarsh flagged this may slip to first week of Sept). Source: [[project-inc42-launch]] (24 Aug section), meeting id `d8fac763-3f4a-42a5-8fae-c77a03f1c628`.

1. **Explore → renamed "News"** — more prominence to news/article section; brief stays a feature, not the hero; left-to-right tab order kept, no center-tab pattern
2. **Homepage banner inventory** replaces the calendar/greeting block — team-controlled banner (CIO/Nityam/Ranjith editable), used to educate users on what "brief" is; the image below the banner stays backend-fetched, not personalizable
3. **Brief card redesign** — fix the "first image/first title vs first card" contradiction; add "personalized to you" messaging/loader before brief renders
4. **Data Labs filters redesign** (company sorting/filters)
5. **App-update banner fix** + a soft "update now" pop-up (explicitly **not** a forced/blocking update — rejected on the call as bad UX; only a dismissable prompt)
6. **Dark mode** — committed within 15–30 days; ambiguous whether it ships in the 31 Aug cut or slips past it
7. **Article page + company page redesign**
8. **Explore/News page cleanup** — remove the auto-popping filter (not user-initiated, flagged as a bad pattern)
9. **Singular deep-linking permanent fix** — install Singular SDK pieces directly in-app rather than relying on the current fragile setup; see [[project-inc42-deep-linking]]
10. **Double-tap-to-exit** on back button (prevents accidental app exit)
11. **Notifications: 1–2/day 1:1 news-based push, sector-segmented** not blanket; editor pings Slack for breaking/important stories, team builds the push manually for now (no automation yet)
12. **PostHog A/B test setup**: brief-first vs explore-first ingest, shorter version, for second half of September

## Thread 2 — pulled forward from the 20 Aug Satya design sessions (predates and feeds #3 above)
Source: meetings `64110c9d...` (Brief Page UI Enhancements) and `66923cf1...` (Brief Card UX Optimization), cross-checked against [[project-inc42-app-behaviour]]'s data.

13. Progress indicator on brief cards ("4/8, tap for next") — ✅ data-supported
14. 🔴 **CORRECTED — do NOT remove the past-brief/calendar card.** Original 20 Aug plan was "remove the card, single entry point." Ranjith overrode this (24 Aug), then simplified to exactly two CTA states — confirmed final, not "Read Past Brief" as an earlier guess in this thread wrongly assumed:
    - **Not yet opened today's brief**: CTA stays **"Read today's brief"** — unchanged from today's copy.
    - **Opened but not completed**: CTA reads **"Continue where you left off."** Clicking it must deep-link to the exact story/card the user last had open, not restart from card 1.
    Only two states, nothing else. A copy-addition + deep-link fix, not a structural removal. Update anywhere this was recorded as "remove past-brief card" (the app-behaviour memory's ✅ data-supported checklist, the v2 tracking Google Sheet row 3) to reflect this correction.
15. Editorial rewrites brief headline/content so it reads as a series of stories, not one article — ✅ data-supported
16. ⚠️ **Hide "Read full article" on brief cards** — protects brief completion but deletes 54 genuine reads (94% never return once they leave); prefer adding a **return path** ("back to your brief · 4 left") over hiding the button outright
17. ⚠️ **Relocate "Rate" to the freed space** — the rate control has **1 user in 8 days**, already flagged dead on the 1 Aug QA list. Verify it actually fires before promoting it or running interviews on "rate visibility."
18. ⚠️ **"Personalizing for you" loader before brief renders** — adds latency in front of the exact step that already loses 55% of users (card 1), on a surface where 9 users hit `load_failed`. Test, don't ship on assumption.
19. ❌ **Article-access MCP as a paid tier** — do not scope for v2. §11 of [[project-inc42-strategy-utkarsh]] explicitly rules out a second demand-side product line, and third-party data exposure needs a DPDP pass first.
20. ⏸️ **Articles/Companies as top-level tabs "powered by Data Labs"** — deferred until the brief-habit thesis is validated; today's meeting effectively re-confirmed this by keeping News (not Companies) as the co-equal tab with Brief.

## Thread 3 — Ravi Kumar's outside-in critique (21 Aug) — not yet decided, should inform v2 design calls
Source: [[project-inc42-app-ravi-critique]]. His core challenge — **merge Brief+Explore, go vertical not horizontal (Jacob's Law)** — was raised and explicitly discussed at today's 24 Aug review; Utkarsh kept them separate (see Thread 1 #1) and the horizontal-vs-vertical brief-card debate was left unresolved ("leaving it to people for now"). His smaller UI fixes are still open and cheap to fold in:

21. Streak: show the 1-day streak **first**, then ask to sign in to save it (currently backwards — asks before any gratification)
22. Article progress bar should run to the end of the **article**, not the end of the page
23. Companies tab should **lead with search**, not a discovery scroll
24. Changing a filter tab should **reset scroll to top**
25. "Recently funded" widget should show **amount raised + valuation**, not the generic card
26. **iOS push fix**: switch from silent/remote push to an **APS alert payload** (title/body/sound, ID in `data`) — root-cause fix for "push never fired"; independent of UI v2 but should ship alongside since notifications are explicitly in scope (Thread 1 #11)

## Thread 4 — sector-based brief images, decided twice, still unbuilt
Source: [[project-inc42-brief-images]]. Decided with Utkarsh 12 Aug, reconfirmed by Ranjith 24 Aug. Owner **Anmol**, no Asana ticket filed as of 24 Aug. ⚠️ Check sector coverage on briefs specifically before commissioning a full image set — 86% of articles carry no sector app-wide ([[project-inc42-content-personalization]]), so "dominant sector" may resolve to nothing for most briefs.

## Thread 5 — the OTHER "v2" scope, still PROPOSED not locked, NOT mentioned in today's 24 Aug close
Source: [[project-inc42-app-v2-release]] (session-authored 21–23 Aug, still tagged "ask before citing as agreed"). This is a **separate 10-item list** — feature flags, app-update mechanics, feedback loop, Play ratings — that has not been folded into or reconciled against Thread 1's closed scope. Someone (Ranjith/Utkarsh) needs to decide whether this ships as part of the same v2, or as v2.1:

- Feature flags: use **PostHog** (fail-closed, proxied endpoint) — owner Ritvik. Ranjith's instruction (24 Aug): drop the "un-halt / was paused" framing entirely when tasking this — state it plainly as "implement feature flags with PostHog," not as resuming halted work.
- App-config endpoint + build-number version gate (soft-prompt Android; **do not force-gate iOS**, 1.0 is locked with no update path until build ≥41)
- Play In-App Update API (flexible + immediate tiers)
- OTA feasibility check (expo-updates/CodePush) — highest-leverage item, feasibility still unconfirmed
- CIO in-app feedback prompt at brief-completion (median 78s), never after full-article webview exit
- Native "Send feedback" entry point, flag-gated
- In-app Play Store review flow, Android-only, behaviour-gated (≥3 completed briefs, no crash, ≥2 sessions) — **not** a sentiment-gate, that's a Play policy violation
- Review-reply alerting via Play Console API → n8n

## Thread 6 — instrumentation that should ride along with any v2 rebuild
Source: [[project-inc42-app-behaviour]]. Not a UI item, but breaks measurement of the v2 changes above if skipped:

- **Data Labs filters returning incorrect/no results — investigate whether Elasticsearch is functioning correctly** (indexing, query, uptime). Flagged by Ranjith 24 Aug. ⚠️ Distinct from the OTHER Elasticsearch item — server consolidation for cost savings, owned by Ranjith per [[project-inc42-weekly-team-leads-sync]] — don't conflate the two; this one is a functional correctness bug, that one is infra cost cleanup.
- Fix `app_installed` under-fire (~5% of users never fire it)
- Fix `summary_expanded` on `company_page` — wrongly carries `story_id` instead of `company_id`
- Instrument `decode` (the AI explainer) — zero telemetry today despite being the core positioning
- Confirm error taxonomy via SQL, not the PostHog panel (it only samples recent values — 403s may be silently swallowed client-side)
- Add `update_prompt_shown/dismissed/cta_tapped/update_completed` events if Thread 5's update-prompt work ships, or uptake is unmeasurable
- **App load is slow; 429 too-many-requests errors observed; Datadog shows a 4.77% overall error rate** (surfaced 21 Aug, [[project-inc42-unification]]-adjacent funnel session, meeting id `417df34b...`) — verify under low-network conditions, not yet confirmed fixed as of 24 Aug.
- **Flag/exclude internal users in PostHog** — now fully specified in the 25 Aug events-fix ticket (source: [[project-inc42-posthog-review]], confirmed 17 Aug, full doc at `~/Downloads/Posthog Review 2026 08 17.md`): add an `is_internal` person property (@inc42.com + pre-Aug-12 cohort) + a PostHog cohort applied as the default dashboard filter.

**Events-fix Asana ticket, finalized scope (25 Aug):** https://app.asana.com/1/176734136274/project/1216274779493698/task/1217810326370973 — Ritvik, project Inc42 App. Went through two revisions same day: first draft was a wide multi-column table (unreadable), rebuilt as 5 short bulleted sections; then Ranjith cut it further to **only unambiguous, ready-to-build fixes** — anything needing a prior "verify/confirm" step was dropped from the ticket entirely, not just reworded. Final scope, 10 items across 5 groups:
- Dead/duplicate events: remove `brief_open_today` (dead since Jul 13); dedupe `story_unsaved`+`company_untracked`+`industry_untracked` into one (all duplicate `watchlist_entity_removed`)
- Add to v1.5 dictionary (firing, undocumented): `walkthrough`, `brief_story_rated`, `sign_in_prompt_shown`, `share_initiated`, `push_priming_dismissed`, `app_installed`
- Property fixes: missing `onboarding.step_name` values (watchlist/push_prompt/signin_prompt); implement `brief_page_opened.is_edition_switch`; exclude `auth_callback` from `deep_link_opened`
- Internal-user exclusion: `is_internal` person property + "Internal & beta" cohort as default dashboard filter
- North star: define `completed_engaged` = `brief_completed` WHERE `duration_sec >= 60`, report that instead of raw completion

**Deliberately dropped from the ticket — real findings, not yet a task, offered to file separately (Ranjith hadn't answered as of 25 Aug):**
- `decode` — needs Ranjith to confirm whether it's even shipped before scoping the instrumentation fix
- `interest_captured`/`locked_feature_tapped`/`watchlist_limit_hit` (monetization dataset) — needs confirming the gates exist in the build
- `push_delivered` — the review's own #1-ranked action item, but the actual fix depends on why push is dark (integration unfinished vs deliberately held), unknown
- `brief_fallback_shown`/`rating_prompt_shown`/`force_update_shown` — needs confirming intentional vs not shipped
- `brief_opened.source` (only ever "organic") — needs confirming deep-link attribution wiring
- register-vs-sign-in anomaly (110 signed in, only 25 registered) — needs verifying which is true before it's actionable
If any of these get confirmed, they still need their own ticket — this list is not tracked in Asana anywhere yet.
- **Fix streak: count same-day on first login/signup** — on first login the streak should register for that day, not start blank until day 2. New instruction, 24 Aug. Asana ticket created 25 Aug: https://app.asana.com/1/176734136274/project/1216274779493698/task/1217799709962157

## Thread 7 — AskInc42, a separate major feature with its own 17-decision PRD, NOT mentioned in the 24 Aug v2 close
Source: [[project-inc42-askinc42]], PRD v6 at `AskInc42_PRD_v6.docx` / artifact `320582bd-1b52-495f-9980-92310d6621e8`. Sequencing was locked 31 Jul: **AskInc42 ships before [[project-inc42-social-intelligence]] (Pulse)** — but it was not raised in today's Weekly App Review, and Thread 1's "v2" scope contains nothing that matches it. Two live possibilities: it's meant to land in this same v2 cut and got dropped from the agenda, or it's tracked as its own separate release. Flag before assuming either.

Locked scope if/when it does ship:
- **v1 placement: brief-end** (swap the existing "Explore Trending Stories" carousel for Ask chips, same cards + new CTA, not a new block) **+ Watchlist/company page** Ask entry points; article-detail secondary
- Logged-in only; auto-fires the seeded question on tap (or post-login)
- Two modes: **Fast** (cached, target 5s / never exceeds 10s) vs **Deep** (Datalab-grounded, never exceeds 30s) — current backend runs 8–25s, already over the Fast ceiling
- Chat history persistent + thumbs up/down feedback
- 5 personas (Founder / Investor / Operator / BD & Partnerships / Other), each with a distinct question "lens," not exact templates
- No paid gating for now (earlier Free/Plus tier idea dropped)
- Response format: ~150–200 words, no Markdown tables, tappable citation cards not inline links
- Delayed-response push notification if the app is closed before an answer finishes
- ⚠️ **DPDP gap**: live Privacy Policy §5.1 already names AI features as active, but no LLM sub-processor is disclosed anywhere and no DPA/zero-retention terms exist on file — raise with Utkarsh independent of the main 3-phase DPDP engagement, don't wait for it.
- Brief-end placement is "pending data," not fully confirmed — needs `brief_completed` rate pulled from the warehouse before being locked as primary (this data likely now exists per [[project-inc42-app-behaviour]]'s 18% completion figure — worth closing this loop).

## Thread 8 — older items, surfaced across July, not confirmed done or reconciled as of 24 Aug
Carry these forward rather than treating Thread 1 as the complete list — they predate the recent run of meetings and nobody has said they shipped.

- **Card copy fix, still open as of 29 Jul**: "✦ Read more (takes 30 seconds)" is contradictory (open-ended "read more" + a promised end time) and fights the app's anti-infinite-scroll positioning. Recommended, not yet confirmed: **`30-sec summary`** or **`Summary · 30 sec`** for the summary block, with the full article getting its own separate **`Read full story →`** CTA. Directly overlaps Thread 1 #3 (brief card redesign) — fold in.
- **Sector-tagging P0s** ([[project-inc42-content-personalization]]): 86% of articles have no `Company_Industries` → sector personalization is structurally dead, not a bug. Fix tagging or drop sector selection from onboarding; add the 6 unmapped industry values (Social Media, Ride Hailing, Quick Commerce, AR/VR, Kitchenware, TBD) to the sector map; add a per-topic diversity cap so briefs aren't monotone (currently a Deals follower gets 10/10 Deals articles). Same root cause as Thread 4's sector-image problem.
- **20-item QA bug list shared 1 Aug, zero confirmed fixed as of 29 Jul** ([[project-inc42-open-items]]) — the ones not already folded into Threads 1–3 above: onboarding notification-permission prompt moved to 2nd screen; Continue button stays enabled with a "choose at least two sectors" validation error instead of being disabled; remove em dashes app-wide; shrink brief-card title; Streak page spacing/overlap fix + keep both nav arrows visible but disable the unavailable direction; company filter bottom sheet capped to 50–70% screen height; Sort By swaps "Headcount Change" → "Total Revenue"; reduce top whitespace on Featured Article; move the bottom nav/CTA action section up; drop "Today's Brief" label from the brief header, keep only branding; "Saving..." should persist until the save action actually completes, not show "Saved" early; tighten spacing around name/Enterprise tag on Companies-in-the-News; guest users must hit a login prompt on interaction (currently don't). Plus 3 follow-ups: tag inline-article-mention opens with a distinct source/campaign so they're separable in analytics; finalize Articles/Companies pill order with Editorial; create a CRM doc listing identified CRM use cases.
- **Cross-platform onboarding unification**: skip onboarding questions already answered on another Inc42 property, unify field/value conventions across web/app/DataLabs (raised 21 Aug, [[project-inc42-fy27-plan]]-adjacent planning session) — distinct from, but related to, the "unified navigation" item Team Leads Sync flagged as needing its own one-pager.

## Thread 9 — surfaced from Utkarsh's LOCKED FY27 plan (21 Aug) and strategy corpus (13 Aug), not previously cross-checked against v2
Source: [[project-inc42-fy27-plan]] (authoritative, supersedes [[project-inc42-strategy-utkarsh]]), 24 Aug Utkarsh feedback on the Sep MOP.

- **Employer + seniority capture must move to app SIGN-IN, not signup.** 198 app persons have `role` captured, **zero** have `employer` — org type is literally half the QIA-qualified-user definition. Sign-in outnumbers register ~4:1, so a signup-only ask permanently caps capture at ~¼ of touchpoints. Not in Thread 1's closed scope — needs a decision on whether it folds into this v2 or Sep goal 06 (unified onboarding).
- **App events emit but never reach the warehouse**: `app_session`, watchlist, search/profile-view. Wiring these in recovers 3 QIA-qualifying actions at once — depends on the Sep event-fix goal landing first. Add to Thread 6 instrumentation.
- **Unified front-end changes across web/app/DataLabs are explicitly blocked** pending the whole team agreeing one unification plan first (per Utkarsh's 24 Aug MOP feedback, referencing the same-day Team Leads Sync discussion) — so the "unified navigation" one-pager Thread 8 flagged isn't just undone, it's structurally gated.
- **Ask (AskInc42) "streaming/fast mode + in-app" is recorded as already shipped 21 Aug** in the FY27 plan's Locks — this may mean some version of Fast mode already exists independent of Thread 7's full brief-end-carousel-swap PRD. Reconcile what's live today against the PRD before assuming Thread 7 is entirely unbuilt.
- **Reassurance, not a live conflict**: the 13 Aug strategy corpus (§11) once called the app "a PILOT, not the committed strategy — few hundred users, no store listing." The 21 Aug FY27 plan, which is more recent and explicitly LOCKED, states plainly **"App is the primary acquisition + engagement surface."** The later, locked doc supersedes the earlier one — no reconciliation needed, just don't cite the "app is a pilot" framing as current.

## Thread 10 — Ranjith's own canonical v2 scope doc, 19 Aug — found 25 Aug, was missing from the tracking sheet entirely
Source: `~/Downloads/Inc42 App v2 Scope.md`. 11 workstreams, built directly on [[project-inc42-posthog-review]]'s 17 Aug findings + an 18 Aug deep-linking Slack thread + the event dictionary v1.4. This is a MORE authoritative source than the meeting-transcript compilation Threads 1–9 were built from — reconcile against it, don't just append.

| # | Item | Priority | Status vs Threads 1–9 |
|---|------|----------|------------------------|
| 1 | Updated events (full instrumentation reconciliation) | **P0** | Became the 25 Aug Asana ticket; overlaps but is more complete than Thread 6 |
| 2 | Datalabs fixes | ⚠️ needs input, undefined in the doc itself | Likely the same gap as the 25 Aug "Investigate Elasticsearch — Data Labs filters" ticket — the doc explicitly says "not yet specified," Ranjith's Elasticsearch instruction may be the missing detail |
| 3 | AskInc42 v2 (3 stored onboarding Qs, web search stays on) | P1 | Matches Thread 7, adds detail: blocked on an API from Anmol not yet raised, and on feature flags (currently halted) |
| 4 | **Dummy screen before 7am** (brief hasn't dropped yet) | P2 | **NOT in Threads 1–9 or the sheet at all.** Open decision: countdown placeholder vs show-yesterday's-brief-with-banner |
| 5 | Tap-again-to-exit | P3 | Matches Thread 1 #10 |
| 6 | Deep linking (newsletter links open Safari not app) | **P0** | Matches Thread 1 #9 / [[project-inc42-deep-linking]], with a fuller root-cause writeup (CIO click-tracker breaks Universal/App Links) |
| 7 | Singular setup revision (campaign=None attribution) | **P0** | Not previously in the v2 threads as its own item — was only in acquisition/tracking memories. Time-critical, was tied to the D2C Summit date |
| 8 | Brief page — design revisit | P1 | Matches Thread 1 #3 / Thread 2, adds the data backing (cover→brief 41%, 7s median) |
| 9 | **Separating Datalabs** (own surface/section — nav split? separate app?) | ⚠️ needs input | **NOT in Threads 1–9 or the sheet.** Explicitly gates item #10. Relation to the One-Inc42 unification direction unconfirmed |
| 10 | Redesign Datalabs + article section | P2 | Overlaps Thread 1 #7, blocked on #9 |
| 11 | Sector images + Dark mode | P2 | Matches Thread 1 #6 / Thread 4, same 86%-sector-tag-gap caveat |

**Genuinely new items to add to the tracking sheet**: #4 (dummy screen before 7am) and #9 (separating Datalabs) have no prior representation anywhere in Threads 1–9. #2 (Datalabs fixes, undefined) and #7 (Singular setup revision) should be added as their own explicit rows rather than left folded into other items.

**Open questions the doc itself flags, still unresolved as of 19 Aug:** what exactly is broken in #2 · full scope/intent of #9 · owners for #4/#8/#10/#11 (Satya?) · confirm P0 order is #1/#6/#7 · #11 fix-tagging vs generic-fallback vs dark-mode-only · #4 countdown vs show-previous.

## Thread 11 — "Beyond Brief" homepage redesign, design conclusion reached 29 Aug via PostHog deep-dive
Source: [[project-inc42-app-explore-deep-dive]]. Not yet raised in a Utkarsh-facing meeting — a design conversation Ranjith worked through directly, resulting in a concrete resolved proposal:
- Remove the calendar strip from the Brief home page; consolidate to the "Past Briefs" carousel as the sole past-navigation entry point (both currently exist, split is unmeasurable — see the deep-dive memory).
- Add unread/started/read visual states to Past Briefs cards, derivable from existing `brief_opened`/`brief_completed` events, no new instrumentation needed.
- Add a "companies mentioned in today's brief" module, framed as a standalone unit ("Today's Startup Movers," not "Mentioned today" — the latter presupposes brief-reading context the target non-Brief-reading audience won't have), using real cards (name + one fact) not bare chips, placed directly below the Today's Edition card so it's visible without completing or even opening the brief.
- Sequencing: ship the calendar/Past-Briefs consolidation first (low risk), the companies-mentioned module second (needs a company-name alias table + source-tagging + editorial sign-off on sensitive mentions first), a rotating "Beyond Brief" filter-teaser last (needs a content-freshness rule from Content/DataLabs that doesn't exist yet).
- This directly unblocks on the sector/company-tagging correction in [[project-inc42-content-personalization]] — previously thought infeasible, now confirmed viable (67.7% of articles fully tagged, 91-94% DataLabs match rate).

## Thread 12 — text overflow on article cards, reported by Utkarsh 4 Sep 2026, MUST be in v2
Slack screenshot: card with left thumbnail + "FILM & THEATRE →" sector chip + headline + "Debarghya Sil · 3 Sep 26" byline + a "30-sec summary" expander row. Headline **"KKR Backs BookMyShow As Live Entertainment Becomes Its Next G"** is hard-clipped mid-word at the container edge, **with no ellipsis** — the text runs past the card boundary rather than truncating.

**Surface not yet confirmed.** The anatomy (thumbnail-left, byline, separate 30-sec-summary expander) does NOT match the brief story card described in [[project-inc42-app-story-card-redesign]] (masthead, 8-segment progress bar, 390x338 hero, "THE DECODE", red-triangle bullets). Most likely Explore → Articles list card or the article page header. **Ask before routing the ticket.**

### Sizing — measured 4 Sep against 100 live headlines (`inc42.com/wp-json/wp/v2/posts?per_page=100`)
Visible budget on the broken card is ~61 characters across 2 lines.
| Headline length | Share of articles |
|---|---|
| median | **65 chars** |
| mean | 63.4 |
| max | 99 |
| >55 chars | 79% |
| **>60 chars** | **63%** |
| >70 chars | 29% |
| >80 chars | 6% |

**The median headline overflows this card.** ~63% of everything published breaks it. This is the normal case, not an edge case. Designing containers to hold **80 characters covers 94%** of headlines.

### Root cause candidates, most likely first
1. **Flex child won't shrink** — text column has default `min-width: auto` (web) / no `flexShrink: 1` (RN), so it refuses to go below its intrinsic content width and overflows the card. This is the classic cause of *exactly* this symptom in a thumbnail-left row card.
2. Fixed height + `overflow: hidden` with no `text-overflow: ellipsis` / no `-webkit-line-clamp`.
3. Line clamp set but the parent has no width constraint to clamp against.

Fix is `min-width: 0` (web) or `flexShrink: 1` (RN) on the text container **plus** an explicit 2-line clamp with tail ellipsis on the headline. Both halves are needed; either alone leaves a defect.

### Supersede check — related but NOT the same item
- **"Shrink brief-card title"** is already on the 1 Aug 20-item QA list (Thread 8), zero confirmed fixed. That is a *font-size* fix on the *brief* card. **Not a duplicate** — shrinking type does not fix an unclamped overflow, and this is probably a different surface.
- Thread 1 #3 (brief card redesign) and the V28 set would absorb it **only if** this turns out to be the brief card.

### The systemic finding — this is the third instance of one root problem
1. V28 story card: "What's new / Why it matters / The detail are long and will not fit" — confirmed against real Ola Electric copy
2. 1 Aug QA list: "shrink brief-card title"
3. This report

**Cards are being designed against short placeholder copy and breaking on real copy.** The V28 round already recorded the method fix ("stopped using invented copy, V28 uses a real story end to end") but that lesson was never applied to the other cards. The v2 item should therefore be a **rule, not a patch**: every text container declares a max line count with ellipsis, and every card design is reviewed against an 80-character headline before sign-off.

### Acceptance criteria
- No headline in the corpus renders past its container edge on any card, any surface
- Truncated text always ends in an ellipsis, never a cut glyph
- Verified against the longest live headline (99 chars) and at the largest OS text-size setting
- Verified at the narrowest supported device width

**Status:** not yet filed in Asana as of 4 Sep 2026. Related: [[project-inc42-app-story-card-redesign]], [[project-inc42-brief-card-corpus-analysis]].

## Possible unreconciled overlap — flag, don't assume
**"B2"** ([[project-inc42-app-placement]], 10 Aug, owner Satya) — placing Inc42 editorial/news content inside the app, design-only so far. This sounds like it could be the same initiative as Thread 1 #1 (Explore → News rename, more prominence to the news section) under an earlier working name, or it could be a separate, narrower placement decision. Never explicitly reconciled in any session since. Ask Ranjith/Satya directly before assuming either.

**How to apply:** when asked "what's in v2," lead with Thread 1 (what's actually closed and dated) and flag Threads 2–4 and 6–8 as feeding into or predating it. Explicitly surface the Thread 1/Thread 5/Thread 7 non-reconciliation, the "B2" naming overlap, and the ⚠️/❌ data-contradicted items rather than presenting everyone's wishlist as equally decided.
