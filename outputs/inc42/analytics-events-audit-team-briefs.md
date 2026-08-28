# One Inc42 Analytics — Team Briefs (28 Aug 2026)

Source: "One Inc42 - Analytics | Master Sheet"
https://docs.google.com/spreadsheets/d/1n6r5QXe-9Pq1uAWMKRe7zSgLHSejASzAq-BAqeI3L6Y

Scope: App, Inc42 Media (website), DataLabs. IP (ticketing/report-purchase funnel) deprioritized per Ranjith.

Proposed assignment — swap names as needed:
- **Employee 1** — App
- **Employee 2** — Inc42 Media (website)
- **Employee 3** — DataLabs
- **Employee 4** — Cross-project QA / Consolidator (starts after 1–3 finish a first pass)
- **Intern** — Knowledge base (starts once Employee 4's consolidated report exists)

---

## Employee 1 — App: PostHog + Customer.io reconciliation

**Objective:** Find every event PostHog and Customer.io are actually receiving from the Inc42 app that is NOT one of the 98 rows in the "App - Events" tab (or fires with different properties than the "App - Event Properties" tab defines). We are not re-testing whether planned events fire — we're hunting for events the sheet doesn't know about.

**Where to look:**
1. PostHog project **146258 (Inc42 App)**, EU cloud. Data Management → Events (lists every distinct event name PostHog has ever seen, including ones nobody defined). Cross-check against Activity/Live events for the last 30 days for volume.
2. Customer.io — the App workspace. Check the Activity log / Data Pipelines "Events" list the same way.

**Known leads to verify first (don't rediscover, confirm current state):**
- 17 Aug PostHog review found `push_delivered` never fired and `push_opened` fired only twice despite 67% push opt-in — check if that's still true.
- Same review found `decode` (the AI explainer) has zero telemetry — confirm whether it's shipped-uninstrumented or still unshipped.
- No internal/beta-user exclusion exists in this project — 34 of 168 early "active" users are pre-12-Aug beta/internal people with no filterable property. **Any volume number you report must note this pollution risk**, don't present raw counts as clean external user behavior.

**Method:**
1. Pull the full distinct event-name list from PostHog for the last 90 days.
2. For each event name NOT in `App - Events` (or in it but with a different property set than `App - Event Properties` defines), open 5–10 raw event payloads and record the actual properties sent.
3. Classify each: dead/debug event, renamed version of a planned event, test-environment leak, or a genuinely new untracked behavior.
4. Repeat for Customer.io.

**Deliverable (one sheet/table):**

| Event name (as seen live) | Platform (PostHog/CIO) | First seen | Volume (30d, flag if internal-user-polluted) | Matches a sheet row? (Y – row ref / N) | Actual properties captured | Suspected origin | Recommendation |
|---|---|---|---|---|---|---|---|

**Recommendation column options:** add to sheet as new row · rename to match an existing planned event · kill (dead code) · needs product owner decision.

---

## Employee 2 — Inc42 Media (website): PostHog + Customer.io reconciliation

**Objective:** Same exercise as Employee 1, for inc42.com, against the "Inc42 - Media - Events" tab (30 rows).

**Start here, don't rebuild it:** there is already a working automated auditor for this exact site at `~/ClaudeDocs/inc42/event-auditor/` (`node audit.mjs`). It already found: only 5 of 63 planned events properly implemented, GA4 receiving MORE distinct event types than PostHog (autocapture is off, so nothing fills gaps automatically), `Plus Lock` firing ~22×/run to GA4 and 0× to PostHog, Customer.io receiving only `page` calls and zero `track()` calls, and three parallel scroll-depth implementations none of which reach PostHog. Read `runs/<latest>/report.html` and `findings.json` before you start manual digging — your job is to (a) sanity-check those findings are still current and (b) find events that tool's 6 scripted journeys wouldn't hit (things outside its test paths — e.g. paid-flow edge cases, logged-in-only surfaces).

**Known contradictions already on record — verify current state, don't re-discover:**
- The sheet's Destinations column lists GA4/Mixpanel/MoEngage/Amplitude/Meta Ads for nearly every row. MoEngage is removed from the real stack (SDK stubbed out since migration to Customer.io) and Mixpanel/Amplitude were never in the real stack at all. PostHog and Customer.io — the tools actually live on the site — appear as a destination on exactly 1 of 30 rows ("Login Modal").
- Rows 3 & 4 ("Newsletter Subscribed" / "s") look like an accidental duplicate — confirm and flag for cleanup, don't spend audit time on it.
- Signed-in users never get `identify()` called on PostHog (distinct_id stays an anonymous UUID even with WordPress + Auth0 session cookies live) — this affects how you should interpret any per-user volume number.

**Method:** same as Employee 1 — Data Management → Events in PostHog project **53557 (Inc42 | Live)**, plus Customer.io Activity log for the website workspace, minus 90 days, classify anything not matching a sheet row.

**Deliverable:** same table format as Employee 1.

---

## Employee 3 — DataLabs: PostHog + Customer.io reconciliation

**Objective:** Same exercise, against the "Datalabs - Events" tab (~40 events across 15 categories) — PostHog project **66351 (Inc42 Datalabs | Live)**.

**This tab is the most self-documented of the three — read the Remarks column on every row before starting.** The team has already caught several planned-vs-actual naming mismatches inline:
- "Customise Column Clicked" fires in production; the row is meant to be "Customise Column Applied."
- On the company-search table, `Table Sort`'s `Table Name` property comes through as `company` when it should be `company search`.
- `datalabs_onboarding_complete` is 99% populated in PostHog but 66% broken in Customer.io — described as a sync bug, not a missing field.

Your job is to find the mismatches like these that AREN'T already flagged in the Remarks column, plus any event PostHog/CIO has that isn't a row here at all.

**Special attention — money events:** `pro_subscription` and `pro_billing` (rows ~121–132) have unusually precise specs (backend-only, WooCommerce+Razorpay webhook-sourced, explicit "NO ads destinations" rule so a failed renewal never fires a Meta/Google conversion). Verify these two are actually landing in PostHog/CIO with the exact property set specified (`subscription_stage`, `billing_stage`, etc.) and that no ads destination is receiving them — a misconfiguration here has real revenue/compliance consequences, prioritize checking this over lower-stakes UI events.

**Also check:** the sheet has a color-coding legend at the bottom (Live Properties / Backlog / People Search / Captable) that doesn't survive CSV export — open the live Google Sheet (not a CSV) to see which rows are actually marked live vs backlog before you assume a row is shipped.

**Known contradiction to verify, don't rediscover:** every single row lists MoEngage as a live destination — same removed-vendor issue as the Media tab.

**Deliverable:** same table format as Employee 1, plus a short separate note confirming pass/fail on the `pro_subscription`/`pro_billing` ads-exclusion check above.

---

## Employee 4 — Cross-project QA & Consolidation

**Starts once Employees 1–3 have a first-pass table each.** Do not run a fourth parallel PostHog audit — your job is validation and synthesis, not new data collection.

**Tasks:**
1. **Spot-check, don't re-audit.** Pick ~5 findings from each of the three tables and independently confirm them in PostHog/CIO yourself. Flag any you can't reproduce.
2. **Cross-project naming collisions.** Several event names are reused across projects with different meanings — e.g. `Pageview` exists on App, Media, DataLabs, and IP. Confirm each project's PostHog project is only receiving its own traffic (no cross-project leakage) and that a shared name doesn't mask genuinely different semantics that should be documented separately.
3. **Fix the destinations-column contradiction once, everywhere.** MoEngage is removed from the real stack (Customer.io + PostHog, EU; Mixpanel/Amplitude/MoEngage are not real destinations). Media and DataLabs tabs list MoEngage on nearly every row. Produce one corrected destinations column for both tabs rather than leaving each employee to flag it separately.
4. **Merge the three tables into one master "Additional Events Found" report**, deduplicated, with a final recommendation per row (add to sheet / rename / kill / escalate).
5. **Hand this consolidated report to the Intern** (below) as the primary input for the knowledge base, alongside the original 8 sheet tabs.

**Deliverable:** one master table (same columns as above, + a "Project" column) + a short written list of the corrections applied to the Destinations columns.

---

## Intern — Analytics Knowledge Base

**Why this exists:** every audit above exists because event/property definitions live only in people's heads and in a spreadsheet whose own Remarks column is full of "this fires wrong" notes nobody centrally tracks. Concrete proof this causes real problems: DataLabs' `Table Name` property silently sends the wrong value depending on which table you sort; the Media tab has had a duplicate event row sitting unnoticed; three separate scroll-depth implementations exist on the website because nobody could see what was already built. The knowledge base's job is to make sure the next person who wants to instrument something checks ground truth first, instead of guessing or duplicating.

**Objective:** Build a single, continuously-maintained reference that answers, for any proposed feature (a banner, a push notification, a new modal, a new export), three questions before any engineer writes a line of tracking code:
1. Does an event or property that already covers this intent exist?
2. If yes — reuse it (don't create a near-duplicate with a slightly different name).
3. If no — what naming convention, property shape, and destination set should the new one follow?

**Inputs to consolidate (in this order):**
1. All 8 tabs of the Master Sheet (App/Media/DataLabs/IP × Events/Properties).
2. Employee 4's consolidated "Additional Events Found" report — these are real, currently-firing events that belong in the KB even though they're not in the original sheet.
3. `~/ClaudeDocs/inc42/event-auditor/` findings (website implementation-gap data).
4. The vendor stack ground truth: Customer.io (website + app, EU) and PostHog (website + app, EU) are the two real cross-platform tools; Firebase + Singular/SKAN are app-only (US); Meta Pixel + GTM are website-only; MoEngage/Mixpanel/Amplitude are NOT live anywhere regardless of what any sheet says.

**Structure to build — four parts:**

**1. Event Dictionary** — one row per event, across all three projects:

| Canonical name | Project | Category/Group | Fires when (exact trigger) | Properties (name : type : allowed values) | Person/user properties updated (identify call?) | Destinations + WHY each one | Status (live / planned / deprecated / known-broken) | Known gotchas | Last verified |
|---|---|---|---|---|---|---|---|---|---|

Preserve every existing inline warning verbatim rather than summarizing it away — e.g. the `pro_billing` note that a bare Customer.io "performed pro_billing" condition can't distinguish a successful renewal from a failed one is exactly the kind of thing someone will get wrong again if it's not carried forward word for word.

**2. Property Dictionary** — one row per property, deduplicated across projects:

| Property name | Type | Allowed values | Which events carry it | Super/context-dependent/person-level | Naming convention it follows (snake_case app-side vs Title Case website-side — document both, don't force one) |
|---|---|---|---|---|---|

**3. Platform Routing Rules** — not per-event, but as general rules a requester can apply themselves:
- Does this represent money moving (or failing to)? → No ads destination, ever.
- Does it need to identify a person across sessions? → Needs an `identify()`/alias call, document where in the flow.
- Is it app-only content (Firebase/Singular) vs website-only (Meta Pixel/GTM) vs both (PostHog/Customer.io)?

**4. Change-Request Workflow** — a short checklist anyone (PM, engineer, designer) follows before requesting a new event:
1. Search the Event Dictionary for existing coverage by intent, not just by name (e.g. "banner impression" should surface `card_viewed`-style precedents even if no event literally says "banner").
2. If reusing an existing event, add the new context as a property value, don't fork a new event name.
3. If genuinely new, follow the project's existing naming convention, run it past Platform Routing Rules, get sign-off from the project owner (Employee 1/2/3's counterpart), and log it in the dictionary BEFORE requesting implementation — not after.

**Acceptance test before calling this done:** hand the intern (or have them self-test) a fresh request — "we want to track a new homepage banner's clicks and impressions" — and confirm they can answer which existing event/property to extend, which destinations it needs, and why, using only the KB, without asking anyone.

**Maintenance:** this decays fast if it's a one-time doc. Fold a KB-freshness check into the existing recurring-audit checklist / weekly team-leads sync rather than creating a new standalone review cadence. Confirm with Ranjith where this should live — INC42 already has a precedent for team-wide AI-queryable knowledge (the DataLabs VectorDB knowledge repo) and this may belong in the same system rather than a new orphaned doc.
