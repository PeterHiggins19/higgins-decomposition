# AI-refresh narrative — 2026-05-19 conference-ready milestone

**Audience.** Any AI agent or external collaborator joining the Hˢ project on or after 2026-05-19, before CoDaWork 2026 (Coimbra, Portugal · 1–5 June 2026). This narrative captures what shifted between the 2026-05-18 state (CODA-Association folder consolidation) and the 2026-05-19 point-of-restore milestone.

**Companion document.** [`../CODA-Association/POINT_OF_RESTORE_2026-05-19.md`](../CODA-Association/POINT_OF_RESTORE_2026-05-19.md) — the canonical milestone record.

---

## The single most important change

The HTML manifold projector at `CODA-Association/CODAwork2026/data_outputs/codawork2026_projector.html` is now a **true visual aid** for compositional time-series, not a stack of indifferent radar charts. Three projection modes — **RADAR STACK**, **BARYCENTER TRAJECTORY**, **BARYCENTER-ALIGNED** — are now the canonical Hˢ visualization standard for compositional data on the simplex. The projector consumes engine-derived ILR-Helmert PCA barycenter coordinates so its BARY and ALIGN modes match the manuscript's Fig 6 navigation chart exactly.

Test case: Japan 2014. In BARY mode, the plate-centre slides outward — the multi-year reorganisation following Fukushima registers visibly. In ALIGN mode, the polygon shape shifts toward solar and renewables — the post-shock absorption registers as pure structural variation around the year's own centroid. The CoDa-correct story is on the screen.

## The engine version policy under conference lockdown

Critical for any AI agent touching the project before the conference:

| Layer | Version | Status |
|---|---|---|
| Engine source — `HCI-CNT/engine/cnt.py` | **v3.2.0** (schema 3.2.0) | Current. Adds `compute_navigation_2d()` and a new top-level `navigation_2d` payload block. |
| R port — `HCI-CNT/engine/cnt.R` | v3.1.0 | Pending v3.2.0 port — queued for post-conference parity work. |
| CoDaWork 2026 corpus — `CODA-Association/CODAwork2026/data_outputs/per_country_json/cnt_v3/` | **v3.1.0** | **LOCKED. Not regenerated.** The conference talk deck, manuscript, supplementary, and cinema scroll all cite engine v3.1.0 for this corpus. |
| Projector inline data | v3.1.0 base + v3.2.0-equivalent `bary_xy` | The CLR/norm arrays are v3.1.0. The `bary_xy` arrays were produced by `outputs/regen_baryxy.py` — a pure-stdlib sidecar that applies the same ILR-Helmert PCA math the engine v3.2.0 would emit, but reads the v3.1.0 JSONs. |
| Manuscript engine citations | v3.1.0 | Unchanged. The v3.2.0 functionality is referenced only in the projector info panel and in this document. |

**Rationale.** Bumping the engine source captures the new function in the canonical engine code (where it belongs). Pinning the corpus to v3.1.0 means no conference artefact has to be regenerated, re-hashed, or re-validated under lockdown. The projector consumes v3.2.0-equivalent geometry without requiring the engine to run a fresh pass over the corpus.

## The three-mode projection standard

Adopted as canon 2026-05-19. Every Hˢ compositional time-series visualisation going forward (post-conference) should support these three modes:

### Mode 1 — RADAR STACK (default)
- Plate centre fixed at (0, 0, z(t)) for every year.
- Carrier j sits at fixed angle θ_j = (j/D)·2π − π/2.
- Vertex radius r_j = R·(0.1 + 0.9·η_j), where η_j is the min-max-normalized CLR for carrier j across the trajectory.
- Use: at-a-glance reading of which carriers swelled when.

### Mode 2 — BARYCENTER TRAJECTORY (click BARY)
- Plate centre at b(t) = PCA₂( Vᵀ·CLR(t) − μ ) · 0.85R, where V is the Helmert-orthonormal basis.
- Spine bends through space, tracing the composition's trajectory on the simplex's principal 2-D subspace.
- Centroid trail drawn through consecutive plate-centres; current year highlighted gold.
- Use: the CoDa-native "where is the composition going" question.

### Mode 3 — BARYCENTER-ALIGNED (click ALIGN)
- Plate centre stays at (0, 0, z(t)); polygon vertices shifted by −b(t).
- Barycenter trajectory mathematically forced onto the central z-axis.
- What survives in the polygon shape is the pure structural variation around each year's own centroid.
- Use: the standard CoDa "centred" view — every composition observed relative to its own geometric centre.

### SHOCK overlay (combinable with any mode)
- Polygon outline tints red proportional to the Aitchison-step distance from the previous year, scaled to the country's maximum step.
- Quiet years stay in the country's base colour; external-shock years light up.
- Precomputed per dataset on load.

### Variance captured by the 2-D PCA projection

The 2-D barycenter projection is essentially lossless for several of the EMBER countries:

| Country | PC1+PC2 |
|---|---|
| World | 99.8 % |
| USA | 99.9 % |
| India | 99.3 % |
| Japan | 99.2 % |
| China | 99.0 % |
| UK | 98.4 % |
| France | 96.7 % |
| Germany | 90.5 % |

