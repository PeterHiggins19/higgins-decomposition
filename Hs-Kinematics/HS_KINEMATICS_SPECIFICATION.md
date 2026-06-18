# Hˢ Kinematics Engine — Full Specification (v1.0, post‑Coimbra)

*The complete designer‑level specification of the unified Hˢ kinematics engine: the one engine that runs the full stack on a composition trajectory and reveals every quantity to the computational floor. This is the reference the pseudocode, the R port, and the replication notebook all mirror. Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. Honest‑broker; claim tiers marked. Conformance anchor recorded in §11.*

---

## 0. Status and scope

This specifies `hs_kinematics_engine.py` (the `run()` entry point) and its companion `hs_diagnosis.py`, as they stand after the post‑Coimbra development arc — the honest‑engine guard layer, the kinematics/dynamics tower, the arrow of intent, the diagnosis language, the fringe/boundary role for EITT, and the streaming data‑prep front door. It is the **distilled** engine: numpy + standard library only, deterministic and hash‑receipted. The frozen CN‑TT oracle adds the deeper depth‑tower / IR / CNQ recursion; this engine is the portable, fully‑qualified working platform that the papers and the guest collaborations stand on.

Everything below is **Tier 1 (deterministic, measured)** except the fringe/boundary layer (§8), which is **Tier 3 (exploratory — a clue, never a claim)**.

## 1. Input contract

- `M` — a real, non‑negative matrix, shape `[T, D]`: `T` ordered records (time/order points), `D` carriers (parts). Need not be closed; the engine closes it.
- `names` — optional list of `D` carrier names; defaults to `c0…c(D‑1)`.
- `dt` — optional time step (default 1.0); scales the derivative tower.

The engine reads the matrix; it does not retain or copy raw data into any claim (*instrument, not data*). Minimum useful shape: `T ≥ 6`, `D ≥ 4` for the full tower (smaller runs degrade gracefully — fewer derivative orders, tiling skipped below D=4).

## 2. Geometry (the Aitchison foundation)

- **Closure** `closure(M)` — clip negatives to 0, divide each row by its sum (zero‑sum rows map to uniform); the composition lives on the simplex.
- **Centered log‑ratio** `clr(P)` — `log(P) − mean(log(P))` per row, with `P` floored at 1e‑12; the isometric image where motion is measured.
- **Helmert / ILR basis** `helmert(D)` — the orthonormal `(D‑1)×D` contrast matrix; available for balance work.
- **Compositional entropy** `shannon_mean(P)` — mean Shannon entropy of the closed rows; the diversity measure behind effective spread and the fringe test.

All later quantities are functions of `clr(P)` and are therefore invariant under part‑relabeling and Aitchison isometry (the property that makes the readings comparable across systems — see Compositional Character Space).

## 3. Carrier guard (E‑21) and zero treatment

- `carrier_health(M)` partitions carriers into **structural zeros** (a part that is zero in every record — a genuine absence), **constant** (non‑zero but never varies), and **active**.
- Structural‑zero carriers are **dropped** and reported (`GD‑ZRC‑CAL`); constant carriers are **retained and flagged** (`GD‑CNC‑CAL`). This is the fix for the all‑zero/constant‑carrier failure that produced `log(0)→NaN→eigh` non‑convergence in the live engine; clean data is untouched (the hash of clean data is unchanged by the guard).
- `treat_zeros(M)` replaces remaining non‑positive entries in a varying carrier with `0.65 × (that carrier's smallest positive value)` — a multiplicative, closure‑respectful zero replacement. **Sparsity** (fraction ≤ 0) is measured and, if ≥ 50%, flagged `GD‑SPZ‑WRN` (the reads remain, but the analyst is told the composition is mostly zeros).

## 4. Lossless reconstruction (the P1 tiling, exactness check)

`tiling_lossless(P)` tiles the carriers into overlapping 4‑part charts, forms the within‑chart pairwise log‑ratios plus the closure row, and least‑squares reconstructs the clr; it reports the **maximum reconstruction error** over the records. On real data this sits at the IEEE floor (≈1e‑15). The output flag `exact` is true when the error is below 1e‑6. This is the run‑time witness of the quaternion‑exact lossless reading (Movement I / P1): the engine demonstrates, every run, that the composition is recoverable from its log‑ratio structure to machine precision.

## 5. Navigation reads

- **Effective spread** (`keff`, navigation) / **entropy diversity** (physics): `exp(Shannon entropy)` — the effective number of active parts; reported start → end (the diversification/concentration trend).
- **Helmsman / fastest coordinate**: three readings, deliberately: the raw fastest clr mover; the **resolvability‑guarded** helmsman (`helmsman_guard`, §6); and the **coherent** helmsman (`coherent_helmsman`, the subcompositionally‑coherent pairwise‑log‑ratio steerer that does not depend on closure choice).
- **Waypoints / phase transitions** (`regimes`): clr step sizes exceeding `mean + 2σ` — candidate structural changes (later refined by hold‑lock, §6).
- **Silent drift / adiabatic drift** (`deceptive`): the count of steps where effective number `K_eff` falls (concentration tightening) while total variation stays at or below its median (motion looks quiet) — the deceptive‑drift signature (Movement V / P2).

