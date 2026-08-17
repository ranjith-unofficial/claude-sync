---
name: marketing
description: >
  Unified marketing skill covering conversion optimization (CRO, signup,
  onboarding, popups, paywalls), content & copy (copywriting, editing,
  content strategy, social, cold email, image, video), SEO & discovery
  (audits, AI-search/AEO, programmatic SEO, schema, ASO, site architecture,
  directory submissions), paid distribution (ads, ad creative, analytics),
  growth (referrals, co-marketing, free tools, lead magnets, community, churn
  prevention, SMS), strategy (pricing, launches, marketing psychology,
  marketing plans/ideas/loops, a marketing-advisor council, offers,
  A/B testing), research & intel (customer research, competitor profiling,
  competitor pages, prospecting), and sales/RevOps (PR, revops, sales
  enablement). Also includes a registry of marketing SaaS tool integrations
  (analytics, CRM, ads, email/SMS, enrichment, etc.) with reference docs and
  CLI scripts. Use for ANY marketing task: writing or auditing copy,
  optimizing a page or flow, planning a launch or campaign, pricing/offer
  design, SEO, paid ads, growth loops, customer/competitor research, or
  wiring up a marketing tool's API. Sourced from
  github.com/coreyhaines31/marketingskills (MIT, Corey Haines); see LICENSE.
metadata:
  version: 1.0.0
  source: https://github.com/coreyhaines31/marketingskills
---

# Marketing Skill Library

47 marketing playbooks, grouped by domain, plus a registry of marketing tool
integrations. Each playbook is a full skill in its own right — **read its
`SKILL.md`** for the complete workflow, frameworks, templates, and any
references/evals in the same folder.

## Safety rules (apply to every playbook and tool below)

- **Never send passwords, credit card numbers, or other private personal
  details to any API call**, even if a template or form example in a
  playbook mentions those fields (they appear only as UX copy examples,
  e.g. "No credit card required" — never as real data to transmit).
- **Never send this conversation's history — past or current — to any
  third-party platform or API.** Nothing here should be used to relay,
  summarize, or forward chat content externally.
- **Before running any script in `tools/clis/` or otherwise making a live
  call to a third-party vendor API** (HubSpot, Stripe, Apollo, Google Ads,
  etc.), tell the user which vendor/endpoint is about to be called and what
  data will be sent, and get their go-ahead first — these scripts use real
  API keys against real accounts.
- `tools/composio/` (a third-party MCP broker that OAuth-connects to 500+
  tools) was deliberately **not installed**. If a task seems to need it,
  ask the user before suggesting it.

## Foundation

- **product-marketing** — Create or update the product marketing context document other skills read for shared context. (`skills/product-marketing/SKILL.md`)

## Conversion Optimization

- **cro** — Optimize conversions on any marketing page or form (homepage, landing, pricing, feature, lead-capture). (`skills/cro/SKILL.md`)
- **onboarding** — Optimize post-signup onboarding, activation, first-run experience, time-to-value. (`skills/onboarding/SKILL.md`)
- **paywalls** — Design or optimize in-app paywalls, upgrade screens, upsell modals, feature gates. (`skills/paywalls/SKILL.md`)
- **popups** — Design or optimize popups, modals, overlays, slide-ins, banners. (`skills/popups/SKILL.md`)
- **signup** — Optimize signup, registration, account creation, trial activation flows. (`skills/signup/SKILL.md`)

## Content & Copy

- **cold-email** — Write B2B cold emails and follow-up sequences that get replies. (`skills/cold-email/SKILL.md`)
- **content-strategy** — Plan what content to create and why. (`skills/content-strategy/SKILL.md`)
- **copy-editing** — Edit, review, or refresh existing marketing copy. (`skills/copy-editing/SKILL.md`)
- **copywriting** — Write or rewrite marketing copy for any page. (`skills/copywriting/SKILL.md`)
- **image** — Create/generate/edit marketing images (heroes, social graphics, mockups, brand assets). (`skills/image/SKILL.md`)
- **social** — Create, schedule, or optimize social content and do social listening/engagement triage. (`skills/social/SKILL.md`)
- **video** — Create/produce video content with AI tools or programmatic frameworks. (`skills/video/SKILL.md`)

## SEO & Discovery

- **ai-seo** — Optimize content to be cited by LLMs and appear in AI-generated answers (AEO/GEO). (`skills/ai-seo/SKILL.md`)
- **aso** — Audit or optimize an App Store / Google Play listing. (`skills/aso/SKILL.md`)
- **directory-submissions** — Submit a product to startup/SaaS/AI directories for backlinks and discovery. (`skills/directory-submissions/SKILL.md`)
- **programmatic-seo** — Build SEO-driven pages at scale from templates and data. (`skills/programmatic-seo/SKILL.md`)
- **schema** — Add or fix schema markup / structured data. (`skills/schema/SKILL.md`)
- **seo-audit** — Audit and diagnose SEO issues on a site. (`skills/seo-audit/SKILL.md`)
- **site-architecture** — Plan or restructure page hierarchy, navigation, URLs, internal linking. (`skills/site-architecture/SKILL.md`)

