# Push #52 — Ready for commit

**Date:** 2026-05-19
**Status:** ✅ READY-TO-COMMIT (HOLD released)
**Headline:** 🏁 Point-of-restore — CoDaWork 2026 conference-ready · publish for attendees
**Pre-flight card:** [`PUSH52_PRE_PUSH_SUMMARY.md`](PUSH52_PRE_PUSH_SUMMARY.md)
**Doctrine class:** S2 (engine source change only; conference artefacts unchanged in substance)

---

## Peter — what you run

### 1. Final sanity check

From the repository root:

```bash
# Confirm working tree
git status

# Confirm you're on the conference branch (or main, per your push policy)
git branch --show-current

# Confirm the new files exist
ls -la CODA-Association/POINT_OF_RESTORE_2026-05-19.md
ls -la CODA-Association/CONFERENCE_ATTENDEES.md
ls -la CODA-Association/CODAwork2026/Compositional_Monitoring_2026.pdf
ls -la ai-refresh/AI_REFRESH_2026-05-19_conference_ready.md
ls -la ai-refresh/PUSH52_PRE_PUSH_SUMMARY.md
ls -la ai-refresh/PUSH52_READY_FOR_COMMIT.md

# Confirm engine bump
grep -n "ENGINE_VERSION" HCI-CNT/engine/cnt.py | head -2
# Expected: ENGINE_VERSION: str = "3.2.0"
```

### 2. Stage everything

```bash
git add -A
git status   # review the staged set; expect ~15-20 files
```

### 3. Commit with the milestone message

```bash
git commit -m "push #52: 🏁 Point-of-restore — CoDaWork 2026 conference-ready · publish for attendees" \
  -m "" \
  -m "* Engine cnt.py v3.1.0 → v3.2.0 with new navigation_2d block (ILR-Helmert PCA" \
  -m "  barycenter trajectory). Backwards-compatible: every v3.1.0 field unchanged." \
  -m "  Conference corpus pinned to v3.1.0; not regenerated. R port queued." \
  -m "" \
  -m "* Projector v2.0: three-mode standard RADAR / BARY / ALIGN + SHOCK overlay." \
  -m "  Consumes engine v3.2.0 ILR-Helmert PCA bary_xy via sidecar regen_baryxy.py." \
  -m "  Live PROJECTION info panel shows the math. Japan 2014 now visibly registers" \
  -m "  the multi-year reorganisation." \
  -m "" \
  -m "* Manuscript v1.3 with cover page + TOC + scientific-report layout. Working" \
  -m "  copies of .docx/.pdf placed inside CODA-Association/CODAwork2026/." \
  -m "" \
  -m "* New milestone document POINT_OF_RESTORE_2026-05-19.md defines the recovery" \
  -m "  target. New CONFERENCE_ATTENDEES.md is the single-link entry page for the" \
  -m "  audience (in-room or remote)." \
  -m "" \
  -m "* README chain refreshed: root, CODA-Association, CODAwork2026, data_outputs." \
  -m "  Attendee callout prominent at the top of the root README." \
  -m "" \
  -m "* VERSION_HISTORY.md 1.6 → 1.10 (four 2026-05-19 entries)." \
  -m "  CHANGELOG.md push #52 entry. EXPERIMENTS_JOURNAL.md push #52 row." \
  -m "  AI_REFRESH_2026-05-19_conference_ready.md narrative." \
  -m "" \
  -m "Admin updates queued (HS_ADMIN, HS_FAST_REFRESH, INV-064 STAGED, cnt.R port)" \
  -m "— not blocking conference."
```

### 4. Push

```bash
git push origin HEAD
```

### 5. Post-push (recommended)

Once the push lands and CI passes:

```bash
# Record the SHA so it can be referenced from POINT_OF_RESTORE_2026-05-19.md
git log -1 --format="%H  %s"
```

Capture that SHA — it is the recovery anchor for the point-of-restore checkpoint.

### 6. Enable GitHub Pages (recommended) — so attendees can run the projector in-browser

The interactive HTML projector is the single most valuable live tool for the audience. To make it work from a URL without anyone having to download:

1. Open repository **Settings → Pages** on GitHub.
2. Source: **Deploy from a branch** · Branch: **main** (or whichever branch this push lands on) · Folder: **`/` (root)** · **Save**.
3. After a couple of minutes the projector will be live at:

   `https://peterhiggins19.github.io/higgins-decomposition/CODA-Association/CODAwork2026/data_outputs/codawork2026_projector.html`

4. If you want, add a redirect or short URL (e.g. via a CNAME or a meta-refresh `index.html` at the repo root) so the announce-from-the-stage URL is short.

This is **optional** — the attendee landing page already documents the local-download path, which works for everyone.

### 7. Announce from the stage (optional)

A short URL or QR code on slide 19 (the Q&A bridge slide) is the most efficient way to broadcast the entry point. Two equivalent short paths:

- **The repo:** `github.com/PeterHiggins19/higgins-decomposition`
- **The attendee page (direct):** `github.com/PeterHiggins19/higgins-decomposition/blob/main/CODA-Association/CONFERENCE_ATTENDEES.md`

Either lands the audience on the same place.

## What lands on GitHub immediately after push

Anyone who visits the repository will see:

1. **At the top of the root README** — a prominent "🎤 CoDaWork 2026 attendees — start here" callout linking to `CODA-Association/CONFERENCE_ATTENDEES.md`.
2. **The attendee page** with direct GitHub-web-view links to every PDF, the HTML projector, the engine source, and reproduction commands.
3. **The point-of-restore document** describing the conference-ready state.
4. **The manuscript** (`Compositional_Monitoring_2026.pdf`) — GitHub will render it inline.
5. **The talk deck PDF** — GitHub will render it inline.
6. **The cinema scroll PDF** (325 pages) — GitHub will render it inline.
7. **The HTML projector** — viewable as raw text, downloadable in one click for local run.
8. **Per-country JSON files** — viewable as raw text, downloadable.
9. **The engine source** (`cnt.py` v3.2.0, `cnt.R` v3.1.0).

## What attendees will see in the talk

Slide 19 of the FinalTalk (Q&A bridge): the projector opens in a browser on the speaker's laptop. The PROJECTION info panel labels the active mode (RADAR / BARY / ALIGN), the engine version (v3.1.0 corpus + v3.2.0 `bary_xy`), and the math being applied. As the speaker takes questions, anyone in the room can pull up the same projector on their phone or laptop in seconds.

## Doctrine + lockdown compatibility

- **Conference corpus output is unchanged.** Every per-country JSON in `CODA-Association/CODAwork2026/data_outputs/per_country_json/cnt_v3/` has the same content hash as before push #52.
- **Talk deck content is unchanged in substance.** The 20→22 slide expansion landed earlier (push #51-aligned) and is reflected in this commit's working tree.
- **Manuscript content is unchanged in substance.** v1.3 adds front matter (cover + TOC) and fixes overflow; no claim or number changes.
- **Engine source bump (v3.1.0 → v3.2.0)** is the only S2 source change. It is additive — every v3.1.0 field in `cnt_run()` output is bit-identical; the new `navigation_2d` block is a superset.
- **No NO-CREATE file changes.** No INV catalog disposition changes (INV-064 is queued for next admin sync, not landed).
- **Pre-conference lockdown holds** through 2026-06-06. This push is doctrine-compliant within that window.

## Recovery anchor

This commit's SHA + the hashes in every output JSON together form the point-of-restore. If anything destabilises between 2026-05-19 and the conference, the recovery target is the state captured in this push.

---

*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*

*Pre-flight complete. HOLD released. Push when ready.*
