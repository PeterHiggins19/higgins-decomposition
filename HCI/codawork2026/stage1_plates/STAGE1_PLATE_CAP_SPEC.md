# Stage 1 Plate-Cap Specification (proposed)

**Version:** 0.2 — bench-test verified, ready for implementation
**Date:** 2026-05-05
**Author:** Peter Higgins
**Status:** EITT gate verified on Ball/Region (Δ = 0.501% at M=261, gate 5%, 10× margin). Spec is buildable.

## 1 — Problem Statement

The Stage 1 CBS plate generator (`stage1_plates_raw.py`) currently emits one
figure per time step plus one System Course Plot. For Japan EMBER (N=26)
this produces 27 pages — manageable. For Ball/Region (N=95) it produces 96
pages — large but still usable. For raw Ball/Region (N=26,266) it would
produce 26,267 pages — unusable as a cine-deck and unwritable as a single PDF.

The Stage 1 cine-deck is a primary CoDaWork conference output. It must
remain **field-deployable**, **predictable in length**, and
**information-complete relative to the data integrity law**.

## 2 — Design Rule

A hard plate-count cap of **101 plates** for the section cine-deck plus
**1 plate** for the System Course Plot.

```
N <=  101  →  1 plate per record (existing behaviour)
N >   101  →  101 plates, M = ceil(N / 101) records per plate, EITT
              geometric-mean (Aitchison) block decimation
```

Plate count, including the System Course Plot, is therefore bounded:
`min(N, 101) + 1` pages.

The number 101 is fixed. It is axis-symmetric (50 + 1 + 50), reads as a
percentage axis, fits a typical conference handout, and falls below the
PDF-rendering performance threshold for Acrobat continuous-scroll. It
shall not be parameterised.

## 3 — Compression Method

### 3.1 — Default and only compression

**EITT geometric-mean (Aitchison) block decimation.**

For block `b` of `M` consecutive records `{x(t_1), ..., x(t_M)}` where
each `x(t_k)` is a closed composition on the D-simplex:

```
x_block_b = AitchisonBary(x(t_1), ..., x(t_M))
          = closure( geometric_mean of {x(t_1), ..., x(t_M)} )
          = closure( exp( mean( ln(x_j(t_k)) ) ) for j = 1..D )
```

This is identical to the operation used in `bin_by_region.py`,
`bin_stracke_OIB.py`, and the EITT decimation operator already documented
in HUF_FAST_REFRESH.json.

### 3.2 — Why not other choices

* **Arithmetic mean per carrier**: destroys Aitchison-geometric structure;
  is the operation EITT proves is wrong (entropy variation 14–22% at
  modest compression).
* **Median per carrier**: not closure-preserving, loses subcompositional
  coherence.
* **Random subsample of 101**: discards 99.6% of the data, fails the
  Data Integrity Law (every nibble preserved).
* **t1→t2 tensor delta** (the alternative Peter raised): deferred to a
  parallel Stage 1-Δ deck (see §9).

### 3.3 — EITT bench-test gate

**Empirical verification (2026-05-05).** Bench-test on Ball/Region
(N=25,449 oxide-complete) at M=261 gives:

```
  Ordering             Δ at M=261     Δ at M=512
  CSV-as-given         0.501 %        0.646 %
  Aitchison-distance   0.949 %        1.033 %
```

The 5% gate passes with ~10× margin in both orderings. Counter-intuitively,
the natural data ordering outperforms a principled Aitchison-distance
sort (geological clustering preserves more entropy than compositional
clustering — see `eitt_benchtest_ball.json` for full M-sweep). The spec's
§7 record-order convention is therefore correct: do not re-order.

Before any plate is emitted with M > 8, the engine shall compute the
EITT residual at the actual M:

```
H_full         = Shannon entropy of the full N-record CLR mean
H_decimated    = Shannon entropy of the 101-block CLR means
variation_pct  = abs(H_decimated - H_full) / H_full * 100
```

Pass condition: `variation_pct < 5.0`.

