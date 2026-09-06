---
name: project-inc42-knowledge-repo
description: "Internal knowledge/IP repo (VectorDB) feeding AskInc42 — covers DataLabs IPs, articles, Inc42 products; owned by Ritvik Sethi"
metadata: 
  node_type: memory
  type: project
  originSessionId: 86dbc707-21f1-4c04-8470-7df437b5acf0
  modified: 2026-08-17T18:17:41.806Z
---

New initiative, raised 2026-08-10 (catch-up call, Ranjith + Ritvik Sethi + Satya, Ashish in office). Utkarsh had flagged in a prior call that Inc42 has no central repo/memory of its own internal documents and IPs — spanning DataLabs, articles, Inc42 products generally. Ritvik's proposed approach: add a new table to the existing Postgres VectorDB (already used elsewhere), embed the internal knowledge into it, and feed that into [[project-inc42-askinc42]] as a knowledge source.

**Why:** AskInc42 needs to answer questions about Inc42's own products/IPs (e.g. DataLabs offerings, pricing) accurately and with awareness of what's time-bound — Ranjith's example: if DataLabs has a CTO-tier product, AskInc42 needs to know current pricing, which may itself be time-limited ("valid for X hrs/Y hrs"), implying some of this data may need real-time/frequent refresh rather than a static embed.

**Plan (updated 2026-08-10, same day):**
1. ~~Ranjith to share DB scope + change-frequency with Ashish~~ / ~~Ritvik syncs with Nithyam~~ — superseded by direct step below: **Ranjith himself spoke to Nithyam** (not Ritvik as originally planned), who agreed to help provide the list of underlying data.
2. **Ranjith to research, via the internet, what product types exist across Inc42 and Inc42 DataLabs**, plus each product's terms & conditions / privacy terms — a scoping/discovery pass, not the architecture decision yet.
3. Combine that research with Nithyam's data list into a **multi-product catalog**: what products exist, how each is structured, etc.
4. Only after that catalog exists: discuss, align on understanding, and decide the implementation approach ("replicate the way we want to have it").

**Status:** scope-discovery phase, still pre-architecture. The earlier EOD-2026-08-10 check-in and Ritvik's draft implementation plan (previous plan steps 3-4) are superseded/deferred until the product catalog (step 3 above) exists — don't assume those happened as originally scheduled.

**SCOPE LOCKED (2026-08-12, Ranjith) — the 5 knowledge sources for this AskInc42 release.** This is what the "documents" conversation with Ashish was actually about:
1. **Articles** — everything Inc42 has published, including in-depth startup stories
2. **Company information** — all company-related data
3. **IPs** — the full event/product IP set (see canonical list below)
4. **App context** — how the app itself works
5. **T&C + Privacy Policy** — **high-level abstraction only**, not verbatim clause retrieval

**Canonical IP list (Ranjith, 2026-08-12):** D2C Summit, AI Summit, D2CX Converge, D2C Retreat, CTO Summit, FAST42, D2CX Runway, MoneyX.

**Deflection rules for this release:** pricing → redirect to the website; refunds → deferred, redirect; support and cancellation → **Contact Us page**. AskInc42 does not transact, quote, or resolve.

**DECISION (2026-08-11, Ranjith) — AskInc42 will NOT answer with real IP pricing.** For any pricing question about an Inc42/DataLabs IP, the answer is a redirect: *"visit the website for the best offers."* Two reasons, both deliberate:
1. **Volatility** — IP pricing changes constantly and is owned by the sales/IP team; keeping it accurate is not worth the effort, and the nuances (offer windows, tiering) are the real risk, not the fetch. Pulling prices from the DB would be technically easy — that's not the blocker.
2. **App-store payment policy** — with Inc42 content now going inside the app, quoting a price and pushing users to pay outside the app invites Apple/Google in-app-purchase enforcement. Ranjith explicitly does not want that headache now.

This bounds the knowledge repo's scope: it feeds AskInc42 product/IP *knowledge*, not commercials.

**Owner action (2026-08-11):** Ashish prepared a list of what IP/product documents exist and is sending it to Ranjith; Ranjith to come back with the pricing/knowledge approach **by 3pm same day**. The Postgres VectorDB direction is still the assumed default, but the doc list is meant to inform the final call.

