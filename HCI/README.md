# HCI — Higgins Computational Instruments

Pure mathematical discovery instruments derived from the Higgins Decomposition.

## Contents

| File | Description |
|------|-------------|
| HCI_FOUNDATION.md | Core proofs, corollaries, tensor engine specification |
| hci_cbs.py | Compositional Bearing Scope (CBS) — oscilloscope instrument |
| README.md | This file |

## Instruments

### Compositional Bearing Scope (CBS)

Oscilloscope-class display showing compositional bearing and heading.

```
python hci_cbs.py <results.json> [width] [height]
```

### Compositional Navigation Tensor (CNT)

The tensor engine powering all HCI instruments.

```
CNT(x) = (theta, omega, kappa, sigma)

theta  : bearing tensor      (all pairwise CLR angles)
omega  : angular velocity    (heading change in full D-space)
kappa  : steering sensitivity (metric tensor diagonal 1/x_j)
sigma  : helmsman index      (argmax |delta CLR|)
```

## Design Rules

- 8-bit monochrome only. No colour.
- 32-level grayscale for density encoding.
- ASCII symbology for all markers and annotations.
- Full sweep display: Hs [0, 1], bearing [0, 360].
- No scale factor. The instrument shows the complete measurement space.
- Pure math. No data interpretation. No domain language.

---

The instrument reads. The expert decides. The loop stays open.
