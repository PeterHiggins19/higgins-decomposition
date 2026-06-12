# Volume III — Verification, Reference and Release

**HUF-CNT System v1.1.x**
**Provenance, audit, and the public-trial dossier**

This volume is the verification handbook plus the release record.
It covers the determinism contract that anchors the system's
reproducibility claim, the hash-chain proposal aimed at the broader
CoDa community as honest-publishing infrastructure, the
30-minute talk plan for CodaWork 2026 (with the Q&A study list),
the public-trial readiness audit, and the hand-off summary that
ties the whole system into a single citable record.

Companion volumes:
* **Volume I — Theory and Mathematics**
* **Volume II — Practitioner and Operations**

---

# Part A — The determinism contract

This section formally states the reproducibility guarantee the
package makes, the mechanisms by which it is enforced, and the
known threats to it.

## The contract

For any input CSV X and any engine configuration block C, the
function F: (X, C) → JSON satisfies:

> Whenever F(X, C) and F(X', C') produce the same `content_sha256`,
> X and X' have the same closed-data SHA-256, and C and C' have
> the same active values for every documented constant.

In plain English: same inputs and same configuration produce
byte-for-byte identical content_sha256 across machines, operating
systems, and time. The contract is the foundation of the entire
package — without it, the schema, the atlas, and the experiment
catalog are all just bookkeeping.

## What "same inputs" means

The input is the **closed data**. Two CSV files producing different
closed-data SHAs are different inputs. Differences that change the
closed data include:

* Different numerical values in any cell.
* Different precision (e.g. trailing zeros that round differently
  after closure).
* Different ordering of rows when ordering is `by-time` or `by-d_A`.
* Different column ordering of carriers.
* Different zero-replacement results when zero counts differ.

Differences that do not change the closed data (and therefore do not
break the contract):

* Whitespace and line-ending differences (the engine reads CSVs
  cleanly).
* File timestamps, file metadata.
* The CSV's header text — the carrier names matter (they are
  recorded in `input.carriers`), but reordering or renaming carriers
  changes the closed data.

## What "same configuration" means

The active values of the USER CONFIGURATION block at the top of
`cnt/cnt.py`. Currently fourteen documented constants:

```
SCHEMA_VERSION         DEPTH_MAX_LEVELS
ENGINE_VERSION         DEPTH_PRECISION_TARGET
DEFAULT_DELTA          NOISE_FLOOR_OMEGA_VAR
DEGEN_THRESHOLD        TRIADIC_T_LIMIT
LOCK_CLR_THRESHOLD     TRIADIC_K_DEFAULT
                       EITT_GATE_PCT
                       EITT_M_SWEEP_BASE
```

Every active value is echoed into `metadata.engine_config` of the
output JSON. A user reproducing a published run inspects the
published `engine_config` and verifies their local config matches.
A run with a different config produces a different SHA, by design.

## Enforcement mechanisms

The contract is enforced by four mechanisms acting together.

**1. Sorted iteration.** Every place in the engine where a tie
between carriers must be broken (e.g. when two carriers have equal
contribution to the helmsman score) uses
`max(sorted(candidates, key=…))` — never bare `max(set(…))` or `max`
over a `dict`'s `.values()` view. Set and dict iteration order is
not deterministic across Python implementations and was the cause
of the original 2.0.0 → 2.0.0 non-determinism that we caught and
fixed.

**2. Explicit float formatting.** All numerical output goes through
JSON's standard float serialiser, never through `repr()` or
`str()`. Python and R float-string conversions are deterministic at
double precision; we rely on that.

**3. Adapter determinism.** Every adapter sorts its output rows
explicitly (alphabetically by region name, by year, etc.) and
processes input deterministically. Adapters that read multi-file
inputs (e.g. BackBlaze 8 quarterly zips) sort the file list before
processing.

**4. Full-corpus determinism gate.** The test
`cnt/tests/test_full_corpus.py` runs the engine against every
reference experiment and verifies the produced
`content_sha256` matches the value in `experiments/INDEX.json`. CI
(`.github/workflows/test-python.yml`) runs this on every push and
PR. A failing gate is a release blocker.

## Known threats and mitigations

The contract holds *if* the underlying floating-point arithmetic is
identical. In practice this means the threats are:

**numpy version drift.** Different numpy versions use different
underlying BLAS libraries which can produce slightly different
results in matrix operations. Mitigation: `requirements.txt` pins
numpy to a tested range (`numpy>=1.24,<3.0`). CI tests against
multiple Python versions to catch drift early.

**System libm version drift.** On rare hardware, the system math
library produces different last-bit results for transcendentals.
Mitigation: the engine avoids transcendentals where possible (uses
log/exp/sqrt only, never trigonometric or special functions in the
hot path). When `log` differs at the last bit, the error compounds
to the SHA — but this is rare on x86-64 Linux/macOS/Windows in
practice.

**matplotlib drift.** Atlas PDF SHAs differ between matplotlib
versions because matplotlib embeds a creation timestamp and version
string in the PDF metadata. This is a known and accepted divergence:
the atlas content_sha256 is *not* part of the determinism contract.
The CNT JSON content_sha256 is. The atlas catalog records both for
audit but only treats the JSON SHA as authoritative.

**R port at engine 2.0.3.** The R port mirrors the Python engine
at engine 2.0.3 with parity-of-logic for the IR taxonomy
refinement. Numerical results are identical to within IEEE floor
on tested datasets, but exact byte-for-byte SHA equality between
Python and R outputs is not guaranteed and not part of the
contract — both produce conformant schema-2.0.0 JSONs and report
the same IR class for every reference experiment, but the embedded
floating-point representations may differ. Use the Python output
as the authoritative reference.

## What breaks the contract

The following are deliberate engine changes that legitimately break
the contract and bump the engine version:

* Bug fixes in the core math (e.g. the curvature formula correction
  in 2.0.0 → 2.0.1).
* Changes to the IR classification rules (e.g. the taxonomy
  refinement in 2.0.2 → 2.0.3).
* Changes to default constants in the USER CONFIG block.
* Schema additions of new fields that are computed by the engine.

Each of these requires the engine version to be bumped, the change
log in `CHANGELOG.md` to be updated, and Mission Command's
`--update` mode to be run to commit the new SHAs to INDEX.json. The
old and new SHAs both appear in git history, making the change
auditable.

