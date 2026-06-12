# 02_per_country — EMBER per-country pages

One folder per country (8 EMBER + World), each with the canonical CNT JSON
plus full Stage 1 + Stage 2 PDFs rendered against engine 2.0.4 / schema 2.1.0.

## Contents

```
02_per_country/
├── ember_chn/    China 2000–2025 — JSON + Stage 1 + Stage 2
├── ember_deu/    Germany ditto
├── ember_fra/    France ditto
├── ember_gbr/    United Kingdom ditto
├── ember_ind/    India ditto
├── ember_jpn/    Japan ditto
├── ember_usa/    United States ditto
└── ember_wld/    World aggregate ditto
```

Each per-country subfolder contains the input CSV, the canonical
`<country>_cnt.json`, and the auto-titled, hash-stamped Stage 1 + Stage 2
PDFs. All eight share the same Helmert basis and pass the determinism gate
bit-for-bit against the canonical experiments folder.

## See also

- `../README.md` — full demo-package overview
- `../03_combined/` — cross-country spectrum + 3D plate-time projector
- `../../../experiments/codawork2026/` — canonical source for these JSONs
