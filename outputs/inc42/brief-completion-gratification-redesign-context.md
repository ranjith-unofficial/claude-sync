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

## V19 — the report-card pattern (from a Cult.fit reference)

Reference supplied by Ranjith: a Cult.fit post-class "Reports" screen — session header
(class name, date, duration), a dark card carrying a logo-in-burst, "You did great
today!", a 2×2 stat tile grid (duration / class rank / energy score / calories), and
SHARE YOUR ACHIEVEMENT as the primary CTA. Saved at
`~/Downloads/WhatsApp Image 2026-08-29 at 20.48.01.jpeg`.

What was borrowed, and what was deliberately not:
- **Achievement lives on a distinct CARD**, an object sitting on the page rather than
  being the page — a deep-ink card on the brand orange, which also supplies the depth
  and contrast earlier rounds kept asking for.
- **2×2 stat tile grid** carries several dimensions at once instead of one hero number:
  READ TIME 78 sec / STORIES READ 8 / SECTORS COVERED 2 of 2 / DAY STREAK 4 (streak
  tinted gold). This is the most direct answer to "tell me what I achieved".
- **Session-record framing** — "TODAY'S BRIEF · FRI 29 AUG · 8 STORIES" gives it the
  quality of a record you accumulate.
- **Sharing was NOT copied wholesale.** For a founder/VC audience "I read the news" is
  not socially shareable — it signals nothing. So the daily card's CTA is *Save today's
  report* (private record), and the SHARE flow is reserved for **streak milestones**
  (day 7 / 30 / 100), where diligence is the thing actually worth signalling: a portrait
  orange asset — "30 MORNINGS / Nothing that mattered in Indian startups got past me" +
  Inc42 wordmark — with WhatsApp / LinkedIn / X / Copy targets.

## V20 / V21 — the current lead design

**V19 (the Cult.fit-style report card) was rejected:** a dark card on orange went muddy,
a 2×2 tile grid read as a dashboard rather than a reward, and nothing gave a reason to
return. Three fixes established in V20 and carried forward:
1. **One glowing focal element**, never a grid of equal tiles. Stats demoted to a thin
   inline row (78s · 8 · 2/2) — they are context, not the event.
2. **Luminosity needs contrast** — a bloom/glow behind the hero.
3. **Something visibly UNFINISHED** as the return hook, with a named unlock.

**V21 is the current lead** (`94:4`), built from V20-C and translated to brand colour:
- **The week ring IS the hero** — 7 segments, 4 lit white with a bloom on today's, 3 left
  at low opacity. The incompleteness is the pull, and it doubles as the achievement.
  Centre reads "4 / OF 7 MORNINGS".
- **Brand orange radial-gradient ground**, not dark ink.
- **Radial ray lines removed** — Ranjith: they "don't make a lot of sense". They were
  decoration carrying no information. Light confetti retained, kept away from the ring.
- **The missed-sector rail lives on the SAME screen** — `ELSEWHERE TODAY · 10 STORIES`,
  one segmented ring per sector (Travel Tech 3 / Healthtech 2 / SaaS 4 / D2C 1), so the
  reward and the stories you missed are a single moment.
- **Named unlock**: "UNLOCKS SUNDAY — Your first weekly recap · 3 to go".

Icon note: the D2C shopping-bag icon read as a **padlock** at 42px (second time this
happened — also in V18). Replaced with a parcel (white box + two ribbon lines in the
background orange). Always render-check small icons at actual size.

⚠️ **The weekly recap is currently a promise with nothing behind it.** If the unlock hook
ships, that recap must exist by day 7 — a broken unlock costs more trust than never
promising one.

## V22 — solving the read-time measurement problem

**The problem Ranjith raised:** measured read time is fragile to compute. A user opens
the brief, backgrounds it, comes back, reads a few cards, leaves, finishes later.
Stitching that into an honest per-user number is hard, easy to get wrong, and easy to
inflate accidentally.

**The fix: stop measuring the user, measure the content.** Every metric below is computed
at publish time from the articles themselves — identical for every reader, no timers, no
session stitching, no backgrounding edge cases:
- **Word counts** — exact, already in the CMS. `12,400 words published → 840 in your brief`.
- **Reading-time estimates** — the standard words-per-minute convention every publisher
  already uses ("5 min read"). Label it as an estimate, never as a stopwatch.
- **Compression ratio** — derived from the two word counts, so it needs no new data.
- Only **editorial hours** (the "6 hrs reporting" framing) needs a new field editorial
  would have to track; everything else is already computable today.

This is also a *better* number than measured read time, because it describes the articles
rather than the reader: bigger, defensible, and the same for everyone.

