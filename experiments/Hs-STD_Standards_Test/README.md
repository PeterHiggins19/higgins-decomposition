# Hs-STD — Standards Test Suite

Synthetic-geometry calibration suite for the Hs/CNT pipeline. Three primitive
solids — cube, cylinder, sphere — sampled as compositional polar stacks so that
the engine has known-truth references for the spherical-coordinate channels
(theta / kappa / signed-omega) and the helmsman corollary.

## Folder layout

```
Hs-STD_Standards_Test/
├── build_standards.py              regenerator for all three solids
├── Hs_INDEX.json                   suite-level registry (hashed)
├── Hs-STD_JOURNAL.md               audit-trail record for the suite
├── STD-standards_suite_projector.html   combined projector across all 3
├── cube/                           STD-cube_polar_stack.json + cinema + projector
├── cylinder/                       STD-cylinder_polar_stack.json + cinema + projector
└── sphere/                         STD-sphere_polar_stack.json + cinema + projector
```

Each per-solid subfolder has its own README explaining the geometry, the
analytic ground truth for the primary CNT channels, and the expected pass
band for the determinism gate.

## Role in the corpus

This is one of the four **reference experiments** in the 25-experiment
determinism-gate corpus (see `../../HCI-CNT/experiments/reference/`). It
exists to provide closed-form ground truth for engine validation — every
release of the engine must reproduce these polar-stack outputs bit-for-bit.

## Running the suite

```bash
# Regenerate all three solids + suite projector
python build_standards.py

# Or analyse a single solid through the current canon
python ../../HCI-CNT/mission_command/mission_command.py std_cube
python ../../HCI-CNT/mission_command/mission_command.py std_cylinder
python ../../HCI-CNT/mission_command/mission_command.py std_sphere
```

## Status

Foundational reference — kept verbatim. The current canonical engine is
**CNT 2.0.4** at `../../HCI-CNT/engine/cnt.py`. Every solid here is
re-verified against that engine on every release; results live in
`Hs_INDEX.json` with full hash-chain provenance.

## See also

- `../README.md` — experiments-folder root index
- `../../HCI-CNT/experiments/reference/` — current canonical reference set
- `../Hs-CNT_2026-05/` — current dated CNT corpus snapshot
- `../../HCI-CNT/handbook/VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md` — the determinism gate, formal
