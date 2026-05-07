# QD — Corpus Comparison Plan

**Status:** experimental. See [`README.json`](README.json).
**Companion:** [`QD_CONCEPTS_FOR_TEST.md`](QD_CONCEPTS_FOR_TEST.md) lists the ten concepts; this file specifies how each is tested *against the existing CNT corpus as the standard to surpass and include*.

---

## Operating principle

The 25-experiment CNT corpus at `HCI-CNT/experiments/INDEX.json` is **the reference**. QD does not propose to "analyze" data — it proposes to **re-analyze corpus runs as a quaternion view**, then asks three things at every gate:

1. **Reproduction.** Does the quaternion view reproduce the canonical `content_sha256` byte-for-byte (or, if that's the wrong granularity, reproduce the underlying numerical quantities to ≤ 1e-12)?
2. **Addition.** Does the quaternion view expose at least one new structural fact that CNT alone cannot compute?
3. **Determinism.** Does the quaternion view itself remain deterministic and hash-chained — same inputs always give same outputs?

A quaternion view that fails (1) is wrong and gets discarded. A quaternion view that passes (1) but does not pass (2) is a re-skin and gets archived. A quaternion view that passes (1) and (2) and (3) is a candidate for promotion.

This is the "surpass and include" framing: QD must include CNT's results (every canonical hash) and surpass CNT's expressiveness (at least one new diagnostic). One without the other is not enough.

---

## The corpus as a measurement instrument

The 25 experiments span the full range of compositional analysis difficulty:

| Subfolder | n | D range | T range | IR class diversity |
|---|---:|---|---|---|
| codawork2026 | 10 | 4–9 | 25–731 | 4 of 8 IR classes |
| domain | 8 | 2–10 | 8–83 | 4 of 8 IR classes |
| reference | 2 | 2–~ | 1338–~ | 1 of 8 (D2_DEGENERATE) |
| extended | 5 | 5–10 | 17–252 | 3 of 8 IR classes |

This is the test bed. Every claim QD makes runs against this set; the corpus's known hash chain is the gate.

---

## Per-concept comparison protocol

For each concept in [`QD_CONCEPTS_FOR_TEST.md`](QD_CONCEPTS_FOR_TEST.md), the test is a four-step protocol:

**Step A — input selection.** Pick the corpus experiment(s) most diagnostic for the concept. Some concepts require a specific D (Concept 1 needs D=4 → backblaze_fleet); some span the corpus.

**Step B — quaternion-view computation.** Compute the candidate quaternion-view value from the input data. This is done *outside* the canonical engine, in an isolated script in this folder. The canonical engine is not modified.

**Step C — canonical reference value.** Read the corresponding value from the canonical CNT JSON for the same experiment. This is the gold standard.

**Step D — gate evaluation.** Compute the diff between the quaternion-view value and the canonical value. Apply the gate criterion documented in `QD_CONCEPTS_FOR_TEST.md`.

If gate passes, the concept is confirmed for that experiment. If it passes for the predicted N experiments out of 25, the concept is confirmed at the corpus level.

---

## Primary test dataset — backblaze_fleet (D=4)

**Why this dataset is critical.** D=4 is the unique simplex dimension where Aitchison's rotation group SO(D−1) = SO(3) is exactly the group whose universal cover is the unit quaternions. For D ≠ 4, the quaternion view requires either projection (information loss) or higher-order generalisations (bi-quaternions for D=8, octonions for D≤8 with caveats, Clifford algebras for general D). At D=4 there is no projection, no generalisation, no information loss — quaternions are the natural coordinates.

If QD's foundation claim doesn't fit cleanly on `backblaze_fleet`, the whole exercise is over. If it does fit cleanly, QD has a real foundation to build on.

**Canonical data:**

| Field | Value |
|---|---|
| `id` | `backblaze_fleet` |
| `subdir` | `codawork2026` |
| `T` | 731 |
| `D` | 4 |
| `ir_class` | `CURVATURE_VERTEX_FLAT` |
| `amplitude_A` | 0.0 |
| `curvature_depth` | 4 |
| `energy_depth` | 8 |
| `content_sha256` | `3e5f8db9e2b8a4a4c64aef59d1898da88f6d99d840768dd8627e5cc3beb6b06d` |
| `wall_clock_ms` | 1518 |

**Round-2 gate (Concept 1 + Concept 10).** Both must pass on backblaze_fleet for QD to advance to Round 3.

---

## Secondary test datasets — diverse-D dimensional sweep

To test how QD degrades as D moves away from 4:

| Experiment | D | T | IR class | Why this experiment |
|---|---:|---:|---|---|
| `commodities_gold_silver` | 2 | 1338 | D2_DEGENERATE | Lower D limit. Quaternion view should reduce to the U(1) bearing-only case. |
| `esa_planck_cosmic` | 5 | 17 | MODERATELY_DAMPED | First D > 4; quaternion view requires dimensional reduction. |
| `chemixhub_oxide` | 7 | 24 | DEGENERATE | Mid-high D; tests whether reduction preserves structure. |
| `ember_chn` | 8 | 26 | CRITICALLY_DAMPED | D = 2×4; tests bi-quaternion factoring (D=8 → SU(2) × SU(2) ?). |
| `geochem_tappe_kim1` | 10 | 8 | CRITICALLY_DAMPED | High D, low T; the CCTT pilot dataset; tests whether quaternion view is robust to small T. |
| `ember_combined_panel` | 9 | 207 | MODERATELY_DAMPED | Long T multi-trajectory panel; tests quaternion view of cross-dataset bundles. |

**Expected result.** QD should be cleanest at D=4, degrade gracefully at D=2 and D=8 (where quaternion-related structures still apply), and require explicit dimensional reduction at D ≠ 2, 4, 8. The pattern of degradation is itself diagnostic — it would tell us *where* in dimension the quaternion view stops being natural.

---

## Cross-dataset reference — the EMBER spectrum

For Concept 7 (Stage 4 ↔ Hamilton product), the reference is the existing CodaWork demo's cross-dataset spectrum:

- **File:** `HCI-CNT/conference_demo/cnt_demo/03_combined/spectrum_paper_codawork2026_ember.pdf`
- **Method:** the spectrum paper computes pairwise structural comparisons across the 8 EMBER countries + World aggregate.
- **QD reproduction:** compute the same comparisons via Hamilton products of the per-country quaternion trajectories; diff the values.

If the diff is at numerical noise, the Stage 4 module is the channel-decomposed form of quaternion multiplication, and we can replace the bespoke Stage 4 logic with one line of quaternion algebra in the proposed Volume IV.

---

## Calibration reference — the Stage 2 directness fixtures

For Concept 10 (directness ↔ scalar/vector velocity), the reference is the existing calibration fixtures:

- **Files:** `HCI-CNT/atlas/STANDARD_CALIBRATION_stage2_*`
- **Method:** these fixtures contain known directness=1 and directness=0 reference trajectories, documented to IEEE-floor precision.
- **QD reproduction:** reconstruct each fixture as a quaternion path; verify pure-scalar / pure-vector velocity decomposition.

If the decomposition is exact at the IEEE floor, the directness parameter is literally the scalar/vector mixture parameter of the quaternion velocity, and the fixtures gain a deeper interpretation.

---

## What "surpass" means concretely

QD doesn't just need to reproduce CNT — it needs to add. Three candidate additions:

**Addition 1 — trajectory parity class (per-experiment scalar).** Every quaternion trajectory has a well-defined *parity*: even (vector sector, lifts to SO(3)) or odd (spinor sector, lifts only to SU(2)). CNT does not currently expose this. The quaternion view computes it as a side-product of Concept 8. Adding it to every JSON would be a new top-level diagnostic field with cost ~zero.

**Addition 2 — relative-trajectory quaternion (per-pair structure).** Stage 4 currently produces per-pair scalar comparisons. Quaternion algebra naturally produces a per-pair *unit quaternion* that encodes the full relative orientation between two trajectories at every timestep. CNT cannot express this in its current vocabulary; quaternion algebra gives it for free.

**Addition 3 — SLERP between timesteps (smooth interpolation).** Currently, between-timestep interpolation in CNT is approximated linearly in CLR space. The quaternion view gives **spherical linear interpolation** on S³ — the geodesic interpolation that respects the underlying simplex geometry exactly. This would benefit the projector_html and any future continuous-time visualisations.

If at least one of these three additions can be demonstrated cleanly on the corpus, QD has surpassed in addition to including.

---

## Determinism

Quaternion algebra is deterministic. The choice of Helmert basis is a fixed convention. The atan2 step is deterministic to IEEE-floor precision. The Hamilton product is deterministic. So the quaternion view, once anchored on a fixed Helmert convention, gives a hash-chainable output indistinguishable in audit-quality from CNT's current JSON.

A QD-generated JSON would carry its own `qd_diagnostics.content_sha256` field, separate from the canonical CNT `diagnostics.content_sha256`. A reviewer auditing a QD-promoted result would check both: the CNT hash to confirm CNT-level integrity, and the QD hash to confirm quaternion-view integrity. Both must match the published values.

---

## What gets reported back

After each round, this folder gains:

| Round | Report file (proposed) |
|---|---|
| 2 | `QD_ROUND_2_REPORT.md` — Concept 1 + 10 results on backblaze_fleet + calibration fixtures |
| 3 | `QD_ROUND_3_REPORT.md` — Concept 2, 3, 7 results across the corpus |
| 4 | `QD_ROUND_4_REPORT.md` — Additions demonstration (parity class, relative-quaternion, SLERP) |
| 5 | `QD_VOLUME_IV_DRAFT.md` — Promotion proposal as draft handbook volume |

Each report includes hashes, code excerpts, and reproducibility recipes. Even at status `0.0.1-experimental`, every QD output is hash-chained from day one — that's what "include CNT's standard" requires.

---

## Failure modes

If QD fails at any gate, this is *not* a setback to the canonical CNT system. CNT's hashes don't change; CNT's papers don't change; CNT's CodaWork story doesn't change. QD is exploratory by design; failure modes are documented for future reference and the project archives quietly.

The three failure scenarios:

1. **Concept 1 fails on backblaze_fleet.** The quaternion view doesn't actually reproduce the CLR vectors. Investigate the Helmert convention, the axis-angle embedding, or the closure step — most likely a fixable orientation/sign mistake. If unfixable, QD is wrong about the foundation; archive.

2. **Concept 1 passes but most other concepts fail.** The Aitchison D=4 ↔ quaternion isomorphism is real, but it doesn't extend to the dynamics (channels, attractors, etc.). This is still interesting and worth a short paper, but doesn't justify integration. Status stays at `0.1.0-candidate` indefinitely.

3. **Most concepts pass but no addition can be demonstrated.** Quaternion view is a faithful re-coordination of CNT, with no new content. Status stays at `0.2.0-validated`; the result becomes a Volume IV essay rather than an active subsystem.

---

## Round 2 trigger

This document does not run any tests. It defines what running them would look like.

To begin Round 2, Peter would say something like *"QD round 2 — start"* and Claude would, *in a fresh Cowork session inside this folder*:

1. Write an isolated Python script `QD_round_2.py` that performs Concept 1 and Concept 10 against backblaze_fleet and the calibration fixtures.
2. Run it; capture the diffs.
3. Write `QD_ROUND_2_REPORT.md` with the verdict.
4. Update `HCI-CNQ_ADMIN.json` with the new status.

Until then, QD remains documents-only.

---

*Exploration. The corpus is the reference. Surpass and include or archive cleanly.*
