# Governance ↔ CN‑TT v4 alignment review — what to keep, modernize, retire

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. 2026‑06‑20.
**Analysis only — nothing changed.** Every proposal below is a *candidate* for Peter's gate (HAGF‑001 /
Charter Art. II DCP lifecycle); touching a breaker without that gate would violate the governance this
document reviews. Safety‑bearing breakers are **kept by default**; the burden of proof is on removal, not
retention.*

---

## The question

The 16‑breaker governance was designed (2026‑05‑12) around the **older multi‑engine pipeline** (CNT v3.x +
CNQ v2.0 as separate stages). The live engine is now **CN‑TT v4** (tile‑native, one engine). Are any steps
trimmable? Is the pipeline concept still sound? Could a governance concept more in line with CN‑TT exist?

## The short answer

**The governance concept is sound and largely engine‑agnostic — keep it.** The reason it survives the
engine change is that *most breakers govern discipline, not stages*: operator authority, claim honesty,
human primacy, the kill‑test, the last breaker. Those do not depend on whether the engine is multi‑stage
or tile‑native. **10 of the 16 are timeless and should not be touched.** A **few mechanical breakers carry
legacy‑pipeline content** that should be **modernized (re‑pointed), not removed**, and **one is genuinely
expired**. And there is **one real upgrade** CN‑TT makes newly possible.

## Breaker‑by‑breaker (the honest map)

### Layer C — doctrinal / operator (timeless — DO NOT TOUCH): breakers 7–14, 16, + Operator
LOOP‑001 (open‑loop priority), KILL‑001 (19 failure modes), SAFE‑001 P2/P4 (do‑nothing / respect‑override),
HAGF‑001 P5 (human primacy), Charter Art. II/III (governed breakpoint / right to interrupt), HCC‑R008
(human governs release), KILL‑3.3 (artificial carrier — the soft honest limit), and **Breaker 16 — the
operator.** None of these reference the engine pipeline; all govern *discipline and authority*. They are
exactly the breakers that make "safety dominant and absolute" real. **Keep, untouched.** The "16 / Breaker
16" structure is itself doctrinally load‑bearing (SAFE‑001: "the other 15 exist to make Breaker 16 less
lonely") — so the **count stays 16**; modernization re‑points content, it does not reduce the number.

### Layer B — doc/state consistency (mechanical CHK‑* checkers): breakers 1–6 — mixed
| # | rule | verdict | why |
|---|---|---|---|
| 1 | CHK‑JSON‑001 (JSON parse) | **KEEP as‑is** | fully engine‑agnostic; catches malformed admin/gov JSON |
| 4 | CHK‑INV‑001 (INV count drift) | **KEEP** | catalog discipline; engine‑agnostic (verify the live count is current) |
| 3 | CHK‑VERSION‑001 (stale version) | **MODERNIZE** | **its token list is itself stale** — it calls `cnt v3.1.0 / cnq v2.0.0` "live," but those are now the **frozen oracle** and **CN‑TT v4 is the live engine**, which it doesn't mention. Re‑point: CN‑TT v4 = current; flag pre‑v4 tokens as stale‑unless‑oracle‑marked. The concern is real and important; the list is out of date. |
| 2 | CHK‑CNQ‑001 (CNQ status drift) | **GENERALIZE + fix gap** | CNQ was a *separate engine* in the old pipeline; CN‑TT v4 absorbed it. Generalize "CNQ status" → "engine‑status drift" for the tile‑native engine, and fix the known **paraphrase gap** (already staged as DCP‑002). |
| 6 | CHK‑README‑001 (CNQ contradiction) | **GENERALIZE** | same: "CNQ‑pending vs CNQ‑shipped" → generic "engine‑status contradiction." |
| 5 | CHK‑CCTT‑001 (CCTT current‑or‑legacy) | **REVIEW** | if CCTT tooling is conference‑era and no longer live under CN‑TT v4, this may be legacy; confirm whether any live CCTT files remain before deciding keep / retire‑replace. |

### Layer A — the one genuinely expired breaker: breaker 15
**PRE_CONFERENCE_LOCKDOWN** declared a window **2026‑05‑12 → 2026‑06‑06**. **That window is past** (today is
2026‑06‑20). The specific instance is **expired**. But the *discipline* (a hard lockdown during sensitive
windows) is reusable and valuable. **Recommendation: retire the expired instance by REPLACING it with a
reusable "declared‑window lockdown" template** (armed only when a window is declared) — keeping the count
at 16 and preserving the pattern. Retiring an *expired* window is a safe trim; deleting the *pattern* is
not.

