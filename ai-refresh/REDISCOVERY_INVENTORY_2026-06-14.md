# Deep-Rediscovery Inventory — the answers already exist (2026-06-14)

*A map of buried/forgotten material across all repos and archives, surfaced by a deep scrape (not the top docs). Purpose: "the answers already exist, they just need rediscovery." This index makes them findable again and routes them to the PhD onramp (`Hs/onramp/`). Author: Peter Higgins (human authorship); AI-assisted per HUF-STD-001. Honest-broker; nothing moved — pointers only. Paths are workspace-relative under `Claude CoWorker/`.*

---

## A. Engine answers to resurface (already produced, filed away)

**The origin "why it works."** `_archive_2026-06-07/HUF-Project/science/coda-monitoring/ORIGIN_BRIDGE_DADC_TO_MC4.md` — the complete genealogy from loudspeaker diffraction (DADC-DADI) to MC-4: the 6.02 dB baffle-step budget = the closure constraint, the Dominance Index = the log-ratio, DADI reconstruction = EITT inversion. The single best "this was forced by physics, not invented" document. Pairs with the live `ORIGIN_BRIDGE_DADC_TO_MC4.md` at workspace root and `RWA/THE_GROUND_STATE.md`.

**EITT, fully proven and bounded (the hidden EITT canon).** `_archive_2026-06-07/HUF-Project/science/eitt/` — `EITT_ENTROPY_LANDSCAPE.md` (literature gap-map across 10 territories), `EITT_Residual_Analysis_001.json` (the *mechanism*: exp/ln duality cancels the first-order term, leaving the Jensen/Hessian second-order — VAR(1) overpredicts by ~10,000×), `EITT_Adversarial_001.json` (scored failure battery: 10/11 real pass, the synthetic non-autocorrelated cases correctly fail → the stationarity boundary), `HUF_Aitchison_Variance_Conservation_001.json` (340:1 daily→annual compression, entropy drifts 0.18%). Plus the honesty record `_archive_2026-06-11/code/analysis/honesty_tests_results_2026april9.txt` (ATK-05 white-noise, ATK-09 arithmetic-mean-also-passes — the honest scope narrowing). These are the EITT engine's own kill-tests, already run.

**The quaternion isomorphism at the IEEE floor.** `_archive_2026-06-11/Quaternion Decomposition/` — `QD_CENTRAL_CLAIM.md` ("CNT measures invariance; CNQ names the algebra it lives in"), `Hs-CMB/QD_ROUND_2_5_REPORT.md` (quaternion-sandwich = Aitchison rotation confirmed to 4.441e-16 = 2× machine-epsilon, bit-identical on Backblaze drive-failures and Planck CMB; Concept-4 spinor conjecture cleanly *falsified*), `QD_DEEPER_CONNECTIONS.md` (10 correspondences labeled isomorphism/equivalence/analogy/conjecture; atan2 = quaternion log map explains the 10⁷ stability gain), `Hs-Neutrino/QD_round_2_6_results.json` (SM neutrino oscillation → same universal P2 signature). This branch lives entirely outside the main tree.

**Cross-domain engine corpus (20+ runs, one table).** `_archive_2026-06-07/HUF-CNT-System/experiments/EXPERIMENTS_RUN_REPORT.md` — the full registry with hashes. Standouts to resurface: `reference/nuclear_semf/JOURNAL.md` (Bethe-Weizsäcker 5 terms over 76 nuclei, A=0.5995), `extended/esa_planck_cosmic/JOURNAL.md` (cosmic energy budget, 7 lock events), `domain/fao_irrigation_methods/INTERPRETATION.md` (83 countries × 3 irrigation methods — and the striking A≈0.066 amplitude match to Tappe kimberlite geochemistry across unrelated domains/dimensions), `codawork2026/ember_usa/USA_DIAGNOSIS.md` (the "DEGENERATE is a hypothesis, not a verdict" operator lesson + a real period-1 parity bug-fix).

**Pre-CoDa findings worth re-running through the engine (Generation 1).** `_archive_2026-06-07/HUF-Project/dormant/` — `deceptive-drift/EMBER_Deceptive_Drift_Analysis_v3.0.json` + `pre-coda-metrics/HUF_Acceleration_FixPoint_Analysis_v1.0.json` (the Japan **deceleration-then-Fukushima** signature — structural velocity bottoms in 2010, explodes in 2011, *before* the event; and the "freeze one carrier" fix-point method = the pre-CoDa helmsman), `pre-coda-metrics/Metric_Correction_L2_vs_TVD_v1.0.json` (the self-correction record: TVD catches distributed drift, L2 catches spikes), `pre-coda-metrics/Sufficiency_Frontier_AllAngles_v1.0.json` (forward/backward/upside-down identifiability), `science/coda-monitoring/Gold_Silver_RSM_Analysis_v1.0.json` (gold is near-isotropic, K_eff≈D=19; currency structure anti-predicts the ratio), `dormant/planck-case/` (Planck 353 GHz sky map: TV=0.0 across half-ring splits — astrophysical EITT before EITT had the name).

