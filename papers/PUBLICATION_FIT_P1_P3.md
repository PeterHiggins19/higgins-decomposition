# Publication fit — P1 and P3 against the papers their fields already publish

*A structure-and-content benchmark: what comparable published work in each target venue looks like, what
P1 and P3 already have, and the specific gaps to close so each meets — and exceeds — what reviewers expect.
Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. Honest-broker.
Sources web-checked 2026-06-18; venue requirements are quoted from the journals' own current docs. Tier 2
(a structural benchmark, not the final Scholar/ADS novelty sweep — that remains the Tier-3 gate).*

---

## P1 — the quaternion-chart / tiling methods paper

**What it is.** An exact algebraic reading of four-part compositional change (ILR ↔ unit quaternion on
S³ ≅ SU(2)) plus a deterministic tiling scheme that carries the reading to high dimension with measured
floating-point reconstruction. Methods paper.

**Where it lands.** The natural home is **arXiv (math.ST / stat.ME)** as the timestamp, with a journal
target in the compositional-data-analysis lineage — **Mathematical Geosciences** (where Egozcue et al.'s
ILR paper itself appeared) or a CoDa-community venue. The comparable, citable neighbours:

- **Egozcue, Pawlowsky-Glahn, Mateu-Figueras & Barceló-Vidal (2003)**, *Isometric Logratio
  Transformations for Compositional Data Analysis*, **Mathematical Geosciences** 35(3):279–300 — the ILR
  foundation P1 builds the quaternion identification on. Already cited.
- **Greenacre (2022)**, *Aitchison's Compositional Data Analysis 40 Years On: A Reappraisal*
  (arXiv:2201.05197) — the current state-of-the-field reappraisal; positions exact-isometry methods against
  "quasi-isometric" pairwise-logratio alternatives. **P1 should cite and engage this directly** — it is the
  paper a CoDa reviewer will measure novelty against, and it explicitly debates whether exact isometry is
  worth its interpretive cost. P1's answer (exactness buys an *algebraic* reading, not just a statistical
  one) is a clean contribution to that live debate.
- **Aitchison (1986)**, *The Statistical Analysis of Compositional Data* — the field's origin. Cited.

**What a CoDa methods paper is expected to contain**, and P1's status:

| Expectation | P1 status |
|---|---|
| Problem in the Aitchison geometry, stated in the field's own terms | ✅ present |
| Explicit relation to ALR/CLR/ILR and prior art | ✅ §"Background and prior art" |
| The new construction, with a worked exactness result | ✅ D=4 quaternion, residual ≈4.4e-16 |
| Reproducible numerical results in a table | ✅ Table of reconstruction residuals |
| Honest scope / limitations | ✅ claim-tier section |
| **Engagement with the *current* CoDa debate (Greenacre 2022)** | ⏳ **add** — cite + one paragraph |
| **A figure that shows the construction** (atlas/diameter) | ⏳ **replace the placeholder** with the real chart-graph figure |
| **Interpretability paragraph** (the known knock on ILR is "hard to interpret") | ⏳ **add** — say plainly what the quaternion reading *means* to a domain reader |

**Meet-and-exceed for P1.** The field's recurring complaint about exact-isometry ILR is that it is
*uninterpretable* (ratios of geometric means). P1 can exceed the baseline by turning that weakness into the
contribution: the quaternion sandwich `q v q*` gives the ILR coordinates a *concrete geometric action*
(a rotation on S³), and the kinematic readouts (helmsman, arrow, regime) are the interpretation the field
says ILR lacks. State that explicitly and P1 is not "another ILR variant" but "the reading that makes ILR
legible." Add the missing figure and the Greenacre engagement and P1 is structurally complete.

## P3 — the deterministic-engine / tool paper (JOSS)

**What it is.** The software paper for the CN-TT / Hs-Kinematics engine: deterministic, hash-receipted
compositional-navigation tool with a replication kit.

