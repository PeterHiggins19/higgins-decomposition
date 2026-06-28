# The Locked-Discriminant Principle — invariance is the lock (PAPER SEED)

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-25. Naming and
papering the math that was actually doing the work when a discriminant was made to "lock": **a decision on a
composition is reproducible across the nuisances the system rejects if and only if it is invariant under those
nuisances** — and the invariant frame that gives common-mode *rejection* for measurement is the same one that
gives the *lock* for decision. Measured; receipt `9055c4a907c2286d` (`locked_discriminant.py`). Honest-broker
tiered; Peter is the sole gate; nothing posted.*

---

## The name and the one line

> **The Locked-Discriminant Principle — invariance is the lock.** A compositional discriminant is *locked*
> (its decision does not change across scale, coupling, or reference) **iff** it factors through the **maximal
> invariant of the nuisance group** — the **centred log-ratio contrast** `clr(x) − baseline`.

## The setup

A composition `x` is observed through nuisances the system is built to ignore:

- a **scalar multiplicative common-mode** `x ↦ g·x` (source level, coupling, gain, dilution), and
- a **baseline / reference offset** `clr ↦ clr + δ` (where "zero" is set; the context).

Call the group of these actions **G**. Two readings of the *same* underlying composition — by different
sensors, at different scales, against different baselines — differ only by an element of **G**. A discriminant
`d(x)` is **locked** when it returns the same decision on all of them.

## The principle (statement)

**A discriminant `d` is locked under G iff it is a function of the maximal invariant of G.**

For G above, the maximal invariant is the **centred log-ratio contrast** `u(x) = clr(x) − baseline`:

- closure → `clr` removes the scalar common-mode exactly (`clr(g·x) = clr(x)`), the scale-maximal-invariant;
- centring against the (co-moving) baseline removes the offset (`(clr+δ) − (base+δ) = clr − base`).

So **`d` is locked ⟺ `d(x) = f(clr(x) − baseline)`** for some `f`. This is the classical *invariance principle*
(group-invariant decision rules factor through a maximal invariant) specialised to the Aitchison simplex.

### Proof sketch
*Sufficiency.* If `d = f∘u` and `g·x` with offset `δ` is any nuisance action, then `u(g·x; base+δ) = u(x; base)`,
so `d` is unchanged — locked. *Necessity.* If `d` depends on any coordinate outside `u` — e.g. the absolute
`clr` level (a baseline direction) or an uncentred projection — then some nuisance action changes that
coordinate and can flip `d`; it is not locked. ∎ (Maximal-invariant factorisation: Eaton 1989; Lehmann–Romano.)

## The evidence (the failures were the proof)

Measured on real Frielingen-9 geology, applying random nuisance actions (scaling × baseline offset, 4,380
draws) and counting how often each discriminant's decision is **unchanged**:

| discriminant | invariant under G? | invariance rate (1.0 = locked) |
|---|---|---|
| `D_static = argmax\|clr(x)\|` (uses the absolute clr level) | no | **0.612** |
| `D_uncentered = sign(v·clr(x))` (no centring) | no | **0.828** |
| `D_diff = argmax\|clr(x) − baseline\|` (the centred contrast) | **yes** | **1.000 — LOCKED** |

The two that failed during construction failed *because they were not G-invariant* — they carried a nuisance
(baseline) direction. The one that locked is exactly the centred contrast: the maximal invariant. **The lock is
the invariance, measured.**

## Why it matters — one frame, two payoffs

This is the deep reason the whole pipeline is coherent. The **same** invariant geometry does two jobs:

- for **measurement**, `clr(g·x) = clr(x)` gives **common-mode rejection** (the confirmed C2 theorem; the
  313 dB / coherence-law / fiber result, `09fff0925dd49fab`);
- for **decision**, factoring through `clr − baseline` gives the **lock** (reproducibility).

So a system that reads in the invariant frame *and* decides in the invariant frame is automatically both
nuisance-rejecting and decision-reproducible — which is precisely the end-to-end coherence the pipeline
demonstrates (`../../library/DOES_THE_SYSTEM_MAKE_SENSE.md`). The discriminant is locked not by fiat but
because it lives in the same coordinates as the read.

## Honest scope (prior art + tier)

- **Classical, cited, not new:** the **invariance principle** and **maximal-invariant** factorisation of
  group-invariant decision rules (Eaton, *Group Invariance in Statistics*, 1989; Lehmann–Romano), and
  **Aitchison's scale invariance / subcompositional coherence** (1986). We claim **no new theorem.**
- **The contribution (T2):** (1) naming and using **"lock = nuisance-group invariance"** as the criterion for
  a *reproducible/deterministic* decision; (2) the **unification** — the invariant frame that rejects the
  common-mode for measurement is the one that locks the decision (one geometry, two payoffs); (3) the
  operational **centred-contrast / differential-helmsman** instance and its **measured** invariance on real
  data.
- **Falsifier:** exhibit a discriminant that is locked (rate 1.0 under G) yet does *not* factor through the
  centred contrast — the principle forbids it.

## Paper-ready statement

*A compositional decision rule is reproducible under the system's rejected nuisances (multiplicative
common-mode and reference offset) if and only if it factors through the centred log-ratio contrast — the
maximal invariant of the nuisance group. The invariant frame that yields exact common-mode rejection for
measurement thereby yields decision reproducibility for classification: one geometry, two guarantees.*

*Cross-refs: `locked_discriminant.py`, `LOCKED_DISCRIMINANT_RESULTS.json`,
`../../library/DOES_THE_SYSTEM_MAKE_SENSE.md`, `../connection-confirmation/CONFIRMATION_LEDGER.md` (C2),
`../../library/THE_BLINDNESS_SUITE.md`, `../UNWRITTEN_CONNECTIONS_SEEDS.md`. Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — the principle is stated + proven (classical, cited) · the lock is measured on real data · the contribution is framing+unification, not a new theorem · the falsifier is named · experts decide.*
