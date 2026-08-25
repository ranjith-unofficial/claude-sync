---
name: project-inc42-foa-candidate-shortlist
description: "Founder's Office Associate hiring — manually re-verified shortlist as of 2026-08-25, and the automated scorer's specific blind spots found"
metadata: 
  node_type: memory
  type: project
  originSessionId: 97ea0664-fc1d-41fd-80f4-9efe9e6f5306
  modified: 2026-08-25T09:54:14.109Z
---

Ranjith asked (2026-08-25) which of the AI Hiring Agent's "Maybe"-status candidates for Founder's Office Associate (FOA) to schedule interviews for. Screening the sheet's own fitScore/reason text wasn't enough — manually pulling and reading the actual resume PDFs surfaced real issues the automated scorer missed or soft-pedaled, including on its own top-scored candidates. See [[project-inc42-hiring-agent]] for the build/scoring-methodology history and [[feedback-hiring-sheet-ctc-parsing]] for a related data-reading rule.

**Final shortlist to schedule (in order), as of 2026-08-25:**
1. **Mansi Gupta** — Pending status, *never run through the automated scorer at all*. Best substantive match in the whole pool: 4 continuous years at one company (Activitybeds), sole owner of product/ops/growth reporting directly to the CEO, no team. Salary asks 15L on a 10L base — above the raw 14.4L cap but passes Inc42's own two-step CTC rule (current + typical hike ≈13L, negotiable). Resume: https://inc42.keka.com/ats/documents/5d6ccd68-aea2-4816-988e-e739d1fa1906/resumes/8995118388e746d293d6a9e0fe97cfc8.pdf
2. **Sushant Kushwaha** — verified clean (Drishti IAS, Founder's Office Research Associate; 0-day notice). Resume: https://inc42.keka.com/ats/documents/5d6ccd68-aea2-4816-988e-e739d1fa1906/resumes/b1682870f8fa4fa0a7f96e3f95d482d8.pdf
3. **Vishrut Sinha** — verified clean (KPMG Water Resources Advisory 29mo → PedalStart startup screening 6mo, zero gaps). Resume: https://inc42.keka.com/ats/documents/5d6ccd68-aea2-4816-988e-e739d1fa1906/resumes/d58477aa72c9458e95407d64e5b5a795.pdf
4. **Peddinti Prithvi** — verified clean, current literal title "Founder's Office – Associate" at Hopcharge. Resume: https://inc42.keka.com/ats/documents/5d6ccd68-aea2-4816-988e-e739d1fa1906/resumes/e80a5320254b4cfa8d52ebf4e09e6157.pdf
5. **Sejal Gupta** — Pending status, unscored. Current title "Founder's Office" (The Guidant Group, 2.3yrs), incl. PMO/investor-comms work on a ₹500–2,000cr IPO. Resume formatting/section order is a bit jumbled — worth a clarity check before scheduling. Resume: https://inc42.keka.com/ats/documents/5d6ccd68-aea2-4816-988e-e739d1fa1906/resumes/d4ee032a96f94b3e970554e4a21d0cf2.pdf

**Excluded after verification — with the specific reason, since the sheet's own text didn't catch these:**
- **Naitik Sarvaiya** (Shortlist, fitScore 78, IIM-C/Accenture/KP-Group Chief-of-Staff) — real current CTC ₹32L (~55% cut to Inc42's band = flight risk) plus an undisclosed current 8-month employment gap on top of a 15-month gap the sheet did catch. Not a hard no — worth a screening call to test genuine interest/comp flexibility — but not a blind schedule.
- **Kushagra Baranwal** (Shortlist, fitScore 75) — real full-time experience is only ~14 months (Amrop India, June 2025–present); everything else on the resume (SRCC clubs/PORs/internships) was done while still a student (graduated 2025). Confirms the internship/PMO-experience-inflation bug flagged in [[project-inc42-hiring-agent]] is still live and affects even the top-scored tier. Shweta's own remark on the sheet already flagged this.
- **Heemaal Razdan** (Maybe, tied top fitScore 68) — real founder's-office-relevant experience is only ~5 months across two stints, one of which claims a "CTO" title after ~2 months at an early-stage app. 85% of her actual career (2.3yrs) was HDFC Bank credit-assessment work, unrelated domain.
- **Raunaq Sharma** (Maybe, fitScore 62) — sheet caught one 20-month gap (2021–23) but missed a second, current 18-month gap (unemployed since Feb 2025). Also a domain mismatch: his career is investment/tax (VC deal sourcing, Deloitte tax compliance), not strategy/founder's-office generalist work.
- **Nitya Sikri** (Maybe, fitScore 62) — real title is Key Account Manager at Zomato (sales/commercial), not a strategy/founder's-office generalist, despite analytics-heavy bullets reading well.
- **Riya Malhotra** (Maybe, tied top fitScore 68) — real substance is solid (Grant Thornton + current founder-facing PM role), but heavy purple block-color resume template and corporate-boilerplate/AI-generated-sounding bullet phrasing are real concerns; salary (14L) sits at the very edge of the 14.4L tolerance ceiling. Not excluded, but needs a resume-format screen first.

**Pattern worth remembering:** the automated scorer's `fitScore`/reason/concerns text is directional, not reliable at the top of the ranking — it missed real issues on 3 of its own top-4 highest-scored candidates (Kushagra, Heemaal, Raunaq) and completely missed the single best-fit candidate (Mansi Gupta) because she was sitting in "Pending" status, never scored. **Before finalizing any interview shortlist from this sheet, pull and read the actual resume PDFs for the top candidates rather than trusting the sheet's summary text alone** — specifically check: (1) real vs. claimed experience duration (internship/PMO-inflation), (2) full employment timeline for undisclosed gaps, (3) whether the candidate's actual job titles match the strategy/founder's-office/consulting domain vs. an adjacent one (sales, account management, finance/tax, product), (4) the Pending/unscored bucket, which may contain HR-advanced candidates the automated pipeline never touched.
