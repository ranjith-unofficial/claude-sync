# Inc42 Event Auditor

Drives the real site in a real browser, captures what actually goes out on the wire to
every vendor, verifies it landed in PostHog, and diffs all of it against your tracking plan.

The two audits you already have are the two halves of this, done by hand:

| Existing audit | Half it covers | What it caught |
|---|---|---|
| `Inc42 Analytics \| Master` → *Audit \| Jun 2026* | Warehouse | 5 dead events, 3 duplicate modal events, `Model Type` typo, enum junk |
| `Inc42 Website - Events & Properties` → *Live Audit — 12 Aug* | Browser | email-as-distinct_id, PII in dataLayer, scroll never reaching PostHog |

Neither can catch **"fires correctly in the browser and never lands in the warehouse"**.
Only the two together can, which is the point of this tool.

## Run it

```bash
npm install
cp .env.example .env      # add your own PostHog personal API key

node audit.mjs                                  # full: browser + warehouse
node audit.mjs --only=browser                   # no API key needed
node audit.mjs --only=warehouse                 # no browser, just PostHog
node audit.mjs --journeys=search,freewall       # subset
node audit.mjs --headed=true                    # watch it work
node audit.mjs --days=90 --ingest-wait=180      # wider window, longer ingest wait
```

Output lands in `runs/<timestamp>/`: `report.html`, `findings.json`, `raw.json`.

## How it works

**1 · Fire.** Playwright drives real Chrome through scripted journeys (`journeys/*.mjs`).
Node intercepts every outbound request and decodes the payload per vendor
(`lib/vendors.mjs` — PostHog gzip/base64 batches, GA4 Measurement Protocol, Meta Pixel,
Customer.io CDP). That is ground truth: the wire, not the console.

**2 · Observe.** `lib/probe.js` is injected before any page script and wraps
`posthog.capture`, `analytics.track`, `fbq` and `dataLayer.push` at the call site, so you
also see arguments that get transformed or dropped before they reach the network. It
streams to Node over an exposed binding — buffering in-page would lose everything on each
navigation. It also snapshots identity state (`distinct_id`, CIO user, feature flags,
`window.eventProperties`) and scans for raw PII.

**3 · Verify.** `lib/posthog.mjs` runs HogQL against the project: 30d volumes, property
coverage, enum values, duplicate keys — and critically, a query on *this run's*
`distinct_id`s to prove the events landed.

**4 · Diff.** `lib/rules.mjs` classifies against the spec. Findings are P0/P1/P2.

## The failure classes

| Class | Means |
|---|---|
| `NOT_INSTRUMENTED` | Planned, nothing fires anywhere |
| `NEVER_FIRES` | Mapped to a live event, but zero in browser *and* zero in 30d warehouse |
| `NOT_REPRODUCED` | Has production volume but this journey didn't trigger it — journey gap, not a defect |
| `UNVERIFIED` | Not seen in browser, no API key to arbitrate. **Set the key to resolve these.** |
| `FIRES_NOT_LANDED` | Left the browser, never arrived. Silent data loss |
| `COVERAGE_GAP` | Reaches GA4/Meta, never PostHog |
| `VENDOR_BALANCE` | The stack as a whole is lopsided |
| `VENDOR_ASYMMETRY` | Same event, rich payload to ads, thin payload to product |
| `DOUBLE_FIRE` | Duplicate listener, or two names for one action |
| `PROP_MISSING` / `PROP_COVERAGE` | Spec'd property absent, or on <90% of rows |
| `NAME_DRIFT` | Casing variants and one-character typos of the same key |
| `IDENTITY` | distinct_id is PII, no reset on logout, CIO never identified |
| `PII_LEAK` | Raw email/phone in the dataLayer or on the wire |
| `ZOMBIE` / `NOISE` / `UNSPECIFIED` | Dead events, GTM leakage, ungoverned live events |
| `PAGE_ERROR` | Uncaught JS error — aborts every analytics call after it |

## The spec layer

`tools/extract-spec.py` turns both spreadsheets into JSON. Re-run it whenever a sheet changes:

```bash
python3 tools/extract-spec.py
```

- `spec/target.json` — 63 planned events, property groups, dictionary. What *should* exist.
- `spec/live.json` — the Jun 2026 warehouse audit. What *did* exist.
- `spec/aliases.json` — **the join, hand-maintained.** The plan is snake_case; production is
  Title Case. Only 2 of 63 names match automatically, so without this file the tool would
  report all 63 as missing. `tools/seed-aliases.py` regenerates it from the audit findings.

Edit `aliases.json` as instrumentation lands. It is the one file that carries judgement.

## Gotchas worth knowing

- **inc42.com serves HTTP 201 + `application/octet-stream` to any UA containing
  `HeadlessChrome`.** The runner overrides the UA. Any synthetic monitor you point at the
  site needs the same, or it silently gets a non-HTML body.
- **PostHog has `autocapture: false` and `capture_pageview: false`.** Nothing is automatic;
  every product event is hand-coded. There is no safety net.
- **Use your own PostHog personal API key.** The team MCP account is shared and its active
  project switches mid-session. This client pins `POSTHOG_PROJECT_ID` and only ever reads.
- Journeys never submit the newsletter form, never register, and never pay. Those paths are
  read-only by design — extend deliberately if you want them.

## Adding a journey

```js
// journeys/07-thing.mjs
export default {
  id: 'thing',
  name: 'What the user is doing',
  expect: [{ event: 'spec_event_name', min: 1, props: ['a', 'b'] }],
  async run(page, ctx) { /* drive the UI; use lib/actions.mjs helpers */ },
};
```

`expect[].event` refers to **spec** names. The alias layer resolves them to production names.
