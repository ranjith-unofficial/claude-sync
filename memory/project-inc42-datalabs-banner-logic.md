---
name: project-inc42-datalabs-banner-logic
description: "Datalabs dunning BANNER logic — scenario -> event -> banner copy -> CTA label -> landing destination, in the 'Test' spreadsheet tab Sheet14. LOCKED 30 Aug: failure-only scope, phased 1/2/3, six scenarios deliberately not shown. Plus the no-update-payment-method-on-UPI finding and 5 blocking decisions"
metadata:
  node_type: memory
  type: project
---

**Built 30 Aug 2026.** Ranjith asked for "the landing system" (= the dunning system) broken down as:
for every payment-failure scenario, what the banner says, what the CTA button says, and **where the CTA
lands**. The destination column had never existed anywhere before this.

**Deliverable: Google Sheet `1NCpTEzgEEtds0uCfqPNSS6aeFhOpKbgkL_F-cgtVPxg` ("Test"), tab `Sheet14`**
(gid 1356843013) — was an empty tab, now A1:M62, five stacked blocks:
- **A1:M25** — 16 scenarios (S1-S16), 13 cols: # / Scenario / Track / Trigger / Events fired /
  `banner_case` / Banner headline / Banner body / CTA label / CTA lands on / Access / Status / Guardrail
- **A27:D34** — destination catalogue D1-D5 + the three rules that apply to all of them
- **A36:C47** — the 9-step precedence ladder (first match wins)
- **A50:D53** — the proposed `dunning_banner` event + its 5 blocking dependencies
- **A56:D62** — the 5 open decisions
Formatted 210px columns, wrap, top-aligned. **Tab is still named "Sheet14"** — rename was offered, not answered.

**What is NEW here vs [[project-inc42-datalabs-dunning-map]] (the 8-case Razorpay status map):**
Eight lifecycle states that map had no banner for — S1 trial-converts-in-2-days (the only message that
lands before the NPCI pre-debit-notification revoke screen, P6), S2 mandate-unconfirmed-while-trial-runs
(the front end of the ₹92,665 bug, caught on webhook not Day 7), S3 mandate-paused (P5, suppress all
dunning), S4 subscription-detached (our own silent-expiry bug, 9 live subs ~₹15,919/mo), S5 insufficient-
balance split out from generic GATEWAY_ERROR (45% of first-charge failures, needs its own actionable copy),
S8 transient-retries-exhausted (policy undefined anywhere), S12 grace-day-6-7 escalation, and
**S13 post-cutoff winback days 8-15 — the locked 15-day attempts window has NO in-product banner today,
the map jumps straight from grace to Terminal.**

**THE DESTINATION FINDING THAT MATTERS MOST: there is no "update payment method" on UPI AutoPay.**
A mandate cannot be edited, only replaced. "Update payment method", "reactivate", and "re-authorize" all
resolve to the same action: a brand-new Razorpay subscription authorisation with a fresh ₹10 mandate (D2).
The locked S10 CTA literally says "Update payment method" and is describing something the system cannot do.
Two further destination rules: **D1 (Razorpay invoice `short_url`) must write back to the WooCommerce order**
or the customer pays and keeps getting dunned; and **every destination needs a logged-out magic-link path**,
because banner + WhatsApp + email all fire simultaneously on Day 0 (locked 24 Aug) and without it the
WhatsApp and email bars measure nothing.

**Five open decisions, all logged in the sheet, none answered as of 30 Aug:**
1. **S10 contradicts itself** — the decision map says Access = Cut, the locked banner says "You have {N}
   days left of access". Cannot ship until one is true. Blocks S10/S11/S12.
2. **S9's locked copy is wrong at fire time** — "your trial hasn't started" fires on Day 7, after they used
   the trial for a week. That wording belongs on S2. Replacement drafted in the sheet.
3. **S2: block or allow** — never grant access on an unconfirmed mandate, vs the trial is free and hard-
   blocking day 0 kills a convertible trial.
4. Still open from 25 Aug — first-payment transient access policy (Cut vs Live) and renewal-transient retry
   count. S5-S8 copy says "{N} of 4 attempts left" and cannot be finalised without it.
5. **Not Ranjith's call, Razorpay's**: is the ₹10 on reactivation charged again or adjusted? Every
   "Reactivate (₹10)" button depends on it.

