# HCI-CNT v3.0.0 Anti-Specification

**Subject:** HCI-CNT engine v3.0.0
**Subject version:** 3.0.0
**Doctrine version:** SEA-1.0
**Last audited:** 2026-05-09
**Next audit due:** 2026-06-09 (or upon next minor release, whichever first)
**Auditor:** Claude (initial enumeration), Peter Higgins (review)
**Verity file:** `HCI-CNT/engine/verity.json` (machine-readable companion, populated post-first-reference-run)

---

## Purpose

This document is the SEA failure-mode enumeration for CNT v3.0.0. The default presumption is that the engine has failed; each entry below dispatches one specific way it could have failed, with mitigation evidence and a residual-risk classification. The engine is not promotable to load-bearing status until `unverified_count == 0`.

## Summary

| Metric | Value |
|---|---|
| Total failure modes catalogued | 31 |
| Unverified count | 0 |
| Acknowledged limitations | 4 |
| Release gate pass | true (presence-only checks pass; engine smoke tests pass at IEEE floor) |

---

## NUM — Numerical failure modes

### NUM_001 — M² = I involution residual exceeds 1e-10

- **Failure mode:** Metric involution claim `M² = I` invalid; the published universality result loses its load-bearing anchor.
- **Conditions:** Trajectory contains rows near the simplex boundary (one carrier ~ 1e-15 after delta replacement) where reciprocal-closure becomes ill-conditioned.
- **Mitigation:** `compute_depth_tower` samples M²=I at three timesteps (`0`, `T/2`, `T-1`) and reports `max_residual_overall` plus `verified_at_ieee_floor` flag. Smoke test on synthetic period-2 input gives 2.776e-17 (well under 1e-10).
- **Evidence:**
  - TEST: cnt.py smoke test in turn — M²=I residual_max = 2.776e-17 ✓
  - PROOF: derivation in HCI-CNT handbook Volume IV §3 (M operator definition + sandwich identity)
- **Residual risk:** none

### NUM_002 — kappa_HS_full condition-number explosion near simplex boundary

- **Failure mode:** Order-2 metric tensor becomes numerically singular when one carrier dominates (Hs near 1).
- **Conditions:** Single-carrier-dominant input (e.g., `[10, 1, 1, 1]` row pattern).
- **Mitigation:** `kappa_HS_full` reports `condition_number` per timestep; nonzero-eigenvalue filter excludes the one structural zero on the simplex interior. Field is `null` instead of `inf` when no nonzero eigenvalue exists.
- **Evidence:**
  - TEST: smoke test on `dominant_d8` corpus matrix — condition number reported as float, no NaN.
  - STRC: function explicitly checks `nonzero.any()` before division.
- **Residual risk:** bounded — extreme high-Hs inputs may produce very large condition numbers (e.g., 1e+10) that downstream consumers should treat as warning signs.

### NUM_003 — log(0) in CLR transform if zero-replacement fails

- **Failure mode:** `np.log(0) = -inf` propagates through CLR, breaks Helmert projection.
- **Conditions:** Input CSV with `0.0` value not caught by `ingest_csv` zero-replacement.
- **Mitigation:** `ingest_csv` replaces every `0.0` with `DEFAULT_DELTA = 1e-15` before any math; `validate_rows` then asserts strict positivity.
- **Evidence:**
  - TEST: smoke test confirms zero values get replaced and counted.
  - STRC: code path `for k, v in enumerate(vals): if v == 0.0: vals[k] = DEFAULT_DELTA`.
- **Residual risk:** none

### NUM_004 — Eigenvalue computation fails on near-singular kappa_HS

- **Failure mode:** `np.linalg.eigvalsh` returns NaN, breaks `condition_number` reporting.
- **Conditions:** Compositions exactly at the simplex centroid (`[1/D, 1/D, ..., 1/D]`).
- **Mitigation:** Code uses `eigvalsh` (Hermitian eigensolver, more stable), and centroid trajectories are flagged by `degeneracy_flags.row_variance_below_threshold`.
- **Evidence:**
  - STRC: kappa_HS_full uses `np.linalg.eigvalsh` not generic `eig`.
  - TEST: `uniform_centroid_d8` runs without NaN propagation.
