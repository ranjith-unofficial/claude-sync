# Utkarsh — Input That Set This Knowledge Scope

**Internal only · v2 · 14 Aug 2026 · Owner: Ranjith**

🔴 **DO NOT INGEST.** Internal reasoning and named owners. If this reaches the vector DB, AskInc42 can quote Inc42's internal decision-making back to a user.

**Scope of this document:** only what Utkarsh said that shaped **what AskInc42 knows and how it answers**. Everything else from those calls — deployment sequencing, streaming and lane architecture, the frontend release brief, design and placement blockers, v2 flow work, analytics — is build workstream, not knowledge scope, and is tracked separately in the AskInc42 execution notes.

---

## 1. Why this workstream exists

Utkarsh flagged that **Inc42 has no central repo or memory of its own internal documents and IPs** — spanning DataLabs, articles and Inc42 products generally. That observation is the origin of the entire knowledge repo.

## 2. The gap, as it stands today

Current live state of AskInc42 on the website, confirmed by Utkarsh (12 Aug 2026):

- It has access to **articles + DataLabs data only**
- It holds **no internal Inc42 documents**
- **Anything asked about Inc42 itself is answered via web search** — it has web-search access

**Decision: web search stays enabled** — currently via Perplexity. The five sources become **authoritative** for Inc42-entity questions rather than exclusive: where they cover something, they win; where they don't, AskInc42 deflects to Contact Us instead of assembling an answer about Inc42's own business from the open web. See `06_Response_Rules.md` §1.

## 3. Ownership

- **Ashish owns the knowledge layer** — Inc42, the app, the IPs, and basic T&C and privacy
- A ticket was created and shared with Ashish on the 12 Aug call

## 4. Utkarsh's maintenance requirement

> The knowledge must live somewhere **deliberately maintained** — repo, doc, Drive, whatever — with either **regular fetching from live sources** or a **defined update cadence**. It must not go stale or static. Manual curation is acceptable **provided the cadence is defined and followed**.

**How this scope answers it:** cadences are defined per document in `00_README_Index.md` — weekly for IPs, per-release for app context, on-version-change for policies. Every document carries a `Verified` date.

**What's still missing:** a **named owner per cadence**. A cadence without one is a static file with extra steps, which is exactly what this requirement rules out. Owners are set in `00_README_Index.md`; the weekly IP review owner is the one to confirm on Ashish's ticket.

**Approach agreed:** Postgres vector DB, **manual weekly review** for the first few iterations — what's missing, what to add, what to remove — with automation later. Deliberately not auto-updating yet.

## 5. Pricing is excluded from the knowledge layer

Locked decision. Two reasons, both deliberate:

1. **Volatility.** IP pricing changes constantly and is owned by the sales and IP team. Keeping it accurate isn't worth the effort, and the nuances — offer windows, tiering — are the real risk, not the fetch. Pulling prices from a database would be technically easy; that was never the blocker.
2. **App-store payment policy.** With Inc42 content now inside the app, quoting a price and pushing users to pay outside the app invites in-app-purchase enforcement. Not a headache worth taking on now.

**This bounds the knowledge repo:** it feeds AskInc42 product and IP *knowledge*, not commercials.

⚠️ Reason 2 is a **product judgement, not a verified legal opinion**, and nothing in this document set treats it as one. Confirmation tracked as B3.

## 6. The five approved sources

Locked scope for this release:

1. **Articles** — everything Inc42 has published, including in-depth startup stories
2. **Company information** — all company-related data
3. **IPs** — the approved event and product IP set
4. **App context** — how the app itself works
5. **T&C + Privacy Policy** — **high-level abstraction only**, not verbatim clause retrieval

## 7. Deflection rules

Pricing → redirect to the website. Refunds, support and cancellation → **Contact Us**. **AskInc42 does not transact, quote or resolve.**

---

## Awaiting Utkarsh

Two items, both of which gate this knowledge scope directly:

1. **Sign-off on the approved T&C and Privacy answer set** in `03_Policies_TnC_Privacy.md`. This gates S5 ingestion — nothing else is blocked by it.
2. **Confirmation of the app-store rationale** behind excluding pricing (§5 above). The rule ships either way; this makes the reasoning defensible if challenged.

Legal and privacy items arising from AskInc42 more broadly — AI sub-processor disclosure, whether the Terms' AI-content disclaimer covers AskInc42's output — sit with the DPDP compliance track, not here.

---

## Deliberately not in this document

Discussed with Utkarsh, but build workstream rather than knowledge scope — tracked in the AskInc42 execution notes, not here:

deployment sequencing (Ask DataLabs before the app) · the frontend release brief in full — auto-routed lanes, stream event contract, Agent V3, webhook selection, "Go deeper" telemetry · the cross-session cache leak and its DPDP reportability question · design and placement blockers · AskInc42 v2's stored-questions flow and its API dependency · Ask DataLabs analytics · feature-flag work · daily priority ordering.
