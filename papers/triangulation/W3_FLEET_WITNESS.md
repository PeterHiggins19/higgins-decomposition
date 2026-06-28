# Witness III — An engineered fleet: hard drives drift toward failure in the ratios, where threshold alarms are blind

### (Triangulation series, Witness III of three; self-contained — assumes no prior reading)

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-22. The third
of three independent witnesses to one compositional law. **Self-contained**: it restates the whole
construction from the ground up. The foundation courses (§2–§5) are cut to the **same dimensions** as the
other two witnesses. Honest-broker tiered; public data, read and never copied; deterministic and
hash-receipted. No relationship with or endorsement by Backblaze is implied — Backblaze is the open dataset
that makes the concept testable. Source: `experiments/Hs-17_Backblaze/`,
`collaborations/distributed-systems-backblaze/`. Nothing posted; Peter is the sole gate.*

---

## Abstract

We read a real engineered fleet — a public hard-drive fleet — as a **composition in motion**: a conserved
failure-mode budget `(Mechanical, Thermal, Age, Errors)` apportioned across units and tracked over 731 days.
The same compositional law a microbiome (Witness I) and a Cretaceous mudstone (Witness II) obey appears again:
the fleet's pre-fault message lives in the **relationships between failure modes**, not in any single-channel
level. The deterministic, hash-receipted read surfaces a measurable arrow of intent toward Mechanical/Age
failure and **159 silent-drift events** — the quiet concentration-toward-failure that single-channel threshold
monitoring is blind to — on a fleet whose risk moves on only ≈1.7 effective directions (so it is sortable).
This is the identical seam the other two witnesses measured: *the aggregate/threshold view loses what the
relational view sees.* A living system, a deep-time system, and an engineered system — three that cannot have
agreed in advance — therefore **locate** the law. This engineered fleet is also the structural precedent for
a much larger one (a satellite constellation), but that extrapolation is the capstone's claim, not this
witness's.

## 1. The claim, in this domain (the apex)

> A drive fleet is a composition in motion: each unit apportions a conserved failure/health budget, and the
> fleet's state is that budget moving in time. If the pre-fault signal lives in the **relationships** among
> failure modes — concentration toward a failure mode while raw activity still looks calm — then a relational
> read will catch a degradation that threshold alarms miss. We test exactly this on real public telemetry.

## 2. The bedrock: what a composition is (matched course, restated)

A composition `x=(x₁,…,x_D)` carries only relative information; closed to a constant sum it lives on the
simplex with the Aitchison geometry \[Aitchison 1986; Egozcue et al. 2003\]. Coordinates are log-ratios:
`clr(x)=log x − mean(log x)`, `ilr(x)=clr(x)·Hᵀ` (`H` Helmert orthonormal) — an **exact bijection** that
loses nothing. (Canonical: `HCI-CNTT/engine/geometry.py`.)

## 3. The exact rung and tiling (matched course, restated)

Four parts are exact: ILR coordinates are an imaginary quaternion rotated by `q v q*` to ≈1.1×10⁻¹⁶; higher
dimension is tiled through overlapping exact four-part charts with `O(log D)` conditioning, to `D=10⁶` at
≈4.1×10⁻¹² (numerical, not identity). The fleet's failure-mode budget is `D=4` — the **exact rung itself**,
read without any tiling approximation. (Full treatment: P1.)

## 4. Trust by construction (matched course, restated)

Every reading is a fixed-engine computation stamped with a SHA-256 content receipt; identical inputs give
identical outputs and a matching hash, and the read reproduces on rerun. In a fleet this is also the control
primitive: every node can verify every other node by hash, **non-contact** — no node has to be trusted, only
checked. This is what lets the agreement across the three witnesses count as evidence rather than echo.

## 5. The message is in the ratios (matched course, the theorem)

For a composition `x∈S^{D-1}` and a label `Y` (here: imminent failure), the ILR map `φ` is a bijection, hence
a **sufficient statistic**: `I(Y;X)=I(Y;φ(X))`. For any reduction `g` — a single-channel threshold, a scalar
health index — the **data-processing inequality** gives `I(Y;g(φ(X)))≤I(Y;φ(X))`: the threshold can only lose
what the relational read keeps, and can stay quiet while the relational signal moves. §6 measures exactly that
as silent drift.

## 6. The measured witness (Tier 1)

**Data.** Public Backblaze Drive Stats, 2024-07-27 (data hash `058fde30806a8e6b`); a four-part failure-mode
budget `(Mechanical, Thermal, Age, Errors)` over 731 days; engine = Hs-Kinematics. Deterministic and
hash-receipted (rerun gives an identical hash).