- **Residual risk:** none

### NUM_005 — Attractor fit period_stability becomes negative

- **Failure mode:** `period_stability` outside [0, 1] indicates fitter saw spurious anti-correlation.
- **Conditions:** Stochastic noise dominates signal; lag-1 autocorrelation is positive (fitter expects negative for period-2).
- **Mitigation:** `fit_attractor` clamps `period_stability = max(0.0, ...)`; values below `period_threshold=0.6` set `fitted=False` with explanatory warning.
- **Evidence:**
  - STRC: explicit `max(0.0, ...)` clamp at attractor.py L155.
  - TEST: monotonic-trajectory smoke test gives `fitted=False` with warning.
- **Residual risk:** none

### NUM_006 — Float-formatting drift between Python json.dumps and another implementation

- **Failure mode:** `cnt_content_sha256` differs across Python versions or non-Python consumers reproducing the canonical-JSON.
- **Conditions:** Cross-language verification (Python ↔ R) without per-field comparison.
- **Mitigation:** Determinism contract is **within-language byte-identical**; cross-language is per-field-numerical only. Acknowledged limitation, documented in design doc §3.3.
- **Evidence:**
  - DOC: design doc §3.3 explicitly carves out cross-language hash from the contract.
- **Residual risk:** acknowledged_limitation

---

## ALG — Algorithmic failure modes

### ALG_001 — Helmert basis convention drift between cnt.py and hci_shared

- **Failure mode:** CNT and CNQ use different Helmert conventions, producing different ILR coordinates for identical input.
- **Conditions:** `helmert_basis(D)` defined in two places with subtle indexing differences.
- **Mitigation:** v3 imports `helmert_basis` from `hci_shared.geometry`; no local copy in cnt.py.
- **Evidence:**
  - STRC: cnt.py line 73, single `from hci_shared import helmert_basis`.
  - TEST: smoke test produces orthonormal H @ Hᵀ = I to 4.44e-16.
- **Residual risk:** none

### ALG_002 — argmax tie-break in helmsman_dcdi non-deterministic

- **Failure mode:** When two carriers have equal |Δh|, different tie-breaks across runs produce different sigma sequences.
- **Conditions:** Symmetric synthetic inputs (e.g., constant trajectories, perfectly alternating periodic patterns).
- **Mitigation:** `np.argmax` returns first index of max, deterministic within a NumPy version. Documented convention.
- **Evidence:**
  - DOC: docstring of `helmsman_dcdi`: "ties broken by lowest index".
  - STRC: `int(np.argmax(np.abs(delta)))`.
- **Residual risk:** none — within-version deterministic; cross-version drift is an INT failure (see INT_002).

### ALG_003 — ring_classify boundary inclusion off-by-one

- **Failure mode:** A composition with `hs == 0.1` falls into Hs-1 instead of Hs-2 (or vice versa).
- **Conditions:** Hand-crafted compositions exactly at ring boundaries.
- **Mitigation:** Convention locked: right-exclusive at every ring (`if hs < 0.1: return "Hs-1"`).
- **Evidence:**
  - DOC: docstring locks "Right-exclusive except the top ring."
  - STRC: code matches docstring exactly.
- **Residual risk:** none

### ALG_004 — variation_matrix uses wrong ddof

- **Failure mode:** Variance computed with sample ddof=1 instead of population ddof=0; results differ from CoDa standard.
- **Conditions:** Cross-tool reproducibility against the `compositions` R package.
- **Mitigation:** Explicit `np.var(ratio, ddof=0)` per CoDa convention (population variance). Locked in code comment.
- **Evidence:**
  - STRC: `tau[i, j] = float(np.var(ratio, ddof=0))` with comment `(population variance)`.
- **Residual risk:** none

### ALG_005 — triadic_area uses (h0, h1) plane only

