# QD — Deeper Connections (the "more pop" document)

**Status:** experimental, not for repo use until status promotion. See [`README.json`](README.json).
**Purpose:** go deeper than the conversational sketch. For each correspondence between CNT and quaternion algebra, label its claim strength (ISOMORPHISM / EQUIVALENCE / ANALOGY / CONJECTURE), spell out the math chain where the connection is exact, and propose a corpus test that would validate or falsify it.

The point of this document is not to assert that CNT *is* quaternion algebra. The point is to show that several specific correspondences are not numerology — they are real mathematical equivalences hiding inside the existing engine, named by other words. If even half of these survive corpus testing, then the quaternion view is not a re-skin; it is the natural coordinate system the engine has been operating in since v2.0.4.

---

## The ten correspondences, ranked by claim strength

### 1. Aitchison D=4 simplex ↔ unit quaternions

**Claim strength: ISOMORPHISM.** This is the load-bearing claim. If it falls, most of the rest collapse with it; if it holds, the others are consequences.

**The math chain:**

Closed compositions on the (D−1)-simplex live, after CLR projection, in the hyperplane Σx_i = 0 in ℝ^D. The Aitchison metric on this hyperplane is the standard Euclidean metric restricted to the hyperplane. The isometry group of this hyperplane (orthogonal transformations preserving Σx_i = 0) is O(D−1), with connected component SO(D−1).

For **D = 4**: the hyperplane is ℝ³. Its rotation group is SO(3). The universal cover of SO(3) is SU(2). SU(2) is, as a manifold, the 3-sphere S³. The unit quaternions are exactly S³ with their multiplication structure.

So: Aitchison rotations on a 4-carrier compositional simplex are **literally** parameterised by unit quaternions (modulo the ±1 sign that distinguishes spin-½ from spin-1 representations). This is not analogy; it is the same group with two names.

**Corpus test:** `backblaze_fleet` is the only D=4 experiment in the corpus (T=731, IR=CURVATURE_VERTEX_FLAT). Reconstruct its trajectory as a unit-quaternion path on S³ using the CLR vectors and a fixed Helmert basis. The reconstructed quaternion path, projected back through the inverse Helmert basis to CLR, must reproduce the original CLR vectors to numerical precision (≤ 1e-12). If it does, the isomorphism is confirmed for the canonical case. If it doesn't, find the bug or the wrong basis choice — the claim is provable.

---

### 2. atan2 bearing computation ↔ quaternion logarithm map

**Claim strength: EQUIVALENCE.** Different formulae for the same operation under explicit transform.

**The math chain:**

CNT's bearing channel is computed as `θ = atan2(y, x)` where (x, y) is a CLR-projected pair. The talk-deck slide `slide_cmp_bearing_atan2.svg` celebrates this as 3× fewer ops and 10⁷ better numerical stability than the arccos alternative.

The reason atan2 wins is not just that it's a better computation — it's that arccos is the wrong operation. Arccos inverts the inner product (a scalar); atan2 inverts the *complex argument* (a 2-vector → angle map). On the 2-sphere, arccos is the geodesic distance from the north pole; on S¹, atan2 is the natural chart.

The quaternion log map is, for q = a + bi + cj + dk with |q| = 1:

```
log(q) = (theta / |v|) * v        where v = (b, c, d), theta = atan2(|v|, a)
```

It uses **atan2 of the (vector-norm, scalar) pair**, not arccos of the scalar. This is exactly the operation CNT performs at every timestep when computing bearing from a CLR-projected coordinate pair — except CNT is doing it in 2D (one bearing per pair), and the quaternion log is the 3D generalization.

So CNT's atan2 step is the rank-1 case of the quaternion log map. The numerical-stability improvement is the same improvement you get on Lie groups whenever you replace arccos-of-trace with atan2-of-axis-norm-and-scalar.

**Corpus test:** for any corpus experiment with D=4, the per-timestep bearing extracted by CNT's atan2 must equal the angle component of the quaternion log of the corresponding unit quaternion. Compute both, diff to numerical precision, confirm.

---

### 3. M² = I metric tensor ↔ quaternion conjugation involution

**Claim strength: EQUIVALENCE.** Two different formal expressions of the same involution.

**The math chain:**

CNT's metric tensor M satisfies M² = I — every CNT JSON includes `metadata.environment` certificates that this holds to ≤ 1e-15 (a Banach contraction certificate). M is therefore an involution on the trajectory state space.

Quaternion conjugation q → q* (where q* = a − bi − cj − dk) is also an involution: (q*)* = q. It is, up to a sign convention, the unique antiautomorphism of the quaternion algebra that fixes the scalar part and negates the vector part.

