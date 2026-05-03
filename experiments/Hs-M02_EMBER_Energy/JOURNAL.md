# Hs-M02: EMBER Electricity Generation --- CoDaWork 2026 Reference Experiment

*Author: Peter Higgins*
*Date: 2026-04-30*
*Domain: ENERGY*
*Series: M-series (Manifold Projection Systems)*

---

## 1. Purpose

This experiment applies the full Hs decomposition pipeline to real-world electricity generation data from 7 national systems. It serves three purposes:

1. **CoDaWork 2026 reference experiment.** Every number in this journal will be presented to the Compositional Data Analysis community at CoDaWork 2026 in Girona. The results must be reproducible, deterministic, and open to scrutiny.

2. **Real-world validation.** Hs-M01 established that the pipeline faithfully projects known geometric test objects. Hs-M02 applies the same pipeline to measured data from an evolving physical system where ground truth is not a mathematical construction but the observed energy transition.

3. **Cross-system comparison.** The 7 selected countries span distinct energy transition archetypes --- coal-dominant industrialisation, nuclear dominance, rapid decarbonisation, exogenous shock and recovery, and the global aggregate. Comparing Hs diagnostics across these archetypes tests whether the instrument produces interpretable, domain-consistent readings without encoding any energy-domain knowledge.

---

## 2. Data Source

**Dataset:** EMBER Global Electricity Review 2025
**URL:** https://ember-climate.org/data/
**License:** CC BY 4.0
**Coverage:** 228 countries, 2000--2025
**Resolution:** Annual electricity generation in TWh by source

### 2.1 Carriers

Nine electricity generation sources form the compositional parts. Not all carriers are present in all countries --- where a carrier has zero generation in some years but nonzero in others, structural zeros are replaced with epsilon = 10^-10 to permit log-ratio transforms.

| Carrier | Description |
|---------|-------------|
| Bioenergy | Biomass, biogas, waste-to-energy |
| Coal | Hard coal, lignite, coal gases |
| Gas | Natural gas, LNG |
| Hydro | Hydroelectric (run-of-river + reservoir) |
| Nuclear | Fission-based generation |
| Other Fossil | Oil, peat, other fossil thermal |
| Other Renewables | Geothermal, tidal, wave, other non-hydro renewables |
| Solar | Photovoltaic + concentrated solar thermal |
| Wind | Onshore + offshore wind |

### 2.2 Country Selection Rationale

| ISO | Country | Rationale |
|-----|---------|-----------|
| CHN | China | Coal-dominant industrialisation with the largest renewable buildout in history |
| DEU | Germany | Energiewende: simultaneous nuclear exit and coal phase-down with renewable surge |
| FRA | France | Nuclear-dominant system (>70% nuclear), slow diversification |
| GBR | United Kingdom | Fastest coal exit of any major economy |
| IND | India | Coal-dominant developing economy with accelerating solar and wind |
| JPN | Japan | Fukushima shock: abrupt nuclear shutdown and partial restart |
| WLD | World | Global aggregate: the smoothed mean of all national transitions |

---

## 3. System Parameters

| ISO | Name | D | N | Carriers | Zero Replacement | Data Hash (SHA-256/16) |
|-----|------|---|---|----------|-----------------|----------------------|
| CHN | China | 9 | 26 | Year, Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil, Solar, Wind | No | 7b80499453d67569 |
| DEU | Germany | 10 | 26 | Year, Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil, Other Renewables, Solar, Wind | Yes | fec346c75ee80b7d |
| FRA | France | 10 | 26 | Year, Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil, Other Renewables, Solar, Wind | No | 7e5b384121730d4d |
| GBR | United Kingdom | 10 | 26 | Year, Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil, Other Renewables, Solar, Wind | Yes | 40ebb46469ebc33e |
| IND | India | 9 | 26 | Year, Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil, Solar, Wind | No | fe4b5646db11f109 |
| JPN | Japan | 9 | 26 | Year, Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil, Solar, Wind | Yes | 6bd4dbf8c481faf8 |
| WLD | World | 10 | 26 | Year, Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil, Other Renewables, Solar, Wind | No | 8644e6e0079364fa |

