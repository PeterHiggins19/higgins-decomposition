# Engine — Compositional Navigation Tensor

The deterministic CNT engine. Same input + same configuration ⇒
byte-identical `content_sha256`.

| File | Purpose |
|---|---|
| [`cnt.py`](cnt.py) | Python canonical engine, version 2.0.4 |
| [`cnt.R`](cnt.R) | R parity port, version 2.0.4 |
| [`native_units.py`](native_units.py) | v1.1-B native-units helper (input_units / higgins_scale_units / units_scale_factor_to_neper) |
| [`tests/`](tests/) | determinism gate + parity tests |

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
