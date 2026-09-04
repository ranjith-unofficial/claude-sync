# Brief page + Brief card — ASCII UX wireframes
4 Sep 2026. Pre-Figma. From the PRD, post-launch behaviour, and the 4 Sep sessions.

Constraints these are drawn against:
- Brief stays home. Page extends from 2-3 scrolls to 4-5, by adding depth BELOW the brief.
- 3 card styles per section (hero / mid / row) + carousel as a 4th, scoped to home.
- No card containment in feeds. Bottom separators only, bold type. The brief card is the
  ONE contained object on the page, which is what makes it the hero.
- The word "Brief" must be visible at the top. It is missing today.
- The 3 preview rows must be distinguishable from each other. They are not today.
- Carousel next item must peek by default.
- Tags use primary or secondary sector only, never tertiary.

===============================================================
A. BRIEF HOME — FULL SCROLL
===============================================================

SCROLL 1 ......................................... above fold

  9:41                                    ▮▮▮ ▮ ▮▮
 ┌─────────────────────────────────────────────────┐
 │  Thu, 25 June                    ◆ 12    ( RM ) │
 │  Good morning                                   │
 └─────────────────────────────────────────────────┘

  TODAY'S BRIEF                        Past briefs ›
  ═════════════════════════════════════════════════

 ┌─────────────────────────────────────────────────┐
 │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ f e a t u r e ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
 │▓ (●) 312 reading now                           ▓│
 │▓                                               ▓│
 │▓                                               ▓│
 │▓  8 STORIES  ·  5 MIN  ·  FILED 7:00 AM        ▓│
 │▓  Thu, 25 June                                 ▓│
 └─────────────────────────────────────────────────┘

   ▪ HEALTHTECH
     Healthify merges with US-based Berry Street
   ───────────────────────────────────────────────
   ▪ FINTECH
     Slice adds ex-SBI, ICICI execs to its board
   ───────────────────────────────────────────────
   ▪ DEEPTECH
     NVIDIA price hike hits India's compute cos

   + 5 more inside

 ┌─────────────────────────────────────────────────┐
 │           OPEN TODAY'S BRIEF              →     │
 └─────────────────────────────────────────────────┘

   New brief every morning at 7:00 AM
 - - - - - - - - - - fold - - - - - - - - - - - - -

SCROLL 2 ......................................... the depth begins

  MOVING TODAY                                     ›
  2 raises · 2 results · 1 IPO filing
  ─────────────────────────────────────────────────

 ┌───────────────┐ ┌───────────────┐ ┌────────
 │ [logo]     ☆  │ │ [logo]     ☆  │ │ [logo]
 │               │ │               │ │
 │ Zepto         │ │ Groww         │ │ Lenskart
 │ CONSUMER      │ │ FINTECH       │ │ ECOMMERCE
 │               │ │               │ │
 │ Raised        │ │ Filed DRHP    │ │ Revenue up
 │ $450 Mn       │ │ ₹6,000 Cr     │ │ 34% QoQ
 │               │ │               │ │
 │ Series G      │ │ SEBI filing   │ │ Q1 FY27
 └───────────────┘ └───────────────┘ └────────
                                       ^ peek

  ^ CAROUSEL. Next card peeks by default so the
    horizontal scroll is signalled without a hint.

