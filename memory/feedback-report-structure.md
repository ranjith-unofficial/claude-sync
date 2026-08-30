---
name: feedback-report-structure
description: "How Ranjith wants multi-project status reports structured — methodology up front, findings grouped holistically per project bucket, never fragmented across cross-cutting sections"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9806e46d-71a9-4068-9df4-aa66c5b57e7f
  modified: 2026-08-30T13:26:39.437Z
---

When reporting on work spanning multiple projects/buckets (e.g. App/Media/DataLabs), structure as:
1. **One "what was done" section up front** — plain-language summary of method, and explicitly name which tools were actually used (not buried later, not per-bucket repetition).
2. **One section per real-world bucket, each fully self-contained.** Every finding belongs to exactly the project it actually affects — never split a bucket's findings into separate top-level sections by theme (e.g. don't pull "the PII leak" or "the login bug" out into their own top-level section if they're actually Media findings; they belong inside the Media section, not beside it).
3. **One explicit "next step" at the end of each bucket**, not buried in prose.
4. Only things that genuinely don't belong to one bucket (cross-project tooling, decisions pending on the user directly) get their own small section, kept brief.

**Why:** first attempt split "Mixpanel/GA4 PII leak" and "Freewall bug" into their own top-level sections even though both are Media findings. Ranjith's exact words: "it's so cluttered, I could not get a holistic understanding of what has happened in each bucket." Fragmenting one project's findings across multiple sections defeats being able to see that project's full picture in one place — this was the core complaint, not visual density.

**How to apply:** before publishing any multi-project report, check every finding is filed under the ONE bucket it actually belongs to, not a thematic cross-cutting section, unless it genuinely spans multiple projects with no single owner. See [[project-inc42-analytics-team-briefs]] for the underlying work this feedback came from.