**Five treatments built (V22-A…E), identical screen, only the value block differs:**
- **A · Words Condensed** — two stacked bars, 12,400 vs 840 words, "Same day. 15× fewer words."
- **B · Reading Estimate** — `47 min → 90 sec`, with the honest footnote "estimated from
  word count — not a stopwatch".
- **C · Editorial Effort** — `6 hrs reporting / 47 min of writing / 90 sec for you` +
  "Our newsroom did the reading, and handed you the short version." Best expression of the
  editorial-labour framing, but needs the reporting-hours field to exist.
- **D · Compression Ratio** — `15×` as a hero stat, word counts as the supporting line.
- **E · Proportion Bar** — one track for everything published with a bright sliver for the
  brief: "You read the 7% that mattered." Most intuitive at a glance.

## V23 — stakes not effort, ring-framing options, real icons

**1. New value line: STAKES, not effort.** Every prior attempt measured the *cost avoided*
(time, words, newsroom hours). For a founder/VC the more persuasive thing is what they now
KNOW — the size of the activity they are on top of: **"₹2,400 Cr of funding news in your
sectors · 3 IPO filings · 2 acquisitions · 8 stories."** Crucially this needs no new
tracking and no timing of the user: funding amounts, IPO filings and acquisitions are
already attached to articles in DataLabs. Alternative framing built as R5 — consequence:
*"Skip a morning and you'd have missed 3 funding rounds in the sectors you follow —
worth ₹2,400 Cr."*

**2. Ring-centre framings built for comparison** (ring geometry identical, 7 segments,
4 lit — only the centre label changes):
- **R1** `4 / DAY STREAK` — streak only
- **R2** `4 / OF 7 THIS WEEK` — week progress (the V21 original)
- **R3** `3 / MORNINGS TO GO` — remaining framing
- **R4** `4 / DAY STREAK` + `4 of 7 this week` — both, streak leading
- **R5** `4 / DAY STREAK` + a `BEST · 12` pill — adds personal record as a second
  gratification dimension
Note the ring itself always encodes the WEEK; only the number's meaning changes. R4 is the
only one where the number and the ring can disagree once a streak exceeds 7 days — needs
a rule for streak > 7 (ring stays weekly, number keeps climbing).

**3. Real icons.** Sector icons are now genuine **Lucide** icons (ISC-licensed) — plane,
heart-pulse, cloud, shopping-bag — fetched from the pinned CDN
(`unpkg.com/lucide-static@0.544.0/icons/<name>.svg`) and rendered via
**`figma.createNodeFromSvg()`**, then `rescale()`d and centred. Important technique note:
Figma's `vectorPaths` parser rejects both commas and arc (`a`) commands, so hand-passing
SVG path data fails — `createNodeFromSvg` handles full SVG properly and is the right tool
for any real icon set.

**4. Copy:** "ELSEWHERE TODAY" → **"WHAT ELSE MOVED TODAY"**.

## V24 — Ranjith's edit to R5, and fixing the "BEST" pill

**Ranjith edited V23-R5 directly in the file.** His changes: deleted the entire middle
value block (the consequence copy), deleted the second divider rule, and pulled the sector
rail, unlock card and footer up (rail label 582→454, unlock 722→594). Result is a much
tighter screen: ring → headline → sector rail → unlock. **Treat that tightened layout as
the current baseline.**

**The "BEST · 12" pill was broken on two counts:** it is unexplained ("best" of what?), and
it is actively demotivating — on day 4 it tells the reader they have done better before,
at precisely the moment meant to feel rewarding. A static personal-record comparison is
negative for most of its lifetime, since a user is below their record on almost every day.

**Fix: a state-dependent pill that is always positive.** Four states built (V24-A…D), all
cloned from the edited R5 so his layout is preserved:
- **A · Everyday** — `+1 TODAY` (white 18% pill). Immediate reward, no comparison needed.
- **B · Nearing record** — `2 DAYS TO YOUR BEST`, fires only when the record is genuinely
  within reach (≤3 days). Turns the record into a target instead of a shortfall.
- **C · Record day** — `YOUR LONGEST YET` in solid gold with dark text. The one moment the
  record is worth mentioning at all.
- **D · No pill** — 7 week dots instead. Clean, but the dots restate what the ring already
  shows (4 of 7), so it is redundant — weakest of the four.

Recommended: **A as the default, B within 3 days of the record, C on the day it is beaten.**
Never show a bare record comparison.

## W — Welcome / onboarding screen (extending the value story upstream)

