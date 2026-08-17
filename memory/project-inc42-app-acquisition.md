---
name: project-inc42-app-acquisition
description: "Inc42 app acquisition plan — 5 beta levers now, public launch 25–26 Aug 2026 (Product Hunt + socials), gates and open gaps"
metadata: 
  node_type: memory
  type: project
  originSessionId: 77ea48a7-b503-4d07-9aad-49655a39c265
  modified: 2026-08-17T18:17:43.012Z
---

**Ranjith's two-phase app acquisition plan, as framed for the Utkarsh discussion on 2026-08-17.** Supersedes the "backup plan" framing in [[project-inc42-launch]] — the context changed: iOS is now live and there is a working install base, so this is a growth plan, not a rescue.

## Framing Ranjith is using
The old backup plan was written when installs were ~zero and Android-only. Now: **controlled beta acquisition → public launch on 25–26 Aug 2026.**

## Phase 1 — beta acquisition (now → 24 Aug), 5 levers
1. **Update the website banner** → straight to Play Store + App Store. **Nityam already briefed by Ranjith.**
2. **Email communication** (Customer.io).
3. **"Read on the go" prompt on Inc42 mobile web** — mobile web is where the majority of users are.
4. **Trigger only for repeat readers** (users who have read 1+ / 2+ articles), not first-time visitors.
5. **Trigger on scroll depth ~60–70%** of the article.

Levers 3–5 are the strongest: biggest addressable pool (mobile web), intent-gated, zero paid spend, and **no design dependency on Satya**.

**Constraint:** the list is deliberately short because **Nityam is occupied with the D2C & Retail Summit ("DRS")**. More levers exist but are held until he's free. Paid acquisition stays ruled out.

## Phase 2 — public launch, tentatively 25 or 26 Aug 2026
- Channels: **Product Hunt**, expanded socials, all owned channels.
- Rationale for the date: ~8 days of beta feedback, one app-update cycle to both stores, and it lands **after D2C Summit so Nityam is free to prepare**. Both dates are Tue/Wed — the strongest Product Hunt days.
- By then: beta feedback collected and an updated app shipped to Play Store + App Store with the agreed change list.
- Ranjith's ask to Utkarsh in this meeting: (1) approve and lock the launch date, (2) approve Nityam's bandwidth split between DRS and launch prep.

## Gaps Ranjith should raise himself (identified 2026-08-17, not yet closed)
- **No sizing.** Needs mobile-web sessions/week, % hitting 2+ articles, % scrolling past 60%, newsletter list size → `pool × prompt CTR × store conversion`.
- **No go/no-go gate for 25 Aug.** Proposed: install threshold, ≥99% crash-free, 0 blocking bugs, ≥4.0 rating with ≥10 ratings, iOS stable. State the slip condition out loud.
- **No attribution.** Distinct UTM/deep link per lever; Singular + Firebase; verify **deferred deep-linking** (tap from an article → land on that article in-app, not a cold home screen).
- **No activation plan** — install ≠ active. First-session experience and push-permission timing undefined.
- **No frequency cap** on the web prompts. Web is the revenue surface; an aggressive interstitial hurts viewability and bounce. Suggested cap: once per user per 7 days.
- **Rating seeding** — Play Store conversion is driven by rating count; ask the WhatsApp community for reviews *before* public launch.
- **D2C & Retail Summit is itself an untapped channel** — captive ICP audience; even a QR on stage slides is free acquisition.
- **Ownership while Nityam is on DRS is unnamed** → levers slip by default.

## ⚠️ Unresolved: the install number
Ranjith has stated **15** and **50** installs in the same conversation, and told Utkarsh **~50** on 2026-08-14. [[project-inc42-launch]] records ~15 (Ranjith) vs 7–8 (Animesh) on 14 Aug. **Get the authoritative Play Console + App Store Connect figure before quoting it** — the whole sizing argument anchors on it. See [[feedback-ask-before-assuming]].

Related: [[project-inc42-launch]], [[reference-inc42-vendor-stack]], [[project-inc42-app-placement]].