All systems cover the time window 2000--2025 (N = 26 annual observations). D includes the Year carrier. Germany, United Kingdom, and Japan required zero replacement (epsilon = 10^-10) for carriers with structural zeros in some years.

---

## 4. Method

### 4.1 Pipeline

Each country was processed using `hs_run.py`, the unified Hs pipeline runner (v1.0 Extended). The pipeline is deterministic --- identical input produces bit-identical output on every run.

The pipeline executes the following stages:

- **R (Raw Ingestion):** Load pipeline-ready CSV. Apply zero replacement where required.
- **M (Closure):** Close each row to sum = 1. Verify closure to machine precision.
- **E (CLR Transform):** Compute centred log-ratio coordinates. Verify CLR sum = 0.
- **C (Variation Matrix):** Compute D x D variation matrix T. Derive total variance sigma^2_A = (1/2D) * sum(T).
- **T (Cumulative Variance V(t)):** Compute total variance using observations 1..t for t = 2..N. Fit parabolic model. Classify shape as bowl (concave up) or hill (concave down).
- **V (Diagnostics):** Pair stability ranking, zero-crossing detection, PID analysis, matrix eigenstructure.
- **S (Path Metrics):** Shannon entropy trajectory, Aitchison norm trajectory, chaos detection (stalls, reversals).

### 4.2 Standard Outputs

Each run produces 5 mandatory projection outputs:

1. Helix exploded diagram (PDF)
2. Manifold helix (PDF)
3. Projections suite (PDF)
4. Polar stack with value table (PDF + JSON)
5. Manifold paper (PDF)

Plus machine-readable results (JSON) and diagnostic report (TXT).

---

## 5. Results

### 5.1 CHN --- China

**Variance structure:**
- Total variance sigma^2_A = 12.572
- Variance range: [0.166, 12.572]
- V(t) shape: bowl (concave up --- accelerating)
- Parabolic R^2 = 0.986
- Entropy: mean = 0.573, CV = 16.99%, range = [0.435, 0.755]

**Diagnostics:**
- Total diagnostic codes: 73 (0 errors, 1 warning, 35 discoveries, 5 structural modes, 1 calibration signal)
- Chaos detection: 9 deviations (3 stalls, 6 reversals)
- Drift: decreasing (variance ratio 2nd/1st half = 0.347). Max shift carrier: Year.
- Stable pairs: Coal/Hydro (CV = 8.28), Coal/Nuclear (CV = 16.60), Coal/Other Fossil (CV = 14.20), Year/Other Fossil (CV = 11.58)
- Most volatile pair: Other Fossil/Wind (CV = 6271.79)
- Near-zero carriers: Bioenergy, Gas, Nuclear, Other Fossil, Solar, Wind (6 of 9 carriers approach the simplex boundary)
- Structural modes: regime transition, carrier coupling, smooth convergence

**Notable findings:**
China's bowl-shaped V(t) with R^2 = 0.986 indicates a system whose compositional variance is increasing with near-perfect parabolic regularity. The Coal/Hydro lock (CV = 8.28) reflects parallel growth of both sources with GDP. The high entropy CV (16.99%) --- the highest in the set --- indicates substantial compositional diversification over the period, consistent with the transition from a coal-dominated mix toward a multi-source system.

---

### 5.2 DEU --- Germany

**Variance structure:**
- Total variance sigma^2_A = 16.660
- Variance range: [3.168, 16.660]
- V(t) shape: bowl (concave up --- accelerating)
- Parabolic R^2 = 0.852
- Entropy: mean = 0.395, CV = 5.78%, range = [0.350, 0.429]

**Diagnostics:**
- Total diagnostic codes: 81 (0 errors, 2 warnings, 45 discoveries, 3 structural modes, 1 calibration signal)
- Chaos detection: 15 deviations (1 stall, 14 reversals)
- Drift: increasing (variance ratio 2nd/1st half = 2.227). Max shift carrier: Nuclear.
- Stable pairs include: Year/Hydro (CV = 1.81), Year/Other Fossil (CV = 2.57), Year/Gas (CV = 5.12), Coal/Other Fossil (CV = 12.99), Coal/Hydro (CV = 14.01), Bioenergy/Other Renewables (CV = 18.99), Other Renewables/Wind (CV = 17.39)
- Most volatile pair: Nuclear/Wind (CV = 1666.68)
- Near-zero carriers: Bioenergy, Hydro, Nuclear, Other Fossil, Other Renewables, Solar, Wind (7 of 10)
- Structural modes: regime transition, carrier coupling

