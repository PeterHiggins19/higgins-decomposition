# Trust and Verification — for skeptical users of the Hˢ codebase

**Filed:** 2026-05-22 (v1.0) · **Revised:** 2026-05-24 (v1.1 — added §1.5 layered parity contract; precision pass through §§1–3, §6.3, §7 per ChatGPT review of byte-identical-hash overclaim across canonicalization profiles) · **Conforms to:** HUF-STD-001 v1.1, HUF-STD-002, HUF-STD-003 · **Author:** Peter Higgins, Rogue Wave Audio · **Status:** Operational reference.

> If you are reading this because you do not yet trust the published code in this repository, **this document is for you.** The framework's discipline is that *trust is earned, not expected*. Every algorithm in the Hˢ repository is documented in at least four forms so that a skeptical user can independently verify the published code without ever running it. Below: what those forms are, where they live, and how to use them to verify the framework's central claims for yourself.

---

## 1. The four forms of every algorithm

Each engine in this repository exists in four forms, by design:

| Form | What it is | Where it lives | Why it matters |
|---|---|---|---|
| **(1) Python reference** | The canonical implementation, executable as `python cnt.py input.csv -o output.json` | [`HCI-CNT/engine/cnt.py`](HCI-CNT/engine/cnt.py), [`HCI-CNQ/engine/cnq.py`](HCI-CNQ/engine/cnq.py) | The published code; what produces the canonical `content_sha256` |
| **(2) R reference** | The parallel implementation in R, executable as `Rscript cnt.R input.csv output.json` | [`HCI-CNT/engine/cnt.R`](HCI-CNT/engine/cnt.R), [`HCI-CNQ/engine/cnq.R`](HCI-CNQ/engine/cnq.R) | An independent re-implementation in a different language. Cross-language parity contract is **per-field numerical agreement at IEEE-floor tolerance** — see §1.5 for the layered parity contract. The fact that two independent implementations agree numerically is part of the determinism contract |
| **(3) Pseudocode** | The language-agnostic algorithm reference — every step described in language-neutral terms with explicit formulas | [`HCI-CNT/engine/CNT_PSEUDOCODE.md`](HCI-CNT/engine/CNT_PSEUDOCODE.md) (v3.1.0), [`HCI-CNQ/engine/CNQ_PSEUDOCODE.md`](HCI-CNQ/engine/CNQ_PSEUDOCODE.md) | The contract. Both Python and R reference implementations are faithful translations of the pseudocode. Any new port (Julia, Rust, C++, Fortran, JavaScript) must reproduce the same per-field numerical results at IEEE-floor tolerance; byte-identical `content_sha256` additionally requires adopting one of the published canonicalization profiles (§1.5) |
| **(4) Software specification** | The formal standard governing input format, output format, determinism contract, and conformance criteria | [`huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json`](huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json) (HUF-STD-002) | What every implementation must satisfy. The "I/O contract" is published as a structured JSON specification |

There is also a fifth form for failure modes:

| Form | What it is | Where it lives |
|---|---|---|
| **(5) Anti-specification** | What the engine MUST NOT do — the failure modes that would invalidate the determinism contract | [`HCI-CNT/engine/ANTI_SPECIFICATION.md`](HCI-CNT/engine/ANTI_SPECIFICATION.md), [`HCI-CNQ/engine/ANTI_SPECIFICATION.md`](HCI-CNQ/engine/ANTI_SPECIFICATION.md) |

If you can read the pseudocode (form 3) and the specification (form 4), you can re-implement the engine in any language and verify it against the published Python (form 1) and R (form 2). The verification has two layers — *per-field numerical agreement* at IEEE-floor tolerance (the unconditional contract), and *byte-identical content_sha256* (a conditional contract that requires adopting a published canonicalization profile). See §1.5 below for the precise statement.

---

## 1.5 The layered parity contract

The framework's parity contract has four explicit layers. *Conflating them is the most common reviewer-side misreading*; this section states them precisely so a technically sharp reviewer can know what is claimed at each level.

### Layer 1 — Intra-language determinism (unconditional, byte-identical)

