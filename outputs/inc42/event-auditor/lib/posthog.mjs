/* PostHog HogQL client.
   NOTE: use YOUR OWN personal API key. The team MCP runs as a shared account whose
   active project switches mid-session; this client pins project_id explicitly and only reads. */

const cfg = () => ({
  host: (process.env.POSTHOG_HOST || 'https://eu.posthog.com').replace(/\/$/, ''),
  key: process.env.POSTHOG_API_KEY,
  project: process.env.POSTHOG_PROJECT_ID || '53557',
});

export function configured() { return Boolean(cfg().key); }

/** HogQL rule: explicit date literals only — relative windows drift between runs. */
export function dateRange(days = 30, endISO = null) {
  const end = endISO ? new Date(endISO) : new Date();
  const start = new Date(end.getTime() - days * 864e5);
  const d = (x) => x.toISOString().slice(0, 10);
  return { start: d(start), end: d(end) };
}

export async function hogql(query, { timeoutMs = 90_000 } = {}) {
  const { host, key, project } = cfg();
  if (!key) throw new Error('POSTHOG_API_KEY not set');
  const ac = new AbortController();
  const t = setTimeout(() => ac.abort(), timeoutMs);
  try {
    const res = await fetch(`${host}/api/projects/${project}/query/`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: { kind: 'HogQLQuery', query } }),
      signal: ac.signal,
    });
    const text = await res.text();
    if (!res.ok) throw new Error(`PostHog ${res.status}: ${text.slice(0, 500)}`);
    const json = JSON.parse(text);
    const cols = json.columns || [];
    return (json.results || []).map((row) => Object.fromEntries(cols.map((c, i) => [c, row[i]])));
  } finally { clearTimeout(t); }
}

const esc = (s) => String(s).replace(/'/g, "''");

/** Every event with volume, reach and recency. The zombie/dead-event detector. */
export function qEventVolumes({ start, end }) {
  return `
SELECT event,
       count()                AS volume,
       uniq(person_id)        AS persons,
       min(timestamp)         AS first_seen,
       max(timestamp)         AS last_seen,
       count() / dateDiff('day', toDate('${start}'), toDate('${end}')) AS per_day
FROM events
WHERE timestamp >= toDateTime('${start} 00:00:00') AND timestamp < toDateTime('${end} 00:00:00')
GROUP BY event
ORDER BY volume DESC
LIMIT 500`;
}

/** Which property keys appear on an event, and on what share of its rows. */
export function qPropertyCoverage(event, { start, end }) {
  return `
SELECT key, count() AS present,
       (SELECT count() FROM events
         WHERE event = '${esc(event)}'
           AND timestamp >= toDateTime('${start} 00:00:00') AND timestamp < toDateTime('${end} 00:00:00')) AS total
FROM (
  SELECT arrayJoin(JSONExtractKeys(properties)) AS key
  FROM events
  WHERE event = '${esc(event)}'
    AND timestamp >= toDateTime('${start} 00:00:00') AND timestamp < toDateTime('${end} 00:00:00')
)
GROUP BY key
ORDER BY present DESC
LIMIT 300`;
}

/** Distinct values of a property — feeds enum conformance + junk-value detection. */
export function qPropertyValues(prop, { start, end }, event = null) {
  const ev = event ? `AND event = '${esc(event)}'` : '';
  return `
SELECT JSONExtractString(properties, '${esc(prop)}') AS value, count() AS volume
FROM events
WHERE timestamp >= toDateTime('${start} 00:00:00') AND timestamp < toDateTime('${end} 00:00:00')
  ${ev}
  AND JSONHas(properties, '${esc(prop)}')
GROUP BY value
ORDER BY volume DESC
LIMIT 200`;
}

/** All property keys site-wide — input to the casing/typo duplicate detector. */
export function qAllKeys({ start, end }) {
  return `
SELECT key, count() AS volume, uniq(event) AS on_events
FROM (
  SELECT arrayJoin(JSONExtractKeys(properties)) AS key, event
  FROM events
  WHERE timestamp >= toDateTime('${start} 00:00:00') AND timestamp < toDateTime('${end} 00:00:00')
)
GROUP BY key
ORDER BY volume DESC
LIMIT 1000`;
}

/** Close the loop: did THIS browser run's events actually land? */
export function qVerifyRun(distinctIds, sinceISO) {
  const list = distinctIds.map((d) => `'${esc(d)}'`).join(', ');
  return `
SELECT event, count() AS volume, max(timestamp) AS last_seen,
       groupUniqArray(10)(distinct_id) AS ids
FROM events
WHERE distinct_id IN (${list})
  AND timestamp >= toDateTime('${esc(sinceISO.slice(0, 19).replace('T', ' '))}')
GROUP BY event
ORDER BY volume DESC
LIMIT 200`;
}

/** Person-property coverage — the identity half of the audit. */
export function qPersonProps() {
  return `
SELECT key, count() AS persons
FROM (SELECT arrayJoin(JSONExtractKeys(properties)) AS key FROM persons)
GROUP BY key
ORDER BY persons DESC
LIMIT 400`;
}
