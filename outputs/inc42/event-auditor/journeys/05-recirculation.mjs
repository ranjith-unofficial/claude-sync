import { mark, settle, clickFirst, articleLinks } from '../lib/actions.mjs';

export default {
  id: 'recirculation',
  name: 'Nav, tag and recommended-card clicks',
  auth: 'anon',
  expect: [
    { event: 'nav_clicked', min: 1, props: ['nav_item', 'nav_group'] },
    { event: 'listing_viewed', min: 1, props: ['listing_type', 'listing_value'] },
    { event: 'recommended_clicked', min: 1, props: ['module', 'position', 'target_story_id'] },
    { event: 'tag_clicked', min: 1, props: ['tag', 'tag_type'] },
  ],
  async run(page, ctx) {
    await page.goto('https://inc42.com/', { waitUntil: 'domcontentloaded' });
    await settle(page, 3000);

    await mark(page, 'recirc:nav');
    const nav = await clickFirst(page, ['header nav a', 'nav a[href*="inc42.com"]', 'header a[href*="/features"]']);
    ctx.log(`nav click: ${nav ?? 'NOT FOUND'}`);
    await settle(page, 3000);
    await mark(page, 'recirc:listing');

    const links = await articleLinks(page, 3);
    if (links.length) {
      await page.goto(links[0], { waitUntil: 'domcontentloaded' });
      await settle(page, 3000);
    }

    await mark(page, 'recirc:tag');
    const tag = await clickFirst(page, ['[class*="tag"] a', '[rel="tag"]', 'a[href*="/tag/"]']);
    ctx.log(`tag click: ${tag ?? 'NOT FOUND'}`);
    await settle(page, 2500);
    await page.goBack().catch(() => {});
    await settle(page, 2500);

    await mark(page, 'recirc:recommended');
    const rec = await clickFirst(page, [
      '[class*="recommend"] a', '[class*="read-next"] a', '[class*="related"] a', '[class*="deep-dive"] a',
    ]);
    ctx.log(`recommended click: ${rec ?? 'NOT FOUND'}`);
    await settle(page, 3000);
    return { nav, tag, rec };
  },
};