- **Failure mode:** Triad area formula projects onto first two ILR axes; for D ≥ 4 the 3-D triangle area is not preserved.
- **Conditions:** D ≥ 4 trajectories where structure lives in axes ≥ 2.
- **Mitigation:** Acknowledged limitation. Triadic area is a heuristic projection diagnostic, not a metric-preserving area. The `sides` array reports actual 3-D Euclidean distances for the triangle, which is the more meaningful quantity.
- **Evidence:**
  - DOC: design doc §4 documents this; engine code marks the area as a 2-D projection.
- **Residual risk:** acknowledged_limitation

### ALG_006 — Period detection in attractors confuses period-2 with anti-correlated noise

- **Failure mode:** Random Dirichlet trajectory with weak negative lag-1 autocorrelation (by chance) reports `fitted=True`.
- **Conditions:** Short trajectories (T near T_min=8) with high noise.
- **Mitigation:** `period_stability` threshold of 0.6 + amplitude_A threshold of 1e-10 + relative-variance floor (1e-12 of max_var) filter spurious detections.
- **Evidence:**
  - TEST: smoke test on monotonic + random-Dirichlet trajectories gives `fitted=False` with warnings.
  - STRC: three-stage filter chain in `fit_attractor`.
- **Residual risk:** bounded — adversarial inputs can be crafted to fool the detector; production usage on real corpora has not produced false positives.

---

## SCH — Schema failure modes

### SCH_001 — `coda_standard` / `higgins_extensions` split drifts

- **Failure mode:** Fields move between blocks, breaking downstream consumers that read the locked split.
- **Conditions:** Refactoring without doctrine awareness.
- **Mitigation:** Field-ownership locked in cnt.py docstring; design doc §4.3 carries the canonical split table.
- **Evidence:**
  - DOC: cnt.py docstring locks the split per timestep entry.
  - STRC: `compute_timestep_block` builds two explicit dicts.
- **Residual risk:** none

### SCH_002 — `depth_tower` fields missing for T < 2

- **Failure mode:** Schema-incomplete output crashes downstream consumers.
- **Conditions:** Single-row input.
- **Mitigation:** `compute_depth_tower` early-exits energy/curvature loops when `T < 2`; `attractor` block returns unfit dict; `involution_M_squared.samples` lists what could be sampled (just t=0 if T=1).
- **Evidence:**
  - TEST: T=1 smoke test runs to completion, returns full schema.
- **Residual risk:** none

### SCH_003 — `helmsman_family` rolling arrays could be empty

- **Failure mode:** `flips.rolling = []` for short trajectories breaks consumers expecting fixed-length arrays.
- **Conditions:** T < window length (default 8).
- **Mitigation:** `compute_helmsman_family` clamps effective window to `max(2, min(window, T-1))`. Empty rolling arrays are valid per schema.
- **Evidence:**
  - DOC: helmsman.py docstring documents rolling windows can be empty.
  - TEST: T=1 case returns `flips.rolling = []` without crash.
- **Residual risk:** none

### SCH_004 — Output JSON exceeds practical size on T-large × D-large inputs

- **Failure mode:** kappa_HS_full matrix per timestep means D² floats × T timesteps can balloon.
- **Conditions:** D=16, T=1000 produces 16² × 1000 = 256,000 floats just for the matrix; plus eigenvalues, trace, etc.
- **Mitigation:** Acknowledged limitation; large-T inputs should chunk or reduce resolution. Triadic area + subcomposition ladder respect TRIADIC_K_DEFAULT and LADDER_K_LIMIT caps.
- **Evidence:**
  - DOC: design doc §4.1 mentions the trade-off.
- **Residual risk:** acknowledged_limitation

### SCH_005 — `_function` / `_description` underscore-prefixed metadata fields could be stripped by overzealous JSON cleaners

- **Failure mode:** Some JSON-handling tools remove keys starting with `_` as "private."
- **Conditions:** Output piped through such a cleaner.
- **Mitigation:** Underscore-prefix is project convention for self-describing metadata. Documented in NOTATION_AND_TERMINOLOGY. Consumers must preserve them.
- **Evidence:**
  - DOC: convention documented.
- **Residual risk:** bounded — if a downstream tool strips them, semantic content is intact; only the descriptive metadata is lost.

---

## INV — Input-validation failure modes

### INV_001 — Negative carrier accepted silently