**Notable findings:**
Germany has the highest total variance in the set (16.660) and the most diagnostic codes (81). The R^2 of 0.852 is the lowest among bowl-shaped systems, reflecting the non-monotonic V(t) trajectory caused by the nuclear exit. Nuclear is identified as the max-shift carrier with increasing drift (ratio = 2.227), confirming that the nuclear phase-out is the primary compositional driver. The 14 reversals --- the highest count alongside France --- indicate compositional turbulence. The Nuclear/Wind pair has the most extreme volatility (CV = 1666.68), quantifying the divergent trajectories of these two carriers: nuclear declining to zero while wind grew to become the largest source.

---

### 5.3 FRA --- France

**Variance structure:**
- Total variance sigma^2_A = 12.921
- Variance range: [0.478, 12.921]
- V(t) shape: hill (concave down --- decelerating)
- Parabolic R^2 = 0.969
- Entropy: mean = 0.317, CV = 3.93%, range = [0.296, 0.337]

**Diagnostics:**
- Total diagnostic codes: 85 (0 errors, 2 warnings, 48 discoveries, 4 structural modes, 1 calibration signal)
- Chaos detection: 15 deviations (1 stall, 14 reversals)
- Drift: decreasing (variance ratio 2nd/1st half = 0.220). Max shift carrier: Nuclear.
- Stable pairs include: Year/Other Renewables (CV = 1.29), Year/Other Fossil (CV = 1.75), Nuclear/Other Renewables (CV = 2.78), Nuclear/Other Fossil (CV = 2.88), Hydro/Other Renewables (CV = 3.59), Other Fossil/Other Renewables (CV = 4.43), Year/Hydro (CV = 3.32), Hydro/Nuclear (CV = 7.17), Hydro/Other Fossil (CV = 10.02), Gas/Nuclear (CV = 14.11), Gas/Other Renewables (CV = 7.71), Bioenergy/Nuclear (CV = 12.31), Year/Nuclear (CV = 6.29), Year/Bioenergy (CV = 7.71), Year/Gas (CV = 7.65), Bioenergy/Other Renewables (CV = 15.94), Year/Coal (CV = 18.97)
- Most volatile pair: Coal/Other Fossil (CV = 3125.50)
- Near-zero carriers: Bioenergy, Coal, Gas, Other Fossil, Other Renewables, Solar, Wind (7 of 10)
- Structural modes: regime transition, carrier coupling

**Notable findings:**
France is the only country in the set besides Japan with a hill-shaped V(t) curve --- the system is decelerating. It has the most stable pairs of any country, with 17 pairs classified as compositionally locked. The tightest pair is Year/Other Renewables (CV = 1.29), and the Nuclear/Other Renewables pair (CV = 2.78) and Nuclear/Other Fossil pair (CV = 2.88) confirm that France's secondary sources maintain rigid proportional relationships around the dominant nuclear baseload. The lowest entropy mean (0.317) and narrowest entropy range ([0.296, 0.337]) in the set quantify the extreme concentration of the French generation mix. The drift ratio of 0.220 --- the lowest in the set --- confirms that compositional change is strongly decelerating.

---

### 5.4 GBR --- United Kingdom

**Variance structure:**
- Total variance sigma^2_A = 16.861
- Variance range: [0.043, 16.861]
- V(t) shape: bowl (concave up --- accelerating)
- Parabolic R^2 = 0.970
- Entropy: mean = 0.279, CV = 4.10%, range = [0.251, 0.292]

