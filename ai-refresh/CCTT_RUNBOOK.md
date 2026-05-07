# CCTT Runbook — CNT Compositional Tensor Train

**Companion to** [`CCTT_BUILD_INSTRUCTION_v1.0.json`](CCTT_BUILD_INSTRUCTION_v1.0.json)
**Audience:** any user — researcher walking the steps by hand, or an AI assistant (Claude, ChatGPT, Gemini, in-house agent) executing on the user's behalf. Same protocol either way.
**Engine target:** CNT 2.0.4 / Schema 2.1.0 / Output Doctrine v1.0.1

> The instrument reads. The expert decides. The hashes carry the receipts.
> CCTT is the same disciplined practitioner protocol whether a human or an AI
> executes the keystrokes — and the hashes verify the result either way.

## User-mode vs User + AI-mode

CCTT is a single protocol with two execution modes. In **User-mode** the
researcher walks the seven phases by hand, reading this runbook on one screen
and a terminal on the other. In **User + AI-mode** the user asks an AI
assistant to execute the same seven phases and confirms the result at every
gate. The AI is never autonomous — at the phase 2 confirmation gate and at
the phase 6 four-check gate, the user always governs. The protocol does not
distinguish between modes because the gates do not. A SHA-256 produced by a
human keystroke and a SHA-256 produced by an AI tool call have the same
audit weight. Pick the mode that fits the moment; switch mid-project if you
want.

---

## What CCTT is, in one paragraph

A researcher hands you a compositional dataset (energy mix, geochemical oxides,
budget shares, market portfolios, anything that sums to a constant). You — the
AI — diagnose the data, build or pick the right pre-parser, run the CNT engine,
choose the correct output pages, render them, hash-verify the result, and hand
back a journalled audit trail. The user does not need to know what an Aitchison
closure is. You do, and this runbook tells you how.

---

## How to use this runbook

If you are a fresh AI session that has never seen CNT before, read these files
in order before you start (about 30 minutes of context):

1. This runbook (you're reading it).
2. [`HS_MACHINE_MANIFEST.json`](HS_MACHINE_MANIFEST.json) — the system pointer block.
3. [`CCTT_BUILD_INSTRUCTION_v1.0.json`](CCTT_BUILD_INSTRUCTION_v1.0.json) — the machine-form spec; this runbook is its narrative twin.
4. [`HCI-CNT/handbook/VOLUME_2_PRACTITIONER_AND_OPERATIONS.md`](../HCI-CNT/handbook/VOLUME_2_PRACTITIONER_AND_OPERATIONS.md) — Part C (adapters) and Part E (walkthrough).

Then come back here.

---

## The seven-phase loop

### Phase 1 — Diagnose the data (no engine calls)

Open the file. Read the first 20 rows and the last 5. Identify:

- **The label column** — usually the first non-numeric column. Could be years,
  country names, species, time stamps, file names.
- **The carrier columns** — numeric columns that aren't units, sources,
  metadata, or commentary.
- **T** — number of data rows after dropping junk.
- **D** — number of carrier columns.
- **The temporal question** — do the labels carry time meaning (years, dates,
  monotonic indices)? If yes, `is_temporal = true` and `ordering_method =
  "by-time"`. If they're named categories (countries, regions, species),
  `is_temporal = false` and `ordering_method = "by-label"`.
- **The positivity question** — is every carrier value strictly positive? Zeros
  and NaNs need imputation in phase 2 before the engine sees them.
- **The unit question** — are the carriers in the same units (TWh and TWh, or
  mass percent and mass percent)? If they're mixed (TWh and GWh, or mass percent
  and mole percent), the adapter must normalise before the engine.

Write a one-paragraph plain-English description of what the dataset is. You'll
echo this back to the user at the end of phase 2 for confirmation.

### Phase 2 — Select or generate the adapter

This is the most domain-sensitive step. Two branches:

**Branch A — match an existing adapter.** The 13 built-in adapters live at
[`HCI-CNT/adapters/`](../HCI-CNT/adapters/). If your dataset is EMBER energy,
geochemical oxides, FAO irrigation, BackBlaze drives, S&P sectors, IIASA
scenarios, NGFS, ESA Planck cosmic, or one of the others listed in the
adapter README, the matching adapter already exists. Use it directly.

**Branch B — generate a new adapter.** Read
[`bin_tappe_and_qin.py`](../HCI-CNT/adapters/bin_tappe_and_qin.py) first as
the gold-standard template — that's a clean, fully-disclosed real-data
adapter. Then write yours following the eight-step skeleton in the JSON
spec. The non-negotiables:

