---
name: project-inc42-launch
description: "Inc42 mobile app launch — dates, team, focus, GTM, and core positioning"
metadata:
  node_type: memory
  type: project
  originSessionId: 9528bcb6-d611-479f-9459-97ac0adfb878
  modified: 2026-08-24T17:00:07.911Z
---

Ranjith is driving the **Inc42 mobile app launch** end to end.

**Timeline (revised 2026-07-11, supersedes the earlier "launch Jul 15" plan):**
- iOS TestFlight — in progress
- iOS **production submission ~Jul 17–18, 2026** (manual release)
- iOS **public launch Jul 22, 2026** — this was the *plan*, not what happened
- **Android follows later** (not at iOS launch)

**PLATFORM FLIP (2026-08-11) — supersedes the iOS-first plan above.** Ranjith confirmed: **the v1 public launch is Play Store / Android only.** iOS is not the launch platform. Do not write "now live on iOS", "iOS first", or "Android follows later" in any launch copy. v1.0 release notes were drafted 2026-08-11 for the Play Store 500-char "What's New" field.

**2026-08-11 (impromptu Meet — Ranjith + Ritvik + Satya + Ashish, 49 min): Android went live, iOS rejected again.**
- **Decision: launch on Play Store now, stop waiting on Apple.** Trigger was yet another iOS rejection that morning. Ranjith uploaded the latest Android APK (note: build **B37 was the iOS binary**; the Android binary was shared alongside it) and coordinated with **Nithyam** for a ~30-60 min window to deploy banners (website + app). Ranjith to post verification in the team group **tagging Utkarsh** so alignment is documented in writing.
- **Comms deliberately held back:** no marketing communication on 11 or 12 Aug — **WhatsApp + email go out Thursday 13 Aug**, purely to avoid colliding with CTO Summit emails already scheduled. No other logic behind the date.
- Ranjith is **not confident in the install numbers** from the marketing plan's aggression level, but Utkarsh is fine with it, so he's not intervening.
- **iOS rejection root cause (this round) = ATT prompt placement, not font size.** The earlier font-size rejection was diagnosed and fixed by Ritvik; Apple then raised a new, unrelated issue (also tested it on iPad despite Inc42 explicitly stating no iPad optimisation). Fix: the **App Tracking Transparency pop-up must fire on the first screen after the splash, before any tracking**. Tracking here means **MMP/Singular only** — PostHog and Customer.io are product analytics, not user tracking, in Apple's view, and are not in scope. **Removing Singular does not remove the requirement** — the prompt is mandated by the "yes" already declared in the privacy form, and Apple checks the form answer, not the SDK. Ritvik to implement + resubmit.
- **Apple escalation path:** Ranjith's contact (a principal engineer at Apple) is unavailable and can't intervene anyway — recommending/fast-tracking an app internally violates Apple policy. His advice was to book the official **App Review appointment; next available slot is 21 Aug 2026** — Ranjith is booking it regardless, to get the full hygiene list in one pass instead of serial rejections. He'll also try LinkedIn outreach to someone more senior, low expectations.
- **Hygiene list:** Ranjith maintains a sheet with 3 tabs — dev / store / blockers. Ritvik to focus on **blockers**, ignore anything Google-Play-specific. AI-generated audits proved too subjective (they anchor on whatever the first search returns, and "if they approved it before, they'll approve it again" reasoning); Ranjith's suggested method is to use Claude to generate *possible rejection reasons* from the guidelines, then have Cursor answer each one — with manual review on top. IDFA-on-first-launch flagged as the known live issue.
- **Bugs (non-blocking for launch):** Android push notifications show the Inc42 logo on some devices and not others — Ritvik investigating, suspects device-level, may not be fixable app-side. Some events (streak, FAQ, industry page) were fixed; 4 further bugs on Animesh's list are open. A revised APK ships when ready.

## 🔴 2026-08-14 — THE LAUNCH IS FAILING ON ACQUISITION. Ranjith now owns the backup plan.

**Actual numbers, from two calls the same day:**
- Total installs: **~15** per Ranjith (10 from the base campaign, 5–6 from the website); **7–8** per Animesh. **The two figures conflict — get one authoritative number.**
- WhatsApp link: **15 clicks → 2 installs**
- EDM went out → **10–12 joined the WhatsApp community**; Animesh expects **30–32 maximum**
- Banners exposed to **~7,000 logged-in users**, segmented as those who opened ≥1 email in the last 30 days (deliberately "warm", not dormant)
- Email **open rate ~1%** — 7,000 sends ≈ 70 opens, and a fraction of those click. Ranjith's point to the team: *mathematically this was never going to work*
- Website traffic available but unused: **~15,000 visitors/day**