**Where it lands.** **Journal of Open Source Software (JOSS)** — the right venue for a research tool, and
the one whose requirements are explicit and checkable. JOSS expectations (from the journal's current docs):

- **Format:** a single `paper.md` (Markdown) + a BibTeX file + figures, **hosted in the same Git repo as
  the software**.
- **Length:** **750–1750 words** (longer papers may be asked to trim).
- **Required sections:** Summary; Statement of need; **State of the field**; **Software design**;
  **Research impact statement**; **AI usage disclosure**; Acknowledgements; References.
- **References:** key references **including other software** addressing related needs, with **full venue
  names**, not discipline abbreviations.
- **Substance gate:** JOSS reviews the *software* (real docs, tests, an OSI license, a clear API), not just
  the paper. The paper is a thin pointer to a substantial, reviewable tool.

P3's status against that list:

| JOSS-required section | P3 status |
|---|---|
| Summary | ✅ present |
| Statement of need | ✅ present (incl. CoDaWork context) |
| State of the field / related software | ✅ §"Related work — how CN-TT differs from existing CoDa software" |
| Functionality | ✅ present |
| Design for reproducibility / portability | ✅ present (maps to "Software design") |
| Validation | ✅ present |
| Honest scope | ✅ present (good practice; exceeds the template) |
| Availability | ✅ present |
| **Software design** (named as such) | ◑ **covered under "Design for reproducibility" — rename/expand to match JOSS's section** |
| **Research impact statement** | ⏳ **add** — JOSS now asks for it explicitly |
| **AI usage disclosure** | ⏳ **add** — JOSS now requires it; we have the HUF-STD-001 disclosure ready, drop it in |
| References with **full venue names** | ⏳ **audit** the seed refs — spell out journals/conferences |
| Length 750–1750 words | ✅ ~800 words prose — in range |

**Meet-and-exceed for P3.** Two things make JOSS reviewers comfortable, and we already have both: an
**honest-scope section** (most software papers oversell; ours states limits) and a **hash-receipted
determinism contract** (most tools cannot claim reproducibility, ours proves it to a content hash). Surface
those as strengths. The work to do is administrative, not intellectual: add the three newer JOSS sections
(Software design as its own heading, Research impact, AI usage disclosure), spell out reference venues, and
— the real gate — make sure the *repository* JOSS will inspect has a visible OSI license, tests, and API
docs, because JOSS reviews the software, not the prose.

## The shared bar both must clear

- **Engage the current literature, not just the founders.** P1 → Greenacre (2022); P3 → name the actual
  competing CoDa software (robCompositions, zCompositions, compositions, easyCODA) and say what CN-TT adds
  alongside them (a deterministic, hash-receipted *navigation/kinematics* layer), not "better than."
- **Every figure readable and on-page** — see [`LATEX_ARXIV_STANDARDS.md`](LATEX_ARXIV_STANDARDS.md). P1's
  placeholder figure is the one open build item.
- **Claim discipline intact** — no "lossless"/"identity" at high D, no "first" as fact until the novelty
  pass is public. Both drafts already hold this; keep it through revision.
- **The Tier-3 gate remains:** a final Scholar/ADS/patent novelty pass and Peter's approval before either
  is posted. This benchmark is structure-and-fit, not the novelty clearance.

## What to hand back to whom

- **P1 → Claude/Peter:** add the Greenacre-2022 engagement paragraph, the interpretability paragraph, and
  the real atlas figure; then it is submission-shaped.
- **P3 → Claude/Peter:** add Software-design/Research-impact/AI-disclosure sections, full reference venues;
  confirm the repo's license + tests + API docs are visible to a JOSS reviewer.
- **State-of-field citations for both → Grok** (work order GR-1/GR-4): resolve the competing-software and
  baseline-method references to real DOIs/venues.

*Sources: JOSS submission + paper-format docs (joss.readthedocs.io); arXiv TeX submission + common-mistakes
docs (info.arxiv.org); Egozcue et al. 2003 (Mathematical Geosciences); Greenacre 2022 (arXiv:2201.05197).*
