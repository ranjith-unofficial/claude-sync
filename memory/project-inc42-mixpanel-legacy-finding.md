---
name: project-inc42-mixpanel-legacy-finding
description: "29 Aug 2026 — legacy Mixpanel instrumentation found live on production inc42.com during the Media analytics audit; undisclosed first-party vendor, unconfirmed PII exposure"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9806e46d-71a9-4068-9df4-aa66c5b57e7f
  modified: 2026-08-29T10:11:08.423Z
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

**How to apply:** don't treat "Mixpanel isn't used" as current fact anywhere (Play Data Safety copy,
DPDP scoping, vendor lists) until this is resolved. Before anyone removes the script, the GTM tag/trigger
behind the `.track()` call needs to be found and checked for PII — removing it blind loses the chance to
audit what's already been collected. Whoever owns DPDP compliance scoping should probably be looped in
directly rather than this staying inside the analytics-audit thread.
