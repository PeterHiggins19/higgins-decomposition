# AI Refresh — 2026-05-06  (Push #19 verified + dual-folder fault-tolerance protocol)

**Engine:** cnt 2.0.4   **Schema:** 2.1.0   **Experiments:** 25 / 25 PASS
**Last validated commit on `main`:** `7d2b25e` (Validate Repository #19 — lock+temp-file cleanup)

## Headline

Pushes #15 through #19 are all verified green on
`https://github.com/PeterHiggins19/higgins-decomposition`. The repo is
ready for CodaWork 2026 review. **One operational note added today**:
the dual-folder fault-tolerance protocol is now formally documented in
`HS_MACHINE_MANIFEST.json` so future Claude Cowork sessions understand
that the Cowork mirror is not the canonical git tree.

## Push history through 2026-05-06

| Push | Commit | Theme |
|---:|---|---|
| #15 | `f38a7c9` | Initial HCI-CNT migration into Hˢ repo |
| #16 | `a92c35b` | INDEX.json engine version + per-country snapshots refresh |
| #17 | `0efda90` | Community-presence assets (CoC, CONTRIBUTING, SECURITY, templates) |
| #18 | `c9dec16` | `Hs-CNT_2026-05/` corpus + `Higgins_Coordinate_System/` docs refresh + 102 folder READMEs + `PUSH_BUNDLE_AUDIT.md` |
| #19 | `7d2b25e` | `talk_deck/` cleanup — `lu4422tlij.tmp` removed, soffice lock removed, `.gitignore` extended |

All five pushes triggered `Validate Repository #N` workflows that
completed with conclusion `success`. Live-repo spot-checks confirmed
the corpus snapshot at `experiments/Hs-CNT_2026-05/` (INDEX.json
18,600 B + 4 subdirs intact) and the HCI-CNT canon at root
(11 subfolders + `README.md` 7,328 B + `.gitignore`).

## Operational note: dual-folder fault-tolerance protocol

Peter operates a **deliberate two-folder method** for fault tolerance.
Future Claude Cowork sessions need to know this:

- **Cowork mirror** at `D:\HUF_Research\Claude CoWorker\Current-Repo\Hs`
  — this is the folder Claude Cowork has read/write access to. All
  Claude-driven edits land here first.
- **Canonical local repo** — a separate folder on Peter's machine
  that *is* the actual git working tree. Pushes originate from there,
  not from the Cowork mirror.

**Synchronisation flow:**

1. Claude edits land in the Cowork mirror.
2. Peter reviews + syncs the changed files into the canonical local repo.
3. Push procedure (per `PREPARE_FOR_REPO.json`) runs from the canonical repo.
4. GitHub Actions `Validate Repository #N` runs and is verified green.
5. Once the workflow conclusion is `success`, the push is **VERIFIED**.

**Recovery rules:**

- *Before push verified:* Either folder may be authoritative. If the
  Cowork mirror gets corrupted or an unintended edit lands, recover
  from the canonical local repo (and vice versa).
- *After push verified:* `origin/main` is the source of truth. Recover
  either folder from there.
- **Claude responsibility:** Claude Cowork edits only the Cowork mirror.
  Claude must not attempt to write to the canonical repo and must not
  push directly. Peter runs all `git push` operations.

This is canonically captured at:

- `ai-refresh/HS_MACHINE_MANIFEST.json` →
  `fault_tolerance_dual_folder_method` (full protocol)
- `ai-refresh/HS_ADMIN.json` → `_meta.fault_tolerance_note` and
  `engine.fault_tolerance` (pointer + summary)

## Triggered by

Push #19 went out as a small targeted cleanup (commit `7d2b25e`,
"remove lock and temp files"). During the live-repo verification I
observed two scratch files still on `main` after push #18 had
allegedly removed them:

- `HCI-CNT/conference_demo/talk_deck/lu4422tlij.tmp` (1,447,606 B —
  soffice scratch from PDF conversion)
- `HCI-CNT/conference_demo/talk_deck/.~lock.CodaWork2026_CNT_Talk.pdf#`
  (110 B — soffice live-lock file)

The cleanup commit I'd queued in `PUSH_BUNDLE_AUDIT.md` had not
landed because the `git rm` was applied in the Cowork mirror but
**the canonical local repo was the one that actually committed and
pushed** — and at the time of that commit, the soffice lock file was
still active on Peter's machine. Peter manually deleted the files
from the canonical repo and pushed #19; that is when this dual-folder
distinction became operationally important to capture.

## Current readiness state

- 25 / 25 experiments PASS the determinism gate.
- Three handbook volumes locked (Theory / Practitioner / Verification).
- Three CoDa-community preprints filed at `HCI-CNT/coda_community/`.
- 10-slide CodaWork 2026 talk deck at
  `HCI-CNT/conference_demo/talk_deck/CodaWork2026_CNT_Talk.{pptx,pdf}`.
- 102 folder-level READMEs in place — every navigable folder has
  orientation copy.
- Repo cleanly ready for CodaWork 2026 review.

## Open items (non-blocking)

- Hs-Lab 12-component integration (plan in Volume II §H).
- Raw-data swap-in for the 5 extended adapters (checklist in Volume II §C,
  ~1.5 person-days for the 3 practical swaps).
- Stage 5+ exploration when desired.