**Telemetry**: proposed ONE event `dunning_banner` with `banner_stage` (viewed/cta_clicked/dismissed) +
`banner_case`, mirroring the `pro_subscription`/`pro_billing` one-event-with-a-stage pattern. NO ads
destinations. **Nothing here is targetable yet**: `pro_subscription` and `pro_billing` are renamed events
not yet fully live (descoped from the 29-Aug audit), `pro_subscription_status` has only one documented
value (`past_due`), and DataLabs `User Type` still has no failure state. Do NOT reuse `Alert Interaction`.

**How to apply:** this tab is now the authoritative reference for banner copy + CTA + landing, layered on
top of [[project-inc42-datalabs-dunning-map]] (which stays authoritative for Razorpay status -> case, retry
counts and grace windows). Locked copy is reproduced verbatim and marked LOCKED; proposed replacements sit
beside it rather than overwriting it. See also [[project-inc42-datalabs-dunning]],
[[project-inc42-datalabs-winback]], [[feedback-status-map-ui-treatment]],
[[feedback-sheets-clipboard-paste-safety]].


## SCOPE NARROWED, 30 Aug 2026 (same day, later in the session) — this supersedes the 16-banner layout above

**Ranjith's call, verbatim reasoning:** *"We will not show the banner in all the scenarios. We will only show the banner only for payment failure, not everything... right now it gets overwhelmed when people see. I'm okay, but people do get overwhelmed. So let's start with majority of cases followed by the other ones."*

**The test that decides inclusion:** a banner appears only when **money is at risk RIGHT NOW** AND **the user can fix it from the banner**. That test alone cut 6 of the 16.

**Phasing, now live in the sheet as a Phase column (A) with the rows reordered):**
- **Phase 1 — S5, S9, S4.** S5 (insufficient balance, 18 of 40) + S9 (dead mandate at first charge, 16 of 40 = 12 unconfirmed + 4 cancelled/inactive) = **34 of 40 first-charge failures (85%), 34 of 47 of all failed charges (72%)**. The real argument for this exact pair is not volume: they are the **two different mechanisms** (retry-and-wait vs re-authorise), so every later scenario becomes a copy variant on an existing rail rather than new engineering.
- **Phase 2 — S6, S7, S10.** Small volumes, but S10 hits existing payers and 30 of 31 payers logged in within 30 days.
- **Phase 3 — S12, S13, S8, S11.** Escalation copy only, no new plumbing.
- **Not shown — S1, S2, S3, S14, S15, S16.** Kept in the sheet with the reason, not deleted.

**S4 was argued INTO Phase 1 as the exception to the failure-only rule, and Ranjith did not answer the question — I proceeded on my own recommendation and flagged it.** The argument: a detached subscription (`requires_manual_renewal=true`, `next_payment_date` null) **never produces a failed charge at all** because no debit is ever attempted, so under a strict failure-only rule it gets no surface ever and just expires silently. 9 live subs, ~₹15,919/mo, plus 5 of 25 current trials. **If Ranjith later says out, it is one row to move.**

**Two consequences of the cut that are recorded in the sheet and should not be quietly forgotten:**
- **S1 was the only message that lands before the NPCI pre-debit-notification revoke screen (P6).** Regulation forces a monthly re-decision 12 times a year and there is now no in-product answer to it. Revisit if cancels are shown to cluster in the 72h after the PDN — still untestable, we do not log the PDN timestamp.
- **S3 shows no banner but its LADDER RULE IS NOT OPTIONAL.** A paused subscriber must still suppress every Phase 1/2 banner and every dunning send. Today paused subscribers get dunning meant for cancellations.
- **S14 (91 external cancels) is named in the sheet as the first candidate to revisit** — largest single cohort in the whole dunning problem.

**Precedence ladder was rebuilt at the same time** (rows 36-47, now 4 columns) with a "Does it render a banner in the current scope?" column. **The ladder is unchanged as logic** — every step is still evaluated in order, because a higher step suppressing a lower one is the entire point; only which steps *render* changed.

**Sheet layout after the rescope:** A1:N25 scenarios (14 cols, Phase added as column A) · A27:D34 destinations · A36:D47 ladder · A50:D53 telemetry · A56:D62 open decisions. Columns A:N at 210px, wrapped, top-aligned.
