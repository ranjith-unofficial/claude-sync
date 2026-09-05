---
name: project-inc42-icp-role-definition
description: "5 Sep 2026 ICP + role-taxonomy definition across Media/App/DataLabs/IP — workbook with ICP MASTER grid, live role-value audit, payer personas"
metadata:
  node_type: memory
  type: project
---

Ranjith asked (4-5 Sep 2026) what the role / ICP should be for each Inc42 product, from Utkarsh's One Inc42 strategy plus the live platform. Deliverable: **`~/ClaudeDocs/inc42/inc42-icp-and-role-definition.xlsx`** — 9 tabs (README · ICP MASTER · Role hierarchy · Capture schema · Current state · Coverage · Payer personas · Qualifying actions · Gaps and actions).

**Deliberately NOT put in "One Inc42 - Analytics | Master Sheet"** — 9 tabs of pasting into a live shared file repeats the 5 Sep near-miss that overwrote his rows 27-256. See [[feedback-sheets-clipboard-paste-safety]].

**The strategic answer:** there is ONE ICP, not four (Strategy §1 H1). The role QUESTION is identical everywhere; only which LEVELS count as qualified differs per surface. Three verdicts used: QIA / IA only / Reach only (R30).

**Proposed schema (NOT approved):** Q1 employer type E1-E11 (required) → Q2 seniority conditional (operating ladder L1-L5, investment ladder I1-I5, or status S1-S3) → Q3 function (optional, DataLabs+Events). Plus mandatory `role_captured_at` (§5 requires it, exists nowhere).

**Per-surface QIA bar proposed:** Media L1-L4/I1-I4 · App L1-L3/I1-I4 · DataLabs L1-L3/I1-I4 + enabler L1-L4 · IP attendee L1-L3/I1-I3 only.

**Ground truth verified in PostHog 4-5 Sep 2026:**
- Media (53557): 10.47M persons · 92,827 with email · **31,597 with role (34% of identified)** · **938 with employer type (1.0%)** · Function dead (40). 33,975 total role answers across **49 distinct values in 5 formats**; 8,031 (23.6%) unusable, 4,734 Student, 20,655 (60.8%) usable+in-market. Cross-checks the 4 Sep property audit's "~34k not 89k".
- DataLabs (66351): 348,160 persons · 38,679 role (11.1%) · 35,269 role+employer (10.1% = Utkarsh's 9.99%). `Designation` only 33 records.
- App (146258): 1,100 persons · 876 role (79.6%, best rate anywhere) · **zero employer type** · 5-value vocabulary `founder/investor/operator/bd/other` · 408 (37%) unqualifiable.

**Findings that mattered:**
- The dropdown mixes 3 axes. **192 people picked "Investor" as seniority while working at Early Stage Startups**; 56 at Indian Corporates.
- Investor ladder is orphaned: Partner (671), Analyst_Associate (542), Principal_VP_Director (181), Senior_Associate_Manager (123) — **100% carry Company Type = NA**.
- **No "enabler / service provider" option exists anywhere.** §5 names exactly this case.
- **SEO/link-building/guest-post population: 197 of 1,554 real free-text Media titles (12.7%)** — would classify as `enabler` = QIA-qualified. Needs function + email-domain suppression.
- DataLabs already has `User_Profile_Fixed`, a 4-way computed persona (Market Researcher 18,156 / Founder-CXO 12,174 / Sales & Marketing 6,255 / Investor 3,035 / Other 653) with **better coverage (45,349) than Seniority (38,679)** — and it appears nowhere in the strategy.
- "Market Researcher" = 40% of the classified base but only **7% senior and 28% student/academic**.

**Payer personas (subscription only — NOT tickets/courses/sponsors; those need `contact_360.net_ltv`):**
- DataLabs project 610 payers: Market Researcher 193 (31.6%) · Founder/CXO 160 (26.2%) · not set 100 · Sales & Marketing 81 · **Investor 73 (12.0% vs 6.7% base = 1.8x over-index, the only persona that over-indexes)**. 250 (41%) have no role. **33 Academic/Journalist/Researcher have paid.**
- Media project 951 payers: 73% no seniority, 96% no company type.
- Cannot dedupe across projects (Pro Member 491 DL vs 435 Media). Dates unusable: 47% of DL payers have no first-payment date.

**Biggest open decision (G14):** does L5/I5 (Analyst, Executive, Associate) count to QIA on Media? Proposed IA-only; it is the single biggest swing factor in the QIA number.

Ranjith's correction that shaped it: "all in-market" was a non-answer, and abstract class names are not designations — he wants named job titles and explicit exclusions. See [[feedback-communication-style]], [[project-inc42-strategy-utkarsh]], [[project-inc42-funnel-analysis]], [[project-inc42-user-properties-audit]].
