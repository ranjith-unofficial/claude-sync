# Open gaps — read before treating this skill as complete

This file exists so a missing or unverified item reads as "not yet confirmed," not as "doesn't exist." If
you hit one of these while answering a question, say so explicitly rather than filling the gap with a guess.

## Scope gap: IP tabs excluded by design

"IP - Event" and "IP - Event Properties" (2 of the 8 tabs in the master sheet) were read but are **not**
turned into a fourth event dictionary. They document a checkout/lead-gen funnel for Inc42's summit-ticketing
microsites (thed2csummit.co — "D2C & Retail Summit," "AI Summit," "CTO Summit"), a separate business line
from the App/Website/DataLabs product surfaces this skill covers, and were explicitly deprioritized by
Ranjith for the audit effort this skill is built from (see `project-inc42-analytics-team-briefs.md`, 28 Aug
2026). If IP tracking ever comes into scope, the raw extraction is preserved in this skill-build's scratch
files (not copied into `references/` — ask if you need it re-pulled from the sheet).

## Sheet-hidden data, resolved via a supplied CSV

`Datalabs - Events Properties` had 130 of its 163 rows hidden on the live Google Sheet by the time this
skill's data was pulled. Rather than risk further edits to a live, actively co-edited document (an earlier
attempt to unhide rows briefly zeroed 6 unrelated columns on a different tab, self-corrected), the property
dictionary's DataLabs section is built from a CSV Ranjith supplied directly
(`~/ClaudeDocs/inc42/datalabs-event-properties-full.csv`), pulled before the rows were hidden. Treated as
complete and reliable — but if DataLabs properties are ever reconciled again from the live sheet directly,
check whether the hidden rows have since been restored or changed.

## Audit columns not exhaustively transcribed (all three per-project audits ran live, 29 Aug 2026)

- **App Audit — 2026-08-29**: columns "Live in PostHog?" and "Actual Properties" are BLOCKED for all 55 rows
  in this specific sheet tab (that audit run had no PostHog MCP access). A **separate, more complete** live
  PostHog+Customer.io audit ran the same day and is cited throughout `event-dictionary-app.md` — but that
  audit's own writeup covers headline findings and the 9 previously-admitted-broken properties, not a
  line-by-line re-verification of all 55 events. Treat any App event's dictionary entry that says "no
  admitted bug" as "not flagged by either audit," not as "independently confirmed working."
- **Media Audit — 2026-08-29**: "Live in PostHog?" / "Live in Customer.io?" columns use chip-style dropdown
  cells that were spot-checked, not exhaustively read for all 26 rows — mitigated because
  `event-dictionary-media.md` is built primarily from the website event-auditor tool's direct production
  testing, which is more authoritative anyway and corroborates every spot-check performed.
- **Datalabs Audit — 2026-08-29**: "Live in PostHog?"/"Live in Customer.io?" columns were read for the
  ~15 flagged rows in `event-dictionary-datalabs.md` but not transcribed verbatim for the remaining ~30
  rows, which read "No action"/"Confirmed correct" with unremarkable matching volumes.

## Color-coding not preserved

Two DataLabs tabs use cell background color as a status signal that plain-text/CSV extraction cannot
capture:
- `Datalabs - Events`: pink/red text apparently marks "proposed, not yet built" event names and properties
  (List Type, Click Interaction, Scroll Depth, Custom Filter Applied, Pro Lock Interaction).
- `Datalabs - Events Properties`: a Colour Code/Feature legend (green=Live Properties, red=Backlog, orange/
  pink=Capturable, plus unlabeled swatches) whose row-to-color mapping isn't preserved in a CSV/plain-text
  read.

Both are flagged inline in `event-dictionary-datalabs.md` and `property-dictionary.md` wherever relevant —
confirm with the DataLabs project owner before treating an event/property's proposed-vs-live status as
settled based on color alone.

## Website event-auditor: 6 scripted journeys, not full site coverage

`event-dictionary-media.md` is built primarily from a tool that drives 6 specific browser journeys
(anonymous article read, search, freewall/register-gate, newsletter prompt, nav/recirculation, authenticated
identity/save/follow/feed, share, sign-out). Several "Missing" verdicts in that dictionary mean "this
journey didn't trigger it" — for events genuinely outside those 6 paths (paid-flow edge cases, logged-in-
only surfaces the journeys don't reach), absence of evidence is not evidence of absence. The tool's own
report distinguishes "not tested" (trigger never reached) from "missing" (trigger reached, nothing fired) —
that distinction is preserved in the dictionary; don't collapse the two when citing it.

## DataLabs money events explicitly out of scope for live verification

`pro_subscription` and `pro_billing` were explicitly descoped from the 29-Aug DataLabs audit (per that
audit's own Part E instruction) — their "renamed, not yet fully live" status in `event-dictionary-datalabs.md`
is a rollout-timeline read from the sheet's own audit columns, not an independent PostHog/Customer.io
re-verification. Don't treat their absence from live data as a clean pass either way.

## The live Mixpanel/PII incident is still being scoped

As of 29 Aug 2026 (the day this skill was built), the Mixpanel PII-leak investigation
(`platform-routing-rules.md`'s incident section) had:
- No containment access secured yet (neither of Ranjith's two Google identities has GTM publish rights).
- The exact exposure-window origin unconfirmed beyond a Jul 2024 Wayback floor (could predate that).
- The remaining ~30 non-PII-confirmed Mixpanel-referencing GTM tags not individually re-verified.
- The GA4 `page_view`-carries-full-PII finding (bonus finding from the same forensics pass) not yet
  cross-checked against how many other GA4 events share the same mechanism.

Check for newer findings before treating this incident as closed, contained, or fully scoped — it almost
certainly is not, as of this skill's build date.

## Low-confidence transcription in App - Events

Several multi-line cells in the "App - Events" sheet tab were visually truncated at the screen edge during
extraction (marked `[...]` or with a bracketed best-guess completion in the raw extraction files). The
high-confidence fields used in `event-dictionary-app.md` (event names, groups, Status checkmarks/admitted-bug
text, destination checkmarks, SKAN tier labels) are accurate; a few longer free-text cells (e.g. some "Notes"
column entries) were reconstructed with a bracketed best guess and are not directly quoted in the finished
dictionary for that reason. If a specific Notes-column detail is needed verbatim, re-check the live sheet
rather than trusting a `[...]`-marked reconstruction.

## No maintained project-owner list

`change-request-workflow.md` step 3 requires sign-off from "the project owner" for App/Media/DataLabs
analytics changes, but no source read while building this skill names who that is per project. Ask Ranjith
directly rather than guessing a name — this skill does not currently maintain an owner registry.

## This skill is a dated snapshot

Every live-volume number, "confirmed broken"/"confirmed fixed" status, and the Mixpanel incident's scope
reflect verification done on or around **29 August 2026**. Event volumes, bug status, and the PII incident's
containment state will all drift. Re-run the underlying PostHog/Customer.io query (or ask whether a newer
audit has run) before citing a specific number as current if this conversation is more than a couple of
weeks past that date.
