# papers/flagship — flagship-paper material

Working material for the flagship publication of the Higgins Decomposition system. Holds drafts, figures, and supporting analyses that build toward the full-system paper.

---

## ⭐ Current master-standard paper

**[`GROUND_STATE_AND_TRACTION.md`](GROUND_STATE_AND_TRACTION.md) — master standard, working flagship draft v2.2 (2026-05-22, consolidated against the Rogue-Wave-Audio archive).**

v2.2 folds in the eight architectural details surfaced by the RWA cross-check: (1) the HUF-GOV/HUF-CLS fork at ADAC (§3.2 — observe or control); (2) the Paired Measurement Doctrine (§4.3 — *"one curve lies"*); (3) DADI as failure-direction diagnostic (§3.3 — the inverse map is a triage operator); (4) date precision (DADC formal paper 2024-12-05; H₁ paper 2026-02; the November 2025 Grok generalization moment where MC-4 was born); (5) the non-monotonic H₁ abstraction path (DADC simplex → H₁ abstract Hilbert → HUF back to simplex, enriched by CoDa vocabulary — §12.1); (6) the RWA `concepts/` folder anticipations of HUF concepts (`entropix/` → EITT, `regimes/` → HUF regime vocabulary, `v-infinity-core/` → V∞Core stack, `ai-reports/` → HUF `briefings/` methodology — §12.2); (7) expanded §17 acknowledgements with Grok's November 2025 role correctly attributed; (8) new §18 *"The recursion test — what v2.2 closes"* documenting that the framework was reconstructed bottom-up by AI synthesis and v2.2 is the version where the recomposition agrees with the canonical record.

969 lines / 14,232 words / 31 pages.

The first unified-formula statement of the framework's foundation. A 40-page master standard with:

- **Symbols and notation** (§1) — five formal tables covering scalars, geometric quantities, spectral and phase quantities, Hˢ system quantities, and operators.
- **The isotropic radiation ground state** (§2) — 6.02 dB as a *power-conserving* invariant; the closure constraint is on total radiated power.
- **Partitions and portions on the simplex** (§3) — DADC closure (Σ Gᵢ = c), BTL measurement table, regime classification (long / short / hybrid).
- **The geometric-frequency association** (§4) — F_c = 115/dim, ERB-rate, log-frequency carrier identity, **constant-power objective with 4th-order Butterworth crossover** (§4.2).
- **Time enters via group delay** (§5) — pure delay as uniform rotation on S³, the *traction coefficient* τ·f.
- **The unified formula** (§6) — equation (13) for the acoustic case, equation (16) closed-form total, with **six measurable quantities, one equation**.
- **Mathematical foundations** (§7) — eight formal lemmas (Closure, Wave equation + Rayleigh-Sommerfeld, Helmholtz reciprocity, Banach fixed-point convergence, ADAC contractive stability, SEA positive-definiteness + Gershgorin, group-delay-as-rotation, closure invariance under CLR) plus two master theorems (unified-formula closure, compositional generalization). Each with formal **Statement** + **Proof** + **∎** + empirical-validation paragraphs anchoring the math to thirty years of BTL measurement.
- **Traction, not stationary** (§8) — why the simplex moves.
- **Empirical history** (§9) — why the confidence is empirical, not philosophical.
- **Generalization** (§10) and **Implications for Hˢ** (§11) — recovery of CNT/CNQ engine independence, Helmsman family, and the Activation Coefficient as instances of the unified formula.
- **Lineage map** (§12), **glossary** (§13, 38 entries), **standard formulas summary card** (§14).
- **Citations** (§15) — externally peer-reviewed only (16 entries: Aitchison 1986, Banach 1922, Born & Wolf 1999, Egozcue et al. 2003, Glasberg & Moore 1990, Hamilton 1843, Hanson 2006, Helmholtz 1860, Linkwitz 1976, Lyon & DeJong 1995, Moore 2012, Olson 1969, Pawlowsky-Glahn et al. 2015, Pierce 1981, Vanderkooy 1991).
- **Repository materials** (§16) — self-hosted works separated and clearly marked as not externally peer-reviewed.
- **Acknowledgements: AI collaboration** (§17) — HUF AI Collective members (Claude, ChatGPT, Grok) and their specific contributions per HUF-STD-001 v1.1.

