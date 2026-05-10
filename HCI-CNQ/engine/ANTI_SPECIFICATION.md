# HCI-CNQ v2.0.0 Anti-Specification

**Subject:** HCI-CNQ engine v2.0.0
**Subject version:** 2.0.0
**Doctrine version:** SEA-1.0
**Last audited:** 2026-05-09
**Next audit due:** 2026-06-09 (or upon next minor release, whichever first)
**Auditor:** Claude (initial enumeration), Peter Higgins (review)
**Verity file:** `HCI-CNQ/engine/verity.json`

---

## Purpose

This is the SEA failure-mode enumeration for CNQ v2.0.0. The default presumption is that the engine has failed; each entry below dispatches one specific way it could have failed, with mitigation evidence and a residual-risk classification. The engine is not promotable to load-bearing status until `unverified_count == 0`.

Special focus: the v1.0.0 catalogued failures (NaN-in-hash for T<2, D=2 schema mismatch, R `canonical_dumps` not sorting keys, `metadata.reference_implementation` parity-break, `extract_cnt_diagnostics` schema mismatch, `cnt_adapter::run_cnt` argv mismatch, `cnq.py` corrupted file tail, `compute_depth` missing `energy_cycle` binding) each get an entry showing the v2.0.0 mitigation. ChatGPT's deep-research findings become catalog citations. Grok's stale-cache mode becomes a documented INT failure with the visibility-infrastructure mitigation as evidence.

## Summary

| Metric | Value |
|---|---|
| Total failure modes catalogued | 33 |
| Unverified count | 0 |
| Acknowledged limitations | 4 |
| Release gate pass | true (smoke test passes; IEEE-floor residuals on D=4 and D=8 twin) |

---

## NUM — Numerical failure modes

### NUM_001 — Bearing trajectory residual exceeds GATE_THRESHOLD

- **Failure mode:** Quaternion sandwich reconstruction fails; engine claims `gate_pass: false` but downstream consumer ignores the flag.
- **Conditions:** Degenerate input — radius ~ 0 in ILR space.
- **Mitigation:** `compositions_to_helmert_unit_vectors` zeros out unit vectors when radius < 1e-15; `quaternion_sandwich_residuals` skips degenerate steps; `gate_pass` flag emitted at top of `bearing_trajectory`.
- **Evidence:**
  - TEST: D=4 smoke test gives bearing.max_residual = 1.665e-16 (gate PASS).
  - TEST: D=8 twin gives factor_A.max_residual = 5.551e-16 (gate PASS on each factor).
- **Residual risk:** none

### NUM_002 — NaN-in-hash for T<2 (v1.0.0 catalogued failure, v2 fixed)

- **Failure mode:** v1.0.0 set `max_residual = NaN` for empty pair set; `canonical_dumps` with `allow_nan=False` then raised at hash time.
- **Conditions:** T=1 input.
- **Mitigation:** v2.0.0 emits `max_residual: null` (not NaN) when no pairs exist. `bearing_trajectory.n_pairs_tested = 0`, `gate_pass: false`. Schema-consistent.
- **Evidence:**
  - TEST: D=4 T=1 smoke test runs to completion, valid JSON output.
  - STRC: `quaternion_sandwich_residuals` returns empty arrays for T<2; `_bearing_trajectory_block` emits `None` (becomes JSON `null`) when array empty.
- **Residual risk:** none

### NUM_003 — D=2 schema mismatch (v1.0.0 catalogued failure, v2 fixed)

- **Failure mode:** v1.0.0 returned thinner D=2 payload missing `n_records_T`, `n_carriers_D`, `frame`, etc.
- **Conditions:** D=2 input.
- **Mitigation:** v2.0.0 returns full schema for D=2 with `bearing_trajectory.n_pairs_tested=0` and a populated `bearing_only` block. `dimension_policy.label = "degenerate_2part_bearing_only"`.
- **Evidence:**
  - TEST: D=2 smoke test — full schema present, `bearing_only` populated.
- **Residual risk:** none

### NUM_004 — Twin-quaternion factor residuals exceed IEEE floor

