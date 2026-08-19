---
name: project-inc42-product-trainee
description: "Product Trainee role Ranjith is hiring for himself — 545 Keka applicants, locked screening criteria, budget 3-5L, calibration tab awaiting his blind grades"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0a7258b2-f45b-4229-84ea-2bf0e20e0797
  modified: 2026-08-17T18:17:56.428Z
---

Ranjith is hiring a **Product Trainee** for his own Product & AI team at Inc42 — so unlike Founder's Office Associate (where Yash is the hiring manager), **he is the hiring manager here** and the calibration brief comes from him directly.

**Role facts (confirmed 2026-08-17):**
- Keka job GUID `a21660ea-028d-40d4-a4b7-707d6523cf6f`; public JD `inc42.keka.com/careers/jobdetails/155271`
- JD file: `~/Downloads/Product Associate_APM.docx.md`
- **545 applicants already in Keka** (bigger than FOA's 397). 243 pass the pay + experience gates.
- Budget **₹3–5L**; Delhi; JD asks for 6+ months in Product/Analytics/Growth, BigQuery/PostHog/GA4/Mixpanel/Amplitude, n8n automations, AI fluency

**Screening criteria Ranjith locked (his own calls, 2026-08-17):**

| Decision | Value |
|---|---|
| Internships count toward experience | **YES** (opposite of FOA) |
| Salary cap | ₹5L, +20% → ₹6L ceiling |
| Experience ceiling | **None** — flag over-experience as retention risk, never auto-reject |
| Presentation | **Not a gate at all.** A photo is fine. Substance decides. |
| Weighting /100 | Analytical 25 · Execution & impact 25 · AI fluency 20 · Written comms 20 · Product sense 10 |
| AI fluency evidence | Built something shippable + AI used in the analysis itself. Tool names in a skills row count for nothing. |
| Hard content rejects | No analytics evidence at all · zero quantified impact |
| Named tools (BigQuery/PostHog/GA4) | Hands-on preferred, **not mandatory** |
| Written comms | Resume as writing sample (primary) + named deliverables (bonus) |
| Students | Must have internship experience and be able to **join now as a trainee**, converting to full-time later |

**Why the internship call mattered:** 134 of 545 (24%) have *only* internship experience. Applying FOA's exclusion rule computes them at 0 years and hard-rejects all of them before any resume is read. This is the reason the internship rule had to move from JavaScript into per-role sheet config.

**The budget/experience tension — flagged to Ranjith, he chose to proceed:** median applicant ask is ₹7L against a ₹5L cap, so only 49% pass on expected CTC alone. Median *current* is ₹3.5L, so the two-step CTC rule brings 377 of 545 back into range. Without that rule this role has almost no pipeline. Realistically the role reaches freshers, intern-converts and career-switchers — not people with the tool fluency the JD lists.

**Status (2026-08-17):** `PT Calibration` tab is **live and waiting on Ranjith's 20 blind grades** — 20 stratified applicants (6 at 6–12mo, 6 at 1–2y, 4 at 2–3y, 4 at 3y+), bands interleaved, resume links + dropdown. Sheet `1nxnP-rhbJCussb4z8bEKbehDe-eY2XyDU_kL_dNXjGs`. Agent columns stay blank until he submits, to keep the blind. Cost so far ₹0.

**How to apply:** do NOT spend on screening until his 20 grades are in and the agent has been measured against them. This is the ground truth that has been missing across the whole project — see [[project-inc42-hiring-agent]] for why (FOA agreement went 1/11 → 8/11 only after calibration). Estimated full run ~₹389 for 243 candidates; needs his explicit go. Approved plan lives at `~/.claude/plans/modular-brewing-toucan.md`.

**Still open:** whether any background is a negative in itself (question skipped; currently defaulting to "judge on evidence only") — confirm before the hiring-manager brief is finalised.

## Calibration RESULT (2026-08-19) — the ground truth finally exists

Ranjith graded all 20 blind: **16 Reject · 3 Maybe · 1 Shortlist** (Arpita Dhingan).

**What actually drove his 20 calls** (from his written reasons, not the locked rubric):
| Driver | Count |
|---|---|
| Background relevance — "he's a developer / designer / data analyst / marketer, irrelevant" | 9 |
| Clutter / "not presentable" / "too cluttered for me to read" | 6 |
| Substance (impact, tailoring, clarity) | 4 |
| Budget | 1 |

⚠️ **Both top drivers contradict decisions he locked on 17 Aug** ("presentation is not a gate at all"; "no background is a negative in itself") **and the JD's own line "We're open in the background."** His revealed rubric is stricter than his stated one. Do not treat the 17 Aug locked list as a complete description of his bar.

**Agreement measured, offline replica of the n8n agent (same model `claude-sonnet-5`, same request shape — adaptive thinking, effort high, json_schema). Live workflow S9IBgvSMZMOVikN7 was NEVER touched.**

| Rubric | Exact | Within one band | Shortlists |
|---|---|---|---|
| v1 (17 Aug locked decisions only) | **15/20 (75%)** | 20/20 | 1 ✅ |
| v2 (+ B2C / structured writing / user thinking / first principles, stated 19 Aug) | **17/20 (85%)** | 20/20 | **0** ❌ |
| v3 (v2 but pure-b2b capped, `mixed` NOT capped) | running on full pool | | |

- v1 was **better than predicted** — it agreed on 5/6 presentation rows and 6/9 relevance rows by reaching the same rejects via *substance* ("no quantified impact", "AI listed as skills only"). Stripping presentation/background rules cost almost nothing.
- v2's B2C rule fixed Utkarsh/Anmol/Siddharth but **capped Arpita — his only Shortlist — at Maybe(57) for "recent core work is B2B fintech."** Hence v3: the `mixed` vs pure-`b2b` split is the load-bearing line. His 4 non-rejects all classified `mixed`; the 8 he rejected hardest all classified `b2b`.
- Zero inversions in any version. All disagreements are one band, agent always the more generous side.

**Cost is ~2.5x the plan's estimate: Rs 2.4-2.6/resume, not Rs 1.6** (`effort: high` + adaptive thinking burns output tokens). Full 235 run ≈ Rs 600, not Rs 389.

**Deployment state (verified 2026-08-19, unchanged since):** plan phases 1a, 1b, 2 and 3a are **NOT deployed**. `Role configs` still has exactly ONE row (FOA) and none of the multi-role columns. `fix_experience.js` no longer exists on disk anywhere. The live agent still cannot screen Product Trainee at all — everything above was run offline, which is now the recommended path: 235 candidates cost ~Rs 600 and ~30 min with no n8n changes. The n8n refactor only buys automated polling and HR self-service.

**Hard-filter numbers (recomputed 19 Aug, two-step CTC + internships counted):** 545 total → **235 eligible**; 184 rejected on salary alone, 91 on experience alone, 35 on both. **60 people are in the pool ONLY because of the current-CTC rescue step.** Tier split: 36 negotiable_comfortable (30% hike also fits), 24 negotiable_stretch.

⚠️ **Keka stores CTC in mixed units** — some rows in lakhs ("5"), some in absolute annual rupees ("600000"), plus an unusable middle band (1000–100000: monthly? low annual?). The **live workflow already handles this** (`raw < 1000 ? raw : raw / 100000`). Any new filter written from scratch must too — getting it wrong cut the eligible pool from 235 to 103.

**Two rubric questions still open with Ranjith:**
1. **Product sense is weighted 10%** in the locked weights, but user thinking / first principles / structured docs — everything he emphasised on 19 Aug — live in Product sense + Written comms (30% combined) while Analytical + Execution hold 50%. The weighting likely no longer matches his bar.
2. Whether the B2C rule should cap `mixed` profiles (v3 says no, based on Arpita).

Artifacts in `<scratchpad 88ba76e1>`: `pt_brief.py` (v1), `pt_brief_v2.py`, `pt_brief_v3.py`, `eligibility.py`, `run_pool.py`, `pool_results.json`, `ranjith_grades.json`.
