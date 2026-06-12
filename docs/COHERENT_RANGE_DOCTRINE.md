# Coherent Range Doctrine — Multi-Carrier Temporal Discipline

**Doctrine ID:** CRD-1.0
**Adopted:** push #33 (2026-05-10)
**Authority:** project doctrine — applies to all multi-carrier analyses across the Hs framework
**Catalog reference:** INV-047
**Source:** Peter Higgins (2026-05-10, in response to USA missing-year-2000 asymmetry surfaced during EMBER 8-country corpus run)

---

## 1. The principle

> *"The set is only valid and computed for the years present across all members. The full report can only go from the period of the smallest carrier."*
> — Peter, 2026-05-10

For any analysis that compares two or more carriers (countries, drivers, components, dimensions, members of any compositional set), the **valid analytical window is the intersection of all members' time ranges**. The shortest-coverage member sets the binding window for the entire set. There is no padding, no imputation, no silent truncation — and no headline result on a window where some members are absent.

This is the temporal analogue of closure. CoDa never reports a composition that fails to sum to the same total; CRD-1.0 never reports a multi-carrier comparison that fails to span the same window.

## 2. Why this discipline matters

**Mismatched T hides asymmetry.** When carrier A reports T=26 and carrier B reports T=25, every per-carrier diagnostic that depends on trajectory length — flips count, attractor stability, depth tower length, helmsman cumulative sigma, CHSH window-averaged S — is computed on different sample sizes. A surface-level "USA has fewer flips than CHN" comparison is meaningless if USA's window is one year shorter. The reader has no warning unless the manifest says so.

**Comparison without manifesto is rumor.** A multi-carrier table is a comparison artifact. Comparison artifacts must declare their basis — what range, what carriers, what closure — or they slide from analysis into anecdote. CRD-1.0 forces the basis into the artifact's header so the reader cannot miss it.

**Drop-and-recover preserves all questions.** If a specific year is essential to a research question, the analyst is not blocked. They drop the limiting carrier, re-run on the now-coherent enlarged range, and the manifest names the drop explicitly. Two principled views (with-USA-2001-2025, without-USA-2000-2025) replace one ambiguous view (mixed-T-asterisks-everywhere). Both are honest; neither is fudged.

**Stops a class of conference embarrassment.** A reviewer asks "why does USA's flips count look anomalously low?" and the answer "USA's window is one year shorter than the others" is fine in a footnote but reads as a hidden assumption when it lives only in a footnote. CRD-1.0 makes the matched-window the headline so the question doesn't arise in the first place.

## 3. Scope — what the doctrine governs

The doctrine applies to:

- **Every multi-carrier comparison** in the Hs framework — engines, wrappers, papers, reports, conference outputs, scheduled runs.
- **Every cross-corpus aggregation** where carriers from different sources must align on a common temporal axis.
- **Every multi-vintage analysis** of the same dataset (e.g., comparing v2.0.4 outputs against v3.0.0 outputs across the same carrier set).
- **Every composite figure** in a paper, slide deck, or instrument readout that places two or more carriers' diagnostics in the same visual frame.

The doctrine does not apply to:

- **Single-carrier reports** — each carrier's standalone analysis uses its own native range. USA's stage-1 report covers 2001-2025; CHN's covers 2000-2025; no truncation when reporting on yourself.
- **One-off diagnostic checks** that are clearly labelled as exploratory and never enter a public artifact.
- **Synthetic fixtures** with controlled time grids where temporal alignment is by construction.

When in doubt, apply the doctrine. The cost of an extra range-coherence check is negligible; the cost of a published comparison with mismatched T is reviewer doubt the project cannot afford.

## 4. The five rules

### Rule 1 — Multi-carrier intersection

For any analysis across two or more carriers:

```
T_set = min(T_member) over all members
range_set = [max(start_member), min(end_member)] over all members
```

Every member is truncated to `range_set` before any diagnostic is computed. The truncated trajectory is what enters the engine; the engine sees a coherent set, computes a coherent result.

### Rule 2 — Single-carrier native

For any analysis of one carrier in isolation, the carrier's native range is used. No truncation to match an external corpus when the artifact's purpose is the carrier itself. USA's standalone STAGE_1_REPORT.md covers USA's 25 years; the corpus comparison covers all 8 countries' shared 25 years; both are correct, neither contradicts the other.

### Rule 3 — Drop-and-recover

If a year present in some members but absent in the limiting member is critical to the research question, the analyst is permitted (and encouraged) to drop the limiting member and re-run on the enlarged coherent range. The drop must be:

