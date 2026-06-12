# Mudstone CNT/CNQ — first pass on real data (Frielingen-9)

**A reproducible run of the method on real mudstone.** Research-grade; faithful implementation of the documented Hs/CNT method; calibration preliminary. **These are instrument readings — the geological meaning is the geologist's to determine.**

## Data
Thöle et al. (2019), **Frielingen-9** core, eastern Lower Saxony Basin (PANGAEA 897615, CC-BY) — Lower Cretaceous mudstones. **219 discrete samples, 15.4–249.8 m.** WD-XRF SiO₂, Al₂O₃, Rb, Zr; plus **independent** CaCO₃ and TOC. Input file: `frielingen9_xrf_4part.csv` (cited header).

## Method
- Composition **D=4: [SiO₂, Al₂O₃, Rb, Zr]** (Rb, Zr mg/kg → same closure). This subcomposition embeds the **Si/Al** and **Zr/Rb** ratios exactly. D=4 ⇒ **CNQ native (exact)**.
- Pipeline: per-sample closure → CLR → **Helmert-ILR** (orthonormal isometry) → per-step Aitchison step, helmsman, power-share/Activation, K_eff, regime tripwire; **CNQ** = radial magnitude + step bearing-rotation of the ilr 3-vector.
- **CaCO₃ and TOC held out as independent calibration targets** (not in the composition).
- Scripts: `cnt_cnq_analysis.py` → `build_dashboard.py`. Fully reproducible — see **`REPRODUCE.md`**.

## What the instrument reported (observations only)
- **Helmsman counts** (which part steers each step): Zr **110**, Rb **68**, Al₂O₃ **22**, SiO₂ **18**. The down-section motion is carried by the trace components; the bulk Si/Al parts move least.
- **Directness 0.43** (123 helmsman flips of 218 steps) — the steering part changes often.
- **19 regime-tripwire steps** (robust threshold > median + 2·MAD of the step series).
- **Six largest Aitchison steps**, with the co-located CaCO₃ value (stated as co-occurrence, not cause): 234.9 m (CaCO₃ 22.6%), 226.9 m (8.4%), 120.8 m (12.4%), 237.8 m (16.2%), 95.8 m (11.8%), 230.9 m (34.8%).
- **Calibration against held-out targets:** Aitchison step vs |ΔCaCO₃| **r = +0.24**; vs |ΔTOC| **r = −0.08** (≈ 0).
- **CNQ (native D=4):** radial magnitude + bearing-rotation trajectory computed down-section (fig 3), exact at D=4.
- **Deceptive-drift flag:** silent here — see honest notes.

## For the geologist to determine (open questions, not answers)
The instrument does not interpret. Reading these against your knowledge of the core:
1. Do the **19 regime tripwires** and the **largest steps** coincide with picked sequence boundaries / flooding surfaces / the Weissert δ¹³C interval?
2. Is the **Zr/Rb-dominated steering** a provenance/sorting signal, a diagenetic one, or an artifact of the D=4 subcomposition choice?
3. Does the **+0.24 step–|ΔCaCO₃|** relationship mean carbonate dilution is partly steering the siliciclastic composition, or is it incidental?
4. Would a **multi-element core-scan** composition (Ca, Ti, K, Mn, Fe, Sr…) change which part is helmsman, and let the deceptive-drift detector fire?

Those are yours to answer, led by the data and the displays.

## Honest notes
- **Deceptive-drift flag silent** — by design: at this closure Zr/Rb sit just **below the 0.1% share guard** (ρ ≥ 10⁻³) the Activation-Coefficient detector requires, so it conservatively does not fire. The trace-steering is still visible in the **helmsman** channel. A calibration point to set with a domain expert.
- **Faithful method, not the canonical engine binary** — running it through the repo engine for byte-provenance is a next step.
- **D=4** uses the discrete dataset's XRF (Si, Al, Rb, Zr). Companion **high-resolution core-scan** datasets (PANGAEA 897630/632/634/636) carry many more elements at 1 cm — a richer multi-element run.
- Calibration is **preliminary** (no picked-surface overlay yet).

## Figures
- `mud_fig1_step_caco3.png` — CNT Aitchison step + regime flags vs independent CaCO₃.
- `mud_fig2_helmsman.png` — helmsman (driver per step) + deceptive-drift markers.
- `mud_fig3_cnq.png` — CNQ native radial + step bearing-rotation.

## Sources
- [Thöle et al. 2019, Frielingen-9 (PANGAEA 897615)](https://doi.pangaea.de/10.1594/PANGAEA.897615) · parent [PANGAEA 898094](https://doi.pangaea.de/10.1594/PANGAEA.898094) · paper [Thöle et al. 2020, The Depositional Record](https://doi.org/10.1002/dep2.83)

*Real data, faithful method, honest caveats. The instrument reads. The expert decides.*
