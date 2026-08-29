# Change-request workflow

The checklist to follow before any new analytics event, property, or user property is created, for App,
Website (Inc42 Media), or DataLabs.

1. **Search the relevant `event-dictionary-*.md` by INTENT, not just by name.** A request for "banner
   impression tracking" should surface `card_viewed`-style precedents (the App's card-impression event) even
   though no existing event says "banner." A request for "track a new modal" should surface the website's
   `Modal Viewed` / `Modal Close` / `Modal Closed` / `Modal Clicked` family before anyone writes a new one.

2. **If an existing event covers the intent, extend it with a new property value — do not create a
   near-duplicate event.** The Media sheet already has two accidental near-duplicates ("Newsletter
   Subscribed" appearing twice with identical trigger/properties) — that's the failure mode this step exists
   to prevent. If in doubt whether two candidate events are really the same thing, check
   `event-dictionary-*.md`'s "Known gotchas" column first — several already-documented near-duplicates and
   renames are listed there (e.g. DataLabs' `Pageview` (planned) vs `Page View` (live); the website's
   `Plus Onboarding` vs the much higher-volume, unmapped `Inc42 Onboarding`).

3. **If genuinely new:**
   - Follow that project's naming convention — see `property-dictionary.md`'s naming-convention column
     (snake_case on App/DataLabs-backend events, Title Case with spaces on the website/DataLabs-frontend
     events). Don't mix conventions within one project.
   - Apply `platform-routing-rules.md` — in particular, check the ads-exclusion rule for anything
     money-related, and the live-PII-incident section before wiring anything to a GTM tag or a shared
     "props object" that already touches personal data.
   - Get sign-off from the project owner before requesting implementation. (This skill does not currently
     have a maintained owner-per-project list — ask Ranjith who owns App/Media/DataLabs analytics changes
     if it isn't already clear from context; don't guess a name.)
   - Add the entry to the dictionary **before** requesting implementation, not after — a planned-but-unbuilt
     event should still have a row (mark its Status as "planned"), so the next person doesn't propose the
     same thing again.

4. **Update the relevant dictionary file the same day the event ships.** A knowledge base that lags
   implementation by weeks is the exact failure mode this skill exists to prevent — see the sheet's own
   history of admitted-but-unfixed bugs and destinations columns that were already stale by the time anyone
   read them again.

## A worked precedent: "we want to track clicks and impressions on a new homepage banner"

This is the kind of request step 1 should catch. Walking it through:

- **Which existing event(s) to extend, not duplicate**: the App's `card_viewed` (Brief group) is the
  existing impression-tracking precedent — same "content enters view" semantics as a banner impression, just
  scoped to Brief cards today. On the website, `Modal Viewed` / `Modal Clicked` is the closer precedent if
  the banner is modal-like; if it's a persistent on-page unit rather than a modal, the closest analog is the
  already-live (but currently mis-tracked) `App Banner Viewed` / `App Banner Clicked` pair, which the
  event-auditor found firing to GA4 with **zero PostHog coverage** — this is a case where the "existing
  event" needs a routing fix, not a new one.
- **What property to add, and its naming convention**: extend with a `surface` or `source` value identifying
  the banner (App convention: snake_case values in an existing `source`/`surface` enum, e.g. the App's
  `source` property already carries values like `brief_card`, `explore`, `search`; the website's convention
  is Title Case values in an existing enum-style property like `Modal Name`/`Modal Type`). Do not invent a
  new property name (e.g. `banner_id`) if an existing `surface`/`Modal Name`-style property can carry the
  new value — see step 2.
- **Which destinations, and why**: PostHog (product decisions) and, if the banner is meant to inform paid
  media, GA4/Meta Ads — but per `platform-routing-rules.md`, PostHog must not be skipped even if GA4 is the
  "obvious" first stop; `App Banner Viewed` is the standing cautionary example of an event that reaches ads
  tooling but is invisible to product analytics.
- **Sign-off needed before implementation**: the project owner for whichever surface the banner lives on
  (App vs website), per step 3 above — plus a platform-routing-rules.md check confirming this isn't a
  money-adjacent surface (it isn't, for a homepage banner) before treating the ads destinations as safe by
  default.
