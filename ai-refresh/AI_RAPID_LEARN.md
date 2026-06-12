# AI Rapid‑Learn — the finer details of a system outside traditional methods

*2026-06-10. A granular onboarding map for an AI (or a careful human) to learn this system fast and deeply — its **governance**, **instrumentation**, and **analysis** — including the parts that are generally invisible to traditional methods. Because the system sits outside much of current practice, this map is deliberately granular: it names the non‑obvious concepts and links the document where each is grounded. Read this after the cold‑start `HANDOFF_TO_OPUS_4.8_*.md` and `HS_FAST_REFRESH.json`; use it to go from "I know the shape" to "I know the details."*

**Canonical source‑of‑truth order (wins on conflict):** `HS_FAST_REFRESH.json` → `ai-refresh/HS_ADMIN.json` → narrative docs. Live agenda: `ai-refresh/UNIFIED_AGENDA_2026-06-10.md` (+ `HS_TRACKING_LOG.json`). Never let a synthesis doc override the JSONs.

---

## 0 · The one‑paragraph mental model
A composition is a vector of parts carrying only **relative** information (oxide fractions, energy mix, drive‑health channels, taxa abundances). Traditional tools treat the parts as independent magnitudes; this instrument treats the whole as a point in **Aitchison (log‑ratio) geometry** and reads its **dynamics** deterministically. At four parts the move is exactly a **quaternion rotation**; at higher dimension it is **tiled** from overlapping exact four‑part charts and reconstructed losslessly. Every step is **deterministic and hash‑chained**: same input → same output, with a receipt. That combination — exact, deterministic, auditable, reconstructable — is what lets the same instrument go from hand‑collected mudstone to off‑world remote sensing to medical monitoring to anything with a budget and a few components to track.

## 1 · Governance (the discipline that makes it trustworthy)
- **Claim tiers** — Tier 1 (verified/computed), Tier 2 (standard math, soundly applied), Tier 3 (to earn). Every claim carries one. → operating discipline; visible in every doc's "Claim tiers" section.
- **Honest‑broker rule** — pitch "interest expressed", never "acquired/implemented"; a divergence is a documented improvement or a defect, never silently absorbed. **Inspected ≠ executed evidence.**
- **Lockdown** — the frozen oracle engine (`HCI-CNT/engine/cnt.py`, `HCI-CNQ/engine/cnq.py`), the schemas (HUF‑STD‑001/002/003), and the INV catalog are not modified; new work is additive. → `CNTT_V4_ENGINE_DESIGN.md §0`.
- **HUF standards** — HUF‑STD‑001 (AI‑use declaration: human authorship for claims, no AI commits), HUF‑STD‑002 (Tensor Train, the 4‑link pipeline), HUF‑STD‑003. → `huf-gov/standards/TENSOR_TRAIN.md`.
- **HUF‑Gov carrier filter** — reconstructable reduction as a natural redaction boundary for need‑to‑know / withhold‑on‑distribution data; verify without exposing raw. → `collaborations/geology-wehner/00_EXECUTIVE_OVERVIEW.md §5`.
- **Provenance + journaling** — canonical hashes everywhere; journal‑as‑you‑go. → `JOURNALING_PROTOCOL.md`; tracker `HS_TRACKING_LOG.json`.
- **Commit gate** — all commits/pushes are Peter's; the §6 admin‑sync rhythm rides after each push. → `PUSH_PROTOCOL.md`, `PUSH_READY_2026-06-10.md`.

## 2 · Instrumentation (the engine, in detail)
- **The Tensor Train (HUF‑STD‑002):** `raw → L1 ingest+treat+calibrate → L2 geometry → L3 tile/atlas → L4 navigate+emit`, each link hash‑linked. → `CNTT_V4_ENGINE_DESIGN.md §3`.
- **Two engines:** the **frozen oracle** (CNT v3.2.0 + CNQ v2.0.0) is the validation baseline; the new **CN‑TT v4** (`HCI-CNTT/`) is the tile‑native successor. The oracle retires only after v4 proves parity; the interop registry then preserves its data legacy.
- **Modular sections** — every processing section is a `Stage` = a **control point** (bounded config) + a **test point** (self_test) + a **hash‑cacheable unit** (identical work is never repeated; a config change recomputes only that section + downstream). → `HCI-CNTT/MODULAR_ARCHITECTURE.md`.
- **Determinism contract** — `stable_hash` normalizes floats to a declared 1e‑12 precision so receipts match across platforms (rover ↔ ground). → same doc §3.
- **Control points & remote adaptation** — 10 bounded, whitelisted, hash‑stamped places adaptation may occur in flight (carrier set, zero‑treatment, basis, atlas/tree, fusion weights, thresholds, delta correction, freeze/rollback). Matthew supplies the geo codes; the engine supplies the *where*. → `HCI-CNTT/CONTROL_POINTS_AND_REMOTE_ADAPTATION.md`.
- **Interop registry** — version routing + per‑pair hash‑certified transforms so any v4+ engine reads any other; lossy‑up ⇒ `RE_RUN_FROM_SOURCE` (never faked). → `ENGINE_INTEROP_REGISTRY.md`.
- **Chain completeness** — what's built vs the gaps (calibration, adapters, streaming, input‑uncertainty propagation, FDIR, schema, anti‑spec). → `CNTT_CHAIN_COMPLETENESS_MAP.md`.
- **Verification quick‑start (run these):** `python HCI-CNTT/engine/self_test/run_self_test.py` (kernel: quaternion exactness, lossless tiling, D=16‑from‑D=4, determinism) and `…/modular_self_test.py` (sections = test points, cache, delta isolation). Real‑data proof: `experiments/backblaze_v4_parity_2026-06/bb_parity.py` (v4 vs oracle, **Tier‑A bit‑identical**).

