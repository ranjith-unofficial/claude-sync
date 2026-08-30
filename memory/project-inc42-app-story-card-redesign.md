---
name: project-inc42-app-story-card-redesign
description: "Story-card (inside the Brief) redesign, 30 Aug 2026 — V28 set built against a real Inc42 story, plus the logged-out streak state and the reaction-control fix"
metadata:
  node_type: memory
  type: project
---

Separate screen from the completion/gratification work in
[[project-inc42-app-brief-gratification-redesign]] — this is the card the reader taps
through *inside* the brief. Started 30 Aug 2026 from Ranjith's brief: the live card
"looks incomplete, very bland, doesn't look like a finished product", and that was
independent feedback from several people too.

## What the live card actually is
Live story card = `2159:11559` (Inc42-App-2026, section `home` `1926:2140`). Anatomy:
masthead, 8-segment progress bar, 390x338 hero illustration with the headline over it,
"THE DECODE · 30-SEC READ", three red-triangle bullets, then an action bar of a black
"Read full article" pill + an 87x46 heart pill labelled **Rate** + bookmark + share.
`3303:2328` (the node Ranjith linked) is a *flattened raster* header-treatment
exploration on top of that card, not a live composition.

**The Rate flow today:** tapping the heart opens a 248x121 dark popover
("Was this relevant to you?" / Relevant | Not for me); the negative path opens a good
bottom sheet with seven reason chips + free text — but that sheet is named
**"Delete · 1 · Confirm popup"** (`2290:1180`), a leftover from the deletion flow, so
nobody searching Figma for the rate flow will find it. There is **no positive-path sheet
at all**; tapping Relevant only fires a toast. Like and dislike are asymmetric in spec.

## The reaction fix (research-backed)
Netflix's collapsed "Rate" thumb is literally the same dead control, and their move from
5 stars to 2 thumbs raised rating volume **200%**. YouTube shipped the *word* under the
thumb. Particle, Blinkist and Apple News keep both halves permanently visible and frame
the negative as a feed preference ("Less", "Suggest less like this"), never a verdict on
the writer. Artifact's 6-emoji set behind a heart is the anti-pattern. Conclusion carried
into every variation: **"More like this" / "Less like this", both visible, inline in the
content block (not the utility row), single tap, words not icons.** Bookmark and share
move onto the hero as glass buttons to free the bottom bar.

## Ranjith's rejections, 30 Aug
- V27-1 had "too many things", no article image, and the **Inc42 Newsroom byline, filed
  time and 30-sec read are not relevant** inside the brief. (Note this contradicts the
  Mobbin finding that attribution is the strongest "finished product" signal — inside the
  brief every story is Inc42's, so it is redundant there.)
- The real blocker he named: **What's new / Why it matters / The detail are long and will
  not fit.** Confirmed against real copy — the Ola Electric PLI story's three summary
  bullets are 19 / 27 / 20 words.

## Method change that mattered
Stopped using invented copy. V28 uses a real story end to end: Ola Electric ₹95.81 Cr
PLI-Auto incentive (WP post 570511), its real featured image, its real scraped summary
bullets. `inc42.com/wp-json/wp/v2/posts?_embed=wp:featuredmedia` gives real headline +
image; the summary block still has to be scraped from the article page.

## The V28 set (draft file `dAsaTgNj0xh25w2OGaurZo`, row y=36600)
1 · Over the image · 2 · Headline does bullet 1's job (backed by the corpus finding that
b1 repeats ~50% of the headline) · 3 · Two taps, one story (split progress segment) ·
4 · Expand in place · 5 · Thumbnail + long body. Row V27 (y=35530) is superseded history.

## Logged-out streak
`V26b-OUT` (x=1800 y=33730): streak numeral 1, one week dot lit, gold
"This streak disappears at midnight." over a white "Log in to save my streak" CTA. The
one place loss framing is legitimate — the streak really is unsaved.

⚠️ **Per-story photography is not a live pipeline** (sector images agreed 12 Aug, owner
Anmol, unbuilt) — variations 1 and 2 depend on a real image per story; 3, 4 and 5 do not.

**Why:** this is the first structural answer to "the card is bland", and the first time
the body-length constraint was designed against real article copy rather than shortened
placeholders.

**How to apply:** read
`~/ClaudeDocs/inc42/brief-completion-gratification-redesign-context.md` before touching
this again — full round history lives there. Related: [[feedback-design-review-ranjith]],
[[project-inc42-brief-card-corpus-analysis]], [[reference-figma-mcp-build-techniques]].
