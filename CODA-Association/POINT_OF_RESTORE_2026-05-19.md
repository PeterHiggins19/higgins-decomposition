# Point of Restore — CoDaWork 2026 conference-ready

**Date:** 2026-05-19
**Author:** Peter Higgins, Rogue Wave Audio · Markham, Ontario, Canada
**Scope:** the Hˢ (Higgins-Decomposition) framework as delivered for CoDaWork 2026, Coimbra, Portugal · 1–5 June 2026
**Status:** restore checkpoint — this is the state we revert to if anything later breaks

---

## What "conference-ready" means here

The framework now has every artefact a CoDaWork audience and a peer reviewer can expect: a publication-grade manuscript with cover page and TOC, a 22-slide narrative talk deck, a 66-slide cinema-scroll of the engine's raw output, an interactive HTML manifold projector that reads compositional trajectories the way CoDa specialists will recognise, and a deterministic engine pinned to a citable version. Each piece is hash-chained back to the EMBER input CSVs. Each is reproducible.

The reason this is the restore point: **the projector finally registers what it should**. Japan 2014 — the multi-year structural reorganisation that follows Fukushima — now slides the plate-centre noticeably outward on BARY and shifts the polygon shape toward solar and renewables on ALIGN. The visualization is no longer a stack of indifferent radar charts. It is a true visual aid that shows the actual compositional motion.

## The five-piece artefact bundle

### 1 — The manuscript (peer-reviewable)
- `CODAwork2026/Compositional_Monitoring_2026.docx` (25 pages, scientific-report layout)
- `CODAwork2026/Compositional_Monitoring_2026.pdf`
- Cover page, table of contents, header on every body page, page numbers, Nature-style structure: abstract → introduction → results (with Germany / Japan / UK case studies + cross-country signature) → discussion → methods → appendices A (Equations 1–10) / B (alphabetical glossary) / C (figure conventions + plate digest) → split references (28 External + 11 Hˢ Repository entries).
- Source: `papers/codawork2026/manuscript/MANUSCRIPT.md` + `build/build_docx.js`.

### 2 — The talk deck (the story)
- `CODAwork2026/data_outputs/CodaWork2026_FinalTalk_2026-05-17.pptx` (22 slides)
- `CODAwork2026/data_outputs/CodaWork2026_FinalTalk_2026-05-17.pdf`
- Story arc: the question → size-view blind spot → five viewpoints → Activation Coefficient → Germany / Japan / UK archetypes → three per-country navigation charts (one country per slide for readability) → cross-country signature → WHAT/WHY synthesis → MC-4 falsifiable claim + four defeat paths → bridge to cinema scroll → bridge to projector + Q&A → AI Use Declaration → Standard Stamp colophon.
- Source: `build_final_talk.py`.

### 3 — The cinema scroll (the engine's actual output, as a movie)
- `CODAwork2026/data_outputs/CodaWork2026_PremierDataOutput_2026-05-13.pptx` (66 slides)
- `CODAwork2026/data_outputs/CodaWork2026_PremierDataOutput_2026-05-13.pdf` (325 pages)
- Master cover + nine country sections × six plates each (cover · Stage 1 Section · system course plot · helmsman · ILR-Helmert Triplet · CNQ dashboard).

### 4 — The interactive HTML projector (live Q&A backdrop) — **upgraded to v2.0**
- `CODAwork2026/data_outputs/codawork2026_projector.html` (runs offline)
- **Three projection modes** plus a SHOCK overlay, all visible in a live PROJECTION info panel that shows the math being applied. See "The three-mode projection standard" below.
- Powered by engine v3.2.0 ILR-Helmert PCA barycenter coordinates pre-injected into the inline data. Math matches the manuscript's Fig 6 navigation chart exactly.

### 5 — The CNT engine (the deterministic computation) — **bumped to v3.2.0**
- `HCI-CNT/engine/cnt.py` (v3.2.0, schema 3.2.0)
- New `compute_navigation_2d()` function emits an ILR-Helmert PCA 2-D barycenter trajectory as a top-level `navigation_2d` block in every run output. Backwards-compatible: all v3.1.0 fields unchanged.
- The CoDaWork 2026 corpus data (`CODAwork2026/data_outputs/per_country_json/cnt_v3/cnt_*.json`) stays pinned to v3.1.0 and is **not regenerated** for the conference. The v3.2.0 functionality is consumed by the projector via the sidecar `outputs/regen_baryxy.py` script which produces identical math from the v3.1.0 JSONs.

## The three-mode projection standard

Adopted as canon 2026-05-19. The Hˢ manifold projector shows compositional time-series in one of three modes, each labelled live in the PROJECTION info panel:

| Mode | Plate centre at | What you read |
|---|---|---|
| **RADAR STACK** (default) | (0, 0, z(t)) — fixed origin | Per-year radar/spider snapshot, stacked along z. Carriers are vertices at fixed angles; radii proportional to min-max scaled CLR. Useful for "which carriers swelled when" at a glance. |
| **BARYCENTER TRAJECTORY** | (b_x(t), b_y(t), z(t)) — engine-derived ILR-Helmert PCA barycenter | The trajectory bends through space. Plate centres trace the composition's path on the simplex's principal 2-D subspace. Centroid trail drawn with current year highlighted gold. The CoDa-native answer to "where is the composition going". |
| **BARYCENTER-ALIGNED** | (0, 0, z(t)), vertices shifted by −b(t) | The barycenter trajectory is removed (mathematically forced onto the central z-axis). Pure compositional shape variation around each year's own centroid. The standard CoDa "centred" view — every composition observed relative to its own geometric centre. |

