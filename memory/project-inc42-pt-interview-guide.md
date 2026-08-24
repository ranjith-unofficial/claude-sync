---
name: project-inc42-pt-interview-guide
description: "Product Trainee interview question bank, weighted to the locked rubric — reusable for any shortlisted candidate; includes the Jatin Saluja probes"
metadata:
  type: project
---

Interview guide for the **Product Trainee** role Ranjith is hiring for his own team. Built 2026-08-23 for **Jatin Saluja** (rank 10 of 235, fit 77) but the bucket structure is **reusable for every candidate down the shortlist** — swap the resume-specific probes. See [[project-inc42-product-trainee]] for the screening run that produced the ranking.

## Time budget, weighted to the locked rubric

| Bucket | Weight | Minutes |
|---|---|---|
| Opening | unscored | 4 |
| B2C consumer experience | filter, not a weight | 5 |
| Analytical judgement | 25% | 10 |
| Execution & impact | 25% | 10 |
| AI fluency | 20% | 10 |
| Written communication | 20% | 4 live + take-home |
| Product sense & first principles | 10% | 7 |
| Close (salary, logistics) | — | 5 |

**⚠️ Standing tension:** Product sense is weighted **10%**, but user thinking and first principles — the two things Ranjith said on 19 Aug matter most — live there and in Written comms. Treat those answers as more decisive than 10% implies. The weighting is probably wrong and is still an open decision.

## The reusable questions (role-generic — keep these for every candidate)

**Analytical (25%)** — the bar is separating signal from noise, not producing reports on request. Reference point: the brief-ranking simulation over 366 real articles that found 86% had no sector tag and killed the feature.
- *"Before you changed anything — how did you work out WHERE people were dropping, and how did you know that was the real problem and not a symptom?"* Strong: instrumented, segmented, **checked the obvious explanation and ruled it out**; names what he expected and didn't find. Weak: conclusion with no interrogation between.
- **The live test:** *"Users pick sectors in onboarding to personalise the brief. It's live, and ranking barely changes what anyone sees. Where would you look?"* Strong: asks about **tag coverage / the data behind the tag** before touching the algorithm. Weak: tunes weights, adds ML, "let's A/B test it." Ranjith already knows the answer, so this grades itself.
- *"What's a number you reported that you later realised was misleading?"* — "can't think of one" is a fail at <2 years.

**Execution (25%)** — shipped, and moved a number they personally influenced.
- *"Walk me from the day you proposed it to the day the number showed up. Who had to agree, what got cut, how long did it take?"* Real shipping has scars; a frictionless story usually means no ownership.
- *"What did you decide NOT to build, and what did it cost?"*

**AI fluency (20%)** — most-inflated bucket. Bar: built something shippable, or used AI inside the analysis itself. Tool names count for nothing.
- *"Draw me the nodes. Where does it break?"* — volunteering failure modes is the tell. Ranjith builds n8n daily and will know in 90 seconds.
- *"What did you do about the cases where it retrieved the wrong thing?"* — anyone claiming it never failed never evaluated it.
- *"Tell me about an AI tool giving you a confidently wrong answer that you caught. How?"*

**Written comms (20%)** — mostly NOT testable live.
- *"Send me one PRD you actually wrote — the real file, not a rewrite. Which one?"* Offering to "put something together" means no PRD exists as claimed.
- **Take-home, 1 page, 48h — the highest-value item in the whole guide:** *"Our newsletter deep links open in Safari instead of the app. Write the problem statement and how you'd find the cause."* Ranjith already knows the answer (Customer.io click-tracker breaking Universal Links / AASA — see [[project-inc42-deep-linking]]), so the reasoning can be graded honestly. Strong: states assumptions, proposes how to **verify** rather than jumping to a fix.
- *"Explain <their domain> to me as if I know nothing."*

**Product sense & first principles (10%)**
- *"Tell me about a time the data told you the thing you were building wouldn't work — and you said so."* The single question closest to Ranjith's bar.
- **The live test:** *"News app, small install base, no paid budget. Where do the next thousand installs come from?"* Strong: reasons from where the audience already is (mobile web, newsletter, repeat readers), gates on **intent**, asks for numbers before committing — i.e. independently reconstructs [[project-inc42-app-acquisition]]. Weak: Product Hunt / influencers / referral loops with no sizing.

**B2C filter** — *"Who was the actual end user? Describe one to me."* Separates real consumer work from B2B wearing a consumer label; the "user" turning out to be an internal colleague is the tell. Then *"how many users were in that funnel?"* — a 10% improvement on 80 users is not a result.

**Close** — talk me through your salary number · can you start now as a trainee · what do you want to ask me (last honest signal; only-perks-and-title is a flag).

## Jatin Saluja — candidate-specific (2026-08-23)

BBA JECRC 2025 · **9 months, ALL internships** (Figs, PrimeWealth, REPP) · Delhi · **₹1.8L current, asks ₹6L**. Scores: AI fluency 82 · Analytical 75 · Execution 73 · Written comms 72 · Product sense 69 · First principles 66 · User thinking 64. Context: **mixed**.

Real strengths, and they map unusually well onto Ranjith's own stack: an **n8n agent** scraping Reddit/HN that themes pain points and drafts PRDs; a **RAG chatbot** over 30+ mutual-fund fields with cited sources; **Figs KYC funnel rework cutting verification drop-off 10%** (the one clearly measured shipped B2C outcome); a quick-commerce search benchmark across 4 apps / 50+ queries.

**Three claims to verify — the whole interview turns on these:**
1. **Projections dressed as results.** InvestMates says *"projected 25% CTR lift"* and *"projected 30% drop-off reduction"* — forecasts formatted identically to the real Figs 10%. Ask which were measured vs forecast; **the test is whether he separates them unprompted.**
2. **"Drove 18% growth in AUM"** as a 3-month GTM intern at a wealth firm. Attribution is doing heavy lifting.
3. **"76% got wrong AI outputs, 84% wanted uncertainty signals"** — percentages with no sample size and no method.

**Salary position:** ₹6L is **exactly the ceiling** (₹5L cap +20%). At ₹5L he still gets a 178% raise from ₹1.8L, so there is real room.

**Decision rule set in advance:** if the Figs 10% holds up under questioning AND he produces a real PRD, he is a strong trainee hire. If both fail, the resume was better than the candidate — worth knowing, because he is rank 10 and the same pattern will repeat down the list.

⚠️ **His resume link in the sheet is dead** — Keka signs document URLs with an Azure SAS token that expired 19 Aug; all 235 links now 403. Local copy: `<scratchpad 88ba76e1>/pool_resumes/890a5eb0-6edf-4f66-be69-94ea36413253.pdf`. Fix pending: re-point the column at stable Keka candidate-profile URLs.

Related: [[project-inc42-product-trainee]], [[project-inc42-hiring-agent]], [[feedback-deliver-in-chat]], [[feedback-always-include-source-links]].
