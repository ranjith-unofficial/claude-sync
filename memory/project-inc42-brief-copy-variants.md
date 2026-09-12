---
name: project-inc42-brief-copy-variants
description: "Brief card copy + push from FULL article text (12 Sep 2026) — LOCKED formula: [anchor lifted from headline] + [one question with a single concrete answer]. 2 questions + 1 aligned push per article. Statements, generic questions and per-interest variants all rejected"
metadata:
  node_type: memory
  type: project
---

**Done 12 Sep 2026.** Ranjith asked for curiosity-led Brief card title variants and push copy so the
same story can be positioned differently per reader interest (startup / investment / founder /
company / industry), with the **top three hooks shown on the Brief entry card**.

## The correction that defines the method
The first pass generated copy from **headline + the 3-bullet CMS summary**. Ranjith rejected it:
*"the title itself is very limited … first understand the article content, then generate a question
and see if that question will be answered by the title and then the article … not the otherwise."*
He also rejected generic pushes and pushes that restate the title.

**Locked method:** pull the **full article body** first, read it end to end, pick the hook from what
the body actually contains, then verify the question is answered and record *where*. If a question
has no answer in the text, it does not get written.

## What that changed, measured on the same 15 stories
- **49 of 61 variants are answered only in the body** — a headline+summary generator could not have
  written them. Only 12 of 61 were derivable from headline + summary.
- **On full text every story supported 4+ angles (15/15). On headline+summary only 8/15 did.**
- **9 of 15 stories have their sharpest hook past the halfway mark** (Ultraviolette's 583 August
  units vs a 2.5 Lakh-capacity factory; Rapido's ₹30-delivery/₹25-driver worked example;
  EaseMyTrip's pledge total being *unchanged*; OpenAI's August sandbox escape onto Hugging Face).
- CMS `push_notification` exists on only **5 of 15 (33%)**, and **0 of those 5 open a curiosity gap**
  — all five restate summary bullet 1. Matches the 20% write-rate in
  [[project-inc42-brief-card-corpus-analysis]].
- Median article 539 words, so there is no cost argument for generating from the headline.

## Second correction: scope, 12 Sep
The first full-text pass produced 61 variants tagged by reader interest (company / investment /
founder / industry / consumer) plus per-persona entry-card hooks. **Ranjith cut that too:**
*"The variant cannot be based on the reader interest … one article, two variants … for copy: two
variants … I would not need this level of customization based on topic sector. These will be
over-engineering for now, before even understanding if this is going to be useful or not."*

**LOCKED shape: per article, 2 card copy variants + 2 push variants. Generic to the story, not to
the reader.** No persona hooks, no sector tagging. Personalisation is a later question, only after
the copy itself is shown to be useful. The "Answered in" check survives the cut — it is what keeps
a curiosity hook from becoming clickbait.

## Third correction: relevance, 12 Sep — THE BINDING RULE
The 2+2 pass led with the buried detail *instead of* the story. Ranjith: *"the copy card variant is
nowhere relevant to headline, and people will not be able to understand this … if I talk about
RentoMojo's profit jumped 142% … the headline says RentoMojo IPO ends with 72x subscription. So
these are very highly irrelevant."* He also rejected the formula of a statement with a question
bolted on the end (*"from which country", "who else on it", "what did the company say"*) and asked
for the curiosity to be **coupled into the sentence itself**, plus *"multiple variations so that I
have more understanding … understand the psychology of a user."*

**RULE (binding, applies to every future copy pass): anchor first, then the interesting part.**
The story must be recognisable in the first few words so the reader knows what they are opening.
The detail earns attention *after* the anchor, never instead of it. Curiosity lives inside the
sentence — a contrast, a number, a consequence — not in an appended question. The reader must be
able to close the loop on opening: "that was my question, and it is answered."

**v3 shape: 5 card variants per article, one per mechanic, plus 3 pushes.** Mechanics:
1 Straight (control, no device) · 2 Straight + twist · 3 Question about the **main event**
· 4 So what (the consequence) · 5 Number first. Only mechanic 3 is a question.
A per-row **Anchor** column states what every variant in that row must make recognisable — the
at-a-glance relevance check.

## Fourth correction, 12 Sep — THE LOCKED FORMULA
Ranjith rejected the five-mechanic set: the statement variants *"don't entreat me to open it"*, and
appending a question to a restated headline (*"paste the entire title and say what is this"*,
*"statement, then follow like what do you think"*) is *"not the right way of doing it"*. He also
flagged that the pushes read as a different creative from the card copy.

**The one he approved, verbatim: "RentoMojo's IPO closed at 72.88X. Who actually drove the final
day?"** Everything is now generated to that shape.

**LOCKED FORMULA: [short anchor lifted from the headline] + [ONE question whose answer is a single
concrete thing: a name, a number, a party, a place, a condition].**
- The anchor is compressed from the headline, never repeated whole. It guarantees relevance.
- **The kill test: can you name the one thing that answers the question?** If the answer is an
  opinion, a paragraph, or "it depends", the question is generic and it is cut. This rules out
  "what happened", "what does it mean", "what is it building towards", "what do you think".
- Every variant is a question. Statements do not earn the open.
- **The push is not a separate creative.** Push title = the card question; push body begins the
  answer. Card and push are one idea.
- The two question shapes that work best: (1) **the named unknown** — who / which one / how much /
  where, answered by a specific party or figure; (2) **the wrong-expectation question** — where the
  obvious answer is wrong ("Amazon Pay keeps adding products. Is the business growing?" No, revenue
  fell 8.3%).
- A hook the reader cannot place is a miss however good the fact is: "Rs 30 for delivery and Rs 25
  to the driver" was cut for exactly this.

## Deliverable
Tab **"Brief Copy Variants (12 Sep)"** (gid `1798377423`) in the **Test** workbook
`1NCpTEzgEEtds0uCfqPNSS6aeFhOpKbgkL_F-cgtVPxg` — see [[reference-inc42-open-ledger-sheet]] for the
same workbook. 15 rows, one per article, 9 columns: headline, link, question 1 + what answers it,
question 2 + what answers it, push title, push body. 30 questions and 15 pushes.
Push titles <=45 chars, bodies <=120.
Local: `~/ClaudeDocs/inc42/brief-copy/` (v2 TSV, full article bodies JSON, source articles JSON).

**Source data:** 15 articles in the real 12 Sep brief window (11 Sep 07:00 → 12 Sep 07:00 IST),
WP REST API `?include=<ids>&_fields=id,date,link,title,content,acf` for full bodies — unauthenticated,
one call for all 15.

**Status:** unreviewed by Ranjith as of 12 Sep.

**Why:** the generator's input, not its prompt, was the binding constraint on how interesting the
copy could be.

**How to apply:** never generate Brief or push copy from headline + summary. Pull the body, and keep
the "where is this answered" column — it is the check that stops a curiosity hook becoming clickbait.
Related: [[project-inc42-content-personalization]], [[project-inc42-brief-impact-continuity]],
[[project-inc42-app-feedback-rating-system]], [[feedback-design-review-ranjith]].
