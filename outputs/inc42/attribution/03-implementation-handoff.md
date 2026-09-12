# Attribution — implementation handoff for Dev

**Owner:** Ranjith M · **Status:** ready for dev review · **Date:** 12 September 2026
**Read with:** `01-tracking-app-installation-source.md` (install contract) · `02-tracking-app-open-source.md` (session contract) · `app-attribution-source-mapping-spec.md` §6 (in-app nav contract)
**Verified:** PostHog project 146258 live query, 30d to 12 Sep 2026 · Singular React Native SDK + Internal BI Postback docs, fetched 12 Sep 2026

---

## 1. The three questions, and the one property that answers each

| Ranjith's question | Property | Scope | Written by |
|---|---|---|---|
| How many opened via notification / organic / someone's shared link? | `entry_channel` | once per session, auto-attached to **every** event in it | app client |
| How did they get from this screen to that screen? | `referrer_screen` | per event | app client |
| Did this user come from paid or organic? | `attribution_source` + `attribution_is_organic` | once per install, immutable | **Singular server postback**, not the app |

**Never put two of these in one field.** Today `app_opened.source` holds `organic`/`deeplink` while `article_opened.source` holds `explore`/`brief_card` — two layers, one field name, which is why neither question can be answered now.

---

## 2. "How do I know the article was opened from a push vs from a brief card?"

Same event, `article_opened`. The answer is **`referrer_screen`**, and it must carry external-entry values, not just in-app screens — otherwise the push case is a null and you need a join to interpret it.

### 2.1 Decision: `referrer_screen` includes three external values

| Group | Values |
|---|---|
| In-app screens (exist today as `source`) | `brief_card` · `brief_end` · `explore_articles` · `explore_companies` · `search` · `watchlist` · `company_page` · `sector_landing` · `article_reader` · `profile` · `streak` · `tab_bar` |
| **External entry (new)** | `push` · `deeplink` · `deferred_link` |

Rule for the client: on cold start, seed `last_screen` to `push` / `deeplink` / `deferred_link` (matching `entry_channel`). The first in-app event of that session then reports the external origin, and every later event reports a real screen. Result: **one breakdown of `article_opened` by `referrer_screen` is complete and mutually exclusive, with no nulls.**

### 2.2 The five ways an article can open — exactly what each event looks like

| # | How the user got there | `entry_channel` | `referrer_screen` |
|---|---|---|---|
| 1 | Tapped a story on a brief card | `organic` | `brief_card` |
| 2 | Tapped a push straight into the story | `push` | `push` |
| 3 | Tapped a WhatsApp link from a friend, app installed | `deeplink_share` | `deeplink` |
| 4 | Installed from that link, lands on the story after onboarding | `deeplink_share` + `entry_is_deferred=true` | `deferred_link` |
| 5 | Opened app organically, then tapped a newsletter link an hour later in-session | `organic` (session started organic) | `deeplink` |

```jsonc
// 2 — push straight into a story
{ "event": "article_opened",
  "properties": {
    "story_id": "1284412",
    "referrer_screen": "push",          // ← how they reached THIS screen
    "entry_channel": "push",            // ← how the session started (super property)
    "entry_campaign": "brief-8am-12sep",
    "entry_destination": "article",
    "push_type": "brief",
    "notif_id": "cio_01J8...",
    "$session_id": "0192f..."
}}

// 1 — same screen, from a brief card, in an organic session
{ "event": "article_opened",
  "properties": {
    "story_id": "1284412",
    "referrer_screen": "brief_card",
    "referrer_position": 3,             // 3rd card in the brief
    "entry_channel": "organic",
    "$session_id": "0192f..."
}}
```

Case 5 is why the two properties must both exist: the *session* was organic, the *tap* was a link. One field cannot say both.

### 2.3 What is already working vs blind (live, 30d)

| Event | State |
|---|---|
| `article_opened` | origin already populated: explore 1,100 · brief_card 831 · deeplink 812 · article_reader 137 · search 102 · company_page 80 · sector_landing 21 · watchlist 13. **This is a rename to `referrer_screen`, not new work** |
| `company_profile_viewed` | works, but enum drift: `companies` 49 **and** `companies_directory` 13 — pick one |
| `story_shared` | enum drift: `article_reader` 148 **and** `article` 1 — pick one |
| `explore_viewed` (9,120) · `watchlist_viewed` (2,056) · `search_result_tapped` (330) | **no origin property at all** — add |
| `push_opened` | **does not exist in the project.** Case 2 above is unmeasurable until it does |

---

## 3. How Singular actually tells PostHog — the mechanics

**There are two separate channels, and they do different jobs. This is the part that matters.**

### 3.1 The hard constraint (verified in Singular's SDK docs, 12 Sep 2026)

The React Native SDK's methods reference exposes `setCustomUserId`, `unsetCustomUserId`, `setDeviceCustomUserId`, `setGlobalProperty`, `getGlobalProperties`, `event`, `handlePushNotification` (iOS only), `limitDataSharing`. **There is no method that returns install attribution — no network, no campaign, no `is_organic` — on the device.**

