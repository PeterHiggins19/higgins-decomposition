#!/usr/bin/env python3
"""
Hˢ COMPOSITIONAL FINGERPRINT GENERATOR
========================================
Generates a compact, deterministic signature file for any Hˢ pipeline result.

The fingerprint captures the compositional identity of a system — its geometric
shape on the simplex, its structural mode pattern, and its transcendental
resonance. Two systems with the same fingerprint are compositionally equivalent,
regardless of domain, scale, or carrier meaning.

Usage:
    python hs_fingerprint.py results.json                    # Single result
    python hs_fingerprint.py results.json -o fingerprint.json # Custom output
    python hs_fingerprint.py --catalog /path/to/hep_validation # All catalog runs
    python hs_fingerprint.py --compare fp1.json fp2.json      # Compare two
    python hs_fingerprint.py --match fp.json --database /path  # Find matches

Author: Peter Higgins / Claude
Version: 1.0
"""

import json
import hashlib
import os
import sys
import argparse
from datetime import datetime, timezone


# ════════════════════════════════════════════════════════════
# FINGERPRINT SCHEMA
# ════════════════════════════════════════════════════════════

def r2_band(r2):
    """Classify R² into bands for fingerprint matching."""
    if r2 is None:
        return "NONE"
    if r2 >= 0.9:
        return "PRECISION"   # R² ≥ 0.9
    if r2 >= 0.7:
        return "STRONG"      # 0.7 ≤ R² < 0.9
    if r2 >= 0.5:
        return "MODERATE"    # 0.5 ≤ R² < 0.7
    return "WEAK"            # R² < 0.5


def constant_family(constant_name):
    """Map a constant to its mathematical family."""
    if constant_name is None:
        return "NONE"

    name = str(constant_name).lower()

    # Euler family
    euler = ['2pi', 'e^pi', 'pi^e', '1/(2pi)', '1/(e^pi)', '1/(pi^e)',
             'pi', 'e', 'pi/4', 'pi/2', '1/pi', '1/e']
    if any(e in name for e in euler):
        return "EULER"

    # Zeta family
    if 'pi^2/6' in name or 'zeta' in name or 'apery' in name or "pi^2" in name:
        return "ZETA"

    # Golden family
    if 'phi' in name or 'golden' in name or 'phi^2' in name:
        return "GOLDEN"

    # Khinchin family
    if 'khinchin' in name:
        return "KHINCHIN"

    # Lambert family
    if 'lambert' in name or 'omega' in name:
        return "LAMBERT"

    # Feigenbaum
    if 'feigenbaum' in name:
        return "FEIGENBAUM"

    # Logarithmic
    if 'ln' in name or 'log' in name:
        return "LOGARITHMIC"

    # Catalan, Dottie, Glaisher
    if 'catalan' in name:
        return "CATALAN"
    if 'dottie' in name:
        return "DOTTIE"
    if 'glaisher' in name:
        return "GLAISHER"

    return "OTHER"


