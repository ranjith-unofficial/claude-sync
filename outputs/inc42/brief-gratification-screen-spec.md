# Brief completion — gratification screen

**Locked 10 September 2026.** This is the screen after the last card of today’s Brief. It is its own beat. Explore does not start here.

Web and home sell **“Cut the noise. Get the Brief.”** The live app sets that up, then finishing is a dead end: a streak count and “Amazing Start! Think You Can Do It Tomorrow?” That does not pay the promise. This screen does.

**Job of this screen, in order**

1. You finished.
2. The noise was cut — your sectors are covered, by the newsroom, not by a feed.
3. That was worth opening. Here is why, from today’s content.
4. You earned a streak. Come back tomorrow.

Do not print the slogan as the headline. The user already saw it on web and home. Here they should **feel** it: caught up, curated, done. The slogan can sit as a quiet masthead echo, never as the claim.

---

## What this is not

Taken from 26 Figma rounds. Do not reopen these.

| Never | Why |
|---|---|
| A generic “Done” / “Amazing start” | Does not pay the promise |
| “We cut the noise” as hero copy | Asserting the claim undercuts it. Show coverage instead |
| Partial progress ring (tiny filled sliver) | Reads as “you only did 10%” |
| 2×2 stat dashboard | Reads as a report, not a reward |
| Measured session time (“you read this in 78s”) | Users background the app; the number is fragile and easy to get wrong |
| “N sources / N articles aggregated” | Inc42 is an original publisher, not an aggregator |
| `NOT YOUR SECTORS` / `OPTIONAL` | Deficit frame. Makes people feel they missed something they follow |
| Bare personal-record pill (`BEST · 12`) | Demotivating on almost every day |
| Public leaderboard, percentile, Rakhi/medallion badge | Rejected. Daily moment, not a trophy |
| Mixing Explore Trending into this screen | Gratification and discovery got blurred. Separate them |
| “Log in to claim 4 mornings” | Product cannot backfill. Do not promise it |

---

## The screen, top to bottom

Full-bleed brand orange `#EA4B2B`. One glowing focal element — the streak — not a grid of equal tiles. Confetti is allowed (it marks a moment). Decorative rays, seals, and scalloped badges are not.

```
┌─────────────────────────────────┐
│  INC42                     ·    │  masthead, quiet
│                                 │
│           ╭─────╮               │
│           │  4  │  +1 TODAY     │  1. STREAK (the reward)
│           ╰─────╯               │
│         DAY STREAK              │
│                                 │
│  You're caught up on            │  2. CLOSURE (the promise paid)
│  Fintech & E-commerce.          │
│                                 │
│  ₹2,400 Cr of funding in        │  3. WORTH OPENING (today's content)
│  your sectors · 3 filings.      │
│                                 │
│  YOUR SECTORS — ALL COVERED     │  4. PROOF
│  ✓ Fintech 5   ✓ E-commerce 3   │
│                                 │
│  ALSO WORTH KNOWING             │  5. DISCOVERY (additive, after closure)
│  (sector rings, tap to look)    │
│                                 │
│  Tomorrow, 8 AM.                │  6. RETURN
│  Same Brief. New day.           │
└─────────────────────────────────┘
```

One screen. Not a three-step flow. The three beats (we curated → you finished → you earned) are layers on one page, read top to bottom.

---

## 1. Streak — the reward

The streak is the object, not a caption under a checkmark. Show yesterday’s number first, then tick it up on screen, so the +1 is seen happening.

**Default pill:** `+1 TODAY`

Swap the pill only when it is still positive:

| State | Pill | When |
|---|---|---|
| Everyday | `+1 TODAY` | Almost every morning |
| Record in reach | `2 DAYS TO YOUR BEST` | Only when the personal record is ≤3 days away |
| Record broken | `YOUR LONGEST YET` | Only on the day it breaks |

Never show `BEST · 12` on a day that is not the record.

**Week dots** under the number (seven, today lit). The number is the lifetime streak and keeps climbing past 7. The dots are this week only. Do not put both meanings in the ring centre — that is how 4-of-7 and day-12 fight.

