import { mark, snapshot, settle, clickFirst, typeInto, articleLinks } from '../lib/actions.mjs';

/* Identity findings (email-as-distinct_id, stale person props, CIO never identified,
   posthog.reset on logout) are only observable in an authenticated session.
   Set INC42_EMAIL / INC42_PASSWORD in .env to enable; skips cleanly otherwise. */
export default {
  id: 'logged-in',
  name: 'Authenticated session — identity, save, follow, logout',
  auth: 'user',
  expect: [
    { event: 'sign_in_completed', min: 1, props: ['method', 'is_new_account'] },
    { event: 'story_saved', min: 1, props: ['source'] },
    { event: 'entity_followed', min: 1, props: ['entity_type', 'entity_id'] },
    { event: 'signed_out', min: 1 },
  ],
  async run(page, ctx) {
    const email = process.env.INC42_EMAIL, pass = process.env.INC42_PASSWORD;
    if (!email || !pass) return { skipped: 'INC42_EMAIL / INC42_PASSWORD not set — identity checks not run' };

    await page.goto('https://inc42.com/', { waitUntil: 'domcontentloaded' });
    await settle(page, 3000);
    await mark(page, 'auth:open-modal');
    await clickFirst(page, ['text=/sign in/i', 'text=/log ?in/i', '[class*="login"] button', 'header a[href*="login"]']);
    await settle(page, 4000);

    await mark(page, 'auth:email');
    const typedEmail = await typeInto(page, ['input[type="email"]', 'input[name="username"]', 'input[name="email"]'], email);
    if (!typedEmail) return { skipped: 'email field not reachable in the auth widget' };
    await clickFirst(page, ['button[type="submit"]', 'text=/continue/i', 'text=/next/i']);
    await settle(page, 3500);

    await typeInto(page, ['input[type="password"]', 'input[name="password"]'], pass);
    await clickFirst(page, ['button[type="submit"]', 'text=/log ?in/i', 'text=/sign in/i']);
    await settle(page, 7000);
    await mark(page, 'auth:signed-in');
    const after = await snapshot(page, 'signed-in');
    ctx.log(`distinct_id after sign-in: ${after?.posthog_distinct_id ?? 'null'}`);
    ctx.log(`customer.io user id: ${after?.cio_user_id ?? 'null'}`);

    // save + follow on an article
    const links = await articleLinks(page, 3);
    if (links.length) {
      await page.goto(links[0], { waitUntil: 'domcontentloaded' });
      await settle(page, 3000);
      await mark(page, 'auth:save-story');
      ctx.log(`save: ${await clickFirst(page, ['[class*="save"]', '[class*="bookmark"]', 'button[aria-label*="ave"]']) ?? 'NOT FOUND'}`);
      await page.waitForTimeout(2500);
      await mark(page, 'auth:follow');
      ctx.log(`follow: ${await clickFirst(page, ['text=/start following/i', 'text=/^follow$/i', '[class*="follow"] button']) ?? 'NOT FOUND'}`);
      await page.waitForTimeout(2500);
    }

    await mark(page, 'auth:logout');
    await page.goto('https://inc42.com/my-inc42/', { waitUntil: 'domcontentloaded' }).catch(() => {});
    await settle(page, 3000);
    await clickFirst(page, ['text=/log ?out/i', 'text=/sign out/i', '[class*="logout"]']);
    await settle(page, 6000);
    const post = await snapshot(page, 'signed_out');
    ctx.log(`distinct_id after logout: ${post?.posthog_distinct_id ?? 'null'}  (should be a fresh anon id)`);
    return { signedIn: after?.posthog_distinct_id ?? null, afterLogout: post?.posthog_distinct_id ?? null };
  },
};
