---
name: project-inc42-posthog-review
description: "Utkarsh's PostHog review — DATE UNCERTAIN (recorded as ~20 Aug 2026 here, but app-behaviour memory cites a '17 Aug PostHog review' with matching subject matter 3x); only the \"flag internal users\" point captured so far — the rest is still uncaptured"
metadata: 
  node_type: memory
  type: project
  originSessionId: 878d7ed0-3fa4-4ffb-81e5-9a0f6d5bff08
  modified: 2026-08-24T17:38:17.736Z
---

⚠️ **DATE RECONCILIATION FLAG (added 2026-08-24, unconfirmed) — read before citing a date.**
This memory originally recorded the review as "~20 Aug 2026" (approximate, never verified).
[[project-inc42-app-behaviour]] separately cites a **"17 Aug PostHog review"** three times,
with concrete numbers attributed to it: "Explore beating Brief 69% vs 31%," a **7-second
median** brief completion, and a **41%** cover→brief entry rate — all three later found on
2026-08-20 to be **measurement artifacts** (walkthrough confound; pre-launch test traffic
polluting the median; corrected entry rate is 55%). Same reviewer (Utkarsh), same subject
(PostHog output for the app), overlapping timeframe → **likely the same review**, with either
this file's date or app-behaviour's date being wrong. **Not confirmed with Ranjith yet.**
If it is the same event, the "flag/exclude internal users" pointer below is plausibly *why*
those three numbers came out distorted in the first place — internal test traffic is a
strong candidate root cause for an artificially low median and skewed entry rate.

**How to apply:** cite this review's date as "17–20 Aug 2026, exact date unconfirmed" until
Ranjith confirms one way or the other — do not silently pick one. If confirmed as the same
event, merge the two memories' content under a single corrected date rather than leaving
both standing. See [[feedback-memory-precise-dates]] for the naming-convention fix this
gap prompted.

---

Utkarsh reviewed INC42's PostHog setup (date per above) and gave Ranjith a list of
improvement pointers. Status: **INCOMPLETE — only one point captured.**

Captured so far:
- **Internal users must be identified/marked in PostHog** so internal activity is
  distinguishable (and presumably excludable) from real user data. Exact mechanism
  (person property, internal-user cohort, filter-out on insights, or IP/domain rule)
  is NOT confirmed.

Not yet captured: "a lot of other pointers" — the remaining items, their owners, and
where the review lives (doc / Slack thread / call recording). Given the three numbers
above turned out to be artifacts, treat any other pointers from this review as **candidates
to re-verify against real data**, not as confirmed problems, once they're captured.

**Why:** analytics decisions on the app (acquisition, funnels, QIA) are being made off
PostHog; internal traffic polluting a small install base (~15–50 installs) distorts
every number materially.

**How to apply:** before quoting any PostHog number for the app, check whether internal
users are excluded. Ask Ranjith for the rest of Utkarsh's pointers AND the exact date,
and append/correct here rather than starting a new memory. Related:
[[reference-inc42-vendor-stack]], [[project-inc42-app-acquisition]], [[project-inc42-launch]],
[[project-inc42-app-behaviour]], [[project-inc42-app-v2-scope-full]].
