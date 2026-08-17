---
name: feedback-ask-before-assuming
description: "Ask before stating a fact as confirmed when it's actually a stale plan date or unverified assumption — don't build downstream recommendations on it"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9859d45d-f58a-4c8b-b439-1562f2def0be
---

Don't state something as confirmed/current fact when it's actually an old plan or an assumption carried forward from memory — ask first.

**Incident:** Told Ranjith to "pull `brief_completed` from the warehouse" as an actionable next step, treating the Inc42 app's iOS public launch (a *planned* Jul 22 2026 date recorded in [[project-inc42-launch]]) as confirmed-live. The app was not actually live. The whole recommendation — gate a placement decision on querying real usage data — was built on that false premise. Ranjith's correction: "So ask before confirming or assuming something."

**Why:** A plan date in memory records what was *intended* at the time it was written, not what happened. Treating it as settled fact, then building a concrete recommendation on top (query this, pull that number), compounds one bad assumption into a chain of wrong next steps that sound actionable and confident.

**How to apply:** Before asserting a status/date/fact pulled from memory as true in the current moment — especially one that gates a recommendation (data exists, a milestone happened, a decision is locked) — flag it as "per memory, as of [date]" and confirm it's still current, or just ask, rather than stating it outright and building on it. This applies most where the fact is time-sensitive (launch status, whether something shipped, whether a number is queryable yet) rather than stable (e.g. team names, locked formulas). Relates to [[feedback-validation-approach]] (similar spirit, scoped to QA/validation tasks specifically — this one is general).