Re-running the *same reference implementation* on the same input on the same platform produces a byte-identical `content_sha256`. This holds for `cnt.py` on Python and for `cnt.R` on R, each within its own language's canonicalization profile. *This is the form-1 / form-2 internal contract* and is enforced by the engine's determinism test suite.

### Layer 2 — Cross-language CNT parity (per-field numerical, NOT byte-identical hash)

Across Python and R, **the CNT engines agree per-field at IEEE-floor tolerance, NOT by byte-identical `content_sha256`**. This is a deliberate design decision: each language has its own canonical-dumps behavior (Python's `json.dumps(sort_keys=True, separators=(",",":"), ensure_ascii=True)` vs R's `jsonlite::toJSON` family; different float-format conventions; different key-sorting algorithms). The cross-language CNT parity verifier is `scripts/verify_cross_language_parity.py`; it operates on the numerical fields and checks IEEE-floor tolerance. *This is explicitly documented at the top of `cnt.R` (lines 9–12).*

### Layer 3 — Cross-language CNQ parity (per-field numerical at ≤1 ULP, byte-identical hash conditional on float-formatting profile)

For CNQ, the parity contract is tighter than for CNT: per-field numerical agreement to ≤ 1 ULP, **and** byte-level `content_sha256` match *given identical float-formatting policy* (per `HS_FAST_REFRESH.json` `canonical_engines.cnq_r.parity_contract`). The conditional byte-match is achievable for CNQ but is not currently the operational default; the unconditional contract is per-field numerical agreement at ≤ 1 ULP.

### Layer 4 — Third-language re-implementation (per-field numerical at IEEE floor, byte-identical hash conditional on profile adoption)

A re-implementation in any third language (Julia, Rust, C++, Fortran, JavaScript) is **conformant** to the framework if it reproduces per-field numerical agreement at IEEE-floor tolerance with the published Python or R reference on the three canonical reference inputs (§3 Step 5 below). A re-implementation is **byte-conformant** if it additionally adopts the canonicalization profile of either the Python reference (sort_keys + separators + ensure_ascii — see §3 Step 6) or the R reference (jsonlite::toJSON with the published configuration); in that case its `content_sha256` will match the corresponding language's published hash byte-identically.

### Summary table

| Comparison | Per-field IEEE-floor parity | Byte-identical `content_sha256` |
|---|---|---|
| Same engine, same language, same platform (Layer 1) | Yes (by construction) | **Yes** (unconditional) |
| `cnt.py` ↔ `cnt.R` (Layer 2) | **Yes** (≤ machine epsilon) | No (by design — different canonicalization profiles) |
| `cnq.py` ↔ `cnq.R` (Layer 3) | **Yes** (≤ 1 ULP) | Conditional on declaring identical float-formatting profile |
| Third-language port ↔ Python reference (Layer 4) | **Yes** (required for conformance) | Conditional on adopting Python's canonicalization profile |
| Third-language port ↔ R reference (Layer 4) | **Yes** (required for conformance) | Conditional on adopting R's canonicalization profile |

**Bottom line.** The framework's central claim is the *numerical* one: two independent implementations of the published pseudocode reproduce the same mathematical result at IEEE-floor precision on the same input. The byte-identical hash is a *stronger* contract that requires explicit canonicalization-profile agreement on top of correct algorithm implementation; it is provided by Layer 1 unconditionally and by Layers 3–4 conditionally. *Both layers are checkable; the framework does not overclaim across the layer boundary.*

---

## 2. Why this matters — the framework's discipline

Software repositories on the public internet have been compromised, both at the language-package-manager level (npm, PyPI) and at the source-host level (GitHub itself, via supply-chain attacks). A skeptical user is right to be cautious. This document acknowledges that caution and gives you the means to act on it without losing access to the framework.

The Hˢ framework's discipline is *trust by independent reproduction*:

