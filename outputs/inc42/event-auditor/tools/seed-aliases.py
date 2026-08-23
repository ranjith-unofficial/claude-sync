#!/usr/bin/env python3
"""Hand-authored map: spec event (snake_case) -> what actually fires in production.

`posthog`  = the live PostHog event name, or null if nothing reaches PostHog
`gtm`      = name seen on the GTM/GA4/Meta path only (evidence that it fires but never lands in PostHog)
`status`   = implemented | partial | gtm_only | missing | server_side
`note`     = why, traceable to one of the two audits
Sources: Master 'Audit | Jun 2026' (warehouse) + Website sheet 'Live Audit - 12 Aug' (browser).
"""
import json
from pathlib import Path

M = {
 "first_visit":            ("first_visit", None, "partial", "fires but 1-4/30d - leaking from GTM dataLayer, not real instrumentation"),
 "session_started":        ("session_start", None, "partial", "1-4/30d, GTM leak into Live project (Master: Noise)"),
 "consent_updated":        (None, None, "missing", "no cookie banner event observed; DPDP May-2027 exposure"),
 "page_viewed":            ("$pageview", "page_view", "implemented", "624K/30d, the only richly-propertied event; capture_pageview=OFF so hand-coded"),
 "scroll_depth":           (None, "Custom Scroll Depth", "gtm_only", "P1 #5: fires to GTM+Meta only, PostHog gets 0. Also double-fires w/ ScrollDepth-Value-Calculator"),
 "read_time_logged":       (None, None, "missing", "no read-time beacon observed"),
 "summary_viewed":         (None, None, "missing", None),
 "listen_started":         (None, None, "missing", "CONDITIONAL in spec - confirm audio narration exists"),
 "story_shared":           ("Share", None, "implemented", "32/30d, Share Platform enum all 6 values valid"),
 "story_saved":            ("Save Story", None, "partial", "P0: 7 events/30d - near-zero, props fine, firing broken"),
 "story_unsaved":          ("Unsave Story", None, "missing", "absent from PostHog entirely"),
 "recommended_clicked":    ("Recommendation Click", None, "implemented", "5,324/30d, Widget Source/Type/Item Number all present"),
 "tag_clicked":            (None, None, "missing", None),
 "inline_cta_clicked":     (None, None, "missing", None),
 "nav_clicked":            (None, None, "missing", "autocapture=OFF so nav clicks are invisible"),
 "listing_viewed":         (None, None, "partial", "subsumed by $pageview + Page Type; no listing_type/page_number"),
 "listing_load_more":      (None, None, "missing", None),
 "home_module_clicked":    (None, None, "missing", None),
 "search_initiated":       ("Search Active", None, "partial", "1,607/30d but base bundle only - no surface/scope"),
 "search_performed":       ("Search Completed", None, "partial", "8,522/30d; Search Query only. No result_count -> zero-result rate unmeasurable"),
 "search_result_clicked":  ("Search Click", None, "partial", "NAME DRIFT (plan 'Search Result Click'); Result Type='Post' only vs 4 planned values"),
 "entity_followed":        ("Follow", None, "partial", "P0: 4 events/30d - dead. 'START FOLLOWING' is a headline feature"),
 "entity_unfollowed":      ("Unfollow", None, "partial", "P0: 1 event/30d - dead"),
 "feed_viewed":            ("My Inc42", None, "partial", "P0: 1 event/30d; should fire on every My Inc42 view. My Inc42 State='MY FEED' wrong casing"),
 "feed_filtered":          (None, None, "missing", None),
 "list_updated":           (None, None, "missing", None),
 "saved_search_updated":   (None, None, "missing", None),
 "newsletter_prompt_shown":(None, None, "partial", "possibly folded into Modal Viewed w/ Modal Type='Newsletter Landing Page' (undocumented value)"),
 "newsletter_subscribed":  ("Newsletter Subscribed", None, "partial", "1,120/30d; Daily_Newsletter_Status lives on PERSON not event; 'Page Url' casing variant"),
 "newsletter_unsubscribed":(None, None, "missing", None),
 "newsletter_edition_clicked": (None, None, "missing", None),
 "freewall_shown":         ("Freewall Lock", None, "partial", "59,561/30d in warehouse BUT 12-Aug browser walk saw ZERO on lock render. Modal Name coverage 2.6%"),
 "freewall_dismissed":     ("Modal Close", None, "partial", "conflated with the Modal Close/Modal Closed duplicate pair"),
 "freewall_cta_clicked":   (None, None, "missing", "the lock->auth step has no event"),
 "plus_wall_shown":        ("Plus Lock", None, "partial", "4/30d - likely superseded by Freewall Lock (60K); confirm deprecate"),
 "plus_page_viewed":       (None, None, "partial", "$pageview w/ Page Type=plus; no source attribution"),
 "plus_plan_selected":     (None, None, "missing", None),
 "plus_checkout_started":  ("Plus Checkout", None, "implemented", "117/30d; Membership Type/Term ID/Checkout State all valid"),
 "plus_subscribed":        ("Plus Subscribed", None, "partial", "10/30d; key names drift (Plus Next Date / Plus Expiry Date / Plus ConversionID)"),
 "plus_payment_failed":    (None, None, "missing", "only 'Plus Payment Initiated' (14/30d) exists"),
 "plus_membership_cancelled": (None, None, "missing", "P1: Plus Cancellation State absent; churn unmeasurable"),
 "plus_renewed":           (None, None, "missing", None),
 "team_membership_interest": ("Form Submission", None, "partial", "generic form event; 'Model Type' typo on 61% of rows"),
 "report_viewed":          ("Report Interaction", None, "implemented", "1,356/30d; NAME DRIFT from plan 'Report View'"),
 "report_downloaded":      (None, None, "missing", None),
 "academy_session_viewed": (None, None, "missing", None),
 "deal_redeemed":          (None, None, "missing", None),
 "event_registered":       (None, None, "missing", None),
 "sign_in_prompt_shown":   ("Login Modal", None, "partial", "P1 #14: 11,012/30d but PostHog gets {Action,Domain} ONLY while Meta gets all 25 editorial props"),
 "sign_in_started":        (None, None, "partial", "Login Modal 'User Action'=Email/OTP Submit is the closest; no method-choice event"),
 "sign_in_completed":      ("Login", None, "partial", "3,136/30d; P0 #1 distinct_id = EMAIL not Auth0 uid"),
 "register":               (None, None, "missing", "P0: 'Registered' absent from PostHog (only user_signed_up=1). The registration conversion is untracked"),
 "onboarding":             ("Plus Onboarding", None, "partial", "32/30d, Plus-only; no general post-register onboarding"),
 "signed_out":             ("Logout", None, "partial", "P0: 12/30d vs Login 3,136. Missing Logout Status. Also P1 #16: posthog.reset() never called"),
 "account_updated":        (None, None, "missing", None),
 "account_deleted":        (None, None, "missing", "DPDP requirement; sets dnd=true to suppress Customer.io"),
 "web_push_prompt_shown":  (None, None, "missing", None),
 "web_push_granted":       (None, None, "missing", None),
 "web_push_denied":        (None, None, "missing", None),
 "form_submitted":         ("Form Submission", None, "partial", "5,337/30d; 'Model Type' typo 61% vs 'Modal Type' 39%; Meta CAPI PII (em/ph/fn/ln)"),
 "outbound_clicked":       (None, None, "missing", None),
 "error_shown":            (None, None, "missing", None),
 "article_published":      (None, None, "server_side", "server->Customer.io only; not browser-observable"),
}

