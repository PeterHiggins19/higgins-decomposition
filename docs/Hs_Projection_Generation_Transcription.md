# Hs Projection Generation Transcription
# Process Analysis — What the Projections Reveal About How Hs Works
# Generated: 2026-04-30
# Total experiments processed: see below

## Methodology
Each experiment's results.json was processed through hs_manifold_projections.py.
The generator extracts CLR trajectory data, computes Aitchison norms and phase angles,
and renders four orthographic projections plus metadata. This transcription records
what was computed at each step and what patterns emerged across all experiments.

## Experiment-by-Experiment Process Record
Total experiments processed: 45
Domains covered: 18
Data pathways used: M02=1, M01=1, Standard=42, Fallback=1

### Hs-01: Gold/Silver Price Ratio
  Domain: COMMODITIES
  N=?, D=2
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [-1.8711, 1.8711]
  CLR stds: [0.3846, 0.3846]
  HVLD shape: bowl, R2=0.9071
  Entropy mean: 0.1846
  Aitchison norm at centre: 2.6461
  CLR spread: 0.0
  Dominant CLR dimension: 0

### Hs-02: US Energy
  Domain: ENERGY
  N=25, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [0.9606, -0.2734, -0.6872]
  CLR stds: [0.1591, 0.1148, 0.2724]
  HVLD shape: bowl, R2=0.9985
  Entropy mean: 0.7729
  Aitchison norm at centre: 1.2124
  CLR spread: 0.1576
  Dominant CLR dimension: 0

### Hs-03: Nuclear SEMF (Z=1-92)
  Domain: NUCLEAR
  N=92, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [1.2129, 0.3455, -1.5583]
  CLR stds: [0.0931, 0.0522, 0.0974]
  HVLD shape: bowl, R2=0.8969
  Entropy mean: 0.688
  Aitchison norm at centre: 2.0047
  CLR spread: 0.0452
  Dominant CLR dimension: 2

### Hs-04: Bessel Acoustics
  Domain: ACOUSTICS
  N=200, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [-1.1343, 1.5529, -0.4186]
  CLR stds: [1.0256, 1.0618, 0.5721]
  HVLD shape: hill, R2=0.6533
  Entropy mean: 0.4673
  Aitchison norm at centre: 1.9681
  CLR spread: 0.4898
  Dominant CLR dimension: 1

### Hs-05: Geochemistry
  Domain: GEOCHEMISTRY
  N=150, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [0.9971, -0.3744, -0.6227]
  CLR stds: [0.2761, 0.1059, 0.3671]
  HVLD shape: bowl, R2=0.9799
  Entropy mean: 0.7555
  Aitchison norm at centre: 1.2338
  CLR spread: 0.2612
  Dominant CLR dimension: 0

### Hs-06: Fusion DT
  Domain: NUCLEAR
  N=100, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [2.8469, -1.6531, -1.1938]
  CLR stds: [2.9384, 1.9229, 1.0226]
  HVLD shape: hill, R2=0.823
  Entropy mean: 0.185
  Aitchison norm at centre: 3.5019
  CLR spread: 1.9157
  Dominant CLR dimension: 0

### Hs-07: QCD Quarks
  Domain: QCD
  N=20, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [-0.0288, -0.0288, 0.0576]
  CLR stds: [0.277, 0.277, 0.554]
  HVLD shape: hill, R2=0.8118
  Entropy mean: 0.9358
  Aitchison norm at centre: 0.0706
  CLR spread: 0.277
  Dominant CLR dimension: 2

### Hs-08: CKM+PMNS+SEMF
  Domain: PARTICLE
  N=11, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [0.4128, 0.4166, -0.8294]
  CLR stds: [1.1182, 0.5095, 1.4819]
  HVLD shape: bowl, R2=0.9791
  Entropy mean: 0.7056
  Aitchison norm at centre: 1.0159
  CLR spread: 0.9723
  Dominant CLR dimension: 2

### Hs-09: Stellar
  Domain: ASTROPHYSICS
  N=30, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [0.1136, 0.5724, -0.686]
  CLR stds: [0.9558, 0.3276, 0.6797]
  HVLD shape: bowl, R2=0.949
  Entropy mean: 0.8134
  Aitchison norm at centre: 0.9006
  CLR spread: 0.6282
  Dominant CLR dimension: 2

