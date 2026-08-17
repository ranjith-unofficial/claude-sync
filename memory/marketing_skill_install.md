---
name: marketing-skill-install
description: "The unified `marketing` skill installed at ~/.claude/skills/marketing, sourced from coreyhaines31/marketingskills"
metadata: 
  node_type: memory
  type: project
  originSessionId: 17b0a9ce-3a35-4e2c-b58a-b536a4b0c2d0
---

Installed a unified `marketing` Claude Code skill at `~/.claude/skills/marketing/` (2026-07-20), sourced from github.com/coreyhaines31/marketingskills (MIT, Corey Haines).

Contains: 47 playbook skills (copywriting, CRO, SEO, pricing, launches, etc. — under `skills/<name>/SKILL.md`), ~93 tool integration reference docs, and 65 executable CLI scripts for calling real marketing SaaS APIs (Apollo, HubSpot, Stripe, etc. via env-var API keys). `tools/composio/` (third-party MCP broker) was deliberately excluded.

**Why:** User asked for this to be installed for marketing work, with two hard constraints baked into the skill's SKILL.md: (1) never send passwords/credit-card/private personal details to any API, (2) never send conversation history to any third-party platform, and (3) always ask before running a CLI script or making a live third-party API call, naming the vendor/endpoint first.

**How to apply:** When doing marketing work for [[nexloid-product]] or anything else, this skill auto-triggers. Respect the ask-before-calling-any-vendor-API rule baked into it even when the request seems to come from a different angle (e.g. "just go post this to HubSpot").