- We have not asked you to trust the binary execution of our code.
- We have asked you to trust the *algorithm* — described in language-agnostic pseudocode, formalised in HUF-STD-002, and proved mathematically in the lemma chain of [`papers/flagship/GROUND_STATE_AND_TRACTION.md`](papers/flagship/GROUND_STATE_AND_TRACTION.md) v2.2.
- The algorithm produces a deterministic, content-addressable output (`content_sha256`) on every run within a given canonicalization profile.
- Two independent implementations that follow the pseudocode and the specification must produce **the same per-field numerical results at IEEE-floor tolerance** on the same input. If both implementations also adopt the same canonicalization profile, their `content_sha256` values match byte-identically; if they adopt different profiles (e.g., one Python-canonical, one R-canonical), they agree per-field numerically but their hashes differ — see §1.5 above.
- Therefore: if your independent implementation produces per-field numerical agreement at IEEE-floor tolerance with the published reference, the published code is faithful. If it also matches the published `content_sha256` byte-identically, your implementation has additionally adopted the canonical canonicalization profile. If neither holds, either your implementation has a bug or the published code has one — either way, the discrepancy is observable.

This is **falsifiability by numerical agreement + content hash**, the closure-check principle of the framework (Theorem 1 of the flagship) applied to its own implementation. The engine satisfies its own determinism contract every time it runs; you can verify the numerical contract holds at IEEE floor (unconditional, cross-language) and the hash contract holds within the canonicalization profile (Layer 1 unconditional; Layers 3–4 conditional).

---

## 3. The verification protocol — step by step

A skeptical user who wishes to verify the published code *without running it* follows this protocol:

### Step 1 — Read the pseudocode

Pick the engine you wish to verify:
- For CNT: [`HCI-CNT/engine/CNT_PSEUDOCODE.md`](HCI-CNT/engine/CNT_PSEUDOCODE.md) (v3.1.0)
- For CNQ: [`HCI-CNQ/engine/CNQ_PSEUDOCODE.md`](HCI-CNQ/engine/CNQ_PSEUDOCODE.md) (v1.0.0)

Read it end-to-end. Every algorithm is described in language-neutral terms with explicit formulas and explicit configuration constants. If anything is ambiguous, that is a documentation bug — open an issue on the repository (you do not need to run any code to file an issue).

### Step 2 — Read the specification

Read [`huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json`](huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json) (HUF-STD-002). This is the formal I/O contract: input format, output format, determinism requirements, anti-specification of what implementations MUST NOT do. The specification is JSON so that it is machine-readable and unambiguous.

### Step 3 — Read the anti-specification

Read [`HCI-CNT/engine/ANTI_SPECIFICATION.md`](HCI-CNT/engine/ANTI_SPECIFICATION.md). This catalogues the failure modes the engine MUST NOT exhibit. It is the falsifiability layer of the implementation — what would break the determinism contract.

### Step 4 — Re-implement in your language of choice

Using only the pseudocode (form 3), the specification (form 4), and the anti-specification (form 5), implement the engine in your preferred language. The pseudocode is deliberately language-agnostic; common implementations follow the natural idioms of the host language (numpy in Python, base R + jsonlite in R, Numpy.jl in Julia, ndarray in Rust, Eigen in C++).

Do not consult the published Python or R reference implementation while doing this. The point of the exercise is independent verification.

### Step 5 — Run your implementation on the canonical reference inputs

The framework publishes three canonical reference inputs with known `content_sha256` values:

| Dataset | D | T | Source | Published `parent_cnt_content_sha256` |
|---|---|---|---|---|
| Backblaze fleet drive failures | 4 | 731 | [`HCI-CNQ/experiments/backblaze/`](HCI-CNQ/experiments/backblaze/) | (see directory) |
| Planck CMB photon power per multipole | 4 | 2499 | [`HCI-CNQ/experiments/planck_cmb/`](HCI-CNQ/experiments/planck_cmb/) | `3de7d4007866dc11c64d5342974d6c9d2dfc1906166627999194df3fe6a400c4` |
| Standard Model neutrino oscillation | 3 | 1000 | [`HCI-CNQ/experiments/sm_neutrino/`](HCI-CNQ/experiments/sm_neutrino/) | `60d733d2219fbe3cf6ea5647d0f17139923d578ffee0d16a124fbe4eac526952` |

The input CSV files in each directory are stable; their bytes do not change. Run your implementation against each input and produce your own output JSON.