1. Source disclosure header — provenance, citation, retrieval date, original SHA.
2. Carrier mapping — which raw column became which carrier, with units.
3. Transformation log — closure, imputation, aggregation, dropped rows, all logged.
4. Output: `<name>_input.csv` (label + D carriers, T rows, every cell positive).
5. Output: `<name>_disclosure.json` with the same data in machine form.
6. Print SHA-256 of `<name>_input.csv` on stdout so you can record it.

**Imputation choice.** When the user has zeros, ask: "are these *true* zeros
(the carrier is genuinely absent) or *below detection limit* zeros (the carrier
is present but unmeasured)?" The answer changes the choice. True zeros need a
zero-replacement strategy that's small enough not to distort the geometry but
large enough to survive log-ratio. Multiplicative imputation with a multiplier
of 0.65×(detection limit) is the CoDa-community standard; document whatever
you choose.

**THE USER CONFIRMATION GATE.** Before phase 3, you MUST write back to the
user with a structured confirmation message:

> I've read your data. Here's what I found:
>
> - **Carriers (D=10):** SiO2, TiO2, Al2O3, FeO, CaO, MgO, MnO, K2O, Na2O, P2O5
> - **Records (T=8):** by region — Central Slave Province Lac de…, Maniitsoq & Sarfartoq, …, southern Africa
> - **Labels:** named categories (regions), so I'll treat this as non-temporal
>   and order by label.
> - **Adapter:** matches the existing `bin_tappe_and_qin.py`, no new code needed.
> - **Imputation:** none needed — all values strictly positive.
>
> Is this what you intended? Reply 'yes' to proceed, or correct anything I
> misread.

Wait for confirmation. Do not silently move on.

### Phase 3 — Run the engine

The engine is `HCI-CNT/engine/cnt.py`. The CLI:

```bash
python3 HCI-CNT/engine/cnt.py <input>.csv -o <output>.json --ordering-method by-label
```

Add `--temporal` if `is_temporal=true`. Add `--ordering-caveat 'note'` if
you're doing anything non-default and want the rationale recorded in the JSON
metadata.

The engine prints the `content_sha256` and signature on its last lines of
stdout — capture them. Then load the JSON and verify it has the seven
top-level keys: `metadata`, `input`, `tensor`, `stages`, `bridges`, `depth`,
`diagnostics`. Extract:

- `metadata.engine_version` — must read 2.0.4 or whatever the current canon is.
  If it doesn't, STOP — there's a schema mismatch.
- `metadata.schema_version` — must read 2.1.0.
- `input.source_file_sha256` — must equal the byte-hash of your input CSV.
- `diagnostics.content_sha256` — this is THE GATE. Record it.
- `diagnostics.higgins_extensions.IR_class` — the dynamics classification.
- `diagnostics.higgins_extensions.amplitude_A` — the period-2 attractor amplitude.

### Phase 4 — Choose the output suite

Conservative defaults; render-more-on-request:

- **Stage 1 (always)** — the orthogonal triplet plate. One per dataset.
- **Stage 2 (when T ≥ 3)** — the 19-plate Order-2 atlas with all CoDa-standard
  views (evolution of proportions, ternary triplets, balance-dendrogram, SBP
  table, scree, biplot, more).
