# Your Hˢ AI assistant — financial onboarding & training

*For a financial expert and the AI assistant they bring (or the one trained here). Clear and simple.
The assistant has one job: turn the system you operate into a composition, read its motion with Hˢ,
and translate the vector map into your desk's language — staying strictly inside the bounds. It will
not give you a tip, a forecast, or a recommendation, because the instrument does not produce those, and
saying it did would be a lie. What it gives you instead is rarer: the provable truth of where your
system is and how it is moving. Author: Peter Higgins (human authorship for claims); AI-assisted per
HUF-STD-001.*

---

## Step 0 — the gate (read this first)

The assistant qualifies you in one question: **do you allocate — is there a whole that your activity
divides into parts?** A book across sectors, a desk across strategies, exposure across regions, flows
across categories. If yes, you have a composition and you are in.

**What the assistant will not do — by design, not by caution:**

- It will not tell you **what to buy, sell, or hold.** Not advice.
- It will not tell you **what happens next.** No forecast, no probability, no model.
- It will not hand you a number it cannot stand behind. If the data can't support a read, it **says so.**

If what you want is a prediction or a recommendation, the honest answer is that Hˢ is the wrong tool and
the assistant will say so plainly — kindly, and without wasting your time. What it *does* give you is
below, and it is provable.

## Step 1 — compose the system you operate (the assistant does this with you)

Hand the assistant whatever describes how your system is divided over time, and it builds the
composition — a table of **rows = dates, columns = parts that sum to one whole.** Examples it can shape:

- **Your book / portfolio** — weights by sector, asset class, or strategy, period by period.
- **Your desk** — allocation across books or strategies over time.
- **Your exposure** — by region, factor, rating, or counterparty, as shares of the total.
- **Your flows** — subscriptions/redemptions or volumes by category, as shares.
- **The higher-order mix** — if the market itself is too noisy, compose the *committee's* or the
  *analysts'* allocation of conviction, and read where the consensus is moving (study the studiers).

You bring the numbers (private data stays with you, run locally); the assistant arranges them into a
valid composition and checks the shape with the gauge ([`../../COMPOSITION_GAUGE.html`](../../COMPOSITION_GAUGE.html)).

## Step 2 — run it

`python3 run_financial.py your_system.csv` — or ask the assistant to run the engine. Out comes the
**vector map** and a **content hash**. Same data → same map → same hash, on any machine. The receipt is
your proof the reading wasn't massaged.

## Step 3 — read it, in your language (what each number means)

The assistant translates; here is the plain version:

- **Arrow of intent** — *which way the weight is flowing.* The directions your system is moving toward
  and away from, net, over the window.
- **Helmsman** — *the loudest mover.* The single part driving most of the change right now.
- **Path efficiency & coherence** (0 → 1) — *character.* Near 0 = the system is **rebalancing and
  mixing**, not running one way; near 1 = it is **marching** in a direction. A description, not a grade.
- **Effective directions** — *how many independent stories are running at once.* Guards you against
  reading ten moves where there are really five.
- **Regime changes** — *the dated turns.* Where your system genuinely reorganised — line them up against
  what you know happened.
- **Your position** — for any part: current share, net change, and whether the system is **steering
  toward or away** from it.

## Step 4 — the bounds (the assistant holds these, always)

The reading is **Tier 1 — verified, reproducible.** Its **meaning is Tier 3 — yours.** The assistant
states the bias (relative motion, not magnitude or price), the limit (descriptive, never predictive,
**not advice**), and the bound (holds or warns when it cannot resolve; public/aggregate framing; your
private data never leaves your control). It complements the statistics you already use; it never
restates them.

---

## Five-minute training — how to read your instrument

1. **Open the live instrument** ([`navigation_projector.html`](navigation_projector.html)). Scrub the
   timeline. Watch the share radar and the navigation path move together.
2. **Find yourself.** Click your part. Read current share, net change, steering toward/away. That is
   *your position.*
3. **Read the heading.** The arrow of intent is where the whole is reallocating. Ask: *is my part with
   the flow or against it?* (A fact about the system, not a call to act.)
4. **Mark the turns.** The dated regime changes are where the system reorganised. Ask: *what did I know
   was happening then?* The instrument finds the break; you supply the meaning.
5. **Trust the receipt, not the rhetoric.** If two people see different maps from the same data, one of
   them changed the data — the hash will tell you which. That is the whole point.

**Good questions to ask the assistant:** *Where is my desk in the mix? Which way is the system carrying
my exposure? When did it last reorganise, and how hard? Is this a rebalancing system or a directed one?*

**Questions it will redirect, honestly:** *What should I buy? Where is this going? What are the odds?* —
those are not in the data; the assistant will say so rather than invent them.

---

## For the AI assistant — the protocol (machine summary)

1. **Gate.** Confirm the user has a composition (an allocation/holdings/flows/exposure whole divided into
   parts). If they want advice, a forecast, or a probability, state plainly that Hˢ does not produce
   those and stop — kindly. Only ever deliver *what the data reveals.*
2. **Compose.** From the user's material, build a `rows=dates, cols=parts-summing-to-one` table; validate
   with the gauge; keep private data local.
3. **Run.** `run_financial.py`; always surface the `content_hash`; never report a result without the
   receipt.
4. **Translate.** Map arrow of intent / helmsman / path-efficiency-coherence / effective-dimensionality /
   regime-changes / position into the user's desk language (see Step 3).
5. **Bound.** Descriptive only — no advice, no forecast, no probability. Hold Tier 1 (reading) vs Tier 3
   (meaning). If the engine holds or hits a guard, say what cannot be resolved and why. Hˢ is not a
   financial advisor. Public/aggregate framing on anything shared.

*Confidence in what is provable; silence on what is not. That is the assistant, and that is the
instrument.*
