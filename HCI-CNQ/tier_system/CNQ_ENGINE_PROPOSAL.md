# CNQ Engine Proposal — `cnq.py` Specification

**Status:** experimental / candidate. See [`README.md`](README.md).
**Foundation:** Round 2 validated at IEEE floor. See [`../experiments/backblaze_fleet_quaternion/QD_ROUND_2_REPORT.md`](../experiments/backblaze_fleet_quaternion/QD_ROUND_2_REPORT.md).
**Scope:** specification for the CNQ engine sibling to `cnt.py` / `cnt.R`. Engineering cost ~14 days of focused work per [`../doctrine/BENEFITS_POST_CODA.md`](../doctrine/BENEFITS_POST_CODA.md). Not implemented yet; this document is the blueprint.

---

## Design principles

1. **Inherit, don't replace.** CNQ reads CNT JSON output as input. It does not re-implement CoDa or CNT operations; it composes on top of them.
2. **Hash-chained provenance throughout.** Every CNQ output carries `cnq_content_sha256`, parallel to CNT's `content_sha256`. A reviewer can verify both independently.
3. **Bit-for-bit reproducibility.** Same engine version + same engine_config + same input → byte-identical CNQ output. No randomness; no dependence on system clock or PID; the same deterministic discipline as CNT.
4. **Dimension-aware.** D=4 uses native quaternion algebra. D=8 uses bi-quaternion factoring. D=2-3 falls back to U(1) bearing or 2D-rotation. D≥9 uses Clifford-algebra extensions or dominant-mode reduction.
5. **CCTT-and-OPERATIONS_PROTOCOL compatible.** CNQ inherits both access protocols; the user-facing experience extends, doesn't replace.
6. **R port at parity.** As with CNT, the Python canonical engine has an R sibling at numerical parity. Same input + same engine_config → same `cnq_content_sha256` from either implementation.

---

## CLI

```bash
python3 cnq.py <cnt_json> -o <cnq_json> [options]
```

Inputs:
- `<cnt_json>`: a canonical CNT JSON conforming to schema 2.1.0. CNQ does not re-run the engine; it lifts the existing CNT output.
- For multi-trajectory bundles: `python3 cnq.py --bundle <id1.json> <id2.json> ... -o <bundle_cnq.json>`.

Options:
- `--mode {single, bundle}`: single-trajectory or multi-trajectory bundle analysis. Default: auto-detect from input count.
- `--reduction {none, dominant, clifford}`: how to handle D > 4. Default: `dominant` (reduce to most-variable D=4 subspace).
- `--reduction-D {4, 8}`: target dimension for reduction. Default: 4.
- `--slerp-density N`: number of SLERP-interpolated points between adjacent timesteps for continuous-time output. Default: 0 (no interpolation; just per-timestep quaternions).
- `--config <json>`: equivalent of CNT's engine_config_overrides; per-experiment overrides.

---

## JSON schema

Top-level keys (parallel to CNT JSON, with extensions):

```json
{
  "metadata": {
    "engine_version": "cnq 1.0.0",
    "schema_version": "cnq 1.0.0",
    "generated": "2026-...",
    "wall_clock_ms": 0,
    "engine_config": {},
    "parent_cnt_content_sha256": "...",   // hash chain to upstream CNT
    "environment": {}
  },
  "input": {
    "cnt_json_path": "...",
    "cnt_content_sha256": "...",
    "n_records_T": 0,
    "n_carriers_D": 0,
    "reduction_method": "none|dominant|clifford",
    "reduction_target_D": 4,
    "reduction_residual_fraction": 0.0   // how much variance was projected away
  },
  "quaternion_path": {
    "_function": "trajectory representation",
    "helmert_basis_signature": "...",     // which Helmert convention was used
    "per_timestep_quaternions": [],       // list of (w, x, y, z) tuples, length T
    "radial_magnitudes": [],              // per-timestep radial scale, length T
    "axis_unit_vectors": [],              // (x, y, z) per timestep
    "rotation_angles_per_step": [],       // length T-1
    "cumulative_rotation_angle": 0.0      // total accumulated rotation (rad)
  },
  "spinor_diagnostic": {
    "_function": "spinor / vector branch classification",
    "cumulative_angle_in_pi_units": 0.0,
    "branch": "spinor|vector|undetermined",
    "branch_confidence": 0.0,             // 0-1; 1 = exact integer multiple of pi
    "matches_cnt_termination": true        // cross-check against curvature_termination
  },
  "bi_quaternion_factoring": {            // present only if D = 8
    "_function": "SO(8) ⊃ SU(2) × SU(2) decomposition",
    "factor_1_quaternions": [],           // first SU(2) component
    "factor_2_quaternions": [],           // second SU(2) component
    "factor_correlation": 0.0,            // Pearson correlation between factors
    "interpretation": "..."               // domain-specific (e.g., 'fossil vs renewables')
  },
  "slerp_interpolation": {                // present only if --slerp-density > 0
    "_function": "geodesic between-timestep interpolation",
    "interpolation_density": 0,
    "interpolated_quaternions": []        // length (T-1) * density + T
  },
  "bundle_analysis": {                    // present only in --bundle mode
    "_function": "cross-trajectory Hamilton products",
    "trajectory_ids": [],
    "pairwise_relative_quaternions": {    // per (i, j) pair, R(t) = Q_i(t) * Q_j(t)^-1
      "(0, 1)": {
        "per_timestep": [],
        "mean_relative_angle": 0.0,
        "axis_correlation": 0.0
      }
    },
    "spectrum_summary": {}                // bundle-level cross-dataset structure
  },
  "diagnostics": {
    "_function": "audit + provenance",
    "coda_compatibility_check": true,     // CoDa-level consistency
    "cnt_compatibility_check": true,      // CNT-level consistency
    "content_sha256": "..."               // the gate
  }
}
```

