# CNQ‑Tiling Paper Suite — 2026

> **Abstracts only.** Per `../PAPERS_LOCATION_POLICY.md`, this suite folder now holds **abstracts and review apparatus only**; the full drafts and the P1 LaTeX live off-repo in the CoWorker `arXiv/` folder. Each abstract cites its arXiv paper (once posted) and each paper cites its Hˢ work location.


*Three papers that emerged once the system "went to school" — i.e., once the prior‑art landscape was mapped and the genuinely novel contributions were isolated. Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. This folder organizes the three publishable items from `papers/FINDINGS_INVENTORY_2026-06-10.md` into draftable papers.*

---

> **Read the arc first.** The five papers form one successive story — *exactness (P1) → trust (P3) → motion (P4) → character (P5) → vigilance (P2)* — written for the public in [`../THE_HIGGINS_DECOMPOSITION_SERIES.md`](../THE_HIGGINS_DECOMPOSITION_SERIES.md). The order below is by identity number, not reading order.

## The three papers

| # | Working title | Kind | Status | Gate before submission |
|---|---|---|---|---|
| **P1** | *Tiling the simplex: an exact quaternion reading of compositional dynamics and lossless high‑dimensional reconstruction* | Methods (novel result) | **Full draft (`P1_CNQ_TILING_METHODS.md`)** — ready for collective review | Final novelty pass (Scholar/ADS/patent/non‑English) |
| **P2** | *Deceptive drift: detecting concentration that hides behind quiet compositional motion* | Applied methods (narrow novel construction) | **Scaffold (`P2_DECEPTIVE_DRIFT.md`)** | Choose a defensible null model (open question Q3) |
| **P3** | *CN‑TT: a deterministic, hash‑chained engine for compositional navigation* | Tool / software paper | **Scaffold (`P3_CNTT_TOOL_PAPER.md`)** | v4 engine reaches navigation parity (engine build P2) |

P1 is the flagship and nearest to submittable. P2 and P3 are scaffolded with abstract, outline, citations, and gating notes.

### Companion concept papers (staged here; part of the broader five‑paper offering)

| # | Working title | Kind | Status | Gate before submission |
|---|---|---|---|---|
| **P4** | *Compositional kinematics — the mechanics of compositional trajectories* | Methods (recognition + synthesis) | scaffold from `HCI-CNTT/COMPOSITIONAL_MECHANICS.md` | write‑up + prior‑art/novelty pass |
| **P5** | *Compositional Character Space — a cross‑domain taxonomy of compositional dynamics* | Methods / complexity (the second‑order read) | **Full draft (`P5_COMPOSITIONAL_CHARACTER_SPACE.md`)** — 107 systems / 13 domains, with the n=11→n=107 self‑correction | the isomorphism‑residual experiment + novelty pass |

P5 is the second‑order read built *on* the P4 kinematics (turn the engine on its own outputs); the two submit as a pair. Full picture: `papers/PUBLICATION_OFFERING_AND_SITE_2026-06-14.md`.

---

## Shared framing — the CoDaWork 2026 mention (light, honest, identical in all three)

CoDaWork 2026 (Coimbra, June 2026) is where the deterministic compositional‑navigation work (CNT/CNQ) was presented, and where the scale of fields like microbiome research made the **high‑dimensional limitation concrete**: the quaternion reading is exact only at four parts, yet real compositional problems run to thousands or hundreds of thousands of parts. That gap is the **inspiration** for this work. The honest one‑line each paper uses:

> *The exact four‑part quaternion reading presented at CoDaWork 2026 raised an immediate question — how to carry that exactness to the high‑dimensional compositions common in microbiome, geochemical, and energy data. This work is the response.*

No paper claims the tiling method itself was presented at CoDaWork; it is framed as the follow‑on the conference inspired. (Keep it to a sentence in the introduction + one line in acknowledgments.)

---

## Shared acknowledgment — the HUF AI Collective (identical block in all three)

> **Acknowledgments.** This work was developed with assistance from the HUF AI Collective under HUF‑STD‑001 (AI Use Declaration): Claude (Anthropic) as executor/test‑runner/file‑writer, ChatGPT (OpenAI) for structure and claim‑audit, Grok (xAI) as independent reviewer and prior‑art devil's‑advocate, Gemini (Google) for cross‑checking, and Copilot (Microsoft) where available. All scientific claims are human‑authored; no AI system is an author. The cardinal rule throughout was to never upgrade inspected evidence into executed evidence. The author thanks the collective for accelerating the initial concept development.

---

## Collective review — what to ask each reviewer to pressure‑test

Each paper goes to the collective for cross‑check before submission (Peter orchestrates the sessions; archive under `ai-refresh/cross_check_archive/`). Suggested assignments by each system's strength:

- **Grok (independent prior‑art / devil's advocate):** the load‑bearing one. For P1, run the final novelty pass on the quaternion↔composition reading (Scholar/ADS/patent/non‑English) and try to find a full prior‑art match for P2's deceptive‑drift construction. Failure mode to watch: stale cache.
- **ChatGPT (structure + claim‑audit):** check that every claim is tiered correctly and that no Tier‑3 statement is phrased as Tier‑1; audit the prior‑art citations for completeness and the "cite‑don't‑claim" boundary.
- **Gemini (cross‑check):** independently re‑derive the reconstruction theorem (connected log‑ratio graph → composition) and the conditioning argument (diameter → Laplacian condition number). Failure mode to watch: training‑data hallucination.
- **Copilot (gated):** re‑run the experiments from the repo and confirm the reported numbers (lossless ≈1e‑13; D=16‑from‑D=4 ≈1e‑15; tree atlas ≈4e‑12 at D=10⁶) reproduce.
- **Claude (executor):** maintain the drafts, integrate review comments, keep claim tiers honest, re‑run the parity/experiment harness as claims change.

Every divergence the collective surfaces is adjudicated the same way as the engine work: documented improvement, or a fix — never silently absorbed.

---

## Honest status line

P1 is drafted and internally grounded (its results are the measured, reproducible experiments in `experiments/cnq_tiling_highd_2026-06/`), but **not submission‑ready** until the final novelty pass clears. P2 and P3 are organized and citation‑grounded but each has a real gate (a null model; engine parity). Nothing here is submitted or sent — that remains Peter's gate, as always.

*The instrument reads. The expert decides. The hashes carry the receipts.*
