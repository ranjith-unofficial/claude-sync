#!/usr/bin/env node
/* One-time auth capture.
 *
 *   node login.mjs
 *
 * Opens a real Chrome window. YOU sign in with Google / LinkedIn / email — the script
 * never sees, asks for, or stores a password. Once it detects an authenticated session it
 * saves the cookies + localStorage to .auth/state.json, and every later audit run reuses
 * that instead of driving a login form.
 *
 * The saved file IS a live session for your Inc42 account. It is gitignored. Delete it
 * with `node login.mjs --clear` when you are done.
 */
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const AUTH_DIR = path.join(ROOT, '.auth');
const STATE = path.join(AUTH_DIR, 'state.json');
const REAL_UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36';

if (process.argv.includes('--clear')) {
  fs.rmSync(AUTH_DIR, { recursive: true, force: true });
  console.log('cleared .auth/');
  process.exit(0);
}

/* Inc42 sets these on a real login; they are explicitly "deleted" while logged out. */
const LOGGED_IN = (cookies) =>
  cookies.some((c) => ['current_user_id', 'user_logged_in'].includes(c.name)
    && c.value && c.value !== 'deleted');

const TIMEOUT_MIN = Number((process.argv.find((a) => a.startsWith('--minutes=')) || '').split('=')[1] || 8);

(async () => {
  fs.mkdirSync(AUTH_DIR, { recursive: true });
  const browser = await chromium.launch({ headless: false, channel: 'chrome' })
    .catch(() => chromium.launch({ headless: false }));
  const ctx = await browser.newContext({
    userAgent: REAL_UA, viewport: { width: 1440, height: 900 },
    locale: 'en-IN', timezoneId: 'Asia/Kolkata',
    extraHTTPHeaders: { 'accept-language': 'en-IN,en;q=0.9' },
  });
  const page = await ctx.newPage();
  await page.goto('https://inc42.com/', { waitUntil: 'domcontentloaded' });

  console.log(`
  ┌──────────────────────────────────────────────────────────────┐
  │  A Chrome window is open.                                    │
  │                                                              │
  │  1. Click Sign In and use Google or LinkedIn as you normally │
  │     would. Nothing you type is visible to this script.       │
  │  2. Leave the window open once you land back on inc42.com.   │
  │                                                              │
  │  Waiting up to ${String(TIMEOUT_MIN).padEnd(2)} minutes…                                 │
  └──────────────────────────────────────────────────────────────┘
`);

  const deadline = Date.now() + TIMEOUT_MIN * 60_000;
  let ok = false;
  while (Date.now() < deadline) {
    await page.waitForTimeout(2000);
    let cookies = [];
    try { cookies = await ctx.cookies(); } catch { break; }
    if (LOGGED_IN(cookies)) { ok = true; break; }
  }

  if (!ok) {
    console.log('  ✗ no authenticated session detected — nothing saved.');
    await browser.close().catch(() => {});
    process.exit(1);
  }

  // let the session settle so any post-login identify() lands in localStorage too
  await page.waitForTimeout(4000);
  const who = await page.evaluate(() => {
    try { return { did: window.posthog?.get_distinct_id?.() ?? null, cio: window.analytics?.user?.()?.id?.() ?? null }; }
    catch { return { did: null, cio: null }; }
  }).catch(() => ({ did: null, cio: null }));

  await ctx.storageState({ path: STATE });
  fs.chmodSync(STATE, 0o600);
  const st = JSON.parse(fs.readFileSync(STATE, 'utf8'));
  console.log(`  ✓ session saved → .auth/state.json (${st.cookies.length} cookies, chmod 600)`);
  console.log(`    posthog distinct_id : ${who.did ?? 'null'}`);
  console.log(`    customer.io user id : ${who.cio ?? 'null'}`);
  console.log(`\n  Now run:  node audit.mjs --auth\n`);
  await browser.close().catch(() => {});
})();
