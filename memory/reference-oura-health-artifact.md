---
name: reference-oura-health-artifact
description: "Oura \"Health Signals\" dashboard artifact + the daily cloud routine that refreshes it"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 0d31876d-c309-4d9a-a04a-3648f6499b0e
---

Oura Ring dashboard artifact "Health Signals — Ranjith": https://claude.ai/code/artifact/8ca8460d-5faa-4c6b-bc2f-bdc57c123594

Rolling 7-day window of readiness/sleep/activity, biometric tiles, trend chart, workouts, daily log. Themed to ranjith.tech (dark + red grid). Data is a static `const D = {...}` block baked into the page — the artifact CSP blocks all outbound network calls, so it can never self-fetch from Oura, and an in-page "refresh" button is impossible. The footer stamp and date range derive themselves from the data, so a refresh only needs to swap the `const D` line.

Refreshed daily at 7am IST by cloud routine `trig_011xJQU6rrHnEvPE2hkPEXHi` ("Oura Health Signals — daily refresh", cron `30 1 * * *` UTC): https://claude.ai/code/routines/trig_011xJQU6rrHnEvPE2hkPEXHi

**How to refresh on demand:** ask in any session — re-pull Oura API v2 (`daily_readiness`, `daily_sleep`, `daily_activity`, `sleep` filtered to `type == "long_sleep"`, `daily_spo2`, `workout`, `daily_cardiovascular_age`, `personal_info`), rebuild `D`, republish with the Artifact tool passing `url`.

**Caution:** Oura revises the current day's data as it goes — a mid-day pull will undercount steps/calories and settle higher by evening. Don't treat same-day numbers as final.

The Oura personal access token is stored in that routine's config. See [[user-personal]].
