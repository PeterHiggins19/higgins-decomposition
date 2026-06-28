# Math Hˢ makes simpler — a deterministic route to the same answer (LIBRARY · for anyone doing math)

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. 2026‑06‑25. Where the
compositional / quaternion / log‑ratio reading reaches a result the standard university route reaches the *harder*
way — faster, exactly, and deterministically. Written so **anyone doing math** can see the shortcut. **Honest by
construction:** most of these are *known* results (Aitchison's geometry, Hamilton's quaternions); the contribution
is the **unifying framing** ("it is all one object — a composition") and a **deterministic, hash‑receipted engine**
around it. Not new theorems; simpler, exact, auditable routes. Honest‑broker tiered; Peter is the sole gate.*

---

## Why this matters (the one‑paragraph case)

A great deal of applied mathematics is taught the *long* way: carry a constraint with Lagrange multipliers, fight
gimbal lock with special cases, propagate the ugly distribution of a ratio, fit a nuisance scale you only want to
divide out. In every one of these, there is a **change of viewpoint** — read the object as a *composition* — under
which the hard machinery dissolves into ordinary, exact, deterministic arithmetic. As intelligent systems put math
in everyone's hands, the *simpler, harder‑to‑get‑wrong* route is the one worth knowing. Each example below names
the standard route, the simpler route, and — honestly — what is genuinely new versus what is a known result given
a unifying home.

## 1 · Rotations: Euler angles → the quaternion (the composition) *(receipted)*

**Standard (the hard way).** Three‑dimensional rotation is taught first with **Euler angles** and rotation
matrices. Two pains follow students for life: rotations **do not compose by adding the angles**, and the
angle→rotation map has a **singularity (gimbal lock)** where a degree of freedom is lost.

**Simpler (the Hˢ way).** A **unit quaternion** composes by *one multiplication*, is exact, and never degenerates —
and **a four‑part composition *is* a unit quaternion** (the D=4 rung Hˢ reads). So compositional change inherits
exact, singularity‑free rotation arithmetic for free.

*Measured (`math_simpler_demo.py`, receipt `552cea61`):* composing two rotations, the quaternion route matches the
true rotation to **2.7×10⁻¹⁶**; "just add the Euler angles" is off by **~0.97** (simply wrong). The Euler→rotation
map's `|det|` falls 1.0 → 0.087 → 0.0017 as pitch climbs 0° → 85° → 89.9° (the gimbal singularity); the quaternion
map is non‑degenerate everywhere.

> **Honest:** quaternions‑over‑Euler is **known** (Hamilton, 1843; standard in graphics, robotics, aerospace). New
> here is only the *framing*: the thing you are already reading — a four‑part composition — is that exact object.

## 2 · The "parts sum to one" constraint: Lagrange multipliers → an isometry

**Standard.** Anything living on the simplex (shares, probabilities, mixtures) carries the constraint
`Σ xᵢ = 1`. The textbook handles it with **Lagrange multipliers**, penalty terms, or softmax — extra machinery on
every optimization and every statistic.

**Simpler.** The **isometric log‑ratio (ILR)** map sends the simplex *isometrically* onto ordinary, unconstrained
Euclidean space `ℝ^{D−1}`. You drop the constraint **exactly** (not approximately), do plain unconstrained linear
algebra / calculus / least squares there, and map back. The constraint isn't *enforced* — it's *dissolved*.

> **Honest:** this is **Aitchison's** compositional geometry (1986), the foundation of the CoDa field. Hˢ's role is
> to make it a *deterministic, hash‑receipted instrument* and to extend it to motion — not to claim the geometry.

## 3 · Ratios of variables: messy distributions → log‑ratio linearization

**Standard.** Take the ratio of two measured quantities and the statistics turn nasty: ratio distributions are
heavy‑tailed (a ratio of Gaussians is **Cauchy‑like — undefined mean and variance**), so error propagation and
inference are awkward and easy to get wrong.

