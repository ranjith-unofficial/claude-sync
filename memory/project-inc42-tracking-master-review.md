---
name: project-inc42-tracking-master-review
description: "Gap review (27 Aug 2026) of the combined 'One Inc42 - Analytics | Master Sheet' tracking plan Ranjith built per Utkarsh's ask to unify App/DataLabs/Inc42-Media tracking docs"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5deecc79-ba14-49dd-9b79-cb3772f52f6f
  modified: 2026-08-28T12:55:08.688Z
---

Ranjith combined the per-platform tracking-plan sheets into one Google Sheet, **"One Inc42 - Analytics | Master Sheet"**
(https://docs.google.com/spreadsheets/d/1n6r5QXe-9Pq1uAWMKRe7zSgLHSejASzAq-BAqeI3L6Y), per Utkarsh's ask to "understand
the master and combine" — this is the "tracking plans: update, verify implementation matches, weekly audits, unify into
one master sheet" item from the 21 Aug Sep-planning call ([[project-inc42-fy27-plan]]). 6 tabs: App - Events, App - Event
Properties, Datalabs - Events, Datalabs - Events Properties, Inc42 - Media - Events, Inc42 - Media - Events Properties.

Reviewed line-by-line 27 Aug 2026 (all 6 tabs) against known verified findings ([[project-inc42-event-auditor]],
[[project-inc42-posthog-review]], [[reference-inc42-vendor-stack]], [[project-inc42-strategy-utkarsh]]). Overall the
sheet is genuinely thorough — push telemetry, the `decode` AI-explainer, DPDP `account_delete`, and the DataLabs
dunning-bug remarks are already self-documented inline. Six real gaps found:

1. **Scroll Depth marked "(Paused)"** in Inc42-Media-Events (destination = GA4 only, no PostHog) — directly contradicts
   Utkarsh's locked FY27 strategy, which names "Scroll Depth restore" as an unconditional H1 fix (it's what the A2
   registration-gating holdout measures against).
2. **No `employer`/`seniority`/`company` property anywhere** in the App Person-property dictionary, and
   `sign_in_completed`/`register` events don't set one either — Utkarsh's 24 Aug "capture at sign-in, not signup" ask
   never made it into the schema, not just the one event.
3. **App-Events has zero "Ask" category** — DataLabs-Events has a full 5-event "Ask Datalabs" group (AI Search
   Active/Completed, Ask Feedback, Ask Interaction, Limit Reached) but AskInc42 on the App (ships before Pulse) has no
   instrumentation planned at all.
4. **Destinations columns are stale on both web tabs** — Inc42-Media-Events lists GA4/Mixpanel/MoEngage/Amplitude/Meta
   Ads as the destination for nearly every row (PostHog/Customer.io — the actually-verified live tools — appear on
   exactly one row, "Login Modal"); Datalabs-Events lists MoEngage as a live destination on every row. Both contradict
   [[reference-inc42-vendor-stack]] (PostHog+Customer.io EU; MoEngage removed; Mixpanel/Amplitude aren't in the real
   stack at all).
5. **"User Segment" (fed by MoEngage) not struck through as dead**, unlike the adjacent "Search Result Click"/"Search
   Close" rows which correctly are — same MoEngage-removed issue, just inconsistently flagged within the sheet itself.
6. Minor: rows 10 & 11 in Inc42-Media-Events are duplicate "Newsletter Subscribed" entries — identical
   trigger/definition/properties, looks like an accidental copy.

**How to apply:** before treating this master sheet as ground truth for any app/web build or Sep MOP amendment, check
whether these 6 gaps have been fixed — they weren't as of 27 Aug 2026. Ranjith was offered Asana tickets for the top 3
or folding them into the Sep MOP artifact as the next step; check [[project-inc42-fy27-plan]] for which path he took.
