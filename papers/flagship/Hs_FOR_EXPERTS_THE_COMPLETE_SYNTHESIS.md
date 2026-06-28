# Hˢ for experts — the complete synthesis

### A deterministic, exact, hash-receipted instrument for reading compositions, with its information theory, its kinematics, EITT, and its honest boundary

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-23. Written for
scientists, data engineers, information theorists, and engineering experts — people who will, correctly, want
the math, the receipts, and the limits before the story. Every headline number cites a reproducible experiment
and a SHA-256. Claims are tiered: **T1 measured/proven · T2 reasoned/sound · T3 open or rejected.** Nothing in
this document is a marketing claim; where Hˢ cannot do a thing, it says so. Peter is the sole gate; nothing
posted.*

---

## 0. The thesis, in three sentences

A **composition** — parts of a conserved whole, where information lives in the ratios — is not merely data to
be summarized; it is a **structured message**, and read in the right geometry it behaves like a communication
channel whose capacity grows with the number of parts. Hˢ is the **deterministic, exact, hash-receipted reader
of compositions**: it reads the relational structure to the IEEE floor, tiles to any dimension, withholds when
the evidence is thin, and stamps every output with a content hash so any third party can re-run it and get the
same answer. The synthesis that organizes everything below is one line — **the data is the carrier**: a
composition's own organization supplies the reference, the coordinate frame, and the noise rejection, so there
is nothing separate to generate or strip away.

If you read only one thing: Hˢ's distinctive position is the **intersection** of *compositional* data and
*audit-critical* decisions — where the answer must be reproducible to the bit by a regulator, insurer, court,
or reviewer. That intersection is thinly served, and it is the whole reason the determinism is foundational
rather than decorative.

---

## 1. First principles — why compositions, and why a ground state

A composition `x = (x₁,…,x_D)`, `xᵢ > 0`, carries only **relative** information: it is invariant under
multiplication by any positive scalar (Aitchison 1982/1986). Closed to a constant sum it lives on the simplex
`S^{D-1}` with the **Aitchison geometry**; its natural coordinates are log-ratios,

```
   clr(x)ᵢ = log xᵢ − mean_j(log xⱼ)        (centred log-ratio, sums to 0)
   ilr(x)  = clr(x) · Hᵀ                     (isometric log-ratio; H = Helmert basis, D−1 coords)
```

The ilr map is an **isometry onto ℝ^{D-1}** and a **bijection on the simplex** — it loses nothing.

The reference state is not arbitrary. Hˢ descends from an acoustic origin (Rogue Wave Audio): a finite body
radiating into a room has, at low frequency, an isotropic pattern — energy shared equally across all
directions. That uniform pattern is the **barycentre of the simplex** `(1/D,…,1/D)`, the maximum-entropy,
zero-information **ground state**, and the conserved diffraction budget (`6.02 dB = 20·log₁₀2`) apportioned
across the cabinet's dimensions is, term-for-term, a composition with closure. *The information is the departure
from the ground state; the ground state had to come first.* (Tier 1 for the acoustic system; the
generalization to abstract compositions is standard math soundly applied.)

Two consequences that matter to an information theorist immediately:

- **Closure is common-mode rejection.** Any factor common to all parts — a gain, a level, a distance, an
  illumination, a broadband common interferer — cancels under closure: `clr(g·x) = clr(x)` exactly. This is the
  multiplicative twin of a balanced/differential line.
- **The log-ratio is the differential, reciprocal coordinate.** `log(a/b) = −log(b/a)` — antisymmetric,
  bidirectional, and the substrate of every reading below.

---

## 2. The exact mathematics — the quaternion rung, tiling, and the boundary

**The exact rung (D=4).** A four-part composition's three ilr coordinates are the imaginary part of a
quaternion `v ∈ Im(ℍ) ≅ ℝ³`; an Aitchison perturbation is the **sandwich** `q v q*` for a unit quaternion
`q ∈ S³ = SU(2)`, reproducing an SO(3) rotation **to the IEEE floor** (residual ≈ 1.1–4.4×10⁻¹⁶, twice machine
epsilon, bit-identical across platforms). The six left/right multiplication generators close as
`so(4) ≅ su(2) ⊕ su(2)` — the full local symmetry of the four-part chart. *(T1; HS-GOLD-1 fixture F1.)*

