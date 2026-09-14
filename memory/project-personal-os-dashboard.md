---
name: project-personal-os-dashboard
description: "ranjith.tech Personal OS dashboard — repo location, leaked secrets, and the prod API deploy gap"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5de0a2e2-4280-4568-9182-9020d731f343
  modified: 2026-09-14T19:00:39.962Z
---

**Personal OS** = the unified `/sys-admin-sec892` dashboard on [[reference-ranjith-tech]].
Built 15 Sep 2026. Four tabs: Home (Today) / Health / Day & Content / Ops.

**Repo:** `github.com/ranjith-unofficial/personal-portfolio` (private).
Local working copy: `~/Documents/ai apps/personal-portfolio` (cloned fresh — the older
`~/Documents/ai apps/ranjith-portfolio` is a **different, stale** repo on remote
`ps-ranjith/personal-portfolio`, Python backend, do not confuse them).

**Two findings he must act on (as of 15 Sep 2026, unresolved by me):**
1. `ranjith_tech_LIVE_DEPLOY.zip` was committed to git containing `backend/.env` with
   live `ADMIN_PASSCODE`, `MONGO_URL`, `WEBHOOK_URL`. Plus `EMERGENCY_RECOVERY_KEY`
   in plaintext in VERSION_LOG.md. All burned — rotate in Hostinger. Untracked from
   HEAD; history purge prepared at `scripts/purge_secrets_from_history.sh`, not run.
2. **The Express backend is not deployed.** CI (`.github/workflows/deploy.yml`) ships
   only static `public_html/*`; `.htaccess` rewrites everything to index.html; no
   `/api` proxy exists. The admin cannot load data in prod until a Node process runs
   on Hostinger *and* Apache proxies `/api` to it.

**Architecture decisions locked:**
- Local JSON in `backend/data/` is the single store. Mongo was never wired —
  `mongoose` is an unused dep; old docs claiming "MongoDB + JSON mirrors" were wrong.
- All dates are Asia/Kolkata days (`istToday()`), never UTC.
- Oura and Google Calendar **never fabricate data** — they return
  `{ synced/connected: false, reason }` and the UI shows the reason. This replaced
  hardcoded fake scores (88/86/91) that were indistinguishable from real ones.
- `POST /api/ingest` is the single write door for external agents, authed with
  `PERSONAL_OS_AGENT_TOKEN` (≥32 chars).
- Content `generate-day` is rule-based, not an LLM. Writes explicit `[fill: …]`
  placeholders instead of inventing achievements — matches
  [[feedback-document-calibration]].

**Auth decision:** he chose to keep the bearer token for v1 rather than switch to
httpOnly-cookie JWT, to avoid lockout risk before `/api/*` is reachable in prod.
