# The constellation as an Earth sensor — environmental & space‑weather sensing

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. Seed/concept —
2026‑06‑20. The dual‑use scientific arm of the study. **Strongly distinctive, entirely unproven:** every
detection claim is **[T3]** until shown on real high‑precision data; the methods are standard **[T2]**;
the physical parameters quoted are textbook references, not Hˢ results.*

---

## 1. The idea

A precisely‑tracked satellite is a **drag sensor**: its orbital response encodes the local neutral
atmosphere. Its radio links are an **ionospheric probe**: their amplitude/phase fluctuations encode plasma
irregularities along the ray path. A constellation of ~10⁴ such satellites, read with a deterministic,
multi‑scale engine, becomes a **distributed, high‑resolution sensor network** for the upper atmosphere —
across altitude, latitude, and local time, continuously, for years. What is built for operations
(§ [`CONCEPT_AND_VALUE.md`](CONCEPT_AND_VALUE.md)) produces, as a by‑product, **scientific data** that is
hard to obtain at this density and continuity by any other means. **[T3]**

## 2. What can (in principle) be measured

| environmental signal | observable | channel | tier |
|---|---|---|---|
| neutral density variation | along‑track drag / Δ(semi‑major axis) | drag | T3 |
| thermospheric winds & gradients | along/cross‑track differential drag | drag | T3 |
| gravity waves (neutral) | quasi‑periodic drag oscillations (~min–hours) | drag | T3 |
| ionospheric plasma irregularities / scintillation | radio amplitude/phase fluctuations (S4, σφ) | radio | T3 |
| geomagnetic‑storm response | rapid density rise correlated with Kp | drag + radio | T3 |
| solar‑cycle modulation | long‑term density trend correlated with F10.7 | drag | T3 |

## 3. The external drivers — F10.7 and Kp

Two public indices contextualize everything:

- **F10.7** — the 10.7 cm solar radio flux (2800 MHz), the standard proxy for solar EUV, which heats and
  expands the thermosphere. It carries the **~11‑year solar cycle** and a **~27‑day** solar‑rotation
  modulation. Higher F10.7 ⇒ higher density at altitude ⇒ more drag. Density at Starlink altitudes can
  vary by a factor of ~2–10 across the solar cycle (standard space‑physics result, not an Hˢ claim).
- **Kp** — the planetary geomagnetic index (0–9, 3‑hourly), capturing **short‑term storms**. During
  strong storms (Kp ≳ 7) thermospheric density can rise by factors of a few within hours and stay
  elevated for 1–3 days.

In the study these are used to **normalize/detrend** drag signals, to **set context‑adaptive thresholds**
(relax during high F10.7/Kp, tighten when quiet), and as **coherence references** (a healthy fleet
responds *coherently* to F10.7/Kp; breakdown flags differential effects or faults). Current Solar Cycle 25
is in/near its active phase through the late‑2020s, so elevated and variable drag is the operative regime.
**[T2** method; **T3** what the fleet data would show.]

## 4. The method toolkit (standard, hence T2)

The engine for this arm is multi‑scale time‑series analysis on per‑satellite drag/radio residuals, then
compositional roll‑up across the fleet:

- **Lomb–Scargle periodogram** — robust frequency identification on **unevenly sampled** tracking data;
  best for stable, long‑duration periodic content (orbital frequency, nodal precession, diurnal, 27‑day).
- **Continuous Wavelet Transform (CWT)** — time–frequency localization; best for *when* a transient (a
  manoeuvre, a storm onset, a wave packet) begins and ends.
- **Discrete Wavelet Transform (DWT)** — efficient multi‑resolution decomposition; denoising and
  trend/detail separation.
- **Wavelet Packet Transform (WPT) + best‑basis** — full adaptive decomposition of *both* approximation
  and detail branches, giving uniform/adaptive frequency resolution; **best‑basis selection** (typically
  **Shannon entropy** cost, Coifman–Wickerhauser bottom‑up pruning) chooses a sparse, signal‑adapted
  representation. With a **fixed wavelet + fixed cost** the basis and features are **deterministic** — the
  property that makes them admissible as Hˢ inputs.
- **Wavelet coherence** — between a satellite's drag/radio residual and an external driver (F10.7, Kp), or
  between neighbouring satellites, to separate driven response from intrinsic/anomalous behaviour.

**Why determinism matters here:** the scientific value depends on reproducibility. Fixed bands, fixed
wavelet, fixed cost function ⇒ identical features ⇒ hash‑receiptable products. That discipline is what
distinguishes an Hˢ data product from a one‑off analysis.

### Indicative LEO bands (starting point, to be refined)

| band | approx. frequency | physical meaning |
|---|---|---|
| orbital | ~15 cycles/day | satellite orbital period |
| nodal precession | ~0.1–1 cycle/day | regression of the ascending node |
| diurnal | ~1 cycle/day | daily atmospheric density variation |
| long‑period | < ~0.05 cycle/day | lunisolar, solar radiation pressure |
| manoeuvre/anomaly | broadband / > orbital | impulsive or unexpected energy |

(These are a documented starting set, not tuned results — they must be validated per shell.)

## 5. Gravity‑wave detection via drag (neutral atmosphere)

