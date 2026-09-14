# Claude brief — Unify ranjith.tech Everything Admin into one Personal OS dashboard

**Owner:** Ranjith (personal)  
**Repo:** https://github.com/ranjith-unofficial/personal-portfolio (private)  
**Live site:** https://ranjith.tech/  
**Admin route (existing):** `/sys-admin-sec892` via `EverythingAdmin.jsx`  
**Date:** 14 Sep 2026  
**Rule:** Personal lane only. Do not touch Inc42 repos. Prefer one coherent architecture over adding more one-off tabs.

---

## 1. What already exists (do not reinvent blindly)

Stack: React/Tailwind frontend + Express backend (`backend/server.js` mounts modular routers). Auth: admin passcode / bearer token (`routes/admin.js`). Persistence: local JSON via `backend/lib/helpers.js` (VERSION_LOG also mentions Mongo + JSON mirrors; reconcile, do not fork a third store).

### Backend routers (`backend/routes/`)
| Module | Mount | Purpose |
|---|---|---|
| `admin.js` | `/api/admin` | login, logout, me, emergency-unlock |
| `health.js` | `/api` | workouts, health dashboard, Oura sync, metrics (weight etc.), nutrition targets |
| `invoices.js` | `/api` | invoice CRUD |
| `shortener.js` | `/api` + `/` | URL shortener create/list/redirect |
| `lms.js` | `/api` | LMS courses/users/submissions |
| `telemetry.js` | `/api` | visit stats |

### Key health APIs already present
- `POST /api/workouts/sets` (admin) — `{ splitName, exercises[], descriptionNotes, date }`
- `GET /api/workouts/history` (admin)
- `GET /api/health/dashboard` — Oura-ish scores + nutrition cache
- `POST /api/health/oura/sync` — Oura v2 daily readiness/sleep/activity when `OURA_PERSONAL_ACCESS_TOKEN` set
- `GET/POST /api/health/metrics` (admin) — weight, bodyFat, bmi, visceralFat, muscleMass, bmr
- `GET/POST /api/health/targets` (admin) — calorie/macro targets

### Frontend admin tabs (`frontend/src/pages/admin/`)
`EverythingAdmin.jsx` switches: Health Hub & Oura · LMS · URL Shortener · Invoices · Insider Telemetry.

**Docs in repo:** `ARCHITECTURE.md`, `VERSION_LOG.md` (treat VERSION_LOG as partially stale vs ARCHITECTURE; fix inconsistencies as part of cleanup).

---

## 2. Product goal (Ranjith’s ask)

One login → **one dashboard home** that answers:

1. **Personal health / fitness** — workouts, weight progress, Oura rings (readiness/sleep/activity), food intake vs targets  
2. **Today / professional day** — what is on my plate, what to close, calendar-shaped day view  
3. **Content OS** — daily structure of posts to make (LinkedIn etc.); generated/updated via API from what he did; dense content optimization  
4. **Ops tools stay in the same shell** — invoices, URL shortener (already exist; fold into nav, do not orphan)

Food + detailed workout logging may be entered by another AI tool; this system must expose clean **write APIs** so either Ranjith or that tool can POST updates. Same for CoS/PA agents posting “today’s content plan.”

---

## 3. Target IA (single shell)

Replace “tab soup” with:

### A. Home — Today
- Date (Asia/Kolkata)
- Oura rings strip (readiness / sleep / activity) + last sync
- Today’s workout status (done / planned / skip)
- Weight trend sparkline (last N metrics)
- Nutrition: logged vs targets (calories + protein minimum)
- **Day board:** Must close today (tasks) · Calendar blocks (read-only first if Calendar connector later) · Content queue for today
- Quick actions: Log workout · Log food · Sync Oura · New invoice · New short link · Generate today’s content pack

### B. Health
- Workouts history + logger
- Weight / body composition charts
- Oura detail + sync button
- Food log + targets

### C. Day & Content
- Task list (CRUD)
- Content calendar / queue (LinkedIn-first; extensible)
- Daily generated pack (API-produced markdown posts/hooks) with approve/edit/copy states

### D. Ops
- Invoices (existing)
- URL shortener (existing)
- Telemetry (existing, secondary)
- LMS (existing; keep but demote if not daily-use)

---

## 4. New / extended API contract (implement these)

Auth: all mutating routes `requireAdmin` (same as today). Add a long-lived **agent token** or reuse admin bearer so Personal OS / external AI can POST without browser login (document in `.env.example`).

### Food (new)
- `POST /api/health/food` — `{ date, meals: [{ name, calories, protein, carbs, fats, notes? }], source? }`
- `GET /api/health/food?from=&to=`
- `GET /api/health/food/today` — totals vs targets

### Day tasks (new)
- `GET/POST /api/day/tasks`
- `PATCH /api/day/tasks/:id` — status complete/open
- Shape: `{ id, date, title, type: personal|work|content, priority, status, dueAt? }`

### Content queue (new)
- `GET/POST /api/content/items`
- `PATCH /api/content/items/:id`
- Shape: `{ id, date, channel: linkedin|x|other, title, body, status: draft|ready|posted, source: generated|manual, hooks?[] }`
- `POST /api/content/generate-day` — body optional `{ date, signals: { workouts?, themes? } }` → creates/updates today’s draft pack (stub LLM or rule-based first; wire real model later)

### Ingest (new — for other AI tools / chat instructions)
- `POST /api/ingest` — `{ kind: workout|food|metric|task|content|note, payload, occurredAt? }`  
  Normalize into the right store. Return `{ ok, kind, id }`.

### Oura
- Keep `/health/oura/sync`; optionally cron-friendly `GET` with admin auth for agent morning sync.
- Stop silently falling back to fake scores when token missing: return `{ synced:false, reason }` and show that in UI.

### Persistence
- Prefer one pattern: JSON files under `backend/data/` OR Mongo with JSON mirror — pick one primary, document it, migrate existing paths (`HEALTH_DB_PATH` etc.) without breaking prod.
- Add `backend/data/food_log.json`, `day_tasks.json`, `content_queue.json` (or Mongo collections).

---

## 5. Frontend implementation notes

- Keep dark admin aesthetic; improve consistency (shared card, table, form, chart components).
- Home should be default tab after login.
- Weight chart: use existing metrics history (seed includes 2026-07-21).
- Do not break public portfolio routes or `/s/:code` short links.
- Follow repo pre-flight: local build, summary table of files changed, no drive-by refactors outside Personal OS scope.
- Remove or redact any secrets accidentally committed in docs (see security note below).

---

## 6. Out of scope for v1
- Full Google Calendar two-way sync (show placeholder “calendar blocks” fed by `day/tasks` + optional manual time ranges first)
- Auto-posting to LinkedIn (queue + copy only)
- Rebuilding LMS or public marketing site

---

## 7. Acceptance checks
1. Login → Home shows Oura (or clear unsynced state), weight sparkline, workout today, food vs target, today’s tasks, today’s content drafts.
2. External tool can `POST /api/ingest` workout + food and Home updates after refresh.
3. `POST /api/content/generate-day` creates editable drafts for today.
4. Invoices + shortener still work from Ops.
5. `npm run build` (frontend) succeeds; health routes smoke-tested.

---

## 8. Security note for implementer
`VERSION_LOG.md` currently embeds a recovery-key-looking string in plaintext. Rotate `EMERGENCY_RECOVERY_KEY` / admin secrets in Hostinger env if that file ever shipped, and stop committing secrets into markdown.
