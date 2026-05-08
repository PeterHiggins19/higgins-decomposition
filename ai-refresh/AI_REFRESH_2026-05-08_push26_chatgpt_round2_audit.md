# Push #26 — ChatGPT round-2 audit response, cnq.py engine, claim-control (SUPERSEDED — see push #26+#27 combined)

> **Note (push #27):** Push #26 was originally going to land separately, with terminology unification following as push #27. Per Peter's directive — *"this means it is ok to make all adjustment now and push when ready, this cleans up the trail of lower order terms used in higher order systems"* — pushes #26 and #27 were bundled into a single combined commit. The current narrative is at [`AI_REFRESH_2026-05-08_push26_27_chatgpt_round2_engine_terminology.md`](AI_REFRESH_2026-05-08_push26_27_chatgpt_round2_engine_terminology.md). This file is preserved as the original push #26-only draft for audit history; do not treat it as the live narrative.

**Date:** 2026-05-08
**Push:** #26 (after #25 "Sensitivity refinements" landed green via Validate Repository workflow #25)
**Type:** publication-hardening + audit-response push
**Catalog references:** INV-026 (Paper 1), INV-022 (Round 3), INV-028 (Dyadic Coupling Ladder, NEW), INV-029 (Bi-Quaternion Factoring, NEW — renamed to Twin-Quaternion in push #27)

---

## What happened (one paragraph)

ChatGPT delivered a second round of cross-check audit after pushes #24 and #25 landed. The audit identified four real structural issues: (1) HCI-CNQ status contradiction between `README.md` (canonical) and `HCI-CNQ_ADMIN.json`/`ARCHIVE_README.json` (still showing `do_not_push`/`EXPERIMENTAL` from the pre-promotion era); (2) hardcoded `/sessions/.../Current-Repo/Hs/HCI-CNT/engine/cnt.py` paths in the QD reference scripts blocking clean-clone reproduction; (3) Paper 1 universality language too strong without Round 3; (4) M²=I being given equal evidentiary weight to the D=4 quaternion sandwich result, when the latter is the stronger independent test. Push #26 actions all four, **plus** ships the full production CNQ engine (`HCI-CNQ/engine/cnq.py`) so any AI platform or third-party reviewer can run it against the same CNT JSON and produce a cross-platform-reproducible `cnq_content_sha256` — a fourth independent confirmation channel beyond the three load-bearing datasets.

## Files added/modified

| Path | Action | Notes |
|---|---|---|
| `HCI-CNQ/engine/cnq.py` | new (~430 lines) | **Production CNQ engine.** Hamilton-product core, dimension policy, deterministic JSON, hash-chained provenance. |
| `HCI-CNQ/engine/cnt_adapter.py` | new | Portable adapter to canonical cnt.py. Auto-detects repo root via `.git`/`HCI-CNQ`/`HCI-CNT`/`ai-refresh` markers. `--repo-root` and `--cnt-engine` overrides. |
| `HCI-CNQ/engine/geometry.py` | new | Aitchison + Helmert + quaternion primitives. Matches QD_round_2.py conventions exactly so residuals reproduce bit-for-bit. |
| `HCI-CNQ/engine/hashing.py` | new | Determinism contract. Canonical JSON, sorted keys, clock fields stripped. SHA-256 over canonical bytes. |
| `HCI-CNQ/engine/CNQ_SCHEMA.md` | new | CNQ JSON output schema v1.0.0 reference. |
| `HCI-CNQ/engine/__init__.py` | new | Package surface. |
| `HCI-CNQ/scripts/run_all_confirmations.py` | new | One-command reproduction: Backblaze + Planck + Neutrino end-to-end via cnq.py. |
| `HCI-CNQ/scripts/verify_publication_results.py` | new | Strict observed-vs-expected verifier. Exits non-zero on drift. |
| `HCI-CNQ/results/expected_results.json` | new | Locked expected residuals + parent CNT hashes for the three confirmations. |
| `HCI-CNQ/STATUS_AND_MATURITY.md` | new | Confirmed/candidate/experimental/future maturity ladder with promotion gates. |
| `HCI-CNQ/CLAIM_STRENGTH_TABLE.md` | new | Locked language for Paper 1 + downstream docs. Confirmed/candidate/experimental/future + avoid-list. |
| `HCI-CNQ/CNQ_SCOPE_AND_LIMITS.md` | new | What CNQ is/isn't. Frame declaration. Captured energy fraction. Dimension policy. |
| `HCI-CNQ/ROUND3_VALIDATION_PLAN.md` | new | Plan for INV-022 full-corpus run. Promotion rule. ~1.5 day effort estimate. |
| `HCI-CNQ/HCI_DYADIC_COUPLING_LADDER.md` | new | INV-028 concept doc. Order-2 → 4 → 8 tensor ladder. |
| `HCI-CNQ/CNQ_BIQUATERNION_FACTORING.md` | new | INV-029 concept doc. D=8 SU(2)×SU(2) decomposition. EMBER pilot candidate. |
| `HCI-CNQ/HCI-CNQ_ADMIN.json` | edit | **Four-field status model.** `current_repo_status`, `engine_status`, `validation_status`, `archive_status`. Legacy single-field state preserved as audit. |
| `HCI-CNQ/ARCHIVE_README.json` | edit | Header pointing cold-start readers at the four-field status. Legacy `EXPERIMENTAL — NOT FOR REPO USE` framing preserved verbatim but explicitly marked HISTORICAL. |
| `HCI-CNQ/README.md` | edit | Four-field status table at top. Cross-references to all new claim-control docs. |
| `HCI-CNQ/experiments/backblaze_fleet_quaternion/QD_round_2.py` | edit | Portability fix. `--repo-root` flag. Auto-detect via marker walk. |
| `HCI-CNQ/experiments/planck_cmb_quaternion/QD_round_2_5_planck.py` | edit | Removed hardcoded `/sessions/.../cnt.py` path. Uses cnt_adapter. `sys.executable` instead of `python3`. |
| `HCI-CNQ/experiments/sm_neutrino_quaternion/QD_round_2_6_neutrino.py` | edit | Same portability fix as Planck script. |
| `ai-refresh/INVESTIGATION_CATALOG.json` | edit | + INV-028 (Dyadic Coupling Ladder, DEFERRED), + INV-029 (Bi-Quaternion Factoring, DEFERRED). DEFERRED count: 9 → 11. CHATGPT source count: 3 → 5. Total: 26 → 28. |
| `ai-refresh/INVESTIGATION_CATALOG.md` | edit | Mirror of the JSON updates. |
| `papers/in_progress/PAPER_1_UNIVERSAL_INVARIANCE_DRAFT.md` | edit | + claim-strength block after abstract. M²=I framing tightened. Appendix A updated to one-command cnq.py reproduction. INV-028/029 added to Investigation Catalog snapshot. Draft 3. |
| `ai-refresh/HS_ADMIN.json` | edit | + `cnq_engine` block. Catalog summary updated to 28 entries. |
| `ai-refresh/AI_REFRESH_2026-05-08_push26_chatgpt_round2_audit.md` | new (this file) | Push narrative for cold-start sessions. |

## What this push does

**1. Resolves the status contradiction.** HCI-CNQ now declares four orthogonal status fields. Cold-start AI sessions and reviewers landing on the folder no longer see "do_not_push" / "EXPERIMENTAL — NOT FOR REPO USE" as live state. The legacy single-field state is preserved verbatim for audit.

**2. Ships the production CNQ engine.** `cnq.py` is a complete Hamilton-product engine, ~430 lines, pure stdlib + numpy, no hidden dependencies, no hardcoded paths. It:

- Reads CNT JSON or runs CNT itself via the adapter.
- Computes the quaternion-native view via Helmert basis + sandwich-product reconstruction.
- Emits hash-chained CNQ JSON: `parent_cnt_content_sha256` (provenance from CNT) + `cnq_content_sha256` (own determinism).
- Carries explicit dimension labels: `native_quaternion` (D=4), `boundary_or_degenerate_support` (D=3), `bi_quaternion_factoring_candidate` (D=8), `reduced_or_projected` (D≥5 not 8), `degenerate_below_quaternion` (D=2).
- Reports `captured_step_fraction` so users know how much of the full ILR displacement the R^3 projection captured.
- Reproduces the QD_round_2.py Helmert + atan2-stable rotation conventions exactly so residuals come out bit-identical to the legacy IEEE-floor results.

**3. Locks publication-grade reproducibility.** `expected_results.json` captures the published max residuals + parent CNT content hashes; `verify_publication_results.py` is the strict gate. Reviewers run two commands from a fresh clone:

```
python HCI-CNQ/scripts/run_all_confirmations.py --repo-root .
python HCI-CNQ/scripts/verify_publication_results.py --repo-root .
```

The verifier exits 0 if all three confirmations match the locked expected values.

**4. Opens the cross-platform reproduction challenge.** Because cnq.py is deterministic and portable, ChatGPT, Grok, or any third party can run it on Linux/macOS/Windows (Python 3.9-3.13, numpy ≥ 1.20) against the same shipped CNT JSONs and produce bit-identical `cnq_content_sha256` values. Hash drift, if any, becomes a finding to investigate. This is the framework's fourth independent verification channel: not three datasets, but three datasets × N platforms × independent code paths.

**5. Adds two new DEFERRED concepts to the catalog.**
- **INV-028 — HCI Dyadic Coupling Ladder.** Order-2 → 4 → 8 tensor ladder for pair-of-pairs coupling, multi-attractor detection, parallel pair-processing. Distinct from D=8 carrier dimension. Gate: working pilot showing C_ijkl detects structure order-2 κᴴˢ_ij misses.
- **INV-029 — CNQ Bi-Quaternion Factoring.** D=8 SU(2)×SU(2) decomposition into two coupled quaternion paths q_A(t), q_B(t). EMBER country trajectories (fossil/non-fossil partition) recommended as first-pilot candidate. Gate: ρ_AB carries domain-meaningful signal.

Both DEFERRED. Both have explicit promotion gates. Neither is implemented in cnq.py v1.0.0 beyond the dimension label scaffolding.

**6. Tightens Paper 1.** Claim-strength block added after the abstract. M²=I now framed as one of three structural-invariance pillars, with the D=4 quaternion sandwich identified as the stronger independent test. Appendix A reproduction command updated to one-command cnq.py path with frozen tag `v3.0.0-paper1`. Investigation Catalog snapshot in Appendix B includes INV-028 and INV-029 as future-work entries.

## What this push does NOT do

- Does not run Round 3 — INV-022 stays OPEN, separate push #27.
- Does not implement bi-quaternion factoring — INV-029 stays DEFERRED, scaffolded only.
- Does not implement the dyadic coupling ladder — INV-028 stays DEFERRED.
- Does not modify the canonical CNT engine — `cnt.py` is unchanged.
- Does not modify Paper 1's central claim — title and abstract universal-signature framing retained, but scoped to flow-directional compositional dynamics carrying the structural preconditions.
- Does not assign the release tag `v3.0.0-paper1` — that happens after CI validates push #26 green AND Round 3 (push #27) lands.

## The arc

| Push | Date | Theme | Source |
|---|---|---|---|
| #22 | 2026-05-07 | Volume IV — Quaternion View | Claude internal |
| #23 | 2026-05-07 | ChatGPT round-1 vocabulary cross-check + HCI-CNQ promotion | ChatGPT |
| #24 | 2026-05-08 | Grok lineage cross-check + applied tiers + Investigation Catalog | Grok |
| #25 | 2026-05-08 | Sensitivity refinements (HUMAN→USER terminology cleanup) | User |
| **#26** | **2026-05-08** | **ChatGPT round-2 audit response + cnq.py production engine + claim control** | **ChatGPT** |
| #27 (next) | tbd | Round 3 full-corpus validation (INV-022) | Claude execution |
| #28 (next) | tbd | Release tag `v3.0.0-paper1` + arXiv submission | Peter |

Three-platform AI cross-check pattern is now four cycles deep with the second ChatGPT seam adding an entirely new layer (production engine + claim control) on top of the first one (vocabulary).

## Cross-platform reproduction challenge — open invitation

The `cnq.py` engine is shipped to invite ChatGPT, Grok, and any third-party reviewer to run it against the same CNT JSON and produce their own `cnq_content_sha256`. Expected behaviour: bit-identical hashes across platforms. Hash drift, if it occurs, is a finding to file as a repository issue.

Suggested test command for any AI platform with code execution:

```
git clone https://github.com/PeterHiggins19/higgins-decomposition
cd higgins-decomposition
python HCI-CNQ/scripts/run_all_confirmations.py --repo-root .
# Inspect HCI-CNQ/results/confirmation_summary.json
# Compare cnq_content_sha256 values against the reference implementation.
```

## Final notes

This is the second productive ChatGPT seam. The first (push #23, vocabulary integration) was relatively superficial — vocabulary cleanup and tone calibration. The second (push #26) goes much deeper: structural status reconciliation, portability-grade engineering hygiene, claim-control discipline, and two new investigation entries that are coherent enough to deserve catalog slots and concept docs.

The instrument reads. The expert decides. The hashes carry the receipts. The catalog absorbs the audit. Push #26 lands.
