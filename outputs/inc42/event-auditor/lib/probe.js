/* Injected via addInitScript BEFORE any page script runs.
   Wraps vendor SDKs at the call site so we see the arguments the site passed,
   not just what survived batching. Network capture happens in Node (vendors.mjs);
   this half exists to catch calls that are transformed, dropped, or never flushed. */
(() => {
  if (window.__AUDIT__) return;
  const T0 = Date.now();
  const A = (window.__AUDIT__ = { sdk: [], identity: [], notes: [], t0: T0 });

  const now = () => Date.now() - T0;
  const safe = (o, depth = 0) => {
    if (o == null || depth > 6) return o ?? null;
    const t = typeof o;
    if (t === 'function') return '[fn]';
    if (t !== 'object') return o;
    if (o instanceof Element) return `[Element ${o.tagName.toLowerCase()}]`;
    try {
      if (Array.isArray(o)) return o.slice(0, 50).map((v) => safe(v, depth + 1));
      const out = {};
      for (const k of Object.keys(o).slice(0, 200)) out[k] = safe(o[k], depth + 1);
      return out;
    } catch { return '[unserializable]'; }
  };
  /* Stream to Node as well as buffering locally. window.__AUDIT__ is destroyed on every
     navigation, so anything only buffered in-page is lost the moment the user clicks a link. */
  const emit = (r) => { try { window.__AUDIT_EMIT__?.(r); } catch {} };
  const rec = (vendor, kind, name, props, extra) => {
    const r = { t: now(), vendor, kind, name: name ?? null, props: safe(props), stack: trace(), ...extra };
    A.sdk.push(r);
    emit({ channel: 'sdk', url: location.pathname, ...r });
    return r;
  };

  // Where in the page did this fire from? Cheap provenance for "who double-fired this".
  function trace() {
    try {
      return (new Error().stack || '').split('\n').slice(3, 6)
        .map((s) => s.trim().replace(/^at\s+/, '')).join(' <- ').slice(0, 300);
    } catch { return ''; }
  }

  /* Run `fn` when window[name] appears, whether it exists already or is assigned later. */
  function onGlobal(name, fn) {
    try {
      if (window[name] !== undefined) { fn(window[name]); return; }
      let v;
      Object.defineProperty(window, name, {
        configurable: true,
        get: () => v,
        set(nv) { v = nv; try { fn(nv); } catch (e) { A.notes.push(`hook ${name}: ${e}`); } },
      });
    } catch (e) { A.notes.push(`onGlobal ${name}: ${e}`); }
  }

  /* Replace obj[method] with a logging passthrough. Idempotent. */
  function wrap(obj, method, handler) {
    if (!obj || typeof obj[method] !== 'function' || obj[method].__audited) return false;
    const orig = obj[method];
    const patched = function (...args) {
      try { handler(args); } catch (e) { A.notes.push(`wrap ${method}: ${e}`); }
      return orig.apply(this, args);
    };
    patched.__audited = true;
    try { Object.defineProperty(obj, method, { value: patched, writable: true, configurable: true }); }
    catch { obj[method] = patched; }
    return true;
  }

  // ---- GTM dataLayer -------------------------------------------------------
  onGlobal('dataLayer', (dl) => {
    if (!Array.isArray(dl)) return;
    dl.forEach((e) => rec('gtm', 'dataLayer', e && (e.event || e[0]), e, { replayed: true }));
    wrap(dl, 'push', (args) => args.forEach((e) => rec('gtm', 'dataLayer', e && (e.event || e[0]), e)));
  });

  // ---- Meta Pixel ----------------------------------------------------------
  onGlobal('fbq', (f) => {
    if (typeof f !== 'function' || f.__audited) return;
    const orig = f;
    const patched = function (...a) {
      // fbq('track'|'trackCustom', name, props)
      if (a[0] === 'track' || a[0] === 'trackCustom') rec('meta', a[0], a[1], a[2]);
      else rec('meta', String(a[0]), a[1], a[2]);
      return orig.apply(this, a);
    };
    Object.assign(patched, orig);
    patched.__audited = true;
    try { Object.defineProperty(window, 'fbq', { value: patched, writable: true, configurable: true }); } catch {}
  });

  // ---- PostHog -------------------------------------------------------------
  // The snippet stubs window.posthog early and swaps in the real lib on load.
  // Re-arm on an interval so we survive the swap.
  const armPostHog = () => {
    const p = window.posthog;
    if (!p || typeof p !== 'object') return;
    wrap(p, 'capture', (a) => rec('posthog', 'capture', a[0], a[1]));
    wrap(p, 'identify', (a) => { rec('posthog', 'identify', a[0], a[1]); snapIdentity('posthog.identify'); });
    wrap(p, 'reset', () => { rec('posthog', 'reset', null, null); snapIdentity('posthog.reset'); });
    wrap(p, 'group', (a) => rec('posthog', 'group', a[0], a[1]));
  };

  // ---- Customer.io CDP (Segment-shaped) + legacy _cio -----------------------
  const armCIO = () => {
    const an = window.analytics;
    if (an && typeof an === 'object') {
      wrap(an, 'track', (a) => rec('customerio', 'track', a[0], a[1]));
      wrap(an, 'identify', (a) => { rec('customerio', 'identify', a[0], a[1]); snapIdentity('cio.identify'); });
      wrap(an, 'page', (a) => rec('customerio', 'page', a[0], a[1]));
    }
    const cio = window._cio;
    if (Array.isArray(cio)) wrap(cio, 'push', (a) => rec('customerio', '_cio', a[0] && a[0][0], a[0]));
  };

  setInterval(() => { try { armPostHog(); armCIO(); } catch {} }, 250);
  armPostHog(); armCIO();

  // ---- Identity + PII snapshot --------------------------------------------
  const PII = {
    email: /\b[\w.+-]+@[\w-]+\.[\w.]{2,}\b/,
    phone: /\b(?:\+?91[- ]?)?[6-9]\d{9}\b/,
  };
  function scanPII(obj, path = '', hits = [], depth = 0) {
    if (obj == null || depth > 5) return hits;
    if (typeof obj === 'string') {
      for (const [k, re] of Object.entries(PII)) if (re.test(obj)) hits.push({ path, kind: k, sample: obj.slice(0, 6) + '…' });
      return hits;
    }
    if (typeof obj !== 'object') return hits;
    for (const k of Object.keys(obj).slice(0, 200)) {
      try { scanPII(obj[k], path ? `${path}.${k}` : k, hits, depth + 1); } catch {}
    }
    return hits;
  }

  function snapIdentity(reason) {
    const s = { t: now(), reason, url: location.pathname };
    try { s.posthog_distinct_id = window.posthog?.get_distinct_id?.() ?? null; } catch {}
    try { s.posthog_person = safe(window.posthog?.get_property?.('$stored_person_properties') ?? null); } catch {}
    try { s.posthog_flags = safe(window.posthog?.featureFlags?.getFlags?.() ?? null); } catch {}
    try { const u = window.analytics?.user?.(); s.cio_user_id = u?.id?.() ?? null; s.cio_anon_id = u?.anonymousId?.() ?? null; s.cio_traits = safe(u?.traits?.() ?? null); } catch {}
    try { s.event_properties_bundle = safe(window.eventProperties ?? null); } catch {}
    try {
      s.pii = [
        ...scanPII(window.dataLayer, 'dataLayer'),
        ...scanPII(window.eventProperties, 'eventProperties'),
      ];
    } catch {}
    A.identity.push(s);
    emit({ channel: 'identity', ...s });
    return s;
  }
  window.__AUDIT_SNAPSHOT__ = snapIdentity;
  window.__AUDIT_MARK__ = (label) => A.sdk.push({ t: now(), vendor: '_marker', kind: 'mark', name: label, props: { url: location.pathname } });

  addEventListener('load', () => setTimeout(() => snapIdentity('load'), 1500));
})();
