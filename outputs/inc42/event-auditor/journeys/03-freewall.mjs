import { mark, snapshot, settle, clickFirst, isVisible, articleLinks } from '../lib/actions.mjs';

export default {
  id: 'freewall',
  name: 'Freewall / register-gate funnel',
  auth: 'anon',
  expect: [
    { event: 'freewall_shown', min: 1, props: ['trigger', 'quota_used'], note: '12-Aug walk saw ZERO on lock render' },
    { event: 'freewall_cta_clicked', min: 1 },
    { event: 'sign_in_prompt_shown', min: 1, propGroups: ['Super', 'Story'], note: 'Meta gets 25 props, PostHog gets 2' },
  ],
  // Reading N articles is what trips the quota; the exact N is the open question in the spec.
  async run(page, ctx) {
    await page.goto('https://inc42.com/', { waitUntil: 'domcontentloaded' });
    await settle(page, 3000);
    const links = await articleLinks(page, 15);
    if (!links.length) return { skipped: 'no article links' };

    let lockedAt = null;
    for (let i = 0; i < links.length; i++) {
      await page.goto(links[i], { waitUntil: 'domcontentloaded' });
      await settle(page, 3000);
      await mark(page, `freewall:article-${i + 1}`);
      await page.evaluate(() => window.scrollTo({ top: document.body.scrollHeight * 0.6 })).catch(() => {});
      await page.waitForTimeout(2000);

      // Structural selectors only. A bare "continue reading" text match hits every
      // card link on the page and reports a freewall that never rendered.
      const lock = await isVisible(page, [
        '[class*="freewall-lock"]', '[class*="lock-model"]', '[class*="register-lock"]',
        '[class*="freewall"]', 'text=/sign in to continue reading/i',
      ]);
      if (lock) { lockedAt = { index: i + 1, url: links[i], selector: lock }; break; }
    }

    if (!lockedAt) {
      ctx.log(`freewall never appeared in ${links.length} articles — quota may be higher, variant-gated, or off`);
      return { lockedAt: null, articlesRead: links.length };
    }

    ctx.log(`freewall tripped on article #${lockedAt.index} (${lockedAt.selector})`);
    await mark(page, 'freewall:shown');
    await snapshot(page, 'freewall-shown');
    await page.waitForTimeout(1500);

    await mark(page, 'freewall:cta');
    const cta = await clickFirst(page, [
      'text=/sign in to inc42/i', 'text=/sign in/i', '[class*="freewall"] button', '[class*="lock"] a',
    ]);
    await settle(page, 4000);
    await mark(page, 'freewall:modal-open');
    await snapshot(page, 'login-modal');

    const modal = await isVisible(page, ['[class*="auth0"]', '[class*="login-modal"]', '[role="dialog"]']);
    ctx.log(`login modal: ${modal ?? 'NOT DETECTED'}`);

    await page.waitForTimeout(2000);
    await mark(page, 'freewall:modal-close');
    await clickFirst(page, ['[class*="close"]', 'button[aria-label*="lose"]', '[role="dialog"] button']);
    await settle(page, 2000);
    return { lockedAt, cta, modal };
  },
};
