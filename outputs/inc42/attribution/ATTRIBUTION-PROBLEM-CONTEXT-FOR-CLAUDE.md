# Attribution problem context — for Claude

**Owner:** Ranjith (Inc42 Product)  
**Packed:** 12 Sep 2026  
**Use:** Paste/open this with Claude before designing or implementing tracking. Do not invent product decisions; propose contracts and call out gaps.

---

## Problem statement (what I am trying to achieve)

I need clear **source** on every meaningful step so product and growth can answer:

1. **Where did this user come from?** (campaign, link, share, organic, push, etc.)
2. **How did they open the app this session?** (icon vs push vs deeplink vs deferred after install)
3. **Inside the app, how did they reach this screen / this content?** (previous screen / module — e.g. Brief → article, Search → company, Home → story)

Today those answers are fragmented or missing: Singular and PostHog are weakly connected; many App events lack a universal previous-screen property; some sheet `source` fields are wrong (DataLabs enums leaking into App). Without source, funnels lie, CIO/ campaigns misfire on “how they arrived,” and we cannot trust “install → open → journey” stories.

**North-star outcome:** For any user journey I care about, I can see **install source** (if first open after install), **open source** (every session), and **in-app navigation source** (screen-to-screen), in PostHog (product) with Singular remaining MMP system of truth for install/campaign attribution.

---

## Three layers (keep them separate)

| # | Layer | Question | Typical owner |
|---|--------|----------|----------------|
| **A** | **App install source** | How / from where was the app **installed**? (paid, Singular link, organic store, deferred deeplink after install) | Singular (MMP) → copy into PostHog person / first-open |
| **B** | **App open source** | How was the app **opened this time**? (organic icon, push, deeplink, deferred) | Client OpenContext → one PostHog `app_opened` (or equivalent) |
| **C** | **In-app screen source** | On this event / screen, **what was the previous screen** (and optional module/position)? | Client `last_screen` → stamp `source_screen` on content events |

**A and B are different.** Install answers “how they got the binary / first attribution.” Open answers “why this session started.” Someone can install from a campaign last week and open organically today — both must be knowable.

**C is different again.** Open source is not enough to know Brief → article vs Search → article.

---

## What “source” means in practice

### A — Install source (file stub: `01-tracking-app-installation-source.md`)
I want to know:
- Was install organic vs attributed network/campaign/creative?
- Was there a deferred deep link destination (content type/id)?
- First-touch attribution on the person (stable), last non-organic touch when relevant.

### B — App open source (file stub: `02-tracking-app-open-source.md`)
I want to know on **each** open/session:
- `open_source`: `organic` | `push` | `deeplink` | `deferred` (and unknown if timed out)
- If push: notif / campaign ids
- If link: path, content type/id, Singular / UTM fields when available
- One open event only; late Singular enriches person / `attribution_updated`, does not double-count opens

### C — Screen-to-screen (include in Claude discussion; not one of the two empty stubs)
I want to know:
- Event name ≈ **current** surface (`article_opened`, `company_profile_viewed`, …)
- Property **`source_screen`** (and optional `source_module` / `source_position`) = **previous** surface
- Reconstruct full path by ordering events in a session + following `source_screen`

Example story path:  
`app_opened` (open_source=organic) → `brief_page_opened` (source_screen=home) → `brief_opened` → `card_viewed` → `article_opened` (source_screen=brief_card) → `story_shared` (source_screen=article)

---

## Constraints already locked / drafted (do not ignore)

- **Singular** = only MMP for now (install + campaign / link attribution).
- **PostHog** = product analytics; pipe Singular fields in; stitch same `user_id` on login.
- Existing draft plan: `singular-posthog-attribution-plan.md` (Phase 1 = open + install attrs; Phase 2 = shares/web Singular wrapping + universal `source_screen`).
- App Lifecycle / Ashish sheet is taxonomy SoT for event **names**; many App rows wrongly show `source` as `woocommerce|razorpay` — that is **not** nav source.
- Separate problem: PH ↔ Customer.io **destination parity** (Animesh / brief_completed) — do **not** mix into A/B attribution design unless asked.

---

## What Claude should produce when working these stubs

For **each** of the two empty files (install vs open):

1. Problem restatement in one paragraph  
2. Event + property contract (names, enums, required/optional)  
3. Runtime flow (SDK init, wait, priority if push+deeplink+Singular race)  
4. PostHog vs Singular responsibilities  
5. QA matrix (scenarios → expected props)  
6. What is **out of scope** for that file (explicitly point to the other file / to screen-source)

Do **not** collapse install and open into one event model without calling out the cost.

---

## Related local paths

- This context: `~/ClaudeDocs/inc42/attribution/ATTRIBUTION-PROBLEM-CONTEXT-FOR-CLAUDE.md`
- Empty stubs (fill with Claude):
  - `~/ClaudeDocs/inc42/attribution/01-tracking-app-installation-source.md`
  - `~/ClaudeDocs/inc42/attribution/02-tracking-app-open-source.md`
- Prior draft: `~/ClaudeDocs/inc42/singular-posthog-attribution-plan.md`
- Screen nav contract already sketched in that plan §10 (`source_screen`)

---

## One-liner for the team

*Install source = how they got the app. Open source = how this session started. Screen source = how they moved inside. Track all three; never confuse them.*