The live welcome screen (frame `Frame 1686562350`, in the **Inc42-App-2026** file, not the
draft) reads "Introducing Brief / A Short Read Built Around The Sectors & Topics You
Follow" over a phone mockup, with a PERSONALIZE MY FEED CTA. Problem: "Introducing Brief"
is product-centric and states no value — it names the feature rather than the outcome.

Four replacements built **in the draft file** (row y=23335), to be moved across:
- **W1 · Outcome-led** — keeps the phone mockup, changes the promise to *"Never miss what
  moves your sectors"*, adds a proof strip (8 STORIES / 90s TO READ / Daily AT 8 AM).
  Lowest-risk edit: same layout as today, better words.
- **W2 · Sector-led** — reuses the **segmented sector rings from the completion screen**
  (Fintech / E-commerce / SaaS / Healthtech with Lucide icons). *"Pick your sectors. We'll
  cover all of them."* + the quiet-sector promise + "REPORTED FIRST-HAND BY INC42'S
  NEWSROOM". Strategically the strongest: what you pick at signup is visually the same
  object you are rewarded against every morning, so onboarding and reward reinforce.
- **W3 · Noise → signal** — the pile-to-pick visual (14 faded lines funnelling into 8
  bright ones): *"Everything gets published. Only eight reach you."* Note this visual was
  rejected on the completion screen ("can't relate to it") but works here, because
  onboarding is exactly where you EXPLAIN the mechanism.
- **W4 · Stakes-led** — leads with ₹2,400 Cr and an itemised ledger (funding rounds 6 /
  IPO filings 3 / acquisitions 2 / stories that affect you 8), then *"Know all of it by
  8:01 AM."* Highest-conviction for a founder/VC, but depends on a live daily ₹ figure and
  needs a quiet-day fallback.

## W2 — welcome screens, minimal copy (current set)

**V24 is FINALISED** for the completion screen (state-dependent streak pill on Ranjith's
tightened R5 layout). Welcome-screen work continues from there.

Feedback that shaped this set: too much text kills attention — few words, but impactful;
drop the faint blurred paper/geometric background shapes; and do **not** reuse the same
layout — image and button placement can differ entirely, as long as colour and type stay
on brand. Five built (draft file, row y=24280), each under ~10 words of body copy and no
two sharing a structure:
- **A · The Number** — a 250px "8", then *"stories a morning. That's the whole thing."*
  CTA floats mid-lower, not glued to the bottom.
- **B · Photo Split** — full-bleed photograph across the top 430px with a real headline
  over a scrim, orange lower half, *"Caught up by 8:01."*, and a **full-width black CTA bar
  flush to the bottom edge** (no margin) — the biggest layout departure.
- **C · Sector Grid** — six sector cards (two shown selected in white, four unselected),
  *"Your sectors. Covered daily."* CTA below the grid.
- **D · Type Poster** — no imagery at all: `8 STORIES` / `90 SECONDS` / `0 MISSED` stacked
  as left-aligned rules, the zero in peach. White CTA on orange. Six words total.
- **E · The Card** — a single large tilted brief card with photo, real headline and sector
  tags, floating on orange; *"This. Every morning."* Shows the product with no phone frame.

**Images:** `upload_assets` works — request N upload URLs with `nodeIds`, then POST the
bytes as multipart `file=@...` to each `submitUrl`; the image is placed as a fill on the
target node automatically. Photos in B and E are placeholder imagery (Picsum) and must be
swapped for Inc42's own art before use.

## W3 — welcome screens, research-led (current set)

Ranjith's rejections of the W2 set, all confirmed as real anti-patterns by Mobbin research:
- **"8 stories a morning — what is stories?"** Feature-nouns mean nothing to a first-time
  user. SCMP does exactly this ("five must-read articles curated for you daily") and it is
  the same trap.
- **Hard counts are misleading** — "8 stories / 90 seconds" breaks when a weekly recap runs
  10+. Finimize's "**minutes a day**" is the pattern that never breaks.
- **Pre-selected sector cards were rejected** — every app that shows topic chips (Medium,
  Perplexity, Bluesky) makes it a *real interactive step* with its own Save/Next. The
  rejected grid borrowed the affordance without the function.
- The product is **more than Brief** — articles, company pages, DataLabs — and the welcome
  screen must convey that breadth without a feature list.

**Research findings that drove the redesign:**
- Serious news apps are **type-only, no mockup**: NYT *"Understand your world."*, X *"See
  what's happening"*. The promise is about the reader's state, never the app's mechanics.
- **A triad conveys breadth without a spec sheet** — Fidelity *"Invest. Save. Spend. Plan."*
  Here **"the news, the companies, the numbers"** signals articles / company pages /
  DataLabs without naming a single feature.
