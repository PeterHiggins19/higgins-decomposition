# Push #17 Audit Report — Community Standards & Presence Enhancement

**Date:** 2026-05-06
**Last validated push:** `a92c35b` (Validate Repository #16 — HCI updates)
**Next push:** #17 — community-standards files + README badges
**Status:** **READY TO PUSH**

---

## Live-repo state at #16 (verified)

A fresh clone of `https://github.com/PeterHiggins19/higgins-decomposition`
at commit `a92c35b` confirms push #16 cleanup is complete:

* All 8 EMBER per-country JSON snapshots now read `cnt 2.0.4 / schema 2.1.0`
* `experiments/INDEX.json` `_meta.engine` reads `cnt 2.0.4`, `_meta.schema` reads `2.1.0`
* No `__pycache__` files are tracked
* `tools/verify_package.py` returns **PACKAGE READY** from a fresh clone

One housekeeping item carried over: `HCI-CNT/conference_demo/talk_deck/lu4422tlij.tmp`
is still in tree (the previous `git rm` instruction wasn't applied).
The new `.gitignore` prevents future leaks but doesn't remove an
already-tracked file. Push #17 includes the explicit removal.

## GitHub community standards check

Visited `https://github.com/PeterHiggins19/higgins-decomposition/community`.
Of the seven standard community-health files GitHub recognises:

| File | Pre-#17 | Push #17 |
|---|---|---|
| Description | configured | unchanged |
| README | present | unchanged |
| License | present (CC BY 4.0) | unchanged |
| **Code of conduct** | missing | **added** (Contributor Covenant 2.1) |
| **Contributing guide** | missing | **added** |
| **Security policy** | missing | **added** |
| **Issue templates** | missing | **added** (3 templates: bug / feature / verification report) |
| **Pull request template** | missing | **added** |
| Citation file | present (CITATION.cff) | unchanged |

Plus optional:

| File | Pre-#17 | Push #17 |
|---|---|---|
| `.github/FUNDING.yml` | missing | **added** (placeholder, commented out — Peter to enable) |
| README badges | missing | **added** (CI status, license, engine version, schema version, experiment count, CodaWork 2026) |

When GitHub re-scans the community page after this push, all six
checklist items currently flagged as missing will be satisfied. The
green tick on the community-standards page is the most visible
presence boost a research repo can ship.

## Files added by push #17

```
CODE_OF_CONDUCT.md                      (Contributor Covenant 2.1)
CONTRIBUTING.md                         (orientation + verification + licensing)
SECURITY.md                             (vuln reporting + hash-chain verification)
.github/PULL_REQUEST_TEMPLATE.md
.github/FUNDING.yml                     (placeholder — uncomment to enable)
.github/ISSUE_TEMPLATE/bug_report.yml
.github/ISSUE_TEMPLATE/feature_request.yml
.github/ISSUE_TEMPLATE/verification_report.yml
ai-refresh/PUSH17_AUDIT_REPORT_2026-05-06.md   (this file)
```

## Files modified by push #17

```
README.md                               (badge row added under the title block)
```

## File to remove

```
HCI-CNT/conference_demo/talk_deck/lu4422tlij.tmp     (LibreOffice temp leak from deck build)
```

## What this buys for community presence

1. **Six new checks pass on the GitHub community-standards page** — the
   page's progress bar fills from 4/7 to 7/7, with three optional extras
   (FUNDING.yml, security policy, three issue templates beyond the basic
   bug/feature pair).

2. **The verification-report issue template** is unusual and on-brand:
   it invites readers to publish their re-runs against the published
   hash chain. This operationalises the Volume III §B argument
   (verification value to the CoDa community) directly inside the
   GitHub workflow.

3. **README badges** give a one-glance status row at the top of the
   repo home page — current CI status, current engine version, current
   experiment count, and a CodaWork 2026 marker that tracks the
   conference deliverable. The badges link directly into the relevant
   files in the repo.

4. **The licensing dual-track is now explicit in CONTRIBUTING.md**:
   Hˢ research is CC BY 4.0; HCI-CNT/ engine and atlas are Apache-2.0.
   Contributors agreeing to "the same terms as the file or folder you
   are modifying" makes the dual licence frictionless.

5. **The Contributor Covenant** is the de-facto industry standard.
   Universities, journals, and partner labs that run their own due
   diligence on a repo before engaging look for it specifically.

## Recommended commit + push

From the parent `Current-Repo/Hs/` directory:

```bash
git add CODE_OF_CONDUCT.md CONTRIBUTING.md SECURITY.md README.md
git add .github/FUNDING.yml .github/PULL_REQUEST_TEMPLATE.md .github/ISSUE_TEMPLATE/
git add ai-refresh/PUSH17_AUDIT_REPORT_2026-05-06.md
git rm  HCI-CNT/conference_demo/talk_deck/lu4422tlij.tmp
git commit -m "Community standards: add code of conduct, contributing, security, issue templates, PR template, README badges; remove stray temp file"
git push origin main
```

## After the push

GitHub's community-standards scanner re-runs automatically (typically
within minutes). Visit
`https://github.com/PeterHiggins19/higgins-decomposition/community`
to confirm the green ticks. The repo's social preview, search ranking,
and partner-lab due-diligence all benefit immediately.

If you want to enable the GitHub Sponsors button, uncomment the
`github:` line in `.github/FUNDING.yml` (one-line change). The other
items in the funding file are placeholders for future use.

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