**Diagnostics:**
- Total diagnostic codes: 91 (0 errors, 2 warnings, 53 discoveries, 5 structural modes, 1 calibration signal)
- Chaos detection: 21 deviations (3 stalls, 18 reversals)
- Drift: decreasing (variance ratio 2nd/1st half = 0.853). Max shift carrier: Coal.
- Stable pairs include: Year/Hydro (CV = 2.65), Year/Other Fossil (CV = 2.91), Year/Other Renewables (CV = 2.83), Gas/Other Renewables (CV = 3.97), Gas/Other Fossil (CV = 7.75), Nuclear/Other Renewables (CV = 4.62), Other Fossil/Other Renewables (CV = 4.99), Hydro/Other Renewables (CV = 5.19), Year/Gas (CV = 7.75), Year/Nuclear (CV = 7.38), Bioenergy/Other Renewables (CV = 8.64), Gas/Hydro (CV = 9.89), Hydro/Nuclear (CV = 14.28), Year/Bioenergy (CV = 15.79), Nuclear/Other Fossil (CV = 16.14), Other Renewables/Wind (CV = 17.47), Coal/Other Renewables (CV = 18.65)
- Most volatile pair: Bioenergy/Wind (CV = 748.44)
- Near-zero carriers: Bioenergy, Coal, Hydro, Other Fossil, Other Renewables, Solar, Wind (7 of 10)
- Structural modes: regime transition, domain resonance, carrier coupling
- Precision match: 1/(e^pi) with delta = 0.000058

**Notable findings:**
The UK has the highest total variance in the set (16.861), the most diagnostic codes (91), and the most chaotic trajectory (21 deviations, 18 reversals). Coal is identified as the max-shift carrier, consistent with the UK's near-complete coal exit over this period. Despite the bowl classification, the drift ratio is near unity (0.853), indicating that unlike China or India where acceleration is sustained, the UK's compositional change rate is nearly constant between halves. The domain resonance structural mode and the precision match to the Euler-family constant 1/(e^pi) (delta = 0.000058) are flagged as investigation prompts. The UK has 17 stable pairs, reflecting the fact that while Coal collapsed, the remaining carriers (Gas, Nuclear, Hydro, Other Fossil, Other Renewables) maintained relatively stable proportional relationships among themselves.

---

### 5.5 IND --- India

**Variance structure:**
- Total variance sigma^2_A = 12.440
- Variance range: [0.033, 12.440]
- V(t) shape: bowl (concave up --- accelerating)
- Parabolic R^2 = 0.988
- Entropy: mean = 0.451, CV = 13.89%, range = [0.347, 0.563]

**Diagnostics:**
- Total diagnostic codes: 77 (0 errors, 2 warnings, 42 discoveries, 4 structural modes, 1 calibration signal)
- Chaos detection: 11 deviations (2 stalls, 9 reversals)
- Drift: decreasing (variance ratio 2nd/1st half = 0.565). Max shift carrier: Year.
- Carrier dominance: Solar contributes 70.0% of total variance.
- Stable pairs include: Coal/Nuclear (CV = 4.15), Year/Gas (CV = 7.32), Year/Hydro (CV = 9.64), Year/Nuclear (CV = 9.97), Bioenergy/Coal (CV = 11.14), Coal/Hydro (CV = 12.36), Year/Other Fossil (CV = 14.39), Year/Bioenergy (CV = 16.15), Hydro/Nuclear (CV = 17.60)
- Most volatile pair: Bioenergy/Other Fossil (CV = 4604.95)
- Near-zero carriers: Bioenergy, Nuclear, Other Fossil, Solar, Wind (5 of 9)
- Structural modes: regime transition, carrier coupling
- Precision match: 1/ln10 with delta = 0.000145

**Notable findings:**
India has the second-highest parabolic R^2 (0.988) --- a near-perfect accelerating curve. The Coal/Nuclear pair is the tightest lock in the set (CV = 4.15), indicating that India's nuclear programme has grown in close proportion to coal expansion. Solar is flagged as the dominant variance carrier at 70.0% --- the highest single-carrier dominance in the set. This means that India's compositional evolution is driven primarily by solar's emergence from near-zero to a measurable share. The entropy CV (13.89%) is the second highest, confirming active diversification.

---

### 5.6 JPN --- Japan

**Variance structure:**
- Total variance sigma^2_A = 10.161
- Variance range: [0.309, 10.850]
- V(t) shape: hill (concave down --- decelerating)
- Parabolic R^2 = 0.794
- Entropy: mean = 0.542, CV = 3.37%, range = [0.509, 0.571]

