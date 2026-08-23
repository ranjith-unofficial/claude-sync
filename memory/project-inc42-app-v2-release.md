---
name: project-inc42-app-v2-release
description: "INC42 app v2 release scope — feature flags, feedback loop, Play Store ratings, and app-update/version-gate mechanics"
metadata:
  node_type: memory
  type: project
---

Scoping work done **2026-08-21/23** for the **INC42 app v2 release**, covering four things Ranjith asked to bring in: **feature flags, feedback loop, Play Store ratings, and app updates (incl. the update pop-up)**.

⚠️ **Status: PROPOSED, not locked.** These are recommendations produced in session, not decisions Ranjith or Utkarsh have signed off. Ask before citing any of it as agreed.

## The dependency chain

Flags first — because Animesh already closed the real constraint ([[project-inc42-launch]]): anything shipped inside a binary needs users to **update**, and there are almost no users to update. Flags + server-driven Customer.io in-app messages make downstream surfaces changeable without a store cycle.

`Feature flags → version gate → feedback loop → rating prompt`

## 1. Feature flags — use PostHog, add no vendor

- **PostHog** (already in the app, EU, same `distinct_id` as analytics) beats Firebase Remote Config (app-only, US, separate identity) and LaunchDarkly/Statsig (new vendor → DPDP + Play Data Safety cost, see [[project-dpdp-compliance]], [[reference-inc42-vendor-stack]]).
- **At ~189 users, flags are NOT for A/B testing** — no v2 experiment reaches significance. Sell them as release safety + kill switch + remote config, or you get asked for results that can't exist. See [[project-inc42-app-behaviour]].
- Guardrails: **fail-closed** (no network → feature OFF); bootstrap flags at start or the Brief flickers; every flag needs an owner + kill date; flag exposure events must go into Bhavika's event audit.
- ⚠️ PostHog is reverse-proxied at `posthog.inc42.com` — **the flag-evaluation endpoint must be proxied too**, not just `/capture`, or flags silently return defaults in prod.
- **Blocker:** feature-flag work is *halted*, owner **Ritvik Sethi**, paused for AskInc42 UI placements ([[project-inc42-askinc42-next-week]]). Needs explicit re-scoping into v2 or it stays parked.

## 2. App updates — three tiers

| Tier | Mechanism | Store review | Use for |
|---|---|---|---|
| 0. OTA | `expo-updates`/EAS Update or CodePush, JS bundle only | none | copy, thresholds, JS bug fixes |
| 1. Flexible | Play In-App Update API, flexible mode | normal | routine native releases |
| 2. Immediate | Play In-App Update API, immediate mode (blocking) | normal | security/compliance, breaking API change |

- **OTA (#5 in scope) is the highest-leverage item of the whole plan** — if the RN setup supports it, the "no users to update" constraint dissolves for everything JS-side. Feasibility unconfirmed; Ritvik to check. Policy edge: bug fixes/copy fine, whole new features via OTA = no.
- Play **staged rollout** (5%→20%→100%, halt on crash spike) is a separate free lever and should be standing practice, not a build item.

## 3. Version gate + the update pop-up

- **Own the config server-side** (PostHog flag payload or `/app-config`). Do **not** use the iTunes lookup API or Play's own check — cached, and they get staged rollouts wrong.
- **Gate on build number, not marketing version** — iOS 1.0 already carries build 40, so the two have diverged.
- Config shape: per-platform `minSupportedBuild` / `recommendedBuild`, `softPromptCooldownDays`, plus title/body/CTA copy so messaging changes without a release.
- States: `< min` → **blocked**, non-dismissable, single store CTA; `>= min < recommended` → **soft**, dismissable with cooldown; else nothing.
- **Where the pop-up shows:** cold start and foreground-resume, **after splash, before the Brief renders**. Never mid-brief (card 1 is already the 45%-advance loss point), never over a webview article. Suppress on a user's first session post-install.
- **Fail-OPEN on the update gate** if config fetch fails (opposite of flags, which fail closed).
- On Android prefer the **native Play immediate flow** over a custom screen; the custom blocking screen is the iOS-only path (`itms-apps://`).
- Telemetry: `update_prompt_shown` (type/current_build/target_build), `..._dismissed`, `..._cta_tapped`, `update_completed` — without these you can't tell low uptake from a prompt that never fired (the daily-brief-push failure mode).

### 🔴 Two situation-specific blockers
1. **Do not enable a forced gate on iOS.** 1.0 is locked, 1.0.1 has no build attached → iOS users *cannot* update. A force gate bricks them until build ≥41 ships. Keep `ios.minSupportedBuild` at the live build.
2. **In-app updates can't be tested in debug/sideloaded builds** — the app must come from Play. Ritvik needs the **internal app sharing** track.

## 4. Feedback loop

At N=189, qualitative wins — **skip NPS, it's meaningless at this size.**

| Channel | Mechanism | Trigger |
|---|---|---|
| Prompted | Customer.io in-app message (server-driven, no release to change) | brief completion (median 78s = the earned moment) or 3rd session |
| Always-on | native "Send feedback" in profile, flag-gated | user-initiated — catches the angry user before Play Store |
| Push | FCM via CIO, deep link | ad-hoc; Animesh's exclusives-for-feedback idea |

- ❌ **Never** after a full-article webview exit — 94% never return, so it's asking at the moment of abandonment. ❌ Never at brief card 1.
- **Open:** where free text lands. New vendor (Instabug/Sprig) = privacy policy + Data Safety update. Cheapest compliant path = CIO form → existing backend. Don't dump free text into PostHog (input masking is ON by design; don't route around it).
- ⚠️ Push-based feedback links inherit the **CIO click-tracker deep-link bug** (opens Safari, not the app) unless routed via Singular — see [[project-inc42-deep-linking]].

