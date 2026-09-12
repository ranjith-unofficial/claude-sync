---
name: project-inc42-app-qa-batch-12sep
description: "Inc42 app QA bug batch filed 12 Sep 2026 - 7 dev subtasks + 1 design subtask, one open taxonomy question"
metadata:
  node_type: memory
  type: project
---

Filed 2026-09-12 from an app review walkthrough. Parent ticket **"[Bug] App QA batch - 12 Sep 2026"** gid `1218419016139021` in the Inc42 App project, assigned Ritvik Sethi, with 7 subtasks:

1. Notification toggle shows disabled even when OS permission is granted
2. Tapping guest user does not open the sign-in prompt (dead control)
3. Company card description cut off, no "View more" (seen on TrueFan AI)
4. Investor label should read "Investor(s)"
5. "Advanced Hardware and Technologies" chopped mid-word on Skyroot
6. "View more" should sit inline at the end of the truncated text, company detail page
7. Company Explore scroll position does not reset (stays at Unicorn section after returning from an article)

Design item "Reduce spacing on the first company page" gid `1218418956025770` filed as a subtask under **"V2 App - Design changes"** (`1218353498240283`), assigned **Satya** (`1204511407773682`, Satya.prusty@ink42.com).

**Not filed as a duplicate:** removing "Headcount change" from the company sort control is already covered by open ticket `1217118240141107` "To replace Headcount change sort by to Total revenue" (created 3 Aug 2026, assigned Ranjith).

**Open question:** whether "Advanced Hardware and Technologies" is the shared Inc42 sector taxonomy value. If it is, renaming app-side only desyncs app from web and DataLabs - see [[feedback-shared-system-safety]]. Ranjith has not confirmed.

Asana parents in play: **"V2 - Dev Task"** `1218172204712996` holds feature-area subtasks for Ritvik; **"V2 App - Design changes"** `1218353498240283` holds unassigned design subtasks. See [[reference-inc42-asana-ids]] for the browser-fetch write method (`X-Allow-Asana-Client: 1` header).
