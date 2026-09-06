# Home brief card — replace dummy stats with what the corpus can actually carry

## Context

The Figma home brief card (`Inc42-App-2026`, node `4163-4056`) is populated with dummy data:
a stat strip (`₹2,900 Cr moved today` / `3 IPO filings` / `6 sectors`), three teaser rows
labelled by sector, and `+ 5 more stories inside · ~5 MIN`.

The question: with the kind of articles Inc42 actually publishes, how should the summary
section of this card work?

I analysed the real corpus — 809 articles, 21 Jun → 20 Aug 2026 (61 days) from
`~/Downloads/42_posts (1).csv`, enriched with WP REST metadata and the live
`<div class="single-post-summary">` block scraped from 750 article pages.

**Two of the three dummy tiles cannot be computed on most real days, and the teaser row's
sector label is missing on 42% of articles.** Meanwhile the 3-bullet summary — the one asset
with 93% coverage — is not used on the card at all.

## Evidence

### Field coverage (what the card can rely on)

| Field | Coverage | Verdict |
|---|---|---|
| `summary` (3 bullets) | **93%** | Most reliable asset Inc42 has. Currently unused on the card. |
| `development_tag` | 85% | Good enough for the row eyebrow |
| `companies` | 73% | Good enough for the watchlist tie-in |
| `sector` | **58%** | Too thin — the current eyebrow blanks on 42% of stories |

### The stat strip, tested over 44 weekdays

| Tile | Real distribution | Verdict |
|---|---|---|
| `₹2,900 Cr moved today` (funding only) | median **₹239 Cr**, p90 ₹6,557 Cr, **₹0 on 14% of weekdays** | Breaks |
| `₹X Cr` (any money in headlines) | median ₹5,541 Cr, never zero | Survives, but conflates funding with block deals / IPO size — mislabelled as "moved" |
| `3 IPO filings` | median **0**, **zero on 59% of weekdays** | Dead — kill |
| `6 sectors` | median 6, never zero | Computable but undercounts (58% coverage) and carries no user value |

Tiles that never hit zero across all 44 weekdays: **# distinct companies** (median 13, p10 8),
**# story types** (median 6, p10 4), **biggest single figure of the day** (median ₹3,371 Cr, p10 ₹180 Cr),
**# funding rounds** (median 2, but zero on 9% of days).

### Summary structure (n = 699 with a summary; 664 have exactly 3 bullets)

| | Bullet 1 | Bullet 2 | Bullet 3 |
|---|---|---|---|
| Carries a money figure | 48% | 24% | 34% |
| Carries any number | 66% | 39% | 61% |
| Forward-looking / "so what" language | 8% | **27%** | 19% |
| Median words | 23 | 24 | 24 |

- **Bullet 1 duplicates the headline.** Median 50% of headline words reappear in it; only 11%
  add a number the headline lacks. Rendering headline + bullet 1 on the card spends the most
  valuable line on something the user already read in push and the newsletter.
- **Bullet 2 is the only line a headline can never carry** — it is the interpretation bullet:
  lowest number density, 3.4× the forward-looking language of bullet 1.
- **But 56% of articles have no "so what" in any bullet.** Cause is visible in the CMS:
  `meta.user_needs` is `"Inform Me"` on 715/750 articles (95%); only 26 are `"Give Me Perspective"`.
  Inc42 publishes news-of-record. A "why it matters" line cannot be promised on every story.

### Weekend collapse

| | Mon | Tue | Wed | Thu | Fri | Sat | **Sun** |
|---|---|---|---|---|---|---|---|
| Avg articles | 14.8 | 17.7 | 18.6 | 17.1 | 14.5 | 8.2 | **1.6** |

`+ 5 more stories inside · ~5 MIN` is false every Sunday (avg 1.6 stories, min 1) and most
Saturdays. The card has no designed state for this.

## Recommendation

### 1. Rebuild the stat strip around figures that survive a bad day

Replace the three fixed tiles with:

| Slot | Content | Why |
|---|---|---|
| 1 | **Biggest number of the day**, attributed — `₹9,422 Cr · Shiprocket mcap` | Never zero (p10 ₹180 Cr). A story, not an aggregate — it teases rather than summarises. |
| 2 | **N funding rounds** with ₹ total, *shown only when N ≥ 1* | Honest label. Suppressed on the 9% of days with none, rather than rendering ₹0. |
| 3 | **N companies in the news · M you track** | Never zero (p10 8). Carries the watchlist hook already in the design ("2 you track"). |

Drop `IPO filings` (zero on 59% of weekdays) and `sectors` (vanity, 58% coverage).

### 2. Switch the teaser-row eyebrow from `sector` to `development_tag`

