# Companies in today's brief — what kind of company news Inc42 actually publishes (90-day corpus)

Corpus: 1,179 articles, 6 Jun – 4 Sep 2026 (91 days, 65 weekdays). Source `corpus90.json` (WordPress REST + ACF).
Classifier: headline rules (`mention_types_90d.csv` has every row with its type, source and URL). 93% agreement with the CMS `development_type` on the 570 rows where the CMS is specific; the CMS "Business Updates" catch-all (255 rows) was split by headline.

## Company tagging coverage
| | Articles | Share |
|---|---|---|
| Real company slug | 860 | 73% |
| Placeholder `tbd` | 166 | 14% |
| Blank | 153 | 13% |
| Distinct companies | 443 | |

## Pivot A — mention type
| Mention type | Articles | % all | With company | Distinct cos | Weekdays with ≥1 (of 65) | Median / weekday |
|---|---|---|---|---|---|---|
| Funding round | 216 | 18% | 197 | 183 | 60 (92%) | 3 |
| Analysis / feature (In-Depth, Startup Stories) | 176 | 15% | 102 | 85 | 56 (86%) | 1 |
| Financials (Q/FY results) | 118 | 10% | 111 | 100 | 38 (58%) | 1 |
| Policy / govt (no company) | 104 | 9% | 7 | 6 | 7 (11%) | 0 |
| Roundup / daily brief | 101 | 9% | 50 | 43 | 48 (74%) | 1 |
| IPO (DRHP, anchor, listing) | 100 | 8% | 94 | 47 | 50 (77%) | 1 |
| Product / launch / expansion | 75 | 6% | 58 | 44 | 31 (48%) | 0 |
| Legal action / controversy | 54 | 5% | 54 | 39 | 35 (54%) | 1 |
| M&A | 45 | 4% | 39 | 35 | 28 (43%) | 0 |
| Stake sale / secondary / ESOP | 40 | 3% | 39 | 24 | 28 (43%) | 0 |
| Stock move (listed) | 39 | 3% | 34 | 24 | 26 (40%) | 0 |
| Leadership / people | 32 | 3% | 27 | 24 | 18 (28%) | 0 |
| Industry / analysis | 23 | 2% | 7 | 6 | 6 (9%) | 0 |
| Fund launch (VC) | 22 | 2% | 17 | 17 | 15 (23%) | 0 |
| Layoffs | 9 | 1% | 6 | 6 | 5 (8%) | 0 |
| Regulatory approval | 9 | 1% | 9 | 9 | 9 (14%) | 0 |
| Shutdown | 8 | 1% | 6 | 6 | 6 (9%) | 0 |
| Business update (other) | 8 | 1% | 3 | 3 | 3 (5%) | 0 |

## Pivot B — mention type × company stage (company-tagged rows)
| Mention type | Late stage | Listed | Growth | Early | Investors | Intl | Indian corp | Govt | Blank | Total |
|---|---|---|---|---|---|---|---|---|---|---|
| Funding | 27 | 20 | 64 | 81 | 2 | 1 | 1 | 1 | 0 | 197 |
| Analysis / feature | 36 | 19 | 17 | 16 | 0 | 3 | 2 | 2 | 7 | 102 |
| Financials | 32 | 68 | 5 | 3 | 0 | 1 | 2 | 0 | 0 | 111 |
| IPO | 75 | 11 | 7 | 0 | 0 | 0 | 1 | 0 | 0 | 94 |
| Product / launch | 18 | 13 | 10 | 6 | 1 | 3 | 6 | 0 | 1 | 58 |
| Legal action | 25 | 16 | 6 | 0 | 0 | 5 | 2 | 0 | 0 | 54 |
| Roundup | 22 | 12 | 3 | 2 | 0 | 3 | 1 | 0 | 7 | 50 |
| M&A | 10 | 12 | 11 | 5 | 0 | 1 | 0 | 0 | 0 | 39 |
| Stake sale | 3 | 34 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 39 |
| Stock move | 1 | 32 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 34 |
| Leadership | 8 | 9 | 5 | 0 | 3 | 1 | 1 | 0 | 0 | 27 |
| Fund launch | 1 | 0 | 0 | 1 | 15 | 0 | 0 | 0 | 0 | 17 |
| Regulatory approval | 1 | 6 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 9 |
| Layoffs | 1 | 1 | 2 | 1 | 0 | 1 | 0 | 0 | 0 | 6 |
| Shutdown | 2 | 0 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 6 |

## Pivot C — what the CMS `development_type` hides (Business Updates = 255 rows)
Product/launch 64 · Stake sale 33 · Stock move 33 · Roundup 24 · Funding 22 · Policy 16 · M&A 10 · Legal 9 · Regulatory approval 7 · Financials 7 · Shutdown 5 · Leadership 4 · other 21.
Controversies (91) = Legal action 44 · Policy (no company) 30 · Roundup 7 · Shutdown 3 · Layoffs 2 · other 5.

## Per weekday (company-tagged, excluding roundups)
| | Median | p25 | p75 | Min |
|---|---|---|---|---|
| Tagged stories | 11 | 10 | 14 | 3 |
| Distinct companies | 11 | | | 3 |
| Stories with a data-backable type | 8 | 6 | 10 | 2 |
Weekdays with ≥5 data-backable company stories: 58 of 65. Zero-days: 0. Share of tagged stories that are data-backable: 71.5%.
Data-backable = Funding, Financials, IPO, M&A, Layoffs, Stock move, Stake sale, Leadership, Shutdown, Fund launch.

## Continuity
440 companies tagged in non-roundup stories; 120 have ≥2 mentions; 109 of those span ≥2 mention types.
Top: Swiggy 18, Flipkart 17, Zepto 15, Ola Electric 13, Ather 12, Turtlemint 12, Meesho 11, Shiprocket 11.

## Mention type → data point (DataLabs free-tier fields confirmed on the Zepto page 5 Sep: total funding, investors count, revenue+YoY, employees+90d trend, web traffic 30d)
| Mention type | Show | Field status |
|---|---|---|
| Funding | Total funding to date · investor count · last round | Confirmed |
| Financials | Last filed FY revenue + YoY · loss/profit | Confirmed, but DataLabs FY lags the article's FY/quarter — must label the year |
| IPO | Total funding · revenue · valuation | Funding/revenue confirmed; valuation & issue size unverified |
| Layoffs / Shutdown | Employees + 90-day trend | Confirmed; 9 layoff stories in 90 days — a fortnightly event, not a daily slot |
| Stock move / Stake sale | Market cap · share price move | Not on company page as verified; exists in Inc42's listed tracker — verify |
| M&A | Acquisitions count · total funding | Unverified |
| Leadership | Key people | Unverified |
| Product / launch | Web traffic 30d trend | Confirmed |
| Legal action | Nothing structured | Show company profile only, no number |
| Analysis / feature | Full profile card | Confirmed fields |
