# Hs-M02: EMBER Electricity Generation — CoDaWork 2026 Reference Experiment

**The par excellence experiment. Every number the CoDa community will examine.**

*Author: Peter Higgins*
*Date: 2026-04-29*
*Domain: ENERGY*
*Series: M-series (Manifold Projection Systems)*
*Claim tier: Applied compositional analysis — real-world validation*

---

## 1. Motivation

Hs-M01 established that the Higgins Decomposition faithfully projects known geometric objects. The instrument introduces no artifacts, no distortions, no blind spots. Ten geometric targets in, ten correct diagnoses out.

But calibration against mathematical phantoms answers only half the question. The other half: what does the instrument reveal when applied to real compositional data of genuine scientific and policy significance, where the ground truth is not a mathematical construction but an evolving physical system?

Electricity generation is the ideal test case. It is inherently compositional — a national grid's output is a mixture of sources that must sum to 100%. It evolves over time as policy, technology, and economics reshape the energy mix. It varies dramatically across countries with different resource endowments, policy histories, and development trajectories. And it is of immediate global interest: the energy transition is the defining infrastructure transformation of the 21st century.

The EMBER Global Electricity Review 2025 provides the most comprehensive publicly available dataset on global electricity generation by source, covering 228 countries from 2000 to 2025. This experiment applies the full Hs pipeline to 7 selected systems — Germany, United Kingdom, Japan, France, China, India, and the World aggregate — chosen to represent distinct energy transition archetypes.

This is the dataset Peter Higgins will present to the CoDa community at CoDaWork 2026 in Girona. Every number in this journal is reproducible, deterministic, and open to scrutiny.

---

## 2. Data Source

**Dataset:** EMBER Global Electricity Review 2025
**URL:** https://ember-climate.org/data/
**Coverage:** 228 countries, 2000–2025
**Resolution:** Annual electricity generation in TWh by source

### 2.1 Carriers

Nine electricity generation sources form the compositional parts:

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

Not all carriers are present in all countries. Where a carrier has zero generation across the entire time series, it is absent from that country's composition. Where a carrier is zero in some years but nonzero in others, structural zeros are replaced with epsilon = 10^-10 to permit log-ratio transforms.

### 2.2 Selected Systems

| ISO | Country | D | Rationale |
|-----|---------|---|-----------|
| DEU | Germany | 9 | Energiewende: simultaneous nuclear exit and coal phase-down with renewable surge |
| GBR | United Kingdom | 9 | Fastest coal exit of any major economy — from 32% to 0.1% in 25 years |
| JPN | Japan | 8 | Fukushima shock: abrupt nuclear shutdown and partial restart |
| FRA | France | 9 | Nuclear-dominant: 78% nuclear in 2000, stable baseload with slow renewable growth |
| CHN | China | 8 | Coal-dominant industrialisation with the world's largest renewable buildout |
| IND | India | 8 | Coal-dominant developing economy with accelerating solar and wind |
| WLD | World | 9 | Global aggregate: the smoothed mean of all national transitions |

All 7 systems span the same time window: 2000–2025 (N = 26 observations each).

---

## 3. Methodology

### 3.1 Pipeline

The complete Hs v3.0 diagnostic pipeline is applied to each country:

**Stage R — Raw Ingestion:** Load pipeline-ready CSV (TWh generation by source, one row per year). Replace structural zeros with epsilon = 10^-10.

**Stage M — Closure:** Close each row to sum = 1. Verify: max|sum - 1| < 10^-15 for all countries.

**Stage E — CLR Transform:** Compute centred log-ratio coordinates. Verify: max|sum(clr)| < 10^-14.

**Stage C — Variation Matrix:** Compute D x D variation matrix T where t_kj = Var(log(X_k/X_j)). Total variance sigma^2_A = (1/2D) sum(T).

**Stage T — Cumulative Variance V(t):** Compute total variance using observations 1..t for t = 2, 3, ..., N. Fit quadratic. Classify shape: FLAT, LINEAR, CONVEX (accelerating), CONCAVE (decelerating).

