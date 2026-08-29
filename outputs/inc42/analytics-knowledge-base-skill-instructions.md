# Inc42 Analytics Knowledge Base — Build This as a Claude Code Skill

## READ THIS BEFORE ANYTHING ELSE

This is a task to execute immediately by writing real files. It is not a document to edit, reformat, review, or summarize back.

**Your deliverable is a working Claude Code Skill** — a `SKILL.md` file plus reference docs — that any future Claude Code session at Inc42 can load to answer "does tracking for X already exist, and if not, how should I add it" without pinging a person.

### DO
- Actually write the skill files described in Part B, with real content pulled from the sources in Part A.
- Actually test the finished skill against the acceptance scenario in Part F before declaring it done.
- Ask Ranjith to confirm the file location in Part B if you're unsure whether this should be a personal (`~/.claude/skills/`) or team-shared skill — this is a real open decision, not something to guess past.

### DO NOT
- Do NOT produce a plan, outline, or description of what the skill will contain instead of writing it.
- Do NOT invent event or property definitions. Every entry in the dictionary must trace back to one of the sources in Part A — if you don't have a source for something, leave it out and flag the gap rather than filling it in with a guess.
- Do NOT collapse three projects' worth of events into one generic table that loses which platform/project each belongs to.
- Do NOT skip the acceptance test in Part F. A skill that hasn't been tested against a real question is not done.

---

## Part A — Inputs to consolidate, in this order

1. **All 8 tabs of the master sheet**: App - Events, App - Event Properties, Datalabs - Events, Datalabs - Events Properties, Inc42 - Media - Events, Inc42 - Media - Events Properties, IP - Event, IP - Event Properties.
   https://docs.google.com/spreadsheets/d/1n6r5QXe-9Pq1uAWMKRe7zSgLHSejASzAq-BAqeI3L6Y
2. **The three audit outputs**, if they exist yet — check the sheet for these tabs before starting; if any are missing, note which project's audit hasn't run yet rather than proceeding without it:
   - "App Audit — [date]" + "App — New Events Found"
   - "Media Audit — [date]" + "Media — New Events Found"
   - "Datalabs Audit — [date]" + "Datalabs — New Events Found"
3. **The website event-auditor findings**: `~/ClaudeDocs/inc42/event-auditor/runs/<latest>/report.html` and `findings.json`.
4. **Vendor stack ground truth** (do not contradict this with anything from the sheet): Customer.io and PostHog are live on BOTH website and app (EU region). Firebase and Singular/SKAN are app-only (US). Meta Pixel and GTM are website-only. MoEngage, Mixpanel, and Amplitude are NOT live anywhere, regardless of what any tab's Destinations column says.

---

## Part B — Build the skill files

Ask Ranjith which of these two locations to use before writing (leave a note if you proceed without an answer):
- **Personal, this machine only**: `~/.claude/skills/inc42-analytics/`
- **Team-shared**: a `.claude/skills/inc42-analytics/` directory inside whatever git repo the Inc42 team's Claude Code sessions share (needs Ranjith to name the repo — a skill saved only under his home directory will not reach other people's sessions).

Create this structure:

```
inc42-analytics/
  SKILL.md
  references/
    event-dictionary-app.md
    event-dictionary-media.md
    event-dictionary-datalabs.md
    property-dictionary.md
    platform-routing-rules.md
    change-request-workflow.md
```

**`SKILL.md` frontmatter and body** — keep this file SHORT. It is the thing Claude reads to decide whether to load the skill at all, and it should route to the reference files rather than contain the full dictionaries itself:

