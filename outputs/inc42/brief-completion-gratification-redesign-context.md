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

## Trust layer (row y=31840)

Three strongest welcome screens cloned and layered with trust elements — **T1 orbit**,
**T2 hero card**, **T3 side-by-side** — plus a **TRUST KIT** reference frame (`134:2`)
listing every element with its placement, why it works, and what it needs to be true.

Ranked by credibility bought per pixel:
1. **Independence — "No sponsored stories. Ever."** The strongest signal available to a
   news product, and it costs nothing. Says the Brief cannot be bought. SHIPPABLE.
2. **Liveness — "Filed 6:00 AM today"** Nielsen's *current content* trust factor: proves a
   person did work this morning rather than a feed refreshing. Needs the real filing time.
3. **Risk removal — "Free · No card · One Brief a day, no spam"** Sits under the CTA and
   kills three objections at once, including the unspoken fear of notification spam.
4. **First-hand reporting — "Reported first-hand by Inc42's newsroom"** The single most
   under-used asset across every version; it is what separates Inc42 from aggregators.
5. **Provenance — "Reporting Indian startups since 20XX"** ⚠️ the founding year was used
   unverified in an earlier draft — must be confirmed, never guessed.
6. **Third-party proof — store ratings.** Only worth showing while genuinely above ~4.3.
7. **Scale — "Read by founders, operators and investors"** deliberately worded without a
   number so it never goes stale; add a figure only if large and current.
8. **Data provenance — "Numbers from Inc42 DataLabs"** backs the "numbers" third of the
   triad and quietly advertises DataLabs.
9. **Named people — bylines/newsroom faces.** Highest ceiling, heaviest to build.

**Limit: two or three per screen.** Past that they stop reading as confidence and start
reading as persuasion, which costs trust rather than building it.

## V25 — the two-zone sector fix (more important than the circle)

Ranjith's diagnosis of V24: the sector rail reads as **unfinished business**. "WHAT ELSE
MOVED TODAY · 10 STORIES" never says the reader's own sectors are done, and never says the
rest is optional — so it lands as "there's more… what is this?", which is anxiety at the
exact moment meant to deliver closure.

**Fix — split the rail into two explicitly labelled zones** (row y=32785):
- **`YOUR SECTORS — ALL COVERED`** (peach label) — ticked chips with counts:
  ✓ Fintech 5 · ✓ E-commerce 3. Closure is stated *first*, and is unambiguous.
- **`NOT YOUR SECTORS`** … **`OPTIONAL`** (right-aligned, low contrast) — the other-sector
  rings, closed by: *"Nothing you need to read — just so you know the whole ecosystem, not
  only your corner."*

**Corrected after review — the first attempt at zone 2 was still wrong.** "NOT YOUR
SECTORS" defines the section by what the reader *didn't* pick (a deficit frame),
"OPTIONAL" implies an obligation exists somewhere, and "Nothing you need to read"
protests too much — naming an obligation is what invokes it. Net effect was still
"am I missing something I follow?"

**Final copy — additive, never subtractive:**
- Zone 1: `YOUR SECTORS — ALL COVERED` + ticked chips with counts
- Zone 2: **`ALSO WORTH KNOWING`** (peach, reused from V17 where it tested well) with the
  "OPTIONAL" tag deleted entirely, closed by an invitation rather than a denial:
  *"Tap any sector for a quick look."*

**Rule that came out of this:** describe the extra content by what it *adds*, never by what
the reader failed to select, and never mention obligation even to deny it. Order stays
**closure first, discovery second, obligation never.**

**Circle treatments built:**
- **25a · Week ring + core** — the V24 segmented ring with a soft inner disc behind the
  number, plus the `+1 TODAY` pill inside the ring.
- **25b · Solid disc + dots** — a filled white disc with the number in brand orange (no
  segments), week progress moved to seven dots beneath. Reads bolder and simpler; the
  streak becomes the object rather than the progress geometry.

## V26 — streak UIs × section-copy options, plus the reveal animation

**Four streak treatments** (row y=33730), each paired with a different discovery-section
label so both variables can be judged in place:
- **26a · Flame + number** / `ALSO MOVING TODAY` — universal streak language, reads
  instantly; the label never mentions sectors at all, which fully dissolves the
  "am I missing something I follow?" problem.
- **26b · Bare numeral** (150px, no container) / `ELSEWHERE IN THE ECOSYSTEM` — week
  reduced to a thin seven-segment bar underneath.