The following are non-changes that should not break the contract
and would indicate a bug if they did:

* Renaming an internal helper function.
* Reformatting the source code.
* Adding a docstring or comment.
* Refactoring the call graph without changing arithmetic.

If a non-change appears to break the SHA, the determinism
mechanisms have failed somewhere — investigate before merging.

## Reproducing a published run

The minimal reproduction is:

```bash
git clone <repo>
cd HUF-CNT-System
pip install -e .                 # or use the pinned requirements.txt
python mission_command/mission_command.py
```

Output: 20 PASS lines, "Results: 20 PASS, 0 FAIL, 0 ERR (total 20)".

If any line is not PASS:

1. Check engine version in `cnt/cnt.py` matches `experiments/INDEX.json._meta.engine`.
2. Check the failing JSON's `metadata.engine_config` matches the
   published version's config (echo into a log and diff).
3. Check `pip freeze` shows the pinned numpy / matplotlib versions.
4. If everything matches and the SHA still differs, file an issue
   with the failing experiment id, your platform, and the diff.

## The receipt

A passing run is the receipt. The combination of (PASS line printed
on screen) + (`content_sha256` in INDEX.json) + (the JSON's
`metadata.engine_config` echo) is end-to-end reproducible by any
third party with access to the same code, the same data, and the
same configuration. That is the determinism contract.

---

*The instrument reads the same way. The expert decides. The loop
stays open.*



---

# Part B — Verification value to the CoDa community


*A community paper proposing hash-chained outputs as honest-publishing infrastructure.*


### What the CNT Hash Chain Offers the Compositional Data Community

**Author:** Peter Higgins (HUF-CNT System v1.1.x)
**Date:** 2026-05-05
**Status:** preprint / community discussion paper
**Companions:** `CNT_VS_CODA_BALANCE.md`, `CNT_ROI_AND_USE_CASES.md`
**Cite as:** Higgins, P. (2026). *Verification, Integrity, and Author Protection: What the CNT Hash Chain Offers the Compositional Data Community.* HUF-CNT System v1.1.x preprint.

---

## Abstract

Compositional data analysis as a field has matured methodologically
but its publication practice has not yet caught up to the
verification standards routine in cryptography or distributed
systems. This paper argues that the HUF-CNT system's hash-chained
output, available as a side-effect of using the engine, provides
infrastructure the community can adopt to (a) let any reader verify
any published CoDa result in minutes, (b) make audit drift and selective reporting locatable rather than implicit, and (c)
protect authors from misrepresentation by giving them a
hash-anchored record of exactly what they published. The argument
is independent of any preference for CNT's analytical methods —
the verification benefit accrues even when the engine is used as a
re-implementation of classical CoDa workflows. The case is
constructed bottom-up from first principles and ends with a
two-line journal-publication standard.

---

## §1  The problem

Three trends have eroded trust in published quantitative results
across many fields, including compositional-data work:

1. **Selective parameter choice**, e.g. zero-replacement δ values
   set silently and reported only in supplementary material if at
   all. The choice can flip a borderline IR classification.
2. **Toolchain drift**, where the same data run a year later
   through an updated pipeline yields different numerics.
   Without recorded engine identity, a reviewer cannot tell
   whether a discrepancy is a mistake, a software update, or a
   misrepresentation.
3. **Post-hoc adjustment and audit gaps**, ranging from honest
   error-correction without re-running the full pipeline through
   to deliberate selective reporting. In the compositional setting
   these are particularly hard to detect because plots can be
   regenerated with the trajectory's worst points trimmed and the
   reader has no anchor to compare against.

None of these problems are unique to CoDa. They are widespread.
What makes them straightforward to address is that the inputs and operations of any
CoDa analysis are entirely deterministic — given the same data and
the same configuration, the same numerical outputs follow. That
determinism is the foundation a hash chain stands on.

---

## §2  The verification chain in CNT

Every CNT JSON output carries a chain of SHA-256 hashes covering
every link from raw input to final figure:

```
raw CSV
  │  hash:   inp.source_file_sha256
  ▼
zero-replaced + closed simplex matrix
  │  hash:   inp.closed_data_sha256
  ▼
canonical analytic JSON
  │  hash:   diagnostics.content_sha256
  ▼
engine source code
  │  hash:   metadata.engine_config.engine_signature
  ▼
PDF report
  │  fixed:  matplotlib metadata, deterministic epoch
  ▼
PDF page footer
       carries (engine version, engine_signature[:12],
                content_sha256[:12], source_file_sha256[:12], date)
```

Each link's hash is recorded inside the next link's metadata
block. To verify a published result, a reader needs only:

1. The raw CSV (or its `source_file_sha256` if they have a copy
   they can hash themselves).
2. The published JSON (or the published PDF, where the SHAs
   are printed on every page footer).
3. Any version of the CNT engine that supports the schema in
   question (schemas are versioned and additive; old JSONs read
   correctly under newer engines).

Verification is the act of running:

```
sha256sum the_data.csv               # confirm input identity
python -m cnt verify the_data.csv \
       --expected-content-sha256 <published value>
```

If the expected SHA matches, the analysis reproduces exactly. If
it doesn't, the discrepancy is by definition diagnosable:

* `metadata.engine_config` records every USER CONFIG constant
  active for the run, plus any per-call `active_overrides`. If the
  recompute used different δ, the override is visible.
* `metadata.units` records the unit lineage; if the recompute
  treated input as ratio when the original treated it as bit, the
  difference is visible.
* `metadata.engine_version` and `engine_signature` record the
  engine's identity. A mismatch is a software-version explanation,
  rather than an integrity question.

In every case the discrepancy is locatable, with the specific cause documented.

---

## §3  Why this matters: the asymmetry of provenance

Consider what would be required to publish a result that a
reader cannot reproduce.

| Action | What changes | Detection |
|---|---|---|
| Modify the raw CSV | `source_file_sha256` changes | Anyone with the original CSV catches it. |
| Modify the engine | `engine_signature` changes | Comparing against the canonical engine release catches it. |
| Modify the engine_config (e.g. different δ) | `engine_config.active_overrides` changes | The value is in the JSON; reviewers see it directly. |
| Modify the JSON post-hoc | `content_sha256` no longer matches the canonical recompute | Recomputation catches it instantly. |
| Modify the PDF | The page footer's SHAs no longer match the JSON | Eye-ball check against the JSON catches it. |
| Modify only one timestep's value in the JSON | The whole `content_sha256` changes (it's a hash over the entire JSON) | Recomputation catches it. |

