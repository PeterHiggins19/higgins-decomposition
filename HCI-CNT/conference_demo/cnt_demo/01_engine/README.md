# 01_engine — Engine source + sample CSV

Self-contained engine drop for CodaWork 2026 attendees who want to read or
re-run the exact code that produced the demo outputs.

## Contents

```
01_engine/
├── cnt.py                                Python canonical (engine 2.0.4)
├── cnt.R                                 R port (parity)
└── ember_JPN_Japan_generation_TWh.csv    sample input (Japan 2000–2025)
```

These two files are byte-identical copies of the canonical engine sources
under `../../../engine/cnt.py` and `../../../engine/cnt.R`. They are bundled
here so the demo folder can be opened standalone — clone, `python cnt.py
ember_JPN_Japan_generation_TWh.csv`, get a CNT JSON.

## See also

- `../README.md` — full demo-package overview
- `../../../engine/README.md` — engine canon, signature, hash provenance
- `../../../handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md` — engine math
