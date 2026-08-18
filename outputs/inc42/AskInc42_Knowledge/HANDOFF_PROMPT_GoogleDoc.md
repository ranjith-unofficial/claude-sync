# Handoff prompt — build the AskInc42 Google Doc with tabs

Paste everything below the line into a session that has **Claude in Chrome** available.

---

## TASK

Create one Google Doc with **9 tabs**, using Claude in Chrome to drive `docs.google.com` directly.

**Document title:** `AskInc42 — Knowledge Set`

**If the Doc already exists** at `https://docs.google.com/document/d/1KhWJP5Q_cS1YH1iG8Y5VV361byEI389oOCaVUyGDvgQ/edit`, update it in place rather than creating a new one — see "IF UPDATING AN EXISTING DOC" below.

## SOURCE CONTENT

Eight markdown files:

```
~/Documents/AskInc42_Knowledge/00_README_Index.md
~/Documents/AskInc42_Knowledge/01_App_Knowledge.md
~/Documents/AskInc42_Knowledge/02_Inc42_Company.md
~/Documents/AskInc42_Knowledge/03_Policies_TnC_Privacy.md
~/Documents/AskInc42_Knowledge/04_IPs_Overview.md
~/Documents/AskInc42_Knowledge/05_Utkarsh_Call_Notes.md
~/Documents/AskInc42_Knowledge/06_Response_Rules.md
~/Documents/AskInc42_Knowledge/07_Decision_Log.md
~/Documents/AskInc42_Knowledge/08_DataLabs.md
```

If you can read local files, read them from these paths.
If you cannot, ask me to paste each file's contents one at a time, and build that tab from what I paste before asking for the next.

DOCX versions exist in `~/Documents/AskInc42_Knowledge/docx/` if importing is easier than typing — but **tabs still have to be created manually**, since no file import creates them.

## TAB STRUCTURE

Create the tabs in this exact order, with these exact names. Google Docs tabs are made from the **left-hand tab panel** (View → Show tabs & outline, then the **+** / "Add tab" control).

| # | Tab name | Source file |
|---|---|---|
| 1 | How to read this | `00_README_Index.md` |
| 2 | App | `01_App_Knowledge.md` |
| 3 | Inc42 | `02_Inc42_Company.md` |
| 4 | IPs | `04_IPs_Overview.md` |
| 5 | DataLabs | `08_DataLabs.md` |
| 6 | Policies — T&C & Privacy | `03_Policies_TnC_Privacy.md` |
| 7 | Response rules | `06_Response_Rules.md` |
| 8 | 🔴 Utkarsh input (internal) | `05_Utkarsh_Call_Notes.md` |
| 9 | 🔴 Decision log (internal) | `07_Decision_Log.md` |

The order differs from the file numbering — IPs and DataLabs come before Policies, and the two internal-only documents go last. Follow the table, not the filenames.

## IF UPDATING AN EXISTING DOC

The Doc already has 8 tabs from a previous transfer. To bring it to 9:

1. **Insert a new tab named `DataLabs` in position 5**, between `IPs` and `Policies — T&C & Privacy`. Tabs 6–9 shift down by one; their names do not change.
2. **Re-transfer these tabs**, whose sources changed: `Inc42` (2 lines rewritten), `Decision log` (renumbered 1–33, new header, a third Utkarsh item added), `How to read this` (new row + source mapping).
3. **Leave untouched:** `App`, `IPs`, `Policies — T&C & Privacy`, `Response rules`, `Utkarsh input`.
4. ⚠️ **Clear each tab and its formatting before re-pasting** (select all, then clear formatting) — pasting into a populated tab inherits the caret's character style. On the previous transfer this turned a whole tab bold and collapsed a table column.

## FORMATTING RULES

Convert markdown into real Google Docs formatting. **Do not paste raw markdown syntax.**

- `#` → Heading 1 · `##` → Heading 2 · `###` → Heading 3 · `####` → Heading 4
- **Markdown tables must become real Google Docs tables**, with the header row bolded and shaded light grey. This matters — most of the content is tabular and it is unreadable as pipes.
- `- ` → bulleted list · `1. ` → numbered list · nested items keep their indent level
- `**bold**` → bold · `*italic*` → italic · `` `code` `` → Courier New
- `> ` → indented italic quote
- `---` → horizontal rule
- Keep every emoji as-is: 🔴 ⚠️ ✅ ❌ ⚙️ — they are severity markers, not decoration
- Keep `~~strikethrough~~` as strikethrough

## HARD RULES — DO NOT BREAK

1. **Do not edit, rewrite, summarise, expand or "improve" any content.** This is a verbatim transfer. Formatting only.
2. **Do not add any pricing anywhere** — no amounts, currency figures, pass tiers, discount codes or seat counts. The source deliberately contains none. If you think something is missing, leave it missing.
3. **Do not merge, split or reorder tabs**, and do not add tabs of your own.
4. **Preserve the 🔴 DO NOT INGEST banners** at the top of tabs 8 and 9 exactly as written. Those two documents must never enter the AskInc42 knowledge base, and the banner is the only thing preventing it.
5. Do not create sub-tabs. Nine top-level tabs only.
6. If a tab fails to paste cleanly, fix that tab before moving on — don't batch and hope.

## WHEN DONE

Reply with:
- The Google Doc share link
- Confirmation that all 9 tabs exist, correctly named and in order
- Confirmation that every markdown table rendered as a real table
- Anything that didn't transfer cleanly

---

## CONTEXT (background only — do not put this in the document)

This is the knowledge scope for **AskInc42**, Inc42's AI assistant. It defines the five approved knowledge sources it answers from, and the boundaries it holds:

- **Pricing** — never stated, always redirected to the relevant website
- **Access model** — free / paid / invite-only *is* answerable, without amounts
- **Eligibility** — published criteria *are* answerable; never a ruling on a specific user
- **Refunds and cancellations** — one line, one destination: Contact Us
- **T&C and Privacy** — high-level summaries only, no clause interpretation
- **Web search** — enabled, but the five sources are authoritative on anything about Inc42's own business

Tabs 2–7 are ingestible knowledge and behaviour rules. Tabs 8 and 9 are internal working documents that must stay out of the knowledge base.