To publish a result that is also unverifiable, a contributor would
have to assemble a self-consistent alternative chain: alternative CSV,
alternative JSON, alternative PDF, alternative hashes — and convince
a reviewer that the alternative chain is canonical. Selective alteration of one link breaks the chain.

Producing such an alternative chain is possible, but it is:

* **Computationally expensive** at large data sizes (regenerating
  the pipeline takes real CPU time).
* **Detectable** when the original raw CSV exists somewhere
  outside the actor's control (e.g. a public dataset).
* **Self-disclosing** — the actor must publish the false SHAs
  alongside the chosen data, which means a reviewer can verify
  *that* the SHAs are internally consistent. If they are
  consistent but the result is implausible, that is itself a flag.

The hash chain does not make alternative chains impossible. It makes them
**asymmetric**: easy for the honest researcher to demonstrate,
hard for anyone reproducing a result to do so unambiguously.

---

## §4  Author protection — provenance against accusation

The same chain that detects audit drift also protects
good-faith authors from accusations of error or selective
reporting.

When a graduate student publishes a CoDa result that produces a
striking IR class, a reviewer who finds the result implausible has
two channels of objection:

* **"This calculation may not reproduce."** Without provenance, the student has
  to defend their workflow line by line. With provenance, they
  hand the reviewer the raw CSV plus the `content_sha256`. The
  reviewer recomputes; if it matches, the calculation is settled.

* **"You changed the data."** Without provenance, the student has
  no way to prove they didn't. With provenance, the
  `source_file_sha256` is published at submission time and
  hashed into the JSON. If the data later changes, the
  recomputation produces a different SHA and the change is
  located, not insinuated.

The author can now demonstrate their work with **arithmetic**
rather than relying on social capital. This matters most for early-career
researchers, for collaborators in different time zones, and for
anyone whose institutional standing is not yet a substitute for
audit trail.

This is not just defensive. The same provenance lets honest authors
**confidently update** results when better data arrives. The
update is a new entry in the chain, not a quiet edit. The
revision history is itself a published artefact.

---

## §5  Worked example

Suppose an EMBER Japan electricity-mix analysis is published with
the headline: "Period-2 attractor amplitude A = 0.0376;
LIGHTLY_DAMPED IR class."

A reviewer wants to verify. They:

1. Download `ember_JPN_Japan_generation_TWh.csv` from EMBER's
   public release.
2. Confirm `sha256sum ember_JPN_*.csv` matches the published
   `source_file_sha256` (32 hex characters in the paper).
3. Run `python -m cnt verify input.csv` with the engine version
   stated in the paper.
4. Compare the recomputed `content_sha256` to the published
   value.

In the canonical case, all four checks pass and the headline
is verified — A = 0.0376 to floating-point precision, IR class
LIGHTLY_DAMPED — in approximately two minutes of CPU time.

If a reviewer wishes to challenge the choice of δ, the active
`engine_config_overrides` block is published in the JSON; the
reviewer can re-run with δ' = 1e-9 and observe how A changes.
That re-run produces a different `content_sha256`; the original
result is not invalidated, but the sensitivity is now public.

If a reviewer obtains the data and gets a `content_sha256` that
does not match, they know with certainty that the published
value cannot have come from the published data + the published
config + the canonical engine. The mismatch is not a slur —
it is a fact, and the discussion can proceed concretely.

---

## §6  A two-line journal standard

Journals already require data and code availability statements.
CNT's chain lets that requirement become directly verifiable:

> *Every quantitative result reported in this paper has been
> generated by HUF-CNT engine version `<X.Y.Z>` (engine_signature
> `<32 hex>`). The full hash chain is available at
> [`<DOI / Zenodo URL>`]: source CSV SHA, closed data SHA,
> engine_config overrides, and final content_sha256. Any reader
> with a copy of the raw CSV can verify the result in ~2 minutes
> using `python -m cnt verify`.*

Two paragraphs in a methods section, plus the chain itself
deposited in any data repository, raises the verification floor
for CoDa publications without changing what authors write or how
reviewers review. The infrastructure does the work.

---

## §7  Counter-arguments and responses

### "The engine itself could vary across releases."

True. That's why the engine source code is hashed
(`engine_signature` = SHA-256 of `cnt/cnt.py` and the active atlas
modules). Releases are tagged in the public repository, and the
release tag's commit SHA is the canonical engine identity. A
reader who is paranoid about a custom engine can use the canonical
release and verify against that.

### "Published SHAs only verify against the data they were
computed on. Different raw data will produce different SHAs."

Correct, and that is the point. The SHA chain proves *internal
consistency* of a published result. It does not adjudicate
whether the raw data the author chose is the right data — that
question is unchanged from current practice. What changes is
that arguments about input choice happen at the raw-data layer,
not inside the analysis.

### "Hash chains feel like cryptography theatre to a research
audience."

Hash chains are simply a structured way to ask "did the bits
change?" The cryptographic specifics matter only because the
hashing algorithm needs collision resistance. SHA-256 has it for
the foreseeable future. The user-facing experience is
`sha256sum file > expected.txt; sha256sum file2 > observed.txt;
diff` — a one-line operation any researcher can run.

### "Many CoDa workflows do not need hashes; they need clearer
methods sections."

Both are true. Clearer methods sections help. Hash chains help
*more* because they cannot be misread, misremembered, or selectively
described. A methods section is documentation; a hash chain is a
verifiable claim. The two are complementary, not competing.

### "Aren't authors who don't use CNT being unfairly disadvantaged?"

The argument here isn't that CNT must be used. It is that *if you
already plan to publish a CoDa result*, using a tool that produces
a hash chain alongside the analysis costs you nothing additional
and gains the verification benefit. CNT is one such tool;
classical pipelines that adopt similar provenance discipline
would offer the same benefit. The community benefits regardless of
which tool drives adoption.

### "Storage costs of full provenance."

A canonical CNT JSON is ~600 KB for a typical T = 26, D = 8
trajectory. For a hundred such results in a paper's supplementary
material, that's 60 MB — well within standard journal data
deposit limits. Larger datasets (T ~ 1000) reach ~50 MB per
result; that's a per-paper cost, not per-figure, and remains
modest by modern journal standards.

---

## §8  What the community gains

