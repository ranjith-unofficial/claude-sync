# Inc42 DataLabs — Knowledge Base

**Source S3 · v1 · Verified against live site 16 Aug 2026 · Owner: Ashish · Review: monthly**

Everything AskInc42 knows about **Inc42 DataLabs** — the startup intelligence platform behind company profiles on the web and in the app. Written in plain, user-facing language.

**Provenance:** live pages on `inc42.com` verified 16 Aug 2026, cross-read against Utkarsh's *DataLabs Master Context v4* (21 Apr 2026). Where the two disagree, the **live site wins** and the conflict is flagged in §12. Everything commercial, internal or strategic in that source document has been deliberately excluded.

**Status tags used below:** `[LIVE]` shipped · `[LIMITED]` shipped but capped or partial · `[COMING]` announced, not yet live.

---

## Never disclose

This is the strictest never-disclose list in the knowledge set, because the internal source behind it is dense with material AskInc42 must never repeat.

| Category | Examples |
|---|---|
| **Anything commercial** | Subscription cost, plan names with prices, credit costs, top-up packs, competitor pricing, trial length |
| **Business metrics** | Registered users, MAU/WAU, activation rates, conversion rates, subscriber counts, revenue, traffic figures, AI citation rates |
| **Strategy** | Competitive positioning against named rivals, growth targets, lead-generation intent, experiment gates or kill criteria |
| **People & org** | Team size, restructuring, role owners, reporting lines |
| **Technology** | Frameworks, databases, search infrastructure, auth providers, analytics tools, AI gateways, hosting or proxy architecture |
| **Roadmap internals** | Ship dates, sprint plans, backlog, internal document names or links |

If asked about any of it: say you can't share internal or commercial details, and offer to help with what DataLabs *does* instead.

---

## 1. What DataLabs is

- **Inc42 DataLabs is India's startup intelligence platform** — structured data on Indian startups, investors, funding rounds, acquisitions, people and sectors, built on Inc42's newsroom.
- It turns startup information into something searchable and comparable: who a company is, who funded it, how much, when, who works there, and how it's trending.
- It is **the data layer behind Inc42** — company profiles in the Inc42 app are powered by DataLabs, and so are company, person and industry pages on the website.
- Positioned publicly as *"India's #1 Startup Intelligence Platform."*

## 2. Coverage

| Entity | Coverage |
|---|---|
| Startups / companies | **75,000+** |
| Investors | **3,000+** |
| Funding rounds | **20,000+** |
| Industries / sectors | **400+** |
| Acquisitions | Tracked as a searchable entity |
| Key people | Founders, executives, board members and investors, as dedicated profiles |

⚠️ **Use these figures, and only these.** They are what the public DataLabs page states. Internal counts run higher on some entities — never quote a higher number than the site shows, and never present a range. If pushed for precision, say coverage grows continuously and point to the site.

## 3. Access tiers — described as capability, never as price

Three levels. **State what each can do; never state what any of them costs.**

### 3.1 Guest — not logged in `[LIVE]`

- Basic company profile data — name, sector, description, founding year, headquarters, founders, total funding summary
- Headline signals on a profile
- General news and feed content
- **Limited depth:** detailed financial data is restricted, and search results are limited beyond the first few pages

### 3.2 Registered — free `[LIVE]`

Registration is free and unlocks the substance of the platform:

- **All company profiles** with full funding rounds, investor names, key people and signals
- **Full investor portfolios** — holdings, co-investors, investment focus
- **All search filters**, basic and advanced
- **Unlimited profile views** — no monthly cap
- **Full pagination** on search results and tables
- **Full Inc42 editorial access**
- **Ask DataLabs** `[LIMITED]` — the AI assistant, with a capped number of queries

### 3.3 Pro `[LIVE]`

Everything in the free tier, plus:

- **Financial statements and regulatory filings** — P&L, balance sheet, revenue, cash flow, MCA documents
- **Exports and downloads** — CSV, Excel, PDF, company snapshots, chart and table downloads
- **Cap tables and valuations** — ownership and valuation history
- **Verified contact information** for founders and executives
- **Custom alerts** on saved searches and tracked entities

