---
name: feedback-live-doc-collision-risk
description: "Before bulk-restructuring or deleting content in a real shared Google Doc via browser automation, check for a live collaborator and treat unexpected text as a stop signal, not a cleanup task"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 03703bc3-38d6-46ae-89df-b20d1af00bb4
  modified: 2026-08-30T13:05:05.339Z
---

Before running bulk destructive/restructuring edits (delete-and-retype a tab, mass
rename, mass "select all + delete") on a real, shared Google Doc via browser
automation, check whether anyone else currently has it open, and treat any
unexpected or unrelated text appearing mid-edit as a signal to STOP immediately
and ask — not as something to quietly clean up.

**Why:** During the [[project-inc42-master-prd-rebuild]] session, Ranjith had the
target Google Doc open in his own browser tab at the same time automation was
restructuring it. Real-time Google Docs sync merged both sets of edits into the
same tabs — unrelated text (a note about a "PostHog OAuth approval") appeared in a
tab being rebuilt. A drafting agent tried to clean it up and ran an undo, which
instead wiped a *different*, already-correctly-completed sub-tab ("Cross-Cutting &
Platform") — turning a detection into actual data loss. This is the same failure
mode [[feedback-shared-system-safety]] already warns about, but specific to live
collaborative documents rather than shared infra objects.

**How to apply:** for any live/shared Google Doc, Sheet, or similar collaborative
surface: (1) before starting a destructive bulk edit, check for a visible
collaborator-presence indicator in the UI, and if unsure, ask the user directly
whether the doc is open elsewhere; (2) if text appears during automation that
wasn't just written by the automation itself, stop immediately rather than
attempting an in-place fix (especially avoid "undo" as a cleanup tool once
collision is suspected — it can silently revert unrelated, already-correct work
elsewhere in the same document); (3) surface exactly what was found and ask before
continuing, rather than guessing at recovery.
