# Property dictionary — App, Website (Inc42 Media), and DataLabs

One row per property. Naming convention differs by project and is preserved rather than forced into one
style: **App and DataLabs-backend events use snake_case** (`source`, `entity_type`, `subscription_stage`);
**Website and DataLabs-frontend events use Title Case with spaces** (`Modal Type`, `Table Sort Column Name`,
`User State`). Do not rename one to match the other — extend the existing convention for whichever project
you're adding to.

## Properties that appear across more than one project

These are the confirmed same-concept properties found under different names/casing in different projects.
Where value sets differ between projects, both are listed — do not assume they're interchangeable.

| Concept | App | Website (Media) | DataLabs | Notes |
|---|---|---|---|---|
| Share destination | `channel` (enum: link/whatsapp/email/linkedin/twitter/…) | `Share Platform` (Link/Whatsapp/Email/LinkedIn/Twitter/Facebook) | — | Same concept, different casing convention; App's `channel` is separately flagged as broken on `story_shared`/`card_rated`. |
| Person email | `email` (person property, set on `sign_in_completed`) | `Email` (User Data Fields) | `Email` (User Identify) | Media and DataLabs' website/DataLabs-frontend forms are also the mechanism behind the live Mixpanel PII leak — see `platform-routing-rules.md` before touching how email flows into any shared-props object. |
| Person first/last name | `first_name`, `last_name` | `First Name`, `Last Name`, `Full Name` | `First Name`, `Last Name` | App added `first_name`/`last_name` as person properties in v1.3 (`profile_name_updated`). |
| Phone | — (not in App's dictionary) | `Phone Number` | `Phone Number` | |
| Company name (person-level) | — | `Company Name` | `Company Name` | Distinct from the App's `primary_company` / DataLabs' `company_name` (event-level, name of a company being viewed) — don't conflate a user's own employer with an entity being browsed. |
| Company type (entity-level) | `company_type` (enum: Early/Growth/Late-stage/Listed/Corporate/Investor/…) | — | `Company Type` (Late Stage Startup, etc. — Identify group) + a **second, differently-valued** `Company Type` under Filter Property Type (search-filter context) | Three different value sets across two DataLabs contexts alone — verify which one applies before reusing. |
| Device type | `device_model` (string, e.g. "iPhone 14") | `Device Type` (Phone/Tablet/Desktop/Laptop), `Model` | `Device Type` (Mobile/Tablet/Desktop), `Model` | App captures OS/manufacturer separately (`os_version`, `manufacturer`); Media/DataLabs don't. |
| User's registration/logged-in state | `is_registered` (bool) | `User Type` (Visitor/Registered), `User State` (Logged Out/Logged In) | `User State` (Guest/Logged-in), `User Type` (Guest/Pro Trial/Free/Plus Member/Pro Member/Pro Team Member) | **Value sets are NOT equivalent** — Media's `User Type` is a simple visitor/registered flag; DataLabs' `User Type` is a full membership-tier enum. Don't cross-reference the two as if they measured the same thing. |
| Modal identity | — | `Modal Name`, `Modal Type` (Newsletter RFV / Newsletter Lock / Exclusive Lock / Freewall Lock RFV / Freewall Lock Article / … — list confirmed truncated/incomplete in the source sheet) | `Modal Name`, `Modal Type` (Button / Banner / Paywall / Filter / Popup / Free_Tier_Lock) | Independently maintained enums per project — do not assume a value valid in one is valid in the other. |
| Membership/plan type | — | `Plus Membership` (Inc42 Plus - Annual/2 Year/3 Year Membership) | `Pro Membership Type` (two occurrences in the sheet with **different value sets** — DL Pro - Annual/Quarterly/Monthly Membership vs Datalabs Pro - Annual/Quarter) | Naming drift within DataLabs alone (see `event-dictionary-datalabs.md`'s Table Sort / Customize Columns section for the same drift pattern) — always check which specific row's value set applies. |
| Search query text | `query` (raw search text, App) | `query` (planned, Search Completed/Search Click — **currently NOT captured live**, see `event-dictionary-media.md`) | `Search Query` (DataLabs) | Website is the one place this is documented as planned but missing in production. |
| Registration source | `register_source` (App: const `inc42_app`) | — | `Register Source`/`register_source` (DataLabs: Inc42 Datalabs, Inc42 / datalabs, inc42) | Exists specifically so CRM dedupe can tell App vs Web vs DataLabs registrations apart — never hardcode a single value across projects. |
| Onboarding stage/state | `step_name`, `step_number`, `status` (App `onboarding` event) | `Plus Onboarding State` (Onboarding Started/Step 1 Completed/Step 2 Completed/Completed) | `onboarding_stage` / `Datalab Onboarding State` (Onboarding Step 2/3/Complete — **missing a step_1 value**, being added via the `onboarding_lifecycle` rename) | All three projects independently model onboarding progress; none share an enum. |

## App properties (from "App - Event Properties")

### Super (attached implicitly to every App event)
| Property | Type | Allowed values / sample |
|---|---|---|
| platform | enum | ios / android |
| os_version | string | 17.2 · 14 |
| app_version | string | 1.0.3 |
| device_model | string | iPhone 14 · Galaxy S21 |
| manufacturer | string | Apple · Xiaomi · Oppo · Vivo · Samsung (OEM push-delivery tripwire) |
| is_registered | bool | true / false |
| days_since_install | number | computed at fire time |
| streak_day | number | current streak day |
| streak_tier | enum | reader / regular / insider / ecosystem_native |
| watchlist_count | number | count of tracked entities |
| push_opt_in | bool | true / false |

### Story (attached to card_viewed, article_opened, decode, story_saved, story_shared)
| Property | Type | Allowed values / sample |
|---|---|---|
| author_name | string | Hemant Kashyap |
| author_type | enum | staff / contributor |
| primary_industry | enum | App's own 17-sector spine — NOT the website's mixed list |
| primary_company | string | Swiggy — links content to a DataLabs entity |
| company_type | enum | Early / Growth / Late-stage / Listed / Corporate / Investor / … |
| story_type | enum | Exclusive / Investigative / Roundup / Listicle / Series / Newsletter / … (same enum as web) |
| development_type | enum | Funding / Layoffs / IPO / M&A / Policy / Financials / Business Updates / … |
| categories | enum | News / Features / Startup Stories / Resources / In-Depth |
| story_age_days | number | derived at fire time |
| story_slug | string | human-readable slug, added v1.3 for PostHog readability |
| publishing_date | date | article publish datetime — newly added/proposed (orange-flag in source) |

### Person (set via identify(), not per-event)
| Property | Type | Allowed values / sample |
|---|---|---|
| role | enum | founder / investor / operator / … (maps to website's Seniority enum) |
| sector_groups | array | 7-group taxonomy |
| topic_groups | array | 8-group taxonomy |
| watchlist_count | number | digest eligibility, upsell scoring (also listed under Super — sheet lists both, not deduplicated) |
| tracked_sector_count | number | digest eligibility |
| push_opt_in | bool | send eligibility |
| push_types_enabled | array | morning_brief / nudge / breaking / watchlist_digest / winback |
| is_registered | bool | lifecycle stage |
| auth_method | enum | google / apple |
| registration_date | date | cohorting |
| register_source | const | inc42_app |
| streak_current | number | nudge copy, winback segments |
| streak_max | number | habit-ceiling analysis |
| streak_tier | enum | reader / regular / insider / ecosystem_native |
| briefs_completed_total | number | CIO nudge/winback state machine |
| last_brief_completed_at | timestamp | nudge suppression |
| last_brief_opened_at | timestamp | nudge targeting |
| install_date | date | cohorting |
| attribution_source | string | Singular postback |
| attribution_campaign | string | campaign-cohort retention |
| interest_features | array | Plus/Pro waitlist source |
| dnd | bool | true while a deletion request is pending; suppresses ALL Customer.io sends. Set true on `account_deleted`, false on `sign_in_completed`. Newly added (orange-flag). |
| walkthrough_status | enum | completed / skipped. Newly added (orange-flag). |

### Event-level (varies per event — see event-dictionary-app.md for which event uses which)
status · step_name · step_number · selection_count · step_answer · source (context-dependent: external
push/deeplink/banner/organic; in-app brief_card/brief/explore/search/profile/watchlist/onboarding/
sector_landing/card_tag/article_reader/company_page) · position · card_type · is_boosted · boost_reason ·
is_first_brief · cards_viewed · duration_sec · edition_date · story_count · latency_ms · success ·
entity_type · entity_id · entity_name · watchlist_size_before · cap · sub_tab · entity_tab · tracked_count ·
pill_or_slice · applied_filters · sector · query · search_scope · result_count · result_type ·
entity_or_story_id · company_id · company_name · is_tracked · section · feature · surface · channel ·
context · prompt_type · push_type · message_id · campaign · variant · setting · new_value · method ·
is_new_account · milestone_day · tier · is_refire · reason · card_count · trigger · error_type · field ·
new_value_count · new_values · current_version · min_version · link_url · destination_screen · item ·
depth_percent · is_today · update_type · rating · first_name · last_name · fields_changed ·
new_first_name · new_last_name · publishing_date · edition_type

## Website (Inc42 Media) properties (from "Inc42 - Media - Events Properties")

### Content properties
| Property | Sample values |
|---|---|
| Author Name | Hemant Kashyap |
| Author Type | Staff |
| Primary Industry | Ecommerce |
| Primary Company | Swiggy |
| Company Type | Late Stage Startup |
| Shelf Life | 3 Days |
| Post Type | B2C, Internet, B2B-B2C, B2G etc. |
| Categories | News, Features, Startup Stories, Resources, In-Depth |
| Development Type | Cohort Launches, Business Updates, Controversies, Startup Financials, Government & Policies, Industry Trends, Startup IPO, People & Culture, Startup Funding & Investments, Startup Mergers & Acquisitions, Fund Launches, Startup Layoffs |
| Story Type | Others, Exclusive, Follow Up, Investigative, Roundup, Inc42 Announcements, Session Article, Listicle, Series, BrandLabs, Newsletter, Spot News |
| Post ID | 405097 |
| Publishing Date | 2023-07-05 |

### Page/session properties
| Property | Sample values |
|---|---|
| Page Title | Swiggy To Launch Co-Branded Credit Card With HDFC Bank |
| Page Type | home, post, archive, page, glossary, datalabs, inc42-videos, fast42, web-story, startup-essential guide |
| Page URL | https://inc42.com/buzz/... |
| User Type | Visitor, Registered |
| User State | Logged Out, Logged In |
| Device Type | Phone, Tablet, Desktop, Laptop |
| Model | Samsung Galaxy S21, iPhone 12 |
| Domain | Inc42, Inc42 Datalabs |
| Plus Membership | Inc42 Plus - Annual / 2 Year / 3 Year Membership |
| Plus Subscription ID | "123456" |

### Person/identify properties
| Property | Sample values |
|---|---|
| UID | auth0\|DB-Inc42-Media\|17171 |
| User Creation Date | 2022-08-24 11:13 |
| Registration State | registered |
| Register Source | Inc42, Inc42 Datalabs |
| First Name / Last Name / Full Name | Madhur / Garg / Madhur Garg |
| Email | madhur.garg@inc42.com |
| Phone Number | 7774049811 |
| Personal Email / Work Email | no / yes |
| Company Name | Inc42 Media |

### Custom event properties
| Property | Sample values |
|---|---|
| My Inc42 State | My Feed, Saved Stories, Member Library, My Membership, Account & Settings |
| Daily_Newsletter_Status | Yes, No |
| Share Platform | Link, Whatsapp, Email, LinkedIn, Twitter, Facebook |
| Checkout State | Start Checkout, Submit Payment, Checkout Error |
| Recommendation Widget Source | In-Article, Article Sidebar, Homepage Sidebar, Post Article |
| Recommendation Widget Type | Trending, Related, Recommended |
| Recommendation Item Number | 1, 2, 3 |
| Plus Onboarding State | Onboarding Started, Onboarding Step 1 Completed, Onboarding Step 2 Completed, Onboarding Completed |
| Industry | AgriTech, CleanTech, Consumer Internet, Consumer Services, Ecommerce, EdTech, Electric Vehicles, Enterprise Tech, FinTech, HealthTech, IT, Logistics, Retail, Startup Ecosystem, Travel Tech |
| Plus Cancellation State | Cancel Membership Initiated/Confirmed, Disable Auto-Renewal Initiated/Confirmed |
| Modal Name | Newsletter RFV, Newsletter Lock, Exclusive Lock, Freewall Lock RFV, Freewall Lock Article |
| Modal Type | **Incomplete in source** — list runs off the sheet's visible/printable area; treat as an unconfirmed enum until re-checked directly in the sheet. |

### Plus-specific properties
| Property | Sample values |
|---|---|
| Plus Subscription ID / Plus Term ID | "123456" |
| Plus Membership (date) | Wed, Sep 11, 2024 7:41 AM |
| Charge Amount / Charge Currency | 1234.23 / INR |
| Plus Email | user.name@domain.com |
| Plus Conversion ID | "123456" |
| Plus Membership Next Payment Date / End Date | **Flagged yellow/uncertain in the source sheet** — verify before use. |

## DataLabs properties (from "Datalabs - Events Properties", 163 rows)

**Source note**: this section is built from a full CSV export Ranjith supplied directly (163 property rows),
because 130 of 163 rows were hidden on the live Google Sheet by the time this skill's data was pulled — treat
this as complete and reliable, not a partial read.

### Page
Page URL · Page Title · Slug · Domain (Inc42, Inc42 DataLabs) · Sidebar State (Open/Closed) · DL Page Type
(30 values: Home, Ask Datalabs, Pricing, Payment, Edit Company Profile, My Feed, Company/Investor/Industry/
Location/Funding/Acquisition/Report Search, Company/Investor/Person/Industry/Location/Report Profile, My
List, My Search, Company/Investor List, Show All, Company Saved Search, My Inc42, My Alerts, Programmatic
Company List, Company Listicle, Disclaimer, People Search) · DL Page Property Type · DL Page Property Value
· Profile Tab Type (Overview, Financials, Funding, Investment, Acquisition, Latest Stories, Insights,
Companies, Key People, Captable) · Profile Tab Property Type/Value

### User (every event)
User State (Guest/Logged-in) · **User Type (Guest/Pro Trial/Free/Plus Member/Pro Member/Pro Team Member —
NOT the same value set as the website's User Type, see cross-project table above)** · User_Profile_Fixed /
User_Profile_Variable (Founder, Investor, Sales & Marketing, Market Researcher)

### User (Identify)
User ID · Register Source (Inc42 Datalabs, Inc42) · Login Method (Email, Gmail, Linkedin) · Email · First
Name · Last Name · Company Name · Phone Number · Linkedin (profile URL) · Industry · Company Type (Late
Stage Startup, etc.) · Seniority (e.g. Founder) · Company Function (e.g. Product) · Trial Start/End Date ·
Datalabs Onboarding Complete (Yes/No)

### User (meta-only boolean flags)
`industry_alert_subscribed`, and 13 `datalabs_popup_*` flags (one per page: pro, existing_user, feed_page,
company_profile, company_search, investor_search, funding_search, acquistion_search, report_search,
industry_search, location_search, mylist, saved_search) — each tracks whether a user has seen an
information modal on a given page. (Description text is copy-pasted "My Feed" for several of these in the
source — likely a sheet artifact, not necessarily inaccurate about the underlying flag's purpose.)

### Pro
Pro Membership Type (DL Pro - Annual/Quarterly/Monthly Membership) · Pro Subscription ID · Pro Term ID ·
Pro Membership Start/End/Recurring Date · Pro Recurring Payment (bool) · Pro Charge Amount/Currency · Pro
Email · Pro Conversion ID

### Device
Device Type (Mobile/Tablet/Desktop) · Model (e.g. Samsung Galaxy S24, iPhone 14)

### Interaction (the largest group — filters, tables, search, lists, modals, payments, AI agent)
Filter Property Type/Value (the full company/investor/funding/acquisition search-filter taxonomy — dozens of
fields, see the DataLabs event-dictionary's Search Action / Table Action sections for which events use these)
· Customise Column Properties · Advanced Filter State (True/False, and separately Open/Closed — likely a
sheet duplication) · Table Name (Company/Investor/Funding/Acquisition Search, Company List, My List, Company
Saved Search, People Search) · Table Sort Column Name · Lock Type (Short Lock/Long Lock) · Lock Interaction
(Load/Click) · Trial Type/Stage · Table Sort Orderby (ascending/descending — corrected name per the 29-Aug
audit, sheet previously said "Table Sort Order") · Data Type · Table View (Table/Card) · Pagination Page
Number · Section Name (full profile-section taxonomy — Financial/Funding/Investment/Acquisition/Key People/
Captable tabs, Industry/Location Insight tabs) · Tab Name · Form Type · Datalab Onboarding State (Onboarding
Step 2/3/Complete) · Search Type (AI Search, Global Search, List Search, Saved Search, Quick Add, Report
Search, Industry Search, Location Search, Ask Datalabs) · Search Source · Search Content · Search Query ·
Checkbox Type/Selection Source/Status · List Interaction Type/ID/Type/Source · Edit Type/Item ID/Field/
Status/Source · Saved Search Type/Source/ID/Interaction Type · Access Type/URL · Report Name · Set Sidebar
State · Alert Type/Status/Content · Verification Stage/Type · Button Interaction/Type/Content · Post ID ·
Feed Filter Type/Value · Modal Type (Button/Banner/Paywall/Filter/Popup/Free_Tier_Lock) · Modal Name · Payment
Stage (Upgrade_To_Pro_Clicked, Checkout Started, Payment Initiated, Payment Cancelled, Payment Completed,
Payment Completed_Backend) · Pro/Plus Cancellation State · Credit Payment Stage/Topup Plan · Export Stage/
Type · Prompt Type/Prompt · Response Feedback · Interaction Type/Click Type · File Format · Profiles Exported
· Scroll Percentage · Booking Stage

### Lifecycle Envelope (feeds `pro_subscription`/`pro_billing` — every note here is load-bearing, see
event-dictionary-datalabs.md for the full money-events writeup)
product (REQUIRED — the campaign-scoping allow-list: datalabs_pro, datalabs_pro_contacts, credit_topup) ·
product_id (REQUIRED — WooCommerce product id) · subscription_id (REQUIRED) · payment_method (REQUIRED —
upi_autopay/card/other; mandate-revoked copy must say "re-authorise," not "update card") · currency
(REQUIRED, ISO) · plan_interval (REQUIRED — month/quarter/year; lives in the envelope, not Subscription,
because a `pro_billing` receipt can't reach `pro_subscription` attributes mid-journey, a CIO limit verified
2026-08-07; never hardcode a cycle in copy, 18% of live subs are non-monthly) · plan_interval_count
(REQUIRED — exists because of mis-provisioned day/1, day/3, day/365 subs) · next_charge_at (REQUIRED,
nullable — same mid-journey-attribute-reach limitation as plan_interval) · occurred_at (REQUIRED — TRUE
event time, not receipt time; webhooks lag and retry) · source (REQUIRED — woocommerce/razorpay) ·
schema_version (REQUIRED — Segment Protocols pattern)

### Subscription
subscription_stage (trial_started/charge_upcoming/cancel_scheduled/mandate_revoked/
access_ended_voluntary/access_ended_involuntary/reactivated — the business meaning, NOT a raw WooCommerce
status) · trial_end_at · current_period_end_at · next_charge_amount (FROM THE ORDER, never a constant —
31.7% of renewals differ from the ₹1,768.82 default) · renewal_count (distinguishes first charge from
renewal — in WooCommerce the post-trial first charge IS a renewal order) · mandate_status (active/revoked/
paused/none — 100 subs have had this revoked externally with NO status change)

### Billing
billing_stage (purchase_succeeded/first_charge_succeeded/renewal_succeeded/first_charge_failed/
renewal_failed/checkout_abandoned/refunded) · order_id · order_type (parent/renewal) · amount (never a
constant) · renewal_count (present on both pro_subscription and pro_billing so copy can branch without a
join) · failure_reason (gateway message on failure stages, empty otherwise)

**Known gotcha, carried forward verbatim**: a bare Customer.io "performed pro_billing" condition cannot by
itself distinguish `billing_stage=first_charge_succeeded` from `billing_stage=first_charge_failed` — always
branch dunning/win-back logic on `billing_stage`, never on the bare event name.

### Onboarding
onboarding_stage (step_1/step_2/step_3/completed — adds step_1, absent from the current live enum) ·
register_source (datalabs/inc42 — Journey A scoping, must not fire on generic Inc42 registration) ·
entry_page_type (company_profile/report_profile/company_search/investor_search/other — Journey B vs C
assignment; MUST also persist as a user property, not just an event property) · registration_page_url

## Not preserved in this dictionary
The DataLabs property tab's color-legend (green=Live Properties, red=Backlog, orange/pink=Capturable, plus
several unlabeled swatches) marks which specific rows are live vs backlog vs capturable via cell background
color, which no plain-text/CSV extraction can capture. Do not assume a property listed above is live in
production just because it appears here — cross-check against the relevant event-dictionary's Status column,
or ask the DataLabs project owner, before building on an unconfirmed/backlog property.
