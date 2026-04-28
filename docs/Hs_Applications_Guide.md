# Hˢ Applications Guide

**Compositional Intelligence Across Domains**

*Author: Peter Higgins, Markham, Ontario, Canada*
*Date: April 2026*
*Claim tier: Core science (architecture) + Exploratory (deployment patterns)*

---

## Purpose

This guide maps the Hˢ compositional analysis instrument to real-world applications across domains. It demonstrates that the same 12-step pipeline, the same diagnostic codes, and the same fingerprinting and power-mapping tools apply universally — from a rover on Mars to a trading desk in London to a reactor control room.

Hˢ is a non-contact compositional analyser. It reads any system that can be expressed as compositional fractions across carriers. It does not require knowledge of the domain physics. It does not require training data. It does not require calibration against domain-specific benchmarks (though reference standards exist for validation). The simplex is the same everywhere.

This guide is organised in two tiers. Three domains receive deep architectural treatment showing exactly how Hˢ components map to operational requirements. A broader catalog then surveys additional application domains at summary level with entry points for each.

---

## Part I: Deep-Dive Applications

### 1. Space Sensing and Remote Exploration

**The problem:** A planetary rover carries spectrometers, LIDAR, mass analysers, and imaging systems. Each produces compositional data — mineral abundances, atmospheric gas ratios, elemental fractions. The fundamental constraint is bandwidth. Earth-to-Mars communication ranges from 3 to 22 minutes one way, with data rates measured in kilobits per second. Every bit transmitted must carry maximum information. Raw spectral data is voluminous and largely redundant once the compositional character is known.

**How Hˢ maps to this problem:**

**Onboard pipeline.** The 12-step Hˢ pipeline runs on the rover's compute module. Each spectrometer reading produces an N×D composition matrix. The pipeline is deterministic, requires no GPU, no internet, no external library beyond NumPy. It runs in milliseconds on modest hardware. The output is a results dictionary containing the full geometric diagnosis.

**Fingerprint-based compression.** Once the pipeline completes, `hs_fingerprint.py` produces a fixed-length identity vector — a 7-dimensional numeric signature plus a SHA-256 hash. This fingerprint replaces the full N×D matrix for transmission purposes. When the fingerprint matches the previous reading (distance below threshold), the rover transmits only a confirmation code: "same regime." When the fingerprint changes, the rover transmits the new fingerprint plus the diagnostic codes that changed. A full fingerprint plus code set fits in approximately 200 bytes. Compare this to a raw spectral dataset of tens of kilobytes to megabytes.

**Power-directed sampling.** The Component Power Mapper (`hs_sensitivity.py`) runs periodically on the accumulated buffer. It identifies which carrier has the highest leverage index and the smallest criticality margin. The rover's sampling strategy adapts: allocate more spectral integration time and higher bit depth to the high-power carriers. Subsample the low-power carriers. This is not lossy compression — it is resolution allocation based on compositional importance. The carriers that matter most to system character get the most measurement precision.

**Phase boundary alerting.** The phase boundary map provides advance warning of regime transitions. When a carrier's value approaches its phase boundary, the rover can autonomously increase sampling rate for that carrier, switch to a higher-resolution instrument mode, or flag the region for targeted investigation. The "dog on a scent" behaviour emerges naturally: the power mapper tells the rover where to look, and the phase boundary map tells it when something is about to change.

**Architecture mapping:**

| Hˢ Component | Rover Function |
|---|---|
| `higgins_decomposition_12step.py` | Onboard compositional analysis engine |
| `hs_fingerprint.py` | Transmission compression — fingerprint replaces raw data |
| `hs_sensitivity.py` | Adaptive sampling controller — bit allocation by carrier power |
| `hs_codes.py` | Event-driven telemetry — transmit codes, not measurements |
| `hs_controller.py` (HsController) | Per-instrument pipeline manager with state machine |
| `hs_controller.py` (Hˢ-GOV) | Multi-instrument supervisor — cross-sensor correlation |
| `hs_audit.py` | Chain-of-custody for all onboard decisions |
| Phase boundary map | Autonomous investigation trigger |
| Diagnostic codes | Ground station receives meaning, not numbers |

**Data flow:**

Sensor → Buffer (sliding window) → HsController (pipeline per buffer) → Fingerprint comparison against previous → Decision: if same regime, transmit confirmation code (tens of bytes); if regime change, transmit new fingerprint + changed codes + power map delta (hundreds of bytes); if phase boundary breach, transmit full results + raw data for the critical carrier (kilobytes). Ground station maintains a mirror fingerprint database and reconstructs the full compositional narrative from the code stream.

