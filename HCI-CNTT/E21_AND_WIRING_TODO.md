# E‑21 + guard‑code wiring — exactly what's left, and the steps

*The two items that touch the hashed run path, and therefore wait on your CI oracle‑parity re‑test. Everything here is small, additive, and conditional (hash‑neutral on clean data by construction) — but it must be **verified**, not assumed, because the hashed path is the one place a subtle change breaks the determinism guarantee. Author: Peter Higgins; AI‑assisted per HUF‑STD‑001. Honest‑broker; Peter is the commit gate.*

---

## Status — what's already done vs what's left

**E‑21 (carrier guard): already wired** in `run_cntt.py` (lines 18–44 + 66–67) — `carrier_health` triage, structural‑zero drop, multiplicative zero‑treatment, and the conditional attach `if carrier_guard is not None`. On clean data nothing is excluded → `carrier_guard = None` → not attached → identical payload → identical hash. **Left:** run the parity check + commit.

**New guard codes (`HM‑NUL`/`HM‑TIE`/`DG‑RNK`): NOT wired.** `run_cntt` never calls `helmsman_guard` / `structural_guards`. **Left:** add the conditional block below, parity‑check, commit. (The **hold‑lock `L4‑HLD`** stays *opt‑in*, NOT per‑receipt — it would change every moving dataset's hash; keep it a separate run‑series call, off by default.)

## The edit (copy‑paste, mirrors the proven carrier_guard pattern)

**1 — add the imports** (line 10, after the existing engine imports):
```python
import helmsman_guard as hg, structural_guards as sg
```

**2 — insert the conditional resolvability block** immediately *before* the hash line (before line 68, `payload["diagnostics"]["cntt_content_sha256"] = ...`):
```python
    # --- additive resolvability guards: attach ONLY when a code fires (hash-neutral on clean data) ---
    _res = hg.helmsman_guard(comp, carriers)          # HM-NUL-WRN at rest / HM-TIE-WRN on a tie / None
    _rnk = sg.effective_rank(comp)                    # DG-RNK-WRN if motion collapses to a subspace / None
    _codes = [c for c in (_res["code"], _rnk["code"]) if c]
    if _codes:                                         # clean oracle data -> no code -> block absent -> identical hash
        payload["diagnostics"]["resolvability"] = {
            "codes": _codes,
            "helmsman_resolvable": _res["helmsman"], "margin": _res["margin"],
            "effective_rank": _rnk["effective_rank"], "max_rank": _rnk["max_rank"],
            "coherent_helmsman": sg.coherent_helmsman(comp, carriers)["helmsman"]}
```

That is the whole change. It attaches the `resolvability` block **only** when a guard actually fires — which does not happen on the clean Backblaze/CNT reference data (clear motion, full rank, no tie), so the oracle hashes are unchanged.

## The steps (run where the engine imports cleanly — your machine, not the torn sandbox)

1. **Baseline** the current committed `main`:
   `python HCI-CNTT/verify_hash_parity.py --save baseline_hashes.json`
2. **Apply** the edit above to `run_cntt.py`.
3. **Re‑check**:
   `python HCI-CNTT/verify_hash_parity.py --check baseline_hashes.json`
   - **ALL MATCH** → parity holds. The guards never fired on clean data; the hash is unchanged. **Safe to commit.**
   - **MISMATCH** → a guard fired on clean data (a bug) → the attach isn't conditional enough, or an import changed float behavior. Fix before commit; do **not** push a hash change to the oracle.
4. **CI**: push triggers the "Validate Repository" workflow, which re‑runs the corpus and re‑checks the determinism/parity gate. Green = done.
5. **Commit** E‑21 + the wiring together (they're both conditional/hash‑neutral) with the determinism gate green.

## Why this is the only gate

The frozen oracle (CNT v3.2.0 + the Backblaze 731×4 parity) is the validation baseline — every `run_cntt` change must reproduce its hashes bit‑for‑bit or the "same input → same output → same receipt" guarantee is broken. Because both attachments are **conditional on a guard firing**, and no guard fires on the clean oracle data, the proof is mechanical — but the CI re‑run is what turns "should be identical" into "is identical," which is the whole point of the gate. Everything else this session stayed **observe‑only** specifically so it would never need this test.

*Optional: I can apply the edit above to the working tree now so it's staged for your CI — or leave it as this snippet for you to apply at the same time you run the parity check. Your call; I won't touch the hashed path without your say.*