Germany sits lowest at 90.5 % — it has the most genuinely multi-dimensional trajectory in the corpus.

## What landed today (2026-05-19)

1. **`CODA-Association/POINT_OF_RESTORE_2026-05-19.md`** (NEW) — the milestone document. Names the five-piece bundle (manuscript, talk deck, cinema scroll, projector, engine). Codifies the three-mode projection standard. Specifies the engine version policy under lockdown. Defines what "restore" means.

2. **`CODA-Association/CODAwork2026/VERSION_HISTORY.md`** (versions 1.7 → 1.10) — four new dated entries:
   - 2026-05-19 — Manuscript v1.3 (cover page + TOC + scientific-report layout)
   - 2026-05-19 — Projector v2.0 (three-mode standard + SHOCK overlay)
   - 2026-05-19 — Engine v3.2.0 (ILR-Helmert PCA barycenter trajectory)
   - 2026-05-19 — Point of restore: CoDaWork 2026 conference-ready

3. **README chain refreshed** —
   - `CODA-Association/README.md` (v2.0 → v2.1): adds milestone callout linking to POINT_OF_RESTORE.
   - `CODA-Association/CODAwork2026/README.md` (v2.0 → v2.1): adds "What's new" section for 2026-05-19, surfaces the manuscript working copies, updates projector description.
   - `CODA-Association/CODAwork2026/data_outputs/README.md` (v3.0 → v4.0): new "The projector — engine v3.2.0 ILR-Helmert PCA" section. Three modes documented. Variance-captured table per country. Engine version policy block.

4. **Manuscript v1.3** — added cover page (page 1) and Table of Contents (page 2). Header on every body page with abbreviated title and thin grey rule. Footer with page numbers and author/conference attribution. Cramped 4-column repository-references table replaced with vertical entry blocks. Colour-key table Notes column widened. Equation font reduced to 22pt to prevent margin overflow. Working copies of `.docx` and `.pdf` now live inside `CODA-Association/CODAwork2026/` alongside the talk deck.

5. **Engine v3.2.0** — `cnt.py` bumped from 3.1.0 to 3.2.0 (schema also 3.2.0). New `compute_navigation_2d(ilr_matrix)` function computes the ILR-Helmert PCA barycenter trajectory and emits a `navigation_2d` block in the run payload. Backwards-compatible (every v3.1.0 field is unchanged). Wired into `cnt_run()`.

6. **Projector v2.0** — three modes (RADAR / BARY / ALIGN) plus SHOCK overlay. Live PROJECTION info panel showing the math being applied. `plateCenter()` consumes `d.bary_xy[t]` when present (engine v3.2.0 coords) and falls back to share-weighted disk barycenter otherwise. Year stripped from carrier list; year labels rotated 90° as floating slice labels.

7. **Sidecar `outputs/regen_baryxy.py`** — pure-stdlib Python script that produces engine-v3.2.0-equivalent `bary_xy` arrays from the v3.1.0 JSONs and patches them directly into the projector HTML's inline DATA. Used 2026-05-19 to populate the projector with engine-equivalent coordinates without re-running the corpus.

## Queued admin updates (not blocking conference)

The following admin-stream updates are recorded as queued; they do not affect the conference deliverables and can be applied at the next admin sync:

- **`HS_ADMIN.json`** session_log entry for 2026-05-19 milestone (engine v3.2.0 + projector v2.0 + manuscript v1.3 + milestone doc).
- **`HS_FAST_REFRESH.json`** `_meta` block — bump `engine_version` reference to v3.2.0; add milestone reference; ensure cross-AI loaders see the new state.
- **`INVESTIGATION_CATALOG.json`** new entry **INV-064** — *Engine v3.2.0 `navigation_2d` block: ILR-Helmert PCA barycenter trajectory as a downstream-visualisation primitive*. Disposition: STAGED (CANONICAL after R-port parity).
- **`cnt.R`** port to v3.2.0 — adds the same `compute_navigation_2d()` function with cross-language parity to IEEE machine-floor precision. Queued for post-conference parity work alongside the existing R-port v3.1.0 → v3.1.1 backlog.

## Recovery target

If anything between now and 1 June 2026 destabilises the visualization, the engine, or the document chain, the recovery target is the state recorded in `POINT_OF_RESTORE_2026-05-19.md`:

- Engine source at v3.2.0 with `compute_navigation_2d`.
- Conference data at v3.1.0, untouched.
- Projector with three modes (RADAR / BARY / ALIGN) and SHOCK overlay.
- Manuscript v1.3 with cover + TOC + scientific-report layout.
- Talk deck FinalTalk_2026-05-17 at 22 slides (three per-country navigation slides).
- Cinema scroll PremierDataOutput_2026-05-13 at 66 slides.
- VERSION_HISTORY.md at v1.10, README chain refreshed, CHANGELOG entry recorded.

The git SHA of the commit that lands this state is the recovery anchor. The hashes in each output JSON are the data-integrity anchor.

---

*The instrument reads.   The expert decides.   The hashes carry the receipts.   The vocabulary holds the line.*
*The mathematics is not new; the monitoring application may be.*

*Refresh narrative recorded 2026-05-19. Conference begins 1 June 2026.*
