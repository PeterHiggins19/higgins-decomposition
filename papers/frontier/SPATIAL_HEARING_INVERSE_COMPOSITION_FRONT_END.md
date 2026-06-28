# Spatial hearing as an inverse composition — the acoustic front end Hˢ was built for

*The stated purpose. Per Peter: "a front end is precisely what is needed to complete my work in acoustics —
the entire reason for Hˢ. I just like to make things that work and not have surprises." This seed records the
target the instrument was always aimed at: a **deterministic, surprise-free front end** that turns a
microphone array's raw multichannel input into decision-relevant compositional features for source
localization, ranging, and broadband reception. Companion to the light and spectral seeds (same sphere).
Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. Honest-broker; every
claim tiered. A seed, not a result. Nothing posted.*

---

## Why this is the point, not a tangent
Hˢ began as the math behind acoustic instruments (the loudspeaker / RWA origin). The **forward** problem is a
cabinet radiating a conserved budget of power into a direction-dependent field. The **inverse** problem —
*what Hˢ is for* — is a sensor array receiving that field and recovering *where* and *what*. Same
HRTF/diffraction/spherical-harmonic operator, run backwards. The front end completes the acoustics work by
closing that loop. The design value is the one Peter names: **no surprises** — a front end that is
deterministic, reproducible to a hash, and that *holds* rather than hallucinates when the data is ambiguous.

## Spatial hearing is already a composition (Tier 2 — established geometry)
- **ILD** (interaural level difference, the high-frequency localization cue) is a **log-ratio** of the two
  channels' energies — the ear works in dB because the problem is relative. That is CLR/Aitchison geometry by
  construction.
- **Array / ambisonic energy** over channels or spherical harmonics is a **composition**: total received
  power = closure; parts = channels / harmonics / bands.
- **The HRTF is the observer-projection.** Head and pinna diffraction imprint direction onto the spectrum;
  the spectral notches/peaks are *the* front/back and elevation cues. This is the same direction-dependent
  projection as the spectral and light seeds — the operator that stamps "where" onto "what."
- **Steered-response power over candidate directions** is a composition on the sphere; over time, a **moving
  composition**.

## What Hˢ reads as the front end (Tier 2/3)
On the moving spatial composition, the engine's native outputs map onto the real tasks:
- **helmsman** — the dominant direction / source;
- **arrow of intent** — a source in motion (tracking);
- **effective dimensionality** — how many sources are live / how concentrated the field is;
- **regimes** — onset/offset; a new source appearing;
- **EITT (the honest-hold)** — when the spatial estimate is at the boundary of reliability (cone of
  confusion, reverberant null), return a calibrated *hold*, not a confident wrong bearing.
The **honest-hold is the differentiator** for robotics: a localizer with a calibrated "I don't know" is worth
more than one a degree more accurate but occasionally certain and wrong. This is the guard layer doing its
designed job — "no surprises" made operational.

## Scope — front end, not the whole cortex (contradiction-test boundaries)
- **Front end only.** Hˢ supplies the deterministic transduction-to-features stage (the CNT-style
  preprocessor). It does **not** replace auditory scene analysis, source separation, or learned priors.
  "Hˢ does what the auditory cortex does" is **rejected**; "Hˢ supplies the geometry the cortex exploits"
  holds.
- **Direction strong, ranging weak.** Direction is well-cued (ITD/ILD/spectral). Passive **ranging** leans on
  direct-to-reverberant ratio and level — weak, ambiguous cues; the compositional reading is in the right
  geometry but does **not** dissolve the ill-posedness. Flag ranging Tier-3-shaky; do not let it ride with
  direction.
- **The cave-mammal motivation, honestly.** Evolution solved an underdetermined inverse (3D world, two ears,
  one head) by turning diffraction into a feature and reading relatively. A robot has it easier (more
  sensors, known geometry, no fixed skull), so a clean compositional core should match the biological
  front-end more cheaply — *for the front-end part*. This motivates; it does not prove.

## The test (Tier 3 — hypothesis, honest null welcome)
Benchmark the Hˢ front end against the standard estimators: **GCC-PHAT** (ITD/TDOA), **MUSIC** and
**SRP-PHAT** (DOA), and a modern learned localizer, on real array recordings with ground-truth angles
(anechoic, then reverberant). Likely honest outcome: it **matches** them on direction accuracy, and the real
gain is **determinism + the honest-hold** (calibrated abstention under ambiguity), not raw degrees. A null
(Hˢ adds nothing over GCC-PHAT/MUSIC and offers no better abstention) is equally publishable and bounds the
claim. Determinism (content-hash reproducibility on identical input) is a Tier-1 property the baselines do
not advertise.

## Status
**SEED — the stated purpose, not yet a result.** Tier 2 for the established geometry (ILD log-ratio; array
composition; HRTF projection); Tier 3 for the engineering claim (front end vs the standard estimators; null
welcome). No "first"; no priority. Companion: `LIGHT_AS_COMPOSITION_RIEMANN_SILBERSTEIN.md`,
`SPECTRAL_COMPOSITION_AND_THE_ROTATION_GROUP.md`. Peter is the sole gate; nothing posted.