Therefore: **paid vs organic cannot be read in the app. It can only arrive from Singular's server.** Any plan that says "read attribution from the SDK on open" is not buildable.

### 3.2 Channel 1 — client SDK, instant, links only

`withSingularLink` / the `SingularLinkHandler` event fires **only when the app is opened through a Singular Link**, and hands back:

| Callback field | Use |
|---|---|
| `params.deeplink` | destination → `entry_destination`, `entry_entity_id` |
| `params.passthrough` | our own params we put on the link → `entry_source`, `entry_campaign`, `share_id` |
| `params.isDeferred` | `entry_is_deferred` |
| `params.urlParameters` | raw query params → fallback parse |

```js
// Expo / RN 0.76+ New Architecture
const emitter = new NativeEventEmitter(NativeSingular);
emitter.addListener('SingularLinkHandler', (params) => {
  resolveEntryAttribution({
    channel:    channelFromPassthrough(params.passthrough),  // deeplink_email | deeplink_share | deeplink_paid
    campaign:   params.passthrough?.campaign,
    shareId:    params.passthrough?.share_id,
    deferred:   params.isDeferred,
    destination: parseDeeplink(params.deeplink),
  });
});
```

Android also requires `SingularBridgeModule.onNewIntent(intent)` in `MainActivity.onNewIntent` or warm-start links are silently dropped. iOS must use **universal links** — URI-scheme deep links are not supported for this.

**What Channel 1 gives you:** everything about links *we* build — campaign, channel, share id, destination, deferred flag. Immediately, client-side, no server.
**What it does not give you:** paid vs organic for an install that came from an ad we don't control the link params for.

### 3.3 Channel 2 — server postback, the only route for paid vs organic

Singular **Internal BI Postbacks** send real-time server-to-server notifications on **installs, re-engagements and in-app events**, configured on Singular's Partner Configuration page. Fields include the standardised attribution set (`is_organic`, `campaign`, network/source, platform, timestamps).

```
Singular  --POST-->  our endpoint  --POST-->  PostHog Capture API
```

```js
// our endpoint (one small serverless function)
app.post('/singular/postback', async (req, res) => {
  const p = req.query;                       // Singular sends macros as query params
  await fetch('https://eu.i.posthog.com/capture/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      api_key: POSTHOG_PROJECT_KEY,
      event: 'install_attributed',
      distinct_id: p.custom_user_id,         // ← THE JOIN KEY, see 3.4
      properties: {
        resolve_latency_ms: Date.now() - Number(p.install_ts) * 1000,
        $set_once: {
          attribution_state:      'resolved',
          attribution_is_organic: p.is_organic === 'true',
          attribution_source:     p.source || p.network,
          attribution_campaign:   p.campaign,
          attribution_network:    p.network,
          attribution_install_at: p.install_ts,
        },
      },
    }),
  });
  res.sendStatus(200);
});
```

Use `$set_once`, never `$set`, so a later re-engagement postback cannot rewrite the install source.
**Confirm the exact macro names in Singular's Partner Configuration UI before coding** — the macro list is behind the console, and the names above are the shape, not gospel.

### 3.4 The join key — the single most likely thing to be skipped

Singular's postback is useless to PostHog unless it carries an id PostHog can resolve to a person.

```js
// first launch, BEFORE Singular.init
const installId = await AsyncStorage.getItem('install_id')
  ?? posthog.getDistinctId();               // PostHog's anonymous id
await AsyncStorage.setItem('install_id', installId);

NativeSingular.init({ apikey, secret, customUserId: installId });
posthog.register({ install_id: installId }); // for debugging the join
```

Why the anonymous distinct_id works: after the user logs in and PostHog merges the anonymous id into the identified person, **the anonymous id remains a valid distinct_id for that person** — so a postback arriving with it still `$set`s the right person, before or after login.

| Rule | Why |
|---|---|
| Persist `install_id` and never regenerate it | a new id = an orphaned postback = a person with no attribution |
| Never call `posthog.reset()` outside of an explicit sign-out-and-switch-user flow | it rotates the anonymous id and breaks the join for every pending postback |
| Add `Singular.setCustomUserId(user_id)` **after login** for Singular's own reporting | the install postback has already fired with `install_id` and still resolves |
| Include `install_id` in the postback macro config | if it is not in the URL template, nothing downstream works |

### 3.5 Division of labour

| Job | Channel 1 (client SDK) | Channel 2 (server postback) |
|---|---|---|
| Paid vs organic | ✗ impossible | ✓ **only source** |
| Campaign for our own links (push, newsletter, share) | ✓ instant | ✓ redundant |
| Deferred destination after install | ✓ | ✗ |
| Latency | ~1,500 ms in-session | seconds to minutes, out of band |
| Blocks the UI | yes (timeout-bounded) | no |

Build **both**. Channel 1 answers "how did this session start" for everything marketing sends. Channel 2 answers "was this user bought or earned".

---

## 4. Marketing's brief-card-story links — the taxonomy they need

