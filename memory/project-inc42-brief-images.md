---
name: project-inc42-brief-images
description: "Sector-based default images for the INC42 app brief card — decided with Utkarsh 12 Aug 2026, reconfirmed by Ranjith 24 Aug; owner Anmol, still open"
metadata: 
  node_type: memory
  type: project
  originSessionId: 878d7ed0-3fa4-4ffb-81e5-9a0f6d5bff08
  modified: 2026-08-24T14:34:57.242Z
---

**Decision (Ranjith ↔ Utkarsh, 12 Aug 2026, reconfirmed by Ranjith 24 Aug 2026):**
the brief card will use **sector-based default images**.

**How the brief image works today**
- Pulled automatically from the **featured article** of the brief.
- When there is **no featured article**, it falls back to **one static default image shared
  across every sector** — the same picture regardless of what the brief is about.

**What was agreed**
- Build **sector-based default image variants** and select by the brief's **dominant sector**.
- **Owner: Anmol** — Ranjith to find bandwidth with him.
- Brief **title** is already auto-generated per sector; that half is done. Images are the gap.

**Status history**
- 12 Aug — decided on the Utkarsh call; listed as one of three short-term focuses alongside
  the guaranteed daily brief and the 1–2 manual pushes. (The *scored/automated push logic*
  was the thing parked, not the images.)
- 13 Aug — Ranjith **deliberately deprioritised** it on the marketing call: *"not my primary
  concern right now"* — acquisition took over.
- 24 Aug — Ranjith restated the decision. Still **not built**; no Asana ticket filed as of
  this date.

**Still unconfirmed:** number of variants (one per sector vs grouped), who produces the
artwork (Anmol vs Satya/design), and the fallback when a brief has **no dominant sector**.

**Tension worth flagging before build:** [[project-inc42-content-personalization]] records
that **86% of articles carry no sector**, which is why sector *personalization* was killed.
If sector data is that sparse, "dominant sector" may resolve to nothing for most briefs and
the generic default would still show — check sector coverage on briefs specifically before
commissioning a full set of variants.

**Why:** it's a small, visible polish item that keeps resurfacing in Utkarsh conversations,
and it has been decided-then-parked twice — easy to lose.

**How to apply:** treat it as an open, owned decision (Anmol), not as shipped. Related:
[[project-inc42-launch]], [[project-inc42-app-behaviour]], [[project-inc42-app-structure]].
