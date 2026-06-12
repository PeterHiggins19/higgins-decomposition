# FAO Aquastat Irrigation Methods — Interpretation Note

**Source:** `fao_irrigation_methods_cnt.json` (CNT v2.0.1)
**Period:** Latest reported year per country (most are 2022)
**Carriers:** Surface, Sprinkler, Localized (D = 3)
**Records:** 83 countries + UN regional aggregates (T = 83)

## What this is

FAO Aquastat reports the area equipped for full-control irrigation in
hectares, broken down by method:

* **Surface** (FAO_AS_4308) — flood, furrow, basin
* **Sprinkler** (FAO_AS_4309) — pivot, hand-move, solid-set
* **Localized** (FAO_AS_4310) — drip, micro-spray, bubbler

The three carriers sum exactly to FAO_AS_4311 ("Area equipped for
full-control irrigation: total"), making this a natural compositional
partition. Each country is one closed simplex point.

This is a cross-sectional snapshot — `is_temporal: false`. Order in
the JSON is by total irrigated area descending (biggest irrigators
first), which is convenient for inspection but should not be read as
a trajectory.

## Headline result

| Quantity | Value |
|---|---|
| T (countries) | 83 |
| D (methods) | 3 |
| Curvature tower depth | **15** |
| Period | 2 |
| Attractor (c_even, c_odd) | (0.719, 0.653) |
| Amplitude A | 0.066 |
| Contraction λ | −0.447 |
| Banach contraction | NO (mean ratio > 1) |
| IR classification | CRITICALLY_DAMPED |

The system shows a real period-2 attractor and asymptotic stability
(λ < 0), but with non-uniform contraction (the same pattern we
observed in Ball/Region geochemistry). Critically-damped because
amplitude < 0.1 — the cross-sectional spread compresses to a tight
attractor band.

## Three irrigation paradigms — the compositional story

### Surface-dominated (the traditional regime)

| Country | Surface | Sprinkler | Localized |
|---|---|---|---|
| Mali | 99.9 % | 0.0 % | 0.1 % |
| Yemen | 99.8 % | 0.1 % | 0.1 % |
| Philippines | 99.2 % | 0.2 % | 0.6 % |
| Malaysia | 98.2 % | 0.5 % | 1.3 % |
| Guinea | 97.7 % | 1.5 % | 0.8 % |

Rice-paddy and basin irrigation, typically gravity-fed. Mostly
South / South-East Asian and Sahelian countries. China (94 %) and
India (97 %) sit in this regime by virtue of their massive paddy
systems.

### Sprinkler-dominated (the temperate-mechanized regime)

| Country | Surface | Sprinkler | Localized |
|---|---|---|---|
| Serbia | 0.1 % | 91.8 % | 8.1 % |
| New Zealand | 3.7 % | 89.7 % | 6.6 % |
| Mauritius | 1.7 % | 88.4 % | 10.0 % |
| France | 4.5 % | 87.0 % | 8.5 % |
| Germany | 9.5 % | 83.3 % | 7.2 % |

Centre-pivot and large-scale sprinkler. Temperate-zone industrial
agriculture. The European cluster (France, Germany) and the
Australasian temperate (NZ) are the canonical examples.

### Localized-dominated (the water-scarce regime)

| Country | Surface | Sprinkler | Localized |
|---|---|---|---|
| Antigua and Barbuda | 0.0 % | 0.4 % | 99.6 % |
| UAE | 6.1 % | 0.2 % | 93.7 % |
| Cyprus | 5.0 % | 5.0 % | 90.0 % |
| Jordan | 16.8 % | 1.9 % | 81.4 % |
| Seychelles | 7.7 % | 15.4 % | 76.9 % |

Drip and micro-spray irrigation — high efficiency, low water loss.
Concentrated in the Middle East, small island states, and
arid-zone economies. Israel sits in this group (not in top 5 here
but historically the originator of drip).

The USA at 45 % Surface / 48 % Sprinkler / 7 % Localized is a
**balanced** outlier — the only major economy with near-equal Surface
and Sprinkler shares. Brazil at 31 % Surface / 20 % Sprinkler / 49 %
Localized is the largest country in the localized-dominated regime.

## Carrier-pair structure (Stage 2)

```
Surface-Sprinkler:  pearson r = −0.48,  bearing spread = 339°
Surface-Localized:  pearson r = −0.73,  bearing spread = 347°
Sprinkler-Localized: pearson r = −0.25, bearing spread = 348°
```

All three pairs are **anti-correlated** — a country with high Surface
share has low Sprinkler and Localized shares, and vice versa. The
Surface–Localized pair is most strongly anti-correlated (r = −0.73)
because the two represent opposite ends of the water-efficiency
gradient (highest waste vs lowest waste). None of the pairs are
"locked" (all have bearing spreads ~340–350°, near the maximum
possible spread for a D=3 simplex), which means countries don't
cluster on any single ratio — they fill the full 2-simplex
ternary plane.

## Helmsman lineage in the curvature tower

```
L1-L4: Surface
L5-L6: Sprinkler
L7-L8: Surface
...
```

The curvature recursion picks Surface as the dominant compositional
carrier through L1-L4, then switches to Sprinkler at L5-L6. This
matches the FAO data structure: Surface is the most-massive carrier
globally (China + India dominate), so the κ_jj = (1−1/D)/x_j² weighting
puts it on top. As recursion deepens, the metric tensor's normalization
shifts attention to the next-largest carrier (Sprinkler), then back to
Surface at L7-L8 as the recursive structure stabilises.

This is the same "diagnostic carrier" pattern observed in geochem —
the curvature tower reads which carrier is most discriminating, and
that carrier shifts level by level as the recursion settles.

## Why this is a CoDaWork-friendly result

1. **Pure CoDa setup.** The composition is a real simplex partition
   (sum = full-control irrigation total). No arbitrary closure choice.
   D = 3 is the canonical ternary simplex — the conference can
   visualize this on a standard CoDa ternary plot.

2. **Genuine policy structure.** The three regimes (traditional
   surface, temperate-sprinkler, arid-localized) are recognized
   irrigation-engineering categories. Aitchison-distance clustering
   would reproduce the geographic / climatic clustering without
   external labels.

3. **The numbers are right.** Top-5 lists per regime match
   independent FAO domain knowledge (Mali / Philippines / China for
   surface; France / Germany / NZ for sprinkler; Israel / UAE / Jordan
   for drip).

4. **CoDa-standard fields are sufficient.** A reviewer can read just
   `tensor.timesteps[i].coda_standard.composition` for each country
   and reproduce the regime clustering with `compositions::aDist()`.
   No HUF-specific machinery required.

5. **Higgins extensions add a layer.** The depth tower's period-2
   attractor (A = 0.066) is small but real — the cross-sectional
   spread of irrigation methods is bounded, with the attractor band
   in (0.65, 0.72) on the Higgins scale. Whether that band has
   physical meaning beyond "compositions are bounded by the simplex
   geometry" is open.

## Comparison to other domain results

| System              | T  | D | curv δ | A     | IR class             |
|---------------------|----|---|--------|-------|----------------------|
| Ball/Region geochem | 95 | 10|   14   | 0.118 | MODERATELY_DAMPED    |
| Stracke OIB         | 15 | 10|   14   | 0.114 | LIGHTLY_DAMPED       |
| Tappe KIM1          |  8 | 10|   16   | 0.066 | CRITICALLY_DAMPED    |
| **FAO irrigation**  | **83** | **3** | **15** | **0.066** | **CRITICALLY_DAMPED** |
| Qin Cpx             | 30 |  9|   15   | 0.099 | CRITICALLY_DAMPED    |

FAO at A = 0.066 sits exactly with Tappe (0.066) — both are
"critically damped" cross-sections with tight attractors. The fact
that a D = 3 cross-section of irrigation methods produces the same
amplitude class as a D = 10 cross-section of mantle kimberlite
geochemistry is interesting — it suggests the class is a property of
the *cross-sectional* nature (compositional bounds set by the
simplex), not of the dimension.

## Files in this folder

- `fao_irrigation_input.csv` — 83 countries × 3 carriers, ready CSV
- `fao_irrigation_methods_cnt.json` — canonical CNT JSON
- `JOURNAL.md` — auto-generated summary
- `INTERPRETATION.md` — this note

---

*The instrument reads. The expert decides. The loop stays open.*
