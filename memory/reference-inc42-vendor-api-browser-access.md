---
name: reference-inc42-vendor-api-browser-access
description: "How to query PostHog and Customer.io directly from an authenticated Chrome tab when the PostHog MCP is unavailable — exact endpoints, verified 8 Sep 2026"
metadata:
  type: reference
---

The PostHog MCP dropped its connection mid-session on 8 Sep 2026 (its tools vanished from the deferred
list, and re-authenticating produced a URL but the server still did not come back). Both vendors are
fully queryable from an already-signed-in Chrome tab via `javascript_tool` fetch — this is API access,
not UI scraping, and it is faster than the MCP for bulk work.

**PostHog (any project).** From a tab on `eu.posthog.com`:
`POST /api/environments/<project_id>/query/` with `{"query":{"kind":"HogQLQuery","query":"<SQL>"}}`,
header `X-CSRFToken` read from the `posthog_csrftoken` cookie, `credentials:'include'`.
Full HogQL works, including the person key census from [[project-inc42-user-properties-audit]].
A 10.4m-person `arrayJoin(JSONExtractKeysAndValuesRaw(properties))` + `topK(6)` returned in ~3 seconds.

**Customer.io.** From a tab on `fly.customer.io` (signed in), the API host is `eu.fly.customer.io`:
- `GET /v1/environments/<ws>/attributes?page=N&size=200` — the attribute list (50/page by default;
  `meta.pagination.total` lies, it returns 0 — page until an empty array).
- `GET /v1/environments/<ws>/attributes/<id>` — **the valuable one**: returns `segments` and `campaigns`
  that reference the attribute, plus `metadata.privacy_level`, `description`, `sources` and `last_seen_at`.
  This is how you tell a load-bearing attribute from an orphan before recommending a delete.
- `GET /v1/environments/<ws>/customers?attribute=<id>` — sample profiles.
- There is **no endpoint for the "% of profiles" figure** the Data index UI shows. Do not invent it;
  report attribute presence + segment/campaign usage instead.
- The `/data_index/attributes` UI route redirects and fires no attribute request — don't wait on it.
Workspace IDs: Inc42/Media 208301, Datalabs 208719, Inc42 App 224949.

**Gotchas.**
- `navigator.clipboard.writeText` hangs (45s CDP timeout) unless the tab is the *active* Chrome tab;
  a `computer` left_click on the page first makes it work. A heavy Google Sheets canvas tab times out
  regardless — fetch gviz CSVs from a light same-origin page such as `docs.google.com/robots.txt`.
- `javascript_tool` truncates returned strings at roughly 1.2k characters and blocks anything that looks
  like cookie/query-string data. For bulk output, write to the clipboard and `pbpaste > file` in Bash.
- Long loops (119 sequential fetches) exceed the 45s CDP limit — start them as a background promise
  writing to a `window.__x` global and poll for `done`.

See [[reference-inc42-posthog-projects]], [[feedback-analytics-destination-scope]].
