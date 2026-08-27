---
name: project-inc42-datalabs-dunning-map
description: "Datalabs dunning system decision map — case-by-case mapping of exact Razorpay statuses to treatment (retries/grace/banner), built from the engineering spec; sheet + artifact locations, locked vs open decisions"
metadata: 
  node_type: memory
  type: project
  originSessionId: e87f7b2e-19d8-490d-a96f-71d19eb01e0a
  modified: 2026-08-27T09:19:22.457Z
---

Aug 2026. Built a case-by-case reference mapping every exact Razorpay status/webhook Datalabs Pro can receive to its treatment (access policy, retries, grace/attempts window, in-app banner copy, guardrails). Source: the Notion engineering spec "Subscription Dunning, Recovery & Winback System" (page `3b85d94315658114ae17f1653876455d`) — the plumbing/state-machine doc, distinct from [[project-inc42-datalabs-dunning]] (the diagnostic numbers) and [[project-inc42-datalabs-winback]] (the business fix plan).

**Deliverables:**
- Google Sheet `1NCpTEzgEEtds0uCfqPNSS6aeFhOpKbgkL_F-cgtVPxg`, tab **"Dunning System"** — full detail, 15 columns (Ranjith transposed it himself to rows=cases/columns=fields), includes exact Razorpay status, full banner copy, FOMO device reasoning, and explicit Should-Happen/Should-NOT-Happen guardrails per case.
- Same sheet, tab **"Dunning - Simple"** — condensed 8-column version (Case, Razorpay Trigger, Access, Retries/Touches, Grace→Attempts, Banner, Guardrail, Status) for quick scanning.
- Artifact **"Dunning Decision Map"**: https://claude.ai/code/artifact/7ff69804-ddbb-4d8b-958b-3a85e7ba5b9c — a status-map legend table (every exact Razorpay trigger → which case it maps to) followed by one full card per case, each showing the access/retry/grace mapping as steps, a real in-app-banner mockup (not just text), and the guardrail. Went through 2 revisions: v1 was an abstract SVG flowchart that collapsed 8 cases into 3 tracks (too abstract, missing exact statuses); v2 (current) is the card-based status-map — see [[feedback-status-map-ui-treatment]] for why.

**The 8 cases and their exact Razorpay triggers:**
1. First payment (Day 7 trial→paid) — Transient: `GATEWAY_ERROR`
2. First payment — Dead mandate: token `initiated` (unconfirmed) → error `RECURRING_TOKEN_NOT_CONFIRMED`
3. Renewal — Dead mandate (existing payer): token `expired`/`rejected`/`cancelled` → `RECURRING_TOKEN_NOT_CONFIRMED`
4. Renewal — dies mid-recovery (edge case): `token.cancelled` webhook arriving while sub already ON-HOLD — stays on existing track, doesn't restart
5. Renewal — Transient (existing payer): `GATEWAY_ERROR`
6. Cancellation — External: `token.cancelled` webhook, sub was ACTIVE
7. Cancellation — Voluntary: not a Razorpay status — our own `POST /subscriptions/{id}/cancel-at-period-end` API call
8. Terminal: not a Razorpay status — our own auto-cancel cron or WCS's own end-date auto-transition

**Locked (confirmed by Ranjith, 25 Aug 2026):** needs-reauth grace period = 7 days (down from the doc's 15-day default), unified with a 15-day total attempts window (7 days of grace-period nudges + up to 8 more days of post-cutoff winback push) — applies to both first-payment and renewal dead-mandate cases (#2, #3). Also locked: on first-payment failure (any flavor), do NOT permit continued trial access — cut same day, no soft grace period riding the trial.

**Open / unresolved:**
- First-payment-Transient (case #1) access policy: doc/sheet currently says Cut, but Claude flagged this has no security rationale (mandate is confirmed, it's a pure funds issue) and recommended Live instead, matching Renewal-Transient (#5) — **Ranjith has not confirmed either way**.
- Renewal-Transient (case #5) retry count: explicitly left OPEN per Ranjith 25 Aug ("not sure, keep open") — doc's baseline is 2 notification touches (Day 0, Day 3), payment retry count unset.
- "Card blocked / permanently declined" is named in the source doc as a needs-reauth trigger but has no documented Razorpay error code.
- What happens when Transient-track retries exhaust at Day 7 (does it convert to needs-reauth? just stay suspended?) is not specified anywhere in the source doc — flagged as a real gap, not guessed at.

**How to apply:** this is the authoritative case-by-case reference for the Datalabs dunning/re-auth/winback build. Before making further changes to retry counts, grace periods, or banner copy, check this map (and the live sheet/artifact) first — don't re-derive from the raw Notion spec, which describes the mechanism but not these specific policy calls.
