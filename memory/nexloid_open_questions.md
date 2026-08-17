---
name: nexloid-open-questions
description: "Nexloid's unvalidated assumptions, weak sources and unresearched gaps as of Aug 2026 — what must be settled before the strategy is trustworthy"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1d7fd985-d66e-401b-af2d-cf56be486f91
  modified: 2026-08-17T18:20:44.339Z
---

Self-audit of the Aug 2026 Nexloid strategy work ([[nexloid-gtm-strategy]], [[nexloid-competitive-landscape]]). Ranjith asked for every doubt to be surfaced so he could sort them. **None of these were resolved as of 17 Aug 2026** — check status before relying on the strategy.

## The five to settle first
1. **Google OAuth scope classification** for `tagmanager.edit.containers` / `tagmanager.publish`. If **sensitive**: verified domain + privacy policy + demo video + justification, ~10 days after a complete submission. If **restricted**: also an annual third-party **CASA** security assessment, $540 (automated scan) to $5,000+ (pentest), paid by Nexloid. **Unknown which applies — it changes both cost and launch date.** Start verification early; it runs in parallel.
2. **Real hours-saved per client per month.** The whole ROI model assumes **2 hours** — a number with no evidence behind it. At 0.5 hrs the US return falls from 13.8× to 3.5× and the India case dies; at 6 hrs Nexloid is underpriced everywhere. Stopwatch it on the design partners.
3. **False-positive rate of the audit.** The positioning is "evidence you can defend." Nobody has assessed whether an LLM reliably reads an arbitrary site's dataLayer. Evidence that's sometimes wrong is worse than none.
4. **Independent verification of "48% of sites have a Consent Mode misconfiguration" and "20–30% of ad budget distorted."** Both trace to a *single* marketing agency's blog with an interest in the number being alarming. They carry the homepage copy and the cold-email hook. Corroborate or stop using them.
5. **Ten customer conversations before the pricing page ships** — not to sell, but to capture how buyers describe the problem in their own words.

## Other unvalidated assumptions
- **"An agency connects ~25 properties."** Honest answer is probably 3–8 in month one. The $199 tier economics depend on it.
- **"Pre-run scans lift reply rates to 7–9%."** An extrapolation from "top quartile is 7–12%," not measured. Plan on the 3.4% baseline.
- **"10–12 focused hours a week is enough."** Asserted, never tracked.
- **No human has validated any price.** Every number is anchored to a competitor's published price, not to stated willingness to pay.

## Sources that are weak (use with care)
- **"$2.81M / $1.93M ad spend per agency"** — weakest metric produced; it's national ad spend ÷ agency count, and most of that money never touches the long tail. **Drop it rather than defend it.**
- **114,014 US / 17,636 UK agency counts** — reliable as counts, but the classification sweeps in creative/PR/media firms that never touch GTM. Addressable subset plausibly 10–30%.
- **Similarweb traffic estimates** — unreliable below ~50K visits; visible bot/proxy noise. Direction believable, figures possibly off 2–5×.
- **Cold-email and partner-led-growth benchmarks** — all published by vendors selling those exact tools.
- **"How many sites run GTM"** — trackers disagree wildly (w3techs says 45.5% of all sites; active-domain crawlers say 10.58M; BuiltWith secondary reports range 31.4M–64.2M and contradict themselves 2.6–3.5× on the same country). **Don't quote a single number.** Only agency counts should drive decisions.

## Never researched
- **Voice of customer — entirely absent.** No G2/Capterra/Reddit reviews of any competitor were read. All copy is built from statistics rather than buyers' language. Most fixable gap.
- **Liability** when a deployment breaks a client's site or corrupts consent config — terms, indemnity, insurance. Intersects with GDPR and DPDP.
- **Agency–client contracts** that bar third-party access to client systems (a harder objection than trust).
- **Server-side tracking** — fastest-growing segment (sGTM domains 482 → 17,239 in a year, 35×). Nexloid doesn't do it; **both funded competitors do.**
- Whether Nexloid can actually **fix Consent Mode** (48% of sites broken; plausibly the highest-value fix).
- **Support load** — 12 customers × 25 properties = 300 production containers, solo, alongside a full-time job.
- Category-specific **churn** (tracking is project-shaped — "fix it and leave" — may churn far faster than general SMB SaaS).
- **GA4 Admin API quotas** (GTM's were checked: 10,000 req/day and 0.25 QPS **per Cloud project**, not per customer — a real scaling wall).
- **Trademark and domain** for "Nexloid."
- **Seasonality** — agency budgets freeze in Q4, release in Q1. The 6-month plan has no timing awareness.
- Competitor **funding size and runway**; anything past month 6.

## Strongest arguments against the strategy
- **This cannibalises some agencies' revenue.** If an agency bills for GA4/GTM setup, turning 4 billable hours into 15 minutes is a threat, not a gift. Fix = target **retainer-based** agencies only.
- **"Tracking assurance" is an invented category.** Nobody searches for it or budgets for it, and the traffic data shows no existing demand to redirect — so this is want-creation, which is slower than the dossier's tone implies.
- **Solo against two funded teams in a category with no pull.** Kill signal: if outbound can't beat a 2% reply rate after 300 sends, this is a feature rather than a company — better to learn that in month three than month twelve.

**How to apply:** treat [[nexloid-gtm-strategy]] as provisional on these. When Ranjith reports back on any of them, update this file and re-derive whatever depended on it — especially pricing, which hangs almost entirely on the hours-saved number.
