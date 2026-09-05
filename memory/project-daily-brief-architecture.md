---
name: project-daily-brief-architecture
description: "Daily-brief system: capture split from briefing so GitHub stays current — two runners (local terminal, cloud routine) with strict file ownership. Built 5 Sep 2026."
metadata: 
  node_type: memory
  type: project
  originSessionId: 90e930bf-5f04-402e-a805-62b9d98d5858
  modified: 2026-09-05T13:20:58.533Z
---

Ranjith's start-of-day system, restructured 5 Sep 2026. The full spec lives in
the repo — `~/inc42-context/daily/README.md` and `inbox/README.md`. This is a
pointer, not a copy; the repo is the survivor.

**The change:** the daily brief used to be the only thing writing to
`master-brain`, so a day away from the Mac left nothing on record and the phone
had nothing to read. Capture is now a separate layer that runs on every Claude
session end (`bin/capture-session.sh`, wired as a `Stop` hook).

**Two runners, strict ownership** — local writes everything; the cloud routine
writes only `daily/*-mobile.md` and the `web` block of `daily/RUNSTATE.json`.
The cloud runner can't verify anything against Slack or a meeting, so it reports
the record and never changes it.

**Locked decisions:**
- Slack and Fathom are read through **Claude-in-Chrome**, not MCP — he declined
  re-enabling those connectors because that Claude access is shared. Chrome is
  local-only, which is *why* the capture layer had to exist.
- Slack via Chrome **clears his unread badges** (his triage queue). A Slack
  *connector* would not. That reversed the recommendation toward the connector —
  still unauthorized as of 5 Sep, and the cloud Slack capture is blocked on it.
- Transcript scan is forward-only from a watermark; no backfill of the 178
  existing sessions.
- `inbox/threads/sessions.jsonl` holds **pointers only, never message content** —
  a session can carry candidate PII or health data.
- Asana MCP is disabled too, so `meeting-intake` step 7 drafts tickets rather
  than filing them.

**How to apply:** never edit the live skill copy directly — the repo copy is
truth, run `bin/sync-skills.sh` (they had already drifted once). Watch for
`.gitignore` line 30 (`state.json`, for Playwright auth state) — it silently
caught `daily/STATE.json` on macOS, which is why the file is `RUNSTATE.json`.

Supersedes the daily-brief half of [[project-personal-ai-ops]]. Related:
[[project-meeting-agent]], [[project-inc42-morning-tape]] (separate 7am
analytics routine, do not duplicate it), [[feedback-no-outbound-without-double-approval]].