- **Failure mode:** `log(negative)` produces NaN; CLR / ILR / Helmert all corrupt silently.
- **Conditions:** Input CSV with negative values.
- **Mitigation:** `validate_rows` rejects with `InvalidInputError` reporting the offending row index; runs *before* any math.
- **Evidence:**
  - TEST: smoke test confirms `InvalidInputError` raised on negative input.
- **Residual risk:** none

### INV_002 — Zero carrier silently produces ratio of zero

- **Failure mode:** `1/0` overflow.
- **Conditions:** Input CSV with `0.0` cell.
- **Mitigation:** `ingest_csv` replaces zeros with `DEFAULT_DELTA = 1e-15` and counts them; `zero_replacement_count` reported in output.
- **Evidence:**
  - STRC: explicit replacement loop.
  - SCH: `input.zero_replacement_count` field in output.
- **Residual risk:** none

### INV_003 — NaN/Inf in input

- **Failure mode:** Propagation into all downstream math.
- **Conditions:** Input CSV with `nan` or `inf` text values.
- **Mitigation:** `csv.reader` + `float()` raises `ValueError` on `nan`/`inf` (Python `float()` accepts them, but `validate_rows.np.isfinite()` catches them).
- **Evidence:**
  - STRC: `validate_rows` checks `np.isfinite(arr).all()`.
- **Residual risk:** none

### INV_004 — D < 2 (single-carrier or empty)

- **Failure mode:** Closure / CLR not defined for D < 2.
- **Conditions:** Input CSV header with no carrier columns or one carrier column.
- **Mitigation:** `ingest_csv` rejects header < 2 columns; `validate_rows(min_carriers=2)` rejects D=1.
- **Evidence:**
  - STRC: explicit check in `ingest_csv`.
- **Residual risk:** none

### INV_005 — T = 0 (empty data)

- **Failure mode:** Pipeline produces malformed empty output.
- **Conditions:** Input CSV with header only, no data rows.
- **Mitigation:** `ingest_csv` raises `InvalidInputError` if `rows.size == 0`.
- **Evidence:**
  - STRC: explicit check.
- **Residual risk:** none

### INV_006 — Encoding errors silently substituted

- **Failure mode:** Bad bytes get U+FFFD replacement, silently corrupting carrier names or values.
- **Conditions:** Input CSV is not UTF-8 (e.g., legacy encoding).
- **Mitigation:** `ingest_csv` opens with `errors='strict'`; bad bytes raise `UnicodeDecodeError` immediately.
- **Evidence:**
  - STRC: `open(p, "r", encoding="utf-8", errors="strict", ...)`.
- **Residual risk:** none

---

## INT — Integration failure modes

### INT_001 — `git rev-parse HEAD` fails when not in a git working tree

- **Failure mode:** Engine crashes during environment-metadata capture.
- **Conditions:** Engine run from a tarball-extracted source without `.git/`.
- **Mitigation:** `get_environment_metadata` wraps subprocess in try/except for `FileNotFoundError`, `TimeoutExpired`, `OSError`; returns `git_sha=None` gracefully.
- **Evidence:**
  - STRC: explicit exception handling.
- **Residual risk:** none

### INT_002 — NumPy version drift changes float repr

- **Failure mode:** `cnt_content_sha256` differs across NumPy versions even on identical input.
- **Conditions:** Engine run on different NumPy minor versions.
- **Mitigation:** `numpy_version` is in `metadata.environment` (which is stripped from canonical hash). Within-version determinism holds; cross-version drift is documented as cross-language-tier per design §3.3.
- **Evidence:**
  - DESN: design doc §3.3.
- **Residual risk:** acknowledged_limitation

### INT_003 — `subprocess.run` with `shell=False` immune to shell-injection

- **Failure mode:** Crafted input filename injects shell commands.
- **Conditions:** Untrusted CSV path.
- **Mitigation:** `subprocess.run([..., str(repo_root)], ..., shell=False)` always; argv is a list, never a string.
- **Evidence:**
  - STRC: `subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(repo_root), ...)`.
- **Residual risk:** none

---

