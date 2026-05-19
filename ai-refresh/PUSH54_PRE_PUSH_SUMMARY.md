# PUSH #54 — Pre-Push Summary (HOLD)

**Date prepared:** 2026-05-19
**Status:** HOLD-TO-PUSH (awaiting Peter's commit via GitHub Desktop)
**Primary deliverable:** Glossary merge — `GLOSSARY.md` v2.0 + `NOTATION_AND_TERMINOLOGY.md` v2.0 **combined into a single authoritative reference** at `GLOSSARY.md` v3.0; `NOTATION_AND_TERMINOLOGY.md` reduced to a redirect stub.

This push also **catches up admin records for pushes #52 and #53**, which landed (SHAs `98ea1dd6` CI #49, `bfb1c41` CI #50) but were not fully recorded in `HS_ADMIN.json` / `HS_FAST_REFRESH.json` / `PUSHES_INDEX.md`. Push #54 carries the admin sync forward.

---

## What changed

### Primary content change

- **`HCI-CNT/handbook/GLOSSARY.md`** → v3.0 (comprehensive merged reference, ~220 entries across 30 sections)
- **`HCI-CNT/handbook/NOTATION_AND_TERMINOLOGY.md`** → v3.0 redirect stub (81 lines, points to merged GLOSSARY)

### Why merge

The two reference documents had reached ~80 % overlap by v2.0. The split was a bootstrap artefact (a readable narrative file plus a locked terms file) that created a maintenance hazard: a term updated in one file but not the other became a silent drift bug.

Peter's directive (2026-05-19, in chat): *"combine the glossary with the terms and make the glossary and terms complete, include simple and obscure references such as PCA and EITT, all huf and coda terms, make it comprehensive."*

The merge fixes the split by making one file authoritative. Old `NOTATION_AND_TERMINOLOGY.md` v2.0 content was reviewed entry-by-entry against `GLOSSARY.md` v2.0. Where the two disagreed, the more precise / more recent definition was kept. Where one file had an entry the other did not, that entry was added to the merged v3.0.

### Net new content in v3.0 (~50 entries)

- **§1 Foundational mathematics** — PCA, SVD, eigenvalue, eigenvector, Spectral Theorem (previously referenced everywhere; now standalone entries)
- **§2 Statistical concepts** — Lyapunov exponent, Feigenbaum constant, CHSH, Tsirelson bound
- **§21 MC-1 through MC-4 hierarchy** — previously only MC-4 was documented; MC-1, MC-2, MC-3 now defined
- **§25 Instrument-family and lineage names** — RWA, BTL, HUF, Hs, V_Core, DADC, HCI-AUDIO, HCI-ULTRASOUND
- **§28 Abbreviations A–Z** — comprehensive index including PCA, SVD, EITT, CHSH, MC, ILR, CLR, CNT, CNQ, HUF, BTL, RWA, MORB, OIB, ...

### Lockdown compliance (S2 doc-only)

Engine code, schemas, INV catalog dispositions, NO-CREATE files, `papers/codawork2026/talk/`, and `CODA-Association/CODAwork2026/data_outputs/` are all untouched.

---

## Files in this push

```
HCI-CNT/handbook/GLOSSARY.md                     (v2.0 → v3.0, ~660 lines)
HCI-CNT/handbook/NOTATION_AND_TERMINOLOGY.md     (v2.0 → v3.0 redirect stub, 81 lines)
ai-refresh/HS_ADMIN.json                         (session_log update + push #52/53/54 entries)
ai-refresh/HS_FAST_REFRESH.json                  (last_push → #54 prepared)
ai-refresh/PUSHES_INDEX.md                       (append #52, #53, #54)
ai-refresh/PUSH54_PRE_PUSH_SUMMARY.md            (this file)
ai-refresh/PUSH54_READY_FOR_COMMIT.md            (release card, written after HOLD clear)
```

---

## Admin catch-up: pushes #52 + #53 history

**Push #52** (SHA `98ea1dd6`, CI #49) — 2026-05-17 — *Conference-ready milestone publish for CoDaWork 2026 attendees.* Bundle included: final-talk deck `CodaWork2026_FinalTalk_2026-05-17.pptx` (18 → 22 slides on 2026-05-19), 66-slide cinema scroll `CodaWork2026_PremierDataOutput_2026-05-13.pptx`, interactive projector v2.0 `codawork2026_projector.html` (RADAR / BARY / ALIGN modes + SHOCK overlay), engine v3.2.0 with `compute_navigation_2d()` block, ILR-Helmert PCA barycenter coordinates, Studies/Energy_HiddenDirections community deck, papers/codawork2026/manuscript Nature-structure draft + Fig 1-6 + Supplementary, CONFERENCE_ATTENDEES.md slide-by-slide follow-along, AI_REFRESH_2026-05-19_conference_ready.md.

**Push #53** (SHA `bfb1c41`, CI #50) — 2026-05-19 — *README polish chain.* Removed restore-point callouts from root + CODA-Association + data_outputs READMEs. Polished CONFERENCE_ATTENDEES.md as the audience-facing entry point. Updated data_outputs/README.md to reflect the 22-slide deck (per-country navigation slides split 12 / 13 / 14, one country per slide) and the projector v2.0 three-mode standard.

**Push #54** (HOLD) — 2026-05-19 — *Glossary merge.* Two parallel reference docs combined into one authoritative file. Plus admin catch-up for #52 + #53.

---

## Verification

- `GLOSSARY.md` v3.0 written via Write tool — Write returned success.
- `NOTATION_AND_TERMINOLOGY.md` redirect stub written via Write tool — Write returned success.
- Cross-mount sync confirmed via bash `wc -l`: 661 lines + 81 lines.
- Header of merged GLOSSARY declares v3.0; companion redirect line points correctly.
- Header of NOTATION stub declares v3.0 (redirect stub); body lists the 30-section coverage of the merged GLOSSARY.

---

## Speaker-binder impact

Peter is preparing two printed copies of conference materials. The merged GLOSSARY v3.0 supersedes any printed copy of NOTATION_AND_TERMINOLOGY v2.0 — for the print binder, only `GLOSSARY.md` v3.0 needs to be included (rendered to PDF separately if desired).

---

## HOLD-clear sequence

When ready to commit:

1. Verify both files render correctly in GitHub preview.
2. Update `HS_ADMIN.json` push_54_completed line + session_log entry.
3. Update `HS_FAST_REFRESH.json` last_push field.
4. Append push #54 entry to `PUSHES_INDEX.md`.
5. Write `PUSH54_READY_FOR_COMMIT.md` release card.
6. Peter pushes via GitHub Desktop; sandbox records SHA + CI run number after commit lands.

---

*The split made drift possible. The merge makes drift impossible. One file holds the vocabulary line.*
