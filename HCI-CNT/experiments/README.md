# Experiments — 25-experiment canonical corpus

The live working folder for the CNT canonical corpus. Every experiment
stored here is hash-traceable end-to-end:

* `<id>_input.csv` — input data (hashed in `inp.source_file_sha256`)
* `<id>_cnt.json` — canonical engine output (hashed in `diagnostics.content_sha256`)
* `JOURNAL.md` — auto-generated narrative summary

| Subfolder | Experiments |
|---|---|
| [`codawork2026/`](codawork2026/) | 10 — 8 EMBER countries + World, 1 combined panel, 1 BackBlaze |
| [`domain/`](domain/) | 8 — geochem (7) + FAO irrigation (1) |
| [`reference/`](reference/) | 2 — gold/silver, nuclear SEMF |
| [`extended/`](extended/) | 5 — markham, NGFS, Planck, financial, ChemixHub (v1.1.x additions) |

Total: **25 experiments**, all passing the determinism gate at engine
2.0.4 / schema 2.1.0.

## INDEX.json

[`INDEX.json`](INDEX.json) is the canonical registry. Every experiment
appears here with its `content_sha256`, `n_records`, `n_carriers`,
`ir_class`, `amplitude_A`, `curvature_depth`, `energy_depth`, and
`wall_clock_ms`. Mission Command reads from INDEX to know what to verify.

## Release snapshots

This folder is the live engine working folder; it changes as the engine
evolves. The dated release snapshot at engine 2.0.4 lives at
[`../../experiments/Hs-CNT_2026-05/`](../../experiments/Hs-CNT_2026-05/)
in the parent Hs research repo.

## Reproducibility

```bash
# Full corpus determinism gate
cd ..        # back to HCI-CNT/
python mission_command/mission_command.py

# Single experiment
python mission_command/mission_command.py ember_jpn
```

The corpus runs end-to-end in ~21 seconds on typical hardware. Same
input + same engine_config + same engine source → byte-identical
output, by design and by automated test.

For the verification recipe, see
[`../handbook/VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md`](../handbook/VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md)
appendix.

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
