# Event dictionary — Website (Inc42 Media, inc42.com, PostHog project 53557)

**Primary source for this file**: the website event-auditor tool (`~/ClaudeDocs/inc42/event-auditor/`), which
drove real Chrome through 6 scripted journeys and decoded every outbound analytics payload on the wire against
a 63-event tracking plan (run `2026-08-23T17-39-56`). This is more authoritative than the sheet's own
"Inc42 - Media - Events" tab and "Media Audit - 2026-08-29" tab wherever they conflict, because it tested live
production traffic directly rather than reading a planning document — and the Media Audit tab's own spot-checks
corroborate it everywhere both were checked (Plus Lock, Modal Viewed, My Inc42, Freewall Lock, the Newsletter
Subscribed duplicate). Sheet data fills in Destinations-column context and fields the auditor's 6 journeys
didn't reach.

**Headline facts, re-verify if this conversation is more than a couple of weeks old**: of 63 planned events,
only 5 fire exactly as specified; 24 fire partially (wrong/thin); 32 never fire at all. GA4 receives 10 distinct
event types across the 6 journeys; PostHog receives 8; Customer.io receives 1 (and that's a page-view type, not
a real conversion event). `autocapture` and `capture_pageview` are both off in PostHog, so nothing fills these
gaps automatically.

**⚠️ Also see `platform-routing-rules.md`'s live PII incident section before touching anything below** — 5+ of
these events (Login, Newsletter Subscribed, Form Submission, Plus Onboarding, Inc42 Onboarding) are confirmed
to leak full PII to an undisclosed live Mixpanel integration via GTM, and `App Banner Viewed`'s GTM path
separately leaks raw email/name/phone into `dataLayer`/`eventProperties`.

## Lifecycle & Session

| Canonical / live name | Planned (spec) name | Fires when | Status | Known gotchas |
|---|---|---|---|---|
| `first_visit` | `first_visit` | GTM dataLayer, new visitor | Partial | Fires but only 1-4/30d — this is leaking from the GTM dataLayer, not real instrumentation. |
| `session_start` | `session_started` | GTM dataLayer, new session | Partial | 1-4/30d — same GTM-leak pattern as `first_visit`; noise in the Live PostHog project. |
| — | `consent_updated` | Cookie-banner interaction | **Missing** | No cookie-banner event observed at all. Direct DPDP (May-2027) exposure — there is no consent record. |

## Page & Reading