## Depth benchmark vs Utkarsh + current transfer state (2026-08-17)

⚠️ **THE GOOGLE DOC DOES NOT YET CONTAIN DATALABS.** It still has **8 tabs**; `08_DataLabs.md` exists only on disk. Pending patch: insert a **`DataLabs` tab at position 5** (between IPs and Policies), then re-transfer **3 tabs whose sources changed** — `How to read this`, `Inc42`, `🔴 Decision log (internal)`. Leave untouched: `App`, `IPs`, `Policies`, `Response rules`, `🔴 Utkarsh input`. Final order = How to read this · App · Inc42 · IPs · DataLabs · Policies — T&C & Privacy · Response rules · 🔴 Utkarsh input · 🔴 Decision log.

**Size comparison (measured, not estimated):**
| | Lines | Bytes |
|---|---|---|
| Utkarsh Master Context v4 (1 product) | 517 | 27,279 |
| My set (9 docs) | 1,463 | 90,861 |
| — `08_DataLabs.md` alone | 205 | 13,449 |

**The honest read:** his DataLabs doc is 2× mine by size, but only ~5 of his 17 sections are things AskInc42 may say — §4 tiers (minus prices), §5 user journey + IA, §8 feature inventory, §9 entities/coverage, §13 URL patterns. Barred: §1–3 strategy, business metrics, §7 activation, §10 metrics, §11 Pro kill criteria, §12 team, §13 tech stack, §14 roadmap, §15–17 internal process. Stripped to the permitted surface his doc is ~8–9KB, so **mine is more detailed on what the assistant can actually say** (I added per-signal explanations, a quick-answers table, the URL lookup table, and the conflicts section). Different jobs: his aligns a team, mine bounds an assistant.

🟡 **OPEN, AWAITING RANJITH'S YES:** add a **"Who DataLabs is for"** section to `08` — Utkarsh's §6 details 3 ICPs (investors · sales & marketing · founders/researchers/corporate innovation) with each one's jobs-to-be-done. My `08` only implies this, and "would DataLabs help someone like me?" is a legitimate user question. Offered as a ~40-line addition stripped of the conversion/ARPU framing. **Cheapest to add before the transfer, not after.**

**Tooling constraint (asked twice, worth remembering):** I **cannot** edit the Google Doc from Claude Code — no browser-control tool exists in this session, and the claude.ai Google Drive MCP is (a) still unauthenticated and (b) read/search only even once authorized. **Claude in Chrome is a separate product running in Ranjith's own browser; it is not callable from here.** All Doc updates must go through a handoff prompt to that session. `HANDOFF_PROMPT_GoogleDoc.md` now covers both a fresh build and an in-place patch.

**Current freeze manifest (verify before any transfer):** `00` 4820/902b171a6871 · `01` 14524/28c335651f1a · `02` 4943/c84c1882ceae · `03` 7081/6ae30046cd5d · `04` 17303/f06c841a7e1a · `05` 5436/73aaaaef37cf · `06` 10881/f06d0cbfb11d · `07` 6647/bfdb9d2ce311 · `08` 13449/4829ccd34c6f

## DataLabs doc added (2026-08-16/17) — 9 docs now

Utkarsh shared **`Datalabs Master Context for AI (April 2026).md`** (in ~/Downloads, v4, 21 Apr 2026, 518 lines, owner Utkarsh, Notion mirror `2ac9dc3fea5e80d1b459c62979c91cc1`) as a depth benchmark.

🔴 **It is NOT a knowledge source and must never be ingested** — it's an internal alignment doc containing Pro pricing + credit costs, MRR/ARR targets and Pro kill criteria, registered/MAU/activation metrics, "kill Tracxn" positioning, the 14→7 FTE restructuring with named owners, BrandLabs deal economics, and the full tech stack.

**Extracted the user-facing layer into new `08_DataLabs.md`** (S3, ~13KB) — coverage, guest/free/Pro as *capability not price*, 5-tab company profile (Overview/Financials/Funding/Cap Table/Key People), the 8 signals, search surfaces, tracking, and the URL patterns. Verified against live `inc42.com/datalabs/` + a live company page 2026-08-16.