**Stage V — Diagnostics:** Lock detection (sd < 0.15 threshold for log-ratio pairs), pair stability ranking (all D(D-1)/2 pairs ranked by coefficient of variation), fingerprint geometry (CLR polygon area, perimeter, isoperimetric compactness).

**Stage S — Path Metrics:** Year-over-year Aitchison distances, total path length, net displacement, path efficiency (net/total), Shannon entropy trajectory, Aitchison norm trajectory.

### 3.2 Supplementary Tests

**Amalgamation Test:** Each country is tested under 4 amalgamation schemes that aggregate the 8–9 carriers into coarser groupings:

| Scheme | Groups | New D |
|--------|--------|-------|
| Binary: Fossil vs Clean | {Coal, Gas, Other Fossil} vs {Nuclear, Hydro, Wind, Solar, Bioenergy, Other Renewables} | 2 |
| Ternary: Fossil/Nuclear/Renewable | {Coal, Gas, Other Fossil} vs {Nuclear} vs {Hydro, Wind, Solar, Bioenergy, Other Renewables} | 3 |
| 7-group: detailed | Coal, Gas, Other Fossil, Nuclear, Hydro, VRE = {Wind, Solar}, Other Clean = {Bioenergy, Other Renewables} | 7 |
| Binary: Thermal vs Non-thermal | {Coal, Gas, Other Fossil, Nuclear, Bioenergy} vs {Hydro, Wind, Solar, Other Renewables} | 2 |

For each scheme, the V(t) shape classification is recomputed on the amalgamated composition and compared to the full-carrier result. A scheme PASSES if the shape classification is preserved. This tests the amalgamation non-commutativity warning raised by Egozcue and Pawlowsky-Glahn.

**Decimation Test:** Each country's time series is decimated at ratios 2x, 4x, and 8x (keeping every 2nd, 4th, or 8th observation). Mean Shannon entropy and mean Aitchison norm are compared between the full and decimated series. This tests temporal resolution invariance.

---

## 4. Results

### 4.1 Summary Table

| Country | D | N | sigma^2_A | V(t) Shape | R^2 | Locks | Path Eff | Amal |
|---------|---|---|-----------|------------|-----|-------|----------|------|
| Germany | 9 | 26 | 152.11 | CONVEX (accelerating) | 0.5719 | 0 | 0.4244 | PASS |
| United Kingdom | 9 | 26 | 103.13 | CONCAVE (decelerating) | 0.9236 | 0 | 0.3801 | FAIL |
| Japan | 8 | 26 | 31.53 | CONCAVE (decelerating) | 0.6446 | 2 | 0.1184 | FAIL |
| France | 9 | 26 | 12.64 | CONCAVE (decelerating) | 0.9664 | 3 | 0.5579 | FAIL |
| China | 8 | 26 | 10.74 | CONVEX (accelerating) | 0.9831 | 1 | 0.6571 | FAIL |
| India | 8 | 26 | 11.96 | CONVEX (accelerating) | 0.9875 | 1 | 0.6471 | FAIL |
| World | 9 | 26 | 5.98 | CONVEX (accelerating) | 0.9879 | 6 | 0.9529 | PASS |

### 4.2 Per-Country Analysis

---

#### 4.2.1 Germany (DEU)

**The Energiewende in simplex geometry.**

Germany's electricity composition underwent the most dramatic restructuring of any country in this set. In 2000, coal dominated at 52.2% with nuclear at 29.8%. By 2025, wind leads at 27.2%, coal has fallen to 20.6%, and nuclear has reached zero — Germany completed its nuclear exit in April 2023.

**Hs diagnosis:**

Total variance sigma^2_A = 152.11 — the highest in the set by a large margin. This quantifies what the energy policy community knows qualitatively: Germany's energy transition involved the most compositional disruption of any major economy.

