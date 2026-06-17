# Geosensing with the Higgins Decomposition (Hs): a deterministic, hardware-locked multi-sensor compositional field instrument

**Public concept proposal · 2026-06-09 · working draft (publication at the author's gate) · honest-broker, claim-tiered**

**Abstract.** We propose developing a portable, multi-sensor **geosensing** instrument that applies the **Higgins Decomposition (Hs)** — a deterministic compositional-navigation method (CNT/CNQ) on the Aitchison simplex — to live field data, and **locking its core vector-space (quaternion) computations in hardware** for real-time, auditable, on-site compositional analysis. The goal is onsite geological knowledge — layer boundaries, the driving element, regime changes — delivered faster and more transparently than current field workflows, on a path that scales from a cell-phone-plus-clip-on-spectrometer to onboard planetary remote sensing. This note develops the device with a **geoscience domain collaborator**, proposes a staged **NASA / USGS** remote-sensing collaboration, and lists the **established results that qualify Hs's performance**.

**Keywords:** compositional data analysis, Aitchison geometry, CLR, ILR, isometric log-ratio, CNT, CNQ, quaternion, geosensing, chemostratigraphy, mudstone, provenance, hyperspectral, multispectral, pXRF, portable XRF, Raman spectroscopy, field spectroscopy, sensor fusion, edge computing, FPGA, VPU, deterministic computation, hash provenance, remote sensing, planetary geology, rover autonomy, NASA, USGS, EMIT, CRISM, PIXL.

---

## 1 · The concept in one line
A geologist carries a multi-sensor probe; **each sensor stream is navigated by its own small, exact CNT**, the streams are **fused by reliability (calibrated against a few onsite grab-samples)**, and the whole computation runs as **fixed vector-space (quaternion) operations locked in hardware** — so layer boundaries and their driving element are read **on-site, in real time, deterministically, and auditably.**

## 2 · Develop the device (with a geoscience domain collaborator)
The collaboration needs two competencies, both established in the literature: compositional-data chemostratigraphy (wavelet + CoDa, Wehner 2017) and **cell-phone Raman field identification** (Dhankhar & Wehner 2023). The instrument:

- **Sensors:** phone-native camera (colour → carbonate/organic/Fe proxies), magnetometer (susceptibility → clay / heavy-mineral proxy), GPS + IMU (position, bed dip); plus a **Raman / pXRF clip-on** as the high-fidelity elemental channel.
- **Per-sensor CNT:** one deterministic CNT per stream (closure → CLR → ILR → step / helmsman / regime).
- **Calibration-weighted fusion:** a handful of onsite grab-samples set each channel's weight; a simulation on a real mudstone wall already shows the design rule — *the elemental sensor leads, naive equal-weight fusion dilutes, calibration-weighted fusion recovers it.* Calibrate and weight by reliability; don't just add sensors.
- **Development path:** phone + clip-on prototype → field-calibrate the sensor→composition transfer functions on known sections → ruggedize. (See `FIELD_MULTISENSOR_TOOL_CONCEPT.md` + the working simulation.)

## 3 · Lock Hs in hardware — vector-space computation for speed
The exact CNQ reading at four parts is a **quaternion operation** — a fixed-size, branch-free vector-space kernel. Burned into an FPGA / vision-processing unit / radiation-hardened spaceflight processor, the per-sensor CNT + fusion run at **deterministic, real-time speed at the sensor**, producing **custom on-device results** (the boundary/driver/regime map) without a downlink or a server. Hardware-locking buys speed, determinism, auditability (hash-stamped output), and edge/onboard operation. **The aim — onsite compositional geo-knowledge above the current field standard — is the hypothesis this build sets out to prove**, by calibration against independently known sections; it is the target, not a claim.

## 4 · The proposal to NASA / USGS — staged, ground-first
1. **Validate with a geoscience domain collaborator** on a ground-truthed multi-element section (co-authored).
2. **USGS — ground reprocessing** of existing hyperspectral mineralogy archives (EMIT, CRISM) with the same multi-sensor CNT atlas; software on existing data.
3. **NASA — onboard kernel** TRL demonstration: the fixed quaternion facet kernel as on-device compositional triage / smart-downlink; autonomy later.

Stated as an **open collaboration concept** — interest expressed, not involvement claimed. Each stage earns the next.

## 5 · Proof list — established Hs performance (the qualification)
What is already demonstrated and in the public repository (each carries its tier):

- **Deterministic to the IEEE-754 double-precision floor (~2.22 × 10⁻¹⁶)**; same input → same output; hash-chainable provenance. *(confirmed)*
- **Numerical stability measured:** the original arccos bearing lost up to **~8 significant digits** near 0°/180°; the atan2 form eliminates it (precision audit P01–P10). *(confirmed)*
- **Reproducible on real geoscience data:** a cited, one-command-reproducible CNT/CNQ run on Lower-Cretaceous mudstone (Frielingen-9, PANGAEA 897615). *(confirmed)*
- **Higher-dimensional reconstruction:** overlapping exact D=4 CNQ charts, glued on shared parts, rebuild the full higher-dimensional compositional move **losslessly** (alignment 9 × 10⁻¹⁶, reconstruction 4 × 10⁻¹⁴; overlap proven necessary). *(confirmed)*
- **Robust data treatment:** an upstream zero-treatment validated across **all 10 EMBER countries** — bit-identical on zero-free data, removes the floor artifact where zeros exist, and **prior results confirmed unchanged**. *(confirmed)*
- **Canonical-engine run** on national Canada electricity composition (hash-stamped, true dimensionality). *(confirmed)*
- **Breadth:** **100 of 101 datasets across 11 domains** ran end-to-end through CNT v3 + CNQ v2; cross-language (Python + R) parity verified at the IEEE floor against three independent reference inputs (Backblaze, Planck CMB, Standard-Model neutrino). *(confirmed)*
- **Four-form transparency:** every algorithm published as Python + R + language-agnostic pseudocode + a formal I/O standard (HUF-STD-002), with a seven-step verification protocol. *(confirmed)*
- **Presented:** the method was delivered at **CoDaWork 2026** (Coimbra). *(confirmed)*

These qualify the *method*. They do not yet claim field-beating performance — that is precisely what the proposed device + calibration program sets out to establish.

## 6 · Verify it yourself
Start with the executive overview ([`00_EXECUTIVE_OVERVIEW.md`](00_EXECUTIVE_OVERVIEW.md)) and its §9 "receipts" links to the engine, standards, trust protocol, and precision tests; rerun the mudstone demo from one CSV ([`demo_frielingen9/REPRODUCE.md`](demo_frielingen9/REPRODUCE.md)). Everything above is reproducible.

## 7 · Governance & honesty
Hs computes; **HUF governs what is released** (carrier filter — need-to-know / withhold-on-distribution, suited to government and pre-publication data). AI assistance is disclosed under HUF-STD-001 (human-only authorship). Claim tiers travel with every statement. This is a **concept proposal and an open invitation to collaborate**, not a statement of any agency's involvement.

## References
- Wehner (2017) — wavelet + compositional-data chemostratigraphy.
- Dhankhar & Wehner (2023) — cell-phone Raman field mineral identification.
- Thöle et al. (2019) — Frielingen-9 core geochemistry, PANGAEA, https://doi.org/10.1594/PANGAEA.897615 (CC-BY 4.0).
- NASA EMIT imaging spectrometer; NASA/JHUAPL CRISM; NASA Mars-2020 PIXL — hyperspectral / elemental remote-sensing context.

*Contact and collaboration are arranged off-channel by the author. The instrument reads. The expert decides. The hashes carry the receipts.*
