---
name: project-daily-brief-architecture
description: "Daily-brief system: capture split from briefing so GitHub stays current — local + cloud runners with strict file ownership. Connectors authorised 5 Sep 2026."
metadata:
  type: project
---

Ranjith's start-of-day system, restructured 5 Sep 2026. Full spec lives in the
repo — `~/inc42-context/daily/README.md`, `inbox/README.md`, and
`daily/WEB-ROUTINE-PROMPT.md`. This is a pointer; the repo is the survivor.

**The change:** the daily brief used to be the only thing writing to
`master-brain`, so a day away from the Mac left nothing on record and the phone
had nothing to read. Capture is now a separate layer running on every Claude
session end (`bin/capture-session.sh`, wired as a `Stop` hook).

**Connectors — CORRECTED 5 Sep 2026.** He initially declined re-enabling them
("shared Claude access"), then authorised **Google Calendar, Gmail, Asana,
Google Drive, Notion, GitHub, Wispr Flow on BOTH web and local**. Do not repeat
the old claim that they are unavailable. Still absent: **Slack** only — read
via Claude-in-Chrome, local runs only.

**Wispr Flow is the notetaker — every meeting, online AND offline. Not Fathom.**
Fathom is not connected and is not part of this design; do not reintroduce it.
Calendar is used only for the *gap*: an event with no Wispr note means nothing
was recorded. A Wispr note with no calendar event is normal — an offline meeting.

**What that fixed:** Wispr gives meeting content on both runners and Gmail covers
the inbound half that had no source, so the cloud runner is now a real brief
rather than a repo recap.

**Two runners, strict ownership** — local writes everything; cloud writes only
`daily/*-mobile.md` and the `web` block of `daily/RUNSTATE.json`. The cloud
runner cannot verify against Slack or the conversation history, so it reports
the record and never changes it.

**Locked decisions:**
- Slack via Chrome **clears his unread badges** (his triage queue); a Slack
  *connector* would not. Still unauthorised as of 5 Sep.
- A dictation notetaker does not diarise speakers. If a Wispr note does not name
  attendees, take them from Calendar; if neither does, record `Present: unknown`
  and **attribute no statement to a named person**. With attendees unknown, the
  external-attendee half of the never-process gate cannot clear a meeting.
- Transcript scan is forward-only from a watermark; no backfill of the 178
  existing sessions.
- `inbox/threads/sessions.jsonl` holds **pointers only, never message content**.
- Gmail and Calendar are **read-only** — never send, archive, label, mark read,
  or create/accept an event.
- A **sensitivity gate runs before anything is written** by either runner.
  Calendar titles and email subjects expose interviews, comp and medical mail
  that Fathom-only never surfaced, and the cloud runner writes to the repo.

**How to apply:** never edit the live skill copy directly — the repo copy is
truth, run `bin/sync-skills.sh` (they had already drifted once). Watch
`.gitignore` line 30 (`state.json`, for Playwright auth state) — it silently
caught `daily/STATE.json` on macOS, which is why the file is `RUNSTATE.json`.

Supersedes the daily-brief half of [[project-personal-ai-ops]]. Related:
[[project-meeting-agent]], [[project-inc42-morning-tape]] (separate 07:00
analytics routine — do not duplicate it),
[[feedback-no-outbound-without-double-approval]].
