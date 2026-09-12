---
name: feedback-browser-new-tab-per-task
description: "Create a new Chrome tab for each browser task instead of navigating a tab that is already showing something"
metadata:
  type: feedback
---

On 12 Sep 2026 Ranjith interrupted a `navigate` call that would have reused a Customer.io tab already
showing a profile page, and said: **"Create a new tab and start doing this."**

**Why:** a tab that is displaying a result is his working context. Navigating it away destroys what he
was looking at, and he may be mid-review of it. Tab creation is free; reuse is not.

**How to apply:** call `tabs_create_mcp` for each new browser task rather than re-pointing an existing
tab — especially any tab that is currently rendering a page (a profile, a dashboard, a document) rather
than a blank/robots.txt scratch page. Close only the tabs I created, and leave his open.

A second reason this matters: page-scoped JS state (`window.__x` globals holding a long collection job)
is destroyed by navigation. Reusing a tab mid-job silently loses the data and forces a re-run — that
happened in this session too.

See [[feedback-shared-system-safety]], [[reference-inc42-vendor-api-browser-access]].
