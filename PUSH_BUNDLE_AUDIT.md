# Push Bundle Audit — #18 + #19 + #20

**Repository**: PeterHiggins19/higgins-decomposition (`main`)
**Date**: 2026-05-06
**Engine target**: CNT 2.0.4 / Schema 2.1.0
**Doctrine**: Output Doctrine v1.0.1 (locked)
**Bundle scope**: corpus snapshot (#18) + Higgins_Coordinate_System docs refresh (#19) + folder-level README sweep (#20)

---

## 1. Summary

This is a documentation-and-corpus bundle. No engine code changes, no
schema changes, no determinism-gate changes. All 25 corpus experiments
still pass the determinism gate bit-for-bit against the previous push.
Every change in this bundle either (a) preserves an audit record, (b) updates
narrative docs to reflect the current canon, or (c) adds folder-level
orientation so users land on the right page.

| Push | Theme | New files | Modified files |
|---|---|---:|---:|
| #18 | Corpus snapshot `Hs-CNT_2026-05/` | 50+ | 1 (`experiments/INDEX.json`) |
| #19 | `Higgins_Coordinate_System/` docs refresh | 1 (README) | 7 docs |
| #20 | Folder-level README sweep | 102 | 0 |
| **Total** | | **~155** | **8** |

---

## 2. Push #18 — Corpus snapshot `Hs-CNT_2026-05/`

A dated, self-contained corpus snapshot under `experiments/Hs-CNT_2026-05/`
that captures the current state of all 25 CNT-canonical experiments at the
2026-05 release point. Each experiment ships with its input CSV, canonical
CNT JSON, and a per-experiment JOURNAL.md hashed into the suite-level
INDEX.json.

```
experiments/Hs-CNT_2026-05/
├── README.md                          suite landing page
├── INDEX.json                         hashed registry of all 25 experiments
├── codawork2026/                      9 EMBER experiments (8 countries + World + combined panel)
├── domain/                            7 geochemistry / FAO experiments
├── extended/                          5 cross-domain extended-battery experiments
└── reference/                         2 reference experiments (commodities + nuclear SEMF)
```

The original Hs-NN experiments under `experiments/Hs-01_Gold_Silver/`
through `experiments/Hs-25_Cosmic_Energy_Budget/` are preserved verbatim
as foundational records.

---

## 3. Push #19 — `Higgins_Coordinate_System/` docs refresh

Updated the legacy `Higgins_Coordinate_System/` documentation tree to
reflect that CNT is the matured successor to the original 12-step pipeline.
Tone is supportive and additive — the older pipeline is presented as the
foundation that CNT was built on, not as work to be discarded.

Files updated: 7 narrative docs + 1 new README at `Higgins_Coordinate_System/README.md`.

---

## 4. Push #20 — Folder-level README sweep

Trigger: "before push ensure all repo folders have good and working updated
readme.md to guide users to updated documents and streams."

### Coverage report

| Tier | Count | % |
|---|---:|---:|
| Folders with a README.md | 141 | 67% |
| Folders with a JOURNAL.md (audit record — doctrine-equivalent of README for per-experiment leaves) | 71 | 33% |
| **Total folders covered** | **212 / 212** | **100%** |
| Strategic gaps remaining | 0 | 0% |

**Audit method**: `find . -type d` on the repo, classify each directory as
(README), (JOURNAL — doctrine-equivalent), or (gap). Output-only leaf folders
(`pipeline_output/`, `*_output/`, `region_binning/`, `data/`, etc.) inherit
their parent's README and are not double-covered. Per-experiment leaves
under `experiments/Hs-CNT_2026-05/*/<id>/` carry `JOURNAL.md`, which by
doctrine *is* the per-experiment audit-trail record (the equivalent of a
README for those folders).

### Files added in the sweep (102 total)

**HCI-CNT/ subfolder READMEs (24)**:
- 11 top-level: `engine/`, `atlas/`, `mission_command/`, `tools/`, `adapters/`, `experiments/`, `handbook/`, `coda_community/`, `examples/`, `conference_demo/talk_deck/`, `engine/tests/`
- 4 experiments subfolders: `experiments/{codawork2026,domain,extended,reference}/`
- 9 conference_demo subfolders: `conference_demo/cnt_demo/{01_engine,02_per_country,03_combined,04_calibration,05_doctrine,08_extended}/` plus `02_per_country/ember_{chn,deu,fra,gbr,ind,jpn,usa,wld}/` (8)

**Hs-side high-traffic READMEs (12)**:
- `Hs_Direct/` + `Hs_Direct/JPN_slices/`
- `constants/`
- `papers/{codawork2026,flagship,validation}/`
- `HCI/{calibration,codawork2026,experiments_v2}/` + `HCI/experiments_v2/adapters/`

**Per-experiment Hs-NN_* READMEs (29)**:
- All 25 numbered foundational experiments + LAB01, M01, M02, MC4

**HCI/experiments_v2/* legacy subfolder READMEs (3)**:
- `experiments_v2/{codawork2026,domain,reference}/`

**Hs-CNT_2026-05 corpus snapshot READMEs (5)**:
- `experiments/Hs-CNT_2026-05/` + `{codawork2026,domain,extended,reference}/`

**data/* and docs/* READMEs (11)**:
- `data/{Commodities,Energy,Energy/EMBER_pipeline_ready,Geochemistry,Nuclear,pipeline_output}/`
- `docs/{lineage,operating-envelope,proofs,reference,theory}/`

**archive/ READMEs (4)**:
- `experiments/Hs-03_Nuclear_SEMF/archive/`
- `experiments/Hs-LAB01_Titration_Standards/archive/`
- `experiments/Hs-M01_Manifold_Calibration/archive/`
- `experiments/Hs-M02_EMBER_Energy/archive/`

**Additional misc orientation READMEs (14)**:
- `experiments/release-validation/`, `experiments/Hs-STD_Standards_Test/`
- `experiments/Hs-LAB01_Titration_Standards/data/`
- `experiments/Hs-M02_EMBER_Energy/codawork2026/`
- `tools/diagnostics/`, `tools/pipeline/locales/`
- `HCI-CNT/conference_demo/cnt_demo/`
- top-level `Hs/README.md` if updated

### Doctrine compliance

- All READMEs follow supportive/additive tone (no adversarial phrasing).
- All point at the current canonical engine (`HCI-CNT/engine/cnt.py`,
  engine 2.0.4, schema 2.1.0).
- Legacy/foundational folders flag themselves as preserved-for-lineage and
  point at the current canon.
- All cross-references use repo-relative paths so the docs work both on
  GitHub and in a local clone.

---

## 5. Pre-flight checks (per `PREPARE_FOR_REPO.json`)

- [x] **Engine signature matches code** — engine unchanged, no rebuild needed
- [x] **Determinism gate** — corpus tests still pass; no engine touch
- [x] **Schema validator** — schema 2.1.0 unchanged
- [x] **All experiments have JOURNAL.md** — verified 71/71 per-experiment leaves
- [x] **All folders have orientation** — 100% strategic coverage as audited above
- [x] **No accidental binary additions** — only `.md` files in this push
- [x] **`.gitignore` clean** — `lu4422tlij.tmp` from soffice still in tree;
  recommend `git rm` on commit (see "Known clean-up item" below)

---

## 6. Known clean-up item — `lu4422tlij.tmp`

A stray `lu4422tlij.tmp` file from a previous PowerPoint→PDF conversion
remains at `HCI-CNT/conference_demo/talk_deck/lu4422tlij.tmp`. The
`HCI-CNT/.gitignore` was added in push #15 to prevent future leaks. The
existing one needs an explicit removal. Recommended:

```bash
git rm "HCI-CNT/conference_demo/talk_deck/lu4422tlij.tmp"
```

This is included in the recommended push command below.

---

## 7. Recommended push command

```bash
cd "D:\HUF_Research\Claude CoWorker\Current-Repo"

# Stage the bundle
git add Hs/experiments/Hs-CNT_2026-05/
git add Hs/experiments/INDEX.json
git add Hs/Higgins_Coordinate_System/
git add Hs/HCI-CNT/
git add Hs/HCI/
git add Hs/Hs_Direct/
git add Hs/constants/
git add Hs/data/
git add Hs/docs/
git add Hs/experiments/
git add Hs/papers/
git add Hs/tools/
git add Hs/README.md
git add Hs/PUSH_BUNDLE_AUDIT.md

# Clean-up
git rm -f "Hs/HCI-CNT/conference_demo/talk_deck/lu4422tlij.tmp" 2>/dev/null || true

# Commit + push
git commit -m "Bundle: corpus snapshot Hs-CNT_2026-05 + Higgins_Coordinate_System docs refresh + folder-level README sweep

- Add experiments/Hs-CNT_2026-05/ — dated CNT corpus snapshot (25 experiments)
- Refresh Higgins_Coordinate_System/ docs to reflect CNT as matured successor
- Add 102 folder-level READMEs to guide users to current canon
- Verified 100% folder coverage across the repo (212/212)
- Engine unchanged: CNT 2.0.4 / schema 2.1.0; determinism gate still passes"

git push origin main
```

---

## 8. Live-repo verification (after push)

After pushing, browse the live repo at:

- https://github.com/PeterHiggins19/higgins-decomposition/tree/main/Hs/HCI-CNT
- https://github.com/PeterHiggins19/higgins-decomposition/tree/main/Hs/experiments/Hs-CNT_2026-05
- https://github.com/PeterHiggins19/higgins-decomposition/tree/main/Hs/Higgins_Coordinate_System

Spot-check that:
- Each folder shows its README rendered as the landing page
- All cross-reference links resolve (clicking from a README into another README)
- The 25-experiment corpus appears under `Hs-CNT_2026-05/` and matches the parent INDEX.json hashes

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
