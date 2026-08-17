---
name: feedback-shared-system-safety
description: "On shared production systems (INC42 n8n, team sheets): change only the one named object, and PROVE non-interference with a diff rather than asserting it"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0a7258b2-f45b-4229-84ea-2bf0e20e0797
  modified: 2026-08-17T18:18:47.162Z
---

Ranjith repeatedly and unprompted checks that I have not touched anything beyond the one object he named. Across one session: *"Ensure you are not changing anything in the existing workflow and anything specific"*, *"Only change that. No, nothing else. Do not change everything. Or if you don't have anything, ask me — I will share. But do not use anything of your own"*, *"Run using INC42. Do not run my own"*, and mid-task: *"Ensure you're not updating anything else, else it's gonna become a problem, right?"*

**Why:** the INC42 n8n instance runs ~25 live production workflows owned by other people (AskInc42, News AI, Datalabs, Master Agent). A stray write there breaks someone else's system, and it lands on him. The same applies to team Google Sheets that Utkarsh and HR are reading. His concern is not about my competence — it is that blast radius is his problem, not mine.

**How to apply:**
- Touch only the exact ID he gave. Never create helper workflows, never "clean up" adjacent objects, never reuse a credential he did not point at.
- When a task genuinely requires temporarily altering the named object (e.g. n8n has no execute endpoint, so reading a sheet means swapping in a proxy workflow), **back up first, restore after, and verify the restore** — do not assume a 200 means it worked. A restore silently failed once with a 400 and left the workflow as a 2-node stub.
- **Prove it, don't claim it.** When he asks "are you sure nothing else changed", answer with evidence: a node-by-node parameter hash diff of before/after, the instance-wide `updatedAt` list showing only one workflow modified in the window, and row counts on any sheet tab that existed before. Asserting "I only touched X" does not settle it; a diff does.
- Additive changes (a brand-new sheet tab) are fine and do not need this ceremony — but say explicitly that it was additive.

Related: [[project-inc42-hiring-agent]] carries the concrete n8n restore gotchas.