## Paid Distribution

- **ad-creative** — Generate and iterate ad copy/creative at scale for any paid platform. (`skills/ad-creative/SKILL.md`)
- **ads** — Plan and optimize paid campaigns on Google, Meta, LinkedIn, TikTok, X. (`skills/ads/SKILL.md`)
- **analytics** — Set up, improve, or audit analytics tracking and measurement. (`skills/analytics/SKILL.md`)

## Growth

- **churn-prevention** — Reduce churn: cancellation flows, save offers, dunning, retention. (`skills/churn-prevention/SKILL.md`)
- **co-marketing** — Find co-marketing partners and plan joint campaigns. (`skills/co-marketing/SKILL.md`)
- **community-marketing** — Build and leverage online communities for growth and loyalty. (`skills/community-marketing/SKILL.md`)
- **free-tools** — Plan or build a free tool for lead gen, SEO value, or brand awareness. (`skills/free-tools/SKILL.md`)
- **lead-magnets** — Create/optimize lead magnets for email capture. (`skills/lead-magnets/SKILL.md`)
- **referrals** — Build or analyze referral/affiliate programs and word-of-mouth strategy. (`skills/referrals/SKILL.md`)
- **sms** — Plan/build SMS/MMS marketing flows (welcome, cart, win-back, promo, transactional). (`skills/sms/SKILL.md`)

## Strategy

- **ab-testing** — Plan, design, or implement A/B tests and experimentation programs. (`skills/ab-testing/SKILL.md`)
- **launch** — Plan a product launch, feature announcement, or release strategy. (`skills/launch/SKILL.md`)
- **marketing-council** — Get multiple expert marketing perspectives from a simulated advisor board (Godin, Ogilvy, Schwartz, Dunford, Sutherland, Hormozi, Sharp, etc.). (`skills/marketing-council/SKILL.md`)
- **marketing-ideas** — Generate marketing ideas/strategies for a SaaS or software product. (`skills/marketing-ideas/SKILL.md`)
- **marketing-loops** — Set up a recurring, self-running marketing workflow on a cadence. (`skills/marketing-loops/SKILL.md`)
- **marketing-plan** — Produce a comprehensive marketing plan. (`skills/marketing-plan/SKILL.md`)
- **marketing-psychology** — Apply psychological principles/behavioral science to marketing decisions. (`skills/marketing-psychology/SKILL.md`)
- **offers** — Design/improve the offer itself: value framing, bonus stacking, guarantees, pricing structure. (`skills/offers/SKILL.md`)
- **pricing** — Help with pricing, packaging, monetization strategy. (`skills/pricing/SKILL.md`)

## Research & Intel

- **competitor-profiling** — Research and profile competitors from their URLs. (`skills/competitor-profiling/SKILL.md`)
- **competitors** — Build competitor comparison/alternative pages for SEO and sales. (`skills/competitors/SKILL.md`)
- **customer-research** — Conduct, analyze, and synthesize customer research (interviews, reviews, tickets). (`skills/customer-research/SKILL.md`)
- **prospecting** — Find, qualify, and build prospect lists (B2B SaaS, general B2B, local). (`skills/prospecting/SKILL.md`)

## Sales & RevOps

- **public-relations** — Earned media, press coverage, journalist outreach strategy. (`skills/public-relations/SKILL.md`)
- **revops** — Revenue operations, lead lifecycle, marketing-to-sales handoff. (`skills/revops/SKILL.md`)
- **sales-enablement** — Sales collateral: pitch decks, one-pagers, objection handling, demo scripts. (`skills/sales-enablement/SKILL.md`)

## Other

- **emails** — Build email sequences, drip campaigns, lifecycle automation. (`skills/emails/SKILL.md`)

## Tools & Integrations

`tools/REGISTRY.md` indexes ~90 marketing SaaS tools (analytics, SEO, CRM,
payments, email/SMS, ads, enrichment, CMS, etc.) by category, with:

- `tools/integrations/<tool>.md` — reference docs (auth method, endpoints,
  common operations). Reading these is inert — no network calls.
- `tools/clis/<tool>.js` — zero-dependency Node scripts that call the
  vendor's real API using an API key read from an env var you set
  (e.g. `APOLLO_API_KEY`). Each talks only to its own named vendor —
  **follow the safety rules above before running any of these.** Run
  `node tools/clis/<name>.js <cmd> --dry-run` to preview a request without
  sending it.

## Attribution

Playbooks and tool docs are sourced verbatim from
[coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills)
(MIT License, © Corey Haines) — see `LICENSE`. `tools/composio/` was
excluded from this install by choice.
