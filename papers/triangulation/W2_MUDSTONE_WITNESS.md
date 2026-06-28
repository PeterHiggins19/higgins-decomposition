# Witness II — Deep time: a Cretaceous mudstone reads exactly, and shows where the coarse view loses the message

### (Triangulation series, Witness II of three; self-contained — assumes no prior reading)

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-22. The
second of three independent witnesses to one compositional law. **Self-contained**: it restates the whole
construction from the ground up. The foundation courses (§2–§5) are cut to the **same dimensions** as the
other two witnesses — the fit, not the filler, is the point. Honest-broker tiered; real data, read and never
copied; deterministic and hash-receipted. Source: `collaborations/geology-wehner/`. Nothing posted; Peter is
the sole gate.*

---

## Abstract

We read a real Lower-Cretaceous mudstone geochemical series (Frielingen-9, PANGAEA) as a **composition** —
oxide and element fractions of a conserved whole — and find the same compositional law a living microbiome
obeys (Witness I), now in deep time. At full resolution (`D=6`) the read is exact, deterministic, and
hash-receipted; it resolves ≈2.23 effective directions and 12 regime boundaries down section, steered by the
Zr/TOC antagonism against a carbonate background, and the entropy-invariant (EITT) test certifies it as
**within analysable structure**. Amalgamated to three macro parts (Detrital · Carbonate · Organic), the same
data drops to ≈1.65 effective directions and EITT returns **boundary**: the coarse view has *lost* the
within-detrital structure the relational full read holds — the identical seam Witness I measured as "diversity
is null while the ratios are informative." A second, independent grain-size read of the same formation
reconstructs losslessly (≈3.6×10⁻¹⁵). The domain is **located 3/3** under our own triangulation method, and
the instrument honestly reports the altitude at which its own coarse reading reaches the edge of what it can
certify. A deep-time natural system, read deterministically, **independently requires the relational reading**
— the second of three witnesses.

## 1. The claim, in this domain (the apex)

> A mudstone's geochemistry is a composition: oxide and element fractions that sum to a whole. If its
> down-section message — the changing balance of detrital input, carbonate, and organic matter — lives in the
> **relationships between components**, then an exact relational reading will resolve structure that a coarse
> or aggregate view discards, and the instrument will be able to say *where its own reading stops being
> trustworthy.* We test exactly this.

## 2. The bedrock: what a composition is (matched course, restated)

A composition `x=(x₁,…,x_D)` carries only relative information; closed to a constant sum it lives on the
simplex with the Aitchison geometry \[Aitchison 1986; Egozcue et al. 2003\]. Its coordinates are log-ratios:
`clr(x)=log x − mean(log x)`, and the isometric `ilr(x)=clr(x)·Hᵀ` with `H` a Helmert orthonormal basis — an
**exact bijection** `S^{D-1}→ℝ^{D-1}` that loses nothing. (Canonical: `HCI-CNTT/engine/geometry.py`.)

## 3. The exact rung and tiling (matched course, restated)

At four parts the read is exact: the three ILR coordinates are the imaginary part of a quaternion, rotated by
`q v q*` to the IEEE floor (≈1.1×10⁻¹⁶). Higher dimension is covered by overlapping exact four-part charts
reconstructed through a connected atlas; a balanced tree keeps conditioning at `O(log D)`, carrying
reconstruction to `D=10⁶` at ≈4.1×10⁻¹² (numerical, not bit-exact identity). The mudstone (`D=6` and `D=11`)
sits well inside the exact regime. (Full treatment: P1.)

## 4. Trust by construction (matched course, restated)

Every reading is computed by a fixed engine and stamped with a SHA-256 content receipt; identical inputs give
identical outputs and a matching hash, cross-platform (HS-EPS-1). The reads below are pinned to their hashes;
nothing depends on a seed. This is what lets the agreement *across* the three witnesses count as evidence
rather than echo.

## 5. The message is in the ratios (matched course, the theorem)

For a composition `x∈S^{D-1}` and any external or structural label `Y`, the ILR map `φ` is a bijection, so it
is a **sufficient statistic**: `I(Y;X)=I(Y;φ(X))`. For any reduction `g` (an aggregate, a coarse
amalgamation), the **data-processing inequality** gives `I(Y;g(φ(X)))≤I(Y;φ(X))` — coarsening can only lose.
The prediction for geology is specific: amalgamating the composition to fewer macro parts must *measurably
discard* structure the full read holds. §6 measures exactly that, and the loss is visible as a drop in
effective dimensionality and a change in the EITT verdict.

## 6. The measured witness (Tier 1)

**Data.** Frielingen-9, a real Lower-Cretaceous mudstone XRF series (PANGAEA); engine =
Hs-Kinematics / CN-TT. Three altitudes of the *same* data, all deterministic and hash-receipted (no invented
numbers):

