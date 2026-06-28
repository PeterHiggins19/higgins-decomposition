# Hˢ for MRI — a public support-case study: where compositional reading is a natural fit, and where it is not

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-26. Peter asked
how useful the compositional instrument is for MRI. The honest answer turns on one line: **raw k-space and raw
image intensity are NOT compositional — but many of the most clinically used MRI quantities are derived
FRACTIONS and metabolite sets, and there the fit is natural and the value is real.** This is a public
support-case study, grounded in the MRI literature, with a deterministic demonstration (`mri_compositional_demo.py`,
`af82b2b6df43cd31`). **RESEARCH / QA framing only — not a clinical or diagnostic device, not a medical claim.**
Certification is the deploying company's (Southmedic); the offer stays off the public repo. Peter is the sole
gate; nothing posted.*

---

## The honest dividing line (where Hˢ fits MRI, and where it does not)

- **NOT compositional:** raw k-space, raw reconstructed image intensity, single-channel signal. MRI intensity
  is **not quantitative** — it varies with scanner, coil, and protocol — and a single intensity is not a
  part-of-a-whole. Hˢ has nothing to add here, and we say so.
- **Compositional (the natural fit):** derived quantities that are **parts of a conserved whole** —
  - **MR spectroscopy (MRS):** the metabolite set {NAA, choline, creatine, lactate/lipid…} read as ratios; the
    field *already* works in ratios (Cho/Cr, Cho/NAA) [1][2].
  - **Multi-compartment diffusion (NODDI):** intra-neurite / extra-neurite / CSF volume **fractions that sum to
    1** [3].
  - **Brain tissue segmentation:** gray-matter / white-matter / CSF **volume fractions** [4].
  - **Dixon fat–water** and **myelin-water** fractions; perfusion compartment fractions.

Wherever the MRI quantity is a fraction-set, the compositional instrument applies unchanged — and brings four
specific advantages, each measured below.

## What it adds — four measured points (`af82b2b6df43cd31`)

1. **Exact cancellation of the multiplicative scanner/coil effect.** Multi-site scanner effects are modelled as
   **multiplicative + additive** factors, and they can *exceed the biological variation of interest* [4]. A
   compositional read (centred log-ratio) **cancels the multiplicative common-mode exactly** — measured
   residual **9×10⁻¹⁶** under random per-scan gain. This is a **deterministic, training-free complement to
   ComBat** [4] for the multiplicative component (the additive/structured part still needs ComBat's additive
   term — stated honestly).
2. **Grade separation on the metabolite simplex.** Built from published glioma signatures (high vs low grade,
   Cho/Cr ≈ 2.44 vs 1.48, Cho/NAA ≈ 2.05 vs 1.41 [1][2]), the compositional read separates the grades by a
   **12.7× margin** (between-grade vs within-grade Aitchison distance) — a locked discriminant on the
   metabolite composition.
3. **Robustness to the creatine-denominator confound.** MRS routinely divides by creatine, *assumed stable* —
   a **known confound** when Cr itself shifts [5]. In the demo a 35% Cr rise drags the **Cho/Cr ratio from 2.51
   down to 1.86** (falsely toward "lower grade"), while the **clr read** (geometric-mean reference, no arbitrary
   denominator) **barely moves** (drift 0.29 vs 1.65 for a real grade change) — ~6× more stable. Compositional
   analysis **removes the arbitrary-denominator problem** the field already worries about.
4. **Correct geometry for sum-to-one compartment fractions.** NODDI fractions sum to 1, so **raw-fraction
   correlation is a closure artifact** — measured at **−0.51 even when the compartments are independent**. The
   principled compositional measure, **log-ratio variance**, correctly separates proportional compartments
   (0.0) from independent ones (0.62). Reading NODDI compositionally avoids a real, well-documented statistical
   trap.

## The probe connection (multi-parametric "determinized lesion" lock)

The intended-probe concept carries straight over: an MRI study is itself a **survey of views** — T1, T2, FLAIR,
DWI/ADC, perfusion, spectroscopy. The same fusion logic locks the feature that is **coherent across the
parametric view-set** (the determinized lesion) rather than the brightest single-sequence artifact — the
multi-parametric analogue of "ignore the loud blob, lock the determinized spot." This is a *research* direction,
not a claim, and it inherits every fence below.

## How to test it (public datasets)

The study is built to be **re-checkable on public data**: brain-tissue GM/WM/CSF fractions (e.g. OASIS, IXI,
Human Connectome Project derivatives), NODDI compartment maps (HCP diffusion derivatives), and published MRS
metabolite tables [1][2]. Run `mri_compositional_demo.py`, get `af82b2b6df43cd31`, then point the same reader at
a public fraction table and confirm the scanner-gain invariance and the log-ratio behaviour for yourself.

## Honest scope

- **T1 (measured):** the four demonstration points — exact multiplicative-gain cancellation (9×10⁻¹⁶), 12.7×
  grade separation, ~6× robustness to the Cr confound, and the log-ratio-variance fix for sum-to-one fractions
  — are measured and reproduce (`af82b2b6df43cd31`), on **synthetic compositions built from published ratios.**
- **T2 (the support case):** that these advantages transfer to clinical MRS/NODDI/tissue-fraction workflows is a
  reasoned support case to be validated on real public data; the demo uses synthetic data from literature
  values, not patient scans.
- **The firm fences:** **research / QA only — not clinical, not diagnostic, not a medical claim.** Compositional
  reading cancels only the **multiplicative** scanner component. Raw k-space / intensity is **not**
  compositional. Certification (IEC 62304 / ISO 13485 / regulatory) is the **deploying company's** (Southmedic);
  the offer stays **off the public repo**. Any read informs an expert; it does not decide. **Nothing posted;
  Peter is the sole gate.**

## References (public literature)

1. MR spectroscopy metabolite ratios for glioma grading — Cho/Cr, Cho/NAA (high vs low grade): [PubMed 21820634](https://pubmed.ncbi.nlm.nih.gov/21820634/); [Radiation-necrosis vs recurrence meta-analysis (PMC4712150)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4712150/).
2. Clinical MRS biochemical composition of intracranial pathology: [IntechOpen chapter](https://www.intechopen.com/chapters/58817).
3. NODDI three-compartment volume fractions (intra-neurite / extra-neurite / CSF): [qsirecon NODDI docs](https://qsirecon.readthedocs.io/en/1.2.0/models/noddi.html); [intra-neurite volume fraction (PMC6331250)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6331250/).
4. Multi-site scanner harmonization (ComBat; multiplicative + additive scanner effects on GM/WM/CSF measures): [RAVEL + ComBat (PMC8820090)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8820090/).
5. Creatine-denominator confound in MRS ratios: [Metabolite ratios to assumed-stable creatine may confound quantification (ScienceDirect)](https://www.sciencedirect.com/science/article/abs/pii/S0730725X03001814).

*Cross-refs: `mri_compositional_demo.py`, `../THE_INTENDED_PROBE_a_pid_on_hs.md` (the multi-view lock),
`../instrument/INSTRUMENT_DATASHEET.md`, `../THE_HONEST_SCOPE_AND_HOME_DOMAIN.md`, `../../industrial-instruments/gas-composition-study/blood-gas/`
(the measured blood-gas thread). Southmedic offer is OFF the public repo. Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — the compositional/not-compositional line is drawn first · the four advantages are
measured and receipted · built from published ratios, validation on public data named · multiplicative-only
cancellation stated · medical research/QA only, certification the company's · the human keeps the gate.*
