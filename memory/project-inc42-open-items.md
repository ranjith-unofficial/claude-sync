---
name: project-inc42-open-items
description: Inc42 app — live open items as of 2026-07-14 (verify before assuming these are still open)
metadata: 
  node_type: memory
  type: project
  originSessionId: 1b85df8c-b255-4a10-9994-1dbcc66c6987
  modified: 2026-07-29T09:01:23.777Z
---

Open items for [[project-inc42-launch]] as of **2026-07-14**. These were unfinished when the session ended — **verify current state before acting; they may since be done.**

## Legal docs (see [[project-inc42-legal-compliance]])
- **T&C §18(f) still says "within 30 days"** — must become the 7-day restore model to match the updated Privacy §9.4. **Not yet applied.**
- **The `.md` sources in ~/Downloads are behind Ranjith's own edits** — he updated Privacy §9.4 and §10 in *his* copy, not in `Inc42 Privacy Policy — App Launch (FINAL, clean).md`. The PDF/DOCX exports are therefore stale.
- `[PUBLISH DATE]` placeholder in both docs. **Policies must be LIVE on inc42.com before the iOS submission (~Jul 17–18)** — reviewers fetch the live URL.
- Ethics page address mismatch (web team). Retention periods need counsel sign-off.
- Tell Animesh: MoEngage comes OFF the Play Data Safety form + Apple labels; Customer.io and PostHog are **EU** processors.

## Ranking / brief (see [[project-inc42-content-personalization]])
- **Sector tagging is 86% missing** — the single biggest product problem. Either fix the tagging or pull sector selection out of onboarding.
- Add the 6 unmapped industry values to the sector map.
- No diversity cap → briefs are monotone.

## Card copy — open as of 2026-07-29
- **"✦ Read more (takes 30 seconds)" is contradictory** and must change. "Read more" is open-ended; "30 seconds" promises it ends. It also fights the app's anti-infinite-scroll positioning — "Read more" is the classic endless-feed CTA.
- The block is an **article summary**, ~30 seconds. The fix is to name it a summary: **`30-sec summary`** or **`Summary · 30 sec`** (recommended), with the full article getting its own separate CTA (**`Read full story →`**) so the two labels do different jobs.
- Rejected: anything needing decoding ("Give it a minute", "Worth a minute") — on a card, a parse pause is a cost. Ranjith's bar is **instant comprehension**.
- **Final pick not yet confirmed.**

## Next phase
- **Social intelligence / "Pulse"** — scoped 2026-07-26/28. See [[project-inc42-social-intelligence]].

## QA bug list shared with team — 2026-08-01
20 UI/UX bugs logged post-launch, spanning: Welcome page (calendar view, remove hand illustration), onboarding (move notification-permission prompt to 2nd screen, Continue button should stay enabled with a "choose at least two sectors" validation error instead), typography (remove em dashes app-wide, shrink brief-card title), Streak page (spacing/overlap fix, keep both streak-history nav arrows visible but disable the unavailable direction rather than hiding it), Explore/Article (remove "View Full Article" button, define a summary character limit), Companies in the News (tighten spacing around name/Enterprise tag), Save Article (keep "Saving..." until action completes, don't show "Saved" early), Featured Article (reduce top whitespace), bottom nav/CTA (move action section up), Brief header (drop "Today's Brief" label, keep only branding), Rate Up (dead click — implement or disable), Guest users (must hit login prompt on interaction, currently don't), Company filter bottom sheet (cap height to 50–70% of screen), Sort By (swap "Headcount Change" → "Total Revenue").
- **3 follow-up asks, not yet actioned:** (1) tag inline-article-mention opens with a distinct source/campaign in analytics so they're separable from normal opens; (2) finalize Articles/Companies pill order with Editorial; (3) create a CRM doc listing all identified CRM use cases.
- **Utkarsh's process feedback:** stop relying only on in-app/observational signals — proactively call/email users for direct qualitative feedback.
- Status: full list was just shared with the team; **none of the 20 fixes or 3 follow-ups confirmed done yet.**
