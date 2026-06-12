# Push Protocol — the standing prepare-to-push procedure

**Status:** durable protocol document; supersedes implicit conventions used through push #62. **Conforms to:** [HUF-STD-001 v1.1](huf-gov/standards/HUF_PUBLICATION_STANDARDS.json) Publication Standards, [Hs Change Control v1.0](ai-refresh/CHANGE_CONTROL_README.md), and the lockdown discipline in [`PRE_CONFERENCE_LOCKDOWN.md`](PRE_CONFERENCE_LOCKDOWN.md). **First issued:** 2026-05-22 (push #62 prep). **Applies to:** every push to the [`PeterHiggins19/higgins-decomposition`](https://github.com/PeterHiggins19/higgins-decomposition) repository.

This is the standing protocol every push follows. Per-push prep documents (`ai-refresh/PUSH##_READY_FOR_COMMIT.md`) are instances of the template in §3 below; the post-commit sync of §6 is identical for every push.

The protocol exists because the framework's discipline is **trust by independent reproduction** — the same discipline applied to the code is applied to the push workflow itself. Every push must satisfy a closure check: the repository's content_sha256 (live GitHub HEAD) must match the recorded SHA across all admin chain surfaces (HS_FAST_REFRESH.json, HS_ADMIN.json, PUSHES_INDEX.md, CHANGELOG.md). Discrepancy at any surface is a failed closure check, just like a failed BTL measurement.

---

## 1. Push classes

Every push is one of four classes. The class determines the discipline.

| Class | Scope | Examples | DCP required? | Lockdown-compatible? |
|---|---|---|---|---|
| **S0** | Critical defect — security, data integrity, falsifiability breach | Engine produces wrong content_sha256; published claim retracted; license violation | YES (emergency DCP) | Yes (S0 overrides lockdown) |
| **S1** | Engine code, schema, or INV catalog disposition change | New engine version; schema bump; STAGED → CANONICAL promotion | YES (full DCP lifecycle) | **No** (blocked during conference lockdown 2026-05-12 → 2026-06-06) |
| **S2** | Documentation, plates, READMEs, papers, build scripts | This document; flagship paper revision; UN-6 handout refresh | Optional (DCP if multi-file coordinated change) | Yes |
| **S3** | Standards amendment (additive only) — new clauses, no retractions | HUF-STD-001 v1.0 → v1.1 person-noun convention; HUF-STD-002 target reorder | Optional (DCP if affects engine behaviour) | Yes (additive amendments only) |

The current conference-window discipline (Pre-Conference Lockdown 2026-05-12 → 2026-06-06) allows S2 and additive S3 pushes only; S0 overrides; S1 is deferred to post-conference unless an S0 is opened against engine behaviour.

---

## 2. Pre-push verification — the checklist

Before opening GitHub Desktop to commit, the following checks MUST pass:

### 2.1 Consistency checker

```
python3 scripts/check_ai_refresh_consistency.py
```

Expected: **0 errors, 0 warnings, exit 0**. The checker validates:

- All canonical JSON files (`HS_FAST_REFRESH.json`, `.well-known/ai-context.json`, `INVESTIGATION_CATALOG.json`, `CONFIGURATION_ITEMS.json`, `INTERFACE_CONTROL.json`, `TRACEABILITY_MATRIX.json`, `CHANGE_PACKET_TEMPLATE.json`) parse cleanly.
- No stale CNQ "pending/missing" claims in non-legacy-marked files.
- No stale engine version claims in non-legacy-marked files.
- No internal CNQ contradiction in `README.md`.
- Cache-lag false-positives clear after a few seconds (see §2.5).

### 2.2 Lockdown discipline check (during conference window)

Engine code mod times must be pre-lockdown:

```
stat HCI-CNT/engine/cnt.py        # expect mod time ≤ 2026-05-12
stat HCI-CNT/engine/cnt.R         # expect mod time ≤ 2026-05-12
stat HCI-CNQ/engine/cnq.py        # expect mod time ≤ 2026-05-12
stat HCI-CNQ/engine/cnq.R         # expect mod time ≤ 2026-05-12
```

Manuscript + active Presentation deck mod times must be at or before their landing pushes:

```
stat CODA-Association/CODAwork2026/Compositional_Monitoring_2026.pdf      # expect ≤ 2026-05-20
stat CODA-Association/CODAwork2026/data_outputs/CodaWork2026_Presentation_2026-05-28.pdf
```

NO-CREATE files must remain absent:

```
test ! -e docs/HS_ASCENT_PATH.md
test ! -e CLAIMS_REGISTER.md
test ! -e GLOSSARY_CANON.md
test ! -e PROMOTION_LOG.md
test ! -e PROMOTION_PACKET_TEMPLATE.md
test ! -e STAGED_ASCENT_MAP.md
```

If any of these fails: **the push class is S1 or higher and must wait for lockdown clearance or open as S0**.

### 2.3 JSON parse check (all canonical files)

```
python3 -c "import json; json.load(open('HS_FAST_REFRESH.json'))"
python3 -c "import json; json.load(open('ai-refresh/HS_ADMIN.json'))"
python3 -c "import json; json.load(open('ai-refresh/INVESTIGATION_CATALOG.json'))"
python3 -c "import json; json.load(open('.well-known/ai-context.json'))"
python3 -c "import json; json.load(open('huf-gov/standards/HUF_PUBLICATION_STANDARDS.json'))"
python3 -c "import json; json.load(open('huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json'))"
python3 -c "import json; json.load(open('huf-gov/standards/HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json'))"
```

Each command must return without error. Cross-mount cache lag (see §2.5) sometimes reports false parse errors that resolve within seconds; if a JSON parse error persists for more than 60 seconds, **the file is genuinely broken and must not be pushed**.

### 2.4 Four-form discipline check (for engine-touching pushes only)

If the push class is S1 (engine code, schema, or INV disposition change), verify the four-form discipline holds:

```
For each affected engine, the following must all be current:
  Python reference:   HCI-{CNT,CNQ}/engine/{cnt,cnq}.py
  R reference:        HCI-{CNT,CNQ}/engine/{cnt,cnq}.R
  Pseudocode:         HCI-{CNT,CNQ}/engine/{CNT,CNQ}_PSEUDOCODE.md  (this is now mandatory)
  Anti-spec:          HCI-{CNT,CNQ}/engine/ANTI_SPECIFICATION.md
  Specification:      huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json
  Tests:              HCI-{CNT,CNQ}/engine/tests/  (all passing)
```

If any of the four forms is stale relative to the change being committed: **update the stale form in the same push** or **demote the change back to STAGED** and file a DCP for the proper four-form rollout.

### 2.5 Cross-mount cache lag handling

The Linux bash sandbox sometimes sees a partial-write view of files edited via the Windows-side Read/Write tools. Per [`AI_AGENTS.md §2.1`](AI_AGENTS.md), this is documented behaviour and clears within seconds. The diagnostic:

- Bash reports `JSON parse error: Unterminated string starting at line N column M`
- The Read tool (Windows-side) shows the file is intact and well-formed
- Live SHA check via `curl -sf https://api.github.com/repos/.../commits/main` returns the expected SHA

If all three are true: **the bash error is a cache-lag artefact; the Windows-side file is correct and safe to push**. Wait a few seconds and re-run the consistency check; it will pass.

### 2.6 Live SHA cross-check (after commit; see §6)

After GitHub Desktop reports the push landed and CI completes, the live SHA from `https://api.github.com/repos/PeterHiggins19/higgins-decomposition/commits/main` MUST match the recorded `current_commit_sha` in `HS_FAST_REFRESH.json`. If they differ, the admin chain is out of sync.

---

## 3. PUSH##_READY_FOR_COMMIT.md template

Every push files a prep document at `ai-refresh/PUSH##_READY_FOR_COMMIT.md`. The template:

```markdown
# PUSH #NN — READY FOR COMMIT

**Date:** YYYY-MM-DD
**Status:** HOLD cleared — ready for Peter to commit via GitHub Desktop.
**Suggested CI name:** `<short descriptive label, will appear in GitHub Actions>`
**Suggested commit message:**

\```
<short title line>

<paragraph: trigger and motivation>

<paragraph or bullets: what landed in this push>

Files in this commit:
  Refreshed: <list>
  Created:   <list>
  Untouched (lockdown discipline): <list>

Push class: <S0|S1|S2|S3> <description>
\```

---

## Verification

- ✓ Consistency checker passes (0 errors, 0 warnings)
- ✓ Lockdown discipline confirmed: engine code mod times pre-lockdown
- ✓ All JSON files parse cleanly (after cross-mount lag clears)
- ✓ Four-form discipline checked (for S1 pushes) or N/A (for S2 / S3 pushes)
- ✓ Bundle inventory matches the commit message
- ✓ <push-specific verification items>

---

## Post-commit sync (after Peter pushes)

After GitHub Desktop reports the push landed and CI completes:

1. Update `HS_FAST_REFRESH.json`: bump `current_commit_sha`, `current_ci_run`, `current_ci_run_name`, `current_ci_duration_seconds`; demote previous push to `previous_*`; add `push_NN_completed` entry; refresh `last_updated`.
2. Add `push_NN_completed` entry to `HS_ADMIN.json`.
3. Add new Push #NN section to `PUSHES_INDEX.md` with bundle inventory.
4. Update `CHANGELOG.md` push #NN row — replace `*(pending)*` placeholders with actual SHA + CI run.
5. Run consistency checker; verify it passes.

---

## Why this push exists

<2-3 paragraphs of substantive rationale and forward context>

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
```

