---
name: feedback-status-map-ui-treatment
description: "For engineering status-mapping artifacts (which exact system status maps to which treatment), Ranjith wants a rich, complete card UI with real component mockups — not an abstract diagram, and not the general minimal-design default"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e87f7b2e-19d8-490d-a96f-71d19eb01e0a
  modified: 2026-08-27T09:19:38.323Z
---

For an artifact whose whole job is mapping exact system statuses/codes to their treatment (e.g. Razorpay webhook → dunning treatment), a sparse hand-drawn flowchart that abstracts/collapses cases together is the wrong call — even if it's visually clean. Ranjith's exact words after seeing one: "It is not a proper UI and doesn't has a lot of importance to visual because it doesn't tell what are the status and how do we map and every single thing."

**What worked instead:** a two-part page — (1) a legend table listing every exact status/webhook/API-call trigger against which case it maps to, no abbreviation; (2) one full card per case, each showing the mapping as explicit labeled steps (not prose), plus a **real mockup of the actual UI component being described** (an in-app banner rendered to look like the real banner — headline, body copy, CTA button — not a text description of it). This directly addresses "not a proper UI": showing the real component beats describing it.

**Why:** don't collapse related cases into one abstracted "track" for visual cleanliness when the reader's job is to look up one specific case's exact treatment — completeness beats abstraction here. This is the opposite instinct from [[feedback-artifact-design-minimal]] (one font, minimal color, tables not cards) — that rule is right for audit/report artifacts meant to be read start-to-end; it does NOT apply when the artifact's job is exact status→treatment lookup for engineering use, where a card grid with real component mockups and per-case detail is what he actually wants.

**How to apply:** before defaulting to minimal/abstract for a technical reference artifact, ask whether the reader needs to look up one exact case's full detail (→ rich cards, real mockups, no collapsing) or read the whole thing once for a decision (→ minimal, per [[feedback-artifact-design-minimal]]). See [[project-inc42-datalabs-dunning-map]] for the artifact this was learned on.