Treatments that already work: a large numeral (V26b), or a flame + number (V26a). Pick one and keep it. Do not invent a new badge shape.

---

## 2. Closure — the promise paid

Headline is an **outcome**, naming the sectors they follow:

> You’re caught up on Fintech & E-commerce.

If they follow more than two, name two and fold the rest: `Fintech, E-commerce and 2 more`.

Quiet sector they follow, with nothing today:

> Cleantech was quiet today — that’s worth knowing too.

No sector follows yet (cold start):

> You’re caught up on today’s Brief.

This line is the “cut the noise / curated for you / you finished” payoff. It does not need those words.

---

## 3. Worth opening — from today’s content

One line. Derived at **publish time from the articles**, identical for every reader of that Brief. Never a stopwatch on the user.

Pick **one** of these, in this order, depending on what the Brief actually contains:

| Mode | Line | Needs |
|---|---|---|
| Stakes (preferred when deals exist) | `₹2,400 Cr of funding in your sectors · 3 filings · 2 acquisitions` | Amounts already on the stories |
| Compression | `12,400 words published today. 840 in your Brief.` | CMS word counts |
| Quiet day | `The day was thin. You still have all of it.` | Fallback when stakes are empty |

Do not rotate five personality modes every day. That was the original Satya brief and it went stale as a system. One line, content-true, is enough. If you want variety, rotate **stakes vs compression** by day-of-week, never by random.

Do not ship a cumulative “4 hrs 52 min back” until the base estimate is a real measured number. Until then it is a compounding guess.

---

## 4. Proof — your sectors, all covered

Peach label, then ticked chips with counts:

`YOUR SECTORS — ALL COVERED`  
`✓ Fintech 5` · `✓ E-commerce 3`

This is the shown artifact of curation. It is what “cut the noise” looks like without saying it.

A followed sector with zero stories: dash, not a tick. `Cleantech — quiet today`.

---

## 5. Discovery — after closure, never instead of it

Label is **additive**:

`ALSO WORTH KNOWING`

Not `NOT YOUR SECTORS`. Not `OPTIONAL`. Not `WHAT ELSE MOVED TODAY` without first saying their own sectors are done.

Sector rings (one arc per story in that sector), Lucide icons, tap opens a quick look. Hint: `Tap any sector for a quick look.`

If there is nothing outside their sectors, **omit the whole block**. An empty discovery row is unfinished business.

Explore Trending is **not** this block. If they want more after this screen, a small text link `See the rest of today` can sit under the return line. It is secondary. The screen’s job is already done.

---

## 6. Return — reason to come back tomorrow

Logged-in default:

> Tomorrow, 8 AM. Same Brief. New day.

Only add an unlock when the thing actually exists. Do not promise a Sunday recap that is not built.

---

## Logged in

Everything above, as written.

Streak is saved on the account. The +1 is durable. Tomorrow continues from N+1.

Primary action is implicit: dismiss / swipe up / the system back. Optional secondary: `See the rest of today` (the Also-worth-knowing rail, or Explore).

No login CTA. No “save your streak”.

First morning on an account (streak becomes 1): same screen, numeral ticks `0 → 1`, pill `+1 TODAY`. The closure and worth-opening lines still lead. Do not make day one a tutorial.

---

## Logged out

Same screen, same closure, same worth-opening, same sector proof. The **streak block and the bottom CTA** change. That is the only structural difference.

The product can hold today’s streak until midnight. It cannot backfill yesterday. So the honest object is **1 day, earned, not saved**.

```
           1
      DAY STREAK
     1 TODAY     2 TOMORROW 🔒

  You're caught up on
  Fintech & E-commerce.

  ₹2,400 Cr of funding in
  your sectors · 3 filings.

  YOUR SECTORS — ALL COVERED
  ✓ Fintech 5   ✓ E-commerce 3

  ALSO WORTH KNOWING
  …

  This streak disappears at midnight.
  [ Log in to save your streak ]
  Takes 10 seconds · keeps every morning from here.
```

