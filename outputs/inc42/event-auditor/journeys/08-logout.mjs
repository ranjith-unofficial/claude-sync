import { mark, snapshot, settle, clickFirst } from '../lib/actions.mjs';

/* Separate from 06 so a failed logout cannot invalidate the save/follow evidence,
   and so the saved session survives for the next run.
   Tests 12-Aug finding #16: posthog.reset() is not called on logout. */
export default {
  id: 'logout',
  name: 'Authenticated — sign out and identity reset',
  auth: 'user',
  // Signing out invalidates the saved session server-side, so every later --auth run would
  // silently degrade to anonymous. Opt in with --include-logout, then re-run node login.mjs.
  optIn: 'include-logout',
  expect: [
    { event: 'signed_out', min: 1 },
  ],
  async run(page, ctx) {
    await page.goto('https://inc42.com/my-inc42/', { waitUntil: 'domcontentloaded' });
    await settle(page, 4000);
    const before = await snapshot(page, 'before-logout');
    ctx.log(`distinct_id before  : ${before?.posthog_distinct_id ?? 'null'}`);

    await mark(page, 'auth:open-menu');
    await clickFirst(page, ['[class*="avatar"]', '[class*="profile"]', 'header [class*="user"]']);
    await page.waitForTimeout(2000);

    await mark(page, 'auth:logout');
    const out = await clickFirst(page, ['text=/log ?out/i', 'text=/sign out/i', '[class*="logout"]', 'a[href*="logout"]']);
    ctx.log(`logout control      : ${out ?? 'NOT FOUND'}`);
    await settle(page, 8000);

    /* Did the sign-out actually take effect? Without this, "Logout never fired" is
       indistinguishable from "the logout button did nothing". */
    const cookies = await page.context().cookies('https://inc42.com');
    const loggedOut = !cookies.some((c) => ['user_logged_in', 'current_user_id'].includes(c.name)
      && c.value && c.value !== 'deleted');
    ctx.log(`session ended      : ${loggedOut ? 'yes — auth cookies cleared' : 'NO — still authenticated'}`);

    const after = await snapshot(page, 'signed_out');
    ctx.log(`distinct_id after   : ${after?.posthog_distinct_id ?? 'null'}`);
    const leaked = Boolean(after?.posthog_distinct_id && before?.posthog_distinct_id
      && after.posthog_distinct_id === before.posthog_distinct_id);
    ctx.log(leaked
      ? 'RESET NOT CALLED — identity survived logout'
      : 'identity changed after logout (reset appears to work)');

    return {
      before: before?.posthog_distinct_id ?? null,
      after: after?.posthog_distinct_id ?? null,
      out, loggedOut,
      resetMissing: loggedOut && leaked,   // only meaningful if the sign-out actually happened
    };
  },
};