def extract_fingerprint(result, name=None, domain=None):
    """
    Extract a compositional fingerprint from an Hˢ pipeline result.

    Parameters
    ----------
    result : dict
        Output from HigginsDecomposition.run_full_extended() or a results.json file.
    name : str, optional
        System name override.
    domain : str, optional
        Domain override.

    Returns
    -------
    dict : The fingerprint document.
    """
    steps = result.get('steps', {})
    ext = result.get('extended', {})
    univ = ext.get('universal', {})
    cond = ext.get('conditional', {})

    # Core geometry
    shape = steps.get('step6_pll_shape', None)
    r2 = steps.get('step6_pll_R2', None)
    vertex = steps.get('step6_vertex', None)

    # Classification
    sq = steps.get('step7_squeeze_closest', {})
    nearest_const = sq.get('constant', None) if sq else None
    delta = sq.get('delta', None) if sq else None

    if delta is not None:
        if delta < 0.01:
            classification = "NATURAL"
        elif delta < 0.05:
            classification = "INVESTIGATE"
        else:
            classification = "FLAG"
    else:
        classification = "FLAG"

    # EITT
    eitt = steps.get('step8_eitt_invariance', {})
    eitt_pass = all(v.get('pass', False) for v in eitt.values()) if eitt else None

    # Structural modes (from codes if available, otherwise from result)
    sm_codes = result.get('structural_modes', [])
    if not sm_codes and ext.get('codes'):
        sm_codes = [c['code'] for c in ext['codes'] if c['code'].startswith('SM-')]

    # Carrier count
    D = result.get('D', steps.get('step1_D', None))
    N = result.get('N', steps.get('step1_N', None))

    # Chaos profile
    chaos = steps.get('step9_chaos_detection', {})
    stalls = chaos.get('stalls', 0)
    spikes = chaos.get('spikes', 0)
    reversals = chaos.get('reversals', 0)
    total_dev = chaos.get('total_deviations', 0)

    # Entropy
    entropy_mean = steps.get('step8_entropy_mean', None)

    # Per-carrier dominance
    pcc = univ.get('per_carrier_contribution', {})
    dominant_pct = pcc.get('dominant_pct', None)

    # Drift
    drift = univ.get('carrier_drift', {})
    drift_dir = drift.get('drift_direction', None)

    # Build fingerprint vector — deterministic, hashable
    fp_vector = {
        "shape": shape,
        "r2_band": r2_band(r2),
        "classification": classification,
        "constant_family": constant_family(nearest_const),
        "eitt": "PASS" if eitt_pass else ("FAIL" if eitt_pass is not None else "UNKNOWN"),
        "structural_modes": sorted(sm_codes) if sm_codes else [],
        "chaos_level": "HIGH" if total_dev >= 10 else "LOW",
        "drift": drift_dir or "unknown",
        "D": D,
    }

    # Generate hash from the fingerprint vector
    fp_string = json.dumps(fp_vector, sort_keys=True)
    fp_hash = hashlib.sha256(fp_string.encode()).hexdigest()[:16]

    # Build full fingerprint document
    fingerprint = {
        "_type": "Hs_FINGERPRINT",
        "_version": "1.0",
        "_generated": datetime.now(timezone.utc).isoformat(),

        "identity": {
            "name": name or result.get('name', 'Unknown'),
            "domain": domain or result.get('domain', 'Unknown'),
            "N": N,
            "D": D,
        },

        "fingerprint": {
            "hash": fp_hash,
            "vector": fp_vector,
        },

        "geometry": {
            "hvld_shape": shape,
            "hvld_r2": r2,
            "r2_band": r2_band(r2),
            "vertex": vertex,
        },

        "classification": {
            "status": classification,
            "nearest_constant": nearest_const,
            "delta": delta,
            "constant_family": constant_family(nearest_const),
        },

        "entropy": {
            "eitt_pass": eitt_pass,
            "entropy_mean": entropy_mean,
            "chaos_profile": {
                "stalls": stalls,
                "spikes": spikes,
                "reversals": reversals,
                "total_deviations": total_dev,
            },
        },

        "structure": {
            "structural_modes": sorted(sm_codes) if sm_codes else [],
            "mode_count": len(sm_codes),
            "dominant_carrier_pct": dominant_pct,
            "drift_direction": drift_dir,
        },
    }

    return fingerprint


def compare_fingerprints(fp1, fp2):
    """
    Compare two fingerprints and return a similarity report.

    Returns
    -------
    dict with:
        - match: bool (True if hashes are identical)
        - similarity: float 0-1 (structural similarity score)
        - differences: list of specific differences
        - shared_modes: list of structural modes in common
    """
    v1 = fp1['fingerprint']['vector']
    v2 = fp2['fingerprint']['vector']

    exact_match = fp1['fingerprint']['hash'] == fp2['fingerprint']['hash']

    # Score each dimension
    score = 0
    max_score = 0
    differences = []

    # Shape (weight 2)
    max_score += 2
    if v1['shape'] == v2['shape']:
        score += 2
    else:
        differences.append(f"shape: {v1['shape']} vs {v2['shape']}")

    # R² band (weight 2)
    max_score += 2
    if v1['r2_band'] == v2['r2_band']:
        score += 2
    else:
        differences.append(f"r2_band: {v1['r2_band']} vs {v2['r2_band']}")

    # Classification (weight 3)
    max_score += 3
    if v1['classification'] == v2['classification']:
        score += 3
    else:
        differences.append(f"classification: {v1['classification']} vs {v2['classification']}")

    # Constant family (weight 2)
    max_score += 2
    if v1['constant_family'] == v2['constant_family']:
        score += 2
    else:
        differences.append(f"constant_family: {v1['constant_family']} vs {v2['constant_family']}")

    # EITT (weight 2)
    max_score += 2
    if v1['eitt'] == v2['eitt']:
        score += 2
    else:
        differences.append(f"eitt: {v1['eitt']} vs {v2['eitt']}")

    # Chaos level (weight 1)
    max_score += 1
    if v1['chaos_level'] == v2['chaos_level']:
        score += 1
    else:
        differences.append(f"chaos: {v1['chaos_level']} vs {v2['chaos_level']}")

    # Drift (weight 1)
    max_score += 1
    if v1['drift'] == v2['drift']:
        score += 1
    else:
        differences.append(f"drift: {v1['drift']} vs {v2['drift']}")

    # Structural modes (weight 3 — Jaccard similarity)
    max_score += 3
    modes1 = set(v1.get('structural_modes', []))
    modes2 = set(v2.get('structural_modes', []))
    shared_modes = modes1 & modes2
    all_modes = modes1 | modes2
    if all_modes:
        jaccard = len(shared_modes) / len(all_modes)
        score += 3 * jaccard
        if modes1 != modes2:
            differences.append(f"modes: {sorted(modes1)} vs {sorted(modes2)}")
    else:
        score += 3  # Both empty = match

    similarity = score / max_score if max_score > 0 else 0

    return {
        "exact_match": exact_match,
        "similarity": round(similarity, 4),
        "score": round(score, 2),
        "max_score": max_score,
        "differences": differences,
        "shared_modes": sorted(shared_modes),
        "systems": [
            f"{fp1['identity']['name']} ({fp1['identity']['domain']})",
            f"{fp2['identity']['name']} ({fp2['identity']['domain']})",
        ],
    }