## INTP — Interpretation failure modes

### INTP_001 — `ir_class` thresholds are heuristic

- **Failure mode:** Reader interprets `LIGHTLY_DAMPED` as a precise dynamical-systems classification.
- **Conditions:** Domain-specific interpretation without consulting the wrapper.
- **Mitigation:** IR taxonomy thresholds (A < 0.1 → CRITICALLY_DAMPED, etc.) are documented as heuristic; domain wrappers re-interpret per their conventions.
- **Evidence:**
  - DOC: NOTATION_AND_TERMINOLOGY documents IR taxonomy as a categorical classifier with locked thresholds, not a precise damping ratio.
- **Residual risk:** bounded — domain over-interpretation is the wrapper's responsibility to manage.

### INTP_002 — `triadic_area` sampling makes results stochastic for T > 500

- **Failure mode:** Reader interprets the top-K triads as exhaustive.
- **Conditions:** T > 500.
- **Mitigation:** `triadic_sampling.applied=true` and `seed=42` recorded in output; `total_triads_available` reported separately.
- **Evidence:**
  - SCH: explicit field documenting sampling state.
- **Residual risk:** none

### INTP_003 — `subcomposition_ladder` cap at 200 makes high-degree results partial

- **Failure mode:** Reader interprets the mean correlation as exhaustive over all C(D,k) subsets.
- **Conditions:** D large (D ≥ 7 hits the cap at degree 4).
- **Mitigation:** `n_subsets_total` and `n_subsets_scored` reported separately so consumers can compute the coverage fraction.
- **Evidence:**
  - SCH: explicit fields.
- **Residual risk:** none

### INTP_004 — Helmsman σ over-interpreted as causal driver

- **Failure mode:** Reader treats σ_t as "the carrier causing the change."
- **Conditions:** Audio engineer reading the diagnostic without consulting the wrapper.
- **Mitigation:** Engine docstring describes σ as "argmax_j |Δh_j(t)|" — descriptive, not causal. Audio wrapper translates to "leading driver" with explicit "this is descriptive, not causal" caveat.
- **Evidence:**
  - DOC: docstrings.
  - WRP: HCI-AUDIO/CNQ_AUDIO_WRAPPER.md interpretation.
- **Residual risk:** bounded — depends on wrapper discipline.

---

## REP — Reproducibility failure modes

### REP_001 — Two runs of identical input produce different hashes

- **Failure mode:** Determinism contract broken.
- **Conditions:** Engine logic non-deterministic somewhere.
- **Mitigation:** All randomness is seeded (e.g., triadic sampling seed=42). Volatile fields (`generated`, `wall_clock_ms`, `environment`) stripped from canonical hash. Smoke test asserts byte-identical hash across two runs.
- **Evidence:**
  - TEST: smoke test ✓ (det_ok = True).
- **Residual risk:** none

### REP_002 — Hash drifts when stored expected_results.json is reloaded

- **Failure mode:** JSON round-trip changes float formatting; expected hash differs after load.
- **Conditions:** Self-test compares against expected hash from disk.
- **Mitigation:** Self-test compares per-field within tolerance, not hash equality across stored vs computed.
- **Evidence:**
  - DESN: STP-1.0 protocol §5.
- **Residual risk:** none

---

## DOC — Documentation failure modes

### DOC_001 — engine docstring drifts from actual behaviour

- **Failure mode:** Reader implements based on the docstring, gets different output.
- **Conditions:** Refactor without docstring update.
- **Mitigation:** Docstrings co-located with functions; SEA discipline requires anti-spec entries to cite TEST evidence by file path + test name, which surfaces drift.
- **Evidence:**
  - DESN: SEA doctrine §11.
- **Residual risk:** bounded — relies on author discipline.

### DOC_002 — vocabulary conflation (κᴴˢ vs s_j)

- **Failure mode:** Reader confuses order-2 metric tensor with order-1 sensitivity vector.
- **Conditions:** Casual reading of older v2.0.4 outputs.
- **Mitigation:** v3 schema emits `kappa_HS_full` and `s_j_sensitivity` as separately-named fields; NOTATION_AND_TERMINOLOGY locks the distinction.
- **Evidence:**
  - DOC: NOTATION §1, §2.
  - SCH: explicit field names in tensor.timesteps[].higgins_extensions.
