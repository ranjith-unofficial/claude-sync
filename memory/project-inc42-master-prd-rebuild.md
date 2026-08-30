---
name: project-inc42-master-prd-rebuild
description: Status of the Inc42 App Master PRD Google Doc rebuild into real Document Tabs with full (not condensed) content — PAUSED mid-rebuild in a partially-broken state as of 2026-08-30
metadata: 
  node_type: memory
  type: project
  originSessionId: 03703bc3-38d6-46ae-89df-b20d1af00bb4
  modified: 2026-08-30T13:04:51.669Z
---

Rebuilding the messy 45-tab "Inc42 App PRD — Consolidated" Google Doc
(https://docs.google.com/document/d/1RJtcNEeOjHiQK6tDxm87MZ2a4uyq0ztFqPUaSYNmyxQ/edit)
into real Google Docs Document Tabs (native sidebar tabs, not markdown-style headings)
was PAUSED on 2026-08-30 in a partially-broken state. Source of full original content:
`~/Downloads/Copy of Inc42 App Master PRD (2).md` (15,256-line full 45-tab export).

**Why paused:** mid-rebuild, signs of a live concurrent editor appeared in the doc
(unrelated stray text about a "PostHog OAuth approval" typed into the "Launch
Infrastructure" sub-tab, plus a live collaborator presence icon). Ranjith confirmed
he had the doc open and closed his tab. See [[feedback-live-doc-collision-risk]].
One drafting agent's own attempt to clean up the stray text triggered an undo that
wiped the already-completed "Cross-Cutting & Platform" sub-tab.

**Governing correction from Ranjith (why this rebuild exists):** an earlier version
of this doc used a single flat tab per tier (Production/Backlog/Next release/etc.)
with markdown-style H1/H2 headings and heavily condensed prose. Ranjith explicitly
rejected this: real original feature detail was missing (how Brief works, how
Explore works, how streak works, the FAQ was dropped entirely) and he wants real
Google Docs Document Tabs — one sub-tab per underlying document/feature — not a
single scrolling tab. Content must preserve full original detail (bullets/tables
over dense prose, per his usual style), not be re-condensed.

**Structure being built:** each tier becomes a parent tab with sub-tabs added via
"Add subtab":
- **Production** (13 sub-tabs planned): Master PRD — Overview, Brief, Explore,
  Watchlist, Company Profile, Cross-Cutting & Platform, Launch Infrastructure,
  Article Ranking Logic, Streak & Rewards, Account Deletion, Singular Deep-Link
  Config, Privacy Policy, Terms of Use — **all 13 sub-tabs exist**, but only
  Master PRD — Overview, Brief, Explore, Watchlist, Company Profile were confirmed
  correctly populated before the pause. Launch Infrastructure has stray unrelated
  content that needs removing. Cross-Cutting & Platform was emptied by an accidental
  undo and needs re-pasting. Article Ranking Logic, Streak & Rewards, Account
  Deletion, Singular Deep-Link Config, Privacy Policy, Terms of Use sub-tabs exist
  but are still EMPTY — content was drafted but never pasted in before the pause.
- **Next release, Backlog, Reference**: NOT yet restructured — still on the old
  flat single-tab condensed content as of the pause.
- **Archive**: left as-is (flat single tab), intentionally not restructured since
  it's meant to stay condensed/superseded reference material.

**Drafted full-detail HTML content**: ~26 per-document HTML files were drafted by
parallel sub-agents during that session and saved to a session scratchpad path
(`/private/tmp/claude-501/.../scratchpad/paste-docs/`) — **this path is ephemeral
and will not exist in a later session**, so that drafted content is effectively
lost and would need to be redrafted from the source markdown file when work resumes.

**How to apply:** before resuming this rebuild, re-verify the actual current state
of every Production sub-tab (don't trust this memory's snapshot — it may be stale
or already partially fixed), confirm no one else has the doc open, then continue
restructuring Next release/Backlog/Reference and finish populating/repairing
Production. Use [[reference-google-docs-html-clipboard-paste]] for the paste
mechanics — keystroke-simulated typing proved slow and error-prone by comparison.