Concrete benefits of community-wide adoption:

1. **Faster review cycles.** A reviewer who can verify a numerical
   claim in two minutes spends those minutes on the *interpretation*
   of the result rather than its arithmetic.
2. **Earlier error detection.** Honest mistakes — incorrect δ, ordering choice, unit choice — are flagged in the verification step
   rather than rediscovered years later by a follow-up paper.
3. **Reduced retraction burden.** Cases that today require a
   contested retraction with arguments about who-did-what-when
   become a one-line verification; either the chain is consistent
   or it is not.
4. **Lowered cost of meta-analysis.** A community catalogue of
   verified results becomes feasible because verification is
   automatic. Cross-dataset comparison (the Stage 4 territory)
   becomes routine.
5. **Author protection** as discussed in §4.
6. **Infrastructure for AI-era publishing.** As more analyses are
   produced by automated pipelines (LLMs assisting code, automated
   re-runs on updated data), the question "did a human or a bot
   sign off on this result" becomes pressing. A hash chain plus a
   human signature is a two-factor record.

---

## §9  What is *not* claimed

To stay scientifically humble:

* CNT's hash chain does not validate the **scientific merit** of
  any analysis. A result can be perfectly hash-verified and still
  still be limited because the chosen dataset, the chosen
  carriers were grouped, or the conclusion overreaches the
  evidence. Verification is a floor, not a ceiling.
* The chain does not address **upstream data integrity**. If the
  raw CSV itself reflects a collection error, hashing it captures
  only that the rest of the pipeline ran on that record. Catching
  upstream issues remains a domain-specific problem unrelated to
  the analysis-side chain.
* Adoption is **voluntary** and the engine is only one possible
  tool that could provide such infrastructure. Other CoDa
  toolchains can adopt similar provenance disciplines; the
  argument here is for the *practice*, not for any particular
  software product.
* The chain does not retroactively verify pre-existing
  publications. It applies forward, from the moment a paper adopts
  the practice.

---

## §10  Conclusion

CoDa is a mature methodology, and the field can strengthen its
verifiability with widely-adopted hash-chained provenance. The HUF-CNT engine's hash chain — a
side-effect of the determinism work needed for the analytical
framework — happens to provide infrastructure the community can
adopt, today, to:

* let any reader verify any published result in minutes,
* make selective reporting and audit drift **detectable** rather
  than invisible,
* protect honest authors from accusations of error or
  manipulation by giving them an arithmetic-grade defence,
* lay groundwork for AI-era publishing where automated and
  manual contributions need to be distinguished.

The argument doesn't require accepting CNT's analytical methods
over classical CoDa methods. It requires only acknowledging that
in 2026, **explicit provenance is increasingly expected**, and that
hash chains over deterministic computations are an inexpensive way
to provide it.

The instrument reads. The expert decides. The hashes carry the receipts.

---

## Citation

```
Higgins, P. (2026). Verification, Integrity, and Author Protection:
What the CNT Hash Chain Offers the Compositional Data Community.
HUF-CNT System v1.1.x preprint.
DOI: 10.5281/zenodo.XXXXXXX  (placeholder).
```

Companion technical papers:

```
Higgins, P. (2026). CNT vs Standard CoDa: A Performance Balance Book.
HUF-CNT System v1.1.x docs.

Higgins, P. (2026). CNT ROI and Use-Case Recommendations: A
Composition-of-Effort Reading of the Method-Choice Decision.
HUF-CNT System v1.1.x docs.
```

Engine reference:

```
Higgins, P. (2026). HUF-CNT System: Compositional Navigation Tensor
Reference Implementation. Version 1.0.0 + v1.1.x.
https://github.com/.../HUF-CNT-System
DOI: 10.5281/zenodo.XXXXXXX
```

---

## Appendix — A reviewer's verification recipe

1. Get the paper. Note the engine version `X.Y.Z` and the
   `engine_signature` from any plate footer.
2. Get the raw CSV from the data deposit.
3. `sha256sum input.csv` → compare against `inp.source_file_sha256`.
4. Install matching engine: `pip install huf-cnt==X.Y.Z`.
5. `python -m huf_cnt run input.csv -o my.json --ordering "<published-ordering>"`
6. Compare `my.json`'s `diagnostics.content_sha256` to the
   published value.
7. If match → result reproduces.
8. If mismatch → check `engine_config.active_overrides` and
   `metadata.units` for any disclosed deviation; re-run with
   matching config; compare again.
9. If still mismatch with all config matching → the result as
   published cannot have come from the data as published with
   the engine as published. Contact the authors.

The recipe is intentionally short. That brevity is the point.



---

# Part C — CodaWork 2026 talk plan (15 min + 5 Q&A)


### Compositional Navigation Tensor: a hash-traceable instrument for compositional dynamics

**Speaker:** Peter Higgins
**Format:** 15-minute presentation + 5-minute Q&A
**Date:** 2026-05-05 (preparation)

---

## Timing budget

| Section | Time | Slides | Why |
|---|---:|---:|---|
| §A  CNT introduction | 4:30 | 10 | Set the framework. Get to the demo with cushion. |
| §B  PDF live walkthrough | 8:00 | (no slides, live PDF) | Demonstrate working software. The strongest moment. |
| §C  Closing — 3D projector | 2:30 | (live HTML viewer) | End on motion. The most memorable visual. |
| **Total presentation** | **15:00** | | 30-sec safety cushion built in |
| §D  Q&A | 5:00 | (no slides) | |

**One-line goal of the talk:** "Here is a deterministic, hash-chained
diagnostic instrument for compositional trajectories that ships
classical CoDa plates inside a single audit-grade report."

---

## §A  Slide deck (10 slides, 4:30 total)

Speaker-note convention: **bold = on slide**; plain text = spoken.

### Slide 1 — Title (~ 25 sec)
**Compositional Navigation Tensor**
*A hash-traceable instrument for compositional dynamics*
Peter Higgins  ·  CodaWork 2026

> "I'm going to show you an instrument my team built that takes the
> classical CoDa toolkit, wraps it in a deterministic engine, adds
> trajectory-native operators, and produces hash-chained reports.
> Every plate you'll see in the demo can be re-verified by anyone
> with the raw CSV in two minutes. That's the whole talk."

