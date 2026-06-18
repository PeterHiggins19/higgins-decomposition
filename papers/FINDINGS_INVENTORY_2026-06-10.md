# Findings Inventory & Publishable Shortlist — 2026-06-10

*A triage of every catalogued development/finding against the now‑mapped prior‑art landscape, to get the publishable items out and organized. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Sources scraped: `docs/Hs_Discovery_Registry.md` (32 discoveries D‑01..D‑32), `papers/codawork2026/planning/NAMED_FINDINGS_FOR_CODA_DISCUSSION.md` (INV‑050/051), `THREE_OPEN_QUESTIONS.md`, `PRIOR_ART_SEARCH_TARGETS.md`, the INVESTIGATION_CATALOG, and this session's CNQ‑tiling work. Two targeted prior‑art searches (this session) ground the novelty calls.*

---

## Headline

Of ~34 catalogued findings, **three are genuinely publishable** once novelty is judged honestly against prior art — and your own read ("only 2 or 3") is correct. The largest cluster — the **transcendental‑constant matches** — should be **set aside from publication** as almost‑certainly coincidental; publishing them is the fastest way to lose the credibility the rest of the work earns. A second cluster is **real but already established** (cite, don't claim). A third cluster is **valid validation evidence** that belongs *inside* the publishable papers, not as standalone findings.

---

## The publishable shortlist (the 2–3)

### P1 — CNQ‑tiling + the quaternion‑exact reading of compositions  ★ strongest
- **What:** identify a 4‑part composition's ILR coordinates with a unit quaternion on S³=SU(2) (`q v q*`) for an exact rotation reading; tile the simplex with overlapping exact D=4 charts and reconstruct the full high‑D trajectory losslessly.
- **Why publishable:** the quaternion↔composition reading is **novel** (two exhaustive searches, no prior art; nearest neighbours Birtea‑Gavra 2022 = flat group, Scealy‑Welsh = sqrt‑sphere — both cleanly distinct). The deterministic locally‑exact + lossless synthesis is a real instrument contribution.
- **Cite, don't claim:** Greenacre 2019/2020 (reconstruction from a connected log‑ratio graph), Singer 2011 + Fiedler 1973 (synchronization / Laplacian), Zhang & Zha 2004 + Brand 2002 (chart alignment), Silverman 2017 PhILR (tree balances), Aitchison/Egozcue (CLR/ILR, subcompositional coherence).
- **Venue:** a CoDa / applied‑math methods paper (e.g., *Mathematical Geosciences*, or a stats/ML methods venue). **Before submission:** the one outstanding Scholar/ADS/patent + non‑English novelty pass.
- **Status:** method + proof + engine kernel already built (`CNQ_TILING_METHOD_AND_PROOF.md`, `CNQ_TILING_CONTRIBUTION.md`, `experiments/cnq_tiling_highd_2026-06/`, `HCI-CNTT/`). **Closest to submittable.**

### P2 — The "deceptive‑drift" detector (concentration‑trend vs movement‑magnitude divergence)
- **What:** flag intervals where concentration is tightening (K_eff = exp(H) declining) while step‑to‑step compositional movement stays quiet (total variation below the series median) — INV‑050/051, the MC‑4 claim.
- **Why publishable (narrowly):** a second prior‑art search (this session) found **no work that fuses a concentration trend and a movement‑magnitude trend into a single divergence detector** — the signature is **unnamed** in CoDa, industrial ecology, nutrition surveillance, ecology, or economics.
- **Frame it honestly (this is essential):** do **not** claim "we invented compositional change monitoring." Aitchison‑geometry monitoring with change detection **already exists** — CoDa SPC control charts (MEWMA‑CoDa, CUSUM‑CoDa, Hotelling‑T²‑CoDa; Tran et al. 2017–2025), online compositional change‑point methods (Prabuchandran et al. 2021; Fisher et al. 2022; Liu & Andrews 2024), and directional‑shift DARMA with component attribution (2026). The novel, load‑bearing element is **only the specific divergence construction**. Cite all of the above generously.
- **Open caveats to carry (already honestly logged in `THREE_OPEN_QUESTIONS.md`):** the right **null model** for a simplex change‑point test (Q3 — most consequential; the p=0.0016 is an opening claim), the **metric family** for verdict‑invariance (Q2), and the **K_eff↔Aitchison‑norm** relationship (Q1).
- **Venue:** an applied compositional‑time‑series / monitoring note. **Before submission:** settle a defensible null model (Q3).

### P3 — The deterministic CN‑TT instrument as a reproducible tool  (tool/software paper, not a "finding")
- **What:** Hs/CN‑TT as a deterministic, hash‑chained, cross‑domain compositional‑navigation engine (now v4, parity‑gated against the frozen oracle).
- **Why publishable:** a legitimate **tool/software paper** (e.g., *JOSS*, *SoftwareX*) — the contribution is reproducibility + determinism + open implementation, which is real and defensible **and entirely sidesteps the numerology problem** (the tool is sound; the dubious findings stay out).
- **Caveat:** this is an engineering/reproducibility contribution, not a novel‑result paper. Strongest *after* P1 (the engine's headline capability) lands.

---

## Set aside from publication — the transcendental‑constant cluster (honest‑broker flag)

**D‑07, D‑08, D‑11, D‑13, D‑26, and the constant‑matching parts of D‑15** — "variance trajectories lock onto Euler‑family constants (2π, e^π, π^e, ln φ, 1/(e^π)) to a few ppm across 44 orders of magnitude," "Th‑232 encodes Gelfond's reciprocal," "hBN encodes ln(φ) at 12 ppm," etc.

**Why set aside (said plainly, with respect for the good‑faith work):** these are very likely **multiple‑comparisons / "look‑elsewhere" coincidences**, not physical law. With many systems × many simple closed‑form constants in {π, e, φ, 2, …} and their reciprocals/products, a 5–6‑digit match to *some* constant is expected by chance — so "no prior art found" is exactly what a coincidence looks like, not evidence of discovery. There is no proposed mechanism linking nuclear binding energy and the cosmic budget to e^π. A physics/stats reviewer would reject these, and — more costly — their presence next to the real work (P1/P2) would taint the credible findings by association.

**Recommendation:** keep them in the registry as *honestly‑labelled curiosities* ("unexplained numerical proximities; no mechanism; consistent with chance under the look‑elsewhere effect; not claimed as findings"). Do not put them in any paper, talk, or agency‑facing material as results. If you ever want to test one seriously, the only honest route is a **pre‑registered** test: fix the constant set and the systems *in advance*, define the match tolerance *in advance*, and report the false‑positive rate — which will almost certainly dissolve the effect.

---

## Real but already established — cite, do not claim as new

| Finding | Status | Established by |
|---|---|---|
| D‑03 CLR ≡ ILR basis invariance | Standard orthonormal‑basis invariance of the trace | Egozcue et al. 2003 (ILR is an isometry) |
| D‑04 tensor‑functor naturality | Categorical restatement of the same invariance | (follows from orthonormality) |
| D‑06 Aitchison–Cartesian distortion | Known: Aitchison geometry ≠ Euclidean ternary | Aitchison 1986; Pawlowsky‑Glahn et al. 2015 |
| D‑10 transfer‑entropy causal direction | Transfer entropy is established | Schreiber 2000 |
| D‑21 amalgamation non‑commutativity | Explicitly "verification of Egozcue's warning"; amalgamation theory known | Egozcue & Pawlowsky‑Glahn; Greenacre 2020 |
| INV‑050 metric‑invariance of the verdict | Pair‑tested only; TV/Aitchison agreeing on hit/miss is partly expected | (a note at most, not a paper — see Q2) |

These can appear as **cited background** inside P1/P2, framed as known results the method respects — never as contributions.

---

## Valid validation evidence — belongs *inside* the papers, not standalone

The "instrument recovers known/plausible structure" results are genuinely useful as **evidence that the tool works** (for P3, and for the geology case), but they are applications/validations, not novel findings:

- **Physics recovery (validation):** D‑12 recoil dominance, **D‑14 diagnosing a missing carrier (neutrino) from geometry alone** (a nice demonstration), D‑19 FLAG counting‑vs‑dynamics, D‑20 conservation‑law detection, D‑15/16/17/18 cosmology recovers known structure.
- **Applied/diagnostic:** D‑22 energy transition near‑geodesic (path efficiency), D‑23 Backblaze homogeneity diagnostic, D‑24 component power‑mapper (the "yeast"/SEMF power‑vs‑fraction point).
- **Geology (feed to the geology collaboration, not standalone):** **D‑25 CaO+MgO depletion dominates over SiO₂ accumulation** in differentiation — a real, domain‑checkable observation worth running by a geoscience domain collaborator as part of the geology collaboration, not published alone.
- **Framework principles (not findings):** D‑28 informational transparency, D‑29 compositional memory, D‑30 dimensional collapse (likely a 1e‑15‑floor artifact — re‑check now that zero‑treatment exists), D‑31 reversed attractor (speculative), D‑32 the 8‑day‑sprint narrative, D‑27 six‑AI collaboration (a methods/commentary piece at best, not a scientific finding).

---

## Suggested order of operations

1. **Finish P1** (CNQ‑tiling/quaternion) → run the final novelty pass → draft the methods paper. This is the flagship and is closest to ready.
2. **Tighten P2** (deceptive‑drift) → pick a defensible null model (Q3) → draft the narrow applied note with generous citation of the CoDa‑SPC/change‑point prior art.
3. **P3 tool paper** once the v4 engine reaches navigation parity (P2 of the engine build).
4. **Quarantine the constant cluster** out of all outward‑facing material; relabel in the registry as curiosities.
5. **Route D‑25** (and any other geology validation) into the geology collaboration.

## Claim tiers for this inventory

- **Tier 1 (verified):** the prior‑art findings and the novelty calls for P1 (two searches) and P2 (one search); the registry contents as scraped.
- **Tier 2 (sound judgment):** the publishable/set‑aside/established/validation classification; the numerology assessment (standard look‑elsewhere reasoning).
- **Tier 3 (to confirm):** P1's absolute novelty (final Scholar/ADS/patent pass); P2's null‑model resolution; whether D‑25 survives a domain collaborator's scrutiny.

*The instrument reads. The expert decides. The hashes carry the receipts.*