- **26c · Tally marks** — seven vertical bars, four lit, today's glowing / `THE WIDER
  PICTURE`. Most tactile and the most obviously *countable*.
- **26d · Day plate** — a calendar-tile with an orange cap / `ALSO WORTH KNOWING`.

**Animation** — eight progressive-reveal stage frames built in Figma (x=2200 onward,
named `ANIM 1 · land` … `ANIM 8 · complete`), screenshotted and assembled into a GIF with
PIL, including two cross-fade tweens between each state:
`~/ClaudeDocs/inc42/brief-card/inc42-streak-reveal.gif`
Sequence: land → flame in → **shows yesterday's 3** → **ticks to 4 with the burst** →
headline → your sectors → discovery → complete (long hold).
The key beat is stage 3→4: the streak is shown at its *previous* value first, then
increments on screen, so the reward visibly happens rather than being reported. To change
timing, edit the `plan` list of `(frame index, milliseconds)` pairs in the assembly script.

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

## V26b-OUT — logged-out streak state (30 Aug)

Cloned from `V26b Bare numeral` into `V26b-OUT · LOGGED OUT` (draft file, x=1800 y=33730).
Same screen, three changes: the numeral reads **1**, only the first of the seven week dots
is lit, and the unlock card is replaced by a loss-framed pair — a gold line
**"This streak disappears at midnight."** over a solid white CTA
**"Log in to save my streak"**, closed by "Takes 10 seconds · keeps every morning you have
read". This is the one place in the product where loss framing is correct: the streak
genuinely is unsaved, so naming the deadline is honest rather than manufactured pressure.

## V27 / V28 — the STORY CARD (a different screen from the completion screen)

Row V27 (y=35530) was the first pass at the in-brief story card and is superseded.
Ranjith's rejection of V27-1: too many elements, no article image, and the newsroom
byline / "30-sec read" / filed time are not relevant inside the brief. He also flagged the
real blocker — What's new / Why it matters / The detail are long and will not fit.

**Row V28 (y=36600) is the current set**, and it changed method: it uses a REAL Inc42
story rather than invented copy — Ola Electric's ₹95.81 Cr PLI-Auto incentive, post id
570511, its real featured image, and its three real summary bullets at **19 / 27 / 20
words**. Designing against the actual lengths is what makes the space problem legible.

Five answers to "the body is too long":
- **28-1 Over the image** — the photograph is the whole card behind a three-stop scrim, so
  the ~210px the image block used to occupy is recovered and all three bullets fit.
- **28-2 Headline does bullet 1's job** — drops What's new entirely. Backed by the corpus
  finding that bullet 1 repeats a median 50% of the headline's words; the two survivors
  then run at 15px instead of 13.5px.
- **28-3 Two taps, one story** — the story spans two cards, shown by splitting segment 2 of
  the progress bar in half. Buys a 31px headline.
- **28-4 Expand in place** — The detail collapses to a single tappable row carrying its own
  teaser ("₹7,240 Cr in battery-cell PLI also in play") with a chevron.
- **28-5 Thumbnail + long body** — image demoted to a 96px thumb beside a company block
  with a Follow control; maximum room for text, and only Why it matters is accented.

All five drop the byline/filed-time/read-time chrome, move bookmark and share onto the
image as glass buttons, and carry the reaction pair inline.

**Reaction control (research-backed, applies to every variation):** the live control is a
heart labelled "Rate" that must be tapped before like/dislike appear — structurally the
same dead control Netflix shipped and then fixed. Netflix's move from 5 stars to 2 thumbs
raised rating volume 200%; YouTube shipped the *word* under the thumb; Particle, Blinkist
and Apple News all keep both halves visible and frame the negative as a feed preference
("Less", "Suggest less like this"), never as a verdict. Hence **"More like this" /
"Less like this", both visible, single tap, words not icons.** The existing negative
bottom sheet (`2290:1180` in the live file, misnamed "Delete · 1 · Confirm popup") is
good and should stay as the second step of the Less path; there is no positive-path sheet
designed at all.

⚠️ Per-story photography does not exist as a pipeline yet (sector images agreed 12 Aug,
owner Anmol, unbuilt). 28-1 and 28-2 depend on a real image per story; 28-3/4/5 degrade
gracefully without one. Confirm the art pipeline before picking a photo-led direction.

## V29 — story card rebuilt as identity devices (30 Aug, current set)

**V28 was rejected wholesale.** Ranjith's verdict, in order: V28-1 was too bright to read,
the More/Less pills were misaligned, the text was not readable, and "the UI is not at all
convincing, it is not making any sense." Asked directly, he named the root cause as
**no visual identity** — the layout was fine but nothing looked designed or looked like
Inc42 — and said to **start clean** rather than salvage any of the five.

Two craft notes banked from that round: the thumb icon and its label were 5px out of
vertical centre inside the pill (centre both against the pill box, and set the label to
`WIDTH_AND_HEIGHT` so the pair can be centred as a unit); and pushing the scrim hard
enough to read white text over Inc42's bright studio photography destroys the photograph,
which kills the text-over-image direction outright.

**Precedent pulled before building (Mobbin):** Blinkist Shorts (whole card is one flat
brand colour, payload is a pull-quote, thumbs pair permanently visible), Life Reset (one
enormous orange numeral on near-black), Formula 1 (oversized black headline plus a red
category chip), The Atlantic (display type on a black ground), Instagram Stories (in the
story format the reaction lives at the bottom edge as chrome, not as a button in the
content).

**The system, shared by all five (row y=37670):** masthead, 8-segment progress bar, and a
**full-width split reaction bar flush to the bottom edge** — 84px tall, halved by a
hairline, `More like this` / `Less like this` with thumbs, both always visible.
**"Read full article" is deleted entirely** (9% usage, and Ranjith said to ignore it).
Bookmark and share sit as glass circles in the top-right.

The five devices:
- **29-1 The orange plate** — the whole card is brand orange, no photograph. Identity is
  the colour itself; every card in the brief is a plate of Inc42 orange.
- **29-2 The number plate** — near-black, the figure at 72px in `#FF6B3D`, then a
  `HOW IT ADDS UP` bar chart of the FY24/FY25/FY26 tranches. Strongest claim to being
  *Inc42's* card, because the graphic device is the data nobody else holds.