**Why four, and where it stops — the Hurwitz boundary.** The exactness is a property of **normed division
algebras**, which by Hurwitz exist only in dimensions 1, 2, 4, 8 (ℝ, ℂ, ℍ, 𝕆). At the octonions associativity
is lost; at the sedenions division is lost (an explicit zero divisor exists). So the "a composition *is* a
single hypercomplex number with exact conjugation-rotation" identity is a **D≤4 phenomenon** (with the SO(4)
two-sided action at D=5), and **not extendable**. This is a theorem, not a limitation to be engineered around.
*(T1; `THE_LADDER_AND_THE_BREAK.md`.)*

**Tiling to any dimension.** A composition of dimension D is covered by **overlapping exact four-part charts**
sharing pivot parts; the global clr state is reconstructed from within-chart log-ratios by a graph-Laplacian
solve. Reconstruction is exact in exact arithmetic **iff the chart graph is connected**; in floating point the
residual scales with the **chart-graph diameter**, not D — a *balanced-tree* atlas (diameter O(log D))
reconstructs to **D = 10⁶ at ≈10⁻¹²** (direct sparse solver), while a *path* atlas (diameter O(D)) degrades by
three orders by D≈16k. *(T1; P1 re-validation, receipt `99ec0581…`. Honest: high-D is **numerical
reconstruction, not bit-exact identity** — never claimed as "lossless at scale.")*

**Generation, unbounded.** Inverting the reader, Hˢ **generates** exact SO(n) for **any** n: every rotation
factors into ⌊n/2⌋ commuting plane rotations, the coordinate form of the Spin(n) rotor sandwich `R v R̃` in the
Clifford algebra Cl(n). Measured exact to the floor to **n = 1024** (orthogonality ≈1.8×10⁻¹⁵; rotor = planar
to ≈10⁻¹⁶). *(T1; receipt `8107b173…`.)* So: **exact rotation goes all the way; the single-number
compositional identity goes to four; arbitrary dimension goes by tiling.**

---

## 3. Determinism and the trust contract — why this is auditable

For a data engineer and an information theorist this is the load-bearing property. Hˢ is a **fixed computation
under a determinism contract (HS-EPS-1):** same input → same output → same **SHA-256** receipt, byte-identical
across operating systems, Python/numpy versions, and clock time (timestamps excluded from the hashed payload).
Conformance is the **frozen golden fixture set HS-GOLD-1**, master hash `d7ac6530…`; a build is genuine Hˢ only
if `hs_gold_fixtures.py --verify` reproduces it. The fixtures hash **platform-stable rounded signal and
pass-flags**, never raw floor-jitter residuals — so the master hash certifies *meaning*, not luck.

Why this compounds:

- a third party can **check** instead of **trust** (the receipt);
- a network of nodes verifies each other **non-contact** — *transitive trust*, explicitly **≠ transitive
  truth** (a hash certifies the *reading*, not the *data*);
- a machine may **act** on a read only because the read is **re-runnable** — safe delegation behind breakers;
- the instrument's **own signature is ~zero** — it is inert to ~10⁻¹⁵, so it reads cleanly and adds nothing.

---

## 4. The reading — kinematics, guards, and the blindness suite

Hˢ reads a composition **in motion**. From a trajectory of compositions it computes, deterministically:

- **arrow of intent** — the mass-weighted net log-ratio flow: which parts gain vs donate share, and how
  committed the motion is (direction + magnitude);
- **character** — Ballistic (one directed arrow) · Contested · Turbulent · Diffusive (churn), via coherence
  `‖Σv‖/Σ‖v‖`;
- **effective dimension** — the participation ratio of the ilr trajectory (often ≪ D−1; this is the
  compressible, denoisable structure);
- **the jet** — velocity/acceleration on the Aitchison manifold, with a noise-bounded maximum order as an
  honesty ceiling.

**Guards and the gate.** The pipeline is a documented state machine: qualifier gate (refuse non-compositional
input) → closure → clr/ilr → guards (zero-treatment, effective-rank, hold-lock hysteresis, carrier guard E-21)
→ kinematic read → **coherence gate** (withhold with code `MO-DIF-WRN`/`MO-NUL-WRN` rather than draw an arrow
the data does not support) → receipt. *The instrument would rather refuse than be confidently wrong; a refusal
is a result.* The operator holds the master breaker; full automation is never reached by design.

**The blindness suite — what each reading cannot see.** Every reading is a projection blind to its complement;
naming the blindness names a recoverable event class:

