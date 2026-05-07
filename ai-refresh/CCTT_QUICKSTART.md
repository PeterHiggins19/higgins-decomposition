# CCTT Quickstart — One-page intro

**CCTT** = **C**NT **C**ompositional **T**ensor **T**rain. It is a 7-phase
protocol that takes any compositional dataset and produces a CNT-grade
analysis with full provenance — even if you have never heard of Aitchison
geometry.

You can run CCTT in either of two modes. The protocol is identical in both;
the only difference is who does the keystrokes.

| Mode | Who executes the steps | When to choose it |
|---|---|---|
| **User-mode** | You, following the runbook | You want to learn the system, you do not have an AI assistant available, or you prefer hands-on control |
| **User + AI-mode** | An AI assistant (Claude, ChatGPT, Gemini, in-house) executes the steps; you confirm at every gate | You want speed, you have many datasets, or you want the AI's pattern-matching against the 13-adapter registry |

In both modes, the *user governs*. The user provides the data, confirms the
column-to-carrier mapping, and decides whether to ship a result. The AI (when
present) is an assistant that follows the same protocol the user would.

---

## What you get back

Identical in either mode:

- A **canonical CNT JSON** — the scientific result, hash-verifiable.
- A **Stage 1 page** (always) plus Stage 2 / Stage 3 / Stage 4 / spectrum /
  projector pages chosen automatically based on what your data supports.
- A **disclosed pre-parser adapter** — if your dataset is novel, one is built
  and its source is open for review.
- A **JOURNAL.md** audit trail with full provenance.
- A **pipeline manifest** listing every output with its SHA-256.

Every artefact is hash-chained, so an auditor can re-run a year later and
prove nothing changed.

---

## What you provide

A compositional dataset — anything where the rows sum to a constant
(percentages, fractions, shares of a budget, mass fractions of oxides, …).
CSV, XLSX, TSV, JSON. Plus, ideally, one sentence about what it is.

Examples that work:

| Dataset | What it is | Adapter |
|---|---|---|
| EMBER country energy mix | yearly electricity-source shares | built-in |
| Geochemistry oxide compositions | major-oxide mass fractions per region | built-in |
| FAO irrigation methods | irrigated-area share by method per country | built-in |
| BackBlaze drive failures | failure-mode shares per drive model | built-in |
| Markham city budget | departmental spending shares per year | built-in |
| **Your dataset here** | any composition that sums to a constant | new adapter generated, fully disclosed |

---

## The 7-phase loop (the same in both modes)

1. **Diagnose data** — read the file, identify label vs carriers, count T and D, decide temporal/categorical.
2. **Select or generate the adapter** — match the dataset signature against the built-in registry (13 adapters); if no match, generate a new one with full disclosure.
3. **Run the engine** — `python3 HCI-CNT/engine/cnt.py <input> -o <output> --ordering-method <method>`.
4. **Choose the output suite** — Stage 1 always; Stage 2 if T≥3; Stage 3 if T≥5 and IR class isn't D2_DEGENERATE; Stage 4 + spectrum + projector only for multi-dataset jobs.
5. **Render the pipeline** — call the chosen modules from `HCI-CNT/mission_command/modules.py` or run the orchestrator end-to-end.
6. **Self-verify (the gate)** — schema validates, re-run reproduces the SHA, source-hash matches, corpus match (if applicable). All four must pass.
7. **Present and journal** — write JOURNAL.md with full provenance, hand back artefacts with their hashes.

The detail of each phase, with worked example and decision rules, lives in
[`CCTT_RUNBOOK.md`](CCTT_RUNBOOK.md).

---

## What you confirm at the phase 2 gate

The protocol pauses here regardless of mode. You see a confirmation message:

> Here's what I found:
>
> - **Carriers (D=10):** SiO2, TiO2, Al2O3, FeO, CaO, MgO, MnO, K2O, Na2O, P2O5
> - **Records (T=8):** by region — Central Slave Province, Maniitsoq & Sarfartoq, …
> - **Labels:** named categories (regions), so this will be non-temporal, by-label.
> - **Adapter:** matches existing `bin_tappe_and_qin.py` — no new code needed.
> - **Imputation:** none — all values strictly positive.
>
> Is this what you intended?

