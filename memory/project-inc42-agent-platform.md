---
name: project-inc42-agent-platform
description: "INC42 internal Agent Platform — Ranjith owns product, Utkarsh sponsors; the 'engine room' (A11) of Utkarsh's strategy: shared internal AI agents in Slack, gated on real demand"
metadata: 
  node_type: memory
  type: project
  originSessionId: 59d37617-438d-4f64-9bd1-898ff0e69b64
---

`~/Downloads/Agent Platform Brief.md` (dated 2026-08-13; read 2026-08-16). **Ranjith owns product; Utkarsh sponsors; engineering & data teams execute in defined lanes.** This is the concrete form of the "engine room" in [[project-inc42-strategy-utkarsh]] (§7b) — the internal-AI programme that is **A11 in the hypothesis ledger** ("an AI-native operation holds the product-org cost base flat while QIA scales 4×").

**What it is:** internal AI agents that live in Slack channels, answer from INC42's own data with sources attached, do repeatable work for teams. NOT transferring one operator's personal setup — shipping the *patterns* as shared infrastructure so any team gets an agent without building plumbing.

**Already live (not a pitch):** News AI v2 + Markets AI v2 (editorial Slack, daily) · two data-team brief channels (social + editorial intelligence, every morning) · the AI Hiring Agent (Ranjith's pilot, 2 roles, <₹1/applicant, first 100 profiles w/ Shweta — see [[project-inc42-hiring-agent]]) · Ask Your Query / social-intelligence bot (Prapti & Tanuj; DM on Slack; also pulse.inc42.com — relates to [[project-inc42-social-intelligence]]) · Nityam building small IP-comms/design agents on his own initiative.

**How an agent works:** one Slack channel = one agent (channel scopes what it can see/do); thread = a conversation with memory; agents only get granted capabilities; answers carry sources + state what they couldn't reach (enforced in plumbing, not model promise); sensitive data (candidate PII, comp, ₹ revenue amounts, board material) restricted by rule in code ("below target" ok, never the number in a shared channel). Three shapes: conversational · pipeline (News AI) · broadcast (scheduled brief).

**The ask to teams:** open the 25-agent Opportunity Catalogue (nothing committed) → pick/propose (a one-line "I keep doing X by hand" comment becomes an entry; self-added entries count more) → Ranjith runs a prioritisation session, top 2–3 become first pilots in 1–3 week sprints. **Gated on real demand:** 1-month honest review — if agents-already-live aren't used by people who didn't build them, they stop.

**Metrics Ranjith is accountable for (3):** weekly-active agent users (people who actually ask — not channel members, platform team doesn't count itself) · trust incidents (wrong numbers/leaked context — target zero) · time from "team picks" to "agent live." Watches hardest: repeat use. **Two pre-written kill conditions:** if teams route around an agent back to a person → stop adding, fix the workflow; if all demand originates from one person → cap at maintenance mode.

**Never-bend rules:** candidate PII / comp / revenue ₹ / board material never indexed, never to a shared surface (named DMs only) · editorial source material (drafts/sources/correspondence) excluded from every layer · every data access logged (who/agent/touched/cost) · no credential sharing, agents run on own governed accounts. **Restricted-data access decisions go to Utkarsh.**

**The strategic dual-use thesis (from the strategy §7b):** the query-tools-behind-endpoints serving internal agents are the SAME ones that will serve the member-facing AI layer later (ask-inc42 is the existence proof) — the internal platform is the low-stakes rehearsal for the AI layer the membership defers. Architecture locked 2026-08-12 (fifteen locks: agent = scope + capability grant + skills + delivery rules; broker on every call; principal argument on every retrieval; two-sided provenance; routine-over-code; earned promotion with kill conditions). Live deployment classes: conversational (new worker pool) · pipeline (n8n — excellent, stays) · broadcast (crons).

**Supporting docs (Google Drive, this folder):** Decisions Log (append-only, wins over reference docs) · Opportunity Catalogue · Blueprint (build plan/roadmap) · Data Classification + Source Registry · frozen references (Vision, Agent Platform locked-architecture, Runtime Landscape, Company Brain Landscape, Knowledge Foundations). Questions channel: #ask-inc42-platform (TBD).

**How to apply:** this is a distinct workstream Ranjith owns, parallel to the [[project-inc42-unification]] product roadmap but strategically linked as A11's engine-room bet. When the unification plan is re-derived under [[project-inc42-strategy-utkarsh]], the agent platform is the A11 lane, not a product feature.