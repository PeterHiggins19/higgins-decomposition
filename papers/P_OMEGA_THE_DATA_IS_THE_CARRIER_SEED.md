# P‑Ω (seed) — Deterministic Compositional Communication: when the data is the carrier

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-23. The pinnacle
paper of the Higgins-Decomposition series: the proof, the fixed point, and the demonstration that a
composition's own relational geometry *is* the carrier — so message, control, and answer travel with no
separate carrier and no control channel, deterministically and auditably. Off the public repo (abstracts
only); honest-broker tiered; nothing posted; Peter is the sole gate.*

---

## Abstract (working)

A communications engineer asked, on hearing the goal, "where is the carrier?" — the trained separation of a
generated carrier from an imposed payload. We answer with proof: for **compositional data** (parts of a
conserved whole), the data's own geometry performs every function a carrier performs. (i) **Closure** supplies
the reference and rejects any gain common to all parts — `clr(g·x) = clr(x)`, exactly. (ii) The **isometric
log-ratio (ilr)** map supplies an orthonormal coordinate frame — a bijection on the simplex onto ℝ^{D−1}.
(iii) The **log-ratios carry the symbols**, and by sufficiency and the data-processing inequality the
transmittable information is relational and **grows with the number of parts D** (measured: capacity 7→79 bits
as D goes 5→48). The encode/decode pair are **exact mutual inverses** — the message is a *fixed point* of
decode∘encode (measured 1500/1500 exact over D = 3…48), and determinism makes the content receipt a fixed point
under recomputation — so the claim is not only argued but **anchored and checkable**. We demonstrate a full
bidirectional protocol (Hˢ Duplex) in which an instruction is carried, *observed and executed by the engine*,
and the verified result returned — all by compositions, common-mode-robust, hash-audited end to end. We place
the result in **Deterministic Identification** theory and **Semantic-Channel Theory**, and we state the cap
plainly: no information-theoretic limit is beaten; the contribution is a *deterministic, exact, auditable*
realization in which **the control is intrinsic to the data**. *Tier 1 the proofs/measurements; T2 the
positioning; T3 no priority/beyond-Shannon claim.*

## 1. The question, and the answer

The carrier-vs-payload separation is so deep it is invisible from inside the field (we name this framing
blindness **data-blind**). The answer is that for compositions the separation is unnecessary: **the data is the
carrier.**

## 2. The proof — three propositions (math it)

Let `x ∈ S^{D-1}` be a composition (`xᵢ>0`), `H` the Helmert basis, `clr`/`ilr` the centred / isometric
log-ratio maps.

**Proposition 1 (the carrier reference — common-mode rejection).** For any common gain `g>0`,
`clr(g·x) = clr(x)` and hence `ilr(g·x) = ilr(x)`. *Proof:* `clr(g·x)ᵢ = log(g xᵢ) − mean_j log(g xⱼ) =
log xᵢ − mean_j log xⱼ = clr(x)ᵢ`. ∎ *(So the composition carries its own reference; level/distance/illumination
drift cannot move it. Measured rejection of a 26.7 dB swing: residual 8.9×10⁻¹⁶, `d8c21c70…` — a numerical
figure, ADC-bounded end-to-end.)*