| reader | blind to | recovered class | recovered by | status |
|---|---|---|---|---|
| scalar / threshold monitor | the **ratios** | deceptive / silent drift | the relational read | T1 |
| helmsman (`argmax|Δclr|`) | the **mass** | small-fast vs where-the-bulk-goes | momentum (mass-weighting) | T1 |
| direction / rotation read | the **size** | budget move with no turn | the dual-quaternion translation channel | T1 |

Measured on a real drive fleet: the relational read surfaces **159 silent-drift pre-fault events** the
threshold view misses, and the SO(4) read adds **30 rotation-blind size events** as a second orthogonal class.
The framing-level member, **"data-blind,"** is the field's assumption that a message needs a separate carrier
(§7). *(T1; `THE_BLINDNESS_SUITE.md`, receipts `058fde30…`, `d531e545…`.)*

---

## 5. EITT — the intrinsic timescale, explained honestly

**The claim.** EITT (Entropy-Invariant Time Transformer) is the temporal face of one idea: *the characteristic
timescale of a compositional system belongs to the object, not to the analyst.*

**Why the timescale is intrinsic (the spatial face, DADC).** In the acoustic origin, the corner frequency
`f_c = 115 / dim` is **not fitted** — it falls out of a boundary condition: when the wavelength reaches the size
of the radiating body, the pattern *must* break, and the physics fixes where. Frequency is the reciprocal of
time, so the characteristic timescale is a **property of the radiating object**, set by the ratio of a wave to
a dimension — not a coordinate someone imposed. This is the deep point that earns the blank stares: in a
conventional model you *choose* a time axis and lay an operator over it, and the dynamics then live in that
choice. Here there is no such choice to make.

**The temporal face (EITT), measured.** Take the **Shannon entropy** of a compositional time series and
coarse-grain time by **geometric-mean decimation** (the compositional-geometry-correct way to merge adjacent
samples). The entropy stays **near-invariant**: measured drift **0.18% over a 341:1** time reduction
(reproduced 0.17% on a synthetic signal, `d8c21c70…`). It holds *because the timescale was intrinsic to begin
with* — coarse-graining cannot destroy a structure the geometry already fixed. DADC is the spatial/frequency
face; EITT is the temporal face; both say the same thing.

**The honest envelope — read this before citing EITT.**

- **Tier 1:** the *measured* entropy invariance under geometric-mean decimation, with its kill conditions
  named (proportional data; sufficient carrier dimension; conservation not prediction; external forcing
  invisible).
- **Critical disambiguation:** this is **Shannon (information) entropy**, **not thermodynamic entropy.** The
  invariance is an information-geometric property of compositional time series under a specific decimation; it
  is **not** a statement about the second law, and Hˢ never conflates the two.
- **Divided status (honest):** EITT's place in the framework is deliberately split — it is a **measured test
  and an open theoretical problem**, *not* a load-bearing engine. The instrument does not depend on EITT; EITT
  is a phenomenon the instrument exposes and that invites a proof. *(See `EITT_PAPER_SEED.md`,
  `EITT_CANONICAL_EXPLANATION_*.md`, and the HUF note on the place EITT holds.)*

So to an information theorist: EITT says a compositional source has an **intrinsic information rate that is
stable under correct temporal coarse-graining** — a useful, falsifiable, measured property — and nothing more
grandiose than that.

---

## 6. The information theory — capacity, coding, channel, and the honest cap

This is the part built for information theorists and communications engineers; it is also the most carefully
caveated.