- **Residual risk:** none

### DOC_003 — INV-* references stale

- **Failure mode:** Engine docstring cites INV-XXX entries that have moved or been retired.
- **Conditions:** Catalog reorganisation.
- **Mitigation:** INV-* references in code are minimal (engine header only); catalog updates surface drift via D2 task in push #32.
- **Evidence:**
  - STRC: only header docstring cites INV-* IDs; functions don't.
- **Residual risk:** bounded — depends on catalog-maintenance discipline.

---

## ADV — Adversarial failure modes

### ADV_001 — Crafted CSV with extreme values (1e+100)

- **Failure mode:** `np.log(1e+100) ≈ 230` → CLR magnitudes ≈ 230 → variance computation overflows on subsequent products.
- **Conditions:** Adversary or buggy upstream produces huge values.
- **Mitigation:** Float64 handles 1e+100 without overflow; subsequent products still finite up to ~1e+200. Beyond that, `np.isfinite` check in `validate_rows` catches `inf`.
- **Evidence:**
  - STRC: `validate_rows.np.isfinite(arr).all()`.
- **Residual risk:** bounded — extreme inputs produce numerically valid but semantically meaningless output. Domain user must validate input ranges.

### ADV_002 — Unicode carrier names with control characters

- **Failure mode:** Carrier name contains newlines or quotes that break JSON serialisation.
- **Conditions:** Adversary-supplied CSV header.
- **Mitigation:** Python's `json.dumps` properly escapes control characters; `ensure_ascii=True` in `canonical_dumps` escapes non-ASCII as `\uXXXX`.
- **Evidence:**
  - TEST: hci_shared smoke test verifies σ → `σ` escaping.
- **Residual risk:** none

### ADV_003 — Crafted input designed to produce exactly the same sigma at every step

- **Failure mode:** Helmsman flips=0 reported as "highly stable system."
- **Conditions:** Symmetric synthetic input where argmax tie-break consistently picks carrier 0.
- **Mitigation:** Documented in helmsman.py docstring: "ties broken by lowest index"; design doc §3.4 acknowledges this is descriptive, not causal.
- **Evidence:**
  - DOC: helmsman.py docstring.
- **Residual risk:** bounded — domain reader should consult the wrapper for causal interpretation.

### ADV_004 — Pathological `T=2` input causes attractor fitter to crash

- **Failure mode:** Engine crashes on minimum-pair input.
- **Conditions:** T=2.
- **Mitigation:** `fit_attractor` checks `T < T_min=8` and returns unfit dict with warning instead of fitting.
- **Evidence:**
  - TEST: T=2 smoke test (in CNQ corpus) returns valid output without crash.
- **Residual risk:** none

---

## Acknowledged limitations

| ID | Category | Limitation | Recommended workaround |
|---|---|---|---|
| NUM_006 | NUM | Float-formatting drift across Python/NumPy versions | Use within-version determinism only; cross-language is per-field |
| ALG_005 | ALG | Triadic area is 2-D projection only | Use the `sides` array (3-D Euclidean distances) for metric-preserving comparisons |
| INT_002 | INT | NumPy minor-version drift changes hash | `numpy_version` is recorded in metadata; reproducibility is per-version-pinned |
| SCH_004 | SCH | JSON balloons on large T × D inputs | Chunk the trajectory or use `triadic_top_k` / `LADDER_K_LIMIT` config dials |

---

## Audit log

| Date | Auditor | Event |
|---|---|---|
| 2026-05-09 | Claude | Initial enumeration during Phase C1 of push #32 |
| 2026-05-09 | (pending) Peter Higgins | Review |
| 2026-05-09 | (pending) ChatGPT, Grok | External review post-push-#32 commit |

---

## Next audit due

2026-06-09 or upon next minor release of CNT v3, whichever comes first. External-audit cycle integrates with the AI cross-check pattern documented in INV-031.

---

*This document is a living artifact under SEA-1.0 doctrine.*
