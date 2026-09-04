# Inc42 app — how the surfaces should work
UX model, not visual design. Written 4 Sep 2026.
Sources: app PRD, post-launch behaviour (189 users, 12–20 Aug), the 28 Aug V2 scope lock,
the 1 Sep Explore companies session, and the two 4 Sep design sessions.

---

## 0. THE ONE RULE THAT REMOVES MOST OF THE CONFUSION

Today the app has five different interaction patterns: tap-through stories, a scrolling
article feed, an expanding company list, an expanding company page, and a watchlist. That
is what "too many interaction patterns, high cognitive load" actually means.

**Reduce to two primitives. Everything in the app is one or the other.**

| Primitive | Gesture | Bounded? | Used by |
|---|---|---|---|
| **DECK** | Tap right / swipe left to advance | Yes, finite and counted | The Brief story cards |
| **FEED** | Vertical scroll | No, infinite | Explore articles, Explore companies, Watchlist, company page |

Consequences that follow automatically:
- A deck always shows position and remaining. A feed never does.
- A deck always has a forward affordance. A feed never needs one.
- Nothing is half-deck-half-feed. The company card that expands in place inside a feed is
  the one violation today and it should become a normal feed row that opens a page.

---

## 1. WHAT EACH TAB OWNS

| Tab | Owns | Never does |
|---|---|---|
| **Brief** | TIME. Today, and the days before it. | Never open-ended browsing |
| **Explore** | BREADTH. Everything we have ever published, and 74,388 companies. | Never named by recency. No "Latest", no "Today's news" |
| **Watchlist** | MINE. The things this reader chose. | Never a discovery surface |

**Brief owns the word "today".** No other surface may use recency in its name, or users
cannot tell Brief and Explore apart. This is the single most common naming mistake and it
has already appeared twice in drafts.

---

## 2. BRIEF PAGE

### 2.1 What it is
The habit. A reader opens it once a morning, finishes, and leaves satisfied. It is
deliberately finite. Finiteness is the product, not a bug.

### 2.2 The tension to design against
Finiteness drives completion but caps session time. The 4 Sep decision was to keep Brief
as home and **extend the page to 4–5 scrolls** rather than 2–3, by adding depth *below* the
brief, not by making the brief itself longer.

### 2.3 Page structure, top to bottom
1. **Header** — greeting, date, streak, profile. Compact. It currently out-shouts the brief card.
2. **Brief card** — the single entry point into today's edition.
3. **Past briefs** — horizontal rail. Calendar strip is removed; past briefs stay behind a small control until usage justifies more.
4. **Exploratory sections** — this is the new depth. Locked on 28 Aug as "main brief card, then past brief, then some other section that helps as an exploratory field."

### 2.4 Brief card states
| State | What it shows | CTA |
|---|---|---|
| Not started | Date, edition time, story count preview, 3 headline rows | Open today's brief |
| In progress | Same, plus position ("you were on 4 of 8") | Continue where you left off |
| Completed | Same, marked done, plus the completion summary | Re-open, or go to yesterday |
| No brief yet (before 7 AM) | Tomorrow's promise and the time it lands | Notify me |

The in-progress state matters more than it looks: median session is 75–78 seconds against
8.4 cards, so a meaningful share of readers are leaving mid-deck and returning.

### 2.5 What the exploratory sections must be
Not content buckets, which go stale. **Each section is a rule that re-runs daily against
content we already own.** A section that cannot fill does not render at all. Hide beats pad.

Two that work:
- **Company-cut of today's news.** Same day's stories, re-cut by company, each card stating in six words or fewer what happened to that company. If that line cannot be generated, the company does not appear. This is not a duplicate of the brief: the brief answers *what happened*, this answers *who it happened to, and can I track them*.
- **Long-form, selected by today's news.** The archive never changes; the selector re-runs daily. A company that moved today surfaces its deep dive, with the connective line stated.

Rule for both: personalisation is **ordering and a badge on the card**, never a filter on the
section. Filters can return zero. Ordering cannot.

---

## 3. STORY CARDS (inside the Brief)

### 3.1 The interaction
A deck. Tap right or swipe left to advance, tap left to go back. Segmented progress at top.
No timed auto-advance — readers finish text at very different speeds and forcing it moves
the drop rather than fixing it.

### 3.2 The actual problem
45–50% of readers never reach card 2. **There is no fatigue curve after card 2** — 80–85% of
those who reach it finish the brief. So this is not fatigue, it is a *learning* problem on
one screen. Card 1 has to teach the mechanic.

### 3.3 What card 1 must do differently
- Carry a visible forward affordance. Every microlearning app that retains ends the card with one; ours ends with nothing.
- Name what comes next rather than saying "next". A headline is a reason; an arrow is not.
- Show the remainder as small and finishable.
- Teach the gesture once, on card 1 only, then get out of the way.
- End above the fold. A card that fills the screen reads as the whole thing.

### 3.4 What comes off the card
| Element | Why |
|---|---|
| "THE DECODE" label | Chrome, no information |
| "30-SEC READ" | Reading-time promise is article copy applied to a card |
| "Read full article" | 9% usage, and it is a one-way door: 94% who open it never return |
| Heart labelled "Rate" | Two taps from the actual control, so nobody reaches it |

### 3.5 The reaction control
One affordance, both halves always visible, single tap, words not icons:
**More like this / Less like this.** Never a verdict on the writer; it is a feed preference.
Collapsed and expanded states use the same control, never a star in one and a button in the
other. The existing negative-reason bottom sheet stays as the second step of the Less path.

### 3.6 Full article
It is a one-way door today. Either give it a designed return path back into the deck at the
same position, or accept that it ends the session and demote it accordingly. Do not leave
it as it is.

