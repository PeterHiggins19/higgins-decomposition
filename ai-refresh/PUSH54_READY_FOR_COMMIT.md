# PUSH #54 — READY FOR COMMIT

**Date:** 2026-05-19
**Status:** HOLD cleared — ready for Peter to commit via GitHub Desktop.
**Suggested CI name:** `Glossary merge`
**Suggested commit message:**

```
Glossary merge — GLOSSARY v3.0 + NOTATION redirect stub

Combine HCI-CNT/handbook/GLOSSARY.md v2.0 and
HCI-CNT/handbook/NOTATION_AND_TERMINOLOGY.md v2.0 into a single
authoritative reference at GLOSSARY.md v3.0 (~220 entries across
30 sections, 661 lines). NOTATION_AND_TERMINOLOGY.md reduced to
an 81-line redirect stub.

Adds ~50 net new entries:
- §1 Foundational mathematics (PCA, SVD, eigenvalue, eigenvector,
  Spectral Theorem)
- §2 Statistical concepts (Lyapunov, Feigenbaum, CHSH, Tsirelson)
- §21 MC-1 / MC-2 / MC-3 (previously only MC-4 documented)
- §25 Instrument-family lineage (RWA, BTL, HUF, Hs, V_Core, DADC)
- §28 Abbreviations A-Z (PCA, SVD, EITT, CHSH, MC, ILR, CLR, ...)

Plus admin catch-up for pushes #52 (98ea1dd6 CI #49) and #53
(bfb1c41 CI #50) which landed but were not fully recorded.

Lockdown-compliant S2 doc-only. Engine code, schemas, INV catalog
dispositions, NO-CREATE files, papers/codawork2026/talk/, and
CODA-Association/CODAwork2026/data_outputs/ untouched.

Triggered by Peter's 2026-05-19 directive: "combine the glossary
with the terms and make the glossary and terms complete, include
simple and obscure references such as PCA and EITT, all huf and
coda terms, make it comprehensive."

The split made drift possible. The merge makes drift impossible.
```

---

## Files in this commit

```
HCI-CNT/handbook/GLOSSARY.md                     v2.0 → v3.0 (661 lines)
HCI-CNT/handbook/NOTATION_AND_TERMINOLOGY.md     v2.0 → v3.0 redirect stub (81 lines)
HS_FAST_REFRESH.json                              last_push → #54 HOLD
ai-refresh/HS_ADMIN.json                          push_52/53/54 entries added
ai-refresh/PUSHES_INDEX.md                        push #52/53/54 sections appended
ai-refresh/PUSH54_PRE_PUSH_SUMMARY.md             new
ai-refresh/PUSH54_READY_FOR_COMMIT.md             this file
```

---

## Verification status

- ✅ `GLOSSARY.md` v3.0 written — header declares v3.0, 661 lines.
- ✅ `NOTATION_AND_TERMINOLOGY.md` v3.0 redirect stub written — 81 lines, points to merged GLOSSARY.
- ✅ Cross-mount sync confirmed via bash `wc -l`.
- ✅ `HS_FAST_REFRESH.json` `last_push` and `last_updated` fields updated (Read-tool side, 2026-05-19).
- ✅ `HS_ADMIN.json` `push_52_completed` / `push_53_completed` / `push_54_prepared` entries added.
- ✅ `PUSHES_INDEX.md` push #52, #53, #54 hand-off table rows + catch-up sections appended.
- ⚠️ Bash-side JSON parse reports stale-mount false positives at lines unrelated to my edits — same cross-mount cache-lag issue documented in `AI_AGENTS.md §2.1` and previously logged for pushes #50 and #51. Will clear once mount syncs.

---

## Post-commit sync (after Peter pushes)

After GitHub Desktop reports the push landed and CI completes:

1. Update `HS_FAST_REFRESH.json` `last_push` field with actual SHA + CI run number.
2. Add `push_54_completed` line to `HS_ADMIN.json` with the SHA + CI run.
3. Update `PUSHES_INDEX.md` push #54 section header line with SHA + CI run.

---

## Speaker-binder note

Peter is preparing two printed copies of conference materials. **For the print binder, only `GLOSSARY.md` v3.0 needs to be included** — `NOTATION_AND_TERMINOLOGY.md` is now a redirect stub and contains no unique content. The merged glossary can be rendered to PDF separately if desired (offer standing).

---

*The instrument reads.   The expert decides.   The hashes carry the receipts.   The vocabulary holds the line.*
*Single source. No drift. One file holds the vocabulary line.*