Marketing wants to open a story directly. Every such link must be a **Singular Link** carrying passthrough params, or the entry arrives blind (today: 718 of 1,198 `deep_link_opened` events have no campaign at all).

| Use case | Link type | Passthrough params marketing sets | Lands in PostHog as |
|---|---|---|---|
| Push → story | Customer.io push payload (no Singular needed) | `push_type`, `notif_id`, `campaign`, `story_id` | `entry_channel=push`, `referrer_screen=push` |
| Newsletter → story | Singular Link, **not** the Customer.io click-tracker | `source=customer_io`, `medium=email`, `campaign=<send>`, `story_id` | `entry_channel=deeplink_email` |
| WhatsApp / LinkedIn post by Inc42 | Singular Link | `source=whatsapp\|linkedin`, `medium=social`, `campaign` | `entry_channel=deeplink_social` |
| User shares a story from the app | Singular Link minted in-app | `source=inc42_app`, `medium=app_share`, `share_id`, `story_id` | `entry_channel=deeplink_share` + `share_id` |
| Paid ad → story | Singular Link | Singular campaign fields + `story_id` | `entry_channel=deeplink_paid` |
| Offline / QR | Singular Link | `source=offline_qr`, `campaign=<event>` | `entry_channel=deeplink_web` |

Two configuration jobs that are not app code and will otherwise silently break everything above:

1. **Put `utm_source` / `utm_medium` / `utm_campaign` into each Singular link's Google Play referrer parameters** — without it the Play Install Referrer comes back empty and install campaign is resolvable only inside Singular.
2. **Stop routing newsletter links through the Customer.io click-tracker.** It is already the diagnosed cause of the deep-link failure (newsletter links open Safari, not the app) and it strips attribution. One change fixes both.

---

## 5. Build order

| # | Task | Done when |
|---|---|---|
| 0 | Lock the naming convention (`attribution_*` / `entry_*` / `referrer_*`) and mark the losing draft superseded | one convention in the repo and in the Master Sheet |
| 1 | Guard `deep_link_opened`: fire only on cold/background entry, from an owned public domain, never the auth callback | `campaign=auth_callback` returns 0 rows (today 462/1,198 = 38.6%) |
| 2 | Route dev builds off project 146258 | no `192.168.x.x` destinations in production |
| 3 | Make `push_opened` exist | non-zero, and cross-checks against Customer.io send volume |
| 4 | `install_id` + `Singular.setCustomUserId` wiring (§3.4) | `install_id` present on every person; survives login |
| 5 | Channel 1: `SingularLinkHandler` → `resolveEntryAttribution()` → `posthog.register({entry_*})` | QA matrix in `02-…` §5 passes, **including the leakage test** |
| 6 | Delay `app_opened` behind the 1,500 ms resolver timeout | `entry_channel` non-null on ~100% of events; open volume stays ~5,700/30d |
| 7 | Channel 2: postback endpoint → PostHog `$set_once` | `attribution_is_organic` populated for >90% of new installs; `install_attributed` fires once per install |
| 8 | Rename `source` → `referrer_screen` on the 7 events that have it, add it to the 3 that don't, add the 3 external values | `referrer_screen` never contains `organic`; `explore_viewed` / `watchlist_viewed` / `search_result_tapped` >95% populated |
| 9 | `share_id` minted into shared URLs + read back | a `story_shared` event is joinable to the sessions it produced |

Items 1–3 are independent bug fixes with no schema decision — they can ship first, and **every external number stays wrong until item 1 lands**.

---

## 6. Two questions only Ranjith can answer

1. **Dual-write or break?** Item 8 makes `article_opened` / `brief_page_opened` history un-joinable across the release. Dual-write `source` + `referrer_screen` for one version, or accept the break?
2. **Does `entry_*` need to reach Customer.io?** Super properties are a PostHog-SDK mechanism — they will **not** appear on Customer.io events automatically. If lifecycle campaigns need entry channel, it must be passed explicitly per call.

---

## 7. Sources

- [React Native SDK — Supporting Deep Links](https://support.singular.net/hc/en-us/articles/360038415972-React-Native-SDK-Supporting-Deep-Links)
- [React Native SDK — Methods Reference](https://support.singular.net/hc/en-us/articles/36951965777051-React-Native-SDK-SDK-Methods-Reference)
- [React Native SDK — Setting a User ID](https://support.singular.net/hc/en-us/articles/36069107481243-React-Native-SDK-Setting-a-User-ID)
- [Internal BI Postbacks: FAQ and Troubleshooting](https://support.singular.net/hc/en-us/articles/360038040791-Internal-BI-Postbacks-FAQ-and-Troubleshooting)
- [Internal BI Postbacks from Self-Attributed Networks: Field Mapping](https://support.singular.net/hc/en-us/articles/360053015771-Internal-BI-Postbacks-from-Self-Attributed-Networks-Field-Mapping-and-Examples)
- [How to Configure Deep Links](https://support.singular.net/hc/en-us/articles/360050910891-How-to-Configure-Deep-Links)
