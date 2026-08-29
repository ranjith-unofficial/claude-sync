---
name: feedback-ui-mockup-research-first
description: "For any UI/app-mockup design artifact: research real reference UIs (Dribbble/actual app screenshots) before building, and never hide comparison variants behind a click-to-reveal interaction — show everything at full scale"
metadata:
  type: feedback
  originSessionId: 1c442aa8-439c-4822-95e9-3864030f3bbb
  modified: 2026-08-29T07:46:24.683Z
---

Two rules learned the hard way while building the [[project-inc42-explore-articles-companies-design]] artifact (5 iterations before it landed):

1. **Always do real web research for visual grounding before designing a UI mockup.** The first few passes invented card layouts from memory/generic patterns and Ranjith called it "not following any design principle... absolutely waste." Only after actually browsing Dribbble for the specific category (news-app cards, fintech watchlists, crypto dashboards) and pulling concrete real patterns — source-row + engagement-row anatomy, bold editorial stat cards, filled-gradient trend charts with tabular right-aligned deltas — did the redesign land. Ranjith's own instruction once frustrated: "find in the internet and get best design and take inspiration and then design."

2. **Never hide comparison variants behind a click-to-reveal switcher (radio/tab toggle) in a review/comparison artifact.** Built a pure-CSS radio switcher so only one of 14 variants showed at a time; Ranjith never discovered the toggle and reported "why is there only 1 variant" — reading the single visible baseline as the entirety of the work. A leftover stray `</div>` also silently broke the switcher's CSS reveal rule, making it a real bug on top of a bad UX choice. Fixed by showing every variant simultaneously, full scale, stacked vertically with jump-nav anchors for convenience only (not as the sole way to see content).

**Why:** both failures cost multiple full-rebuild cycles on the same request before the actual problem (invented-not-researched visuals; hidden-not-shown content) was identified — the user's feedback ("vague," "cluttered," "basic") was symptom-level each time, not root-cause, until asked directly.

**How to apply:** before writing any HTML/CSS for an app-screen mockup or design-direction artifact, spend a browsing pass on Dribbble (or the App Store/Play Store) for the relevant product category first. When presenting multiple design variations for comparison, default to showing all of them at once in realistic scale — never gate content behind an unprompted interaction unless the user has asked for an interactive/exploratory artifact specifically.
