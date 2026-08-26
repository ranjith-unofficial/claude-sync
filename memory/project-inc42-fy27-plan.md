---
name: project-inc42-fy27-plan
description: "Utkarsh's LOCKED FY27 Plan — Engines × Tracks (the authoritative horizon frame all Inc42 work serves)"
metadata: 
  node_type: memory
  type: project
  originSessionId: d8963308-0bb1-4e90-a221-f2c4311ce0ba
  modified: 2026-08-26T06:16:17.350Z
---

**Utkarsh's FY27 Plan — Engines × Tracks**, LOCKED 2026-08-21. The authoritative horizon plan (Aug 2026→Mar 2027). File: `~/Downloads/PMTD MOP 2026.xlsx`, tab "FY27 Plan — Engines × Tracks" (the only tab to reference; the MOP tabs are per-month operating plans that SERVE these tracks). Supersedes/overarches [[project-inc42-strategy-utkarsh]]. Griffin is out of scope.

**Spine = the engine verbs (one person, any surface):** Acquire & Identify → Activate & Deepen → Retain & Renew. Every MOP row is a SURFACE (App/Datalabs/Web/Data) that "Serves" one of these journey-stage tracks — Monday serves-check enforces both directions.

**Engines × Tracks (owner):**
- Newsroom (Editorial) — upstream of all engines, thin by design.
- **O1 Brand & Distribution:** Brand & Campaigns (Nityam), Social (Arminder), Video (Aditya), Distribution/citations (Nityam).
- **O2 Audience:** Measurement & Data Activation (Prapti warehouse · Ranjith instruments) · **Unification** (Utkarsh chair → Ranjith at delivery; Nityam owns brand/messaging half) · Acquire & Identify (Growth+Ranjith gates/capture · Nityam acquisition) · Activate & Deepen (Ranjith runs · Utkarsh scores) · Retain & Renew (Ranjith renewal/in-product · Animesh campaigns) · AI Layer/Ask (Ranjith+Ashish) · Offering (Ranjith+Utkarsh).
- **O3 IPs/Events/Communities** (per-IP owners; QAA = same bar as QIA).
- **O4 Engine Room:** Internal AI & Agent Platform (Prapti pilots · Ranjith platform; A11 = cost/QIA flat while QIA scales), Automation & Infra.

**Unification track (the TRUE scope, narrow):** Aug = define "One Inc42" in writing (one login, one nav, one value-prop — a dated DOC is the deliverable, not a meeting) + audit where the 3 services contradict + lifecycle journeys ship for Datalabs & App SEPARATELY first (unify after, by design). Sep = **UNIFICATION PLAN shipped** (one design for messaging/nav/onboarding/lifecycle across all 3; delivery phased) + cross-surface use measurable (1.6–3.4% today). Oct = hands to Ranjith for delivery. **Waits on: identity spine (Sep, Engine/Measurement track).**

**Locks that reconcile our unification roadmap (which mixes several tracks):**
- Capture at **app SIGN-IN, not signup** (3 in 4 app users already have accounts). 🔴
- **QIA jump is a MEASUREMENT fix, not growth** — only 3 of 9 activities computed today; when the rest pipe in the number jumps; must not be banked as growth. 30-day tracking changeover clears **~20 Sep** → north star measurable properly for first time.
- The **sign-up gate is a TEST** (web, Sep) with an **Oct decision** owned by Ranjith ("does it cost more traffic than it gains identity") — NOT a committed build.
- **Mechanism competition** (alerts/community/Datalabs Weekly/Pulse/entity surfaces) runs INSIDE Activate & Deepen: candidates named Aug, **FIRST SCORING Oct** (30-day return, real data), winners invested Nov, become membership candidate entitlements Dec.
- **A1 price probe = Sep**, read Sep (Offering).
- Ask: streaming/fast mode + in-app shipped 21 Aug; decide Ask on Inc42.com (Sep); Ask on all 3 surfaces by Oct.

**Undecided register (owner · when · signal):** what "One Inc42" means (Utkarsh · Sep · written doc) · unification owner after Oct (Utkarsh · Oct retro) · which retention mechanisms survive (Utkarsh scores Oct → Ranjith invests Nov) · membership contents (Dec) · price/packaging (Utkarsh · Sep · probe) · sign-up gate stays? (Ranjith · Oct · gate test) · AI layer paid vs free (Nov) · editorial metric (Utkarsh+Editorial · ~Oct) · message convergence (Nityam · Sep) · consent rules (Prapti→legal · Oct) · merge 3 messaging workspaces (Utkarsh · TBD).

