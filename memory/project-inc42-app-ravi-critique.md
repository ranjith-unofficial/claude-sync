---
name: project-inc42-app-ravi-critique
description: Ravi Kumar's outside-in product critique of the INC42 app (21 Aug 2026) — Brief IA is the core problem, plus the iOS silent-push bug fix
metadata:
  type: project
---

**Ravi Kumar** — senior product mentor Ranjith calls "sir", outside INC42, gives unfiltered
first-time-user critique. Call on **21 Aug 2026, 11:48 PM – 12:53 AM IST**
(Wispr Flow logs it under the misleading title "Wispr Flow Notification Improvements",
meeting id `8746bb3f-0a33-4693-83d6-191f54f9738f`; searching "Ravi" does NOT find it —
his name appears only in the transcript, not the summary).

## His verdict (the part that matters)
Everything else is cosmetic — **define the primary use case and audience segments first**.
The trap he named: if you treat the wrong thing as the core use case, incremental changes on
top of it will ALSO produce bad data, because the core is right for you and wrong for the user.
In the beginning, don't hesitate to scrap and rebuild; run wild experiments, not tweaks.
Ship what's designed meanwhile and collect data.

## Brief
- He could not answer "what is Brief?" even after using it — matches [[project-inc42-app-behaviour]]
  (all loss at card 1) and the 20 Aug Brief Card UX session. Three independent sources, same finding.
- Brief and Explore overlap → merge the feed; **Brief becomes top headlines inside it**.
- **Horizontal scroll kills it** — Jacob's Law, go vertical Inshorts-style.
- Never re-serve read stories; open at story 6. Fatigue → once/day → zero.
- Weekly recap / weekend brief = bells and whistles, must not hold homepage prominence.
- Recency should be a *weight* in personalization, not a hard filter — let users resume.
- Nowhere does the app say the brief is personalized → the value never lands.
- He questioned personalization itself: order needs personalizing, story *selection* maybe not,
  given daily publish volume. (Relevant to [[project-inc42-content-personalization]].)

## Concrete UI fixes
- Streak: show the 1-day streak FIRST, then "sign in to save it" — currently asks before any gratification.
- Article progress bar runs to end of page; should run to end of article.
- Explore's auto-popping filter is not user-initiated — his instinct was to hit ✕.
- Companies tab must **lead with search**, not a discovery scroll.
- Changing a filter tab should reset scroll to top.
- "Recently funded" widget should show amount raised + valuation, not the generic card.

## Metrics he prescribed
- **App opens per day per user** = the single most important metric for an information app.
- Cohort/frequency chart (D0 → D1 → D2) + RFM segments. *(The Wispr transcript garbles this line;
  he did mean cohort analysis.)*
- Benchmark: ~3.5 opens/day/user or ~30 min/user — **from strangers, not testers or early adopters**.
- Rule: if early adopters aren't giving good numbers, it's very bad — they'll read anything.

## Method he taught
Sticky-notes / card-sorting for IA: list use cases → map areas → have 5–10 people group them →
majority pattern = natural IA. (His example: where does "diamond rings" belong on a jewellery site.)

## iOS push bug — root cause
The app sends a **silent/remote push**, which NEVER delivers when the app is force-killed from the
switcher. Fix: send an **APS alert payload** (title, body, sound) with the ID in `data`; let
FCM → APNs render it directly instead of waking the app to check push type. Test by creating an
iPhone-user segment and reading the delivery report — a fresh install won't reproduce the failure.
This is the likely explanation for "push never fired" in [[project-inc42-app-behaviour]].

Standing offer: Ravi is happy to be called again for a sounding board.
