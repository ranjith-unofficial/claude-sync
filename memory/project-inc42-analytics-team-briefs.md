---
name: project-inc42-analytics-team-briefs
description: "28 Aug 2026 — detailed team briefs delegating a PostHog+Customer.io 'dark events' reconciliation audit (App/Media/DataLabs) to 4 employees, plus an intern brief to build a living analytics knowledge base"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9806e46d-71a9-4068-9df4-aa66c5b57e7f
  modified: 2026-08-28T18:25:12.952Z
---

Ranjith asked for two deliverables built from the [[project-inc42-tracking-master-review]] sheet (same Google Sheet,
now confirmed to have 8 tabs incl. IP - Event/Event Properties, which weren't reviewed before): a delegation brief for
4 employees to audit PostHog + Customer.io for events firing live that AREN'T in the master sheet (App, Inc42 Media,
DataLabs in scope; IP explicitly deprioritized), and a separate brief for an intern to build a persistent, team-wide
analytics knowledge base (event dictionary + property dictionary + platform-routing rules + a change-request
checklist) so future feature requests (a banner, a push notification) get checked against ground truth instead of
causing naming mismatches.

Full content: `~/ClaudeDocs/inc42/analytics-events-audit-team-briefs.md`.

**Assignment structure proposed (not yet confirmed by Ranjith with real names):** Employee 1 = App, Employee 2 =
Inc42 Media, Employee 3 = DataLabs, Employee 4 = cross-project QA/consolidator (starts after 1–3's first pass,
feeds the intern). Employee 2's brief points at the existing [[project-inc42-event-auditor]] tool/output as a
starting point rather than having them redo browser-side testing from scratch.

**Why this task exists:** distinct from the 27 Aug line-by-line sheet review (which checked the sheet's internal
consistency) — this is the reverse direction: hunting PostHog/CIO for events the sheet doesn't know about at all,
executed by humans rather than by Claude directly.

**How to apply:** when Ranjith reports back employee findings or asks to build the actual knowledge base, treat this
file + the saved brief as the spec; don't re-derive the task structure from scratch. If he names real people for the
4 slots, update this memory with names.