**The bridge job:** Generation-1 (additive/Euclidean, `dormant/`) and Generation-2 (CoDa-correct CNT engine, `experiments/`) are not yet reconciled. The highest-value re-run is the **Fukushima deceptive-drift archetype** through the current label-permutation null + the new hold-lock — does the deceleration signature survive proper Aitchison geometry?

## B. Domain-onboarding prototypes (live repo — "I have X, here is what it told me")

Every real run shares one structure: **(1)** what went in (domain, D, N, source) → **(2)** lossless error (the trust certificate) → **(3)** the helmsman (who is driving) → **(4)** regime boundaries (when it changed), often **(+)** the activation coefficient (a tiny carrier doing outsized work = early warning). These six are the cleanest self-contained "what your data tells you" documents — the prototypes for the onramp:

- **Blood/anaesthesia gas:** `Hs/industrial-instruments/gas-composition-study/blood-gas/results_real_vitaldb/REAL_DATA_RESULTS.md` (+ `cohort/COHORT_RESULTS.md`, `results_real_uq/README.md`) — O₂ the dominant driver in **13/13** real cases across two hospitals/continents, all lossless.
- **Produced water / hydrogeochemistry:** `Hs/industrial-instruments/gas-composition-study/produced-water-codawork/results_real_usgs/README.md` — 683 Williston-Basin samples; the drivers are the **minor ions SO₄/HCO₃, not the Na-Cl bulk** (magnitude misleads; ratios don't).
- **Chemostratigraphy / core geology:** `Hs/collaborations/geology-wehner/demo_frielingen9/RESULTS_Frielingen9_CNT_CNQ.md` (+ `REPRODUCE.md`, offline `frielingen9_projector.html`) — 219 mudstone samples; **trace elements Zr/Rb drive over bulk oxides**; blind CaCO₃ calibration r=+0.24; 19 regime tripwires.
- **Microbiome:** `Hs/collaborations/microbiome/results/RESULTS_real_microbiome.md` — Crohn D=48 honest null (no global separation) + ECAM infant **maturation recovered from composition alone** (ρ=0.71). Scaling: `RESULTS_microbiome_sniff.md` (lossless to D=10,000, ~7 ms).
- **Transcriptome (high-D):** `Hs/collaborations/spaceflight-glds1/README.md` — Drosophila spaceflight D=18,952, lossless 1.2e-13, honest global null (signal is sparse → pair with DE).
- **Social science:** `Studies/Religion_2026-05-14/README.md` — Pew D=7; "rise of Nones" running 10 pts ahead of projection, flagged as a 5–10× angular-velocity anomaly. *(Marked internal.)*
- **New-domain seeds:** `Hs/papers/in_progress/WETLAND_COMPOSITIONAL_ANALYSIS_RAMSAR.md` (invasive grass at 0.4% share doing 62% of structural work, **4 years before** the 5% threshold) and `IGNEOUS_DIFFERENTIATION_SEED.md` (8 completed geochem CNT JSONs in `collaborations/geology-wehner/copies/hs/cnt_results/` awaiting synthesis).

## C. Onboarding infrastructure that already exists

- **17+ distributed `AI_ASSIST.json` nodes** (root, applications/, collaborations/*, industrial-instruments/*, papers/, HCI-AUDIO/, HCI-ULTRASOUND/, HUF/*) — the bring-your-own-AI scaffold the onramp extends.
- **Multi-AI cold-start tests:** `Current-Repo/HUF/ai-refresh/test-results/` (ChatGPT/Claude/Copilot/Gemini/Grok, 2026-04-13) — record which concepts survive context compression vs. get hallucinated. Direct input to a robust intake node.
- **CoDa bridges (machine-readable):** `Current-Repo/HUF/ai-refresh/CODA_BRIDGES.json` — each HUF claim as a falsifiable CoDa-testable prediction.
- **External validation:** `DATA/HIGGINS_gold_standard_results.json` (20-dataset blind test, 85% accuracy, errors documented) and `DATA/HIGGINS_coda_eitt_integration.json` (combined-pipeline pass rates).
- **Operationally mature spec:** `Hs/collaborations/geology-wehner/flight_spec_suite/` (HGS-000…008, NASA-style ConOps→V&V) — a real deployment proposal could build on it.

## D. Routing

The onramp (`Hs/onramp/`) draws its worked examples from §B and its "why it works" credibility from §A. The Generation-1→2 bridge re-runs in §A are the next engine experiments (at Peter's gate). This inventory is the resurfacing map — promote selected items per `DOCUMENT_DISTRIBUTION` when ready; nothing has been moved.