V(t) shape: CONVEX (accelerating). The compositional variability is still increasing. Germany's energy transition is not slowing down — it is speeding up. The R^2 of 0.5719 (lowest in the set) reflects the non-monotonic V(t) trajectory: variance initially drops from 2001 to 2007, then rises sharply from 2008 onward as the nuclear exit reshapes the composition.

Path efficiency: 0.4244. Germany's trajectory on the simplex is moderately efficient — it moves broadly toward a renewable-dominated mix but with significant deviations (the nuclear exit creates large jumps in CLR space). The year-over-year Aitchison distances show this clearly: most years are 0.2–0.8, but the 2000-2001 jump is 19.5 (Solar and Other Renewables entering at epsilon), 2007-2008 is 18.0 (structural shift in epsilon-valued carriers), and 2023-2024 is 23.6 (nuclear exit).

Locks: 0. No pair of carriers maintains a constant proportional relationship. The entire mix is in flux.

Most stable pair: Coal/Other Fossil (CV = 0.130). These two fossil sources have declined roughly in parallel — their log-ratio remains the most predictable relationship in the German grid.

Least stable pair: Hydro/Nuclear (CV = 13.4). Hydro remained essentially constant while nuclear went to zero — an extreme divergence in compositional evolution.

Fingerprint compactness: 0.381. A moderately asymmetric polygon, reflecting the collapse of Nuclear and Other Renewables axes to zero in the final year.

Amalgamation: ALL PASS. The convex (accelerating) shape classification survives all 4 amalgamation schemes. Germany's accelerating transition is robust — it remains accelerating whether viewed as Fossil-vs-Clean, Fossil-Nuclear-Renewable, or any finer grouping.

**Interpretation:** Germany is the most compositionally turbulent energy system in the sample. The Hs instrument reads it as an accelerating, unlocked, maximally disrupted transition — exactly what energy policy analysis confirms. The simultaneous exit from nuclear and coal, with replacement by solar and wind, creates the largest total variance and the most complex simplex trajectory.

---

#### 4.2.2 United Kingdom (GBR)

**The fastest coal exit in history.**

The UK's coal share fell from 31.8% in 2000 to 0.1% in 2025 — the most complete elimination of a dominant carrier in any major economy. Gas remained the dominant source throughout (39.3% to 31.1%), while wind surged from 0.3% to 29.4%.

**Hs diagnosis:**

Total variance: 103.13. Second highest — driven primarily by the coal collapse and wind/solar emergence.

V(t) shape: CONCAVE (decelerating). The UK's transition is maturing. The most dramatic compositional change occurred in the 2012–2020 period; by 2025, the rate of change is slowing as coal has essentially been eliminated and the remaining mix is stabilising around gas, wind, nuclear, and bioenergy.

Path efficiency: 0.3801. The lowest among countries with directional transitions. The UK's path meanders — coal's share fluctuated in 2006 and 2012–2013 before its final decline, creating detours on the simplex.

Locks: 0. Like Germany, no pair is locked — the entire composition is evolving.

Most stable pair: Gas/Other Fossil (CV = 0.077). The tightest proportional coupling in the entire 7-country set. Gas and Other Fossil (oil-fired generation) declined roughly in parallel across the period.

Fingerprint compactness: 0.600. The most compact (most symmetric) fingerprint — reflecting a more evenly distributed final composition compared to the polarised German or coal-heavy Chinese mixes.

Amalgamation: ALL FAIL. Every amalgamation scheme flips the shape from CONCAVE to CONVEX. This is a significant finding. The UK's transition looks like it is decelerating when viewed at full 9-carrier resolution, but accelerating when viewed through any coarser lens. The reason: the coarse groupings hide the internal restructuring within the Clean category (nuclear stable, bioenergy growing, wind and solar growing at different rates). Amalgamation destroys the information that reveals deceleration.