def find_matches(target_fp, database_dir, threshold=0.7):
    """
    Search a catalog directory for fingerprint matches above threshold.

    Parameters
    ----------
    target_fp : dict
        The fingerprint to match against.
    database_dir : str
        Path to a catalog directory containing numbered run folders.
    threshold : float
        Minimum similarity score (0-1) to include in results.

    Returns
    -------
    list of (similarity, fingerprint, comparison) tuples, sorted by similarity desc.
    """
    matches = []

    # Look for fingerprint.json files in subdirectories
    for entry in sorted(os.listdir(database_dir)):
        fp_path = os.path.join(database_dir, entry, 'fingerprint.json')
        if os.path.isfile(fp_path):
            with open(fp_path) as f:
                candidate = json.load(f)
            comp = compare_fingerprints(target_fp, candidate)
            if comp['similarity'] >= threshold:
                matches.append((comp['similarity'], candidate, comp))

    # Also check for results.json files and generate fingerprints on the fly
    for entry in sorted(os.listdir(database_dir)):
        results_path = os.path.join(database_dir, entry, 'results.json')
        fp_path = os.path.join(database_dir, entry, 'fingerprint.json')
        if os.path.isfile(results_path) and not os.path.isfile(fp_path):
            with open(results_path) as f:
                result = json.load(f)
            # Try to get name/domain from metadata
            meta_path = os.path.join(database_dir, entry, 'metadata.json')
            name = domain = None
            if os.path.isfile(meta_path):
                with open(meta_path) as f:
                    meta = json.load(f)
                name = meta.get('name')
                domain = meta.get('domain')
            candidate = extract_fingerprint(result, name=name, domain=domain)
            comp = compare_fingerprints(target_fp, candidate)
            if comp['similarity'] >= threshold:
                matches.append((comp['similarity'], candidate, comp))

    matches.sort(key=lambda x: x[0], reverse=True)
    return matches


def generate_catalog_fingerprints(catalog_dir):
    """
    Generate fingerprint.json for every run in a catalog directory.

    Parameters
    ----------
    catalog_dir : str
        Path to catalog root (containing numbered subdirectories).

    Returns
    -------
    int : Number of fingerprints generated.
    """
    count = 0
    for entry in sorted(os.listdir(catalog_dir)):
        run_dir = os.path.join(catalog_dir, entry)
        results_path = os.path.join(run_dir, 'results.json')
        if not os.path.isfile(results_path):
            continue

        with open(results_path) as f:
            result = json.load(f)

        # Get metadata
        name = domain = None
        meta_path = os.path.join(run_dir, 'metadata.json')
        if os.path.isfile(meta_path):
            with open(meta_path) as f:
                meta = json.load(f)
            name = meta.get('name')
            domain = meta.get('domain')

        fp = extract_fingerprint(result, name=name, domain=domain)

        fp_path = os.path.join(run_dir, 'fingerprint.json')
        with open(fp_path, 'w') as f:
            json.dump(fp, f, indent=2)

        h = fp['fingerprint']['hash']
        cls = fp['classification']['status']
        print(f"  [{entry}] {name or 'Unknown'}: {h} ({cls})")
        count += 1

    return count


