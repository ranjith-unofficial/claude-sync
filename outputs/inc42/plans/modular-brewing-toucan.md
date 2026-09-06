# Multi-role hiring agent: add Product Trainee, fix two live bugs

## Context

The hiring agent currently screens exactly one role — Founder's Office Associate. Ranjith is now hiring for **Product Trainee** (545 applicants already in Keka, job GUID `a21660ea-028d-40d4-a4b7-707d6523cf6f`) and will keep adding roles.

The workflow already reads salary/experience/city per role from a `Role configs` sheet, so it is *nearly* multi-role. What blocks it is that three rules are hard-coded in JavaScript and are correct for FOA but wrong for Product Trainee:

- **Internship exclusion** — correct for FOA (hires on full-time experience), fatal here. 134 of 545 applicants (24%) have *only* internship experience; excluding internships computes them at 0 years and hard-rejects all of them.
- **Presentation gate** — Yash rejects on photos and colour. Ranjith explicitly does not: *"I don't see even someone's adding a photo... no sense to reject as long as they are analytical, data-backed and mentioned some impact."*
- **Bucket weighting** — FOA is comms-50%. Product Trainee is a balanced operator split.

Two live defects must be fixed first because both change who passes the gates:

1. **Experience is miscounted.** Four failure paths found across 382 candidates — 38 (9%) fall back to Keka's self-reported figure which *includes* internships (7 of them cleared the 2-year floor on it), plus unhandled Trainee/Articleship/Summer Analyst titles, double-counted overlapping roles, and 4 candidates with absurd totals (60.27y) auto-rejected on garbage data.
2. **Salary gate is single-step.** Confirmed with Utkarsh: rejecting on expected CTC alone loses affordable candidates, because asks are inflated (median +31% over current). Needs the two-step current-CTC fallback.

**Outcome:** one workflow that screens any number of roles, with per-role rules living in the sheet where HR can change them, and Product Trainee live and calibrated against Ranjith's own judgement.

---

## Decisions locked

| Decision | Value | Source |
|---|---|---|
| Internships count toward experience (PT) | **Yes** | user |
| Salary cap (PT) | **₹5L**, 20% tolerance → ₹6L ceiling | user |
| Experience ceiling (PT) | **None** — flag over-experience as retention risk, never auto-reject | user; only 23 of 243 eligible have 3+ yrs |
| Presentation (PT) | **Not a gate at all.** Photo/colour/pages never reject. Substance decides | user |
| Weighting (PT) | Analytical 25 · Execution & impact 25 · AI fluency 20 · Written comms 20 · Product sense 10 | user |
| AI fluency evidence | Built something shippable + AI used in the analysis itself. Tool names in a skills row count for nothing | user |
| Hard content rejects (PT) | No analytics evidence at all · zero quantified impact | user |
| Tools (BigQuery/PostHog/GA4) | Hands-on preferred, **not** mandatory | user |
| Written comms judged on | Resume as writing sample (primary) + named deliverables (bonus) | user |
| Students | Must have internship experience and be able to join now as a trainee | user |
| CTC rule | Applies to **all roles** going forward | user |

---

## Architecture: one workflow, not two

**Do not clone the workflow.** 26 duplicated nodes means every bug fix applied twice with guaranteed drift — six bugs were fixed in it this week alone. Instead, move role-specific rules out of JavaScript and into `Role configs`, one row per role.

**Separate results tab per role.** FOA's tab is already 397 rows and shared with Utkarsh; a 545-row Product Trainee dump would swamp it, and a candidate can apply to both roles (dedup keys on candidate ID).

---

## Work, in order

### Phase 1 — Prerequisite fixes (code already written and tested)

**1a. `Normalize Candidate Fields` — experience computation**

Replace `INTERN_RE` / `splitRoles` / `computeTenureStats` with the tested implementation in
`<scratchpad>/fix_experience.js` (10/10 cases pass via `<scratchpad>/test_exp.js`). It:

- expands classification to Trainee / Apprentice / Articleship / Summer Analyst / campus ambassador / volunteer
- counts founder, freelance, contract and consulting as full-time
- sums the **calendar union** of spans, so overlapping roles count once
- returns `undatedRoleCount` and a human-readable `breakdown` string per candidate
- drives inclusion from a new `countInternships` role-config flag rather than always excluding