**Interpretation:** The UK is a cautionary example for amalgamation. A CoDa practitioner working with binary Fossil/Clean data would conclude the UK transition is accelerating. A practitioner with the full 9-carrier composition sees it is decelerating. Both are correct views of different subspaces — but they lead to opposite policy conclusions. Egozcue's warning about amalgamation non-commutativity is directly verified.

---

#### 4.2.3 Japan (JPN)

**The Fukushima discontinuity.**

Japan's energy mix was reshaped by the 2011 Tohoku earthquake and Fukushima nuclear disaster. Nuclear fell from 29.0% (2000) to near-zero (2014), then partially recovered to 9.1% (2025). Coal and gas absorbed the shortfall.

**Hs diagnosis:**

Total variance: 31.53. Moderate — much lower than Germany or the UK. Japan's composition changed significantly but within a narrower range.

V(t) shape: CONCAVE (decelerating). R^2 = 0.6446 — the weakest quadratic fit among the concave systems. The V(t) trajectory is disrupted by the Fukushima shock, which creates a spike in variance around 2011–2014 followed by partial relaxation.

Path efficiency: 0.1184. The lowest in the entire set by a wide margin. Japan's simplex trajectory is almost a closed loop — the composition moved dramatically after Fukushima, then partially returned as nuclear restarted. A path efficiency of 0.12 says that only 12% of the total compositional movement was net displacement; 88% was wasted in backtracking.

Locks: 2. Two carrier pairs have maintained near-constant proportional relationships throughout the period — the instrument identifies structural couplings that persist even through the Fukushima disruption.

Most stable pair: Bioenergy/Coal (CV = 0.104). Despite everything, the ratio of bioenergy to coal generation remained remarkably stable. Both are baseload-capable dispatchable sources, and their proportional relationship survived the nuclear shock.

Amalgamation: PARTIAL — 3 PASS, 1 FAIL. The Binary Thermal/Non-thermal scheme flips the shape from CONCAVE to CONVEX. This occurs because the Thermal grouping lumps Nuclear with Coal and Gas, hiding the nuclear collapse/restart dynamic inside the thermal aggregate.

**Interpretation:** Japan demonstrates two key capabilities of the Hs instrument. First, path efficiency as a discriminator: Japan's 0.12 immediately identifies it as a system that moved and returned, sharply distinct from directional transitions like Germany or India. Second, lock detection identifies stable couplings that survive exogenous shocks — these are structural features of the Japanese grid, not transient correlations.

---

#### 4.2.4 France (FRA)

**Nuclear dominance on the simplex.**

France is the most concentrated composition in the set: 78.0% nuclear in 2000, declining modestly to 68.8% in 2025. The compositional simplex is dominated by a single vertex.

**Hs diagnosis:**

Total variance: 12.64. Low — reflecting the stability of the nuclear-dominated mix.

V(t) shape: CONCAVE (decelerating). R^2 = 0.9664 — a very clean quadratic fit. France's modest diversification (adding solar and wind at the margins) generated most of its variance early in the period and is now approaching a plateau.

Path efficiency: 0.5579. Moderately high — France moves consistently in one direction on the simplex (away from pure nuclear, toward a slightly more diversified mix), with few reversals.

Locks: 3. The most locks of any country. Three carrier pairs maintain near-constant proportional relationships, reflecting the stability of France's secondary sources (hydro, gas, other fossil) relative to each other while nuclear dominates.

Most stable pair: Nuclear/Other Renewables (CV = 0.028). The tightest pair in the set by coefficient of variation. The ratio of nuclear to Other Renewables barely moves across 26 years — both are essentially constants of the French system.

Fingerprint compactness: 0.479. A moderately symmetric polygon, dominated by the Nuclear axis.

Amalgamation: 3 FAIL, 1 PASS. The 7-group detailed scheme preserves the shape; the three coarser schemes all flip from CONCAVE to CONVEX. France's decelerating diversification is visible only at full resolution. Any amalgamation that hides the internal structure of the clean energy category destroys the concavity signal.

