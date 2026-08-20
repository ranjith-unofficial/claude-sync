---
name: project-inc42-posthog-review
description: "Utkarsh's PostHog review (~20 Aug 2026) with a list of improvements; only the \"flag internal users\" point captured so far — the rest is still uncaptured"
metadata: 
  node_type: memory
  type: project
  originSessionId: 878d7ed0-3fa4-4ffb-81e5-9a0f6d5bff08
  modified: 2026-08-20T08:05:01.755Z
---

Utkarsh reviewed INC42's PostHog setup around **20 Aug 2026** and gave Ranjith a list of
improvement pointers. Status: **INCOMPLETE — only one point captured.**

Captured so far:
- **Internal users must be identified/marked in PostHog** so internal activity is
  distinguishable (and presumably excludable) from real user data. Exact mechanism
  (person property, internal-user cohort, filter-out on insights, or IP/domain rule)
  is NOT confirmed.

Not yet captured: "a lot of other pointers" — the remaining items, their owners, and
where the review lives (doc / Slack thread / call recording).

**Why:** analytics decisions on the app (acquisition, funnels, QIA) are being made off
PostHog; internal traffic polluting a small install base (~15–50 installs) distorts
every number materially.

**How to apply:** before quoting any PostHog number for the app, check whether internal
users are excluded. Ask Ranjith for the rest of Utkarsh's pointers and append them here
rather than starting a new memory. Related: [[reference-inc42-vendor-stack]],
[[project-inc42-app-acquisition]], [[project-inc42-launch]].
