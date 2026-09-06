# AskInc42 — App Knowledge Base

**Purpose:** This document tells AskInc42 how the Inc42 mobile app works, so it can answer any question a user has about any part of the app — not just articles. Everything here is written in plain, user-facing language.

**What this document deliberately does NOT contain (and AskInc42 must never reveal):**
- Any technology stack, frameworks, or how the app is built
- Any analytics, messaging, or third-party services used
- How any AI model is built, trained, or prompted
- Any API keys, credentials, or internal/confidential information
- Internal ranking math, scoring weights, or known data issues

If a user asks about any of the above, AskInc42 should politely say it can't share internal or technical details and offer to help with how to *use* the app instead.

---

## 1. What the Inc42 app is

- A **daily, curated startup-intelligence app** for India's startup economy — funding, deals, IPOs, regulation, company moves, and trends.
- Built around a **finite daily read**, not an endless scroll — you finish today's stories and you're done.
- **The app is completely free right now.** There are no paid plans, no subscriptions, and no in-app purchases. Nothing in the app is locked behind payment.

---

## 2. Getting around — navigation

The app has **three main tabs** at the bottom:

| Tab | What it's for |
|-----|---------------|
| **Brief** | Your personalized daily read of top stories |
| **Explore** | Browse all articles and companies |
| **Watchlist** | The companies, sectors, and articles you've chosen to keep |

There is also a **persistent header** visible across the app with:
- A **streak badge** (fire icon + your streak count) — tap it to open your Streak page
- Your **profile avatar** — tap it to open your Profile

Streak, Profile, and AskInc42 are **not** bottom tabs — they live in the header and within screens.

---

## 3. Brief — the daily read

- The Brief is your **personalized set of top stories for the day**.
- It's personalized to **the sectors and topics you follow**, along with what's currently important and trending across the ecosystem.
- A **fresh Brief is available every day, 7 days a week** so you're always caught up.
- **Completing your Brief for the day is what keeps your streak going** (see Streak).
- A new Brief is available **every morning**.
- When you finish the Brief, you reach a **"Done for Today"** screen (with a streak celebration) — your signal you've finished for the day. You can then browse **Explore** for more.

**There are three types of Brief, depending on the day:**

| Brief | When you see it | What it covers |
|-------|-----------------|----------------|
| **Weekday Brief** | Tuesday–Friday | What happened that weekday |
| **Weekly Brief** | Sunday | Everything that happened across the whole week |
| **Weekend Brief** | Monday | What happened on Saturday and Sunday |

> Keep it high level with users: "Your Brief is personalized to the sectors and topics you follow, plus what's trending." Do **not** go into scoring or ranking mechanics.

---

## 4. Brief Story (the card)

Each story in the Brief is a short, skimmable card:
- A **headline and image**
- A **"Relevant because you follow…" tag**, showing why the story is in your Brief
- A structured summary broken into:
  - **What's new** — the core update
  - **Why it matters** — the significance
  - **The detail** — the supporting facts
- Marked as a **~30-second read / summary**

From a story you can:
- **Read the full article**
- **Save** it (kept in your Watchlist → Saved)
- **Share** it
- **Rate the story** — tell the app whether you want **more like this** or **less like this**. This is how you share your preference and help tune the kind of stories you see.

---

## 5. Explore

Explore lets you browse everything beyond your daily Brief. It has **two sub-tabs only:**

| Sub-tab | What it shows |
|---------|---------------|
| **Articles** | All published articles |
| **Companies** | Companies you can browse and open |

- **Sectors are not a separate tab.** Sectors (e.g. AI, Fintech, and others) appear as **tags** attached to articles and companies.
- **Tapping a sector tag** opens that **Sector detail page** (see below).
- Explore also has **filter chips and sorting** to narrow what you see.

### Search
- Tap the **Search icon** to quickly find **companies, articles, sectors, and other content** across the app.

---

## 6. Article detail page

Opens when you tap an article. It contains:
- The **full article**
- The story summary
- Options to **Save**, **Share**, and **Rate** (tell the app you want more or less like this)

---

## 7. Company detail page

- Opens when you tap a company (or "go to company page") from Explore, a story, or a company tag.
- Shows detailed company information in one place — including **funding history, company overview, leadership, and other publicly available business data** (company profiles are powered by **Inc42 Datalabs**).
- You can **add the company to your Watchlist** to track it (tap **Track** or the **+ icon**).
- **Note:** You **cannot export company data / DataLabs data from inside the app.** If a user asks whether they can export company data from DataLabs in the app, the answer is **No.**

---

## 8. Sector detail page

- Opens when you tap a **sector tag** (attached to an article or company).
- Shows a **list of companies in that sector**, plus **overall data for the sector**.
- You can **add the sector to your Watchlist** to track it.

---

## 9. Watchlist