**Simpler.** Work in **log‑ratios.** Multiplicative / ratio structure becomes **additive / linear** structure,
where ordinary means, variances, and linear models behave. The thing that was ill‑posed as a ratio is well‑posed
as a difference of logs.

> **Honest:** the log‑ratio transform is classical CoDa. The point for a general reader: *if you find yourself
> doing statistics on ratios, take the log first* — it is the deterministic fix, and it is what Hˢ does internally.

## 4 · Dividing out an unknown common gain: fit a nuisance → cancel it exactly

**Standard.** A shared, unknown multiplicative factor — a laser power, a sensor gain, a dilution, a bulk
temperature — is usually **estimated**: fit a scale/normalization nuisance parameter, then divide.

**Simpler.** **Closure + centered‑log‑ratio cancels any shared multiplicative factor exactly:**
`clr(g·x) = clr(x)` for any scalar `g`. No estimation, no fitting — the common mode is gone **deterministically**.
(This is the same identity behind the measured common‑mode rejection results: e.g. ~313 dB in the ground‑state
case, and the coherence law `suppression ≈ −10·log10(1−ρ)`.)

> **Honest:** the algebra is elementary; the value is recognizing that a problem usually *solved by estimation* has
> an *exact, deterministic* solution once you read the data as a composition.

## The pattern (and the honest meta‑point)

| you were taught (harder) | the simpler route | what dissolves |
|---|---|---|
| Euler angles + gimbal‑lock special cases | the **quaternion** (= the D=4 composition) | non‑additive composition; the singularity |
| Lagrange multipliers for `Σx=1` | the **ILR isometry** to unconstrained space | the constraint (dissolved, not enforced) |
| statistics on ratios (Cauchy‑like) | **log‑ratios** (additive) | the ill‑behaved distribution |
| fit a common gain, then divide | **closure + clr** (`clr(g·x)=clr(x)`) | the nuisance parameter |

The unifying claim — the only genuinely new thing — is that **these are one move, not four**: *read the object as a
composition,* and the constraint, the singularity, the ratio pathology, and the nuisance gain all dissolve into
exact, deterministic arithmetic on log‑ratios and quaternions. Hˢ is the engine that does this move the same way
every time, with a receipt. **Nothing here overturns standard mathematics; it offers a shorter, exact, auditable
path to results the long road also reaches.**

## The bigger picture (Peter's vision — tiered T3)

The same shift is what the **ratio‑blind** result is about at scale: ordinary readings see totals and miss the
proportions, so a large fraction of what could be observed stays invisible. The early, **unmeasured** estimate was
that making that hidden quarter of observations visible — if adopted broadly as intelligent systems spread — could
be worth into the **trillions** across the world economy. That number is a **vision figure, Tier 3, not a
measurement** — offered to convey scale and motivate the work, not as a forecast. The honest, durable claim is the
small one this page demonstrates: *for a real class of everyday math, the compositional route is simpler, exact,
and deterministic — and that is worth teaching to anyone doing math.*

## Honest scope

- **T1:** the receipted rotation demonstration (`552cea61`) and the cited exact identities.
- **T2:** the framing that these are one move; the pedagogical claims.
- **T3:** the economy‑scale value of ratio visibility (a vision figure, not a forecast).
- **Known vs new** is marked in every section. Not a new‑theorem claim; not advice; Peter is the sole gate.

*Cross‑refs: `math_simpler_demo.py`, `THE_BLINDNESS_SUITE.md`, `../papers/cnq_tiling_suite_2026/P1_THE_FIRST_FACE.md`,
`../papers/THE_HIGGINS_DECOMPOSITION_SERIES.md`, `NEW_DEVELOPMENTS_CATALOGUE_2026-06.md`. Peter is the sole gate;
nothing posted.*

*Proof & Honesty Standard — the shortcut is real and receipted · known is marked known · the vision figure is fenced · the human decides.*
