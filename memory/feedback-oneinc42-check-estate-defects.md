---
name: feedback-oneinc42-check-estate-defects
description: "Standing rule — every OneInc42, login, onboarding, website or DataLabs change must be checked against the Estate Defects doc before work starts"
metadata:
  type: feedback
---

Whenever we pick up **OneInc42 work, login, onboarding, or any website/DataLabs change**, read the Estate Defects doc first and incorporate the relevant EST-## items into the scope — don't design or spec the change without it. Stated by Ranjith 9 Sep 2026.

Doc + full defect list: [[project-inc42-estate-defects]].

**Why:** the 39 defects are what six independent outside reviewers actually hit in their first 48 hours logged-out. They are reproducible and sit in the path of every new user, so any login/onboarding/web/Datalabs change that ignores them will either re-ship the same defect or be measured through a broken input (EST-32 attribution, EST-29 activation counter).

**How to apply:**
- Before scoping: pull the EST-## items that touch the surface in question and list them in the doc/ticket by ID.
- Use the IDs verbatim — EST numbering is stable and shared with the App Review and Product & Data rooms; never renumber.
- Call out prerequisites explicitly: EST-05 (role taxonomies) and EST-06 (auth providers) must be fixed *before* any identity-unification or CDP work, not alongside it.
- Flag items still marked unverified (EST-18, EST-29, EST-32, EST-33) as "reproduce first" rather than treating them as confirmed.