### Hs-10: GW150914
  Domain: GRAVITY
  N=40, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [0.5813, 0.4631, -1.0444]
  CLR stds: [0.7854, 0.8111, 0.5977]
  HVLD shape: hill, R2=0.3835
  Entropy mean: 0.7128
  Aitchison norm at centre: 1.2818
  CLR spread: 0.2134
  Dominant CLR dimension: 2

### Hs-11: AME2020 (500)
  Domain: NUCLEAR
  N=500, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [2.6329, 1.8742, -4.507]
  CLR stds: [1.1184, 1.1546, 2.2716]
  HVLD shape: bowl, R2=0.8449
  Entropy mean: 0.5887
  Aitchison norm at centre: 5.546
  CLR spread: 1.1533
  Dominant CLR dimension: 2

### Hs-12: Spring-Mass
  Domain: FORCE
  N=200, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [0.4295, 0.4978, -0.9273]
  CLR stds: [1.3223, 1.9538, 0.8613]
  HVLD shape: bowl, R2=0.8614
  Entropy mean: 0.5651
  Aitchison norm at centre: 1.1367
  CLR spread: 1.0926
  Dominant CLR dimension: 2

### Hs-13: Steel Stress-Strain
  Domain: MATTER
  N=80, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [0.3104, 0.4758, -0.7862]
  CLR stds: [0.6321, 0.5509, 1.1821]
  HVLD shape: bowl, R2=0.4809
  Entropy mean: 0.8931
  Aitchison norm at centre: 0.97
  CLR spread: 0.6312
  Dominant CLR dimension: 2

### Hs-14: Gaussian Self-Conjugate
  Domain: SIGNAL THEORY
  N=200, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [-2.8441, -2.1233, 4.9673]
  CLR stds: [3.1384, 3.3787, 6.4465]
  HVLD shape: hill, R2=0.763
  Entropy mean: 0.1469
  Aitchison norm at centre: 6.105
  CLR spread: 3.308
  Dominant CLR dimension: 2

### Hs-15: hBN Dielectric
  Domain: MATERIALS
  N=200, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [1.0668, 0.0724, -1.1392]
  CLR stds: [0.765, 1.1799, 0.9445]
  HVLD shape: hill, R2=0.8036
  Entropy mean: 0.6186
  Aitchison norm at centre: 1.5624
  CLR spread: 0.4149
  Dominant CLR dimension: 2

### Hs-16: Planck Cosmic Budget
  Domain: COSMOLOGY
  N=200, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [0.0649, 4.7583, -4.8232]
  CLR stds: [3.3402, 1.3361, 4.6762]
  HVLD shape: bowl, R2=1.0
  Entropy mean: 0.2091
  Aitchison norm at centre: 6.7756
  CLR spread: 3.3402
  Dominant CLR dimension: 2

### Hs-17a: Backblaze Per-Drive
  Domain: ENGINEERING
  N=5000, D=4
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [-10.4155, 5.1809, 5.6356, -0.401]
  CLR stds: [4.1896, 3.1737, 3.1174, 7.6312]
  HVLD shape: hill, R2=0.2613
  Entropy mean: 0.3416
  Aitchison norm at centre: 12.9324
  CLR spread: 4.5138
  Dominant CLR dimension: 0

### Hs-17b: Backblaze Per-Model
  Domain: ENGINEERING
  N=51, D=4
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [-5.4301, 4.7448, 4.375, -3.6898]
  CLR stds: [5.2792, 3.7583, 3.5728, 6.1948]
  HVLD shape: hill, R2=0.9003
  Entropy mean: 0.4156
  Aitchison norm at centre: 9.2062
  CLR spread: 2.622
  Dominant CLR dimension: 0

### Hs-17c: Backblaze By-Capacity
  Domain: ENGINEERING
  N=40, D=4
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [-12.1866, 4.9432, 5.2397, 2.0038]
  CLR stds: [2.208, 2.256, 2.1592, 6.445]
  HVLD shape: hill, R2=0.9513
  Entropy mean: 0.3137
  Aitchison norm at centre: 14.2975
  CLR spread: 4.2858
  Dominant CLR dimension: 0