# Live events with NO spec counterpart - the other half of the diff.
UNSPECD = {
 "Private Mode Modal": "152,639/30d. Modal Name/Id/Type only ~56% coverage",
 "Modal Viewed":       "104,050/30d. Scroll Depth property attached (odd)",
 "Modal Close":        "67,510/30d. DUPLICATE of 'Modal Closed' -> double-count risk",
 "Modal Closed":       "5,025/30d. DUPLICATE of 'Modal Close'",
 "Modal Clicked":      "384/30d. Modal click lifecycle",
 "Pro Payment":        "87/30d. Divergent schema vs Plus (DL Page Type, Slug, Pro Membership Type, Payment Stage)",
 "Plus Payment Initiated": "14/30d, no custom payment props",
 "Search Close":       "503/30d",
 "ResetPassword":      "53/30d",
 "Qr Scan":            "4/30d, carries only 'email'",
 "User Segment":       "1/30d. DEAD - MoEngage segment feed, and MoEngage is REMOVED",
 "test_event":         "GTM/test leak into the LIVE project",
 "gtm.js":             "GTM leak into the LIVE project",
 "dl_event":           "GTM dataLayer leak into the LIVE project",
 "user_signed_up":     "1/30d - the real 'register' signal, wrong name, not wired",
 "payment_completed":  "GTM leak",
 "subscription_created": "GTM leak",
}

out = {
  "_doc": "spec event -> production reality. Hand-maintained. Regenerate target/live JSON freely; this file is the join.",
  "map": {k: {"posthog": v[0], "gtm": v[1], "status": v[2], "note": v[3]} for k, v in M.items()},
  "unspecified_live_events": UNSPECD,
}
p = Path(__file__).resolve().parent.parent / "spec" / "aliases.json"
p.write_text(json.dumps(out, indent=2, ensure_ascii=False))

from collections import Counter
c = Counter(v["status"] for v in out["map"].values())
print(f"aliases.json written: {len(M)} spec events mapped, {len(UNSPECD)} unspecified live events")
for k, n in c.most_common():
    print(f"  {k:12} {n}")
