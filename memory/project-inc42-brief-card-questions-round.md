---
name: project-inc42-brief-card-questions-round
description: "Brief entry card 'questions inside' — round 1 (10 static cards, page 681:2) reviewed 13 Sep: keep Folder/Front page/Self-check; round 2 = 6 interaction flows × 4 states on page 692:2; unreviewed"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2108306a-d9b7-4fc6-a2d9-a4a80c791caf
  modified: 2026-09-13T14:21:37.934Z
---

**13 Sep 2026.** Ranjith said Satya's folder card (Inc42-App-2026 `5763:32218`) doesn't convey what Brief is. Ask: a card that says "this is a brief, these are the questions it answers, open today's brief", 2-3 question copies. Draft file `dAsaTgNj0xh25w2OGaurZo`.

## Round 1 — page "Brief Card · Questions (13 Sep)" `681:2`
Ten static cards in Satya's live shell (red header + floating nav). Review, same day:
- **Kept:** V01 Folder of questions, V05 Front page, V06 "Can you answer these yet?"; V07 Photo hero "aligned".
- **Rejected, with reasons (binding):** V03 chat — *looks like it opens a chatbot*. V02 redacted — *Q&A, not interested*. V08 carousel — *people won't be interested*. V09 bento — *not every day has a 72X / 306% number, not feasible*. V10 story rings — *a lot of problems*.
- Ranjith duplicated V01/V05/V06 to x≥2888 on that page (`687:2`, `687:71`, `687:141`) — untouched.
- His direction: *"more mature … how people will interact … do not make this a UI, like color change … think in a different way."*

## Round 2 — page "Brief Card · Interaction flows (13 Sep)" `692:2`
Six flows, each 4 states (fresh → action → back mid-read → done/next day) with a left column: idea / how people get it / needs / open.
1. Folder · Pull a sheet (tap a sheet = open at that story; read sheets sink; FILED stamp) — rows y=300
2. Folder · Explains itself on day one (coach notes, then yesterday's folder behind today's; "still here" if missed) — y=1600
3. Front page · Next unread leads — y=2900
4. Front page · Folds away as you read (full → half → strip) — y=4200
5. Self-check · "I know / Tell me" (reorders brief per reader) — y=5500
6. Self-check · Before → after (rows flip light; card flips to "Now you can"; yesterday strip) — y=6800
Day-2/3 questions are stand-ins from the 12 Sep pool, labelled on the steps.

**Needs surfaced:** per-story read state; open brief at a chosen story (vs push promise that named stories are cards 1–3); card copy + image for every story (not just top 3); first-visit flag; past briefs reachable.

**Round 2 review (13 Sep):** red tap-marker dot = "big no-no"; F4.2 half-fold = "just a list"; Flow 5 (I know / Tell me) "not making sense", dropped; not interested in the lifecycle states. Asked for 10 more formats of the first (fresh) card, same 3 questions, built on marketing psychology: how people perceive it, what makes them agree to open, what makes them come back.

## Round 3 — page "Brief Card · Psychology round (13 Sep)" `704:2`
Ten fresh-state formats, each with a note (Lever / Why they open / Why they come back / Needs):
C01 Sealed envelope "For Satya" 704:5 (curiosity + endowment) · C02 Editor's note, questions in prose 704:78 (authority) · C03 Magazine cover 704:146 (picture superiority, cover lines) · C04 From the pile 704:218 (labour illusion) · C05 Reader pass 705:2 (identity/commitment) · C06 Week chain 705:87 (loss aversion) · C07 Open questions, pinned photos 705:195 (Zeigarnik) · C08 One big question poster 706:2 (isolation effect) · C09 Filed by reporters 706:71 (authority; WP avatars are defaults, initials used) · C10 Pick a door 706:159 (alternative-choice close; needs open-at-story).
Rows y=360 / 1640, x step 490. No tap markers, no lists, no counts.

**Round 3 review (13 Sep):** all rejected. Envelope "useless"; editor's note "too textual"; cover "somewhat okay"; pile + pass "too many things, can't tell what to focus on"; week chain / open questions "can't relate" (open questions "could work" but not with the UI and not developer friendly). Interaction flows "okay-ish". Missing across everything: **subtle urgency** and **a personalisation signal** ("is this a personalised brief?"), and **developer-friendliness** ("what if the image is too long?").