| Canonical / live name | Planned (spec) name | Fires when | Status | Known gotchas |
|---|---|---|---|---|
| `$pageview` | `page_viewed` | Page load | **Implemented** | 624K/30d — the only richly-propertied event on the site. `capture_pageview` is OFF, so this is hand-coded, not PostHog's automatic pageview. |
| `Custom Scroll Depth` (GTM tag) | `scroll_depth` | Scroll thresholds | **GTM-only** | Fires to GTM+Meta only — **zero PostHog captures**. Three parallel implementations exist simultaneously: this GTM tag, a separate `ScrollDepth-Value-Calculator` tag (they double-fire against each other), and two differently-named/thresholded GA4 events (`scroll` at 90% only, `Scroll Depth` at 25/50%). Restoring scroll-depth to PostHog is a **locked company strategy item** (Utkarsh's FY27 plan names it as an unconditional H1 fix, feeding the A2 registration-gating holdout) — this is not a routine backlog item. Sheet marks it "(Paused)," which directly contradicts that locked strategy. |
| — | `read_time_logged` | Active read time (unload/30s beacon) | **Missing** | No read-time beacon observed at all. Blocks the "engaged-read time / Plus-content value proof" metric entirely. |
| — | `summary_viewed` | — | **Missing** | Zero hits anywhere in the master sheet — planned, never implemented. |
| — | `listen_started` | Audio narration start | **Missing** | CONDITIONAL in spec — confirm audio narration exists as a feature before treating this as a real gap. |

## Content Engagement

| Canonical / live name | Planned (spec) name | Fires when | Status | Known gotchas |
|---|---|---|---|---|
| `Share` | `story_shared` | Share sheet completes | **Implemented** | 32/30d. `Share Platform` enum has all 6 valid values. |
| `Save Story` | `story_saved` | Save action | **Partial (P0)** | Only 7 events/30d — near-zero. Properties are fine; the firing mechanism itself is broken (this is a duplicate finding to the App's own `story_saved`, but the Website and App events are independent implementations — do not conflate). Also double-fires via GTM (2 identical calls within 2s observed). |
| `Unsave Story` | `story_unsaved` | Saved article removed | **Missing** | Absent from PostHog entirely. |
| `Recommendation Click` | `recommended_clicked` | Recommended-card tap | **Implemented**, but **regressed since June 2026** | 5,324/30d historically (Widget Source/Type/Item Number all present) — but the 23-Aug re-audit's "recirculation" journey drove a recommended-card tap and produced **zero captures on any vendor**. Either a real regression, or this click navigates away and an unflushed batch is masking a working event (check for `sendBeacon` on `pagehide` before assuming a missing handler). |
| — | `tag_clicked` | Inline tag/industry chip tapped | **Missing** | |
| — | `inline_cta_clicked` | — | **Missing** | |

## Discovery & Navigation

| Canonical / live name | Planned (spec) name | Fires when | Status | Known gotchas |
|---|---|---|---|---|
| — | `nav_clicked` | Header/sub-nav/footer link tapped | **Missing** | `autocapture` is OFF, so nav clicks are completely invisible to PostHog with no fallback. |
| (subsumed by `$pageview`) | `listing_viewed` | Listing page loads | **Partial** | Subsumed by `$pageview` + `Page Type` — no `listing_type`/`page_number` dimension exists to slice by. |
| — | `listing_load_more` | — | **Missing** | |
| — | `home_module_clicked` | — | **Missing** | |

## Search

| Canonical / live name | Planned (spec) name | Fires when | Status | Known gotchas |
|---|---|---|---|---|
| `Search Active` | `search_initiated` | Search bar focus | **Partial** | 1,607/30d, but only the base property bundle — missing the `surface` property, which is the exact dimension this event exists to slice by. |
| `Search Completed` | `search_performed` | Query submitted | **Partial** | 8,522/30d, only `Search Query` captured. Missing `query`, `search_scope`, `result_count` — without `result_count`, the zero-result rate is unmeasurable. |
| `Search Click` | `search_result_clicked` (planned name: "Search Result Click") | Result opened | **Partial — name drift + broken** | 531/30d historically, but the 23-Aug re-audit's "search" journey drove a search-result open and got **zero captures on any vendor** — "still not firing," unchanged since June. Where it does fire: `Result Type` = "Post" only, vs 4 planned values. Missing `query`, `position`. **Vendor asymmetry**: PostHog gets 11 properties on this event, ads tools get 33 — same user action, same moment, product analytics gets the thinner payload. This click navigates away, so check `sendBeacon`/`pagehide` before assuming a missing handler rather than an unflushed batch. |

## Follow & Personalization (My Inc42)

| Canonical / live name | Planned (spec) name | Fires when | Status | Known gotchas |
|---|---|---|---|---|
| `Follow` | `entity_followed` ★ north-star | Follow button tapped | **Partial (P0)** | 4 events/30d — near-dead, despite "START FOLLOWING" being a headline feature. |
| `Unfollow` | `entity_unfollowed` | Unfollow tapped | **Partial (P0)** | 1 event/30d — dead. Cascades from Follow being broken (can't unfollow what was never tracked as followed). |
| `My Inc42` | `feed_viewed` | My Inc42 page/tab view or tab click | **Partial (P0)** | 1 event/30d — should fire on every My Inc42 view, functionally dead. `My Inc42 State` value `'MY FEED'` has wrong casing vs the rest of the enum. |
| — | `feed_filtered` | — | **Missing** | |
| — | `list_updated` | — | **Missing** | |
| — | `saved_search_updated` ↑ (commercial intent) | — | **Missing** | |

## Newsletters

| Canonical / live name | Planned (spec) name | Fires when | Status | Known gotchas |
|---|---|---|---|---|
| (possibly folded into `Modal Viewed`) | `newsletter_prompt_shown` | Subscribe prompt shown (inline/footer/exit-popup) | **Not instrumented — P0** | No production event is mapped to this spec event at all. Possibly folded into `Modal Viewed` with an undocumented `Modal Type='Newsletter Landing Page'` value — unconfirmed. Blocks the entire prompt→subscribe funnel denominator. **Confirmed PII risk**: Newsletter Subscribed is one of the 5 GTM tags confirmed leaking full PII to Mixpanel — see platform-routing-rules.md. |
| `Newsletter Subscribed` | `newsletter_subscribed` | Subscribe completes | **Partial** | 1,120/30d. `Daily_Newsletter_Status` lives on the PERSON, not the event. A `Page Url` casing variant exists. **Sheet has an exact accidental duplicate row** ("Newsletter Subscribed" appears twice, identical trigger/properties/destinations) — confirmed, not yet cleaned up as of 29 Aug 2026, safe to delete the duplicate row. |
| — | `newsletter_unsubscribed` | — | **Missing** | |
| — | `newsletter_edition_clicked` | — | **Missing** | |

## Freewall (Register Gate)

| Canonical / live name | Planned (spec) name | Fires when | Status | Known gotchas |
|---|---|---|---|---|
| `Freewall Lock` | `freewall_shown` ↑ | Register gate renders | **Partial** | 59,561/30d in the warehouse, BUT the 12-Aug browser walk saw ZERO on lock render — the 23-Aug re-audit's freewall journey also couldn't trigger it (the register gate itself never rendered in-journey, so this is "not tested," not confirmed broken). `Modal Name` coverage is only 2.6% when it does fire. Sheet's `Modal Name` is currently NOT populating — flagged for a production fix in the Media Audit tab. |
| `Modal Close` | `freewall_dismissed` | Freewall dismissed | **Partial** | Conflated with a separate, near-duplicate `Modal Closed` event (see "Events live but not in the sheet" below) — two differently-named close events exist side by side. |
| — | `freewall_cta_clicked` | Register CTA tapped on the freewall | **Not instrumented — P0** | No event maps to this at all — the lock→auth step has no event, meaning the freewall→registration funnel has no measurable middle step. |

## Inc42 Plus (Monetization)

| Canonical / live name | Planned (spec) name | Fires when | Status | Known gotchas |
|---|---|---|---|---|
| `Plus Lock` | `plus_wall_shown` ↑ | Plus paywall lock shown | **Partial — misrouted, not "near-zero"** | Fires **35-45×/run to GA4, ZERO to PostHog** — a routing bug, not a volume problem. The June 2026 audit read its own low PostHog volume (4/30d) as "near-zero, likely superseded" — that read was wrong; the event fires reliably, just into the wrong tool. Media Audit tab (29 Aug) independently confirms: "Broken-not firing" in PostHog terms, "only 4 hits sitewide in 90 days," recommends a product-owner decision on whether Plus Lock is still meant to exist vs superseded by `Freewall Lock`. |
| `$pageview` w/ Page Type=plus | `plus_page_viewed` ↑ | Plus page loads | Partial | No source attribution beyond the generic pageview. |
| — | `plus_plan_selected` ↑ | — | **Missing** | |
| `Plus Checkout` | `plus_checkout_started` ↑ | Plus subscription initiated | **Implemented** | 117/30d. `Membership Type`/`Term ID`/`Checkout State` all valid. |
| `Plus Subscribed` | `plus_subscribed` ★ north-star | Subscription confirmed | **Partial** | 10/30d. Key names drift across the payload: `Plus Next Date` / `Plus Expiry Date` / `Plus ConversionID` are inconsistently named. **Also one of the 7 tags in the Mixpanel PII-leak forensics — but very likely inert in practice**: its script calls `amplitude.track()` before `mixpanel.identify()`, and Amplitude is confirmed dead, so the resulting `ReferenceError` probably crashes the tag before the PII block runs (not empirically fired to confirm, since it also fires a real ad-conversion pixel with billing side effects — don't trigger it without separate sign-off). |
| `Plus Payment Initiated` | (closest analog to) `plus_payment_failed` | Payment attempt on a Plus purchase | Partial | 14/30d — this is the ONLY payment-outcome-adjacent event that exists; there is no dedicated `plus_payment_failed`, so failure cannot currently be distinguished from other payment states via this event alone. |
| — | `plus_membership_cancelled` | — | **Missing — P1** | `Plus Cancellation State` property is entirely absent — churn is unmeasurable. Sheet does have a "Cancel Plus Membership" row with a `Plus Cancellation State` property planned, so this is a build gap, not a planning gap. |
| — | `plus_renewed` | — | **Missing** | |
| `Form Submission` | `team_membership_interest` ↑ | Generic form submit | Partial | This is a generic form-submission event, not specific to team-membership interest. `Model Type` property has a typo on 61% of rows (should be `Modal Type`). **Confirmed PII leak** — one of the 5 GTM tags confirmed sending full PII to Mixpanel; also carries Meta CAPI PII (em/ph/fn/ln). See platform-routing-rules.md. |

## Plus Value Surfaces

| Canonical / live name | Planned (spec) name | Fires when | Status | Known gotchas |
|---|---|---|---|---|
| `Report Interaction` (live, per event-auditor) | `report_viewed` (planned name: "Report View") | Report viewed | **Implemented** (per event-auditor, 1,356/30d) — **but see contradicting live finding below** | Name drift from the plan ("Report View" planned, "Report Interaction" is what the auditor found live). **Media - New Events Found (29 Aug) separately found `Report Interaction` at ZERO volume in the last 30 days, stopped firing 2026-07-02** — the two checks disagree on current liveness; treat as "was live per the 23-Aug audit, may have died since — re-verify before relying on either number." |
| — | `report_downloaded` | — | **Missing** | |
| — | `academy_session_viewed` | — | **Missing** | |
| — | `deal_redeemed` | — | **Missing** | |
| — | `event_registered` | — | **Missing** | |

## Auth & Account

| Canonical / live name | Planned (spec) name | Fires when | Status | Known gotchas |
|---|---|---|---|---|
| `Login Modal` | `sign_in_prompt_shown` | Auth wall / modal shown | **Partial — P1** | 11,012/30d, but PostHog gets only `{Action, Domain}` while Meta gets all 25 editorial properties for the same moment — a severe vendor asymmetry. |
| (closest: `Login Modal`'s `User Action`=Email/OTP Submit) | `sign_in_started` | Method-choice step | Partial | No dedicated method-choice event exists — this is inferred from a `Login Modal` sub-state, not a real distinct event. |
| `Login` | `sign_in_completed` | Auth success | **Partial — P0** | 3,136/30d. **`distinct_id` is set to the user's EMAIL, not an Auth0 uid** — a real identity-hygiene issue on its own, separate from (and less severe than) the newer "never identified at all" finding below. **Confirmed PII leak** — one of the 5 GTM tags confirmed sending full PII to Mixpanel via `mixpanel.identify(email)`, ~10,500 fires/90d, routine not rare. See platform-routing-rules.md. |
| — | `register` ★ north-star | Registration completes | **Missing — P0** | "Registered" is absent from PostHog entirely — only a `user_signed_up=1` property exists somewhere, not a real event. The registration conversion itself is untracked, despite being a north-star spec event. Note: the sheet's own "Registered" row expects GA4/Mixpanel/etc — worth reconciling whether that fires outside PostHog even though PostHog itself sees nothing. |
| `Plus Onboarding` | `onboarding` | Post-register onboarding flow | **Partial** | 32/30d — Plus-only; there is no general post-registration onboarding event. **A much higher-volume, entirely separate `Inc42 Onboarding` event exists (14,960/30d) with no sheet row and no spec mapping** — see "Events live but not in the sheet" below; likely the real onboarding flow, unconfirmed which is canonical. **Confirmed PII leak** — both `Plus Onboarding` and `Inc42 Onboarding` are among the 5 GTM tags confirmed sending full PII to Mixpanel. |
| `Logout` | `signed_out` | Sign out | **Partial — P0** | 12/30d vs `Login`'s 3,136/30d — badly under-firing relative to logins. Missing a `Logout Status` property. **`posthog.reset()` is never called on logout** — a signed-out browser can keep carrying the previous user's identity into new anonymous activity. |
| — | `account_updated` | — | **Missing** | |
| — | `account_deleted` | — | **Missing** | DPDP requirement — should set `dnd=true` to suppress Customer.io on deletion (mirrors the App's own `account_deleted` behavior, which does this correctly). |

## Web Push & Ops

| Canonical / live name | Planned (spec) name | Fires when | Status | Known gotchas |
|---|---|---|---|---|
| — | `web_push_prompt_shown` / `web_push_granted` / `web_push_denied` | — | **Missing** (all three) | |
| `Form Submission` | `form_submitted` | Generic form submit | Partial | 5,337/30d. `Model Type` typo on 61% of rows vs `Modal Type` on 39% — a data-quality split, not just a naming choice. Meta CAPI leg carries PII (em/ph/fn/ln). |
| — | `outbound_clicked` | — | **Missing** | |
| — | `error_shown` | — | **Missing** | (Note: the App has its own working `error_shown` — do not assume this covers the website too; they are independent.) |

## Content Ops (server-side)

| Canonical / live name | Planned (spec) name | Fires when | Status | Known gotchas |
|---|---|---|---|---|
| — | `article_published` | Editorial publish | Server-side only | Server → Customer.io only; not browser-observable, so the event-auditor's browser-only method cannot confirm it either way. |

## Sheet rows with no clean spec mapping (from "Inc42 - Media - Events")

| Canonical / live name | Fires when (per sheet) | Destinations (per sheet — see vendor correction) | Status | Known gotchas |
|---|---|---|---|---|
| `Modal Viewed` | Any modal render (generic) | GA4, Mixpanel(dead sheet claim — see incident), MoEngage(removed), Amplitude(dead), Meta Ads | **Live, high-volume, undocumented** | 104,050/30d (✅ Healthy in June) — but the 23-Aug re-audit's article-read journey couldn't trigger any modal render, so it's "not tested" this round, not confirmed broken. Media Audit tab flags this as a top-5-volume PostHog event with **zero documented destinations** in the sheet — PostHog + Customer.io need to be added to the Destinations column. |
| `Private Mode Modal` | Not described in sheet row | (blank in sheet) | **Live, high-volume, undocumented — PRIORITY per Media Audit** | 36 PostHog captures in one run alone (3rd-largest event the site sends). Media Audit tab flags this as priority: "update sheet to match reality; this is the 3rd-largest event PostHog receives sitewide and the sheet lists zero PostHog/Customer.io destinations." Also **double-fires via GTM** (up to 4 identical calls within 2s). |
| `Plus Bottom Bar` | Bottom bar triggered | (blank in sheet) | Undetermined — not seen in the event-auditor's 6 journeys | Media Audit: needs product-owner decision on whether this banner still exists on the site at all. |
| `ResetPassword` | Reset password initiated | (blank in sheet) | Undetermined — not seen in the event-auditor's 6 journeys | Media Audit: update sheet to match reality (destinations). |
| `Cart Abandon` | (not described) | Mixpanel(dead-claim), MoEngage(removed), Amplitude(dead), Meta Ads | Undetermined | Media Audit's Actual Name check: live name is `Cart Abandoned`/`Cart Abandoner` on Customer.io — **no PostHog equivalent exists at all**. Confirm intentional before treating the PostHog gap as a bug. |

## Events live but not in the sheet at all ("Media - New Events Found", 29 Aug 2026)

| Canonical name | Volume | Matches a sheet/spec event? | Classification | Recommendation |
|---|---|---|---|---|
| `Modal Close` | ~70,000/30d (214,979/90d) | No — closest is `Modal Viewed`, but this is a distinct event | Confirmed correct | Top-10 volume event with zero sheet row — add one. |
| `Modal Closed` | ~14,000/30d (42,209/90d) | No — distinct from both `Modal Viewed` and `Modal Close` | Confirmed correct | Add a row — three separate "modal ended" events (`Modal Close`, `Modal Closed`, and the freewall's own dismiss) is likely unintentional duplication worth a product-owner look, not just a documentation gap. |
| `Modal Clicked` | ~750/30d (2,243/90d) | No | Confirmed correct | Add a row. |
| `Inc42 Onboarding` | ~5,000/30d (14,960/90d PostHog; 6% of CIO profiles) | No — sheet only has the much lower-volume `Plus Onboarding` (139/30d per Media Audit) | Confirmed correct | **14,960 vs 139 is a 100x+ volume gap** — strong signal `Inc42 Onboarding` is the current production onboarding flow and `Plus Onboarding` is legacy/superseded. Confirm with product owner before documenting either as canonical. One of the 5 confirmed Mixpanel PII-leak tags. |
| `Pro Payment` | ~180/30d (548/90d) | No | Confirmed correct | Properties (`Payment Stage`, `Pro Membership Type`, `DL Page Type`, `Slug`) look DataLabs/Pro-tier related, not a Media/Plus event — needs a product-owner decision on which project actually owns this event before it's documented anywhere. |
| `dl_event` / `gtm.js` / `session_start` / `first_visit` / `gtm.timer` / `user_engagement` | ≤14 hits total, all one URL, one day (4 Jul 2026) | No | Dead-test event | No action — looks like a one-off GTM/GA4 debug leak into the PostHog project, not a real production signal. Confirm it's not still wired. |
| `ai_summit_team`, a DRS-named lead event, generic `Lead`, `Purchase`, `Page View test` (Customer.io only) | <1% of profiles each, except `Purchase` (1%, used in 6 live automations) | No | Mostly confirmed-correct campaign events / one dead-test event | Out of the core content-tracking taxonomy this dictionary covers (AI Summit / D2C & Retail Summit ticketing — see the IP tabs note in open-gaps.md — and generic lead-gen). `Purchase` is used in 6 live Customer.io automations and may warrant a real row if it represents a genuine conversion; needs product-owner confirmation before adding. `Page View test` is confirmed leftover test data, no action. |

## Uncaught page errors that can silently break analytics on this site

Two uncaught JS errors were observed firing repeatedly during normal browsing (34× and 2× respectively across
the 6 journeys): `TypeError: undefined is not iterable (cannot read property Sy...)` and
`TypeError: Cannot read properties of undefined (reading 'map')`. An uncaught error aborts the rest of its call
stack — **any analytics call queued after one of these in the same handler silently never fires.** If a "why
isn't this event firing" investigation comes up empty on the tracking-code side, check for one of these errors
on the page first.
