---
name: project-inc42-brief-card-corpus-analysis
description: "Corpus analysis of 809 Inc42 articles (Jun-Aug 2026) answering what the home brief card can actually show — summary is the only 93%-covered field, bullet 2 is the payload, and 2 of 3 dummy stat tiles are uncomputable"
metadata:
  node_type: memory
  type: project
---

Done 27-28 Aug 2026. Ranjith asked how the **article summary section** should be used on the
Figma home brief card (`Inc42-App-2026`, node `4163-4056`), given what Inc42 actually publishes.
Target confirmed by Ranjith as the **home entry card**, not the story cards inside the brief.

This is the concrete, structural answer to the "make it more impactful" stalemate logged in
[[project-inc42-app-brief-gratification-redesign]] — that memory records Ranjith's action to
give Satya data-point direction instead of subjective feedback. This analysis is that direction.

## Method (reproducible)
- **809 articles, 21 Jun – 20 Aug 2026** from `~/Downloads/42_posts (1).csv`
- Enriched via the **WordPress REST API** — `https://inc42.com/wp-json/wp/v2/posts?include=<ids>`
  works unauthenticated, batches of 50, returns `meta` and `acf`. Rate-limits with **429 at
  ~6 concurrent**; 3 threads + 1.2s delay is safe.
- Summary text is **not in the REST API**. It must be scraped from the article page:
  `<div class="single-post-summary">` containing `<span>SUMMARY</span>` then `<p>` bullets.
  Sits at ~byte 127-130K of the page.

## The findings

### Field coverage — the point of the whole exercise
| Field | Coverage | Implication |
|---|---|---|
| **`summary` (3 bullets)** | **93%** | The most reliable content asset Inc42 has. Not used on the card at all. |
| `development_tag` | 85% | Better row eyebrow than sector |
| `companies` | 73% | Enough for the watchlist hook |
| `sector` | **58%** | The card's current eyebrow — blanks on 42% of stories |

### Summary structure (n=699 with a summary; 664 are exactly 3 bullets, ~23 words each)
| | b1 | b2 | b3 |
|---|---|---|---|
| money figure | 48% | 24% | 34% |
| any number | 66% | 39% | 61% |
| forward-looking / "so what" | 8% | **27%** | 19% |

- **Bullet 1 duplicates the headline** — median 50% of headline words reappear in it; only 11%
  add a number the headline lacks. Headline + b1 wastes the card's best line.
- **Bullet 2 is the only line a headline can't carry** (the interpretation bullet).
- **56% of articles have no "so what" in any bullet.** Root cause is visible in the CMS:
  **`meta.user_needs` = "Inform Me" on 715/750 (95%)**; only 26 "Give Me Perspective".
  Inc42 publishes news-of-record — a why-it-matters line cannot be promised per story.
- Other live CMS fields found: `push_notification` (written on only 20% of articles, median
  133 chars), `newsletter_snippets` (0.7%), `acf.sentiment__tonality`.

### The dummy stat strip fails on real data (44 weekdays tested)
| Dummy tile | Reality | Verdict |
|---|---|---|
| `₹2,900 Cr moved today` | median **₹239 Cr**, **₹0 on 14% of weekdays**, p90 ₹6,557 | breaks |
| `3 IPO filings` | median **0**; **zero on 59% of weekdays** | dead |
| `6 sectors` | median 6, never zero | computable, no user value |

Tiles that never hit zero: distinct companies (median 13), story types (median 6),
biggest single transaction (median ₹3,371 Cr).

## ⚠️ Trap: aggregate numbers poison any "biggest number today" tile
First implementation picked **TAM and tracker numbers, not money that moved** — top pick
₹34.5 L Cr (*cumulative unicorn valuation*), then ₹26 L Cr (*a 2030 government export target*),
₹15 L Cr (*cumulative mcap*). **11 of the top 12 were false.** Any money-extraction over this
corpus must exclude: market-size/TAM language, cumulative/combined trackers, multi-company
roundups ("Startups Raised $1.1 Bn This Week", "Top 10 … of H1"), and income-statement figures
(revenue/loss/profit). After filtering, picks are genuine: Amazon $13 Bn, Accel Fund IX $550 Mn,
CRED $900 Mn. Residual issue: still can't separate **prospective** (planned IPO size) from
**completed** (actual raise).

## 🔴 The biggest defect found — and it is NOT a summary problem
Backtesting exposed that the **hero tile's company appears in the three teaser rows only 28%
of the time**, because rows are recency-sorted. The card announces "₹3,000 Cr · Navi deal"
then shows three unrelated D2C panel recaps. **This is a ranking problem.** The ranking formula
is LOCKED elsewhere ([[project-inc42-content-personalization]]) so it was deliberately not
changed — but no summary treatment fixes a card that contradicts itself.

## ✅ Correction — the "weekend collapse" finding was wrong for the brief
Raw publishing does collapse: **Sun avg 1.6 articles/day**, Sat 8.2, vs ~17 Tue-Thu. The initial
conclusion was that the Sunday card can't promise "~5 MIN". **That is wrong.**
[[project-inc42-content-personalization]] records the LOCKED schedule: **Sunday = Weekly Recap
covering Mon 7AM → Sat 7AM**, and **Monday = Weekend brief covering Sat+Sun**. Neither Sunday
nor Monday is built from that day's articles, so neither is thin. The thin-day state is a much
smaller edge case than the raw publishing curve suggests.

Also unreconciled: this CSV's `sector` is **58% populated**, but
[[project-inc42-content-personalization]] records **86% missing** on BigQuery's
`Company_Industries`. Different fields — do not quote them interchangeably.

## Artefacts
`~/ClaudeDocs/inc42/brief-card/` — `render_card.py` (rerunnable renderer + tile/bullet logic),
`cards.txt` (all 61 days rendered), `backtest.csv` (per-day audit), `summaries.json` (750
scraped summaries), `README.md`. Plan: `~/.claude/plans/eager-enchanting-clover.md`.

**Why:** the card had been designed on dummy data nobody had checked against the corpus, and
two of its three stat tiles are literally uncomputable on most real days. The summary — the one
field with 93% coverage — was unused.

**How to apply:** lead with the coverage table when anyone proposes card furniture keyed on
`sector`. Before promising any aggregate money tile, apply the aggregate/roundup/statement
filters or it will surface a TAM number. And state plainly that row **ordering**, not the
summary, is the card's real defect. Related: [[project-inc42-app-v2-scope-full]],
[[project-inc42-brief-images]], [[project-inc42-app-behaviour]].