**Three conflicts this surfaced — all real, all unresolved:**
1. 🔴 **Live T&C is stale vs the product** — Terms (16 Jul 2026) still name a multi-seat/Team plan and an annual option that the April free-pivot removed, and state a Pro Trial length that contradicts Utkarsh's doc. **Because AskInc42 summarises the T&C, a stale T&C propagates into policy answers.** Added as a 3rd Utkarsh item, to resolve *alongside* the answer-set sign-off.
2. ⚠️ **Coverage figures differ** — public DataLabs page says 3,000+ investors / 20,000+ rounds; internal doc says 3,500+ / 25,000+. Rule set: **use the public figures**; if they're understated, fix the page not the assistant.
3. ⚠️ **Free web tier caps Ask DataLabs queries** — app knowledge states no cap. Confirm whether a cap applies in-app.

**Structural devices worth stealing from Utkarsh's doc** (partly adopted): status tags `[LIVE]`/`[LAUNCH]`/`[POST-LAUNCH]`, a "what changed from vN" diff section, explicit supersession with an archive path (I deleted rather than archived `07_Open_Items`), a companion-docs block, and per-doc owner + refresh triggers.

Decision log renumbered **1–33**; handoff prompt updated to **9 tabs** (DataLabs inserted at position 5) with an "IF UPDATING AN EXISTING DOC" section.

## 🔗 GOOGLE DOC IS THE TEAM-FACING COPY (2026-08-14)

**"AskInc42 — Knowledge Set"** — https://docs.google.com/document/d/1KhWJP5Q_cS1YH1iG8Y5VV361byEI389oOCaVUyGDvgQ/edit

8 tabs, built by a separate Claude-in-Chrome session, manifest-verified byte-for-byte: 1 How to read this · 2 App · 3 Inc42 · 4 IPs · 5 Policies — T&C & Privacy · 6 Response rules · 7 🔴 Utkarsh input (internal) · 8 🔴 Decision log (internal). All 26 md tables rendered as real Docs tables. Both DO-NOT-INGEST banners intact.

**Source files:** `~/ClaudeDocs/inc42/AskInc42_Knowledge/*.md` (+ `docx/` builds). ⚠️ **Doc and MD files are now two copies — drift risk is live.** The weekly IP review must pick ONE side; decision pending with Ranjith (recommendation given: Doc wins, MD becomes a dated snapshot, ingestion exports from the Doc).

**Handoff-transfer lessons worth reusing:** (1) always issue a **byte-count + md5 manifest** before a transfer — the first attempt raced my live edits and 5 of 8 tabs went stale; (2) **pasting into a populated Google Docs tab inherits the caret's character style** — a bold caret turned an entire tab bold and collapsed a table column; clear the tab + formatting (cmd+\) before re-pasting; (3) round-trip text verification out of Docs collides with the system clipboard.

## OPEN ITEMS CLOSED BY RANJITH (2026-08-14) — these supersede earlier recommendations

- **IP list expanded 8 → 11.** Added **Griffin (Founders Club / Retreat)**, **D2CX** (12-wk, Cohort 10 from Aug 2026, paid, application + interview) and **D2CX Foundations** (6-wk, paid, direct enrolment, no application). Verified live. Still out: ManagementX, AngelX, Fintech Summit, Plus, DataLabs, Reports, BrandLabs, 30 Startups, Startup Spotlight.
- **Access model IS answerable** — free/paid/invite-only varies by event and may be stated. **The moment the question becomes "how much" → redirect to the website.** Eligibility criteria also answerable (thresholds described qualitatively); never rule on whether a specific user qualifies.
- 🔴 **WEB SEARCH STAYS ENABLED — via Perplexity.** Ranjith rejected the disable-web-search recommendation outright ("just completely ignore this"). Reframed: the 5 sources are **authoritative, not exclusive** — they win on Inc42-entity questions; where silent, deflect to Contact Us rather than reconstructing Inc42 facts from the open web. Don't re-raise this.
- **CTO Summit being absent from inc42.com/events is DELIBERATE**, not a bug. Never mention site structure to users; just use the `events.inc42.com` link.
- **Refunds/cancellations:** confirmed — always redirect to Contact Us.
- **Part B (items owned by others) deleted entirely.** Doc 07 renamed `07_Decision_Log.md` and is now a pure decision log (31 decisions). Only 2 items remain open, both Utkarsh sign-offs, and they live in doc 05: T&C/Privacy answer-set sign-off (gates S5) + app-store rationale confirmation. **AI sub-processor gap and AI-disclaimer coverage moved OUT to the DPDP track** — not knowledge scope.

