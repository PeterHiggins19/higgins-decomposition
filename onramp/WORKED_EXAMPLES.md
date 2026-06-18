# Worked examples — "I have X, here is what Hˢ told me"

*Real runs on real, published data, each in the four-element shape (what went in → trust certificate → who is driving → when it changed). Pick the one closest to your field; the point is to recognize the *kind* of answer Hˢ gives before you bring your own X. Every example links to its full record in the repo. Honest-broker; the nulls are included on purpose — they are what make the positives trustworthy. Tier 1 unless noted.*

---

### You have a gas-analyzer trace (anaesthesia / life-support / process gas)
**Data:** expired-gas fractions {O₂, CO₂, agent, N₂}, hundreds of readings over a case. **Hˢ found:** lossless to 6.7e‑16; **O₂ is the dominant driver of mixture change in 13 of 13 real cases** across two hospitals on two continents (Seoul VitalDB + Adelaide UQ); 11 datable regime shifts in the reference case. **Why care:** the thing moving the mixture is identified and time-stamped automatically, and it replicates across an independent cohort — the honest road to confidence. *Full: `industrial-instruments/gas-composition-study/blood-gas/results_real_vitaldb/REAL_DATA_RESULTS.md` (+ `cohort/`, `results_real_uq/`).*

### You have a water-chemistry log (hydrogeochemistry / produced water)
**Data:** 683 USGS Williston-Basin samples, 7 major ions {Na, Cl, Ca, Mg, K, SO₄, HCO₃} down-depth. **Hˢ found:** lossless to 3.1e‑15; the drivers are the **minor ions SO₄ (253 helmsman steps) and HCO₃ (239) — not Na or Cl** (9 and 3), the bulk brine that magnitude-thinking would chase; 38 regime boundaries; K_eff rises 1.84→5.21 with depth. **Why care:** your bulk-dominated intuition points at the wrong ions; the compositional signal lives in the trace species. This is ratio blindness, caught on real data. *Full: `industrial-instruments/gas-composition-study/produced-water-codawork/results_real_usgs/README.md`.*

### You have core-sample geochemistry (chemostratigraphy)
**Data:** 219 Lower-Cretaceous mudstone samples (PANGAEA), {SiO₂, Al₂O₃, Rb, Zr} down-section. **Hˢ found:** **trace elements Zr (110) and Rb (68) drive over the bulk oxides SiO₂ (18) and Al₂O₃ (22)**; 19 regime tripwires; the Aitchison step size correlates (r=+0.24) with an independent CaCO₃ signal that was *not in the composition* — a blind calibration hit. **Why care:** automatic, datable facies/regime boundaries plus a hidden driver, on data you already have; reproducible offline. *Full: `collaborations/geology-wehner/demo_frielingen9/RESULTS_Frielingen9_CNT_CNQ.md` (+ `REPRODUCE.md`, offline `frielingen9_projector.html`).*

### You have time-series microbiome / abundance data
**Data:** Crohn (D=48 OTUs, 975 samples) and ECAM infant gut (34 timepoints). **Hˢ found:** Crohn — **honest null**: no global diversity separation CD-vs-control (the signal is taxon-specific, not global); ECAM — **maturation recovered from composition alone** (K_eff vs age, ρ=0.71, p=2.5e‑6). Scales lossless to D=10,000 at ~7 ms. **Why care:** it tells you *where the signal is not* (don't chase a global effect that isn't there) as readily as where it is — and it runs at metagenomic scale. *Full: `collaborations/microbiome/results/RESULTS_real_microbiome.md` (+ `RESULTS_microbiome_sniff.md`).*

### You have very high-dimensional omics (transcriptome / proteome)
**Data:** Drosophila spaceflight, D=18,952 probesets (NASA GeneLab). **Hˢ found:** lossless at 1.2e‑13; **honest global null** (ground-vs-flight composition does not separate globally — the signal is sparse and gene-specific). **Why care:** Hˢ gives you a global "navigation certificate" and tells you plainly to use differential-expression for the sparse signal — it complements your method instead of competing with it. *Full: `collaborations/spaceflight-glds1/README.md`.*

### You have national energy / market-share time series
**Data:** EMBER fuel-mix shares, 9 countries. **Hˢ found:** named, datable events detected with no prior labeling — Japan's **Fukushima 2011** spike (Aitchison step 3× neighbors, 17 helmsman flips), the UK coal exit reading OVERDAMPED_EXTREME; and a **deceptive-drift** flag where K_eff concentrates *quietly* (DEU/FRA/GBR/IND tightening in 2021 without the velocity you'd expect). **Why care:** structural change — and *quiet* structural change — surfaced automatically from public data, with policy-interpretable balances available. *Full: `papers/codawork2026/conference_2026_06/` (`per_country/`, `DECEPTIVE_DRIFT_REPORT.md`).*

### You have social-science composition data
**Data:** Pew religion shares, D=7, 6 regions. **Hˢ found:** the "rise of the Nones" running ~10 points ahead of the standing projection, surfaced as a 5–10× angular-velocity anomaly at the data splice. **Why care:** a domain with no CoDa tradition still yields a surprising, datable signal from published data. *(Marked internal.) Full: `Studies/Religion_2026-05-14/README.md`.*

### Early-warning, in any domain (the activation coefficient)
**Data:** Ramsar wetland composition (vegetation/chemistry/sediment/avian/hydroperiod). **Hˢ found (seed, Tier 2):** an invasive grass at **0.4% share doing 62% of the structural work — flagged ~4 years before** it crossed the conventional 5% detection threshold. **Why care:** the activation coefficient surfaces a tiny component punching far above its share — the early warning a magnitude threshold structurally cannot give. *Full: `papers/in_progress/WETLAND_COMPOSITIONAL_ANALYSIS_RAMSAR.md`.*

---

**The pattern.** In five of these, the driver or the warning is a *minor* component — the recurring payoff of reading ratios instead of magnitudes. In two, the honest answer is "no global signal, use your targeted method." That mix is the point: Hˢ tells you what your data says, including when it says little — which is exactly why the positive readings are worth acting on. Bring your X (see `PHD_ONRAMP_PROTOCOL.md`) and an AI will produce the same four-element answer for your field.
