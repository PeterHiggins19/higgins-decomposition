# E-21 — Carrier guard + CAL code — READY FOR REVIEW (uncommitted)

*2026-06-11. Drafted by Claude Fable 5 under HUF-STD-001; human authorship for claims; **Peter is the sole commit gate — nothing committed or pushed.** Additive, live-engine-only. The frozen oracle (HCI-CNT/, HCI-CNQ/), schemas (HUF-STD-001/002/003), and the INV catalog are UNTOUCHED.*

## The bug (Tier 1, reproduced)
Real data with an **all-zero carrier** (a column with no positive value in any record) survives the loader's multiplicative zero-treatment (`pos.size == 0` → the replacement is skipped), stays `0` through `closure`, then `geo.clr` computes `log(0) → -inf → nan`. The nan propagates into the PCA/navigation block and `np.linalg.eigh` (diagnostics.py:133) raises **`LinAlgError: Eigenvalues did not converge`**. Minimal repro: a 5-carrier CSV with one all-zero column crashes `run_cntt.py`.

## The fix (additive, live engine only)
A single admissibility triage at ingestion, applied in both engine entry points, plus a calibration code so the event is machine-readable and never silent.

| File | Change |
|---|---|
| `HCI-CNTT/engine/geometry.py` | **New** pure function `carrier_health(M)` — classifies carriers into `active` / `structural_zero` (no positive value → undefined in Aitchison geometry) / `constant` (positive but flat). Classifies only; never mutates. No existing function changed. |
| `HCI-CNTT/run_cntt.py` | After building `M`, call `carrier_health`; **drop** structural-zero carriers (the established harness behaviour), **retain** constant carriers. Adds `input.carrier_guard` **only when** something is excluded/flagged. Defense-in-depth `np.isfinite(clr)` check raises a descriptive error instead of the opaque `eigh` failure if a non-finite ever survives. |
| `HCI-CNTT/engine/cntt.py` | Same guard in the `cntt_run` kernel (additive `carrier_guard`; same finiteness check). |
| `HCI-CNTT/engine/codes.py` | Emits `GD-ZRC-CAL` (structural-zero carrier excluded) and `GD-CNC-CAL` (constant carrier flagged) from `carrier_guard`; new structural mode `SM-SZC-CAL` ("confirm these are true absences, not missing data"). |

Design rule that protects parity: the `carrier_guard` block is added **only** when a degenerate carrier exists, so on well-formed data the payload — and therefore the content hash — is byte-identical to before.

## Verification (Tier 1, all green)
- **Previously-failing all-zero case** now runs to completion: drops `Dead`, keeps `navigation_2d`, emits `GD-ZRC-CAL` + mode `SM-SZC-CAL`, `carrier_guard` records `excluded_structural_zero: ["Dead"]`.
- **Clean-data hash neutrality**: same clean CSV → content hash `1a7f8c5b…4203a704` **identical** before and after the patch; no `carrier_guard` key on clean data.
- **Constant-carrier case**: `Const` carrier **retained** (D unchanged), flagged `GD-CNC-CAL`.
- **Engine self-test**: `VERDICT: PASS`; determinism hash `8734e2474a2dd8ff…` **identical** to the pre-patch run — the kernel is bit-for-bit unchanged on clean input.

## Policy choice (for Peter's review)
- **Structural-zero carrier** (no positive value anywhere) → **excluded**. It is undefined under the log-ratio map; this matches what the analysis harnesses already did manually, now centralised in the engine and recorded with a code.
- **Constant carrier** (positive, zero variance) → **retained and flagged**, not dropped. It is admissible under CLR/ILR and carries real relative information; only a calibration note is raised.
- Open question worth a sentence from you: should an excluded structural-zero carrier ever be treated as a *count* zero to be imputed (kept in the composition) rather than a *structural* absence (removed)? The current default treats all-zero columns as structural absence. The `SM-SZC-CAL` mode message asks the analyst to confirm exactly this.

## Note (separate, not patched)
`run_cntt.py`'s CSV loader does not skip `#` comment headers (surfaced when reproducing the Frielingen-9 demo through the front door). Flagged only; out of E-21 scope.

*Engine self-test receipt for this session: `2ea63ff14cd6d7dc165870d8`. The instrument reads; the expert decides; the hashes carry the receipts.*