**Standing lesson (he enforced it twice):** this doc set is **knowledge scope only**. Build workstream — design/placements, streaming + lane architecture, frontend release contract, v2 flow, analytics, cache leak — does NOT belong in it, not even in the internal docs. He caught me dumping the whole workstream into the Utkarsh doc; it was cut from 132 → ~80 lines.

## SPLIT INTO 8 SEPARATE MD FILES (2026-08-14, Ranjith's instruction)

Ranjith rejected the single-document form — "if I dump everything into one document it doesn't make a lot of sense." Also: **no artifact**, plain MD files only, meant to be pasted into separate Google Doc tabs, and **zero pricing anywhere** (verified by grep — no ₹/INR/tier/discount tokens in any file).

**Folder: `~/ClaudeDocs/inc42/AskInc42_Knowledge/`**
| File | Ingest? |
|---|---|
| `00_README_Index.md` | map + cadences + owners |
| `01_App_Knowledge.md` | ✅ S4 (carried over from the earlier App KB, incl. verbatim approved FAQ) |
| `02_Inc42_Company.md` | ✅ S3 |
| `03_Policies_TnC_Privacy.md` | ✅ S5 |
| `04_IPs_Overview.md` | ✅ S3 — weekly review |
| `05_Utkarsh_Call_Notes.md` | 🔴 **NEVER** |
| `06_Response_Rules.md` | ⚙️ behaviour, not knowledge |
| `07_Open_Items_And_Decisions.md` | 🔴 **NEVER** |

