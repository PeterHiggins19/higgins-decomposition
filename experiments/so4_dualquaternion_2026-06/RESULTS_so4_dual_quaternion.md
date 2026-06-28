# RESULTS — the SO(4) / dual-quaternion SE(3) component, built and tested

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-23. This is the
worked, receipted construction `papers/frontier/SO4_SPIN4_FUTURE_COMPONENT.md` §5 named as the one thing that
could move the second-`su(2)` material from **T2/T3 → T1**: a dual-quaternion encoding of a rigid pose
(rotation **+** translation) of a compositional configuration, read back to the IEEE floor, deterministically,
hash-receipted. It is now built and it passes. Honest-broker tiers below.*

---

## What was built

The frontier note established (T1) that the four-part chart carries the full **Spin(4) = SU(2)×SU(2)**
symmetry, but the P1 reading uses only the adjoint **SO(3)** (the sandwich `q v q*`) — it spends 3 of the 6
available degrees of freedom and leaves the second, independent `su(2)` on the table (§2). The note's §6 also
showed the *ill-posed* way to use that second handle (recovering separate global/local rotation frames is a
gauge redundancy) and pointed instead to the **well-posed** use: let the second factor carry **translation**, a
physically observable DOF — i.e. **dual quaternions**, the standard rigid-pose tool in robotics/aerospace.

The build (`dual_quaternion_se3.py`; reproducible single file `run_so4_selftest.py`) implements that: a unit
dual quaternion `η = q_r + ε q_d` (ε²=0) with `q_d = ½ t q_r`, encoding rotation **and** translation as one
exact object, with exact read-back of both, exact composition of rigid motions, and the screw (Chasles)
decomposition.

## The test battery — all pass, to the IEEE floor

Deterministic (seed 4; 4,000 random trials per numeric test). Receipt below.

| # | what is checked | residual | tier |
|---|---|---:|---|
| **T1** | `so(4) = so(3)_L ⊕ so(3)_R`: recompute left/right commutators from the Hamilton product — `[L_i,L_j]=+2ε_{ijk}L_k`, `[R_i,R_j]=−2ε_{ijk}R_k`, `[L_i,R_j]=0` | **exact 0** | T1 |
| **T2** | two-sided action `x ↦ q_L x q_R^*` is a genuine SO(4) element (orthogonal, det +1) | orth **8.9e-16**, det **1.6e-15** | T1 |
| **T3** | Spin(4) double cover: `(q_L,q_R)` and `(−q_L,−q_R)` give the **identical** SO(4) matrix | **exact 0** | T1 |
| **T4** | pose round-trip `(q_r,t) → η → (q_r,t)` exact | rot **0**, trans **1.4e-14** | T1 |
| **T5** | rigid-motion composition: dual-quaternion product == homogeneous 4×4 composition | **1.1e-14** | T1 |
| **T6** | **four-form conformance**: a 4-part composition's ILR point moved by a pose four independent ways — (A) dual-quaternion sandwich, (B) extract-then `Rp+t`, (C) homogeneous 4×4 — agree | **1.4e-14** | T1 |
| **T6b** | screw / Chasles rotation recovery from the dual quaternion | **1.4e-16** | T1 |
| **T7** | determinism: full re-run yields the byte-identical SHA-256 | **match** | T1 |

**Receipt (canonical-JSON SHA-256):** `b0fd32a2a1eac074d68024861bb9229a6998b436252a8fea94e6b9652979c813`
(`run_so4_selftest.py`, seed 4). Same input → same output → same receipt.

## One honest note on process (the test did its job)

The first run **failed T6** by ~31 (not a rounding miss — a real error): the point-transform sandwich used the
wrong dual-quaternion conjugate. The correct point-transform conjugate is the **combined** one,
`η⋆ = q_r^* − ε q_d^*` (quaternion *and* dual conjugate), which collapses the dual part to exactly `R p + t`.
The four-form cross-check is what caught it — a single-form implementation would have shipped the bug silently.
That is the Proof & Honesty Standard working as intended: the receipt corrected the claim.

## What this does and does not establish

- **T1 (established now):** the dual-quaternion / Spin(4) SE(3) reading is implemented, **exact to the IEEE
  floor**, composes correctly, reads back rotation **and** translation, and is **deterministic + hash-
  receipted**. The second `su(2)` is no longer "on the table" — it carries translation, exactly.
- **T2 (still):** the *Hs application* — using this to read a real constellation pose/control trajectory or an
  SMT-line kinematic configuration — is a sound mapping, **not yet run on real field data**. The promotion is
  of the *capability* (built + exact), not of any domain result.
- **Not claimed:** no accuracy/performance advantage over existing dual-quaternion libraries (the algebra is
  shared, mature). The distinctive Hs contribution is the **exact + deterministic + hash-receipted + with
  withholding-guards reading of a *composition* as a 6-DOF pose** — the intersection of
  `WHERE_HS_BELONGS.md`, now demonstrated rather than asserted.

## Reproduce

```
cd experiments/so4_dualquaternion_2026-06
python3 run_so4_selftest.py          # prints the table + receipt; exit 0 iff ALL_PASS
```

*Cross-refs: `../../papers/frontier/SO4_SPIN4_FUTURE_COMPONENT.md` (§5 promoted),
`../exact_dim4_generator_2026-06/exact_dim4.py` (the D=4 rung + D=8 SO(4) twin this builds on),
`../../papers/WHERE_HS_BELONGS.md`, `../../papers/HONEST_COMPETITIVE_SCOPING.md` §2,
`../../HCI-CNQ/engine/geometry.py` (shared quaternion conventions). Peter is the sole gate; nothing pushed.*

*Proof & Honesty Standard — numbers cited-or-fenced · math proven + receipted · value shown · experts decide.*
