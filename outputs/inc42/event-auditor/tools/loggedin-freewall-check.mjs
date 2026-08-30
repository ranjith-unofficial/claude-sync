import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, '..');
const AUTH_STATE = path.join(ROOT, '.auth', 'state.json');
const runId = new Date().toISOString().replace(/[:.]/g, '-');
const outDir = path.join(ROOT, 'runs', `loggedin-freewall-${runId}`);
fs.mkdirSync(outDir, { recursive: true });

const ARTICLES = [
  'https://inc42.com/features/zerodhas-diversification-clock-is-ticking/',
  'https://inc42.com/buzz/esds-ipo-fully-subscribed-within-hours-on-day-1/',
  'https://inc42.com/buzz/ola-electric-secures-centres-%e2%82%b995-81-cr-incentive-under-pli-auto-scheme/',
  'https://inc42.com/features/fy26-financial-tracker-tracking-the-financial-performance-of-indian-startups/',
  'https://inc42.com/buzz/ipo-bound-esds-software-bags-%e2%82%b9216-cr-from-anchor-investors/',
];

const log = [];
function record(entry) {
  log.push({ t: Date.now(), ...entry });
  console.log(JSON.stringify(entry));
}

const REAL_UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36';

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ storageState: AUTH_STATE, viewport: { width: 1440, height: 900 }, userAgent: REAL_UA });
const page = await context.newPage();

// Instrument dataLayer.push and expose scroll% + login-wall DOM checks
await page.addInitScript(() => {
  window.__capturedEvents = [];
  const origPushDesc = Object.getOwnPropertyDescriptor(Array.prototype, 'push');
  const patch = () => {
    if (window.dataLayer && !window.__dlPatched) {
      const origPush = window.dataLayer.push.bind(window.dataLayer);
      window.dataLayer.push = function (...args) {
        try {
          const realScrollPct = Math.round((window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100);
          window.__capturedEvents.push({ t: Date.now(), realScrollPct, payload: JSON.parse(JSON.stringify(args[0])) });
        } catch (e) {}
        return origPush(...args);
      };
      window.__dlPatched = true;
    }
  };
  window.dataLayer = window.dataLayer || [];
  patch();
  const iv = setInterval(patch, 200);
  setTimeout(() => clearInterval(iv), 8000);
});

for (let i = 0; i < ARTICLES.length; i++) {
  const url = ARTICLES[i];
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(1500);

  // check auth state as the SITE sees it
  const authCheck = await page.evaluate(() => {
    const hasLogoutCookie = document.cookie.includes('wordpress_logged_in');
    const bodyHasLogout = document.body.innerText.includes('LOGOUT') || document.body.innerText.includes('Logout');
    let phDistinctId = null, phIsIdentified = null;
    try {
      if (window.posthog) {
        phDistinctId = window.posthog.get_distinct_id ? window.posthog.get_distinct_id() : null;
        phIsIdentified = window.posthog._isIdentified ? window.posthog._isIdentified() : null;
      }
    } catch (e) {}
    return { hasLogoutCookie, bodyHasLogout, phDistinctId, phIsIdentified };
  });
  record({ article: i + 1, url, stage: 'loaded', authCheck });

  const dims = await page.evaluate(() => ({
    h: document.documentElement.scrollHeight,
    vh: window.innerHeight,
  }));
  const max = dims.h - dims.vh;

  for (const pct of [0.25, 0.5, 0.75, 1.0]) {
    const target = Math.round(max * pct);
    // gradual scroll in steps to mimic real scrolling, not an instant jump
    const steps = 8;
    for (let s = 1; s <= steps; s++) {
      await page.evaluate((y) => window.scrollTo(0, y), Math.round(target * (s / steps)));
      await page.waitForTimeout(150);
    }
    await page.waitForTimeout(800);

    const modalCheck = await page.evaluate(() => {
      const text = document.body.innerText;
      const modalKeywords = ['Sign in to continue', 'Login to continue', 'You need to log in', 'Please log in', 'Sign In', 'Log In Required', 'members only', 'subscribe to continue'];
      const found = modalKeywords.filter(k => text.includes(k));
      // check for a visible overlay element covering most of viewport
      const overlays = Array.from(document.querySelectorAll('[class*="modal"],[class*="overlay"],[class*="freewall"],[class*="paywall"],[id*="modal"]'))
        .filter(el => {
          const r = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          return style.display !== 'none' && style.visibility !== 'hidden' && r.width > 200 && r.height > 200;
        })
        .map(el => ({ tag: el.tagName, cls: el.className.toString().slice(0, 120), text: el.innerText.slice(0, 150) }));
      return { keywordsFound: found, visibleOverlays: overlays };
    });

    const scrollEvents = await page.evaluate(() =>
      window.__capturedEvents.filter(e => JSON.stringify(e.payload).toLowerCase().includes('scroll')).slice(-6)
    );

    record({ article: i + 1, url, stage: `scroll_${Math.round(pct * 100)}pct`, modalCheck, recentScrollEvents: scrollEvents });

    if (modalCheck.visibleOverlays.length > 0 || modalCheck.keywordsFound.length > 0) {
      await page.screenshot({ path: path.join(outDir, `article${i + 1}_${Math.round(pct * 100)}pct_MODAL_FOUND.png`), fullPage: false });
    }
  }

  await page.screenshot({ path: path.join(outDir, `article${i + 1}_final.png`), fullPage: false });
}

await browser.close();
fs.writeFileSync(path.join(outDir, 'log.json'), JSON.stringify(log, null, 2));
console.log('DONE. Output dir:', outDir);
