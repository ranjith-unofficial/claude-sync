---
name: project-inc42-decode-does-not-exist
description: "Decode (the AI explainer panel) does not exist in the Inc42 app — confirmed by Ranjith 29 Aug 2026; it is spec-only in the v1 PRD and must not be treated as a shipped feature or an instrumentation gap"
metadata:
  node_type: memory
  type: project
---

Confirmed by Ranjith on 2026-08-29: **"there is no such thing called Decode existing in our app."**

This closes a question that had been open across several sessions. Decode appears only as unbuilt spec:
- `PRD Final v3` §4.2 "Decode panel (✨)" and §8.2 "Decode & Ask" — in the Google Doc "Inc42 App Master PRD" (`1eT472QdzWOg_ChvvmoO3cX5CnL2sqToR5jU8-GvMxzw`)
- Same sections in the two older generations (`App PRD Final`, `App PRD Final v2`)

**Corrects these earlier records — do not repeat them as current:**
- [[project-inc42-app-v2-scope-full]] Thread 6: "Instrument `decode` (the AI explainer) — zero telemetry today despite being the core positioning." The telemetry is zero because the feature was never built, not because instrumentation was missed.
- [[project-inc42-app-analytics-audit]] / the 25 Aug events-fix ticket's dropped list: `decode` was parked pending confirmation that it shipped. It did not ship. Drop it entirely rather than filing a separate ticket.

**Why:** two separate audits treated a dead event name as an instrumentation defect and nearly turned it into engineering work.

**How to apply:** treat Decode as archived spec. Do not list it as a live surface, a tracking gap, or a v2 item. When splitting the v1 PRD into per-surface tabs, the Decode sections go to Archive, not to the product tabs. Name the cross-cutting surface "Ask entry points," not "Decode & Ask."
