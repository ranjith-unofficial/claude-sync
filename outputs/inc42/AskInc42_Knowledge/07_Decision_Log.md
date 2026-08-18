# Decision Log

**Internal only · v2 · 16 Aug 2026 · Owner: Ranjith**

*v2: DataLabs promoted to its own source document (`08`); Utkarsh's master context ruled out as a knowledge source; decisions renumbered 1–33.*

🔴 **DO NOT INGEST.** Internal record. If this reaches the vector DB, AskInc42 can quote Inc42's internal decision-making back to a user.

Every locked decision behind this knowledge set. Knowledge scope only — build-workstream decisions live in the AskInc42 execution notes.

---

## Scope

| # | Decision |
|---|---|
| 1 | **Five approved knowledge sources:** editorial articles · company information · Inc42 IPs · app context · T&C and Privacy Policy (summaries only) |
| 2 | Articles and company information come from **existing live pipelines**. IPs, app context and policies are **authored documents, not scrapes** — the live sites carry the volatile commercials this scope excludes |
| 3 | **"About Inc42" is part of the IP/company source**, not a sixth source |
| 4 | **Eleven approved IPs:** The D2C & Retail Summit · Inc42 AI Summit · CTO Summit · The D2C Retreat · D2CX Converge · D2CX Runway · FAST42 · MoneyX · Griffin (Founders Club / Retreat) · D2CX · D2CX Foundations |
| 5 | **Griffin, D2CX and D2CX Foundations added** (14 Aug). Griffin is a flagship on Inc42's own About page; D2CX is the parent brand of two IPs already in scope. Leaving them out meant deflecting on live Inc42 properties |
| 6 | **DataLabs promoted to a full source document** (16 Aug), `08_DataLabs.md`. It has more user-facing surface than any single IP and was previously two lines inside the company doc. Tiers are described **as capability, never as price** |
| 7 | **Still out of scope:** ManagementX · AngelX · Fintech Summit · Inc42 Plus · Reports · BrandLabs · 30 Startups To Watch · Startup Spotlight. Inc42 Plus gets company-level description only |
| 8 | **Utkarsh's DataLabs Master Context is NOT a knowledge source.** It is an internal alignment document dense with pricing, business metrics, competitive strategy, personnel and architecture. Only user-facing capability is extracted from it, and only after re-verification against the live site |
| 9 | Every IP record carries **edition, status and dates**. The model answers from them — no separate past/present logic needed |
| 10 | **Concluded editions are retained**, marked concluded, never deleted. Deleting leaves a retrieval gap |
| 11 | On a rename, the **old name is kept as an alias** so existing queries still resolve |

## Behaviour

| # | Decision |
|---|---|
| 12 | **Web search stays enabled**, currently via Perplexity. The five sources are **authoritative** for Inc42-entity questions, not exclusive. Where they don't cover something about Inc42's own business, deflect to Contact Us rather than assembling an answer from the open web |
| 13 | **No price, range, "starts from", tier name, discount code, struck-through price or seat count** — for any IP or product |
| 14 | **Access model is answerable.** Free, paid or invite-only may be stated — it varies by event and is stable. **The moment the question becomes *how much*, redirect to the website** |
| 15 | **Eligibility is answerable.** State published criteria and who an IP is for; describe threshold figures qualitatively and point to the page for exact numbers. **Never rule on whether a specific user qualifies** |
| 16 | **All refund and cancellation queries get one line and one destination: Contact Us.** No policy terms, no per-IP routing |
| 17 | Basic refund awareness is held **only so nothing gets invented**, and is never stated — including on a repeated push |
| 18 | Support routes to Contact Us. How-to-use-the-app questions are answerable; account issues are not |
| 19 | **"High-level summary" = topic + user-facing outcome + where to read the full text.** Nothing more |
| 20 | **Never interpret or apply a clause** to a user's situation |
| 21 | Policy answers come from a **fixed signed-off set**, not free generation over policy text at query time |
| 22 | **Redirect targets are surface-specific.** No email or phone number is ever stated in the app — route to Profile → About → Contact Us |
| 23 | Use **`inc42.com/contact`** — `/contact-us` 404s |
| 24 | **The app has no payments**, so cancellation queries never refer to the app |
| 25 | AskInc42 **links to applications and registrations; it never submits one** |
| 26 | Deflection shape: **name the boundary, offer the nearest capability, hand off concretely.** No speculation, no padding |
| 27 | **Never surface how Inc42's own sites are structured.** The CTO Summit sitting on `events.inc42.com` rather than `inc42.com` is deliberate — use the correct link, say nothing about it |

## Maintenance

| # | Decision |
|---|---|
| 28 | Knowledge lives in a deliberately maintained set with a **defined cadence per document**; manual curation is acceptable provided the cadence is followed |
| 29 | **Weekly review** for IPs; per-release for app context; on-version-change for policies |
| 30 | Every document carries a **`Verified` date**, updated on every review even when nothing changed |
| 31 | The weekly sweep covers **both `inc42.com` and `events.inc42.com`**, plus the standalone IP domains |
| 32 | **`05_Utkarsh_Call_Notes.md` and `07_Decision_Log.md` are never ingested** |
| 33 | This set covers **knowledge scope only**. Design, placements, streaming and lane architecture, v2 flow work and analytics are tracked in the AskInc42 execution notes |

---

## Still with Utkarsh

Two items, both gating this scope directly. Detail in `05_Utkarsh_Call_Notes.md`.

1. **Sign off the approved T&C and Privacy answer set** in `03_Policies_TnC_Privacy.md` — gates S5 ingestion.
2. **Confirm the app-store rationale** behind excluding pricing — the rule ships either way.
3. 🔴 **The live Terms of Use appear stale against the current DataLabs product** — they reference a multi-seat plan and an annual option the product simplified away from, and a Pro Trial length that contradicts internal product documentation. **Since AskInc42 summarises the Terms, a stale Terms document propagates into policy answers.** Resolve alongside item 1, not after it. See `08_DataLabs.md` §12.

Legal and privacy items arising from AskInc42 more broadly sit with the DPDP compliance track.

---

## Immediate

🔴 **The D2C & Retail Summit runs 19 August 2026.** It must flip to `concluded` in `04_IPs_Overview.md` at the first weekly review after that date, or AskInc42 will invite people to an event that's already over. First real test of whether the cadence gets followed.
