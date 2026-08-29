---
name: feedback-no-empty-container-tabs
description: "Ranjith's rule for hierarchical docs (Google Docs tabs, folders, nav): a grouping level must earn its place — never create a container that holds one item or has no content of its own"
metadata:
  node_type: memory
  type: feedback
---

When structuring anything hierarchical (Google Docs tabs and sub-tabs, folders, navigation), Ranjith rejects grouping levels that exist only to satisfy a pattern. Stated 2026-08-29, after reviewing a restructure of the Inc42 App Master PRD:

> "Why are there a lot of empty tabs? ... If there is nothing to be added and there is only one sub, if you think it could be added in the tab itself, add in the tab. It is not mandatory to always create sub tabs."

**The rules he is applying:**
- A group holding **one** child must be collapsed. The child moves up a level; the wrapper goes.
- A group needs roughly **3+ items** before it earns a level. Two items usually read better flat.
- **Every container must have its own body content** — at minimum a short index saying what is inside and what to know before opening it. A container that renders as a blank page is a defect, not a neutral shell.
- Mixed depth is fine: a real document and a group can sit as siblings at the same level.

**Why:** he clicks through the structure top to bottom and judges it by what each tab shows when opened. A tab that opens blank reads as unfinished work regardless of how sound the taxonomy is.

**How to apply:** before shipping any hierarchy, walk every node and ask two questions — does this hold more than one thing, and does it say anything when opened? If either answer is no, collapse it or fill it. Beware the trap that caused this: an earlier instruction of his ("I need every single thing to be under a sub-tab") is about *not leaving items loose at the top level*, NOT a mandate to wrap every single item in a group. Applying it literally produced ~20 empty wrappers. See [[feedback-document-calibration]] and [[project-inc42-knowledge-repo]].