- FotMob *"Changing how you follow football."* is the closest structural model — wordmark,
  one sentence, one button.
- Product screenshots are the minority in professional apps; they appear mainly in consumer
  fintech.

**Five built** (draft file, row y=25225), all type-led, zero counts, no chips, cadence
stated as "every morning":
- **A · NYT model** — *"Know what's moving Indian startups."* + the triad as subhead.
- **B · Triad hero** — "The news. / The companies. / The numbers." stacked large, third line
  in peach, then *"All of it, every morning."*
- **C · One sentence** — *"Changing how you follow Indian startups."* Nothing else.
- **D · Type as image** — "Know what's moving." at 78px, "moving." in peach.
- **E · Masthead** — newspaper rules + "REPORTING INDIAN STARTUPS SINCE 2014" +
  *"Understand the Indian startup ecosystem."*

Craft note: setting a line to ~0.5 white opacity to de-emphasise it reads as **disabled**,
not as an accent. Use the peach accent colour at full opacity instead.

## W4 — fifteen welcome variations across three families

**Key copy resolution:** naming a **count** ("8 stories") misleads and breaks; naming a
**product** ("the Brief") builds equity — the Morning Brew / Robinhood Snacks move. So
Inc42's own marketing line **"Cut the noise. Get the Brief."** is usable verbatim, and
makes app and banners finally say the same thing. Cadence is always "every morning",
never a duration.

**SET 1 · PLAIN** (type only, row y=26170) — five copy directions:
P1 "Cut the noise. / Get the Brief." (brand line, second line in peach) · P2 "Know what's
moving Indian startups." + triad · P3 "Changing how you follow Indian startups." · P4
"Everything Indian startups did today. / **Briefly.**" · P5 "Start every morning ahead."
with a labelled "The Brief" block.

**SET 2 · WITH IMAGES** (row y=27115) — I1 photo-top + copy below · I2 full-bleed photo
with scrim · I3 floating tilted brief card · I4 two-photo split labelled THE NEWS /
THE COMPANIES · THE NUMBERS · I5 circular photo mask. Photos are placeholder (Picsum) —
swap for Inc42 editorial art.

**SET 3 · VISUAL ELEMENTS** (no photography, row y=28060) — V1 sector constellation (five
segmented rings with Lucide icons) · V2 layered card stack · V3 noise-to-signal (faded
lines funnelling into a white THE BRIEF card) · V4 glowing orb on deep ink · V5 ticker
grid of real companies and deal values.

Craft notes: a photo scrim needs a **three-stop** gradient (0 → 0.75 → 0.96) over ~70% of
the frame; a two-stop scrim left white text illegible on a light sky. V3 is the strongest
articulation of "cut the noise" because it *shows* the noise being cut rather than saying
it; V5 is the strongest proof that the product covers real companies and real money.

## W5 — 15 refinements of the three strongest welcome directions

Ranjith singled out **"Every corner of the Indian startup world."** as the line that works,
asked for more sectors represented, and said "In one Brief, every morning" was too subtle —
so the second line now carries the brand line **"Cut the noise. Get the Brief."** on almost
every version. Sector coverage widened from 5 to 9-14 (fintech, e-commerce, SaaS,
healthtech, edtech, logistics, mobility, agritech, consumer, gaming, AI, travel, D2C,
cleantech), using Lucide icons throughout.

**V1 SET · constellation** (row y=29005): 1a wider constellation (10 bubbles) · 1b tidy
3×4 icon grid · 1c icons with sector names · 1d sector word-cloud (type only, varying
size/opacity) · **1e orbit — eight sector bubbles circling a white "THE BRIEF" core.**
1e is the strongest: it makes the value proposition *structural* — every sector feeds into
one Brief — rather than asserting it in copy.

**V2 SET · card stack** (row y=29950): 2a deeper stack with real headline and sector tags ·
2b fanned hand of five · **2c single hero card** (white, orange top-rule, dateline, sector
tags, newsroom credit) · 2d descending feed stack · 2e swipe deck with an 8-segment
progress bar and "1 OF 8". 2c is the most credible — it looks like a real published
artefact rather than a UI mock.

**V3 SET · noise to signal** (row y=30895): 3a tighter funnel · 3b drawn funnel walls ·
3c converging curves into one bright line · **3d side-by-side WITHOUT vs WITH INC42** ·
3e noise as labelled chips (PR launches, listicles, press releases) collapsing into the
Brief. 3d is the clearest read in one glance; 3e is the most *specific* about what the
noise actually is, which makes the claim concrete rather than abstract.

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