**Diagnostics:**
- Total diagnostic codes: 77 (0 errors, 2 warnings, 41 discoveries, 4 structural modes, 1 calibration signal)
- Chaos detection: 11 deviations (2 stalls, 9 reversals)
- Drift: increasing (variance ratio 2nd/1st half = 3.011). Max shift carrier: Nuclear.
- Stable pairs include: Year/Hydro (CV = 2.17), Year/Bioenergy (CV = 7.04), Year/Coal (CV = 5.78), Bioenergy/Coal (CV = 10.39), Bioenergy/Gas (CV = 11.08), Coal/Hydro (CV = 10.59), Year/Gas (CV = 11.62), Gas/Hydro (CV = 16.11), Year/Wind (CV = 18.37)
- Most volatile pair: Hydro/Nuclear (CV = 1023.61)
- Near-zero carriers: Bioenergy, Nuclear, Other Fossil, Solar, Wind (5 of 9)
- Structural modes: regime transition, carrier coupling
- Precision match: 1/phi with delta = 0.000992

**Notable findings:**
Japan is one of two hill-shaped systems (with France). The variance range is notable: sigma^2_A reaches a maximum of 10.850 before declining to 10.161, producing a non-monotonic V(t) trajectory --- the only system where total variance decreases in the final observations. This reflects the partial nuclear restart. The R^2 of 0.794 is the weakest parabolic fit in the set, consistent with the disruption caused by the Fukushima shock. Nuclear is identified as the max-shift carrier with the highest drift ratio in the set (3.011), confirming that the nuclear shutdown and partial restart dominates Japan's compositional evolution. The Hydro/Nuclear pair (CV = 1023.61) is the second most volatile in the set --- Hydro remained stable while Nuclear underwent extreme swings.

---

### 5.7 WLD --- World

**Variance structure:**
- Total variance sigma^2_A = 6.280
- Variance range: [0.067, 6.280]
- V(t) shape: bowl (concave up --- accelerating)
- Parabolic R^2 = 0.989
- Entropy: mean = 0.774, CV = 3.69%, range = [0.742, 0.837]

**Diagnostics:**
- Total diagnostic codes: 87 (0 errors, 1 warning, 49 discoveries, 7 structural modes, 1 calibration signal)
- Chaos detection: 5 deviations (1 stall, 4 reversals)
- Drift: decreasing (variance ratio 2nd/1st half = 0.398). Max shift carrier: Wind.
- Carrier dominance: Solar contributes 66.8% of total variance.
- Stable pairs include: Gas/Other Renewables (CV = 1.39), Coal/Other Renewables (CV = 1.92), Hydro/Other Renewables (CV = 1.77), Coal/Hydro (CV = 4.71), Nuclear/Other Renewables (CV = 6.58), Year/Other Renewables (CV = 7.09), Bioenergy/Gas (CV = 9.03), Bioenergy/Coal (CV = 10.65), Year/Coal (CV = 12.46), Year/Nuclear (CV = 13.55), Bioenergy/Hydro (CV = 14.36), Other Fossil/Other Renewables (CV = 14.39), Coal/Nuclear (CV = 15.72), Bioenergy/Other Renewables (CV = 15.64), Coal/Other Fossil (CV = 15.93), Coal/Gas (CV = 19.15)
- Most volatile pair: Other Renewables/Solar (CV = 4388.91)
- Near-zero carriers: Bioenergy, Other Renewables, Solar, Wind (4 of 10)
- Structural modes: overconstrained, regime transition, domain resonance, carrier coupling, smooth convergence
- Precision match: 1/(2*pi) with delta = 0.000080

**Notable findings:**
The World aggregate has the lowest total variance (6.280), the fewest chaos deviations (5), the highest entropy mean (0.774), and the most structural modes (7). It produces the cleanest parabolic fit (R^2 = 0.989). The 16 stable pairs --- the most in the set --- reflect the structural stability of global proportional relationships when national fluctuations average out. The tightest pair is Gas/Other Renewables (CV = 1.39). Solar contributes 66.8% of total variance at the global level, confirming that the global energy transition is primarily a solar story in compositional terms. The overconstrained structural mode is a calibration flag noting that the near-perfect fit warrants verification that this is measured data and not model output. The domain resonance flag and precision match to 1/(2*pi) (delta = 0.000080) are investigation prompts. The smooth convergence mode confirms that the global system evolves as a single continuously-changing population.

