# How far the math goes — exact SO(n) generation to any n, and the wall the identity hits

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-23. The
**complement** to `THE_LADDER_AND_THE_BREAK.md`: that note shows where the division-algebra *identity* breaks
(octonions lose associativity, sedenions lose division). This one shows the **other half** — that the exact
*rotation* does **not** break: SO(n) can be generated exactly for any n, deterministically, as a test-matrix
factory. Together they answer the question "how far does the math itself go." Tooling: `experiments/
son_generator_2026-06/son_exact_generator.py`, run receipt `8107b173ffaaa7938098e652e475d7efa8fc57a06cca71edeb33b14d7ce29ac1`. Honest-broker tiered; conforms to the Proof &
Honesty Standard. Nothing posted; Peter is the sole gate.*

---

## The question

Invert the new SO(4)/dual-quaternion tools — make them a **generator** (the Piccirillo move already used at
D=4: *settle a hard object by building an exact adjacent one*). Can a deterministic dataset be generated for
**any n**, structured so the data itself is a **test matrix set** that validates the readers and helps find
higher-dimensional structure? And how far does the underlying math actually go?

## The answer is two-sided — and both sides are theorems

**Side A — the EXACT ROTATION is unbounded in n.** Every rotation in `SO(n)` factors (the spectral theorem
for antisymmetric generators) into `⌊n/2⌋` commuting **2-plane rotations**. That planar (Givens) product is
the *coordinate form* of the **Spin(n) rotor sandwich** `R v R̃` in the Clifford algebra `Cl(n)` — and it is
exact for **any** n. So generation never breaks. Measured ladder (the receipt):

| n | rotation planes ⌊n/2⌋ | SO(n) orthogonality resid | angle-recovery resid | rotor == planar |
|---:|---:|---:|---:|---:|
| 3 | 1 | 4.4e-16 | 8.3e-17 | 2.8e-17 |
| 4 | 2 | 1.3e-15 | 1.1e-16 | 1.1e-16 |
| 8 | 4 | 1.8e-15 | 5.6e-17 | 1.1e-16 |
| 64 | 32 | 1.6e-15 | 1.1e-15 | 2.2e-16 |
| 256 | 128 | 2.2e-15 | 2.6e-15 | — |
| **1024** | **512** | **1.8e-15** | **4.9e-15** | — |

Exact to the IEEE floor at every rung to **n = 1024**, and the **rotor build equals the planar build to
~1e-16** — confirming they are the same exact object. The planted rotation angles are **recovered from the
matrix spectrum** to the floor, which is what makes the output a genuine *test matrix*: known invariants, in,
recoverable, out.

**Side B — the single-number IDENTITY is bounded at four.** A 4-part composition's 3 ILR coordinates literally
*are* a quaternion, and an Aitchison perturbation is the exact sandwich `q v q*` = SO(3) (measured 1.3e-15);
D=5 gives the two-sided SO(4) (orthogonality 7.8e-16). **There it stops.** By Hurwitz the normed division
algebras are only `ℝ, ℂ, ℍ, 𝕆` (dims 1, 2, 4, 8); the octonions are non-associative (no clean rotation-group
sandwich) and the sedenions have zero divisors (`THE_LADDER_AND_THE_BREAK.md` exhibits one). So for `n ≥ 5`
there is **no single hypercomplex number that a composition equals** — the *identity* breaks even though the
*rotation* does not.

## What that means for the generator (and for "finding the face")

- **Yes — a deterministic test set exists for any n.** `son_exact_generator.py` emits, for any n: an `SO(n)`
  matrix with **known rotation planes/angles** (a structured test matrix with a known spectrum) and a
  compositional trajectory driven by that rotation plus a known size schedule. Ground truth in, residual-to-
  truth out.
- **It calibrates the blindness suite at any n.** Plant the two faces and they separate **exactly**: a
  *rotation-only* step gives `dθ > 0, dsize = 0`; a *size-only* step gives `dθ = 0, dsize > 0` — verified at
  n = 3, 4, 8, 64 to the floor. So the synthetic data is a **faithful calibration rig** for the
  ratio/mass/rotation/size readers (`library/THE_BLINDNESS_SUITE.md`): you can plant a face and confirm each
  reader fires on exactly its own face and is blind to the rest. *Finding the face becomes a measured,
  ground-truthed operation, not a guess.*
- **The boundary is the design, not a defect.** Because the single-number identity stops at four, high-n
  compositions are **tiled** into overlapping exact 4-charts (the `O(log D)` atlas), not read by a native
  high-n rotor. The generator makes this testable: drive structure at dimension n, read it back, and the
  residual map shows exactly where the exact rung ends and tiling/conditioning takes over.

## So — how far does the math go?

> **Exact rotation: all the way (Spin(n), any n).** **The composition-as-a-single-number identity: to four,
> and no further (Hurwitz).** **The reading of arbitrary dimension: by tiling exact 4-charts.** The generator
> spans the first, respects the second, and instruments the third.

## Tiers

- **T1 (measured):** exact `SO(n)` generation + spectral angle recovery to n = 1024 (`8107b173…`); rotor ==
  planar to ~1e-16; the D=4 quaternion / D=5 SO(4) identities; the exact face-separation calibration.
- **T2 (reasoned):** that this generator is the right instrument to *probe* higher-dimensional structure and
  extend the blindness suite — a method, demonstrated to work on planted structure, not yet a discovery.
- **T3 (open / to earn):** any *new* higher-dimensional face or invariant found by running it on real or
  designed data — claimed only when it arrives with a receipt. The suite is open by construction.

*Cross-refs: `THE_LADDER_AND_THE_BREAK.md` (the identity wall — the other half), `SO4_SPIN4_FUTURE_COMPONENT.md`
(the built SO(4) module), `../../library/THE_BLINDNESS_SUITE.md` (what the generator calibrates),
`../../experiments/son_generator_2026-06/son_exact_generator.py`,
`../../experiments/exact_dim4_generator_2026-06/` (the D=4 precedent). Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — numbers cited-or-fenced · math proven + receipted · value shown · experts decide.*