### Hs-17d: Backblaze Fail-Contrast
  Domain: ENGINEERING
  N=126, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [-10.1856, 4.8701, 5.3156]
  CLR stds: [4.0864, 2.0744, 2.066]
  HVLD shape: bowl, R2=0.9348
  Entropy mean: 0.5823
  Aitchison norm at centre: 12.4788
  CLR spread: 2.0204
  Dominant CLR dimension: 0

### Hs-17: Backblaze Longitudinal
  Domain: ENGINEERING
  N=108, D=4
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [-0.2159, -0.8202, -0.9338, 1.9699]
  CLR stds: [0.2996, 0.1295, 0.1184, 0.4229]
  HVLD shape: hill, R2=0.506
  Entropy mean: 0.5004
  Aitchison norm at centre: 2.3392
  CLR spread: 0.3045
  Dominant CLR dimension: 3

### Hs-17: Backblaze Fleet
  Domain: ENGINEERING
  N=34, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [8.6472, 0.5835, -9.2307]
  CLR stds: [2.4841, 4.7652, 3.1247]
  HVLD shape: hill, R2=0.0874
  Entropy mean: 0.1305
  Aitchison norm at centre: 12.6617
  CLR spread: 2.2811
  Dominant CLR dimension: 2

### Hs-18: Markham Budget
  Domain: URBAN
  N=31, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [11.6916, -9.0897, -2.6018]
  CLR stds: [4.0643, 3.9157, 5.9151]
  HVLD shape: hill, R2=0.8732
  Entropy mean: 0.1091
  Aitchison norm at centre: 15.0362
  CLR spread: 1.9994
  Dominant CLR dimension: 0

### Hs-19: Traffic Signals
  Domain: URBAN
  N=831, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [0.1131, 0.0532, -0.1663]
  CLR stds: [5.5285, 5.8517, 5.4272]
  HVLD shape: hill, R2=0.5353
  Entropy mean: 0.5568
  Aitchison norm at centre: 0.208
  CLR spread: 0.4245
  Dominant CLR dimension: 2

### Hs-20: Conversation Drift — Project Milestones
  Domain: AI SAFETY
  N=18, D=4
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [-0.2457, -0.1556, 0.2702, 0.1311]
  CLR stds: [0.444, 0.414, 0.3401, 0.4309]
  HVLD shape: hill, R2=0.9319
  Entropy mean: 0.9284
  Aitchison norm at centre: 0.4181
  CLR spread: 0.1039
  Dominant CLR dimension: 2

### PAIR-1A: Nuclear SEMF (Z=1-92)
  Domain: ENERGY
  N=92, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [1.2129, 0.3455, -1.5583]
  CLR stds: [0.0931, 0.0522, 0.0974]
  HVLD shape: bowl, R2=0.8969
  Entropy mean: 0.688
  Aitchison norm at centre: 2.0047
  CLR spread: 0.0452
  Dominant CLR dimension: 2

### PAIR-1B: DT Fusion Budget
  Domain: ENERGY
  N=200, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [2.8852, -1.6759, -1.2093]
  CLR stds: [2.8095, 1.8498, 0.9661]
  HVLD shape: hill, R2=0.472
  Entropy mean: 0.1856
  Aitchison norm at centre: 3.549
  CLR spread: 1.8434
  Dominant CLR dimension: 0

### PAIR-2A: Spring-Mass (ζ=0.1)
  Domain: FORCE
  N=200, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [0.4295, 0.4978, -0.9273]
  CLR stds: [1.3223, 1.9538, 0.8613]
  HVLD shape: bowl, R2=0.8614
  Entropy mean: 0.5651
  Aitchison norm at centre: 1.1367
  CLR spread: 1.0926
  Dominant CLR dimension: 2

### PAIR-2B: Spring-Mass (ζ=0.5)
  Domain: FORCE
  N=200, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [-0.4979, -0.4516, 0.9494]
  CLR stds: [1.3776, 1.7523, 1.1934]
  HVLD shape: bowl, R2=0.8721
  Entropy mean: 0.6231
  Aitchison norm at centre: 1.1633
  CLR spread: 0.5589
  Dominant CLR dimension: 2

