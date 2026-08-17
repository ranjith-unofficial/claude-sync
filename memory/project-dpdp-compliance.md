---
name: project-dpdp-compliance
description: "DPDP compliance engagement with external vendor (Shivang) — 3-phase, ₹12-13L, tech review with leads Prapti & Ashish"
metadata: 
  node_type: memory
  type: project
  originSessionId: 76c2b18d-df04-4054-8ad6-b08fabbe668a
  modified: 2026-08-12T04:25:49.569Z
---

DPDP (India data protection) compliance engagement. Vendor is **KavachOne** (leads: **Shivang**; workbook contact **Anupam Singh**); Ranjith's tech leads are **Prapti** and **Ashish**. Kickoff call held ~Jul 18 2026.

**Mandate:** DPDP compliance required post **May 2027**; supersedes existing obligations, GDPR-style. Non-compliance → regulator NC/fines (illustrative risk cited up to ₹200–500 cr). 168 controls target alignment.

**Verified statutory dates** (DPDP Rules 2025 notified **13 Nov 2025**): Rule 4 **consent management → 13 Nov 2026**; Rules 3, 5–16, 22, 23 (notice, safeguards, breach, erasure, children, rights, cross-border, SDF) → **13 May 2027**. The Nov 2026 consent-manager date is the *earlier* binding deadline and is often missed.

