---
name: reference-inc42-30-sec-summary-naming
description: "The Inc42 app feature specced as 'Decode' ships as the '30 sec summary' — Decode was only ever an internal document name and must not be used"
metadata:
  node_type: reference
  type: reference
---

Confirmed by Ranjith 2026-08-30: **"Decode, we are calling it as 30 sec summary and not as a Decode."**

**Use "30 sec summary". Never "Decode".** Decode was an internal spec name that never left the document.

**This corrects an earlier note of mine** that recorded Decode as "not built". The name was not in use; that is not the same as the feature being absent. I had inferred absence from a name nobody recognised, and from a `decode` event with zero fires. Both were explained by the rename.

**Consequences already applied to the Master PRD** (`13vNB88le_0-mOGv3nueRJEQOUfrLVYIujBWLGAj6qow`):
- 77 occurrences of "Decode" replaced with "30 sec summary" across all tabs, match-case on so the lowercase `decode` event name survived.
- §4.2 and §8.2 headings renamed.
- The two decisions-log entries that were *about* the naming were reworded so the history still reads truthfully rather than saying "name locked as 30 sec summary".
- App PRD v2 item 16: the `decode` event is no longer written off as dead. It needs renaming to match the shipped feature, and someone must confirm whether it is wired.

**Still open, and it matters:** the 5 Jul decision in the doc treated these as two different things — "Decode" as a live, user-triggered AI explainer, and a separate pre-written editorial one-liner then called "In 30 seconds". Whether the app ships the live AI explainer or only the editorial summary is unconfirmed. Ask before describing §4.2 as accurate.

**How to apply:** when auditing events or features, a zero-fire event plus an unrecognised name is a naming question first and an instrumentation gap second. Ask what the team calls the thing before recording it as missing. See [[reference-inc42-master-prd-update-rules]].
