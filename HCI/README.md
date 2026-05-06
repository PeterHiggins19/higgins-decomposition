# HCI — Higgins Compositional Instrument

Compositional systems navigation plotter. HCI charts where the system is, where it has been, which carriers drove displacement, and which metric directions support future guidance.

## Contents

| File | Description |
|------|-------------|
| HCI_FOUNDATION.md | Core proofs, corollaries, tensor engine specification |
| HCI_USER_GUIDE.md | User guide — reading HCI outputs, HLR units, scale provenance |
| HCI_CHATGPT_BRIEFING_2026-05-04.json | Authoritative briefing for terminology and standards |
| hci_cbs.py | Compositional Bearing Scope (CBS) — oscilloscope instrument |
| README.md | This file |

## Unit Standard

All plate coordinates are reported in **Higgins Log-Ratio Level (HLR)** — a dimensionless natural-log ratio unit. Nearest relative in the log-level family: the neper.

```
h_j(t) = ln(x_j(t)) - mean_k ln(x_k(t))
       = ln(x_j(t) / g(x(t)))
```

## Instruments

### Stage 1 — Section Plate Generator

Fixed-scale instrument display with Higgins tensor data field layout v1.0. One section plate per time index showing XY scatter (plan view), XZ bearings, YZ CLR bars, plus info and legend panels. System Course Plot as final page.

```
python codawork2026/stage1_plates/stage1_plates_raw.py <stage1_output.json> [output.pdf]
```

### Compositional Navigation Tensor (CNT)

The tensor engine powering all HCI instruments.

```
CNT(x) = (theta, omega, kappa_HS, sigma)

theta    : bearing tensor               (all pairwise CLR angles)
omega    : angular velocity             (heading change in full D-space, atan2-stable)
kappa_HS : Higgins Steering Metric Tensor  (full D×D Aitchison metric)
           kappa_HS_ij(x) = (delta_ij - 1/D) / (x_i * x_j)
sigma    : Dominant Carrier Displacement Index / Helmsman  (argmax |delta h_j|)
```

Diagonal carrier steering sensitivity: `s_j(x) = 1/x_j` — this is one diagnostic channel, not the full tensor.

## Scale Provenance

```
Y_j(t) → x_j(t) = Y_j/T → h_j(t) = CLR → section coordinate
```

The plate does not plot raw values. It plots closed compositions as Higgins-coordinate displacement from the barycentre under a fixed run scale.

## Design Rules

- 8-bit monochrome only. No colour.
- Fixed-scale graticule locked across all plates.
- ASCII symbology for all markers and annotations.
- Pure math. No data interpretation. No domain language.

---

The instrument reads. The expert decides. The loop stays open.
