# Event dictionary — DataLabs (PostHog project 66351, "Inc42 Datalabs | Live")

Source: "Datalabs - Events" tab (46 planned events) + "Datalabs Audit - 2026-08-29" tab (live PostHog +
Customer.io re-verification) + "Datalabs - New Events Found" tab.

**Vendor-stack correction — apply to every row below**: nearly every row in the source sheet lists
Destination = "Customer.io, PostHog, Mixpanel, GA4, MoEngage, Meta Ads, Google Ads, LinkedIn Ads,
UserGuiding," unchanged, for almost all 46 events. **MoEngage is confirmed removed.** Mixpanel was believed
dead but is now confirmed live and leaking PII on the *website* (see `platform-routing-rules.md`) — its
presence specifically on DataLabs pages has not been separately confirmed or ruled out, so treat any
DataLabs event routed to Mixpanel as an open question, not a safe assumption either way, and never add a
new one. Only Customer.io, PostHog, GA4, Meta/Google/LinkedIn Ads, and UserGuiding in this column should be
treated as plausibly real destinations.

## Money events — read `platform-routing-rules.md` before touching either of these

### `pro_subscription` (Pro Membership)
- **Trigger**: ACCESS state changed. One event, `subscription_stage` carries the meaning. Backend only
  (WooCommerce + Razorpay webhooks).
- **Properties**: Lifecycle Envelope group (product, product_id, subscription_id, payment_method, currency,
  plan_interval, plan_interval_count, next_charge_at, occurred_at, source, schema_version — all REQUIRED) +
  Subscription group (subscription_stage: trial_started/charge_upcoming/cancel_scheduled/mandate_revoked/
  access_ended_voluntary/access_ended_involuntary/reactivated; trial_end_at; current_period_end_at;
  next_charge_amount; renewal_count; mandate_status: active/revoked/paused/none).
- **Destinations**: Customer.io, PostHog — **ads destinations deliberately excluded.**
- **Status**: **Renamed event, not yet fully live per the 29-Aug audit** — Actual Name column reads "N/A
  (renamed event not yet live)"; explicitly DESCOPED from the 29-Aug audit's verification (see Part E of the
  audit instructions), so its absence from live PostHog/CIO data is not evidence it's broken.
- **Known gotchas (carry forward verbatim)**: "NO ads destinations — a failed renewal must never fire a
  Meta/Google conversion. Replaces the state-check 'Trial Started' automation. **CAMPAIGN BUILD WARNING:
  never branch on a bare CIO `Event` condition for this event — it has no attribute filter, so 'performed
  pro_subscription' is true for ANY stage. Branch on profile attributes or a segment.**"

### `pro_billing` (Pro Membership)
- **Trigger**: MONEY moved, or failed to. Backend only (WooCommerce + Razorpay webhooks).
- **Properties**: Lifecycle Envelope group (same as above) + Billing group (billing_stage:
  purchase_succeeded/first_charge_succeeded/renewal_succeeded/first_charge_failed/renewal_failed/
  checkout_abandoned/refunded; order_id; order_type: parent/renewal; amount; renewal_count; failure_reason).
- **Destinations**: Customer.io, PostHog — **ads destinations deliberately excluded.**
- **Status**: Same as `pro_subscription` — renamed, not yet fully live, explicitly DESCOPED from the 29-Aug
  audit.
- **Known gotchas (carry forward verbatim)**: "NO ads destinations — a failed renewal must never fire a
  Meta/Google conversion. Distinct from the existing frontend 'Pro Payment' funnel event, which stays as-is
  for ads/CAPI. **CAMPAIGN BUILD WARNING: a bare CIO `Event` condition ('performed pro_billing') is TRUE for
  renewal_failed as well as renewal_succeeded — it cannot tell success from failure. Exit the grace sequence
  on pro_subscription_status != past_due, never on the event.**" Also: "leaveing abandoned as per
  discussion" [sic, sheet's own wording].
