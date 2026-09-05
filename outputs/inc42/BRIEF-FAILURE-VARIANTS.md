# Brief landing — remaining people and failure days (row V)

5 Sep 2026. Draft file `dAsaTgNj0xh25w2OGaurZo`, row V at y=136600.
Existing frames were not edited, including S10, Q, T, and U1–U5.

Figma: [V1 · One story](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=512-2)

Same language as U: orange in the header only, paper card, Newsreader on “Today’s Brief”, three named stories, +5 behind the tap. This row is the rest of section 9 and the ICP seats U did not draw.

---

## Screens

| | Who | Day | What it shows |
|---|---|---|---|
| V1 | Logged in, any follow | 14 June | One story. Zepto. No type, so no meta line. CTA: “Open today’s story.” Chip gone — nothing to match. |
| V2 | Founder, Deals + Financials | 6 Aug | Heavy Thursday (27 published). Practo, Solinas, Wakefit. Still says 8, never 8 of 27. |
| V3 | Follows News | 8 June | Two companies on one row: Incuspaze · iKeva. `second_company` is empty in the file; the second name is parsed from the headline. |
| V4 | Any | 8 June | 27% case. First row is the type (“Industry Trends”), not a hole. Kuku FM has a company and no type — name only. |
| V5 | C-suite, Financials | 6 Aug | Wakefit / ixigo / Shiprocket. Figures from the headlines. Because you follow Financials. |
| V6 | Investor, follows IPO | 11 June | No IPO that day. Chip omitted. Popularity still names Lenskart, Ethereal, Manam. |
| V7 | Founder | 7 June | Weekend. Two stories, both untyped. Ola Consumer, Wagh Bakri. Length 2, not padded. |
| V8 | Same founder as U1, done | 8 June | “You finished today’s 8.” All three marked Read. CTA: Read again. Does not restart. |
| V9 | Follows Consumer | 8 June | Sector field empty on that day, so the 0.6 term is zero. Chip omitted. Names are News then Deals. |
| V10 | Logged out | 8 June | Greeting is “Morning”. No streak, no avatar, no chip. Same named brief as the guest. |

U already had: founder Deals, investor IPO (same Monday), operator Team, guest, continue-from-3. V fills the gaps.

---

## Fields

| Slot | Field | Coverage | Rule |
|---|---|---|---|
| Title “Today’s Brief” | none | 100% | always |
| Folio count | brief length = min(8, published) | 100% | “1 story” / “2 stories” when N<8 |
| Folio date | article date | 100% | always |
| Chip “Because you follow X” | followed topic with ≥1 match | 13–87% by profile | **only when K ≥ 1**. V1, V4, V6, V7, V9, V10 omit it |
| Company name | `primary_company` | 73% | V4 uses `development_type` as the name when company is empty |
| Second name | `second_company` | **0% in this extract** | V3 parses the headline. Declared. |
| Type + figure | `development_type` + headline figure | type 85%; figure 47% (Deals 82%) | slot absent when type empty (V1, V7, V4 Kuku) |
| +N more | 8 minus 3, if N=8 | 100% of 8-story days | hidden when N≤3 |
| CTA | N, and progress | 100% | “Open today’s story” when N=1; “Read again” when finished |
| Past briefs | previous days, cap 8 | 7-day retention | “—” when the day is outside the 90-day file |
| Streak / avatar | logged-in | — | hidden when logged out (V10) |

Not used: scores, TopicAff, popularity bars, logos, full headlines, newsletter title, “8 of 27”, DataLabs metrics.

---

## Failure days (section 9)

| Failure | Screen |
|---|---|
| 1 story | V1 |
| Nothing matches what the user follows | V6 (IPO on 11 June), V9 (Consumer, sector empty) |
| No preferences | U4 (already) |
| Not logged in | V10 |
| Article with no company | V4, first row |
| Article with two companies | V3 |
| Company with no logo | never shown — names, not marks |
| Weekend / untyped | V7 |
| Heavy day | V2 — still 8, not “8 of 27” |
| Finished (4 visits a day) | V8. U5 is the mid-deck return |

---

## New content required

None. No daily dek, no editorial thesis, no impact score. V3’s second name is a headline parse, not a CMS field — say so if this ships.

---

## What this row is not

It does not replace U. It does not go back to T’s scores. It does not go back to Q’s masthead. It is the same card, run against the days and people the brief said it had to survive.
