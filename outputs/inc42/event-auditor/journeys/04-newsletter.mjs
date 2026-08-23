import { mark, settle, clickFirst, typeInto, isVisible } from '../lib/actions.mjs';

export default {
  id: 'newsletter',
  name: 'Newsletter prompt → subscribe (stops before submit)',
  auth: 'anon',
  expect: [
    { event: 'newsletter_prompt_shown', min: 1, props: ['newsletter_name', 'placement'] },
    { event: 'newsletter_subscribed', min: 0, note: 'NOT submitted — we do not create real subscriptions' },
  ],
  async run(page, ctx) {
    await page.goto('https://inc42.com/newsletter/', { waitUntil: 'domcontentloaded' }).catch(() => {});
    await settle(page, 3500);
    await mark(page, 'newsletter:page');

    const prompt = await isVisible(page, [
      '[class*="newsletter"]', 'input[type="email"]', 'text=/daily brief/i',
    ]);
    ctx.log(`newsletter prompt: ${prompt ?? 'NOT FOUND'}`);

    // Type but DO NOT submit — we are auditing the prompt-shown event, not creating a subscriber.
    const typed = await typeInto(page, ['input[type="email"]'], 'audit-probe@example.invalid');
    await page.waitForTimeout(1500);
    await mark(page, 'newsletter:typed-not-submitted');

    return { prompt, typed, submitted: false };
  },
};