If the dataset fails this gate at the chosen M, the engine emits a single
diagnostic page in place of the cine-deck:

```
EITT BENCH-TEST FAILED
M = {M},  variation = {pct}% (>= 5%)
Cine-deck not generated.
Use full-resolution (--no-cap) or finer binning.
```

Failure should be loud, not silent. The instrument refuses to publish a
misleading summary; the expert decides whether to override.

## 4 — Plate Display — Layout v1.1

The existing layout-v1.0 grid (Info | Legend | XZ | XY-spans-2 | YZ)
remains. Three additions are made in the Info panel header strip:

```
+--------------------------------------------------+
| HCI Stage 1 | FIXED SCALE | M = {M} : 1          |  ← line 1
| Block {b} of 101    samples {t_lo} - {t_hi}      |  ← line 2
| EITT residual: {pct}% PASS                       |  ← line 3
| Y -> x = Y/T -> EITT(M={M}) -> h = CLR -> sect.  |  ← scale provenance
| Unit: HLR (Higgins Log-Ratio Level)              |
+--------------------------------------------------+
```

When `M = 1` (small-N case, no decimation) lines 1–3 collapse to:

```
HCI Stage 1 | FIXED SCALE | M = 1 : 1
Sample t = {t}
```

i.e. the existing display is preserved exactly when no compression occurs.

### 4.1 — Block-extrema sidebar

The Info panel gains a new fixed sub-section displaying block diagnostics:

```
BLOCK DIAGNOSTICS
n_in_block       : {M}
max d_A in block : {dA_max} HLR  (helmsman: {h_max})
min d_A in block : {dA_min} HLR  (helmsman: {h_min})
helmsman shifts  : {n_shifts}
lock events      : {n_lock_events}
```

This is the answer to the smoothing concern in the Data Integrity Law:
the plate's polygon is the barycenter, but the operator can immediately
read whether the block is compositionally tight (extrema close to bary)
or compositionally wide (extrema far from bary, drill required).

### 4.2 — Lock-event marker passthrough

Within any block, samples flagged as DEGEN, LOCK-ACQ, or LOCK-LOSS in
`stage1_output.json` shall plot their markers (DEGEN diamond, green
dashed ring, amber dashed ring) on the plate at their proportional
position within the block, *in addition to* the block-barycenter polygon.
The polygon is the summary; the markers are the anomaly preserved.

This matches the Manifold Projector lock-marker convention already in
the repo (HS_MACHINE_MANIFEST.json `visualization_standard.boundary_markers`).

## 5 — Course Plot

Unchanged. The System Course Plot operates on the **full N records**, not
the 101 decimated barycenters. It is a single PCA whole-run page with no
scaling problem, and decimating the trajectory before PCA would distort
the path-length, displacement, and dynamic-range metrics in the info
panel.

The course plot's info panel should declare:

```
N (full)      : {N_raw}
N (cine-deck) : 101 (M = {M})
```

so the reader knows the course plot is the truth and the cine-deck is
the M-summary view.

## 6 — Lock-Event Handling Decision

(Decided 2026-05-05 via AskUserQuestion: option *Strict 101 cap, lock
events as in-block markers*.)

* The cap is hard. Always exactly 101 plates.
* Lock events appear on whichever plate covers their block.
* Block boundaries are *not* aligned to lock events — they are uniform
  blocks of M = ⌈N/101⌉ samples.
* Rationale: predictable PDF length, simplest semantics, matches the
  Manifold Projector convention.

## 7 — Block Boundary Convention

For N records with M = ⌈N/101⌉ records per block:

```
block 0 :  records [   0,   M )
block 1 :  records [   M,  2M )
...
block 100: records [100M, N )    ← may be smaller if N % 101 != 0
```

The last block has size `N - 100M`, which can be less than M. The plate
header always reports the actual sample range and actual block size.
This is preferred over irregular sizing in the middle of the deck.

## 8 — File Changes Required

### 8.1 — `stage1_engine.py`