### Slide 2 — Value to the CoDa community (~ 30 sec)
**Three additions CNT brings to the established CoDa toolkit:**
- Trajectory-native operators (bearings, ω, helmsman, period-2 attractor, IR class)
- End-to-end determinism (raw CSV → JSON → PDF, byte-identical)
- Cross-dataset structural comparison (Stage 4 reports)

**These ship alongside the classical plates — both languages, one report.** Variation
matrix, biplot, balance dendrogram, SBP, ternary, scree are all
in the report — same engine.

> "The framing matters: this isn't a replacement for ILR or the
> classical biplot. It's an extension that ships those plates plus
> the trajectory-native ones in one report — both languages, one
> document."

### Slide 3 — Math step 1: Closure to the simplex (~ 25 sec)
**x ← x / Σx     (with δ-replacement for zeros)**

Diagram: dollar-share / mass-fraction / energy-share rows → simplex points.

> "Standard closure operator. The δ value is in the JSON's
> engine_config.DEFAULT_DELTA. Anyone re-running with a different
> δ produces a different content_sha256 — by design."

### Slide 4 — Math step 2: CLR transform (~ 25 sec)
**clr(x)_j = ln(x_j) − ⟨ln x⟩**

Diagram: simplex points → centred log-ratio space (zero-mean rows).

> "Aitchison's centred log-ratio. Dimension D, but constrained to
> Σ clr_j = 0, so D-1 degrees of freedom."

### Slide 5 — Math step 3: Helmert ILR basis (~ 30 sec)
**ilr(x) = V · clr(x)**

Diagram: D × D Helmert basis schematic; clr → ilr in (D-1) dims.

> "Egozcue's orthonormal Helmert basis. Same as classical CoDa.
> What's different is what we do next."

### Slide 6 — Math step 4: Bearing tensor (atan2 simplification) (~ 35 sec)
**θ_{i,j}(t) = atan2(y_{i,j}, x_{i,j})**

Side by side:
- arccos((u·v)/(|u||v|)) → 12 ops, sign loss, √ε noise floor near 0/π
- atan2 → 4 ops, [-π, π], machine precision

> "Pairwise bearings via atan2. Three-times-fewer ops, 10⁷-times
> better stability near locks. The bearing tensor is what makes
> trajectory-native operators tractable."

### Slide 7 — Math step 5: Metric tensor and M² = I (~ 35 sec)
**M(x) — D × D metric tensor**
**M² = I — verified per timestep, mean residual ≈ 1e-15**

Diagram: M ∘ M = I; residual histogram showing peak at IEEE floor.

> "The metric-dual involution. We compute M's dual, square it,
> verify it's the identity at IEEE floor. This is what lets the
> depth tower be Banach-contractive."

### Slide 8 — Math step 6: Depth tower (recursion) (~ 35 sec)
**Energy tower    ω(level), Hs(level)**
**Curvature tower ω(level), Hs(level)**

Diagram: trajectory of (ω, Hs) per level, each iteration one step deeper.

> "Recursive depth sounder. Two towers — energy and curvature.
> Each level applies the metric-dual; convergence shows up as ω
> dropping to the noise floor."

### Slide 9 — Math step 7: Period-2 attractor & IR classification (~ 35 sec)
**Convergence → period-2 attractor (c_even, c_odd, amplitude A)**
**Eight IR classes** (CRITICALLY / LIGHTLY / MODERATELY / OVERDAMPED + 4 edge cases)

Diagram: amplitude-A reference band with the 8 classes coloured.

> "The depth tower converges to a period-2 attractor whose amplitude
> A is the headline diagnostic. The eight-class taxonomy lives in
> the engine and the JSON. Every class has an interpretation rule."

### Slide 10 — One picture summary (~ 30 sec)
**raw CSV → JSON → 4 stages of PDF report**
**Stage 1: per-timestep | Stage 2: geometry+dynamics 28 plates**
**Stage 3: depth+attractor 11 plates | Stage 4: cross-dataset 11 plates**
**Every page footer carries: engine sig, content SHA, source SHA, date**

> "Here's what comes out the other end. Four stages. Hash chain on
> every page. Now I'm going to show you the actual PDFs."

---

## §B  PDF demo (8 min, no slides)

Open `codawork2026_conference/cnt_demo/02_per_country/ember_jpn/stage2_ember_jpn.pdf`
on the projector in full-screen mode. Have the file already open
and at page 1 to avoid fumbling.

### Walkthrough — choose 5 dwell pages (~ 90 sec each)

**Dwell 1 — Cover page (page 1)**
Talking points:
- "Compositional system geometry and dynamics for, Japan — EMBER electricity generation 2000-2025"
- Auto-generated title from dataset_id
- The traceability block: engine version, engine signature, source SHA, content SHA — all on this one page
- The reading-order map at the bottom: §A disclosure → §B geometry → §C dynamics → §D summary

**Dwell 2 — Data disclosure (page 2)**
Talking points:
- "This is what page 2 of every report looks like — before any analysis"
- Walk down the columns: source SHA, ordering, zero-replacement (δ value visible), units lineage, active engine_config_overrides, lock event count, EITT residuals
- "If any flag is non-empty, the analysis still ran but the reader knows to weight downstream plates accordingly"
- "This is the page that protects you, the author, from accusations later"

**Dwell 3 — Evolution of proportions + ternary (pages 3–4)**
Talking points:
- "Geometry first, basic to advanced"
- Page 3: top is per-carrier line plot, bottom is cumulative stacked area — same data, two views, both Order 1
- Page 4: top-3 ternary with colour-coded time trajectory — Japan's Solar/Wind/Hydro share trajectory through 2000-2025; the post-Fukushima shift is visible

**Dwell 4 — Biplot + balance dendrogram (pages 9 + 11)**
Talking points:
- Page 9: classical CoDa biplot — ray length = carrier importance, angle = log-ratio correlation
- "I'm showing this so the reviewers from the Pawlowsky-Egozcue tradition see we ship the standard plate, computed from the same engine"
- Page 11: Ward dendrogram on the variation matrix — data-driven SBP, not a hand-picked one

**Dwell 5 — System Course Plot + CBS (pages 16 + 25)**
Talking points:
- Page 16: System Course Plot from the Math Handbook Ch 15 — V_net (start → end vector), course directness, PCA path
- Page 25: Compositional Bearing Scope, three orthogonal faces (θ × d_A, θ × κ, d_A × κ)
- "These are the trajectory-native operators CNT adds on top of the established CoDa toolkit"

