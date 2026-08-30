# Event Validation — Marketing Skill Analytics Checklist

## READ THIS BEFORE ANYTHING ELSE

This is a task to execute immediately using your tools. It is not a document to edit, reformat, review, or summarize back.

**Your deliverable is a filled-in checklist per event**, verified live against PostHog/Customer.io/the site or app — not a description of how you'd check it.

Use the `marketing` skill's `analytics` sub-skill validation framework (`~/.claude/skills/marketing/skills/analytics/SKILL.md`) as your criteria. For every event listed below, check all six:

1. **Firing on the correct trigger** — does it fire when and only when it should, not on unrelated actions?
2. **Properties populating correctly** — are the documented properties actually present and correctly valued, not null/placeholder?
3. **No duplicate events** — is this event, or a near-identical sibling, firing more than once for the same user action?
4. **Works across browsers/platforms** — for web events, check at least two browsers; for app events, check both iOS and Android where applicable.
5. **Conversions recorded correctly** — if this event feeds a conversion/goal anywhere (ads, CIO campaign, revenue reporting), is it counted accurately?
6. **No PII leaking** — does the payload carry anything it shouldn't (raw email, phone, name) given its destination?

### DO NOT
- Do NOT re-validate the ~150 already-confirmed sheet events from the 29 Aug audit. This task is scoped to the NEW findings below only.
- Do NOT guess at any checklist item — pull a real live sample, or check real code/config, for each.
- Do NOT mark something "no action needed" without evidence for all six checklist points.

---

## Media — validate these (found 29–30 Aug, never previously checked)

| Event | Why it needs validation |
|---|---|
| `Loaded a Page` | 22.7M events, second-highest volume in the project, never documented anywhere. Confirm: still needed, or dead legacy tracker safe to formally retire? |
| `Plus Lock` | 1,044,508 PostHog events — directly contradicts an earlier report that it fires "0× to PostHog." Resolve the contradiction: pull a real payload, confirm properties, confirm it's not a duplicate of another lock event. |
| `User Segment` | 2.66M events, firing as recently as 3 days ago — contradicts an earlier "dead, MoEngage-only" claim. Confirm what's actually driving it now. |
| `Modal Clicked` / `Modal Closed` | Undocumented siblings of `Modal Viewed` (3,427 / 61,189 events). Confirm trigger conditions and properties; check they're not double-firing alongside `Modal Viewed`. |
| `Inc42 Onboarding` | 67,192 events — also one of the 5 confirmed PII-leaking GTM tags. Validate specifically for PII (checklist item 6) as top priority. |

## DataLabs — validate these

| Event | Why it needs validation |
|---|---|
| UserGuiding cluster (`guide started`, `guide completed`, `survey shown`, `survey question answer`, `guide button click`, `checklist item trigger`) | ~31,000 combined events, an entire undocumented third-party integration. Confirm triggers and whether this data is actually used anywhere. |
| `Register Lock Interaction` | 421,734 events — likely the real name behind the sheet's vague "Lock Type/Lock Interaction" row. Confirm properties match what that row intends. |
| `Customise Columns Applied` vs `Customize Columns Applied` | Confirm the migration is complete — old spelling should have zero recent volume; if it still fires at all, that's a duplicate-event problem (checklist item 3). |
| `master_agent_query` | Confirm property values (`evidence_density`, `ungrounded_claims`) are populating correctly, not placeholder/null. |

## App — validate these

| Event | Why it needs validation |
|---|---|
| `force_update_shown`, `brief_fallback_shown`, `watchlist_limit_hit`, `locked_feature_tapped`, `rating_prompt_shown`, `article_published` | All confirmed to have ZERO events ever, despite being expected. Confirm with engineering: is the trigger condition simply never met, or is instrumentation missing/broken? This determines the fix. |
| `Application Backgrounded` / `Application Became Active` / `Application Opened` / `Application Installed` | Confirmed duplicate of `app_opened` etc. (same SDK autocapture). Validate checklist item 3 formally and get the product/eng disable decision documented. |

---

## When you're done

Report, per project: a filled checklist (six columns) for every event listed above, with real evidence for each column — not assumptions. Flag anything where you couldn't get evidence for a checklist item, and why.
