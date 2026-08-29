---
name: reference-inc42-keka-api-access
description: "Direct Keka Hire API credentials and how to use them, found in Ranjith's n8n workflow export"
metadata: 
  node_type: memory
  type: reference
  originSessionId: a44f396b-c24a-49ef-8e79-300e18498cf8
  modified: 2026-08-28T13:20:19.387Z
---

Ranjith has a working Keka Hire API OAuth client, sitting in plaintext inside the n8n workflow export at `~/Downloads/hiring-agent-workflow.json` (also `~/Documents/hiring-agent-workflow1.json`), in the `Workflow Config` node: `kekaSubdomain` (inc42), `kekaClientId`, `kekaClientSecret`, `kekaApiKey`.

**Auth flow (confirmed working 2026-08-27):**
```
POST https://login.keka.com/connect/token
Content-Type: application/x-www-form-urlencoded
grant_type=kekaapi&scope=kekaapi&client_id=...&client_secret=...&api_key=...
```
Returns a Bearer token, `expires_in: 86400` (24h).

**Endpoints confirmed live:**
- `GET https://inc42.keka.com/api/v1/hire/jobs?pageSize=50` — lists all jobs with GUIDs (e.g. Product Trainee = `a21660ea-028d-40d4-a4b7-707d6523cf6f`, matches the GUID already recorded in [[project-inc42-product-trainee]]).
- `GET https://inc42.keka.com/api/v1/hire/jobs/{jobId}/candidates?pageSize=200&pageNumber=N` — full structured candidate data (name, email, phone, education, experienceDetails with dates, skills, `additionalCandidateDetails` incl. current/expected CTC and self-reported experience, `jobApplicationDetails`). pageSize 200 works; totalRecords/totalPages returned for pagination.
- `GET https://inc42.keka.com/api/v1/hire/jobs/candidate/{candidateId}/resume` — returns a `fileUrl`, but it's an Azure-blob **SAS-signed URL that expires in a few hours**. Not durable enough to paste into a spreadsheet.

**Why this matters:** this bypasses needing browser automation or n8n API calls entirely for any future Keka data pull — straight `curl` + Bearer token from Bash. Confirmed working end-to-end pulling all 731 Product Trainee candidates in ~5 API calls total (vs. hundreds of browser interactions).

**For a durable "resume link" in a sheet, use the permanent candidate profile URL instead of the resume fileUrl:**
`https://inc42.keka.com/#/hire/candidate/job/{jobId}/{candidateId}/summary` — works while logged into Keka in the browser, shows the resume embedded, never expires.

**How to apply:** before reaching for Keka's Excel-export UI or browser automation for any hiring-data task, check this file first and just hit the API directly.

**Security note (already flagged in [[project-inc42-hiring-agent]]):** these are live production credentials sitting in plaintext in a Downloads-folder file. Treat as sensitive — don't paste into chat, artifacts, or anywhere outside local Bash calls.