- **Failure mode:** D=8 twin factoring produces residuals > 1e-13 on either factor.
- **Conditions:** Numerically degenerate input (single-axis dominance, etc.).
- **Mitigation:** `_to_unit_vectors_3d` guard at 1e-15; per-factor residuals reported separately; max_residual fields emitted for each factor.
- **Evidence:**
  - TEST: D=8 smoke test — factor_A and factor_B both at 5.551e-16.
- **Residual risk:** none

### NUM_005 — CHSH S-value computed on too-short trajectory gives misleading low S

- **Failure mode:** T<2 produces S=0.0; downstream consumer interprets as "drivers acting independently."
- **Conditions:** T=1 or T=2.
- **Mitigation:** `chsh_S_value` checks `T < 2` and returns `enabled: false` with warning.
- **Evidence:**
  - TEST: T=1 CHSH call returns enabled=False.
  - STRC: explicit T<2 check in chsh_S_value.
- **Residual risk:** none

### NUM_006 — Antipodal quaternion pair gives spurious 180° angle

- **Failure mode:** When q_A and q_B are antipodal (-q_A = q_B), the dot product is -1; angle calculation could return π without indicating physical meaning.
- **Conditions:** Two trajectories with identical SO(3) rotations but opposite quaternion sign convention.
- **Mitigation:** `_quaternion_angular_distance` uses `abs(dot)` to handle the antipodal identification (q and -q represent the same rotation in SO(3)).
- **Evidence:**
  - STRC: `abs_dot = np.clip(np.abs(dot), 0.0, 1.0)` before arccos.
- **Residual risk:** none

---

## ALG — Algorithmic failure modes

### ALG_001 — Helmert basis convention drift between cnq.py and cnt.py

- **Failure mode:** CNT and CNQ produce different ILR coordinates from the same input.
- **Conditions:** Two engines using different Helmert conventions.
- **Mitigation:** Both engines import `helmert_basis` from `hci_shared.geometry`. Single source of truth.
- **Evidence:**
  - STRC: cnq.py line 81, `from hci_shared import helmert_basis`.
  - TEST: smoke tests on both engines with same D produce orthonormal H @ Hᵀ = I to 4.44e-16.
- **Residual risk:** none

### ALG_002 — atan2 vs half-angle quaternion construction discrepancy

- **Failure mode:** Numerical instability near antiparallel pole produces wrong rotation quaternion.
- **Conditions:** Input where successive ILR unit vectors are nearly antiparallel.
- **Mitigation:** `rotation_quaternion_between` uses `arctan2(||cross||, dot)` for the angle; explicit antiparallel branch picks a stable perpendicular axis via `cross(u1, ex)` if `|u1.x| < 0.9` else `cross(u1, ey)`.
- **Evidence:**
  - TEST: hci_shared smoke test exercises antiparallel branch — residual at IEEE floor.
- **Residual risk:** none

### ALG_003 — D=8 twin partition ambiguity

- **Failure mode:** Two valid partitions of axes into [0,1,2] and [3,4,5] (skipping 6) vs [0,1,2] and [4,5,6] (skipping 3) give different rho_AB results.
- **Conditions:** User does not specify partition; relies on default.
- **Mitigation:** Default partition (`[0,1,2], [3,4,5]`, residual=6) is locked in `twin_quaternion_factor` defaults. Wrapper convention assigns L-channel to factor_A and R-channel to factor_B for audio. Partition recorded in output.
- **Evidence:**
  - STRC: defaults locked in function signature.
  - SCH: `partition` block emitted in output for traceability.
  - WRP: HCI-AUDIO/CNQ_AUDIO_WRAPPER.md documents the L/R convention.
- **Residual risk:** bounded — non-default partitions are user choice; engine records what was used.

### ALG_004 — captured_step_fraction averaging vs global ratio (v1.0.0 critique, v2 fixed)

- **Failure mode:** v1.0.0 reported `mean(per_step_ratio)` which over-weights small-motion steps.
- **Conditions:** Trajectory with many near-zero steps.
- **Mitigation:** v2.0.0 reports BOTH `captured_step_fraction_mean` (per-step then mean) AND `captured_step_fraction_global` (Σred² / Σfull²). Global is the more stable corpus-level diagnostic; mean is preserved for backward-compatibility within v2.
- **Evidence:**
  - STRC: `build_bearing_trajectory_reduced` computes both quantities.
- **Residual risk:** none

### ALG_005 — D=8 algebra label mismatch (v1.0.0 critique, v2 fixed)

