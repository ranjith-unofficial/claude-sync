# **Inc42 [Agent Platform](https://docs.google.com/document/d/1HASW58FME2W_mvVu_e7viMq_PKzYA61NZfsoArz4gZk/edit) – Brief**

**Date:** 2026-08-13 · Owner: Ranjith (product) · Sponsor: Utkarsh · Execution: engineering & data teams, in defined lanes This document: the 2-page entry point. Everything it summarises links out at the bottom – you can act on this page alone.

---

## **What this is**

Inc42 is standing up an internal agent platform: AI agents that live in Slack channels, answer from our own data with sources attached, and do repeatable work for teams – the same way News AI and Markets AI already work for editorial, but available to every function.

**The core idea:** we spent a year proving these systems work for one operator. We are not transferring that personal setup – we are shipping the *patterns* from it as shared infrastructure, so any team can get an agent without building the plumbing.

## **What already runs (this is not a pitch, it started already)**

- News AI v2 and Markets AI v2 – live in editorial's Slack, processing stories daily.  
- Two data-team brief channels – social and editorial intelligence, delivered every morning.  
- The AI Hiring Agent – live pilot by Ranjith, now running on two roles: two-stage screening at under ₹1 per applicant, first 100 profiles reviewed with Shweta.  
- Ask Your Query – the data team's social-intelligence bot (Prapti and Tanuj): DM it on Slack and ask what India's founders and operators are actually posting; every answer shows exactly what it searched and links back to the original posts. Also at pulse.inc42.com.  
- And more is coming from inside the team – Nityam is building a set of small agents for IP communications and design work on his own initiative.

## **How an agent works here (the 60-second version)**

- One Slack channel \= one agent. The channel decides what the agent can see and do. A thread is a conversation with memory; a new thread starts fresh.  
- Agents only get what they're granted. Each agent holds a named set of capabilities (e.g. "query the editorial corpus", "read Metorik") – nothing else. Sensitive data (candidate PII, compensation, ₹ revenue amounts, board material) is restricted by rule, enforced in code: an agent may say "below target", it may never say the number in a shared channel.  
- Answers carry sources. Every number names where it came from; every output says what it could not reach – a build requirement every platform agent ships with, enforced by the plumbing, not a promise the model makes.  
- **Three shapes:** conversational (ask it things in a channel) · pipeline (it processes items, like News AI) · broadcast (it posts a scheduled brief).

## **What we're asking you to do**

1. Open the [Opportunity Catalogue](https://docs.google.com/document/d/1lKhc4JKhJ9LAurMJ595dq3tmgN5vRnyus-0oc9oL3QQ/edit) – a menu of 25 candidate agents found by scanning everything we've already built. Nothing on it is committed.  
2. Pick what would actually help your team – or better, add your own. A one-line comment on the doc ("I keep doing X by hand every week") is enough; the platform team turns it into an entry. *Entries you add count for more than entries we wrote.*  
3. Ranjith runs a prioritization session and the team's top 2–3 picks become the first pilots, built with you in 1–3 week sprints.

**The honest part:** at the one-month mark we review honestly – picks, additions, and whether the agents already live are being used by people who didn't build them. If none of that shows life, we stop. The platform is gated on real demand, not on our enthusiasm for it.

## **Who helps with what**

| Level | You want to… | You need | Who helps |
| :---- | :---- | :---- | :---- |
| Run | Use an agent that exists | Channel membership | Nobody – just use it |
| Author | Teach an agent a workflow/checklist of your own | A markdown skill file | Self-serve, docs \+ examples |
| Extend | An existing agent's ability, in *your* channel | A grant (reviewed) | Product team sets up the surface |
| New capability | An agent on a data system not yet connected | A query tool \+ registry entry | Data team builds the tool; platform owner connects it |

The bottom rung is free by design; only the top rung needs real engineering.

## **How we'll know it's working**

**Three metrics Ranjith is accountable for:** weekly-active agent users (people who actually ask an agent something – not channel members, and the platform team doesn't count itself) · trust incidents (wrong numbers, leaked context – target zero) · time from "team picks an agent" to "agent live". What we watch hardest is repeat use: the same people coming back week after week.

**And two kill conditions we've written down in advance:** if teams route around an agent back to asking a person, we stop adding agents and fix the workflow instead; if all demand keeps originating from one person, the platform caps at maintenance mode.

## **The rules that never bend**

- Candidate PII, compensation, revenue ₹ amounts, and board/investor material are never indexed and never delivered to a shared surface – named-individual DMs only.  
- Editorial source material (drafts, sources, correspondence) is excluded from every layer, full stop.  
- Every data access is logged: who asked, which agent, what it touched, what it cost.  
- No credential sharing between people; agents run on their own governed accounts.

## **The documents**

| Read this if… | Document | Where |
| :---- | :---- | :---- |
| You want the current state of every decision | [Decisions Log](https://docs.google.com/document/d/1fy2i_c65Ng935tynVWFaZIXtSmsWJkmvbR10D63Rqw0/edit) – append-only; where a reference doc conflicts with it, the log wins | Drive (this folder) |
| You want to pick or propose an agent | [Opportunity Catalogue](https://docs.google.com/document/d/1lKhc4JKhJ9LAurMJ595dq3tmgN5vRnyus-0oc9oL3QQ/edit) | Drive (this folder) |
| You're building on the platform | [Blueprint](https://docs.google.com/document/d/12PU3vsNNtxHVeb37jM6OBvRQB8MxuqlgIPGiR9IAzV0/edit) (build plan & roadmap – live) | Drive (this folder) |
| You're wiring data access | [Data Classification](https://docs.google.com/document/d/1GB4IAUW7Z_NgFQbG8htpEnqh6qS1ZfXv8vScP1fdpGc/edit) · [Source Registry](https://docs.google.com/document/d/1UVOPylgYFB3sGoaRb2V9ZGf0uI-bkOwJ4-7JE2Y8Xso/edit) | Drive (this folder) |
| You want the why, and the reasoning record | Frozen references (dated, superseded by the log where they conflict): [Vision](https://docs.google.com/document/d/1Vq-hSiPDwg93Ns1hqt8zyq8xlLM-IurVXgVLCCdnEig/edit) · [Agent Platform](https://docs.google.com/document/d/1HASW58FME2W_mvVu_e7viMq_PKzYA61NZfsoArz4gZk/edit) (the locked architecture) · [Runtime Landscape](https://docs.google.com/document/d/1_lWCpyp3M-lo8P5n9NZy4clFale_pYEKgHtKg-MBp0I/edit) · [Company Brain Landscape](https://docs.google.com/document/d/1wRfiLMidxR6-x6JSOA_Zs41Jw7jGQ1kmAn4Lu92uMFY/edit) · [Knowledge Foundations](https://docs.google.com/document/d/1LLdr4pw6c9EUCQpGbgLm2nJ2oVk6imwZTJInrb5bDDc/edit) | Drive (this folder) |

**Questions:** \#ask-inc42-platform (channel TBD) or Ranjith directly. Restricted-data access decisions go to Utkarsh.  
