---
name: feedback-measure-field-coverage-before-designing
description: Before designing any slot that depends on a data field, measure that field's coverage in the real corpus; a slot may only promise what its field delivers on ≥85% of days, and must never announce its own absence
metadata:
  type: feedback
---

Ranjith rejected three consecutive Brief entry rounds on 4–5 Sep 2026 (rows C, D, E) because
each assumed a field was always present. Measured afterwards on the 809-article corpus:
27% of articles have **no company**, 5% have two, sector is missing on 24% after roll-up,
AI has zero articles on 50% of weekdays, 23% of days have fewer than 8 stories.
His words: "you cannot say you don't have anything in AI today… not every card necessarily
needs to have a company attached… you have the entire data with you."

**Why:** the corpus is fully available (WP REST `structure_data`, the tagging-audit workbook,
`summaries.json`), so any assumption about coverage is a choice not to look. A design that
renders only on cooperative days is not a design.

**How to apply:** before building a slot, run the coverage query. Gate every slot with an
explicit rule (`render if field present`, `hide if ladder empty`). Never render an empty-state
that names a followed thing. Backtest the shell across all publishing days and report render
rates per slot. Build screens on **real days** picked for their edge cases (heaviest, thinnest,
zero-match, no-company), not on invented content. See [[project-inc42-brief-entry-coverage]]
and [[feedback-ui-mockup-research-first]].
