#!/usr/bin/env node
/* Re-run the rules against a saved run. Use after editing spec/coverage.json or the rules,
   so a classification fix does not require another 10-minute browser sweep. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { runRules } from '../lib/rules.mjs';
import { runMasterRules } from '../lib/rules-master.mjs';

const ROOT = path.dirname(fileURLToPath(import.meta.url)) + '/..';
const readJSON = (p) => JSON.parse(fs.readFileSync(path.join(ROOT, p), 'utf8'));
const runs = fs.readdirSync(path.join(ROOT, 'runs')).filter((d) => /^\d{4}/.test(d)).sort();
const run = process.argv[2] || runs.at(-1);
const dir = path.join(ROOT, 'runs', run);
const raw = JSON.parse(fs.readFileSync(path.join(dir, 'raw.json'), 'utf8'));

const target = readJSON('spec/target.json');
const spec = { ...target, byName: Object.fromEntries(target.events.map((e) => [e.event, e])) };
const aliases = readJSON('spec/aliases.json');
const liveSheet = readJSON('spec/live.json');
const coverage = readJSON('spec/coverage.json');

const findings = runRules({ spec, aliases, liveSheet, browser: raw.browser, warehouse: raw.warehouse });
const drift = runMasterRules({ live: liveSheet, coverage, browser: raw.browser, warehouse: raw.warehouse });
fs.writeFileSync(path.join(dir, 'findings.json'), JSON.stringify(findings, null, 2));
fs.writeFileSync(path.join(dir, 'drift.json'), JSON.stringify(drift, null, 2));

const c = (a) => a.reduce((o, f) => ((o[f.severity] = (o[f.severity] || 0) + 1), o), {});
console.log(`run ${run}`);
console.log(`  findings ${findings.length}  P0:${c(findings).P0 || 0} P1:${c(findings).P1 || 0} P2:${c(findings).P2 || 0}`);
console.log(`  drift    ${drift.length}  P0:${c(drift).P0 || 0} P1:${c(drift).P1 || 0} P2:${c(drift).P2 || 0}`);
for (const f of drift.filter((x) => x.severity !== 'P2')) console.log(`   ${f.severity} · ${f.cls.padEnd(20)} ${f.title}`);