**Decisions taken with Animesh / Nityam / Amit:**
- **Website banners now go DIRECT to the Play Store**, not WhatsApp-first. The old flow was 3–4 steps (banner → WhatsApp community → Play Store); higher friction on a bigger audience beats low friction on 7,000.
- Banners open beyond logged-in users to the full ~15k/day base.
- **Feedback collection moves in-app** — pop-up and/or push notification — instead of depending on the WhatsApp community. Post-signup, email users to join WhatsApp.
- **Objective re-ordered: installs are primary, feedback is secondary.** That's a reversal — the WhatsApp community existed to gather beta feedback.
- **Paid acquisition is ruled out** — no Meta/Google spend.
- Daily **brief push notification is confirmed running**, agreed to send regardless of the tiny user count.
- Animesh's steer for Ranjith's research: **don't benchmark ET / HT / TOI — look at international media brands at a similar scale.** His framing of the problem: it's media/information, so there's no technical USP to sell.
- Cadence: sync **twice a day**; backup plan to be shipped **by the next day**.

**Ranjith's position (stated to Ritvik and Ashish):** he flagged before launch that a logged-in-only banner reaching ~2,000 people over a month could not produce the 100–200 beta installs marketing projected. Marketing held the conviction it would work and had taken it to Utkarsh, so he didn't override it. Now, post-launch, the acquisition problem has landed back on him and **he is deprioritising everything else to build the backup plan.** His own read: the failure is a planning gap, not an execution gap — there was time to plan for this and it wasn't used.

**Marketing call attendees:** Animesh, Nityam and Amit. Animesh had already raised the backup-plan concern with Utkarsh before this call.

**Additional points from that call:**
- **Animesh's incentive idea:** inside the app, offer exclusives over the next few days in exchange for feedback, then surface the WhatsApp community join to whoever responds. His framing: *"App aa gaya shop ke andar — aap kuch bhi bech sakte ho"* — once someone is inside the app, everything else becomes reachable.
- **Push notification is the lever, not email.** Push can drive feedback and community joins; email open rate makes email nearly useless for acquisition.
- **A dead end Ranjith raised and Animesh closed:** shipping a feedback form into the Play Store beta build isn't blocked by approval — it's blocked because users would have to **update** the app, and there are almost no users to update. Approval speed was never the constraint.
- **Animesh's core problem statement:** *"If this app were a product, I know the ways. But this is media and information — there's no technical USP to sell."* That's the framing Ranjith's research has to answer.
- **Brief image work: deliberately deprioritised by Ranjith** — "not my primary concern right now."

**Ideas on the table (not yet locked):** Product Hunt, LinkedIn newsletter, every owned channel, in-app feedback loops, "download the app / read more in the app" prompts on mobile web articles, and a device-detecting URL shortener for the store redirect — Ranjith notes that last one is **not a tech task**, any URL shortener does it.

**2026-08-12 (Utkarsh call) — post-launch distribution, brief and notification decisions.**
- **Banner targeting was wrong and is being fixed.** The app-download banner was shown **only to logged-in website users** — ~2,000 logins/month ≈ **66/day**, so over 10 days ~660 people would see it and downloads wouldn't cross 50. **Decision: open the banners to all visitors, not just logged-in users.** Ranjith flagged to Nithyam that the marketing plan needs revision. User-base comms go out 13 Aug as planned.
- **Brief image:** pulled automatically from the featured article; when there's no featured article it falls back to **one static default image shared across all sectors**. **Action: build sector-based default image variants** and pick by the brief's dominant sector. Ranjith to find bandwidth with **Anmol**.
- **Brief title:** already auto-generated per sector — done.
- **Sector-based notifications: built but NOT switched on.** Nithyam wants to test **static notifications with static content** first. Ranjith disagrees with static on principle but agreed to a **2–3 day experiment** (small user base) to see click-through. If it doesn't perform, switch to generated notification copy pushed to Customer.io. Base work is done either way.
- 🔴 **The daily brief push did not reach Utkarsh on 12 Aug.** It's meant to be scheduled automatically at ~8 AM (Animesh set it up). **Utkarsh's instruction: the daily brief notification cadence starts now and cannot be missed — send it manually if the automation isn't firing.**
- **New cadence agreed: 1–2 manual push notifications per day for big/breaking stories**, sent **universally** (not sector-targeted). Ranjith to sync with **Ashish** on execution.

