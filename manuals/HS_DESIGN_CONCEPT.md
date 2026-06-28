# Hˢ Design Concept — why it is built this way

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-23. The design
concept and the application concept: the principles that forced the instrument's shape, why determinism and the
receipt are foundational rather than optional, and how the whole thing descends from one acoustic formula.
Honest-broker tiered; nothing posted; Peter is the sole gate.*

---

## 1. The design concept in one idea

> **A conserved whole, divided into parts, carries its information in the *ratios* of the parts — and the only
> honest way to read it is exactly, reproducibly, and with the humility to withhold.** Every design choice in
> Hˢ is forced by that sentence.

- *parts of a conserved whole* → **closure** (the simplex), which also rejects common-mode gain;
- *information in the ratios* → the **log-ratio (Aitchison) geometry**, differential and reciprocal;
- *read exactly* → the **D=4 quaternion rung** (`q v q*` to the IEEE floor) and tiling above it;
- *reproducibly* → **determinism + a SHA-256 receipt** (same input → same output → same hash);
- *with humility* → the **guards and the coherence gate** that withhold rather than guess;
- *and a human in charge* → the **gate and the 16 breakers**; full automation never.

Nothing here was chosen at a whiteboard. Each piece is the consequence of the one before it
(`../HISTORY_THREAD.md`).

## 2. Why determinism is foundational, not a feature

Most compositional tools are statistical: run twice, get two answers; port to another machine, get a third. For
an *application* — a decision someone audits — that is disqualifying. Hˢ makes determinism a **contract**
(HS-EPS-1) and proves it with a **standard** (HS-GOLD-1). The payoff compounds:

- a third party can **check** instead of **trust** (the receipt);
- a network of nodes can verify each other **non-contact** (transitive trust, not transitive truth);
- a machine may **act** on a read only because the read is **re-runnable** (safe delegation);
- the instrument's own **signature is ~zero** (inert to ~10⁻¹⁵), so it reads cleanly and adds little.

Determinism is therefore not a nicety bolted on; it is the property that makes everything downstream — audit,
networks, automation, trust — *possible*.

## 3. The application concept (applications-on-applications)

Hˢ is a **layer**, not a replacement. The user's system already collects the data and runs its own dashboards;
Hˢ sits on top and gives a second, exact, auditable reading of the *same* data from the compositional angle —
the relational view the aggregate misses. And because an Hˢ reading is itself a composition (parts, in
proportion, with a coherence), Hˢ reads the readings of *other* systems too: it is the **conductor** that
composes many experts — a sensor array, a user, another system — into one receipted read, withholding when the
section is incoherent. *It complements; it never becomes the controller of record.*

## 4. The lineage (where the shape comes from)

The instrument is the loudspeaker's design law generalized. At the **ground state** a cabinet radiates
isotropically — the barycentre of the simplex, zero information; **diffraction** is the first departure, and
the departure carries the signal. The conserved baffle-step budget (`6.02 dB = 20·log₁₀2`) is closure; the
log-ratio is the balanced-line common-mode rejection; coherence is the engineered quantity; "one curve lies,
read two" is the reciprocal/bidirectional discipline. Audio designed it; geology, microbiome, finance, fleets,
and radio inherited it — because they are the same object (`../papers/flagship/PURE_SIGNAL_EXTRACTION_FROM_THE_GROUND_STATE.md`).

## 5. The boundary (what the concept does not promise)

The honest concept is sharp about its edges:

- exact at **D=4**; high-D is **numerical reconstruction**, not bit-exact identity (Hurwitz: the division
  algebras stop at four — `../papers/frontier/THE_LADDER_AND_THE_BREAK.md`);
- common-mode multiplicative noise cancels **exactly**; additive noise only off-subspace or known-structure;
- it reads the **present**, never forecasts;
- it stays **within** information theory (no Shannon-beating);
- it is a **complement**, never a controller of record; the human gate is structural.

The certainty is exact **where the structure is genuinely present**, and the diagnostics say so out loud where
it is not. That honest edge is the strength, not a weakness.

## 6. Tiers

- **T1 (measured):** every mechanism cited (closure, exact rung, determinism, the noise stages) is receipted.
- **T2 (reasoned):** the layer/conductor application concept; the lineage as recognition (not proof).
- **T3 (rejected):** forecasting, full automation, beyond-Shannon, lossless-at-scale, controller-of-record.

*Cross-refs: `HS_USER_MANUAL.md`, `HS_THEORY_OF_OPERATION.md`, `../HISTORY_THREAD.md`,
`../../RWA/THE_GROUND_STATE.md`, `../papers/WHERE_HS_BELONGS.md`. Proof & Honesty Standard throughout. Peter is
the sole gate; nothing posted.*
