---
name: project-personal-ai-ops
description: "Ranjith's personal daily-brief/triage system — email digest, doc gap-check, Slack triage, wearable notes — phased build, started 2026-08-01"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8230394b-c29c-4ec1-ab47-1ef725d5b743
  modified: 2026-08-01T09:48:56.498Z
---

Ranjith is building a personal "chief of staff" system to stop losing time to manual triage across 10 Gmail/Workspace inboxes, unread newsletters, Slack, and shared docs — so effort goes into new work rather than repeatable admin.

Phased roadmap (locked 2026-08-01, he wants all of it — phasing is a dependency order, not a priority cut):
- **Phase 1** (buildable now — Gmail + Notion already connected in this environment): daily Notion morning brief (email digest + newsletter surfacing across inboxes); document gap-check agent that applies his existing completeness-audit lens ([[feedback-prd-completeness]], [[feedback-completeness-audits]]) automatically to any shared doc.
- **Phase 2** (needs one setup step from him): resolve multi-inbox access for all 10 Gmail/Workspace accounts (separate OAuth connections per account vs. forwarding into one aggregator); Slack connector authorization + triage/next-action agent (reads message, tells him what to do).
- **Phase 3** (blocked externally, revisit later): Neo Sapien wearable integration for offline-discussion notes — feasibility unverified, don't assume it plugs in until device is purchased and its export path (Notion sync? webhook? own app?) is confirmed. News aggregation — sources not yet defined, ask when this phase starts.

Output surface: **Notion page**, not Artifact or email — his explicit choice, fits his existing daily Notion habit for offline notes so everything lands in one app.

**Locked morning-brief design (2026-08-01):**
- Section 0 (added later same day): this week's focus / today's plan / yesterday's misses — sourced from Notion INC42 pages + meeting notes (incl. Utkarsh discussions) + Calendar + his project memory. Needs a "Daily Focus" Notion database as source of truth (created so "missed yesterday" is exact, not inferred) — he wants full accountability tracking, not just an inbox summary.
- Section 1: needs-action-today (Gmail, read-only — agent never archives/labels/modifies his inbox, report only, confirmed explicitly)
- Section 2: worth reading — newsletters/reports condensed to one line each; LinkedIn/Indeed job alerts shown with titles (he wants them visible, not bucketed as noise)
- Section 3: skim-count-only bucket for pure promo (count, not itemized)
- Section 4: gap-checked summary of new/edited Notion Meetings/Discussions pages
- Runs daily ~10:30 AM IST

**Why:** terminal text is hard to consume for a recurring daily-read use case; he wants one place to check each morning instead of 10 inboxes + Slack + Notion separately, freeing cognitive effort for higher-leverage work. The accountability layer (section 0) is explicitly meant to make daily work "a little easier to believe" — i.e. reduce the mental load of self-tracking.
**How to apply:** when resuming this work, check Phase 1 build status before proposing new scope. Don't assume Slack or Neo Sapien are connected/available until explicitly confirmed in-session — both were open blockers as of the roadmap date. Don't assume a Daily Focus Notion database exists until confirmed built.