**Proposition 2 (the carrier frame — an exact coordinate system).** `ilr = clr · Hᵀ` is an **isometry** from
the Aitchison simplex onto ℝ^{D−1} and a **bijection** (it loses nothing); `clr = ilr · H` inverts it exactly.
*(So the composition carries its own orthonormal frame — no external frame to synchronize. Cf. P1's D=4
quaternion exactness as the frame's exact rung.)*

**Proposition 3 (the symbols — relational, and growing with D).** The ilr map is a **sufficient statistic** for
any label on the simplex; by the **data-processing inequality**, any scalar aggregate carries ≤ the relational
information. The number of independent symbol channels is **D−1**, and the channel capacity of the composition
(Gaussian capacity over the ilr covariance eigen-directions) **increases with D**. *(Measured on real Crohn
data: relational AUC 0.64→0.83 and capacity 7→79 bits as D goes 5→48, scalar read at chance; `bf24c615…`.)*

**Corollary (the carrier theorem, stated honestly).** Closure (P1), the ilr isometry (P2), and the relational
log-ratios (P3) together perform the three functions of a communications carrier — **reference, frame, and
symbol-bearing** — using only the data's own organization. Therefore a composition needs no carrier distinct
from itself: **the data is the carrier.** *This is the composition of three established/measured facts, not a
new grand theorem — which is exactly why it is checkable.*

## 3. The fixed point (fix-point it)

The argument is anchored by an **exact fixed point**, which is what turns "a good idea" into "a proof you can
re-run":

- **Inverse pair.** The encoder `E` (structure → composition) and reader `R` (composition → structure) satisfy
  `R∘E = id` on the message space — the message is a **fixed point** of `R∘E`. Measured **1500/1500 exact** over
  D = 3, 4, 8, 16, 48 (`742f1b5a…`).
- **Recomputation fixed point.** Determinism makes `M ↦ SHA256(E(M))` single-valued: the same message yields the
  same composition and the same receipt on any machine, every run. (The string `"the data is the carrier"`
  encodes to a fixed composition hash.)

The fixed point is the engineer's "wee bit of proof": the carrier claim is not asserted, it is **pinned** —
exact, reproducible, hash-anchored.

## 4. The demonstration — Hˢ Duplex

A full bidirectional loop done entirely by compositions: Node A generates a deep message (instruction +
payload), encodes it, transmits over a ±20 dB common-mode + additive channel; Node B decodes it byte-exact,
**observes the instruction, runs Hˢ on the payload** (compute-in-the-loop), encodes the reading, returns it;
Node A decodes the result and **re-derives B's result hash** — end-to-end integrity without trust. Round-trip
exact; capacity 16→376 bits/composition for D = 3→48 (`4241d38a…`). The link carries *understanding*, with no
control channel.

## 5. Position (engage the rigorous frame)

- **Deterministic Identification (DI) theory** (active, IEEE ICC 2026 / Trans. IT 2025): the information-theoretic
  home for deterministic message handling over channels — P‑Ω is a *compositional* instance; the DI capacity
  comparison is the named formal test.
- **Semantic-Channel Theory / goal-oriented (beyond-Shannon) communication** (Shannon–Weaver semantic +
  effectiveness levels): P‑Ω operates at those levels but in the **deterministic, exact, auditable** corner the
  dominant deep-learning approaches leave open.
- **In-band signaling / self-describing data** (established): "control in the data via geometry," not metadata —
  the novel step.

## 6. The honest cap

No Shannon channel capacity or true source rate-distortion bound is beaten or claimed. Capacity is bounded as
always; the additive margin is a finite measured operating point; the 313 dB common-mode is numerical, not an
analog CMRR. The contribution is **determinism, end-to-end integrity, exact common-mode rejection,
interpretable channels, and control intrinsic to the data** — value *within* information theory.

## 7. Tiers

- **T1 (proven/measured):** Props 1–2 (algebra), Prop 3's sufficiency/DPI + the measured capacity (`bf24c615`),
  the fixed point (`742f1b5a`), the Duplex (`4241d38a`), common-mode (`d8c21c70`).
- **T2 (reasoned):** the carrier corollary as the unifying reading; the DI / Semantic-Channel positioning.
- **T3 (open / rejected):** priority/"first" — to the arXiv timestamp; beyond-Shannon — rejected; the DI-capacity
  and hardware comparisons — to earn.

*Cross-refs: `flagship/Hs_FOR_EXPERTS_THE_COMPLETE_SYNTHESIS.md`, `../library/THE_DATA_IS_THE_CARRIER.md`,
`../experiments/hs_duplex_2026-06/`, `../experiments/dimension_is_the_message_2026-06/`,
`P_C_COMPOSITIONAL_CODING_SEED.md`, `WORLD_TEST_AND_VALUE_compositional_semantic_comms.md`,
`THE_PINNACLE_RELEASE_ARCHITECTURE.md`. Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — numbers cited-or-fenced · math proven + receipted · value shown · experts decide.*
