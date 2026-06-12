# Operations Index — run it, govern it, expand it (2026‑06‑11)

*One condensed map of the **current** operational surface of the Hs repo, so an operator or a new collaborator can run, govern, and extend the system without reading the whole tree. This is a **navigation layer added additively** — nothing was moved or rewritten to make it (the dated push/session history stays exactly where it is; it is the audit trail). On any conflict, `HS_FAST_REFRESH.json` wins. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001.*

---

## 1 · Start here (onboarding, in order)

1. `HS_FAST_REFRESH.json` — **the single source of truth** (live state, names, numbers, pointers).
2. `HS_GUIDE.md` — the one‑file "what / why / how" comprehension guide.
3. `ai-refresh/AI_RAPID_LEARN.md` — deep AI onboarding.
4. The local `AI_ASSIST.json` in whatever folder you land in — bring‑your‑own‑AI node (schema `hs_ai_assist/1.1`); 30 nodes seeded across the repo, each linking back up the chain.

## 2 · Run it (one engine, one path)

| Do | Command |
|---|---|
| Run a composition CSV | `python HCI-CNTT/run_cntt.py <csv> -o out.json` |
| Human diagnostics + code report | `python tools/cntt_report.py <csv>` *(the current general tool; E‑21 carrier‑guard aware)* |
| Self‑test (BIST) | `python HCI-CNTT/engine/self_test/run_self_test.py` → `VERDICT: PASS` |
| Read the codes | `HCI-CNTT/engine/codes.py` — `SS‑CCC‑LLL` (incl. the NULL flag + E‑21 carrier‑guard codes) |

**Current engine:** CN‑TT v4 (`HCI-CNTT/`). **Frozen oracle (archived reference, do not edit):** CNT v3.2.0 (`HCI-CNT/`) + CNQ v2.0.0 (`HCI-CNQ/`). Determinism is binding: same input → same `cntt_content_sha256`.

## 3 · Govern it

- **Doctrine (current):** `HUF/huf-gov/doctrine/HUF_GOV_OPERATING_DOCTRINE_2026-06.md` — Open‑Loop (Skydiver) · Safe‑Operations · Kill‑Test · Composition‑Monitoring (MC‑4).
- **NASA‑style governance:** `HUF/huf-gov/NASA_STYLE_GOVERNANCE.md` (honest cross‑walk; flight‑readiness Tier‑3).
- **Standards (locked):** `huf-gov/standards/` — HUF‑STD‑001/002/003.
- **Push discipline:** `PUSH_PROTOCOL.md` (classes S0–S3; the §6 admin‑chain closure check).
- **Verification / trust:** `TRUST_AND_VERIFICATION.md` · `REPRODUCIBILITY_CHECKLIST.md`.
- **Change control:** `ai-refresh/CHANGE_CONTROL_README.md`; investigation catalog `ai-refresh/INVESTIGATION_CATALOG.json`.

## 4 · The domains (where the work lives)

- `collaborations/` — geology‑wehner, microbiome, spaceflight‑glds1, codawork‑2026 (real‑data, honest nulls).
- `industrial-instruments/` — the **commercial** deterministic‑instrument line (gas/process‑fluid).
- `stewardship/` — the **public‑good** line (ISO MC‑4 standards + Ramsar wetlands), offered not sold.
- `experiments/` — parity harness, high‑D tiling, real‑data runs.
- `papers/` — manuscripts + in‑progress notes.

## 5 · Expand it (the pattern for a new pursuit)

To add a domain or instrument without disturbing the core:
1. **Adapter only.** Add a domain adapter (Order 0 of the tensor train) that closes the data to a composition; the engine, schemas, and INV catalog stay untouched (additive discipline).
2. **A folder + a node.** Create the domain folder and drop an `AI_ASSIST.json` (`hs_ai_assist/1.1`) so a roaming AI can onboard; link it into `collaborations/` or a top‑level pursuit beside `industrial-instruments/` and `stewardship/`.
3. **Run + receipt.** Run via `run_cntt.py` / `cntt_report.py`; commit the outputs/figures/writeup (not raw data — instrument‑not‑data).
4. **Tier every claim** (1 verified / 2 standard / 3 to‑earn); report nulls straight.
5. **Push** via `PUSH_PROTOCOL.md` (pick the class; file a `PUSH##_READY_FOR_COMMIT.md`; run the §6 sync).

## 6 · Where history lives (do not rewrite — it's the audit trail)

These are **intentionally preserved** point‑in‑time records; condensing the operational surface does **not** mean editing them (that would break path references and falsify the trail):
- `ai-refresh/PUSH##_READY_FOR_COMMIT.md` / `PUSH##_PRE_PUSH_SUMMARY.md` — per‑push prep (≈53 docs).
- `ai-refresh/AI_REFRESH_*.md` — dated session records (≈26 docs).
- `CHANGELOG.md` · `ai-refresh/PUSHES_INDEX.md` — the push ledger.
- `HS_FAST_REFRESH.md` (legacy snapshot, marked), `PRE_CONFERENCE_LOCKDOWN.md` (window May 12 → Jun 6, now closed), `archive/` subtrees, `_legacy_*` folders.

*The instrument reads. The expert decides. The hashes carry the receipts. One engine, one run path, one source of truth — and a clear path to add the next domain.*
