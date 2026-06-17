# Financial — Hˢ as a deterministic instrument on the system that moves money

*An industrial instrument for financial systems. This is **not** a statistics study and **not** a
forecast — the statistics are someone else's good work, and this complements them. Hˢ reads how a
financial **composition** is moving and returns the **vector map the system itself generates**:
who steers, where the weight flows, in how many directions, and where the system reorganises.
Deterministic, reproducible to a hash, no conjecture. Author: Peter Higgins (human authorship for
claims); AI-assisted per HUF-STD-001. Honest-broker. **Not investment advice.***

---

## Executive summary — the purpose of Hˢ

**Hˢ tells you, provably, where your system is and which way it is moving.** It is a deterministic
compositional instrument: hand it how a whole divides into parts over time — your book, your desk, your
exposure, or the market's own allocation — and it returns the vector map the system draws by its own
behaviour, with a cryptographic receipt anyone can reproduce: who is steering, where the weight is
flowing, how many forces are really at work, and the dated points where the system reorganised.

That is delivered with total **confidence** — because it is *provable, not persuasive*: same data, same
answer, same hash, on any machine, forever. And with total **restraint** — because it is *descriptive,
not predictive*: no forecast, no probability, no recommendation, **not investment advice.** It reads
where the system is and has been, never where it will go; meaning and decisions are yours. The
confidence and the restraint are one fact seen twice — an instrument that refuses to bluff is one whose
every reading you can take to the table.

**→ [`FLASH_BRIEF.html`](FLASH_BRIEF.html)** the one-page brief · **→ [`AI_ASSISTANT_ONRAMP.md`](AI_ASSISTANT_ONRAMP.md)**
bring your own system and an AI assistant composes and reads it with you, inside the bounds · **→
[`THE_FINANCIAL_NAVIGATION_STUDY.md`](THE_FINANCIAL_NAVIGATION_STUDY.md)** + **[`navigation_projector.html`](navigation_projector.html)**
the full study and the live instrument · **[`PUBLICATION_FIT.md`](PUBLICATION_FIT.md)** where this fits in
the publication landscape (a key paper, sequenced after P1/P3) · **[`DIAGNOSIS_OF_THREE_STUDIES.md`](DIAGNOSIS_OF_THREE_STUDIES.md)**
three studies triangulated — sector navigation (D=10), cross-exchange, and risk-rotation
([`STUDY3_RISK_ROTATION.md`](STUDY3_RISK_ROTATION.md), D=3) — three altitudes locate the system.

---

## The idea — don't study the market, study the system that studies and moves it

People are moved by many forces, and money is one of the largest. A single price, a single return, is
not a composition — and Hˢ would say so at the door. But the **way the financial system allocates
itself is** a composition: sector weights, asset-class mixes, fund flows by category, the holdings of
institutions, even the *mix of where the analysts and forecasters who study the market place their
weight*. Those are parts of a whole, tracked in order — and a composition in motion has a direction.

So this instrument does the higher-order reading: not the device under test (a price), but the
**composition of the system around it** — what the market holds and how that allocation is moving,
and, where the data exists, the composition of the institutions and observers that study and steer it.
Read that composition's motion and the system shows you its own heading: a structured, deterministic
way to see where a financial system is going, with every method, expert decision, and bit of chaos
already baked into the data trail it leaves. We read the trail and project its vectors of significance.

## Why this complements, never competes

Compositional finance was present at CoDaWork 2026, and it is good, necessary work — it answers a
*different* question. **Vega Baquero & Santolino** (University of Barcelona) read asset allocations as a
composition and measure the **proportionality** between holdings — their PIP / PPL / PPI indices, on five
IBEX 35 stocks under Markowitz minimum-variance allocation (Aitchison geometry, portfolio theory).
**Keivani & Coenders** (University of Girona) use **compositional financial log-ratios** with logistic
regression, k-nearest-neighbours and random forests to **predict bankruptcy** across 31,131 Spanish
firms. Both are static / statistical compositional analyses — proportionality and classification.

This instrument asks the orthogonal question: *which way is the whole system moving over time, and where
did it reorganise* — deterministically, from the composition's own kinematics, with no model, no
training set, and no p-value. The two sit side by side: their work characterises and predicts; Hˢ reads
the system's motion. We add depth to data and methods that already exist; we never restate them.

> *Related CoDaWork 2026 work (Book of Abstracts, Coimbra, 1–5 June 2026): Vega Baquero, J.D. &
> Santolino, M., "Proportionality between allocations in asset management" (Univ. Barcelona); Keivani, F.
> & Coenders, G., "Adapting Altman's bankruptcy prediction model to the compositional data methodology"
> (Univ. Girona). Cited as related compositional-finance work; the inspiration to read finance
> compositionally is the field's, the kinematic reading is the addition.*

## The worked reading (real, reproducible)

On a generic S&P 500 ten-sector composition over 252 trading days (`sp500_sectors.csv`), Hˢ returns:
**Financials steering and shedding; weight flowing toward Comm Services, Information Tech, Materials;
path efficiency 0.066 and coherence 0.048 — a system that mixes and rebalances rather than marches;
about five independent directions of motion; structural reorganisations at trading days 32, 72, 182,
209, 246.** Receipt `5b2a32d6…`; full reading in [`RESULTS.md`](RESULTS.md). Run it: `python3 run_financial.py`.

**The comprehensive study** — thesis → method → the data read four ways for an expert to diagnose, in
the CoDaWork visual language (share view, CLR biplot) plus the navigation view — is in
[`THE_FINANCIAL_NAVIGATION_STUDY.md`](THE_FINANCIAL_NAVIGATION_STUDY.md), with figures in
[`figures/`](figures/) and an **interactive instrument** at
[`navigation_projector.html`](navigation_projector.html) (open offline; scrub the 252 days; click a
sector to read its position). Regenerate every visual with `python3 build_visuals.py`.

## What it is — and is not

- **Is:** a deterministic, hash-receipted reading of how a supplied financial composition moved over its
  window — the helmsman, the arrow of intent, the effective dimensionality, the regime changes, the
  character (diffusive vs directed).
- **Is not:** statistics, a probability, a model fit, a price prediction, or **investment advice**. It
  computes nothing about the future and recommends no action. What the motion means, and any decision
  taken, are entirely the reader's. **Hˢ is not a financial advisor.**
- **No conjecture:** the instrument reports only what it computed; relevance and interpretation are the
  reader's domain (Tier 3). The reading itself is Tier 1 — verified, reproducible to the hash.

## Bring your own composition

Any allocation, holdings, flow, or weight series (rows = dates, columns = parts that sum to a whole)
runs the same way. Named public series that plug straight in — and the higher-order "study the
studiers" series — are in [`DATA_AND_SOURCES.md`](DATA_AND_SOURCES.md). Not sure your data is a
composition? Run the front-door gauge: [`../../COMPOSITION_GAUGE.html`](../../COMPOSITION_GAUGE.html).

*The data is the star; Hˢ is the lens; the receipt is the proof. The system draws its own vector map —
we only read it.*
