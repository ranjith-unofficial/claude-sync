---
name: project-daily-signal
description: "Daily personal intelligence briefing artifact ('Daily Signal') — full 20-section exec-report format, calendar-strip UI, cloud-scheduled, push-notified"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6359b600-48ff-414f-93bc-75b5a1066c87
  modified: 2026-08-03T14:41:24.317Z
---

Ranjith is building a personal daily AI/product/geopolitics intelligence briefing, separate from [[project-personal-ai-ops]] (which only covers email/Slack triage — he explicitly called that "very basic"). Delivered as a self-updating Artifact (calendar-strip UI, one entry per date) at https://claude.ai/code/artifact/3827154b-c3ee-43eb-8b50-0044434a8355, redeployed daily by a scheduled cloud agent. Notification method is a push notification, not email — the Gmail MCP connection here can only create drafts, not send, so automated email wasn't viable.

**Format decision (2026-08-03):** started from a simple 4-category test (AI News / Product Decisions / Breakdowns / Wildcard) that worked well and matched his original stated constraint ("cannot see myself reading a 15-page document"). He then shared a 20-section "Chief Intelligence Officer" ChatGPT prompt (Bloomberg-terminal/McKinsey-report depth: per-company AI industry analysis, one product reverse-engineered daily, startup radar, geopolitics across 10 regions, decision labs, research paper breakdowns, etc.). After being warned this directly contradicts his own "not a 15-page doc" constraint and won't be a quick daily read, he explicitly chose the full 20-section version anyway.

**Why:** the original trigger for this whole project was wanting real depth on *why* product/AI decisions get made — not headlines. He confirmed the heavier format knowingly, after the tradeoff was flagged, not by default.

**Scheduling (2026-08-02, ~7:53pm IST):** stopped the local fork mid-run because he flagged Claude credits running low. Set up two cloud routines instead — RemoteTrigger `trig_01HyMvAijkZMk53XnKq4XLXE` (recurring daily, first fires 2026-08-03) and `trig_01AdkgHaBQdUJSSzG4dyMz1V` (one-off catch-up, ran ~8:53pm IST same night). Both use claude-sonnet-5, no repo, WebFetch/WebSearch/Artifact/PushNotification only.

**Schedule changed (2026-08-03):** moved from 9:00 AM IST to **6:30 AM IST**, per explicit request. `trig_01HyMvAijkZMk53XnKq4XLXE` cron is now `0 1 * * *` (1:00 AM UTC = 6:30 AM IST), trigger renamed to "Daily Signal - recurring 6:30am IST". Next fire confirmed 2026-08-04 ~6:30 AM IST.

**Known fragility:** each run recovers prior days' data by WebFetching the published artifact and asking it to return the `briefings` JS object verbatim — WebFetch actually summarizes via a small model rather than returning raw source, so exact fidelity across many days isn't guaranteed. History is capped at the last 14 days for this reason. If entries start going missing or garbled, this recovery step is the likely cause — worth moving to a real backing store if it becomes a problem.

**How to apply:** when resuming this work, the target format is the full 20-section structure (exec summary → AI industry per-company → product launches → one product reverse-engineered → startup radar → pattern of the day → engineering-for-PMs → research paper → founder wisdom → decision of the day → metric of the day → design critique → AI workflow → geopolitics → reading queue → decision lab → learning corner → questions to think about → action items → closing "one insight"), not the simpler 4-tab version. Sections framed as "pick one X" (reverse-engineering, founder wisdom, research paper, pattern, metric, design critique) are meant to rotate topics daily rather than require fresh news. Sections needing genuine daily news (exec summary, AI industry, product launches, startup radar, geopolitics) should state plainly when nothing notable happened that day rather than padding with filler — don't manufacture content to hit the section count.