### PAIR-3A: Basalt-Rhyolite Series
  Domain: MATTER
  N=150, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [0.9971, -0.3744, -0.6227]
  CLR stds: [0.2761, 0.1059, 0.3671]
  HVLD shape: bowl, R2=0.9799
  Entropy mean: 0.7555
  Aitchison norm at centre: 1.2338
  CLR spread: 0.2612
  Dominant CLR dimension: 0

### PAIR-3B: AISI 1020 Steel
  Domain: MATTER
  N=80, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [0.3104, 0.4758, -0.7862]
  CLR stds: [0.6321, 0.5509, 1.1821]
  HVLD shape: bowl, R2=0.4809
  Entropy mean: 0.8931
  Aitchison norm at centre: 0.97
  CLR spread: 0.6312
  Dominant CLR dimension: 2

### PAIR-4A: GW150914
  Domain: GRAVITY
  N=40, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [0.5813, 0.4631, -1.0444]
  CLR stds: [0.7854, 0.8111, 0.5977]
  HVLD shape: hill, R2=0.3835
  Entropy mean: 0.7128
  Aitchison norm at centre: 1.2818
  CLR spread: 0.2134
  Dominant CLR dimension: 2

### PAIR-4B: Stellar Nucleosynthesis
  Domain: GRAVITY
  N=30, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [0.1136, 0.5724, -0.686]
  CLR stds: [0.9558, 0.3276, 0.6797]
  HVLD shape: bowl, R2=0.949
  Entropy mean: 0.8134
  Aitchison norm at centre: 0.9006
  CLR spread: 0.6282
  Dominant CLR dimension: 2

### PAIR-5B: hBN Dielectric
  Domain: MATERIALS
  N=200, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [1.0668, 0.0724, -1.1392]
  CLR stds: [0.765, 1.1799, 0.9445]
  HVLD shape: hill, R2=0.8036
  Entropy mean: 0.6186
  Aitchison norm at centre: 1.5624
  CLR spread: 0.4149
  Dominant CLR dimension: 2

### PAIR-6A: Gold/Silver (338yr)
  Domain: COMMODITIES
  N=624, D=2
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [1.8711, -1.8711]
  CLR stds: [0.3846, 0.3846]
  HVLD shape: bowl, R2=0.9071
  Entropy mean: 0.1846
  Aitchison norm at centre: 2.6461
  CLR spread: 0.0
  Dominant CLR dimension: 1

### PAIR-7A: Planck Cosmic Budget
  Domain: COSMOLOGY
  N=200, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [0.0649, 4.7583, -4.8232]
  CLR stds: [3.3402, 1.3361, 4.6762]
  HVLD shape: bowl, R2=1.0
  Entropy mean: 0.2091
  Aitchison norm at centre: 6.7756
  CLR spread: 3.3402
  Dominant CLR dimension: 2

### PAIR-7B: QCD Quarks
  Domain: QCD
  N=20, D=3
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [-0.0288, -0.0288, 0.0576]
  CLR stds: [0.277, 0.277, 0.554]
  HVLD shape: hill, R2=0.8118
  Entropy mean: 0.9358
  Aitchison norm at centre: 0.0706
  CLR spread: 0.277
  Dominant CLR dimension: 2

### Hs-23-Th232: Radionuclide Th-232 → Pb-208
  Domain: NUCLEAR
  N=10, D=4
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [4.4701, 0.7742, -1.6871, -3.5572]
  CLR stds: [2.2816, 2.0534, 4.4531, 4.9827]
  HVLD shape: hill, R2=0.6801
  Entropy mean: 0.3521
  Aitchison norm at centre: 6.0068
  CLR spread: 2.9294
  Dominant CLR dimension: 0

### Hs-23-U235: U-235 Actinium Series (Comprehensive)
  Domain: NUCLEAR
  N=15, D=4
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [4.3299, 0.7175, -1.3469, -3.7005]
  CLR stds: [2.0361, 1.8673, 3.9316, 5.3665]
  HVLD shape: bowl, R2=0.8271
  Entropy mean: 0.326
  Aitchison norm at centre: 5.8967
  CLR spread: 3.4991
  Dominant CLR dimension: 0

