# Multi-sensor field tool — the rover at human scale (concept + simulation)

*2026-06-09 · Cowork working tree. Extends `FIELD_DIRECTIONAL_SNIFFER.md`. **This is a concept demonstrator on a synthetic-but-real-grounded wall** — the proxy sensor models are explicit assumptions; the architecture and the fusion result are the demonstrable parts. The instrument reads; the expert decides.*

## The idea
Run the space/remote-sensing architecture at human field scale, where it can be tested cheaply today: **the geologist is the rover, the phone is the multi-sensor platform.** Each sensor stream, as the rover scans a wall, is an ordered compositional series — so Hs runs **one CNT per sensor** ("several copies of CNT functioning per sensor") and a **fusion layer** combines them into a single, robust boundary/regime reading. A few **onsite grab-samples** are the held-out calibration (the role CaCO₃/TOC played in the mudstone demo).

The key geometric fact that makes the blend free: **a vertical wall's height axis is a stratigraphic depth axis.** So the wall scan and the down-core mudstone profile share one coordinate. In this demo the wall *is* the real Frielingen-9 section (PANGAEA 897615) stood upright — the mudstone layers and the wall scan are literally the same data seen two ways.

## Architecture
```
        phone / clip-on sensors (per height h on the wall)
   ┌───────────────┬───────────────┬───────────────┬───────────────┐
   │ camera RGB    │ magnetometer  │ Raman/pXRF     │ GPS + IMU      │
   │ (colour comp) │ (χ susceptib.)│ (elemental comp)│ (position,dip)│
   └──────┬────────┴──────┬────────┴──────┬─────────┴──────┬────────┘
          │ CNT#1         │ CNT#2         │ CNT#3          │ (geo-tag)
          ▼               ▼               ▼                ▼
     navigation      navigation      navigation       position / dip
          └───────────────┴───────┬───────┴────────────────┘
                                   ▼
                    FUSION  →  boundary / regime consensus
                                   ▼
                 calibrate against onsite grab-samples
                                   ▼
              robust layer map + driver per boundary (live, on-device)
```
Each cheap, noisy channel is navigated by its own exact CNT; the fusion takes the **consensus** (a boundary flagged by several sensors is high-confidence; noise in one channel does not trip a false boundary). This is the front-end / edge-instrument thesis (`HS_FRONTEND_POSITION.html`) at field scale: small deterministic CNT kernels, one per sensor, fused on-device.

## Sensors — what's real, what's modelled
| Channel | What it senses | Real availability | Proxy model in the sim (explicit) |
|---|---|---|---|
| **Camera RGB** | colour → carbonate (pale), organic (dark), Fe/clay (hue) | every phone | RGB = f(CaCO₃ lightness, TOC darkness, Si/Al hue) + noise → 3-part colour composition |
| **Magnetometer** | magnetic susceptibility → detrital clay / heavy minerals vs carbonate dilution | every phone | χ ∝ (Al₂O₃ + Zr) − CaCO₃ dilution → 2-part [susceptible, diluent] + noise |
| **Raman / pXRF clip-on** | elemental composition directly | clip-on add-ons exist; **cell-phone Raman is Matthew's own field-ID work (Dhankhar & Wehner 2023)** | reads [SiO₂, Al₂O₃, Rb, Zr] with multiplicative noise → 4-part elemental composition (the high-fidelity channel) |
| **GPS + IMU** | position, bed dip/strike | every phone | tags each reading; not navigated, used for geometry |
| **Onsite grab-samples** | lab-grade ground truth at a few heights | the geologist's hammer | a handful of exact composition points = calibration anchors |

## Why it matters to NASA / USGS — and as a field tool today
- **Direct compositional analysis at the edge.** The same multi-sensor, CNT-per-sensor, fuse-on-device architecture is what an autonomous rover needs; demonstrating it at human field scale is the cheapest possible proof-of-concept, on hardware everyone already carries.
- **A useful fast geological tool in its own right.** Even without the space framing, a phone that maps layer boundaries and names the driving element as you walk a wall — calibrated by a few grab-samples — is a real, immediately useful field instrument. The space case and the field case are the same tool.
- **The bandwidth argument, downscaled.** A rover can't downlink everything; a field geologist can't lab-sample everything. In both, the win is the same: cheap continuous sensing + a principled on-device reduction + a few high-quality calibration points.

## What the simulation shows
On the Frielingen-9 wall: each synthetic sensor's CNT navigation, a calibration-weighted fusion track, the live per-height readout, and onsite-sample calibration. The honest result it surfaces (and it is more useful than a tidy "fusion wins"):

- The **elemental clip-on (Raman/pXRF) is the workhorse** — it tracks the true down-wall dynamics at **r = 0.91**.
- The phone-native **colour and magnetic proxies, as modelled here, carry almost none of the elemental signal** (r ≈ 0), so **naive equal-weight fusion dilutes** the good channel down to **r = 0.04**.
- **Calibration-weighted fusion** — weights set by each channel's agreement with the onsite grab-samples — downweights the weak channels (weights came out ≈ [1.0, 0, 0]) and **recovers r = 0.91**.

So the demonstrated lesson is sharper than "more sensors = better": **calibrate, weight by reliability, let the high-fidelity compositional sensor lead — and the grab-samples earn their place by setting the weights.** The naive-fusion failure is shown on purpose. See `field_tool_sim/field_multisensor_sim.html`.

## Honest tiering
- **Simulation, not measurement.** Sensor readings are synthetic proxies of the real Frielingen-9 composition; the proxy mappings are modelling assumptions, stated above.
- **Demonstrable here:** the multi-sensor / CNT-per-sensor / calibration-weighted-fusion architecture runs end to end; and the simulation correctly surfaces that **fusion must be reliability-weighted** — naive averaging of a strong channel with weak ones degrades it, and calibration against the onsite samples fixes that.
- **To test on real hardware:** the actual sensor→composition transfer functions (the synthetic colour/magnetic proxies here are deliberately crude and came out near-uninformative about the *elemental* dynamics — real RGB and magnetic-susceptibility geology proxies may carry more, and that is an empirical question for Matthew), real-device noise, and field calibration. Architecture CONFIRMED in simulation; field performance and proxy fidelity TO TEST.

*The instrument reads. The expert decides. The hashes carry the receipts.*