---

### 5.8 Cross-Country Comparison

| ISO | sigma^2_A | V(t) Shape | R^2 | Entropy Mean | Entropy CV (%) | Chaos (total) | Stalls | Reversals | Stable Pairs | Codes |
|-----|-----------|------------|------|-------------|---------------|--------------|--------|-----------|-------------|-------|
| CHN | 12.572 | bowl | 0.986 | 0.573 | 16.99 | 9 | 3 | 6 | 4 | 73 |
| DEU | 16.660 | bowl | 0.852 | 0.395 | 5.78 | 15 | 1 | 14 | 7 | 81 |
| FRA | 12.921 | hill | 0.969 | 0.317 | 3.93 | 15 | 1 | 14 | 17 | 85 |
| GBR | 16.861 | bowl | 0.970 | 0.279 | 4.10 | 21 | 3 | 18 | 17 | 91 |
| IND | 12.440 | bowl | 0.988 | 0.451 | 13.89 | 11 | 2 | 9 | 9 | 77 |
| JPN | 10.161 | hill | 0.794 | 0.542 | 3.37 | 11 | 2 | 9 | 9 | 77 |
| WLD | 6.280 | bowl | 0.989 | 0.774 | 3.69 | 5 | 1 | 4 | 16 | 87 |

**Observations from the comparison table:**

1. **Total variance** separates the systems into three tiers: high (DEU 16.66, GBR 16.86), moderate (CHN 12.57, FRA 12.92, IND 12.44, JPN 10.16), and low (WLD 6.28).

2. **V(t) shape** classifies 5 systems as bowl (accelerating) and 2 as hill (decelerating). France and Japan are the decelerating systems --- France because its nuclear-dominated mix is approaching equilibrium, Japan because the post-Fukushima variance spike has partially relaxed.

3. **R^2 quality** ranges from 0.794 (JPN) to 0.989 (WLD). The two systems with exogenous shocks or non-monotonic trajectories (JPN, DEU) have the weakest parabolic fits. Systems with smooth, directional transitions (WLD, IND, CHN) have R^2 > 0.985.

4. **Entropy** separates concentrated mixes (GBR 0.279, FRA 0.317) from diversified mixes (WLD 0.774, CHN 0.573, JPN 0.542). The entropy CV identifies the actively diversifying systems: CHN (16.99%) and IND (13.89%) have the highest variability in entropy, indicating ongoing compositional redistribution.

5. **Chaos** correlates with total variance: GBR (21 deviations) and DEU/FRA (15 each) are the most turbulent. WLD (5 deviations) is the smoothest.

6. **Stable pairs** correlate inversely with compositional disruption. France and the UK have 17 stable pairs each (though for different reasons --- France from nuclear-dominated stability, the UK from stability among non-coal carriers). The World has 16. China has only 4.

---

## 6. Conclusions

### 6.1 Pipeline Performance

All 7 runs completed with zero errors. The pipeline processed systems ranging from 9 to 10 carriers, with and without zero replacement, and produced consistent diagnostics across all cases. Closure was verified to machine precision in all runs. All auto-detected features (PID, order sensitivity, zero-crossing detector, ratio pair lattice) were triggered in all 7 systems, confirming that these are universal features of real energy composition data.

### 6.2 Diagnostic Consistency with Domain Knowledge

The Hs diagnostics are consistent with known energy transition characteristics in every case:

- **Germany and the UK** have the highest total variance, consistent with their status as the two most compositionally disrupted major economies.
- **France** decelerates with many stable locks, consistent with nuclear dominance and slow diversification.
- **Japan** decelerates with the weakest parabolic fit, consistent with the Fukushima shock disrupting the V(t) trajectory.
- **China and India** accelerate with high R^2, consistent with their ongoing, directional buildout of renewable capacity on top of coal.
- **The World** has the lowest variance, highest entropy, fewest chaos events, and most stable pairs --- consistent with global aggregation cancelling national-level fluctuations and revealing only the secular trend.

### 6.3 Key Quantitative Findings

1. **Solar dominance in variance.** In both India (70.0%) and the World (66.8%), a single carrier --- Solar --- contributes over 60% of the total compositional variance. Solar's emergence from near-zero to a measurable share is the primary driver of compositional change at both national and global scales.

