---
name: project-datalabs-weekly-newsletter
description: "Datalabs Weekly automated newsletter review (13 Sep 2026) — bugs found, 7-block redesign, email + WhatsApp Channel plan, unreviewed"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0eab017f-4eae-493c-94d0-914f6845d54e
  modified: 2026-09-13T16:33:14.725Z
---

Reviewed on 13 Sep 2026: content preview artifact 3a899f48, logic artifact 9dc40307, and the Gmail test "[TEST] Datalabs Weekly: $539 Mn Across 14 Deals" (sent 20 Aug, forwarded by the tech lead 31 Aug).

Output: artifact 0482d4e1-96bf-4ba3-8c6b-abe34db79bd1, file ~/ClaudeDocs/inc42/datalabs-weekly/datalabs-weekly-redesign.html. **Not yet reviewed by Ranjith.**

Verified findings:
- Sector chart says Health Tech "$127Mn". Sector values add up to $653.8 Mn against a $539.3 Mn total, so the real figure is $12.7 Mn (the bar length matches too).
- The prior-week comparison ("$4.2 Mn across 6 deals") looks broken, and the label "Aug 13 – Aug 20" covers 8 days.
- The sent test does not match the logic doc: Ecosystem includes funding items, M&A uses 30 days (logic says 90), and the investor, people and financials sections are missing.
- Company links go to inc42.com/buzz, not Datalabs profiles. Personalisation is dormant because there is no `sector` or `icp` on the Customer.io profile.

Proposed: 7 fixed blocks (one number → 3 things → your sector → money → scoreboard → also moving → chart) with one watchlist CTA. Sector is collected through links inside the email.
Channels: email for everyone. A free WhatsApp Channel as the Monday reminder (recommended). WhatsApp 1:1 only for opted-in Datalabs users with no email click in 24h (~₹1.02/msg incl GST).

Open questions: list size and click rate, which build ships, any existing WhatsApp Channel or number, WhatsApp consent on checkout phone numbers, whether reply-to is monitored.

**How to apply:** check this before any further newsletter work, and re-verify the bugs against a fresh test send, since the pipeline may have changed. Related: [[project-inc42-deep-linking]], [[project-inc42-datalabs-winback]], [[reference-inc42-vendor-stack]].