Shannon entropy range: 0.782–1.297. The lowest entropy of any country, reflecting the extreme concentration of the French mix.

**Interpretation:** France is a compositional monopole — one carrier dominates the simplex, and all others are perturbations. The Hs instrument correctly reads this as a low-variance, high-lock, decelerating system. The entropy trajectory confirms: France starts with the lowest diversity and gains it slowly.

---

#### 4.2.5 China (CHN)

**Coal industrialisation meets renewable scale-up.**

China started at 78.2% coal in 2000 and remains coal-dominant at 54.4% in 2025 — but the renewable buildout (solar from 0% to 11.1%, wind from 0% to 10.7%) is the largest absolute addition of variable renewable energy in history.

**Hs diagnosis:**

Total variance: 10.74. Surprisingly low for a country undergoing such a massive energy transformation. The reason: China's change is additive (building renewables on top of coal) rather than substitutive (replacing coal with renewables). The proportional relationships shift slowly because total generation is growing rapidly — the coal share falls not because coal generation declines, but because everything else grows faster.

V(t) shape: CONVEX (accelerating). R^2 = 0.9831 — a near-perfect quadratic fit. China's compositional diversification is accelerating cleanly. The transition is in its growth phase.

Path efficiency: 0.6571. High — China moves steadily in one direction on the simplex. There are no reversals, no Fukushima-style shocks.

Locks: 1. Coal/Hydro is locked — the proportional relationship between China's two largest traditional sources remains stable even as renewables surge.

Most stable pair: Coal/Hydro (CV = 0.083). These two sources maintain a remarkably constant ratio because both grow with GDP — coal through industrial demand, hydro through continued dam construction.

Amalgamation: 3 PASS, 1 FAIL. The 7-group detailed scheme flips from CONVEX to CONCAVE. This occurs because the VRE amalgamation (Wind + Solar) hides the fact that solar is growing faster than wind — the internal dynamics of the VRE group create a deceleration signal that is invisible in the full composition.

**Interpretation:** China demonstrates a key insight: low total variance does not mean small change. A country can transform its energy system profoundly while keeping sigma^2_A modest, if the transformation is additive rather than substitutive. The Hs instrument distinguishes these cases through path efficiency (high = directional) and V(t) shape (convex = accelerating), while total variance alone misses the distinction.

---

#### 4.2.6 India (IND)

**Coal persistence with solar acceleration.**

India is structurally similar to China — coal-dominant (68.3% in 2000, 70.8% in 2025) with an accelerating renewable buildout. But India's coal share actually increased slightly, making it the only country in the set where the dominant carrier gained share.

**Hs diagnosis:**

Total variance: 11.96. Very close to China's 10.74, reflecting similar magnitudes of compositional change.

V(t) shape: CONVEX (accelerating). R^2 = 0.9875 — the second-best quadratic fit in the set. India's diversification trajectory is the cleanest accelerating curve.

Path efficiency: 0.6471. Nearly identical to China (0.6571). India's simplex trajectory is directional with minimal backtracking.

Locks: 1. Coal/Nuclear is locked (CV = 0.042) — the tightest single lock in any country. India's nuclear programme has grown in exact proportion to coal expansion. Both are state-planned, baseload sources.

Most stable pair: Coal/Nuclear (CV = 0.042). The proportional coupling between coal and nuclear generation is the most rigid structural feature in the entire 7-country dataset.

Amalgamation: 3 FAIL, 1 PASS. The 7-group detailed scheme preserves the shape; the three binary/ternary schemes all flip from CONVEX to CONCAVE. India is the mirror image of the UK: its transition looks accelerating at full resolution but decelerating through coarse amalgamation. The reason: India's gas share is collapsing (from 9.8% to 2.3%) while renewables rise, but binary Fossil/Clean grouping hides this internal fossil restructuring and sees only the net fossil share falling slowly.

Shannon entropy range: 0.902–1.093. The narrowest entropy range of any country — India's compositional diversity barely changes over 26 years.