### Quick scroll through Stage 3 + Stage 4 (~ 60 sec total)

Open Stage 3 (`stage3_ember_jpn.pdf`) — 11 pages — flip through:
- Cover, depth-tower convergence, period-2 attractor card, IR classification card
- "This is Order 3 — the depth tower / IR / attractor view"

Open Stage 4 (`stage4_codawork2026_ember.pdf`) — 11 pages — flip through:
- Per-dataset summary table, cross-dataset amplitude A bar chart, IR-class distribution
- "This is Order 4 — comparing the 8 EMBER countries side by side in one report"

### Close the demo
- "Every PDF you've just seen was generated by `python tools/run_pipeline.py codawork2026_ember`"
- "The full corpus — 25 experiments — runs deterministic in 21 seconds"

---

## §C  Closing — 3D projector (3 min, live HTML)

Open `codawork2026_conference/cnt_demo/03_combined/plate_time_projector_codawork2026_ember.html`
in the browser, full-screen.

Set the dropdown to "◆ ALL COMBINED (shared PCA frame)".

### Talking arc (~ 3 min)

Open with — "I want to leave you with one image."
Click and drag to start the orbit.

> *[Orbiting view, 30 sec]*
> "What you're looking at is 8 EMBER countries' 26-year electricity-mix
> trajectories projected into one shared PCA frame. The barycenter
> of the simplex is the z-axis spine running vertically through the
> middle. Each year is a horizontal slice. Each country is a coloured
> trajectory winding through that stack."

> *[Pause orbit; scrub year slider from 2000 → 2025, 60 sec]*
> "Watch what happens as I scrub forward in time. China climbs in
> coal. Germany drifts toward Solar/Wind. France stays anchored at
> Nuclear. Japan's pre-2011 trajectory is steady, then 2011 hits and
> Nuclear collapses; the trajectory makes a sharp right turn. The
> shape of each country's history is now a 3D curve."

> *[Toggle layers off/on — Trajectory, Carrier rays, Pair edges, 60 sec]*
> "Every line you see is one of five known relationships:
> consecutive-year trajectory, carrier rays from the barycenter,
> pair edges where Pearson r exceeds your threshold, helmsman links,
> lock events. Every one of them traces back to a specific JSON
> field. There are no fabricated connections."

> *[Lock back to ISO view, last 30 sec]*
> "This is the system. Engine 2.0.4, schema 2.1.0, twenty-five
> reference experiments, all reproducing byte-identically. The
> conference package — engine, per-country reports, combined views,
> calibration, doctrine — is one folder, fully self-contained.
> The papers, the engine, the reports, the determinism gate — all
> in the GitHub repo. The instrument reads. The expert decides.
> Thank you."

[Cue: pause for applause; transition to Q&A]

---

## §D  Q&A — 15-question study list

For each: a short answer (~ 20 sec spoken) and a one-line
"if pressed" follow-up. Prepare to answer in 30 seconds or less.

### Q1. "Is CNT a replacement for ILR or an extension?"
**Short:** Extension. The Helmert basis from Egozcue 2003 is the
foundational projection; CNT operates *on top* of ILR coordinates
to compute trajectory-native quantities (bearings, ω, helmsman).
**If pressed:** "Every CNT JSON contains the canonical ILR — you
could ignore everything Higgins-tagged and still use the report
as a classical CoDa pipeline output."

### Q2. "What does the Higgins scale add over the neper?"
**Short:** Nothing physically — it's measured in nepers by
default. The schema 2.1.0 `metadata.units` block just records
which unit (`ratio`, `bit`, `dB_power`, etc.) the input was in
and the conversion factor to neper.
**If pressed:** "The scale's value is in the unit lineage being
auditable, not in a different number space."

### Q3. "How is the bearing tensor different from log-ratio
differences?"
**Short:** Same information, different representation. The bearing
is the angle between two carriers' centred coordinates via atan2;
the log-ratio difference is the magnitude of the same vector. CNT
keeps both because the angular form is what makes period-2
attractor detection clean.
**If pressed:** "Bearing's distribution over carrier-pairs is the
'rose'; the log-ratio's distribution is what the variation matrix
shows. They're the polar and Cartesian readings of the same field."

### Q4. "Why integer orders only? Couldn't trajectory aggregates
be Order 1.5?"
**Short:** Doctrine choice. We round trajectory aggregates UP to
Order 2 because they aggregate across multiple timesteps.
Half-orders would be a category mistake — there's no such thing as
"half a recursion."
**If pressed:** "We considered fractional orders early on. They
made the doctrine harder to teach without buying any clarity in
the diagnostics."

### Q5. "What does the period-2 attractor mean physically?"
**Short:** It means the depth tower's recursion converges to two
alternating compositional states. The amplitude A is the gap
between them in Hs space. For most well-conditioned compositional
trajectories, A is small (CRITICALLY_DAMPED); for trajectories
with carrier phase-out, A is large (OVERDAMPED).
**If pressed:** "It's not a physical limit cycle of the original
data — it's the limit cycle of the metric-dual recursion. The
amplitude is structural."

### Q6. "How is zero-replacement handled differently from standard
practice?"
**Short:** The δ value is in `metadata.engine_config.DEFAULT_DELTA`
and any per-call override is in `active_overrides`. Different δ →
different content_sha256, by design. So the choice is auditable.
**If pressed:** "We don't claim to solve the zero problem; we
claim to disclose how we addressed it."

### Q7. "Can the engine handle very high-D problems? Genomics
datasets are D > 100."
**Short:** The math scales. The bottleneck for high D is plate
clutter — at D > 8 the full biplot starts to crowd, which is why
we ship `p_biplot_topN`. We've tested up to D = 10 on financial
data; D > 50 hasn't been benchmarked but should run.
**If pressed:** "If you have a high-D problem we'd love a test
case to add to the corpus."

### Q8. "How does CNT compare to van den Boogaart's compositions
package in R?"
**Short:** Different scopes. compositions is the canonical R
toolkit for static-snapshot CoDa; CNT is built around trajectory
dynamics with a deterministic engine. They're complementary —
the cnt.R port is parity-tested against the Python engine and
honours the same schema.
**If pressed:** "For single-snapshot work, compositions is the simplest path. If it's trajectory-native, CNT is the differentiator."

