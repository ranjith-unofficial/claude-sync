---
name: project-inc42-brief-title-per-article-copy
description: "Per-article generated brief card copy + push title/body (13 Sep 2026) — CMS generates on publish/schedule, editable, API fallback to article title, Customer.io sync; tab 'Brief Title' in Master PRD Copy"
metadata: 
  node_type: memory
  type: project
  originSessionId: 089689b3-9104-4ca6-9ce2-216277f228c3
  modified: 2026-09-12T21:53:11.071Z
---

Verified 13 Sep 2026. Came from Ranjith's call with Utkarsh (~12-13 Sep) plus follow-up decisions in chat.

**Doc:** Master PRD Copy `13vNB88le_0-mOGv3nueRJEQOUfrLVYIujBWLGAj6qow`, tab **"Brief Title"** (`tab=t.xz87uin8g5v0`), under 1.1 Brief after "Brief Page - Structure". Created 13 Sep. Decisions log (0.1) NOT yet updated.

**Utkarsh's decoupling (meeting):** new backend field = primary, article title = fallback. App ships the fallback in the 15 Sep build (Ritvik) with no dependency on generation; generation + editorial loop is a separate CMS track (Anmol) after release. Slack "pick 1/2/3" editor loop parked for later. No feature flag (Ranjith: bandwidth).

**Locked rules (Ranjith, 13 Sep):**
- 3 fields generated together: brief card copy, push title, push body. On publish AND on schedule.
- Generation fail: push title = article title; push body = empty.
- Editors can edit any field in CMS anytime.
- Article title/content edited after publish → regenerate all 3 (overwrites editor edits).
- Empty brief card copy → app shows article title (Ritvik handles; blank = missing).
- Every copy change syncs to Customer.io.

**Open (in the tab §8):** does article push start from CIO `article_published` event or manual; does editing a field itself trigger regen (recommended no); regen age window; is brief card copy sent to CIO; overlap with older tab "Brief: Title + Image Generation" (27 Jul draft, per-sector daily title/push set) — which one sends the push.

**Unresolved design tension:** Ranjith wants a question-led brief card UI (with Satya), but at launch the fallback means plain headlines render in it.

Related: [[project-inc42-brief-copy-variants]], [[project-inc42-brief-impact-continuity]], [[reference-inc42-master-prd-skill]]