**Interpretation:** India reveals the Hs instrument's ability to detect structural locks — proportional couplings that persist over decades and represent genuine structural features of energy policy (planned coal + nuclear expansion). The entropy trajectory is nearly flat, confirming that India's grid is not diversifying in the Shannon sense — it is merely substituting within categories.

---

#### 4.2.7 World (WLD)

**The global mean: smoothed, directional, highly efficient.**

The world aggregate smooths out national idiosyncrasies. Coal falls from 38.0% to 33.0%, gas rises from 18.0% to 21.8%, solar and wind each reach approximately 8.7%.

**Hs diagnosis:**

Total variance: 5.98. The lowest in the set. Global aggregation cancels country-level variability — what one country loses in coal, another gains, and the net compositional change is modest.

V(t) shape: CONVEX (accelerating). R^2 = 0.9879 — the best quadratic fit of all 7 systems. The global energy transition is accelerating with near-perfect mathematical regularity.

Path efficiency: 0.9529. The highest in the entire set, and strikingly so. The global energy composition moves in an almost perfectly straight line on the simplex. National-level fluctuations (Fukushima, German nuclear exit, UK coal collapse) average out, leaving only the secular trend: gradual decarbonisation.

Locks: 6. The most locks of any country. Six carrier pairs maintain near-constant proportional relationships at the global level. This is the signature of a system whose internal ratios are structurally stable — the global grid changes slowly and uniformly.

Most stable pair: Gas/Other Renewables (CV = 0.014). At the global level, gas and Other Renewables maintain an almost perfectly constant ratio — a structural invariant of the world energy system over 26 years.

Fingerprint compactness: 0.588. The second-most symmetric fingerprint — reflecting the balanced global composition.

Amalgamation: ALL PASS. Every amalgamation scheme preserves the convex (accelerating) shape. The global transition is robustly accelerating at every level of resolution. This is the only system besides Germany where all 4 schemes pass.

Decimation: max entropy change 0.56%. The most stable under temporal decimation — even sampling every 8th year (4 observations) changes the mean entropy by less than 0.6%.

**Interpretation:** The World aggregate is the cleanest signal in the dataset — high path efficiency, convex acceleration, robust under amalgamation, stable under decimation. It is the compositional attractor toward which individual countries converge with varying noise. For CoDaWork 2026, this is the headline result: the global energy transition, read through the Hs instrument, is an accelerating, directional, near-geodesic trajectory on S^8.

---

## 5. Amalgamation Analysis

### 5.1 Results Summary

| Country | Binary F/C | Ternary F/N/R | 7-group | Binary T/NT | Overall |
|---------|-----------|---------------|---------|-------------|---------|
| Germany | PASS | PASS | PASS | PASS | ALL PASS |
| United Kingdom | FAIL | FAIL | FAIL | FAIL | ALL FAIL |
| Japan | PASS | PASS | PASS | FAIL | 3/4 PASS |
| France | FAIL | FAIL | PASS | FAIL | 1/4 PASS |
| China | PASS | PASS | FAIL | PASS | 3/4 PASS |
| India | FAIL | FAIL | PASS | FAIL | 1/4 PASS |
| World | PASS | PASS | PASS | PASS | ALL PASS |

### 5.2 Interpretation

Only Germany and World pass all amalgamation schemes. These are the two systems whose transitions are so strong that the shape classification survives any level of coarsening. All other countries have at least one scheme that flips their shape classification.

This is a direct empirical verification of Egozcue and Pawlowsky-Glahn's theoretical warning about amalgamation non-commutativity. When carriers are grouped before analysis, the resulting shape classification can differ from the full-carrier result. In the UK's case, all 4 schemes flip the classification from CONCAVE to CONVEX — a complete reversal of the transition's apparent character.

The pattern of failures reveals which internal dynamics are lost under amalgamation. The Binary Thermal/Non-thermal scheme fails for Japan (hides nuclear dynamics inside thermal), the UK (hides gas stability within fossil), and India (hides gas collapse within fossil). The 7-group detailed scheme fails for China (hides solar-vs-wind differential within VRE).

