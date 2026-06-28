# P1 on Hˢ — abstract only

*Publication model: **the full paper is posted to arXiv** (the arXiv timestamp is the authority); **this
repository carries the abstract and the reproducibility kit**, not the paper text. The arXiv link is added
here once Peter posts. Author: Peter Higgins (human authorship for all claims); AI-assisted per
HUF-STD-001. Nothing here is a priority claim beyond the public timestamp.*

---

**Tiling the Simplex: An Exact Quaternion Reading of Compositional Dynamics and Reproducible
High-Dimensional Reconstruction**

> We present a deterministic, quaternion-chart construction for reading compositional trajectories. For a
> four-part composition, the three isometric-log-ratio (ILR) coordinates are identified with the imaginary
> part of a quaternion, so that an Aitchison perturbation acts as an exact, norm-preserving rotation
> **v′ = q v q\*** on S³ ≅ SU(2), reproducing the compositional geometry to the IEEE floor (residual
> ≈ 4.4×10⁻¹⁶). For higher dimension, a composition is tiled into overlapping exact four-part charts that
> share pivot components and reconstruct the full centered-log-ratio state through a connected atlas;
> structuring the atlas as a balanced tree bounds the graph diameter to O(log D) and, with it, the
> accumulated floating-point drift — giving measured reconstruction to D = 10⁶ at ≈ 4.1×10⁻¹²
> floating-point residual (numerical reconstruction, not bit-exact identity). The construction is
> deterministic and hash-receipted: identical inputs yield identical outputs and a matching content hash
> across platforms. We provide an open reference implementation, language-agnostic pseudocode, and a
> replication kit. This is a deterministic instrument whose exactness at four parts and reproducible
> high-dimensional reconstruction are demonstrated; the work makes no priority claim beyond the public
> timestamp.

**Cross-platform conformance (HS-EPS-1).** The D=4 exactness was reproduced bit-for-bit across five
independent `float64` implementations (core receipt SHA-256 `06ccdb25…`); see
[`../../ai-refresh/HS_MACHINE_EPSILON_CONFORMANCE.json`](../../ai-refresh/HS_MACHINE_EPSILON_CONFORMANCE.json).

**What lives where**

| | location |
|---|---|
| Full paper (text, figures, references) | **arXiv** — link pending Peter's post |
| Abstract (this page) | here, on Hˢ |
| Reproducibility kit (engine, pseudocode, R port, notebook, HS-EPS-1) | the Hˢ repository |
| LaTeX source (pre-submission working copy) | `arXiv/P1_cnq_tiling/latex/` (off-repo) — the assembly that compiles to the arXiv PDF |

*Status: **OPEN to revision (2026‑06‑25)** — locks lifted across all papers per the
mature‑and‑publish‑and‑mature‑some‑more discipline; the 2026‑06‑15 approval is now a stable checkpoint, not a
freeze. Full paper assembled and compiling; the whole chain re‑runs the collective review again and again;
submission gated on Peter's post. The `latex/` source is the working copy used to produce the arXiv PDF — it is
the reproducibility artifact, not a second publication.*