- **Additional gotcha, carried forward verbatim from `property-dictionary.md`'s Billing group**: "a bare
  Customer.io 'performed pro_billing' condition cannot by itself distinguish `billing_stage=
  first_charge_succeeded` from `billing_stage=first_charge_failed` — always branch dunning/win-back logic on
  `billing_stage`, never on the bare event name." (This is the exact note referenced in prior dunning-project
  memory — see `project-inc42-datalabs-dunning.md`.)

## User Engagement

| Canonical name | Planned name (if different) | Fires when | Properties | Identify? | Destinations | Status | Known gotchas |
|---|---|---|---|---|---|---|---|
| `user_registered` | `Registered` (renamed + 2 new properties) | New user registration | register_source, entry_page_type, registration_page_url | Yes | Customer.io, PostHog (+ see vendor correction for the rest) | **Renamed, not yet fully live** per 29-Aug audit — "N/A (renamed event not yet live)," needs product-owner confirmation of rollout timeline. | `entry_page_type` MUST also persist as a **user property**, not just an event property — today `DL Page Type` is event-only, which is why Journey B-vs-C assignment can't be evaluated at enrollment. Original sheet remark: "Difficult to track, Auth0 dependency." |
| `Login` | — | User login | (none listed beyond standard groups) | Yes | (see vendor correction) | Live (no audit finding flagged) | |
| `Pro Trial` | — | User's pro trial begins | Trial Type, Trial Stage, event_id/event_name/event_time/fbp | — | Frontend | ✓ No action (29-Aug audit). | |
| `Register Lock Interaction` | Sheet's own Event cell reads a broken two-line fragment "Lock Type / Lock Interaction" | User interacts with the freewall lock | Lock Type (Short Lock/Long Lock), Button Interaction (Load/Click) | — | (see vendor correction) | **Sheet issue, not a production bug** — 29-Aug audit classification "Renamed / sheet issue": the sheet's Event cell itself needs fixing to read the single clean name "Register Lock Interaction." | Separately confirmed alive again at ~1,000/wk, 3,364 people/30d (per dunning-project memory) after being called dead since 18 May in an earlier funnel doc — don't cite that older "dead" status. |
| `Logout` | — | Manual logout | — | — | Frontend | Not flagged in 29-Aug audit (assume "No action"). | |
| `Export Interaction` | — | Any interaction on the export feature | Data Type, Export Stage, Export Type, File Format, Profiles Exported | — | Frontend | Not flagged. | Appears twice in the source sheet with different property-completeness — treat the fuller listing (Data Type/Export Stage/Export Type/File Format/Profiles Exported) as current. |

## Onboarding

| Canonical name | Planned name (if different) | Fires when | Properties | Identify? | Destinations | Status | Known gotchas |
|---|---|---|---|---|---|---|---|
| `onboarding_lifecycle` | `Datalab Onboarding` (renamed) | Onboarding progress | onboarding_stage: step_1/step_2/step_3/completed | Yes | Customer.io, PostHog (+ vendor correction) | **Renamed, not yet fully live** per 29-Aug audit rollout-timeline caveat — but its completion flag WAS independently re-confirmed: **99.03% correct in PostHog (5,033 of 5,082 completers), exact-count match to the sheet's "99%" claim.** Customer.io side not re-verified this run. | Current enum starts at "Onboarding Step 2" — **first-step drop-off is unmeasurable** because there's no step_1 value yet in production (the rename is meant to add it). Historical gotcha, still relevant until the sync is confirmed fixed: "99% populated in PostHog but 66% broken in Customer.io — the SYNC is the bug, not the field." |

## Search Action