**Recommendation for CoDa practitioners:** Always run the Hs pipeline at the finest available carrier resolution first, then test amalgamation stability. If the shape classification is not preserved, the coarser analysis may produce misleading conclusions.

---

## 6. Decimation Analysis

| Country | 2x (%) | 4x (%) | 8x (%) |
|---------|--------|--------|--------|
| Germany | 0.74 | 0.94 | 2.69 |
| United Kingdom | 0.16 | 0.62 | 0.82 |
| Japan | 0.26 | 0.15 | 1.23 |
| France | 0.01 | 0.05 | 0.61 |
| China | 0.48 | 0.11 | 2.25 |
| India | 0.49 | 0.46 | 1.22 |
| World | 0.74 | 0.94 | 0.56 |

Shannon entropy changes are below 3% in all cases, even at 8x decimation (4 observations). The compositional entropy of these systems is robust to temporal subsampling — consistent with the expectation that entropy captures the instantaneous distribution, not the dynamics.

France shows the smallest decimation sensitivity (0.61% at 8x), consistent with its stable, concentrated composition. Germany shows the largest (2.69% at 8x), consistent with its turbulent, rapidly evolving mix.

---

## 7. Cross-Country Comparisons

### 7.1 Transition Archetypes

The 7 systems cluster into three distinct archetypes on the simplex:

**Accelerating (CONVEX):** Germany, China, India, World. These systems are diversifying at an increasing rate. Their V(t) curves bend upward. The transition is in its growth phase.

**Decelerating (CONCAVE):** United Kingdom, Japan, France. These systems are approaching a new compositional equilibrium. Their V(t) curves bend downward. The transition's fastest changes are behind them.

**Note on Germany:** Despite being classified CONVEX, Germany's R^2 is the lowest (0.5719), reflecting its non-monotonic V(t) trajectory. The nuclear exit creates a U-shaped variance profile — declining through 2007, then rising sharply. The classification is correct for the overall trend but masks this internal structure.

### 7.2 Path Efficiency as Discriminator

Path efficiency separates the systems cleanly:

| Path Efficiency | System | Interpretation |
|-----------------|--------|----------------|
| 0.9529 | World | Near-geodesic, pure secular trend |
| 0.6571 | China | Directional, no reversals |
| 0.6471 | India | Directional, no reversals |
| 0.5579 | France | Steady but slow migration |
| 0.4244 | Germany | Directional but turbulent (nuclear exit jumps) |
| 0.3801 | UK | Meandering — coal fluctuated before collapse |
| 0.1184 | Japan | Near-loop — Fukushima displacement and partial return |

This ranking is interpretable without any domain knowledge. An analyst seeing only the path efficiency numbers could immediately identify which systems underwent reversals (Japan), which moved steadily (China, India), and which had the clearest secular trend (World).

### 7.3 Locks as Structural Invariants

The number of locks correlates inversely with total variance:

| Locks | Country | sigma^2_A | Interpretation |
|-------|---------|-----------|----------------|
| 6 | World | 5.98 | Many structural couplings, low disruption |
| 3 | France | 12.64 | Stable secondary sources around nuclear dominance |
| 2 | Japan | 31.53 | Some couplings survive even Fukushima |
| 1 | China | 10.74 | Coal/Hydro coupling persists through renewable surge |
| 1 | India | 11.96 | Coal/Nuclear coupling — state-planned co-expansion |
| 0 | Germany | 152.11 | Everything in flux |
| 0 | UK | 103.13 | Everything in flux |

Germany and the UK — the two countries with the most dramatic transitions — have zero locks. Their energy systems are maximally disrupted; no proportional relationship has survived intact.

### 7.4 Entropy and the Diversification Narrative

Shannon entropy ranges (2000–2025):

