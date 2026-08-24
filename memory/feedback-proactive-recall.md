---
name: feedback-proactive-recall
description: "When asked to recall/compile what's known ('what have we discussed', 'have you incorporated this'), proactively sweep and cross-reference all related memory myself before answering — don't present partial recall and wait for Ranjith to catch the gap"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 59cedaa8-a793-4cf6-9ab8-edd7339fa0a4
  modified: 2026-08-24T17:40:14.699Z
---

When Ranjith asks a recall-style question — "what have we discussed," "have you incorporated this," "what's included as part of X" — the burden is on me to have already swept everything relevant and cross-referenced it, not on him to spot what I missed and prompt me again.

**Why:** on the PostHog review question, I initially reported it as an incomplete, standalone memory ("~20 Aug, only one point captured") without noticing that a *different* memory (`project-inc42-app-behaviour.md`) independently referenced a "17 Aug PostHog review" from the same reviewer, same subject, with numbers that turned out to be wrong. Ranjith had to ask "don't you remember this one?" to surface a connection I should have made myself on the first pass. That's the exact failure this rule exists to prevent — he did the cross-referencing work that was mine to do.

**How to apply:**
- On any "what do we know / have we covered X" question, don't stop at the first matching memory file — grep across memory for the same people, same subject, same rough timeframe, and same artifacts before answering, the way I'd search code before claiming a function doesn't exist.
- Treat approximate dates, informal names, or partially-captured items as a signal to search harder, not a reason to report them as isolated/incomplete and move on — those are exactly the records most likely to have a sibling entry recorded under a different label.
- When compiling "everything relevant" (like the v2 scope list), re-check it against fresh angles each time asked again, rather than replaying the same answer — the whole point of being asked repeatedly is that more may now be findable.
- If, after a genuine sweep, something is still missing or unconfirmed, say so plainly — but only after actually having done the sweep, not as a default deflection back to him.

Related: [[feedback-memory-precise-dates]] (the specific date-cross-linking mechanic this general rule motivated), [[feedback-completeness-audits]] (same principle — surface my own misses first — applied to document review rather than recall).
