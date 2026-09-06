# Inc42 App — v2 Scope

**Date**: 2026-08-19 · **Owner**: Ranjith · **Status**: Draft for team alignment
**Source inputs**: PostHog first-week review (2026-08-17), Aug-18 deep-linking Slack thread, event dictionary v1.4

11 workstreams. Priorities are proposed defaults. ⚠️ = needs input before it can be scoped. Effort = rough T-shirt (S <2d · M 2–5d · L >1wk).

---

## Summary table

| # | Item | Type | Owner | Priority | Effort | Depends on |
|---|------|------|-------|----------|--------|-----------|
| 1 | Updated events | Instrumentation | Ranjith + Eng | **P0** | M | — |
| 2 | Datalabs fixes | Bug/backend | ⚠️ | ⚠️ | ⚠️ | — |
| 3 | AskInc42 | Feature | Ritvik | P1 | L | Anmol API |
| 4 | Dummy screen before 7am | UX | Design + Eng | P2 | S | — |
| 5 | Tap-again-to-exit | UX | Eng | P3 | S | — |
| 6 | Deep linking | Bug | Nityam + Eng | **P0** | M | #7 |
| 7 | Singular setup revision | Attribution | Eng + Marketing | **P0** | M | — |
| 8 | Brief page — design revisit | UX/CRO | Design | P1 | L | #1 |
| 9 | Separating Datalabs | Architecture | ⚠️ | ⚠️ | L | strategy |
| 10 | Redesign Datalabs + article section | Design | Design | P2 | L | #9 |
| 11 | Sector images + Dark mode | UX | Design + Eng | P2 | M | ⚠️ sector data |

---

## 1. Updated events — P0

**Problem**: Event dictionary v1.4 has drifted from the shipped app in both directions — specced events that never fire, and live events not in the dictionary. Half the v1 metrics can't be trusted.

**Scope**
- **Fire the dark events** (in dictionary, 0 fires all-time):
  - `push_delivered` — retention/OEM-delivery trip-wire; blocks the entire CRM layer readout
  - `decode` — the AI explainer; the whole "AI that explains it for you" positioning has zero telemetry
  - `interest_captured`, `locked_feature_tapped`, `watchlist_limit_hit` — v1 monetization dataset (specced "clean day 1", currently empty)
- **Reconcile off-spec events** (firing, not in dictionary): `walkthrough` (104 users), `brief_story_rated`, `sign_in_prompt_shown`, `share_initiated`; dedupe the 3 untrack events (`story_unsaved` + `company_untracked` + `industry_untracked`) into one; remove dead `brief_open_today`
- **Property gaps**: add missing `onboarding.step_name` values (watchlist / push_prompt / signin_prompt); implement `is_edition_switch`; exclude `auth_callback` redirects from `deep_link_opened`
- **Internal-user tagging**: `is_internal` person property (@inc42.com + pre-Aug-12 cohort) + a "Internal & beta" cohort as default dashboard filter
- **North-star fix**: adopt `completed_engaged` = `brief_completed` where `duration_sec ≥ 60`

**Acceptance**: dictionary v1.5 published + signed off by eng; every event in v1.5 either fires in prod or is explicitly deprecated; internal traffic excludable from all dashboards.

---

## 2. Datalabs fixes — ⚠️ needs input

**Problem**: ⚠️ Not yet specified.
**Need from you**: which surface, what's broken, expected vs actual behaviour, affected build/platform.
**Structure once known**: bug list → root cause per bug → owner → acceptance. Placeholder until detailed.

---

## 3. AskInc42 — P1

**Context**: v1 (brief-end swap + Watchlist/company page) shipped. Ships **before** Pulse. Owner: Ritvik Sethi.

**Scope (v2)**
- **3 stored onboarding questions** — captured at onboarding, persisted to personalize AskInc42 answers
- Web search stays ON (Perplexity)

**Dependencies / blockers**
- Needs an **API from Anmol** — **not yet raised with him** (raise first)
- Feature flags currently **HALTED** — unblock or route around

**Acceptance**: 3 onboarding Qs captured + stored; AskInc42 answers reflect stored context; API contract with Anmol agreed.

---

## 4. Dummy screen before 7am — P2

**Problem**: The brief publishes 7am IST. Users opening before drop hit an empty/undefined state.

**Scope** — pick one behaviour:
- (a) Placeholder: "Today's brief drops at 7am" + live countdown, or
- (b) Show yesterday's brief with a "New brief at 7am" banner

**Approach**: gate on server publish-time, not device clock (timezone safety). Handle the 6:59→7:00 transition without a manual refresh.

**Acceptance**: opening pre-7am shows the chosen state; auto-updates to today's brief at drop without app restart.
**⚠️ Decide**: (a) countdown vs (b) show-previous.

---

## 5. Tap-again-to-exit — P3

