---
name: reference-inc42-master-prd-skill
description: "The inc42-master-prd skill holds the full procedure for updating the Inc42 App Master PRD Google Doc — load it before touching that document rather than working from memory"
metadata:
  node_type: memory
  type: reference
---

**Skill:** `~/.claude/skills/inc42-master-prd/SKILL.md` (invoke as `inc42-master-prd`).

Built 2026-08-30 at Ranjith's request, after a long restructure of the Master PRD: *"once this entire structure is finalized, you need to create certain guidelines on how this document should get updated ... so that whenever this document gets updated, they go through the memory or certain steps before updating this particular document."*

**Load the skill before any edit to that document.** It carries what does not fit in a memory line:
- The seven-section structure and the nesting rules (a group needs 3+ documents; every container tab needs its own content; nothing loose at the top level).
- **The supersede check** to run before adding any new document. Skipping it is how three generations of the v1 PRD and five overlapping AskInc42 docs accumulated.
- **The naming trap.** The doc's internal names are not the team's names. This caused two live features to be recorded as missing — see [[project-inc42-app-live-feature-status]].
- **The fan-out table**: every other place that must change in the same pass (inventory table, decisions log, event dictionary, Asana, the Open Ledger sheet).
- **Browser mechanics** for a canvas-rendered Google Doc: how to move tabs via "Move into", how to set a dual-flavour clipboard so pastes land, and why coordinate clicking fails.

**Two documents exist and have diverged.** The restructure lives only in the Copy (`13vNB88le_0-mOGv3nueRJEQOUfrLVYIujBWLGAj6qow`). The original (`1eT472QdzWOg_ChvvmoO3cX5CnL2sqToR5jU8-GvMxzw`) still has the old flat 47-tab layout and is the one the team has historically opened. Confirm which one is being edited before starting, and say which one in the report.

**How to apply:** treat the skill as the procedure and this memory as the pointer. Do not reconstruct the rules from conversation history.
