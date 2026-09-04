# Brief home screen — one shell, driven by the ranking logic
4 Sep 2026 · draft file row D (y=71000) · six states

## The first-principles problem

The ranking function emits a score that is a **pure function of (topic, sector, popularity)**.
It therefore knows nothing about whether a story is important, surprising, large, or in conflict
with another story. Any entry design that leads with "a big number", "a versus", or "a verdict"
is asserting a semantic property the pipeline does not compute — so it will render correctly only
on the days the content happens to cooperate. That is the whole defect in row C.

Everything on the entry screen must be a function of what the logic actually emits:

| Always available | Source |
|---|---|
| headline | article |
| parent topic (8 buckets) | Development_Type → map |
| parent sector(s) (7 buckets) | Company_Industries → map |
| published_time | article |
| score, and its rank | computed |
| **which branch produced the score** | computed — see below |
| App Featured flag | editorial |
| day length, matched count | computed per user per day |

## Positional vs presence guarantee

There are only two guarantees possible in a ranked list:

1. **Positional** — "your IPO is card 1". Requires overriding the score. Breaks the ranking.
2. **Presence** — "your IPO is in here, at card 3". Requires only that you *say so*.

The score exists to order; the reader's need is to know their thing is in there. So the correct
guarantee is **presence**, and it costs nothing. That is the `YOUR TOPICS TODAY` slot: for each
followed topic and sector, the highest-scoring article in it, with its card number. It answers
"we cannot be sure an IPO will be visible" without touching the ranking.

Corollary: because presence is guaranteed, **nothing except the editorial override should ever
jump the queue** — and the override must be visibly labelled as editorial, or the chip
"Because you follow IPO" becomes a lie.

## Reason chips — exhaustive, in precedence order

Every article in the brief carries exactly one. Evaluated top to bottom, first match wins.

| # | Chip | Condition |
|---|---|---|
| 1 | `PICKED BY OUR NEWSROOM` | App Featured Article = Yes |
| 2 | `BECAUSE YOU FOLLOW {TOPIC}` | TopicAff == 1.0 |
| 3 | `BECAUSE YOU FOLLOW {SECTOR}` | any ParentAffinity == 1.0 |
| 4 | `CLOSE TO {FOLLOWED THING}` | 0 < affinity < 1 |
| 5 | `MOST READ TODAY` | both affinities 0 |

This is exhaustive and mutually exclusive — every article the logic can produce gets a label,
so no state of the data can produce an unlabelled row.

**API requirement this creates:** the endpoint must return the *argmax followed entity*, not just
the score. `max(affinity[t → topic])` tells you the value but not which followed topic won it,
and chips 2–4 need the name. Also return the parent topic/sector labels and the featured flag.

## The shell

| Slot | Renders |
|---|---|
| 1 Header | always — wordmark, date, streak chip |
| 2 Opener | always — true count + a personalization line computed from matched_count |
| 3 Editorial block | only if App Featured = Yes. Black ground, own chip, "outside today's ranking" |
| 4 Lead card | always — real headline, its reason chip, image, standfirst |
| 5 CTA | always — "n cards · about m min" from the true day length |
| 6a YOUR TOPICS TODAY | if matched_count >= 1 — one row per followed thing + card number |
| 6b Empty state | if matched_count == 0 — names the followed thing, offers notify |
| 7 WHAT'S INSIDE | always — full ranked order, every row chipped |
| 8 Tab bar | always |

6a and 6b are mutually exclusive; never both. A followed topic with nothing today renders inside
6a as a greyed "Nothing today" row rather than being dropped — the reader has to be able to see
that the app checked.

## Non-render rules

- Never pad to eight. If the day produced two, the brief is two and the opener says so.
- Never render a score or a match percentage. The score orders; it does not measure.
- Never claim personalization when matched_count == 0.
- If the day produced zero articles, show yesterday's brief with a dated label. Only safe fallback.

## The six states (row D)

| Screen | User | Result |
|---|---|---|
| D1 | Follows IPO, Deals / Fintech, Consumer | 4 of 8 matched. **The followed IPO ranks 3rd** — presence guarantee earns its place |
| D2 | Follows Team / Fintech | 1 of 8 matched. Team published nothing; shown as a greyed row |
| D3 | Follows AI only | 0 of 8 matched. Named empty state + notify CTA, brief still runs on popularity |
| D4 | No preferences | Pure popularity. Identical for every such user, every day |
| D5 | Thin Sunday | 2 stories. Shell shortens honestly |
| D6 | Editorial override active | Black slot above the personal ranking, labelled as editorial |

## Three findings in the spec itself

### 1. ParentMultiplier rewards broad tagging quadratically — this one is a bug
`SectorAff = Σ over parents (n × ParentAffinity)` scales as **n² × avg_affinity**.

| Article | SectorAff |
|---|---|
| One sector, **followed** | 1.00 |
| Two sectors, **neither followed**, affinity 0.30 each | 1.20 |
| Three sectors, **none followed**, affinity 0.15 each | 1.35 |

