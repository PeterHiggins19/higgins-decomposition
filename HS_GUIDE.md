# Hˢ — Understand & Employ (the one‑file guide)

*2026‑06‑10. The single modern entry point: what Hˢ is, what it does, why, and how to use it. The full theory and history live across the handbook volumes and a hundred papers/manuscripts; **this guide distills them into one comprehension layer and cites the authoritative sources.** Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Current engine: **CN‑TT v4** (`HCI-CNTT/`). For machine context: `HS_FAST_REFRESH.json`; for AI deep‑onboarding: `ai-refresh/AI_RAPID_LEARN.md`.*

---

## 1 · What Hˢ is (in three sentences)
Hˢ (Higgins Decomposition) is a **deterministic instrument that reads the dynamics of compositional data** — data where only the *relative* sizes of the parts carry information (oxide fractions, energy mixes, microbiome taxa, drive‑health channels, anything that is "a few components of a whole tracked over time"). It works in **Aitchison (log‑ratio) geometry**, reads each step's structure exactly, and emits a result with a **hash receipt** — same input, same output, always. It is an *instrument*, not a statistical model: it reads structure; the domain expert decides what it means.

## 2 · The one big idea
A four‑part composition has exactly three log‑ratio degrees of freedom — the dimension of a **quaternion rotation** — so a four‑part move can be read **exactly** as a rotation (bearing, dominant driver, reversal). Higher‑dimensional data is handled by **tiling**: cover the composition with overlapping exact four‑part charts and stitch them on shared parts. This reconstructs the full high‑dimensional structure **losslessly** (proven to 1,000,000 parts), deterministically, in seconds — *without* inventing a bigger algebra and *without* statistics. The phylogeny/hierarchy of the parts is used as the tiling atlas where one exists.

## 3 · What it does (capabilities, plainly)
- **Navigation read** — per step: effective diversity `K_eff = exp(Shannon)`, the **helmsman** (which part is steering the change), regime dynamics, "deceptive drift" (concentration tightening while motion stays quiet), bearing/angular velocity, attractor fit.
- **Lossless high‑D reconstruction** — recover the full log‑ratio structure of compositions with tens to millions of parts, exactly and deterministically.
- **Self‑diagnostics (FDIR)** — with redundant channels, tell an **external** change (the world moved) from an **internal** fault (a sensor failed) and isolate the faulty channel.
- **A diagnostic code system** — every run emits machine‑readable `SS‑CCC‑LLL` codes (incl. the **automated NULL flag** when a comparison finds no separation — a finding, not a failure).
- **Operational control** — each processing stage has a state (READY/RUNNING/HALTED/…) and responds to start/halt, for embedded/flight use.
- **Provenance** — a canonical content hash at every step; bit‑for‑bit reproducible across machines.
- **Honest resolvability (guard layer, 2026‑06)** — the engine now reads *the boundary of what it can resolve*: it **holds** instead of naming a noise leader at rest (`HM‑NUL‑WRN`), flags ties and rank‑collapse and high‑sparsity, ties down near‑zero drift with a self‑calibrating **hold‑lock** (discovers its own noise floor), and — only behind mandatory **breakers + e‑stop** — can close a control loop (`SafeLoop`). Full list: `HCI-CNTT/ENGINE_CAPABILITIES_DELTA_2026-06.md`.
- **Static‑only mode (no dynamics forced)** — if your data is a single snapshot / cross‑section, or you just want standard CoDa, the atlas Stage‑2 produces the **standard static apparatus** (ternary, CLR biplot, variation matrix, scree, balance dendrogram) under a `coda_standard/` key — *the dynamic layer is offered, never imposed* (see `onramp/`).

## 4 · Why it matters
Most high‑dimensional compositional tools reach for **statistics and lossy reduction**; they discard information and are not bit‑reproducible. Hˢ is the opposite: **deterministic, lossless, and auditable**, and it reads things traditional magnitude/statistics methods cannot see deterministically — *which* part is steering, concentration tightening behind quiet motion, the exact rotational structure of a move — each with a receipt. That makes it suitable from a notebook to **mission‑critical and flight systems**: hand‑collected mudstone → field geosensing → off‑world remote sensing → medical/microbiome monitoring → energy/markets → anything with a budget and a few components to track.

## 5 · How to use it (the practical core)

**Install:** `pip install numpy scipy` (plus `pandas` for some adapters, `pyreadr` to read R `.rda` data).

**Run (one command):**
```
python HCI-CNTT/run_cntt.py  <composition.csv>  -o out.json
```

**Input** — a CSV: **first column = a row label** (a time index, depth, or sample id), **remaining columns = the parts** (carriers). Values are counts or amounts; the engine closes them to a composition and treats zeros automatically. Rows are read in order (so for a *trajectory*, order them by time/depth).

**Output** — `out.json`, with these blocks:
- `atlas` — `lossless` + `reconstruction_max_err` (confirms the high‑D read is exact) ;
- `navigation` — per‑step `k_eff`, `helmsman`, `tv`/Aitchison step, `regime` tags, and series `regime_boundaries` ;
- `helmsman_family`, `attractor_fit`, `depth_tower` — the dynamic diagnostics ;
- `stages` + `navigation_2d` — pairwise/PCA views (auto‑omitted above D≈64) ;
- `diagnostics.cntt_content_sha256` — the run's receipt.