### Q9. "What's the engine's computational cost?"
**Short:** Engine pass is ~120 ms per dataset for typical T = 26,
D = 8. Stage 1 + 2 + 3 atlas adds ~5 s rendering. Full 25-experiment
corpus runs in ~21 seconds with the determinism gate.
**If pressed:** "Memory peak is ~35 MB; not GPU-bound; trivially
parallelisable across datasets."

### Q10. "Is the R port at full parity with Python?"
**Short:** Yes — engine 2.0.4 / schema 2.1.0 in both. Parity test
in `tests/test_parity.sh` confirms identical content_sha256 from
the two implementations on the same inputs.
**If pressed:** "Some atlas modules are Python-only; the R port
covers the engine + JSON output."

### Q11. "Why use a SHA chain instead of just publishing the
script?"
**Short:** Because scripts mutate. The hash chain pins the bits.
A reviewer who has the raw CSV plus the published content_sha256
can verify in two minutes; reading and trusting a script takes
hours and assumes the script you read is the script that ran.
**If pressed:** "The chain doesn't replace the script — it
authenticates which version of the script ran, when, and on what."

### Q12. "Can I integrate it with my existing ILR pipeline?"
**Short:** Yes. The JSON's `coda_standard` block carries the
canonical ILR, CLR, variation matrix, etc. — read those into your
existing pipeline and ignore the `higgins_extensions`. The schema
is open and stable.
**If pressed:** "We've designed the dual-classification (CoDa
standard / Higgins extensions) precisely so the engine doesn't
force adoption of the extension layer."

### Q13. "When does the engine fail or refuse to produce output?"
**Short:** Three cases. (1) D = 2 — the depth tower can't exercise
off-diagonal metric structure; flagged D2_DEGENERATE. (2) Single
carrier > 60 % — flagged CURVATURE_VERTEX_FLAT. (3) M² ≠ I
beyond floating-point error — flagged in `involution_proof`. None
of these halt; all of them annotate.
**If pressed:** "The engine's discipline is annotate, never crash.
Disclosure trumps refusal."

### Q14. "Is the Helmert basis a fixed choice or can users pick
their own SBP?"
**Short:** The engine emits the Helmert basis as the canonical
ILR. The Stage 2 atlas separately computes a data-driven SBP via
Ward clustering on the variation matrix and shows it as a
balance dendrogram + SBP-table plate. So users see both: the
canonical ILR and the data-driven balance hierarchy.
**If pressed:** "User-supplied SBP is a v1.2 candidate; the
schema has the slot reserved."

### Q15. "What's the licence and how do I get the system?"
**Short:** Apache-2.0. GitHub repo at the URL on the title slide.
The conference package is one folder, fully self-contained:
engine source, per-country reports, combined views, calibration,
doctrine. `pip install -e .` runs the full demo.
**If pressed:** "Patent grant included. We want this used."

---

## Pre-talk preparation checklist

The morning of the talk:

- [ ] Test the projector with the full Stage 2 PDF in full-screen
- [ ] Test the HTML projector in browser; pre-set ISO view + scrub to year 2010
- [ ] Have backup copies on USB and on a cloud drive
- [ ] Print this plan as a single page for the lectern
- [ ] Check microphone before stepping up — practice voice level
- [ ] Drink water, breathe, remember: the work is solid; you're
      reporting on it, not auditioning

Practice once front-to-back the night before with a watch
running. Aim for 14:30. If you finish early, that's better than
running over.

---

*The instrument reads. The expert decides. The hashes hold the line.*



---

# Part D — Public-trial readiness audit


**Build:** v1.0.0 (CodaWork 2026 demo) + v1.1.x feature set in tree
**Date:** 2026-05-05
**Audience:** independent reviewers, partner labs, conference attendees

This document collects every claim the system makes and points the reader at
the file that proves the claim.

## 1. Determinism

| Claim | Evidence |
|---|---|
| Same input + same config → identical `content_sha256` | `cnt/tests/test_determinism.py` (3-experiment fast gate) |
| 20-experiment full-corpus determinism gate passes | `cnt/tests/test_full_corpus.py` |
| Python ↔ R parity at engine 2.0.3 | `tests/test_parity.sh`, GitHub Actions workflow |
| PDF outputs byte-identical across runs (post v1.1-A) | `atlas/det_pdf.py` — fixed-epoch metadata, deterministic across calls |

## 2. Correctness (math)

| Claim | Evidence |
|---|---|
| ILR ≡ Helmert · CLR | `cnt/cnt.py` §0 + `atlas/stage1_v4.py` calibration |
| M² = I residual ≤ 1e-15 typical | `diagnostics.higgins_extensions.involution_proof` per JSON |
| Aitchison distance = ‖clr(x)−clr(y)‖₂ | engine implementation; verified at IEEE floor |
| Stage 1 calibration: 27-point HLR grid drift O(1e-10) | `atlas/STANDARD_CALIBRATION_27pt_*` |
| Stage 2 calibration: directness = 1.0 (straight) / 0.0 (loop) at IEEE floor | `atlas/STANDARD_CALIBRATION_stage2_*` |

## 3. Doctrine

| Claim | Evidence |
|---|---|
| Output Doctrine v1.0.1 — integer orders only, round UP | `atlas/OUTPUT_DOCTRINE.md` |
| Doctrine document hash-stamped | `atlas/OUTPUT_DOCTRINE.md.sha256` |
| Stage 1 standard locked | `atlas/stage1_v4.py` |
| Stage 2 standard locked + pseudocode + R port | `atlas/stage2_locked.py`, `STAGE2_PSEUDOCODE.md`, `stage2.R` |

## 4. Disclosure (every adapter is shipped and documented)

| Claim | Evidence |
|---|---|
| Every reference experiment's pre-parser is shipped | `adapters/` |
| Each adapter's transformations are itemised | `adapters/ADAPTERS_DISCLOSURE.md` |
| Five surveyed-but-deferred datasets enumerated | `experiments/DEFERRED_ADAPTERS.md` |

## 5. Reproducibility

| Claim | Evidence |
|---|---|
| Quickstart runs in 5 minutes | `examples/01_quickstart.py` |
| Full-corpus replay in ~21 seconds | `mission_command/mission_command.py` |
| Per-experiment journals auto-generated | `experiments/<sub>/<id>/JOURNAL.md` |
| Module pipeline (Stage 1/2/Spectrum/Projector) on-demand | `tools/run_pipeline.py codawork2026_ember` |

