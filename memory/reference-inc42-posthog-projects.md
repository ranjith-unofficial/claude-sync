---
name: reference-inc42-posthog-projects
description: INC42 PostHog project IDs (editorial/DataLabs/app) + shared-account switch caveat
metadata: 
  node_type: memory
  type: reference
  originSessionId: d8963308-0bb1-4e90-a221-f2c4311ce0ba
  modified: 2026-08-24T17:04:48.959Z
---

INC42 PostHog projects (EU cloud, org `019552c3-f13d-0000-5857-79eecae29c22`), reachable via the PostHog MCP `exec` tool:

- **53557 — Inc42 | Live** = the **editorial media website** (inc42.com). Articles at `/buzz/<slug>/` and `/features/<slug>/`. Events incl. `Registered`, `Newsletter Subscribed`, `Share`, `Follow`, `Save Story`, `Freewall Lock`, `Plus Subscribed`, `Pro Payment`.
- **66351 — Inc42 Datalabs | Live** = DataLabs. Company profiles at `/company/<slug>`; events incl. `Search Completed`, `Advanced Filter Applied`, `Report Interaction`, `Saved Search Interaction`, `Alert Interaction`, `Ask Interaction`. No `Share` event (referral untracked).
- **146258 — Inc42 App** = the mobile app (events `brief_completed`, `card_viewed`, etc. — see [[project-inc42-launch]]).
- Others: 57482 Inc42 | Stage · 66352 Datalabs | Stage · 71580/84344/128752 D2CX · 128843 Inc42 Events · 177210 D2C Retail Summit.

**These are the "3 PostHog projects that can't see one person"** the One Inc42 strategy names — converging them (canonical Auth0 `distinct_id`) is Horizon-1 spine work. See [[project-inc42-strategy-utkarsh]].

⚠ **Shared account** — the MCP runs as **Prapti (prapti@inc42.com)**, and the active project **switches mid-session** (she uses it live). Always `switch-project` to the one you need, run, then **switch back to where you found it** (leave the session as-is).

⚠ **The mid-session flip is NOT specific to Prapti's login.** On 2026-08-23 the MCP was authenticated as **ranjith.m@inc42.com** and the active project still reverted to 146258 **twice** while querying 66351 — silently, mid-analysis. The tell is a **`<taxonomy_warnings>` block saying known event names "not found in this project"** plus an empty result set; that is a wrong-project error, not a wrong-query error. **Re-`switch-project` and re-run rather than debugging the SQL**, and re-verify the project before any query whose emptiness would be a finding. Only ever query (read); never create insights/dashboards without asking — [[feedback-shared-system-safety]]. No `bq`/`gcloud`/GA4 CLI on the machine, so GA4/BigQuery aren't directly queryable; PostHog undercounts vs GA4 (ad-block/sampling).