**The Compositional Message Principle (CMP).** The discriminative signal about an external label lives in the
inter-part log-ratios. Formally the ilr map is a **sufficient statistic** (a bijection on the simplex), so by
the **data-processing inequality** any scalar aggregate (Shannon diversity, dominance, depth) carries ≤ the
relational information and can be **null while the relational read is strong.** Measured on real gut-microbiome
data (Crohn's, N=975): relational CV-AUC **0.832** vs diversity/depth scalars at **chance (~0.5)**, PERMANOVA
p=0.001; replicated on an independent HIV cohort (p=0.002). *(T1; `acf65ce…`.)*

**Dimension is the message — capacity grows with the number of parts.** As the number of parts grows 5 → 48 on
the Crohn data, the relational signal rises (**AUC 0.64 → 0.83**) and the composition's **symbol-capacity** —
the Gaussian-channel capacity over its ilr covariance eigen-directions — grows **7 → 79 bits**, while the
scalar Shannon read stays at chance. More parts = more message and more communication symbology. *(T1;
`bf24c615…`.)* This is the compositional realization of the comms fact that *N-dimensional constellations carry
more symbols.*

**The codec and the channel.** Generator and reader are exact inverses, so the pair is a **deterministic
codec**: a payload maps to the ⌊(D−1)⌋ log-ratio channels of a composition and decodes byte-exact. The channel
self-protects (closure rejects common-mode gain — measured **313 dB**, residual 8.9×10⁻¹⁶ on a 26.7 dB swing,
exact to the floating-point floor — note: a *numerical* rejection, not an analog CMRR, and bounded in any real
system by the ADC). Additive noise off the coherent k-subspace is removed **exactly** at `10·log₁₀((D−1)/k)`
dB; in-subspace random noise is provably **not** separable and the instrument returns **0 dB and says so**.
*(T1; `cb0c3f52…`, `d8c21c70…`.)*

**Compression — measured, not claimed.** On real 8-part energy-mix data, Hˢ's compositional coder reaches the
target fidelity at **~3.5× fewer bits than a structure-agnostic baseline and ~10× smaller than lossless float**,
running **within ~10%** of the entropy of its own symbols. *(T1; `305cc0db…`.)*

**The crowning demonstration — Hˢ Duplex.** A full **bidirectional** loop done entirely by compositions: Node A
generates a deep message (an *instruction* + a payload), encodes it into compositions, transmits over a noisy
channel; Node B decodes it byte-exact (common-mode rejected), **observes the instruction, runs Hˢ on the
payload** (compute-in-the-loop), encodes the reading, transmits back; Node A decodes the result and
**re-derives B's result hash from the reply** — end-to-end integrity without trust. Round-trip exact; capacity
16 → 376 bits/composition for D = 3 → 48. *(T1; `4241d38a…`.)*

**The honest cap, stated to the information theorist directly:** **no Shannon limit is beaten, and none is
claimed.** Channel capacity and the true source rate-distortion bound are theorems; the apparent "below the
bound" in early drafts was a **self-caught mislabel** (the Gaussian rate-distortion is a *ceiling*, not a
floor). What Hˢ offers is **determinism, end-to-end integrity, exact common-mode rejection, interpretable
channels, and control intrinsic to the data** — value *within* information theory, not beyond it. In the
Shannon–Weaver hierarchy, Hˢ operates at the **semantic** and **effectiveness** levels (the message is
understood and acted on) — the live "beyond-Shannon" goal-oriented / semantic-communication paradigm — but in
the **deterministic, exact, auditable** corner that the field's dominant deep-learning approaches leave open.

---

## 7. The keystone — the data is the carrier

Pulling §1, §4, and §6 together: a composition's own relational organization plays **every role a communication
carrier plays** — the barycentre is the reference, the log-ratio geometry is the coordinate frame, closure is
the noise rejection. There is **nothing separate to generate, modulate, or strip away**; the control is
intrinsic to the data. The Duplex proves a message, an instruction, and a verified answer travel with **no
control channel**. The reason this is hard to see — the "where is the carrier?" reflex — is **data-blindness**:
a framing assumption, not a missing measurement, that a message requires a carrier distinct from itself. It is
the hardest blindness because the frame is invisible from inside it. *(T2 thesis; T1 demonstration.)*

---

## 8. Where it stands against the world (web-checked)

| idea | standing | Hˢ's relation |
|---|---|---|
| Compositional data / log-ratios / D→D−1 coords | established (Aitchison; CoDa community) | the geometry Hˢ uses and cites |
| "A community is a message; species are symbols" | established, old (Margalef, E.O. Wilson) — but read as a **scalar** diversity index | Hˢ advances it to the **relational, dimensional** read (the scalar is shown to be at chance) |
| Quaternion/SO(4)/dual-quaternion computation | mature (ADCS, robotics/SLAM, graphics, gauge theory) | Hˢ is **not** a leader here; it uses the exact rung and the SE(3) read on *compositions* |
| Semantic / goal-oriented (beyond-Shannon) communication | a major, funded 6G thrust — but mostly **deep-learning, lossy, opaque** | Hˢ is the **deterministic, exact, auditable** corner; not first, but distinct |
| In-band signaling / self-describing data | established for decades | "control in the data" via **geometry**, not metadata or a trained model — the novel step |
| **Compositional relational geometry as a channel whose capacity grows in D** | **not in the literature — it crawls** | **Hˢ's distinctive, now-measured contribution** |

Honest scope: on the narrow self-defined intersection — *exact, deterministic, hash-receipted reading of
compositions as kinematics and as a channel* — direct competition is thin, **partly because the intersection is
self-defined**; that is a real differentiator and a thin moat at once. Leadership here is **earned by receipts,
not claimed by priority.**

