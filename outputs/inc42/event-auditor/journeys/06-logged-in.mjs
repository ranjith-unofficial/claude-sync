import { mark, snapshot, settle, clickFirst, articleLinks, isVisible } from '../lib/actions.mjs';

/* Runs on the session captured by `node login.mjs` — no credentials are handled here.
   This is where the four identity P0s from the 12-Aug audit become observable. */
export default {
  id: 'logged-in',
  name: 'Authenticated — identity, save, follow, feed',
  auth: 'user',
  expect: [
    { event: 'story_saved', min: 1, props: ['source'] },
    { event: 'entity_followed', min: 1, props: ['entity_type', 'entity_id'] },
    { event: 'feed_viewed', min: 1, props: ['follow_count', 'is_empty'] },
  ],
  async run(page, ctx) {
    await page.goto('https://inc42.com/', { waitUntil: 'domcontentloaded' });
    await settle(page, 4000);
    await mark(page, 'auth:landed');
    const id = await snapshot(page, 'authenticated');
    ctx.log(`posthog distinct_id : ${id?.posthog_distinct_id ?? 'null'}`);
    ctx.log(`customer.io user id : ${id?.cio_user_id ?? 'null'}`);
    if (id?.pii?.length) ctx.log(`PII in dataLayer    : ${id.pii.map((p) => `${p.kind}@${p.path}`).join(', ')}`);

    const person = id?.posthog_person;
    if (person && typeof person === 'object') {
      const keys = Object.keys(person).slice(0, 12);
      ctx.log(`person props        : ${keys.join(', ')}${Object.keys(person).length > 12 ? '…' : ''}`);
    }

    const links = await articleLinks(page, 4);
    if (!links.length) return { skipped: 'no article links', identity: id ?? null };

    await page.goto(links[0], { waitUntil: 'domcontentloaded' });
    await settle(page, 3500);

    await mark(page, 'auth:save-story');
    const saved = await clickFirst(page, [
      '[class*="save"] button', '[class*="bookmark"]', 'button[aria-label*="ave"]',
      '[class*="save-story"]', '[class*="save"]',
    ]);
    ctx.log(`save story          : ${saved ?? 'NOT FOUND'}`);
    await page.waitForTimeout(3000);

    await mark(page, 'auth:follow');
    const followed = await clickFirst(page, [
      'text=/start following/i', '[class*="follow"] button', 'button:has-text("Follow")', '[class*="follow-btn"]',
    ]);
    ctx.log(`follow entity       : ${followed ?? 'NOT FOUND'}`);
    await page.waitForTimeout(3000);

    await mark(page, 'auth:my-inc42');
    await page.goto('https://inc42.com/my-inc42/', { waitUntil: 'domcontentloaded' }).catch(() => {});
    await settle(page, 4000);
    const feed = await isVisible(page, ['[class*="feed"]', '[class*="my-inc42"]', 'main']);
    ctx.log(`my-inc42 feed       : ${feed ?? 'NOT DETECTED'}`);
    await snapshot(page, 'my-inc42');

    await mark(page, 'auth:feed-filter');
    const filtered = await clickFirst(page, ['[class*="tab"]', '[class*="filter"] button', '[role="tab"]']);
    await page.waitForTimeout(2500);

    return { identity: id ?? null, saved, followed, feed, filtered };
  },
};