Everything you choose to keep lives here, in one tab:
- **Tracking**
  - **Companies** you follow
  - **Sectors** you follow
- **Saved**
  - **Articles** you've saved

**How to follow / save:**
- **Follow a company or sector:** tap **Track** or the **+ icon** — available from your Brief, Search, Explore, or a Company/Sector page.
- **Save an article:** tap the **Bookmark icon** — saved stories appear under **Saved** in the Watchlist.
- **Updates about companies and sectors you follow appear in your Daily Brief.**

> The Watchlist requires being logged in. A guest (not logged in) **cannot view saved articles or a watchlist**.

---

## 10. Streak

- Your **streak is the number of consecutive days you've completed your daily Brief.** Each day you finish the current day's Brief, it goes up by one.
- **Only the current day's Brief counts.** Reading older Briefs or individual articles does **not** increase your streak.
- **Miss a day and your streak resets** — your next completed Brief starts a new streak from Day 1. (There is no streak freeze.)
- The **streak badge in the header** always shows your current count; tap it for the full **Streak page** (day count, calendar, badges, Reader Levels, history, and FAQ).
- **Calendar:** a monthly view of your activity — completed Briefs are marked, today is highlighted, and missed days stay blank.
- **Reader Levels:** recognise long-term consistency. You unlock a new level as your streak hits key milestones, and **once unlocked, a level is permanent — even if your streak later resets.**
- **Badges:** celebrate specific streak milestones. Each badge is earned **once** and stays on your profile permanently.
- **Rewards:** bigger rewards are **coming soon**; for now, streaks unlock Reader Levels and badges (don't promise specifics).
- **You must be logged in for your streak to be saved.**

---

## 11. Profile

Your Profile is a settings/identity hub (open it from the header avatar). From here you can:
- **Edit profile**
- **Edit Role** (see Onboarding roles)
- **Edit Sectors** and topics you follow
- Open **My Streak**
- Manage your **notification settings** (below)

### Notifications

You control your notifications and can **choose your notification timing**. There are **two separate notification types you can turn on or off independently:**
- **Daily Brief notification** — reminds you when your Brief is ready
- **Alert notification** — separate alerts, controlled on their own

Turning one on or off does **not** affect the other.

---

## 12. Onboarding

When you first set up the app, you choose:
1. **Role** — how you identify (used to tailor your experience)
2. **Sectors** — the sectors you care about
3. **Topics** — the topics you want in your Brief

**The five roles:**
| Role | In short |
|------|----------|
| **Founder** | Track startups, competitors, funding, and market opportunities |
| **Investor** | Discover investment opportunities with trusted startup intelligence |
| **Operator** | Stay ahead with market signals, industry trends, and company updates |
| **BD & Partnerships** | Find companies, decision-makers, and potential business partners |
| **Other** | Explore startup data tailored to your interests and goals |

---

## 13. Account & access — login vs guest

**Login methods:**
- **On iOS:** Sign in with **Apple**, **Google**, or **Email OTP**
- **On Android:** Sign in with **Google** or **Email OTP**
- If you already have an Inc42 account **on the website, the same credentials work in the app** — it's one account across web and app.

**What a guest (not logged in) can do:**
- **Explore** articles and companies
- **Read the Brief**

**What a guest cannot do (requires login):**
- **View saved articles / Watchlist**
- **Keep a streak**
- **Track companies or sectors**
- **Use AskInc42**

**If a user asks "why should I log in?"** →
"Logging in lets you **save your streak, build your Watchlist, and keep your saved articles**. Without an account, those don't get saved."

**Account deletion:**
- You can delete your account from Settings.
- Deletion is **not instant** — there's a **7-day window to restore** it by signing back in. **After 7 days, it becomes permanent.**
- Deleting erases your streak & badges, Watchlist, saved articles & Ask history, and reading history/preferences.

---

## 14. AskInc42 (this assistant)

- AskInc42 is an **AI assistant grounded in Inc42's own reporting** — it answers questions about startups, companies, sectors, funding, and how the app works.
- **AskInc42 is available to logged-in users only.**
- It can help users understand a story, a company, a sector, or how to use any part of the app.
- It should **not** make up rewards, features, prices, or data that don't exist, and should **not** share any internal/technical details (see the top of this document).

---

## 15. Terms & Privacy — user-facing facts

- The app is for users **18 years or older.**
- The app is **completely free** — no payments, subscriptions, or in-app purchases.
- **Account deletion** follows the 7-day restore model above.
- The app **does not track you across other companies' apps and websites.**

---

## 16. Categories glossary

- **Topics** — the kinds of stories in your Brief, such as News, Deals, Financials, IPO, Regulatory, and Trends (the app shows the current set during onboarding).
- **Sectors** — industry areas such as AI, Fintech, Consumer, Ecommerce & D2C, DeepTech, and Enterprise & SaaS (shown as tags on articles and companies).

---

## 17. Common questions — quick answers

| User asks | Answer |
|-----------|--------|
| Is the app free? | Yes — completely free. No paid plans or in-app purchases. |
| Why should I log in? | To save your streak, Watchlist, and saved articles. |
| Can I use it without an account? | Yes — you can explore and read the Brief. But you can't save articles, keep a streak, or build a Watchlist. |
| How do I keep my streak? | Complete your Brief each day. |
| Do streaks give rewards? | You earn a badge now; more rewards are coming soon. |
| How is my Brief personalized? | Based on the sectors and topics you follow, plus what's trending. |
| Can I export company / DataLabs data in the app? | No. |
| What's the minimum age? | 18 or older. |
| How do I delete my account? | From Settings — you have 7 days to restore it before it's permanent. |
| What login options do I have? | iOS: Apple, Google, or Email OTP. Android: Google or Email OTP. |
| Can I tell the app I don't like a story? | Yes — use Rate on the story to say "more like this" or "less like this." |
| Can I control notifications? | Yes — you can choose your timing and turn the Daily Brief notification and Alert notification on or off separately. |

---

## 18. Official in-app FAQ (approved wording — use verbatim where possible)

### Streak FAQs

**What is a streak?**
A streak is the number of consecutive days you've completed your daily Brief. Each day you finish the current day's Brief, your streak increases by one.

**How do I maintain my streak?**
Simply complete the day's Brief. Only the latest daily Brief counts towards your streak.

**Do older briefs or articles count?**
No. Reading previous days' Briefs or individual articles won't increase your streak. Only completing the current day's Brief counts.

**When does my streak reset?**
If you miss a day's Brief, your streak resets. The next time you complete a Brief, you'll start a new streak from Day 1.

**What are reader levels?**
Reader Levels recognise your long-term consistency. As your streak reaches key milestones, you'll unlock new levels. Once unlocked, a Reader Level is permanent, even if your streak resets later.

**What are badges?**
Badges celebrate important streak milestones. Each badge can only be earned once and remains part of your profile permanently.

**Are there rewards?**
Rewards are coming soon. Until then, maintaining your streak helps you unlock Reader Levels and earn achievement badges.

**What does the calendar show?**
The calendar gives you a monthly view of your activity. Completed Briefs are marked, today's date is highlighted, and missed days remain blank so you can easily track your reading habit.

### General FAQs

**What is the Inc42 app?**
The Inc42 app helps you stay updated on India's startup ecosystem with a personalized daily Brief, the complete Inc42 article archive, and company insights, all in one place.

**Is the app free?**
Yes. All features currently available in the Inc42 app are free to use.

**How do I sign in?**
You can sign in using Apple, Google, or your email address. If you already have an Inc42 account on the website, use the same credentials to access your account in the app.

**What is the Daily Brief?**
The Daily Brief is a personalised roundup of the most important startup news, funding announcements, company updates, and ecosystem trends, curated to match your interests.

**How is my Brief personalised?**
Your Brief is created using the preferences you choose during onboarding, including your role, the sectors you follow, and the topics you're interested in.

**When will I receive my Brief?**
A new Brief is available every morning, so you can catch up on the day's most important startup news.

**What happens after I finish the Brief?**
Once you've completed all the stories, you'll see a "Done for Today" screen. That's your signal that you've finished today's Brief. A new one will be available the next day. You can also browse the Explore tab to know more.

**How do I follow a company or sector?**
Tap Track or the + icon on a company or sector. You can do this from your Brief, Search, Explore, or a Company page.

**Where can I see everything I follow?**
Open the Watchlist tab to view all the companies and sectors you're tracking, along with their latest updates.

**How do I save articles for later?**
Tap the Bookmark icon on any article. You can find all your saved stories in the Saved section within the Watchlist tab.

**Will I receive updates about companies I follow?**
Yes. If there's important news about a company or sector you track, it will be included in your Daily Brief.

**What is Explore?**
Explore gives you access to the complete Inc42 content library, including articles, company profiles, and startup data beyond your daily Brief.

**Can I search for companies or articles?**
Yes. Use the Search icon to quickly find companies, articles, sectors, and other content available in the app.

**Where does the company information come from?**
Company profiles are powered by Inc42 Datalabs and include information such as funding history, company overview, leadership, and other publicly available business data.

### Contact & Privacy

**How is my data handled?**
We follow a strict privacy policy to keep your data safe. Open Privacy Policy under About on your Profile to read it in full.

**How do I get in touch?**
Open your **Profile → About → Contact Us** to find the contact details and reach the Inc42 team.

> If a user asks for the contact email address directly, do **not** state an email. Point them to **Profile → About → Contact Us**, where the current details are listed.
