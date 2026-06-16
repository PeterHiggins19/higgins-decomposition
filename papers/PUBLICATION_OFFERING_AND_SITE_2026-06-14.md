# The publication offering, and how to create the site

*What can now be assembled into a harmonious, publication‑worthy body — and exactly what you need to do to put it online. Built on the honest triage in `FINDINGS_INVENTORY_2026-06-10.md` and the prior‑art notes, updated for everything this session added (the guard layer, the kinematics, the diagnosis language, the determinism/gauge‑R&R standard, the reproducibility kit, the cross‑domain demos). Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker; readiness tiered, nothing overclaimed.*

---

## Part A — the harmonious offering

The strength is **coherence**: one instrument seen from four angles, every piece reproducible from the same engine and citing the same CoDa foundations under the same honest‑broker discipline. A reviewer in any one area meets a rigorous, reproducible, honestly‑scoped body — that *coherence* is the offering.

### The five papers (one instrument, five faces)

*The coherent, successive public reading of all five — the five‑movement arc (exactness → trust → motion → character → vigilance) — is [`THE_HIGGINS_DECOMPOSITION_SERIES.md`](THE_HIGGINS_DECOMPOSITION_SERIES.md). Use it as the front matter for the site and the lay reader; the table below is the technical index.*

| | Paper | What it claims | Venue | Readiness |
|---|---|---|---|---|
| **P1 ★** | **CNQ‑tiling — the quaternion‑exact, lossless reading of compositions** | a D=4 composition's ILR ≡ a unit quaternion (S³=SU(2)); `q v q*` reads a move as exact rotation; tile + reconstruct high‑D losslessly (proven to D=1e6, IEEE floor). *Novel* (two searches, no prior art). | CoDa / applied‑math methods (*Mathematical Geosciences* or a stats/ML methods venue) | **Closest to submittable** — method + proof + kernel built (`cnq_tiling_suite_2026/`, `PAPER_1_UNIVERSAL_INVARIANCE_DRAFT.md`). Needs only the final Scholar/patent novelty pass. |
| **P3** | **The deterministic Hˢ instrument (tool/software paper)** | a deterministic, hash‑chained, gauge‑R&R≈0 compositional engine with an honest guard layer + diagnostic codes + a full reproducibility kit. | **JOSS** or **SoftwareX** (open‑source software venues) | **Strong now** — the guards, determinism/gauge‑R&R doctrine, single‑cell, R port, notebook, and designer spec all exist; needs assembly into the paper format. |
| **P4 (new)** | **Compositional kinematics — the mechanics of compositional trajectories** | velocity/acceleration/momentum/curvature/action of a composition in Aitchison geometry, as a *deterministic descriptive instrument*, with a noise‑bounded jet and the diagnosis language. | a methods / data‑science venue (+ arXiv) | **Fresh + compelling** — built + demonstrated this session; must be framed as **recognition + synthesis** (cite replicator dynamics, information geometry, CoDa per `PRIOR_ART_compositional_kinematics_2026-06-14.md`); needs write‑up + the final novelty pass. |
| **P5 (new)** | **Compositional Character Space — a cross‑domain taxonomy of compositional dynamics** | apply the engine to its own outputs (the *second‑order read*, Hˢ²): each system's invariant profile becomes a point; systems sort into four recurring *characters* whose ordering is cross‑domain‑coherent (107 systems, 13 domains); coherence is the principal organizing axis and governs the embedding dimension; "character" interpreted as an *isomorphism class*, with the exact D=4 quaternion isomorphism as anchor. | a methods / complexity / data‑science venue (+ arXiv) | **Fresh, with a built‑in integrity story** — demonstrated this session; includes a reproducible self‑correction (the ~3‑axis collapse at n=11 correcting to ~4 at n=107). Pairs with P4 (it is the layer built *on* the kinematics). Drafted: `cnq_tiling_suite_2026/P5_COMPOSITIONAL_CHARACTER_SPACE.md`; needs the isomorphism‑residual experiment + novelty pass. |
| **P2** | **Deceptive‑drift / MC‑4 monitoring** | a single divergence detector (concentration tightening while motion stays quiet); the fourth monitoring category. | applied compositional‑time‑series / monitoring note | **Needs the null model (Q3) + monthly data** — honest framing essential (cite the existing CoDa SPC/change‑point literature). |

### The backbone that makes all five credible (publish/host alongside)

- **The reproducibility kit** — `tools/CNTT_single_cell.py/.ipynb`, the **R port**, the annotated notebook, `CNTT_DESIGNER_SPECIFICATION.md` + `CNTT_PSEUDOCODE.md`, and `verify_hash_parity.py`. Open‑science gold; cite from every paper.
- **The trust/metrology standard** — `DETERMINISM_GAUGE_RR_AND_CONFIDENCE.md` + `stewardship/iso-standards/PATH_TO_A_STANDARD.md`. The "why you can trust it" layer; the standards/position white paper.
- **The cross‑domain demonstrations** — energy (Canada/Portugal), microbiome (Crohn/ECAM + the diagnosis language), geology (Frielingen), finance (sector rotation), exact‑D=4 physics. Evidence *inside* the papers; optionally a short applications paper.