| File | Purpose |
|---|---|
| [`GROUND_STATE_AND_TRACTION.md`](GROUND_STATE_AND_TRACTION.md) | Editable Markdown source (v2.2) — single source of truth |
| [`GROUND_STATE_AND_TRACTION_v2.2.pdf`](GROUND_STATE_AND_TRACTION_v2.2.pdf) | PDF render of v2.2, 31 pages, 262 KB — **current** |
| [`GROUND_STATE_AND_TRACTION_v2.2.docx`](GROUND_STATE_AND_TRACTION_v2.2.docx) | Word format of v2.2 (pandoc-rendered) |
| [`GROUND_STATE_AND_TRACTION_v2.1.docx`](GROUND_STATE_AND_TRACTION_v2.1.docx) | v2.1 in the visually-styled docx-js typography (navy/gold accents, cover page, formatted equation blocks, 40 pages). Kept as the visual reference; the *content* is superseded by v2.2 |
| [`GROUND_STATE_AND_TRACTION_v2.1.pdf`](GROUND_STATE_AND_TRACTION_v2.1.pdf) | v2.1 PDF, 40 pages — visual reference; content superseded by v2.2 |
| [`GROUND_STATE_AND_TRACTION.docx`](GROUND_STATE_AND_TRACTION.docx) | v2.0 — earlier draft, preserved for lineage |
| [`GROUND_STATE_AND_TRACTION.pdf`](GROUND_STATE_AND_TRACTION.pdf) | v2.0 PDF — earlier draft, preserved for lineage |

The paper is **outside the CoDaWork 2026 conference scope** (lockdown-irrelevant; develops independently). It can be drafted, refined, and committed during the lockdown without touching any locked surface.

---

## Other flagship working drafts

| File | Status | Theme |
|---|---|---|
| [`Higgins_Decomposition_Character_Analysis.md`](Higgins_Decomposition_Character_Analysis.md) | Working draft | Character analysis of the decomposition. |
| [`Hs_Manifold_Character_Handbook.pdf`](Hs_Manifold_Character_Handbook.pdf) | Working draft | Manifold-character handbook. |
| [`Hs_Software_Handbook.pdf`](Hs_Software_Handbook.pdf) | Working draft | Software handbook. |
| [`Manifold_Characterization_by_Decomposition.pdf`](Manifold_Characterization_by_Decomposition.pdf) | Working draft | Manifold characterization. |

---

## Companion canonical material

For the canonical CNT-side material, see:

* The three handbook volumes at [`../../HCI-CNT/handbook/`](../../HCI-CNT/handbook/) (including [`ORIGIN_DADC_LINEAGE.md`](../../HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md) — the historical narrative companion to `GROUND_STATE_AND_TRACTION.md`).
* The three CoDa-community preprints at [`../../HCI-CNT/coda_community/`](../../HCI-CNT/coda_community/).
* The conference demo + talk plan at [`../../HCI-CNT/conference_demo/`](../../HCI-CNT/conference_demo/).
* The HCI-AUDIO doctrine at [`../../HCI-AUDIO/doctrine/`](../../HCI-AUDIO/doctrine/) (ERB band mapping, quaternion phase mapping, Helmsman at listening position — the modern acoustic instance referenced throughout `GROUND_STATE_AND_TRACTION.md`).
* The CoDaWork 2026 manuscript at [`../codawork2026/manuscript/`](../codawork2026/manuscript/) — first non-acoustic application of the unified formula.

---

*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*
*The simplex was already there in the 4π → 2π physics. The traction was always carried by the log-frequency carrier.*
*The lemmas were proved when the iterations converged. The confidence is empirical, not philosophical.*