---

## Operation map: CNT → CNQ

For each significant CNT operation, the CNQ-native equivalent:

| CNT operation | CNQ-native equivalent | Equivalence proof |
|---|---|---|
| `bearing = atan2(y, x)` per timestep | `quaternion_log(q).angle` | Concept 2 (atan2 is the 1D / single-axis case of the quaternion log) |
| `rotation between two CLR vectors` | `quaternion_from_axis_angle(cross(u1, u2), atan2(\|cross\|, dot))` | Concept 1 (verified IEEE-floor on backblaze_fleet) |
| `Stage 4 cross-dataset comparison` | `R(t) = Q1(t) * conj(Q2(t))` (single Hamilton product) | Concept 7 (planned Round 3 verification) |
| `linear interpolation between timesteps in CLR space` | `slerp(Q_t, Q_{t+1}, alpha)` | SLERP is the geodesic; linear in CLR is the chord. SLERP is exact, linear is the approximation. |
| `M^2 = I metric tensor (Banach contraction)` | `q -> conj(q)` (quaternion conjugation involution) | Concept 3 (planned Round 3 verification) |
| `LIMIT_CYCLE_P2 termination code` | `cumulative_rotation_angle / pi is odd` (spinor branch) | Concept 4 (Concept 10 revised result already supports) |
| `helmsman channel sigma (signed cumulative omega)` | `cumulative_rotation_angle - parity correction` | Concept 8 (planned Round 3 verification) |
| `8-class IR taxonomy from amplitude + damping thresholds` | `sign-octant of time-averaged quaternion` | Concept 6 (planned Round 3 verification) |
| `depth tower depth (recursion until terminator)` | `recurrence time of quaternion walk on S^3` | Concept 9 (planned Round 3 verification) |
| `D = 8 channel-by-channel processing` | `bi-quaternion factor (SU(2) × SU(2))` | Natural for D=8; not present in CNT |

---

## What CNQ adds that CNT cannot express

Three CNQ-only diagnostics:

**1. Spinor parity per trajectory (top-level scalar per experiment).**

CNQ exposes `spinor_diagnostic.branch` as one of `spinor` / `vector` / `undetermined`. CNT's LIMIT_CYCLE_P1 vs LIMIT_CYCLE_P2 termination implicitly encodes this, but as a side-effect rather than a first-class diagnostic. Researchers can ask "is this trajectory in the spinor sector?" directly.

**2. Pairwise relative quaternion R(t) (per cross-dataset pair).**

For any pair of trajectories with shared carriers, CNQ produces R(t) = Q₁(t) · Q₂(t)⁻¹ as a single quaternion-valued time series encoding the full relative orientation. CNT's Stage 4 produces decomposed scalar comparisons; CNQ produces the unified geometric object that all those comparisons are projections of.

**3. Bi-quaternion factor structure for D=8 trajectories.**

EMBER country trajectories (D=8 or D=9) can be decomposed into two coupled quaternion paths under the natural SO(8) ⊃ SU(2) × SU(2) factoring. The first factor potentially captures fossil-fuel sub-mix dynamics; the second potentially captures renewables sub-mix dynamics; the correlation between the two factors is itself a domain-meaningful quantity. CNT has no analogue.

---

## Engineering plan (~14 days)

