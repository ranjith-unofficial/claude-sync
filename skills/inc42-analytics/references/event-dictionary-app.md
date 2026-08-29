# Event dictionary — App (Inc42 mobile app, PostHog project 146258)

Source: "App - Events" tab (55 events, 11 groups) + "App Audit - 2026-08-29" tab (Customer.io coverage %,
this run had **no PostHog MCP access** so PostHog-side verification below comes from a separate, more
complete live audit instead — see the note under Status) + "App - New Events Found" tab + memory
`project-inc42-app-analytics-audit.md` (29 Aug 2026 live HogQL + Customer.io audit, the authoritative
source for what's actually true in production).

**Read this before trusting any single column:** the sheet's own "App Audit - 2026-08-29" tab has PostHog
columns entirely BLOCKED (no MCP access that run) — its only real contribution is the Customer.io coverage
% per event, included below as "CIO: NN%". The actual PostHog-verified findings come from a second, separate
live audit run the same day (memory `project-inc42-app-analytics-audit.md`), which is cited inline wherever
it confirms, contradicts, or updates the sheet's own Status column.

Legend: **Status** = the sheet's self-admitted bug status, updated with the live audit's 29-Aug verification
where one exists. CIO % = share of Customer.io profiles carrying that event (from the App Audit tab).

## Lifecycle

| Canonical name | Planned name (if different) | Fires when | Properties | Person props updated | Destinations + why | Status | Known gotchas |
|---|---|---|---|---|---|---|---|
| `app_opened` | — | App foregrounded (new session) | source (organic/push/deeplink/banner) : enum; push_type : string (if push) | — | PostHog | ✓ working | **Duplicate risk**: PostHog's own React Native SDK autocapture fires `Application Opened` in parallel via `captureApplicationLifecycleEvents` (see "Events live but not in the sheet" below) — `app_opened` (3,710/90d) and `Application Opened` (3,763/90d) are within 1.4% of each other, near-certainly the same trigger firing twice. |
| `deep_link_opened` | — | Universal/deep link resolved | link_url, destination_screen, campaign utm_source/utm_medium/utm_content | — | PostHog, Singular/SKAN | **Broken**: sheet admits "no source, medium, content" — those UTM/attribution properties aren't actually captured. CIO: 28% | |
| `app_installed` | — | First app open after a fresh install (once per install) | none new (SDK auto-captures platform/os_version/app_version/device_model/manufacturer) | install_date, attribution_source, attribution_campaign | PostHog, Firebase, Customer.io, Singular/SKAN | **Broken**: the install-time call does not send these person properties itself — they're set later via a separate identify call. CIO: 51% | |
| `app_updated` | — | First app open after an app-version update | update_type (forced/voluntary), previous_version + version (auto-captured) | — | PostHog, Firebase, Customer.io | ✓ working. CIO: 2% | |
| `force_update_shown` | — | Min-version gate blocks entry | current_version, min_version | — | PostHog | ✓ working. Not expected in CIO (confirmed N). | |
| `onboarding` | — | Flow state machine, consolidated (mirrors the website's `Plus Onboarding State` convention) | status (started/step_completed/step_skipped), step_name (role/sectors/topic/push_prompt/signin_prompt), step_number, selection_count, step_answer (shape varies by step) | — | PostHog | ✓ working. CIO: 61% | step_name enum order still pending final confirmation. |
| `onboarding_completed` | — | Final onboarding step done | role, sector_groups (7-group array), topic_groups | role, sector_groups, topic_groups | PostHog, Firebase, Customer.io, Singular (SKAN tier 1) | ✓ working. CIO: 49% | Deliberately kept as a STANDALONE event, name-keyed, rather than folded into `onboarding`'s status enum — Meta/Firebase/SKAN need a distinct name-keyed conversion event, not a status value. |
| `walkthrough` | — | User taps Next/skip through the app walkthrough | status (next/skip/…) | walkthrough_status | PostHog, Customer.io | ✓ working. CIO: 41% | |

## Onboarding-adjacent / Brief

| Canonical name | Planned name (if different) | Fires when | Properties | Person props updated | Destinations + why | Status | Known gotchas |
|---|---|---|---|---|---|---|---|
| `brief_page_opened` | — | Brief home page opened | source, edition_type | — | PostHog | **Confirmed still broken 29 Aug 2026**: `source` is still wrong. CIO: 60% | |
| `brief_opened` | — | Cover CTA tapped | edition_date, story_count, source, is_first_brief, edition_type | — | PostHog, Firebase, Customer.io, Singular (SKAN tier 2) | ✓ working per sheet. CIO: 34% | Retention is measured on this event specifically. |
| `card_viewed` | — | A Brief card enters view | edition_date, position, edition_type (+ Story property group) | — | PostHog | ✓ working. CIO: 33% | Highest-volume App event (~80% of total volume). |
| `article_opened` | — | Full article opened from the Brief | story_id, source (+ Story properties) | — | PostHog | ✓ working. CIO: 29% | |
| `decode` | — | Decode (the in-app AI explainer) requested/completed | status (requested/…) (+ Story properties) | — | PostHog | **Confirmed dead, 29 Aug 2026**: zero PostHog telemetry, event absent from the taxonomy entirely. Not just unwired for one property — never fires at all. CIO: not expected (N). | |
| `brief_completed` ★ NORTH STAR | — | Final card of an edition reached | edition_date, cards_viewed, duration_sec | streak_current, streak_max, streak_tier, briefs_completed_total, last_brief_completed_at, last_brief_opened_at | PostHog, Firebase, Customer.io, Singular (SKAN tier 3) | ✓ working per sheet. CIO: 16% | This is the app's north-star event; streak state is derived entirely from this + `last_brief_opened_at`. |
| `brief_fallback_shown` | — | Content-scarcity fallback edition shown | reason (scarcity), edition_type | — | PostHog | ✓ (no admitted bug). Not expected in CIO (N). | |
| `story_saved` | — | Save action on a story | story_id, source | watchlist_count (setPersonProperties) | PostHog, Singular/SKAN | **Broken**: no `setPersonProperties` call fires. CIO: 5% | |
| `story_unsaved` | — | Saved article removed | story_id, source | watchlist_count (setPersonProperties) | PostHog | **Broken**: same missing setPersonProperties issue as `story_saved`. CIO: 1% | |
| `story_shared` | — | Share sheet action completes | story_id, channel | — | PostHog | **Confirmed still broken 29 Aug 2026**: `channel` property is wrong. Sheet's fallback plan (keep bare event only if channel can't be fixed) not yet applied. CIO: 4% | |
| `card_rated` | **live production name is `brief_story_rated`** (confirmed via live PostHog 29 Aug 2026, not just inferred from Customer.io) | User taps 👍/rating on a Brief card | edition_date, rating, edition_type | — | PostHog | **Rename confirmed, not yet reflected in the sheet.** `channel` property bug note in the sheet is actually a copy-paste artifact from the `story_shared` row above it — verify directly before treating "channel is wrong" as this event's real bug. CIO: 2% (as `brief_story_rated`) | Update the sheet's Event name to `brief_story_rated` — this is a confirmed rename, not a candidate. |

## Streak

| Canonical name | Planned name (if different) | Fires when | Properties | Person props updated | Destinations + why | Status | Known gotchas |
|---|---|---|---|---|---|---|---|
| `streak_opened` | — | Streak screen opened | source (profile/brief) | — | PostHog | ✓ working. | |
| `streak_milestone` | `streak_milestone_viewed` in some references | Full-screen milestone modal shown | milestone_day, tier, is_refire | Daily streak state (person property) | PostHog | **Confirmed still broken 29 Aug 2026**: firing on unrelated days, not just at real milestones. CIO: 8% | |

## Watchlist

| Canonical name | Planned name (if different) | Fires when | Properties | Person props updated | Destinations + why | Status | Known gotchas |
|---|---|---|---|---|---|---|---|
| `watchlist_entity_added` | — | Company/sector added to watchlist | entity_type, entity_id, entity_name, watchlist_size_before | watchlist_count, tracked_sector_count | PostHog, Singular (SKAN tier 4 fallback) | **Still broken 29 Aug 2026** (multiple admitted issues, all re-confirmed live): no `setPersonProperties` call fires; `entity_name` is null when tracking a sector but NOT null when removing one (inconsistent); `watchlist_size_after` is wrong. CIO: 5% | Add/remove are deliberately kept as separate events, not one event with a direction property. |
| `watchlist_entity_removed` | — | Company/sector untracked | entity_type, entity_id, watchlist_size_before | watchlist_count, tracked_sector_count | PostHog | Same setPersonProperties gap as `watchlist_entity_added` (not independently re-verified 29 Aug). CIO: 2% | Possible unplanned twins `company_untracked` / `industry_untracked` fire on Customer.io — see "Events live but not in the sheet." |
| `watchlist_viewed` | — | Watchlist tab opened | sub_tab (tracking/saved) | — | PostHog | ✓ working. CIO: 42% | |
| `watchlist_limit_hit` | — | Free-tier watchlist cap reached | entity_type, cap | — | PostHog | ✓ (no admitted bug). Not expected in CIO (N). | Upsell signal — treat as monetization-adjacent when changing. |

## Explore

| Canonical name | Planned name (if different) | Fires when | Properties | Person props updated | Destinations + why | Status | Known gotchas |
|---|---|---|---|---|---|---|---|
| `explore_viewed` | — | Explore tab or sub-tab opened | sub_tab (articles/companies) | — | PostHog | ✓ (no admitted bug). CIO: 50% | |
| `sector_landing_viewed` | — | Industry tag tapped → sector landing page | sector, sub_tab | — | PostHog | ✓ working. CIO: 4% | |
| `search_initiated` | — | Search bar focused | search_scope | — | PostHog | ✓ working. CIO: 7% | Added v1.3. |
| `search_performed` | — | Query submitted | query (raw), search_scope | — | PostHog | ✓ working. CIO: 7% | Raw queries are logged as-is — flagged in the sheet as a product-insight/privacy consideration, not resolved either way. |
| `search_result_tapped` | — | Search result opened | query, position, entity_or_story_id | — | PostHog | **Confirmed still broken 29 Aug 2026**: `entity_or_story_id` contains a story slug instead of a real ID when the tapped result is an article. CIO: 5% | |

## Profiles

| Canonical name | Planned name (if different) | Fires when | Properties | Person props updated | Destinations + why | Status | Known gotchas |
|---|---|---|---|---|---|---|---|
| `company_profile_viewed` | (sheet's Event cell reads truncated as "company_profile") | Company profile opened | company_id, company_type | — | PostHog | ✓ (no admitted bug). CIO: 12% | |
| `profile_opened` | — | User's own Profile tab opened | source (brief/explore/…) | — | PostHog | ✓ working. CIO: 22% | |
| `profile_section_viewed` | — | A profile section scrolled into view | section (funding/…) | — | PostHog | ✓ working. CIO: 11% | |
| `locked_feature_tapped` | — | 🔒 gated feature tapped | feature (alerts/filters/exports/api/reporting), surface | — | PostHog | ✓ (no admitted bug). Not expected in CIO (N). | Upsell signal. |
| `interest_captured` | — | "Notify me when…" tapped | feature, surface | interest_features | PostHog, Customer.io (per sheet — **not actually reaching CIO**) | **Confirmed still broken 29 Aug 2026**: sheet expects Customer.io delivery, but the event is absent from Customer.io entirely — worse than a property mismatch, it's a full destination gap. Also absent from PostHog per the 29-Aug audit's cross-check. Sheet calls this "THE v1 monetization signal" and demands it be "clean from day 1" — it currently is neither instrumented nor reaching either platform reliably. | Needs a product-owner decision, not a routine fix — this is the highest-priority broken event in this dictionary given its stated importance. |

## Notifications

| Canonical name | Planned name (if different) | Fires when | Properties | Person props updated | Destinations + why | Status | Known gotchas |
|---|---|---|---|---|---|---|---|
| `push_permission_prompt_shown` | — | Pre-prompt or OS push prompt shown | context (onboarding/…) | — | PostHog | ✓ (no admitted bug). CIO: 52% | |
| `push_permission_granted` | — | OS grants push permission | context | push_opt_in | PostHog, Firebase, Customer.io, Singular (SKAN tier 4) | **Confirmed still broken 29 Aug 2026**: `setPersonProperties` call fails for non-logged-in users, works for logged-in ones. CIO: 33% | Name-keyed for SKAN/Firebase per sheet notes. |
| `push_permission_denied` | — | OS denies push permission | context | push_opt_in | PostHog, Customer.io | **Confirmed still broken 29 Aug 2026**: same non-logged-in setPersonProperties gap as `push_permission_granted`. CIO: 18% | |
| `push_delivered` | — | Client-side delivery receipt | push_type, message_id | — | PostHog, Customer.io | **Confirmed dead, 29 Aug 2026**: zero PostHog volume ever, absent from Customer.io too — this event does not exist in the taxonomy at all despite being in the plan. CIO: not expected (N, matches). | OEM background-kill caveat noted in sheet (Xiaomi/Oppo/Vivo) — irrelevant while the event doesn't fire at all. |
| `push_opened` | — | Notification tapped | push_type (morning_brief/…) | push_opt_in, push_types_enabled | PostHog, Customer.io | **Confirmed near-dead, 29 Aug 2026**: only 2 lifetime PostHog events, both on 10 Jul 2026, zero since — despite 67% push opt-in. CIO: <1% (matches). | A/B pattern (two-message variant) is defined in the sheet but essentially untestable at this volume. |
| `notification_settings_changed` | — | Any push setting changed | setting, new_value, source (track_company/track_sector/save_article/profile/brief_card) | — | PostHog | **Confirmed still broken 29 Aug 2026**: `setPersonProperties` fails for non-logged-in users, same pattern as the push-permission events. CIO: 1% | |

## Auth

| Canonical name | Planned name (if different) | Fires when | Properties | Person props updated | Destinations + why | Status | Known gotchas |
|---|---|---|---|---|---|---|---|
| `sign_in_prompt_shown` | — | Anonymous user hits an auth wall | method (google/apple) | — | PostHog | **Sheet says "not working" — this is now WRONG per the 29-Aug audit: confirmed firing with real volume since 1 Aug 2026.** Update the sheet's Status column, don't keep citing "not working." CIO: 4% | |
| `sign_in_started` | — | Sign-in sheet displayed | method | — | PostHog | ✓ (no admitted bug). CIO: 51% | SIWA (Sign in with Apple) required on iOS per App Store guidelines. |
| `sign_in_completed` | — | Auth success | method, is_new_user | is_registered, auth_method, dnd=false, email, first_name, last_name | PostHog, Customer.io | ✓ per sheet, **but see the separate, more severe finding**: distinct_id at sign-in reportedly ends up as the email rather than the Auth0 uid in some references (verify current state — this may since have changed given the website's parallel, still-open identify() gap; do not assume fixed without re-checking). CIO: 41% | Anon device UUID aliases to the Inc42 web/Auth0 ID here. |
| `register` | — | First-time registration | method | is_registered, auth_method, registration_date, register_source | PostHog, Customer.io, Singular (SKAN tier 5) | ✓ working. CIO: 19% | Identity-merge point for attribution. |
| `signed_out` | — | Sign out | — | — | PostHog, Singular/SKAN | ✓ per sheet Status, but cross-check the website's parallel finding that `posthog.reset()` is never called on its own sign-out (same class of bug may apply here — not independently confirmed for the App in this audit round). CIO: 5% | |
| `account_deleted` | — | In-app deletion confirmed (Apple mandate) | — | dnd=true | PostHog, Firebase, Customer.io, Singular/SKAN | ✓ working. CIO: 1% | Customer.io profile must be suppressed via `dnd`; DPDP-relevant. |

## Ops / Content

| Canonical name | Planned name (if different) | Fires when | Properties | Person props updated | Destinations + why | Status | Known gotchas |
|---|---|---|---|---|---|---|---|
| `rating_prompt_shown` | — | Streak Day-7 milestone or 3rd completion | trigger | — | PostHog | ✓ (no admitted bug). Not expected in CIO (N). | |
| `error_shown` | — | User-facing error state | error_type (incl. offline), surface | — | PostHog | ✓ working. CIO: 7% | Crashes are Crashlytics, not this event. |
| `preferences_updated` | — | Post-onboarding preference change | field (role/sectors/topics), new_value_count, new_values | role, sector_groups, topic_groups | PostHog, Singular/SKAN | **Confirmed still broken 29 Aug 2026**: `setPersonProperties` fails for non-logged-in users — same class of bug as the notification-settings family above. CIO: 3% | |
| `menu_item_tapped` | — | Profile → About item opened | item (terms/privacy/contact_us/faq/rate_app) | — | PostHog | ✓ working. CIO: 4% | Complements `rating_prompt_shown` via the `rate_app` value. |
| `scroll_depth` | — | Article scroll, once per threshold (25/50/75/100) | depth_percent | — | PostHog | ✓ working (App-side; unrelated to the website's separate, much more broken `scroll_depth`/`Scroll Depth` situation — see event-dictionary-media.md). CIO: 20% | |
| `summary_expanded` | — | Collapsible summary expanded on an article/company card | surface (article_card/company_card), entity_or_story_id | — | PostHog | **Confirmed still broken as of the sheet's own admission**: sends `entity_or_story_id` instead of a proper `story_id`. CIO: 17% | |
| `profile_name_updated` | — | User edits name in Profile → Edit Profile and saves | fields_changed (array), new_first_name, new_last_name | first_name, last_name | PostHog | **Confirmed absent from BOTH PostHog and Customer.io as of 29 Aug 2026** — worse than the sheet's Customer.io-only gap assumption. CIO: N (confirmed). Added v1.3. | |
| `article_published` | — | Editorial team publishes an article (server-side) | story_id, title, url | — | Customer.io only (deliberately backend-triggered) | **Sheet expects Customer.io delivery but the 29-Aug audit found this event NOT reaching Customer.io** ("still broken", needs product-owner decision). | Server-side only — not browser/app-observable by design. |

## Events live but not in the sheet ("App - New Events Found", 29 Aug 2026)

| Canonical name | Matches a planned event? | Classification | Recommendation |
|---|---|---|---|
| `Application Backgrounded` / `Application Foregrounded` / `Application Opened` | No sheet row | **Confirmed: this is PostHog React Native SDK's own built-in `captureApplicationLifecycleEvents` autocapture** (`$lib=posthog-react-native`), the same SDK instance as the manual `app_opened`/`app_installed` calls — not a third-party or forgotten SDK. `app_opened` (3,710/90d) and `Application Opened` (3,763/90d) are within 1.4% of each other. | Needs a product+engineering call on whether to disable this SDK autocapture now that the app has its own manual instrumentation — it is currently double-tracking lifecycle. `Application Foregrounded` exists only in Customer.io with no confirmed PostHog counterpart. |
| `brief_open_today` | No | Dead-test candidate — <1% of profiles | Needs product-owner decision. |
| `brief_story_rated` | **Yes — this is `card_rated`'s live name, confirmed** (see App Audit's Auth/Brief section above) | Renamed, confirmed | Update the sheet: rename `card_rated` → `brief_story_rated`. |
| `company_untracked` / `industry_untracked` | Possibly `watchlist_entity_removed`'s twin | Property mismatch (candidate) — may be name-keyed Firebase/Meta twins, same pattern as `onboarding_completed` | Needs product-owner decision before merging into the dictionary as confirmed. |
| `push_priming_dismissed` | No | Confirmed correct, just undocumented | Update sheet to add a row. |
| `share_initiated` | No — `story_shared` only covers completed shares | Confirmed correct, just undocumented — looks like the funnel-top event before `story_shared` completes | Update sheet to add a row. |

## Open items not resolved by any source read for this dictionary
- Whether `sign_in_completed`'s `distinct_id` is the Auth0 uid or the email (both have been claimed at
  different points in different reviews) was not independently re-verified in the 29-Aug audit — check
  live before asserting either way.
- Final `step_name` enum order for `onboarding` is still pending per the sheet's own open item.
