---
name: project-inc42-app-qa-batch-12sep
description: "Inc42 app QA bug batch filed 12 Sep 2026 - 7 dev subtasks + 1 design subtask, one open taxonomy question"
metadata:
  node_type: memory
  type: project
---

Filed 2026-09-12 from an app review walkthrough. Parent ticket **"[Bug] App QA batch - 12 Sep 2026"** gid `1218419016139021` in the Inc42 App project, assigned Ritvik Sethi, with 15 subtasks filed across five passes the same day:

1. Notification toggle shows disabled even when OS permission is granted
2. Tapping guest user does not open the sign-in prompt (dead control)
3. Company card description cut off, no "View more" (seen on TrueFan AI)
4. Investor label should read "Investor(s)"
5. "Advanced Hardware and Technologies" chopped mid-word on Skyroot
6. "View more" should sit inline at the end of the truncated text, company detail page
7. Company Explore scroll position does not reset (stays at Unicorn section after returning from an article)
8. TLDR tap extends the card instead of opening the bottom bar (Article Explore)
9. After login from the watchlist prompt, the user lands on Brief instead of the page they were on
10. Show "Bootstrapped" below the company name when stage is blank (company explore)
11. Search results use the old company card design
12. Switching role shows "Couldn’t save, try again" although the role does change (screen recording exists, Ranjith to attach)
13. No success confirmation when role, topic or sector is changed
14. Contact Us modal defaults seniority to Founder instead of the user’s profile role (screen recording exists, Ranjith to attach)
15. "Profitable startups" View all defaults to Headcount change sort instead of Total funding (high to low)

Design item "Reduce spacing on the first company page" gid `1218418956025770` filed as a subtask under **"V2 App - Design changes"** (`1218353498240283`), assigned **Satya** (`1204511407773682`, Satya.prusty@ink42.com).

**Not filed as a duplicate:** removing "Headcount change" from the company sort control is already covered by open ticket `1217118240141107` "To replace Headcount change sort by to Total revenue" (created 3 Aug 2026, assigned Ranjith).

**Not filed, by explicit instruction:** the profile name-edit observations (save toast sits oddly between the bottom bar, slow to load, no confirmation) - Ranjith narrowed that dictation to just the two role/sector issues above.

**Parent has more subtasks than the 14 filed here:** Ranjith added 4 himself directly in Asana on 12 Sep (Company detail page; TL;DR background colour; streak FAQ placement; Save changes button highlight state). The parent description numbering covers only the 15 filed here.

**Unresolved sort conflict:** subtask 15 wants **Total funding** (high to low) as the default sort; open ticket `1217118240141107` specifies **Total revenue** (high to low). Different fields, both claimed as the default. Ranjith has not picked one.

**Open question:** whether "Advanced Hardware and Technologies" is the shared Inc42 sector taxonomy value. If it is, renaming app-side only desyncs app from web and DataLabs - see [[feedback-shared-system-safety]]. Ranjith has not confirmed.

Asana parents in play: **"V2 - Dev Task"** `1218172204712996` holds feature-area subtasks for Ritvik; **"V2 App - Design changes"** `1218353498240283` holds unassigned design subtasks. See [[reference-inc42-asana-ids]] for the browser-fetch write method (`X-Allow-Asana-Client: 1` header).
