---
name: feedback-prd-completeness
description: "Every PRD I help draft must cover evidence/data validation, legal/compliance exposure, and an independent reframe-check before being called final — not just product mechanics"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 60cb3464-2e9c-4ebe-a009-471fcce371a0
---

PRDs cannot ship as "product mechanics only." Every PRD must explicitly address, even if briefly:

1. **Evidence/validation layer** — decisions backed by actual data (usage, supply, demand signals), not just product judgment. If the data doesn't exist yet, say so explicitly and flag the decision as provisional rather than locking it.
2. **Legal/compliance exposure** — ToS, data protection (DPDP), copyright, defamation, or any third-party content/data handling risk relevant to the feature. Flag gates explicitly (blocking vs non-blocking).
3. **Independent reframe-check** — before calling a PRD final, stress-test the core framing/job-to-be-done against outside judgment (e.g. a multi-model review or outside read), not just internal conviction. The "efficiency vs status" reframe in [[project-inc42-social-intelligence]] only surfaced this way, after v1.0 was already drafted.
4. Sizing/threshold decisions (allowlist size, cutoffs, caps) should cite the measurement they're derived from, not be picked as round numbers.

**Why:** Ranjith's Pulse v1.0 PRD (drafted in a 2-day scoping sprint, 2026-07-26→28) covered mechanics and editorial workflow well, but had no evidence layer, no legal analysis, and no outside reframe-check. Utkarsh ran all three as a separate parallel research track, and the two had to be reconciled into a v2.0 combined doc — several v1.0 assumptions (story-matching as a gate, 50-voice allowlist, fixed publish times) were overridden by data that simply didn't exist when v1.0 was written. Ranjith wants this gap closed pre-emptively next time, not caught in a merge.

**How to apply:** When drafting or reviewing any future PRD (INC42 or otherwise) with Ranjith, proactively ask/flag: what's the evidence for this decision, is there a legal/compliance angle, and has the core framing been pressure-tested from outside the room — before treating any section as locked. If those tracks can't run in the same sprint as the mechanics draft, say explicitly in the doc which decisions are "pending evidence/legal/reframe-check" rather than presenting them as final.