| Canonical name | Fires when | Properties | Status | Known gotchas |
|---|---|---|---|---|
| `Search Active` | First click on global search bar | Search Type, Search Source, Search Content | Not flagged in 29-Aug audit. | |
| `Search Completed` | Search results generated & displayed | Search Type, Search Source, Search Query | Not flagged. | |
| `Advanced Filter Clicked` | Advanced Filter button opened/closed | Advanced Filter State, Table View | Not flagged. | `Advanced Filter State` appears twice in the property dictionary with two different value sets (True/False in one place, Open/Closed in another) — likely a sheet duplication, verify which is live before using. |
| `Advanced Filter Applied` | Filter applied | Filter Property Type, Filter Property Value, Table View | Not flagged. | `Filter Property Type`/`Filter Property Value` carry the entire company/investor/funding/acquisition search filter taxonomy — see `property-dictionary.md` for the full field list, do not re-derive it here. |
| `Customize Columns Applied` | Column order customized | Customise Column Properties | **Bug shape changed, sheet is stale** — 29-Aug audit: the OLD documented bug ("fires as 'Customise Column Clicked'") is **no longer what's happening**. Live name is now `Customize Columns Applied` (US spelling, differs from the sheet's planned "Customise Columns Applied"). | Update the sheet's remark — it currently describes a bug that has since drifted into a different bug (a spelling/naming mismatch, not a wrong-event-name mismatch). Decide whether to standardize on "Customise" (matches the rest of the property naming) or "Customize." |

## Table Action

| Canonical name | Fires when | Properties | Status | Known gotchas |
|---|---|---|---|---|
| `Table Sort` | Table sorted asc/desc | Table Name, Table Sort Column Name, Table Sort Order(by), Table View | **Both previously-documented bugs confirmed still live** (29-Aug audit, 2 payloads sampled) + one new one found. | (1) `Customise Column Properties` also fires redundantly on this event. (2) On the company-search table specifically, `Table Name` still comes through as `"company"` instead of `"company search"`. (3) **New finding**: the correct property name is `Table Sort Orderby`, not `Table Sort Order` as previously documented — update the sheet. |
| `Table Pagination` | Next/previous page clicked | Table Name, Pagination Page Number, Table View | Not flagged. | |

## Feedback / User Interaction

| Canonical name | Fires when | Properties | Status | Known gotchas |
|---|---|---|---|---|
| `Form Submitted` | Feedback form submitted | Form Type (Download Report / View Report) | Not flagged. | Identify call fires specifically for Form Type = Download Report or View Report. |
| `Tab View` | Interaction with a profile sub-section tab | Section Name, Tab Name, Data Visualisation Metric Type, Chart Type, Date Range | Not flagged. | Sheet notes a planned rename to "Section Interaction." Designed specifically for tables inside a tab (e.g. "Funding amount over time" under the Funding tab). |
| `Edit Interaction` | Edit action on profile/list/saved search | Edit Type, Edit Field, Edit Source, Edit Status, Edit Item ID | Not flagged. | Covers all edit actions except delete. |
| `Checkbox Interaction` | Any checkbox interaction | Checkbox Type, Data Type, Selection Source, Selection Status | Not flagged. | |
| `List Interaction` | Any list create/add/delete action | List Interaction Type, List Interaction Source, List ID, List Type | Not flagged. | `List Type` is marked red/unconfirmed in the source sheet's color-coding — verify it's actually live before treating it as a shipped property. |
| `Alert Interaction` | Alert enable/disable/frequency/delivery change | Alert Type, Alert Status, Alert Content, industry_alert_subscribed (user property) | Not flagged in this audit. | **Separate finding (dunning-project memory)**: this event fires 1,831× for 1,815 people as a page-load state readout, not a real action — its retention "lift" in other analyses is spurious. Don't treat raw volume as engagement. |
| `Click Interaction` | Any button interaction | Button Type, Button Interaction, Button Content | Marked pink/red (proposed, not yet in production) in the source sheet's color-coding — unconfirmed live. | |
| `Scroll Depth` | Page scroll | Scroll Percentage | **Confirmed partially live, fresh rollout** — 29-Aug audit: live in PostHog as **lowercase `scroll_depth`** (not "Scroll Depth" as planned), only 2 events since 2026-08-12. Zero Customer.io matches. | Looks like a fresh/incomplete rollout rather than simply broken — confirm rollout status with engineering before treating as a bug. Marked red/proposed in the sheet's color-coding, consistent with "not fully shipped yet." Do not confuse with the Website's separate, much more broken scroll-depth situation in `event-dictionary-media.md`. |
| `Custom Filter Applied` | Dropdown/subtab filters on a profile page | Section Name, Filter Type, Filter Value | **Confirmed broken — not firing** (29-Aug audit). | Marked red/proposed in the sheet's color-coding. |
| `Demo Call` | Demo-call button clicked | Booking Stage, Modal Name, Modal Type | **Platform gap** — fires to Customer.io (<1% of profiles) but has **zero occurrences in PostHog's 90-day event list.** | Confirm whether the PostHog SDK call was ever wired for this event at all — needs engineering investigation, not just a product decision. |
| `Demo Call Booked` | Demo call booking completed | event_id, event_time, fbp | Same platform-gap pattern as `Demo Call`. | Same — PostHog SDK call possibly never wired. |

