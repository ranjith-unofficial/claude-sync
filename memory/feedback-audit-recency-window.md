---
name: feedback-audit-recency-window
description: "Every INC42 audit must be scoped to recent data — 2025-01-01 to today — not all-time; late 2024 is the absolute earliest"
metadata:
  type: feedback
---

Ranjith, 8 Sep 2026: *"while you audit, always consider recent data of 2024, 2025 and 2026. do not
consider anything beyond even consider late 2024 or consider from 2025 till this date"*

**Rule:** scope every audit query to **2025-01-01 → today**. Late 2024 is the earliest acceptable
boundary. Never report an all-time figure as the headline number.

**Why:** Inc42's PostHog and Customer.io hold profiles and events going back to 2018. An all-time count
mixes dead 2019 accounts into a live coverage figure and makes a field look better or worse covered than
it is. It also drags in products that no longer exist (the old Plus dates are 2021-2023) and inflates
"people affected" on anything that was written once and never removed.

**How to apply:**
- PostHog person queries: `WHERE created_at >= '2025-01-01'` (or the event window equivalent).
- Customer.io: check `last_seen_at` / recent activity before calling an attribute live.
- If an all-time number is genuinely needed for contrast, show it **second and labelled**, never alone.
- State the window in the deliverable itself, so a reader knows what the counts mean.

This applies to user-property audits, event audits, funnel work and coverage claims alike.
Related: [[project-inc42-user-properties-audit]], [[feedback-analytics-destination-scope]],
[[feedback-completeness-audits]].