- **Arrow of intent → Mechanical, Age** (away from Errors, Thermal), coherence ≈0.22: the aging fleet's
  trouble is measurably migrating toward mechanical/age-related failure modes — a real, gradual trend, not
  noise.
- **159 silent-drift events** — the quiet *concentration-toward-failure while activity looks calm* signature
  that single-channel threshold monitoring misses. **This is the pre-fault tell**, and it is precisely what a
  scalar/threshold view cannot see.
- **Effective dimensionality ≈1.7** — fleet risk moves on ~2 axes; the fleet is low-dimensional and therefore
  **sortable** by measured behaviour.
- **Datable reorganisation events** (hold-lock structural changes), within-regime, full content hash.

**The matching seam (the joint that fits Witnesses I and II).** Single-channel threshold alarms stay green
through 159 events that the compositional read flags as drift toward failure. *The aggregate/threshold view
loses what the relational view sees* — the same seam measured in a microbiome (diversity null, ratios
informative) and a mudstone (coarse view at the EITT boundary, full view within structure). Three regimes,
one joint.

## 7. Back to the apex

An engineered fleet — built, instrumented, and failing on its own physics, with no possibility of being
arranged to agree — independently exhibits the law: the pre-fault message is in the compositional motion,
invisible to threshold alarms, read deterministically on the exact four-part rung. This is the **third located
coordinate**. With a living system and a deep-time system, the three **locate** the compositional law: not one
domain's coincidence, but a property that holds across the living, the geological, and the engineered.

## 8. Honest envelope

- **Tier 1 (measured/proven):** the deterministic, hash-receipted fleet read; the arrow of intent; the 159
  silent-drift events; effective dimensionality ≈1.7; datable reorganisations; the sufficiency/DPI theorem
  behind the threshold's blindness.
- **Tier 2 (design, from Tier-1 parts):** the migration/tiering/retirement policy and the distributed
  leader-election + all-watch-all orchestration — assembled from Tier-1 reads, **not deployed.**
- **Tier 3 / not claimed here:** the **decisive open test** is a per-drive backtest against Backblaze's
  labelled failures (lead-time distribution, false-positive rate) — buildable from the public dataset, **not
  yet run**; until then the pre-fault *tell* is measured but its operational lead-time is not certified. The
  extrapolation to a satellite constellation is the **capstone's** claim, supported by this witness, not made
  by it.
- **Kills.** The claim dies if a single-channel threshold caught the same degradations the compositional read
  flags (it did not — 159 silent events), or if the silent-drift signature fails to lead labelled failures in
  the backtest (the named open test).

## 9. Reproducibility

The fleet composition, the daily reads, and the navigation results ship at `experiments/Hs-17_Backblaze/`
(deterministic to the data hash `058fde30806a8e6b`); the preprocessor streams any public fleet/telemetry
export into engine-ready compositions. Public data read, never copied into claims (instrument-not-data).

## Acknowledgments

Developed from a body of acoustic-engineering practice; AI-assisted per HUF-STD-001. The AI collective
contributed independent cross-checks; all claims are the author's. Backblaze publishes the Drive Stats data
openly; no affiliation is implied.

## 10. Supporting studies — the three-study trust (HUF support standard)

Two supporting studies reinforce this witness into a three-study trust:

- **Support A — rotation-blind orthogonal class.** The dual-quaternion 6-DOF read surfaces **30 rotation-blind
  size events** on the same fleet — a second, orthogonal event class beyond the 159 silent-drift events
  (`d531e545…`, `../../experiments/so4_dualquaternion_2026-06/`).
- **Support B — deceptive-drift null.** The silent-drift detector is validated with an honest
  label/time-permutation **null** on independent EMBER energy data
  (`../../experiments/deceptive_drift_null_2026-06/`).

Main + A + B = a three-study trust. Full chain: `../NINE_STUDY_TRUST_LEDGER.md`.

*Witness III of three. The aggregate loses what the relational keeps — measured on a real engineered fleet,
matched to the seams of Witnesses I and II, completing the three that locate the law. The fleet is also the
ground-based precedent the constellation capstone leans on — earned there, not borrowed here. Cross-refs:
`W1_MICROBIOME_WITNESS.md`, `W2_MUDSTONE_WITNESS.md`, `../THE_HUF_CONSTELLATION_SYSTEM_PROPOSAL.md`,
`../TRIANGULATION_TRILOGY_PLAN.md`. Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — numbers cited-or-fenced · math proven + receipted · value shown · experts decide. See [`../PROOF_AND_HONESTY_STANDARD.md`](../PROOF_AND_HONESTY_STANDARD.md).*