## 6. Conference demo

The complete demo package lives at `codawork2026_conference/cnt_demo/`:

- 8 EMBER countries + World, all stages × all plates
- Combined spectrum (paper) + interactive plate-time projector
- Full calibration suite
- Doctrine + pseudocode

A 30-minute walkthrough script is at `codawork2026_conference/DEMO_GUIDE.md`.

## 7. Known limitations (audit-honest)

All v1.0.x items are now in place in v1.1.x:

- ✅ `engine_config_overrides` block in `master_control.json` is now
  honoured by the engine. Per-experiment and per-project overrides
  flow through `cnt_run(..., engine_config_overrides=...)`. Different
  overrides → different `content_sha256`, by design. Echoed in
  `metadata.engine_config.active_overrides` for full audit.
- ✅ Native units adopted in the engine (schema 2.1.0). The engine
  writes `metadata.units` with `input_units`,
  `higgins_scale_units`, and `units_scale_factor_to_neper`. The
  adoption is additive — INPUT_UNITS=ratio (the default) reproduces
  v1.0.x JSON shape modulo the new metadata block.
- ✅ All 5 previously-deferred adapters built and shipping
  (`markham_budget`, `iiasa_ngfs`, `esa_planck_cosmic`,
  `financial_sector`, `chemixhub_oxide`). Synthetic baselines
  derived from published recipes; raw-data swap-in points
  documented in every adapter's docstring.

The reference corpus is now **25 experiments**, all passing the
determinism gate at engine 2.0.4 / schema 2.1.0.

## 8. License

Apache-2.0. Permissive use including commercial; only obligation is
attribution; patent grant included.



---

# Part E — Master handbook reading list (legacy CNT_HANDBOOK.md, retained for context)


**Version:** 1.0.0 (in build)
**Engine:** cnt 2.0.3
**Schema:** 2.0.0
**Date:** 2026-05-05

This handbook is the canonical reference for the HUF-CNT System. It is
written for users who need to (a) understand what the system computes,
(b) trust the result, and (c) reproduce the result on their own data.

The handbook is organised into ten sections. Each section is a separate
markdown file under `handbook/`; this file is a master table of contents
that also serves as a single-document reference when concatenated. The
HTML build at `handbook/docs_html/index.html` is the same content
rendered for browser navigation.

---

## Table of contents

| § | Title | File |
|---|---|---|
| 1 | Introduction — what HUF, Hˢ, and CNT are; how to read this handbook | `01_introduction.md` |
| 2 | Compositional data basics — simplex, closure, CLR/ILR, Aitchison geometry | `02_compositional_data_basics.md` |
| 3 | The engine — cnt.py / cnt.R | `03_engine_cnt.md` |
| 4 | The schema — JSON contract | `04_schema.md` |
| 5 | The atlas — plate viewer | `05_atlas.md` |
| 6 | Mission Command — orchestrator | `06_mission_command.md` |
| 7 | **Pre-parsers and adapters — full disclosure** | `07_pre_parsers_disclosure.md` |
| 8 | Experiments walkthrough — twenty real datasets | `08_experiments_walkthrough.md` |
| 9 | **Determinism contract** — the reproducibility guarantee | `09_determinism_contract.md` |
| 10 | Glossary | `10_glossary.md` |

Sections 7 and 9 are the trust foundation. Read them first if your
question is "should I rely on this for published research?"

---

## How the system fits together

```
                  raw third-party data
                          |
                  [ pre-parser / adapter ]   <-- handbook §7 — disclosed
                          |
                input CSV (compositional)
                          |
                          | metadata.input_csv_sha256
                          v
                  [ cnt engine ]              <-- handbook §3
                          |
                          | metadata.engine_config
                          | diagnostics.content_sha256
                          v
                canonical CNT JSON           <-- handbook §4 — schema
                  /                  \
                 /                    \
        [ atlas ]                [ mission command ]
        §5                       §6
         |                        |
         v                        v
  PDF + HTML atlas           multi-run catalog
  with cover banner          delta comparisons
  + run catalog              cross-experiment reports
```

Every box names a tool; every arrow names an artifact; every artifact is
hashed. The chain is acyclic and complete.

---

## What you can do with this handbook in five minutes

1. Read §1 (introduction) for the what and why.
2. Skim §3 (engine) and §4 (schema) for the compute path.
3. Read §9 (determinism contract) to understand the trust model.
4. Pick one experiment in §8 that's near your domain and read its narrative.
5. Run `examples/01_quickstart.py` against your own CSV.

---

## What this handbook does not cover

* **The mathematical proofs.** The engine implements known CoDa results
  plus the Higgins decomposition. For the proofs, see the references in
  §1 and §2 — Aitchison 1986, Egozcue 2003, Pawlowsky-Glahn 2015,
  Higgins 2026.
* **Hand-tuned plotting.** The atlas produces deterministic standard
  plates. If you need a custom figure for a paper, the JSON contains
  every number you need; export those and plot with the tool of your
  choice.
* **Stream / online processing.** The engine is a batch tool. Each run
  ingests a finite CSV and writes a finite JSON.
* **Adapters for data sources we did not use.** Five datasets are
  documented as deferred in `experiments/DEFERRED_ADAPTERS.md` with
  blueprints for future contributors.

---

*The instrument reads. The expert decides. The loop stays open.*



---

# Part F — Citation block

If you use this software in published research, please cite:

```
Higgins, P. (2026). HUF-CNT System: Compositional Navigation Tensor
reference implementation. Version 1.0.0 + v1.1.x.
https://github.com/.../HUF-CNT-System
DOI: 10.5281/zenodo.XXXXXXX
```

The companion preprint papers (consolidated into this volume) cite as:

```
Higgins, P. (2026). CNT vs Standard CoDa: A Performance Balance Book.
HUF-CNT System v1.1.x — VOLUME I §I.

Higgins, P. (2026). CNT ROI and Use-Case Recommendations.
HUF-CNT System v1.1.x — VOLUME II §G.

Higgins, P. (2026). Verification, Integrity, and Author Protection:
What the CNT Hash Chain Offers the Compositional Data Community.
HUF-CNT System v1.1.x — VOLUME III §B.
```

See `CITATION.cff` for machine-readable citation metadata.

---

# Part G — License

Apache-2.0. The license grants permissive use including commercial;
the only obligation is attribution. The patent grant is included.

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
