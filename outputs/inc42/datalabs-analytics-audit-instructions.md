# DataLabs Analytics Audit — Instructions

**Owner:** [assign name]
**Objective:** Find every event PostHog and Customer.io are actually receiving from DataLabs that is NOT accurately described in the master tracking sheet — either a completely new/untracked event, or a planned event firing with the wrong name/properties.

---

## Files and tools you need — open all four before starting

1. **Google Sheet, tab "Datalabs - Events"** (the event list — ~40 rows across 15 categories)
   https://docs.google.com/spreadsheets/d/1n6r5QXe-9Pq1uAWMKRe7zSgLHSejASzAq-BAqeI3L6Y/edit — click the "Datalabs - Events" tab at the bottom.
2. **Same Sheet, tab "Datalabs - Events Properties"** (the property dictionary — ~820 rows: Page/User/Interaction/Content property groups, plus a full "Lifecycle Envelope"/"Subscription"/"Billing" section near the bottom for the two money events).
3. **PostHog** — project **66351, "Inc42 Datalabs | Live"** (EU cloud). If your PostHog login defaults to a different project, switch explicitly — this account has 6+ projects and it silently reverts mid-session sometimes, so re-check the project name in the top-left before every query, not just at the start.
4. **Customer.io** — the DataLabs workspace. Activity Log / Data Pipelines → Events.

Do NOT work from the CSV export of these tabs if you were given one — CSV export strips the row background color-coding (a legend at the bottom of "Datalabs - Events" marks Live Properties / Backlog / People Search / Captable in color). You need the live Sheet to see which rows are actually shipped vs still backlog.

---

## Background — read the Remarks column first, on every row

The "Datalabs - Events" tab already self-documents several known planned-vs-actual mismatches in its Remarks column. Read every remark before you start hunting — these are confirmed, not things to re-find:

- **Customise Columns Applied** — the sheet's intended name. Production actually fires the event as **"Customise Column Clicked."** Confirm this is still true; don't log it again as a new finding, just verify current state.
- **Table Sort** — two known issues: (1) it also triggers the "Customise Column Properties" property, which shouldn't belong to this event; (2) when sorting the company-search table specifically, the `Table Name` property comes through as `company` instead of the intended `company search`.
- **onboarding_lifecycle** — `datalabs_onboarding_complete` is 99% populated correctly in PostHog but 66% broken in Customer.io. This is described as a sync bug between the two tools, not a missing field on either side — don't spend time re-diagnosing which tool is "wrong," both should already agree on the same underlying value.
- **entry_page_type** (on `user_registered`) — currently event-only; it's supposed to also persist as a user/person property but doesn't yet, which is why a specific segmentation (Journey B vs C) can't be evaluated at enrollment. Flag whether this has been fixed.

Your job is to find mismatches like these that AREN'T already flagged in the Remarks column, plus any event PostHog/Customer.io is receiving that has no row in the sheet at all.

---

## Special priority: the two money events

Rows for **`pro_subscription`** and **`pro_billing`** (bottom of the "Pro Membership" section, just above the color-legend rows) are the most tightly specified rows in the whole sheet — backend-only, sourced from WooCommerce + Razorpay webhooks, with an explicit rule: **NO ads destination should ever receive these**, because a failed renewal must never fire a Meta/Google conversion event.

Before doing anything else on this audit, check this specifically:
1. In PostHog, confirm `pro_subscription` and `pro_billing` are landing with the full property set the sheet specifies: `subscription_stage`, `trial_end_at`, `current_period_end_at`, `next_charge_amount`, `renewal_count`, `mandate_status` (subscription) and `billing_stage`, `order_id`, `order_type`, `amount`, `renewal_count`, `failure_reason` (billing).
2. Check whether either event is mapped as a conversion source in Meta Ads Manager or Google Ads. If either is, that's a P0 finding — report it immediately, don't wait for the full audit to finish.
3. Note in the sheet's own words: a bare Customer.io condition like "performed pro_billing" can't distinguish a successful renewal from a failed one (no attribute filter on the event itself) — check whether any live Customer.io campaign is actually branching on the bare event rather than on `billing_stage`/`subscription_stage`. If you find one, that's also a P0 finding, not a documentation nitpick — it likely means Customer.io has already sent the wrong message to someone.

---

## Method — step by step

1. **Build your baseline.** From "Datalabs - Events," list all ~40 event names + which category each belongs to. From "Datalabs - Events Properties," note which property group (Page/User/Interaction/Content/Lifecycle Envelope/Subscription/Billing) each property belongs to.
2. **Pull PostHog's real event list.** PostHog → Data Management → Events. This lists every distinct event name the project has ever received, including ones nobody defined in the sheet. Set the date range to last 90 days and note volume per event.
3. **Pull Customer.io's real event list.** Activity Log / Data Pipelines → Events, same approach.
4. **Match each live event name to a sheet row.** Watch for near-matches, not just exact string matches — the sheet itself documents at least one case (Customise Column Clicked/Applied) where the live name differs from the planned one. A live event that looks unrelated by name might still be the "real" version of a planned row.
5. **For anything unmatched, open 5–10 raw event payloads** (PostHog: click into the event → "..." → view raw properties) and record the actual property names/values being sent — do not guess from the event name alone.
6. **Classify each unmatched or mismatched event:**
   - Renamed version of a planned event (name differs, behavior matches)
   - Property-level mismatch (name matches, one or more properties are wrong/missing/extra)
   - Genuinely new, untracked behavior (no corresponding row at all)
   - Dead/test/debug event (fires from a staging environment or old code path, negligible volume, safe to ignore)
7. **Check the live-vs-backlog color coding** in the Sheet for anything you flag as "new" — a "new" event might actually already be a known backlog item, not a surprise.

---

## Deliverable

One table, plus the separate money-events note from the section above:

| Event name (as seen live) | Platform (PostHog / Customer.io) | First seen | Volume (30d) | Matches a sheet row? (Y – which row / N) | Actual properties captured | Classification | Recommendation |
|---|---|---|---|---|---|---|---|

**Recommendation options:** update the sheet row to match reality · fix production to match the sheet's intended name/properties (this is the case for Customise Column Clicked/Applied — likely a naming bug, not a spec problem) · add as a new row · kill (dead code) · escalate (money events / P0s).

**Where this goes next:** hand your finished table to the cross-project consolidator (Employee 4), who merges it with the App and Media findings into one master report.
