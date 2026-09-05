# Brief landing — 15 UI types (row W)

5 Sep 2026. Draft file `dAsaTgNj0xh25w2OGaurZo`, row W at y=140200.
Existing frames were not edited (Q, T, U, V, S10, live Brief).

Figma: [W1 · Live room](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=521-2)

The Q header (node `474:5` — Monday / Morning Ranjith / streak chip) is not used. Brand orange `#EA4B2B` is. Each screen is a different object, not a content swap on one card.

Live social-proof numbers are **new product fields**. They are mocked at a scale that fits ~80 daily actives (788 users / 21 days / 1,650 person-days). They are not in the CMS extract. 78 seconds and “45% of people who opened, finish” are measured.

---

## The 15

| | Object | Freeze | FOMO | Open |
|---|---|---|---|---|
| [W1](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=521-2) | Dark live room | Giant **34** | People in it now | Orange CTA |
| [W2](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=521-17) | Completion wall | Giant **51** | They finished. You didn’t. | “Open before it’s only yesterday” |
| [W3](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=521-32) | One-story takeover | **Aye Finance** fills the page | 12 people are on it now | Join them |
| [W4](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=521-45) | Orange streak field | Giant **12** | 12 becomes 0 at 7 AM *(new mechanic — see below)* | Keep the 12 |
| [W5](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=521-54) | Seal | You cannot see inside | 34 already inside | Break the seal |
| [W6](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=521-70) | Ticket | Admit-one stub | 34 holding it / 51 through the gate | Tear and enter |
| [W7](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=521-108) | Stories ring | Unopened orange ring | 34 in it, you have not started | Open the ring |
| [W8](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=521-135) | Fourth-visit desk | Two words: Still unopened | 51 finished / 34 in it | Open it this time |
| [W9](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=521-149) | Peer room | Avatars of founders on Deals | 41 / 19 / 22. You are not in the 41 | Step in |
| [W10](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=523-2) | Type poster | Names as a poster, no chrome | 34 reading · 51 finished · you are not in | Open the brief |
| [W11](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=523-12) | Page freeze | The tab is locked under a sheet | 34 reading now. Page stays frozen until open | Open today’s brief |
| [W12](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=523-30) | On air | 2h 41m since 7 AM | 34 listening. You are not in the room | Tune in |
| [W13](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=524-2) | Scoreboard | Reading vs done per company | You are in none of these numbers | Get on the board |
| [W14](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=524-28) | City bar | **45%** who opened, finished | 5 of 8 segments filled citywide | Start today’s brief |
| [W15](https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen?node-id=524-49) | Missed beat | **0 of 8** on the 4th visit | 51 finished. Brief gone at 7 AM | Open today’s brief |

---

## Why not one layout

U/V answered “what is in the brief” with the same card, three names, a chip. That is a reader’s index. It does not stop a thumb that already visits four times and leaves 44% of the time.

These 15 answer a different job: **other people are in it, you are not, the set ends at 7 AM.** Marketing editorial already does this (live rooms, “X reading”, completion walls). The newsroom homepage does not. The app can.

W5 and W11 are the strictest freeze: nothing of the eight is readable until the tap. That respects the old rejection of listing all headlines.

---

## Fields

| Slot | Source | Coverage | New? |
|---|---|---|---|
| Word “Brief” | static | 100% | no |
| Company names (3) | `primary_company` | 73% | no — W5/W11/W8 hide them |
| Type + figure | `development_type`, headline figure | 85% / 47% | no — only W3 uses it |
| Brief length | min(8, published) | 100% | no |
| Time since 7 AM | clock | 100% | no (W12) |
| Visit index today | session | 100% of logged-in days | no — W8, W15 (4.0 visits/person-day is measured) |
| Streak | existing | logged-in | no — W4. **Reset-if-unopened is a new rule** |
| Live readers now | not in extract | — | **YES** W1, W5–W13, W15. Mock: 34 |
| Completions today | not in extract | — | **YES** W2, W9, W10, W15. Mock: 51 |
| Currently on story N | not in extract | — | **YES** W3, W13. Mock: 12 / 8 / 6 |
| Peer room (role × topic) | not in extract | — | **YES** W9 |
| % of openers who finish | PostHog 25% complete / 56% opened ≈ **45%** | measured | W14. Not a live field |

Not used: scores, TopicAff, newsletter title, photos, “8 of 14 published”, DataLabs metrics, “5 minutes”.

---

## Failure days

| Failure | What happens |
|---|---|
| 1 story | W3 becomes the one company. W5 seal says 1 INSIDE. W13 has one row. W15 is 0 of 1. |
| Nothing matches follows | Chip never existed on this row. W9’s “Founders following Deals” falls back to “people on Inc42” (declare). |
| No preferences / logged out | W4 streak and W9 peer room drop. W1/W2/W5/W11 still work. |
| No company | W3/W10/W13 use `development_type` as the name (same rule as V4). |
| Two companies | W6/W10 can print “Incuspaze · iKeva”. |
| No logo | none of these screens use logos. |

---

## What would have to be built

1. **Live counters** (readers now, finished today, on-story-N). Not in the app today. Push has never fired either — this is the same class of missing cue.
2. **W4 streak death at 7 AM if unopened** — not how streak works today. Do not ship that line without a product decision.
3. **W9 role × topic rooms** — needs the role picker plus follow graph, aggregated, not identified (initials are decorative).

Everything else is layout on fields we already have.
