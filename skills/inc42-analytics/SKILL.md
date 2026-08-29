---
name: inc42-analytics
description: Reference for Inc42's real analytics event and property schema across App, Website (Inc42 Media), and DataLabs — what events exist, what they actually fire with (vs. what's planned), which platforms receive them and why, and the checklist to follow before adding any new event, property, or user property. Load before creating, naming, or routing any new analytics event or property, before adding tracking to a banner/notification/modal/feature, or when asked what tracking already covers a given user action.
---

Route by what's being asked:
- "Does an event for X already exist?" / "what should I name a new event?" → read the relevant
  references/event-dictionary-*.md for the project in question, then property-dictionary.md.
- "Which destinations should this go to?" → references/platform-routing-rules.md.
- "I want to add a new event/property" → follow references/change-request-workflow.md in order,
  do not skip to writing code.
- Money/payment events (subscriptions, billing, cancellations) → check platform-routing-rules.md's
  ads-exclusion rule before anything else; a failed charge must never fire an ads conversion.
- Before citing ANY vendor as live or dead → check platform-routing-rules.md's "Live PII incident"
  section first. It is not stale housekeeping — it overrides the general vendor list below it.

These references reflect verified production behavior as of 29 August 2026, cross-checked against
live PostHog/Customer.io data and a direct browser-based production audit (the "event-auditor" tool),
not just the planned tracking sheet ("One Inc42 - Analytics | Master Sheet"). Where the tracking sheet
and live data disagree, the references note both and say which is true. Three per-project audits
(App/Media/DataLabs) all ran on 29 Aug 2026 — treat every live-volume number here as a dated snapshot,
not a standing truth; re-verify if this conversation is more than a couple of weeks old.

Known incomplete areas are listed in references/open-gaps.md — check it before treating a dictionary's
silence on something as "doesn't exist" rather than "not yet verified."