- **Named** in the manifest header (`carriers_dropped: ["USA"]`)
- **Justified** in one sentence (`reason: "to recover 2000 baseline absent from USA EMBER coverage"`)
- **Reproducible** as a separate artifact, not as a footnote on the original

This produces a sibling table or report. Both versions ship; the reader compares them.

### Rule 4 — Manifest header

Every multi-carrier output declares, at the top of the artifact:

```
Coherent range: <YYYY-YYYY>
T_set: <integer>
Members: <comma-separated list of carrier IDs>
Limiting member(s): <carrier IDs that pin range_set>
Carriers dropped (if any): <list>
Range policy: <coherent|native|explicit>
```

For prose reports this is a five-line manifest table. For JSON outputs this is a `coherent_range_manifest` block. For figures this is a sub-caption line. No exceptions.

### Rule 5 — Anti-specification entry

Reporting a multi-carrier comparison with mismatched T per carrier — without an explicit manifest declaring the asymmetry — is a SEA failure mode. Each engine and wrapper anti-specification document carries an entry under category INTP or DOC for "mismatched-T multi-carrier comparison reported as headline." Mitigation evidence is the runner's `--range-policy coherent` default plus the manifest header on every output.

## 5. Range policies

The runner exposes three explicit policies. The default for any multi-carrier invocation is `coherent`.

| Policy | Meaning | When to use |
|---|---|---|
| **coherent** | Truncate every member to the intersection of all members' ranges. T_set = min(T_member). | Default for any multi-carrier comparison, conference output, paper figure, or aggregated report. |
| **native** | Each member uses its own native range. Output table will have mixed T per row. Manifest must declare `mixed_T: true`. | Per-carrier standalone reports placed side-by-side for inspection (not for headline comparison). |
| **explicit** | Caller passes `--range-start YYYY --range-end YYYY` and the runner truncates every member to that exact window, dropping carriers that don't span it. | Re-running historical artifacts on a fixed window for replication; aligning to a non-natural boundary (e.g., a regulatory reporting period). |

The runner refuses `native` for any output that is shaped as a single comparison table. `native` is reserved for explicitly per-carrier outputs.

## 6. Per-engine workflow

Engines themselves never enforce CRD — they consume whatever input they're given. The doctrine is enforced at the **runner / orchestrator** layer, before any data reaches the engine. The contract:

1. **Runner receives carrier list + range policy.**
2. **Runner computes `range_set`** from member metadata.
3. **Runner truncates each carrier's CSV** to `range_set` and writes the truncated CSVs to a working directory.
4. **Runner invokes the engine** on the truncated CSVs, one per carrier.
5. **Runner aggregates outputs** with the manifest header attached.
6. **Engine outputs are unmodified** — the engine has no knowledge of CRD; it only sees the input it was handed.

This keeps engine independence intact. CNT v3 and CNQ v2 do not change. The runner is the locus of CRD enforcement.

## 7. Per-paper workflow

For Paper 1, Paper 2, future papers, and any public claim that involves a multi-carrier table or figure:

1. **Every comparison table** carries a coherent-range manifest in its caption or in a footnote-1 immediately under the title.
2. **Every figure with multiple carriers** carries a sub-caption line declaring the coherent range.
3. **Drops are documented** in the methods section with the one-sentence justification from Rule 3.
4. **The reproduction command** in the appendix specifies `--range-policy coherent` (or the explicit window used).

The Paper 1 anti-specification gains an entry: "INTP — multi-carrier figure could be misread as native-range comparison if manifest is removed." Mitigation: figure caption lock; reviewer checklist item.

## 8. Per-wrapper workflow

Wrappers translate engine outputs to domain audiences. When a wrapper-generated report aggregates more than one carrier (e.g., the audio wrapper running across multiple drivers, or the government-budget wrapper running across multiple departments):

1. **The wrapper inherits** the runner's coherent-range manifest verbatim.
2. **The wrapper's locale-specific text** must include a translation of the manifest header (en, fr, es, ru, zh, ar — the UN-6 locales).
3. **The wrapper anti-specification** carries a WRP-category entry: "manifest header lost in translation."

## 9. Integration with existing doctrine

CRD-1.0 is additive to and compatible with:

- **SEA-1.0 (Suspicion of Every Assumption)** — CRD violations are SEA failure modes (INTP and DOC categories). The two doctrines reinforce each other.
- **STP-1.0 (Self-Test Protocol)** — BIST corpora are themselves coherent-range by construction (synthetic test matrices have known T). CRD applies to BIST aggregate reports across corpora.
- **Engine independence policy (push #32)** — CRD is enforced at the runner layer; engines remain independent and unchanged. Adding CRD does not couple CNT and CNQ.
- **The lineage doctrine** — if v2.0.4 and v3.0.0 outputs are compared, both vintages must be produced on the same coherent range. Lineage comparisons are themselves multi-vintage analyses subject to Rule 1.
- **OPERATIONS_PROTOCOL.md** — the Gawande-style transition checklist gains a CRD step: "Does this output involve multiple carriers? If yes, has the manifest header been verified?"

## 10. Edge cases

**Single member.** Trivially coherent. Manifest still emitted (T_set = T, range_set = native range, members = [single_id], no drops). The manifest is a structural invariant, not a conditional decoration.

**Two members with identical ranges.** Coherent range = either member's range. Manifest emitted normally; limiting member field lists both.

**All members disjoint (no intersection).** `range_set` is empty. The runner refuses to produce a comparison. Error message names which members fail to overlap with which others. Caller must drop members until at least one coherent range exists.

**Member with internal gap (sparse coverage).** The doctrine governs *range endpoints*, not internal density. A member covering 2000-2025 with a missing 2010 is treated as covering 2000-2025; the gap is a separate concern handled by the engine's input-validation layer (which may reject the trajectory or interpolate per its own policy). CRD does not interact with internal gaps; it only enforces window alignment.

**Member with non-uniform sampling.** Same answer: CRD governs endpoints. If carriers report at different temporal resolutions (yearly vs monthly), resampling is a pre-processing step that happens before CRD is applied. The runner resamples every carrier to a common resolution, then applies CRD on the resampled set.

**Vintage comparison (v2.0.4 vs v3.0.0).** Both vintages are members for CRD purposes. Both must have output on the same coherent range. If only the new vintage was run on the full set and the old vintage's archive is partial, the comparison range is the intersection of the available archives — and the manifest names the v2.0.4 archive as the limiting member.

## 11. Migration of existing artifacts

Artifacts produced before push #33 may carry mixed-T comparisons without manifests. The doctrine's adoption obligates a one-time sweep:

1. **Conference outputs** (`papers/codawork2026/conference_2026_06/`) — promote common-range tables to headlines, demote full-range tables to per-carrier-native appendices, attach manifests. *Done in this push.*
2. **Paper 1 and Paper 2 figures** — add manifest sub-captions where multi-carrier figures appear. Add to the Paper 1 update queue.
3. **Legacy v2.0.4 artifacts** — leave in place as historical record; future comparisons against them inherit the limiting-vintage manifest treatment from §10.

Pre-doctrine artifacts are not retroactively rejected; they are flagged in `OPERATIONS_PROTOCOL.md` as "produced under pre-CRD discipline; manifest implicit."

## 12. The principle, recapitulated

> *"Make the set only coherent. Matches of all members with the same range can be computed, and range limits exist to the smallest set."*
> — Peter, 2026-05-10

The default for a multi-carrier comparison is the intersection. The default is the headline. The native ranges live in standalone reports and in a clearly-labelled appendix. When a research question demands the longer range, a member is dropped and the reduced set re-runs on its enlarged coherent window — a separate, named, manifested artifact.

No mixed-T headlines. No silent truncation. No padding. No imputation. Every comparison declares its window in its header.

A coherent range is a small thing structurally and a large thing for credibility. The cost is negligible, the discipline is mechanical, and the reader is never left wondering whether the table they are looking at is comparing like with like.

---

**Status:** doctrine adopted push #33 (2026-05-10). Applies to all multi-carrier outputs across the Hs framework, retroactive to the conference deliverables and forward to all subsequent artifacts.

**See also:**
- `docs/SUSPICION_OF_EVERY_ASSUMPTION.md` — SEA-1.0 doctrine; CRD violations are SEA failure modes
- `docs/SELF_TEST_PROTOCOL.md` — STP-1.0 doctrine; BIST corpora are coherent-range by construction
- `papers/codawork2026/conference_2026_06/run_ember_corpus.py` — first runner with `--range-policy` flag
- `papers/codawork2026/conference_2026_06/COMPARISON_v2_0_4_vs_v3_0_0.md` — first conference output restructured under CRD
- `ai-refresh/INVESTIGATION_CATALOG.json` — INV-047 records the doctrine adoption
- `OPERATIONS_PROTOCOL.md` — integration of the CRD checklist step
