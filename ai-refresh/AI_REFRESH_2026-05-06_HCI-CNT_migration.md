# AI Refresh — 2026-05-06  (HCI-CNT folded into Hˢ)

**Engine:** cnt 2.0.4   **Schema:** 2.1.0   **Experiments:** 25 / 25 PASS
**Last validated commit on `main`:** 6f7fb26 (Validate Repository #14)

## Headline

The Compositional Navigation Tensor system, previously developed as the
standalone `HUF-CNT-System` package outside this repository, is now
folded into `HCI-CNT/` inside the Hˢ repository. CNT and Hˢ share the
same foundations (Aitchison geometry, simplex closure, the
*same input → same output → always* axiom) and the same audience.
Maintaining two separate repositories no longer made sense given how
closely the two fit together.

## What's at `Current-Repo/Hs/HCI-CNT/`

| Subfolder | Contents |
|---|---|
| `engine/`      | cnt.py + cnt.R + native_units.py + tests |
| `atlas/`       | Stage 1/2/3/4 modules + spectrum + projector + det_pdf + calibration fixtures |
| `mission_command/` | orchestrator + module registry + master_control.json |
| `tools/`       | run_pipeline.py + verify_package.py |
| `adapters/`    | 13 pre-parsers (full disclosure in Volume II §C) |
| `experiments/` | 25 reference experiments — INDEX + per-experiment input/output/journal |
| `examples/`    | quickstart + tutorials |
| `handbook/`    | three consolidated volumes (Theory / Practitioner / Verification) |
| `coda_community/` | three preprint papers + ROI ternary figure |
| `conference_demo/` | CodaWork 2026 demo package + 10-slide deck + walkthrough |

## What changed in the Hˢ top-level

1. `README.md` — added the HCI-CNT section pointing at the new
   subfolder and the three handbook volumes.
2. `EXECUTIVE_SUMMARY.md` — appended a 2026-05-06 update entry.
3. `ai-refresh/AI_REFRESH_2026-05-06_HCI-CNT_migration.md` — this file.
4. `ai-refresh/HS_MACHINE_MANIFEST.json` — pointers updated to the
   new location for engine, atlas, handbook, conference demo.
5. `ai-refresh/PROJECT_HISTORY.json` — phase appended for the
   migration.

## CNT engine + atlas current state

* Engine 2.0.4 / Schema 2.1.0 (additive `metadata.units` block).
* 25-experiment determinism gate passes byte-identical from the
  Python and R engines.
* Stage tower complete:
  * Stage 1 — per-timestep ILR-Helmert orthogonal triplet plate.
  * Stage 2 — single 28-plate report combining classical CoDa
    plates (variation matrix, biplot, balance dendrogram, SBP,
    ternary, scree, evolution-of-proportions) with CNT trajectory
    plates (course plot, polar rose, bearing heatmap, ω, helmsman,
    ring strip, lock timeline, CBS three orthogonal faces, divergence
    ranking, ω↔Hs phase plot).
  * Stage 3 — depth tower / period-2 attractor / IR class single
    report (11 plates).
  * Stage 4 — cross-dataset inference report (11 plates).
* All outputs hash-chained: every plate's footer carries
  `engine_version + engine_signature[:12] + content_sha256[:12]
  + source_file_sha256[:12] + date`.

## Three CoDa-community papers

Living at `HCI-CNT/coda_community/`:

1. **CNT_VS_CODA_BALANCE.md** — technical balance book. atan2
   simplification, three-orthogonal-views comparison, M²=I licence
   for the depth tower, performance balance with honest costs.
2. **CNT_ROI_AND_USE_CASES.md** — ROI break-even analysis with the
   time-budget composition rendered as a CoDa-style ternary
   diagram (`cnt_roi_ternary.{pdf,png}`).
3. **CNT_VERIFICATION_VALUE_FOR_CODA.md** — hash-chain proposal as
   honest-publishing infrastructure for the CoDa community,
   reframed in supportive (not adversarial) language.

All three preserve their citable form even though their content is
also inside the relevant handbook volumes.

## CodaWork 2026 talk package

Living at `HCI-CNT/conference_demo/`:

* `talk_deck/CodaWork2026_CNT_Talk.pptx` — 10-slide editable deck
  with embedded SVG sources and the regenerable `build_deck.js`.
* `CODAWORK2026_TALK_PLAN.md` — slide-by-slide plan + 8-min PDF
  demo talking points + 3-min closing on the 3D projector +
  15-question Q&A study list.
* `DEMO_GUIDE.md` — 30-minute walkthrough.
* `cnt_demo/` — self-contained demo folder (engine source,
  per-country reports, combined views, calibration, doctrine).

## Tone-flip applied

The whole CNT documentation was previously written with some
adversarial framing toward classical CoDa methods. A systematic
sweep replaced phrases like "things classical CoDa doesn't provide"
with "what CNT adds on top of the established CoDa toolkit",
"fragile" with "δ-sensitive", "tampering" with "audit drift", and
so on. The papers now read as supportive and additive, not
competitive.

## Status

* Hˢ repository is the active development line (last push commit
  `6f7fb26`, Validate Repository #14).
* CNT lives inside Hˢ at `HCI-CNT/`.
* Standalone `HUF-CNT-System` package outside the repo is archived;
  no further work happens there.
* All deferred-adapter checklist items are documented (see Volume II
  §C); 5 extended adapters built with synthetic baselines, raw-data
  swap-in paths documented.
* Hs-Lab integration plan is documented (Volume II §H) but
  implementation is a follow-on track.
* Stage 5+ exploration is open future work; the Stage 1–4 tower
  covers the v1.1.x scope.

The instrument reads. The expert decides. The hashes carry the receipts.
