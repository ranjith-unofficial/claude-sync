---
name: project-inc42-askinc42
description: "Inc42 app — AskInc42 (AI assistant) in-app placement; PRD v1 drafted 2026-08-02 (https://claude.ai/code/artifact/320582bd-1b52-495f-9980-92310d6621e8), matched to Pulse PRD's rigor level"
metadata:
  node_type: memory
  type: project
  originSessionId: cfdaafef-22f2-4a21-a0ed-5e11ce4c0f5f
  modified: 2026-07-31T10:45:42.036Z
---

Bringing **AskInc42** (the AI assistant already live on inc42.com, mainly inside **Datalab**) into the mobile app. Scoped with Ranjith 2026-07-30/31. **Pre-PRD — direction agreed, PRD not written yet.** Post-launch feature; the app went public 2026-07-22 ([[project-inc42-launch]]).

**Sequencing (confirmed 2026-07-31): AskInc42 ships first, [[project-inc42-social-intelligence]] (Pulse) second.**

## "Compass" — false alarm, dismissed
The Login-screen "Compass, your AI co-pilot" text was **sample/placeholder content in the Figma file**, not a real competing initiative (Ranjith confirmed 2026-07-31). Not a blocker. No reconciliation needed.

## Placement analysis — REDONE 2026-07-31 against the confirmed real IA
The 2026-07-31 (early) version of this analysis (brief-end primary, article secondary, guessed "Companies" candidate) was scoped **before** the full IA was confirmed. The real IA (see [[project-inc42-app-structure]]) is: 3-tab bottom nav (Brief / Explore / Watchlist), a persistent cross-tab header (streak badge + profile avatar), Streak living in the header + a dedicated deep page, and a brief-end sequence that already ends in a content carousel, not a blank state.

**Core psychology kept, re-tested against every real surface:**
- Web intent = research (question already formed) → blank input works. App intent = consumption → **no seeded question, so a blank "Ask" entry point still dies anywhere it appears.** This holds regardless of which tab/surface.
- Intent is inherited from the entry point — never ask the user what they want.
- Peak-end rule: the last moment of an engaged session is the highest-leverage, cheapest-to-learn-from screen.

| Surface (real, confirmed) | Verdict | Why (re-tested) |
|---|---|---|
| **Brief-end** (after streak celebration) | ✅ **Primary — but repurpose, don't stack.** | This screen is **not empty** — it already runs streak hero → "Explore Trending Stories" carousel → "EXPLORE MORE" CTA. That carousel is generic content recirculation solving the same "what now?" job Ask would solve, just worse (no personalization, no seeded intent). **Recommendation: replace the "Explore Trending Stories" carousel slot with Ask's tappable question chips** (chips generated from that day's cards — same interaction pattern already validated by Explore's own filter-chip UI), rather than adding a new block and re-triggering the two-rewards-compete risk. |
| **Article detail** | ✅ Secondary — confirmed, and reinforced. | Deeper intent, lower volume, as before. New evidence: the account-deletion screen already buckets **"Saved articles & Ask history"** together as one data category — the product's own data model already assumes Ask lives conceptually next to saved articles, not next to streak/watchlist. |
| **Watchlist tab** | 🆕 **New candidate, worth a v1.1 look — missed entirely in the earlier guess.** | JTBD here is closer to web's "question already formed" than Brief's "consumption": a user opening Watchlist has implicit intent ("what's new with the companies I track"). A per-company "Ask about [Company]" affordance is arguably better-seeded than brief-end chips. Don't ship in v1 — but flag for Utkarsh/Nityam as the strongest non-obvious candidate once query logs exist. |
| **Explore tab (Articles/Companies)** | ❌ Still rejected as a blank entry point, ✅ confirmed as the UI-pattern precedent. | Browsing/comparison JTBD, no seeded question — same failure mode as a dedicated Ask tab. But Explore's existing filter-chip row (Latest/Top Deals/Financials/Edtech) is proof the chip interaction pattern is already native to this app — reuse it for Ask chips rather than inventing a new component. |
| **Streak header badge / Streak page (full)** | ❌ Rejected, now with certainty. | Confirmed the Streak page is pure gamification (badges, streak-freezes, FAQs, history) — no content or query surface exists there to hang Ask off of. |
| **Profile** | ❌ Rejected. | Settings/identity hub (Edit profile/role/sector, notifications, My Streak). No fit. |
| **Per-card inside the brief** | ❌ Rejected (unchanged). | Adds an off-ramp mid-brief, breaks the completion loop. |
| **Dedicated Ask tab** | ⏸ Deferred to v2 (unchanged) — but now note there's no open 4th tab slot; a dedicated tab would mean adding a tab, not filling a gap. | Ship only once query logs prove unprompted demand. |