## The real upgrade CN‑TT makes possible (the "governance in line with the engine" you intuited)

When the breakers were designed, the engine had **no internal guard/diagnostic system** — so governance had
to police state from the *outside* with brittle **literal‑string document scans** (which is exactly where
the one known gap lives: CHK‑CNQ‑001's paraphrase miss). **CN‑TT v4 changed that.** It ships a structured
diagnostic code system (`engine/codes.py`, `CNTT_DIAGNOSTIC_CODES.md`): `SS‑CCC‑LLL` codes with a **`GD`
Guard** stage (input validation), an **`SK` Shock / FDIR** stage, and `ERR / WRN / CAL / DIS` levels —
including the automated **NULL flag**. **The engine now refuses bad input and self‑reports, mechanically.**

So a CN‑TT‑aligned governance concept is a clean **three‑layer** model:

- **Layer A — engine‑internal (mechanical, NEW): the front line.** The engine's own `GD` guards, `SK`
  FDIR, and `ERR/CAL` codes are now the most robust mechanical breakers — structured, not string‑matched.
  Governance should **lean on these** rather than re‑implement them as external scans.
- **Layer B — doc/state consistency (external): thinner.** Keep the engine‑agnostic checkers (JSON, INV);
  modernize the version/engine‑status ones; let the engine's codes carry what literal‑string scans did
  poorly. This is where a *real, safe* reduction in brittle surface area lives — replacing fragile scans
  with the engine's structured self‑report **fixes the gap at its root** rather than patching the regex.
- **Layer C — doctrinal / operator: untouched.** LOOP‑001 … Breaker 16. Timeless.

That is the honest version of "trim": **not fewer safety breakers — fewer brittle external string‑scanners,
because the engine now guards itself, with the doctrinal and operator breakers fully preserved.**

## Candidate DCPs (proposed; Peter's gate)

1. **DCP‑A — re‑point CHK‑VERSION‑001** to CN‑TT v4 = live, pre‑v4 = oracle/stale. *(stale content; clear win)*
2. **DCP‑B — generalize CHK‑CNQ‑001 + CHK‑README‑001** from CNQ‑specific to engine‑status, and land the
   already‑staged paraphrase‑gap fix (DCP‑002). *(closes the one known gap)*
3. **DCP‑C — retire‑and‑replace breaker 15** (expired lockdown) with a reusable declared‑window template;
   count stays 16. *(safe — window is over)*
4. **DCP‑D — review CHK‑CCTT‑001** for liveness; keep, generalize, or retire‑replace per finding.
5. **DCP‑E — integration map: bind Layer‑B checkers to the CN‑TT `codes.py` system** so governance reads
   the engine's structured self‑report instead of scanning prose. *(the structural modernization)*

**Not proposed for change:** every Layer‑C doctrinal/operator breaker, and the 16‑count itself.

## Verification (how any change earns its place)

Any accepted DCP must (a) be implemented as a candidate, (b) **re‑run `huf-gov/tools/breaker_test_runner.py`
and show the modernized breaker still TRIPs** (and the gap closes), (c) pass through the DCP gates
(proposed → implemented → verified → released) under Peter's authorization. The breaker‑test methodology
itself — *a set with no gap is suspicious; finding one is the sanity check* — is how a trim proves it
didn't quietly remove protection.

## Verdict

The pipeline (governance) concept is **sound and worth keeping** — it survived the engine change because it
governs discipline, not stages. **No safety breaker should be trimmed.** The legitimate modernizations are:
re‑point the stale version checker, generalize the two CNQ‑era checkers (closing the known gap), retire the
one expired window into a reusable template, and — the real upgrade — **let CN‑TT v4's own guard/FDIR/code
system carry the mechanical front line**, shrinking the brittle external‑scan surface without touching a
single doctrinal or operator breaker. Power admitted only behind governance; the modernization makes the
governance *match the engine*, not loosen it.

*Analysis only. Nothing executed. Peter is the sole gate; the doctrinal breakers and Breaker 16 are not on
the table. Cross‑refs: `BREAKER_INVENTORY.md`, `papers/HUF_GOV_BREAKER_TEST_2026-05-12.md`,
`../HCI-CNTT/CNTT_DIAGNOSTIC_CODES.md`.*
