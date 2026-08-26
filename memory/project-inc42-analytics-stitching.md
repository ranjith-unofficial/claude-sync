---
name: project-inc42-analytics-stitching
description: "Consulting-call architecture for web→app identity stitching, acquisition vs session source, deferred deep linking, and why not to merge PostHog workspaces"
metadata: 
  node_type: memory
  type: project
  originSessionId: a7af69b6-fb2f-41b2-8c5c-b7d1daa6c4c7
  modified: 2026-08-26T07:43:50.421Z
---

From a call (speakers not identified in transcript; implementer estimated 1-2 weeks to build, targeting start ~2026-09-01) walking through the intended architecture for INC42's web→app attribution problem.

**Web→app identity stitching:**
- Not logged in (the majority — INC42 is a content site; logged-in users are a small share of ~7L media / 3-4L DataLabs total): web sends the **analytics cookie ID as a URL query param** on the redirect to the app; the app runs a **resolver** that reads it and stitches it into the app's session variables.
- Logged in: stitch via **backend user ID** instead — called the more refined method, but low volume given login isn't mandatory.

**Acquisition source vs session source** — both meant to be written as base params on nearly every event hit:
- Acquisition source = captured on first-ever install (click → store → install fires a special "app install" event carrying the resolved source).
- Session source = captured on subsequent opens where the app is already installed and a web click redirects straight in.

**Deferred deep linking mechanics:** tracking link routes by device to Play/App Store; UTM/campaign params stay attached through the store visit ("deep embedding," native Play/App Store library support); if not yet installed, an after-install URL (install-referrer pattern) fires on first open and routes to the right landing page + logs the install event with attribution; if already installed, the link routes directly in-app (normal deep link).

**Do NOT merge app/website/DataLabs PostHog workspaces.** Different platforms need different properties (app: churn, app version/utilization; web: bounce rate, engagement rate) — not comparable, and suffixing event names (`page_view_app` vs `page_view`) isn't sufficient since PostHog expects distinct properties per source, not just distinct names. Correct pattern: keep event streams separate per platform, then post-process/unify downstream into a processed data layer (e.g. all-apps-by-company), not by merging raw events.

**Why this matters:** this is the architecture behind the fix already tracked in [[project-inc42-deep-linking]] (Singular smart links, the `campaign=None` attribution bug) and it validates the existing 3-project PostHog split in [[reference-inc42-posthog-projects]] with unification happening at the [[project-inc42-data-warehouse]] layer rather than in PostHog itself.