SCROLL 3 ......................................... article section

  BEYOND THE BRIEF                                 ›
  ─────────────────────────────────────────────────

 ┌─────────────────────────────────────────────────┐
 │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ HERO  IMAGE ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
 │▓ AI                                    6 MIN   ▓│
 │▓                                               ▓│
 │▓  The enterprise fight against runaway         ▓│
 │▓  AI costs                                     ▓│
 └─────────────────────────────────────────────────┘
   ^ CARD STYLE 1 — hero. One per section.

   ┌────────────┐  D2C                    4 MIN
   │  ▓ img ▓   │  Why Dot & Key waited until
   │  ▓▓▓▓▓▓▓   │  ₹300 Cr before going offline
   └────────────┘
   ─────────────────────────────────────────────────
   ┌────────────┐  D2C                    5 MIN
   │  ▓ img ▓   │  Why Hammer prefers cables over
   │  ▓▓▓▓▓▓▓   │  premium headphones
   └────────────┘
   ^ CARD STYLE 2 — mid. Positions 2 and 3 only.
   ─────────────────────────────────────────────────
   POLICY                                    3 MIN
   The RBI fund row, and the PM's I-Day address
   ─────────────────────────────────────────────────
   MOBILITY                                  4 MIN
   Ola Electric secures ₹95.81 Cr under PLI-Auto
   ─────────────────────────────────────────────────
   ^ CARD STYLE 3 — row. No image, no container.
     Separator only. This is the NYT / Bloomberg
     / WSJ / ET pattern.

SCROLL 4 ......................................... long-form

  DEEP DIVES                                       ›
  Long reads, picked for what moved today
  ─────────────────────────────────────────────────

 ┌─────────────────────────────────────────────────┐
 │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ IMAGE ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
 │▓ ( Because Zepto moved today )                 ▓│
 │▓                                               ▓│
 │▓  ZEPTO                                        ▓│
 │▓  Zepto's dark store maths, three years on     ▓│
 │▓                              12 MIN · 14 MAR  ▓│
 └─────────────────────────────────────────────────┘

   ┌──────────────────┐  ┌──────────────────┐
   │ LENSKART         │  │ MEESHO           │
   │ Lenskart's       │  │ Why Meesho went  │
   │ offline bet      │  │ horizontal       │
   │                  │  │                  │
   │ 29 Jun  ▼12%     │  │ 14 May  ▲8%      │
   └──────────────────┘  └──────────────────┘
   ^ the delta is the point: the article is
     static, the number is not.

SCROLL 5 ......................................... close

  PAST BRIEFS                                      ›
  ─────────────────────────────────────────────────
   ┌──────────────┐ ┌──────────────┐ ┌───────
   │ ▓▓▓▓▓▓▓▓▓▓▓▓ │ │ ▓▓▓▓▓▓▓▓▓▓▓▓ │ │ ▓▓▓▓▓▓
   │ Mon 25 Aug   │ │ Sun 24 Aug   │ │ Sat 23
   │ 8 · 5 min ✓  │ │ 8 · 5 min    │ │ 8 · 5
   └──────────────┘ └──────────────┘ └───────

 ┌─────────────────────────────────────────────────┐
 │  ⌂ Brief        ⊞ Explore       ⚑ Watchlist     │
 └─────────────────────────────────────────────────┘


===============================================================
B. BRIEF CARD — ANATOMY
===============================================================

 ┌─────────────────────────────────────────────────┐
 │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│ 1
 │▓ (●) 312 reading now                           ▓│ 2
 │▓                                               ▓│
 │▓                                               ▓│
 │▓  8 STORIES  ·  5 MIN  ·  FILED 7:00 AM        ▓│ 3
 │▓  Thu, 25 June                                 ▓│ 4
 └─────────────────────────────────────────────────┘
   ▪ HEALTHTECH                                      5
     Healthify merges with US-based Berry Street     6
   ───────────────────────────────────────────────    7
   ▪ FINTECH
     Slice adds ex-SBI, ICICI execs to its board
   ───────────────────────────────────────────────
   ▪ DEEPTECH
     NVIDIA price hike hits India's compute cos
   + 5 more inside                                    8
 ┌─────────────────────────────────────────────────┐
 │           OPEN TODAY'S BRIEF              →     │ 9
 └─────────────────────────────────────────────────┘

 1  Feature image. Sized for hero use, not a scaled
    thumbnail. Thumbnails pixelate here today.
 2  Live signal. Only renders above a floor, never
    "3 reading now".
 3  FINITENESS. This line is the whole point of the
    card: bounded, timed, and already filed.
 4  The edition, named by date. Brief owns "today".
 5  Sector tag, primary or secondary only.
 6  Headline, 2 lines max.
 7  Separator, not a container. The 3 rows must read
    as three distinct stories, which they do not
    today.
 8  The remainder, stated small. Reinforces finite.
 9  One action. The only button on the page.


