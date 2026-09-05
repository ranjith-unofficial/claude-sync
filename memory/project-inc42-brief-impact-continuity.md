---
name: project-inc42-brief-impact-continuity
description: Brief page impact score and continuity personalisation (5 Sep 2026) — validated on 1,179 articles; the ranking formula has no story-level importance signal
metadata:
  type: project
---

**The finding (5 Sep 2026):** the personalised-brief ranking formula has **no story-level
importance signal**. `Pop` is a category constant — every `Startup IPO` article scores 0.116
whether it is Zepto's ₹8,010 Cr filing or a seed-stage company saying it may list in 12–18 months.
Same (topic, sector) = identical score, separated only by recency. That is why no design has felt
prominent: there was nothing to make prominent with. Raised by Ranjith as "how do we prioritize
any news, how do we show impactfulness".

**Impact score, built and validated on 1,179 articles (6 Jun – 4 Sep):**
`0.40·event + 0.25·company_stage + 0.20·magnitude + 0.15·editorial`
- event = `development_type` (85% coverage); company_stage = `company_type` (85%, unused until now);
  magnitude = ₹/$ parsed from headline, log-scaled (47%); editorial = Exclusive/Investigative,
  In-Depth, or `shelf_life` > 3 days.
- **Clear hero on 57% of weekdays; no hero on 25%** (layout must change, not fake one).
- Reorders vs recency on 91% of days. Ranjith's IPO + big-company example occurs on 52% of days.

**Continuity beats category for personalisation.** 98% of weekdays contain a company covered in
the prior 30 days (median 3 of 8, ≥3 on 75%). Editorial already tags `Follow Up` (6%) and
`Series` (11%) — 94% of weekdays carry one. "The 4th Zepto story you have seen this month" reads
as personal; "you follow Ecommerce" does not.

**Personalisation hides big news:** a ≥0.62-impact story is cut from the top 8 on 58% of days
(Deals+Fintech), 48% (Ecom+IPO), 72% (AI-only) — justifies a `Big today, not in your brief` section.

**Also established:** `sentiment__tonality` is "Positive" on 1,178/1,181 — a default, unusable for
a positive/negative day signal; tone must be derived from development type. The *Inc42 Daily Brief*
newsletter title exists on 62/65 weekdays (~08:00) and solves Utkarsh's "static title" objection —
needs the CMS draft field exposed at 07:00.

Row L in draft file `dAsaTgNj0xh25w2OGaurZo` (y=99600) builds it on three real days.
Spec: `~/ClaudeDocs/inc42/brief-entry-coverage-spec.md`.
See [[project-inc42-brief-entry-coverage]], [[project-inc42-content-personalization]].

## Update 5 Sep — impact enters the ranking, and the jargon purge
`score = 1.0·TopicAff + 0.6·SectorAff + 0.15·Pop + 0.4·Impact`. At W_impact=0.4 the day's
highest-impact story reaches the personalised brief on 97–100% of days (vs 30–73% today) while a
followed story still leads 97% of days. This **deletes** the "Big today, not in your brief" section —
Ranjith's objection was that it implies the brief is incomplete and invites "if it's so big, why
isn't it in my brief?". Fixed in ranking, not copy.

**Terms banned from the UI:** "cards" (→ stories), "DataLabs" (→ describe what it holds),
"10-minute read" (→ state the payoff), "In-Depth" (→ "one longer story").

**DataLabs researched (5 Sep):** company pages are on inc42.com/company/{slug}, same domain.
Free tier includes search, live signals, preview metrics; Pro ₹1,499/mo adds full P&L, MCA, cap
table, exports, contacts. Zepto page carries free: total funding $2.45 Bn, revenue ₹4,178.3 Cr FY24
+101%, 39 investors, employees 19,938 +6.55%/90d, web traffic 2.44 Mn −2.21%/30d. The four
self-explanatory numbers for a media reader: revenue+YoY, loss, total funding, headcount+trend.

**Structure:** three pages (The brief · Companies · Deeper) under one sticky completion bar
(`0 of 8 read` + 8 segments). Page 1 leads with the numbered SET, not a hero article — that is what
stops it reading like an article. Onboarding = 3 screens (14→8 shown, pick sectors, the 7 AM deal).
Row M in the draft file.

## Row P — four content rules (5 Sep, from Ranjith's rejection of row N)
1. **Never state the publish count.** "8 of the 14 published today" makes Inc42 look like it
   publishes very little. Completeness = an outcome ("read them and you are done for the day"),
   never arithmetic.
2. **Every story needs a reason chip.** Marking only the followed ones makes the rest look like
   filler — "what happens to the non-highlighted ones?". All eight get a label:
   BIGGEST TODAY / YOU FOLLOW X / BIGGEST ROUND / MOST READ NOW / FROM OUR NEWSROOM.
3. **Continuity is a row marker, never the headline.** Leading with the Zepto thread made the whole
   brief look like it was about Zepto.
4. **Time copy needs a subject.** "Expires tonight, tomorrow arrives at 7 AM" → "This brief is only
   for today. Tomorrow's brief arrives at 7 AM."

Six full-page structures in row P: THE DECK (pliability daily-sessions stack), THE RANKED RAIL
(Apple TV Top 10), THE PATH (Alan/Duolingo), THE REMAINING (Finch "10 goals left"), THE SPREAD
(magazine cover + contents), THE BRIEFING (dark, reason-first left column).

## Rows R and S (5 Sep) — what the content can actually support
- **Continuity cannot lead the card.** Top story is about a company seen in the prior 30 days on
  48% of weekdays; seen twice (so "3rd story about them" is true) on only 32%. Row R built all 15
  cards on Zepto continuity — Ranjith rejected it as cherry-picked, correctly.
- **Aspirational copy is the recurring failure.** Lines needing a daily editorial thesis
  ("quick commerce just ran out of private money") are not producible. Design only from fields that
  exist daily: headline, development_type, company, company_type, counts, headline figures, streak,
  read history.
- **The Daily Brief newsletter title is not a clean spine.** 11 June's title names ZEE5 and WinZO —
  neither is in the impact top 8 that day. 18 June (13 stories) has no Daily Brief post at all.
  Using it on the card requires ordering the brief to match it.
- **Anti-article rule:** an article card is one photo + one headline + one standfirst. A brief card
  must carry a masthead (publication + edition no. + rule + "chosen by our newsroom"), the word
  "brief" used naturally, and a countable-but-unreadable set of eight. Never lead with a photo.
- Row S builds ten cards on Thursday 11 June — a deliberately ordinary day (nine small stories,
  no IPO, no famous name).
