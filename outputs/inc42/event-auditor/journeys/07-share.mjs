import { mark, settle, clickFirst, articleLinks, isVisible } from '../lib/actions.mjs';

/* `Share` had 32 events/30d in the Jun 2026 audit — healthy props, tiny volume.
   Worth driving directly to see whether it still fires at all. */
export default {
  id: 'share',
  name: 'Share an article + modal open/close',
  auth: 'anon',
  expect: [
    { event: 'story_shared', min: 1, props: ['channel', 'source'] },
  ],
  async run(page, ctx) {
    await page.goto('https://inc42.com/', { waitUntil: 'domcontentloaded' });
    await settle(page, 3000);
    const links = await articleLinks(page, 3);
    if (!links.length) return { skipped: 'no article links' };

    await page.goto(links[0], { waitUntil: 'domcontentloaded' });
    await settle(page, 3500);
    await mark(page, 'share:open');

    // Share controls are usually a rail or a row of platform icons.
    const opened = await clickFirst(page, [
      '[class*="share"] button', '[class*="share"] a[href*="linkedin"]',
      '[class*="social"] a[href*="twitter"]', '[class*="social"] a[href*="linkedin"]',
      '[aria-label*="hare"]', '[class*="share-icon"]', '[class*="share"]',
    ]);
    ctx.log(`share control: ${opened ?? 'NOT FOUND'}`);
    await page.waitForTimeout(2500);

    await mark(page, 'share:copy-link');
    const copy = await clickFirst(page, ['text=/copy link/i', '[class*="copy"]']);
    ctx.log(`copy link: ${copy ?? 'not present'}`);
    await page.waitForTimeout(2000);

    // any modal that opened — close it, to exercise Modal Close / Modal Closed
    await mark(page, 'share:modal-close');
    const modal = await isVisible(page, ['[role="dialog"]', '[class*="modal"]']);
    if (modal) {
      await clickFirst(page, ['[class*="close"]', 'button[aria-label*="lose"]', '[role="dialog"] button']);
      ctx.log(`closed modal: ${modal}`);
    }
    await settle(page, 2500);
    return { opened, copy, modal };
  },
};