## 6. The honesty guards

- **Resolvability** `helmsman_guard` — if the largest total clr movement is below the floor (1e‑6), it returns **nothing** and fires `HM‑NUL‑WRN` (*at rest; refuse to name a leader*); if the top two movers are within a tie band (1e‑3 of the leader), it returns `TIE` with `HM‑TIE‑WRN`.
- **Effective rank** `effective_rank` — the SVD participation ratio of the centered clr trajectory (intrinsic dimensionality of the motion); fires `DG‑RNK‑WRN` if the motion has collapsed to under half the available rank.
- **Hold‑lock** `hold_lock` — discovers the system's own **noise floor** from the clr step distribution (a robust MAD/quantile estimate, floored at the engine epsilon), then runs a **Schmitt‑trigger hysteresis** (enter MOVING above 4×floor, return HOLD below 2×floor) and registers a structural change only when the displacement from the last reference exceeds 3×floor. This is what turns near‑zero drift into either a held rest state or a registered, defensible change — the discovered‑floor + hysteresis answer to "tie down near‑zero drift but identify it as such."

The fired codes are collected in `guards_codes_fired`. The guard philosophy: the engine would rather **hold or warn** than emit a confident‑wrong reading.

## 7. Kinematics and dynamics (the jet to the noise floor)

`mechanics(P, names, dt, noise_ratio=1.5)` computes, in clr space:

- **The jet** — position, velocity, acceleration, jerk, snap, crackle by successive differencing — and stops at the **maximum meaningful order**: the highest derivative whose magnitude amplification ratio over the previous order stays below `noise_ratio` (1.5). Beyond that order the signal is white‑noise differentiation and is *not* reported as structure. (On ~yearly data this typically caps at acceleration.) The amplification ratios are returned so the cutoff is auditable.
- **Turn rate / curvature** — the Frenet curvature of the clr path (median).
- **Arrow of intent / momentum** — mass (the mean adjacent composition) × velocity, summed per carrier into a net momentum vector; the carriers it points **to** (gaining) and **from** (shedding), and a **coherence** scalar = ‖net momentum‖ / Σ‖per‑step momentum‖ ∈ [0,1] (how aligned the motion is — 1 = ballistic, 0 = churn). *This coherence is the principal organizing axis of Compositional Character Space, and the descendant of the loudspeaker's engineered radiation coherence.*
- **Reshaping pressure / force** — `d(momentum)/dt` (mean magnitude).
- **Activity / kinetic energy** — `½ Σ mass·v²` (mean); **transit effort / action** — its time integral.
- **Circulation / angular momentum** — the bivector magnitude `‖r∧p‖` (mean), the rotational content of the motion.
- **Journey / path length**, **net course / displacement**, and **course directness / path efficiency** = displacement ÷ path length ∈ [0,1] (the second directedness measure; with coherence it forms the directedness axis).

Every quantity is named twice (navigation / physics) per `TERMINOLOGY_BRIDGE.md`.

## 8. Spectral modes, equilibrium, fringe

- **Spectral modes** — the leading clr singular values and the **effective dimensionality** (= effective rank, §6).
- **Station keeping / equilibrium hold** — the discovered noise floor and the registered structural‑change indices (from hold‑lock).
- **Fringe / boundary (EITT, Tier 3)** `eitt_boundary` — Shannon entropy of the composition under geometric‑mean decimation at levels (1,2,4); if the **relative drift** across levels stays below the gate (0.01) the structure is *within‑regime* (EITT holds — entropy is decimation‑invariant, the signature of coherent structure); if it drifts past the gate it fires `FR‑BND‑INF` (*at the edge of analysable structure*). This is the old engine's invariant repurposed as a boundary test — Tier 3, a clue never a claim.

## 9. Output schema and determinism

`run()` returns one JSON‑serializable payload: `identity`, `input` (records, carriers, names, sparsity, optional `carrier_guard`), `dead_reckoning…lossless_reconstruction`, `navigation_reads`, `kinematics_and_dynamics`, `spectral_modes`, `station_keeping…equilibrium_hold`, `guards_codes_fired`, `fringe_boundary_TIER3`, `computational_floors`, and a terminal **`content_hash`**.

`stable_hash` rounds every float to 12 decimals, canonicalizes (sorted keys), and SHA‑256s the result — so the receipt is **cross‑platform value‑identical** (demonstrated Windows ≡ Linux). Same data → same payload → same hash. This is the conformance anchor (§11) and the basis of the verify‑after‑push discipline (`ADAPTIVE_ANTICIPATION.md`).

