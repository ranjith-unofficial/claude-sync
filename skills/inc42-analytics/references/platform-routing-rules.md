# Platform routing rules

Rules, not a per-event table. Apply these before routing any event/property to a destination — check the
event dictionaries for what's already wired, but these rules govern what SHOULD be wired.

## ⚠️ Live PII incident — read this before trusting any "Mixpanel is dead" statement

As of 29 Aug 2026, a **live, undisclosed, first-party Mixpanel integration** was confirmed on inc42.com,
directly contradicting the "Mixpanel was never in the real stack" assumption that used to be ground truth
here (and that this section will keep repeating below for the *other* dead vendors — Mixpanel is the
exception).

- Two real Mixpanel project tokens (one for `/datalabs/`, one for the rest of the site) are baked into
  inc42.com's server-rendered `<head>`. Not a GTM/ad-network/iframe injection — deliberately configured.
- Live continuously since mid/late 2023 (Wayback), predates everyone currently on the team, nobody owns it.
- **Confirmed actively leaking PII.** 5 of 37 Mixpanel-referencing GTM tags (container `GTM-WBHJLKR`) call
  `mixpanel.identify(email)` + `people.set(...)`, sending email, phone, first/last/full name, employer,
  designation, seniority — on **Login** (~10,500 fires/90d, routine not rare), **Newsletter Subscribed**,
  **Form Submission**, **Plus Onboarding**, **Inc42 Onboarding**. A 6th tag ("User Segment") sends a raw
  `Email` property directly, low-volume (~3 hits/90d, fed by the already-removed MoEngage trigger). A 7th
  ("Plus Subscribed") carries the same PII code path but is very likely inert in practice — its script
  calls `amplitude.track()` first, and Amplitude is confirmed dead, so a `ReferenceError` crashes the tag
  before the Mixpanel block runs (not empirically verified live, since triggering it also fires a real ad
  pixel with billing side effects).
- **Also found in the same pass**: a plain GA4 `page_view` call carries the full name/email/phone/employer
  bundle as GA4 user-properties on every page load for a logged-in session — same shared-props GTM
  mechanism, wider blast radius than the Mixpanel-specific finding.
- **No containment access as of 29 Aug 2026** — neither of Ranjith's reachable Google identities has GTM
  publish rights on `GTM-WBHJLKR`. Two parallel tracks are open: technical containment (pause the tags —
  needs someone else's GTM access) and DPDP/legal escalation (confirmed directly with Ranjith: Mixpanel
  "is not supposed to exist" — this is a live incident, not sheet cleanup).

**How to apply:**
- Do not add Mixpanel as a destination for anything, ever — it should not exist at all; this is an
  incident being contained, not a channel to build on.
- Do not repeat "Mixpanel isn't used" in any deliverable (Play Data Safety copy, DPDP scoping, vendor
  lists) without checking whether this incident is resolved first.
- If a change touches any of the 7 tagged events above (Login, Newsletter Subscribed, Form Submission,
  Plus Onboarding, Inc42 Onboarding, User Segment, Plus Subscribed) or the shared "props object" that
  feeds GA4/Mixpanel/Amplitude together, flag it — the same mechanism is the PII fan-out.
- Treat this as more current than every other vendor claim in this file, including the vendor table below
  (dated 13 Jul 2026) and the sheet's own Destinations columns (which still list Mixpanel as a normal,
  intended destination on nearly every Media and DataLabs row — that column is planning-doc residue, not
  evidence Mixpanel is meant to be there).

## The verified vendor stack (everything except Mixpanel, confirmed 13 Jul 2026)

| Vendor | Where | Region | Notes |
|---|---|---|---|
| **Customer.io** | Website AND App | EU (`cdp-eu`, `track-eu`) | CDP + in-app messaging + push + email. Not app-only. |
| **PostHog** | Website + App | EU | Reverse-proxied at `posthog.inc42.com`. Input masking ON by default (`maskAllInputs: true`) — PII typed into fields is not captured this way (the GTM/dataLayer leak above is a separate mechanism). |
| **MoEngage** | **REMOVED** | — | SDK commented out / stubbed. Migrated to Customer.io. Any sheet row still listing it as live is stale. |
| **Amplitude** | **Dead, confirmed 29 Aug 2026** | — | Directly tested: firing the real `Login` dataLayer trigger throws `ReferenceError: amplitude is not defined` from inside `gtm.js`. Not just "never verified" — actively broken/absent. This is also why the Plus Subscribed → Mixpanel leak above likely never fires (the Amplitude call ahead of it crashes first). |
| **Mixpanel** | **Live, undisclosed, leaking PII — see incident above** | — | Was previously believed dead. It is not. Never add as a destination. |
| **Meta Pixel + GTM** | Website only | — | Two Meta Pixels; retargeting. Must NOT be extended to the app. GTM is also the mechanism carrying the PII leak above — treat any GTM tag touching user data as sensitive by default now, not just Meta ones. |
| **Singular** | App only | US | SKAN-aggregated only, no device-level ID sharing. |
| **Firebase** (Analytics, Crashlytics, FCM) | App only | US | |
| **Auth0** + Sign in with Apple + Google Sign-In | Both | US | |

**App-only tools (Firebase, Singular/SKAN) must never receive website-only events, and website-only tools
(Meta Pixel, GTM) must never receive app-only events.** PostHog and Customer.io are the only two destinations
genuinely live on both surfaces — route cross-platform events there, not through app- or web-specific SDKs.

## Money moving or failing to move → never an ads destination

