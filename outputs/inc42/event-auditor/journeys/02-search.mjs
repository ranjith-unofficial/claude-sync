import { mark, settle, clickFirst, typeInto } from '../lib/actions.mjs';

export default {
  id: 'search',
  name: 'Search funnel — open, query, click result',
  auth: 'anon',
  expect: [
    { event: 'search_initiated', min: 1 },
    { event: 'search_performed', min: 1, props: ['query', 'search_scope', 'result_count'] },
    { event: 'search_result_clicked', min: 1, props: ['query', 'position', 'result_type'] },
  ],
  async run(page, ctx) {
    await page.goto('https://inc42.com/', { waitUntil: 'domcontentloaded' });
    await settle(page, 3000);

    await mark(page, 'search:open');
    const opened = await clickFirst(page, [
      '[class*="search"] button', 'button[aria-label*="earch"]', 'a[href*="/search"]',
      '[class*="search-icon"]', 'svg[class*="search"]', 'header [class*="search"]',
    ]);
    ctx.log(`search opener: ${opened ?? 'NOT FOUND'}`);
    await page.waitForTimeout(2500);

    await mark(page, 'search:type');
    const typed = await typeInto(page, [
      'input[type="search"]', 'input[placeholder*="earch"]', 'input[name*="s"]', '[class*="search"] input',
    ], 'fintech funding');
    ctx.log(`search input: ${typed ?? 'NOT FOUND'}`);
    if (!typed) return { skipped: 'search input not reachable' };

    await page.waitForTimeout(2500);
    await mark(page, 'search:submit');
    await page.keyboard.press('Enter');
    await settle(page, 4000);

    await mark(page, 'search:result-click');
    const clicked = await clickFirst(page, [
      '[class*="result"] a', '[class*="search"] a[href*="inc42.com/"]', 'article a',
    ]);
    ctx.log(`result click: ${clicked ?? 'NOT FOUND'}`);
    await settle(page, 3000);
    return { opened, typed, clicked };
  },
};