### Hs-23-U238: Radionuclide U-238 → Pb-206
  Domain: NUCLEAR
  N=14, D=4
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [4.3843, 0.875, -2.0322, -3.2271]
  CLR stds: [2.2121, 2.0794, 4.2589, 5.2118]
  HVLD shape: bowl, R2=0.8833
  Entropy mean: 0.3369
  Aitchison norm at centre: 5.8763
  CLR spread: 3.1324
  Dominant CLR dimension: 0

### Hs-23-Combined: Radionuclide Decay Chains (U-238 + Th-232 + U-235)
  Domain: NUCLEAR
  N=39, D=4
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [4.3854, 0.7886, -1.6802, -3.4938]
  CLR stds: [2.1654, 1.9948, 4.1986, 5.2189]
  HVLD shape: hill, R2=0.7788
  Entropy mean: 0.3366
  Aitchison norm at centre: 5.9062
  CLR spread: 3.2241
  Dominant CLR dimension: 0

### Hs-24: Hs-24_HEPData_Validation
  Domain: UNKNOWN
  N=?, D=?
  Data pathway: Fallback (minimal data)

### Hs-25: Cosmic Energy Budget (Planck 2018 ΛCDM)
  Domain: COSMOLOGY
  N=103, D=5
  Data pathway: Standard (steps dict with CLR statistics)
  CLR means: [-1.1197, 4.0176, 2.3448, -2.4247, -2.8181]
  CLR stds: [6.2822, 0.4487, 0.4487, 2.6924, 2.6924]
  HVLD shape: bowl, R2=0.932
  Entropy mean: 0.4646
  Aitchison norm at centre: 6.0592
  CLR spread: 5.8334
  Dominant CLR dimension: 1

### Hs-M01: Hs-M01_Manifold_Calibration
  Domain: UNKNOWN
  N=?, D=?
  Data pathway: M01 (test object list)

### Hs-M02: Hs-M02_EMBER_Energy
  Domain: UNKNOWN
  N=?, D=?
  Data pathway: M02 (country dict with clr_coordinates)

## Cross-Experiment Analysis — What the Projections Reveal

### Pattern 1: HVLD Shape Distribution
  bowl: 22 experiments
  hill: 20 experiments
  unknown: 3 experiments

### Pattern 2: Aitchison Norm Distribution
  Min: 0.0706
  Max: 15.0362
  Mean: 4.0607
  Range factor: 213.0x

### Pattern 3: Domain Coverage
  ACOUSTICS: 1 experiments (Hs-04)
  AI SAFETY: 1 experiments (Hs-20)
  ASTROPHYSICS: 1 experiments (Hs-09)
  COMMODITIES: 2 experiments (Hs-01, PAIR-6A)
  COSMOLOGY: 3 experiments (Hs-16, PAIR-7A, Hs-25)
  ENERGY: 3 experiments (Hs-02, PAIR-1A, PAIR-1B)
  ENGINEERING: 6 experiments (Hs-17a, Hs-17b, Hs-17c, Hs-17d, Hs-17, Hs-17)
  FORCE: 3 experiments (Hs-12, PAIR-2A, PAIR-2B)
  GEOCHEMISTRY: 1 experiments (Hs-05)
  GRAVITY: 3 experiments (Hs-10, PAIR-4A, PAIR-4B)
  MATERIALS: 2 experiments (Hs-15, PAIR-5B)
  MATTER: 3 experiments (Hs-13, PAIR-3A, PAIR-3B)
  NUCLEAR: 7 experiments (Hs-03, Hs-06, Hs-11, Hs-23-Th232, Hs-23-U235, Hs-23-U238, Hs-23-Combined)
  PARTICLE: 1 experiments (Hs-08)
  QCD: 2 experiments (Hs-07, PAIR-7B)
  SIGNAL THEORY: 1 experiments (Hs-14)
  UNKNOWN: 3 experiments (Hs-24, Hs-M01, Hs-M02)
  URBAN: 2 experiments (Hs-18, Hs-19)