Exports, contact reveals and document downloads draw on a **monthly allowance**. Describe it as an allowance — **never state its size, its unit costs, or the cost of topping it up.**

A **trial of Pro** exists. ⚠️ **Do not state its length** — see §12.

> **The line to hold:** "Is X available on the free tier?" is answerable. "What does Pro cost?" is a redirect to the DataLabs pages. See `06_Response_Rules.md`.

## 4. Company profile

The most-used surface on DataLabs. Five tabs:

| Tab | What's on it |
|---|---|
| **Overview** | Description, founding year, headquarters, founders, sector tags, headline signals |
| **Financials** | Revenue, growth, and financial statements where available |
| **Funding** | Funding rounds with dates, stages, amounts and investor names |
| **Cap Table** | Ownership and valuation history |
| **Key People** | Founders, executives and board members |

Company pages also carry **recent Inc42 reporting on that company** — the editorial layer is part of the profile, not separate from it.

## 5. Signals

Signals are the momentum indicators shown on company cards and profiles. This is the most distinctive thing about a DataLabs profile and worth explaining well:

| Signal | What it tells you |
|---|---|
| **Funding stage** | Where the company is in its funding journey — e.g. Series B, debt financing |
| **Total funding** | Cumulative capital raised |
| **Last funding date** | Recency of the most recent round |
| **Revenue + YoY change** | Latest reported revenue and how it moved year on year |
| **Investors** | Who has backed the company, and how many |
| **Employee count + 90-day change** | Headcount and its recent direction — a hiring or contraction signal |
| **Web traffic + 30-day change** | Monthly traffic and its recent direction — a demand signal |
| **Glassdoor rating + review count** | Employee sentiment |

**How to explain signals to a user:** they answer "is this company moving, and which way" without reading a single article. Headcount and traffic changes are the two that show momentum earliest.

## 6. Investor and person profiles

**Investor profile** — overview, full portfolio, co-investors, and investment focus. Searchable in its own right with dedicated filters.

**Person profile** — dedicated pages for founders, executives, board members and investors, covering role, company affiliation and professional background.

## 7. Search and discovery

| Surface | What it does | Status |
|---|---|---|
| **Company search** | The main search — many filters across sector, stage, funding, financials, signals and location. Card or list view | `[LIVE]` |
| **Investor search** | Filtered investor discovery | `[LIVE]` |
| **Funding rounds search** | Search rounds directly rather than companies | `[LIVE]` |
| **Acquisitions search** | Search M&A activity | `[LIVE]` |
| **Feed** | A running view of ecosystem activity | `[LIVE]` |
| **Ask DataLabs** | Natural-language questions over DataLabs data | `[LIMITED]` |
| **Unified global search** | One search across all entity types | `[COMING]` |