| Phase | Effort | Deliverables |
|---|---|---|
| Round 3: full corpus quaternion-view validation | 3 days | All 25 corpus experiments lifted to quaternion view; every CNT content_sha256 reproduced; `QD_ROUND_3_REPORT.md` |
| `cnq.py` core engine | 4 days | Single-trajectory mode, hash-chained output, schema-validated JSON, R port at parity |
| Bundle mode + Hamilton products | 2 days | Multi-trajectory analysis, EMBER 8-country test |
| SLERP interpolation | 1 day | Geodesic between-timestep, projector_html upgrade-ready |
| Bi-quaternion factoring (D=8) | 2 days | EMBER country bi-quaternion view, fossil/renewables interpretation |
| Spinor-parity diagnostic | 0.5 day | Top-level field; cross-check vs LIMIT_CYCLE_P2 termination |
| Documentation: Volume IV draft | 1 day | Math + worked examples + cross-references to Volumes I-III |
| README sweep + admin registration | 0.5 day | Update affected READMEs; add `cnq` block to HS_ADMIN.json (post-promotion) |

Total: 14 days. Distributed across one CNT release cycle.

---

## Compatibility matrix

| CNT version | CNQ version | Compatibility |
|---|---|---|
| 2.0.4 | 1.0.0 | Reads CNT 2.0.4 JSON; produces CNQ 1.0.0 JSON; full back-compatibility |
| 2.0.x (future minor) | 1.0.x (matching minor) | Lockstep minor versions; CNQ tracks CNT |
| 2.1.x (future schema bump) | 1.1.x | Schema bump in CNT triggers schema bump in CNQ; tested in lockstep |
| 3.x.x (hypothetical major) | 2.x.x | Major version bump on either side requires explicit compatibility audit |

---

## Determinism gate (CNQ-specific)

CNQ inherits CNT's 25-experiment determinism gate AND adds its own:

```
For each of the 25 corpus experiments:
  1. Read CNT JSON (already pinned by CNT determinism gate).
  2. Run cnq.py to produce CNQ JSON.
  3. cnq_content_sha256 must match cnq_INDEX.json[experiment_id].cnq_content_sha256.
  4. If experiment_id is registered for bundle membership, the bundle CNQ analysis
     must also match the bundle's pinned hash.
```

A CNQ-promoted release pushes both `experiments/INDEX.json` (CNT, unchanged) and `experiments/CNQ_INDEX.json` (CNQ, new). The two-gate audit means a reviewer can verify either tier independently or both together.

---

## What the user-facing experience looks like

A practitioner using CNQ via CCTT:

```
User: I have a 30-country, D=15 monthly economic-flow dataset, T=120 (10 years),
      and I want cross-country structural comparison.

CCTT (with CNQ extension): I see 30 trajectories at D=15. CNQ recommends:
      - Reduce D=15 to D=4 dominant subspace (variance retention check first).
      - Lift each reduced trajectory to a quaternion path.
      - Compute pairwise Hamilton products R_AB(t) for all 435 country pairs.
      - Output: bundle CNQ JSON, plus per-country CNT JSON for downward compatibility.
      Estimated wall-clock: ~30 seconds. Output size: ~50 MB.
      Confirm to proceed?

User: Yes.

CCTT: [runs CNQ in --bundle mode with --reduction dominant --reduction-D 4]
      Reduction retained 87.3% of variance.
      Bundle CNQ written to /tmp/economic_flow_30country_cnq.json
      Per-country CNT JSONs in /tmp/economic_flow_per_country/
      All hashes recorded.
      Spinor-parity diagnostic: 19 spinor / 11 vector trajectories
      (a non-trivial split; worth investigating).
      Top-3 most-anti-correlated country pairs:
        (Country_A, Country_B): mean R angle 1.82 rad (anti-correlated trajectory)
        (Country_C, Country_D): mean R angle 1.71 rad
        (Country_E, Country_F): mean R angle 1.65 rad

User: [investigates the spinor split and the anti-correlated pairs in their domain]
```

The same dataset would have taken several hours with CNT's per-channel arithmetic and Stage 4 pairwise routine. CNQ's Hamilton-product approach makes it a half-minute operation.

---

## What CNQ explicitly does NOT do

- CNQ does not modify CNT. CNT 2.0.4 / Schema 2.1.0 / Output Doctrine v1.0.1 are unchanged.
- CNQ does not modify CoDa. The Aitchison foundations are inherited, not replaced.
- CNQ does not replace the determinism gate. It adds a parallel gate; both must pass.
- CNQ does not bypass the user confirmation gate at CCTT phase 2. The user still confirms the carrier mapping before CNQ runs.
- CNQ does not push to the canonical repo while in experimental status. Same isolation rules apply.

---

*The instrument reads. The expert decides. The hashes carry the receipts. CNQ is the next engine, sized for the next problems, built on the algebra the existing engine has been computing in all along.*