**NEW: `article published` event → Customer.io (built by Ranjith, first disclosed to Utkarsh 2026-08-12).**
- Flow: article publishes in the **CMS → backend DB → Redis tag → event to Customer.io**, named `article published`, carrying **sector, company, development tag, topic, author, published time** and similar properties already on the page-view event.
- **Problem it solves:** the marketing team previously had no way to know an article had been published, or what type it was — segmenting was effectively impossible. **Amit has already tested the event**; CIO can build segments off it directly.
- **Intended use:** on `article published` → read the article's sector → push to the matching follower segment (e.g. fintech).
- **Utkarsh's challenge:** a user following 2–3 sectors could get 5–6 pushes a day. Currently capped at **1 notification**; the intended end state is **collating matches into a single notification**.
- **Weighting is required before automating** — a story must be judged important enough to push (e.g. app-featured = higher priority), scored in the backend and passed to CIO.
- **DECISION: park the scored/automated push logic.** Define the logic and setup later, once there are real users (~a week out). Short-term focus is the default images, the guaranteed daily brief, and the 1–2 manual pushes.

**Correction (2026-08-05) — load-bearing, don't re-cite Jul 22 as done.** As of 5 Aug 2026, the app has **not** publicly launched — it's still awaiting app store approval, expected "this week" per Ranjith. The Jul 22 date was a plan recorded before it happened; it slipped. A leadership memo had stated it as a past/confirmed fact (public launch date, post-launch iteration) and had to be corrected — the app's current PostHog activity is internal/test usage, not a live public cohort, and no retention conclusion can be drawn from it yet. See [[feedback-ask-before-assuming]] — this is the exact failure mode that memory already warns about, recurring with the same date.

**How to apply:** don't state "Jul 22 2026, confirmed" or "post-launch" as current fact from memory alone — ask or flag as "per the Jul-11 plan, unconfirmed" until Ranjith confirms the actual launch happened. Re-check this memory's date before citing app-launch status in anything new.

**RESOLVED 2026-08-15 — iOS IS LIVE. Verified directly in App Store Connect (app ID 6789025146), not reported.** Version **1.0 = "Ready for Distribution"**, carrying **build 40** (marketing version 1.0.0). The earlier "v40 submitted, approval unverified" question is closed — it was approved and shipped. Supersedes any note saying iOS is rejected/pending.

**App Store Connect state as of 2026-08-15:**
- **1.0 (live)** is **locked**. Screenshots, description, keywords and the localization selector are all read-only. Only fields carrying an inline "Edit" link are changeable: **Promotional Text, Copyright, App Review Information**. Promotional Text is the only user-visible field editable without review.
- **1.0.1 exists as a "Prepare for Submission" draft** with **no build attached** — so it cannot be submitted until someone uploads build ≥41.
- 🔴 **The live listing carries only ONE iPhone screenshot.** The 1.0.1 draft already has **four** staged and waiting. Apple surfaces the first 3 in search results, so the live page is under-using the highest-leverage conversion slot while the fix sits unshipped behind a missing build. Directly relevant to the acquisition problem above.

**How to apply:** to change anything user-visible on the iOS listing except Promotional Text, the route is ship 1.0.1 — there is no metadata-only edit path on 1.0 while a draft version exists. The blocker is a build, not Apple.

**✅ SUPERSEDED 2026-08-20 — iOS 1.0.1 IS LIVE.** PostHog `app_opened` by version shows 1.0.1 appearing 17 Aug (3 users), then 16 on 18 Aug and 27 on 19 Aug. The build shipped and is rolling out. Close any item reading "blocked on build ≥41" or "awaiting Apple review of the screenshots", and verify the four staged screenshots are now on the live listing.

**🔴 The install-count question is answered: 189 real users since 12 Aug** (persons first seen on/after 12 Aug, @inc42.com excluded), of whom 180 fired `app_installed` — the event under-fires ~5%, so PostHog will always read low against Play Console. This supersedes the 15 / 37–38 / 50 / 7–8 figures that were circulating. Full behavioural picture in [[project-inc42-app-behaviour]].

**2026-08-17 — acquisition reframed from "backup plan" to a two-phase growth plan.** iOS is live and there is a working base, so the rescue framing is retired. Full detail (5 beta levers, public launch 25–26 Aug, gates, open gaps) lives in **[[project-inc42-app-acquisition]]**.

