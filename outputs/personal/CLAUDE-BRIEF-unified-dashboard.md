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
- **Day board:** Must close today (tasks) · **Google Calendar sync** (real calendar blocks on Today) · Content queue for today
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
- LMS (existing; **must keep working exactly as today** — no rebuild, no behavior change)

---

## 4. New / extended API contract (implement these)

Auth: all mutating routes `requireAdmin` (same as today). **v1: keep bearer** (harden; no httpOnly JWT cookie this pass). Add **revocable scoped agent API keys** (hashed at rest) for Personal OS / external AI POSTs without browser login (document in `.env.example`). Stop storing raw passcode in `localStorage`.

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


### Google Calendar (new — in scope)
- OAuth with Google Calendar (server-side tokens in env/secure store only — never in GitHub).
- `GET /api/calendar/today` and `GET /api/calendar/range?from=&to=` (auth required) → events for Today board.
- Read sync required for v1; write-back optional later.

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

## 6. Scope adjustments (15 Sep 2026)
- **Google Calendar sync: IN SCOPE for v1.** Show real calendar events on Today / Day board (read from Google Calendar; write-back optional later if easy, but at least reliable read sync).
- **Auto-posting to LinkedIn: still OUT of scope** (queue + copy / approve only).
- **LMS: keep existing LMS working the same way.** Do not rebuild or demote behavior; leave `/l/m/s/*` and LMS admin flows intact. Only fold navigation into the unified shell if needed.
- Public marketing/portfolio site: do not rebuild.

---

## 7. Acceptance checks
1. Login → Home shows Oura (or clear unsynced state), weight sparkline, workout today, food vs target, today’s tasks, today’s content drafts.
2. External tool can `POST /api/ingest` workout + food and Home updates after refresh.
3. `POST /api/content/generate-day` creates editable drafts for today.
4. Invoices + shortener still work from Ops.
5. Google Calendar events appear on Today (synced).
6. Existing LMS student/teacher/admin flows still work unchanged.
7. `npm run build` (frontend) succeeds; health routes smoke-tested.
8. **Security gates before merge/deploy:** no secrets in repo; **bearer admin auth hardened** (rate limit, CORS, no passcode in localStorage) + revocable scoped agent keys; unauthenticated mutating/private routes fail closed; burned recovery key rotated in Hostinger and scrubbed from docs. JWT httpOnly cookie deferred until prod API is same-origin with admin UI.

---

## 8. Security hardening (non-negotiable — 15 Sep 2026)

Fold into Claude build **before any public deploy**. Auth is the real gate; obscure admin path is not enough.

**Auth decision (15 Sep, Ranjith via CoS):** Keep bearer for v1; harden around it. Do not switch to httpOnly JWT cookie in this pass.

### Absolute rules
1. **Never commit secrets to GitHub** (not even a private repo as the long-term store). No tokens in source, `VERSION_LOG`, README, client JS, or zip artifacts.
2. Secrets live only in **Hostinger/server env** (or a secrets manager): `ADMIN_PASSCODE`, `EMERGENCY_RECOVERY_KEY`, `OURA_PERSONAL_ACCESS_TOKEN`, `JWT_SECRET` / signing keys, agent API keys, Mongo URI if any.
3. **Rotate now:** recovery-key-looking string was previously in `VERSION_LOG.md` — treat as burned; set new env values; scrub git history if it was pushed.
4. Admin + all mutating APIs: **auth required**. **v1 auth model (locked):** keep **Authorization Bearer** after passcode login (do not store raw passcode in localStorage — store a server-issued bearer/session token only) + **separate long-lived agent API keys** (hashed at rest, prefix-visible only, revocable, scoped). **JWT httpOnly cookie deferred** until prod `/api/*` is same-origin with the admin UI.
5. Public portfolio stays public; `/sys-admin-*` must not be guessable-only security (obscurity ≠ auth). Keep obscure path but **auth is the real gate**.
6. Rate limit login + ingest; lockout after N fails; constant-time compare; helmet, CORS allowlist (`ranjith.tech` only), no `origin: true` in prod.
7. TLS only (HTTPS). No admin over plain HTTP.
8. Agent ingest keys: one key per tool/agent, scoped permissions (food/workout/content), rotatable, logged.
9. Do not return fake Oura scores that look real when unsynced — don’t leak whether token exists via verbose errors either.
10. `.env` in `.gitignore`; ship `.env.example` with empty placeholders only.



### Auth v1 decision (15 Sep 2026 — locked)
**Keep bearer token for v1; harden around it.** Do not switch to httpOnly JWT cookie in this pass (lockout risk if API and static site differ by origin). Still required now: rate limits, CORS allowlist, no raw passcode in localStorage, env-only secrets, hashed revocable scoped agent keys. JWT/cookie = follow-up once prod `/api/*` is same-origin with admin UI.

### Implementer checklist
- Scrub any plaintext secrets from docs/history; rotate Hostinger env for burned values.
- Harden bearer admin auth (no raw passcode in localStorage); hashed, scoped, revocable agent keys for `/api/ingest` and mutating agent routes.
- Rate limit + lockout on login and ingest; helmet + strict CORS in prod.
- Do **not** migrate to JWT httpOnly cookies in this v1 pass.
- Confirm back to Ranjith in Personal OS chat when coded.