**Compression estimate:** For a 5-carrier mineral spectrometer sampling at 1 Hz with 100 observations per buffer: raw data is 500 floats × 8 bytes = 4 KB per buffer. Hˢ fingerprint + codes = ~200 bytes per buffer in steady state. Compression ratio: 20:1 minimum, with no loss of diagnostic information. During regime transitions, targeted raw data for the critical carrier only: ~800 bytes. Effective average compression across a typical traverse: 10:1 to 50:1 depending on geological variability.

**What Hˢ does not replace:** Domain-specific spectral calibration, instrument health monitoring, orbital mechanics, communication protocols. Hˢ operates on the compositional layer only. The expert on the ground still interprets what a mineral phase transition means geologically.

---

### 2. Financial Markets — Real-Time Portfolio and Risk Composition

**The problem:** A portfolio of D assets produces a compositional vector at every market tick — the weight of each asset as a fraction of total portfolio value. The composition changes continuously. Risk managers need to know not just *what* the composition is, but *which component has disproportionate power over portfolio character*. A position that is 2% of portfolio value but drives 40% of the portfolio's geometric identity is the critical employee — the one whose departure (liquidation, default, or extreme move) changes everything.

**How Hˢ maps to this problem:**

**Streaming pipeline.** Each tick produces a new observation row. The HsController operates on a sliding window (e.g., last 100 ticks). The pipeline runs at each window advance. The HVLD shape tells you whether portfolio variance is accelerating (bowl — risk integrating, positions converging) or decelerating (hill — risk segregating, positions diverging). The classification (NATURAL, INVESTIGATE, FLAG) gives an immediate regime assessment.

**Power map as risk decomposition.** The Component Power Mapper replaces traditional risk attribution. Traditional methods decompose risk by position size or volatility contribution. The power map decomposes by *influence on portfolio character*. A small illiquid position with high transfer entropy to other positions — one that informationally predicts the behaviour of larger positions — has a power-to-fraction ratio far exceeding 1.0. This is the hidden risk that position-size-based metrics miss entirely.

**Phase boundaries as stress limits.** The phase boundary map tells the risk manager: "Position X can decline by 15% before the portfolio classification flips from NATURAL to FLAG." This is not a VaR calculation — it is a geometric statement about where the portfolio's compositional character changes state. It is deterministic, not probabilistic.

**Regime transition detection.** The structural mode SM-RTR-DIS (Regime Transition) fires when the portfolio undergoes a compositional state change — stalls and reversals in the entropy trajectory. The stall points mark the exact moments where the portfolio crossed from one regime to another. Historical replay with Hˢ produces an audit trail of every regime boundary the portfolio has crossed.

**Architecture mapping:**

| Hˢ Component | Financial Function |
|---|---|
| Sliding window pipeline | Real-time portfolio composition monitor |
| Power mapper | Risk attribution by influence, not size |
| Phase boundary map | Stress limit per position — deterministic |
| HVLD shape | Risk regime indicator (integrating vs. segregating) |
| Classification | Portfolio health signal (NATURAL/INVESTIGATE/FLAG) |
| Transfer entropy | Directed information flow — which position predicts which |
| PID decomposition | Redundancy vs. synergy in position interactions |
| Fingerprint database | Historical regime catalog — "we've seen this geometry before" |
| Diagnostic codes | Compliance-ready event stream |
| Audit trail | Regulatory audit: every decision traced with chain hash |

**The critical employee analogy in finance:** A market-maker position in an illiquid credit derivative — 0.5% of portfolio notional — that is the sole liquidity provider for a cluster of correlated positions. Its PCC (per-carrier contribution to variance) is low. Its transfer entropy is high: it informationally predicts the behaviour of positions 10x its size. Its PID contribution is synergistic: it creates information that no other position can replicate. The power mapper ranks it #1. Remove it, and the portfolio's geometric identity changes: NATURAL → FLAG. The criticality margin is 0.08. This is the position the risk committee needs to know about, and traditional risk metrics would rank it last by size.

---

### 3. Nuclear Reactor Monitoring

**The problem:** A nuclear reactor core contains an array of fuel assemblies, each with measurable neutron flux, temperature, and isotopic composition. The system is inherently compositional: the total neutron economy is distributed across fuel assemblies, control rods, moderator, and structural materials. Small compositional shifts — a control rod position change, a fuel burnup gradient, a coolant flow redistribution — can move the reactor from one operating regime to another. The operators need to know which component has disproportionate influence on reactor character, and how far the current state is from a regime boundary.

