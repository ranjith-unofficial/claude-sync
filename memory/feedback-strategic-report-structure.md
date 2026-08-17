---
name: feedback-strategic-report-structure
description: "For comprehensive strategy/product reports, build one narrative argument, not an incrementally-appended list of tables"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 84f0537a-600a-48eb-b04f-79a6905e32fc
  modified: 2026-08-01T09:29:50.980Z
---

When Ranjith asks for a "comprehensive" or "holistic" strategy report (e.g. the [[project-inc42-unification]] work), don't build it as a growing stack of additive sections (findings table, then backlog table, then roadmap table...). He explicitly rejected that shape twice in one session, calling it "not building a holistic thought" even though each individual section was accurate and well-evidenced.

**Why:** individual correct facts don't add up to a usable argument on their own. He wants to be able to read the report top to bottom and come away with a decision, not a reference document he has to synthesize himself.

**How to apply:** structure comprehensive strategic reports as a sequence that argues something, roughly: why this matters (thesis, grounded in a real cost/number) → who's actually affected (audience/JTBD, not personas invented from nothing) → what the best comparable operators already prove works (competitor benchmarks) → the specific bar being set because of that evidence → the features, each explicitly checked against a named precedent (not just "steal this") → the actual mechanics of how pieces connect to each other in both directions → a short closing verdict that could stand alone if nothing else got read.Each section should refer back to earlier ones (e.g. "this backlog item exists because of the gap found in §3") rather than sitting as an independent list.

This doesn't relax [[feedback-communication-style]] for chat replies — those stay crisp/bulleted. It's specifically about how long-form artifact reports should be built when he asks for "comprehensive"/"holistic"/"the whole night task" scope.

Also: when he names a specific comparable company (e.g. "there is a brand called Tech in Asia who does the same as us"), research that company directly and by name before generalizing to the broader competitive set — don't substitute a generic category scan for the specific example he gave.

**Depth check (2026-08-01, same session, after v6):** even a report built on real live data (GA4/PostHog live audits) and cross-checked across two independent AI research tools (Gemini + Perplexity) still landed as "surface level, just a normal document" to him. His specific complaint named three concrete missing layers, not just "more depth" in the abstract:
1. **Positioning** — an actual claimed category/statement ("who are we, versus whom"), not just a list of what competitors do.
2. **Mechanisms** — literally how a recommendation would work (data model, trigger, sync logic, failure mode), not just the outcome ("merge the Watchlist" needs a table schema and a migration plan, not a sentence).
3. **Paths** — genuine alternative strategies with named tradeoffs, not one implied plan dressed up in research tables. He explicitly said "a few paths, which is okay" — optionality itself isn't the problem, the absence of it being surfaced as a real choice is.

**How to apply:** for any request that could be read as "give me a comprehensive/detailed strategic report," assume research findings and data tables alone will read as "surface level" no matter how well-sourced. Budget explicit space for: a stated position/claim, mechanism-level specs (data models, triggers, concrete failure modes) for the top few recommendations, and 2-3 named strategic alternatives with an explicit tradeoff table — before considering the report done. Ground truth data and competitor research are necessary inputs to this, not a substitute for it.
