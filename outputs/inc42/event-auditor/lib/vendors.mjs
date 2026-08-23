import zlib from 'node:zlib';

const j = (s) => { try { return JSON.parse(s); } catch { return null; } };
const arr = (x) => (x == null ? [] : Array.isArray(x) ? x : [x]);

/** PostHog: proxied at posthog.inc42.com/i/v0/e/. Body is one of:
 *  raw JSON | `data=<base64>` form-encoded | gzip (?compression=gzip-js) | base64(gzip). */
function decodePostHog(url, body, buf) {
  let payload = null;
  const tryGz = (b) => { try { return j(zlib.gunzipSync(b).toString('utf8')); } catch { return null; } };
  const tryB64 = (s) => {
    try {
      const b = Buffer.from(decodeURIComponent(s), 'base64');
      return tryGz(b) ?? j(b.toString('utf8'));
    } catch { return null; }
  };
  if (buf?.length) payload = tryGz(buf);
  if (!payload && body) {
    payload = j(body);
    if (!payload && body.startsWith('data=')) payload = tryB64(body.slice(5).split('&')[0]);
    if (!payload) payload = tryB64(body);
  }
  if (!payload) {
    // batch endpoints wrap: {api_key, batch:[...]}
    const q = new URL(url).searchParams.get('data');
    if (q) payload = tryB64(q);
  }
  if (!payload) return [];
  const batch = payload.batch ?? payload;
  return arr(batch).filter(Boolean).map((e) => ({
    vendor: 'posthog',
    name: e.event,
    props: e.properties ?? {},
    distinct_id: e.properties?.distinct_id ?? e.distinct_id ?? null,
    set: e.$set ?? e.properties?.$set ?? null,
  }));
}

/** GA4 Measurement Protocol: en=<event>, ep.<k>=<v>, epn.<k>=<num>. POST body can hold N events, one per line. */
function decodeGA4(url, body) {
  const out = [];
  const parse = (sp, base = {}) => {
    const props = { ...base };
    let name = null;
    for (const [k, v] of sp) {
      if (k === 'en') name = v;
      else if (k.startsWith('ep.') || k.startsWith('epn.')) props[k.replace(/^epn?\./, '')] = v;
      else props[k] = v;
    }
    if (name) out.push({ vendor: 'ga4', name, props, distinct_id: props.cid ?? null });
  };
  const u = new URL(url);
  const common = Object.fromEntries(u.searchParams);
  if (u.searchParams.get('en')) parse(u.searchParams);
  for (const line of (body || '').split('\n').filter(Boolean)) parse(new URLSearchParams(line), common);
  return out;
}

/** Meta Pixel: /tr?ev=<event>&cd[<k>]=<v>  (also POST for large payloads) */
function decodeMeta(url, body) {
  const sp = new URL(url).searchParams;
  const merged = new URLSearchParams(body || '');
  for (const [k, v] of sp) if (!merged.has(k)) merged.append(k, v);
  const name = merged.get('ev');
  if (!name) return [];
  const props = {};
  for (const [k, v] of merged) {
    const m = k.match(/^cd\[(.+)\]$/);
    if (m) props[m[1]] = v;
    else if (['ud[em]', 'ud[ph]', 'ud[fn]', 'ud[ln]'].includes(k)) props[k] = v;
  }
  return [{ vendor: 'meta', name, props, distinct_id: merged.get('external_id') ?? null }];
}

/** Customer.io CDP (Segment-shaped): {type:'track'|'identify'|'page', event, userId, anonymousId, properties, traits} */
function decodeCIO(url, body) {
  const p = j(body);
  if (!p) return [];
  return arr(p.batch ?? p).filter(Boolean).map((e) => ({
    vendor: 'customerio',
    name: e.event ?? `$${e.type}`,
    props: e.properties ?? e.traits ?? {},
    distinct_id: e.userId ?? e.anonymousId ?? null,
    identified: e.userId != null,
    type: e.type,
  }));
}

export const VENDORS = [
  { id: 'posthog',    test: (u) => /posthog\.inc42\.com|i\.posthog\.com|posthog\.com/.test(u) && /\/(e|i\/v0\/e|batch|capture|s)\/?(\?|$)/.test(u), decode: decodePostHog },
  { id: 'ga4',        test: (u) => /google-analytics\.com\/(g|mp)\/collect|analytics\.google\.com\/g\/collect|\/gtag\/|region\d*\.google-analytics/.test(u), decode: decodeGA4 },
  { id: 'meta',       test: (u) => /facebook\.com\/tr/.test(u), decode: decodeMeta },
  { id: 'customerio', test: (u) => /(track|cdp)(-eu)?\.customer\.io/.test(u), decode: decodeCIO },
];

export function matchVendor(url) {
  return VENDORS.find((v) => v.test(url)) ?? null;
}

/** Turn a Playwright request into normalised event records. Never throws. */
export function decodeRequest(req) {
  const url = req.url();
  const v = matchVendor(url);
  if (!v) return [];
  let body = null, buf = null;
  try { body = req.postData(); } catch {}
  try { buf = req.postDataBuffer(); } catch {}
  try {
    return (v.decode(url, body, buf) || []).map((e) => ({ ...e, url, method: req.method() }));
  } catch (err) {
    return [{ vendor: v.id, name: '__DECODE_FAILED__', props: { error: String(err), bodyPreview: (body || '').slice(0, 200) }, url }];
  }
}
