---
name: nexloid-gtm-strategy
description: "Nexloid's locked go-to-market decisions as of Aug 2026 — positioning, market sequence, buyer model, pricing ladder, channels"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1d7fd985-d66e-401b-af2d-cf56be486f91
  modified: 2026-08-17T18:20:15.218Z
---

Go-to-market decisions for [[nexloid-product]], derived from the Aug 2026 research in [[nexloid-competitive-landscape]]. Full dossier lives at `/Users/thrillophilia/nexloid-launch-dossier.html` (standalone HTML, 14 sections, all sources linked).

**Build state at time of writing (Aug 2026):** site scrape + audit report working, GTM auto-install working. Solo founder, ₹1–3L budget, 6-month horizon, alongside the INC42 job.

## The core reframe
**Stop selling "cheaper than an agency." Sell "tracking you can prove is correct, forever."** The agency-replacement premise only holds at enterprise scale — the real floor is $10–35 on Fiverr and a $30/hr Upwork median. What nobody sells at any price is continuous, evidenced correctness, and that's a subscription rather than a project. Category claimed: **tracking assurance**, not "AI analytics setup" (already occupied by two funded competitors and commoditised by free MCP servers).

## Market sequence — UK first
- **Primary: UK.** 17,636 agencies = 1,470× the 12-customer target. Full USD-equivalent pricing. PECR gives the clearest B2B cold-email permission of any market. Working day = 1:30–9:30pm IST, the only large English market workable around a full-time job.
- **Parallel: Australia.** 8,373 digital agencies, fastest-growing (digital ad spend +12.7%/yr, Q1 2026 record A$4.9B +15.3%). Least contested. Work it before the INC42 day starts.
- **Month 4: US.** 114,014 agencies, ~$320B digital ad spend — 9× bigger, but the most saturated inbox market and where every competitor concentrates. Enter with a proven message.
- **India: run in parallel, priced in INR.** Revised after Ranjith confirmed GST, UPI and multi-currency billing are already solved — that removed 4 of 5 barriers.
- **LinkedIn only (no cold email):** Canada (CASL needs prior consent), EU/EEA (GDPR), Ireland, NZ.

**Why India needs a different price (the real mechanism):** Nexloid replaces analyst hours, so it's worth what the labour costs. GA4/GTM person ≈ $55/hr US, ~$38/hr UK, ~$10/hr India. At 2 hrs saved per client/month against $7.96/client, the return is 13.8× (US), 9.5× (UK), **2.5× (India)**. Fix with price, not exclusion: **₹4,999/mo Agency, ₹1,499/mo Solo** restores ~8.8×. (The earlier "4.4× share-of-revenue" argument was measuring the wrong thing — discard it.)
**Exception:** Indian agencies whose *clients* are Western bill in hard currency → quote them the USD price. Filter on whether published client logos are Western.

## Buyer model — three different businesses, not one
- **A · Agency is the customer** (agency pays, covers all their clients) → **do this now.** Every competitor ships an agency tier; agencies spend 7–10% of revenue on software, run ~12 subscriptions, and mark software up 15–50% or bundle it into retainers, so your cost can become their revenue.
- **B · Agency is the channel** (they resell to brands) → **month 4–6.** Partner-sourced customers churn 20–30% lower, close 46% faster, 40% higher AOV, up to 50% lower CAC. Build sub-accounts + white-label into the Agency tier from day one to enable it.
- **C · Brand direct subscription** → **never as primary.** SMB CAC is $200–700 against a $588 ACV; sub-$5K ACV median payback is 11 months; the benchmark's own answer for sub-$50/mo is PLG or referral — and this category has no inbound to power PLG.
- **Cold outbound goes to agencies only.** Brands only for the $299 one-time Rescue, and only warm (network, referrals, free scanner).

**ICP filter that matters most:** target **retainer-based** agencies (5–50 clients, 2–30 staff), where tracking is unbilled cost and removing it is pure margin. Hourly/project-billing shops are *cannibalised* by this — for them the pitch must be "more clients, same team," or skip them. Client type: lead-gen SMB (home services, dental/med, legal, education, local B2B, small SaaS) — **not Shopify**, that's solved and defended.

## Pricing ladder (anchored to competitors' published prices, not margin targets)
Value metric = **connected property per month**. Never per-audit (races to $49), never per-event (unpredictable).
- **Scan** — $0, no login, no OAuth. Matches GAfix/NiceLookingData free tiers, and no-login beats both.
- **Solo** — $49/mo, 3 properties. Anchored to NiceLookingData Pro $49 — same price, but you deploy where they only recommend.
- **Agency** — $199/mo, 25 properties, white-label, sub-accounts. Anchored to NiceLookingData Agency $199 / GA4 Auditor $999 yr.
- **Scale** — $499/mo, 100 properties, API. Deliberately under Trackingplan $999 and ObservePoint $599.
- **Tracking Rescue** — **$299 one-time**, the cash-flow on-ramp. GAfix charges $199–499 for the same thing delivered by humans; a human audit alone is $1,500–3,000. **Lead with this for the first 90 days** — it closes on a demo where a subscription needs trust you haven't earned.
- Annual 25% off (Analyzify precedent). Founding 20 get a lifetime price lock for a named case study.

**Six-month target: 12 paying customers = 4 Agency + 8 Solo ≈ $1,188/mo ≈ ₹1L MRR**, plus ~10 Rescues.

## Channels, ranked
1. **Cold email where the personalisation IS the product output** — pre-run a scan on the prospect's own client site and name a specific broken event in line one. No competitor can do this at volume; their tools sit behind OAuth, yours reads public pages. ~110 emails/week.
2. Founder-led LinkedIn + Measure Slack / r/GoogleTagManager / r/analytics.
3. Free no-login scanner (shareable permanent report URLs) — outbound weapon + ranking asset.
4. Error-library pages (one per check, ~150 pages) + an honest comparison page naming competitors and real prices → built for **LLM citation and credibility, not lead volume** (the traffic isn't there).
5. Co-marketing with **Stape, Analytics Mania, MeasureSchool** — 162K/mo of the exact audience, all complementary.
6. Directories: G2, Capterra, AlternativeTo, Product Hunt.
7. **Paid ads: don't.** Disproven in-category — GAfix runs 77.7% paid with a 90% bounce rate.

Headline shipped: **"The tracking audit that ships the fix."** Cold-email/ads hook: "Your ad budget is bidding on broken data." Agency page: "Tracking your clients can't argue with." Never claim a precision accuracy figure, never say "replaces your analytics agency" (agencies are the buyer), never lead with "AI-powered."

**How to apply:** these are decided, not open. Revisit them only against new evidence, and check [[nexloid-open-questions]] first — several of these rest on assumptions that aren't validated yet.