**Revised known risk:** the earlier note ("two rewards compete on one screen, sequence not stack") was correct in direction but understated — brief-end doesn't just carry the streak reward, it carries a **second, already-designed recirculation mechanic** (Explore Trending Stories + Explore More CTA). The fix isn't sequencing three things — it's **substitution**: swap the trending-stories carousel for Ask chips in that exact slot, keeping the CTA button pattern ("Explore More" → something like "Ask Inc42" or a specific chip tap). Needs Nityam in design to confirm the carousel isn't load-bearing for some other metric (e.g. Explore tab traffic) before displacing it.

**Blank-box fix (unchanged):** seed with tappable question chips generated from that day's cards (real companies/sectors, not generic prompts).

Assumption Ranjith set: **the app version is faster** than web.

## Open before the PRD
1. **Resolve the Compass collision** (above) — this now comes before the other four.
2. Grounded on **Inc42 content only** or open-web? Changes trust + answer scope.
3. **Free or gated behind Inc42 Plus?** Gating changes placement entirely (also note: "Access Datalabs Pro" is already a separate sign-in incentive bullet from Compass — check if Plus/Pro gating already implies Compass is Plus-gated).
4. **Latency budget** — "faster" needs a number; sub-2s or it stays a tab feature.
5. **Success metric** — engagement (asks/user) or retention (D7 of askers vs non-askers)?
6. Whether displacing the "Explore Trending Stories" brief-end carousel has a metrics cost Nityam/analytics needs to sign off on.

## ⚠️ Recognition-over-recall correction (Ranjith, 2026-07-31) — supersedes/extends the chip-timing fix below
Ranjith went further than the timing fix: even a "last card" or "cross-card pattern" chip fails if the user can't **recall** the content well enough to find the question meaningful. Consumption intent (brief-end) means shallow encoding — people skim to finish, they don't necessarily retain detail. A bare text question ("Why did investors bet $350M on Zepto?") forces recall; the user may not have it, which makes the feature feel worse than a blank box, not better.
**Root cause, generalized:** the usability principle is *recognition over recall*. Article detail and Watchlist don't have this problem structurally — the anchor (the article body, the company name/badge) is still on screen when the question appears. **Brief-end is the only surface where the anchor has left view**, so it's the only one that has to manufacture recognition back.
**Fix applied to the artifact:** stop proposing bare text chips at brief-end. Keep the existing card's headline + thumbnail (the recognition anchor already in the current "Explore Trending Stories" carousel) and change only the CTA underneath — add "Ask: why now?" alongside or instead of "View Full Article." For cross-card synthesis questions, show the small thumbnails of the 2–3 contributing cards alongside the question, not just the sentence.
This changes the *design* of the brief-end swap (Section 06) — it's no longer "carousel → text chips," it's "same cards, new CTA." Placement verdicts (brief-end primary, article-detail secondary) still unchanged; this only fixes how brief-end's Ask surface should look.

