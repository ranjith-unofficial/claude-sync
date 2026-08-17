---
name: reference-doc-generation
description: How to produce PDF/Word deliverables for Ranjith on this Mac (no pandoc/LibreOffice)
metadata: 
  node_type: memory
  type: reference
  originSessionId: 1b85df8c-b255-4a10-9994-1dbcc66c6987
---

Ranjith frequently wants deliverables as **PDF and Word**, not markdown. This Mac has **no pandoc, no LibreOffice, no Word**.

**Working toolchain:**
- **Markdown → HTML**: hand-rolled converter (headings, tables, lists, inline bold/code).
- **HTML → PDF**: headless Chrome —
  `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf=OUT.pdf file://IN.html`
- **Markdown → DOCX**: **`python-docx`** (`pip3 install python-docx`).

**⚠️ Do NOT use `textutil` for DOCX.** It silently **flattens every table** into plain paragraphs — the file opens fine and looks broken. Ranjith caught this. Always verify after generating:
```python
from docx import Document
len(Document(f).tables)   # must be > 0
```

**Also:** copying text out of a *PDF* always flattens tables — that's normal PDF behaviour, not a bug. If he needs to copy content, point him at the DOCX.

**Convention:** keep the `.md` as the editable source, regenerate PDF + DOCX from it, and tell him plainly when the exports are stale relative to the source. Related: [[feedback-communication-style]].