**Read the codes (the fast way to understand a run):**
```python
from engine import codes, run_cntt
payload = run_cntt.run("data.csv")
report  = codes.generate_codes(payload)        # SS-CCC-LLL codes + structural modes
# compare two groups -> automated NULL/SEP flag:
cmp = codes.group_separation(closed_comps, labels, metric="k_eff")
report = codes.generate_codes(payload, comparison=cmp)
```
Key codes: `L3‑LSL‑INF` lossless · `L4‑RGB‑DIS` regime shift(s) · `DX‑SEP‑DIS` groups separate · **`DX‑NUL‑DIS` no separation (advance via a targeted signature)** · `SK‑INT‑ERR` internal fault (channel isolated) · `RP‑SHA‑INF` the hash. Full table: `HCI-CNTT/CNTT_DIAGNOSTIC_CODES.md`.

**Interpret it (the discipline):** `K_eff` is effective diversity (how many parts effectively matter); the **helmsman** names the part driving each move; **regime boundaries** mark where the system shifts; the **null code** says "the global read doesn't separate these — look for a specific balance." Hˢ gives you the geometry and the flags; **you (or the domain expert) assign the meaning.** Every claim should carry its tier (verified / standard / to‑earn).

## 6 · The map — where the authoritative detail lives
This guide is the front door; the depth is here:
- **Engine (current):** `HCI-CNTT/CNTT_COMPLETE_SPECIFICATION.md` (the full spec) · `MODULAR_ARCHITECTURE.md` · `CNTT_DIAGNOSTIC_CODES.md` · `CONTROL_POINTS_AND_REMOTE_ADAPTATION.md` · `SELF_DIAGNOSTICS_AND_LIFECYCLE.md`.
- **Space & flight:** `SPACE_READINESS_AND_CHALLENGE.md` (the space‑readiness arc + the open challenge — deterministic Earth/space twin studies for any composition) · `collaborations/geology-wehner/GEOSENSING_FLIGHT_ROADMAP.md` · `collaborations/geology-wehner/flight_spec_suite/`.
- **Method & proof:** `collaborations/geology-wehner/CNQ_TILING_METHOD_AND_PROOF.md` · `HIGHD_DETERMINISTIC_SCALING.md` · `CNQ_TILING_PRIOR_ART.md` · `CNQ_TILING_CONTRIBUTION.md`.
- **Theory & operations (deep handbook):** `HCI-CNT/handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md`, `VOLUME_2_PRACTITIONER_AND_OPERATIONS.md`, `VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md`, `VOLUME_4_QUATERNION_VIEW.md`; `docs/Hs_Applications_Guide.md`, `Hs_Architecture_Overview.md`, `Hs_Learning_Path.md`.
- **Evidence:** `experiments/backblaze_v4_parity_2026-06/` (v4 = old engine, bit‑identical on real data) · `experiments/cnq_tiling_highd_2026-06/` (scaling to 10⁶) · `collaborations/microbiome/` (real microbiome) · `collaborations/geology-wehner/demo_frielingen9/` (mudstone).
- **Live state & plan:** `HS_FAST_REFRESH.json` (source of truth) · `ai-refresh/UNIFIED_AGENDA_2026-06-10.md` · `ai-refresh/HS_TRACKING_LOG.json` · `ai-refresh/AI_RAPID_LEARN.md`.

## 7 · Governance & scope (the operating terms)
- **Claim tiers** on everything: Tier 1 (verified/computed), Tier 2 (standard math, soundly applied), Tier 3 (to earn).
- **Honest‑broker:** results are reported straight — including nulls; "interest expressed," never "acquired."
- **Determinism + provenance:** no statistics in the science path; a hash receipt at every link (HUF‑STD‑002 Tensor Train).
- **Data scope:** Hˢ is the **instrument**; datasets and their domain interpretation belong to their owners — we do not redistribute others' data.
- **AI use:** developed with the HUF AI Collective per **HUF‑STD‑001**; human authorship for all claims; no AI commits.
- **Communications:** per **RWA‑001** — correspondence to `PeterHiggins@RogueWaveAudio.com`, Rogue Wave Audio / Binaural Test Lab, Markham, Ontario, Canada.

## 8 · Lineage (one paragraph)
Hˢ grew from acoustics and control engineering, not statistics: **DADC** (diffraction apportionment — the first natural simplex constraint, Binaural Test Lab) → **Higgins Operator H₁** → **HUF** (governance + carrier filter) → **Hˢ** (Higgins Decomposition) → **CNT** (Compositional Navigation Tensor) → **CNQ** (Compositional Navigation Quaternion) → **CN‑TT v4** (the tile‑native engine). That origin is why Hˢ is an *instrument with receipts* rather than a statistical procedure. Full lineage: `HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md`.

## 9 · Engine status
- **Current engine:** `HCI-CNTT` **v4.0.0** (tile‑native). Run it; build on it.
- **Frozen oracle (archived, past reference only):** `HCI-CNT` (CNT v3.2.0) + `HCI-CNQ` (CNQ v2.0.0). v4 reproduces their entire output bit‑for‑bit (certified on real Backblaze data). They are kept as the validation reference; corpus‑wide re‑validation (the parity harness) is the one open verification step.

## Claim tiers for this guide
- **Tier 1:** the engine capabilities and run instructions are implemented and verified (self‑tests + Backblaze parity + real microbiome run).
- **Tier 2:** the distillation and the map to authoritative sources.
- **Tier 3:** completeness — this guide summarizes; the cited documents are authoritative, and a few (corpus‑wide parity, the per‑domain wrappers) remain in progress.

*The instrument reads. The expert decides. The hashes carry the receipts. Start here, then follow the map.*
