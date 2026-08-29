# Inc42 Media (Website) Analytics Audit — Instructions

**Owner:** [assign name]
**Objective:** Find every event PostHog and Customer.io are actually receiving from inc42.com that is NOT accurately described in the master tracking sheet — either a completely new/untracked event, or a planned event firing with the wrong name/properties/destination.

This document is written so you can follow it top to bottom with no prior context. Every step says exactly where to click.

---

## Part A — Access you need before you start

1. **Google account** with access to the master Sheet below.
2. **PostHog** login (EU cluster) with access to the website project.
3. **Customer.io** login with access to the Inc42 Media (website) workspace.
4. **Ask Ranjith for the latest event-auditor report** (`report.html` + `findings.json`) — this is a tool that already ran automated browser tests against the live site and lives on his machine, not somewhere you can open directly. Get this BEFORE you start Part C — it saves you re-testing things that are already answered.

If you can't get any of these, stop and ask before doing manual work you'd otherwise redo.

---

## Part B — Open and read the source files

### B1. Open the master sheet

1. Open: https://docs.google.com/spreadsheets/d/1n6r5QXe-9Pq1uAWMKRe7zSgLHSejASzAq-BAqeI3L6Y/edit
2. Click the tab **"Inc42 - Media - Events"** at the bottom. ~30 rows: Event Name, Triggers, Trigger Type (Frontend/Backend), Event Property Groups, Custom Event Properties, Triggers Identify Call?, Definition, Destinations.
3. Click the tab **"Inc42 - Media - Events Properties"** next to it. This lists sample values for every property, grouped into Property Group 1, Property Group 2, User Data Fields, Custom Properties, Plus Properties. Skim once so you recognize property names later.

### B2. Known issues — verify current state, do NOT log these as new discoveries

- **Destinations column is stale.** Nearly every row lists GA4, Mixpanel, MoEngage, Amplitude, Meta Ads as destinations. MoEngage's SDK is stubbed out (removed, migrated to Customer.io); Mixpanel and Amplitude were never part of the real stack at all. The tools actually live on the site are **PostHog and Customer.io** — yet across all ~30 rows, PostHog appears as a destination on exactly one row ("Login Modal"). Your job is to find out what PostHog and Customer.io ARE actually receiving (regardless of what this column claims), not to trust this column.
- **Two rows look like an accidental duplicate**: "Newsletter Subscribed" and a row literally named "s" — same trigger, same properties, same destinations. Confirm they're duplicates and flag for cleanup; don't spend audit time treating "s" as a separate real event.
- **"Scroll Depth (Paused)"** — row shows GA4 as the only destination, nothing to PostHog. The event-auditor findings (see Part A4) found THREE separate scroll-depth implementations on the live site with different property formats and none reaching PostHog. Confirm this is still the case.
- **Logged-in users may not be identified in PostHog** — a prior check found `distinct_id` stays an anonymous UUID even when someone is fully signed in (WordPress + Auth0 cookies present). If still true, every "per-user" number you pull from PostHog for logged-in behavior is unreliable — flag this loudly rather than quietly reporting volumes as if they're clean.
- **"Plus Lock"** was previously found firing ~22 times per browsing session to GA4 and 0 times to PostHog. Confirm current state.

### B3. Make your own working copy

1. Right-click the "Inc42 - Media - Events" tab → **Duplicate**. Rename to **"Media Audit — [Your Name]"**.
2. Add columns to the right: `Live in PostHog?`, `Live in Customer.io?`, `Actual Name if Different`, `Actual Properties`, `Classification`, `Recommendation`.

---

## Part C — Read the existing event-auditor findings FIRST

Before manually querying PostHog, open the file Ranjith gave you (`report.html`, or read `findings.json`). This tool already ran 6 scripted user journeys against the live site and found:
- Only 5 of 63 planned events are properly implemented; 24 partial, 32 missing.
- GA4 receives MORE distinct event types than PostHog on the same journeys (autocapture is off, so nothing fills gaps automatically).
- Customer.io receives only page-view calls, zero `track()` (custom event) calls.
- Several "not tested" events had specific reasons (e.g. the freewall/register-gate never rendered during the test runs, so Freewall Lock/Login Modal/Modal Viewed never got a chance to fire) — read these reasons so you don't waste time assuming those are simply broken.