---

## 9. The evidence — the nine-study trust

Three measured witnesses *locate* the compositional law across systems that cannot have agreed in advance;
each is reinforced into a **three-study trust** (HUF support standard, nine studies total):

- **Microbiome** (living): Crohn relational read · HIV replicate · dimension-is-the-message.
- **Geoscience** (deep time): Frielingen-9 mudstone (3/3 located, eff-dim 2.23→1.65) · independent ball-clay
  oxides · Hs-05 regional geochemistry.
- **Engineered fleet**: Backblaze drive fleet (159 silent-drift) · rotation-blind SO(4) class · deceptive-drift
  null. *(`NINE_STUDY_TRUST_LEDGER.md`.)*

The recurring measured fact across all nine: **the discriminative signal is relational and grows with the
number of parts; the scalar/aggregate read is blind.**

**Receipt index (reproduce any of them):** exact rung & SO(n) `8107b173` · P1 tiling `99ec0581` · conformance
`d7ac6530` · common-mode `d8c21c70` · denoise `cb0c3f52` · compression `305cc0db` · QAM `f502c15d` · CMP
`acf65ce` · dimension `bf24c615` · Duplex `4241d38a` · self-read `120bb621`.

---

## 10. The honest boundary — what Hˢ does NOT do

Stated plainly, because a serious reader checks the limits first:

- **It is not lossless at scale.** Exact at D=4; high-D reconstruction is floating-point, residual grows with
  chart-graph diameter (Hurwitz forbids more).
- **It does not beat Shannon** — channel capacity or the true rate-distortion bound. The 313 dB is a *numerical*
  common-mode figure, ADC-bounded end-to-end, not an analog CMRR.
- **It does not forecast.** The kinematic read is of the **present**; momentum continues "absent a force," and
  the instrument does not claim no force will act.
- **It does not cancel in-subspace random noise** — only common-mode multiplicative and off-subspace/structured
  additive; otherwise it returns NO.
- **It is a complement, never a controller of record.** The human gate is structural; full automation is never
  reached.
- **EITT is a measured phenomenon and an open problem, not an engine**; Shannon entropy ≠ thermodynamic
  entropy.
- **Universality is located, not proven.** Three (now nine) studies *locate* the law; peer review decides reach.

These are not hedges; they are the spec. A deterministic instrument is valuable precisely because it can be
tested and will answer **yes or no.**

---

## 11. How to engage (reproduce, then extend)

1. **Read** — `IS_Hs_RIGHT_FOR_YOU.md`, the manuals (`manuals/`), the datasheet (`papers/datasheets/HS-CN1_DATASHEET.md`).
2. **Run** — point the engine at any table of conserved-budget rows; you get the read + a receipt.
3. **Verify** — `experiments/conformance_fixtures_2026-06/hs_gold_fixtures.py --verify` reproduces `d7ac6530…`.
4. **Extend** — the open determinism contract (HS-EPS-1), the SO(n) generator, the four-form port; the
   blindness suite is open (a fourth face joins only with a receipt).

The contribution is reproducible by anyone who adopts the discipline — determinism, exactness, receipts, honest
tiers. That is a feature, not a vulnerability: the work survives even if someone else builds it, because it is
checkable.

---

*Cross-refs (the substance behind each section): `GROUND_STATE_AND_TRACTION.md`, `../P7_FOUNDATIONS_SEED.md`,
`../frontier/HOW_FAR_THE_MATH_GOES.md`, `../frontier/THE_LADDER_AND_THE_BREAK.md`,
`../frontier/SO4_SPIN4_FUTURE_COMPONENT.md`, `../frontier/HS_ENGINE_MORPHOLOGY_AND_CODEC.md`,
`../COMPOSITIONAL_MESSAGE_PRINCIPLE_PAPER_SEED.md`, `../EITT_PAPER_SEED.md`,
`PURE_SIGNAL_EXTRACTION_FROM_THE_GROUND_STATE.md`, `../NINE_STUDY_TRUST_LEDGER.md`,
`../COMMUNICATIONS_GEOMETRY_LITERATURE_SCAN.md`, `../WORLD_TEST_AND_VALUE_compositional_semantic_comms.md`,
`../../library/THE_DATA_IS_THE_CARRIER.md`, `../../library/THE_BLINDNESS_SUITE.md`, `../../manuals/`,
`../../experiments/`. Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — numbers cited-or-fenced · math proven + receipted · value shown · experts decide.*