| view | composition | result | hash |
|---|---|---|---|
| **A — full read** | `D=6` (SiO₂, Al₂O₃, Rb, Zr, CaCO₃, TOC) | Zr/TOC steer vs carbonate background; **≈2.23 effective directions**; **12 regimes**; EITT **within-regime** | `f40be455` |
| **B — macro read** | `D=3` (Detrital · Carbonate · Organic) | arrow Detrital↔Organic *vs* Carbonate; **≈1.65 effective directions**; EITT **boundary** | `3d568d24` |
| **C — vigilance** | EITT on each run | A sits **within** analysable structure; B sits **at the boundary** | (carried by A, B) |

**The matching seam (the joint that fits Witness I).** From the full read to the macro read, effective
dimensionality falls 2.23 → 1.65 and the EITT verdict moves from *within-regime* to *boundary*. The coarse
view has **lost** the within-detrital structure (the Zr/Rb/Si interplay) that the relational full read holds —
the same shape as a living microbiome whose disease signal is null in a scalar diversity index but strong in
the log-ratios. *The aggregate loses what the relational keeps* — measured here as a dimensionality drop and a
boundary verdict, there as an AUC gap.

**A system property, at every scale.** Both altitudes place the carbonate pole opposite the clastic–organic
pair; the detrital-vs-carbonate antagonism is therefore a property of the system, not an artifact of how
finely the elements are split — the relational structure is real and scale-stable.

**Exact and lossless.** An independent grain-size read of the same formation (`D=11`) reconstructs losslessly
at ≈3.6×10⁻¹⁵, confirming the exact-rung + tiling base on real geological data.

**Self-vigilance (the boundary, honestly).** EITT does not report a confident number at every scale; it tells
you *at which altitude its own reading is still trustworthy* — full read within structure, macro read at the
edge. This is the determinism-boundary premise in action: the instrument draws, and reports, where its exact
read stops.

## 7. Back to the apex

A deep-time mudstone — laid down over a hundred million years ago, with no possibility of agreeing with
anything by arrangement — independently exhibits the law: its message is in the relational geometry, visible
at every scale; the coarse view measurably loses it; the read is exact and deterministic; and the instrument
honestly flags where its own coarse reading reaches the boundary. This is the **second located coordinate**
of the compositional law. One witness remains (an engineered fleet); three locate it.

## 8. Honest envelope

- **Tier 1 (measured/proven):** the three deterministic, hash-receipted views; the 2.23→1.65 effective-
  dimensionality drop and the within-regime→boundary EITT shift under amalgamation; the detrital–carbonate
  system property; the lossless grain-size reconstruction; the sufficiency/DPI theorem behind the loss.
- **Tier 2/3 (not claimed):** this is a descriptive instrument reading, **not** a stratigraphic or
  paleoenvironmental interpretation; the macro grouping is the standard mudstone partition, not a discovered
  one; universality across all compositional domains is the *series'* claim, established only by the three
  witnesses together. EITT carries its own kill conditions (proportional data; sufficient carrier dimension;
  conservation, not prediction; external forcing invisible).
- **Kills.** The claim dies if the coarse amalgamation lost nothing the full read holds (it lost the
  within-detrital structure, measurably), or if a relationship-blind aggregate matched the full relational
  read.

## 9. Reproducibility

`demo_frielingen9/frielingen9_xrf_4part.csv` through the Hs-Kinematics engine — View A on the six parts,
View B on the detrital/carbonate/organic amalgamation — deterministic to the hashes above; the grain-size
read reproduces independently. Real data read from PANGAEA and never copied into the repository
(instrument-not-data).

## Acknowledgments

Developed from a body of acoustic-engineering practice; AI-assisted per HUF-STD-001. The AI collective
contributed independent cross-checks; all claims are the author's. Data: Frielingen-9 (PANGAEA); the geology
collaboration is documented at `collaborations/geology-wehner/`.

## 10. Supporting studies — the three-study trust (HUF support standard)

Two supporting studies reinforce this witness into a three-study trust:

- **Support A — independent geochemistry.** The same engine reads an independent major-oxide composition
  (ball-clay) coherently — the compositional read is not Frielingen-specific (`collaborations/geology-wehner/`,
  BALL_OXIDES).
- **Support B — regional geochemistry reproduction.** The Hs-05 regional-binning / diffraction-composition
  read reproduces the compositional structure on a separate geochemical section
  (`experiments/Hs-05_Geochemistry/`, `Higgins_Diffraction_Composition_Principle.md`).

Main + A + B = a three-study trust. Full chain: `../NINE_STUDY_TRUST_LEDGER.md`.

*Witness II of three. The aggregate loses what the relational keeps — measured in deep time, matched to the
living-system seam of Witness I, and located only when the fleet (Witness III) says the same with its own
receipts. Cross-refs: `W1_MICROBIOME_WITNESS.md`, `../COMPOSITIONAL_MESSAGE_PRINCIPLE_PAPER_SEED.md`,
`../TRIANGULATION_TRILOGY_PLAN.md`. Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — numbers cited-or-fenced · math proven + receipted · value shown · experts decide. See [`../PROOF_AND_HONESTY_STANDARD.md`](../PROOF_AND_HONESTY_STANDARD.md).*