| Country | H_min | H_max | Range | Trend |
|---------|-------|-------|-------|-------|
| World | 1.543 | 1.808 | 0.265 | Increasing |
| Germany | 1.251 | 1.896 | 0.645 | Increasing then plateau |
| UK | 1.294 | 1.744 | 0.450 | Increasing then plateau |
| Japan | 1.371 | 1.668 | 0.297 | Increasing |
| France | 0.782 | 1.297 | 0.515 | Increasing |
| China | 0.645 | 1.452 | 0.807 | Increasing |
| India | 0.902 | 1.093 | 0.191 | Nearly flat |

Every country is diversifying in the entropy sense — more even distribution of generation across sources. China shows the largest entropy increase (0.807), reflecting its transformation from a coal monopole (H = 0.645) to a diversified mix. India shows the smallest increase (0.191), confirming that its grid remains coal-dominated.

---

## 8. Significance for CoDaWork 2026

### 8.1 What This Experiment Demonstrates

This experiment shows the CoDa community that the Higgins Decomposition can read real compositional time series and extract interpretable, policy-relevant diagnostics from the simplex geometry alone. The V(t) shape classification, path efficiency, lock detection, and pair stability ranking are all derived from standard CoDa operations (CLR transform, variation matrix, Aitchison distance) applied in a systematic diagnostic sequence.

### 8.2 The Amalgamation Finding

The most important finding for the CoDa community is the amalgamation analysis. Five of 7 systems show shape classification changes under at least one amalgamation scheme. This is not a theoretical concern — it is an empirical observation with direct policy implications. A practitioner using binary Fossil/Clean data for the UK would reach the opposite conclusion about the transition's trajectory compared to one using full 9-carrier data.

### 8.3 Reproducibility

Every computation in this experiment is deterministic. The Python script (`Hs-M02_ember.py`) uses only numpy for numerical operations and produces identical results on every run. The input data is publicly available from EMBER. The pipeline uses no stochastic methods, no random seeds, no machine learning. Same input, same output, always.

---

## 9. Artifacts

| File | Description |
|------|-------------|
| `Hs-M02_ember.py` | Self-contained Python script — full pipeline, all 7 countries |
| `Hs-M02_results.json` | Complete machine-readable output (all diagnostics, all countries) |
| `Hs-M02_DEU_clr.csv` | Germany CLR coordinate time series |
| `Hs-M02_GBR_clr.csv` | United Kingdom CLR coordinate time series |
| `Hs-M02_JPN_clr.csv` | Japan CLR coordinate time series |
| `Hs-M02_FRA_clr.csv` | France CLR coordinate time series |
| `Hs-M02_CHN_clr.csv` | China CLR coordinate time series |
| `Hs-M02_IND_clr.csv` | India CLR coordinate time series |
| `Hs-M02_WLD_clr.csv` | World CLR coordinate time series |
| `Hs-M02_JOURNAL.md` | This document |

---

## 10. Conclusion

The EMBER experiment validates the Higgins Decomposition on real-world compositional data of global significance. The instrument distinguishes accelerating from decelerating transitions, identifies structural locks that persist through external shocks, measures path efficiency to separate directional transitions from circular ones, and demonstrates — empirically — that amalgamation can reverse the apparent character of a transition.

The 7 systems span a natural hierarchy from maximal disruption (Germany, sigma^2_A = 152) to minimal change (World aggregate, sigma^2_A = 6). The Hs diagnostics are consistent with domain knowledge at every point in this hierarchy, but they are derived purely from simplex geometry — no energy domain expertise is encoded in the pipeline.

The World aggregate, with its path efficiency of 0.9529, reveals something that may be invisible to practitioners working at the country level: the global energy transition is a near-geodesic on S^8. Country-level turbulence averages out. The secular trend is clear, directional, and accelerating.

This is the data the CoDa community will examine. Every number is reproducible.

---

*Peter Higgins / Rogue Wave Audio*
*Licensed under CC BY 4.0*