## 10. The diagnosis language (`hs_diagnosis.py`)

A fixed grammar composes the same deterministic readings into a human sentence, and the number of **active voices** = the count of carriers whose net momentum exceeds 12% of the top mover (deterministic — not chosen). A 2‑part system says one or two things; a 60‑taxon microbiome speaks in many voices. At rest it says so in one sentence and stops. Same input → same words → same hash; an LLM may polish the phrasing but the canonical utterance is rule‑generated and carries the numbers' trust.

## 11. Conformance anchor (the determinism receipt)

Reference composition: a fixed 12×6 energy‑transition matrix (`Coal, Gas, Hydro, Nuclear, Wind, Solar`), hardcoded in the replication notebook for cross‑platform reproducibility. The engine on this reference yields:

- lossless reconstruction exact (error ≈ 1.78e‑15), effective dimensionality 1.5, max meaningful order = acceleration, discovered noise floor 0.16009, arrow of intent → Wind, Solar (coherence 0.938), fringe verdict within‑regime;
- diagnosis: *"Coal is steering (shedding). Weight is moving toward Wind, Solar. … The mixture is diversifying (effective spread 4.51 → 5.92). The motion runs in about 2 independent directions. (4 of 6 parts have something to say…)"*;
- **`content_hash = fcae0ebe5c4f443aa076d1900d3d04219c2628591323cd7745621e740a3d7ae7`**.

Any port (R, notebook, future refactor) is conformant iff it reproduces this hash on this reference. A deviation is a precisely‑located signal, not noise.

## 12. Post‑Coimbra changelog (what this version added)

Over CoDaWork 2026 it became clear the static four‑part exactness had to carry into dynamics and high dimension, and into hands that are not CoDa experts. This engine is the response: (1) the **guard layer** — resolvability, coherent helmsman, effective‑rank, discovered‑floor hold‑lock, E‑21 carrier guard, sparsity flag — so the instrument is honest about the limit of its own reading; (2) the **kinematics/dynamics tower** with the noise‑bounded jet and the **arrow of intent**; (3) the **diagnosis language** that scales with complexity; (4) **EITT repurposed** as the Tier‑3 fringe/boundary test; (5) the **dual navigation/physics vocabulary** throughout; (6) the **streaming data‑prep** front door (`hs_data_prep.py`) so any data zip becomes engine‑ready; (7) the **second‑order read** (Compositional Character Space) built on these outputs. The result is one fully‑qualified platform: every diagnostic and control concept in place, deterministic, portable, honest.

## 13. Traceability (a REQUIRED feature)

Full traceability is **not optional** in Hˢ — it is a required property of every read, and the engine is built so that no result can exist without its provenance. A conformant implementation MUST provide all of:

1. **A content receipt on every result.** Every `run()` payload ends with `content_hash` (SHA‑256 over the 12‑dp‑rounded, key‑sorted payload). The same applies to `hs_diagnosis` (utterance hash) and `hs_budget` (budget hash). No reading is emitted without its receipt.
2. **Input provenance.** Any data passing through the streaming front door (`hs_data_prep.py`) carries a `.manifest.json` recording the **source path, the exact config, the output shape, the carriers, and the SHA‑256 of the engine‑ready output** — so a result traces back to the precise input and transformation that produced it.
3. **The chain.** The end‑to‑end path is hash‑linked — `raw data → prep (manifest + output hash) → engine (content_hash) → diagnosis/budget (their hashes)` — the HUF‑STD‑002 "Tensor Train" discipline: every link carries the entry hash forward, so any output is reproducible and auditable to its origin.
4. **Determinism as the guarantee.** Because the engine is value‑deterministic (cross‑platform identical hashes), traceability is *verifiable*, not merely asserted: anyone re‑running the chain reproduces the receipts bit‑for‑bit, or the divergence is located exactly (`ADAPTIVE_ANTICIPATION.md`).
5. **Claim tiers travel with the numbers.** Every reported quantity is marked Tier 1 / 2 / 3, so the *epistemic* provenance (measured vs reasoned vs exploratory) is as traceable as the *computational* provenance.

The requirement, stated plainly: **given any Hˢ result, one can recover the exact input, the exact operations, the exact code version (via the conformance anchor §11), and the confidence tier — and re‑derive the identical receipt.** A result without this chain is not a valid Hˢ result. See `TRACEABILITY.md` for the full specification.

*Companion files: `HS_KINEMATICS_PSEUDOCODE.md` (language‑agnostic), `hs_kinematics.R` (R port), `HS_KINEMATICS_REPLICATION.ipynb` (annotated, reproduces §11), `TRACEABILITY.md`, `DATA_PREP.md`, `MOVING_BUDGET_AND_CONTROL_PRIMITIVE.md`, `DIAGNOSIS_LANGUAGE.md`, `TERMINOLOGY_BRIDGE.md`. The geometry is CoDa's; the engine is the instrument built on it.*
