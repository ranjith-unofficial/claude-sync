---
name: feedback-analytics-destination-scope
description: "For Inc42 analytics event status/validation work, only PostHog and Customer.io count as real destinations — ignore Mixpanel, MoEngage, GA4, Meta/Google/LinkedIn Ads, UserGuiding when judging whether an event is 'working'"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9806e46d-71a9-4068-9df4-aa66c5b57e7f
  modified: 2026-08-30T13:47:35.341Z
---

Ranjith's exact words: "You talk about only those events which are part of PostHog, nothing else. If it is sending to MoEngage or Mixpanel, we should completely ignore that. I mean posthog and customer io."

**Rule:** when reporting an event's status (firing correctly / broken / missing), score it only against PostHog and Customer.io. Every sheet row's "Destination" column also lists Mixpanel, MoEngage, GA4, Meta Ads, Google Ads, LinkedIn Ads, UserGuiding — this is legacy documentation clutter, not a real destination list. Per [[reference-inc42-vendor-stack]], MoEngage is removed and Mixpanel was never authorized (and is now the subject of a live PII-incident investigation, [[project-inc42-mixpanel-legacy-finding]]).

**Exception:** Mixpanel work under the PII-incident thread itself is a different question ("should this vendor even receive data at all") — that stays in scope, it's just not part of "is this event tracking working."

**How to apply:** every future per-event audit/validation table for App/Media/DataLabs should show only "Live in PostHog?" and "Live in Customer.io?" columns — drop any Mixpanel/MoEngage/GA4/Ads/UserGuiding status columns entirely, even if the source sheet documents those as intended destinations.
