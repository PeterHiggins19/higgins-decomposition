# P3 — CN-TT deterministic engine (abstract only)

*The repo holds the abstract; the **full paper lives off-repo** in `arXiv/P3_cntt_tool/`. NOTE: JOSS expects
`paper.md` inside the software repo at submission — when P3 is submitted to JOSS, the full draft returns to
the repo as the JOSS `paper.md`; until then the working copy is off-repo. Author: Peter Higgins; AI-assisted
per HUF-STD-001.*

**CN-TT: a deterministic, hash-chained engine for compositional navigation.**

> CN-TT (HCI-CNTT v4) is an open, deterministic engine for compositional-navigation analysis: it reads the
> geometric and dynamic structure of compositional time series in Aitchison geometry, tiles high-dimensional
> compositions with exact four-part quaternion charts (P1), and emits a canonical, hash-chained record. Its
> distinguishing properties are **determinism** (same input → same output, bit-for-bit) and **auditability**
> (a SHA-256 content hash at every pipeline link) — properties most high-dimensional compositional tooling
> does not guarantee.

**Work done in Hˢ:** the engine itself (`Hs-Kinematics/`, `HCI-CNTT/`); the 5-way machine-epsilon conformance (`ai-refresh/HS_MACHINE_EPSILON_CONFORMANCE.json`). **Full paper:** `arXiv/P3_cntt_tool/` (off-repo). **arXiv/JOSS:** link added once posted.
