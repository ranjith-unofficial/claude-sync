---
name: project-inc42-app-attribution-architecture
description: "Inc42 app source attribution — 3-layer model (attribution_/entry_/referrer_), measured 6 Sep 2026; deep_link_opened is 54% noise, UTMs 0%"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4aa6f516-654e-40d9-8de5-e8592aa32fba
  modified: 2026-09-06T16:14:54.815Z
---

Inc42 app **source attribution & journey mapping** design, worked out 6 Sep 2026. Spec at
`~/ClaudeDocs/inc42/app-attribution-source-mapping-spec.md`. **Proposed, not approved.**

## The core defect
One property, `source`, answers two incompatible questions — external channel AND in-app
screen. `brief_page_opened.source` holds `organic`/`deeplink` alongside `brief`/`explore`/
`watchlist`/`profile`/`streak`. Since they're mutually exclusive values of one field, neither
question is answerable, and the combined one ("which channel drives brief completion?") is
impossible.

## LOCKED design decisions (Ranjith chose both, 6 Sep)
Three layers, distinct prefix each, **no property may hold values from two layers**:
- **`attribution_*`** — install, person props, immutable (Singular postback + Play referrer + Apple `ct`)
- **`entry_*`** — session entry, PostHog **super properties** via `posthog.register()`, rewritten every session
- **`referrer_*`** — in-app origin, event property (`referrer_screen`/`_position`/`_module`)

1. **`referrer_screen`** chosen over `from_screen`. He picked it despite the flagged risk that
   "referrer" reads as *external* origin. Naming guard must be documented: `referrer_*` =
   in-app only, `entry_*` = external.
2. **Delay `app_opened` up to 1,500 ms** on cold start until attribution resolves, rather than
   firing immediately with `pending`.

**`surface` must NOT be reused for layer 3** — it already exists live meaning "which screen
this element is displayed ON" (`summary_expanded.surface`=brief_card 762; `error_shown.surface`
=explore 215), with nearly the same value vocabulary and inverted meaning.

**Top implementation risk:** PostHog RN `register()` persists across sessions. The resolver must
rewrite the whole `entry_*` block every session including resetting to `organic`, or one push
session leaks its campaign into every later organic session.

## Measured ground truth (PostHog 146258, 30d to 6 Sep 2026 — re-verify, dated)
- **UTMs: 0 events** carry utm_source/medium/campaign anywhere (app_opened 4,358 / app_installed 1,085 / deep_link_opened 978 / register 394)
- `attribution_source` person prop **0% populated** — Singular postback never reaches PostHog
- `app_opened.source` only ever `organic` (3,648) / `deeplink` (710) — no push/banner/store/share
- `push_opened` **0 events in 30d** despite ~67% opt-in
- **`deep_link_opened` is 54% noise**: 396 `campaign=auth_callback` (Auth0 return, ~1:1 with 394 `register`), 56 dev-server `192.168.1.x:8083`, 75 in-app router transitions. Genuine ≈451 (279 inc42.com + 172 unparsed sng.link)
- **VERIFIED**: the 75 in-app-route events are a **real production code path, not dev noise** — of 12 people with dev-IP or in-app-route events, only 1 has both; 8 have in-app-route with zero dev traffic. So the guard needs a real "entered from outside" check, not just a dev-build exclusion.
- In-app `source` **already works** on 7 events — `article_opened`: explore 858 / brief_card 600 / deeplink 586 / article_reader 116 / search 76 / company_page 59. So "Brief card vs Explore → full article" is answerable TODAY.
- No origin property at all on `explore_viewed` (7,419), `watchlist_viewed` (1,797), `search_result_tapped` (274)
- `$session_id` on 100% of events (105,975 events / 4,390 sessions) — layer 2 is wiring, not new plumbing

## Sequencing
Steps 1–3 are standalone bug fixes (deep-link guard, dev builds off prod project, make
`push_opened` fire). Steps 4–8 are the schema change and need `change-request-workflow.md` +
the master sheet updated in the same pass. Step 7 (layer 2 + rename) breaks
`brief_page_opened`/`app_opened` history — dual-write vs accept-break is an open product call.

Related: [[project-inc42-app-analytics-audit]], [[reference-inc42-app-tracking-links]],
[[project-inc42-deep-linking]], [[project-inc42-app-event-validation]],
[[feedback-entry-point-instrumentation]].
