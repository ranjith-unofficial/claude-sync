---
name: project-inc42-estate-defects
description: "Estate Defects consolidated external review (Sept 2026) — 39 stable EST-## defects across web, newsletter, reports, Datalabs, app; the authoritative defect list for OneInc42/login/onboarding work"
metadata:
  type: project
---

**Doc:** "Estate Defects — consolidated external review (Sept 2026)" — https://docs.google.com/document/d/1OsiPhcmz5WI1K5kSQJdM-9XOCTP-J2OVLtt_mZr6E0k/edit?tab=t.0 (read 9 Sep 2026; Google Docs canvas blocks text extraction — use the `/mobilebasic` URL variant to read it).

Six independent reviewers walked the full Inc42 estate logged-out, as first-time visitors, over two days each, on their own devices — web, newsletter, report download, Datalabs registration + onboarding, app D1/D2. IDs **EST-01 … EST-39 are stable; never renumber.** Reference them as EST-## in App Review and Product & Data rooms. Folds in the earlier 15-item `estate-defects-2026-09-01.md` from two reviewers.

**The single pattern:** one problem, 39 symptoms — Inc42 asks for identity constantly and uses it almost nowhere. Behaviour-based email capability already exists and is live, but on Datalabs only; app identity feeds it nothing. Highest leverage is extending what works, not new infrastructure.

**Tier 1 (4+ reviewers independently):**
- EST-01 (6/6) identity captured on every surface, carried across none — caps QIA-30, makes the number double-count by an unknown factor
- EST-02 (4/6) newsletter signup returns no confirmation on screen or by email
- EST-03 (5/6) report download is terminal — ungated in one path, unlogged, no route back to Datalabs
- EST-04 (3/6) push permission asked at zero-intent moment while zero notifications have ever been sent

**Tier 2 — identity/onboarding:** EST-05 app vs Datalabs role taxonomies differ (schema-level blocker, fix *before* CDP work); EST-06 auth providers differ by surface (app Google/Apple/OTP; web+Datalabs Google/LinkedIn/email) → up to 4 partial records per person, Apple private relay may break email as join key; EST-07 app re-onboards users with an existing full Datalabs profile; EST-08 MyInc42 says "not following any topics" same session as a completed profile; EST-09 "Continue without account" sits under the sign-in CTA after 3 profiling screens; EST-10 logged-in state lost on Datalabs logo click; **EST-11 employer never captured → no app user can qualify as QIA** — flagged the cheapest fix in the doc: autocomplete against the existing 74,388-company Datalabs DB at sign-in, one field, no new screen.

**Tier 3 — Datalabs:** EST-12 onboarding = 4 pages / ~10–12 fields / 3–5 min, then a Pro wall on the first scroll (fix: one full free company profile first, signup cut to 2–3 fields, rest progressive); EST-13 phone mandatory on free tier; EST-14 Pro payment succeeds with no redirect, no confirmation, stale "Upgrade to Pro" CTA; EST-15 use-case picker "max 3" permits a 4th then greys out Next; EST-16 tab click scrolls to top; EST-17 Ask-Datalabs buried in hamburger, breaks when tab minimised; EST-18 registration 400 Bad Request (the "0% can succeed" generalisation is **refuted** — another reviewer completed free signup + Pro checkout same period; a specific path may still be broken); EST-19 unverified phones polluting the base; EST-20 payment drop-offs with no recovery (confirms the dunning work).

**Tier 4 — app:** EST-21 phone never captured in-app so WhatsApp is structurally unavailable; EST-22 end-of-Brief screen is highest intent and asks for nothing; EST-23 Brief home card reads as long-form, reviewer skipped it entirely; EST-24 no sector filter despite sectors collected at onboarding; EST-25 streak reads 0 from session one, explained only after earned (best retention feature, unprotected outside the app — suggested streak-freeze + day-of-risk nudge); EST-26 sign-in doesn't return to the triggering feature; EST-27 blank state before ~7am; EST-28 watchlist creation absent from onboarding = identity without intent; EST-29 Brief-read counter stayed 0 across two days of real use (if reproducible, every retention number is unreadable); EST-30 ATT prompt on splash while paid marketing is held back; EST-31 guest sign-in prompts stop after day 1.

**Tier 5 — web/lifecycle:** EST-32 top nav carries `?utm_medium=referral&utm_source=menu` — internal clicks attributed as external referrals, gates all attribution inputs; EST-33 mobile app-install popup ~30s load, unclosable, top half unclickable; EST-34 paywall promises personalisation before collecting any signal; EST-35 welcome email lands in Promotions; EST-36 report signup asked twice, view vs download differ; EST-37 "Read Latest" in newsletter module opens news, not a newsletter sample; EST-38 Datalabs sign-in carries to inc42.com but changes nothing in the feed; EST-39 dismissed notifications dead-end.

**Suggested order (cheapest first, from the doc):** EST-32 verify attribution → EST-29 · EST-33 · EST-18 reproduce the three possible functional breaks → EST-11 employer capture → EST-05 · EST-06 reconcile taxonomies and auth → EST-02 · EST-14.

Standing rule for using this: [[feedback-oneinc42-check-estate-defects]]. Related: [[project-inc42-unification]], [[project-inc42-funnel-analysis]], [[project-inc42-datalabs-dunning]], [[project-inc42-icp-role-definition]], [[project-inc42-fy27-plan]].