```markdown
---
name: inc42-analytics
description: Reference for Inc42's real analytics event and property schema across App, Website (Inc42 Media), and DataLabs — what events exist, what they actually fire with (vs. what's planned), which platforms receive them and why, and the checklist to follow before adding any new event, property, or user property. Load before creating, naming, or routing any new analytics event or property, before adding tracking to a banner/notification/modal/feature, or when asked what tracking already covers a given user action.
---

Route by what's being asked:
- "Does an event for X already exist?" / "what should I name a new event?" → read the relevant
  references/event-dictionary-*.md for the project in question, then property-dictionary.md.
- "Which destinations should this go to?" → references/platform-routing-rules.md.
- "I want to add a new event/property" → follow references/change-request-workflow.md in order,
  do not skip to writing code.
- Money/payment events (subscriptions, billing, cancellations) → check platform-routing-rules.md's
  ads-exclusion rule before anything else; a failed charge must never fire an ads conversion.

These references reflect verified production behavior as of [fill in date you built this],
cross-checked against live PostHog/Customer.io data, not just the planned tracking sheet.
Where the tracking sheet and live data disagree, the references note both and say which is true.
```

**`references/event-dictionary-{app,media,datalabs}.md`** — one row per event, per project:

| Canonical name (as it actually fires) | Sheet's planned name (if different) | Category/Group | Fires when | Properties (name : type : allowed values) | Person/user properties updated | Destinations + WHY | Status | Known gotchas |
|---|---|---|---|---|---|---|---|---|

Pull "Canonical name" and "Known gotchas" from the audit outputs (Part A2) wherever they exist — an event confirmed live with a different name than planned should show BOTH names, not just the sheet's intended one. Carry forward every existing warning verbatim (e.g. the DataLabs `pro_billing` note that a bare Customer.io "performed pro_billing" condition can't distinguish success from failure) rather than summarizing it into something vaguer.

**`references/property-dictionary.md`** — one row per property, deduplicated across all three projects:

| Property name | Project(s) it appears in | Type | Allowed values | Naming convention (snake_case app/datalabs-backend vs Title Case website — note both, don't force one) |
|---|---|---|---|---|

**`references/platform-routing-rules.md`** — rules, not a per-event table:
- Money moving or failing to move → never an ads destination.
- Needs to identify a person across sessions/devices → needs an explicit identify/alias call; document where in each project's flow this happens (e.g. App's anon-device-UUID-to-Auth0-ID alias on `sign_in_completed`).
- App-only tools (Firebase, Singular/SKAN) vs website-only (Meta Pixel, GTM) vs both (PostHog, Customer.io) — state this plainly so nobody routes an app-only event to a website-only tool or vice versa.
- MoEngage/Mixpanel/Amplitude are dead — any sheet row still listing them as a destination is stale, not a valid target.

**`references/change-request-workflow.md`** — the checklist a requester follows before any new event/property is created:
1. Search the relevant event-dictionary-*.md by INTENT, not just by name (a request for "banner impression tracking" should surface `card_viewed`-style precedents even though no existing event says "banner").
2. If an existing event covers the intent, extend it with a new property value — do not create a near-duplicate event.
3. If genuinely new: follow that project's naming convention, apply platform-routing-rules.md, get sign-off from the project owner, and add the entry to the dictionary BEFORE requesting implementation.
4. Update the relevant dictionary file the same day the event ships — a KB that lags implementation by weeks is the same failure mode this skill exists to prevent.

---

## Part C — Where gaps exist, say so explicitly

If any of the three audit outputs (Part A2) don't exist yet, or the event-auditor findings are stale, do not backfill the gap with your own inference. Write a `references/open-gaps.md` listing exactly what's missing and what would need to run first — an incomplete-but-honest skill is usable; a complete-looking skill built partly on guesses is not.

---

## Part D — Acceptance test before calling this done

Simulate this exact request against your finished skill and confirm you can answer using ONLY the skill's files, without asking anyone: *"We want to track clicks and impressions on a new homepage banner. What should we do?"*

You should be able to state: which existing event(s) it should extend rather than duplicate, what property to add and its naming convention, which destinations it needs and why, and what sign-off step it needs before implementation. If you can't answer all four from the skill alone, the skill isn't finished — go back and fill the gap.

---

## Part E — When you're done

Report, explicitly:
- The file location you used (personal vs team-shared, and why if Ranjith didn't specify).
- Which reference files are complete vs. blocked on a missing audit output (Part C).
- The result of the Part D acceptance test — the actual answer you produced, not just "passed."
