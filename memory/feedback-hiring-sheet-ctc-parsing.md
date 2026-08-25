---
name: feedback-hiring-sheet-ctc-parsing
description: How to read currentCTC/expectedCTC fields in the INC42 AI Hiring Agent sheet — units and invalid-data handling
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 97ea0664-fc1d-41fd-80f4-9efe9e6f5306
  modified: 2026-08-25T09:53:40.909Z
---

When reading `currentCTC`/`expectedCTC` fields from the INC42 AI Hiring Agent Google Sheet ("AI Hiring Agent - Pipeline", Candidate Scores / equivalent per-role tabs):

- **Any plain number is LPA (lakhs per annum), never thousands/month.** A value of "32" means ₹32L/year, not ₹32K/month — confirmed by Ranjith 2026-08-25. Don't hedge on this or ask the candidate/user to disambiguate; just read it as LPA.
- **Implausibly low values (≈≤2) are bad data, not real figures — exclude that candidate's CTC comparison rather than reporting the number as fact.** E.g. `expectedCTC = 1` is a parsing/entry error, not "candidate wants ₹1L." Confirmed on NAITIK SARVAIYA (current=32 read as ₹32L, expected=1 treated as invalid/excluded) and AYUSH TANWAL (current=1, expected=0.1, both invalid).

**Why:** Ranjith corrected me after I flagged Naitik Sarvaiya's ₹32-vs-1 CTC pair as ambiguous and asked whether to interpret 32 as LPA or K/month — he confirmed the sheet's convention directly rather than have it re-litigated per candidate.

**How to apply:** Any time I re-pull or re-screen candidates from this sheet (or its Product Trainee equivalent, likely same convention), apply this rule automatically before presenting salary-fit analysis — don't re-ask. See [[project-inc42-foa-candidate-shortlist]] and [[project-inc42-hiring-agent]].