## 5. Play Store ratings

- Mechanism: Play **In-App Review API** (`ReviewManager.requestReviewFlow()` → `launchReviewFlow()`); iOS `SKStoreReviewController`. RN wrapper (`expo-store-review` / `react-native-in-app-review`) to be confirmed against the actual stack with Ritvik.
- Three constraints: Google quota-limits the sheet (**you cannot guarantee it shows**; iOS caps at 3/365 days); **no callback** on whether the user rated, so rating conversion is unmeasurable — only prompt attempts vs Play Console rating delta.
- 🔴 **Play policy forbids pre-qualifying the prompt** — no questions before or during the review flow. **This kills the standard sentiment gate ("Enjoying Inc42?" → happy to store / unhappy to form). Do not build it.**
- Compliant equivalent: **gate on behaviour, not a question.** A PostHog cohort/flag decides eligibility (≥3 completed briefs, no crash in session, ≥2 sessions); eligible users get the native sheet with no preamble. Everyone else only ever sees the feedback surface.
- Timing: right after a completed brief — the finish state, which is the "actually finish" positioning.
- **Prereqs:** fix Android defects first (missing 24dp notification icon, webview failure states) — at ~200 installs three 1-stars set the visible rating for months; and rating prompt is **Android-only** until iOS build ≥41 ships.
- **Close the loop on Play's side:** Play Console **Reply to Reviews API** → n8n → alert on any ≤3★. Public replies move the visible rating meaningfully at low review counts and are the only public-facing part of the system.

## Proposed v2 scope (10 items, owners)

1. PostHog flags: SDK, proxy config, fail-closed defaults — Ritvik (un-halt parked task)
2. App-config endpoint / flag payload + build-number gate — Ritvik
3. Play In-App Update API (flexible + immediate) — Ritvik (needs internal app sharing)
4. iOS version-check screen — Ritvik (gated on build ≥41 live)
5. **OTA feasibility check (expo-updates / CodePush) — Ritvik — investigate first, highest leverage**
6. Flag + update exposure events into the audit — Bhavika
7. CIO in-app feedback prompt, brief-completion trigger — Ranjith + Ashish (gated on deep-link fix)
8. Native feedback entry, flag-gated — Ritvik
9. In-app review, behaviour-gated, Android only — Ritvik (gated on Android defects)
10. Review-reply alerting via Play API → n8n — Ranjith (independent, can start now)

**Open decisions:** feedback storage destination; review-eligibility thresholds (must be *picked*, not derived — no data at N=189); whether flag work comes out of Ritvik's DataLabs-split bandwidth or gets an explicit swap with Utkarsh ([[project-inc42-askinc42-next-week]]).

**Not yet written up as a PRD** — offered to draft it into `~/ClaudeDocs/inc42/`, Ranjith hasn't asked for it yet.
