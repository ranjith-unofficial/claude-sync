---
name: project-inc42-mixpanel-legacy-finding
description: "29 Aug 2026 — legacy Mixpanel instrumentation found live on production inc42.com during the Media analytics audit; undisclosed first-party vendor, unconfirmed PII exposure"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9806e46d-71a9-4068-9df4-aa66c5b57e7f
  modified: 2026-08-29T10:21:11.215Z
---

During the [[project-inc42-analytics-team-briefs]] Media audit, Ranjith flagged a live Mixpanel POST as
surprising (Mixpanel was believed dead per [[reference-inc42-vendor-stack]]). Follow-up investigation
(29 Aug 2026) confirmed it's real and significant, not a false positive:

- **First-party, deliberately configured**: two real Mixpanel project tokens, branched by URL path
  (one for `/datalabs/`, one for the rest of the site), baked directly into inc42.com's server-rendered
  `<head>` — not a GTM/ad-network/iframe injection.
- **Legacy, not new**: Wayback Machine history shows it live ≤2020 through late 2022, removed for ~9
  months, reinstated mid/late 2023, and live continuously since — roughly a year before PostHog was even
  added to the page. Almost certainly predates everyone currently on the team; nobody currently owns it.
- **Unresolved: PII exposure risk.** `track_pageview` is explicitly `false` in the init config and there's
  no static `.track()` call in the HTML — something else (most likely a GTM tag) fires `mixpanel.track()`
  on real user interactions. The one payload the audit could trigger and capture was clean (device ID,
  UTM params, browser metadata, no PII) — but a **separate, already-confirmed finding** is that another
  GTM-fed event, "App Banner Viewed," sends raw email/name/phone to GA4 via the same tag-management layer.
  That means the mechanism that could carry PII into Mixpanel already exists elsewhere on the same site.
  The specific GTM tag/trigger behind the Mixpanel `.track()` call had not been identified as of 29 Aug —
  follow-up requested.

**Why this matters beyond a tracking-sheet gap:** the vendor stack this finding contradicts
([[reference-inc42-vendor-stack]], "verified" 13 July 2026) is the same one feeding Play Data Safety /
Apple nutrition-label disclosures and [[project-inc42-legal-compliance]] / [[project-dpdp-compliance]]
provider lists. An undisclosed vendor silently collecting site-wide browsing data for years is a
compliance exposure, not just a stale spreadsheet row.

⚠ **CONFIRMED 29 Aug 2026 — this is an active PII exposure, not a hypothetical.** Traced the compiled GTM
container (GTM-WBHJLKR, publicly served): 37 Custom HTML tags reference Mixpanel, each gated on a Custom
Event trigger (`dataLayer.push({event: "<name>"})`). Resolved 6 so far, all confirmed sending full PII via
`mixpanel.identify(email)` + `mixpanel.people.set(...)`: **Plus Subscribed, Newsletter Subscribed, Form
Submission, Login, Plus Onboarding, Inc42 Onboarding.** The Login tag alone fires ~10,500×/90 days — this
is routine, continuous exposure, not a rare conversion-moment leak. Payload per event: email (as
distinct_id), phone, first/last/full name, seniority, designation, company name, personal/work email, UID
— built from the same shared props object also confirmed feeding GA4 ("App Banner Viewed") and, per code
reference only (live execution unconfirmed as of 29 Aug), possibly Amplitude too.

**How to apply:** this is no longer analytics-audit housekeeping. Two parallel tracks needed: (1) technical
containment — pause the identified GTM tags, low-risk single-container-publish action; (2) compliance/legal
escalation — loop in whoever owns [[project-dpdp-compliance]] directly, today. Don't treat "Mixpanel isn't
used" as current fact anywhere (Play Data Safety copy, DPDP scoping, vendor lists) until this is resolved.
Exposure-window scoping (when these specific GTM tags were published — separate from the base `<script>`
init block's ~2023 Wayback date) and the remaining 31 tags' PII-leak status were still being investigated
as of 29 Aug — check for updates before treating the incident as fully scoped.