Thermospheric gravity waves (periods ~minutes–hours) appear as small quasi‑periodic perturbations in
along‑track acceleration. Proposed pipeline **[T2 methods / T3 detections]**:

1. High‑precision ephemerides → along‑track acceleration residual (kinematics layer).
2. Remove large‑scale drivers (F10.7 baseline, Kp storms, diurnal).
3. WPT + best‑basis (Shannon) on the residual, focused on gravity‑wave scales.
4. Extract energy / dominant scale / intermittency (kurtosis, wavelet entropy) per satellite.
5. **Fleet‑level spatial coherence** of those features — a spatially coherent wave field vs localized
   perturbation is the discriminator a single satellite cannot provide.
6. Catalogue events (timing, amplitude, dominant scale, coherence) with F10.7/Kp context; hash‑receipt.

Value: high‑resolution maps of gravity‑wave activity (sources, propagation, dissipation), better
gravity‑wave parameterization in whole‑atmosphere models, and improved small‑scale drag models that feed
back into fuel budgeting. **Caveat:** amplitudes are small ⇒ this needs high‑precision OD and careful
separation from manoeuvres/attitude/instrument effects.

## 6. Ionospheric plasma waves / scintillation (radio channel)

Plasma irregularities mainly affect satellites through **radio propagation** (amplitude/phase
scintillation), not mechanical drag. If high‑rate link‑quality metrics are available, a six‑stage
**radio pipeline** applies **[T2 methods / T3 detections]**:

1. **Ingest & synchronize** link metrics (amplitude, phase, SNR/CNR, AGC) with precise ephemerides and
   ray‑path geometry; align F10.7/Kp.
2. **Preprocess & detrend** — remove solar/geomagnetic/diurnal baselines; quality‑filter manoeuvres &
   handovers; isolate high‑frequency fluctuations.
3. **Feature extraction** — WPT + best‑basis (Shannon) on amplitude/phase residuals at scintillation
   fading scales; energy, dominant scale, intermittency, wavelet entropy; wavelet coherence with drivers
   / neighbours.
4. **Scintillation indices** — S4 (amplitude), σφ (phase), plus wavelet‑derived enhancements, per
   satellite and per spatial cluster.
5. **Fleet‑level coherence** — spatial structure of scintillation (large‑scale plasma structure vs
   patchy); a "plasma‑activity coherence" sub‑signal.
6. **Contextual anomaly detection & products** — F10.7/Kp‑adaptive thresholds; occurrence statistics,
   scale characterizations, event catalogues; every product hash‑receipted.

Value: operational (link‑reliability awareness during space weather, OD phase‑error context) and
scientific (high‑density maps of ionospheric irregularities; ionosphere–thermosphere coupling). **Caveat:**
this needs **radio metrics**, which are largely **proprietary**; on public data this arm is limited to the
drag channels.

## 7. Upper‑atmosphere wind & density mapping (the headline science)

Combining the neutral channels — density from along‑track drag, winds from along/cross‑track differential
drag, waves from the multi‑scale layer — and rolling up compositionally across the fleet yields the most
distinctive product: **continuous, high‑spatial‑density maps of thermospheric density and winds**, from
local features up to global circulation, with multi‑scale wave structure resolved. This is difficult to
obtain at this density/continuity from dedicated science missions alone, and it is **directly useful** to
the operator (better drag models) and to planetary science (model validation across a solar cycle). It is
the strongest dual‑use case in the study — and the most dependent on **orbit‑determination precision**.
**[T3]**

## 8. Scientific value & collaboration

Potential partners and uses (no engagement implied or authorized): NASA, NOAA/SWPC, ESA, and academic
space‑physics groups, for thermospheric density/winds, gravity‑wave climatology, ionospheric scintillation
statistics, and atmospheric/space‑weather model validation (NRLMSISE‑00, JB2008, DTM, TIE‑GCM). The
deterministic, hash‑receipted nature of the products is a real asset for scientific reproducibility.

## 9. Honest limitations (the whole arm depends on these)

- **Precision floor.** Public TLEs are generally **insufficient** for the high‑precision OD these science
  products need; high‑precision ephemerides (operator‑grade) are typically required. See
  [`DATA_AND_SOURCES.md`](DATA_AND_SOURCES.md).
- **Ballistic coefficient.** Drag→density conversion needs each satellite's mass/area (attitude‑dependent)
  — non‑trivial and often proprietary.
- **Model dependence.** Some atmospheric modelling is still needed to separate density from other
  perturbations; Hˢ is a **complement**, not a replacement.
- **Radio access.** The plasma/scintillation arm needs proprietary link metrics.
- **Domain expertise.** Mapping spectral/wavelet features back to physical causes requires orbital‑
  mechanics and space‑physics knowledge — collaboration, not solo analysis.

## 10. The minimal scientific demonstration

On **public** data: take one shell's TLEs over a window containing a **documented geomagnetic storm**,
derive an along‑track drag proxy via the kinematics layer, detrend with public F10.7/Kp, run WPT +
best‑basis, and show (reproducibly, hash‑receipted) that the fleet's drag response (a) tracks the storm
coherently and (b) carries multi‑scale structure beyond the storm trend. Even at the coarse precision of
public TLEs, a clean positive here would justify pursuing high‑precision data for the full product — and
would be the first **T3 → T1** promotion on the science side.