Treat this as your starting checklist, not something to redo from scratch. Your manual work in Parts D–E should focus on: (1) confirming these findings are still accurate today, and (2) finding events outside what those 6 scripted journeys covered — e.g. paid-membership flows, logged-in-only pages, anything behind a form.

---

## Part D — Pull the real event list from PostHog and Customer.io

1. Log into PostHog. Confirm the project switcher (top-left) shows the **Inc42 website project** (project **53557, "Inc42 | Live"**) — not the App or DataLabs project. Re-check this every time you return to PostHog during the task; it can silently switch.
2. Left sidebar → **Data Management → Events**. Set the date range to **last 90 days**. This lists every distinct event name PostHog has actually received, including undocumented ones.
3. Copy every event name into a plain list (a new Google Doc or a sheet tab called "PostHog Raw List").
4. For unfamiliar events, click in → view recent live occurrences → click one → expand its full property payload. Copy/screenshot this — you need real properties, not a guess from the name.
5. Log into Customer.io, confirm you're in the **website workspace**, open **Activity Log / Data Pipelines → Events**, and repeat steps 3–4 for whatever it shows.

---

## Part E — Match everything and fill in your working tab

1. Go back to "Media Audit — [Your Name]."
2. For each row, check your PostHog/Customer.io raw lists for an exact or near-name match. Website event names are Title Case with spaces ("Newsletter Subscribed," "Recommendation Click") — watch for a live event firing under a slightly different label, capitalization, or with the words reordered.
3. Fill `Actual Properties`, `Classification` (Confirmed correct / Renamed / Property mismatch / Broken-not firing / Dead-test event), and `Recommendation` (update sheet to match reality / fix production / needs product owner decision / no action) for every row you check.
4. For anything with no sheet row at all, add it to the new-events table in Part F instead of forcing it into an existing row.

---

## Part F — Log genuinely new events

New tab, **"Media — New Events Found,"** with these exact headers:

| Event name (as seen live) | Platform (PostHog / Customer.io) | First seen | Volume (30 days) | Matches a sheet row? (N — confirmed not in sheet) | Actual properties captured | Classification | Recommendation |
|---|---|---|---|---|---|---|---|

---

## Part G — Priority checks (do these even if you haven't finished everything else)

1. **MoEngage/Mixpanel/Amplitude dead-vendor check.** Confirm none of these three are actually receiving live data — check the site's GTM container and page source for any non-commented-out script tag referencing them. A `grep`/search for the vendor name alone isn't enough — commented-out code will falsely show up as a "hit." If you find any of them still live, that's a P0 (data going somewhere nobody's monitoring) — report immediately.
2. **Identify-call check.** Sign into inc42.com yourself in a fresh browser session, then check PostHog's live event stream for your session — does `distinct_id` switch from an anonymous UUID to something tied to your account? If not, report as P0 — every logged-in analytics number is unreliable until this is fixed.
3. **Scroll depth reconciliation.** Confirm how many separate scroll-depth implementations currently exist on the site and whether any reaches PostHog. If nothing reaches PostHog, note this explicitly — it directly contradicts a locked company strategy decision to restore scroll depth as a real metric, so flag it as a priority, not a routine finding.
4. **Duplicate Newsletter Subscribed rows** — confirm and note for sheet cleanup (low priority, just don't skip logging it).

---

## Part H — Finishing up

1. Confirm both new tabs (`Media Audit — [Your Name]` and `Media — New Events Found`) are fully filled in.
2. Don't edit the original "Inc42 - Media - Events" / "Inc42 - Media - Events Properties" tabs.
3. Message Ranjith with a link to the sheet, which tabs you added, and a one-line summary of any P0s from Part G.
4. Hand this to the cross-project consolidator (Employee 4) as soon as it's done — don't wait to be asked.