**Hero number is always 1.** Do not show 4, 7, or “mornings on this phone”. A returning logged-out reader seeing `1` every day is acceptable **because the CTA is the point**: the streak is real, and it is about to vanish. That is more powerful than a fake climbing number the account cannot honour.

**The pair `1 TODAY` (solid) · `2 TOMORROW` (dashed, padlock)** is the return hook. It names what they gain, not only what they lose: log in tonight and tomorrow starts at 2.

**Primary CTA, full width, white on orange:** `Log in to save your streak`

Support line under it: `Takes 10 seconds · keeps every morning from here.`

Do not use a live countdown all day. A ticking `08:42:19` shouts from breakfast. If you want urgency, fire it only after 8 PM, when midnight is actually close: `Log in before midnight`. Until then, T5 (today / tomorrow locked) is enough.

**On successful login from this CTA:** keep them on this same completion screen, tick 1 as saved (do not replay the whole brief), pill becomes `SAVED`. Tomorrow they are a logged-in day-2.

**Do not** drop the streak for logged-out users (“streaks start when you log in”). They already earned today. Hiding it weakens the ask.

---

## Copy bank (use as written)

**Logged in**

| Slot | Copy |
|---|---|
| Headline | You’re caught up on {Sector} & {Sector}. |
| Quiet sector | {Sector} was quiet today — that’s worth knowing too. |
| Cold start | You’re caught up on today’s Brief. |
| Stakes | ₹{amount} Cr of funding in your sectors · {n} filings. |
| Compression | {published} words out today. {brief} in yours. |
| Thin day | The day was thin. You still have all of it. |
| Proof label | YOUR SECTORS — ALL COVERED |
| Discovery label | ALSO WORTH KNOWING |
| Discovery hint | Tap any sector for a quick look. |
| Return | Tomorrow, 8 AM. Same Brief. New day. |
| Pill | +1 TODAY |

**Logged out — extras**

| Slot | Copy |
|---|---|
| Streak label | DAY STREAK |
| Today chip | 1 TODAY |
| Tomorrow chip | 2 TOMORROW |
| Loss line | This streak disappears at midnight. |
| CTA | Log in to save your streak |
| CTA support | Takes 10 seconds · keeps every morning from here. |
| Evening CTA | Log in before midnight |

Masthead may carry `Cut the noise. Get the Brief.` at small size, peach on the second clause. It is branding, not the payoff.

---

## Motion

1. Land on orange.
2. Streak numeral at **yesterday’s** value (logged in) or empty (logged out).
3. Tick to new value with a short burst. Logged out: land on **1**.
4. Headline, then the worth-opening line.
5. Your-sectors chips.
6. Also-worth-knowing, if present.
7. Return line / login CTA last.

Keep it under ~1.2s to the headline. Reduced-motion: skip the tick, show the final number.

---

## Data this screen needs

All of this already exists or is computable at publish. No new session timer.

| Field | Used for |
|---|---|
| `streak_count` | Hero number (logged in) |
| `streak_personal_best` | Pill state B/C only |
| `followed_sectors[]` | Headline + proof chips |
| `stories_per_followed_sector` | Chip counts; quiet-day dash |
| `stories_per_other_sector` | Also-worth-knowing rings |
| `brief_funding_inr` / filings / acquisitions | Stakes line |
| `words_published_today` / `words_in_brief` | Compression line |
| `is_logged_in` | Which bottom block |
| `local_hour` | Evening login CTA after 8 PM |

`session_duration_sec` is **not** used on this screen.

---

## How the two states differ

| | Logged in | Logged out |
|---|---|---|
| Streak number | Real account streak, ticks up | Always **1**, earned just now |
| Pill | `+1 TODAY` (or record states) | `1 TODAY` · `2 TOMORROW` locked |
| Closure + worth opening + proof | Same | Same |
| Also worth knowing | Same | Same |
| Bottom | Tomorrow, 8 AM | Login to save this streak |
| Primary action | Dismiss | `Log in to save your streak` |
| What happens at midnight | Streak persists | Streak drops unless they logged in |

The logged-out version is not a poorer screen. It is the same reward, with the save still in their hands. That is why it is more powerful than hiding the streak until after login.
