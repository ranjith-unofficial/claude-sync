---
name: feedback-instructions-plain-language
description: "Any action/'what to do' column Ranjith hands to a developer must be Where / What exactly / Done when in plain language - no jargon, no leftover audit scaffolding"
metadata:
  type: feedback
---

On 8 Sep 2026 Ranjith read cell G7 of the "Unified User Properties" tab and said: *"you have simply
written media writer must emit numeric PK... I'm not able to understand what exactly to be changed...
It should be simple language to understand and implement."*

**Why:** these columns get handed to developers who did not sit in the audit. A finding is not an
instruction. "Media writer must emit numeric PK" states a defect; it never says which codebase, what
to write instead, or how anyone knows it is done.

**How to apply — every action cell answers three questions, in three columns:**
1. **Where to change it** — the actual place: "Inc42 Media website - the code that identifies a
   logged-in user to PostHog and Customer.io", not "Media".
2. **What exactly to do** — plain English imperative, with the ordering and the do-nots
   ("Do not delete the old values until the new one is live").
3. **Done when** — an observable check a non-author can run.

**Banned vocabulary in these cells:** PK, slug, enum, E.164, auth string, canonical, backfill, null (verb),
array, controlled vocab, "writer". Say: number from the user database / field name / the agreed list /
one-time clean-up of existing records / leave the field empty / list.

**Also:** "Delete" is ambiguous to a developer - always split it into *stop writing it from now on* and
*remove the field from Customer.io and PostHog*.

**Never leave working scaffolding in a deliverable cell.** G7 and G8 still carried my own audit template
("1. Standardise - ... 2. Merge/delete - — 3. Fill check - OK") with em-dash placeholders. Strip it.

**Where a row contradicts itself, say DECISION NEEDED in the cell** rather than picking silently -
e.g. column C said Delete while the DataLabs column said Keep with live data.

Related: [[project-inc42-user-properties-audit]], [[feedback-communication-style]],
[[feedback-stakeholder-doc-writing]].
