import { mark, snapshot, settle, scrollThresholds, articleLinks } from '../lib/actions.mjs';

export default {
  id: 'article-read',
  name: 'Anonymous article read + scroll',
  auth: 'anon',
  // Spec events this journey should produce. `min`/`max` bound the count.
  expect: [
    { event: 'page_viewed', min: 2, where: { page_type: 'article' }, note: 'home + article' },
    { event: 'scroll_depth', min: 4, max: 4, note: 'one fire per 25/50/75/100 threshold' },
    { event: 'read_time_logged', min: 1 },
    { event: 'session_started', min: 1 },
  ],
  async run(page, ctx) {
    await page.goto('https://inc42.com/', { waitUntil: 'domcontentloaded' });
    await settle(page, 3000);
    await mark(page, 'home:loaded');
    await snapshot(page, 'home');

    const links = await articleLinks(page, 4);
    ctx.log(`found ${links.length} article links`);
    if (!links.length) return { skipped: 'no article links found on home' };

    await page.goto(links[0], { waitUntil: 'domcontentloaded' });
    await settle(page, 3000);
    await mark(page, 'article:loaded');
    const snap = await snapshot(page, 'article');
    ctx.log(`article: ${links[0]}`);

    await scrollThresholds(page);
    await mark(page, 'article:scrolled');

    // read_time_logged is spec'd to fire on unload / 30s beacon — give it a beat, then navigate away.
    await page.waitForTimeout(4000);
    await page.goto('https://inc42.com/', { waitUntil: 'domcontentloaded' });
    await settle(page, 2000);
    await mark(page, 'article:unloaded');

    return { article: links[0], bundle: snap?.event_properties_bundle ?? null };
  },
};
