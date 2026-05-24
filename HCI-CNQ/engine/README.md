# Engine — Compositional Navigation Quaternion

The deterministic CNQ engine. Same input + same configuration ⇒ byte-identical `cnq_content_sha256`.

The engine-independence policy is in force: `cnt_content_sha256` and `cnq_content_sha256` are unrelated by design. Each engine can be verified independently. CNT reads the static partition (amplitude); CNQ reads the dynamic trajectory (phase) on S³ ≅ SU(2).

| File | Purpose |
|---|---|
| [`cnq.py`](cnq.py) | Python canonical engine, version **2.0.0** (shipped in push #26) |
| [`cnq.R`](cnq.R) | R parity port, version 2.0.0 (shipped in push #27) |
| ⭐ [`CNQ_PSEUDOCODE.md`](CNQ_PSEUDOCODE.md) | **Language-agnostic algorithm reference** — re-implement in any language from this document alone |
| [`CNQ_SCHEMA.md`](CNQ_SCHEMA.md) | Formal CNQ output schema (schema cnq/2.0.0) |
| [`ANTI_SPECIFICATION.md`](ANTI_SPECIFICATION.md) | What the engine MUST NOT do (failure-mode catalogue) |
| [`geometry.py`](geometry.py) | Quaternion algebra helpers (Hamilton product, conjugate, sandwich, SLERP, log) |
| [`hashing.py`](hashing.py) | Canonical serialization and `content_sha256` computation |
| [`cnt_adapter.py`](cnt_adapter.py) | Adapter that consumes CNT JSON output as input to CNQ |
| [`self_test/run_self_test.py`](self_test/run_self_test.py) | End-to-end self-test against pinned reference data |
| [`tests/`](tests/) | Determinism, dimension-policy, first-principles tests |

**For skeptical users:** see [`../../TRUST_AND_VERIFICATION.md`](../../TRUST_AND_VERIFICATION.md) at the repo root. That document explains how to independently verify this code without running it: read the pseudocode, re-implement in your language of choice, run on the three canonical reference inputs (Backblaze, Planck CMB, SM neutrino), compare `cnq_content_sha256` against the published values. The engine is published in four forms (Python + R + pseudocode + HUF-STD-002 specification) precisely so that trust is earned by independent reproduction, not expected by default.

## Usage

```python
from engine.cnq import run_cnq
payload = run_cnq(
    cnt_json_path="your_cnt_output.json",
    input_csv_path="your_data.csv",          # optional fallback if CNT JSON doesn't carry input
    out_path="your_cnq_view.json",
)
print(payload["cnq_view"]["quaternion_path"]["max_residual"])
print(payload["cnq_content_sha256"])
```

```R
source("HCI-CNQ/engine/cnq.R")
payload <- cnq_run(
  cnt_json_path = "your_cnt_output.json",
  input_csv_path = "your_data.csv",
  out_path = "your_cnq_view.json"
)
cat(payload$cnq_view$quaternion_path$max_residual, "\n")
cat(payload$cnq_content_sha256, "\n")
```

## Schema

The engine writes JSON conforming to **schema cnq/2.0.0** — see [`CNQ_SCHEMA.md`](CNQ_SCHEMA.md) for the formal output structure, and [`CNQ_PSEUDOCODE.md`](CNQ_PSEUDOCODE.md) for the algorithm that produces it.

## Determinism contract

Every constant in the USER CONFIGURATION block at the top of `cnq.py` is echoed in `metadata.engine_config` of every output JSON. Different config → different `cnq_content_sha256`, by design and by automated test (`tests/test_determinism.py`). Engine source is hashed into `metadata.engine_config.engine_signature`.

The IEEE-floor convergence on Backblaze and Planck CMB (`max_residual = 4.441 × 10⁻¹⁶`) is bit-identical between Python and R implementations — that is the determinism contract in operation. The framework's core claim that **two independent implementations following the pseudocode produce the same hash on the same input** is empirically validated at the IEEE float64 floor.

## Engine-independence policy

The CNQ engine produces a hash (`cnq_content_sha256`) that is *not* algorithmically derived from CNT's hash. This is by design and mirrors a structural fact about the underlying physics: amplitude (CNT readout) and phase (CNQ readout) are mathematically independent. See flagship §11 *Implications for Hˢ* and §4.3 *Paired Measurement Doctrine* for the full rationale.

## Three IEEE-floor confirmation datasets

| Dataset | D | T | max_residual | termination | parent_cnt_content_sha256 |
|---|---|---|---|---|---|
| Backblaze fleet | 4 | 731 | 4.440892098500626e-16 | LIMIT_CYCLE_P2 | (see experiments/backblaze/) |
| Planck CMB | 4 | 2499 | 4.440892098500626e-16 | LIMIT_CYCLE_P2 / OVERDAMPED_EXTREME | `3de7d4007866dc11c64d5342974d6c9d2dfc1906166627999194df3fe6a400c4` |
| SM neutrino | 3 | 1000 | 3.330669073875470e-16 | LIMIT_CYCLE_P2 / LIGHTLY_DAMPED | `60d733d2219fbe3cf6ea5647d0f17139923d578ffee0d16a124fbe4eac526952` |

Bit-identical residuals on physically unrelated D=4 datasets → the residual is hardware float64 representation, not algorithmic noise. The math is exact on the simplex.

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