**SHOCK** is a separate overlay (not a mode): when active, each plate's outline tints red proportional to its Aitchison step distance from the previous year, so external-shock years light up in colour while quiet years stay in the country's base palette. Combinable with any of the three modes.

### Why this matters for CoDa specialists

The BARY and ALIGN modes consume **engine-derived ILR-Helmert PCA** coordinates, not the share-weighted disk barycenter that was the previous projector default. The math:

```
ILR(t)   =  V^T · CLR(t)                      # Helmert-orthonormal basis V, V^T V = I
X        =  ILR(t) − mean_t ILR(t)            # centred trajectory
PC1, PC2 =  top-2 eigenvectors of (X^T X)/(T−1)
bary_xy[t] = ( X[t]·PC1, X[t]·PC2 ) · 0.85 / max_t ‖·‖
```

This is the same projection used to render the navigation-chart figures (Fig 6, slides 12–14 of the FinalTalk). The projector now matches the manuscript's geometric story exactly, and the audience can verify the read directly on the live tool.

PC1 + PC2 variance captured ranges from 90.5 % (Germany — the most multi-dimensional trajectory) to 99.9 % (United States) across the nine EMBER countries. Lossless enough for an audience-facing tool; the projector reports the captured-variance per-country on demand.

## Engine version policy (conference-stability lock)

- **Engine source (cnt.py):** v3.2.0 — current. Adds `navigation_2d` block.
- **Conference data (CODAwork2026/data_outputs/per_country_json/cnt_v3/):** v3.1.0 — locked. Not regenerated.
- **Projector inline data:** v3.1.0 base CLR/norm + v3.2.0-equivalent bary_xy produced by the sidecar regen script from the v3.1.0 JSONs.
- **R port (cnt.R):** v3.1.0 — pending v3.2.0 port (queued for post-conference parity work).
- **Manuscript citations:** continue to cite engine v3.1.0 for the corpus; v3.2.0 is referenced only in the projector info panel and in this document.

This split preserves every word of the conference materials while allowing the projector to use the CoDa-correct geometry the audience will expect.

## Folder authority

`CODA-Association/CODAwork2026/` is the standard CoDa folder and the canonical home for all conference-current artefacts. Every piece of the bundle lives at the root or in `data_outputs/`. Outdated material is in `archive/` with structured subfolders (`talk_decks_legacy/`, `prep_docs_legacy_2026-05-13/`, `legacy_decks_external/`) and an `archive/README.md` explaining what each holds.

The companion paper lives at `papers/codawork2026/manuscript/`. The community study deck lives at `Studies/Energy_HiddenDirections_2026-05-17/`. Both are referenced from this folder's READMEs.

## Why this is a point of restore

If anything between now and 1 June 2026 destabilises the visualization, the engine, or the document chain, the recovery target is this state:

- Engine source at v3.2.0 with `compute_navigation_2d`
- Conference data at v3.1.0, untouched
- Projector with three modes (RADAR / BARY / ALIGN) and SHOCK overlay
- Manuscript v1.3 with cover + TOC + scientific-report layout
- Talk deck FinalTalk_2026-05-17 at 22 slides with three per-country navigation slides
- Cinema scroll PremierDataOutput_2026-05-13 at 66 slides
- VERSION_HISTORY.md, README chain, and CHANGELOG entries through 2026-05-19

The git SHA of the commit that lands this state is the recovery anchor. The hashes in each output JSON are the data-integrity anchor.

## Cross-references

| Layer | File |
|---|---|
| Folder map | `CODA-Association/README.md` |
| Conference folder map | `CODA-Association/CODAwork2026/README.md` |
| Presentation flow | `CODA-Association/CODAwork2026/data_outputs/README.md` |
| Version log | `CODA-Association/CODAwork2026/VERSION_HISTORY.md` |
| Engine source | `HCI-CNT/engine/cnt.py` (v3.2.0) |
| Projector | `CODA-Association/CODAwork2026/data_outputs/codawork2026_projector.html` |
| Manuscript | `papers/codawork2026/manuscript/MANUSCRIPT.md` + `output/Compositional_Monitoring_2026.docx` |
| AI refresh narrative for this milestone | `ai-refresh/AI_REFRESH_2026-05-19_conference_ready.md` |
| Investigation Catalog (queued INV-064 navigation_2d) | `ai-refresh/INVESTIGATION_CATALOG.json` |
| Experiments journal | `EXPERIMENTS_JOURNAL.md` |
| Repo CHANGELOG | `CHANGELOG.md` |

---

*The instrument reads.   The expert decides.   The hashes carry the receipts.   The vocabulary holds the line.*
*The mathematics is not new; the monitoring application may be.*

*Restore point recorded 2026-05-19. Conference begins 1 June 2026.*