## Plus / Pro Membership

| Canonical name | Fires when | Properties | Status | Known gotchas |
|---|---|---|---|---|
| `Cancel Plus Membership` | User intends to cancel Plus | Plus Cancellation State | **Confirmed broken — not firing** (29-Aug audit). | |
| `Pro Lock Interaction` | Interaction with a Pro-gated feature | Modal Type, Modal Name | Marked pink/proposed in the sheet's color-coding — unconfirmed live. | Sheet's own description text appears copy-pasted from an adjacent row ("When user intends to cancel Datalabs Pro membership") — verify the real trigger description against the live sheet before treating it as accurate. |
| `Pro Payment` | Datalabs Pro purchase initiated | Payment Stage, Pro Membership Type | Backend-sourced. | Same copy-paste description caveat as `Pro Lock Interaction`. **Also independently seen firing on the Media/website side** (`event-dictionary-media.md`'s "Events live but not in the sheet" — 548/90d) — needs a product-owner decision on which project actually owns this event; it may be a cross-surface event, not DataLabs-exclusive. |
| `Cancel Pro Membership` | User intends to cancel Pro | Pro Cancellation State, Pro Membership Type | **Confirmed broken — not firing** (29-Aug audit). | |
| `Plus Subscribed` | Plus subscription confirmed | (rich payload, 34 attributes on Customer.io, not individually inspected) | **Live, real, undocumented** — found in "Datalabs - New Events Found": 106 events/90d PostHog (first seen 2026-06-02), 48 CIO profiles, 0 in the last 30 days. | Not in the sheet at all — it's the subscribe/confirm counterpart to the documented `Cancel Plus Membership` row. Add a row. |

## Ask Datalabs

| Canonical name | Fires when | Properties | Status | Known gotchas |
|---|---|---|---|---|
| `AI Search Active` | Search box clicked to type a prompt | Search Type | Not flagged. | |
| `AI Search Completed` | Prompt submitted | Search Type, Prompt Type | Not flagged. | |
| `Ask Feedback` | Feedback submitted on an AI response | Response Feedback (Positive/Negative) | Not flagged. | |
| `Ask Interaction` | Click on an AI-generated link | Interaction Type: Click; Click Type: Source Button/Source Link/Copy/New Chat | Not flagged. | |
| `Limit Reached` | Daily prompt limit hit | (none listed) | Not flagged. | Sheet's own description text is copy-pasted from `Ask Interaction`'s row — verify the real trigger wording before quoting it. **Separately, dunning-project memory found this fires only 8× for 3 people in 60 days, all on the AI query cap** — very low real usage, not indicative of a broken event, just a rarely-hit limit. |
| `master_agent_query` | Backend query-classification/orchestration for AI Search / Ask Datalabs | query, query_type (discovery/company/sector/funding/people/ranking/comparison/investor/advisory/out_of_scope), mode (thinking/fast/deep_research), complexity, elapsed_ms, tool_count, source_count, entity_count, cache_status, cache_age_seconds, **evidence_density, ungrounded_claims**, has_followups, is_fallback, fallback_model, timeout_warning, has_enrichment, agent_attempt, response_length, body_length | **Live, real, undocumented — the single most valuable find in the 29-Aug new-events audit.** PostHog only (2,359 events/90d, first seen 2026-05-31), not expected on Customer.io. | Carries answer-quality signals (`evidence_density`, `ungrounded_claims`) not captured anywhere else in the documented Ask Datalabs event set. Add to the sheet under the Ask Datalabs category — needs product-owner review to decide what should be formally tracked from this payload before treating Ask Datalabs instrumentation as complete. |

## Saved Search, Sidebar, Report, Data Verification, My Feed, Credits, Export

| Canonical name | Fires when | Properties | Status | Known gotchas |
|---|---|---|---|---|
| `Saved Search Interaction` | Create/update/delete a saved search | Saved Search Type, Saved Search Interaction Type, Search Search Source (likely sheet typo for "Saved Search Source"), Saved Search ID | Not flagged. | |
| `Sidebar Interaction` | Sidebar action (desktop) | Set Sidebar State | Not flagged. | |
| `Report Interaction` | Interaction on a published report | Access Type, Access URL, Report Name | Not flagged in the DataLabs audit. | **Cross-check `event-dictionary-media.md`**: a `Report Interaction` event also appears in the website's event-auditor findings (name-drifted from planned "Report View," 1,356/30d as of 23 Aug but found at ZERO volume, stopped 2 Jul, in the 29-Aug Media new-events check) — confirm whether this is the same event double-counted across projects or two independently-built events before treating either dictionary entry as complete. |
| `Data Verification` | Interaction on a company-data verification flow | Verification Stage, Verification Type | **Confirmed broken — not firing** (29-Aug audit). | |
| `Feed Interaction` | Interaction on My Feed | Feed Filter Type, Feed Filter Value | Not flagged. | |
| `Post Interaction` | Interaction on a feed post | Post ID, Button Type, Button Interaction, Button Content | Not flagged. | Category attribution in the source sheet is ambiguous (may be "My Feed" or a new category) — verify against the live sheet if the exact grouping matters. |
| `Credit Payment` | Purchase additional credits | Credit Payment Stage, Credit Topup Plan | Not flagged in this audit, but **dunning-project memory found zero purchases since 22 Apr, 3 of 4 packs have no purchasable SKU, and the event has no completion stage** — treat as effectively dead for any win-back/monetization proposal even though this audit didn't independently re-flag it. | |
| `Export Interaction` | Export feature interaction | Data Type, Export Stage, Export Type, File Format, Profiles Exported | Not flagged. | |

## Events live but not in the sheet ("Datalabs - New Events Found", 29 Aug 2026)

| Canonical name | Platform | Volume | Classification | Recommendation |
|---|---|---|---|---|
| `Login Modal` | Customer.io (3 profiles) + PostHog (4 events) | 0 in last 30 days on either platform; date-order between platforms is inconsistent (worth a second look, not resolved here) | Dead-test event | No action — appears to be an abandoned test/legacy event; confirm with engineering it's not still wired anywhere before deleting. |
| `Plus Subscribed` | See "Plus / Pro Membership" section above | — | — | — |
| `master_agent_query` | See "Ask Datalabs" section above | — | — | — |

## Known gaps in this audit
- **`pro_subscription`/`pro_billing` were explicitly out of scope for the 29-Aug live audit** — their
  "not yet live" status above is a rollout-timeline read, not an independent production re-verification.
  Do not treat their absence from live PostHog/CIO data as a clean pass.
- Live-in-PostHog/Customer.io volumes were read for the flagged rows above but not transcribed for all 46
  rows verbatim — the majority not listed here read "No action"/"Confirmed correct" with unremarkable
  matching volumes. See `open-gaps.md`.
- The tab's color-coding (rows in pink/red/orange marking proposed-vs-live status) is referenced above
  wherever noted but is not independently confirmed — verify with the DataLabs project owner before treating
  color as a status signal.
