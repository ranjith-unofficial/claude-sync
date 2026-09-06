---
name: project-inc42-askinc42-next-week
description: "AskInc42 — running execution task list for the upcoming week, separate from the positioning/strategy memo"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9859d45d-f58a-4c8b-b439-1562f2def0be
  modified: 2026-08-14T05:08:28.177Z
---

Separate module from [[project-inc42-askinc42]] (which holds positioning/JTBD/placement strategy) — this one tracks near-term execution tasks as they're assigned, so the strategy memo doesn't get cluttered with task-tracking.

## Week of 2026-08-03 (full list confirmed by Ranjith, 2026-08-02, PRD now complete)

- **Feature flag work.** Owner confirmed **Ritvik Sethi** (spelling confirmed 2026-08-10, catch-up call transcript — previously "Ritvi," unconfirmed). **Status as of 2026-08-10: HALTED** — Ritvik is focused on AskInc42 UI placements instead; feature flag work paused, not abandoned.
  - **Notification** — sub-item under feature flag. Likely connects to D12 (push notification when a delayed AskInc42 response is ready) from the PRD, but that link is inferred, not confirmed.
- **AskInc42 — backend + UI initiation.** Build kickoff for the PRD ([[project-inc42-askinc42]], 17 locked decisions as of 2026-08-02, artifact: https://claude.ai/code/artifact/320582bd-1b52-495f-9980-92310d6621e8). **2026-08-10 update:** Ritvik is mid-build — has gone through the internal flow/APIs and confirmed they need changes vs. the PRD as written ("we'll check again"). First placement chosen by Ranjith: **the Brief** (deliberately low-stakes pick — Ranjith said placement choice doesn't matter much right now, priority is proving AskInc42 works end-to-end in the app at all). Target: one working placement stitched together by EOD 2026-08-10, then an APK handed to Ranjith to test/play with; other placements to be duplicated from that first one afterward. Ranjith will work with Satya on design in parallel once Ritvik's backend/API revision (needs to be scalable) is further along.
- **Process for delete functionality.** Possibly connects to Section 09 of the PRD (confirming Ask chat history is covered by account deletion) or to [[project-inc42-legal-compliance]]'s existing account-deletion model — link inferred, not confirmed. Could also be unrelated to AskInc42 entirely (e.g. deleting a tracked company from Watchlist).
- **Companies — card design changes + implementation.** Scope not detailed yet.
- **Singular set-up.** Singular is the existing app-only SKAN attribution vendor ([[reference-inc42-vendor-stack]]) — this task is presumably finishing/configuring that integration, not a new vendor.
- **Hiring agent — completion.** Separate initiative, see [[project-inc42-hiring-agent]] for full context (Keka API paid add-on confirmed, DPDP consent-scope question unresolved, Notion MCP pending for Yash's meeting notes).

## 2026-08-14 team call (Ranjith + Ritvik + Ashish)

- **iOS build v40 submitted** carrying: the earlier font-size fix, the **ATT tracking-permission placement fix**, and a new **fallback UI for the webview** when the connection is poor or the API returns a bad response. ⚠️ **Contradiction inside the same call:** Ritvik opens with "approval aa gaya Apple se", but later says he'll plan social posts *"after we get the approval from Apple"*, and Animesh separately says App Store timing is unknown. **Treat approval as NOT received until confirmed in App Store Connect.**
- **Two Animesh bugs fixed:** (1) notification toggles (Daily Brief, Watchlist Alerts) weren't being set true when a user granted permission **pre-login** — now written to the API if logged in, held in secure store as pending if not; (2) the **Android small notification icon** — no asset at the required size, so Android substituted its own base icon. **Not device-specific** despite first appearing on one handset; needs 24dp icon assets, which Ritvik had already requested once and not received.
- **Ask DataLabs work is partially blocked on Utkarsh.** Ritvik implemented part of the August release brief but some decisions need clarification; he stayed up late to catch Utkarsh, who was in back-to-back meetings. He is **not idle-blocked** — he switches tasks — but those decisions gate closure.
- **Bhavika ran her first events audit** — ~40–50 events reported in one pass, Ritvik fixed them; **4–5 interactions still need work plus some missing properties**. Note: this was a single batch audit, not drip-fed bugs.
- **AskInc42 first in-app placement: Ritvik is targeting Friday/Saturday.** Causes of the slip from the Mon/Tue commitment: 2–3 days spent on the Apple fixes, Anmol's side not started, and n8n changes agreed with Anmol and Ashish. Ranjith's read is that ad-hoc work from multiple directions caused it, not Ritvik.
- **Ritvik's load is split three ways, and that's structural.** Beyond the app, he is **expected by Ashish and Utkarsh to contribute to DataLabs** as part of his role. Separately, **Utkarsh shared a document directly with Ashish and Ritvik** which they are implementing — Ranjith's stated position: *"I have zero problem with him dealing with you guys"*, but he has committed timelines to Utkarsh off the back of work he isn't sighted on. That's the coordination gap, not a people problem.
- **Work already done on AskInc42 before the build stalled:** Ritvik spent real time getting AI to plan it, **built an n8n automation**, and discussed the required APIs with Anmol and Ashish. What didn't happen was kickstarting the implementation itself — 2–3 days went to the Apple fixes.
- **Ritvik offered product help unprompted**, on the basis that he built DataLabs and Inc42 Plus from scratch and has seen them scale — and said he personally knew the launch plan wouldn't work.
- **Satya's design finally surfaced** — Ritvik forwarded the link during the call. Satya is occupied with the **CTO Summit website rebuild** (marketing recreating the whole site). Ranjith's actual complaint is not the delay but that **nothing was communicated** — he had told Utkarsh drafts would land Tue/Wed and had no answer when asked.
- **Process ask from Ritvik:** add Ranjith's tasks to the **Product Backlog** project, because that's the single view Ritvik uses to see team load and re-allocate bandwidth. Ranjith's caveat: a backlog is for backlog, not tracking — but agreed, and a task can sit in both its own project and the backlog. Ritvik admitted his own tasks were not updated and committed to daily end-of-day updates; **Satya updates nothing**. Ranjith has created a separate Asana project for unification.

## Frontend release brief — "Ask Inc42 — August release brief (frontend)" (shared by Utkarsh to Ashish + Ritvik, read 2026-08-12)

Source: `~/ClaudeDocs/inc42/sources/Brief Ashish Release 2026 08.pdf`, 6 pages, Google Doc export. Supersedes `BRIEF-ASHISH-LANE-UX-CONTRACT.md`. This is the engineering contract behind the "deploy fast mode + streaming to Ask DataLabs first" decision. **Six items need frontend work; items 2–6 are flagged as the ones that can break on launch day.**

**Already live in production (2026-08-02), no frontend action:**
- 🔴 **Cross-session cache leak — fixed, but it was live.** Follow-up fragments shared **one global cache entry**, so a user asking "financials of company" could receive **another user's answer**. Now session-scoped. Worth a separate call on whether this counts as a reportable incident under [[project-dpdp-compliance]] breach-notification obligations.
- Session memory fix — pronoun follow-ups ("who invested in them?") now at **100% entity resolution**, up from intermittent failure.
- Response JSON unchanged: same **19 fields** (output, sources, entity_links, suggestions, mode, tool_count, …) regardless of internal path.

**LOCKED PRODUCT MODEL — three auto-routed lanes, no mode picker:**

| Public label | Subtitle shown | Measured median |
|---|---|---|
| Answer | "Seconds" | ~3.5s |
| Analysis | "Under a minute" | ~20s |
| Research | "A few minutes" | ~45s |

- Internal names **Snap / Scan / Deep** appear in logs and code — **never shown to users**.
- **No upfront picker, deliberately.** Rationale in the doc: **62% of multi-turn sessions span more than one complexity level**, so a sticky mode would need changing mid-conversation; and industry data shows **<5% of users ever change a default**, while routing raises depth usage.
- **ETAs are shown because P90 latency is 52.6s** — silence at 50s reads as a hang. ETAs are measured medians, not aspirations.

**Stream event contract:** `activity_plan` (live, ~1.5s, before tokens — render as a checklist; do NOT use `mode` for the badge) → `lane` (live on dev, once routing decides; carries label + `eta_seconds`) → `final` (live on dev, added 2026-08-11; **last event on every path** — agent, fast-path, cached, validation error). `final.payload` equals the non-streaming response body; **`payload.output` is authoritative**, and **sources / entity_links / suggestions exist nowhere else in a stream**. Cached answers = final-only, zero tokens, `cache_hit: true`. Errors = final-only, `payload.error` set and `output` absent → render the error, not a blank answer.

**Escalation:** a **second `lane` event** (e.g. answer → analysis) means the fast path found thin data and promoted mid-flight. Append to the checklist, don't reset. Verified on dev.

**⚠ The single most likely launch-day breakage:** two cases return a complete, correct answer with **zero streamed tokens** — fast-path answers (agent never runs), and escalated answers, which are **non-deterministic**: two runs of the same query gave **81 events / 0 characters** vs **95 events / 1,885 characters**, roughly 50/50, cause not established. A client that waits for a first token **hangs on our fastest queries**. Implementing `final` covers both by construction.

**"Go deeper" button** on completed `answer` and `analysis` responses — resubmits the same query with `force_lane: analysis|research`. **Every click must be logged**: each one is a labelled routing error and is the only telemetry that shows whether auto-routing under-selects depth.

**⚠ Agent V3 — land the fix now, it's backward compatible.** Forcing function is the **11 Dec gpt-5.4 deprecation**. V3 re-enters the agent per tool iteration: begin/end pairs go **1→3**, text events **15→29**. A client that finalises on the *first* `end` truncates the answer to the first fragment. Fix: treat `end` as "segment finished", accumulate, finalise on stream close — behaves identically on V2.

**Two open questions the doc asks Ashish/Ritvik to answer:**
1. Will the client implement `final`? (reduced from the broader "does it render a token-less response")
2. 🔴 **Which webhook will the live frontend call after deploy — `master-agent-v1` or `master-agent-v2-stream`?** This decides **when the fast lane actually reaches users**, and step 2 of the sequence is gated on it.

**Sequence:** ship streaming as-is → soak a few days → add fast lane + lane events (gated on Q1) → Agent V3 (only the streaming slot is gated on the item-6 fix; non-streaming slots `master-agent-v1`/staging/GPT twin emit no begin/end so V3 is invisible there and can ship independently) → lane badges + "Go deeper" can land alongside or after. Nothing changes the response JSON, so **every step is independently revertible**.

## 2026-08-12 update (Utkarsh call)

- **Current live state (website AskInc42):** it has access to **articles + DataLabs data only**. It holds **no internal Inc42 documents** — anything asked about Inc42 itself is currently answered via **web search**, which it has access to. That's the gap the knowledge repo closes.
- **Ashish owns the knowledge layer** (Inc42 / app / IPs / basic T&C + privacy). A ticket for it was created and shared with Ashish on this call. See [[project-inc42-knowledge-repo]] for the locked scope.
- **Utkarsh's requirement on maintenance:** the knowledge must live somewhere deliberately maintained — repo, doc, Drive, whatever — with either **regular fetching from live sources** or a **defined update cadence**. It must not go stale/static. Manual curation is acceptable **provided the cadence is defined and followed**. Ranjith's plan: Postgres vector DB, **manual weekly review** for the first few iterations (what's missing / to add / to remove), automate later — deliberately not auto-updating yet.
- 🔴 **DESIGN IS THE BLOCKER.** Ritvik's backend/basic setup is done and waiting on UI. **Four placements** are needed; as of Wednesday 12 Aug Ranjith had **not received even an initial draft from Satya**, despite raising it in daily standups. Ranjith flagged it to Utkarsh as needing intervention (noting Satya is normally fast). Ranjith to run a call with Ashish + Satya + Ritvik same day and report back.
- **Goal set for 12 Aug:** one AskInc42 placement **live in the app** with basic UI — functional, without the knowledge layer (that's Ashish's track).
- **DECISION: ship the new work to Ask DataLabs FIRST.** Utkarsh has already conveyed this to Ashish and Ritvik, and they agreed: deploy the **fast mode + streaming** changes to **Ask DataLabs** ahead of the app, because DataLabs already has users and volume → faster real usage data, feedback and bug discovery. App design gets locked in parallel; app deployment happens later anyway.
- **Ask DataLabs analytics is broken** — the separate analytics workspace was removed. Fix: implement the same analytics **inside the DataLabs workspace itself**, not a separate one.

## 2026-08-11 update (impromptu Meet)

- **AskInc42 v2 design settled with Ashish:** the flow opens with **3 questions the user answers**, and those answers are **stored in the DB** so the user is never asked again. Ritvik has built a plan + automation for it and it needs to be wired in.
- **Blocker: needs an API from Anmol** — and as of the call, **this had not been discussed with Anmol at all**. Ashish said Anmol has bandwidth for one-off work; agreed that Ritvik won't be blocked for ~2 days either way, since he has bugs to clear meanwhile.
- **Ritvik's priority order for the day (agreed with Ranjith):** 1) close the App Store / ATT fix and resubmit → 2) close the open **Bavika HubSpot / DataLabs analytics** thread (still open, only ~30 min of consultation invested so far) → 3) events work → 4) AskInc42 v2. Ranjith explicitly ranked events above AskInc42 v2 if time is short.
- Feature-flag work remains parked (unchanged from 2026-08-10).

## Flagged, not on the latest list — check if still pending
- **"MCP something"** — Ranjith flagged this as a next-week item on 2026-08-02, before the list above. Not repeated in the latest list — unclear if it's resolved, subsumed into "AskInc42 — backend + UI initiation," or just not restated. Worth confirming.

## Still genuinely open (not yet resolved)
- What "MCP something" (heard as "MCP 1") actually covers — see flag above
- What the "native screen which comes up in Android" surface is
- What "me-too ads" (as heard) actually refers to — Ranjith clarified it's *not* an ad despite the name
- Whether the chatbot needing to "understand how the app works" means product/UI knowledge or live access to the user's own app state (watchlist, tracked sectors)

## Resolved since this list was first written
- ~~Edit Role enum values~~ — resolved 2026-08-02 from the real onboarding screenshot: Founder, Investor, Operator, BD & Partnerships, Other (D16 in [[project-inc42-askinc42]]).
