---
name: project-inc42-deep-linking
description: INC42 app deep links fail from email newsletter — root cause + fix (route via Singular)
metadata: 
  node_type: memory
  type: project
  originSessionId: d8963308-0bb1-4e90-a221-f2c4311ce0ba
---

INC42 app deep links open in-app on a **direct** browser tap of `inc42.com/...` but **fail from the email newsletter** — open in Safari instead of the app on iOS (Safari/in-app webviews) and for some Android users. Surfaced 2026-08-18 via Slack (Ranjith/Utkarsh; Nityam has extra pointers).

**Root cause (hypothesis):** the newsletter wraps links in a **Customer.io click-tracker** that 302-redirects. iOS Universal Links check the app-association against the *first tapped domain* (the tracker), not the final URL — tracker isn't in AASA, so the app never opens. Android App Links need `assetlinks.json` + domain verification on the tapped domain (fails same way; Android 12+ also needs the link verified / "open supported links" on). Worse since iOS 17 for redirect chains.

**Same root cause as the PostHog-review `campaign=None` Singular/Summit attribution bug** — links aren't routed through an app-link-configured domain.

**Fix:** route newsletter links through **Singular smart links** (already in the stack — see [[reference-inc42-vendor-stack]]) → fixes deep linking AND attribution in one move. Verify: AASA at `/.well-known/apple-app-site-association` (Content-Type application/json, no redirect); Android `assetlinks.json` autoVerify; server-side 301/302 only, no JS/interstitial; don't wrap app-destined links in the CIO tracker. The Ken deep-links in all emails this way.

**Tickets pending (Ranjith asked to file, 2026-08-18):** #1 deep linking (owner Nityam + dev), #6 Explore › Companies filters not working (owner Prapti — needs repro detail; may tie to review's Explore `load_failed`). Destination Asana project + create-vs-draft still to be confirmed. See [[project-inc42-launch]].