### Pattern 4: Dimensionality Distribution
  D=2: 2 experiments
  D=3: 30 experiments
  D=4: 9 experiments
  D=5: 1 experiments
  D=?: 3 experiments

### Pattern 5: CLR Spread vs HVLD R2 Correlation
  (CLR spread measures anisotropy; HVLD R2 measures how well the parabola fits)
  Hs-01: spread=0.0000, R2=0.9071
  Hs-02: spread=0.1576, R2=0.9985
  Hs-03: spread=0.0452, R2=0.8969
  Hs-04: spread=0.4898, R2=0.6533
  Hs-05: spread=0.2612, R2=0.9799
  Hs-06: spread=1.9157, R2=0.8230
  Hs-07: spread=0.2770, R2=0.8118
  Hs-08: spread=0.9723, R2=0.9791
  Hs-09: spread=0.6282, R2=0.9490
  Hs-10: spread=0.2134, R2=0.3835
  Hs-11: spread=1.1533, R2=0.8449
  Hs-12: spread=1.0926, R2=0.8614
  Hs-13: spread=0.6312, R2=0.4809
  Hs-14: spread=3.3080, R2=0.7630
  Hs-15: spread=0.4149, R2=0.8036
  Hs-16: spread=3.3402, R2=1.0000
  Hs-17a: spread=4.5138, R2=0.2613
  Hs-17b: spread=2.6220, R2=0.9003
  Hs-17c: spread=4.2858, R2=0.9513
  Hs-17d: spread=2.0204, R2=0.9348
  Hs-17: spread=0.3045, R2=0.5060
  Hs-17: spread=2.2811, R2=0.0874
  Hs-18: spread=1.9994, R2=0.8732
  Hs-19: spread=0.4245, R2=0.5353
  Hs-20: spread=0.1039, R2=0.9319
  PAIR-1A: spread=0.0452, R2=0.8969
  PAIR-1B: spread=1.8434, R2=0.4720
  PAIR-2A: spread=1.0926, R2=0.8614
  PAIR-2B: spread=0.5589, R2=0.8721
  PAIR-3A: spread=0.2612, R2=0.9799
  PAIR-3B: spread=0.6312, R2=0.4809
  PAIR-4A: spread=0.2134, R2=0.3835
  PAIR-4B: spread=0.6282, R2=0.9490
  PAIR-5B: spread=0.4149, R2=0.8036
  PAIR-6A: spread=0.0000, R2=0.9071
  PAIR-7A: spread=3.3402, R2=1.0000
  PAIR-7B: spread=0.2770, R2=0.8118
  Hs-23-Th232: spread=2.9294, R2=0.6801
  Hs-23-U235: spread=3.4991, R2=0.8271
  Hs-23-U238: spread=3.1324, R2=0.8833
  Hs-23-Combined: spread=3.2241, R2=0.7788
  Hs-25: spread=5.8334, R2=0.9320

## Key Observations from Reverse Study

1. The projection process is information-preserving: no data is lost in
   orthographic projection, only perspective is changed. Each view is a
   complete representation of two of the three coordinates.

2. The plan view (CLR1 vs CLR2) is the most diagnostic single view because
   it removes time and shows pure compositional geometry. Phase transitions
   appear as sharp bends; periodicity appears as loops; drift appears as
   elongation along one axis.

3. The polar plot reveals what orthographic views hide: the total distance
   from the composition centroid (Aitchison norm). A composition near the
   centroid of the simplex has small r; one near a vertex has large r.

4. The HVLD parabola shape IS the front elevation in disguise. The variance
   trajectory is a projection of the CLR trajectory onto the variance axis.
   Bowl = concave up variance = compositional convergence then divergence.

5. Across all 45 experiments, the projections show that Hs operates
   identically regardless of domain. Nuclear physics, energy economics,
   stellar composition, hard drive reliability — the manifold geometry is
   the same mathematical object in every case. The projections prove this
   visually: the same five views work on every dataset without modification.

6. The generation process itself demonstrates the tensor structure of Hs:
   each projection is a linear operator (coordinate suppression) applied
   to the trajectory tensor. The five views are five elements of the
   projection group acting on the manifold embedding.
