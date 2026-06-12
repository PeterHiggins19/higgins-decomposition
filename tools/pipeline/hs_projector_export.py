#!/usr/bin/env python3
"""
Hˢ PROJECTOR EXPORT
====================
Converts Hˢ pipeline results JSON into projector manifest JSON
for the universal Manifold Projector (tools/interactive/hs_projector.html).

The universal projector accepts pipeline results JSON directly, but this
script can also produce a lightweight projector manifest with just the
data needed for visualization — useful for sharing or embedding.

Usage:
  # From pipeline results (multi-system)
  python hs_projector_export.py results.json -o projector.json

  # From multiple single-system results
  python hs_projector_export.py sys1.json sys2.json -o combined.json

  # Programmatic use
  from hs_projector_export import export_projector
  manifest = export_projector(results_dict)

Author: Peter Higgins / Claude
Version: 1.0
"""

import json
import sys
import os
import numpy as np

# Default palette for systems without assigned colors
PALETTE = [
    '#ffd700', '#ff6b6b', '#ff69b4', '#4169e1', '#ff4500', '#32cd32',
    '#ffffff', '#00ced1', '#ff8c00', '#9370db', '#20b2aa', '#dc143c'
]


def clr_from_composition(comp, epsilon=1e-10):
    """Compute CLR coordinates from a composition vector.

    Parameters
    ----------
    comp : array-like
        Composition vector (proportions summing to 1).
    epsilon : float
        Zero replacement value.

    Returns
    -------
    list : CLR coordinates (log of each part / geometric mean).
    """
    x = np.array(comp, dtype=float)
    x = np.where(x <= 0, epsilon, x)
    x = x / x.sum()
    gm = np.exp(np.mean(np.log(x)))
    return (np.log(x / gm)).tolist()


def extract_clr_from_results(results):
    """Extract CLR matrix from pipeline results JSON.

    Handles multiple formats:
    - Multi-system: { "countries": { "SYS": { "clr_coordinates": {...} } } }
    - Single system: { "carriers": [...], "clr_coordinates": {...} }
    - Composition only: { "carriers": [...], "composition_pct": {...} }

    Returns
    -------
    dict : { key: { code, name, carriers, labels, clr } }
    """
    systems = {}

    # Multi-system format
    if 'countries' in results:
        for key, sys in results['countries'].items():
            carriers = sys.get('carriers', [])
            years = sys.get('years', [])

            if sys.get('clr_coordinates'):
                if not years:
                    years = sorted(sys['clr_coordinates'].keys(), key=lambda y: int(y))
                clr = []
                for yr in years:
                    yr_str = str(yr)
                    if yr_str in sys['clr_coordinates']:
                        row = [sys['clr_coordinates'][yr_str].get(c, 0.0) for c in carriers]
                        clr.append(row)
                systems[key] = {
                    'code': key,
                    'name': sys.get('country', sys.get('name', key)),
                    'carriers': carriers,
                    'labels': [str(y) for y in years],
                    'clr': clr
                }
        return systems

    # Single system format
    if 'carriers' in results and 'clr_coordinates' in results:
        carriers = results['carriers']
        years = results.get('years', sorted(results['clr_coordinates'].keys(), key=lambda y: int(y)))
        clr = []
        for yr in years:
            yr_str = str(yr)
            if yr_str in results['clr_coordinates']:
                row = [results['clr_coordinates'][yr_str].get(c, 0.0) for c in carriers]
                clr.append(row)
        key = results.get('iso', results.get('code', 'SYS'))
        systems[key] = {
            'code': key,
            'name': results.get('country', results.get('name', key)),
            'carriers': carriers,
            'labels': [str(y) for y in years],
            'clr': clr
        }
        return systems

    return systems


def export_projector(results, title=None, subtitle=None, colors=None):
    """Convert pipeline results to projector manifest format.

    Parameters
    ----------
    results : dict
        Pipeline results JSON (parsed).
    title : str, optional
        Override title. Defaults to experiment title from results.
    subtitle : str, optional
        Override subtitle. Defaults to domain or series.
    colors : dict, optional
        { system_key: '#hex' } color overrides.

    Returns
    -------
    dict : Projector manifest JSON.
    """
    systems = extract_clr_from_results(results)

    if not systems:
        raise ValueError("No systems with CLR data found in results.")

    if title is None:
        title = results.get('title', results.get('experiment', 'Hˢ Analysis'))
    if subtitle is None:
        subtitle = results.get('series', results.get('domain', ''))

    # Assign colors
    colors = colors or {}
    ci = 0
    manifest_systems = {}
    for key, sys in systems.items():
        color = colors.get(key, PALETTE[ci % len(PALETTE)])
        manifest_systems[key] = {
            'name': sys['name'],
            'color': color,
            'carriers': sys['carriers'],
            'labels': sys['labels'],
            'clr': [[round(v, 6) for v in row] for row in sys['clr']]
        }
        ci += 1

    return {
        'projector': True,
        'title': title,
        'subtitle': subtitle,
        'generator': 'hs_projector_export.py v1.0',
        'systems': manifest_systems
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='Hˢ Projector Export — convert pipeline results to projector manifest'
    )
    parser.add_argument('inputs', nargs='+', help='Input JSON file(s)')
    parser.add_argument('-o', '--output', default='projector_manifest.json',
                        help='Output JSON file (default: projector_manifest.json)')
    parser.add_argument('--title', help='Override title')
    parser.add_argument('--subtitle', help='Override subtitle')
    args = parser.parse_args()

    combined_systems = {}
    title = args.title
    subtitle = args.subtitle

    for path in args.inputs:
        with open(path, encoding='utf-8') as f:
            results = json.load(f)

        systems = extract_clr_from_results(results)
        combined_systems.update(systems)

        if title is None:
            title = results.get('title', results.get('experiment', 'Hˢ Analysis'))
        if subtitle is None:
            subtitle = results.get('series', results.get('domain', ''))

    if not combined_systems:
        print("Error: No systems with CLR data found in input files.")
        sys.exit(1)

    # Build manifest
    ci = 0
    manifest_systems = {}
    for key, sys in combined_systems.items():
        manifest_systems[key] = {
            'name': sys['name'],
            'color': PALETTE[ci % len(PALETTE)],
            'carriers': sys['carriers'],
            'labels': sys['labels'],
            'clr': [[round(v, 6) for v in row] for row in sys['clr']]
        }
        ci += 1

    manifest = {
        'projector': True,
        'title': title or 'Hˢ Analysis',
        'subtitle': subtitle or '',
        'generator': 'hs_projector_export.py v1.0',
        'systems': manifest_systems
    }

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Projector manifest written: {args.output}")
    print(f"  Systems: {len(manifest_systems)}")
    for key, sys in manifest_systems.items():
        print(f"    {key}: {sys['name']} — D={len(sys['carriers'])}, N={len(sys['clr'])}")


if __name__ == '__main__':
    main()