**How Hˢ maps to this problem:**

**Compositional decomposition of neutron flux.** Each fuel assembly's contribution to total core flux is a carrier. The N×D matrix is: N time steps (or spatial samples), D assemblies (or zones). The pipeline processes this as a standard compositional system. The HVLD vertex lock tells the operator whether core variance is integrating (approaching equilibrium after a transient) or segregating (diverging — potential instability signature).

**Power map for safety-critical carriers.** The Component Power Mapper identifies which assembly or zone has the highest influence on core character. In a validated SEMF (Semi-Empirical Mass Formula) decomposition, the Symmetry+Pairing term — 8.2% of total binding energy — was ranked #1 in power with a 4.68x power-to-fraction ratio. This is physically correct: these terms determine nuclear stability. Applied to reactor flux composition, the power map identifies which assembly, if perturbed, would most alter the core's geometric identity. This is the assembly that needs the closest monitoring.

**Phase boundary map for operational envelope.** The phase boundary map defines, for each assembly, how much its flux contribution can change before the core composition transitions to a different regime. This is a compositional complement to traditional reactivity margins. It does not replace nuclear engineering safety analysis — it provides an independent geometric view of the same system from a different mathematical framework.

**Continuous monitoring architecture.** The HsController runs continuously on streaming flux data. The Hˢ-GOV supervisor manages multiple analysis streams (flux composition, temperature composition, isotopic composition) and detects cross-stream correlations. If the flux composition fingerprint changes while the temperature composition remains stable, the governor flags the discrepancy for operator review. The audit trail provides full chain-of-custody for every analysis, compatible with nuclear regulatory requirements for traceability.

**Architecture mapping:**

| Hˢ Component | Reactor Function |
|---|---|
| Pipeline on flux composition | Core character monitor |
| Power mapper | Safety-critical assembly identification |
| Phase boundary map | Operational envelope per assembly |
| HsController | Per-stream continuous analyser |
| Hˢ-GOV | Multi-stream supervisor (flux + temp + isotopic) |
| Audit trail (SHA-256 chain) | Regulatory-compliant traceability |
| EITT invariance | Structural stability indicator — turbulence is real, not noise |
| Fingerprint database | Historical operating regime catalog |
| Breakpoint system | Configurable hold points for operator review |
| SM-RTR-DIS | Regime transition detection — operator alert |

**What Hˢ does not replace:** Neutronics codes (MCNP, Serpent), thermal-hydraulics (RELAP), safety analysis (PSA/PRA), regulatory compliance frameworks. Hˢ provides an independent compositional view. The nuclear engineer interprets the results within the established safety framework. The instrument reads. The expert decides.

---

## Part II: Application Domain Catalog

The following domains are mapped at summary level. Each entry identifies the compositional structure, the key Hˢ capabilities that apply, and the primary value proposition.

### 4. Environmental Monitoring

**Compositional structure:** Air quality (pollutant fractions of total particulate), water chemistry (dissolved species as fractions of total dissolved solids), soil composition (mineral/organic/contaminant fractions).

**Key Hˢ capabilities:** Continuous fingerprinting of environmental composition. Power mapper identifies which pollutant or species has disproportionate influence on environmental character. Phase boundary map defines safe operating limits per species. EITT detects whether compositional variability is natural turbulence or regime change.

**Value:** Early detection of environmental regime transitions (e.g., eutrophication onset in water systems). Compression of environmental sensor network data for remote transmission. Regulatory audit trail for all compositional assessments.

### 5. Medical Diagnostics — Biomarker Composition

**Compositional structure:** Blood panel composition (cell type fractions, protein fractions, metabolite ratios), microbiome composition (species abundances as fractions of total population), tissue composition (cell type proportions in biopsy samples).

**Key Hˢ capabilities:** Fingerprinting of patient compositional state. Power mapper identifies which biomarker has disproportionate diagnostic power — the yeast in the bread. Phase boundary map defines the compositional distance to a pathological state transition.

**Value:** A blood panel fingerprint that changes classification from NATURAL to INVESTIGATE is a geometric signal of compositional disruption — independent of which specific marker moved. The power map tells the clinician which marker to investigate first.

### 6. Manufacturing Process Control

**Compositional structure:** Alloy composition (element fractions), chemical process streams (reactant/product/byproduct fractions), food production (ingredient fractions, as demonstrated with the bread/yeast validation).

**Key Hˢ capabilities:** Real-time pipeline on process stream samples. Power mapper identifies which ingredient or component has the highest leverage on product character. Phase boundary map defines process control limits per component — deterministic, not statistical.

