---
name: feedback-figma-not-artifact
description: "When Ranjith asks for a Figma design, build it in Figma — do not substitute an Artifact or design canvas"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ff608462-8c66-4e2b-b954-0f3c6f4ba592
  modified: 2026-09-06T14:49:19.934Z
---

When Ranjith asks for a design **in Figma** (he usually gives the file URL and a node to
use as reference), build it in Figma. Do not substitute an Artifact, a design canvas, or
local HTML mockups.

On 6 Sep 2026 the Figma MCP connector appeared unauthorised at the start of the session,
so the fallback of building a design canvas was started instead. He interrupted with
"I have given you figma access already, design there." The connector was in fact
available — it just needed `/mcp` to surface it.

**Why:** his design work lives in Figma files the team already reviews in. A separate
artifact is a dead end he has to translate back by hand.

**How to apply:** if Figma tools look unavailable but he has asked for Figma, say so in
one line and ask him to check the connector — do not silently switch medium. Check
`ListAgents`/`/mcp` state or just try a `ToolSearch` for the Figma tools before concluding
they are missing; deferred MCP tools do not show until searched for.

Related: [[reference-figma-mcp-limits]], [[reference-figma-mcp-build-techniques]],
[[feedback-ui-mockup-research-first]], [[feedback-deliver-in-chat]].