Also fix the silent inflation path: when Keka has no work history, do **not** quietly adopt the ATS figure as if it were full-time. Keep using it, but set `experienceReliable: false` and route those candidates to the AI with a flag rather than letting the number decide a gate.

Add a sanity bound — anything over 25 years is a data error, flag for manual review instead of auto-rejecting as overqualified.

**1b. `Evaluate Filter Bands` — two-step CTC**

```
expected ≤ cap                        → within_budget
expected ≤ cap × (1+tolerance)        → over_budget_tolerable
else if current × 1.30 ≤ ceiling      → negotiable_comfortable   (NEW)
else if current × 1.20 ≤ ceiling      → negotiable_stretch       (NEW)
else                                  → over_budget_reject
```

Note for Utkarsh: testing 30% *then* 20% does not change the pass set — 1.20 is the looser test and defines who passes. The 30% check separates *comfortable* from *stretch*, which is a tier, not a gate. Implement it as a tier so HR sees negotiating room per candidate.

On FOA this rescues **28 candidates** currently rejected on salary, including MANSI GUPTA (the only AI shortlist among the 11 HR had advanced — asks ₹15L, on ₹10L, affordable at ~₹13L).

Emit `typicalHikePercent` from the role config (default 20) so HR can tune it.

### Phase 2 — Make the workflow multi-role

**2a. New `Role configs` columns**

| Column | FOA | Product Trainee |
|---|---|---|
| `countInternships` | FALSE | TRUE |
| `presentationMode` | strict | off |
| `typicalHikePercent` | 20 | 20 |
| `experienceMaxYears` | 5 | *(blank = no ceiling)* |
| `bucketWeights` | comms 50, systems 30, research 10, ownership 10 | analytical 25, execution 25, ai 20, comms 20, product 10 |
| `hardRejects` | *(blank)* | no analytics evidence; zero quantified impact |
| `resultsTab` | Candidate Scores | Product Trainee Scores |
| `pilotCap` | *(blank)* | 25 for the first run |

`hiringManagerBrief` already exists — Ranjith's brief goes in that column on the new row.

**2b. `Sheet Data` — dynamic ranges**

Currently one static `batchGet` of `Candidate Scores` + `Role configs`. Split into two calls:
1. `batchGet` `Role configs` only
2. a Code node builds ranges from every `resultsTab` value, then a second `batchGet`

Two HTTP calls per run. This does not reintroduce the earlier quota problem — that was caused by n8n's Sheets node re-resolving tab names per item, not by call count.

**2c. `Build Claude Request Body` — read rules from config**

The `presentationCalibration` block is currently a hard-coded constant. Make it switch on `presentationMode`:

- `strict` — existing FOA calibrated block (single accent colour fine, 2 pages at 3+ yrs, one typo is a remark)
- `off` — presentation is **not assessed and cannot affect the verdict**. A photo, colour, icons and multiple pages are all explicitly fine. State this positively so the model does not smuggle it back in via "professionalism".

Weighting text and hard-reject text also come from the config columns rather than being fixed.

**2d. `Append Score to Sheet` — dynamic tab**

`sheetName` becomes an expression reading `resultsTab` from the role config. Create the `Product Trainee Scores` tab with the same 30-column schema, plus two new columns: `experienceBreakdown` (the audit string) and `salaryTier`.

**2e. `Filter Out Already-Scored + Enforce Pilot Cap`**

Read `pilotCap` per role instead of a constant, and dedup against the role's own results tab.

### Phase 3 — Product Trainee row + calibration

**3a.** Write the Product Trainee config row using the locked decisions above, with Ranjith's hiring-manager brief assembled from his answers.

**3b. Calibration tab (user asked for this explicitly).** Build a `PT Calibration` tab with **20 stratified applicants** — spread across the eligible pool by experience and expected CTC, not the top 20, so the sample contains real rejects.

The sample is already generated and reviewed with the user: `<scratchpad>/pt_calibration_sample.json`. Band spread across the 243 eligible — 6 at 6–12 months, 6 at 1–2 years, 4 at 2–3 years, 4 at 3 years+.

Tab layout:

| Column | Filled by | Contents |
|---|---|---|
| name, resumeUrl, experience, expectedCTC, currentCTC, location | agent | facts only — resumeUrl as a clickable PDF link |
| `yourVerdict` | **Ranjith** | Shortlist / Maybe / Reject (data-validation dropdown) |
| `yourReason` | **Ranjith** | one line |
| `agentVerdict`, `agentFit`, `agentReason` | agent | **written only after grading is submitted**, so the blind is not broken |