===============================================================
C. BRIEF CARD — THE FOUR STATES
===============================================================

NOT STARTED                    IN PROGRESS
┌───────────────────────┐      ┌───────────────────────┐
│▓▓▓▓▓ image ▓▓▓▓▓▓▓▓▓▓▓│      │▓▓▓▓▓ image ▓▓▓▓▓▓▓▓▓▓▓│
│▓ (●) 312 reading now ▓│      │▓ ▪▪▪▪░░░░  4 OF 8    ▓│
│▓ 8 STORIES · 5 MIN   ▓│      │▓ 4 LEFT  ·  2 MIN    ▓│
│▓ Thu, 25 June        ▓│      │▓ Thu, 25 June        ▓│
└───────────────────────┘      └───────────────────────┘
│ 3 preview rows        │      │ next 3 unread rows    │
│ OPEN TODAY'S BRIEF  → │      │ CONTINUE — CARD 4   → │
└───────────────────────┘      └───────────────────────┘

DONE                           NOT YET FILED (pre 7 AM)
┌───────────────────────┐      ┌───────────────────────┐
│▓▓▓▓▓ image ▓▓▓▓▓▓▓▓▓▓▓│      │                       │
│▓ ✓ DONE  ·  DAY 12   ▓│      │   Tomorrow's brief    │
│▓ 8 STORIES · 5 MIN   ▓│      │   lands at 7:00 AM    │
│▓ Thu, 25 June        ▓│      │                       │
└───────────────────────┘      │   ◷ NOTIFY ME         │
│ what you missed rows  │      │                       │
│ YESTERDAY'S BRIEF   → │      │ Yesterday's brief   › │
└───────────────────────┘      └───────────────────────┘

Why IN PROGRESS matters: median session is 75-78 sec
against 8.4 cards. People leave mid-deck and return.
That state is not a nicety, it is the common case.


===============================================================
D. THE FOUR CARD STYLES, SIDE BY SIDE
===============================================================

 1 HERO              2 MID              3 ROW
 ┌────────────────┐  ┌──────┐ TAG       TAG        4 MIN
 │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│  │▓ img │ Headline  Headline over
 │▓ TAG    6 MIN ▓│  │▓▓▓▓▓▓│ over two  two lines here
 │▓ Headline     ▓│  └──────┘ lines     ─────────────
 │▓ over 2 lines ▓│  ─────────────
 └────────────────┘
 1 per section       positions 2-3      everything else
 contained           contained thumb    NO container
                     only               separator only

 4 CAROUSEL
 ┌──────────┐ ┌──────────┐ ┌────
 │          │ │          │ │
 │  item    │ │  item    │ │  ← peek is mandatory
 │          │ │          │ │
 └──────────┘ └──────────┘ └────
 home only. Breaks the vertical monotony.


===============================================================
E. WHAT THIS FIXES, AND WHAT IT DOES NOT
===============================================================

FIXES
- "Brief" word missing at top            -> section label
- 3 articles indistinguishable           -> tag + rule per row
- Page too finite, 2-3 scrolls           -> 5 scrolls of depth
- Carousel not visible                   -> peek by default
- Cards bulky / too much containment     -> only hero contained
- Thumbnails pixelate in hero            -> separate image size

DOES NOT FIX, needs a separate call
- What rule actually fills MOVING TODAY and DEEP DIVES.
  The slots are drawn; the selection logic is not chosen.
- Whether the feature image is available at hero resolution
  for every edition. If not, hero style cannot be the default.
- The A/B variant. This is variant A. Variant B still needs
  a different hypothesis, not a restyle.