Two docs added beyond his five topics, both justified in the README: **06** (deflection rules are a rule set, not knowledge — left inside a knowledge file they get ingested as facts or missed by whoever wires prompts) and **07** (he explicitly asked for open items + decision log pulled out into one reviewable place — "if you are adding open items it's simply a waste of time" = don't scatter them, make them closeable).

**07 Part A = 6 decisions formatted with a recommendation + tickbox so he can close them in one pass:** A1 add Griffin Retreat/D2CX/D2CX Foundations (rec: yes), A2 may it say free/paid/invite-only (rec: yes), A3 keep eligibility criteria (rec: keep, qualitative), A4 MoneyX stale site, A5 D2CX Runway duration contradiction, A6 CTO Summit invisible from inc42.com/events. Part B = 10 items owned by Utkarsh/Ashish/Ritvik/Satya. Part C = 27 locked decisions.

**Time-critical:** D2C & Retail Summit is **19 Aug 2026** — must flip to `concluded` at the next weekly review or AskInc42 invites people to a finished event. First real test of whether the cadence gets followed.

## Knowledge Scope PRD written + full live-web IP audit (2026-08-13)

Two docs created (`~/Documents/`, both published):
- **Knowledge Scope & Response Boundaries PRD v1** — https://claude.ai/code/artifact/0508e11a-a17e-4af6-bf80-82ebdeeba04e — 19 locked decisions **K1–K19** (separate numbering from the product PRD's D1–D17 to avoid collision), deflection matrix, eval probe set, acceptance criteria restated as testable.
- **IP Knowledge Base v1 (the S3 source doc)** — https://claude.ai/code/artifact/eae4f04f-4253-43e8-9225-abec4452cb0f — parallel to `AskInc42_App_Knowledge_Base_v1.md` (which is S4 and already existed).

**Every one of the 8 IPs verified against its live site 2026-08-12. Three names in Ranjith's list don't match what's live:**
- **CTO Summit — real, and the newest IP.** ✅ **`events.inc42.com/cto-summit/`** (Ranjith supplied the URL 2026-08-13). **Inaugural edition, 30 Sep 2026, JW Marriott Bengaluru**, "Technology In The AI Era", invite-only, 175+ tech leaders, 10+ sessions, 20+ experts, 4 tracks (AI & Intelligent Systems / Infrastructure & Cloud / Cybersecurity & Trust / Engineering Leadership), speakers TBA. ⚠️ **Lives on the `events.inc42.com` subdomain — `inc42.com/cto-summit` 404s AND `inc42.com/events` doesn't list it**, which is why the first audit missed it. Lesson: sweep both hosts. All redirects must use the events subdomain path. "The CTO Dinner" (Inc42 × Snowflake, 2024) is a separate historical property, NOT ingested.
- ⚠️ **"D2C Summit" renamed** → **The D2C & Retail Summit 2026** (7th ed, 19 Aug 2026, Leela Ambience Gurugram); `inc42.com/d2c-summit` **301s** to `thed2csummit.co`.
- ⚠️ **FAST42's live cycle is 2027** (6th ed), not 2026 — the 2026 URL now serves 2027 content.
- 🔴 **MoneyX site is stale** — still showing MoneyX 2025 (3rd ed). The "redirect to the website" rule fails when the destination itself is a year old.
- ⚠️ **Concluded as of now:** AI Summit 2026 (28 May), D2CX Runway 2026 cohort (Demo Day 7 Aug). Needs an explicit status rule (K9) or the bot describes past events in present tense.
- **D2CX Runway page self-contradicts** — titled "4-week accelerator", body says 6-wk virtual + 6-day residency.

**Biggest engineering implication (K1):** adding 5 sources does NOT remove the web-search fallback Utkarsh described. If web search stays on for the Inc42-entity query class, the "no knowledge outside 5 sources" criterion is unachievable — the model fills retrieval gaps from the open web and the answer looks identical to a grounded one. Retrieval miss must return the deflection template.

**REFUNDS SIMPLIFIED (Ranjith, 2026-08-13) — K11 revised.** One line, one destination for every refund AND cancellation question, every property: *"please reach out through the Contact Us page."* No policy terms, no per-IP routing. AskInc42 holds only a basic awareness that terms are per-property and conditional, purely so it doesn't invent one (K11a) — it never states a window or condition, even if pushed twice.
Ranjith's simplification is well-founded: the audit found **four incompatible refund regimes** — `inc42.com/refund-policy` (DataLabs/Plus: non-refundable once activated, **exporting any data disqualifies you**, and it *explicitly excludes events and courses*); D2C Summit (refund in 7 working days **if not shortlisted**); MoneyX (7–10 days **if application rejected**); D2C Retreat (none at all). Routing accurately per-IP would require a policy-interpretation engine, which K13 forbids anyway.

**`inc42.com/contact-us` 404s** — the live page is `inc42.com/contact`. In-app the rule stays Profile → About → Contact Us with **no email/phone ever stated** (K4/K5).

**Live IPs deliberately excluded by the 8-item list** — Griffin Retreat (Inc42's own About page calls it flagship), **D2CX** core (12-wk, 8 cohorts, 400+ founders — the parent brand of Converge and Runway, both of which ARE in scope), D2CX Foundations, ManagementX, AngelX, Fintech Summit. Recommended adding the first three (K10); Ranjith's call, not silently fixed.

**Legal facts verified:** entities = **Inc42 Plus Media Pvt Ltd** (operator) + **Ideope Media Pvt Ltd** (licence holder). T&C 35 sections, Privacy 17 sections, **both last updated 2026-07-16**, Indian law / New Delhi exclusive jurisdiction. T&C **§11 is already an AI-Generated Content Disclaimer** and **§10 a Data Attribution Requirement** — worth confirming they cover AskInc42's own output. Privacy 3rd-party list (Razorpay, Stripe, Firebase, PostHog, Google, GCP, Fullenrich, Customer.io, event sponsors) still names **no LLM/AI sub-processor** while naming AI/Ask Mode as active — the [[project-dpdp-compliance]] gap is confirmed still live in the current policy version.

**2026-08-14 — a source doc was missing and is now being written.** Ranjith identified that the document he owes **Ashish** — *what Inc42 is, how the company works, and related company-level context* — had **not been produced**, and has delegated it to an agent. This is distinct from the two docs already published (Knowledge Scope PRD, IP Knowledge Base v1) and from the app knowledge base; it's the company/organisation source. **Status: in progress, not delivered to Ashish yet.**

**How to apply:** don't assume static VectorDB embedding is the final architecture — real-time/volatile fields (esp. pricing) may still need a different approach; that decision now explicitly waits on the product catalog being built first, not on Ritvik's earlier draft-plan step.
