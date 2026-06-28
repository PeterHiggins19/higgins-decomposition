# Geology located — three views of the Frielingen-9 mudstone, cross-read

*The triangulation protocol ([`../../papers/TRIANGULATION_PROTOCOL.md`](../../papers/TRIANGULATION_PROTOCOL.md))
applied to the real Lower-Cretaceous mudstone XRF series (Frielingen-9, PANGAEA). Three altitudes of the
same data, then a diagnosis. All readings are deterministic and hash-receipted; no invented numbers.
Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001. Honest-broker — this is
a descriptive instrument reading, not a stratigraphic interpretation.*

---

## The three views

| View | What it reads | Composition | Result | Hash |
|---|---|---|---|---|
| **A — Navigation** | the full-resolution path | D=6 (SiO₂, Al₂O₃, Rb, Zr, CaCO₃, TOC) | Zr/TOC steer; ≈2.23 effective directions; 12 regimes; EITT **within-regime** | `f40be455` |
| **B — Structure** | the macro skeleton | D=3 macro: **Detrital** (SiO₂+Al₂O₃+Zr+Rb) · **Carbonate** (CaCO₃) · **Organic** (TOC) | arrow Detrital↔Organic *vs* Carbonate; ≈1.65 effective directions; EITT **boundary** | `3d568d24` |
| **C — Boundary / vigilance** | where the analysable structure ends | EITT entropy-invariant test on each run + deceptive-drift watch | A sits **within** analysable structure; B sits **at the boundary** | (carried by A, B) |

View B is the amalgamation the ledger flagged as the missing third leg, run once on the same data at the
exact low-D end. The macro grouping is the standard mudstone partition: siliciclastic/detrital input,
carbonate production/dilution, and organic enrichment.

## Diagnosis (the cross-read)

**Agreement → a property of the system.** Both altitudes place the *carbonate* pole opposite the
clastic–organic pair: at full D the steer is Zr/TOC against the carbonate background, and at the macro D=3
the arrow is Detrital↔Organic *versus* Carbonate. The detrital-vs-carbonate antagonism (clastic input
diluting carbonate, or carbonate diluting clastics) is therefore a **system property**, visible at every
scale — not an artifact of how finely the elements are split.

**Disagreement → scale information.** Effective dimensionality falls from ≈2.23 (D=6) to ≈1.65 (D=3 macro).
The structure the full read resolves — the Zr/Rb/Si interplay *inside* the detrital pole — is real but
*internal* to the macro skeleton; amalgamation deliberately discards it. The drop is the size of the
within-detrital story, made measurable by the difference between the two views.

**The boundary verdict carries the headline finding.** This is what geology adds that finance did not.
At full resolution EITT returns **within-regime** — the system is on solid analysable ground. Amalgamated
to three macro parts, EITT returns **boundary** — *the edge of analysable structure*. Coarse-graining a
located system can carry it to the boundary: with only three super-parts there is less internal structure
left for the entropy-invariant test to certify, so the macro view is honestly flagged as near the edge.
The instrument tells you *at which altitude its own reading is still trustworthy*, rather than reporting a
confident number at every scale. That self-vigilance is the point of keeping View C on every run.

**Cross-validated regimes.** The detrital↔carbonate antagonism survives both lenses; the finer regime
transitions (12 at full D) are lens-specific to the high-resolution view. System-wide vs lens-specific is
read directly off the agreement/disagreement split, exactly as the protocol prescribes.

## Verdict

Geology is **located, 3/3** — the second domain after finance to carry all three views on real data, and
the first to surface a **cross-scale EITT disagreement** as a finding in its own right. The instrument
that triangulates a market triangulates a mudstone; here it also reports, honestly, where its own coarse
reading reaches the edge of what it can certify.

*Reproduce: `demo_frielingen9/frielingen9_xrf_4part.csv` through the Hs-Kinematics engine — View A on the
six parts, View B on the detrital/carbonate/organic amalgamation. Deterministic to the hashes above.*
