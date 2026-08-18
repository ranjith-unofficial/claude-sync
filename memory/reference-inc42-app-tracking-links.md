---
name: reference-inc42-app-tracking-links
description: "Inc42 app store URLs, UTM/Singular naming convention, and the verified D2C Summit QR tracking link behaviour"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 77ea48a7-b503-4d07-9aad-49655a39c265
  modified: 2026-08-18T10:13:09.942Z
---

How Inc42 app install tracking links are built and named. Established 2026-08-18 for the **D2C & Retail Summit offline banner**, but the convention applies to every acquisition channel.

## Canonical store URLs
- **iOS:** `https://apps.apple.com/in/app/inc42/id6789025146`
- **Android:** `https://play.google.com/store/apps/details?id=com.inc42.brief`

## ⚠️ Plain UTMs do NOT work on store URLs — both stores drop them
- **Google Play:** UTMs must be URL-encoded *inside* a `referrer` parameter (`%3D` = `=`, `%26` = `&`). Firebase/Singular SDK reads it automatically.
- **Apple:** ignores UTMs entirely. Uses `pt` (Provider Token) + `ct` (campaign token, **40 char max**) — generated in **App Store Connect → App Analytics → Campaigns**.

## UTM → Singular parameter mapping
Singular calls them **partner parameters**, not UTMs. Source is **not** in the parameter dropdown — it is the **Partner** selected at link creation.

| UTM concept | Singular field | Convention |
|---|---|---|
| `utm_source` | Partner / Custom Source | `Offline Events` |
| `utm_campaign` | `pcn` — Partner Campaign Name | `d2c_retail_summit_2026` |
| — | `pcid` — Partner Campaign ID | `drs2026` |
| `utm_content` | `pcrn` — Partner Creative Name | `standee`, `backdrop`, `badge` |
| placement | `psn` — Partner Site/Publisher Name | `main_stage`, `reg_desk`, `expo_booth` |
| `utm_medium` | **no equivalent** | encode in the name, e.g. `offline_qr` |

Ignore `pscn`, `pscid`, `pssid`, `pssn`, `paffn` — ad-network sub-publisher fields, irrelevant here.

**Source naming rule:** use a *channel-level* source (`Offline Events`, `Email`, `Web Banner`, `Product Hunt`), NOT a per-event source. Singular reports roll up by source first — a source per summit fragments the "how much did offline give us" number. The event identity belongs in `pcn`.

**One link per printed asset**, varying `pcrn` — a single link across all assets means you never learn which placement worked.

## Which Singular link to copy
- **Click-through tracking link** ✅ — anything a human taps or scans (QR, banner, buttons)
- **View-through tracking link** ❌ — impression pixels for paid ads only (carries `_smtype=3`)
- For print: download the QR as **`.svg`**, not `.png`. Print the short URL as text underneath for people who won't scan.

## VERIFIED behaviour of the DRS link (`https://inc42.sng.link/Dj9zc/qcq2/hfjb`, tested 2026-08-18 by curl UA-spoofing)
| Device | Redirect chain | Result |
|---|---|---|
| iPhone | `sng.link` → `apps.apple.com/us/app/inc42/id6789025146` → `itms-appss://` | ✅ opens the App Store **app** |
| Android | `sng.link` → `play.google.com/store/apps/details?id=com.inc42.brief&hl=en_IN` | ✅ works |
| Desktop | JS page → falls through to the Play Store web listing | ⚠️ not a dead end, but wrong-ish |

**Two issues found, not yet fixed:**
1. **iOS resolves to the `/us/` storefront while Android uses `hl=en_IN`.** Apple normally auto-corrects to the signed-in user's storefront, so it works — but check Singular for a storefront/country setting.
2. 🔴 **The referrer carries ONLY `singular_click_id`** — no `pcn`/`pcrn`/UTMs. Singular's own dashboard resolves the campaign server-side and is fine, but **GA4/Firebase will show these installs with no campaign attached.** Fix: add `utm_source`/`utm_medium`/`utm_campaign` under the link's **Google Play referrer / custom referrer parameters** setting.

## Testing method
```bash
curl -sIL -A "<user agent>" "<link>" | grep -i location
```
Also works: Chrome DevTools → device toolbar (⌘⇧M) → pick iPhone/Pixel.

**Neither method can test** app-already-installed behaviour (Universal Links / App Links), deferred deep linking, or real install attribution. **Only a real device does.** Uninstall → scan the printed QR → install → confirm the campaign appears in Singular. Do this before print — an offline QR is unfixable once it's on a standee.

**Note:** every test click registers as a real click in Singular. Record test timestamps so they can be discounted.

## Also worth knowing
- iOS install counts will **under-report** because of the ATT prompt limiting IDFA. Cross-check against Apple's own campaign token in App Store Connect — if Singular says 4 and Apple says 19, believe Apple.
- Keep all UTM values **lowercase with underscores** — GA4 is case-sensitive.

Related: [[project-inc42-app-acquisition]], [[reference-inc42-vendor-stack]], [[project-inc42-launch]].
