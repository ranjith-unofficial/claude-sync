/* Resilient page actions. Every one records what happened instead of throwing,
   so a changed selector degrades one step rather than killing the run. */

/* Shared with audit.mjs so Node-side network captures can be stamped with the
   journey step they belong to. Same process, so a module-level holder is enough. */
export const state = { marker: null };

export async function mark(page, label) {
  state.marker = label;
  await page.evaluate((l) => window.__AUDIT_MARK__?.(l), label).catch(() => {});
}

export async function snapshot(page, reason) {
  return page.evaluate((r) => window.__AUDIT_SNAPSHOT__?.(r), reason).catch(() => null);
}

export async function settle(page, ms = 1500) {
  await page.waitForLoadState('domcontentloaded').catch(() => {});
  await page.waitForTimeout(ms);
}

/** Scroll to each depth threshold with a human-ish pause so lazy handlers fire. */
export async function scrollThresholds(page, steps = [25, 50, 75, 100], pause = 1200) {
  const done = [];
  for (const pct of steps) {
    await mark(page, `scroll:${pct}`);
    await page.evaluate((p) => {
      const h = document.documentElement.scrollHeight - window.innerHeight;
      window.scrollTo({ top: Math.max(0, h * (p / 100)), behavior: 'smooth' });
    }, pct).catch(() => {});
    await page.waitForTimeout(pause);
    done.push(pct);
  }
  return done;
}

/** Try selectors in order; click the first visible match. Returns the winner or null. */
export async function clickFirst(page, selectors, { timeout = 4000 } = {}) {
  for (const sel of selectors) {
    try {
      const loc = page.locator(sel).first();
      await loc.waitFor({ state: 'visible', timeout });
      await loc.scrollIntoViewIfNeeded().catch(() => {});
      await loc.click({ timeout: 3000 });
      return sel;
    } catch { /* next */ }
  }
  return null;
}

export async function typeInto(page, selectors, text, { timeout = 4000 } = {}) {
  for (const sel of selectors) {
    try {
      const loc = page.locator(sel).first();
      await loc.waitFor({ state: 'visible', timeout });
      await loc.click({ timeout: 2000 });
      await loc.fill('');
      await loc.type(text, { delay: 90 });
      return sel;
    } catch { /* next */ }
  }
  return null;
}

/** Collect article links off a listing/home page. */
export async function articleLinks(page, limit = 6) {
  return page.evaluate((n) => {
    const seen = new Set();
    return [...document.querySelectorAll('a[href]')]
      .map((a) => a.href)
      // a real article has a slug segment after the section; /buzz/ alone is a listing
      .filter((h) => /inc42\.com\/(buzz|features|resources|startups|entrepreneurship)\/[a-z0-9][a-z0-9-]{10,}\/?(\?|#|$)/.test(h))
      .map((h) => h.split('?')[0].split('#')[0])
      .filter((h) => !seen.has(h) && seen.add(h))
      .slice(0, n);
  }, limit).catch(() => []);
}

export async function isVisible(page, selectors) {
  for (const sel of selectors) {
    try { if (await page.locator(sel).first().isVisible({ timeout: 1500 })) return sel; } catch {}
  }
  return null;
}
