---
name: project-inc42-legal-compliance
description: "Inc42 app T&C + Privacy Policy update — locked decisions, account-deletion model, store gates"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1b85df8c-b255-4a10-9994-1dbcc66c6987
---

Updating Inc42's live T&C and Privacy Policy to cover the mobile app, for [[project-inc42-launch]]. **Must be live on inc42.com BEFORE the iOS submission (~Jul 17–18)** — store reviewers fetch the live URL.

**Source of truth:** Utkarsh's compliance review + tracked drafts (`Inc42 App — Legal Policy Updates (Jul 2026)`, in ~/Downloads). It **supersedes** Ranjith's earlier amendments doc. Privacy changes = P-1…P-17; T&C changes = T-1…T-7.

**Utkarsh's 12 locked decisions (2026-07-11)** — the ones that keep resurfacing:
1. **Ad tracking = SKAN-only.** No device-level IDs to Meta/Google → **no ATT prompt**, no "Data Used to Track You" label.
2. Deletion = **in-app on BOTH platforms** + `inc42.com/delete-account` web page. Email-only was the one 🔴 error (Play has required in-app deletion since 2023).
5. Deletion/privacy contact = **grievances@inc42.com** (NOT plus@, which stays subscription support).
8. Apple **Standard EULA** governs the app licence (pattern (a)) → Apple's 10 "minimum terms" do NOT bind us; no developer name/address clause needed.
12. **Ideope Media Pvt Ltd** owns both developer accounts → the App must be attributed to **Ideope** in both policies (store-listing ↔ policy entity must match).

Also: grievance officer stays **title-only** (accepted risk); Cookie Policy folded into Privacy §6 (the standalone page 404s); accounts stay **18+** while the app rates Teen; **EU storefronts excluded** at launch.

**Account deletion model (Ranjith's, finalized 2026-07):**
- Request → account deactivated, signed out of **all devices incl. Datalabs**
- **7-day restore window** — signing in restores everything
- After 7 days → permanent deletion; signing in creates a new account
- **Exception:** suspected fraud/unauthorised access → verify first, complete within **30 days**
- **If no response in 30 days → do NOT delete. Restore the account** (an unverified deletion is more likely hostile, and it's irreversible)
- Dev: revoke Sign in with Apple tokens at **permanent deletion (day 7)**, not at request. Fire a Customer.io event so deleted users get no newsletters.

**Still open:** `[PUBLISH DATE]` in both docs; Ethics-page address mismatch; retention periods need counsel sign-off.

See [[reference-inc42-vendor-stack]] for the verified vendor facts these policies depend on.
