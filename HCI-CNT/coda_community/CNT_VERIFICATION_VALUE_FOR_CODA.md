# Verification, Integrity, and Author Protection
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
