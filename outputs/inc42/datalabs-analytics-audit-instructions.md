# DataLabs Analytics Audit — Instructions

**Owner:** [assign name]
**Objective:** Find every event PostHog and Customer.io are actually receiving from DataLabs that is NOT accurately described in the master tracking sheet — either a completely new/untracked event, or a planned event firing with the wrong name/properties.

This document is written so you can follow it top to bottom with no prior context on this audit. Every step says exactly where to click.

---

## Part A — Access you need before you start

Confirm you can log into all three of these. If you can't get into any one of them, stop and ask Ranjith for access before doing anything else — don't work around a missing login.

1. **Google account** with access to the Sheet below.
2. **PostHog** login for `app.posthog.com` (or `eu.posthog.com` — INC42's PostHog is hosted on the EU cluster) with access to the DataLabs project.
3. **Customer.io** login with access to the DataLabs workspace.

---

## Part B — Open and read the source files

### B1. Open the master sheet

1. Open this link: https://docs.google.com/spreadsheets/d/1n6r5QXe-9Pq1uAWMKRe7zSgLHSejASzAq-BAqeI3L6Y/edit
2. At the very bottom of the screen you'll see a row of tabs (like Excel sheet tabs). Click the tab named **"Datalabs - Events"**.
3. This tab has one row per event. Columns are: Category, Event, Event Triggers, Event Property Groups, Custom Event Properties, Trigger Identify Call, Source, Destination, Event Description, Remarks. Scroll down — there are roughly 40 event rows, grouped under category headers like "User Engagement," "Search Action," "Table Action," "Ask Datalabs," "Pro Membership," etc.
4. **Read the "Remarks" column on every single row before doing anything else.** Several rows already have a note describing a known bug. Do not skip this — re-finding something already written here wastes your time. The three most important ones to notice now (you'll use them again in Part E):
   - Row for **"Customise Columns Applied"**: remark says the event actually fires in production as **"Customise Column Clicked"** instead.
   - Row for **"Table Sort"**: remark says (1) it also fires a property called "Customise Column Properties" that shouldn't belong to it, and (2) when sorting the company-search table, the `Table Name` property value comes through as `company` instead of `company search`.
   - Row for **"Datalab Onboarding" / "onboarding_lifecycle"**: remark says the completion flag is 99% correct in PostHog but 66% broken in Customer.io — a sync bug between the two tools.
5. Scroll to the very bottom of this tab. You'll see a small color legend: "Live Properties," "Backlog," "People Search," "Captable," each with a different background color. Look back up through the event rows — the ones shaded in one of these colors tell you whether that row is actually shipped ("Live Properties") or still unshipped ("Backlog"). **This color only shows in the live Google Sheet — if anyone gives you a CSV/Excel export of this tab instead, it will look plain white and you'll lose this information. Always work from the live link above, not a downloaded copy.**
6. Now click the tab named **"Datalabs - Events Properties"** next to it. This is the property dictionary — one row per property (e.g. `Page URL`, `User Type`, `subscription_stage`). Skim it once so you recognize property names when you see them later in raw PostHog/Customer.io data. Near the bottom you'll find three special groups — "Lifecycle Envelope," "Subscription," "Billing" — these belong to the two money events covered in Part D.

### B2. Make your own working copy to fill in as you go

1. In the same Google Sheet, right-click the "Datalabs - Events" tab → **Duplicate**. Rename the new tab to **"Datalabs Audit — [Your Name]"**.
2. On this new tab, add these columns after the last existing column (starting in the first empty column to the right): `Live in PostHog?`, `Live in Customer.io?`, `Actual Name if Different`, `Actual Properties`, `Classification`, `Recommendation`. You'll fill these in as you check each row against PostHog/Customer.io in Part C–E.
3. This duplicated tab is where your row-by-row findings live. The separate NEW-events table (Part F) is for events you find that have no row here at all.

---

## Part C — Pull the real event list from PostHog

1. Log into PostHog. In the top-left corner there's a project switcher (it shows the current project name). **Click it and make sure you are on the project named "Inc42 Datalabs | Live" (project ID 66351).** This account has several other INC42 projects (App, Website, staging environments) — if you're on the wrong one you'll get empty or wrong results without an obvious error. Double-check the project name every time you come back to PostHog during this task, not just once at the start — it has been known to silently switch back to a different project mid-session.
2. In the left sidebar, find **Data Management** → click **Events**. This page lists every distinct event name PostHog has ever received on this project — including ones nobody documented anywhere. This is your ground truth.
3. At the top of this list there's a date range filter — set it to **last 90 days**.
4. Sort or scan this full list. For each event name, note whether it also shows a rough volume count.
5. **Copy every event name from this list into a plain list** (paste into a blank Google Doc or a new sheet tab called "PostHog Raw List") — you'll cross-check this against the sheet in Part E.
6. For events you don't recognize or that look unfamiliar, click into the event name. This opens a detail view. Click **"View recent events"** or the equivalent button showing a live feed of that event firing. Click on one individual event occurrence — it expands to show the full JSON of properties sent with that event. **Screenshot or copy this raw property list** for any event you flag as unmatched in Part E — you need the actual properties, not a guess based on the event's name.

---

## Part D — Pull the real event list from Customer.io

1. Log into Customer.io. Make sure the workspace selector (top-left or top-right, depending on your account) shows the **DataLabs** workspace, not the App or website workspace.
2. In the left sidebar, look for **Activity Log** or **Data Pipelines → Events** (the exact menu label can vary by Customer.io plan — if you don't see either, search "Activity" in Customer.io's own search bar).
3. This shows a live/recent feed of events Customer.io has received. Filter or scroll to see the full range of distinct event names over the last 90 days if the interface allows a date filter; otherwise scroll back as far as you reasonably can.
4. Same as PostHog: copy every distinct event name into your "PostHog Raw List" doc (add a second column or section labeled "Customer.io").
5. Click into individual event instances the same way to see their actual property payload for anything unfamiliar.

---

## Part E — Match everything and fill in your working tab

1. Go back to your "Datalabs Audit — [Your Name]" tab from Part B2.
2. For every row (every planned event from the sheet), check your PostHog Raw List and Customer.io Raw List: does an event with this exact name appear? Mark `Live in PostHog?` / `Live in Customer.io?` as Yes/No.
3. **Watch for near-matches, not just exact text matches.** The sheet itself already told you one case where the live name differs from the planned name (Customise Column Clicked vs Applied) — there may be others nobody's written down yet. If a live event name looks like it could be the "real" version of a planned row even though the text doesn't match exactly, note it in `Actual Name if Different` and investigate its properties to confirm.
4. For the "Customise Columns Applied" and "Table Sort" rows specifically: confirm the known bugs from Part B1 are still happening exactly as described, and write "confirmed still happening" or "appears fixed" in the Remarks — don't just assume the old note is still accurate.
5. For any live PostHog/Customer.io event name that has **no corresponding row at all** in the sheet, don't try to force-fit it into an existing row — instead add it as a new row in the separate table described in Part F.
6. For every row/event you touch, fill in `Actual Properties` with what you actually saw in the raw payload (Part C step 6 / Part D step 5), and `Classification` with one of:
   - **Confirmed correct** — matches the sheet exactly, no action needed
   - **Renamed** — same behavior, different live name than the sheet says
   - **Property mismatch** — right event, wrong/missing/extra properties
   - **Broken/not firing** — the sheet describes it but you found zero occurrences in either tool
   - **Dead/test event** — fires from an old code path or staging environment, safe to ignore
7. Fill `Recommendation` with one of: *update sheet to match reality* / *fix production to match sheet's intended name or properties* / *needs product owner decision* / *no action — confirmed correct*.

---

## Part F — Log genuinely new events in a separate table

Create a new tab in the same Google Sheet called **"Datalabs — New Events Found."** Use exactly these column headers in row 1:

| Event name (as seen live) | Platform (PostHog / Customer.io) | First seen | Volume (30 days) | Matches a sheet row? (N — confirmed not in sheet) | Actual properties captured | Classification | Recommendation |
|---|---|---|---|---|---|---|---|

Add one row per genuinely new event you found in Part C/D that had no corresponding sheet row at all, using the same `Classification`/`Recommendation` options as Part E step 6–7.

---

## Part G — Priority check: the two money events (do this even if you haven't finished everything else)

`pro_subscription` and `pro_billing` are the two most sensitive events on this whole sheet — they're sourced from real WooCommerce + Razorpay payment webhooks, and the sheet has an explicit rule: **these two events must NEVER be connected to an ads platform**, because a failed renewal must never fire a Meta/Google "purchase" conversion.

1. In PostHog Data Management → Events, confirm both `pro_subscription` and `pro_billing` are present and firing with these exact properties:
   - `pro_subscription` should carry: `subscription_stage`, `trial_end_at`, `current_period_end_at`, `next_charge_amount`, `renewal_count`, `mandate_status`.
   - `pro_billing` should carry: `billing_stage`, `order_id`, `order_type`, `amount`, `renewal_count`, `failure_reason`.
2. Log into **Meta Ads Manager** → Events Manager, and separately **Google Ads** → Tools → Conversions. In each, look at the list of configured conversion events/sources. Check whether `pro_subscription` or `pro_billing` (or any Customer.io event fed by them) appears anywhere in that list.
   - If either does appear as a conversion source: **stop and report this immediately to Ranjith as a P0 finding** — don't wait until your full audit table is done. This is a live business-risk bug, not a documentation gap.
3. In Customer.io, open any live campaign/workflow that triggers off `pro_billing`. Check the trigger condition: does it branch only on "performed pro_billing" with no property filter? If so, it cannot tell a successful renewal from a failed one — check what message that campaign actually sends, and whether it's currently sending the wrong message to people whose payment failed. **Report this as a P0 finding too if you find it**, don't fold it quietly into the main table.

---

## Part H — Finishing up

1. Make sure both new tabs you created (`Datalabs Audit — [Your Name]` and `Datalabs — New Events Found`) are filled in completely — every row from the original sheet should have a Yes/No/note in your working tab, and every genuinely new event should be a row in the New Events tab.
2. Do not delete or edit the original "Datalabs - Events" / "Datalabs - Events Properties" tabs — your findings go in your own new tabs only.
3. Message Ranjith (or whoever is coordinating this) with: a link to the sheet, which two tabs you added, and a one-line summary of anything you marked P0 in Part G.
4. Your output feeds directly into the cross-project consolidator's work — don't wait for a follow-up request to hand it over, send it as soon as both tabs are complete.
