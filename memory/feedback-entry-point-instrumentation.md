---
name: feedback-entry-point-instrumentation
description: "Don't infer which UI entry point drove an event from adjacency/timing — verify a real distinguishing property exists, and if not, that's the finding"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1bd2fc68-b479-44c7-b355-a8f9bafeb94c
  modified: 2026-08-29T07:46:09.405Z
---

When two UI elements can trigger the same downstream event (e.g., a calendar date-pill vs. a card carousel both opening the same "past brief" screen), don't infer which one fired from session-adjacency, timing, or any other proxy signal — check directly whether the event actually carries a property that distinguishes them, and report plainly if it doesn't, rather than presenting an inference as a measured split.

**Why**: on the INC42 app's Explore/Brief work (25-29 Aug 2026), an initial inferred split (session-linking a past-brief open to a preceding cover-view) was presented as if it approximated "calendar vs carousel" usage. Ranjith pushed back ("I am not talking about... think twice before answering this") and asked for the real property to be checked. It turned out neither event had ANY property distinguishing the two entry points — the inference, while directionally reasonable, could not be verified and should not have been offered as if it were closer to measured than it was.

**How to apply**: before answering "which of these two paths drove this outcome," check the actual event schema for a distinguishing property FIRST. If none exists, say so as the primary finding ("this can't be measured with current instrumentation") and offer the inferred estimate only as a clearly-labeled secondary, with the caveat attached every time it's cited afterward — don't let the caveat fade after the first mention. The real fix is almost always to recommend the client set an explicit property at the point of interaction (e.g., at tap-time), not to build a better inference from existing data.