### Step 6 — Compare your output to the published reference

You have two parity layers to choose from (per §1.5). The numerical contract is unconditional; the hash contract is conditional on canonicalization-profile adoption.

**Numerical comparison (recommended; the unconditional contract).** Compare your output JSON field-by-field against the published reference output JSON at IEEE-floor tolerance (`abs(your_value − reference_value) ≤ 1e−15` for scalars; per-element tolerance for arrays). The `scripts/verify_cross_language_parity.py` script in the repository implements exactly this comparison and operates on the cnt.py ↔ cnt.R baseline; you can run it against your own output as the second argument.

**Hash comparison (additional, conditional).** If you want to claim the *stronger* byte-identical-hash conformance with the Python reference, your serialization must adopt the Python canonical-dumps profile exactly:

```
1. Deep-copy your output JSON
2. Zero out the metadata.content_sha256 field itself
3. Zero out metadata.timestamp_utc and metadata.host_metadata (non-deterministic fields)
4. Reduce metadata.input_path to its basename
5. Serialize canonically using the Python profile:
   - sort_keys=true (recursive, all dict levels)
   - separators=(",",":")  (compact form, no whitespace)
   - ensure_ascii=true     (non-ASCII characters escaped to \uXXXX)
   - float repr: Python's default repr(float) — shortest round-tripping decimal
6. UTF-8 encode and SHA-256 the result
```