Implication for [[project-inc42-funnel-analysis]] / the unification sheet: our "Unification Roadmap" spans MANY of these tracks — per Note 1 every feature must name the FY27 track it Serves; the true Unification track is just define→design→phased-deliver.

---

**Sep planning call with Utkarsh — 21 Aug 2026, 9:00–10:10 PM IST** (Wispr meeting `b516e3d6-63b2-43ed-96d7-0fdc447210db`).
⚠️ That notetaker summary has the speaker labels FLIPPED — items it credits to "Utkarsh" are Ranjith's and vice versa. The list below is corrected.

**Ranjith owns:** the **detailed September MOP** (merge Aug + Sep MOPs into one plan, ambitious + practical goals, structured Awareness/Acquisition/Activation/Retention against a north-star metric) · the **Mon–Wed task plan** so devs aren't blocked · two recorded user-feedback calls stored in a shared folder · product-marketing referral asks · reconnect with Utkarsh over the weekend to **lock the plan before Monday**.

**Utkarsh owns:** the analytics + DataLabs tracking-plan sheets · finalizing the product-marketing hiring assignment (interviews next week) · following up with Ashish on the "remaining scan bug fix" (*what this refers to is UNKNOWN — six garbled words from the notetaker; transcript never pulled*).

**Decisions from that call:**
- Event and event-property conventions stay unchanged; **only user properties** migrate to the new convention, pushed via reverse ETL from the warehouse.
- **Workspaces stay separate per platform** — historical stitching is impossible for the ~95% non-logged-in base.
- **App is the primary acquisition + engagement surface.** Inc42 website gets hygiene + small experiments only, capped at **5–10% of bandwidth for 15–20 days**. DataLabs' core gap is retention (no reason to return) → parallel experiments.
- Tracking plans: update, verify implementation matches, **weekly audits**, unify into one master sheet.
- Behavioural scoring / RFV in the warehouse **deprioritized** until logic and use case are clear.
- **Monday leads meeting** becomes the channel for weekly priorities and design-bandwidth conflicts (e.g. Satya on website banners vs app).
- **QIA likely shifts 30-day → 7-day** for faster feedback loops.
- Onboarding fields/values to be unified across platforms; skip questions already answered.
- Ideas raised: MCP connector for Inc42 content as an acquisition play; shift IP ticket acquisition from ~70–80% paid to 50/50 organic via the audience engine.

---

**Sep MOP artifact** (built from this call): https://claude.ai/code/artifact/3c67e85a-aaed-47c3-bb57-4bd5eb366607 — 5 Aug close-out items + 9 (now 13) September goals, "only goals Ranjith is accountable for."

**Utkarsh's feedback on the Sep MOP draft — 24 Aug 2026.** Deliberately excludes "when are we launching Pulse" (out of scope for this MOP). Added as rows 10–13 in the artifact; row-1-equivalent (employer/seniority capture) explained in chat but NOT yet folded into Goal 06 — pending Ranjith's call.
- **Employer+seniority capture must happen at app SIGN-IN, not signup.** 198 app persons have `role` captured; ZERO have an `employer` property — org type is literally half the QIA-qualified bar ([[project-inc42-strategy-utkarsh]]'s "role+company" definition). Sign-in outnumbers register 119:29 (~4:1) — a signup-only ask permanently caps capture at ~¼ of touchpoints. Sep goal 06 (Unified onboarding) is adjacent but doesn't name this.
- **App events already emit but never reach the warehouse** — `app_session`, watchlist, search/profile-view. Wiring them in recovers 3 QIA-qualifying actions at once. Depends on Sep goal 01 (fix the events) landing first.
- **Unified Inc42 frontend changes** discussed in a 24 Aug meeting — blocked on the whole team agreeing one unification plan first. No further detail captured on that meeting yet.
- **Reverse ETL to Customer.io + PostHog** — sequenced after Sep goal 02 (unify tracking docs); can't run on today's uncorrected property set.
- **DataLabs lifecycle journeys + the new DataLabs newsletter are missing from the MOP entirely** — no owner, no target, needs scoping before the Monday lock.

**How to apply:** treat rows 10–13 in the Sep MOP as unowned gaps needing assignment before Monday's lock, not committed work yet. Re-check with Ranjith whether Goal 06 gets amended for the sign-in/employer point once he's decided.

**Row 14 added 26 Aug 2026 — Search functionality + visibility.** Ranjith's own addition (not Utkarsh's), framed explicitly as an engagement lever, not a discovery/UX nice-to-have. No baseline, target, surface (app/web/Datalabs) or owner specified yet — flagged "New — needs scoping" rather than a number invented for it.
