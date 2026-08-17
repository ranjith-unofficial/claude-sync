---
name: project-inc42-app-structure
description: "Inc42 app navigation/IA — CONFIRMED from Figma (vKuPUMuhLos0rC1AFR5cWq) 2026-07-31: 3-tab bottom nav, persistent header, Streak/Profile mechanics, and a pre-existing 'Compass' AI concept"
metadata:
  node_type: memory
  type: project
  originSessionId: 60cb3464-2e9c-4ebe-a009-471fcce371a0
  modified: 2026-07-31T10:44:39.127Z
---

**Full IA confirmed 2026-07-31** by reading the Figma file directly (metadata tree, ~22.6K lines, file `vKuPUMuhLos0rC1AFR5cWq`, page "APP UI V1"). This replaces the earlier partial/guessed structure. See [[project-inc42-askinc42]] for the placement analysis this unlocked.

## Bottom navigation — only 3 tabs
Confirmed via the shared component "Frame 1686561727" (`solar:home-2-outline` / `solar:card-search-bold` / `solar:bookmark-line-duotone`), present identically on Brief, Explore→Article tab, and other core screens:
1. **Brief** (labeled "Home" in some variants, "Brief" in others — a naming inconsistency in the file, flag to Nityam)
2. **Explore** — sub-tabs **Articles** / **Companies** (icons `news` / `building-03`), plus horizontal filter chips (Latest / Top Deals / Financials / Edtech, sector-scoped)
3. **Watchlist** — states seen: `watchlist/tracking` and `watchlist/Saved`

**No 4th tab.** Streak, Profile, and Ask are not bottom-nav items.

## Persistent global header (all 3 tabs)
Component "Frame 1686562036" repeats on Brief, Explore, and Watchlist screens alike:
- A contextual left icon/label (search on Explore; date+greeting on Brief; a bell/opportunities icon on Watchlist)
- **Streak badge** — fire icon + count (e.g. "1.2K"), always visible, tap-through to the Streak page
- **Profile avatar** (initial letter) — tap-through to My Profile

This header, not a tab, is the actual persistent real estate across every screen — more prominent than Explore/Watchlist for anything wanting cross-tab visibility.

## Streak — not a tab, lives in two places
1. **Header badge** (above) — always-visible glanceable counter.
2. **"Streak page (full)"** — a dedicated deep screen (found loose under an "exploration" scratch section, reached via the header badge and/or Profile): day count, weekly calendar, badges, "2 streak freezes," "Streak safe · 6 days," streak history, and a streak FAQ block. Pure gamification — no query/content surface here.
Also nested inside **My Profile**: "My Streak" entry point, "Edit profile," "Edit Role," "Edit Sector," Push notification settings — Profile is a settings/identity hub, not a content hub.

## Brief-end (post-completion) — already a designed sequence, not a blank slate
Confirmed via frames "streak celebration part 1/2" and screenshot: on completing the brief —
1. Full-screen streak hero animation ("Day Streak!" + count, weekly Mon–Sun check row, "Amazing start! Think you can do it tomorrow?")
2. Immediately followed, same screen, by an **"Explore Trending Stories" horizontal carousel** (article cards with Decode / View Full Article buttons)
3. A pinned **"EXPLORE MORE"** pill CTA at the bottom, routing into the Explore tab

This is the app's existing answer to "what now?" after the brief — and it answers with *more content*, not a question prompt. Directly relevant to [[project-inc42-askinc42]] placement.

## Account deletion screen — data categories (relevant to legal/DPDP, see [[project-inc42-legal-compliance]])
The delete-account confirmation lists exactly 4 things erased, grouped as:
- "Your 12-day streak & all badges"
- "Watchlist" (e.g. "8 companies · 3 sectors")
- **"Saved articles & Ask history"** — confirms an Ask/AskInc42-style history is already assumed as existing user data, and is bucketed with saved articles (content), not with streak/watchlist (gamification/tracking)
- "Reading history & preferences"

## "Compass" — dismissed, sample content only
The Login screen's "Compass, your AI co-pilot" line was **placeholder/sample Figma content**, not a real product concept (Ranjith confirmed 2026-07-31). Not a naming or scope collision with [[project-inc42-askinc42]]. No action needed.