## ⚠️ Chip content strategy correction (Ranjith, 2026-07-31)
Ranjith caught a real inconsistency: a single-story chip (e.g. "Why did investors bet $350M on Zepto right now?") does **not** belong at brief-end — by the time a user finishes all ~10 cards, the specific curiosity from an early card has faded (this is the doc's own curiosity-gap-timing principle, Section 03, which the original worked example contradicted). **Resolution, not a placement change:** brief-end and article-detail need *different kinds* of questions, matched to what's still fresh —
- **Article detail** (seconds after reading one story) → single-story questions (the Zepto example belongs here)
- **Brief-end** (after the whole brief) → chips must be **recency-weighted to the last card read**, or **synthesis questions spanning multiple cards** ("3 of today's cards were quick-commerce layoffs — is there a pattern?") — a question that only exists *because* the user saw everything, so it doesn't fade the way a single-story question does
Placement verdicts unchanged (brief-end still primary, article-detail still secondary) — this only changes the **chip-generation logic** for brief-end, which the original "generated from today's cards" language got wrong (it implied any card, not the last one or an aggregate). Artifact updated with two separate worked examples reflecting this.

## Market scan (2026-07-31) — full writeup published as an artifact
Full strategy doc (JTBD, Hook-model psychology, placement matrix, competitor scan, sources) published here: https://claude.ai/code/artifact/065326a9-7085-4241-b56d-573b0d49439c

Key findings that changed the plan:
- **Watchlist/company-page placement promoted from "v1.1, worth a look" to a real v1 candidate.** Two unrelated competitor categories converged on it independently: **Crunchbase Scout** (AI assistant on every company profile page, B2B market intel) and **Robinhood Cortex** ("Stock Digests" on the stock detail page explaining why a ticker moved, consumer fintech, Gold-gated $5/mo, "hundreds of thousands" adopted, 95% positive feedback). Two unrelated categories landing on the same answer is real signal.
- **CB Insights ChatCBI** — natural-language research LLM gated to a dedicated "Strategy Terminal" tier for VC/M&A users — supports gating *deep* query tools behind Plus/Pro rather than exposing everywhere.
- **PitchBook** chose not to build its own chat UI — federated its data into Microsoft 365 Copilot/Excel instead (announced 25 Jun 2026). Counter-model: meet the user in their existing tool. Less applicable to a consumer app with no obvious "host tool."
- **Bloomberg Terminal** — rebuilding around conversational-first AI, but reporting notes senior traders still use the old Terminal "because they have always used it." **Caution, not validation**: a new interface layer doesn't guarantee the habit moves with it. Reinforces why the brief-end plan is "swap the existing carousel," not "add a new competing block."
- **Perplexity** — evolved from a blank-box "answer engine" to a context/memory-aware assistant. Confirms the blank-box-fails logic already in this doc.
- **Spotify AI DJ** — best pure habit-formation numbers found: >50% of first-time users return next day, 25% of listening time on engaged days, +15% retention, 140 vs 99 min/day (AI vs non-AI users). Treat as **directional only** — Spotify's JTBD is continuous ambient consumption, Inc42's is a short daily digest, not transferable 1:1.
- **Arc XP "Ask The News"** (Washington Post's Arc XP, launched 13 Jul 2026) — closest category comp: AI Q&A grounded only in the publisher's own reporting, with attribution/editorial safeguards. Ships a **"Subscription Gateway"**: the paywall prompt shows only *after* the reader gets a useful answer, not before. **Directly informs the open free-vs-Plus question** — answer-then-gate is a real, live alternative to a flat upfront Plus-gate, and fits Inc42's "the daily read is deliberately free" stance better.
- **Tracxn / Entrackr / YourStory** (direct Indian competitors) — no comparable AI assistant feature found in the public record. Whitespace, not validated demand — no local precedent, but also no local competitive pressure forcing this.

**Revised v1 plan**: Brief-end (swap carousel, reach/activation) + Watchlist/company page (signal quality, industry-proven placement), Article detail stays secondary but instrument separately. Dedicated tab still v2-only. Gating: test Arc XP's answer-then-paywall pattern instead of defaulting to a flat upfront Plus-gate.

Related: [[project-inc42-content-personalization]] (the brief itself), [[project-inc42-social-intelligence]], [[project-inc42-app-structure]] (full IA + evidence trail for all of the above).

## Refinements (Ranjith, 2026-08-01) — memo updated, artifact republished at the same URL

**Brief-end downgraded from confirmed "Primary" to "Primary — pending data."** Ranjith pushed back: peak-end rule only justifies brief-end as the lead surface if brief *completion* is meaningfully high — and no completion rate exists anywhere in this scoping. It's not an unknowable unknown: `brief_completed` already has to be tracked as an event, since Streak logic depends on it ([[project-inc42-content-personalization]]). **Action: pull `brief_completed` from the warehouse before writing brief-end into a PRD as the primary surface.** If completion is low, article-detail and Watchlist — neither of which require finishing the brief — become the more defensible leads instead.

Note: the earlier recognition-over-recall objection (can readers meaningfully engage with a question after 8 cards) was a separate, already-resolved concern — solved by re-showing the card thumbnails/headlines next to the question so it's recognition, not recall. Ranjith flagged that the memo was presenting peak-end and recognition-over-recall as two competing open principles instead of one resolved argument; merged into a single section in the artifact. The *reach* question (completion rate) is the one still genuinely open, and it's separate from the *recall* question (already closed).

**Role-reframed chips added to article-detail (v1-shippable).** Same underlying question, phrased through the reader's stored profile role (Founder / Investor / Operator — "Edit Role" already exists in Profile). This is a generation-time prompt change, not a matching/ranking problem — **it does not depend on sector tagging**, so it sidesteps the sector-personalization failure entirely (86% of articles have no `Company_Industries`, per [[project-inc42-content-personalization]]). Example: Zepto's $350M raise → investor gets "why did investors bet now," founder gets "what playbook did they run," operator gets "what does this mean for quick-commerce hiring."

## PRD v1 drafted (2026-08-02)
Full PRD published: https://claude.ai/code/artifact/320582bd-1b52-495f-9980-92310d6621e8 — structured to match Utkarsh's Pulse PRD v2.0 rigor (numbered locked decisions D1&ndash;D9, proposed kill criteria, explicit tier-boundary proposal, legal/DPDP gate called out by section).

**Session inputs that shaped it (voice-transcribed brainstorm, 2026-08-02):**
- Placement expanded beyond the 07-31 matrix: **company detail page** and **sector detail page** added as new candidate surfaces; Watchlist reframed as 3 sub-tabs (Companies/Articles/Sectors), each with its own Ask context.
- **Access locked: logged-in only.** Auth flow: logged-in tap → chat opens and auto-fires the seeded question (no second tap); logged-out tap → login prompt → post-login auto-fire of the same original question (intent never discarded).
- Chat history persistent + thumbs up/down feedback → evals, both locked.
- **Two modes locked: Fast (cached/surfaced, sub-2s target) vs Deep (Datalab-grounded, no hard latency target)** — resolves the old single-latency-number tension from the placement memo.
- **Question-generation design refined twice:** first pass (Persona × Topic template) was rejected by Ranjith as too generic ("why did investors bet here" fits every Deals article, is specific to none). Fixed by flipping what Topic × Persona does — it sets a *rubric* (what fact to extract), not the sentence; the model must ground the question in a specific number/name/comparison from that article, validated by checking the generated question against the article body; failure falls back to the plain template, tagged for eval tracking.

**⚠️ Critical gate surfaced while drafting the PRD, not from this session's transcript:** cross-referencing [[project-dpdp-compliance]] found that the *live* Privacy Policy §5.1 already names Ask Mode/AI features as active, but **no LLM/AI sub-processor is disclosed anywhere** (§7.1, §8) — no DPA, no zero-retention/no-training terms on file. [[reference-inc42-vendor-stack]]'s verified audit found zero LLM vendor in live traffic, consistent with the gap. Bringing AskInc42 into the app scales this exposure (persona/role, Watchlist context, and persistent chat history all start flowing into prompts) rather than opening a new problem. **This blocks nothing today but should not wait for the full 3-phase DPDP engagement (Shivang, May 2027 deadline) — it's fixable independently and should be raised with Utkarsh separately.**

**Still open, carried into the PRD's Section 17:** current app launch status (unconfirmed since the Jul 22 date proved wrong), Edit Role's real enum values, AskInc42's current backend/architecture, "MCP something," the Android native screen, "me-too ads," and what "the chatbot needs to understand how the app works" actually means. None of these were guessed at in the PRD — see [[project-inc42-askinc42-next-week]] for the ones tracked as active tasks.

## PRD went through 4 versions in one sitting (2026-08-02) — see [[feedback-document-calibration]]
Same URL throughout: https://claude.ai/code/artifact/320582bd-1b52-495f-9980-92310d6621e8 — currently **PRD v4**.

**v1 → v2 → v3 → v4, what actually changed each time:**
- v1: Utkarsh-Pulse-style structure (D1-D9 decision log, kill criteria, legal gate, tiering) — Ranjith said too much invented detail (fabricated kill-criteria numbers, a legal contingency plan he didn't ask for).
- v2: rebuilt around his literal 9-question outline (why/JTBD/positioning/terms/placement/fallbacks/content) — he then said it was *too thin*, one-liners with no argument behind them, "I have no pointers on" the reasoning.
- v3: restored full reasoning per decision — but over-corrected: narrated rejected brainstorm alternatives (the "peak-end rule"/end-of-brief-screen idea that was dropped) and invented unrequested infra (a URL/deep-link routing scheme, a Free/Plus tier table for a feature that has no monetization decision).
- v4 (current, landed): state decisions directly, reasoning only where it prevents real confusion (e.g. sector page vs. Watchlist's Sectors sub-tab), no brainstorm narration, no speculative sections. Also fixed a real error carried since v3: I'd invented an "editorial approval queue" for generation — the actual mechanism Ranjith described is simpler, AI drafts the persona titles when an article is published, the editor sees and can edit them as part of that same publish action, no separate queue/approval state.

**Other v4 corrections, now locked:**
- **No paid version.** Fast and Deep modes are both free, for now — the earlier Free/Plus tier proposal is gone.
- **Delayed-response notification** — if a reader closes the app before an AI response finishes, a push notification tells them it's ready and deep-links back to it.
- Content-examples section and the proposed URL-routing section were both cut as unrequested/unnecessary at this stage.

Related: [[feedback-document-calibration]] (the general lesson), [[feedback-ask-before-assuming]] (same root cause, mirror case).

## Backend/mobile-optimization PRD merged in (2026-08-02), D13-D15 added
Ranjith shared a separate, engineering-side "Ask42 Mobile Optimization" PRD (source unspecified — "I got it from somewhere else") covering three problems with the current AskInc42 backend: unacceptable latency (n8n webhook hop + a keep-alive hack that bypasses timeouts, causing 8-25s hangs), context blindness (no screen/entity awareness), and hostile formatting (900-word walls of text, broken Markdown tables, raw links instead of tappable citations).

Pulled into the product PRD, product-level only (the n8n/SQLAlchemy/asyncio implementation detail stayed out — that belongs in the engineering doc, not this one):
- **D13** — context resolution: each surface (story/article/company/sector) passes its entity automatically so a query resolves without the reader naming it; an explicit ask about something else overrides it. This is the actual mechanism behind the "every surface already implies a question" JTBD claim (Section 02) that had no stated mechanism before.
- **D14** — response format: ~150-200 words per response, no Markdown tables (bullets instead), sources as tappable citation cards instead of inline links. Ties directly to the trust positioning (Section 04) — citation cards make "grounded in Inc42's reporting" visible, not just claimed.
- **D15** — latency guardrails, **Ranjith's numbers, not derived from the shared doc**: Fast mode targets 5s, never exceeds 10s; Deep mode never exceeds 30s. Current backend runs 8-25s — already over the Fast-mode ceiling. Added as a new Section 01 "Problem statement" subsection naming all three frictions, plus guardrail bullets in Section 11 alongside the existing brief-completion guardrail (D9).

Doc now at 15 locked decisions total. Latest DOCX: `AskInc42_PRD_v5.docx`, built via python-docx (same script pattern each time — `build_prd_docx.py` in the job tmp dir — update in place rather than rewriting from scratch for future revisions).

## Personas resolved (2026-08-02) — D16, closes the oldest open thread in this project
Ranjith shared the real onboarding "Edit Role" screenshot (`Screenshot 2026-08-02 at 2.22.51 AM.png`, confirmed to match Figma too). **Five personas, not three** — every earlier guess (Founder/Investor/Operator, or Founder/Investor/Partnership) was wrong on count:
1. **Founder** — "Track startups, competitors, funding, and market opportunities."
2. **Investor** — "Discover investment opportunities with trusted startup intelligence."
3. **Operator** — "Stay ahead with market signals, industry trends, and company updates."
4. **BD & Partnerships** — "Find companies, decision-makers, and potential business partners."
5. **Other** — "Explore startup data tailored to your interests and goals." No specific angle to draft toward — gets the generic template question, same fallback path as D7's Watchlist message pool.

Added to the PRD as D16, with the confirmed table and two new rubric rows (Operator, BD & Partnerships) in Section 06. Doc now at 16 locked decisions. **Still not done:** the full 8-topic × 4-persona rubric grid (32 cells, Other excluded) is still only a representative slice — worth finishing now that personas are locked, nothing blocking it anymore.

**Also still open, not yet resolved:** the D13 context-override detection mechanism (how the system tells a referential query apart from an explicit topic change) — flagged in chat twice, never actually written into the document as a caveat. Offered to add it; no answer yet.

## D17 added (2026-08-02) — persona lens pattern
Ranjith asked for the general pattern behind each persona's question, not exact examples — what each persona is "always trying to learn," independent of topic. Added as a layer above the Topic × Persona rubric: **lens + topic-specific fact = the actual question**, so the full 8-topic × 4-persona grid (Other excluded) doesn't need every cell hand-authored, just the lens applied per topic.
- Founder → what strategic/operational move does this reveal
- Investor → what does this signal about risk or opportunity
- Operator → what trend/shift does this represent in the market
- BD & Partnerships → what partnership/relationship angle does this create
- Other → no lens, generic template

Doc now at 17 locked decisions (D1-D17).

## D13 clarified (2026-08-02) — sticky context, not per-message classification
The open gap was "how does the system tell a referential query apart from an explicit override." Ranjith's answer resolved it as a **product rule, not an algorithm spec**: the surface's entity (company/article/sector) is the **primary context for the entire thread**, not just the seeded first message — a reader tapping "Founder" on Zepto's page stays in a Zepto-scoped conversation for every follow-up, on every surface, until they explicitly divert to a different topic. The actual classification logic for "explicit divert" is left to engineering — the PRD locks the *what* (sticky by default, overridden only on explicit topic change), not the *how*. D13's summary line and Section 06's Context Resolution text both updated to reflect this; DOCX regenerated as `AskInc42_PRD_v6.docx`.

**Correction to D17's "Other" row, same session:** Ranjith caught that I'd made "Other" default to the generic template — his pushback: "you cannot be generic because you know the kind of people already, generic should be only for the case of error." Fixed: "Other" readers still have followed topics/sectors captured at onboarding (same fields [[project-inc42-content-personalization]]'s ranking engine already reads), so their question is framed through whichever followed topic/sector the story matches — not a role-based lens, but real signal, not nothing. The actual generic template is now scoped to one real error case only: no role AND no followed topics/sectors. Also fixed a mischaracterization — I'd linked "Other"'s fallback to D7's Watchlist rotation, which is itself already persona-specific, not generic; that cross-reference was wrong and is removed.
