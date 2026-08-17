---
name: feedback-validation-approach
description: "How Ranjith wants validation/QA tasks approached — confirm feasibility first, cross-check against independent ground truth"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 52748f95-69d6-4f09-abf4-4343d28c22c2
---

When Ranjith shares a validation/testing/QA task (e.g. "check if this search endpoint is good enough"), before diving in:

1. **Confirm feasibility first.** Assess and state up front how well I can actually validate/deliver it, and surface the limits of my approach — don't run a narrow check and hand back a falsely confident result.
2. **Think out of the box — use independent ground truth.** Don't just run the provided/curated test list (it's often self-referential and flattering). Cross-validate against an external source of truth.
   - Example he gave: to test the INC42 search endpoint, search real keywords on Google → find real articles in Google results → query those same entities against the INC42 endpoint. If Google proves content exists but the endpoint returns nothing → confirmed bug.

**Why:** A curated 20-query validation of the INC42 search endpoint gave a flattering "18/20 pass," but the query "wagh bakri" (a brand INC42 has fully profiled) returned 0 results — a real recall gap the narrow test missed. Self-referential test sets hide failures; adversarial cross-checks against reality expose them.

**How to apply:** For any "is X good enough?" task, design tests that could actually fail — pull ground truth from outside the system under test, cover the long tail, and report honest limits rather than a rosy pass. Relates to [[project-inc42-launch]] and [[project-inc42-content-personalization]].