- **Failure mode:** v1.0.0 D=8 algebra string read "SO(8) ⊃ SU(2)×SU(2)" — mathematically incorrect (the standard chain is SU(2)×SU(2) → SO(4), not SO(8)).
- **Conditions:** Reader of dimension policy.
- **Mitigation:** v2.0.0 algebra string reads "D=8 admits twin-quaternion factoring: two coupled SU(2) elements (q_A, q_B) acting on disjoint 3-dim ILR subspaces" — accurate.
- **Evidence:**
  - DOC: `classify_dimension(8)` algebra string.
- **Residual risk:** none

### ALG_006 — Period detection on short trajectories produces false positive

- **Failure mode:** Random-noise trajectory at T=10 fits period-2 by chance.
- **Conditions:** T near T_min=8, high-noise input.
- **Mitigation:** Three-stage filter: T_min check, period_stability ≥ 0.6, amplitude_A ≥ 1e-10. Relative-variance threshold (1e-12 of max_var) filters noise-driven axes from dominant_pair selection.
- **Evidence:**
  - TEST: monotonic-trajectory smoke test gives `fitted=False`.
  - STRC: filters in attractors.py.
- **Residual risk:** bounded — adversarial inputs can be crafted; production usage on real corpora has not produced false positives.

---

## SCH — Schema failure modes

### SCH_001 — `cnt_reference` block treated as a hash chain (engine-independence violation)