**Entity facts (verified, use these — don't re-derive):** two entities. **Ideope Media Pvt Ltd** (inc. 21 Nov 2014, CIN U63119DL2014PTC273439 per thecompanycheck — ClearTax shows U74140DL2014PTC273439 for the same reg. no., *unresolved, ask Finance*) owns the mobile app + Datalabs + both store dev accounts; FY24 revenue ₹15.69 Cr; EPFO ~41 on-roll. **Inc42 Plus Media Pvt Ltd** (inc. 19 Feb 2024, CIN U58191DL2024PTC427039) operates inc42.com under exclusive licence from Ideope. Common board: Vaibhav Vardhan, Utkarsh Agarwal, Pooja Sareen. Turnover band **< ₹50 Cr**. Headcount to quote = **~80–100 total workforce** (not the 41 EPFO figure — 41 under-scopes endpoint licensing). Data principals **~1–5 lakh**. Not notified as an SDF.

**KavachOne intake workbook completed 2026-07-26** → `~/Downloads/DPDP_Input Sheet - Inc42 FILLED.xlsx` (3 tabs: Org Profile 14 Qs, Data Inventory 24 rows, Scope & Logistics 10 Qs). The **live Privacy Policy (updated 16 Jul 2026) is effectively a ready-made ROPA** — its §3 data categories, §4 legal-basis table, §7.1 processor list, §8 cross-border table and §10 retention schedule were the source for the inventory. Start there for any future DPDP artefact.

**Two NEW gaps found while filling it (not from the tech call):**
- **AI features are undisclosed processing.** Privacy Policy §5.1 names Ask Mode / AI reports / company summaries as live, but **no LLM/AI sub-processor appears in §7.1 or §8**. Provider unidentified, no DPA, no zero-retention/no-training terms. Needs identification + policy update.
- **Deletion likely doesn't cascade** from the app DB to BigQuery, Elasticsearch, Customer.io and HubSpot. Unverified; if true, the published 7-day permanent-deletion promise is not actually met.
- Also: Datalabs "Listed Individuals" (Fullenrich-enriched business contacts) is the **highest-risk processing** — relies on DPDP **s.14 publicly-available exemption** + notice/opt-out because DPDP has no legitimate-interest basis. Whether *enriched* data is still "publicly available" is the weak point.

**Phases:**
- Phase 1 — Gap assessment/discovery: data mapping (structured/unstructured, sensitive/non-sensitive), data flow diagrams, gap report, prioritized critical/high gaps.
- Phase 2 — Implementation: controls, patch high-vuln gaps, TPRM (up to 25 vendors), consent manager, security tooling (EDR, DLP/encryption, DSPM). ISMS/ISO audits alongside.
- Phase 3 — Managed services: optimization, stabilization, audits, resilience.

**Commercials:** ₹12–13L full 3-phase (₹12L excl. consent manager, ~₹13L incl.). Consent manager ~₹1.5L separately. Payment staggered 30/30/rest. Timeline 8–10 months (worst case 10).

**Tech review call held ~Jul 20 2026** (Shivang + Ashish + Prapti + Ranjith, ~22 min). Current-state findings:
- Infra: GCP-hosted, multiple websites, VPC + firewall + Cloud DNS security rules. Google Workspace only (no Microsoft).
- ~80–90 company laptops, mostly Mac, some Windows; no/negligible Linux.
- **Absent:** DNS filtering, EDR/XDR, DLP, MDM, consent manager, ISO 27001 / ISMS / cyber audits, written security policies.
- Present: Datadog (app logs only — endpoints/laptops not connected), multi-level app logging, rate limiting + IP blocking on brute force, server-to-server encryption, per-account Google Doc sharing (no public links).
- **Red flag raised in call:** subscriber passwords stated as MD5-hashed.
- Shivang quoted CrowdStrike EDR ≈ ₹1,500/user/yr → ~₹1.5L for 100 users.
- Shivang will do data flow mapping himself in Phase 1 regardless of inputs; Phase 2 includes a face-to-face workshop + cyber training (he cites 60–75% of India attacks stem from unintentional employee error).

**Open action items:**
- Shivang: revised proposal + 100% accurate SOW; data flow mapping; schedule face-to-face session.
- Ashish: plan EDR (CrowdStrike-class) rollout across all endpoints; connect endpoint logs to Datadog.
- INC42: consent manager + DLP; employee cyber-security training program.

**2026-08-11 — vendor quote from "Mitigator" (agency); Ranjith deliberately slowing the whole engagement down.**

⚠️ **Unresolved:** the transcript names the agency as **Mitigator**, while this memo's earlier entries name **KavachOne / Shivang**. Same 3-phase shape and a similar consent-manager carve-out, but different numbers — could be the same vendor re-quoting, a second vendor being compared, or a transcription slip. **Ask Ranjith before treating these as one engagement.**

**Commercials as pitched (Mitigator):**
- Opening quote **₹15L + GST**, 3 phases, timeline ~**1 year** → would land in **Jul 2027**, past the **13 May 2027** full-enforcement date. Ranjith rejected it on both timeline and price, and noted the long timeline itself looked like a way to bill more.
- Revised to **₹10L + GST** for all phases, targeting completion **Nov–Dec 2026**.
- **Excluded, and this is the trap:** consent manager **+₹2L**, and TPRM (third-party risk management) / security tooling quoted at a further **~₹15–20L**, "if identified during assessment." Realistic all-in ≈ **₹30L**.
- **Lock-in risk Ranjith called out explicitly:** once ₹12L is paid (₹10L + ₹2L consent manager), Inc42 can't credibly switch vendors for the security tooling — the incumbent alone knows what/how to implement, so the ₹15L follow-on is effectively captive. He also flagged that the vendor keeps surfacing new line items after every conversation.

**Ranjith's stance:** buying time on purpose. He will **not go to Utkarsh until he knows the minimum DPDP requirement** — what's actually mandatory vs. what the agency is upselling. Rationale: entering implementation without that understanding means paying for optional controls and burning team bandwidth. He's told Utkarsh not to rush this.

**Ritvik's read (worth testing, not accepting):** the proposed program looks calibrated for a large corporate. Inc42 holds fairly basic, user-submitted personal data plus internal docs — he is not confident the government's actual minimum requires this level of security tooling. Action: **check the statutory minimum first.**

**Baseline obligations Ranjith named as genuinely in scope** (his own framing of the "four or five basic things"): vendor onboarding/due diligence; breach notification to affected users + remediation; HR data — where Keka-held data (PAN, Aadhaar) is stored, how long, who internally beyond HR can see it; customer data access mapping; undocumented contact lists (e.g. the speaker team keeping prospect lists in personal Excel/phone contacts); and **what employee-side AI usage sends customer PII to third-party models** — the same gap already flagged above under "AI features are undisclosed processing."

**Next step:** Ranjith to work out the minimum-requirement picture over 11–12 Aug, then push the agency for a re-scoped plan.

Related: [[project-inc42-launch]] (separate app work), [[reference-inc42-vendor-stack]], [[project-inc42-hiring-agent]] (candidate PII → LLM, same exposure).
