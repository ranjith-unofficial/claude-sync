---
name: project-inc42-mixpanel-gtm-tag-forensics
description: "29 Aug 2026 — GTM tag-level forensics on the Mixpanel PII leak, plus the higher-priority discovery that GA4 gets the same PII sitewide on every page view (a Google ToS violation, property-suspension risk); decisions on next steps"
metadata: 
  node_type: memory
  type: project
  originSessionId: 73542b43-99df-491b-a583-06fb51da089c
  modified: 2026-08-29T11:53:53.431Z
---

Follow-up to [[project-inc42-mixpanel-legacy-finding]] — Ranjith confirmed directly with Inc42 that Mixpanel
"is not supposed to exist," reframing this from stale-sheet cleanup to a live PII incident. This memory
holds the GTM tag-level forensics done the same day, once the incident moved to two parallel tracks
(technical containment + DPDP/legal escalation).

**No containment access.** Neither of Ranjith's two reachable Google identities (ranjith.m@inc42.com,
datalabs@inc42.com) has any GTM account access — checked directly, both show "click here to create an
account" with zero containers listed. Pausing the tags requires someone else with `GTM-WBHJLKR` publish
rights; this agent could not do it.

**Full 37-tag audit — 7 tags carry PII, not the original 6:**
- Confirmed via `mixpanel.identify(email)` + `people.set()` sending email, phone, first/last/full name,
  employer, designation, seniority: **Login** (tag 296, ~10,500 fires/90d — routine, not rare), Newsletter
  Subscribed (82), Form Submission (140), Plus Onboarding (315), Inc42 Onboarding (427).
- **Plus Subscribed (tag 80) is likely NOT actually leaking**, despite the code being present: its script
  calls `amplitude.track()` *before* it reaches `mixpanel.identify()`, and Amplitude is confirmed dead (see
  below) — the resulting `ReferenceError` crashes the script before the mixpanel PII block ever runs. Not
  empirically fired to confirm — that tag also fires `mida.converted()`, a real ad-conversion pixel with
  possible billing/attribution side effects, so it wasn't triggered without separate sign-off.
- **New 7th leak found: tag 439 ("User Segment")** sends a raw `Email` property directly (no `.identify()`
  call) — but this trigger is fed by the already-removed MoEngage integration and barely fires (~3 hits/90d
  per the PostHog data), so low current exposure despite being a confirmed code path.
- The other 30 mixpanel-referencing tags carry only page/content metadata (URL, title, author, device type;
  a few include IP address) — no name/email/phone confirmed in those.

**Amplitude confirmed dead, not just "unconfirmed."** Fired the real `Login` dataLayer trigger on Ranjith's
own live authenticated session (`dataLayer.push({event:'Login'})`) — `window.amplitude` stays `undefined`
before and after, and the console threw `ReferenceError: amplitude is not defined` from inside `gtm.js`.
This matters for severity in both directions: it's why Plus Subscribed's mixpanel leak likely doesn't fire
(see above), while Login/Newsletter Subscribed/Plus Onboarding/Inc42 Onboarding never reference `amplitude`
at all and are unaffected by the crash.

**Dated exposure window — more precise than the earlier `<script>`-block Wayback date.** archive.org
independently captured the *compiled GTM container itself*
(`googletagmanager.com/gtm.js?id=GTM-WBHJLKR`, 5 snapshots, earliest 31 Jul 2024 — nothing earlier exists
for this specific resource). Diffing them:
- Tags 80/82/140/296/315 already live with full PII by 31 Jul 2024 (a floor, not the true origin — could
  predate this).
- Tag 427 added between Jul 2024–Jan 2025 (tracked under the name "Registered" at first, later repointed to
  fire on "Inc42 Onboarding").
- Tag 439 added between Jan 2025–Sep 2025.
- No further change to the identify-call count since Sep 2025 through today.

**Bonus finding, same session:** the PII fan-out isn't Mixpanel-specific or interaction-specific — a plain
GA4 `page_view` call (not just the previously-flagged "App Banner Viewed") also carries the full
name/email/phone/employer bundle as GA4 user-properties on every page load for a logged-in session. Same
shared-props GTM mechanism, wider blast radius than scoped in [[project-inc42-mixpanel-legacy-finding]].

**GA4 PII is the top-priority fact now, ahead of Mixpanel (Ranjith's call, 29 Aug).** The GA4 `page_view`
leak above isn't scoped to 5-6 specific actions like the Mixpanel one — it fires sitewide, every page view,
for any logged-in user. And it's not just a DPDP/privacy-law exposure: sending PII into GA4 violates
Google's own Terms of Service, which carries a separate real risk of Google suspending the property
outright. Whoever gets looped in on this should hear the GA4 point first, not Mixpanel.

**Two decisions made (Ranjith, 29 Aug), not left open:**
1. **Do not empirically fire Plus Subscribed to confirm the Amplitude-crash inference.** The code-order
   deduction is already ~90% established; firing it for real risks a genuine `mida.converted()` ad-billing
   side effect to settle something already strongly inferred. Leave it as an inference unless someone
   specifically needs empirical certainty for a legal filing.
2. **Containment is blocked on finding a name, not a technical step.** Neither Google identity checked has
   GTM publish rights for `GTM-WBHJLKR`. Next action is organizational: find who at Inc42 has publish
   rights, today, and get both the Mixpanel tags and the GA4 PII issue in front of them together — they're
   almost certainly the same underlying GTM logic (the shared props object), so one container publish likely
   fixes both.

**How to apply:** treat "6 leaking events" (the prior finding) as superseded — it's 5 confirmed-live
(Login, Newsletter Subscribed, Form Submission, Plus Onboarding, Inc42 Onboarding) + 1 low-volume-but-real
(User Segment) + 1 probably-inert (Plus Subscribed, blocked by the Amplitude bug, not verified live — and
per decision 1 above, will stay unverified). Treat the GA4 sitewide leak as the lead item when escalating,
not a footnote to Mixpanel. Whoever scopes the DPDP/legal exposure should use "at least 2 years" (Jul 2024 →
Aug 2026) as the dated floor, not the true origin — Wayback simply has nothing earlier for the GTM resource
itself. Next action is identifying the GTM-WBHJLKR publish-rights owner, not further agent investigation.
Related: [[project-inc42-mixpanel-legacy-finding]], [[reference-inc42-vendor-stack]],
[[project-dpdp-compliance]].