**Value:** The bread/yeast validation proved the concept: yeast at 0.9% mass fraction has a 33.64x power-to-fraction ratio. In any manufacturing process, the component with disproportionate power is the one that needs the tightest control, regardless of its mass fraction. Traditional SPC (Statistical Process Control) monitors all components equally or by variance contribution. Hˢ power mapping monitors by *influence on product character*.

### 7. Telecommunications — Network Traffic Composition

**Compositional structure:** Traffic type fractions (video, voice, data, signalling as fractions of total bandwidth), protocol distribution, source/destination composition, quality-of-service class distribution.

**Key Hˢ capabilities:** Streaming pipeline on traffic composition windows. Fingerprint-based anomaly detection — a new fingerprint indicates a compositional shift in traffic. Power mapper identifies which traffic class has the highest influence on network character. Phase boundary map defines where traffic composition changes regime (e.g., the point at which video traffic causes congestion-driven quality degradation).

**Value:** Network capacity planning based on compositional character rather than raw volume. Detection of DDoS or anomalous traffic patterns as compositional regime transitions. Bandwidth allocation by carrier power rather than by traffic volume.

### 8. Defence and Intelligence — Multi-Sensor Fusion

**Compositional structure:** Sensor returns from multiple platforms (radar, infrared, acoustic, electromagnetic) expressed as compositional fractions of total signal energy. Target signature decomposition across spectral bands.

**Key Hˢ capabilities:** Hˢ-GOV managing multiple sensor streams. Cross-stream fingerprint correlation. Power mapper identifying which sensor modality is most diagnostic for the current target. Phase boundary map defining signature stability margins.

**Value:** Sensor fusion at the compositional level rather than the signal level. The fingerprint provides a platform-independent target identity. The power map directs sensor allocation: which sensor to point where, based on compositional importance rather than availability.

### 9. Energy Grid Composition

**Compositional structure:** Generation mix (solar, wind, nuclear, gas, hydro as fractions of total supply), demand composition (residential, commercial, industrial fractions), storage state composition.

**Key Hˢ capabilities:** Continuous pipeline on grid composition. Power mapper identifying which generation source has disproportionate influence on grid character — the renewable source with high intermittency but critical timing. Phase boundary map defining stability margins per source.

**Value:** Grid stability assessment from a compositional perspective. Detection of grid composition regime transitions (e.g., the point at which renewable penetration changes grid character from baseload-dominated to intermittency-dominated). Dispatch optimisation based on carrier power rather than capacity factor alone.

### 10. Geochemistry and Mineral Exploration

**Compositional structure:** Rock and mineral compositions (oxide fractions, elemental abundances). This is the original domain of Compositional Data Analysis (CoDa).

**Key Hˢ capabilities:** The full pipeline as validated across 18 domains. Fingerprint database for lithological classification. Power mapper for identifying which element drives the petrological character. Phase boundary map for metamorphic facies transitions.

**Value:** Hˢ extends CoDa from a statistical framework to a diagnostic instrument. The 73 original diagnostic codes were developed on geochemical data. The structural modes (bimodal population, regime transition, carrier coupling) have direct geological interpretations.

### 11. Pharmaceutical — Drug Formulation Composition

**Compositional structure:** Excipient and active ingredient fractions. Dissolution profile composition over time. Stability testing — compositional change during storage.

**Key Hˢ capabilities:** Power mapper identifying which excipient has disproportionate influence on formulation character — the component that, if slightly altered, changes bioavailability. Phase boundary map defining formulation stability margins.

**Value:** Formulation robustness assessment. The power-to-fraction ratio identifies the critical excipient that needs the tightest manufacturing control. The phase boundary map defines the compositional space within which the formulation maintains its therapeutic character.

### 12. Climate Science — Atmospheric Composition

**Compositional structure:** Greenhouse gas fractions (CO₂, CH₄, N₂O, fluorinated gases as fractions of total radiative forcing), aerosol composition, ocean heat content distribution by depth layer.

**Key Hˢ capabilities:** Long time-series pipeline on atmospheric composition. Power mapper identifying which gas has disproportionate influence on climate system character. Phase boundary map for tipping point proximity.

**Value:** Compositional view of climate system — which forcing agent, regardless of concentration, has the highest leverage on system character. The phase boundary map provides a geometric measure of distance to compositional tipping points.

### 13. Sports Analytics — Team Composition

**Compositional structure:** Player contribution fractions (scoring, assists, defence, minutes as fractions of team totals), play-type composition (fast break, half-court, transition as fractions of possessions).

