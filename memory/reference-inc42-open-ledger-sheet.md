---
name: reference-inc42-open-ledger-sheet
description: "The INC42 master task ledger now also lives as a Google Sheet tab, not just the local CSV — location, and a caution about an adjacent tab's name"
metadata:
  type: reference
  originSessionId: 1c442aa8-439c-4822-95e9-3864030f3bbb
  modified: 2026-08-29T07:46:43.121Z
---

The master open-items ledger (`~/ClaudeDocs/inc42/inc42-open-ledger-MASTER.csv`, ~178 rows, sections A-P) was, until 27 Aug 2026, a local-file-only tracker. Ranjith asked for it to also live in Google Sheets.

**Location:** a new tab named **"Open Ledger (27 Aug)"** inside the spreadsheet titled **"Test"** at `https://docs.google.com/spreadsheets/d/1NCpTEzgEEtds0uCfqPNSS6aeFhOpKbgkL_F-cgtVPxg` (gid `875381206` for this tab specifically). This is the same workbook that already holds the **App V2 Roadmap**, **App - Funnel Diagnostics**, **Dunning System**, and **Dunning - Simple** tabs — i.e. it's the team's general working spreadsheet, not a dedicated ledger file.

**Caution:** while creating this tab, an adjacent pre-existing, apparently-never-named tab got briefly (and accidentally) relabeled, then renamed to a best-guess **"DataLabs & Other"** based on its visible content (a DataLabs/Razorpay/Sep-MOP funnel-diagnostics table matching the second sheet of `inc42-app-v2-friction-sheet.xlsx`). Its data was never altered, only the tab name was ever in question, and only briefly — but if that tab's *original* name mattered to someone, "DataLabs & Other" is a reconstruction, not a confirmed original.

**Why:** the CSV and the Sheet are now two copies of the same 27 Aug snapshot — they will drift unless both are updated together going forward.

**How to apply:** when updating the open ledger, update both the local CSV and this Sheet tab (or confirm with Ranjith which one he now treats as canonical, since duplicated sources of truth tend to only get one of them updated in practice).
