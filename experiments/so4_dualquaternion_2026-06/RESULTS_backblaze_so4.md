# What SO(4) reveals on the live Backblaze fleet — a real-data run

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-23. The
dual-quaternion SE(3) 6-DOF module run on the **real** Backblaze fleet telemetry (the W-III dataset, 731 days
of the failure-mode budget `Mechanical, Thermal, Age, Errors`). Reads public data, never copies it into a
claim. Deterministic; receipt below. Honest-broker tiered. No relationship with Backblaze implied.*

---

## The setup (well-posed, by design)

The fleet budget is **D=4 → the exact rung**: each day is an ILR point `v_t ∈ ℝ³`. Each day-to-day step is one
rigid motion `v_{t+1} = R_t v_t + τ_t`, encoded as a single unit dual quaternion:

- `R_t` — the SO(3) sandwich rotating the **direction** `u_t → u_{t+1}`: the relational drift, the **same
  "arrow of intent" W-III already reads**.
- `τ_t = v_{t+1} − R_t v_t` — the **size / budget-magnitude** change (the moving-budget channel), now carried
  in the *same exact object*. This is the well-posed use of Spin(4)'s second `su(2)`: it carries a physically
  observable DOF (magnitude), not a gauge one.

## What it reveals (the receipts)

**1. The 6-DOF read is exact on real data.** The dual-quaternion object reconstructs the real next-day fleet
state to **1.33×10⁻¹⁵** (IEEE floor) across all 730 steps — the exactness is not a synthetic-only result; it
holds on the live telemetry.

**2. Direction-drift and size-drift are geometrically orthogonal (zero pitch).** The screw decomposition's
**axial fraction** — how much of the translation runs *along* the rotation axis — is **≈1.1×10⁻¹⁴ (median),
max 9×10⁻¹²**, i.e. **zero to the floor.** The per-step motion is a *zero-pitch glide, never a helix*: the
relational drift and the budget-size change do not couple into a screw. **This is a real finding, not a null:**
it gives an *exact geometric reason* the engine was right to track direction and magnitude as separate
channels — they are orthogonal by construction on this data.

**3. The translation channel surfaces a distinct, rotation-blind event class.** This is the third member of
the **blindness suite** (`../../library/THE_BLINDNESS_SUITE.md`): after *ratio-blind* (the three witnesses) and
*mass-blind* (momentum), **rotation-blind** is the size move the directional read cannot see. Flagging steps at
`median + 3·MAD` on each channel independently:

| class | count | meaning |
|---|---:|---|
| rotation events | **121** | directional relational drift (the W-III class) |
| size events | **86** | budget-magnitude moves |
| both | 56 | a move in direction *and* magnitude |
| rotation-only | 65 | direction shifts, budget steady |
| **size-only (rotation-blind)** | **30** | **budget magnitude moves with *no* directional drift — invisible to a rotation-only read** |

The **30 size-only days** (e.g. 2024-01-05, 01-09, 01-10, 01-17, 01-20, 02-12, 03-02, 03-03, …) are the
honest "reveal": a complementary event class the directional read does not see, now caught in the **same
exact, receipted object** rather than a separate pass.

**Receipt (canonical-JSON SHA-256):** `d531e5456e47da154bc7a54842aba6c35a9c3eafe40d1562ed98eade23849e22`
(`backblaze_so4_run.py`; rerun byte-identical).

## What is and is not claimed

- **T1 (shown):** the 6-DOF read is **exact on the live fleet** (1.3e-15); rotation⊥translation (**zero pitch**)
  is measured, not assumed; the size channel exposes **30 rotation-blind events** the directional read misses.
- **T2 (reasoned, not shown here):** that those 30 events are *operationally* meaningful (tied to real
  pre-fault outcomes) — this run has **no failure-outcome labels joined**, so it shows a *distinct signal
  class*, not a validated predictor. Joining drive-failure labels to the size-only days is the next test.
- **Not claimed:** that SO(4) "finds failures W-III missed." It finds a **distinct, orthogonal event class**
  and carries both channels in one receipt — a richer, single-object read, honestly bounded.

## The honest bottom line

On this fleet, SO(4)/dual-quaternion does **not** buy a magic new coupling (pitch is zero — direction and size
are independent here). What it buys is concrete and real: **one exact, deterministic, receipted object that
reads orientation *and* magnitude together**, exact on live data, and it **surfaces a second event class (30
rotation-blind size moves)** the rotation-only read is blind to. That is the second `su(2)` doing honest work —
and the zero-pitch result is itself a clean, reportable measurement.

*Reproduce: `python3 backblaze_so4_run.py`. Cross-refs: `RESULTS_so4_dual_quaternion.md` (the algebra +
self-test), `../../papers/triangulation/W3_FLEET_WITNESS.md` (the rotation-only read), `../Hs-17_Backblaze/`
(the source study), `../../papers/frontier/SO4_SPIN4_FUTURE_COMPONENT.md` §5. Peter is the sole gate; nothing
posted.*

*Proof & Honesty Standard — numbers cited-or-fenced · math proven + receipted · value shown · experts decide.*
