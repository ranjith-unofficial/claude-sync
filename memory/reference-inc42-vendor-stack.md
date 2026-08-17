---
name: reference-inc42-vendor-stack
description: "Inc42's real vendor/SDK stack — verified against the live site, not assumed"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 1b85df8c-b255-4a10-9994-1dbcc66c6987
---

The **verified** Inc42 vendor stack (checked against live inc42.com HTML on 2026-07-13, not taken from docs). Several team assumptions were wrong, so **verify before asserting**.

| Vendor | Where | Region | Notes |
|---|---|---|---|
| **Customer.io** | **Website AND App** | **EU** (`cdp-eu`, `track-eu`) | CDP + in-app messaging + push + email. NOT app-only, which everyone assumed. |
| **PostHog** | Website + App | **EU** | Reverse-proxied at `posthog.inc42.com` (Cloudflare) — hides the region; `phc_` key = PostHog Cloud. Input masking is **ON by default** (`maskAllInputs: true`), so PII typed into fields is not captured. |
| **MoEngage** | **REMOVED** | — | SDK is commented out, replaced by a no-op stub (`// Moengage removed`). Migrated to Customer.io. Not used for email either. Removed from the policy. |
| **Meta Pixel + GTM** | Website only | — | Two Meta Pixels; retargeting. Website-only — must NOT be extended to the app. |
| **Singular** | **App only** | US | SKAN-aggregated only, no device-level ID sharing. |
| **Firebase** (Analytics, Crashlytics, FCM) | **App only** | US | |
| **Auth0** + Sign in with Apple + **Google Sign-In** | Both | US | Google Sign-In DOES ship in v1 alongside SIWA. |

**Hard-won lesson:** a naive `grep` for a vendor name on a page **counts commented-out dead code as live**. MoEngage showed 30 "hits" while being fully disabled. Always strip `<!-- -->` **and** `//` comments before concluding a script is running. Control-test with a vendor you know is absent (Singular/Firebase returned 0 live hits on the website, which validated the method).

Feeds [[project-inc42-legal-compliance]] (§7.1 providers, §8 cross-border) and the Play Data Safety form / Apple nutrition labels, which must all match real traffic. Related: [[reference-tools-stack]].