- **DataLabs `pro_subscription` / `pro_billing`** (backend-only, WooCommerce + Razorpay webhooks) are
  deliberately routed to **Customer.io + PostHog only — no ads destinations.** Rationale, carried forward
  verbatim from the instrumentation spec: "a failed renewal must never fire a Meta/Google conversion."
  - **`pro_subscription` gotcha**: never branch a Customer.io campaign on a bare `Event` condition
    ("performed pro_subscription") — it has no attribute filter, so it's true for ANY stage (trial started,
    cancelled, reactivated, everything). Branch on the `subscription_stage` profile attribute or a segment.
  - **`pro_billing` gotcha**: a bare CIO `Event` condition ("performed pro_billing") is true for both
    `billing_stage=renewal_failed` and `renewal_succeeded` — it cannot tell success from failure. Never use
    it to gate a dunning/grace-period exit; branch on `billing_stage` (or the `pro_subscription_status`
    profile attribute) instead. This is the exact mistake that would make a failed charge look like a
    success to any automation gated on "the event fired."
  - The existing frontend "Pro Payment" event stays as-is for ads/CAPI — it's a separate, deliberately
    un-restricted funnel-top event, not a duplicate of `pro_billing`.
- The website's own PII leak (above) demonstrates the failure mode in the other direction: shared "props
  objects" built for one purpose (editorial personalization) end up feeding payment-adjacent tags (Plus
  Subscribed, Plus Onboarding) without anyone deciding that should happen. When wiring a new payment event,
  build its property payload from scratch — don't inherit an existing shared-props bundle.

## Needs to identify a person across sessions/devices → explicit identify/alias call, and where it happens

- **App**: anonymous device UUID aliases to the Inc42 web / Auth0 ID on `sign_in_completed`. Person
  properties (`is_registered`, `auth_method`, `dnd`, `email`, `first_name`, `last_name`) are set at the
  same call, not on the earlier `sign_in_started`.
- **Website — confirmed broken, most load-bearing gotcha in this file**: a fully signed-in user (WordPress +
  Auth0 cookies present) still gets an **anonymous UUID as their PostHog `distinct_id`** — `identify()`
  never fires on page load for an authenticated session. The same session holds a Customer.io **guest
  token** (`gist.web.usingGuestUserToken` in localStorage) — every browser-side Customer.io event is
  attributed to a guest, not the account. One consequence: the *same* signed-in user can carry 3+ different
  `distinct_id`s across browser contexts with no merge. **Any "per-logged-in-user" website metric is
  unreliable until this is fixed** — treat this as the default caveat on web identity numbers, not a
  one-off footnote.
  - **Fix direction** (not yet shipped): call `posthog.identify()` with the Auth0 uid on every page load for
    an authenticated user, not only at the login moment; call Customer.io's identify() on auth too; keep
    email as a `$set` property, not the distinct_id itself.
  - Also: `posthog.reset()` is never called on sign-out (`signed_out` event: 12/30d vs `Login` 3,136/30d) —
    a signed-out browser can keep the previous user's identity attached to new anonymous activity.
- **DataLabs**: `Registered` / `Login` / `Datalab Onboarding` all trigger an identify call per the sheet.
  `onboarding_lifecycle`'s completion flag is separately confirmed 99.03% correct in PostHog but historically
  broken in Customer.io (a sync issue, not a field-definition issue) — check current sync state before
  relying on the Customer.io side of this flag.

## MoEngage, and (with the Mixpanel exception above) Mixpanel/Amplitude are not valid new-destination targets

- **MoEngage**: confirmed removed from the stack. Any sheet row (App, Media, or DataLabs) still listing it
  as a destination — which is most of them — is stale, not a valid target for new work.
- **Amplitude**: confirmed dead (see incident section). Do not route new events to it.
- **Mixpanel**: live, but as an unauthorized incident under containment — see the section at the top of this
  file. Do not route new events to it under any circumstance; the goal is to remove it, not extend it.
- When a Destinations column in the sheet lists "GA4, Mixpanel, MoEngage, Amplitude, Meta Ads" (the default
  boilerplate on almost every Media and DataLabs row), read that as "planning-doc residue from before the
  vendor stack changed," not as a description of where the event should go. The two tools actually meant to
  receive product-analytics/lifecycle traffic are **PostHog and Customer.io** — treat those as the real
  contract and mirror to GA4/Meta Ads for marketing needs, not the other way round (this is also the
  event-auditor's core website finding: GA4 receives more distinct event types than PostHog does, because
  autocapture is off and nothing fills the gap automatically).

## Known routing/coverage gaps to check before assuming an event reaches the tool you expect

- **Website**: `Plus Lock`, `scroll` / `Scroll Depth` / `Custom Scroll Depth` (three parallel scroll-depth
  implementations, all GA4/Meta-only), and `App Banner Viewed` all reach GA4 but send **zero** events to
  PostHog. `App Banner Viewed`'s GTM path is also separately confirmed to carry raw email/name/phone via
  `dataLayer.0.email` / `eventProperties.email` — a second, independent PII path from the Mixpanel one above,
  same root cause (shared GTM props object).
- **App**: `push_delivered` and `decode` (the AI explainer) have never fired at all — confirmed absent from
  the PostHog taxonomy entirely as of 29 Aug 2026, not just low-volume. `push_opened` has fired exactly twice
  ever (10 Jul 2026) despite 67% push opt-in.
- **DataLabs**: `Demo Call` and `Demo Call Booked` fire to Customer.io but have zero PostHog occurrences —
  the PostHog SDK call may never have been wired for these at all.