A re-implementation that adopts this exact serialization profile will produce a `content_sha256` byte-identical to the Python reference. A re-implementation that uses a different canonicalization (e.g., R's `jsonlite::toJSON` with different float-formatting; or a custom canonicalization) will produce a *different* hash *but the same per-field numerical values* — that re-implementation is conformant via the numerical contract but not via the hash contract. Either form of conformance is publishable; the framework does not privilege one over the other.

The published Python reference hash is the one in §3 Step 5 above; the published R reference hash for `cnt.R` is *different* from the Python one for CNT (Layer 2; by design), so do not compare your Python-canonicalised hash against the R-reference hash and conclude there is a discrepancy.

### Step 7 — Interpret the result

The interpretation depends on which parity layer your comparison is operating in (§1.5). The recommended primary test is the **numerical comparison** (unconditional contract); the hash comparison is the **conditional secondary test** that requires canonicalization-profile adoption.

#### Numerical comparison outcomes

| Outcome | What it means |
|---|---|
| **All fields agree at IEEE-floor tolerance** | The published Python / R code is a faithful translation of the pseudocode you re-implemented. You have independently verified the framework via the unconditional cross-language contract. *This is the framework's central conformance claim.* |
| **Most fields agree at IEEE-floor; a small subset differs by ≤ a few ULP** | Probable per-field tolerance issue (intermediate-result rounding order; trigonometric function library differences across languages). Document the specific fields; this is a publishable observation but not necessarily a defect — open a discussion issue |
| **Fields differ at levels much larger than IEEE floor (e.g., 10⁻⁶ or worse)** | Either (a) your implementation has a real bug, (b) the pseudocode has an ambiguity, or (c) the published Python / R has drifted from the pseudocode. Open an issue — the discrepancy is actionable |
| **You cannot produce a comparable JSON at all** | The CSV input was misread or the JSON output schema is wrong. Check input-parsing against the CCTT v1.0 standard ([`ai-refresh/CCTT_RUNBOOK.md`](ai-refresh/CCTT_RUNBOOK.md)) and the output schema in HUF-STD-002 |

#### Hash comparison outcomes (only meaningful if you have adopted the Python canonicalization profile per Step 6)

| Outcome | What it means |
|---|---|
| **Hash matches the Python reference byte-identically** | You have additionally verified that your serialization adopts the same canonicalization profile as the Python reference. This is a stronger conformance statement than numerical-only. |
| **Hash differs from Python reference but numerical fields agree at IEEE-floor** | Your canonicalization profile differs from Python's. This is *not* a defect under the framework's parity contract — it is Layer 2 / Layer 4 behavior. Either adopt the Python profile (per Step 6) to also match the hash, or document your own canonicalization profile and publish your own hash. |
| **Hash differs and numerical fields also differ** | The numerical-comparison outcomes above apply; the hash mismatch is a downstream consequence of the numerical mismatch and is not itself diagnostic. |

The framework's central claim is that **the per-field IEEE-floor numerical agreement is the normal result** of an independent implementation of the pseudocode. This has been validated across the published Python and R implementations on the three canonical datasets above; the bit-identical residuals on physically unrelated D=4 datasets (Backblaze and Planck CMB both at `max_residual = 4.440892098500626 × 10⁻¹⁶`) are the empirical proof. The byte-identical hash match is the additional conformance available when canonicalization profiles agree; it is true for `cnt.py` ↔ `cnt.py` and `cnt.R` ↔ `cnt.R` (Layer 1) and is conditionally true for `cnq.py` ↔ `cnq.R` (Layer 3 — see §1.5) and for any third-language port that adopts a published canonicalization profile (Layer 4).

---

## 4. The CCTT v1.0 protocol — the end-to-end runbook

For users who *do* wish to run the published code, the framework provides a single executable protocol that walks the user through a complete reproducible analysis with confirmation gates at every step:

- [`ai-refresh/CCTT_QUICKSTART.md`](ai-refresh/CCTT_QUICKSTART.md) — the 30-second orientation
- [`ai-refresh/CCTT_RUNBOOK.md`](ai-refresh/CCTT_RUNBOOK.md) — the 7-phase protocol with explicit user confirmation gates
- [`ai-refresh/CCTT_BUILD_INSTRUCTION_v1.0.json`](ai-refresh/CCTT_BUILD_INSTRUCTION_v1.0.json) — the machine-readable spec for AI-assistant execution

The CCTT protocol runs in two interchangeable modes:

- **User-mode** — researcher walks the runbook by hand
- **User + AI-mode** — AI assistant (Claude, ChatGPT, Gemini, or in-house model) executes the 7 phases; user confirms at every gate

The protocol is identical in both modes. Pilot acceptance test: an AI given only the spec and a raw CSV produced a Python implementation that reproduced the canonical Python `content_sha256` byte-for-byte (Layer 1 of the parity contract — same canonicalization profile). The same protocol executed with an R-targeting AI would reproduce the canonical R `cnt_content_sha256` byte-for-byte (also Layer 1) and would reproduce the Python numerical fields at IEEE-floor tolerance (Layer 2, cross-language); whether the R-derived hash would match the Python-derived hash byte-identically depends on whether both implementations adopt the same canonicalization profile (Layer 4).

---

## 5. The mathematical correctness layer

Verification by hash is verification of *implementation faithfulness*. Verification of *mathematical correctness* is a separate question, answered by:

### 5.1 The flagship paper's lemma chain

[`papers/flagship/GROUND_STATE_AND_TRACTION.md`](papers/flagship/GROUND_STATE_AND_TRACTION.md) v2.2 — §7 contains eight formal lemmas with proofs:

| Lemma | What it certifies |
|---|---|
| 1 | Closure of the DADC partition (Σ Gᵢ = c) — proves the partition apportionment is well-defined |
| 2 | Wave-equation / Rayleigh-Sommerfeld basis — proves the acoustic instance is rigorous |
| 3 | Helmholtz reciprocity — proves forward (DADC) ↔ inverse (DADI) consistency |
| 4 | Banach fixed-point convergence — proves the DADI iteration converges geometrically |
| 5 | ADAC contractive stability — proves the adaptive feedback is asymptotically stable |
| 6 | SEA matrix positive-definiteness + Gershgorin — proves the high-frequency room solution exists and is unique |
| 7 | Group delay as uniform rotation on S³ — proves the time-on-simplex mechanism |
| 8 | Closure invariance under CLR — proves the log-ratio transform preserves the closure |

Plus two master theorems (unified formula closure, compositional traction generalization). The proofs are each a few lines and rely only on standard mathematical results that have been in the literature for 60–130 years. *You do not need to trust the engine to verify the math; you need to read the lemmas and check the proofs.*

### 5.2 The peer-reviewed citation chain

[`papers/flagship/GROUND_STATE_AND_TRACTION.md`](papers/flagship/GROUND_STATE_AND_TRACTION.md) §15 lists 16 externally peer-reviewed references that ground every lemma. Banach (1922), Helmholtz (1860), Hamilton (1843), Aitchison (1986), Egozcue et al. (2003), Glasberg & Moore (1990), Pawlowsky-Glahn et al. (2015) — each of these is a published, citeable, independently checkable source. The framework's lemma chain composes their results; the proofs do not invent new mathematics.

### 5.3 The IEEE-floor empirical evidence

The three confirmation datasets (Backblaze, Planck CMB, SM neutrino) produce convergence at the IEEE float64 floor (`max_residual ≈ 4.44 × 10⁻¹⁶`). This is *not* a soft validation; it is convergence to the hardware precision limit, on *physically unrelated* datasets. The residual is `2 * machine_epsilon` to within a factor of two — that is the algorithmic result agreeing with the float64 representation to the last bit.

This level of convergence is impossible to fake. If you re-implement the engine and your implementation produces a higher residual, you have a real bug. If you re-implement the engine and your implementation produces the same hardware-floor residual on the same dataset, your implementation is converging to the same mathematical limit the canonical code does.

---

## 6. What is complete today, and what is queued

The framework's discipline includes honest accounting of gaps:

### 6.1 Complete

- **Python reference implementations** of both CNT (v3.1.0) and CNQ (v2.0.0) — fully tested
- **R reference implementations** — CNT at v3.0.0, CNQ at v2.0.0 (CNT R port to v3.1.0 queued as EngPromo-2; cf. §6.2)
- **Pseudocode** — CNQ_PSEUDOCODE.md (v1.0.0, 18 KB) and CNT_PSEUDOCODE.md (v3.1.0, ~30 KB, this consolidation)
- **Schema** — CNQ_SCHEMA.md (formal CNQ output schema); CNT schema documented in handbook VOLUME_1_THEORY_AND_MATHEMATICS.md Part E
- **Specification** — HUF-STD-002 Tensor Train I/O Standard (machine-readable JSON)
- **Anti-specification** — both engines have explicit ANTI_SPECIFICATION.md files cataloguing failure modes
- **Test suites** — both engines have determinism, first-principles, dimension-policy, and full-corpus tests
- **CCTT v1.0 protocol** — 7-phase end-to-end reproducible runbook, both human and AI modes
- **Three IEEE-floor confirmation datasets** — Backblaze, Planck CMB, SM neutrino, all with pinned input CSVs and published `content_sha256` values
- **Hash-chained provenance** — SHA-256 from raw input CSV → CNT JSON → CNQ JSON → plates → projector → manuscript
- **Engine-independence policy** — `cnt_content_sha256` and `cnq_content_sha256` are unrelated by design; each engine can be verified independently

### 6.2 Queued (post-conference, 2026-06-06+)

Per HUF-STD-002 `post_conference_implementation_targets.ordered_targets`:

1. Power Share / Activation Coefficient diagnostic block in CNT (INV-060 STAGED → CANONICAL)
2. `hs_cnq_pdf_exporter.py` implementation (INV-062 STAGED → CANONICAL; PDF/A-3 + veraPDF)
3. PNG / SVG export siblings for all Stage plate modules
4. Stage 3 plate module (`atlas/stage3.py`) — visual surface for the depth tower
5. Stage 4 plate module (`atlas/stage4.py`) — cross-dataset comparison + EITT bench

Other queued items per [`papers/in_progress/POST_CONFERENCE_ROADMAP_2026-06.md`](papers/in_progress/POST_CONFERENCE_ROADMAP_2026-06.md):

- R port of CNT to v3.1.0 (EngPromo-2)
- Cross-platform reproduction confirmation (independent reproductions of the published hashes on Windows, macOS, Linux × Intel and ARM)
- Lyapunov-block in CNT (new diagnostic per the roadmap §4.1)
- Pairwise entanglement matrix (new diagnostic per the roadmap §3.1)
- Additional concordance documents (line-by-line mapping of pseudocode ↔ Python ↔ R ↔ test)

### 6.3 Known gaps that do NOT block verification

- The R port of CNT is at v3.0.0 while Python is at v3.1.0. The v3.0.0 → v3.1.0 delta is the Helmsman family promotion (already documented in the pseudocode) and the `compute_navigation_2d` block from v3.2.0. **Verifying against the v3.0.0 R port reproduces the v3.0.0 per-field numerical results (Layer 2; not byte-identical to the v3.0.0 Python hash because of Layer 2's per-language canonicalization), not the v3.1.0 numerical results.** Both versions are checkable; the v3.1.0 numerical state is the conference-current target. R v3.1.0 parity is queued as EngPromo-2 per §6.2.
- The `Power Share` field in the v3.1.0 output JSON is reserved (`null`) pending INV-060 promotion. A re-implementation should also produce `null` for this field.
- Stage 4 plate module is `planned`; it does not exist as code yet. Stage 4 output fields in the JSON are present but stub-only.

---

## 7. Reporting discrepancies

First, determine which parity layer the discrepancy is in (§1.5):

- **If per-field numerical values differ at much larger than IEEE-floor (≫ 10⁻¹⁵):** this is a substantive parity discrepancy regardless of canonicalization profile. *This warrants reporting.*
- **If per-field numerical values agree at IEEE-floor but `content_sha256` differs:** this is almost certainly a canonicalization-profile mismatch (Layer 2 or Layer 4 behavior — see §1.5). Check whether your implementation adopts the Python canonicalization profile per Step 6, or whether you are comparing your Python-profile hash against the R reference hash (the two are different by design). This is not necessarily a defect; it may just be a layer-confusion that resolves once profiles are aligned.
- **If both per-field values and hashes match:** there is no discrepancy.

If after layer-disambiguation you still have a substantive numerical discrepancy:

1. **Do not assume the published code is correct.** It might be; it might not be.
2. **Run the determinism tests** in the engine's `tests/` directory against the published Python or R. If those tests pass, the published code is internally consistent at minimum.
3. **Open an issue on the GitHub repository** with: your platform (OS, CPU, language version), the canonical input you ran, the configuration block you used, the per-field numerical comparison output, the canonicalization profile you used, and the hash you computed (so the discrepancy can be classified by layer). **You do not need to share your code unless you wish to.**
4. **Or contact the author directly** at `PeterHiggins@RogueWaveAudio.com`. Discrepancies are taken seriously and triaged under Hs Change Control v1.0 as candidate Discovery Change Packets (DCPs).

The framework's discipline includes accepting that the published code might be wrong. If you find a real discrepancy, the framework benefits — that is exactly the closure-check principle (Theorem 1) applied to its own implementation.

---

## 8. Why this discipline is in the framework

The doctrine that *trust must be earned* came from the original Binaural Test Lab (BTL) measurement programme. Every BTL measurement that has ever been taken is subject to a closure check (`Σ Gᵢ = c = 6.02 dB`). When closure fails, the measurement is wrong, not the theory. The same discipline is applied to the implementation: when your hash differs from the published hash, the implementation is wrong (yours or ours), not the algorithm.

This is the Paired Measurement Doctrine (flagship §4.3) extended to software: *"one curve lies"*. A single measurement is not sufficient; a single implementation is not sufficient. The framework provides four-plus forms (Python + R + pseudocode + specification + anti-specification) and three reference confirmation datasets so that any user can perform their own independent verification. The framework's central claim — that closure on the simplex is a real invariant of compositional systems — is testable by the hash discipline at the implementation layer.

You do not have to trust this repository to use the framework. You only have to trust the mathematics (lemmas, citations, IEEE-floor empirical evidence) and your own re-implementation of the algorithm. *That is the deal.*

---

## 9. Cross-references

| Document | Purpose |
|---|---|
| [`HCI-CNT/engine/CNT_PSEUDOCODE.md`](HCI-CNT/engine/CNT_PSEUDOCODE.md) | CNT v3.1.0 language-agnostic algorithm reference |
| [`HCI-CNQ/engine/CNQ_PSEUDOCODE.md`](HCI-CNQ/engine/CNQ_PSEUDOCODE.md) | CNQ v1.0.0 language-agnostic algorithm reference |
| [`HCI-CNT/engine/ANTI_SPECIFICATION.md`](HCI-CNT/engine/ANTI_SPECIFICATION.md) | What the CNT engine MUST NOT do |
| [`HCI-CNQ/engine/ANTI_SPECIFICATION.md`](HCI-CNQ/engine/ANTI_SPECIFICATION.md) | What the CNQ engine MUST NOT do |
| [`HCI-CNQ/engine/CNQ_SCHEMA.md`](HCI-CNQ/engine/CNQ_SCHEMA.md) | Formal CNQ output schema |
| [`huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json`](huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json) | HUF-STD-002 — the formal I/O specification |
| [`huf-gov/standards/HUF_PUBLICATION_STANDARDS.json`](huf-gov/standards/HUF_PUBLICATION_STANDARDS.json) | HUF-STD-001 — Publication Standards (citation, AI Use Declaration, authorship) |
| [`huf-gov/standards/HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json`](huf-gov/standards/HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json) | HUF-STD-003 — the seven Linear Algebra Foundations of Hˢ |
| [`papers/flagship/GROUND_STATE_AND_TRACTION.md`](papers/flagship/GROUND_STATE_AND_TRACTION.md) v2.2 | The mathematical foundation paper with 8 lemmas + 2 theorems |
| [`ai-refresh/CCTT_QUICKSTART.md`](ai-refresh/CCTT_QUICKSTART.md) | The 30-second orientation for running the framework |
| [`ai-refresh/CCTT_RUNBOOK.md`](ai-refresh/CCTT_RUNBOOK.md) | The 7-phase reproducible runbook |
| [`AI_AGENTS.md`](AI_AGENTS.md) | Operating instructions for AI assistants who engage with the repo (including §1.5 cross-domain partnership context) |
| [`papers/in_progress/POST_CONFERENCE_ROADMAP_2026-06.md`](papers/in_progress/POST_CONFERENCE_ROADMAP_2026-06.md) | Roadmap of queued post-conference work |

---

## 10. Contact

Peter Higgins · Rogue Wave Audio · Binaural Test Lab
Markham, Ontario, Canada

- Business email: `PeterHiggins@RogueWaveAudio.com`
- Repository: [`github.com/PeterHiggins19/higgins-decomposition`](https://github.com/PeterHiggins19/higgins-decomposition)
- Community folder: [`CODA-Association/`](CODA-Association/)
- Conference (June 2026): [`CODA-Association/CODAwork2026/`](CODA-Association/CODAwork2026/)

Open issues on the repository are triaged under Hs Change Control v1.0. Direct email contact is welcomed for discrepancy reports, re-implementation questions, and collaboration proposals.

---

*The instrument reads.   The expert decides.   The hashes carry the receipts.   The vocabulary holds the line.   The AI follows the same protocol.   Same input, same output, always.*
*Trust is earned, not expected.   The framework holds itself to the same standard it holds the apparatus to.*
**The closure check is the test we are using to know whether the measurement is right — and that includes the measurement of our own implementation.**


---

## Addendum — 2026-06-09 (post-publication advancement)

*Non-destructive note (Cowork working tree; not yet git-committed). The content above is unchanged and remains valid as published.*

A new end-to-end verification target now exists: the cited, one-command-reproducible Frielingen-9 demo. The CNQ-tiling reconstruction was demonstrated lossless on real data. The four-form / layered-parity discipline is unchanged.

Since publication the system advanced: Hs/CNT/CNQ was applied to **mudstone chemostratigraphy** as a cited, reproducible demo on real PANGAEA data (`collaborations/geology-wehner/`), and a new concept — **CNQ tiling / "faceted read"** (overlapping exact D=4 charts glued on shared parts reconstruct the full higher-dimensional compositional move **losslessly**: alignment 9e-16, reconstruction 4e-14, overlap proven necessary) — was tested. **Engine, schemas, and canonical numbers are UNCHANGED**; this is a documentation / application / concept advance. Gluing maths CONFIRMED; scientific value on real high-D data TO TEST. Full current picture: `collaborations/geology-wehner/00_EXECUTIVE_OVERVIEW.md`.
