# Home brief card — data backtest

Tests the proposed card logic (plan: `~/.claude/plans/eager-enchanting-clover.md`)
against the real corpus: 809 articles, 21 Jun – 20 Aug 2026.

## Run
    python3 render_card.py          # -> cards.txt, backtest.csv

Inputs: `~/Downloads/42_posts (1).csv`, `summaries.json` (699 scraped 3-bullet summaries).

## Files
| File | What |
|---|---|
| `render_card.py` | Tile selection + bullet selection + card renderer |
| `cards.txt` | A rendered card for all 61 days |
| `backtest.csv` | Per-day audit: tiles rendered, rows with a line, bullet source |
| `summaries.json` | Scraped `single-post-summary` blocks, 750 articles |

## Results
- 0 zero-value tiles, 0 empty tile strips across 61 days
- Thin-state fires on 10 days (9 Sundays + 1 Saturday), all with <5 stories
- 88% of teaser rows get a sub-line; 41% of those come from bullet 2
- Hero tile resolves to a real transaction on 47/61 days

## Known gaps (not fixed here)
1. **Row ordering** — rows are recency-sorted, so the hero tile's company appears
   in the three teaser rows only 28% of the time. Card contradicts itself.
   Ranking formula is owned elsewhere; not changed here.
2. **Prospective vs completed** — the hero tile can surface a planned IPO size
   rather than a completed raise (19 Aug shows Navi ₹3,000 Cr IPO plan, not the
   $100 Mn round).
3. 5% of rows pick a fallback bullet that never names the story's company.
