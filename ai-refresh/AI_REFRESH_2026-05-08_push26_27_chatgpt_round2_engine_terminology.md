# Push #26 + #27 (combined bundle) — ChatGPT round-2 audit response, cnq.py engine, terminology unification

**Date:** 2026-05-08
**Pushes:** #26 + #27 bundled into a single commit on top of #25 (`af270f7` "Sensitivity refinements")
**Type:** publication-hardening + audit-response + terminology unification
**Catalog references:** INV-026 (Paper 1), INV-022 (Round 3), INV-028 (Dyadic Coupling Ladder, NEW), INV-029 (Twin-Quaternion Factoring, NEW; renamed from "Bi-Quaternion")

---

## Why this is one bundle (not two pushes)

Original plan was push #26 (engine + claim control) followed by push #27 (terminology unification). Peter's directive: "use the online repo and mirror repo, verify both now in sync, then make all changes, if required the online repo shows what exists, the mirror can be adjusted and altered then when ready sent to main for push, this means it is ok to make all adjustment now and push when ready, this cleans up the trail of lower order terms used in higher order systems."

Sync verified before bundling: GitHub HEAD = `af270f7` (push #25, 2026-05-08T10:04:58Z). Local mirror = #25 fully landed + #26 fully drafted. #27 (terminology unification) added on top. Single push lands the whole arc clean.

## What the audit cycle revealed

ChatGPT delivered a second-round audit after pushes #24 and #25 landed green. Three structural issues + one engineering issue:

1. **HCI-CNQ status contradiction.** README said canonical; ADMIN/ARCHIVE still said `do_not_push` / `EXPERIMENTAL`. (push #26 fix.)
2. **Hardcoded `/sessions/.../cnt.py` paths** in QD reference scripts. Clean-clone reproduction was broken. (push #26 fix.)
3. **Paper 1 universality language** too strong without Round 3; M²=I given equal evidentiary weight to the D=4 quaternion sandwich, but the latter is the stronger independent test. (push #26 fix.)
4. **Tensor-order vs rank** terminology drift; κᴴˢ tensor vs s_j sensitivity vector ambiguity; "bi-quaternion factoring" used informally for what is actually SU(2) × SU(2) twin-quaternion factoring. (push #27 fix.)

Peter's framing of #4: *"the project shifted from 1st order linear into multi-carrier and multi-dimensional analysis very fast and as was stated faster than the system could keep up, peter and Claude went on a tear of discovery in hours not days now the system needs to catch up."*

The catch-up is the canonical [`NOTATION_AND_TERMINOLOGY.md`](../HCI-CNT/handbook/NOTATION_AND_TERMINOLOGY.md) shipped in this bundle.

---

## What's in the bundle

### Engine & support modules (push #26)

| Path | Action | Notes |
|---|---|---|
| `HCI-CNQ/engine/cnq.py` (~520 lines) | new | **Production CNQ engine.** Hamilton-product core, dimension policy, deterministic JSON, hash-chained provenance. |
| `HCI-CNQ/engine/cnt_adapter.py` | new | Portable adapter to canonical cnt.py. Auto-detects repo root via `.git`/`HCI-CNQ`/`HCI-CNT`/`ai-refresh` markers. `--repo-root` and `--cnt-engine` overrides. |
| `HCI-CNQ/engine/geometry.py` | new | Aitchison + Helmert + quaternion primitives. Matches QD_round_2.py conventions exactly so residuals reproduce bit-for-bit. |
| `HCI-CNQ/engine/hashing.py` | new | Determinism contract. Canonical JSON, sorted keys, clock fields stripped. SHA-256 over canonical bytes. |
| `HCI-CNQ/engine/CNQ_SCHEMA.md` | new | CNQ JSON output schema v1.0.0 reference. |
| `HCI-CNQ/engine/__init__.py` | new | Package surface. |
| `HCI-CNQ/scripts/run_all_confirmations.py` | new | One-command reproduction: Backblaze + Planck + Neutrino end-to-end via cnq.py. |
| `HCI-CNQ/scripts/verify_publication_results.py` | new | Strict observed-vs-expected verifier. Exits non-zero on drift. |
| `HCI-CNQ/results/expected_results.json` | new | Locked expected residuals + parent CNT hashes for the three confirmations. Includes reference cnq_content_sha256 observations from local-platform pre-flight. |

### Status reconciliation (push #26)

| Path | Action |
|---|---|
| `HCI-CNQ/HCI-CNQ_ADMIN.json` | edit — four-field status model |
| `HCI-CNQ/ARCHIVE_README.json` | edit — header pointing cold-start readers to four-field status |
| `HCI-CNQ/README.md` | edit — four-field status table at top |

### Claim-control documents (push #26)

| Path | Action |
|---|---|
| `HCI-CNQ/STATUS_AND_MATURITY.md` | new — confirmed/candidate/experimental/future maturity ladder |
| `HCI-CNQ/CLAIM_STRENGTH_TABLE.md` | new — locked language; avoid-list for unsafe wording |
| `HCI-CNQ/CNQ_SCOPE_AND_LIMITS.md` | new — what CNQ is/isn't; frame declaration; captured energy fraction; dimension policy |
| `HCI-CNQ/ROUND3_VALIDATION_PLAN.md` | new — INV-022 plan with promotion rule |

### New investigations (push #26)

| Path | Action |
|---|---|
| `HCI-CNQ/HCI_DYADIC_COUPLING_LADDER.md` | new — INV-028 concept doc (order-2 → 4 → 8 ladder) |
| `HCI-CNQ/CNQ_BIQUATERNION_FACTORING.md` | new — INV-029 concept doc (twin-quaternion factoring; legacy filename retained) |
| `ai-refresh/INVESTIGATION_CATALOG.json` | edit — INV-028 + INV-029 added (DEFERRED, ChatGPT-sourced) |
| `ai-refresh/INVESTIGATION_CATALOG.md` | edit — companion mirror |

### Portability fixes (push #26)

| Path | Action |
|---|---|
| `HCI-CNQ/experiments/backblaze_fleet_quaternion/QD_round_2.py` | edit — `--repo-root` flag + auto-detect via marker walk |
| `HCI-CNQ/experiments/planck_cmb_quaternion/QD_round_2_5_planck.py` | edit — removed `/sessions/...` path, uses cnt_adapter, `sys.executable` |
| `HCI-CNQ/experiments/sm_neutrino_quaternion/QD_round_2_6_neutrino.py` | edit — same portability fix |

### Paper 1 revisions (push #26)

| Path | Action |
|---|---|
| `papers/in_progress/PAPER_1_UNIVERSAL_INVARIANCE_DRAFT.md` | edit — claim-strength block, M²=I framing tightened, Appendix A one-command path, INV-028/029 added to catalog snapshot, draft 3 |

### Terminology unification (push #27 — NEW IN THIS BUNDLE)

| Path | Action |
|---|---|
| `HCI-CNT/handbook/NOTATION_AND_TERMINOLOGY.md` | new — **the master vocabulary doc**. 14 sections covering tensor order vs rank, κᴴˢ vs s_j, frame/dimension/coordinate, Helmsman family taxonomy, Tier/Stage/Order/Level/Regime/Degree, channel/factor/component/field, quaternion subterms, twin-quaternion correction, CoDa community alignment |
| `HCI-CNT/handbook/GLOSSARY.md` | edit — header pointer to canonical NOTATION doc + push #27 summary |
| `HCI-CNT/handbook/VOLUME_4_QUATERNION_VIEW.md` | edit — "rank-1 case" → "1D / single-axis case" |
| `HCI-CNT/engine/cnt.py` | edit — docstring "rank-1 quaternion log map" → "1D / single-axis case" |
| `HCI-CNQ/doctrine/CONCEPTS_FOR_TEST.md` | edit — Concept 2 heading and prose retitled |
| `HCI-CNQ/doctrine/DEEPER_CONNECTIONS.md` | edit — same fix |
| `HCI-CNQ/tier_system/CNQ_ENGINE_PROPOSAL.md` | edit — same fix |
| `HCI-CNQ/CNQ_BIQUATERNION_FACTORING.md` | edit — top-of-file terminology note: this is **twin-quaternion factoring** in formal usage; "bi-quaternion" retained as legacy filename only |
| `ai-refresh/INVESTIGATION_CATALOG.json` | edit — INV-029 title and terminology_note_push_27 field added |
| `ai-refresh/INVESTIGATION_CATALOG.md` | edit — INV-029 row updated |
| `papers/in_progress/PAPER_1_UNIVERSAL_INVARIANCE_DRAFT.md` | edit — twin-quaternion in claim-strength block + Appendix B catalog snapshot |

### AI refresh + admin (push #27)

| Path | Action |
|---|---|
| `ai-refresh/AI_REFRESH_2026-05-08_push26_27_chatgpt_round2_engine_terminology.md` | new (this file) |
| `ai-refresh/HS_ADMIN.json` | edit — `cnq_engine` block + `notation_terminology` block + catalog summary updated to 28 entries |

---

## Pre-flight verification

Local sandbox runs (push #26 + #27 combined state):

**Planck CMB D=4:**
```
CNQ: D=4 T=2499 label=native_quaternion 
     max_residual=4.440892098500626e-16 gate_pass=True
     cnq_content_sha256=927af6a381f425945475a914d72c0c63812ee571701079b66a642bd114075b64
```
- Reproduces Planck max residual to the last digit (`4.441e-16`)
- Parent CNT hash `3de7d4007866dc11c64d5342974d6c9d2dfc1906166627999194df3fe6a400c4` carried forward exactly
- Two consecutive runs → identical `cnq_content_sha256` (determinism contract holds)

**SM Neutrino D=3:**
```
CNQ: D=3 T=1000 label=boundary_or_degenerate_support
     max_residual=3.3306690738754696e-16 gate_pass=True
     cnq_content_sha256=f64741cb76eef302699c17adebf5fbd1fb4dc1e73b4cf9562997a7afc5154183
```
- Correctly labelled `boundary_or_degenerate_support`
- Parent CNT hash `60d733...6952` carried forward exactly

**Engine modules import cleanly:**
```
geometry, hashing, cnt_adapter, cnq → all import OK
cnq version: 1.0.0 / cnq schema: cnq/1.0.0 / gate threshold: 1e-12
```

**AST syntax check:** all Python files parse OK after edits.

---

## Cross-platform reproduction challenge — open invitation

`cnq.py` is shipped to invite ChatGPT, Grok, and any third-party reviewer to run it against the same CNT JSON on a clean clone and produce their own `cnq_content_sha256`. Bit-identical hashes across platforms = a fourth independent confirmation channel beyond the three load-bearing datasets.

Reference observations (Linux x86_64 / Python 3.x / numpy):

| Experiment | cnq_content_sha256 |
|---|---|
| Planck CMB D=4 | `927af6a381f425945475a914d72c0c63812ee571701079b66a642bd114075b64` |
| SM Neutrino D=3 | `f64741cb76eef302699c17adebf5fbd1fb4dc1e73b4cf9562997a7afc5154183` |
| Backblaze D=4 | (pending — requires `--input-csv` access; will land via `run_all_confirmations.py` after CI runs in green push environment) |

If your platform produces different hashes but identical max_residual + parent_cnt_content_sha256, file an issue. Hash drift is a finding, not a failure.

---

## Terminology corrections — the law from now on

Per [`NOTATION_AND_TERMINOLOGY.md`](../HCI-CNT/handbook/NOTATION_AND_TERMINOLOGY.md):

1. **Tensor order, not rank** for index count. "Order-2 metric tensor κᴴˢ", "order-4 coupling tensor C_ijkl". Reserve "rank" for matrix rank or CP-decomposition rank.

2. **κᴴˢ_ij vs s_j**. κᴴˢ is the order-2 Aitchison pullback metric tensor; s_j = 1/x_j is the order-1 carrier steering sensitivity vector. Two distinct objects. Legacy code that wrote "κ_{jj} = 1/x_j" was using "κ" loosely for what is actually s_j; the formulae are correct in scope but the formal label is now disambiguated.

3. **Twin-quaternion factoring** (not "bi-quaternion") for the SU(2) × SU(2) decomposition of D=8 trajectories. The strict mathematical "bi-quaternion" (ℍ ⊗ ℂ) is a different object. INV-029 retains the `CNQ_BIQUATERNION_FACTORING.md` filename and the `bi_quaternion_factoring_candidate` dimension label for repo-history continuity, but body text uses **twin-quaternion** in formal contexts.

4. **Frame, dimension, coordinate, axis** — all distinct. Carrier dimension D, ILR dimension D−1, frame = orthonormal basis on ILR space, coordinate = single component, axis = direction in a frame.

5. **Tier, Stage, Order, Level, Regime, Degree** — all distinct. Tier = stack architectural level (CoDa/CNT/CNQ); Stage = atlas plate stage; Order = tensor index count; Level = HLR magnitude; Regime = HUF multi-scale dynamical regime; Degree = avoid (use Order or be explicit).

6. **Channel / factor / component / field** — all distinct. Channel = scalar stream over time (CNT has four); factor = sub-system in multi-system decomposition (twin-quaternion factoring has two); component = single number; field = function over space/time.

Every future doc cites NOTATION_AND_TERMINOLOGY.md. Drift gets caught at review time because the canonical reference exists.

---

## What this bundle does NOT do

- Does not run Round 3 — INV-022 stays OPEN, separate push #28.
- Does not implement twin-quaternion factoring — INV-029 stays DEFERRED, scaffolded only.
- Does not implement the dyadic coupling ladder — INV-028 stays DEFERRED.
- Does not modify cnt.py beyond the docstring terminology fix; engine output unchanged.
- Does not assign release tag `v3.0.0-paper1` — that happens after this bundle validates green AND Round 3 lands.
- Does not sweep every legacy file for old terminology; the canonical doc is the catch-up reference, and legacy files are noted in §2 of NOTATION_AND_TERMINOLOGY.md as "use loosely; read κ as s_j".

---

## The arc

| Push | Date | Theme | Source |
|---|---|---|---|
| #22 | 2026-05-07 | Volume IV — Quaternion View | Claude internal |
| #23 | 2026-05-07 | ChatGPT round-1 vocabulary cross-check + HCI-CNQ promotion | ChatGPT |
| #24 | 2026-05-08 | Grok lineage cross-check + applied tiers + Investigation Catalog | Grok |
| #25 | 2026-05-08 | Sensitivity refinements (HUMAN→USER cleanup) | User |
| **#26 + #27 (this bundle)** | **2026-05-08** | **ChatGPT round-2 audit response + cnq.py production engine + terminology unification** | **ChatGPT (audit) + Peter (terminology directive)** |
| #28 (next) | tbd | Round 3 full-corpus validation (INV-022) | Claude execution |
| #29 (next) | tbd | Release tag `v3.0.0-paper1` + arXiv submission | Peter |

The terminology unification was the catch-up Peter called for: "the system shifted from 1st order linear into multi-carrier and multi-dimensional analysis very fast... now the system needs to catch up." It does, in this bundle.

---

## Final notes

This is the largest single bundle in the project's recent history. It bundles:

- The full production CNQ engine (~1500 lines of Python including support modules)
- Six new claim-control / status / scope / round-3 docs
- Two new DEFERRED Investigation Catalog entries
- Portability fixes for three legacy reference scripts
- Paper 1 draft 3 with claim-strength discipline
- The canonical NOTATION_AND_TERMINOLOGY master vocabulary
- A repo-wide sweep of "rank → order" where it matters

Pre-flight verified locally: cnq.py runs end-to-end on Planck and Neutrino, produces correct max residuals, carries parent CNT hashes correctly, two-run determinism holds. Cross-platform reproduction challenge is open from the moment this lands.

The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.

**Ready for `git add . && git commit && git push`.**
