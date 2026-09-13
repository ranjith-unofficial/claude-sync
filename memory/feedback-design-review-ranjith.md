---
name: feedback-design-review-ranjith
description: What Ranjith rejects and accepts in UI design reviews — earned over ~26 rounds on the Inc42 gratification screen
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 32dcfc27-29c8-427f-8e82-f96c2295f2dd
  modified: 2026-08-30T10:32:35.745Z
---

Patterns from a long design engagement (29-30 Aug 2026, Inc42 brief-completion and welcome
screens). He iterates hard and rejects fast; these are the rejections that repeated.

**Never state a number that can vary or that a first-time user cannot parse.**
"8 stories a morning" drew *"what is stories?"* — feature-nouns mean nothing before someone
has used the app. "8 stories / 90 seconds" also breaks the moment a weekly recap runs 10+.
Naming a **product** ("the Brief") is fine and builds equity; naming a **count** is not.
Cadence phrasing that never breaks: "every morning", not a duration.

**Never describe content by what the user did not choose.**
"NOT YOUR SECTORS / OPTIONAL" made him feel he was *missing something he followed* — a
deficit frame, and "optional" implies an obligation exists elsewhere. Even a denial
("nothing you need to read") invokes the obligation by naming it. Additive framing only:
`ALSO WORTH KNOWING`, `ALSO MOVING TODAY`. **Closure first, discovery second, obligation
never.**

**Decoration without meaning gets cut.** Radial "burst" rays around a circle: *"not making
a lot of sense"* — they carried no information. He keeps confetti (it marks a moment) but
cuts lines that merely fill space. Similarly a scalloped medallion read as *"a Rakhi"* —
ornamental, not achievement.

**But minimal is not the goal either — he wants visual weight.** Stripping to plain text on
flat colour got *"there is no visual attraction"*. The resolution is contrast and scale, not
ornament: a luminous focal element on a deep ground, one hero rather than a grid of equal
tiles. A 2×2 stat grid read as *"a dashboard, not a reward"*.

**Show, don't tell — explicit value claims undercut themselves.** *"We cut the noise"* as
on-screen copy "loses its essence"; he wants the user to *feel* it. Best-performing move was
showing the mechanism (noise funnelling into one Brief) rather than asserting it. Note the
same visual can fail on one screen and work on another: pile-to-pick was rejected on the
completion screen ("can't relate") but is right for onboarding, where explaining is the job.

**Ask for research before redesigning after a second rejection.** He explicitly asked for
Mobbin/competitor grounding, and it changed the outcome every time — real precedent settled
arguments that opinion could not.

**How to work with him:** build, don't describe — *"give the design, I am not able to
understand"* when given prose. Ship 3-5 variations per round, state a recommendation with
reasoning, and flag what needs real data before it can ship. He edits Figma frames directly
between turns, so **re-read the file before assuming your last state holds**, and treat his
edits as the new baseline. Related: [[feedback-communication-style]],
[[feedback-ui-mockup-research-first]], [[reference-figma-mcp-build-techniques]].

**"Different designs" means different STRUCTURE, shown in the real screen (6 Sep 2026).** Round 2's
fifteen "UI types" were rejected as "coming with the same design" because they varied the mechanic
on the same card; Satya's folder round was praised for being an object, but he then refused
fifteen folder variants. What he wants: fifteen different *structures* for the same content
(inbox, checklist, memo, graph, table, changelog…), each placed inside the actual app screen
with the live greeting header and nav — not floating cards. See
[[project-inc42-brief-entry-round3-15-structures]].

**No lists. Ever. (6 Sep 2026, round 3 → 4.)** Fifteen "structures" that were all row-based (inbox,
checklist, table, memo, threads…) got "very poor … never ever give me this design … everything is a
list … I cannot show the entire list." What he means by "design itself" is a spatial object with
visual weight — orbit, treemap, ring, skyline, mosaic — where size/position/colour carry the
meaning and the eight stories are never stacked as rows. The one round-3 survivor was the graph.
See [[project-inc42-brief-entry-round4-15-objects]].

**Brief card round, 13 Sep 2026 — rejections with reasons.** A chat-bubble card was cut because it
*implies tapping opens a chatbot* (the visual metaphor sets the expectation of what the tap does). A
design whose visual is a number pulled from the copy (72.88X, 306%) was cut as *not feasible every
day* — any slot must survive days without that field. A variant round that only restyles the same
card is "a UI, like color change": he wants how people **interact over the day** (fresh / mid-read /
done / next day), shown as flows. See [[project-inc42-brief-card-questions-round]].

**No tap/touch markers in mockups (13 Sep 2026).** A red dot showing where the finger taps was a
"big no-no". Show the interaction through the card's state and the step caption instead. He also
wants psychology stated per design: the reason people would open it and come back, not only the
visual.

**Dev-ready + urgency + personalisation are baseline requirements (13 Sep 2026).** Any card round must
show: a subtle, true urgency cue; a visible answer to "is this personalised?"; and proof it survives real
data (long copy, missing copy, tall/missing image) — he rejected a whole round partly for "not developer
friendly … what if the image is too long?". Formats with many competing elements ("too many things, I'm
not sure which one to focus on") and text-heavy cards are rejected.

**Personalisation must be felt, not labelled (13 Sep 2026).** Tags like "You follow IPO / Fintech" were
rejected. Use the reader's name, possessive framing ("Satya's Brief"), their own streak, "picked for"
language. He also wants the Inc42 logo on brand cards, social proof of other readers, and visual
appeal over explanatory labels.

**One page per exploration, and no scroll cues (14 Sep 2026).** Add new rounds to the same Figma page
he is already reviewing — never a new page per iteration. On cards meant to be tapped whole, never show a
partially visible/fading item or sheets peeking out: it reads as scrollable and defeats the card. Say what
the content literally is ("stories"), not a metaphor ("answers").
