# Brief landing — 20 ranking variants (row T)

5 Sep 2026. Draft file `dAsaTgNj0xh25w2OGaurZo`, y=128600.
Existing frames were not edited, including S10 and the Q Edition landings.

Figma: [T1 · Deals follower](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=490-10)

These exist because the Edition masthead could not be related to, and did not show how the eight are chosen. Every screen below uses a real day and the live formula:

`score = 1.0×TopicAff + 0.6×SectorAff + 0.15×Pop` then newest first. Editorial featured jumps the queue.

Company + development type, not the headline — so the order is visible without spending the story.

---

## The pair that shows the logic

Same Monday 8 June, twelve stories.

| | You follow Deals (T1) | You follow IPO (T2) |
|---|---|---|
| 1–3 | Aye $15 Mn, GPS ₹635 Cr, Immuneel ₹100 Cr | Zepto 11:36 pm, Klassroom 4:01 pm, Curefoods 11:24 am |
| Zepto | **Not in the eight** | #1, because it is newest among equal IPO scores |
| Why | IPO is not Deals. Industry field empty, so Consumer cannot pull Zepto in. | TopicAff=1.0 for all three IPOs. ₹8,010 Cr is not a signal. |

T3 is the third column: no topics. Popularity only. News (Incuspaze) leads, IPO last.

---

## All 20

| # | Screen | Day | Profile | What it makes visible |
|---|---|---|---|---|
| T1 | Sorted for Deals | 8 Jun | Deals | Matches lead. Zepto absent. |
| T2 | Sorted for IPO | 8 Jun | IPO | Same pool, different eight. Recency among ties. |
| T3 | Default brief | 8 Jun | No prefs | Popularity order, identical for every such user. |
| T4 | Three weights | 8 Jun | Deals | 1.0 / 0.6 / 0.15 bars. Sector term is zero. |
| T5 | The tie | 8 Jun | IPO | Three IPOs, score 1.009, newest first. Figure unused. |
| T6 | Match, then fill | 8 Jun | Deals | Two bands, every row labelled — no unmarked filler. |
| T7 | One Team match | 11 Jun | Team | Opendoor layoff leads. Popularity fills 2–8. |
| T8 | No AI match | 11 Jun | AI | AI is not a mapped topic. Popularity still builds eight. |
| T9 | One story | 14 Jun | any | Length 1, no type, score 0. Not padded. |
| T10 | Logged out | 8 Jun | none | Popularity brief. No name, no streak. |
| T11 | Headline figures | 8 Jun | IPO | ₹8,010 Cr / $15 Mn / ₹635 Cr / ₹100 Cr. Not a ranking input. Klassroom/Curefoods have none — slots absent. |
| T12 | Initials, no logos | 8 Jun | Deals | Empty circle for the company-less row. |
| T13 | Two names | 8 Jun | — | Incuspaze · iKeva. `second_company` empty in the file; second name parsed from the headline. Tagged Business Updates, so a deal loses to News popularity. |
| T14 | No company | 8 Jun | — | 27% case. Row is “Industry Trends · no company”, not a hole. |
| T15 | Why Zepto is missing | 8 Jun | Deals | Five steps of the current formula. |
| T16 | Sector never fired | 8 Jun | Consumer | Following Consumer does nothing this day. |
| T17 | Editorial override | 8 Jun | Deals | Simulated `App Featured`. Not in the 90-day extract. Mechanic only. |
| T18 | Follows as the lens | 8 Jun | Deals | The inputs, on the card, then the eight they produced. |
| T19 | Type mix | 8 Jun | Deals | 3 funding / 1 news / 2 trends / 2 IPO, in score order. |
| T20 | Heavy Thursday | 6 Aug | Deals+Financials | Practo, Solinas, Wakefit, ixigo, LEAP, Groww. Does not say 8 of 27. |

---

## Fields used

| Field | Coverage | Where |
|---|---|---|
| `development_type` → topic | 85% | almost every screen; T9 collapses it |
| `primary_company` | 73% have one | name/initial; T14 is the miss |
| `second_company` | **0% in this extract** | T13 declares a headline parse |
| `company_type` | 85% | T5, T9 |
| Headline figure | 47% (Deals 82%, IPO 56%) | T11, and as flavour on Deals rows |
| `primary_industry` | empty on most of 8 Jun | T16 is the consequence |
| Date/time | 100% | folio, recency (T2, T5) |
| Followed topics | user input | T1 T2 T7 T8 T15 T18 T20 |
| Popularity table | constants | T3 T4 T8 T10 |
| App Featured | **not in the extract** | T17 simulated |

Not used: sentiment, shelf_life, story_type, newsletter title, logos, full headlines.

---

## Failure days

| Failure | Screen |
|---|---|
| 1 story | T9 |
| Nothing matches | T8 |
| No preferences | T3 |
| Logged out | T10 |
| No company | T12, T14 |
| Two companies | T13 (headline parse; field missing) |
| No logo | T12 |

---

## Editorial work

None per day, except T17 which is a simulated featured flag and is labelled as such.
T13’s second name is a headline parse, not a CMS field.
