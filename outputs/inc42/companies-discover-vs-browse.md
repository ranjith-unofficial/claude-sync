# Companies: Discover vs Browse (V2 lock draft)

**Date:** 10 Sep 2026 · **Status:** recommendation for lock (Ranjith)  
**Sources:** Sep 9 design Wispr (c7L16n7… / `975a26fb…`); Sep 8 product review; Sep 9 P&D; Prapti Slack (tag defs + cadence); prior IA briefs

---

## Split (locked from Wispr)

| Surface | Job | What belongs |
|---|---|---|
| **Discover** (NEW) | Fresh discovery — “what’s happening” | Event-driven rails first; editorial only with time-decay / calendar boost |
| **Browse / All companies** (existing Explore companies) | Database + quick filters | Stage/sector chips; Recently Funded as *filter*; full 70k |

Utkarsh: Recently Funded / in-the-news style rails stay on **Discover**, or the feed recirculates the same ~20 curated companies. 30 To Watch = *manually dynamic* (monthly + ~7-day boost), not permanent Discover hero.

---

## Discover rail stack (recommended lock)

### Tier A — Always-live (above fold; refresh daily+)

| # | Rail | Query / source | Refresh SLA | Card “why now” |
|---|---|---|---|---|
| 1 | **Recently Funded** | DataLabs funding events (latest rounds) | **Daily** (or near-live) | Raised X · date |
| 2 | **In the News** | Companies mentioned in Media (article join → company_id) | **Daily** | In news · article date |
| 3 | **Just Launched** | Launch / incorporation window if data exists | **Daily** when live | Launched · date |

*Seasonal overlay (not permanent dead weight):* **New Financials / filings** — boost Oct–Nov+ and around listed earnings windows (Utkarsh); otherwise hide or demote.

### Tier B — Calendar / editorial boost (not permanent heroes)

| Rail | Behaviour | Refresh SLA |
|---|---|---|
| **30 Startups To Watch** | Pin high **~7 days after monthly edition publish**, then demote/hide until next edition | **Monthly** edition (Prapti pipeline) + 7-day boost |
| **Series tags** (AI / manufacturing / etc.) | Same: boost N days after Marketing/Editorial series launch | Per series calendar |
| **Profitable Startups** | Keep on Discover only if membership/ranking moves often; else Browse chip + optional carousel with “updated” stamp | Filter rebuild when financials refresh (MCA-dependent) |
| **IPO Pipeline** | Discover only when tagging live; else Browse | Build 2–3d (Prapti); partly manual / Enterprise today |
| **AI Startups** | OK as Discover rail if tracker membership updates; else Browse chip + series-boost when AI series launches | Tracker cadence |

### Tier C — Status lists → Browse by default

Unicorn · Soonicorn · Minicorn → **Browse quick filters** (membership changes slowly). Discover only with a **delta** story (“new unicorns this quarter”) — optional later.

---

## Browse quick-filter stack (recommended lock)

**Primary chips:** Unicorn · Soonicorn · Minicorn · Recently Funded · Fintech (and other sectors) · AI Tracker · Profitable · IPO-bound / Listed (when ready)

**Secondary / don’t hero:** FAST42 · Startup Watchlist (inactive series) · UpNext (use as series boost or Browse chip, not third editorial hero next to 30 To Watch)

Entry: Discover CTA “Browse all ~70k” → this page (make path memorable; Utkarsh flagged hierarchy).

---

## Freshness mechanics (non-negotiable)

1. Each Discover section = **query** (company_id + event_time + score), not a monthly pasted sheet.
2. **Rail order is dynamic** — calendar can promote a rail for N days; Recently Funded always high.
3. **Dedupe across rails** — same company must not dominate every carousel.
4. Card shows **why now** (raised / in news / new filing / new edition).
5. Optional microcopy: “Updated today / this week” on Tier A.
6. Cards still use shared **top-3 of ~10 metrics** hierarchy (separate lock with Prapti).

---

## Data readiness (evidence, not invented)

| Asset | Cadence / state | Implication |
|---|---|---|
| Funding / Recently Funded | Live/near-live events (Prapti: funding OK for Brief) | **Tier A #1 — ship** |
| 30 To Watch / Watchlist / UpNext | **Monthly** pipeline; upsert by company+tag+edition; ~2,108 rows mapped | Tier B with 7-day boost; Watchlist inactive |
| Unicorn / Soonicorn / Minicorn | DB tags exist (Prapti) | Browse chips |
| Profitable (~60, >10cr, >90% margin) | Filter exists; financials same-day hard | Discover only if refresh story exists |
| IPO pipeline | 2–3 days to build; not full yet | Gap — Browse/Discover when ready |
| Listed stock movement | Daily data exists; **tech sync pending** | Gap for Listed chip |
| In the News join | Needed for Tier A #2 | **Gap** — confirm Media→company_id join |
| Just Launched | Value prop still to vet | Gap — park until definition + data |
| AI Tracker | 151 rows | Browse or Discover if membership moves |

---

## Gaps to flag

1. **In the News** company join for Discover (may not exist end-to-end).
2. **Just Launched** definition + data still unvetted.
3. **IPO pipeline** still partly manual.
4. **Listed** needs tech sync of daily stock data.
5. **Profitable** Discover placement depends on how often the set moves.
6. Analytics: new events for Discover page + universal source-screen (Wispr).

---

## Proposed V2 lock (one screen)

**Discover (default Companies landing):**  
1 Recently Funded → 2 In the News *(if join)* / else skip → 3 Just Launched *(if ready)* → 4 calendar rail (30 To Watch when in boost window, else hide) → 5 AI or Profitable or IPO *(whichever has freshest membership that week)* → CTA Browse all.

**Browse:** chips Unicorn · Soonicorn · Minicorn · Recently Funded · Sector · AI · Profitable · IPO/Listed (when ready).

**Do not:** make Unicorn/Soonicorn/30 To Watch permanent Discover heroes; do not leave Discover as only monthly editorial lists.