## Round 4 — page "Brief Card · Folder, dev-ready (13 Sep)"
Base = his pick V01 (duplicate 687:2). 8 folder variations, each as normal + stress-test pair, all auto-layout, 2-line clamps, fixed image boxes; shared rules block in the page header (urgency: streak ≥2 else "Fresh since 7:00 AM"; personal: "Ordered by what you follow" else "Top stories since yesterday"; reason tag "You follow X" / "Also moving today").
A Folder refined 718:7/718:90 · B Lead photo 718:180/718:259 · C Thumbnails + reason tags 719:2/719:94 · D Lead cover 719:197/719:280 · E Sheets in the pocket (negative spacing) 722:2/722:92 · F Compact + also-inside chips 722:192/722:269 · G Picks up where you left off 724:2/724:89 · H Personal header (name, follow chips, Edit) 724:188/724:281.

**Round 4 review (13 Sep):** "not visually appealing"; no "you follow IPO / Fintech" labels — personalisation must be *felt*, not stated; wants Inc42 logo on the card, simpler, social proof ("so many people completed the brief"), marketing pull to open; keep folder direction; think about lead-image placement.

## Round 5 — page "Brief Card · Folder round 5 (13 Sep)"
10 folder versions, real Inc42 logo (SVG exported from Satya's frame, node 6488:9914), name-based personalisation, real social proof, one image placement each:
01 Satya's Brief 727:7 · 02 Photo cover "Good morning, Satya" 727:96 · 03 Clipped photo "Picked for Satya this morning" 727:187 · 04 Split header 727:278 · 05 Prepared-for stamp + pocket 727:368 · 06 Start here (one big lead) 728:2 · 07 Kraft light folder 728:92 · 08 Three photos 728:182 · 09 Day 12 streak 728:276 · 10 Join them (proof in CTA) 728:370.

**Real numbers used (PostHog app 146258, 13 Sep, ritviksethi56 excluded):** brief_completed unique/day 25–44 (33 on 12 Sep); 138 unique in last 7 days; 461 all-time since 10 Jul; median open→complete 82 s (IQR 32–210 s, n=320, 10 days); brief_opened unique/day 60–92. Proposed display rule: today's count once ≥30, else week count, else "Most readers finish in under 2 minutes".

**Round 5 → Satya's card (13 Sep):** Ranjith moved to Satya's card in Inc42-App-2026 — `6559:3292` "BRIEF PAGE · question loop" (folder, logo, edition note + paperclip, week tabs, "Today's Brief", "By the end you'll know :", 3 numbered questions in an inner panel, "1,284 READING" chip, white CTA; motion study section 6674:3292: highlighter sweep / printed-in / CTA light orbit / CTA shake). He "almost likes" it. Asks: too many boxes inside boxes, can't tell the headline; numbering 1/2/3 doesn't work; replace "1,284 reading"; card can be bigger, use the space; convey there is MORE inside beyond the 3 questions, while staying minimal; plus urgency subtle, personalisation felt, dev-friendly.
Flagged to him: 1,284 is not real (60–92 open/day, 25–44 finish); "Monday's edition 8 September" wrong (8 Sep 2026 = Tuesday).

## Round 6 — page "Brief Card · Satya card, no boxes (13 Sep)"
8 variants of Satya's card, no inner panel, 342 px wide, questions 20 px Fraunces on the folder, auto-layout:
A Hairlines + "5 more answers inside" 736:6 · B Fade into 4th question + "and 4 more inside" 736:103 · C Big lead + "Also inside: OpenAI, Ultraviolette, PhonePe and 2 more" 736:198 · D Rail to open marker "5 more" 736:294 · E Pages underneath "5 more answers filed inside" 738:2 · F "Starting with" + CTA "Open all 8 answers" 738:99 · G Cream folder 738:191 · H "8 answers" count hero 738:288.

**Status:** round 6 unreviewed. Related: [[project-inc42-brief-copy-variants]], [[project-inc42-brief-title-per-article-copy]], [[feedback-design-review-ranjith]], [[reference-figma-mcp-build-techniques]].
