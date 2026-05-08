# Operations Protocol — How we run this repo

**Audience:** anyone working on or with the Hs / HCI-CNT repository — the
researcher walking the steps by hand, the AI assistant executing on the
researcher's behalf, the reviewer auditing the result, the new collaborator
landing here for the first time.

**Pattern:** the [Atul Gawande checklist principle](https://en.wikipedia.org/wiki/The_Checklist_Manifesto). Complexity creates
failure modes at *transition points* — the moments when control passes from
one phase or actor to another. The fix is a structured pause-and-verify
checklist at each transition, written in plain language, with binary
pass/fail items, executed by whoever is on point at that moment. The repo
already has a checklist at every important transition; this document is
the **map of those checklists**.

**User governs in both modes.** Every transition below works whether you
execute it by hand (User-mode) or have an AI assistant execute it on your
behalf (User + AI-mode). The gates are the same. The hashes are the same.
You confirm at every gate.

---

## Transition map

| # | Transition | When this applies | Canonical checklist |
|---|---|---|---|
| 1 | **Starting a new compositional analysis** | You have a CSV/XLSX and want a CNT-grade result | [`ai-refresh/CCTT_RUNBOOK.md`](ai-refresh/CCTT_RUNBOOK.md) — 7-phase loop |
| 2 | **Adding a new adapter** | Your dataset doesn't match any built-in adapter | [`HCI-CNT/adapters/README.md`](HCI-CNT/adapters/README.md) + [`HCI-CNT/handbook/VOLUME_2_PRACTITIONER_AND_OPERATIONS.md`](HCI-CNT/handbook/VOLUME_2_PRACTITIONER_AND_OPERATIONS.md) Part C |
| 3 | **Adding an experiment to the corpus** | Run is solid; you want it pinned in the determinism gate | Section 3 below — INDEX update + JOURNAL + hash registration |
| 4 | **Modifying the engine** | Editing `cnt.py` or `cnt.R` | Section 4 below — full 25-experiment determinism gate before commit |
| 5 | **Pushing to origin/main** | Cowork mirror changes are ready to ship | [`ai-refresh/PREPARE_FOR_REPO.json`](ai-refresh/PREPARE_FOR_REPO.json) → `push_checklist` (16 items) + verify GitHub Actions green |
| 6 | **Cowork session start** | Opening a new Claude Cowork (or other AI) session on this repo | Section 6 below — read tier-1 files, respect dual-folder protocol |
| 7 | **Cowork session end** | Closing a Cowork session with pending changes | Section 7 below — confirm mirror state, surface unpushed work |
| 8 | **Bringing a new AI assistant on cold-start** | First time a fresh AI sees this repo | [`ai-refresh/CCTT_RUNBOOK.md`](ai-refresh/CCTT_RUNBOOK.md) "How to use this runbook" + [`ai-refresh/HS_MACHINE_MANIFEST.json`](ai-refresh/HS_MACHINE_MANIFEST.json) |
| 9 | **Push fails Actions validation** | `Validate Repository #N` workflow goes red | Section 9 below — workflow-failure recovery |
| 10 | **Determinism-gate experiment drifts** | A corpus experiment's `content_sha256` no longer matches | Section 10 below — corpus-drift recovery |
| 11 | **Documentation update** | Editing handbook, READMEs, or admin JSONs | Section 11 below — README sweep + handbook update + admin JSON validation |
| 12 | **Reviewer requests reproducibility** | An external auditor asks "can I re-run this?" | Section 12 below — 30-second reproduction recipe |

---

## Section 1 — Starting a new compositional analysis

The CCTT v1.0 protocol is the front-door for *any* compositional analysis
done in this repo. It works the same for User-mode (you walk the runbook
yourself) and User + AI-mode (an AI assistant walks it; you confirm the
gates).

**Local checklist:**

- [ ] Read [`ai-refresh/CCTT_QUICKSTART.md`](ai-refresh/CCTT_QUICKSTART.md) for the high-level flow.
- [ ] Open [`ai-refresh/CCTT_RUNBOOK.md`](ai-refresh/CCTT_RUNBOOK.md) and walk the 7-phase loop.
- [ ] At phase 2, confirm the column-to-carrier mapping before running the engine.
- [ ] At phase 6, all four gate checks must pass before ship.
- [ ] At phase 7, write JOURNAL.md with full provenance + AI build provenance block (if AI-assisted).

**Canonical document:** [`ai-refresh/CCTT_BUILD_INSTRUCTION_v1.0.json`](ai-refresh/CCTT_BUILD_INSTRUCTION_v1.0.json)

---

## Section 2 — Adding a new adapter

When the dataset doesn't match any of the 13 built-in adapters, generate
one with full disclosure. The adapter source IS the documentation.

**Local checklist:**

- [ ] Source disclosure header — provenance, citation, retrieval date, original SHA.
- [ ] Carrier mapping documented — which raw column became which carrier, with units.
- [ ] Transformation log — closure, imputation, aggregation, dropped rows, all logged.
- [ ] Output writes `<name>_input.csv` (label + D carriers, T rows, every cell positive).
- [ ] Output writes `<name>_disclosure.json` with the same data in machine form.
- [ ] Adapter prints SHA-256 of `<name>_input.csv` on stdout for the journal.
- [ ] Use [`HCI-CNT/adapters/bin_tappe_and_qin.py`](HCI-CNT/adapters/bin_tappe_and_qin.py) as the gold-standard template.

**Canonical document:** [`HCI-CNT/handbook/VOLUME_2_PRACTITIONER_AND_OPERATIONS.md`](HCI-CNT/handbook/VOLUME_2_PRACTITIONER_AND_OPERATIONS.md) Part C.

---

## Section 3 — Adding an experiment to the corpus

The 25-experiment corpus in [`HCI-CNT/experiments/INDEX.json`](HCI-CNT/experiments/INDEX.json)
is the determinism gate's source of truth. Adding an experiment pins a new
hash that every future engine release must reproduce.

**Local checklist:**

- [ ] Engine run is clean (zero stderr, JSON has all 7 top-level keys).
- [ ] `JOURNAL.md` written for the experiment (use any existing experiment's JOURNAL as the template — `HCI-CNT/experiments/codawork2026/ember_jpn/JOURNAL.md` is canonical).
- [ ] Adapter is fully disclosed and lives in [`HCI-CNT/adapters/`](HCI-CNT/adapters/).
- [ ] `INDEX.json` entry added with: `id`, `subdir`, `csv_path`, `json_path`, `n_records (T)`, `n_carriers (D)`, `curvature_depth`, `energy_depth`, `ir_class`, `amplitude_A`, `lock_events`, `M2_residual`, `content_sha256`, `wall_clock_ms`.
- [ ] Mission Command per-id ordering registered in `mission_command/mission_command.py` `DEFAULT_ORDERING`.
- [ ] Re-run the determinism gate (`tools/verify_package.py`) — must show 26/26 PASS.

**Canonical document:** [`HCI-CNT/experiments/INDEX.json`](HCI-CNT/experiments/INDEX.json) + [`HCI-CNT/handbook/VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md`](HCI-CNT/handbook/VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md).

---

## Section 4 — Modifying the engine

The engine (`cnt.py` / `cnt.R`) is locked behind the determinism gate. Any
modification must reproduce all 25 corpus content_sha256 values bit-for-bit
or be accompanied by a documented schema bump.

**Local checklist:**

- [ ] State the change in plain language (one paragraph).
- [ ] Run `python3 tools/verify_package.py` — must show all 25 corpus experiments PASS.
- [ ] If any experiment drifts, this is a real signal — go to Section 10 (corpus-drift recovery).
- [ ] If the change introduces new fields, bump `metadata.schema_version` and update [`HCI-CNT/handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md`](HCI-CNT/handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md) schema reference.
- [ ] R port (`cnt.R`) updated to parity if Python engine changed.
- [ ] Engine signature line updated.
- [ ] CHANGELOG entry written.

**Canonical document:** [`HCI-CNT/engine/README.md`](HCI-CNT/engine/README.md) + [`HCI-CNT/handbook/VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md`](HCI-CNT/handbook/VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md).

---

## Section 5 — Pushing to origin/main

The push pre-flight is the system's most-tested checklist. 16 items, all must
be true before the canonical repo is allowed to push.

**Local checklist:** [`ai-refresh/PREPARE_FOR_REPO.json`](ai-refresh/PREPARE_FOR_REPO.json) → `push_checklist` runs:

1. all_files_present
2. pipeline_complete
3. locales_complete
4. counts_consistent
5. all_experiments_rerun
6. stress_test_passed
7. executive_summary_current
8. hci_cnt_integrated
9. three_handbook_volumes_present
10. codawork_demo_complete
11. admin_json_files_updated
12. ai_refresh_updated
13. machine_manifest_pointers_correct
14. no_blocking_issues
15. cnt_determinism_gate_passes
16. governance_drift_audit_passed
→ READY_TO_PUSH must be `true`

**After the push:** verify the GitHub Actions `Validate Repository #N`
workflow goes green. The push is **not verified** until both signals are
green; until then, the canonical local repo is the recovery source per the
dual-folder protocol.

**Canonical documents:** [`ai-refresh/PREPARE_FOR_REPO.json`](ai-refresh/PREPARE_FOR_REPO.json) + [`ai-refresh/HS_MACHINE_MANIFEST.json`](ai-refresh/HS_MACHINE_MANIFEST.json) → `fault_tolerance_dual_folder_method`.

---

## Section 6 — Cowork session start

A new Claude Cowork (or other AI) session arrives blind. The cold-start
reading list gives it the operational knowledge of an experienced
practitioner in about 30 minutes.

**Local checklist (Cowork operator runs):**

- [ ] Confirm the AI is editing the **mirror folder** at `D:\HUF_Research\Claude CoWorker\Current-Repo\Hs`, NOT the canonical local repo.
- [ ] Brief the AI: "this is a Cowork mirror; you do not push to git; respect the dual-folder protocol."

**Tier-1 reading list (AI runs):**

- [ ] [`ai-refresh/HS_MACHINE_MANIFEST.json`](ai-refresh/HS_MACHINE_MANIFEST.json) — system pointer block + dual-folder protocol.
- [ ] [`ai-refresh/HS_ADMIN.json`](ai-refresh/HS_ADMIN.json) — current state, push history, registered ai_helpers.
- [ ] [`OPERATIONS_PROTOCOL.md`](OPERATIONS_PROTOCOL.md) — this file.
- [ ] [`ai-refresh/CCTT_RUNBOOK.md`](ai-refresh/CCTT_RUNBOOK.md) — if the session involves a compositional analysis.

**Canonical document:** [`ai-refresh/HS_MACHINE_MANIFEST.json`](ai-refresh/HS_MACHINE_MANIFEST.json) → `fault_tolerance_dual_folder_method`.

---

## Section 7 — Cowork session end

Don't leave a session with surprises pending in the mirror.

**Local checklist:**

- [ ] All edits are saved (no unwritten Edit tool calls in queue).
- [ ] Surface to the user every file modified during the session, with rough byte/line counts.
- [ ] If admin JSONs were touched, validate them parse (`python3 -c "import json; json.load(open(p))"`).
- [ ] Identify any file that needs to be synced into the canonical local repo before next push.
- [ ] If any GitHub Actions workflows are still running, note it; don't claim a push is verified until the workflow goes green.

---

## Section 8 — Bringing a new AI assistant on cold-start

Same as Section 6, with one extra step: confirm the AI can read files and
execute shell commands in the sandbox before you start serious work.

**Local checklist:**

- [ ] AI confirms it can read `OPERATIONS_PROTOCOL.md` and `HS_MACHINE_MANIFEST.json`.
- [ ] AI confirms it understands the Cowork mirror is not canonical.
- [ ] AI executes a no-op shell command (`ls`) and confirms it sees the repo root.
- [ ] AI follows the tier-1 reading list from Section 6.

**Canonical document:** [`ai-refresh/CCTT_RUNBOOK.md`](ai-refresh/CCTT_RUNBOOK.md) "How to use this runbook" section.

---

## Section 9 — Push fails Actions validation

The `Validate Repository #N` workflow went red. This is rare (5/5 most recent
pushes #15-#19 went green), but here's the recovery path.

**Local checklist:**

- [ ] Pull the workflow logs at `https://github.com/PeterHiggins19/higgins-decomposition/actions/runs/<run_id>`.
- [ ] Identify which validation step failed (file present, pipeline, locale, count, experiment-rerun, stress-test, doctrine-drift, etc.).
- [ ] Map the failure back to its Section 1-12 transition (e.g. a determinism-gate failure routes to Section 10).
- [ ] Fix in the canonical local repo, run the local equivalent of the failed check, push the fix.
- [ ] Mark the original push as not-verified in the AI_REFRESH note for the day.

---

## Section 10 — Determinism-gate experiment drifts

The engine is deterministic. If a corpus experiment's `content_sha256` no
longer matches its INDEX entry, that is a **real signal** — either the
input data changed or the engine version changed. Do not "fix" by updating
the INDEX without understanding why.

**Local checklist:**

- [ ] Compare regenerated `diagnostics.content_sha256` to `INDEX[id].content_sha256`. Record both.
- [ ] Compare regenerated `input.source_file_sha256` to a freshly-computed `sha256sum <input>.csv`. If different, the **input changed** — locate the change before doing anything else.
- [ ] Compare regenerated `metadata.engine_version` to the canonical engine version. If different, the **engine drifted** — Section 4 applies.
- [ ] If both inputs are unchanged but the output drifted, the engine has a non-determinism bug. STOP. Do not push. Surface to user with full diff.

**Canonical document:** [`HCI-CNT/handbook/VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md`](HCI-CNT/handbook/VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md).

---

## Section 11 — Documentation update

Handbook volumes, READMEs, or admin JSONs are being edited.

**Local checklist:**

- [ ] If editing one of the three handbook volumes, update the cross-references in the other two if needed.
- [ ] If editing a folder README, check that it still points at the current canon (engine 2.0.4 / schema 2.1.0).
- [ ] If editing an admin JSON (HS_ADMIN, HS_MACHINE_MANIFEST, PREPARE_FOR_REPO), validate it parses (`python3 -c "import json; json.load(open(p))"`) before saving.
- [ ] If adding a new top-level README, add it to the folder-README sweep coverage report (currently 100% — see [`PUSH_BUNDLE_AUDIT.md`](PUSH_BUNDLE_AUDIT.md)).
- [ ] No tone drift — supportive/additive framing across the whole document family (see [`AI_REFRESH_2026-05-05_v1.1.x.md`](ai-refresh/AI_REFRESH_2026-05-05_v1.1.x.md) for the locked tone).

---

## Section 12 — Reviewer requests reproducibility

An external auditor (CodaWork reviewer, journal referee, partner lab) asks
"can I re-run this myself?". The answer is yes; here's the 30-second
recipe to give them.

**Local checklist (the recipe to share):**

```bash
# 1. Clone the repo
git clone https://github.com/PeterHiggins19/higgins-decomposition.git
cd higgins-decomposition

# 2. Run the engine on the example experiment
python3 HCI-CNT/engine/cnt.py \
  experiments/Hs-05_Geochemistry/region_binning/tappe_kim1_by_country_barycenters.csv \
  -o /tmp/check.json \
  --ordering-method by-label

# 3. Verify the gate
python3 -c "
import json
expected = '707034ecc512c29df57e73fcb68466e10611bc63cc3c4d88a4b2152ff39e4063'
got = json.load(open('/tmp/check.json'))['diagnostics']['content_sha256']
print('PASS' if expected == got else 'FAIL', got)
"
# Expected output: PASS 707034ec...
```

The reviewer can substitute any of the 25 corpus experiments. Full corpus:
[`HCI-CNT/experiments/INDEX.json`](HCI-CNT/experiments/INDEX.json).

For the full operations protocol behind any single result, see the relevant
section above. For a researcher who wants to re-do the analysis from raw
data, see [`ai-refresh/CCTT_QUICKSTART.md`](ai-refresh/CCTT_QUICKSTART.md).

---

## Section 13 — Validating a result using the quaternion view (Volume IV)

As of 2026-05-07, the canonical handbook includes Volume IV — the Quaternion View, which names
the algebra CNT has been computing in.  This adds an optional second verification path:
any CNT result whose `diagnostics.content_sha256` matches the corpus can additionally be
checked against its quaternion-view consistency by computing the per-timestep quaternion
sandwich-product reconstruction.

**Local checklist (optional, for D=4 datasets):**

- [ ] Read the engine's CNT JSON; confirm `diagnostics.content_sha256` matches expected.
- [ ] Compute the Helmert-projected unit-vector trajectory.
- [ ] For each consecutive pair, compute the rotation quaternion and verify the sandwich
      product `q · v · q*` reproduces the next timestep.  Gate: max diff ≤ 1e-12 (typical: ≈ 1e-16, IEEE floor).
- [ ] Verify `M_squared_I_residual` is at IEEE floor (typical: ≈ 7e-17).

If both checks pass, the result is doubly verified: once against the canonical determinism
gate, once against the quaternion-algebra interpretation.  Two independent paths confirming
each other is stronger than one.

**Canonical document:** [`HCI-CNT/handbook/VOLUME_4_QUATERNION_VIEW.md`](HCI-CNT/handbook/VOLUME_4_QUATERNION_VIEW.md)

Reference reproduction script (in the QD experimental folder, outside the canonical repo):
`Quaternion Decomposition/QD_round_2.py` — performs the Concept-1 sandwich-product test on
any D=4 CNT JSON, reproducing the IEEE-floor result documented in Volume IV §B.1.

---

## Section 14 — Maintaining the Investigation Catalog (push #24, 2026-05-08)

The Investigation Catalog at [`ai-refresh/INVESTIGATION_CATALOG.json`](ai-refresh/INVESTIGATION_CATALOG.json)
(plain-text companion: [`ai-refresh/INVESTIGATION_CATALOG.md`](ai-refresh/INVESTIGATION_CATALOG.md))
is the canonical record of every speculative branch / hypothesis raised by any AI session,
user contributor / researcher, or experimental pilot. Each investigation carries one of four
dispositions: **CANONICAL**, **DEFERRED**, **FALSIFIED**, or **OPEN**. The catalog formalises
the framework's research methodology — a single place to see what has been tried, what
landed, what's still open, and what was killed and why.

**When to add a new entry:**

- A new speculative branch is raised in any AI cross-check pass and is worth more than
  a throwaway remark (analogous to EITT's 5% carrier-contribution threshold — when in
  doubt, err toward inclusion).
- A new pilot is proposed (with explicit gate criteria for what would promote it).
- A canonical artifact is added or moved.
- An idea is tested experimentally or analytically and refuted (FALSIFIED).

**Local checklist when raising / updating an investigation:**

- [ ] Append entry to `ai-refresh/INVESTIGATION_CATALOG.json` with next sequential id.
- [ ] Required fields populated (id, title, raised_by, raised_date, raised_in_push, disposition, summary).
- [ ] Disposition-specific fields populated (gate_criteria for OPEN/DEFERRED, falsification_record for FALSIFIED, canonical_location for CANONICAL).
- [ ] Update `summary_by_disposition` and `summary_by_source` counts.
- [ ] Mirror new/changed entry into the disposition table in `INVESTIGATION_CATALOG.md`.
- [ ] If the investigation is being **promoted** (OPEN → CANONICAL), cross-reference the supporting commit, pilot report, or experiment JSON.
- [ ] If the investigation is being **falsified** (any → FALSIFIED), capture what was tested, what was expected, what was observed, and any reformulation that survives.

**Promotion-gate discipline:**

Investigations are promoted to CANONICAL only when their stated gate criteria are met.
The DADC origin (INV-008) was promoted because the gate was external verification against
the Rogue-Wave-Audio repo and that verification ran cleanly. CNQ-Q (INV-013) sits at
DEFERRED because its gate is a working computational pilot on public CKM data that has
not yet been run. The discipline is demonstration-first; mathematical coherence alone
is not sufficient for promotion.

**Falsification is data:** Round 2.5's Concept 4 (P2 = fermion / P1 = boson) was tested
against Planck CMB and refuted. The refutation produced the cleaner reformulation
(LIMIT_CYCLE_P2 is universal). The falsified conjecture stays on record because the
audit trail is what gives the reformulation its credibility.

---

## When in doubt

Three rules:

1. **The hashes carry the receipts.** When you don't know whether a result is good, re-run and compare SHAs. The engine is deterministic; if the hashes match, the result is good.

2. **The user governs.** No transition in this protocol bypasses the user-confirmation gate. An AI may execute the steps, but the user confirms at every gate that matters.

3. **The mirror is not canonical.** Cowork edits land in the mirror; pushes originate from the canonical local repo; truth lives on `origin/main` after the GitHub Actions workflow goes green. See [`ai-refresh/HS_MACHINE_MANIFEST.json`](ai-refresh/HS_MACHINE_MANIFEST.json) → `fault_tolerance_dual_folder_method`.

---

## How this protocol is itself maintained

This file is part of the documentation update transition (Section 11). Edit
it the same way you'd edit any other admin doc: validate the markdown, check
that all referenced files still exist, update the transition map if you've
added or removed a transition.

The pilot exercise that proved this protocol functions end-to-end on the
live repo lives at [`OPERATIONS_PROTOCOL_PILOT_REPORT.md`](OPERATIONS_PROTOCOL_PILOT_REPORT.md).

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
*The protocol holds the line so the work can move forward.*
