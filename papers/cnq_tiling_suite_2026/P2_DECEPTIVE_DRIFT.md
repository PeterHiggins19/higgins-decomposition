# Deceptive drift: detecting concentration that hides behind quiet compositional motion

**Scaffold — 2026-06-10. For HUF AI Collective review. Gate before submission: choose a defensible null model (open question Q3).**
**Author:** Peter Higgins. Human authorship for all claims; AI‑assisted per HUF‑STD‑001.

---

## Abstract (draft)

In a compositional time series, concentration can increase steadily while the step‑to‑step composition barely moves — the system tightens without any loud transition. We define **deceptive drift**: an interval where the effective number of categories (K_eff = exp(Shannon entropy) on the closed composition) declines while the total‑variation step distance stays below the series median. We give an operational detector, demonstrate it on the EMBER national electricity‑generation corpus (the signature reproduces in 5 of 9 countries, 2001–2025), and position it carefully against existing compositional monitoring. The contribution is narrow and specific: monitoring compositional series in log‑ratio geometry with change detection and component‑level attribution already exists; what is new is fusing a *concentration trend* and a *movement‑magnitude trend* into a single divergence detector — a construction we could not find named anywhere.

## 1 · Introduction (incl. CoDaWork mention)
- The problem: dangerous structural change that does not announce itself as a large step. Energy‑mix and market‑share examples.
- **CoDaWork 2026 mention (one line):** the deterministic compositional‑navigation work presented at CoDaWork 2026 surfaced this signature in energy data; the high‑dimensional follow‑on is treated separately (P1).

## 2 · Prior art — what exists, and the precise gap (cite generously; do NOT over‑claim)
Honest framing established by a dedicated prior‑art search (2026-06-10):
- **Aitchison‑geometry monitoring with change detection already exists:** CoDa statistical‑process‑control charts — MEWMA‑CoDa, CUSUM‑CoDa, Hotelling‑T²‑CoDa, SVDD‑MEWMA‑CoDa (Tran et al., 2017–2025), including component‑level fault diagnosis. → cite as the closest C1+C2(+partial C3) cluster.
- **Online compositional change‑point detection exists:** Prabuchandran et al. (2021, *Applied Intelligence*); Fisher et al. (2022, *AOAS*); Liu & Andrews (2024, arXiv:2402.18130). → cite.
- **Component‑level attribution of compositional shifts exists:** directional‑shift Dirichlet‑ARMA with break intervention (2026, arXiv:2601.16821); coda4microbiome balance selection (Calle & Susin 2023). → cite.
- **Concentration/diversity trends exist** (Herfindahl–Hirschman, Shannon/inverse‑Simpson over time) in economics and ecology. → cite.
- **The precise gap:** none of these fuses a *concentration trend* and a *movement‑magnitude trend* into one divergence detector; the "deceptive‑drift" signature (K_eff down ∧ TV below median) is unnamed. *Frame the novelty exactly here — not as "we invented compositional change monitoring."*
- Clarification for the record: Egozcue & Jarauta‑Bragulat (2014) is "Differential Models for Evolutionary Compositions" (forecasting; no change detection); the compositional‑ARIMA line is modeling/forecasting, not detection.

## 3 · Method
- Definitions: K_eff = exp(H); TV = ½Σ|pₐ−p_b|; the regime tagger (tightening / loosening / **deceptive** = tightening ∧ TV ≤ series median / stable), threshold on K_eff year‑over‑year change.
- The detector and its decision rule; carrier‑level attribution (which parts drive the tightening).
- Determinism + provenance (shared with the CN‑TT engine, P3).

## 4 · Results
- EMBER 9‑country, 2001–2025: deceptive‑drift signature in 5 of 9 (INV‑051); the metric‑invariance check (TV vs Aitchison agree on hit/miss across the shock‑candidate steps; INV‑050) as a robustness result.
- The p‑value result (p≈0.0016 under the series' empirical‑frequency null) — **stated as an opening empirical claim, conditional on the null (see §6).**
- Zero‑treatment confirmed not to change rounded‑zero navigation (prior results robust).

## 5 · Discussion
- What the detector buys for monitoring (energy policy, market share, surveillance): catches tightening that magnitude‑based change detection misses.
- Honest scope: narrow construction; complements, does not replace, CoDa SPC.

## 6 · Open questions carried honestly (from THREE_OPEN_QUESTIONS.md)
- **Q3 (the gate): the right null model** for a simplex change‑point test — Dirichlet (parametric), permutation (disrupts temporal structure), bootstrap (heavy), compositional‑ARIMA (over‑specified), or a new simplex‑native null. **A defensible choice is required before submission**; the p‑value reads only as strongly as the null.
- **Q2:** the right *family* of valid simplex distances for verdict‑invariance (INV‑050 is pair‑tested only).
- **Q1:** the precise K_eff ↔ Aitchison‑norm relationship.

## 7 · Claim tiers
- Tier 1: the EMBER observations as computed; the unnamed‑signature finding (one prior‑art search).
- Tier 2: the gap framing vs CoDa SPC / change‑point literature.
- Tier 3: the p‑value's strength (null‑model dependent); generalization beyond EMBER.

## Acknowledgments
[Shared HUF AI Collective block — see `00_SUITE_README.md`.]

## References (seed)
Tran et al. (MEWMA/CUSUM‑CoDa, 2017–2025); Prabuchandran et al. 2021 (*Appl. Intell.*); Fisher et al. 2022 (*AOAS* 16:477); Liu & Andrews 2024 (arXiv:2402.18130); directional‑shift DARMA 2026 (arXiv:2601.16821); Calle & Susin 2023 (*BMC Bioinformatics* 24:82); Aitchison 1986; Egozcue et al. 2003; Egozcue & Jarauta‑Bragulat 2014 (*Math. Geosci.* 46:381); Herfindahl–Hirschman / Shannon diversity literature.