In **User-mode**, you are reading this from the runbook and writing the answer
in your own working notes. In **User + AI-mode**, the AI typed the message and
is waiting for your reply. Either way, you say "yes" or correct the bit that
looks wrong, and the rest is automatic.

---

## What you do *not* need to know

In either mode:

- Aitchison geometry
- ILR-Helmert basis construction
- The atan2 simplification
- The 8-class IR taxonomy
- Schema 2.1.0 internals
- How the determinism gate works internally

The protocol handles all of that. You only need to recognise your own data.

---

## What you *do* need to think about

- Which columns are carriers vs labels (the protocol guesses; you confirm).
- Whether the labels are temporal (years, dates) or categorical (countries, species).
- Whether your zeros are *true* zeros or *below detection limit* zeros — they need different imputation.
- Whether your carriers all share units (TWh and TWh, or mass% and mass%) or are mixed.

---

## Pilot proof

CCTT v1.0 was acceptance-tested against `geochem_tappe_kim1` — 8 regions × 10
oxides of kimberlite Group-1 bulk-rock compositions. A Claude session given
nothing but the spec, the runbook, and the raw CSV reproduced the canonical
`content_sha256` byte-for-byte:

```
expected: 707034ecc512c29df57e73fcb68466e10611bc63cc3c4d88a4b2152ff39e4063
got:      707034ecc512c29df57e73fcb68466e10611bc63cc3c4d88a4b2152ff39e4063
PASS
```

A user following the same runbook produces the same hash. Full pilot details:
[`CCTT_PILOT_REPORT.md`](CCTT_PILOT_REPORT.md).

---

## How to start, by mode

### User-mode

1. Open [`CCTT_RUNBOOK.md`](CCTT_RUNBOOK.md) on one screen, your terminal on the other.
2. Walk the 7 phases against your dataset. Each phase has explicit decision rules and explicit stop conditions.
3. At phase 2, write the confirmation message in a notebook or scratch file; review it for correctness before moving to phase 3.
4. At phase 6, run the four checks; all must pass before phase 7.
5. Write the JOURNAL.md.

The runbook is short enough to walk in one sitting on a small dataset (15–30
minutes for a fresh user the first time, 5–10 minutes once you have done it
twice).

### User + AI-mode

Paste this into any new chat with Claude, ChatGPT, Gemini, or another AI
assistant that has access to this repo:

> I want to use **CCTT v1.0** to analyse the compositional dataset attached.
> Please read [`ai-refresh/CCTT_RUNBOOK.md`](CCTT_RUNBOOK.md) and follow the
> 7-phase loop. Echo your phase-2 confirmation message before running the
> engine. Stop and ask me before any decision you can't make from the
> instructions alone.

The AI will read the runbook, diagnose your data, and come back with the
confirmation message. From there, it's automatic.

---

## Files in the CCTT family

| File | Purpose |
|---|---|
| [`CCTT_BUILD_INSTRUCTION_v1.0.json`](CCTT_BUILD_INSTRUCTION_v1.0.json) | Machine-readable spec (the AI consumes this) |
| [`CCTT_RUNBOOK.md`](CCTT_RUNBOOK.md) | Narrative protocol (you read this in either mode) |
| [`CCTT_PILOT_REPORT.md`](CCTT_PILOT_REPORT.md) | Acceptance test result — bit-for-bit reproduction proof |
| [`CCTT_QUICKSTART.md`](CCTT_QUICKSTART.md) | This page |
| `HS_ADMIN.json` → `ai_helpers.cctt` | Registration block — future AI sessions discover CCTT here |

---

## Why this matters

Compositional data analysis is powerful but most researchers in fields that
*generate* compositional data (ecology, urban planning, forensic accounting,
medicine, climate science, bench chemistry) have never seen the toolkit.
CCTT closes that gap two ways at once: a researcher who wants to learn the
system can walk the runbook by hand, and the same researcher who wants to go
fast can have an AI assistant execute it. The protocol is the protocol.

The hashes mean the result is reproducible. The disclosed adapter means it's
auditable. The JOURNAL means it's reviewable. None of this requires trust in
any particular executor — it requires only that the engine still computes
deterministically, which the 25-experiment corpus continuously verifies.

The instrument reads. The expert decides. The hashes carry the receipts. CCTT
makes that promise available to everyone — by hand or with help.
