---
name: project-inc42-brief-companies-mention-types
description: "Companies in today's brief (6 Sep 2026) — 90-day mention-type classification of 1,179 articles: what kind of company news Inc42 publishes, per-weekday counts, and which DataLabs field each type can show"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4f897cf8-f958-4498-b0c8-58aee870b09f
  modified: 2026-09-06T11:12:07.001Z
---

**Done 6 Sep 2026.** Ranjith wants the Brief page's "Companies in today's brief" section to show a
data point matched to *why* the company is in the news (layoff → headcount, funding → total
funding). Before designing, he asked for a 90-day categorisation of company mentions.

**Method:** reused `~/ClaudeDocs/inc42/brief-data/corpus90.json` (1,179 articles, 6 Jun – 4 Sep
2026, 65 weekdays). Headline-rule classifier into 18 mention types; 93% agreement with the CMS
`development_type` where the CMS is specific. Every row with type + URL in
`~/ClaudeDocs/inc42/brief-data/mention_types_90d.csv`; pivots in
`companies-in-brief-mention-types.md` (same folder).

## What the corpus says
- **Company tagging: 73% real slug, 14% the placeholder `tbd` (166 rows), 13% blank.** `tbd`
  hits 18 funding, 14 product and 14 analysis stories — CMS hygiene issue, not a design one.
- **Median weekday: 11 company-tagged stories, 8 with a data-backable type, min 2, never 0.**
  ≥5 data-backable on 58 of 65 weekdays. 71.5% of tagged stories are data-backable.
- **Mix:** Funding 18% (60/65 weekdays, median 3/day) · Analysis 15% · Financials 10% (58% of
  weekdays) · IPO 8.5% (77%) · Product/launch 6% · Legal action 5% · M&A 4% · Stake sale 3% ·
  Stock move 3% · Leadership 3% · **Layoffs 0.8% (9 stories, 5 weekdays)** · Shutdown 0.7%.
- **Stage determines the field:** Funding skews Early+Growth (145/197) where DataLabs financials
  are thinnest; Financials skews Listed (68/111); IPO skews Late Stage (75/94); Stake sale and
  Stock move are ~all Listed → need market-cap data, not the startup profile.
- **CMS `development_type` alone cannot route:** "Business Updates" (255) hides 64 product, 33
  stake-sale, 33 stock-move, 22 funding, 16 policy stories. "Controversies" (91) is 30 policy,
  44 legal action. A mention-type classifier (rules or LLM at publish) is required.
- **Continuity:** 120 of 440 companies have ≥2 mentions in 90 days; 109 span ≥2 types.

**Why:** the section was going to be built from `development_type`, which would misroute ~200
of 1,179 stories, and the layoff→headcount example that motivated it is a fortnightly event.

**How to apply:** design the section around Funding / Financials / IPO first (they cover 92%,
58%, 77% of weekdays); treat Layoffs, Shutdown, Leadership as rare states that must degrade to
"profile only". Label the DataLabs FY when showing financials — the article is usually a newer
period. See [[project-inc42-brief-impact-continuity]] (DataLabs confirmed fields),
[[project-inc42-brief-card-corpus-analysis]], [[project-inc42-content-personalization]].