58% → 85% coverage. `FUNDING`, `IPO`, `FINANCIALS`, `POLICY` are also more legible to a reader
than `CONSUMER SERVICES`. Pair with the company name from `companies` where present (73%).

### 3. Put **bullet 2**, not bullet 1, under the headline

This is the core change. One clipped line per teaser row, ~12 words.

Selection order at render time:
1. Bullet 2 if it matches the forward-looking pattern (`could|would|signals|marks|comes as|amid|positions|expects|set a precedent|…`)
2. Else the bullet with the highest number density that is *not* near-duplicate of the headline
   (token overlap < 40%)
3. Else render headline only — no empty line, no placeholder

Expect a "so what" line on ~44% of stories, a number line on most of the rest.

### 4. Design a weekend/thin state

When the day has < 5 stories, drop the stat strip and `+N more · ~M MIN`, and render the
available stories in full. Sunday's card should not promise a 5-minute brief.

### Worked example — real data, Tue 19 Aug 2026 (21 stories)

```
TODAY'S EDITION · 7:00 AM                    Wed, 20 Aug
─────────────────────────────────────────────────────────
  ₹9,422 Cr            2              14
  Shiprocket mcap      funding rounds companies
                       ₹935 Cr        2 you track
─────────────────────────────────────────────────────────
  FUNDING · Navi
  IPO-Bound Navi Raises $100 Mn From Prosus
  ↳ Revives its ₹3,000 Cr IPO plan                    [b2]
─────────────────────────────────────────────────────────
  IPO · Shiprocket
  Shiprocket Shares End First Session 48% Above Issue
  ↳ Subscribed 99.38X; listed at ₹9,422 Cr mcap       [b2]
─────────────────────────────────────────────────────────
  FINANCIALS · Cashfree
  Cashfree FY26: Revenue Inches Closer To ₹1,000 Cr
  ↳ Loss narrowed 23.1% to ₹118.5 Cr                  [b1 number]
─────────────────────────────────────────────────────────
  + 18 more · ~6 MIN            [ OPEN TODAY'S BRIEF ]
```

## The editorial question — to settle with Utkarsh

Both paths are viable; they differ in ceiling, not in whether the card ships.

| | **A. Render-time (default — ship now)** | **B. Editorial convention** |
|---|---|---|
| Change needed | None to newsroom | Each bullet gets a fixed job: b1 news, b2 so-what, b3 proof |
| Reliability | Degrades on the 56% with no so-what | Position becomes a contract the UI can trust |
| Also fixes | Nothing | The 7% with no summary and the 5% that aren't 3 bullets |
| Risk | Heuristic picks a dull line | Newsroom bandwidth; 95% `Inform Me` means b2 is often genuinely absent, not just unwritten |

Recommendation: **ship A now, raise B separately.** B is a content-ops commitment, and the
`user_needs` distribution says a real so-what line does not exist for most stories — a
convention would force writers to manufacture one.

## Files / systems touched

Nothing in this repo — this is a design + data-contract change:

- **Figma** `Inc42-App-2026`, node `4163-4056` — stat strip, row eyebrow, add the b2 line, add thin-day state
- **App brief-feed API** — must start returning the 3 summary bullets and `development_tag` per story; currently the card is built on `sector` + headline
- **Bullet-selection logic** — server-side, so the heuristic can be tuned without a release
  (relevant given feature flags are HALTED per `project-inc42-askinc42-next-week`)

## Verification

1. **Backtest the tiles** — replay the selection logic over all 61 days in the corpus; assert no
   tile ever renders zero, empty, or a placeholder. Fail the build if any day produces a blank slot.
2. **Backtest bullet selection** — dump the chosen line for all 699 summarised articles; manually
   review a 40-article sample for lines that are duplicative of the headline or read as a non-sequitur.
3. **Weekend check** — force-render the card for the 8 Sundays and 8 Saturdays in the corpus.
4. **Instrument** — `brief_card_impression` with which tiles rendered and whether a b2 line was
   shown, so tap-through on b2-present vs b2-absent cards is measurable. This is the actual test:
   the current loss point is card 1 of the brief (45% advance, per `project-inc42-app-behaviour`),
   and the home card is upstream of that.

## Data artefacts

- `/private/tmp/claude-501/-Users-thrillophilia/4c665638-1d86-4566-8ae3-59818b87710f/scratchpad/summaries.json`
  — 750 articles with scraped bullets (699 with a summary)
- `posts_rest.json` — WP REST metadata incl. `user_needs`, `push_notification`

Note: an initial scrape pass reported ~41% of articles missing a summary. That was a scraper
artefact — 277 HTTP 429s counted as absences. Re-fetched; true coverage is 93%.