Add a `decimate_blocks(records, n_target=101)` function that:
* Takes the full record list (each record being a closed composition + metadata)
* Returns a new record list of length min(N, 101)
* Each new record carries:
  - `composition` = Aitchison barycenter of block
  - `block_index`, `block_size`, `t_lo`, `t_hi`
  - `dA_max_in_block`, `dA_min_in_block`, `helmsman_max`, `helmsman_min`, `n_helmsman_shifts`
  - `lock_events_in_block` (list of original-index + type)
* Computes EITT residual at block M and returns it alongside

Output JSON gains a `cine_deck` section with the decimated records and
EITT diagnostics, separate from the existing full-resolution `records`
section. The full data is preserved.

### 8.2 — `stage1_plates_raw.py`

* `load_json` reads the new `cine_deck` section if present, else falls back
  to `records` (low-N case).
* `render_plate` adds the three header lines (compression / block range /
  EITT pass) and the block-extrema sidebar.
* `render_plate` plots lock-event markers from `lock_events_in_block` in
  addition to the polygon.
* The course-plot generator continues to read full `records`.

### 8.3 — README and HCI_USER_GUIDE.md updates

* Document the cap rule and the EITT residual gate.
* Update the layout diagram to layout-v1.1.
* Note that the page count is now bounded.

### 8.4 — No changes required

* `stage1_engine.py` core compositional engine (CLR, bearings, etc.) —
  operates on the full record list as before; decimation is post-engine.
* Manifold Projector — already handles arbitrary T with its own slider.
* Stage 2 / Stage 3 — operate on the same full record list, unaffected.

## 9 — Stage 1-Δ Deferred

(Decided 2026-05-05: defer to follow-up update.)

A parallel transient-display deck (per-plate t1→t2 tensor deltas — bearing
rotation, angular velocity, helmsman shift, per-carrier CLR delta) shall
be specified in a separate document and built after this state-display
version is locked, tested, and pushed. Both decks shall share the same
block partition so plates are page-aligned.

## 10 — Acceptance Criteria

This implementation is acceptable when:

1. **Japan EMBER (N=26) cine-deck is bit-identical** to the current output.
   No regression on the canonical small-N case.
2. **Ball/Region (N=26,266) cine-deck produces exactly 102 pages** (101
   section plates + 1 course plot), each plate displays M = 261, block
   range, EITT residual, and block-extrema sidebar.
3. **EITT bench-test passes** at M = 261 on Ball/Region with variation
   pct < 5%. (Pre-condition; if it fails, the cap is violated by the
   data and the spec must be revisited.)
4. **Lock-event markers ride through** decimation. Tested by injecting
   a synthetic DEGEN at sample 13,000 in a known dataset and verifying
   the corresponding plate displays the diamond marker.
5. **Course plot** continues to operate on full N and reports both
   N_raw and the cine-deck M in its info panel.
6. **Failure mode**: when EITT fails the bench-test, the engine emits
   the failure-page and returns a non-zero exit code. The cine-deck PDF
   is not produced.

## 11 — Open Questions

* Should the System Course Plot also display a 101-marker overlay showing
  the block boundaries on the PCA path, so the reader can see which
  segment of the global course each cine-plate represents?
* The block-extrema sidebar adds five lines to the Info panel. Does that
  push existing text below the 18pt body-text minimum? May require a
  small layout adjustment (move sidebar to its own gridspec cell).

**Resolved 2026-05-05:** The 5% EITT gate is the canonical Math Handbook
value and bench-test on Ball/Region passes with 10× margin (Δ = 0.501%).
No tightening warranted.

## 12 — Estimated Implementation Effort

* `stage1_engine.py` decimate function + EITT bench-test: ~150 lines
* `stage1_plates_raw.py` header strip + sidebar + lock markers: ~80 lines
* Tests + acceptance battery: ~100 lines
* Documentation updates: ~50 lines
* Total: ~380 lines, one push, single-day effort with bench-test on
  Ball/Region as the live validation case

---

*The instrument reads. The expert decides. The loop stays open.*
