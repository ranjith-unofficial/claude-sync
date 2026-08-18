# AskInc42 Knowledge Set — Index

**v1 · 14 Aug 2026 · Product owner: Ranjith · Knowledge layer owner: Ashish · Build: Ritvik Sethi**

One document per topic. Each is self-contained and can sit in its own tab. Nothing is duplicated across files — if a fact belongs in two places, it lives in one and is cross-referenced.

**No pricing appears in any document in this set.** No amounts, pass tiers, discounts, or seat counts. This is deliberate — see `06_Response_Rules.md`.

**This set covers knowledge scope only** — what AskInc42 knows and how it responds. The AskInc42 build workstream — design and placements, streaming and lane architecture, the frontend release contract, v2 flow work, analytics — is tracked separately and does not belong in any document here, including the internal ones.

---

## The documents

| # | File | What it is | Ingested into AskInc42? | Owner | Review |
|---|---|---|---|---|---|
| 01 | `01_App_Knowledge.md` | How the Inc42 app works, in user-facing language | ✅ Yes — **Source S4** | Ranjith | Per app release |
| 02 | `02_Inc42_Company.md` | What Inc42 is, what it runs, how to reach it | ✅ Yes — **Source S3** | Ashish | Monthly |
| 03 | `03_Policies_TnC_Privacy.md` | Approved high-level summaries of T&C + Privacy Policy | ✅ Yes — **Source S5** | Ashish, signed off by Utkarsh | On policy version change |
| 04 | `04_IPs_Overview.md` | The eight approved Inc42 IPs, high level | ✅ Yes — **Source S3** | Ashish | **Weekly** |
| 05 | `05_Utkarsh_Call_Notes.md` | Utkarsh's input that set this knowledge scope — nothing else from those calls | ❌ **NO — internal only** | Ranjith | As calls happen |
| 06 | `06_Response_Rules.md` | How AskInc42 must behave: deflections, boundaries, refusals | ⚙️ System behaviour, not knowledge | Ranjith | On rule change |
| 07 | `07_Decision_Log.md` | Every locked decision behind this set | ❌ **NO — internal only** | Ranjith | On decision change |
| 08 | `08_DataLabs.md` | What DataLabs is, its tiers as capability, profiles, signals, search | ✅ Yes — **Source S3** | Ashish | Monthly |

🔴 **05 and 07 must never be ingested.** They contain internal reasoning, blockers and named owners. If they end up in the vector DB, AskInc42 can quote Inc42's internal decision-making back to a user.

---

## The five approved knowledge sources

| Source | Where it comes from | Covered by |
|---|---|---|
| **S1 — Editorial articles** | Existing live pipeline | Already live, no doc needed |
| **S2 — Company information** | Existing live pipeline (DataLabs) | Already live, no doc needed |
| **S3 — Inc42 IPs** | Authored | `02` + `04` + `08` |
| **S4 — App context** | Authored | `01` |
| **S5 — T&C + Privacy** | Authored summaries only | `03` |

S1 and S2 are pipelines. S3, S4 and S5 are **authored documents, not scrapes** — the live sites carry the volatile commercials this set deliberately excludes.

---

## What was added beyond the five topics requested

| Doc | Why it exists |
|---|---|
| `06_Response_Rules.md` | The deflection behaviour is not knowledge — it's a rule set. Left inside a knowledge file it either gets ingested as facts or gets missed by whoever wires the prompts. It needs its own home. |
| `07_Decision_Log.md` | Every decision behind this set in one place, so nobody re-opens a settled call. Open items were reviewed and closed on 14 Aug — only two Utkarsh sign-offs remain, and they sit in `05`. |
| `00_README_Index.md` | Seven files with no map is how the confusion comes back. |

---

## Maintenance

Utkarsh's requirement: the knowledge must live somewhere deliberately maintained, with either regular fetching from live sources or a **defined update cadence**. Manual curation is fine **provided the cadence is defined and followed**.

- Cadences are in the table above. `04_IPs_Overview.md` is weekly because editions, dates and application windows move fastest.
- Every document carries a `Verified` date in its header. Update it on every review, even when nothing changed.
- **A cadence with no named owner is a static file with extra steps.** Owners are named above; confirm them on Ashish's ticket.
- **Sweep both hosts** — `inc42.com` *and* `events.inc42.com`. The CTO Summit was missed in the first audit because it lives on the subdomain and isn't on the main events listing.

---

## Where the lines fall

Three rules do most of the work, and they are easy to blur:

- **Access model vs price.** *"Is D2CX paid?"* is answerable. *"How much is D2CX?"* is a redirect.
- **Eligibility vs a ruling.** *"What are the criteria?"* is answerable. *"Do I qualify?"* is not.
- **Authoritative vs exclusive.** Web search is on. The five sources win on anything about Inc42's own business; where they're silent, deflect rather than reconstruct.
