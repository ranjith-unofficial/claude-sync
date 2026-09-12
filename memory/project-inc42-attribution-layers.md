---
name: project-inc42-attribution-layers
description: "Inc42 app attribution — three-layer model (install/session/nav), the naming collision between two drafts, and live-verified state as of 12 Sep 2026"
metadata:
  type: project
---

Two drafts existed with **conflicting property names** for the same design: `app-attribution-source-mapping-spec.md`
(6 Sep, measured, uses `attribution_*` / `entry_*` / `referrer_*`) and `singular-posthog-attribution-plan.md`
(11 Sep, cleaner runtime flow, uses `attr_*` / `open_source` / `source_screen`). On 12 Sep 2026 the two empty
stubs were filled recommending **6 Sep naming + 11 Sep runtime flow**; the losing draft must be marked superseded
or a third convention appears in the next ticket. Recommendation is unreviewed by Ranjith.

Layers, never merged: A install = `attribution_*` on person, immutable, 3,000 ms wait · B session entry =
`entry_*` PostHog super properties re-registered every session, 1,500 ms delayed `app_opened` · C in-app =
`referrer_*` event property (contract already written in the 6 Sep spec §6 — do not redesign it).

**Live-verified 12 Sep 2026, project 146258, 30d** — two corrections to the 6 Sep spec:
- `attribution_source` / `attribution_campaign` are NOT missing from persons: the keys are written on
  1,386/1,437 persons (96.4%) with a **literal JSON null value** on all of them. The `$set` fires; the
  resolver behind it returns nothing. Same pattern on `app_opened.push_type` — present on 5,733/5,733
  events, null on all. The contract exists in code; only the values are absent.
- UTMs are not entirely absent: `deep_link_opened` already carries a parsed `source`/`medium`/`content`/
  `campaign`/`link_url`/`destination_screen` block on 1,195/1,198 events (unprefixed, not `utm_*`).
  Inbound app shares are already visible there as `medium=app_share` / `source=inc42_app`, 72 events/30d.

Other verified figures: `app_opened` 5,733 events, source only ever `organic` 4,738 / `deeplink` 995 ·
`push_opened` **does not exist** in the project · 355 of 5,772 sessions (6.2%) have no `app_opened` at all
(foreground-after-idle) · `deep_link_opened` still 38.6% `auth_callback` noise (462/1,198), unfixed since 6 Sep ·
`$session_id` 100% coverage · 0 of 132,435 events carry `entry_channel`, `open_source` or `referrer_screen` ·
`story_shared` 196 events with **no `share_id`**, so no share is traceable to an inbound click ·
app_opened people: Android 761 / iOS 537 / iPadOS 26.

See [[project-inc42-app-event-validation]], [[project-inc42-app-analytics-audit]], [[reference-inc42-posthog-projects]],
[[reference-inc42-vendor-api-browser-access]], [[reference-inc42-vendor-stack]].
