# Brief landing — editorial / app balance

5 Sep 2026. Draft file `dAsaTgNj0xh25w2OGaurZo`, row U at y=134200.
Existing frames not edited.

Figma: [U1 · Founder · Deals](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=501-8)

---

## Who is coming

P1 on the app (qualifying in-app action): founders at every stage, startup C-suite and heads, investor decision-makers (partners, principals). Operators and BD are in the role picker. ICs are not the app ICP.

They already know Inc42 as a newsroom. They open a phone in the morning to not miss what moved in funding, IPOs, and their companies. They are not here to learn a ranking engine.

## How they actually behave

788 users, 21 days. They visit the Brief tab **4 times a day** and **44% never open the brief**. Of those who do, **45% leave at story 1**. After that they finish (77–87%). Completers take **78 seconds**. D3 retention falls to 7–21%. Push has never fired.

So the landing is not a magazine cover and not a dashboard. It has about two seconds, on a fourth visit, to say: this is today’s set, it is for you, tap.

## How the brief actually works (what we can say)

Stories matching a followed **topic** go first (weight 1.0). Followed **sectors** next (0.6) — but sector tags are often empty, so this frequently does nothing. Then **popularity** (0.15), which is a category constant: News always outranks IPO. Ties break on **newest**. A newsroom pin can jump the queue. Cap 8, 07:00 to 07:00, never padded.

Same Monday, a Deals founder and an IPO investor do not get the same eight. Zepto’s ₹8,010 Cr IPO is first only if you follow IPO. If you follow Deals, it is not in the eight. The rupee figure is not in the formula.

We do not put that paragraph on the card. We put the **result**: Aye, GPS, Immuneel for Deals; Zepto, Klassroom, Curefoods for IPO; “Because you follow Deals.”

## The balance

| Too editorial (Edition) | Too modern (ranking row) | This |
|---|---|---|
| Masthead, folio, no names | TopicAff, scores, MOST READ | “Today’s Brief” in Newsreader |
| Felt like a newspaper PDF | Felt like an admin tool | App chrome they already have |
| Couldn’t relate | Couldn’t be a reader | Three companies + type + figure |
| Didn’t say it was a set | Listed the whole eight | +5 more, behind the tap |

Orange stays in the header. The card is paper-coloured, not orange. Inter for UI, Newsreader only on the title.

## Screens

| | Who | Day | What it shows |
|---|---|---|---|
| U1 | Founder, follows Deals | 8 June | Three fundings. Zepto not named. |
| U2 | Investor, follows IPO | 8 June | Zepto, Klassroom, Curefoods. Same day as U1. |
| U3 | Operator, follows Team | 11 June | Opendoor layoff first. Ordinary Thursday. |
| U4 | Guest, no topics | 8 June | No personal chip. Popularity order, still named. |
| U5 | Same founder, came back | 8 June | “You were on 3 of 8.” Continue, don’t restart. |

## Fields

Company name (73%), development type (85%), headline figure when present (Deals 82%), date, count, followed topic. No scores, no publish totals, no full headlines, no logos, no newsletter title.

Failure: 1-story drops to one row and “Open today’s story.” No match drops the chip (U4). No company uses the type as the name. Two companies would read “Incuspaze · iKeva” if we parse the headline; the CMS field is empty.