## 3 · Analysis (what the instrument actually reads)
- **Geometry:** closure → CLR → Helmert‑ILR; **radial** = ‖ilr‖ (magnitude of compositional change).
- **The navigation family (per step):** **K_eff = exp(entropy)** (effective number of carriers / concentration), **Aitchison norm & step** (compositional distance), **TV distance**, **higgins_scale + ring class**, **helmsman** = `argmax|Δclr|` (which carrier is steering the change), **bearing** (atan2‑stable), **angular velocity** (the any‑dimension stable angle), **κ_HS**, **s_j sensitivity**, **concentration regime** (tightening / loosening / **deceptive** / stable), **regime boundaries**. → `HCI-CNTT/engine/navigate.py`; oracle definitions in `HCI-CNT/engine/cnt.py`.
- **CNQ‑tiling / faceted read:** overlapping exact D=4 quaternion charts reconstruct any‑D move losslessly (lossless **iff** the part co‑occurrence graph is connected). → `collaborations/geology-wehner/CNQ_TILING_METHOD_AND_PROOF.md`.
- **The novel core (cited & confirmed):** the **quaternion reading of a composition** (ILR→S³=SU(2)) — see the prior‑art map and contribution statement for exactly what is new vs prior art (Greenacre, Singer/Fiedler, LTSA/Brand, PhILR). → `CNQ_TILING_PRIOR_ART.md`, `CNQ_TILING_CONTRIBUTION.md`.

## 4 · Why it's invisible to traditional methods (and why that raises the documentation bar)
Traditional analysis reads **magnitudes** and reaches for **statistics**; it cannot see, deterministically, *which carrier is steering*, *concentration tightening while motion stays quiet* ("deceptive drift"), or the *exact rotational structure* of a four‑part move — and it cannot give a bit‑reproducible receipt for any of it. This instrument does. A reviewer therefore cannot fall back on familiar intuition; the documentation *is* the means of understanding. That is why every concept above is named and linked, every claim is tiered, and every change is journaled in lock‑step.

## 5 · The mission‑critical span (one instrument, many budgets)
Hand‑collected **mudstone** chemostratigraphy (the Frielingen‑9 demo) → field **geosensing** (rover/phone multi‑sensor fusion) → **off‑world remote sensing** (flight‑spec suite, control points, redundancy) → **medical** monitoring (research‑only; blood‑gas D=4 is CNQ‑native) → **energy/markets** (EMBER, deceptive‑drift) → **anything with a budget and a few components to track**. The common thread: a few parts whose *relative* behavior over time carries the signal, read deterministically with a receipt.

## 6 · Gotchas a new AI must know (or it will go wrong)
- **Stale‑mount:** the sandbox serves truncated sizes for the big admin JSONs (`HS_ADMIN.json`, `HUF_ADMIN.json`), so `json.load` falsely fails mid‑file. The Read tool is authoritative; validate JSON on Peter's machine. → `AI_AGENTS.md §2.1`.
- **Mount can't delete directories** (e.g. `__pycache__`, empty folders) — gitignored anyway; Windows‑side cleanup.
- **Don't edit the frozen oracle, schemas, or INV catalog** — additive only.
- **`__pycache__`/`*.pyc` are gitignored** — never commit them.
- **The differential‑geometry tower** (curvature/holonomy/Chern‑Simons/Berry/instanton) and the **transcendental‑constant "findings"** are **quarantined** — out of all claims until earned / not publishable. → `papers/FINDINGS_INVENTORY_2026-06-10.md`.

## 7 · The AI‑assist path (distributed knowledge nodes)
Folders that matter now carry a small local **`AI_ASSIST.json`** node — the *specific* knowledge of that topic plus a link **up** to this chain — so an AI (or its **bring‑your‑own‑AI** owner) can self‑onboard on a topic in seconds and climb to the full picture only as needed. Knowledge is distributed to the edge; the control system stays single and structured (the source‑of‑truth order in the header is unchanged — nodes link up, the centre never has to track down). This is the distributed form of *this* map. **From now on, a new topic folder gets a node.** → `ai-refresh/AI_ASSIST_PATH_PROTOCOL.md` (the convention + `hs_ai_assist/1.0` schema; seed nodes under `industrial-instruments/`).

*Read the docs this links to in priority order, run the three self‑tests, and you will know the finer details. The instrument reads. The expert decides. The hashes carry the receipts.*