def print_fingerprint(fp):
    """Pretty-print a fingerprint to stdout."""
    ident = fp['identity']
    geom = fp['geometry']
    cls = fp['classification']
    ent = fp['entropy']
    struct = fp['structure']

    print(f"\n{'=' * 60}")
    print(f"Hˢ COMPOSITIONAL FINGERPRINT")
    print(f"{'=' * 60}")
    print(f"System:          {ident['name']}")
    print(f"Domain:          {ident['domain']}")
    print(f"Dimensions:      N={ident['N']}, D={ident['D']}")
    print(f"Hash:            {fp['fingerprint']['hash']}")
    print(f"{'─' * 60}")
    print(f"HVLD Shape:      {geom['hvld_shape']}")
    print(f"HVLD R²:         {geom['hvld_r2']}")
    print(f"R² Band:         {geom['r2_band']}")
    print(f"{'─' * 60}")
    print(f"Classification:  {cls['status']}")
    print(f"Nearest Const:   {cls['nearest_constant']}")
    print(f"Delta:           {cls['delta']}")
    print(f"Const Family:    {cls['constant_family']}")
    print(f"{'─' * 60}")
    print(f"EITT:            {'PASS' if ent['eitt_pass'] else 'FAIL'}")
    chaos = ent['chaos_profile']
    print(f"Chaos:           {chaos['total_deviations']} deviations "
          f"({chaos['stalls']}S {chaos['spikes']}K {chaos['reversals']}R)")
    print(f"{'─' * 60}")
    print(f"Modes ({struct['mode_count']}):      {', '.join(struct['structural_modes']) or 'none'}")
    print(f"Dominant Carrier: {struct['dominant_carrier_pct']}%")
    print(f"Drift:           {struct['drift_direction']}")
    print(f"{'=' * 60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Hˢ Compositional Fingerprint Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python hs_fingerprint.py results.json
  python hs_fingerprint.py results.json -o fingerprint.json
  python hs_fingerprint.py --catalog /path/to/hep_validation
  python hs_fingerprint.py --compare fp1.json fp2.json
  python hs_fingerprint.py --match fp.json --database /path/to/catalog
        """
    )
    parser.add_argument('input', nargs='?', help='Path to results.json file')
    parser.add_argument('-o', '--output', help='Output fingerprint file path')
    parser.add_argument('--catalog', help='Generate fingerprints for all runs in a catalog directory')
    parser.add_argument('--compare', nargs=2, metavar=('FP1', 'FP2'),
                        help='Compare two fingerprint files')
    parser.add_argument('--match', help='Find matches for a fingerprint in a database')
    parser.add_argument('--database', help='Catalog directory to search for matches')
    parser.add_argument('--threshold', type=float, default=0.7,
                        help='Minimum similarity threshold for matching (default: 0.7)')
    parser.add_argument('--name', help='System name override')
    parser.add_argument('--domain', help='Domain override')

    args = parser.parse_args()

    # Mode: Generate fingerprints for entire catalog
    if args.catalog:
        print(f"Generating fingerprints for catalog: {args.catalog}")
        count = generate_catalog_fingerprints(args.catalog)
        print(f"\nGenerated {count} fingerprints.")
        return

    # Mode: Compare two fingerprints
    if args.compare:
        with open(args.compare[0]) as f:
            fp1 = json.load(f)
        with open(args.compare[1]) as f:
            fp2 = json.load(f)

        comp = compare_fingerprints(fp1, fp2)

        print(f"\n{'=' * 60}")
        print(f"FINGERPRINT COMPARISON")
        print(f"{'=' * 60}")
        print(f"System 1: {comp['systems'][0]}")
        print(f"System 2: {comp['systems'][1]}")
        print(f"{'─' * 60}")
        print(f"Exact match:  {'YES' if comp['exact_match'] else 'NO'}")
        print(f"Similarity:   {comp['similarity']:.1%} ({comp['score']}/{comp['max_score']})")
        if comp['shared_modes']:
            print(f"Shared modes: {', '.join(comp['shared_modes'])}")
        if comp['differences']:
            print(f"{'─' * 60}")
            print("Differences:")
            for d in comp['differences']:
                print(f"  - {d}")
        print(f"{'=' * 60}\n")
        return

    # Mode: Find matches in database
    if args.match:
        if not args.database:
            print("Error: --database required with --match")
            sys.exit(1)

        with open(args.match) as f:
            target = json.load(f)

        print(f"\nSearching for matches (threshold: {args.threshold:.0%})...")
        matches = find_matches(target, args.database, args.threshold)

        if not matches:
            print("No matches found above threshold.")
        else:
            print(f"\nFound {len(matches)} match(es):\n")
            for sim, fp, comp in matches:
                name = fp['identity']['name']
                domain = fp['identity']['domain']
                print(f"  {sim:.1%}  {name} ({domain})")
                if comp['shared_modes']:
                    print(f"         Shared modes: {', '.join(comp['shared_modes'])}")
                if comp['differences']:
                    print(f"         Differs: {', '.join(comp['differences'][:3])}")
                print()
        return

    # Mode: Generate single fingerprint
    if not args.input:
        parser.print_help()
        sys.exit(1)

    with open(args.input) as f:
        result = json.load(f)

    fp = extract_fingerprint(result, name=args.name, domain=args.domain)
    print_fingerprint(fp)

    # Save if output specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(fp, f, indent=2)
        print(f"Fingerprint saved to: {args.output}")
    else:
        # Default: save alongside input
        base = os.path.splitext(args.input)[0]
        out_path = base + '_fingerprint.json'
        with open(out_path, 'w') as f:
            json.dump(fp, f, indent=2)
        print(f"Fingerprint saved to: {out_path}")


if __name__ == "__main__":
    main()
