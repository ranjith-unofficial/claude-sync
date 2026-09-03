---
name: project-inc42-event-audit-4sep
description: "4 Sep 2026 live PostHog event + event-property audit of App/DataLabs/Media, written to a new 'Event Audit (4 Sep)' tab; found the Table VIew typo, three same-second duplicate epidemics, and corrected 6 stale sheet bug rows"
metadata: 
  node_type: memory
  type: project
  originSessionId: 85e07568-8fea-4d71-99b5-a33466c831d6
  modified: 2026-09-03T19:49:25.083Z
---

Ran a full live event validation of all three PostHog projects on **4 Sep 2026** and wrote it to a NEW
tab **"Event Audit (4 Sep)"** (gid 708067589, 295 rows x 12 cols) in the "One Inc42 - Analytics | Master
Sheet". Nothing existing was edited. It supersedes the "Fixing Event Properties" tab, which Ranjith built
~2 Sep and called cluttered.

**Tab structure** (per project: App, DataLabs, Media): 1. Never fires / dead / renamed · 2. Duplicate /
loop · 3. Fires correctly · 4. Property missing / wrong · 5. Extra (live, not on sheet). Then
6. Unification (cross-project) and 7. Could not validate. Columns: Project · Bucket · Event/property ·
Live name in PostHog · Verdict · 30d volume · People 30d · Last fired · In Customer.io (29 Aug) ·
What the live data shows · What to do · Priority.

**Method that produced the new findings** (reuse it): per project, (a) 90d event census with 30d/7d
splits, (b) `arrayJoin(JSONExtractKeys(properties))` per-event property-key census — this is what surfaces
mis-spelled and undocumented keys that a value query would miss, (c) same-second duplicate detection
(`count() - uniq(toStartOfSecond(timestamp))` grouped by event/person/day), (d) property value
distributions for enum drift.

## The findings that were genuinely new

- **`Table VIew` — capital I typo** on DataLabs Advanced Filter Applied (72% of events) and Advanced
  Filter Clicked (59%). The correctly-spelled `Table View` IS used on Table Pagination (97%) and Table
  Sort (99%). This is the root cause of Ranjith's own "Table View (new) never fills" note. One typo,
  two events, one-line GTM fix.
- **Same-second duplicate firing is an estate-wide epidemic nobody had measured.** Worst offenders:
  Media Private Mode Modal 22.6% (84,284 dupes), Media Recommendation Click 43.3%, Media Newsletter
  Subscribed 23.7%, DataLabs Table Pagination 25.1% (max 1,208/person-day), DataLabs Credit Payment
  52.8%, App menu_item_tapped 41.8%, App card_viewed 18.8%, App search_performed 35.5%.
- **Search fires per keystroke on ALL THREE products** — same defect three times.
- **A live `Scroll Depth` PROPERTY exists on 179,484 Media modal events/30d** while the Scroll Depth
  EVENT is dead. Utkarsh's locked H1 "scroll depth restore" may be satisfiable from data already flowing.
- **`pro_subscription` + `pro_billing` went live 1 Sep (Media) and 3 Sep (DataLabs)** with 100% property
  fill on every documented Lifecycle Envelope / Subscription / Billing field — the cleanest instrumentation
  in the estate and the first genuinely unified event pair. Neither is on the Media sheet. Sheet status
  "renamed event not yet live" is now stale.
- **Property bleed between GTM tags on Media**: `Registered` carries `Charge Amount`="1" on 100% of 1,600
  events; `Logout` carries `Charge Amount` and `Search Query`; DataLabs `Pro Payment` carries Checkbox
  Interaction's own four properties on 5 events. Two tags sharing a payload object.
- **Media `Form Submission` `Model Type` typo is now 94/6**, not the documented 61/39, and its only value
  is the constant "Form".
- **`Modal Clicked` died 19 Aug and `Modal Closed` died 26 Aug** on Media — two modal events stopped
  within a week of each other. Data shows when, not why.

## Six stale sheet rows this audit CORRECTED

1. App `summary_expanded` "sends entity_or_story_id" — **fixed**, now sends story_id/company_id/sector_id.
2. App `search_result_tapped` "story slug instead of id" — **fixed for articles** (74/74 numeric).
3. App `watchlist_entity_added` "entity_name null for sector" — **inverted**: sector is 100% filled,
   COMPANY is blank on 32%.
4. App `deep_link_opened` "no source, medium, content" — **stale**, they ARE sent (unprefixed); the real
   bug is they are null on 90%.
5. App `sign_in_prompt_shown` "not working" — fires since 1 Aug; the documented `method` property is what
   is missing (live sends `source`).
6. Media "Registered is absent from PostHog entirely" — **wrong**, live since 2 Jul 2026, 1,600/30d.
   DataLabs `Click Interaction`, `Pro Lock Interaction`, `List Interaction` are colour-coded "proposed"
   on the sheet but are live at 100% property fill.

## PII status (differs sharply by project)

- **DataLabs: 122,598 events/30d (16.3%), 3,872 people** use a raw email as `distinct_id`. Live today.
- **Media: 150,776 events/30d (7.4%), 7,618 people** same defect. Live today. Plus raw `email` property
  on 1,973 `Login Modal` events.
- **App: clean now.** The `email` event-property leak (2,124 events, 40 event types, 17 people) ran
  29 Jul - 11 Aug 2026 and has had zero occurrences since. Historical rows remain in PostHog and were
  forwarded to Customer.io.
- Media `Form Submission`'s `em`/`ph`/`fn`/`ln` are **hashed**, not raw — not a leak.

## Caveats carried into the tab

Customer.io column is carried from the 29 Aug audit tabs, NOT re-verified 4 Sep, and is lifetime profile
coverage rather than a 30d firing rate. GA4/Meta/Ads/Mixpanel/MoEngage/UserGuiding deliberately unscored
per [[feedback-analytics-destination-scope]].

Related: [[project-inc42-user-properties-audit]] (the user-property half, same week),
[[project-inc42-app-event-validation]], [[project-inc42-datalabs-event-validation]],
[[project-inc42-media-event-validation]], [[project-inc42-tracking-master-review]],
[[reference-inc42-posthog-projects]].