**2026-08-14 Product & Data call (Ranjith + Utkarsh + Prapti + Ashish, 35 min) — Ranjith's commitments:**
- Draft a **1–2 month unification + agent-platform roadmap** from Utkarsh's strategy plan, the unification plan and the agent-platform architecture doc; brainstorm internally with Prapti + Ashish first; keep open/debatable points listed separately. Review with Utkarsh **Monday 17 Aug**.
- **Unblock the Ask Inc42 card design** — Satya is blocked on CTO Summit. Utkarsh's explicit instruction: **plan Satya's bandwidth jointly with the design team**, merging their queue with Inc42 product priorities, rather than assigning unilaterally.
- Share the **daily/weekly cadence checklist** (notifications, weekly brief, app knowledge updates) with Utkarsh, and hand it to **Ashish to chunk into the vector DB**.
- **Master context doc:** Utkarsh has one, last updated **April 2026**. Ranjith to merge it with his own knowledge doc, add DataLabs context, and share back. Agreed process: **manual updates by Ranjith + Ashish for 1–2 weeks**, log how often things change, then automate.
- **LLMs.txt / AEO** — Utkarsh raised it independently; already in Ranjith's AEO section, to be folded into the unification roadmap. Revisit properly **after the D2C Summit**, alongside the new Inc42 messaging.
- Chase **Yash's consolidated hiring-agent feedback** (promised 14 Aug) — blocks rollout beyond the Founder's Office Associate role; increased budget range already communicated.
- **Azure:** Varun has the credit context, Microsoft POC response expected within the week.

Primary success metric is **Day 1 / Week 1 installs**.

**Core positioning:** anti-infinite-scroll — "no endless scroll / actually finish."

**Team (learned 2026-07):**
- **Ranjith** — product, onboarding, personalization, legal amendments, PRDs, analytics
- **Utkarsh** — owns the canonical v1 PRD, launch infra, and the legal/store compliance review. Effectively the technical/compliance authority; his locked decisions supersede earlier drafts.
- **Animesh** — store submission (App Store Connect, Play Console, nutrition labels, Data Safety form)
- **Nityam** — design / Figma

**Scope Ranjith owns:** onboarding flow, industry/sector selection, news personalization, company tracking, funnel estimation, product metrics, PRDs, analytics, and the T&C + Privacy Policy app amendments.

**GTM:** grounded in *verified* Inc42 channel metrics (not assumptions). Cold-reader-first copy across LinkedIn, Instagram, X, email.

**2026-08-24 Weekly App Review (Ranjith + Utkarsh + Animesh + Nityam) — v2 scope closed, September targets locked.**
- **v2 scope closed today; designs due Wednesday (26 Aug); release by 31 Aug.** Items: explore renamed to "news" (kept in tab order, no center-tab pattern; brief stays a feature, not the hero), homepage banner inventory replacing the calendar/greeting space to educate on brief, brief card redesign, Data Labs filters, app-update banner fix, dark mode within 15–30 days. This is a separate, distinct scope from the flags/feedback/ratings 10-item list in [[project-inc42-app-v2-release]] (still PROPOSED) — don't merge the two lists.
- **Notifications: move to 1–2/day 1:1 news-based push** on breaking/important stories (editor flags via Slack), sector-segmented over blanket blasts — supersedes the "universal, not sector-targeted" cadence agreed 12 Aug above. CIO LLM actions + batch processing for personalized brief titles floated as a later step.
- **September target: 5,000 installs, ~20% activation (~2,000)** via amplified basic campaigns — no brand campaign yet. Brand/full launch pushed to **mid-October** (post-Dussehra), tied to the D2C Retreat and Griffin shoots. Install CPI benchmark ~₹100–150.
- **Activation redefined: brief completed + minimum 60 seconds, measured on median (not average).** Use this definition going forward, not raw completion.
- Ranjith's opens: share v2 scope list, finalize designs by Wed, add a forced/prominent app-update prompt in v2, fix Singular deep-linking with a permanent in-app integration ([[project-inc42-deep-linking]]), set up a shorter brief-first-vs-explore-first A/B via PostHog for second-half September.
- Utkarsh's opens: send the app download link/ready-message for team sharing, plan the October brand launch, propose budget options to hit the 5,000 install target.

Related: [[project-inc42-legal-compliance]], [[project-inc42-content-personalization]], [[reference-inc42-vendor-stack]].