An article in two unfollowed sectors beats a direct follow-match once affinity > 0.25; with three
parents the threshold falls to 0.11. So an article tagged broadly outranks the user's actual
interest, the lead card gets a `CLOSE TO` chip, and the genuine match sits lower.
**Recommend:** `SectorAff = max(ParentAffinity) + 0.1 × (unique_parents − 1)`, capped at 1.2.
A direct follow then always beats an indirect one, and breadth still gets a small nod.

### 2. Popularity measures supply, not appetite
`topicPopularity = unique_readers(topic) / unique_readers(biggest topic)`. News anchors the scale
at 1.000 — but News is the residual bucket (Business Updates, Cohort Launches, Controversies).
It has the most readers largely because it has the most articles. Using total readership as an
importance prior therefore systematically promotes the least specific category, permanently, for
every no-preference user.
**Recommend:** divide by articles published in that category over the same 90 days —
`readers per article`, then rescale to 0–1. That turns a supply artifact into a real appetite
signal. Same fix for sectors.

### 3. Same topic + same sector = identical score
Score is a pure function of (topic, sector) for a given user, so two articles in the same box tie
exactly and are separated **only by recency**. On a high-supply weekday (Tue–Thu median 18–20
articles into 8 topics × 7 sectors, heavily skewed to News/Deals × Ecommerce/Consumer/Fintech),
a large share of the brief is ordered by publish time, not by the model.
**Not yet measured** — the tie rate per day should be computed from DataLabs before tuning
weights, because if it is high the personalization is doing less work than it appears to.

## Open question worth answering first
D4 (no preferences) may not be an edge case. If most app users skip or abandon topic selection,
D4 is the *majority* screen and the popularity formula in finding #2 is the highest-leverage line
in the whole spec. Onboarding completion rate needed.

---

# Row E — what actually makes someone tap
4 Sep 2026 · draft file row E (y=74000)

## The error in row D
`WHAT'S INSIDE` listed all eight full headlines. Eight headlines **is** the brief for a skimmer —
20 seconds, free, no tap. The entry screen was competing with the product it was selling.

My Mobbin justification for showing headlines was wrong in one specific way: in SCMP's *My Daily 5*
and Bloomberg's *The Bulletin*, **the list is the destination** — tapping a row opens that article,
there is no deck behind it. Inc42's Brief has a bounded 8-card deck behind the list, so the list and
the deck compete for the same job. Import the pattern and you kill the thing it fronts.

## The layer rule
| Layer | Owns | Where it belongs |
|---|---|---|
| Entity | which company, which topic | entry screen |
| Event (predicate) | what happened — the verb and the number | first card |
| Consequence | what it means, what changed | the card body |

The headline is the *event*. The card is the *consequence*. So the entry screen should carry
entities and withhold predicates. "Don't leak the edition" was too crude a rule; the real rule is
**which layer leaks**.

## The guarantee needs the entity, not the predicate
This is the precise fix, and it costs nothing:

| Row D (wrong) | Row E (right) |
|---|---|
| `IPO · RentoMojo files for a ₹1,256 Cr IPO · Card 3` | `IPO · RentoMojo · Card 3` |
| Presence proven, story spent | Presence proven, story intact |

Both satisfy "we cannot be sure an IPO will be visible." Only the second leaves an open loop —
*RentoMojo did something IPO-related, what?* The row stops being a substitute and becomes a tease.

## The lead card stays full
One story is given completely: headline, standfirst, image, its reason chip, "CARD 1 OF 8".
That is the sample that earns the tap. Withholding all eight reads as evasive; giving one fully and
indexing the rest is how a front page has always worked.

## Three treatments

| | Pull | Cost | Risk |
|---|---|---|---|
| **E1 entity index** | medium-high | none — company + parent topic already exist | reader may not care about a bare company name |
| **E2 open questions** | highest | needs a new per-article question field; summary bullets are 93% covered so ~7% would have no row | question quality becomes an editorial burden every single day |
| **E3 no index** | low | none | nothing to skim, but also nothing that proves the 5 minutes are worth it |

**Recommend E1 now, E2 as the v2 upgrade** once there is a question field. E1 needs no new content
and no new pipeline — it is a rendering change to a list that already exists. E3 is worth building
only if the deck's first card is strong enough to carry the whole decision alone.

## The fork underneath all of this
If the card contains nothing the headline does not — if it is the headline plus a restatement —
then no entry design fixes the tap rate, because there is genuinely nothing behind the door.
In that case the honest product is the list, and the deck should be dropped.

The corpus work says the cards do carry a distinct layer (summary bullets, "what's new / why it
matters", 93% coverage). So the deck earns its place — **but only if the card body leads with the
consequence rather than repeating the headline.** That is a content requirement, not a design one,
and it should be written into the card template before any of this ships.
