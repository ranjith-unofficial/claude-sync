---
name: project-inc42-brief-impact-continuity
description: Brief page impact score and continuity personalisation (5 Sep 2026) — validated on 1,179 articles; the ranking formula has no story-level importance signal
metadata:
  type: project
---

**The finding (5 Sep 2026):** the personalised-brief ranking formula has **no story-level
importance signal**. `Pop` is a category constant — every `Startup IPO` article scores 0.116
whether it is Zepto's ₹8,010 Cr filing or a seed-stage company saying it may list in 12–18 months.
Same (topic, sector) = identical score, separated only by recency. That is why no design has felt
prominent: there was nothing to make prominent with. Raised by Ranjith as "how do we prioritize
any news, how do we show impactfulness".

**Impact score, built and validated on 1,179 articles (6 Jun – 4 Sep):**
`0.40·event + 0.25·company_stage + 0.20·magnitude + 0.15·editorial`
- event = `development_type` (85% coverage); company_stage = `company_type` (85%, unused until now);
  magnitude = ₹/$ parsed from headline, log-scaled (47%); editorial = Exclusive/Investigative,
  In-Depth, or `shelf_life` > 3 days.
- **Clear hero on 57% of weekdays; no hero on 25%** (layout must change, not fake one).
- Reorders vs recency on 91% of days. Ranjith's IPO + big-company example occurs on 52% of days.

**Continuity beats category for personalisation.** 98% of weekdays contain a company covered in
the prior 30 days (median 3 of 8, ≥3 on 75%). Editorial already tags `Follow Up` (6%) and
`Series` (11%) — 94% of weekdays carry one. "The 4th Zepto story you have seen this month" reads
as personal; "you follow Ecommerce" does not.

**Personalisation hides big news:** a ≥0.62-impact story is cut from the top 8 on 58% of days
(Deals+Fintech), 48% (Ecom+IPO), 72% (AI-only) — justifies a `Big today, not in your brief` section.

**Also established:** `sentiment__tonality` is "Positive" on 1,178/1,181 — a default, unusable for
a positive/negative day signal; tone must be derived from development type. The *Inc42 Daily Brief*
newsletter title exists on 62/65 weekdays (~08:00) and solves Utkarsh's "static title" objection —
needs the CMS draft field exposed at 07:00.

Row L in draft file `dAsaTgNj0xh25w2OGaurZo` (y=99600) builds it on three real days.
Spec: `~/ClaudeDocs/inc42/brief-entry-coverage-spec.md`.
See [[project-inc42-brief-entry-coverage]], [[project-inc42-content-personalization]].
