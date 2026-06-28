# How to verify — the Hˢ-as-DUT stress sheet (anyone, from the repo)

*This test is self-contained and reproducible. No private data, no network. The real anchors are public
files already in the repo. Author: Peter Higgins; AI-assisted per HUF-STD-001. 2026-06-25.*

---

## One command

```
cd experiments/hs_dut_stress_2026-06
python3 hs_dut_stress.py
```

Requirements: Python 3 + NumPy. Runs in a few seconds.

## What to check

1. **Master receipt.** The output's `MASTER_RECEIPT` must equal:

   ```
   e395fa38af43be4e
   ```

   It is one SHA-256 over the entire deterministic stress table. If you get the same hash, you have
   reproduced the whole stress sheet bit-for-bit.

2. **Engine version.** `_meta.engine_version` must equal `Hs-DUT-v1.f6bebfb2`. This is stamped from the
   centres of the **real** public datasets (gas / geology / produced-water), so the version is anchored to
   real data — change the data, change the version.

3. **The envelope.** `envelope.deterministic_core_passes_all_D` must be `true` (the exactness, common-mode
   rejection, codec and conveyor pass at every D from 2 to 1000 under 10⁶× deformation), and
   `envelope.statistical_layer_failures` lists the **four** honest low-dimension limits (memory recall at
   D=2/3/4, discriminant at D=2). Those failures are expected and documented — see `THE_DUT_STRESS_REPORT.md`.

## The real data it uses (all public, in the repo)

- `industrial-instruments/gas-composition-study/results/gas_series.csv` (O₂/CO₂/N₂)
- `collaborations/geology-wehner/demo_frielingen9/frielingen9_xrf_4part.csv` (Frielingen-9 mudstone, PANGAEA 897615)
- `industrial-instruments/gas-composition-study/produced-water-codawork/results/produced_water.csv` (USGS produced water)

Higher dimensions (D = 8 … 1000) use deterministically seeded synthetic compositions (fixed seeds in the
script), so they reproduce identically on any machine.

## If your hash differs

Then either NumPy changed a reduction order on your platform (unlikely at these tolerances) or the input
files differ. Compare your `per_dimension` table against `HS_DUT_STRESS_RESULTS.json` line by line — the
deviation localises itself.

*Cross-refs: `hs_dut_stress.py`, `HS_DUT_STRESS_RESULTS.json`, `THE_DUT_STRESS_REPORT.md`. Peter is the sole
gate; nothing posted.*