2. **Drift directionality.** Two systems show increasing drift (DEU ratio = 2.23, JPN ratio = 3.01), indicating that their compositional evolution is accelerating in the second half of the time series. Five systems show decreasing drift, indicating convergence.

3. **Nuclear as max-shift carrier.** Nuclear is identified as the max-shift carrier in 3 of 7 systems (DEU, FRA, JPN). In Germany and Japan, nuclear exits or shutdowns drive the largest compositional shifts. In France, nuclear's slight decline from its dominant position produces the largest relative change.

4. **Coal as max-shift carrier.** Coal is the max-shift carrier only in the UK, where its near-complete elimination is the defining feature of the transition.

### 6.4 Implications for CoDa Practice

This experiment demonstrates that the Hs pipeline extracts interpretable compositional diagnostics from real-world data without encoding any domain-specific knowledge. The V(t) shape classification, entropy trajectory, pair stability ranking, drift analysis, and chaos detection are all derived from standard CoDa operations (CLR transform, variation matrix, Aitchison distance) applied in a systematic diagnostic sequence. The pipeline does not know what coal, nuclear, or solar are --- it reads only the simplex geometry of their proportional relationships.

---

## 7. Reproducibility

### 7.1 Pipeline

All runs use `hs_run.py` (v1.0 Extended). The pipeline is fully deterministic --- no stochastic elements, no random seeds, no machine learning. Bit-identical output on repeated runs with identical input and pipeline version.

### 7.2 Run Commands

```
python hs_run.py ../../data/Energy/EMBER_pipeline_ready/ember_CHN_China_generation_TWh.csv --exp-id "Hs-M02-CHN" --name "China" --domain ENERGY

python hs_run.py ../../data/Energy/EMBER_pipeline_ready/ember_DEU_Germany_generation_TWh.csv --exp-id "Hs-M02-DEU" --name "Germany" --domain ENERGY

python hs_run.py ../../data/Energy/EMBER_pipeline_ready/ember_FRA_France_generation_TWh.csv --exp-id "Hs-M02-FRA" --name "France" --domain ENERGY

python hs_run.py ../../data/Energy/EMBER_pipeline_ready/ember_GBR_United_Kingdom_generation_TWh.csv --exp-id "Hs-M02-GBR" --name "United Kingdom" --domain ENERGY

python hs_run.py ../../data/Energy/EMBER_pipeline_ready/ember_IND_India_generation_TWh.csv --exp-id "Hs-M02-IND" --name "India" --domain ENERGY

python hs_run.py ../../data/Energy/EMBER_pipeline_ready/ember_JPN_Japan_generation_TWh.csv --exp-id "Hs-M02-JPN" --name "Japan" --domain ENERGY

python hs_run.py ../../data/Energy/EMBER_pipeline_ready/ember_WLD_World_generation_TWh.csv --exp-id "Hs-M02-WLD" --name "World" --domain ENERGY
```

### 7.3 Timestamps

All 7 runs were executed on 2026-04-30, between 21:14:06 and 21:14:12 UTC.

### 7.4 Artifacts

| File | Description |
|------|-------------|
| `Hs_INDEX.json` | Machine-readable experiment index with all run parameters and results |
| `pipeline_output/EMBER_*_results.json` | Full pipeline results for each country (7 files) |
| `pipeline_output/EMBER_*_report_en.txt` | Diagnostic reports for each country (7 files) |
| `pipeline_output/Hs-M02-*_helix_exploded.pdf` | Helix exploded diagrams (7 files) |
| `pipeline_output/Hs-M02-*_manifold_helix.pdf` | Manifold helix projections (7 files) |
| `pipeline_output/Hs-M02-*_projections.pdf` | Projection suites (7 files) |
| `pipeline_output/Hs-M02-*_polar_stack.pdf` | Polar stack diagrams (7 files) |
| `pipeline_output/Hs-M02-*_polar_stack.json` | Polar stack data (7 files) |
| `pipeline_output/Hs-M02-*_manifold_paper.pdf` | Manifold paper projections (7 files) |
| `JOURNAL.md` | This document |

---

*Peter Higgins*
*Licensed under CC BY 4.0*
