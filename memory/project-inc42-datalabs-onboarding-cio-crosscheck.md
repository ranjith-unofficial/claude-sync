---
name: project-inc42-datalabs-onboarding-cio-crosscheck
description: "In-progress CIO-vs-PostHog onboarding completion sync cross-check for the DataLabs audit — what's done, what's still open"
metadata: 
  node_type: memory
  type: project
  originSessionId: 89944606-7a76-4026-a114-806b40d5dc68
  modified: 2026-08-29T10:46:02.682Z
---

Mid-task state as of 2026-08-29, DataLabs analytics audit follow-up (session interrupted while building the CIO cross-filter segment).

**The question being answered:** sheet remark claims `datalabs_onboarding_complete` is "99% populated in PostHog but 66% broken in CIO." User explicitly asked for this to be tested against the *same completer cohort* in both platforms, not a mismatched-denominator estimate (an earlier 68%-of-all-CIO-profiles figure was correctly rejected as not answering the same question).

**Done:**
- PostHog side re-verified twice after catching a silent project-context revert (from DataLabs 66351 to the App project 146258 mid-session — re-check project before every query, this bit us once already). Confirmed: of 5,082 unique persons who fired `Datalab Onboarding` with `Datalab Onboarding State = Onboarding Completed` in the last 90 days, 5,033 (99.03%) have person property `Datalabs Onboarding Complete` = Yes. This number is solid, re-run and identical both times.
- Pulled a 2,000-email sample (of the 5,082, ~39%, alphabetically sliced via `ORDER BY email LIMIT 500 OFFSET n`) via PostHog `execute-sql`, wrote to `~/private/tmp/.../scratchpad/posthog_completer_sample.csv` (also `posthog_completer_sample.csv` — check scratchpad, path is session-specific and may be gone).
- Created a Customer.io **manual segment** in the DataLabs workspace (208719): **"[Analysis] PostHog onboarding-completers sample - 29 Aug 2026"**, segment id **24**. Uploaded the 2,000-email CSV by email match. Result: **1,988 of 2,000 matched (99.4%)** to real CIO profiles — itself a notable finding (CIO profile coverage of this cohort is excellent).
- This segment is a temporary analysis artifact, description says "Temporary, safe to delete after review" — should be deleted once the cross-check number is captured, or left for the user to decide.

**Not done — this is the actual blocker:**
- Need to build a second segment/condition: profiles where `Segment in [that id-24 segment]` AND `Datalabs Onboarding Complete = Yes`, then read the resulting profile count. That count ÷ 1,988 (or ÷ whatever the matched total is) is the real CIO-side completion-sync percentage, comparable to PostHog's 99.03%.
- Was actively building this in CIO's segment builder when interrupted. **CIO's data-driven segment builder has a real UI bug**: clicking "Add condition or group" → "Attribute" repeatedly auto-spawns extra phantom trailing condition rows (Page/SMS/SMS/Device/Screen/Event, with valid-looking default values like "any screen has been viewed") that were NOT clicked into existence — they self-generate after every add or delete action. Clicking "Close" on the condition editor resets the whole unsaved condition set to blank (lost partial progress twice this way). Workaround found: select condition-type and attribute-value via `find` + ref-based clicks rather than typing into the attribute search box — typing into that box seems to be what triggers the phantom-row spawn. Was mid-way through this careful ref-click approach (had gotten to selecting "Datalabs Onboarding Complete" via ref_346) when interrupted — should resume from there rather than restarting the whole condition build.
- Once the real percentage is obtained, report it back to the user as the answer to "Item 1" (the CIO-side 66%-broken claim), and note whether it confirms/refutes/partially-confirms the sheet's remark.
- Also still pending from the same conversation: check whether AskInc42 (Inc42 App, PostHog project 146258) has an equivalent backend query-classification event to DataLabs' `master_agent_query` (2,359 events/90d, PostHog-only, undocumented — carries quality signals like `evidence_density`/`ungrounded_claims`). User asked for this explicitly and flagged it as worth prioritizing into the master sheet ahead of routine cleanup items. Not started.

**Where the deliverables live:**
- Sheet `1n6r5QXe-9Pq1uAWMKRe7zSgLHSejASzAq-BAqeI3L6Y`, tabs "Datalabs Audit - 2026-08-29" (46 rows, fully filled incl. PostHog Y/N+volume) and "Datalabs - New Events Found" (3 rows incl. master_agent_query) — these are already complete and correct, not blocked on the above.
- Sibling App/Media audit tabs (other concurrent agents' work) were read-only row-count-verified and matched expectations: App Audit 55✓, App New Events 11 (expected ~10, close), Media Audit 37✓, Media New Events 12✓.

See also [[project-inc42-datalabs-onboarding-cio-crosscheck]] (this file), [[project-inc42-content-personalization]], [[reference-inc42-posthog-projects]].
