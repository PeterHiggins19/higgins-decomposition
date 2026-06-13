# Clifford + tiling redundancy — compute both, use both (2026‑06‑11)

*A dual‑path, self‑validating reader of a D‑part compositional move. Peter's design: **compute both Clifford and tiling and use them as a redundancy check** — the apps that need what Clifford offers (the global rotor) get it; tiling is the cross‑check; where the full Clifford object becomes intractable, tiling stands alone. This is the framework's own epistemology turned on the geometry: two independent paths landing on the same answer to the machine floor is a confirmation, not a coincidence (the Backblaze+Planck IEEE‑floor pattern; the FDIR dual‑channel doctrine). Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. **Tier 1** (verified/computed on the real CN‑TT v4 atlas).*

Run: `python experiments/clifford_tiling_redundancy_2026-06/clifford_tiling.py` → `results.json`.

---

## The two paths

A D‑part composition has D−1 log‑ratio degrees of freedom, so a move is a rotation in ℝ^(D−1).

1. **Clifford simple‑rotor.** The Spin(D−1) rotor that takes the unit ilr direction at *t−1* to the one at *t*, in their common 2‑plane — computed in closed form (the rotor sandwich `R w R⁻¹` for `R = exp(−(e₁∧e₂)θ/2)`). It yields the **global object** some applications need: the rotation **plane** and the global **angle** θ — used for interpolation (SLERP), global rotational invariants, geometric‑algebra‑native operations. Exact, O(D), valid at any dimension.
2. **Tiling.** Lossless reconstruction of the clr displacement from overlapping exact 4‑part charts (the canonical CN‑TT atlas). Linear in D, exact per chart, streamable, parallel.

## What the run shows (verified)

**Per‑step dual read (D=12, real atlas) — they agree at the floor:**

| step | θ (Clifford) | θ (tiling) | rotor self‑check | tiling lossless | **cross‑residual** |
|---|---|---|---|---|---|
| 1 | 1.286509285 | 1.286509285 | 1.4e‑16 | 2.4e‑15 | **4.4e‑16** |
| 3 | 0.927804211 | 0.927804211 | 1.6e‑16 | 2.2e‑15 | **4.2e‑16** |
| 6 | 1.805191991 | 1.805191991 | 1.3e‑16 | 1.0e‑15 | **3.9e‑16** |

The two independent paths compute the **same rotation angle to nine digits**, and the cross‑residual sits at the machine floor → **redundancy confirmed.**

**The crossover (where Clifford is limited; where tiling stands alone):**

| D | tiling recon err | Clifford simple err | Clifford time | full Clifford multivector dim |
|---|---|---|---|---|
| 4 | 4.4e‑16 | 1.1e‑16 | 0.04 ms | 2² |
| 64 | 3.6e‑15 | 8.3e‑17 | 0.03 ms | 2⁶² |
| 1024 | 7.4e‑14 | 2.3e‑16 | 0.06 ms | 2¹⁰²² |
| 10000 | 1.9e‑13 | 2.2e‑16 | 0.11 ms | 2⁹⁹⁹⁸ (∞) |

- The **Clifford simple‑rotor** (plane + angle) stays **exact and O(D) at any D** — so it is a redundancy check available *everywhere* for single moves, and it hands over the global rotor for free.
- The **full Clifford multivector** object (the even subalgebra, needed for GA‑native *composition of general rotors*) is **2^(D−2)‑dimensional** → intractable past ~D=25. **That** is the boundary Peter named: Clifford‑as‑GA‑object is "limited redundancy to a point," and beyond it **tiling stands alone.**

## The design — compute both, use both

| Regime | Use |
|---|---|
| Any D, single move | **Both.** Tiling = the lossless read; Clifford simple‑rotor = the global rotor (plane+angle) **and** a redundancy cross‑check. Agreement → confidence; disagreement → flag (a fault, per FDIR). |
| Apps needing the global rotor (interpolation, invariants, GA ops) up to ~D=25 | **Clifford gives the data; tiling checks it.** Full geometric‑algebra object affordable here. |
| High D / streaming / GA object not needed | **Tiling alone** — linear, exact, parallel; Clifford's full‑multivector cost is the limiter, not tiling. |

So Clifford is not a fallback for a quaternion limitation — it is the genuine general rotor *and* a free redundancy channel; tiling is the always‑on lossless engine. Used together they **mutually certify** the read.

## Exceeding the combo — the triple‑channel reader (BUILT + VERIFIED, Tier 1)

Two channels can **detect** a fault (they disagree) but cannot **isolate** it (which one is wrong?). The framework's own FDIR doctrine says fault *isolation* needs **≥3 independent channels** and a vote. So the system that exceeds Clifford+tiling is a **triple‑channel reader** (`triple_channel.py`), with three independent reconstructions of the move endpoint:

1. **Tiling** — 4‑part chart reconstruction (independent *data* path).
2. **Clifford** — Spin(n) bivector rotor, closed form (rotor‑algebra path).
3. **Matrix** — explicit n‑D 2‑plane rotation matrix (linear‑algebra path).

A 2‑of‑3 vote emits a **confidence‑graded verdict code** (`SS‑CCC‑LLL`, `SS=RC` "redundancy check"; proposed for `HCI-CNTT/engine/codes.py`):

| Verdict | Code | Meaning |
|---|---|---|
| all 3 agree | **`RC‑CON‑INF`** | consensus — full confidence; emit read + global rotor |
| 2 of 3 agree | **`RC‑ISO‑WRN`** | **isolate** the outlier channel; emit the majority read + flag |
| no majority | **`RC‑HLT‑ERR`** | **halt‑and‑report** — the Safe‑Operations safe state; no read |

**Verified by fault injection** (`triple_results.json`):

| case | verdict | residuals |
|---|---|---|
| clean | `RC‑CON‑INF` consensus | all ~5e‑16 |
| fault in tiling | `RC‑ISO‑WRN` → **isolates tiling** | clif‑til 3.2e‑3, mat‑til 3.2e‑3, clif‑mat 1.8e‑16 |
| fault in clifford | `RC‑ISO‑WRN` → **isolates clifford** | clif‑til 4.4e‑3, mat‑til 4.5e‑16, clif‑mat 4.4e‑3 |
| fault in 2 channels | `RC‑HLT‑ERR` → **halt‑and‑report** | no two agree |

So the dual cross‑check is now a **self‑diagnosing, confidence‑graded instrument**: it detects, isolates, and — when it cannot isolate — refuses to read and reports a safe state. That is the same step up the framework already took for sensor channels (FDIR), now applied to the *mathematics of the read itself.* It maps directly to the **Safe‑Operations + Open‑Loop doctrine** (`huf-gov/doctrine/`): hold‑and‑report is the safe state; the instrument flags, the expert decides.

*Two paths agree at the machine floor — so the read is not a claim, it is a confirmation. Three paths, and a disagreement names its own culprit or steps aside. The instrument reads; the expert decides; the channels carry the receipts.*