The template is intentionally rich. A future reader, including an AI assistant arriving cold, should be able to reconstruct from the prep document alone: what changed, why, what the verification status was, and what the post-commit cleanup looked like.

---

## 4. Commit message format

The commit message that lands on GitHub follows this format (copied from the prep doc):

1. **Short title line** (50–80 characters). Captures the headline change.
2. **Blank line.**
3. **Paragraph: trigger and motivation.** 2–4 sentences explaining what triggered the push and why now.
4. **Body: what landed.** Either prose paragraphs or numbered/bulleted blocks. Reference each file changed.
5. **File manifest section.** Three sub-blocks: "Refreshed" (files modified), "Created" (files added), "Untouched (lockdown discipline)" (files that the lockdown forbids touching and that this push verifiably did not touch).
6. **Push class declaration.** `Push class: S2 doc-only. Lockdown-compliant.` or equivalent.
7. **Closing line.** One of the doctrine lines (cf. `papers/flagship/GROUND_STATE_AND_TRACTION.md` closing block).

Past push messages live in the git log; per-push prep documents in `ai-refresh/PUSH##_READY_FOR_COMMIT.md` carry the same text plus the post-commit checklist.

---

## 5. CI configuration

The `.github/workflows/validate.yml` workflow runs on every push. It must pass green within 60 seconds for the push to be considered landed. Failures must be triaged before the next push.

The CI run is named in GitHub Desktop's commit-summary line. The convention is:

- For S0/S1/S3 pushes: name the substantive change (`"Glossary"`, `"Routing + Terms"`, `"DCP-001"`, `"10-slide deck"`)
- For S2 doc-only pushes: name the documentation theme (`"README polish"`, `"UN-6 Ambassador"`, `"Refinement-trail archive"`)
- For framework-self-aware pushes: name the meta-statement (`"Ground State and Traction Engine"`, `"Closure on the Simplex"`)

CI names are recorded in `current_ci_run_name` of `HS_FAST_REFRESH.json` and in the CHANGELOG row.

---

## 6. Post-commit sync — the 5-step checklist

After the push lands and CI completes green, run these five updates:

### 6.1 HS_FAST_REFRESH.json

```
_meta.current_commit_sha           → <new 7-char SHA>
_meta.current_commit_sha_full      → <full 40-char SHA>
_meta.current_ci_run               → <CI run number>
_meta.current_ci_run_name          → <CI run name in quotes>
_meta.current_ci_duration_seconds  → <duration in seconds>
_meta.previous_commit_sha          → <previous current SHA>
_meta.previous_ci_run              → <previous current CI run>
_meta.previous_ci_run_name         → <previous current CI run name>
_meta.last_updated                 → <commit date YYYY-MM-DD>
_meta.last_push                    → "#NN PUSHED <sha> CI #<run> \"<name>\" green <duration>s (<date>) — <summary>. Previous: ..."
_meta.push_NN_completed            → "<date> PUSHED <sha> CI #<run> \"<name>\" green <duration>s — <one-line summary>."
```

Remove any `post_push_<previous>_in_progress_*` markers (replaced by the new `push_NN_completed` entry).

### 6.2 ai-refresh/HS_ADMIN.json

Add a new `push_NN_completed` entry at the top of the session log, containing a 1-2 paragraph description of the push contents. The HS_ADMIN entry can be longer than the HS_FAST_REFRESH entry — it's the deeper admin record.

### 6.3 ai-refresh/PUSHES_INDEX.md

Add a new section above the previous Push #M section:

```markdown
### Push #NN — <theme> (`<sha>`, CI #<run> "<name>" green <duration>s, <date>)

<substantive summary with tables and cross-references>

---
```