- **29-3 The masthead poster** — full-bleed photo, a hard seam, and an orange category
  plate straddling it under an oversized headline.
- **29-4 The filed record** — cream ground, a white document card with an orange top rule,
  tabular label/value rows and a `VERIFIED · INC42 DATALABS` footer. Reads as a record you
  are being handed rather than a feed item.
- **29-5 The split plate** — orange top half carrying the headline, cream bottom half
  carrying the body, with a circular sector token straddling the seam.

Note 29-1, 29-2, 29-4 and 29-5 need **no photograph at all**, which matters while per-story
art is still unbuilt.

## V30 — logged-out completion screen, four options (row y=38740)

The structural problem, which the first single-frame attempt missed: signed out, the streak
is only kept for the current date, so **a returning reader sees the same "1" every
morning**. The reward stops being a reward by about day three, and the login prompt becomes
wallpaper. All four variants are clones of `V26b Bare numeral` with only the streak block
and the CTA changed.

- **OUT-A · Day 1, ends tonight** — numeral 1, gold `ENDS TONIGHT` pill, week dots removed,
  "Signed out — we only keep today's streak." over `Log in to save my streak`. Honest and
  shippable against storage as it works today, but identical every morning.
- **OUT-B · The week that cannot fill** — numeral 1 with the seven week dots faded and the
  gold caption `THE REST ONLY FILL ONCE YOU LOG IN`. Teaches the mechanic. (Craft note:
  a dashed stroke on a 14x4 dot renders as noise — use a faded solid fill instead.)
- **OUT-C · Claim what you already read** — an outline numeral **4** over
  `MORNINGS ON THIS PHONE` + "None of them saved.", CTA `Log in to claim 4 mornings`.
  Needs only a device-local counter (anonymous, no auth), and the hook **grows** with every
  return instead of being stuck at 1. On day one it degrades gracefully into OUT-A.
  ⚠️ Only ship it if logging in genuinely backfills the streak to that number — otherwise
  it is a promise the product breaks at the moment of signup.
- **OUT-D · No number at all** — drops the streak entirely for signed-out readers;
  "You're all caught up." as the hero with "Streaks start when you log in." Removes the
  stuck-number problem but has the weakest pull.

Recommendation: **C, with A as its day-one state**, subject to the backfill check.

## V31 — honest urgency on the logged-out streak (row y=39810)

**OUT-C is dead.** Ranjith: the product cannot backfill past mornings, so "Log in to claim
4 mornings" is a promise that breaks at signup. The only true mechanic is that today's
streak is held until midnight and then dropped, so every treatment works off that real
deadline. Five, deliberately spanning tones:

- **T1 · Live countdown (urgent)** — a dark pill under DAY STREAK with a clock and
  `08 : 42 : 19`, caption `UNTIL TODAY'S STREAK RESETS`, CTA `Log in before midnight`.
- **T2 · The day draining (neutral)** — a gold bar depleting between `NOW` and `11:59 PM`.
  Same deadline, no ticking digits. CTA `Keep today's streak`.
