# Geology applications of Hs — collaboration overview (public)

This folder collects the Hs-side material for applying the **Higgins Decomposition (Hs / CNT)** to compositional geoscience, and an **open invitation** to compositional-geoscience colleagues to collaborate. It is written as public science; the working relationship and any private contact are handled off-repo (HUF carrier-filter governance).

## What Hs / CNT is (one paragraph)
The Higgins Decomposition is a **deterministic instrument for compositional time-series on the simplex.** Its core engine, **CNT** (Compositional Navigation Tensor), takes an ordered sequence of compositions and reads the motion at each step: the size of the compositional change (Aitchison step), its direction (bearing), which part is driving it (the "helmsman"), the effective number of active carriers, and where the regime shifts. A companion layer, **CNQ**, names the quaternion algebra where the dimension allows. Everything is hash-chained and byte-reproducible. It is built to **complement** established compositional-data and time-series methods — not to replace them.

## Why geoscience
Geochemical and stratigraphic data are canonically compositional and frequently ordered (down-section, across space, or over a cooling/differentiation path). That is exactly the object CNT reads. The published wavelet + compositional-data chemostratigraphy approach (Wehner 2017) and cell-phone-Raman field identification (Dhankhar & Wehner 2023) define adjacent, complementary tooling that this work connects to.

## Candidate studies
1. **Mudstone chemostratigraphy — a deterministic compositional-navigation layer.** Strongest near-term fit. → `MUDSTONE_HS_FIT.md`
2. **Igneous differentiation as compositional dynamics** (fractional crystallization through phase points). → `IGNEOUS_DIFFERENTIATION_SEED.md`
3. **Field directional compositional sniffer** (Hs on a cell-phone micro-lab; remote-sensing / mapping). → `FIELD_DIRECTIONAL_SNIFFER.md`

## Existing Hs geochemistry (already run)
- **Hs-05** — CNT on 26,266 intraplate volcanic rocks, 10 major-element oxides (Ball / EarthChem).
- **Intermediate-rocks decode** (mafic↔felsic transition structure), **HFSP** fixed-point / phase machinery, **X-ray crystallography** decomposition, and a set of CNT geochem domain runs (Stracke OIB/MORB, Tappe kimberlite, Qin clinopyroxene, Ball TAS/age).
- All copied into `copies/`; full cross-repo index in `REPO_MAP.md`.

## Collaboration posture
An open, research-grade collaboration: Hs/CNT applied to compositional geoscience, anchored against established methods and known sections, calibration-gated before any interpretive claim. Contributors steer the domain and publication standard; Hs supplies a deterministic, reproducible navigation/driver/regime layer.

## Discipline
Public science only in this folder. Research-grade; candidate applications labelled as such; the geologist decides. Personal/relationship material is off-repo by HUF carrier-filter governance.