**Problem**: On Android, a single back-press from the home tab exits the app — accidental exits.
**Scope**: standard "Tap again to exit" toast — first back shows toast, second within ~2s exits.
**Acceptance**: single back on root tab shows toast + stays; double-back exits; only on root (not nested screens). Low effort.

---

## 6. Deep linking — P0

**Problem**: Newsletter links open in Safari instead of the app — iOS (Safari + in-app webviews) and some Android. Direct browser taps of `inc42.com/...` work; newsletter-wrapped links don't.

**Root cause**: The Customer.io click-tracker redirect breaks Universal Links / App Links — iOS checks the app association against the *first tapped domain* (the tracker), not the final URL; the tracker isn't in AASA. Android App Links need `assetlinks.json` + domain verification on the tapped domain (fails the same way).

**Scope / fix**
- Route newsletter article links through **Singular smart links** (see #7) — carries the app-link association + attribution
- Verify AASA at `https://inc42.com/.well-known/apple-app-site-association` — `Content-Type: application/json`, **no redirect**
- Verify Android `assetlinks.json` at `/.well-known/`, `autoVerify=true`, domain verified
- Server-side 301/302 only — no JS/interstitial hop
- Don't wrap app-destined links in the CIO tracker (or register the tracker domain in AASA/assetlinks)

**Acceptance**: tap from Gmail + Apple Mail on iOS and Android opens the in-app article; verified on Safari and in-app webviews. Repro link: `inc42.com/buzz/razorpay-launches-ai-foundation-model-vulcan…`
**Note**: Nityam has additional pointers — fold in.

---

## 7. Singular setup revision — P0

**Problem**: Deep links arrive with `campaign = None` → Summit (QR tent-card) and any campaign installs are unattributable.

**Root cause**: same as #6 — links not routed through properly configured Singular smart links.

**Scope**
- Rebuild Singular smart-link config so `campaign` / `source` / `medium` populate on click
- Wire `brief_opened.source` to read the deeplink attribution (currently only ever "organic")
- Validate the QR → preloaded-onboarding path end-to-end

**Acceptance**: a campaign smart link produces a non-null `campaign` in PostHog + Singular; Summit QR installs attributable. **Time-critical** for campaign attribution.

---

## 8. Brief page — design revisit — P1

**Problem (data-backed)**:
- **Cover→brief cliff**: 99 users saw the cover, 41 tapped in (**41%** — the biggest funnel drop)
- **Completion quality**: median completion 7s; half of "completions" <10s — the brief is flicked, not read

**Scope**
- Treat the brief cover as a **conversion surface** — stronger/clearer CTA, or auto-advance into card 1 (kill the dead-end cover)
- Redesign the card flow so a genuine read is the default path (pacing, dwell nudges)
- Instrument against `completed_engaged` (#1) so we can measure the fix

**Watch-item**: Explore beats Brief today (69% vs 31%). Re-read after the cliff is fixed — if Explore still wins with a working brief entry, that's a v1.1 strategy signal, not a bug.

**Acceptance**: cover→brief conversion up from 41%; engaged-completion (≥60s) share rises; no regression in card drop-off curve.

---

## 9. Separating Datalabs — ⚠️ needs input

**Problem / intent**: ⚠️ Split DataLabs into its own surface/section — scope undefined.
**Need from you**: is this a nav split, a separate section, or a separate app? Relation to the One-Inc42 / unification direction? This gates #10.
**Structure once known**: IA change → nav model → migration of existing Datalabs content → acceptance.

---

## 10. Redesign Datalabs + article section — P2

**Context**: Pairs with #9 — scope depends on that decision.
**Scope (provisional)**: redesign the Datalabs surface + the article-reading section (typography, layout, in-article actions).
**Dependency**: blocked on #9's IA decision. Design owner TBD (Satya?).
**Acceptance**: TBD once #9 is defined.

---

## 11. Sector images in brief card + Dark mode — P2

**Scope**
- **Dark mode**: full theming pass across app surfaces
- **Sector-based images**: brief cards show imagery keyed to the story's sector

**⚠️ Data caveat (important)**: **86% of articles currently have no sector tag** — the same gap that shelved sector personalization. Sector-based imagery will only cover ~14% of cards unless sector-tagging is fixed first.
- **Decision needed**: (a) fix sector tagging first, (b) ship with a generic fallback image for untagged cards, or (c) defer sector images and ship dark mode alone.

**Acceptance**: dark mode toggles cleanly across all screens; sector images render per the chosen fallback strategy without blank cards.

---

## Open questions before locking scope
1. **#2 Datalabs fixes** — what exactly is broken?
2. **#9 Separating Datalabs** — full scope + intent (unification link)?
3. **Owners** for design items (#4, #8, #10, #11) — Satya?
4. **Priority order** — confirm P0s = #1, #6, #7.
5. **#11 sector images** — fix tagging first, generic fallback, or dark-mode-only?
6. **#4 dummy screen** — countdown vs show-previous-brief?