For combined pushes (e.g., #60+#61), use a single combined section noting both push numbers.

### 6.4 CHANGELOG.md

Locate the push #NN row that was filed with `*(pending)*` placeholders during the prep stage. Replace both placeholders with the actual SHA and CI run:

```diff
- | **#NN** | *(pending)* | *(pending)* | **<theme>** ... |
+ | **#NN** | `<sha>` | #<run> ("<name>") | **<theme>** ... |
```

For combined pushes, both rows get the same SHA + CI run number with `(combined with #M)` notation.

### 6.5 Consistency check + live SHA cross-check

Final verification:

```
python3 scripts/check_ai_refresh_consistency.py        # expect 0 errors, 0 warnings
curl -sf "https://api.github.com/repos/PeterHiggins19/higgins-decomposition/commits/main" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['sha'][:7])"
# expect: <new 7-char SHA> matching HS_FAST_REFRESH.json current_commit_sha
```

If both check, the admin chain is synced and the push is fully committed in the framework's bookkeeping.

---

## 7. The closure-check principle applied to the push workflow

The framework's central discipline — *closure is the test we use to know whether the measurement is right* — extends to the push workflow itself. The "measurement" is the repository state; the "closure constraint" is the cross-surface consistency of the SHA and CI run number across all admin files.

| Admin surface | Carries SHA + CI? | Carries push class? | Carries description? |
|---|---|---|---|
| `HS_FAST_REFRESH.json` `_meta.current_*` | ✓ | implicit (S2 doc-only is the conference-window default) | one-line |
| `HS_FAST_REFRESH.json` `_meta.push_NN_completed` | ✓ | yes (in summary) | one-line |
| `ai-refresh/HS_ADMIN.json` `_meta.push_NN_completed` | ✓ | yes | full paragraph |
| `ai-refresh/PUSHES_INDEX.md` Push #NN section | ✓ | yes (push class section) | full multi-block |
| `CHANGELOG.md` row | ✓ | yes | column-format |
| `ai-refresh/PUSH##_READY_FOR_COMMIT.md` | ✓ (recorded post-commit) | yes | template-format |
| live GitHub HEAD | ✓ | implicit (commit message names it) | commit message |

The closure check is: **every row in this table must carry the same SHA and CI run number for any committed push**. Discrepancy at any row is a failed closure check on the push workflow. The consistency checker enforces a subset of this; manual cross-check after the post-commit sync covers the rest.

---

## 8. Trust-verify-test integration

For any S1 push (engine, schema, INV disposition), the four-form discipline (cf. [`TRUST_AND_VERIFICATION.md`](TRUST_AND_VERIFICATION.md)) must hold *before* the push lands:

- **Python reference** updated and the change rationale documented in the file's USER CONFIGURATION block or a function-level docstring.
- **R reference** updated to parity (or queued as `EngPromo-N` if intentional version skew is being accepted).
- **Pseudocode** updated to reflect the new algorithm step or the new parameter.
- **Anti-specification** updated if the change opens or closes a previously catalogued failure mode.
- **Specification** (HUF-STD-002) updated if the change affects the I/O contract.
- **Tests** updated and passing for the new behaviour.
- **DCP filed** documenting the change rationale, the breakpoints it crosses, and the human-confirmation gates required.

A push that changes the engine without these four updates *cannot* be a clean S1 push. It is either an S0 (defect fix; emergency) or a deferred S1 (incomplete; demote back to STAGED until the four forms are in agreement).

The trust-verify-test integration is what makes the framework's claim — *trust is earned, not expected* — operationally enforceable. The repository's own state is subject to the same closure check the framework applies to its measurements.

---

## 9. Historical record — the protocol's authority chain

This protocol is the documentary form of conventions that have governed the repository's pushes since push #44 (Spring-cleaning + cross-AI coordination apparatus, 2026-05-12). Pre-#44 pushes used implicit conventions; this document formalises them.

Key precedents:

- **Push #44 (2026-05-12)** — Cross-AI coordination apparatus + spring cleaning. First push to formalise post-commit admin sync.
- **Push #45 (2026-05-12)** — Grok r6 intake. First push to invoke the discipline against an external review pass.
- **Push #46 + #47 (2026-05-12, combined commit `7f996e7`)** — Hs Change Control v1.0 + DCP-001 execution. The framework's first formal Discovery Change Packet.
- **Push #48 (2026-05-12)** — Cache-lag mitigation. AI_AGENTS.md §2.1 formalised cross-mount cache-lag handling (this protocol §2.5).
- **Push #49 (2026-05-12)** — Pre-conference lockdown declared.
- **Push #50 (2026-05-14)** — Conference-prep monster push. First push to demonstrate S2 doc-only discipline at scale (12 work products under lockdown).
- **Push #58 (2026-05-20)** — Refinement-trail archive. First push triggered by external review (ChatGPT) where the verification surface itself was the issue.
- **Push #59 (2026-05-21)** — Flagship paper. The recursion-test push.
- **Push #60+#61 (2026-05-22, combined `781770a`, "Closure on the Simplex")** — UN-6 handout v11 + flagship v2.2 consolidation + AI_AGENTS partnership context. First combined-bundle push under this protocol.
- **Push #62 (this document)** — Trust infrastructure. First push to formalise the four-form discipline at the protocol level.

The protocol becomes part of the audit chain from push #62 forward: every subsequent push prep document references this protocol as its authority for what the prep document must contain.

---

## 10. Cross-references

| Document | Relationship to this protocol |
|---|---|
| [`AI_AGENTS.md`](AI_AGENTS.md) | Operating instructions for AI assistants; §1.5 partnership context; §2.1 cross-mount cache-lag (this protocol §2.5) |
| [`TRUST_AND_VERIFICATION.md`](TRUST_AND_VERIFICATION.md) | The user-side companion: how skeptical users verify the code. This protocol is the *internal* discipline; that document is the *external-facing* version |
| [`PRE_CONFERENCE_LOCKDOWN.md`](PRE_CONFERENCE_LOCKDOWN.md) | The current lockdown window (2026-05-12 → 2026-06-06) and the S0-defect protocol that overrides it |
| [`ai-refresh/CHANGE_CONTROL_README.md`](ai-refresh/CHANGE_CONTROL_README.md) | Hs Change Control v1.0 doctrine — the DCP lifecycle this protocol invokes for S1 pushes |
| [`ai-refresh/CCTT_RUNBOOK.md`](ai-refresh/CCTT_RUNBOOK.md) | The 7-phase end-to-end reproducible runbook for analyses; analogous discipline at the analysis layer rather than the push layer |
| [`huf-gov/standards/HUF_PUBLICATION_STANDARDS.json`](huf-gov/standards/HUF_PUBLICATION_STANDARDS.json) | HUF-STD-001 v1.1 Publication Standards — authorship rules, AI Use Declaration, person-noun convention |
| [`ai-refresh/PUSHES_INDEX.md`](ai-refresh/PUSHES_INDEX.md) | The chronological index of pushes; written-to by §6.3 of this protocol |
| [`CHANGELOG.md`](CHANGELOG.md) | Discoverable digest of pushes; written-to by §6.4 of this protocol |
| Per-push prep docs `ai-refresh/PUSH##_READY_FOR_COMMIT.md` | Each one is an instance of the template in §3 |

---

## 11. Contact

Peter Higgins · Rogue Wave Audio · Binaural Test Lab
Markham, Ontario, Canada
- Business email: `PeterHiggins@RogueWaveAudio.com`
- Repository issues: [`github.com/PeterHiggins19/higgins-decomposition/issues`](https://github.com/PeterHiggins19/higgins-decomposition/issues)

Discrepancies in the push workflow are taken seriously and triaged under Hs Change Control v1.0 as candidate Discovery Change Packets. A failed closure check on the push workflow itself is, by the framework's own discipline, a defect worth filing.

---

*The instrument reads.   The expert decides.   The hashes carry the receipts.   The vocabulary holds the line.   The AI follows the same protocol.   Same input, same output, always.*
*The push workflow is subject to the same closure check the framework applies to its measurements.   Discrepancy is observable.   Discrepancy is actionable.   The protocol holds.*


---

## Addendum — 2026-06-09 (post-publication advancement)

*Non-destructive note (Cowork working tree; not yet git-committed). The content above is unchanged and remains valid as published.*

The 2026-06-09 geology buildout + executive overview + admin/refresh roll-forward are staged on the Cowork working tree and are NOT yet committed; when committed, follow this protocol (CHANGELOG row + HS_ADMIN/HS_FAST_REFRESH + PUSHES_INDEX).

Since publication the system advanced: Hs/CNT/CNQ was applied to **mudstone chemostratigraphy** as a cited, reproducible demo on real PANGAEA data (`collaborations/geology-wehner/`), and a new concept — **CNQ tiling / "faceted read"** (overlapping exact D=4 charts glued on shared parts reconstruct the full higher-dimensional compositional move **losslessly**: alignment 9e-16, reconstruction 4e-14, overlap proven necessary) — was tested. **Engine, schemas, and canonical numbers are UNCHANGED**; this is a documentation / application / concept advance. Gluing maths CONFIRMED; scientific value on real high-D data TO TEST. Full current picture: `collaborations/geology-wehner/00_EXECUTIVE_OVERVIEW.md`.