- **T3 · The fading number (show, don't tell)** — the numeral itself is filled with a
  white-to-transparent gradient so it is visibly dissolving; caption
  `FADING · GONE AT MIDNIGHT`. The only one that carries the idea without stating it.
- **T4 · The ledger (formal)** — the numeral becomes a gold **0** over `MORNINGS SAVED`,
  with "You have read four. None of them are on an account." States the loss as fact and
  promises nothing. ⚠️ It puts a zero on a screen whose job is to reward completion.
- **T5 · Tomorrow is locked (polite, forward-looking)** — `1 TODAY` solid beside a dashed
  `2 TOMORROW` with a padlock; "Log in tonight and tomorrow picks up from two." The only
  variant that names what the reader gains rather than what they lose.

Recommendation: **T5 as the default, T1 only in evening sessions** when the deadline is
genuinely close — the urgency escalates with real time remaining instead of shouting all
day. That is also the honest answer to "should there be a timer": yes, but only when the
timer means something.

Craft note: the base V26b streak block has to be lifted (numeral y=110 → 86, label
282 → 256) before any treatment taller than ~30px will clear the section divider at y=396.

## Row L — the LIVE card, edited (row y=40890)

Ranjith's instruction after V29: keep the live card in the same fashion and edit on top of
it. Four removals: **THE DECODE label, 30-SEC READ, Read full article, and the heart/Rate
control**. Structure preserved exactly — dark rounded hero card holding the image and the
headline, white body, three labelled bullets with orange markers, relevance pill.

The four removals delete the entire eyebrow row, which is what was holding the bullet block
together — so each variant answers that hole differently:
- **L1 · Clean cut** — removals only, plus hairline dividers between the bullets and a
  full-width dark split reaction bar at the bottom edge. Smallest possible diff.
- **L2 · Tinted panel** — the three bullets sit in a peach panel with numbered orange
  chips; reaction becomes two large 56px buttons, filled `More` and outlined `Less`.
- **L3 · Asked, not offered** — the relevance line is promoted off the image into a proper
  row under the card; the reaction bar carries a question, `WAS THIS WORTH YOUR MORNING?`,
  above the two options.
- **L4 · Stat lead** — the deal figure `₹35 Cr · SERIES A · D2C` occupies the space the
  decode row used to, so the removal replaces itself with something of value.

Bookmark and share move onto the hero as glass circles in all four — that is what frees the
bottom edge for the reaction alone, which is how it gets more prominent without adding
chrome. Recommendation: **L4**, with L1 as the minimum-change fallback.

⚠️ **Figma craft trap that cost four rebuilds here.** A TEXT node's `.height` is NOT
readable from a script — it reports the pre-render value (2 lines where 3 will render), so
any manual `y += t.height` stacking silently overlaps, and re-reading it in a later call
does not fix it. The only reliable approach is auto-layout, and it needs all three of:
the text at a FIXED width (`resize(w,10)` + `textAutoResize='HEIGHT'`, never
`layoutSizingHorizontal='FILL'`, which truncates), `row.layoutSizingVertical='HUG'`, and
`text.layoutSizingVertical='HUG'`. Omit the HUG calls and rows render clipped to two lines.

## Row M — Clean Cut modernised (row y=41960)

Ranjith picked **L1 · Clean Cut** as the base, with three notes: the horizontal hairline
dividers between bullets read as a table and date the card; the filled orange square marker
should be a circle and smaller (or replaced with something better consumed); and the dash
after the label should be a colon. He separately noted the older Figma file uses a glass
bottom bar but explicitly did **not** ask for glass here — the solid bar stays.

Five ways to separate three points without drawing a line between them. Hero card,
relevance pill and reaction bar are identical across all five; only the bullet block moves:
- **M1 · Small dot + colon** — 7px orange dot, 24px gaps, `What's new:`. The literal
  execution of his note, smallest change from Clean Cut.
- **M2 · Eyebrow label** — no marker at all; the label becomes a 9.5px orange caps eyebrow
  on its own line with the body beneath at full 342px width. The most modern and the most
  editorial, and the longest measure so the copy breathes.
- **M3 · Left rule** — a 3px vertical rule per block, orange on the payload bullet and pale
  on the other two. Vertical marks read modern where horizontal rules read tabular.
- **M4 · Soft blocks** — each point sits on its own rounded surface, the middle one tinted
  peach. Separation by surface rather than by line.
- **M5 · Numbered chip** — a 20px outlined orange circle with 1/2/3. Keeps the sequence
  legible without a table.

The star glyph inside the relevance pill was also swapped for the same small orange dot —
at 12px the star rendered as an orange blob and repeated exactly the problem he flagged.

Recommendation: **M2**, with M1 as the literal-note fallback.

## Row G — Gen Z register, and the card-one drop (row y=43030)

Ranjith rejected row M: still not a complete card, the black More/Less bar at the bottom is
not convincing, and the whole thing is "not enticing me to read". He asked for heavy Gen Z
reference work, and added the real problem — **~50% of readers never reach card 2**, and
he wants an in-depth answer to how people are moved forward.

**The research finding that reframed it.** Every microlearning/card app that successfully
keeps people moving ends the card with one large forward action: Deepstash `Continue`,
Duolingo `CHECK`, Mimo `Continue`, Liven `Complete lesson`, Life Reset `Next Lesson →`
(with "1 of 8" up top), Speak `TAP TO CONTINUE`, Quizlet showing the next card's edge.
**Inc42's card has no forward affordance at all** — the bottom slot was spent first on
`Read full article` and then, in my own rows, on the reaction bar. That is very likely a
large part of the 50%: nothing on the screen says a next card exists.

So the priority inverted: **the forward move takes the primary bottom slot, and the
reaction demotes to two quiet 38-40px ghost circles labelled "Useful?"** — which also
resolves the black-bar objection. Visual register is near-black `#0C0C0E`, surface
`#18171B`, brand orange kept as the only accent (no new hue family), chunky fully-rounded
pills, `2 OF 8` chip in the header.

Cards also carry **two points instead of three** — a shorter card is itself part of the
fix, since a card that fills the screen reads as the whole thing.

Four mechanisms:
- **G1 · The continue button** — `UP NEXT` + the next story's headline, then a full-width
  orange `Next story →` pill. Closest to the proven pattern.
- **G2 · The peek** — the story sits on a card with the next card's edge visible at the
  right, plus "Swipe for the next story". Teaches the gesture physically (Quizlet).
- **G3 · The stack** — deck edges peeking below the card and
  `6 MORE STORIES IN TODAY'S BRIEF` beside a 60px orange arrow. Makes the remainder feel
  small and finishable.
- **G4 · The next story strip** — a 122px strip at the bottom carrying the next story's
  thumbnail, `UP NEXT` and its headline; the whole strip is the tap target. Curiosity gap
  does the work rather than a generic button.

Recommendation: **G4 for the mechanism, G1's button as the fallback**, and G2's peek added
to **card 1 only** as a one-time teaching device, since the data says the loss is entirely
at card 1→2 with no fatigue curve afterwards.

Do not add timed auto-advance — readers read at different speeds and news is not Stories.
Keep tap-right, swipe-left and the button all live as three targets for the same action.

## Row H — the corrections on row G (row y=44100, current)

Ranjith's notes on G: the card did not feel personalised to him; the **Inc42 wordmark and
the TODAY'S BRIEF tagline had been dropped** and must come back; **all four G screens had
lost "The detail"**, so only two of the three points were shown; the layout was not well
aligned; **G3's stack read as scroll/swipe-up rather than swipe-left**; and G2's peek was
the right idea but poorly represented.

What changed, applied to all four:
- **Masthead restored** — `Inc42 | TODAY'S BRIEF · 3 AUG` with `2 / 8` on the right, over
  the 8-segment bar.
- **Personalisation is stated, not implied** — an avatar chip plus
  *"In your brief because you follow **Sauce.vc**"* as its own row directly under the
  progress bar, and the sector chip reads `YOUR SECTOR · D2C` (additive framing).
- **All three points return** — What's new / Why it matters / The detail.
- **One grid.** Image, chip, headline and every body line share the same 24 / 366 margins;
  nothing is inset differently from anything else. This was the actual alignment defect.
- **The reaction moved up beside the sector chip**, so the entire bottom of the screen
  belongs to the forward move. This is also what makes room for three points.

The four forward mechanisms:
- **H1 · Next story strip** — 116px strip with the next story's thumbnail, `UP NEXT · 3 OF 8`
  and its headline; the whole strip is the target.
- **H2 · Horizontal deck** — the remaining stories drawn as small cards laid out **to the
  right**, under `STILL TO COME` / `6 MORE`, with an orange arrow. Fixes G3's vertical
  misread: direction is now unambiguous.
- **H3 · The peek, properly** — the next story sits to the right with its own thumbnail and
  skeleton lines, dimmed behind a gradient, and a 58px orange **seam button** straddles the
  boundary, plus `SWIPE LEFT FOR STORY 3` with chevrons. Teaches the gesture.
- **H4 · The named next button** — a 74px orange block carrying `NEXT · 3 OF 8` and the
  next story's actual headline, "Zomato's ₹2,000 Cr bet". One target, and the reason to
  tap it is written inside it.

Recommendation: **H4 as the default, H3 on card 1 only** as a one-time gesture lesson,
since the loss is entirely at card 1→2 with no fatigue curve afterwards.

## Rows A–F — Brief page: MOVING TODAY and DEEP DIVES (rows y=45300 onward)

New brief from Ranjith: two new sections below the existing Brief page, each defined by a
**rule that re-runs daily against content we already own**, never by a content bucket.
Base screen referenced: `4316:4729` in Inc42-App-2026 (orange header, white sheet, dark
cards, black pill CTA, 3-tab nav) — matched, and built only in the draft file.

Deliverables on canvas:
- **A** (x=0) full Brief page, cold / logged out · **B** (x=450) logged in, with the
  `2 you track` pill on the brief card and an `On your watchlist` badge on the Zepto card
- **C1–C4** (y=47200) MOVING TODAY supply ladder: 6+ / 3–5 / widened 48h window / absent
- **D** (y=47780) card anatomy at 2x, annotated, reason line called out in orange
- **E1 / E2 / E5** (y=48420) DEEP DIVES selector rules 1, 2 and 5
- **F** (y=48980) the connective moment, with a dotted link from the Zepto card down to
  "Because Zepto moved today"

Decisions taken while building:
- **The reason line is set in brand orange at 15.5px Black** — larger than the company
  name. It is the thing being read, so it outranks the entity.
- **Rail cards are 162×196 at a 174px pitch**, which leaves a deliberate ~22px peek of the
  third card at 390 wide. Six cards never fit; the peek is what says "scrolls".
- **The 48h widening is stated on the section**, as a `LAST 48 HOURS` pill beside the
  header, never silently applied.
- **C4 shows Past Briefs closing straight into Deep Dives** — the honest picture of a
  non-render, with no gap or placeholder.
- **E5 is a single upcoming-issue card** (`THE CHECKOUT · Lands Tuesday` + `Notify me`),
  not an empty shelf.
- Company marks are **coloured monograms**, not fake logos — honest, and it matches the
  91.2% DataLabs-resolution reality where art may or may not exist.
- Header subline is generated from the day's set (`2 raises · 2 results · 1 IPO filing`),
  which changes daily by construction and needs no login.

⚠️ Placeholder art: the hero, past-brief and deep-dive images are reused crops from earlier
rounds and one still carries faint baked-in headline text. Swap for real editorial art
before this goes to anyone outside the team.

## Company profile page — one shell, four fills (rows y=50200 and y=51900)

Brief saved at `~/ClaudeDocs/inc42/company-profile-page-designer-prompt.md`. Template picked
by the API's `signals_count` (1–6), never by per-field null checks. The data-poor profile is
the default case — half of all companies are T1 — so it was designed first.

Built only in the draft file; `955:16300` in Inc42-App-2026 was read but not touched (it is
the Explore **list**, not a profile — it shows the current logo + chip + blurb +
"Read more" card the brief describes).

- **A · T1** Sleepy Owl Coffee — identity, full description, articles. No numbers anywhere.
- **B · T2** The Whole Truth — plus one traffic figure.
- **C · T3** Perfios — clamped description, funding, founders, traffic, articles.
- **D · T4** Lenskart — plus financials and corporate.
- **E** is the row read across: orange guides drawn on canvas at the shared shell landmarks
  (top bar ends, 64px logo tile, name baseline, first block rule) prove the shell is
  identical on all four.
- **F1/F2** funding block collapsed and expanded (all six rounds).
- **G1/G2** watchlist star off and on, with a `Tracking` pill and the line
  "On your Watchlist. You'll see it in Moving Today." — which ties the toggle to
  [[Moving Today]] rather than leaving it an orphan action.
- **H** company not found.

Decisions taken inside the brief's gaps:
- **T1's page is carried by making ON INC42 the hero** — a full-bleed lead article card plus
  three list rows plus an "All 12 stories" row. The description runs at 16px/25 instead of
  T3/T4's clamped 15px/23. Same shell, different weight, so T1 reads as composed rather
  than as T4 minus blocks.
- **Every block leads with exactly one large figure** (42px Black) with its change indicator
  to the right — traffic, funding total, revenue. Never a metric grid.
- **The expand only exists when there is something behind it.** F2's "All 6 rounds" is not
  chrome; on a company with one round the control is absent.
- Company marks are coloured monograms on the neutral tile, not scraped logos.

⚠️ Two things not deliverable in Figma and worth stating to whoever builds it: **tabular
numerals** (`font-variant-numeric: tabular-nums`) are specified by the brief but cannot be
set through the plugin API, so the mockups use proportional figures — the build must turn
them on or the funding and traffic columns will not align. And the tier labels on canvas are
illustrations of data density, not claims about those companies' real DataLabs records.

## Explore › Companies tab (row y=52840)

Brief at `~/ClaudeDocs/inc42/companies-tab-card-designer-prompt.md`. Full app chrome on
every mockup — orange Explore header, ARTICLE | COMPANIES segmented control, filter pill
row with the filter icon, 3-tab nav with Explore active.

Built: **A** All pill (figure slot empty) · **B** Recently Funded · **C** IPO Bound ·
**D** expanded at signals_count 1 · **E** expanded at signals_count 6 · **F** the guides
drawn across D and E · **G** watchlist control in all four states · **H** empty filter result.

Decisions taken inside the brief's gaps:
- **The pill row reorders so the active pill is always first.** With five pills at 390 wide
  the row overflows, and the first build silently dropped the active pill off-screen. A
  selected filter scrolling into view is also what a real list does.
- **A text figure needs a smaller size than a numeric one.** `DRHP filed` at the 19px used
  for `$450 Mn` collided with the meta line and wrapped. IPO stage sets at 15.5px Bold; the
  rule "one figure, larger than supporting text" holds without a fixed size.
- **The three facts on a signals-6 card are label-left / value-right rows on hairlines**,
  not a grid — so a company with two facts loses a row rather than leaving a hole.
- **The star is the only watchlist control, in both states.** Expanded it gains the word
  `Track` / `Tracking`; it is never swapped for a separate TRACK button. G states this on
  the frame.
- **The empty state names why it is empty** ("Only three funded companies are IPO bound this
  quarter…") and offers **Clear the last filter** before Clear all — undoing one filter is
  almost always what the reader wants.
- Descriptions are trimmed to a single line at ~46 characters; two lines collide with the
  star and chevron at the 112px row pitch.

⚠️ Same tabular-numerals caveat as the profile page: the plugin API cannot set
`font-variant-numeric`, so the funding column in B is proportional in the mockup and must be
switched to lining/tabular figures in the build or the amounts will not align.

## Row K — Companies tab rethought as a browse surface (row y=54140, current)

Ranjith rejected the row-list version outright: monotonous, static, too much to consume and
none of it relevant at the moment of consumption, and not premium. He asked for the **page
as a concept** to be redefined, not just the card.

**The diagnosis:** a uniform 112px row repeated fifty times is a lookup tool, and nobody
browses a lookup tool. Mobbin confirms none of the premium browse surfaces use one uniform
list — Fable blocks colour tiles then cuts to a full-bleed moment; Matter runs a single
Staff Pick with "a new selection will be ready tomorrow"; Mindvalley ranks with ordinals;
Goodreads and Blinkist use collections with counts. **Rhythm change is the mechanism.**

In all five concepts the A–Z directory moves behind Search, which is where lookup belongs.

- **K1 · The browse magazine** — three shelves, three card shapes: MOVING THIS WEEK (rail of
  large event cards), THE CHART (ranked five), COLLECTIONS (2×2 colour tiles with counts),
  closing on "Search all 74,000 companies".
- **K2 · The chart** — the whole page is a ranking with a period switcher; top three get a
  large treatment with 34px ordinals, four to eight compact. Rank creates narrative, so the
  page is never uniform.
- **K3 · The question deck** — opens with "74,000 Indian companies. Start somewhere." and
  four questions, each with a three-logo preview and a count. The most direct answer to
  "make people open something".
- **K4 · The daily five** — one editorially chosen company as a full-bleed hero with a
  written reason, four beneath, closing on "Tomorrow's five lands at 7 AM". Refresh is
  promised, so monotony is impossible by construction. Matter's model.
- **K5 · The two-up grid** — tiles instead of rows, broken every six by a full-width dark
  editorial band (IPO WATCH). Denser and more scannable, least editorial effort.

Recommendation: **K4 for the top of the page, K1's shelves beneath it.** K4 is the only one
that changes daily without anyone maintaining it and gives a reason to return; K3 is the
strongest for a first-time or logged-out visitor with no idea where to start.

⚠️ K1 and K4 need an editorial or rules layer that does not exist yet — "today's five" and
the collection membership have to be generated daily. K2 and K5 run off DataLabs fields
alone. That is the real cost difference between the concepts.

## Row L — the reader who arrives with no intention (row y=55500, current)

Ranjith's gap in row K: every concept there is event-led, which serves an investor or founder
who came looking for something specific. It leaves out the visitor who "just wants to see
what else is happening", or a general list, or simply the companies in their sector. Two
audiences, and K only served one.

- **L1 · Sectors first** — the page opens as sectors, not companies. `YOUR SECTORS` first
  (outlined in brand, with a "4 raised this week" micro-line), then every other sector as a
  plain counted row, closing on "Browse all companies A–Z". Direct answer to "companies in
  my sector".
- **L2 · The activity feed** — uncurated reverse-chronological stream of everything that
  happened, grouped TODAY / YESTERDAY / SATURDAY with hour stamps, pills for
  Everything / My sectors / Funding. Literal answer to "what else is happening", and
  infinite, so it satisfies aimless scrolling.
- **L3 · The directory, done properly** — the count stated (74,388), sticky letter headers,
  compact rows and an A–Z scrubber down the right edge. Answers "a general list of what is
  available"; monotony is fine here because lookup is the job.
- **L4 · One page, two zones** — `WHAT'S HAPPENING` (three event rows + "See everything that
  moved") above a full-bleed divider, then `OR JUST LOOK AROUND` (sector grid + A–Z entry).
  Both intents on one scroll with no mode switch to discover.
- **L5 · Serendipity** — one company at a time with a written reason it is interesting
  ("Profitable since 1996. Has never raised a rupee."), a black **Show me another** shuffle,
  and sector chips. Pure aimless browsing.

Recommendation: **L4 is the shape of the page** — it needs no mode switch and neither
audience has to know what they want first. Feed L2 into its top zone and L1 into its bottom
zone, and keep L3 behind the A–Z row. L5 is the strongest single addition on top, because it
is the only surface that rewards a reader with no goal at all.

⚠️ L5 needs an editorial reason line per company, which does not exist as a field. It could
be derived (never raised + founded before 2010 + profitable) but the sentence itself is
writing, not data.

## Row M — the card is the problem, not the page (row y=57000, current)

Ranjith on row L: still bland, still a listicle, still monotonous when you look at any single
card. L1 (sectors first) was the only one with promise. The real ask is **card design
variety** — different card styles within one page — not another page concept.

**The reference class that solves this is stock and crypto apps**, because they have the same
problem (a data row that must feel alive): Apple Stocks, Bloomberg At A Glance, Coinbase,
Yahoo Finance and Binance all **put a shape inside the row** — a sparkline, a filled area, a
coloured delta chip.

**The unlock for Inc42:** the one shape every company has is **how often Inc42 has written
about them**. Funding history exists for 13%, traffic for 44%, but editorial coverage exists
for every company reachable from the news by construction. So the card can carry a chart even
when there is no money data at all.

**M0 · Card style library** (x=0) — ten treatments: 01 Ticker row (spark + delta chip) ·
02 Glance tile (3-up) · 03 Dark hero (one company owns the width) · 04 Split colour (the
monogram becomes the graphic) · 05 Timeline (last three moves) · 06 Milestone (for companies
with no numbers) · 07 Sector cluster (overlapping marks) · 08 Comparison (two companies, one
bar each) · 09 Coverage (86 stories + 12-month bar chart) · 10 Pull quote (editorial voice,
not a data row).

**M1 / M2** are two pages assembled from mixes of those styles — a sectors page and a
happening page. Neither repeats a card style more than twice.

The governing rule written on the library frame: **mix three or four styles per page, never
repeat one more than about three times.** A card style repeated past that becomes the
wallpaper it was meant to replace.

⚠️ Styles 06 and 10 carry written lines, not fields. 09 needs a per-company monthly story
count, which the CMS can produce but is not currently exposed.

## Row N — a card set that only uses provable data (row y=58600, current)

Ranjith asked two things at once: do we actually have the data row M assumed, and give an
altogether different set of variations.

**Answer to the first: no, not for most of it.** Row M's sparklines needed per-company monthly
story counts (CMS can produce, not exposed), the delta chips needed round counts (13% of
companies), the comparison bars needed total raised (6% on the long tail), and the timeline
needed dated event history that is not confirmed anywhere. Two of its ten styles were written
lines, not fields. That set was building on sand.

**Row N uses only what the brief confirms is present for all 74,388** — logo, name, sector,
sub-sector, city, founded year, company type, description, website, socials — plus Inc42's own
articles, which exist for any company reachable from the news.

Twelve styles: 01 The sentence (the description as the card — 100% populated and unused
today) · 02 The headline (Inc42's latest story is the card, the company is the byline) ·
03 The age (founded year as the figure) · 04 The type stamp (Bootstrapped / Listed as a
graphic) · 05 The taxonomy (sector → sub-sector set large) · 06 The index card (all spine
fields as a record) · 07 The wordmark (name at maximum size on brand orange) · 08 The stack
(three headlines under one name) · 09 The place (city as the organising idea, with a company
count) · 10 The pair (two companies sharing a sub-sector) · 11 The quiet list (dense utility
rows — every list needs one) · 12 The count (74,388, and the sector splits).

**N1** assembles five of them into one page: headline card → sentence card → place card →
quiet list → count card. Five different shapes, no chart anywhere, nothing invented.

The principle worth keeping: **impact from type scale, colour blocking and composition rather
than from charts** — which is also the only thing that survives when a company has no
numbers, i.e. most of them.
