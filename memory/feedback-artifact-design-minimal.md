---
name: feedback-artifact-design-minimal
description: "Ranjith wants audit/report artifacts plain and low-color, not visually designed — corrected after a heavily-styled HTML report"
metadata:
  node_type: memory
  type: feedback
---

A data-dense HTML audit report (analytics event audit, multiple severity colors, colored pill badges,
colored left-border accent stripes on cards, a condensed display font for headers) was rejected outright:
"very much confusing it is not structured and has too many color and very confusing and frustrating to go
through this document."

**Why:** matches [[feedback-communication-style]] — he wants tables/bullets, not designed layouts, and that
extends to artifacts, not just chat. Heavy color-coding and card-style findings read as decoration that gets
in the way of scanning, even when the underlying content is dense and technical.

**How to apply, for audit/report/findings-style artifacts specifically:**
- One font family (not a display + body + mono trio). Plain sans-serif is enough.
- Minimal color: reserve color for the one thing that matters (e.g. P0 severity in red text). Everything
  else stays grayscale/black-on-white.
- Severity/status = a plain text label or a thin bordered badge, never a colored block filling a whole cell
  or a colored left-stripe on a card.
- Tables over cards. A findings list is a table (Sev | Class | Finding), not a grid of colored panels.
- No decorative "thesis" sections, bar charts as hero elements, or stat-tile walls with big colored numbers
  — a plain summary strip of numbers is fine, colored numbers for P0/OK is the ceiling, not glowing tiles.
- This does not mean skip design entirely — structure (headers, tables, spacing) still matters. It means:
  calm and scannable, not "designed." When in doubt for this user, undershoot on color and visual flourish.

Related: [[feedback-document-calibration]] (same instinct — don't add unrequested polish/structure), 
[[project-inc42-event-auditor]] (the artifact this was corrected on).
