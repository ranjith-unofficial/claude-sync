---
name: project-inc42-analytics-team-briefs
description: "28 Aug 2026 — detailed team briefs delegating a PostHog+Customer.io 'dark events' reconciliation audit (App/Media/DataLabs) to 4 employees, plus an intern brief to build a living analytics knowledge base"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9806e46d-71a9-4068-9df4-aa66c5b57e7f
  modified: 2026-08-29T13:02:54.286Z
---

Ranjith asked for two deliverables built from the [[project-inc42-tracking-master-review]] sheet (same Google Sheet,
now confirmed to have 8 tabs incl. IP - Event/Event Properties, which weren't reviewed before): a delegation brief for
4 employees to audit PostHog + Customer.io for events firing live that AREN'T in the master sheet (App, Inc42 Media,
DataLabs in scope; IP explicitly deprioritized), and a separate brief for an intern to build a persistent, team-wide
analytics knowledge base (event dictionary + property dictionary + platform-routing rules + a change-request
checklist) so future feature requests (a banner, a push notification) get checked against ground truth instead of
causing naming mismatches.

Full content: `~/ClaudeDocs/inc42/analytics-events-audit-team-briefs.md`.

**Assignment structure proposed (not yet confirmed by Ranjith with real names):** Employee 1 = App, Employee 2 =
Inc42 Media, Employee 3 = DataLabs, Employee 4 = cross-project QA/consolidator (starts after 1–3's first pass,
feeds the intern). Employee 2's brief points at the existing [[project-inc42-event-auditor]] tool/output as a
starting point rather than having them redo browser-side testing from scratch.

**Why this task exists:** distinct from the 27 Aug line-by-line sheet review (which checked the sheet's internal
consistency) — this is the reverse direction: hunting PostHog/CIO for events the sheet doesn't know about at all,
executed by humans rather than by Claude directly.

**How to apply:** when Ranjith reports back employee findings or asks to build the actual knowledge base, treat this
file + the saved brief as the spec; don't re-derive the task structure from scratch. If he names real people for the
4 slots, update this memory with names.

**Notable findings from the 29 Aug run (agents were Claude Code sessions using PostHog MCP + browser
automation, not humans clicking UIs — instruction files rewritten mid-task to a hard DO/DO-NOT directive
format after a first attempt just edited the instructions file instead of executing):**
- App: PostHog's own `captureApplicationLifecycleEvents` autocapture has been running in parallel with the
  manually-added `app_opened` event the whole time — same SDK, redundant tracking, needs a product/eng call
  on whether to disable it now that app_opened is instrumented.
- DataLabs: `master_agent_query` (2,359/90d, PostHog-only) is a completely undocumented backend
  classification/quality-scoring event behind Ask Datalabs (`evidence_density`, `ungrounded_claims`) — real
  product-quality telemetry nobody had listed anywhere. `pro_subscription`/`pro_billing` were descoped
  mid-audit (not yet live in Customer.io at all, so the ads-conversion risk they guard against is moot for now).
- Media: found live, undisclosed, first-party Mixpanel instrumentation on production inc42.com (two real
  tokens branched by URL, live since ~2020 with a gap, reinstated ~2023) — see
  [[project-inc42-mixpanel-legacy-finding]] and the correction now in [[reference-inc42-vendor-stack]].
  Also: a Claude Code session ran `rm -f ~/Downloads/*.csv` mid-task and wiped the whole Downloads folder,
  not just its own files — add "never wildcard-delete without listing/confirming first" to any future
  agent instructions of this kind.
- Operational lesson: three agents editing the same live Google Sheet concurrently caused one tab to
  vanish and need recreating. Future runs of this pattern should either serialize the writes or give each
  agent its own sheet/copy.

**Skill built and rigorously tested (29 Aug).** `~/.claude/skills/inc42-analytics/` — personal, this machine
only (Ranjith's choice). Passed 6/6 test scenarios: the original acceptance test plus 5 independent
fresh-agent tests run afterward (no shared context with the build), including two adversarial "trap"
scenarios — requesting Mixpanel as a destination, and requesting a Google Ads conversion off `pro_billing`.
Both were correctly refused with the skill's own stated reasoning quoted back, not just hedged. Every
uncertain point across all 5 tests was flagged honestly rather than guessed. One real recurring gap: "no
maintained project-owner list" surfaced in 3 of 5 tests — every real request needs to know who signs off
per project, and the skill can't answer that. Worth adding an actual owner list before this scales past
one-off use.

**Second test round run proactively (29 Aug), ahead of Utkarsh's independent review** — 5 more fresh-agent
tests targeting person-property mechanics, cross-project identity, deliberately vague requests, and
reasoning transparency. **10/10 total across both rounds, all correct.** Every trap scenario (Mixpanel,
Google Ads renewal, is_vip, forced property-name alignment) was refused; every genuinely unanswerable
question (streak_tier's CIO delivery timing/decay behavior, App↔DataLabs identity merging) got an honest
"the skill doesn't specify this" instead of a plausible-sounding fabrication — including a precise
epistemic distinction on the identity question ("not yet verified/undocumented" vs. "confirmed absent").
Reasoning-transparency tests showed real citation discipline (exact file/line numbers, systematic
elimination of near-miss candidates before concluding a gap was genuine). The no-owner-list gap is the
one consistent weak point across all 10 tests — everything else held up.

**Utkarsh will independently stress-test the skill next**, likely covering similar ground (person-property
behavior, weird/edge-case phrasing, reasoning transparency) — his pass is a second independent check, not
a first one, given the above.
