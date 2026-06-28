# Compositional system — specifications (datasheet)

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-25. The full
specification sheet of the compositional system, **every line measured** — this session's components run
fresh in one consolidated harness (`system_specs.py`, deterministic-specs receipt `dbe4690effd6d2f5`), the
established results cited from past testing with their receipts, the character read from the Compositional
Character Space. Impressive where true, **fenced where not** — honest-broker throughout. Peter is the sole
gate; nothing posted.*

---

## 1 · Determinism & exactness

| spec | value | tier | source |
|---|---|---|---|
| determinism (same input → bit-identical output + hash) | **yes** | T1 | `dbe4690e` |
| clr ⇄ composition round-trip residual | **8.3×10⁻¹⁷** | T1 | `dbe4690e` |
| common-mode rejection — exact `clr(g·x)=clr(x)` | **8.9×10⁻¹⁶** | T1 | `dbe4690e` |
| common-mode rejection — anchor (26.7 dB swing) | **313 dB** (resid 8.9×10⁻¹⁶) | T1 | `d8c21c70` |
| coherence law `−10·log₁₀(1−ρ)` | ρ=0.9→**10 dB** · 0.99→**20 dB** · 0.999→**30 dB** | T1 | `dbe4690e` |
| exact quaternion / SO(3) reconstruction | residual **1.1–4.4×10⁻¹⁶** (≈2× machine ε) | T1 | past (P1) |
| exactness boundary | **Hurwitz** — exact only at D = 1, 2, 4, 8 (ℝ,ℂ,ℍ,𝕆) | T1 | past |
| EITT timescale invariance | **0.17%** over a 341:1 decimation | T1 | `d8c21c70` |

## 2 · Codec & storage (8-bit form)

| spec | value | tier | note |
|---|---|---|---|
| 7-bit codec fidelity **in clr** (max err) | gas **0.047** · water **0.049** | T1 | near-lossless |
| 7-bit codec **linear** (max err) | gas 0.383 · water **7.13** | T1 | **FAILS** on high dynamic range → must use clr |
| storage | **D bytes/unit** (7-bit payload + 1 XOR/how-to bit) | T1 | byte-aligned, integer |
| content address | **SHA-256 self-tag** (content-addressable) | T1 | `dbe4690e` |

## 3 · Memory & conveyor

| spec | value | tier | source |
|---|---|---|---|
| associative recall under magnitude + context scale + noise | **compositional 1.00** vs raw-magnitude **0.36** | T1 | `dbe4690e` |
| conveyor non-disruption (round-trip within 7-bit floor) | **yes** (max err 0.047) | T1 | `dbe4690e` |
| conveyor deterministic routing (same stream → same routes) | **yes** | T1 | `dbe4690e` |
| conveyor storage | **D bytes/unit** | T1 | `dbe4690e` |

## 4 · Decision & coherence

| spec | value | tier | source |
|---|---|---|---|
| **locked-discriminant invariance** (centred contrast) | **1.000** | T1 | `dbe4690e` / `9055c4a9` |
| non-invariant baselines (for contrast) | static argmax\|clr\| **0.615** | T1 | `dbe4690e` |
| triad cross-verify (Q/Hˢ/DUT) certification | **TRIAD-CON** on coherent device; outlier located otherwise | T1 | `f8ee9f6f` |
| end-to-end pipeline | compositional + deterministic + **tamper-evident** | T1 | `7f015532` |

## 5 · Reads

| spec | value | tier | source |
|---|---|---|---|
| effective dimension (water, D=7) | **2.64** | T1 | `dbe4690e` |
| drift self-report vs engine Aitchison step (real geology) | correlation **1.00**; 14 events localized | T1 | `26572eb8` |
| resolution frontier (max-power) | finest grain = min(data ceiling, compute ceiling); stops at max Q | T2 | `88d64e73` |

## 6 · Character analysis (Compositional Character Space)

| spec | value | tier | source |
|---|---|---|---|
| character battery | **107 systems across 13 domains** | T1 | CCS |
| character axes | **4 characters generalize** (Diffusive/Turbulent … Directed) | T1 | CCS |
| CCS effective rank | **corrected**: 2.80/5 at n=11 → does **not** collapse to ~3 at n=107 | T1 (honest correction) | CCS |
| conformance fixture | **HS-GOLD-1** known-hash set | T1 | `experiments/conformance_fixtures_2026-06/` |

## 7 · Throughput & complexity

| spec | value | tier | note |
|---|---|---|---|
| per-unit cost | **O(D)** encode/read | T2 | linear in parts |
| throughput | **~95,000 units/sec** | T2 | single-thread CPython, unoptimized, illustrative — excluded from the receipt (wall-clock) |
| cross-verify cost | O(log D) per link (transitive trust) | T2 | past |

## The honest fences (read these)

- **Exactness is the IEEE numerical floor** (~10⁻¹⁶), not infinite precision; and it is **exact only at
  D = 1, 2, 4, 8** (Hurwitz) — higher D is *tiled* from exact D=4 charts, lossless to ~10⁻¹² at D=10⁶.
- **The 313 dB / common-mode figures are numerical** — they do **not** beat Shannon channel capacity or the
  rate-distortion bound; only the *shared multiplicative* common-mode cancels; additive noise sets the floor.
- **The 7-bit codec is near-lossless only in clr coordinates** — linear 7-bit fails on high dynamic range
  (water 7.13).
- **Throughput is unoptimized single-thread Python** — illustrative, not a productized rate; excluded from
  the deterministic receipt.
- **Tiers:** T1 = measured + receipted; T2 = modeled / a design choice / unoptimized. Medical/clinical use of
  any instrument remains research-only until validated to standards.

*Cross-refs: `system_specs.py`, `SYSTEM_SPECS_RESULTS.json`, `HS-CN1_DATASHEET.md`,
`AN-001_DETERMINISTIC_NOISE_REJECTION.md`, `../../library/DOES_THE_SYSTEM_MAKE_SENSE.md`,
`../locked-discriminant/THE_LOCKED_DISCRIMINANT_PRINCIPLE.md`, `../../library/THE_WORLD_EXPERT_SYSTEM.md` (CCS).
Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — every spec measured or cited with a receipt · the impressive numbers are real · the fences are stated next to them · experts decide.*
