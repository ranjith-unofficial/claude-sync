---
name: project-inc42-brief-copy-variants
description: "Brief card title variants + push copy generated from FULL article text (12 Sep 2026) — 61 variants over 15 stories, each with a verified answer location; Ranjith rejected headline+summary generation"
metadata:
  node_type: memory
  type: project
---

**Done 12 Sep 2026.** Ranjith asked for curiosity-led Brief card title variants and push copy so the
same story can be positioned differently per reader interest (startup / investment / founder /
company / industry), with the **top three hooks shown on the Brief entry card**.

## The correction that defines the method
The first pass generated copy from **headline + the 3-bullet CMS summary**. Ranjith rejected it:
*"the title itself is very limited … first understand the article content, then generate a question
and see if that question will be answered by the title and then the article … not the otherwise."*
He also rejected generic pushes and pushes that restate the title.

**Locked method:** pull the **full article body** first, read it end to end, pick the hook from what
the body actually contains, then verify the question is answered and record *where*. If a question
has no answer in the text, it does not get written.

## What that changed, measured on the same 15 stories
- **49 of 61 variants are answered only in the body** — a headline+summary generator could not have
  written them. Only 12 of 61 were derivable from headline + summary.
- **On full text every story supported 4+ angles (15/15). On headline+summary only 8/15 did.**
- **9 of 15 stories have their sharpest hook past the halfway mark** (Ultraviolette's 583 August
  units vs a 2.5 Lakh-capacity factory; Rapido's ₹30-delivery/₹25-driver worked example;
  EaseMyTrip's pledge total being *unchanged*; OpenAI's August sandbox escape onto Hugging Face).
- CMS `push_notification` exists on only **5 of 15 (33%)**, and **0 of those 5 open a curiosity gap**
  — all five restate summary bullet 1. Matches the 20% write-rate in
  [[project-inc42-brief-card-corpus-analysis]].
- Median article 539 words, so there is no cost argument for generating from the headline.

## Deliverable
Tab **"Brief Copy Variants (12 Sep)"** (gid `1798377423`) in the **Test** workbook
`1NCpTEzgEEtds0uCfqPNSS6aeFhOpKbgkL_F-cgtVPxg` — see [[reference-inc42-open-ledger-sheet]] for the
same workbook. Four sections: variants (one row each, with "Where the article answers it" + the
answer), push per story (title/body + char counts + why it is not the headline), top-3 entry-card
hooks for 6 reader interests, and the findings above.
Local: `~/ClaudeDocs/inc42/brief-copy/` (v2 TSV, full article bodies JSON, source articles JSON).

**Source data:** 15 articles in the real 12 Sep brief window (11 Sep 07:00 → 12 Sep 07:00 IST),
WP REST API `?include=<ids>&_fields=id,date,link,title,content,acf` for full bodies — unauthenticated,
one call for all 15.

**Status:** unreviewed by Ranjith as of 12 Sep.

**Why:** the generator's input, not its prompt, was the binding constraint on how interesting the
copy could be.

**How to apply:** never generate Brief or push copy from headline + summary. Pull the body, and keep
the "where is this answered" column — it is the check that stops a curiosity hook becoming clickbait.
Related: [[project-inc42-content-personalization]], [[project-inc42-brief-impact-continuity]],
[[project-inc42-app-feedback-rating-system]], [[feedback-design-review-ranjith]].
