# CodaWork 2026 — EMBER 8-country corpus headline comparison

**Engines:** CNT v3.0.0 + CNQ v2.0.0 (push #32). Both engines run on the 8-country EMBER pipeline-ready dataset (Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil, Other Renewables, Solar, Wind; D = 9; coherent range **2001-2025**, T = 25 years per country).

## Coherent range manifest (CRD-1.0)

| Field | Value |
|---|---|
| Coherent range | **2001-2025** |
| T_set | **25** |
| Members | USA, CHN, DEU, FRA, GBR, IND, JPN, AUS, WLD |
| Start-limiting member(s) | USA |
| End-limiting member(s) | (all share) |
| Carriers dropped | (none) |
| Range policy | `coherent` |

*Per [CRD-1.0](../../../docs/COHERENT_RANGE_DOCTRINE.md): every member is truncated to the intersection of all members' time ranges before any diagnostic is computed. The shortest-coverage member sets the binding window for the entire set. "Start-limiting" identifies the carrier(s) whose native data begins LATER than the rest (pinning the corpus's first year); "end-limiting" identifies the carrier(s) whose native data ends EARLIER than the rest. "(all share)" means no unique binder — every member naturally aligns at that endpoint.*

## Headline diagnostics across all countries

| Country | T | termination | IR class | M^2=I residual | period | stability | A | zeta | flips |
|---|---|---|---|---|---|---|---|---|---|
| USA (United States) | 25 | EXHAUSTED | OVERDAMPED_EXTREME | 3.30e-13 | — | 0.000 | 9.688 | -0.084 | 8 |
| CHN (China) | 25 | EXHAUSTED | LIGHTLY_DAMPED | 1.11e-16 | — | 0.000 | 0.894 | +0.038 | 12 |
| DEU (Germany) | 25 | EXHAUSTED | OVERDAMPED_EXTREME | 4.41e-14 | — | 0.000 | 3.092 | -0.014 | 13 |
| FRA (France) | 25 | EXHAUSTED | MODERATELY_DAMPED | 1.11e-16 | — | 0.000 | 0.290 | -0.047 | 12 |
| GBR (United Kingdom) | 25 | EXHAUSTED | OVERDAMPED_EXTREME | 1.71e-14 | — | 0.000 | 7.638 | -0.008 | 14 |
| IND (India) | 25 | EXHAUSTED | LIGHTLY_DAMPED | 1.11e-16 | — | 0.000 | 0.555 | +0.017 | 14 |
| JPN (Japan) | 25 | EXHAUSTED | LIGHTLY_DAMPED | 1.67e-16 | — | 0.000 | 7.131 | +0.019 | 17 |
| AUS (Australia) | 25 | EXHAUSTED | LIGHTLY_DAMPED | 3.33e-16 | — | 0.000 | 1.408 | +0.020 | 8 |
| WLD (World) | 25 | EXHAUSTED | LIGHTLY_DAMPED | 5.55e-17 | — | 0.000 | 0.127 | +0.002 | 3 |

## Determinism + numerical anchors

- **M^2 = I metric involution verified at IEEE floor (< 1e-10) on 9 of 9 countries.**
  - All 9 countries pass. Worst residual across the corpus: **3.300e-13**.
- **CNQ dimension policy:** all countries are D = 9 -> `reduced_or_projected` (D=5..15 reduced-projection branch).
  - Native twin-quaternion factoring (D = 8) and quad-quaternion factoring (D = 16) are not exercised by the EMBER corpus; these are reserved for D-matched datasets when they arrive.

## Per-country canonical hashes (engine-independence policy verified)

| Country | cnt_content_sha256 | cnq_content_sha256 |
|---|---|---|
| USA | `c03cf346c68658e0...` | `82657a8f777ce657...` |
| CHN | `89499d8014926a70...` | `796ef6f178617526...` |
| DEU | `030e28a304f53767...` | `3329a9b54b7e0ce8...` |
| FRA | `2c91984954c06a9b...` | `91db85d3408c5050...` |
| GBR | `e77f67ede57a5bdc...` | `3075b34012510e9b...` |
| IND | `a19b8d222cdb260c...` | `1d5e64c1363c46eb...` |
| JPN | `2fb45dd99cc2e077...` | `18f3e452e013314b...` |
| AUS | `22e1aa4c284617cf...` | `5f6ac234ae952a25...` |
| WLD | `b10c0b62979d160f...` | `4f4aa51ade020c76...` |

Each country produces two unrelated hashes — CNT and CNQ canonical hashes are independent by design (push #32 engine-independence policy).

## Comparison vs v2.0.4 (legacy)

v2.0.4 baseline outputs available for **8** of 9 countries at `HCI-CNT/experiments/codawork2026/`.
Per-country comparison detail in each `<country>/ADVANCED_ANALYSIS.md`.

---

## Reading these reports

Each country folder contains two reports for two audiences:

- **`STAGE_1_REPORT.md`** — pure CoDa community vocabulary (closure, CLR, ILR, variation matrix tau_ij, carrier-pair Pearson r, section atlas). This is what a CoDa-community reviewer reads to verify that the math fits their framework. **Stage 1 = pure CoDa.**

- **`ADVANCED_ANALYSIS.md`** — full Hs-extension stack (kappa^HS metric tensor, s_j sensitivity, depth tower, P2 attractor fit, helmsman family, IR classification) plus the CNQ v2 quaternion view (bearing trajectory, radial trajectory, dimension policy). **Full CNQ = the more advanced option.**

The two-document structure makes the positioning unambiguous: Stage 1 is a clean entry point in the CoDa community's own vocabulary; Advanced is the differentiator that justifies the framework's existence beyond standard CoDa.

*Generated for CodaWork 2026 (June) by `run_ember_corpus.py` (CRD-1.0 range policy: `coherent`).*