# Brief Completion / Gratification Screen Redesign — Full Context

Last updated: 2026-08-29

## Origin

Prompt sent to Satya (with Figma links) asking for a redesign of the brief-completion
"gratification" screen. Core ask: the value promise ("cut the noise, get the brief an
authority already filtered for you") and the gratification shown at completion are two
different things today. Live design shows a static streak hero → "Amazing Start! Think
You Can Do It Tomorrow?" → Explore Trending Stories carousel, identical every day, so it
stops registering by day 4–5.

Original spec: design 4–5 rotating gratification "modes" pulling from different real
data (median completion 78s, avg 8.4 cards/brief), cycled deterministically (day-of-week
or session count), each with explicit template + data-field requirements so it can be
wired to real numbers instead of shipping as flavor text.

Working file (view/edit as access allows): **App - Draft Screen**
`https://www.figma.com/design/dAsaTgNj0xh25w2OGaurZo/App---Draft-Screen`
All exploration for this project lives on this one file/page — deliberately kept off the
live `Inc42-App-2026` file and off any page other people are actively using.

## Figma access saga (resolved)

- Figma MCP was stuck on "Ranjith M's team" (Starter/View — read-only) even after
  Utkarsh approved a Full/Dev seat on the "Inc42" org team.
- Browser session (Claude in Chrome) was *also* read-only on the live team file — the
  "Ask to edit" button was the tell; Share button/Properties panel are visible to
  viewers too, so don't use those as an edit-access signal.
- Seat access eventually propagated; `whoami` now shows Inc42/Full/Pro. Confirmed
  working via a live `createFrame` test on the draft file.
- The draft file (`dAsaTgNj0xh25w2OGaurZo`) is personally owned/editable regardless of
  team seat status — this is why all builds happened there.

## Round-by-round build history (what was tried, what happened)

**V1 — first pass.** 5 rotating modes (time/effort, curation/authority, streak/identity,
personal relevance, cumulative weekly), plain white ring + number, spec cards underneath
with template strings + data fields. Functional but not evaluated for "compelling."

**Psychology + Mobbin research (round 1).** Grounded in Fogg Behavior Model, Nir Eyal's
Hook Model (variable rewards of "self"/mastery), Kahneman's Peak-End rule, Self-
Determination Theory (competence), loss-aversion/streak-anxiety risk, and
specificity-of-feedback research (generic praise underperforms specific claims).
Mobbin: plain circle-with-number reads as the *generic default* — strong examples use a
distinct badge/medallion shape, multi-stat breakdowns, motion-implying celebration
energy (confetti/bursts), personalized copy, and comparison baselines.

**V2 — badge + burst.** Scalloped star-shaped medallion (28-point star, 0.93 inner
radius) with radiant burst rays + confetti dots behind it, white-on-orange. **User
verdict: looks like a "Rakhi"** (festive Indian ornament), not a modern achievement
token. Badges that appear *daily* stop reading as special.

**Research round 2 (impact/anticipation).** Badge-shape research confirmed: premium/
non-childish apps use bold oversized numerals with no ornamental frame for *daily*
(non-milestone) moments. Anchoring-effect + precision research: specific numbers beat
round ones, but a number that *feels* invented backfires harder than a modest honest
one. Curiosity/anticipation research (Loewenstein information-gap, Duolingo forward-
prompt data) supported adding a forward-pull, but a fabricated specific-story teaser
("Tomorrow: Ola-Uber pricing war escalates") is infeasible — news outlets can't predict
tomorrow's actual news the way Duolingo can promise lesson content.

**V3 — 4 impact-framing variations**, no badge: (A) huge editorial numeral, (B)
manual-research-vs-brief comparison bars, (C) 4-stat fact ticker, (D) numbers embedded
in a narrative sentence with rich-text highlighting. **User verdict:** concept-level
failure, not just visual — "47 articles, 15 sources" wrongly implied Inc42 is a news
*aggregator*; it's actually an original publisher. Real framing should be "N published
today → 8 personalized for you." Fact-ticker style (C) was liked structurally.

**V4 — converged hero.** Dropped aggregator language, added a large ring (tiny bright
sliver = 78 sec "you," mostly-muted full ring = ~73 min "manual") with an explicit
legend, "56× faster" verdict stated only after both quantities were established,
"15 published → 8 personalized, not aggregated" stat chips, honest routine-based
forward-pull ("Next brief · Tomorrow, 8 AM") replacing the fabricated story-teaser.
**User verdict: confusing** — "56×" and "78 seconds" had no clear referent on first
read; fixed by adding a plain-language setup sentence before any numbers, explicit
ring legend, and moving the verdict statement to *after* the numbers were explained.

**V5 — 8 visual-language variations** (content held constant): minimal editorial type,
refined ring w/ pills, full-width bars, split before/after panel, dark-navy premium,
icon-clock metaphor, black/amber terminal-dashboard, conversational speech-bubble.
Mid-round correction: **the ring itself is being read as a *progress* indicator** (per
universal UI convention: filled = done, empty = remaining) — a 4.5%-filled sliver
therefore reads as "you only did 10%," which fights the entire point of a completion
screen. This is a structural bug, not a color/copy issue.
**User verdict:** dark-navy variant "weird" (off-brand color jump); explicit copy like
"We cut the noise" and "Handpicked, not algorithmic" undercuts its own point — **show,
don't tell**. Also flagged: "cut the noise, get the brief" (the *original* value prop)
had drifted out of the copy entirely somewhere in the iteration.

**Research round 3 (show-don't-tell + single-hue craft).** Show-don't-tell principle:
state outcomes ("you're caught up"), not effort/process claims ("we did X for you");
surface a *shown artifact* (real recognizable content) instead of an abstract process
stat. Visual-craft principle: premium single-accent apps (Linear, Arc) build depth from
luminance/tint steps *within one hue*, never by swapping to an unrelated color family.

**V6 — one converged screen.** Single warm-hue "surface ladder" (deep maroon base → mid
burnt-orange → warm peach highlight) via a radial gradient — deliberately *not* navy.
"YOU'RE CAUGHT UP." (outcome-state) + real topic-name chips (shown artifact) instead of
"handpicked" claims. Ring kept, but verdict sentence dropped — just the plain fact
("78 sec — you, just now" / "~73 min, usually"). **User verdict, mixed:** liked the
single-hue palette direction ("it is sorted"). Two new critical structural problems
surfaced: (1) **the ring-reads-as-partial-progress bug** (see above) was still
unresolved — "only a few portion is highlighted... not giving a sense of completeness";
(2) wanted **social proof from same-domain peers** added, and wanted the sector names
actually covered in the brief stated in the "caught up" line, not left generic.

**V7 / W1–W4 — 4 completeness-fix variations**, same palette: (W1) fully-closed ring +
checkmark, (W2) solid filled badge/stamp + checkmark, (W3) 100%-filled progress bar +
label + checkmark, (W4) grid of 8 individually-checked story cards. All four added a
sector-named headline ("You're caught up on Fintech & E-commerce"), illustrative peer
social-proof line ("2,400+ in Fintech caught up today too"), and demoted the time stat
to a small secondary caption. **User verdict:** color had drifted from the *actual*
brand orange (#EA4B2B, matching the live app) into an invented maroon — needs to revert
to real brand color, not further "premium" reinterpretation. The achievement/time-saved/
authority *feeling* had been demoted so far it now read as absent — overcorrection.
Social-proof line ("2,400+ in Fintech") felt abstract/unrelatable. W3 was cluttered
(bar + "100%" label + checkmark all saying "done" redundantly). W4's 8 identical
checkmark cards were repetitive/uninformative (no distinguishing content per card).
Overall: too many simultaneous changes, "not so much convinced" — asked for a **written
plan before any further building**.

**Plan-first round.** Proposed 5 *described-only* variations, each adding some form of
Inc42 brand/authority mark alongside a completion shape: Masthead Seal, Newsroom Byline
Card, Masthead Header Bar, Stat Ledger (receipt-style itemized stats), Sealed Stamp
(monogram+checkmark fused). User asked for real reference precedent for each via Mobbin,
plus wanted the social-proof line reworked into something "more dynamic."

**Reference research round 1 (Mobbin, first batch).** Careem scalloped gold seal, Uber
verified badge, NYTimes inline photo-credit byline, Matter "Text by" byline, Finimize
"THE DAILY BRIEF" masthead banner (closest category match — same business-news-brief
genre as Inc42), Instacart/Starbucks receipt screens, Honest Greens wax-seal monogram,
Speak graduation-cap medallion, Duolingo "#9 last week" personal-rank screen, Brilliant
league leaderboard. Key finding: **dynamic social proof ≠ a bigger static number** — the
real pattern is *relative/comparative personal standing* (Duolingo's own-rank-over-time),
not a live headcount (TikTok-style live-viewer counts don't fit non-live content).
Opened all 11 in Chrome for direct review.
**User verdict:** liked Honest Greens (wax seal), Careem (seal), Speak (medallion),
Duolingo (personal rank). Rejected NYT byline-credit idea entirely. Rejected Brilliant's
*public* leaderboard specifically (too competitive/gamified for this audience) while
keeping Duolingo's *personal* rank-over-time idea. Asked whether other/different
players had been checked — existing set skewed toward casual consumer-lifestyle apps
(Careem, Uber, Starbucks), tonally off for a professional business-news product.

**Reference research round 2 (Mobbin, broader/professional-context batch).** Flo
(ISO-certified shield+ribbon crest), **Monarch** ("Great work! You're all caught up on
your financial progress for July" — checkmark + confetti, personal-finance app, closest
register match found so far), Cash App (plain checkmark, no ornament), Strava (personal-
record badge, no other people shown), Hevy ("You are stronger than 48% of male lifters
your age and bodyweight" — percentile vs. an aggregate, no visible leaderboard), Runna
(personal-bests hexagon grid), **Commons** ("ALL DONE. SEE YOU BACK HERE NEXT WEEK,
SAM." — personalized sign-off, newsletter/insights app, no gamification), Blinkist
(plain "mark as finished," weaker precedent). Opened 6 of these in Chrome.
**User verdict — decisive:** only **Monarch** "still somehow makes sense." Hevy
(percentile/deadlift stat), Flo (ISO crest), and Cash App ("investing 40%... empty and
wide space") all explicitly rejected as not making sense / feeling empty. Strong meta-
feedback that the reference search itself had lost the plot — pulling isolated visual
patterns (badges, percentiles, crests) rather than understanding what the screen
actually needs to *say*.

## V13 — make the AVOIDED EFFORT visible (the breakthrough round)

Diagnosis that unlocked it: every prior round showed the *result* (8 stories, caught up)
but never showed *what the reader escaped*, so effort-saved stayed an abstract caption
number. Five builds: (A) Pile vs Pick — 15 faded ragged rows collapsing to 8 clean ones;
(B) **Time as Physical Mass** — a 510px muted column vs a 14px bright sliver, baseline
aligned, so the scale occupies real screen space instead of being read as text;
(C) **Labor Ledger** — "While you were asleep / Our newsroom did the reading" + itemised
work + "Filed 6:00 AM · Inc42 newsroom" signature; (D) struck-through chore list of what
you skipped; (E) tangled scribble vs one straight arrow (built, but the scribbles came
out as smooth parallel waves — reads decorative, weakest of the five).
**User verdict:** B and C are the direction. A explicitly rejected ("not able to relate
what is that"). Asked for C's newsroom message to be **more concise**, delivered with
B's visual force — and, critically, for the **streak to be stitched in as the reward**:
"this is what you have done, and as a reward, we are giving. Your streak also increases."

## V14 — the stitched three-beat arc (current direction)

Narrative locked as: **we did the work → here's what it saved you → here's what you
earned.** Streak is now the *consequence* of finishing, shown ticking up in front of the
user (+1 today / 3 → 4), not a separate widget bolted on. Three builds:
- **V14-1 Stitched Narrative** — newsroom line, then the time-mass columns, then Day 4 +
  week dots. Reads top-to-bottom as one story.
- **V14-2 Reward First** — inverts it: streak "3 → 4" is the hero, week dots, then a
  compact "HOW YOU GOT HERE" proof table (read 15 / kept 8 / 78 sec / ~73 min).
- **V14-3 Three Beats** — explicit `WE DID` / `YOU SAVED` / `YOU EARNED` section labels,
  hairline-separated, most legible structure, horizontal bars for the time contrast.

## V15 / V16 — the 3-beat flow (current direction)

Clutter was diagnosed as a symptom of forcing the whole arc onto one static screen, so
it became a **flow**: `1 · THE MOMENT` → `2 · THE VALUE` → `3 · THE REWARD`.

Two things the user said were missing and are now the spine:
- **Effort + authenticity.** Not "15 published". The alternative is not merely slower, it
  is *unverifiable* — the cost line reads "hunting across tabs — and sources you can't
  vouch for", against "Reported first-hand. Checked before it reached you."
- **Coverage completeness per opted-in sector.** Counted per sector (Fintech ✓ 5 /
  E-commerce ✓ 3), so "this is what I asked for and I got all of it" is legible, with
  "+N more worth knowing" for stories beyond the followed sectors.

**V16 refinements after the user said V15-2 still wasn't compelling and V15-3's reward
had no comparison:**
- **Derive the number, never assert it.** V16-2 itemises work the reader recognises
  doing — check six news sites 22 min / sort the PR from real news 18 / check who's
  actually funded 15 / work out what it means 18 — and lets the 73 min total build
  itself, then flips to a white card: "WITH INC42 / 78 seconds." The list doubles as the
  authenticity argument, shown as labour rather than claimed.
- **The streak must buy something.** V16-3 converts the streak into cumulative time
  returned: "Four mornings has bought you 4 hrs 52 min of your own mornings, back",
  with the arithmetic shown (73 min × 4 days), plus a forward hook ("a full day back
  before the month is out"). Streak alone was a number going up; this gives it meaning.
- **Quiet-sector edge case handled** (V16-1): a followed sector with no news renders as
  "Cleantech — quiet today" with a dash instead of a tick, and is framed as valuable:
  "Cleantech was quiet today — that's worth knowing too."

## V17 — story rail, earlier streak, and solving the daily-repeat problem

- **"+2 more worth knowing" became a story rail.** The uncovered/lower-relevance stories
  now render as tappable Instagram-style circles with unread rings (PhonePe, Meesho,
  Zepto, Smartworks) and a "tap to flick through the rest of today" hint. Tapping opens
  a full story viewer (V17-2): segmented progress bar, company header, "OUTSIDE YOUR
  SECTORS" tag, headline + standfirst, "Read the full story", swipe for next. This turns
  the leftover news from an announcement into a browsable surface.
- **Streak moved onto beat 1** as a compact strip (7 small dots + "DAY 4" + gold "+1"),
  so gratification starts at the moment of completion rather than waiting for beat 3.
  Beat 3 still carries the full streak + cumulative-hours payoff.
- **The daily-repeat problem.** The V16-2 itemised ledger is too heavy to show every
  day — it becomes a **weekly / milestone** screen. Beat 2 daily gets lighter rotating
  framings instead: **2a effort** ("6 hours of reporting → 78 seconds of yours. That's
  the trade.") and **2b verification** ("Every number in today's brief was checked" —
  funding figures verified 6 / claims sourced on record 4 / numbers corrected
  pre-publish 2, signed Inc42 Newsroom). Each mode needs a real backing field
  (reporting hours, claims checked, corrections) or that mode must not fire that day.

## V18 — the rail is SECTORS, with segmented rings

- **"Also worth knowing" is sector-level, not company-level.** The rail answers "what
  happened in the sectors I don't follow" — Travel Tech, Healthtech, SaaS, D2C — rather
  than naming individual companies. Header reads `ELSEWHERE TODAY` / `10 STORIES`.
- **Segmented rings: one arc per story.** A sector with 3 stories renders as a 3-segment
  ring, 4 stories as 4, 1 story as a near-full ring — so story volume per sector is
  countable at a glance before tapping, using the familiar unread-story-ring convention.
  Implemented with `ellipse.arcData` (startingAngle / endingAngle / innerRadius), one
  ellipse per segment with a small angular gap between them.
- **Drawn sector icons** (vector, no asset dependency): paper plane = Travel Tech, plus =
  Healthtech, stacked layers = SaaS, shopping bag = D2C. Note: the first bag attempt read
  as a padlock — fixed by making the body a trapezoid (wider at top) with the handle arc
  clear above it. Any new sector icon needs the same read-check.
- **Inc42 masthead** added at the top of beat 1 (wordmark, letter-spaced, hairline rule
  beneath), so the branding sits on the screen without a badge or seal.

⚠️ **Compounding-estimate risk:** the weekly "4 hrs 52 min" multiplies the unverified
~73 min figure by the streak length, so any error in the base estimate is amplified and
displayed far more prominently. Measure ~73 min before shipping any cumulative version.

## Earlier hypothesis (superseded by V13/V14)

The one thing that worked (Monarch) has **no badge, no seal, no percentile, no
comparison stat, no forward-pull chip, no social-proof line** — just a plain checkmark
and one warm, complete, specific human sentence. Proposed next direction, stated but
**not yet built or confirmed**:

- Plain checkmark. No medallion/seal/ring-as-metaphor.
- One warm, complete sentence naming the actual sectors covered that day — e.g.
  *"Nicely done. You're caught up on Fintech & E-commerce — today's 8 stories, in your
  own words."*
- Nothing else competing for attention: no time-saved stat, no peer count, no
  percentile, no forward-pull pill. Deliberately smaller/calmer than every prior round.

**Open question the user has not yet answered:** whether dropping the time-saved /
effort-saved / authority-signal entirely (as Monarch does) loses something Inc42
specifically needs, or whether the plain-sentence approach can carry all of that
implicitly through wording alone.

## Standing facts / constraints to remember

- Inc42 is an **original publisher**, not an aggregator — never frame value as
  "N sources" or "N articles aggregated." Correct frame: "N published → M personalized
  for you."
- Real analytics data available: median brief-completion time **78s**, average
  **8.4 cards/brief**. Everything else (73 min manual-research comparison, 56× multiplier,
  2,400+ peer counts, 15-published/8-personalized figures, sector names, social-proof
  numbers) used so far is **illustrative placeholder data**, explicitly flagged each
  time, pending real numbers from Inc42's content pipeline / analytics / follow-graph.
- Brand color is **#EA4B2B** (bright orange→red gradient, as seen in the actual live
  app) — do not invent a different hue family (navy, deep maroon) for "premium" effect;
  depth should come from tint/shade steps within that one hue if needed at all.
- Explicit process-claim marketing copy ("We cut the noise," "Handpicked, not
  algorithmic," "56× faster than doing it yourself") consistently reads as undermining
  its own point. Prefer outcome-state language and shown artifacts over asserted claims.
- A ring/donut visual with only a small arc filled reads as **incomplete progress**,
  not "fast completion" — this metaphor is structurally wrong for a completion screen
  and should not be reused in this form.
- Gamification mechanics tested and explicitly rejected by the user: scalloped/star
  medallion ("Rakhi"), public leaderboard, percentile-vs-strangers stat, ISO-style
  certificate crest, generic ornamental badges.
- All exploration must stay on the **App - Draft Screen** file only — never on the live
  `Inc42-App-2026` file or any page other collaborators are using.
