---
name: feedback-always-include-source-links
description: "Every candidate/record list Ranjith reviews must carry a clickable link back to the source document — he has asked repeatedly and it keeps getting dropped"
metadata:
  type: feedback
---

Any list of records Ranjith is expected to **review** — screened candidates, applicants, articles, companies — must include a **clickable link to the underlying source document** (resume PDF, article, profile). Not the internal ID. Not just the name.

He flagged this on 2026-08-19 after the `Product Trainee Scores` tab shipped with 22 columns of scores and no resume URL, and said explicitly: *"I have mentioned it multiple times. Every single time this is happening."* The existing `PT Calibration` tab already had an `Open resume` column — the pattern was right there and still got dropped.

**Why:** a score he cannot click through to verify is useless. The whole review loop is read the verdict → open the resume → agree or disagree. Without the link the sheet is a dead end and he has to go hunt in Keka.

**How to apply:**
- Put the link **near the identity columns** (right after `name`), not buried at the far right of 20+ columns.
- Make it clickable: `=HYPERLINK("<url>","Open resume")`, matching the label already used in the sheet.
- Keep the raw URL in a plain column too, so the data is still usable when exported to CSV.
- Before delivering ANY reviewable list, check the link column exists and is populated for every row — the URLs were sitting in `pool_eligible.json` the entire time; this was an omission, not a data gap.

Related: [[project-inc42-product-trainee]], [[project-inc42-hiring-agent]], [[feedback-completeness-audits]].
