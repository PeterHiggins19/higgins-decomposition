# QAM space radio with Hˢ in the loop — a sandbox, measured

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-23. "Assume
nothing, test everything." A real end-to-end 16-QAM / AWGN link simulator, **validated against textbook BER
first**, then Hˢ dropped in to see what actually changes. It surfaced a genuine surprise and a clean honest
negative. Receipt `f502c15d…`. Honest-broker tiered; nothing posted; Peter is the sole gate.*

---

## 0. The sanity gate (assume nothing)

Before any Hˢ claim, the simulated 16-QAM BER over AWGN is checked against the closed-form curve. It matches:

| Eb/N0 | simulated BER | theory BER |
|---:|---:|---:|
| 4 dB | 0.0581 | 0.0586 |
| 8 dB | 0.0090 | 0.0093 |
| 12 dB | 0.00013 | 0.00014 |

The channel model is trustworthy — the rest is measured on a correct link.

## 1. The setup

Payload: real telemetry — 300 energy-mix compositions (D=8). Same modulation (16-QAM), same channel (AWGN),
same power. Three **source/representation** paths compared by delivered fidelity (mean Aitchison RMSE):

- **baseline** — raw shares, 10-bit uniform, no FEC (what a naive telemetry encoder sends).
- **HS-A** — the composition in **ILR (log-ratio) coordinates**, 10-bit, no FEC (isolates representation effect).
- **HS-B** — ILR top-3 (effective-dimension) compressed **2.67×** + repetition FEC at **equal airtime**.

## 2. What the channel delivered (mean Aitchison error vs Eb/N0 — lower is better)

| Eb/N0 | baseline (raw shares) | **HS-A (ILR, no FEC)** | HS-B (compress + FEC) |
|---:|---:|---:|---:|
| 3 dB | 14.29 | **6.53** | 6.61 |
| 5 dB | 13.11 | **5.15** | 5.90 |
| 7 dB | 11.93 | **3.49** | 5.12 |
| 9 dB | 10.60 | **1.67** | 4.85 |
| 12 dB | 10.14 | **0.015** | 4.77 |

## 3. The surprise (the real finding) — geometry, not FEC

The dominant effect is **not** error-correction and **not** compression — it is the **representation**.
Encoding the telemetry in compositional **ILR (log-ratio)** coordinates instead of raw shares makes the
delivered payload **dramatically more robust to channel bit errors**, at identical modulation, power, and bit
budget: HS-A beats the raw-share baseline by **~2× at 3 dB and ~700× at 12 dB**, and it **degrades gracefully**
with SNR while the baseline stays catastrophically wrong even at 12 dB.

*Why:* a corrupted raw share blows up through the closure-and-log (a tiny true share flipped to large is a
huge Aitchison error — one bad bit destroys a sample); a corrupted **log-ratio** coordinate perturbs the
composition by a **bounded** amount. The same compositional geometry that helped compression also makes the
link error-resilient. **This is a genuine, measured benefit of putting Hˢ's geometry in the radio — at the
source layer, leaving QAM itself untouched.**

## 4. The honest negative (the sandbox correcting intuition)

The "obvious" move — compress hard, spend the saved bits on FEC (HS-B) — was **worse than the simple robust
representation (HS-A)** at every SNR above 3 dB. Dropping 4 of 7 ILR coordinates introduced a reconstruction
floor (~4.8) that the repetition FEC could not buy back. **Lesson the data taught:** at usable SNR, the win is
the *robust representation kept whole*, not aggressive lossy compression — compress only when airtime, not
fidelity, is the binding constraint. (A stronger FEC than repetition, and gentler compression, is the obvious
next experiment.)

## 5. What this says about "making QAM space radio better with Hˢ"

- **Hˢ does not change QAM's symbol-error rate** — the modulation and channel are identical (the sanity gate
  proves it). No capacity claim.
- **Hˢ helps at the source/representation + integrity layer**, and the help is large and measured: a
  compositional payload survives the channel far better in ILR coordinates, and each frame can carry a content
  hash for built-in integrity. For *telemetry that is compositional* — power budgets, fleet-health mixes,
  spectral occupancy, gas/material fractions — that is a real link-level improvement, stackable on top of
  whatever modulation and FEC the radio already uses.
- **The honest pitch:** "Hˢ is an error-graceful, self-verifying source layer for compositional telemetry on a
  QAM link" — not "a better modulation."

## 6. Tiers

- **T1 (measured):** the validated BER; the ~2×–700× representation-robustness of ILR vs raw shares; the
  HS-B negative; receipt `f502c15d…`.
- **T2 (reasoned):** that this extends to other compositional telemetry classes and stacks with real FEC /
  coded modulation; the structured-constellation (unitary/rotation) idea for non-coherent space links.
- **T3 (open / to earn):** any specific dB link-budget gain on real hardware; the differential-unitary
  constellation built from the SO(n) generator (named, not yet simulated). **Rejected:** any claim that Hˢ
  changes QAM capacity or beats the channel limit.

*Reproduce: `python3 qam_hs_link.py`. Cross-refs: `../compression_benchmark_2026-06/RESULTS_compression.md`,
`../../papers/frontier/HS_ENGINE_MORPHOLOGY_AND_CODEC.md` (§6 application frontier),
`../son_generator_2026-06/son_exact_generator.py` (the unitary-constellation generator). Peter is the sole gate.*

*Proof & Honesty Standard — numbers cited-or-fenced · math proven + receipted · value shown · experts decide.*