### Recommended sequence
1. **Lead with P1 + P3** (closest to ready; the math + the tool, mutually reinforcing).
2. **P4 then P5 as a pair** (the kinematics is the engine; Compositional Character Space is what it reveals when turned on itself — the most arresting result, carrying its own integrity story in the n=11→n=107 self‑correction; frame both humbly, cite generously).
3. **P2 after the monthly data + null model.**
4. The standard/position piece rides alongside, aimed at the CoDa community.

*The honest discipline is the asset: set aside the transcendental‑constant cluster (FINDINGS_INVENTORY says so), cite what's prior art, claim only the instrument and its reproducible reads. That restraint is what earns the room.*

## Part B — what you need to do to create the site

The repo is already on GitHub; a publication site is low‑friction. A **deployable landing page is provided** (`../site/index.html`) — self‑contained HTML, no build step. The structure:

- **Landing** — what Hˢ kinematics is, the one‑line demo, the honest one‑sentence promise.
- **The offering** — the four papers (abstracts → preprint PDFs/arXiv links as they land).
- **Try it** — the single‑cell + notebook (a Colab/Binder badge optional), `START_HERE.md`.
- **Demos** — the cross‑domain case studies.
- **Trust** — determinism / gauge‑R&R / reproducibility kit / conformance test.
- **References & acknowledgments** — the CoDa canon and community (already maintained in the README block).

### The concrete steps (yours — the gate)

1. **Push the repo** (the `COMMIT_READY_2026-06-14.md` recipe) so all content is live on GitHub.
2. **Turn on GitHub Pages** (repo *Settings → Pages*). Simplest: serve from the `main` branch root or `/docs`. Drop `site/index.html` into the slot you choose (root, or rename to `/docs/index.html`), or push it to a `gh-pages` branch. Free, instant, no server.
3. **Mint a DOI with Zenodo** — link your GitHub repo to Zenodo, cut a GitHub *Release*; Zenodo archives it and issues a citable **DOI** (your `CITATION.cff` already supports this). This makes the *software* citable even before the papers.
4. **Preprint on arXiv** — submit **P1** first (math.ST / stat.ME). First‑time arXiv submission may need an endorsement; the draft + proof are ready. Add the arXiv link to the site.
5. **Pick the public name + (optional) domain** — lead with **Hˢ kinematics**; a custom domain (e.g., `hs-kinematics.org`) can point at GitHub Pages, or use the free `github.io` URL.
6. **The one gate before any "novel" claim** — the final **Google Scholar / patent / non‑English** novelty pass for P1 and P4 (the prior‑art notes scoped what to check). Until then, the site says "deterministic instrument + reproducible reads," not "first."
7. **Licensing is already set** — `LICENSE` (code) + `LICENSE-DOCS` (docs, CC) + `CITATION.cff`. Keep CC‑BY on the data/figures for the CoDa community's comfort.

### arXiv — account live (2026‑06‑15)

The arXiv account is **verified and active**: `PeterHiggins19`, email `peterhiggins@roguewaveaudio.com`, affiliation *Independent Researcher*, default category **cs.IT**, groups physics + math, URL the GitHub repo. The account gate is cleared; submission remains Peter's gate, after each paper's own readiness gate.

**Suggested categories (primary + cross‑list):**

| Paper | Primary | Cross‑list |
|---|---|---|
| P1 CNQ‑tiling | cs.IT | math.MG, stat.ME |
| P3 tool paper | cs.MS | stat.CO (+ JOSS in parallel) |
| P4 kinematics | math.DS | physics.data‑an |
| P5 Compositional Character Space | cs.IT | stat.ME, math.DS |
| P2 deceptive‑drift | stat.ME | cs.IT |

**Two honest notes before the first upload:** (1) **Endorsement** — a first‑time submitter in cs.IT may be prompted for an endorser unless arXiv auto‑endorses; arXiv states this at submission (a CoDa‑community or any cs.IT/stat.ME arXiv author can endorse). (2) **The novelty‑pass gate still binds** — until the Scholar/patent/non‑English pass clears for P1 (and P4/P5), the abstract claims "deterministic instrument + reproducible reads," not "first." The arXiv timestamp itself secures precedence the moment a paper posts — which is why P1‑first protects priority without any "first" wording.

**Sequence:** account ✓ → final novelty pass on P1 → post P1 (precedence) → P3 → the P4+P5 pair → P2 after its null model.

### What I can do next (additive, your gate)
- Flesh out `site/index.html` into a multi‑page site (papers, demos, try‑it pages) if you want more than the landing page.
- Assemble **P3 (the tool paper)** in JOSS format from the existing material — it's the most "ready to write" of the unwritten ones.
- Draft the **P4 (kinematics)** paper from `COMPOSITIONAL_MECHANICS.md` + the prior‑art note, in the recognition‑not‑invention framing.

*The offering is a coherent body, not a scramble; the site is a half‑day of your gate actions on top of content that already exists. Lead with the math and the tool, let the kinematics and the diagnosis language be the thing people remember, and keep the honesty that makes all of it trustworthy.*
