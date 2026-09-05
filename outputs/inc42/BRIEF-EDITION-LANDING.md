# Brief landing — THE EDITION

5 Sep 2026. Draft file only: `dAsaTgNj0xh25w2OGaurZo`, row Q at y=126200.
Existing frames were not edited. S10 · THE EDITION (`462:208`) and the current Brief page (`236:127`) are untouched.

Figma: [App - Draft Screen, Q1](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=474-4)

Shell taken from the live Brief chrome (orange header, greeting, streak, Past briefs, tab bar). The photo-and-three-headlines block is replaced by S10’s masthead. Orange stays in the header only.

---

## What it is answering

| Question | How the screen answers it |
|---|---|
| What is Brief? | Masthead: **THE INC42 BRIEF**. The word is the title, not a tab label. |
| Is this personalised? | One line, only when true: “Six are in what you follow.” If nothing matches, the line is not there. |
| Is this everything I need? | “Chosen from everything published today.” Completeness as an outcome, not “8 of 14”. |
| What is inside? | A countable set (folio + equal ticks). Not the headlines. |
| What is the card for me / FOMO? | An edition number you can miss. Tomorrow’s brief arrives at 7 AM. |
| Not just an article? | No photo, no headline, no standfirst of a story. A publication has a masthead, a number, a set. An article does not. |

---

## The five screens

### Q1 — Monday 8 June 2026 (big day)
Logged in. Follows Consumer + Deals/News. Brief of 8.

**Dek:** “Three IPO filings and three rounds.”
Computed from `development_type` on that day’s likely eight: Zepto / Klassroom / Curefoods (Startup IPO ×3), Aye / GPS / Immuneel (Startup Funding ×3). No company is named, so the Brief does not appear to be “about Zepto”.

### Q2 — Thursday 11 June 2026 (ordinary day)
The day S10 was drawn for. Logged in. Follows Consumer.

**Dek:** “Four rounds and one layoff.”
Ethereal, Manam, 4baseCare, IN-SPACe (funding ×4) + Opendoor (Startup Layoffs). Dropped S10’s “A quiet Thursday” (a judgment) and the orange-vs-grey ticks (marking followed stories as the real ones).

### Q3 — Sunday 14 June 2026 (one story)
One published article: *Zepto’s Battle Beyond Speed*. `development_type` empty → dek slot gone. Folio says ONE STORY. One tick. CTA: “Open today’s story”.

### Q4 — Thursday 11 June, AI-only, no direct match
Same day as Q2. Personal line omitted. No “nothing in AI today”.

### Q5 — Thursday 11 June, logged out / no preferences
Greeting is “Morning”. Streak chip gone. Card identical to Q4.

---

## Field coverage

| Slot | Field | Coverage | Rule |
|---|---|---|---|
| Masthead “THE INC42 BRIEF” | none (static) | 100% | always |
| Folio date | article date | 100% | always |
| Folio “N stories” | brief length (min(8, published that day)) | 100% | “ONE STORY” when N=1 |
| Edition number | sequential Brief counter since launch | **new field, 100%** | calendar/product, not editorial. Mock: 11 June = No. 235 as S10 already set |
| Dek | counts of `development_type` in the 8, mapped to plain words (round / IPO filing / layoff / acquisition) | 85% (15% of articles have no type) | render if ≥1 typed event in the 8; otherwise the slot is absent |
| “Chosen from everything published today.” | none (static) | 100% | always. Does not state how many Inc42 published |
| “K are in what you follow” | direct topic/sector match count | 13–87% by profile | **only when K ≥ 1**. No substitute text |
| Ticks | N = brief length | 100% | all equal. None highlighted |
| CTA | N | 100% | “Open No. N” / “Open today’s story” when N=1 |
| Footnote | static | 100% | “This brief is only for today. Tomorrow’s brief arrives at 7 AM.” |
| Past briefs | previous Brief dates + counts, 7-day retention | 100% of days the app has been live | Q1’s third slot is hidden: 5 June is outside the 90-day file |

**Not used:** `primary_company` (27% missing), `second_company`, logo, `primary_industry` (24% missing after roll-up), summary bullets, headline figures, `sentiment__tonality` (unusable), `shelf_life`, `story_type`, `parent_category`, the Daily Brief newsletter title (misaligned with ranking).

---

## Failure days (section 9)

| Failure | What happens |
|---|---|
| 1 story | Q3. Folio, tick count, CTA all switch. Dek collapses if untyped. |
| Nothing matches what the user follows | Q4. Personal line omitted. Card still complete. |
| No preferences | Q5. Same card as Q4. |
| Not logged in | Q5. Name and streak gone. |
| Article with no company | Never shown on this screen. Unaffected. |
| Article with two companies | Never shown on this screen. Unaffected. |
| Company with no logo | Never shown on this screen. Unaffected. |

---

## New content / editorial work

None per day.

- Dek is a count of `development_type`. No one writes a thesis at 07:00.
- Edition number is a counter.
- Personal line is a match count, gated on K ≥ 1.

The Daily Brief newsletter title is **not** used. On 11 June it named ZEE5 and WinZO, neither of which is required to be in the ranked eight.

---

## What was taken from S10, and what was refused

Kept: masthead, Newsreader, double rule, folio, cream stock, black CTA, the word “brief”, a countable set.

Changed, because of the rejection table:

| S10 had | Why it moved |
|---|---|
| “A quiet Thursday: …” | A judgment. Replaced with the type-count. |
| 3 orange ticks / 5 grey | “What will happen to the non-highlighted ones?” All ticks equal. |
| “About four minutes” | Time claims are not believed. Dropped. |
| Card only, 358px | Placed in the existing 390px Brief chrome, as a landing. |

The current Brief page’s photo + three headlines was not copied onto these screens. That layout is the “looks like an article” failure.
