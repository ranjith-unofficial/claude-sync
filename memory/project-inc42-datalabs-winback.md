---
name: project-inc42-datalabs-winback
description: "Datalabs subscription payment-failure/churn win-back plan — artifact, key metrics, and locked design decisions"
metadata: 
  node_type: memory
  type: project
  originSessionId: 63f9925b-7dae-44a5-b4f7-ae143c5226fa
  modified: 2026-08-24T09:53:44.392Z
---

**Datalabs Win-Back Plan** — artifact built 23 Aug 2026, revised 24 Aug 2026: https://claude.ai/code/artifact/efaafcd9-c00a-464d-92d8-1e30e08e5702

Diagnoses why Datalabs subscription payments fail and what's recoverable. Source: PostHog 66351 + a "Funnel State 2026-07" snapshot (WooCommerce Subscriptions/Razorpay billing data — not a PostHog event funnel).

**Key numbers (as documented; some derived, not source-stated — flagged inline in the doc):**
- Day 7 first real charge: 57.9% success rate (was 73.7% in May) — reconciled as ~55 of ~95 Day-7 charge attempts succeeding, the other 40 failing for the reasons below. This denominator isn't explicit in the source; it was derived by matching totals — high-confidence, not confirmed.
- 40 total first-charge failures: insufficient balance 18, mandate never confirmed 12, cancelled/inactive 4, bank declined 2, other 4.
- ~21 of 40 (52%) is a **projected** recovery target from the seven fixes below, not an observed result — nothing has shipped yet, baseline is 0%. The doc's own "Fixed by" attribution doesn't cleanly match the "~11/~8 worth" headline figures (bank-declined's ~1 sits under P1, cancelled/inactive's ~1 sits under P3) — flagged as an open reconciliation, not silently fixed.
- Only 16 subscriptions have ever reached a 2nd charge.

**Seven problems (P1–P7), ordered by worth:**
- P1 retry logic — failed payment never retried (47 failures, 0 retries ever); worth ~11 of 21
- P2 unconfirmed mandates — trials start on mandates never confirmed (30% of first-charge failures; 9 paying + 5 of 25 trials affected right now); worth ~8 of 21
- P3 no dead-mandate messaging — 73 revoked subs with no failed charge yet, none contacted
- P4 late detection — revocation detected via polling, not webhook (0 of 91 caught before the next charge bounced)
- P5 paused ≠ dead — 263 logged paused instances get dunning meant for cancellations
- P6 no messaging around the 12 annual pre-debit notifications
- P7 four uncontacted groups (revoked-not-broken 73, paused TBC, paying-mandate-detached 9 [~₹15,919/mo], trials-can't-convert 5 of 25)

**Locked design decision (24 Aug):** P3's banner + WhatsApp + email fire **simultaneously on Day 0**, not staggered (was 0h / +48h / +5d) — the cohort is small enough (73+9+TBC+5) that staggering's cost-saving is negligible, and recovery speed matters more. Each channel gets its own tracked link so the individual bars (banner ≥3%, WhatsApp ≥3%, email beats 0.2%) still measure separately even though they launch together.

**Owner column deliberately excluded** from the task table (25 tasks) and the decisions table — Ranjith confirmed not required for this doc.

Related: [[project-inc42-funnel-analysis]], [[reference-inc42-posthog-projects]] (project 66351 = DataLabs)