- **Stage 3 (when T ≥ 5 and IR class isn't D2_DEGENERATE)** — depth tower,
  IR taxonomy view, attractor analysis.
- **Stage 4 (only when the user has 2+ datasets sharing carriers)** —
  cross-dataset comparison.
- **Spectrum + projector (multi-trajectory data)** — optional but
  visually impactful when there are multiple trajectories to overlay.

If the user explicitly asks for "everything", render Stage 1 + Stage 2; mention
that Stage 3 is gated on T and Stage 4 on having more than one dataset.

### Phase 5 — Render the pipeline

For a single experiment, call each module from
[`HCI-CNT/mission_command/modules.py`](../HCI-CNT/mission_command/modules.py)
with the engine JSON as input.

For a project of multiple experiments, write a project block into
`HCI-CNT/mission_command/master_control.json` (use one of the existing
projects as a template — `codawork2026_geochem` is a good simple one) then
call:

```bash
python3 HCI-CNT/mission_command/mission_command.py --project <project_name>
```

Capture the file paths of every artefact (PDFs, JSONs, HTML) into a pipeline
manifest. Hash each one.

### Phase 6 — Self-verify

This is the gate. Four checks, all must pass:

1. **Schema validation:** `python3 HCI-CNT/tools/validate_cnt_schema.py
   <name>_cnt.json` — exit 0, "schema 2.1.0 OK".
2. **Re-run determinism:** call the engine a second time on the same input;
   compare `diagnostics.content_sha256`. Must be byte-equal.
3. **Source-hash consistency:** `input.source_file_sha256` in the JSON must
   equal `sha256sum <name>_input.csv`. Byte-equal.
4. **Corpus match (when applicable):** if this experiment ID exists in
   [`HCI-CNT/experiments/INDEX.json`](../HCI-CNT/experiments/INDEX.json),
   `diagnostics.content_sha256` must equal `INDEX[id].content_sha256`. If they
   differ, STOP and surface both SHAs to the user with a line-by-line diff of
   the input CSVs. The engine is deterministic — any drift is a real signal.

If any check fails, do not ship. Write the failure into the JOURNAL with full
reproduction steps.

### Phase 7 — Present and journal

Hand back:

- `<name>_cnt.json` — the canonical engine output.
- `<name>_input.csv` — the engine-ready input CSV.
- `<name>_<adapter>.py` + `<name>_disclosure.json` — if you generated a new
  adapter.
- Stage 1 PDF + (Stage 2/3/4 PDFs as chosen).
- `<name>_pipeline_manifest.json` — file list with SHA-256s, engine signature,
  CCTT version, AI model, gate results.
- `<name>_JOURNAL.md` — auto-written audit trail using the template at
  [`HCI-CNT/experiments/<any-id>/JOURNAL.md`](../HCI-CNT/experiments/) as the
  reference shape. Include an **AI build provenance** block at the bottom with:
  CCTT version, AI model + version, the user prompt that triggered the build,
  the user's confirmation message at the phase 2 gate, all four gate results
  from phase 6.

---

## What you must do, what you must not do

**Must do.**

- Read the three handbook volumes before generating a new adapter.
- Echo the proposed `(T, D, ordering, carriers)` to the user and wait for
  confirmation before phase 3.
- Hash-check at every gate; report mismatches verbatim.
- Write the JOURNAL with every run.
- Disclose every transformation in the adapter source.

**Must not do.**

- Modify the canonical engine (`cnt.py` / `cnt.R`) — schema and signature are locked.
- Modify the determinism gate corpus
  ([`HCI-CNT/experiments/INDEX.json`](../HCI-CNT/experiments/INDEX.json))
  without explicit user authorisation.
- Push to git or modify the canonical local repo — you are working in the
  Cowork mirror only; see
  [`HS_MACHINE_MANIFEST.json`](HS_MACHINE_MANIFEST.json) →
  `fault_tolerance_dual_folder_method`.
- Skip the user-confirmation gate at the end of phase 2.
- Ship a result whose phase-6 checks did not all pass.
- Invent carrier names or column meanings — when ambiguous, ASK.

---

## Worked example — the v0.1 pilot on `geochem_tappe_kim1`

This is the acceptance test for CCTT v1.0. The dataset is an 8-row × 10-oxide
geochemistry composition (kimberlite Group-1 bulk rocks, binned by country/region).

**Phase 1.** Open the CSV at
[`experiments/Hs-05_Geochemistry/region_binning/tappe_kim1_by_country_barycenters.csv`](../experiments/Hs-05_Geochemistry/region_binning/tappe_kim1_by_country_barycenters.csv).
First column is `Country_Region`, ten following columns are `SiO2, TiO2, Al2O3,
FeO, CaO, MgO, MnO, K2O, Na2O, P2O5`. T=8, D=10. All values strictly positive.
Labels are named regions — non-temporal, by-label.

**Phase 2.** Match against the adapter registry: this dataset was generated by
[`bin_tappe_and_qin.py`](../HCI-CNT/adapters/bin_tappe_and_qin.py) (already
disclosed). Echo confirmation to user. User confirms.

**Phase 3.** Run:

```bash
python3 HCI-CNT/engine/cnt.py \
  experiments/Hs-05_Geochemistry/region_binning/tappe_kim1_by_country_barycenters.csv \
  -o /tmp/cctt_pilot_tappe.json \
  --ordering-method by-label
```

Engine prints `content_sha256: 707034ecc512c29d…` on stdout. Open the JSON.
Verify all 7 top-level keys present. `metadata.engine_version=2.0.4`,
`metadata.schema_version=2.1.0`. `diagnostics.content_sha256 =
707034ecc512c29df57e73fcb68466e10611bc63cc3c4d88a4b2152ff39e4063`.

**Phase 4.** T=8 ≥ 5, IR class is `CRITICALLY_DAMPED` (not D2_DEGENERATE) — so
Stage 1, Stage 2, Stage 3 are all in scope. No second dataset to compare against,
so no Stage 4. No multi-trajectory data, so no spectrum or projector.

**Phase 5.** Call Stage 1 + Stage 2 + Stage 3 modules. Capture artefact paths.

**Phase 6.** All four gate checks pass. The corpus-match check is decisive: the
canonical INDEX records `content_sha256 =
707034ecc512c29df57e73fcb68466e10611bc63cc3c4d88a4b2152ff39e4063` for
`geochem_tappe_kim1`. Our regenerated value is byte-equal. ✓

**Phase 7.** Write JOURNAL, hand artefacts back to user. The pilot result is
recorded in [`CCTT_PILOT_REPORT.md`](CCTT_PILOT_REPORT.md).

---

## Failure modes and recovery

**Engine returns non-zero.** Most often: missing `--ordering-method` flag, or
input CSV with negative/zero values. Capture stderr verbatim, surface to user.
Do not retry with a different flag silently — the choice of ordering method is
analytically meaningful.

**`content_sha256` doesn't match the corpus.** The engine is deterministic, so
this means either (a) the input CSV changed (compare byte-by-byte with the
canonical) or (b) the engine version changed (check `metadata.engine_version`).
Surface both SHAs to the user; do not "fix" silently.

**Schema validator fails.** Schema 2.1.0 is locked; if the engine produced
JSON that doesn't validate, you have a real bug. Read the validator's error,
quote it to the user, then check whether you're calling the right engine
binary.

**User says the adapter mapping is wrong at the phase 2 gate.** Apologise,
ask which column was misidentified, regenerate the adapter, re-echo the
confirmation message. Do not push past this gate without a clean "yes".

**Mission Command project block is missing for a multi-experiment job.** Write
one as a temporary project; copy the structure of `codawork2026_geochem` from
[`master_control.json`](../HCI-CNT/mission_command/master_control.json). Do
not modify the existing project blocks.

---

## What this protects the user from

A non-expert researcher in (say) urban planning, forensic accounting, or
ecology can hand you a CSV of departmental budget shares or species abundances
and get back a CNT-grade analysis with full provenance — without having read a
single page of Aitchison or Egozcue. They get to ask the questions; CCTT
handles the geometry.

The hashes mean an auditor can re-run the pipeline a year later and prove
bit-for-bit that nothing changed. The disclosed adapter means another
researcher can reproduce the result on their own machine. The JOURNAL means a
referee can see what was done and what was decided. None of this requires
trust in the AI — it requires only that the engine still computes
deterministically, which the 25-experiment corpus continuously verifies.

---

## CCTT and the dual-folder fault-tolerance protocol

CCTT lives in the Cowork mirror at
`D:\HUF_Research\Claude CoWorker\Current-Repo\Hs\ai-refresh\`. The canonical
repo is separate; Peter syncs the mirror to the canonical repo before each
push. See [`HS_MACHINE_MANIFEST.json`](HS_MACHINE_MANIFEST.json) →
`fault_tolerance_dual_folder_method` for the full protocol.

If you (the AI) are reading this in a fresh Cowork session, you may write
freely into the mirror. You may NOT push to git, modify the canonical local
repo, or assume the mirror is authoritative for verified pushes. After Peter
syncs and a `Validate Repository #N` workflow goes green on
[origin/main](https://github.com/PeterHiggins19/higgins-decomposition), the
remote becomes the source of truth.

---

## Versioning

| Version | Date | Notes |
|---|---|---|
| 1.0.0 | 2026-05-06 | Initial spec — 7-phase loop, 13-adapter registry, pilot on `geochem_tappe_kim1`. |

Future planned hooks (v1.1+): structured Q&A dialog at phase 2, auto-generated
adapter unit tests, first-class XLSX/JSON ingestion, multi-dataset orchestration
scaffold. See `extension_hooks` in [`CCTT_BUILD_INSTRUCTION_v1.0.json`](CCTT_BUILD_INSTRUCTION_v1.0.json).

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