**Research surfaces:** Reports (Inc42's research publications) · Industries (sector-level pages) · Locations.

## 8. Tracking

| Feature | What it does | Status |
|---|---|---|
| **Watchlist** | Star companies to follow them | `[LIVE]` |
| **Custom lists** | Build and manage your own named lists | `[LIVE]` |
| **Saved searches** | Save any filter configuration and return to it | `[LIVE]` |
| **Alerts** | Notifications on saved searches and tracked entities | Pro |

## 9. Where DataLabs lives

**DataLabs content sits on `inc42.com` itself, not on a separate subdomain.** This matters for every link AskInc42 gives:

| Content | URL pattern |
|---|---|
| Company profile | `inc42.com/company/{slug}/` |
| Person profile | `inc42.com/person/{slug}/` |
| Industry / sector | `inc42.com/industry/{slug}/` |
| Reports | `inc42.com/reports/{slug}/` |
| Curated lists | `inc42.com/lists/{slug}/` |
| DataLabs home | `inc42.com/datalabs/` |

**Never send a user to a `datalabs.inc42.com` URL.** Never describe the hosting arrangement — just use the right link.

## 10. DataLabs and the Inc42 app

- **Company profiles in the app are powered by DataLabs** — funding history, company overview, leadership and other publicly available business data.
- **You cannot export company or DataLabs data from inside the app.** If asked, the answer is **No**, and it stays No regardless of tier.
- Sector pages in the app draw on the same sector structure.
- The app itself is **completely free with no in-app purchases** — a DataLabs subscription is a separate thing on the web, and the app never sells it. See `01_App_Knowledge.md`.

## 11. Quick answers

| User asks | Answer |
|---|---|
| What is DataLabs? | Inc42's startup intelligence platform — structured data on Indian startups, investors, funding rounds, acquisitions, people and sectors, built on Inc42's newsroom. |
| How many companies does it cover? | 75,000+ companies, 3,000+ investors, 20,000+ funding rounds, 400+ sectors. |
| Is DataLabs free? | Yes — registration is free and unlocks all company profiles, full funding rounds, investor portfolios, all search filters and unlimited profile views. A paid Pro tier adds financial statements, exports, cap tables and verified contacts. **No amounts.** |
| What do I get without an account? | Basic company data and headline signals, with limited depth and limited search pagination. Registering is free and removes those limits. |
| What does Pro add? | Financial statements and filings, exports and downloads, cap tables and valuations, verified contacts, and custom alerts. For what it costs, check the DataLabs pages. |
| How much is Pro? | Redirect to the DataLabs pages. **Never a number.** |
| Is there a trial? | Yes, Pro has a trial — details are on the DataLabs pages. **Never state its length.** |
| Can I export data? | On Pro, on the web — CSV, Excel, PDF and company snapshots. **Not from inside the Inc42 app**, on any tier. |
| What are signals? | Momentum indicators on a company — funding stage, total funding, last funding date, revenue and YoY change, investors, employee count and 90-day change, web traffic and 30-day change, and Glassdoor rating. |
| What's on a company profile? | Five tabs — Overview, Financials, Funding, Cap Table, Key People — plus recent Inc42 reporting on that company. |
| Can I track companies? | Yes — Watchlist, custom lists and saved searches. Alerts are a Pro feature. |
| Where does the data come from? | Inc42's newsroom and its maintained startup database, covering publicly available business information. |
| How do I cancel / get a refund? | "I can't help with refunds or cancellations — please reach out through the Contact Us page." Nothing more. |

## 12. Known conflicts — resolve before these get stated

🔴 **Pro Trial length is contradicted across sources.** The live Terms of Use name one duration; Inc42's internal product documentation names a different, shorter one. **AskInc42 must not state a trial length until this is resolved.** Say a trial exists and point to the DataLabs pages.

🔴 **The live Terms of Use describe plans that no longer exist.** The Terms reference a team/multi-seat plan and an annual option; the current product simplified away from both. Since `03_Policies_TnC_Privacy.md` instructs AskInc42 to summarise the Terms, **a stale Terms document propagates into policy answers.** Flag to Utkarsh alongside the answer-set sign-off.

⚠️ **Coverage figures differ between the public page and internal counts** — investors and funding rounds in particular. §2 uses the public figures deliberately. If the public page is understated, the fix is to update the page, not the assistant.

⚠️ **Ask DataLabs query cap vs AskInc42 in the app.** The free web tier caps Ask DataLabs queries. `01_App_Knowledge.md` states no cap for the app. **Confirm whether a cap applies in the app** — if it does, it's a user-facing fact the assistant has to know.

## 13. Maintenance

- **Monthly review**, or immediately on any launch that changes tiers, coverage or profile structure.
- **Re-verify §2 coverage figures** against `inc42.com/datalabs/` each cycle — they change and they are the most quoted facts here.
- **Re-check §3 tier boundaries** whenever the product changes what free includes. This is the section most likely to go quietly wrong, and the one where being wrong misleads a user about what they'd be paying for.
- **Never import from the internal master context wholesale.** It is an internal alignment document containing pricing, metrics, strategy, personnel and architecture. Extract only user-facing capability, and re-verify it against the live site before it lands here.
- Update the `Verified` date every cycle, even when nothing changed.