**Key Hˢ capabilities:** Power mapper identifying the critical player — the one whose absence changes team character most, regardless of their statistical contribution to any single metric. Phase boundary map for roster construction limits.

**Value:** The critical employee analogy applied to sports: the player with a 5x power-to-fraction ratio is the one the team cannot afford to lose, even if their box score statistics are unremarkable. Roster construction guided by compositional power rather than individual performance metrics.

---

## Cross-Domain Patterns

Several architectural patterns recur across all applications:

**Pattern 1: Fingerprint compression.** In any bandwidth-constrained application (space, remote sensing, IoT networks), the fingerprint replaces the raw data for routine transmission. Only regime changes trigger full data transmission.

**Pattern 2: Power-directed allocation.** In any resource-constrained application (sensor time, measurement precision, monitoring attention, capital allocation), the power map directs resources to the carriers that matter most to system character.

**Pattern 3: Phase boundary as operating envelope.** In any safety-critical or quality-critical application (nuclear, pharmaceutical, manufacturing, finance), the phase boundary map defines deterministic limits per component — not probabilistic confidence intervals, but geometric distances to regime transitions.

**Pattern 4: Multi-stream governance.** In any multi-sensor or multi-source application (defence, grid, environmental networks, rover platforms), Hˢ-GOV provides supervisory correlation across independently analysed streams.

**Pattern 5: Audit trail as compliance.** In any regulated application (nuclear, pharmaceutical, finance), the SHA-256 chain hash audit trail provides tamper-evident traceability from raw measurement to final diagnosis, compatible with ISO 17025 and regulatory frameworks.

**Pattern 6: Code stream as event bus.** In any operational application, the diagnostic code stream replaces verbose monitoring dashboards. Each code is a machine-readable event with known semantics. Systems integrate on codes, not on raw metrics.

---

## Entry Points

| Application Domain | Start With | Key Pipeline Tool |
|---|---|---|
| Space sensing | `hs_ingest.py` with spectral CSV | `hs_sensitivity.py` (power-directed sampling) |
| Financial markets | Sliding window on tick data | `hs_sensitivity.py` (risk attribution) |
| Nuclear reactors | Flux composition matrix | `hs_controller.py` (continuous monitoring) |
| Environmental | Sensor network CSV | `hs_fingerprint.py` (anomaly detection) |
| Medical diagnostics | Blood panel composition | `hs_sensitivity.py` (diagnostic power ranking) |
| Manufacturing | Process stream samples | `hs_sensitivity.py` (critical ingredient) |
| Telecommunications | Traffic composition windows | `hs_fingerprint.py` (anomaly detection) |
| Defence | Multi-sensor returns | `hs_controller.py` + Hˢ-GOV (multi-stream) |
| Energy grid | Generation mix time series | `hs_sensitivity.py` (stability margins) |
| Geochemistry | Standard CoDa workflow | Full pipeline (original domain) |
| Pharmaceutical | Formulation composition | `hs_sensitivity.py` (critical excipient) |
| Climate science | Atmospheric composition series | Phase boundary map (tipping proximity) |
| Sports analytics | Player contribution fractions | `hs_sensitivity.py` (critical player) |

---

## Constraints and Honest Limitations

Hˢ analyses *compositional* systems — data that represents parts of a whole. It does not apply to absolute measurements that are not compositional (e.g., raw temperature readings, absolute pressure values). The data must be expressible as fractions that sum to a constant.

Hˢ does not replace domain expertise. It provides a geometric reading of compositional structure. A geochemist interprets what a mineral phase transition means. A nuclear engineer interprets what a flux redistribution implies for safety. A clinician interprets what a biomarker shift means diagnostically. The instrument reads. The expert decides. The loop stays open.

The real-time streaming architecture described in Part I is an architectural pattern, not a deployed system. The pipeline, controller, governor, fingerprint, power mapper, and audit trail all exist as validated Python code. The embedded systems engineering — hardware integration, real-time operating systems, communication protocols, bit-level streaming — is deployment work that follows from this architecture but has not yet been built.

The compression ratios quoted are estimates based on fingerprint and code sizes versus raw data sizes. Actual compression depends on regime variability, carrier count, and sampling rate. The estimates are conservative for steady-state operation and optimistic for highly variable systems.

---

*The simplex is the same everywhere. The instrument reads any system that lives on it.*
*The power map reveals what mass fraction hides.*
*The fingerprint compresses what bandwidth cannot carry.*
*The phase boundary warns before the regime changes.*