Order the 20 rows so bands are interleaved rather than grouped, so the grading is not anchored by seeing all the juniors first. Est. 30–40 min of the user's time.

This is the ground truth that has been missing across the whole project — every argument about models, bands and thresholds has been unresolvable without it.

Note: the sample surfaces a real data-quality issue the user should see directly — several rows carry blank CTC, and one candidate (HEMANT KANOJIYA) reads as asking ₹1.25L while currently on ₹7.5L. These are ATS entry errors, not real asks, and they are part of why the salary gate needs the two-step rule plus an `unknown` path rather than a single hard comparison.

**3c.** Run the pilot (cap 25), compare against the calibration grades, tune, then run the full eligible pool.

---

## Files and nodes

**Live workflow** — `https://automations.ink42.com/workflow/S9IBgvSMZMOVikN7` (currently inactive, 26 nodes). The only n8n object to be changed.

| Node | Change |
|---|---|
| `Normalize Candidate Fields` | experience computation (1a) |
| `Evaluate Filter Bands` | two-step CTC (1b) |
| `Sheet Data` | dynamic ranges (2b) |
| `Build Claude Request Body` | config-driven rules (2c) |
| `Append Score to Sheet` | dynamic tab (2d) |
| `Filter Out Already-Scored + Enforce Pilot Cap` | per-role cap (2e) |
| `Get Already Processed Candidates` | read the role's own tab |

**Sheet** — `1nxnP-rhbJCussb4z8bEKbehDe-eY2XyDU_kL_dNXjGs`: new columns on `Role configs`, new `Product Trainee Scores` and `PT Calibration` tabs. `Candidate Scores` is not restructured.

**Reference** — `<scratchpad>/fix_experience.js`, `<scratchpad>/test_exp.js`, `<scratchpad>/pt_candidates.json` (545 applicants), `<scratchpad>/keka_jobs.json` (48 jobs).

---

## Verification

1. **Unit** — `node test_exp.js` must stay 10/10. Add cases for `countInternships: true` (internships included) and the >25-year sanity bound.
2. **`node --check` every Code node before pushing.** Two nodes use top-level `await` and will fail a bare `--check`; check those by wrapping in an async IIFE, not by skipping them.
3. **No-op safety** — re-run FOA with `countInternships: FALSE` and `presentationMode: strict` and confirm verdicts match the current sheet apart from the experience fix and the 28 salary rescues. Any other movement means a regression in the multi-role refactor.
4. **Experience audit** — spot-check 5 Product Trainee candidates whose `experienceBreakdown` shows an intern→full-time conversion; the stated total must match a manual count off the PDF.
5. **Gate simulation before spending** — confirm the eligible count lands near the predicted 243 of 545. A large deviation means a config error, not a discovery.
6. **Pilot** — 25 candidates, verify rows land in `Product Trainee Scores` and not in `Candidate Scores`.
7. **Calibration** — agreement rate against Ranjith's 20 blind grades. FOA went from 1/11 to 8/11 after calibration; treat anything under ~60% here as not ready.

---

## Cost

| Item | Estimate |
|---|---|
| Product Trainee full run (243 eligible × ₹1.6) | **~₹389** |
| FOA re-run of candidates moved by the fixes | ~₹100 |
| Pilot (25) | ~₹40 |

Gets explicit approval before the full run — 545 applicants is larger than anything screened so far.

---

## Open items

- **Background wariness** — question was skipped. Defaulting to *"no background is a negative in itself; judge on evidence."* Needs confirming before the brief is final.
- **FOA salary cap** — stated three ways (Yash "10–12", Utkarsh "12–14", live config ₹12L). Moves ~30 candidates. Needs Yash's single number. Not blocking Product Trainee.
- **Typos** — Yash treats misspellings as a hard negative, Shweta as a remark. Now resolved *per role* by `presentationMode`, so the global conflict no longer blocks anything.
- **Security** — the Keka client secret, Keka API key and an Anthropic API key sit in plaintext in the `Workflow Config` node, readable by anyone with n8n access. Should move to n8n credentials. Flagging, not fixing, unless asked.
