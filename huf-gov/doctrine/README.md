# Operating doctrine — pointer (canonical lives in the HUF repo)

*This stub keeps cross‑repo references valid (lose nothing; keep both repos coherent). The Hˢ instrument relies on the framework's operating doctrine, but the **canonical doctrine is governed in the HUF repo** (the governance home), not duplicated here. This avoids two copies drifting out of sync. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001.*

---

## The four doctrines (summary; canonical text in HUF)

1. **Open‑Loop / Skydiver** — the instrument reads; it never decides, acts, or recommends. The expert decides; the loop stays open.
2. **Safe Operations** — perceive before acting; *sometimes do nothing*; always have a **hold‑and‑report** safe state. A null is a finding, not a failure.
3. **Kill‑Test** — the boundary where the instrument is **inapplicable** is documented with the rigour of the successes (non‑proportional data, degenerate carriers/E‑21, broken closure).
4. **Composition Monitoring (MC‑4)** — composition is the missing fourth monitoring category; ignoring it is *ratio blindness*.

## Canonical source

`Higgins-Unity-Framework` repo → `huf-gov/doctrine/HUF_GOV_OPERATING_DOCTRINE_2026-06.md` + `DOCTRINE_INDEX.json`, cross‑walked to NASA‑style governance in `huf-gov/NASA_STYLE_GOVERNANCE.md`.

## Where Hˢ uses it

- The **FDIR / Safe‑Operations** mapping in the triple‑channel redundancy reader (`experiments/clifford_tiling_redundancy_2026-06/`) — the halt‑and‑report verdict (`RC‑HLT‑ERR`) *is* the Safe‑Operations safe state.
- The **diagnostic code system** (`HCI-CNTT/engine/codes.py`) — the automated NULL flag and the E‑21 carrier‑guard codes implement the doctrine in code.
- The **Double‑Verify & Staged‑Recovery Protocol** (`ai-refresh/VERIFICATION_PROTOCOL.json`, DVR‑1.0) — the operating discipline that grew from the same governance.

*On any conflict about current state, `HS_FAST_REFRESH.json` wins. The instrument reads; the expert decides; the loop stays open.*
