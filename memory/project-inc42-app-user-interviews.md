---
name: project-inc42-app-user-interviews
description: "Inc42 App user-interview round (30-45 min calls) — the 4 Tally screener respondents, their contradictions, and the interview guide built 30 Aug 2026"
metadata:
  node_type: memory
  type: project
---

The WhatsApp screener from [[project-inc42-app-feedback-survey]] went live and collected responses into the Google Sheet "Inc42 App | Feedback" (id `10ftNlSE1RtGXVjFXlskr0CQIjeXqGlPB28VwJ94kEh8`, Sheet1). As of **30 Aug 2026 there are only 4 responses**, all submitted 28-29 Aug. The shipped Tally form kept ~13 of the redesigned 15 questions but **dropped the explicit interview-consent question** — all 4 left WhatsApp numbers, so they were treated as opted in (unconfirmed with Animesh).

Sheet columns: submission id, respondent id, submitted at, frequency, tenure, other Inc42 products, first thing checked (unaided), Brief experience, Brief usefulness, current streak, last Explore item, Explore relevance, one thing stuck with you, persona, name, WhatsApp number.

**The 4 respondents** (all "since launch"):
- **Mohit** — Founder, few times/week, DataLabs + Website/Newsletter. Brief "not useful", **never opened Explore**. Verbatim: "use it until it's free, no one come for paid news at all it's news only". Streak 0. The rejector / monetisation interview.
- **Amal Subhash** — Founder, daily, Website/Newsletter. Opens for the Daily Brief but hadn't opened it that day. Streak 3. Rates Explore "rarely" relevant yet gave the only detailed feedback in the set: company tracking is "another level", wants a **company fundamentals tab (revenue streams / business models)**. The power case for Companies-in-Explore.
- **Kishore** — Investor, daily, DataLabs. Reads articles, Explore "yes, often". Streak 5. Probes app-vs-DataLabs overlap.
- **Sastry** — persona "Other", daily, Website/Newsletter. Streak 1. "Yet to get used to the buttons… could really use it full screen on iPad." Usability/observation interview.

**Three contradictions the interviews are built around:**
1. Self-reported daily use vs streaks of 0/1/3/5 on a launch-cohort app — streak is either broken, invisible, or "daily" is aspirational. Trustworthy because it is functional recall.
2. Amal's stated entry point (Brief) differs from where he gets value (companies), and he hadn't opened the Brief that day.
3. Mohit is DataLabs+newsletter engaged but rejects the app's premise outright.

**Sample limits (stated explicitly to Ranjith):** all 4 are launch cohort — zero new users, zero lapsed users, so this round cannot explain the 55% card-1 drop or the 94% article one-way-door in [[project-inc42-app-behaviour]]. Recommended recruiting 2-3 churned users and 2 new installs from PostHog separately. Also: the DataLabs Pro incentive is worthless to Mohit and Kishore, who already use DataLabs.

**Interview guide (delivered in chat 30 Aug 2026)** — three objectives only: (a) what the app's real job is, Brief-as-habit vs Explore/companies-as-tool; (b) where the session actually ends and why; (c) acquisition and word of mouth, on which there is no qualitative data at all. Six blocks with a 30-min and 45-min timebox: last-session story → substitution/competitive stack → Brief comprehension (aided, only after Block 3) → Explore/companies → streak + push functional recall → acquisition/word of mouth → close. Plus per-person probes. Run order: Mohit → Amal → Kishore → Sastry.

**Moderation rules agreed:** nothing named before Block 3 (unaided before aided, per [[feedback-survey-question-design]]); ask "last time", never "usually"; never ask what they want, ask what they did; don't demo, defend, or mention v2 / Beyond Brief / AskInc42 / the Explore split; the push-notification question is a functional trap because app push has never fired correctly, so a vivid memory means newsletter or web push.

**How to apply**: before the calls, check whether churned/new-user recruits were added — the guide's conclusions are only valid for the launch cohort without them. Feeds decisions tracked in [[project-inc42-explore-articles-companies-design]] and [[project-inc42-app-v2-scope-full]].
