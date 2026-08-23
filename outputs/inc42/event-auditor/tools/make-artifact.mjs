/* Emit the artifact-shaped page (no doctype/html/head/body — the host wraps it). */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { reportStyles, reportBody } from '../lib/report.mjs';

const ROOT = path.dirname(fileURLToPath(import.meta.url)) + '/..';
const runs = fs.readdirSync(path.join(ROOT, 'runs')).filter((d) => /^\d{4}/.test(d)).sort();
const run = process.argv[2] || runs.at(-1);
const raw = JSON.parse(fs.readFileSync(path.join(ROOT, 'runs', run, 'raw.json'), 'utf8'));
const findings = JSON.parse(fs.readFileSync(path.join(ROOT, 'runs', run, 'findings.json'), 'utf8'));
const readJSON = (p) => JSON.parse(fs.readFileSync(path.join(ROOT, p), 'utf8'));
const target = readJSON('spec/target.json');
const spec = { ...target, byName: Object.fromEntries(target.events.map((e) => [e.event, e])) };

const html = `<title>Inc42 Event Audit</title>
${reportStyles()}
${reportBody({ spec, aliases: readJSON('spec/aliases.json'), browser: raw.browser, warehouse: raw.warehouse, findings, stamp: run, days: 30 })}`;

const out = process.argv[3] || path.join(ROOT, 'runs', run, 'artifact.html');
fs.writeFileSync(out, html);
console.log(`${out}  (${(html.length / 1024).toFixed(0)} KB, run ${run})`);
