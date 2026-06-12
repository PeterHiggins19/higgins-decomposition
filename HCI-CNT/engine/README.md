> ⚠️ **ARCHIVED — frozen oracle · past reference only.** Not the active engine. Current engine: **CN‑TT v4** → [`../../HCI-CNTT/`](../../HCI-CNTT/) (latest info always there; see [`../../HCI-CNTT/CNTT_COMPLETE_SPECIFICATION.md`](../../HCI-CNTT/CNTT_COMPLETE_SPECIFICATION.md) and [`../../HS_GUIDE.md`](../../HS_GUIDE.md)). v4 reproduces this engine's output bit‑for‑bit (Backblaze parity). Do not build new work here.

---

# Engine — Compositional Navigation Tensor

The deterministic CNT engine. Same input + same configuration ⇒
byte-identical `content_sha256`.

| File | Purpose |
|---|---|
| [`cnt.py`](cnt.py) | Python canonical engine, version **3.1.0** |
| [`cnt.R`](cnt.R) | R parity port, version 3.0.0 (v3.1.0 parity queued as EngPromo-2 post-conference) |
| ⭐ [`CNT_PSEUDOCODE.md`](CNT_PSEUDOCODE.md) | **Language-agnostic algorithm reference for v3.1.0** — re-implement in any language from this document alone |
| [`ANTI_SPECIFICATION.md`](ANTI_SPECIFICATION.md) | What the engine MUST NOT do (failure-mode catalogue) |
| [`native_units.py`](native_units.py) | v1.1-B native-units helper (input_units / higgins_scale_units / units_scale_factor_to_neper) |
| [`tests/`](tests/) | determinism gate + parity tests |

**For skeptical users:** see [`../../TRUST_AND_VERIFICATION.md`](../../TRUST_AND_VERIFICATION.md) at the repo root. That document explains how to independently verify this code without running it: read the pseudocode, re-implement in your language of choice, run on the three canonical reference inputs (Backblaze, Planck CMB, SM neutrino), compare `content_sha256` against the published values. The engine is published in four forms (Python + R + pseudocode + HUF-STD-002 specification) precisely so that trust is earned by independent reproduction, not expected by default.

## Usage

```python
from engine import cnt
j = cnt.cnt_run("input.csv", "output.json",
                ordering={"is_temporal": True, "ordering_method": "by-time"})
```

## Schema

The engine writes JSON conforming to **schema 2.1.0** — see
[`../handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md`](../handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md)
Part E for the full schema reference.

## Determinism contract

Every constant in the USER CONFIGURATION block at the top of
`cnt.py` is echoed in `metadata.engine_config` of every output JSON.
Different config → different `content_sha256`, by design and by
automated test. Engine source is hashed into
`metadata.engine_config.engine_signature`; every page footer of every
generated PDF carries this signature.

For the full audit chain, see
[`../handbook/VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md`](../handbook/VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md)
Part A.

---

*The instrument reads. The expert decides. The hashes carry the receipts.*

## Known design choices (documented per Grok cross-check round 2, 2026-05-08)

**Triadic enumeration cap.** The `cnt.py` engine caps triadic-relationship enumeration at T = 500 timesteps. This is a deliberate design choice because the cost of triple-enumeration grows combinatorially with T (specifically O(T³) in the worst case for a naive triplet pass). For T > 500, the engine emits the standard CNT JSON without the triadic block, with a `_triadic_skipped: true` flag in the diagnostics block. The decision to enable triadic analysis on longer series should be made deliberately — typically by sub-sampling or windowing the trajectory before invoking the engine, rather than by removing the cap. See `HCI-CNT/handbook/VOLUME_2_PRACTITIONER_AND_OPERATIONS.md` §E for the rationale.

**R port version skew.** The R port `cnt.R` was last refreshed 2026-05-06; the Python `cnt.py` had a docstring update on 2026-05-08 (push #28 — terminology refinement around "rank-1" → "1D / single-axis" in the quaternion-log description). The algorithmic content is identical; the docstring updates are documentation revisions. The cross-language parity contract is on numerical output and `content_sha256`, not on docstring text. A future push will sync the R port docstrings; this is a low-priority item.

**Pseudocode placeholders.** Some `...` placeholders appear in handbook Volume 1 §F-Stage3 sections describing depth-tower iteration patterns. These are intentional — the placeholders point at the canonical source (`HCI-CNT/atlas/stage3_locked.py`) rather than duplicating implementation details. Future handbook refresh will either inline the source or expand the pseudocode to be fully self-contained.