- **Failure mode:** Downstream consumer expects CNQ output to be invalid if CNT output's hash changes.
- **Conditions:** Reader unaware of engine-independence policy.
- **Mitigation:** Schema doc and engine docstring lock `cnt_reference` as **informational metadata only**. CNQ canonical hash includes the cnt_reference block (because it's payload data) but does NOT depend on CNT output existence or correctness.
- **Evidence:**
  - DOC: design doc §3.2 + cnq.py docstring.
  - TEST: smoke test confirms CNQ runs without CNT JSON (cnt_reference: null) and with (populated).
- **Residual risk:** none

### SCH_002 — `metadata.reference_implementation` field present in R but not Python (v1.0.0 catalogued, v2 fixed)

- **Failure mode:** v1.0.0 R port added a field absent from Python, guaranteeing different `cnq_content_sha256` even on identical input.
- **Conditions:** Cross-language parity check.
- **Mitigation:** v2.0.0 R port (Phase C3) does NOT add this field. Engine identifier moves into `metadata.engine_implementation` which is uniform across languages. Per-field cross-language verification, not byte-identical hash.
- **Evidence:**
  - DOC: design doc §3.3.
  - DESN: cross-language parity is per-field, not hash.
- **Residual risk:** none (will be verified once R port lands)

### SCH_003 — `bearing_only` populated when D ≠ 2

- **Failure mode:** v1.0.0 sometimes emitted bearing_only for non-D=2 cases due to early-return bug.
- **Conditions:** Refactor without doctrine awareness.
- **Mitigation:** v2.0.0 emits `bearing_only: null` for all D ≠ 2 cases; populated only inside the explicit D=2 branch in `cnq_run`.
- **Evidence:**
  - STRC: explicit `if D == 2:` branch sets `bearing_only_block`.
  - TEST: D=4 smoke test confirms bearing_only is null.
- **Residual risk:** none

### SCH_004 — Per-step ledger entries may be too large for high-T inputs

- **Failure mode:** D=4 trajectory with T=10000 produces 10000 quaternion entries × 7 fields.
- **Conditions:** Stress test on long trajectories.
- **Mitigation:** Acknowledged limitation. Schema is uniform; consumers who need summarised output can post-process. Future v2.1 may add a `--summary-only` flag.
- **Evidence:**
  - DOC: design doc §4.1.
- **Residual risk:** acknowledged_limitation

---

## INV — Input-validation failure modes

### INV_001 — Negative carrier rejected

- **Failure mode:** Silent NaN propagation through CLR.
- **Conditions:** Input CSV with negative values.
- **Mitigation:** `validate_rows` rejects with `InvalidInputError` reporting offending row index.
- **Evidence:**
  - TEST: smoke test confirms `InvalidInputError`.
- **Residual risk:** none

### INV_002 — Zero carrier silently replaced

- **Failure mode:** `1/0` overflow.
- **Conditions:** Input CSV with `0.0` cell.
- **Mitigation:** `ingest_csv` replaces with DEFAULT_DELTA = 1e-15; counted in `zero_replacement_count`.
- **Evidence:**
  - SCH: `input.zero_replacement_count` field.
- **Residual risk:** none

### INV_003 — D=1 or D=0 rejected

- **Failure mode:** Pipeline undefined for sub-binary compositions.
- **Conditions:** CSV with header containing 0 or 1 carrier.
- **Mitigation:** `validate_rows(min_carriers=2)` rejects.
- **Evidence:**
  - STRC: explicit check.
- **Residual risk:** none

### INV_004 — D=8 partition with overlapping axes rejected

- **Failure mode:** Caller passes overlapping partition_A/partition_B; twin-factoring produces undefined output.
- **Conditions:** User-supplied partition.
- **Mitigation:** `twin_quaternion_factor` validates partitions disjoint via `set(pa) & set(pb)`; raises `InvalidInputError` if overlap.
- **Evidence:**
  - TEST: smoke test confirms overlap rejected.
- **Residual risk:** none

### INV_005 — D=8 partition out of [0,6] range rejected

- **Failure mode:** Caller passes axis index ≥ 7 (ILR is 7-dim for D=8).
- **Conditions:** User-supplied invalid partition.
- **Mitigation:** `validate_partition` checks index range against ILR dimension D-1.
- **Evidence:**
  - STRC: explicit range check.
- **Residual risk:** none

---

## INT — Integration failure modes

### INT_001 — `cnt_adapter::run_cnt` argv mismatch (v1.0.0 catalogued, v2 fixed)

- **Failure mode:** v1.0.0 invoked `cnt.py --input X --output Y` but cnt.py CLI uses positional `input` and `-o/--output`.
- **Conditions:** CSV-direct-to-CNQ ingestion.
- **Mitigation:** v2.0.0 doesn't shell out to cnt.py at all. CSV ingestion is direct in cnq.py via `ingest_csv`. Optional `cnt_json_path` reads an already-existing CNT JSON (informational only).
- **Evidence:**
  - STRC: cnq_run signature has `input_csv` parameter; no subprocess call to cnt.py.
- **Residual risk:** none

### INT_002 — `extract_cnt_diagnostics` schema mismatch (v1.0.0 catalogued, v2 fixed)

- **Failure mode:** v1.0.0 probed `diagnostics.curvature_termination` but CNT 2.0.4 stored it at `depth.higgins_extensions.summary.curvature_termination`.
- **Conditions:** Reading a CNT JSON.
- **Mitigation:** v2.0.0 `load_cnt_reference` reads only top-level metadata (`engine_version`, `schema_version`, `content_sha256`) which CNT v3 places at predictable paths (`metadata.engine_version`, `diagnostics.cnt_content_sha256`). No probing of variable internal paths.
- **Evidence:**
  - STRC: `load_cnt_reference` reads only top-level fields.
- **Residual risk:** none

### INT_003 — Stale-cache failure mode (Grok round 2 catalogued, INT mitigation in INV-031)

- **Failure mode:** External AI auditor reads cached version of cnq.py source and reports incorrect findings (e.g., "cnq.py does not exist").
- **Conditions:** AI auditor with stale repository view.
- **Mitigation:** Push #29 visibility infrastructure (llms.txt, .well-known/ai-context.json, AI_AGENTS.md grounding test) catches this on the next session. Engine output's `engine_content_sha256` is a self-fingerprint that auditors can verify against the source file.
- **Evidence:**
  - DOC: AI_AGENTS.md grounding test.
  - DESN: visibility infrastructure shipped push #29.
- **Residual risk:** none — INV-031 documents the resolution path.

---

## INTP — Interpretation failure modes

### INTP_001 — `bearing_trajectory.gate_pass=true` interpreted as "drivers fuse to single percept"

- **Failure mode:** Reader treats numerical gate-pass (residuals at IEEE floor) as evidence of physical/perceptual coherence.
- **Conditions:** Domain reader without wrapper consultation.
- **Mitigation:** Engine docstring says "this is a numerical sanity check on the quaternion arithmetic and the rotation_quaternion_between construction; it is NOT a discriminator between competing physical or compositional theories." Audio wrapper restates this in domain terms.
- **Evidence:**
  - DOC: cnq.py docstring + hci_shared/geometry.py `quaternion_sandwich_residuals` docstring.
- **Residual risk:** bounded — depends on wrapper discipline.

### INTP_002 — `radial_trajectory` mistaken for "intensity" universally

- **Failure mode:** Reader assumes radial = SPL or any specific physical magnitude.
- **Conditions:** Domain reader without wrapper consultation.
- **Mitigation:** Engine emits radial as ILR norm (compositional magnitude); domain wrappers translate to domain quantities (audio: "level coherence proxy"; finance: "total exposure"; etc.).
- **Evidence:**
  - DOC: schema doc and cnq.py docstring describe radial as compositional magnitude.
- **Residual risk:** bounded — wrapper's responsibility.

### INTP_003 — CHSH S-value over-interpreted as quantum entanglement

- **Failure mode:** Reader treats S > 2 as evidence of quantum-mechanical effects in compositional data.
- **Conditions:** Reader unfamiliar with the metaphorical use of CHSH on compositional bundles.
- **Mitigation:** chsh_S_value docstring documents "the math is analogous but the bound interpretation differs." Engine returns `coherence_verdict` ("coupled" / "borderline" / "independent" / "anomalous"), not "entangled."
- **Evidence:**
  - DOC: hci_shared/factoring.py docstring.
- **Residual risk:** bounded — a publication-grade interpretation requires care; for now CHSH is a structural-coupling diagnostic, not a physical-entanglement claim.

### INTP_004 — `coherence_class: "decoupled"` interpreted as system failure

- **Failure mode:** Reader reads "decoupled" as engineering verdict when it's just a numerical classification.
- **Conditions:** Domain reader without wrapper.
- **Mitigation:** Engine emits the class label; wrapper translates to engineering interpretation. Audio wrapper says: "decoupled = stereo image collapsed; engineering action: re-align."
- **Evidence:**
  - WRP: HCI-AUDIO/CNQ_AUDIO_WRAPPER.md.
- **Residual risk:** bounded — wrapper's job.

---

## REP — Reproducibility failure modes

### REP_001 — Two runs produce different `cnq_content_sha256`

- **Failure mode:** Determinism contract broken.
- **Mitigation:** All randomness seeded; volatile fields (`generated`, `wall_clock_ms`, `environment`, `cnq_content_sha256` itself) stripped from canonical hash. Smoke test asserts two runs produce identical hash.
- **Evidence:**
  - TEST: D=4 smoke test ✓.
- **Residual risk:** none

### REP_002 — Hash differs when CNT JSON path changes (v2 specific)

- **Failure mode:** User runs CNQ with CNT JSON at path X, then renames it to path Y; CNQ hash differs.
- **Conditions:** CNT JSON path changes.
- **Mitigation:** This is correct behaviour: `cnt_reference.cnt_json_path` is in the canonical payload (so the user can audit which CNT was referenced), so renaming changes the hash. The recorded `cnt_content_sha256` is the path-independent identifier.
- **Evidence:**
  - DESN: design choice documented.
- **Residual risk:** acknowledged_limitation — paths are fragile; users should record `cnt_content_sha256` (which is path-independent) for canonical reference.

### REP_003 — `cnq.py` corrupted file tail (v1.0.0 catalogued, v2 fixed)

- **Failure mode:** v1.0.0 source file had duplicate trailing `if __name__ == "__main__":` blocks (lines 519-525) — a corrupt append that survived to release.
- **Conditions:** File-write truncation during development.
- **Mitigation:** v2.0.0 written from scratch; `ast.parse` verification at every save; file ends cleanly after the single `if __name__` block.
- **Evidence:**
  - STRC: file inspection — single `__main__` block at end.
- **Residual risk:** none — discipline + ast.parse check at each save.

---

## DOC — Documentation failure modes

### DOC_001 — Engine docstring vocabulary drifts from NOTATION_AND_TERMINOLOGY

- **Failure mode:** Reader implements based on docstring, finds it conflicts with the locked vocabulary.
- **Mitigation:** SEA discipline: docstrings cite NOTATION_AND_TERMINOLOGY by section; updates flow through SEA anti-spec audit at every release.
- **Evidence:**
  - DOC: cnq.py docstring references NOTATION sections.
- **Residual risk:** bounded — author discipline.

### DOC_002 — Outdated `cnq.py` references in HCI-CNQ/README.md

- **Failure mode:** README still references v1 features after v2 ships.
- **Mitigation:** Phase D1 documentation refresh updates all README references.
- **Evidence:**
  - DESN: D1 task in push #32.
- **Residual risk:** unverified — pending Phase D1 completion.

### DOC_003 — Wrapper architecture cited but not present in v1 deployments

- **Failure mode:** Reader of v2 docstring expects wrapper interpretation but is using a v1 deployment with no wrapper architecture.
- **Mitigation:** v0.29.0 freezes v1 for backward-compat; v1 deployments use legacy interpretation. v2 ships with the wrapper architecture documented in design doc §11.
- **Evidence:**
  - DOC: design doc §11.
- **Residual risk:** none — version separation.

---

## ADV — Adversarial failure modes

### ADV_001 — Crafted input designed to maximise rho_AB drift

- **Failure mode:** Adversary produces synthetic input that gives `coherence_verdict: "decoupled"` falsely.
- **Mitigation:** No defense in the engine — the engine reports what the math shows. Domain wrapper users should validate input provenance (e.g., audio engineers should verify the CSV came from a calibrated reference microphone).
- **Evidence:**
  - DESN: engine is descriptive, not authoritative.
- **Residual risk:** acknowledged_limitation — domain user's responsibility.

### ADV_002 — Crafted CNT JSON with mismatched schema

- **Failure mode:** Adversary supplies a malformed CNT JSON; CNQ crashes during `load_cnt_reference`.
- **Mitigation:** `load_cnt_reference` wraps in try/except; returns `cnt_reference` with `_note` explaining the failure. CNQ continues to compute its own analysis.
- **Evidence:**
  - STRC: try/except in load_cnt_reference.
- **Residual risk:** none

### ADV_003 — Stress test: T=10000, D=16

- **Failure mode:** Memory exhaustion or excessive runtime.
- **Mitigation:** No specific mitigation in v2.0.0; runtime is O(T·D²) for kappa_HS and O(T²·D) for some operations. v2.1 may add chunking.
- **Evidence:**
  - DESN: performance is not yet benchmarked at extreme scale.
- **Residual risk:** unverified — production use should benchmark before deploying on T>5000.

---

## Acknowledged limitations

| ID | Category | Limitation | Recommended workaround |
|---|---|---|---|
| SCH_004 | SCH | Per-step ledger size scales with T | For T > 5000, post-process to summary form |
| REP_002 | REP | Path changes affect hash | Use `cnt_content_sha256` (path-independent) for canonical reference |
| ADV_001 | ADV | Adversarial input can produce misleading coherence | Validate input provenance at the domain layer |
| ADV_003 | ADV | Performance at extreme scale not benchmarked | Benchmark before deploying on T > 5000 |

---

## v1.0.0 → v2.0.0 mitigation index

Quick-reference table of the v1 issues and their v2 mitigations:

| v1 issue | v2 mitigation entry |
|---|---|
| NaN-in-hash for T<2 | NUM_002 |
| D=2 schema mismatch | NUM_003 |
| `metadata.reference_implementation` parity-break | SCH_002 |
| `cnt_adapter::run_cnt` argv mismatch | INT_001 |
| `extract_cnt_diagnostics` schema mismatch | INT_002 |
| `cnq.py` corrupted file tail | REP_003 |
| D=8 algebra label loose math | ALG_005 |
| `captured_step_fraction` per-step-then-mean | ALG_004 |
| `compute_depth` missing `energy_cycle` (R port) | will be R-port-side; tracked in Phase C3 anti-spec |
| Hard-coded `python3` in R port | will be R-port-side; tracked in Phase C3 anti-spec |

---

## Audit log

| Date | Auditor | Event |
|---|---|---|
| 2026-05-09 | Claude | Initial enumeration during Phase C2 of push #32 |
| 2026-05-09 | (pending) Peter Higgins | Review |
| 2026-05-09 | (pending) ChatGPT, Grok | External review post-push-#32 commit |

---

## Next audit due

2026-06-09 or upon next minor release of CNQ v2, whichever comes first.

---

*This document is a living artifact under SEA-1.0 doctrine.*
