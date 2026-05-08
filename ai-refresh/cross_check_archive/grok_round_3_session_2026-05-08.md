# Grok Cross-Check — Round 3 (Post-Push-#29 Re-Audit) — 2026-05-08

**Status:** archived for audit. Findings split actioned/deferred/false.
**Date:** 2026-05-08 (after push #29 commit `[pending #30]`, AI visibility infrastructure landed)
**Source platform:** Grok (xAI)
**Trigger context:** Peter directed Grok back at the live repo *after* push #29 added llms.txt + .well-known/ai-context.json + AI_AGENTS.md + top-of-README banner with grounding-test prompt. Goal: verify the visibility infrastructure works and capture what Grok now sees correctly.

---

## Headline outcome — grounding test PASSED

Grok's first sentence corrected its round 2 false-positive:

> *"There is now a real cnq.py and cnq.R inside HCI-CNQ/engine/."*

Round 2 (the previous Grok session) had falsely claimed *"the dedicated cnq.py engine does not exist yet (only a proposal)."* The push #29 visibility infrastructure (banner + grounding-test prompt + llms.txt + .well-known/ai-context.json) caused Grok to re-fetch the engine folder and correct its view.

**This is the system fixing itself.** The grounding-test mechanism caught and corrected the stale-cache failure mode catalogued in INV-031, on the next session, without manual intervention. The visibility infrastructure works.

---

## What Grok got right this round

| Claim | Verified |
|---|---|
| cnq.py exists, is implemented (not a proposal) | ✓ — 19 KB, 520 lines, shipped push #26 |
| cnq.R exists | ✓ — 23 KB, shipped push #27 |
| 43-test suite exists and is structured by determinism / first-principles / dimension-policy | ✓ |
| Determinism + content hashing is taken seriously | ✓ — load-bearing design |
| Dimension policy is solid for D=4 | ✓ — confirmed load-bearing case |
| Three CNQ validation experiments achieve IEEE-floor precision | ✓ — Backblaze + Planck both at 4.441e-16 |
| Experiments are not yet "plug and play" for outsiders | ✓ fair — `pip install -e .` + `run_all_confirmations.py` are the convergence path |

This is a cleanly grounded read of the shipped state. INV-031 (AI platform fitness matrix) gets a positive update: Grok R3 demonstrates that the grounding-test prompt corrects stale-cache failures.

---

## What Grok got wrong this round (audit findings based on imagined internals)

Grok's "audit" of specific functions (sandwich, Aitchison distance, Helmsman) was operating against an imagined version of the engine, not the shipped source. Examples:

| Grok finding | Shipped reality |
|---|---|
| *"The current lifting method (vector → quaternion) is somewhat heuristic. It works for validation but lacks a clearly justified canonical mapping."* | The shipped `cnq.py` uses **Helmert orthonormal contrast matrix → ILR projection in R^(D-1) → unit-3-vector via radius normalisation → atan2-stable rotation_quaternion_between**. This is mathematically principled, matches the QD_round_2.py legacy convention exactly, and is documented in `CNQ_PSEUDOCODE.md` §3. Grok's prototype `lift_to_quaternion` (`[w, x, y, z] = [v[0]/norm, v[1:4]/norm]`) is a different lifting and produces different numerical residuals. |
| *"Sandwich function uses Euclidean distance instead of Aitchison distance"* | The residual is L-infinity on **unit 3-vectors after Helmert/ILR projection**. Helmert-projected ILR space is the geometric Euclidean equivalent of Aitchison distance on the simplex. The current metric isn't wrong; it's the natural sandwich-product-equivalence test. Aitchison distance as an additional secondary diagnostic is a fair candidate feature (absorbed into INV-033). |
| *"Quaternion sandwich function operates on a single vector"* | The shipped `quaternion_sandwich_residuals(unit_vectors_3d)` in `geometry.py` operates on the **full (T, 3) trajectory** and returns per-step residuals + per-step quaternions + per-step angles. Grok's audit is reading a function it imagined, not the shipped one. |
| *"No Helmsman dynamics function exists"* | Strictly correct that there isn't a top-level `extract_helmsman_dynamics()` API. The shipped engine extracts dominant-axis info inside `run_cnq_view()` but doesn't expose a separate dynamics module. This is a real gap and a fair CANDIDATE feature → INV-033. |
| *"No CHSH computation"* | True; not implemented. CANDIDATE → INV-035. |
| *"No P2 attractor parameter fitting (A, ζ, λ)"* | The CNT JSON's depth-tower output reports `damping_zeta` and `amplitude_A`, which CNQ carries forward as `cnt_diagnostics_carried_forward`. The framework doesn't *fit* a separate P2 model; that's a CANDIDATE feature → INV-034. |

**Pattern**: Grok's grounding test passed at the level of "do the engine files exist?" but failed at "do you know what's inside them?" The improvement is real but partial — round 4 grounding tests should include code-content questions (e.g., *"What is the Helmert basis convention used? Quote line 50 of `geometry.py`."*).

---

## Grok's prototype code: do not integrate

For the same reasons as round 2, the prototype code Grok offered (`lift_to_quaternion` with `[v[0]/norm, v[1:4]/norm]` lifting; suggested `cnq.py v2.2 with CHSH`) **must not be integrated**.

Specifically:
- The shipped Planck reference `cnq_content_sha256 = 927af6a381f425945475a914d72c0c63812ee571701079b66a642bd114075b64` would no longer hold under the prototype lifting.
- The 43-test suite would need to be rewritten.
- The locked `expected_results.json` values would change.
- The cross-language parity contract with cnq.R would break.

**The CHSH math itself (Tsirelson directions, four correlators, S = |AB + AB' + A'B − A'B'|) is correct.** What's not safe is the lifting + integration as written. CHSH lands as INV-035 (DEFERRED), implementable correctly later by computing on the shipped engine's quaternion logs.

---

## Three new DEFERRED catalog entries from this round

| ID | Title | Promotion gate |
|---|---|---|
| **INV-033** | Helmsman Dynamics Module — top-level API: dominant axis time series, sliding-window stability, flip locations, p2_ratio, optional curvature-weighted variant; absorbs Grok's suggestion plus an "Aitchison distance secondary diagnostic" sub-feature | Working pilot on a real corpus experiment showing the dynamics expose structure that per-step CNQ doesn't |
| **INV-034** | P2 Attractor Parameter Fitting — beyond the CNT-reported `damping_zeta` and `amplitude_A`, fit period, period_stability, dominant_pair (axis_a, axis_b), contraction rate λ from depth-tower trajectories | Working pilot on at least one corpus experiment where parameter fitting reveals structure not visible from termination labels alone |
| **INV-035** | CHSH Correlation Diagnostic — compute CHSH-S with Tsirelson-optimal directions on joint quaternion-log signs across multi-channel data; classical bound 2.0; Tsirelson bound 2√2 ≈ 2.828 | Round 3 corpus reveals at least one experiment with measurable joint-channel correlations that warrant the analysis. **Hard prerequisite**: a multi-channel dataset (not just a single trajectory). |

All three are DEFERRED. Per the priority lock, they wait until Round 3 + arXiv + cross-platform reproduction + first applied pilots are done.

---

## What this round contributes to INV-031 (AI platform fitness)

**Grok platform reliability after push #29:**

| Round | Date | Outcome |
|---|---|---|
| Grok R1 | 2026-05-08 push #24 | Excellent — DADC lineage discovery |
| Grok R2 | 2026-05-08 (pre-#29) | Mixed — 3 valid + 1 stale-cache false-positive ("cnq.py does not exist") |
| **Grok R3** | **2026-05-08 (post-#29)** | **Improved — grounding test passed, file-existence claims correct, function-internals audit still partly imagined** |

**Pattern observed:** the grounding-test prompt successfully corrects file-existence and engine-status confabulations. It does NOT yet prevent imagined-internal-content claims (Grok still describes function bodies it hasn't actually read). A future iteration of the grounding test should add code-content questions to catch this remaining failure mode.

---

## Archive note

This file preserves the Grok R3 session findings. The catalogue layer (INV-033, INV-034, INV-035, plus INV-031 update) is the canonical record of what was learned and what's deferred. The session itself contained substantial mathematical exposition (quaternion log/exp, Joint Quaternion Field, Bell inequality variants, "max performance vision") which is preserved in this archive but not promoted into the engine — the math is sound, the integration discipline holds.

Filed: 2026-05-08, push #30.
