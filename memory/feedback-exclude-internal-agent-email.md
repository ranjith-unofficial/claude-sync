---
name: feedback-exclude-internal-agent-email
description: "Never include ritviksethi56@gmail.com in any INC42 audit, count, example or sample user — it is an internal agent account"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 76d907d2-a950-4b87-956e-2bca7123da0c
  modified: 2026-09-12T21:24:53.652Z
---

`ritviksethi56@gmail.com` is INC42's **internal agent**. Ranjith (13 Sep 2026): "never ever include this email".
Exclude it from every PostHog / Customer.io audit: totals, loss %, user counts, and sample-user columns.

**Why:** it is the heaviest single App user and distorts results. In the 12 Sep PH→CIO audit it alone
caused 10 of 11 `story_unsaved` losses (47.8% → 7.7% without it), the entire iOS `story_saved` loss, and
it was the sample user on 12 rows of the "THE ONLY TWO QUESTIONS" tab (Test sheet, gid 149884656).

**How to apply:** filter it out before computing anything, not after. Only this address — `ritviksethi33@gmail.com`
was not named, so ask before excluding other internal/test accounts.

Related: [[project-inc42-ph-cio-parity-android]], [[feedback-analytics-depth]].