If we identify CNT's trajectory state at time t with a unit quaternion Q(t), and identify M with the operation Q → Q*, then M² = I becomes (Q*)* = Q, which holds trivially. Furthermore, the *physical interpretation* of quaternion conjugation is **time reversal**: if Q(t) parameterises a trajectory, then Q*(t) parameterises the time-reversed trajectory.

So M² = I is, in the quaternion view, a certificate that **the CNT trajectory respects time-reversal symmetry**. The Banach contraction is the algebraic shadow of a physical invariance.

**Corpus test:** for every experiment in the 25-experiment corpus, compute the time-reversed trajectory (same CSV with rows in reverse order) and run CNT on it. The metric tensor M of the reversed run should equal the conjugate of the original M (under the candidate quaternion identification). Pick three experiments with different IR classes (CRITICALLY_DAMPED, OVERDAMPED_EXTREME, MODERATELY_DAMPED) and confirm.

---

### 4. Period-2 attractor (LIMIT_CYCLE_P2) ↔ spinor double cover signature

**Claim strength: ANALOGY → CONJECTURE.** Suggestive structural match; needs corpus test to upgrade.

**The math chain:**

CNT's depth tower terminates with one of several termination codes. `LIMIT_CYCLE_P2` means the trajectory returns to itself after exactly two recursion steps but not one. Many corpus experiments hit this terminator: ember_chn, ember_jpn, ember_ind, ember_wld, ember_fra, geochem_tappe_kim1, fao_irrigation_methods, and others.

In group theory, an order-2 element of a group is one that squares to identity but is not itself identity. The most famous physically-meaningful example is the **spinor**: an object whose double-cover representation needs a 720° rotation to return to identity, while the underlying SO(3) rotation needs only 360°. Fermions are spinors; bosons are not. The 720° / 360° distinction is the difference between the universal cover (SU(2)) and the quotient (SO(3)).

