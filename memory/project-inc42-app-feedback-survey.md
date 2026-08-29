---
name: project-inc42-app-feedback-survey
description: "WhatsApp user-research recruitment form for Inc42 App — redesigned from marketing's flawed feedback-survey draft into a funnel screener with concept-then-relevance questions; Slack thread with Animesh/Ritvik"
metadata: 
  node_type: memory
  type: project
  originSessionId: b685198d-c342-4727-a8fb-284c615d0d53
  modified: 2026-08-28T13:20:54.439Z
---

Ranjith wants to gather feedback from Inc42 App users via WhatsApp: collect basic details, gauge interest in a 30-45 min user interview, incentivize with 1 month free DataLabs Pro. Marketing (Animesh) built a Tally form (https://tally.so/r/obLxjx) in response, but it was a 9-question full feedback survey (Brief star rating, streak/onboarding/sign-in/Explore questions, 3 open text fields, file upload) — not a lightweight recruiting screener, and never mentioned the incentive or the interview ask until the last question.

**Slack thread**: Animesh shared the form Yesterday 6:58 PM in a channel with Ranjith + Ritvik Sethi, followed up Today 11:01 AM asking for edits. Ranjith replied 11:28 AM (28 Aug 2026): Q1 "How is the Daily Brief?" should split into (a) test whether users understand Daily Brief as a concept, then (b) whether they find it relevant/useful — flagged "a few similar changes" and said he'd call to discuss. Ranjith then worked through a full redesign before that call.

**Redesign methodology** (see [[feedback-survey-question-design]] for the reusable principles):
- Funnel order: disqualify (real usage) → context → unaided recall → interest+incentive → contact logistics
- Apply concept-then-relevance to each major feature (Brief, Streak, Explore), not just Brief
- Replace self-assessed "do you know what X is" questions (face-saving bias) with functional recall questions (a concrete fact only a real user could produce) — e.g. streak: "what's your current streak?" not "do you know what streak is"
- Incentive (DataLabs Pro) placed after usage context is established, not as the opening hook
- DataLabs Pro flagged as a possibly weak incentive for this audience — niche product (31 active paying subscribers total across Inc42, see [[project-inc42-datalabs-dunning]]), unfamiliar to general app readers; added a screening question ("do you use any other Inc42 products") specifically to test whether the reward is even legible to the respondent

**Final 15-question set** (as of 28 Aug 2026, sent to Animesh, not yet rebuilt in Tally):
1. Usage frequency (Daily/Few times a week/Rarely/Not anymore)
2. Tenure (Since launch/A few months/Just started)
3. Other Inc42 products used (Website/DataLabs/Plus/Just the app)
4. Open: "what's the main thing you do when you open the app" (unaided recall, tests if Brief registers as a concept without naming it)
5. Brief engagement description (opened & read/opened, didn't read much/haven't opened today/don't know what this refers to)
6. Brief relevance/usefulness (gated on Q5 showing engagement)
7. Current streak number (a number/0/don't know what a streak is)
8. Last thing looked at on Explore (company profile/article/something else/haven't opened/don't know)
9. Explore relevance (gated on Q8; options include a diagnostic "feels repetitive")
10. Open: "one thing that's stuck with you, good or bad"
11. Persona (Founder/Investor/Operator/BD & Partnerships/Other — reuses existing onboarding taxonomy)
12. Interest + incentive ask (Yes/No, DataLabs Pro stated plainly)
13-15. Name, WhatsApp number, preferred day/time

**UPDATE 30 Aug 2026**: the form went live and collected responses into the Google Sheet "Inc42 App | Feedback" (id `10ftNlSE1RtGXVjFXlskr0CQIjeXqGlPB28VwJ94kEh8`). Only **4 responses** as of 30 Aug. The shipped version kept most of the redesigned set but **dropped the interview-consent question**. Respondents, contradictions and the interview guide are in [[project-inc42-app-user-interviews]].

**Status**: Ranjith sent Animesh a short message pointing to the revised questions + a summary of what was missing (functional recall vs self-report, funnel ordering, dropped file-upload/"add to Explore" questions). Awaiting Animesh to rebuild in Tally; Ranjith will review before it goes out. Ritvik is cc'd on the Slack thread but not yet directly involved in this specific form.

**How to apply**: when asked about this form's status, check whether Animesh has rebuilt it before assuming the old 9-question version is still live. If asked to extend or re-open this design, reuse the methodology in [[feedback-survey-question-design]] rather than re-deriving from scratch.