---

## 4. EXPLORE

### 4.1 What it is
The breadth surface. Two sub-tabs, Articles and Companies. A reader arrives here either
with an intention ("what raised this week") or with none at all ("what else is happening").
**Both must work without the reader declaring which they are.**

### 4.2 The structural answer
One page, two zones, no mode switch:
- **Top zone** — what is happening. Event-led, a handful of items, for the reader with intent.
- **Below a full-bleed divider** — browse everything. Sections, counts, and a way into the whole archive, for the reader with none.

A mode switch fails because it asks the reader to declare intent before the page will help.

### 4.3 Articles feed
- Home is a **multi-section correlation view**, which then breaks into dedicated section pages.
- **Three card styles per section**: hero, mid-size for second and third, then regular feed rows. **Carousel as a fourth format**, scoped to home.
- **No card containment.** Bottom separators only, bold typography. NYT, Bloomberg, WSJ and ET all do this; containment is what makes ours read bulky.
- Section headers link to a **dedicated section page**, not a filtered feed.
- Ordering is latest-first with **light personalisation weighting**: sectors chosen at onboarding get priority when fresh news exists in them.
- Target: 50% of readers who reach the article section open at least one article, moving to 60–70%.

### 4.4 Companies feed
- Cards are **section-driven, not property-driven.** A priority list supplies which field renders, with fallbacks.
- Values like "undisclosed" never occupy the hero slot; the next-priority field renders instead.
- Two to three prominent sections (Recently Funded, Early Fund Raisers), then a normal listicle feed, with horizontal carousels between them to break monotony.
- **Filters and search are untouched this iteration.** View All opens a dedicated filtered page.
- Full dynamicity is deferred.

### 4.5 The fill-rate rule that makes this work
Data availability is a property of the **section**, not the card. A section defined by "last
round" has a 100% fill rate by construction. A section defined by sector has about 13%. So
**a section's lead figure must be the field that defines that section**, and a section with
no defining field carries no figure at all — the slot is simply absent, and that is the
common case, not an error state.

### 4.6 Conveying scale
Explore must feel like a way into 74,388 companies, not a page about eight of them. Scale is
shown, not stated: counts on every section header, several different axes visible at once
(sector, city, founding year, type, A–Z), and rails that visibly run off the right edge.

---

## 5. COMPANY PAGE

### 5.1 What it answers
"Why is this company in my feed, and should I track it." It is a news reader's company page,
not a Tracxn competitor.

### 5.2 The constraint
Only 13% of companies are funded at all; 82% have no money data. Present for 100%: logo,
name, sector, sub-sector, city, founded year, company type, description, website, socials.
**The data-poor profile is the default case and is designed first.**

### 5.3 One shell, four fills
Template chosen by the `signals_count` integer the API already returns. No per-field null
checking at runtime.

| Tier | Share | Adds |
|---|---|---|
| 1 | ~half | Identity, full description, Inc42 articles. No numbers |
| 2 | ~28% | Web traffic |
| 3 | ~9% | Funding total, last round, investors |
| 4 | ~13% | Financials, IPO status, acquisitions |

Header, type scale, spacing and block chrome are identical across all four. Only which
blocks appear, and in what order, changes.

### 5.4 Rules
- A block with no data is removed entirely. Never a dash, "N/A", or a greyed placeholder.
- Never a metric grid with holes. If it cannot be filled it becomes a list, or it goes.
- **Editorial is the block that never blanks.** Any company reachable from the news has
  coverage by construction. This is what makes a thin profile feel finished.
- Excluded by product decision, not data gap: headcount, team size, Glassdoor or any rating.

---

## 6. WATCHLIST

The return reason, and currently the least designed surface. Minimum it must do:
- Say why each company is there and what changed since it was added.
- Have a real empty state that explains what tracking does, reachable from any company card.
- Connect to the Brief: a tracked company appearing in today's edition should be marked as
  such, which is what makes tracking feel worth doing.

---

## 7. CROSS-CUTTING RULES

**Missing data**
1. Missing figure means an empty slot of the same size, never a dash or placeholder.
2. Never a labelled field with no value. The label travels with the value.
3. Card height and shape never change based on which data exists.
4. A section that cannot fill does not render. Define the non-render state explicitly.

**Personalisation**
Additive decoration on cards, never a filter on sections. Ordering cannot return zero;
filters can.

**Logged out**
Every surface must be fully readable and fully valuable with no account. Design the cold
state first; personalised states are layers on top. A meaningful share of users are here.

**Copy**
- Never a count that can vary or that a first-time reader cannot parse. Name the product, not the number.
- Cadence is "every morning", never a duration.
- Additive framing only. Never describe content by what the reader did not choose.
- Copy and placeholders must be changeable via the PostHog walkthrough, not a new build.

---

## 8. WHAT EACH SURFACE IS MEASURED ON

| Surface | Primary | Guardrail |
|---|---|---|
| Brief card | Brief open rate | — |
| Story deck | Card 1 → card 2 advance rate | Completion rate |
| Completion screen | Return next morning | — |
| Explore articles | Share opening ≥1 article (50% → 60–70%) | Session depth |
| Explore companies | Company page opens | — |
| Company page | Watchlist adds | — |

---

## 9. DECISIONS STILL OPEN

1. **What fills Brief scrolls 3–5.** Locked as "an exploratory section"; the actual rule is not chosen.
2. **Full-article return path** — designed return, or accept it ends the session.
3. **Does the reaction feed the ranking?** If not, More/Less is theatre and should not ship.
4. **Watchlist has no design owner or ticket.**
5. **Search.** Out of scope this iteration, but it is a known P0. Needs a date.
6. **Dark mode needs a colour token layer first**, or every screen gets built twice.