If CNT trajectories live on SU(2) (per claim #1 above for D=4), then LIMIT_CYCLE_P2 is the algebraic signature that the trajectory's lift to SU(2) is the **double-valued** branch — the spinor sector — rather than the **single-valued** branch — the vector sector. LIMIT_CYCLE_P1 (returns after one step) would be the vector sector.

This is the most provocative claim in the document because, if it survives the test, it means CNT has been doing **fermion/boson classification on compositional data** without anyone naming it that.

**Corpus test:** look at the existing 25-experiment corpus. Tabulate `curvature_termination` against `D`. The conjecture predicts:
- All D=4 experiments hitting LIMIT_CYCLE_P2 are in the spinor sector.
- No LIMIT_CYCLE_P1 experiment at D=4 should exist if the trajectory has odd winding number.
- The classification is invariant under continuous deformation of the input.

The current corpus has only one D=4 experiment (backblaze_fleet, terminator CURVATURE_VERTEX_FLAT — neither P1 nor P2). To test, we would need to *generate* synthetic D=4 trajectories with known parity (controlled spinor vs vector) and check that CNT places each in the predicted termination class. This is round-3 work, not round-0.

---

### 5. CBS cube (three orthogonal faces) ↔ Cayley diagram of the quaternion group Q₈

**Claim strength: ANALOGY.** Strong structural similarity; the dimensions match exactly; the algebra needs to be formally verified.

**The math chain:**

CNT's Stage 2 atlas includes the CBS cube — a 3D structure with three orthogonal faces representing the (ω, κ), (κ, σ), and (ω, σ) planes of the trajectory state space. The Higgins time axis runs through the cube as the projection direction.

The quaternion group Q₈ = {±1, ±i, ±j, ±k} has a natural Cayley diagram in 3D where each generator (i, j, k) labels a coordinate axis and the multiplication table determines the edge structure. The three planes spanned by the imaginary basis pairs — span(i, j), span(j, k), span(k, i) — are exactly the three coordinate planes of the Cayley diagram. The scalar axis (the ±1 axis) is orthogonal to all three.

If CNT's (ω, κ, σ) channel triple is identified with the (i, j, k) basis, then the CBS cube's three faces are the three coordinate planes of Q₈'s Cayley diagram, and the Higgins time axis is the scalar (±1) axis.

**Corpus test:** the multiplication table of Q₈ predicts specific algebraic relations between products of channel values. For instance, ω · κ should equal σ (with sign), κ · σ should equal ω, σ · ω should equal κ — under quaternion multiplication. CNT does not currently compute these products, but they can be evaluated post-hoc on the JSON. For three corpus experiments, compute the channel-product table over time and check whether it matches Q₈'s multiplication table (with appropriate normalization).

---

### 6. 8-class IR taxonomy ↔ partition of S³ by sign-octants

**Claim strength: ANALOGY → CONJECTURE.** The number 8 matches; the partitioning needs to be verified.

**The math chain:**

CNT classifies every trajectory into one of 8 IR classes:
1. CRITICALLY_DAMPED
2. OVERDAMPED_EXTREME
3. LIGHTLY_DAMPED
4. MODERATELY_DAMPED
5. DEGENERATE
6. D2_DEGENERATE
7. ENERGY_STABLE_FIXED_POINT
8. CURVATURE_VERTEX_FLAT

These are currently characterised by thresholds on amplitude A and damping ζ (continuous parameters). The taxonomy boundaries are documented in the IR taxonomy fix (engine 2.0.3).

The 3-sphere S³ decomposes naturally into 8 sign octants based on the signs of the four quaternion components (a, b, c, d). The quaternion group Q₈ has 8 elements, one in each octant. So the taxonomy and the octant decomposition both have cardinality 8.

The conjecture is that the IR class boundaries are not arbitrary — they coincide with the boundaries between sign-octants when the trajectory's average quaternion is computed.

**Corpus test:** for each of the 25 corpus experiments, compute the time-averaged quaternion (or, equivalently, the dominant axis of the trajectory). Check whether IR class is determined by the sign-octant of that average. If yes, this is a strong confirmation. If only partially yes, the IR thresholds and the octant boundaries are related but not identical, and the relation is interesting in its own right.

---

### 7. Stage 4 cross-dataset comparison ↔ Hamilton product Q₁ · Q₂⁻¹

**Claim strength: EQUIVALENCE.** Different operation names for the same algebraic operation under the candidate identification.

**The math chain:**

CNT's Stage 4 (Order 4+) module performs cross-dataset inference — given trajectories from two or more datasets that share carrier sets, it computes pairwise structural comparisons (relative bearing, relative curvature, divergence ranking).

In quaternion algebra, the relative orientation between two quaternion-valued trajectories Q₁(t), Q₂(t) is:

```
R(t) = Q1(t) * Q2(t)^{-1}    (Hamilton product, quaternion inverse)
```

This R(t) is itself a unit quaternion, encoding the rotation that takes one trajectory's frame to the other's at time t. The decomposition of R(t) gives a relative angle (axis angle of R) and a relative axis (rotation axis of R) — exactly the quantities CNT's Stage 4 computes by hand.

So CNT's Stage 4 is the Hamilton product cast in channel-by-channel notation. The current implementation does pairwise comparisons via explicit angle subtraction; the quaternion view does it by multiplication, which is a single algebraic operation rather than a coordinate-by-coordinate procedure.

**Corpus test:** Stage 4 produces specific output values for the cross-dataset spectrum (`spectrum_paper_codawork2026_ember.pdf`). Reconstruct the same values from the Hamilton product of the participating per-country quaternion trajectories. Diff to numerical precision.

---

### 8. The "helmsman" channel σ (signed-omega) ↔ spinor parity tracker

**Claim strength: ANALOGY.** Naming this isn't the proof; corpus consistency would be.

**The math chain:**

CNT's σ channel is the helmsman corollary: the *signed* angular accumulation, distinguishing left-handed from right-handed rotation. Without σ, ω alone is unsigned and loses handedness information.

In quaternion algebra, the spinor double cover SU(2) → SO(3) is exactly the algebra that **preserves handedness through 720° rotation** — a feature the SO(3) quotient loses. The "lifted" quaternion path tracks which sheet of the cover the trajectory is on; the projected SO(3) rotation does not.

So the helmsman channel σ is the spinor-parity tracker: it carries the information that distinguishes the two preimages of every SO(3) rotation under the SU(2) → SO(3) cover.

**Corpus test:** for any trajectory, if the cumulative σ-integral over the trajectory is an even multiple of 2π, the trajectory is in the vector sector; if odd, the spinor sector. Check whether this parity matches the LIMIT_CYCLE_P1 vs LIMIT_CYCLE_P2 termination codes.

---

### 9. The depth tower ↔ random walk recurrence on S³

**Claim strength: ANALOGY.** Plausible mechanism; not yet shown to be exact.

**The math chain:**

CNT's depth tower applies a contraction operator recursively until termination. Termination codes include LIMIT_CYCLE_P1, LIMIT_CYCLE_P2, SIGNAL_SHORT, ENERGY_STABLE, CURVATURE_VERTEX_FLAT, and others. The tower depth (number of recursion steps before termination) is a per-experiment scalar that varies from 1 (commodities_gold_silver D=2) to 22 (ember_jpn).

A random walk on S³ — repeated multiplication by random unit quaternions — has a well-defined recurrence time: the expected number of steps before the walk returns to a small neighborhood of its starting point. For walks confined to a great circle (degenerate case), the recurrence time is short; for walks that fully explore S³, it is longer.

The conjecture is that CNT's depth tower depth is the recurrence time of the canonical (deterministic, not random) walk corresponding to the trajectory's quaternion-coordinate dynamics.

**Corpus test:** for each experiment, compute the recurrence time analytically from the quaternion dynamics and compare against `summary.curvature_depth` from the JSON. If they correlate strongly across the 25 experiments, the connection is real even if the constant of proportionality varies.

---

### 10. The directness=1 / directness=0 calibration trajectories ↔ pure scalar / pure vector quaternion velocities

**Claim strength: ISOMORPHISM (after explicit construction).**

**The math chain:**

CNT's Stage 2 calibration uses two synthetic reference trajectories: directness=1.0 (a "straight" trajectory through carrier space) and directness=0.0 (a "loop" trajectory that returns to its origin). These give CNT's calibration the IEEE-floor reference points for amplitude and damping.

In quaternion algebra:
- A trajectory with pure-scalar velocity (q̇ = scalar · 1) corresponds to a trajectory that does not rotate — it just translates along the scalar axis. This is the directness=1 case: pure progression with no return.
- A trajectory with pure-vector velocity (q̇ = b·i + c·j + d·k, no scalar component) corresponds to pure rotation on S³ — the trajectory traces a great circle and returns to its start. This is the directness=0 case: pure looping with no progression.

So the directness parameter is the **relative scalar/vector weight** of the trajectory's instantaneous quaternion velocity. directness=1 is "all scalar"; directness=0 is "all vector"; intermediate values are mixtures.

**Corpus test:** the calibration fixtures `STANDARD_CALIBRATION_stage2_*` contain directness=1 and directness=0 reference trajectories. Reconstruct each as a quaternion path. Confirm that the directness=1 path has identically-zero vector-part velocity, and the directness=0 path has identically-zero scalar-part velocity. This test should pass at the IEEE-floor precision the calibration is documented to achieve.

---

## Summary table

| # | Correspondence | Claim strength | Testable on existing corpus? |
|---|---|---|---|
| 1 | Aitchison D=4 ↔ unit quaternions | ISOMORPHISM | Yes — backblaze_fleet |
| 2 | atan2 bearing ↔ quaternion log map | EQUIVALENCE | Yes — any D=4 experiment |
| 3 | M² = I ↔ quaternion conjugation = time reversal | EQUIVALENCE | Yes — pick any 3 experiments |
| 4 | LIMIT_CYCLE_P2 ↔ spinor sector | CONJECTURE | Partially — need synthetic D=4 trajectories |
| 5 | CBS cube ↔ Q₈ Cayley diagram | ANALOGY | Yes — channel-product tables |
| 6 | 8-class IR taxonomy ↔ S³ sign octants | CONJECTURE | Yes — average quaternion per experiment |
| 7 | Stage 4 cross-dataset ↔ Hamilton product Q₁·Q₂⁻¹ | EQUIVALENCE | Yes — diff against existing Stage 4 outputs |
| 8 | Helmsman σ ↔ spinor parity tracker | ANALOGY | Yes — σ-integral parity vs LIMIT_CYCLE_P1/P2 |
| 9 | Depth tower ↔ S³ random walk recurrence | ANALOGY | Yes — correlate depth with computed recurrence |
| 10 | directness=1/0 ↔ scalar/vector velocity | ISOMORPHISM | Yes — at IEEE-floor precision |

**Three of these (1, 7, 10) should produce numerical agreement to ≤ 1e-12.** They are paper-provable. If they hold against the existing corpus on first run, the connection is not a stretch — it is the right name for what CNT has been doing.

**Two more (2, 3) should hold to ≤ 1e-15** if the algebraic identification is the right one.

**Three (5, 6, 9) are softer correspondences** that would still be interesting if they hold approximately but not exactly.

**Two (4, 8) are the deepest claims** and would be the most striking if they survive — they would mean CNT has been doing fermion/boson classification on compositional data without naming it.

---

## What "the connection is real" looks like, operationally

If, on Round 2 of the project, we run claim #1 against backblaze_fleet and the quaternion-reconstructed CLR vectors match the canonical CLR vectors to 1e-12 — then the connection is real. Not "interesting analogy"; not "suggestive structure"; *real*, in the sense that two different mathematical frames are being used to describe the same operation, and the equivalence transform between them is constructible.

If additionally claim #10 holds (the calibration directness=1/0 maps cleanly to pure-scalar/pure-vector velocities) — then we have *two independent confirmations* of the same identification, which is what mathematicians require to call something an isomorphism rather than a coincidence.

At that point QD's status promotes from `0.0.1-experimental` to `0.1.0-candidate`, and the next round becomes worth the engineering investment.

---

*Exploration. The instrument reads. The expert decides. The hashes carry the receipts. The protocol holds the line so the work can move forward.*
