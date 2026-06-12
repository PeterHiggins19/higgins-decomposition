#!/usr/bin/env python3
"""
Hˢ INSTRUMENT METROLOGY
=========================
Meta-evaluation of the Hˢ pipeline as a measurement instrument.
Evaluates the tool itself — not the data it processes.

This module scans all experiment results, generates diagnostic codes
for each, and produces instrument quality metrics:

  1. Code coverage — which codes fire, which never fire
  2. Code distribution — INF/WRN/ERR/DIS/CAL/SM balance
  3. Structural mode consistency — do modes fire appropriately
  4. Code impossibility check — logically contradictory combinations
  5. Dynamic range — instrument sensitivity across domains
  6. Noise floor calibration — false positive rate from reference standards
  7. Structural mode predictability — are modes derivable from pipeline codes
  8. Cross-domain mode coherence — structural archetypes across domains

Output: JSON metrology report + human-readable summary
Designed for ISO 17025 / GUM-style instrument qualification.

Author: Peter Higgins / Claude
Version: 1.0
"""

import json, os, sys, glob
from collections import Counter, defaultdict
from datetime import datetime

# Add pipeline to path
PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PIPELINE_DIR)

from hs_codes import generate_codes, CODE_DICTIONARY, STRUCTURAL_MODES

REPO_ROOT = os.path.abspath(os.path.join(PIPELINE_DIR, "..", ".."))
EXPERIMENTS_DIR = os.path.join(REPO_ROOT, "experiments")


def find_all_results():
    """Find all *_results.json files in the experiments directory."""
    pattern = os.path.join(EXPERIMENTS_DIR, "**", "*_results.json")
    paths = sorted(glob.glob(pattern, recursive=True))
    return paths


def load_and_generate_codes(result_path):
    """Load a result JSON and generate diagnostic codes."""
    with open(result_path, encoding='utf-8') as f:
        result = json.load(f)
    codes = generate_codes(result)
    exp_id = result.get('experiment', os.path.basename(result_path))
    domain = result.get('domain', 'UNKNOWN')
    name = result.get('name', '')
    N = result.get('N', 0)
    D = result.get('D', 0)
    return {
        'path': result_path,
        'experiment': exp_id,
        'domain': domain,
        'name': name,
        'N': N,
        'D': D,
        'codes': codes,
        'code_set': set(c['code'] for c in codes),
        'code_prefixes': set(c['code'].rsplit('-', 1)[0] for c in codes),
    }


# ════════════════════════════════════════════════════════════
# METRIC 1: CODE COVERAGE
# ════════════════════════════════════════════════════════════

def compute_code_coverage(all_experiments):
    """Which codes fire across all experiments, which never fire."""
    all_defined = set(CODE_DICTIONARY.keys())
    all_fired = set()
    fire_counts = Counter()

    for exp in all_experiments:
        for c in exp['codes']:
            all_fired.add(c['code'])
            fire_counts[c['code']] += 1

    never_fired = all_defined - all_fired
    coverage_pct = len(all_fired & all_defined) / len(all_defined) * 100

    return {
        'total_defined': len(all_defined),
        'total_fired': len(all_fired & all_defined),
        'coverage_pct': round(coverage_pct, 1),
        'never_fired': sorted(never_fired),
        'fire_counts': dict(fire_counts.most_common()),
        'most_common': fire_counts.most_common(10),
        'least_common': fire_counts.most_common()[-10:] if len(fire_counts) >= 10 else fire_counts.most_common(),
    }


# ════════════════════════════════════════════════════════════
# METRIC 2: CODE DISTRIBUTION (Dynamic Range)
# ════════════════════════════════════════════════════════════

def compute_code_distribution(all_experiments):
    """Distribution of code levels across all experiments."""
    level_counts = Counter()
    level_per_exp = defaultdict(list)

    for exp in all_experiments:
        exp_levels = Counter()
        for c in exp['codes']:
            code = c['code']
            if code.startswith('SM-'):
                level = 'SM'
            elif code.endswith('-INF'):
                level = 'INF'
            elif code.endswith('-WRN'):
                level = 'WRN'
            elif code.endswith('-ERR'):
                level = 'ERR'
            elif code.endswith('-DIS'):
                level = 'DIS'
            elif code.endswith('-CAL'):
                level = 'CAL'
            else:
                level = 'OTHER'
            level_counts[level] += 1
            exp_levels[level] += 1
        for lev in ['INF', 'WRN', 'ERR', 'DIS', 'CAL', 'SM']:
            level_per_exp[lev].append(exp_levels.get(lev, 0))

    # Compute per-level stats
    level_stats = {}
    for lev in ['INF', 'WRN', 'ERR', 'DIS', 'CAL', 'SM']:
        vals = level_per_exp[lev]
        if vals:
            level_stats[lev] = {
                'total': sum(vals),
                'mean_per_exp': round(sum(vals) / len(vals), 1),
                'min': min(vals),
                'max': max(vals),
            }

    total = sum(level_counts.values())
    distribution = {k: round(v/total*100, 1) for k, v in level_counts.items()}

    return {
        'total_codes_emitted': total,
        'distribution_pct': distribution,
        'level_stats': level_stats,
        'n_experiments': len(all_experiments),
    }


# ════════════════════════════════════════════════════════════
# METRIC 3: STRUCTURAL MODE CONSISTENCY
# ════════════════════════════════════════════════════════════

def compute_mode_consistency(all_experiments):
    """Check structural mode firing patterns for consistency."""
    mode_fires = Counter()
    mode_experiments = defaultdict(list)

    for exp in all_experiments:
        sm_codes = [c['code'] for c in exp['codes'] if c['code'].startswith('SM-')]
        for sm in sm_codes:
            mode_fires[sm] += 1
            mode_experiments[sm].append(exp['experiment'])

    # Check which modes never fire
    all_modes = set(m['mode'] for m in STRUCTURAL_MODES)
    fired_modes = set(mode_fires.keys())
    never_fired = all_modes - fired_modes

    return {
        'total_modes_defined': len(all_modes),
        'modes_fired': len(fired_modes),
        'mode_fire_counts': dict(mode_fires.most_common()),
        'mode_experiments': {k: v for k, v in mode_experiments.items()},
        'never_fired': sorted(never_fired),
    }


# ════════════════════════════════════════════════════════════
# METRIC 4: CODE IMPOSSIBILITY CHECK
# ════════════════════════════════════════════════════════════

def compute_impossibility_check(all_experiments):
    """Check for logically contradictory code combinations."""
    # Define impossible pairs (codes that should never co-occur)
    IMPOSSIBLE_PAIRS = [
        ('S7-BWL-INF', 'S7-HIL-INF', 'Cannot be both bowl and hill'),
        ('S8-NAT-INF', 'S8-FLG-WRN', 'Cannot be both NATURAL and FLAG'),
        ('S8-NAT-INF', 'S8-INV-WRN', 'Cannot be both NATURAL and INVESTIGATE'),
        ('S8-INV-WRN', 'S8-FLG-WRN', 'Cannot be both INVESTIGATE and FLAG'),
        ('S9-EIT-INF', 'S9-EIF-WRN', 'Cannot both pass and fail EITT'),
        ('S9-CHS-INF', 'S9-CHH-DIS', 'Cannot be both low and high chaos'),
        ('S4-ZRP-INF', 'S4-ZRN-INF', 'Cannot both apply and not apply zero replacement'),
        ('SM-SCG-INF', 'SM-BPO-DIS', 'Smooth convergence contradicts bimodal population'),
        ('SM-SCG-INF', 'SM-TNT-DIS', 'Smooth convergence contradicts turbulent natural'),
        ('SM-MCA-WRN', 'SM-OVC-CAL', 'Missing carrier contradicts overconstrained'),
        ('XU-DRI-INF', 'XU-DRU-DIS', 'Cannot be both stable and increasing drift'),
        ('XU-DRI-INF', 'XU-DRD-DIS', 'Cannot be both stable and decreasing drift'),
        ('XU-DRU-DIS', 'XU-DRD-DIS', 'Cannot be both increasing and decreasing drift'),
    ]

    violations = []
    for exp in all_experiments:
        code_set = exp['code_set']
        for a, b, reason in IMPOSSIBLE_PAIRS:
            if a in code_set and b in code_set:
                violations.append({
                    'experiment': exp['experiment'],
                    'code_a': a,
                    'code_b': b,
                    'reason': reason,
                })

    return {
        'pairs_checked': len(IMPOSSIBLE_PAIRS),
        'violations_found': len(violations),
        'violations': violations,
        'status': 'PASS' if len(violations) == 0 else 'FAIL',
    }


# ════════════════════════════════════════════════════════════
# METRIC 5: DYNAMIC RANGE
# ════════════════════════════════════════════════════════════

def compute_dynamic_range(all_experiments):
    """Measure the instrument's ability to discriminate across domains."""
    domain_profiles = defaultdict(list)

    for exp in all_experiments:
        domain = exp['domain']
        profile = {
            'experiment': exp['experiment'],
            'n_codes': len(exp['codes']),
            'n_warnings': sum(1 for c in exp['codes'] if c['code'].endswith('-WRN')),
            'n_discoveries': sum(1 for c in exp['codes'] if c['code'].endswith('-DIS')),
            'n_structural': sum(1 for c in exp['codes'] if c['code'].startswith('SM-')),
            'has_euler': any(c['code'] == 'S8-EUL-DIS' for c in exp['codes']),
            'classification': 'NATURAL' if any(c['code'] == 'S8-NAT-INF' for c in exp['codes'])
                else 'INVESTIGATE' if any(c['code'] == 'S8-INV-WRN' for c in exp['codes'])
                else 'FLAG',
            'hvld_shape': 'bowl' if any(c['code'] == 'S7-BWL-INF' for c in exp['codes']) else 'hill',
        }
        domain_profiles[domain].append(profile)

    # Compute discrimination metrics
    classifications = Counter()
    shapes = Counter()
    for exp in all_experiments:
        for c in exp['codes']:
            if c['code'] in ('S8-NAT-INF', 'S8-INV-WRN', 'S8-FLG-WRN'):
                classifications[c['code']] += 1
            if c['code'] in ('S7-BWL-INF', 'S7-HIL-INF'):
                shapes[c['code']] += 1

    total_exps = len(all_experiments)
    code_range = [len(exp['codes']) for exp in all_experiments]

    return {
        'n_domains': len(domain_profiles),
        'n_experiments': total_exps,
        'classification_distribution': dict(classifications),
        'shape_distribution': dict(shapes),
        'codes_per_experiment': {
            'min': min(code_range),
            'max': max(code_range),
            'mean': round(sum(code_range) / len(code_range), 1),
        },
        'domain_profiles': {d: profiles for d, profiles in domain_profiles.items()},
    }


# ════════════════════════════════════════════════════════════
# METRIC 6: NOISE FLOOR CALIBRATION
# ════════════════════════════════════════════════════════════

def compute_noise_floor(all_experiments):
    """Identify noise floor from reference standards and synthetic data."""
    ref_exps = [e for e in all_experiments
                if 'reference' in e['experiment'].lower()
                or 'REF' in e['experiment']
                or e['domain'] == 'REFERENCE']

    # Also look for known synthetic/simulated results
    synthetic_exps = []
    natural_exps = []
    for exp in all_experiments:
        has_nat = any(c['code'] == 'S8-NAT-INF' for c in exp['codes'])
        has_flg = any(c['code'] == 'S8-FLG-WRN' for c in exp['codes'])
        if has_flg:
            synthetic_exps.append(exp['experiment'])
        elif has_nat:
            natural_exps.append(exp['experiment'])

    return {
        'reference_experiments': len(ref_exps),
        'natural_count': len(natural_exps),
        'flag_count': len(synthetic_exps),
        'natural_experiments': natural_exps,
        'flag_experiments': synthetic_exps,
        'natural_rate': round(len(natural_exps) / max(len(all_experiments), 1) * 100, 1),
    }


# ════════════════════════════════════════════════════════════
# METRIC 7: STRUCTURAL MODE PREDICTABILITY
# ════════════════════════════════════════════════════════════

def compute_mode_predictability(all_experiments):
    """Can pipeline codes predict which structural modes will fire?

    For each experiment, use only pipeline codes (non-SM) to predict
    SM codes. Measure prediction accuracy.
    """
    predictions = []

    for exp in all_experiments:
        pipeline_codes = set(c['code'] for c in exp['codes'] if not c['code'].startswith('SM-'))
        pipeline_prefixes = set(c.rsplit('-', 1)[0] for c in pipeline_codes)
        actual_sm = set(c['code'] for c in exp['codes'] if c['code'].startswith('SM-'))

        # Predict SM codes using the same logic as generate_codes
        predicted_sm = set()
        for mode in STRUCTURAL_MODES:
            required = mode.get('requires', [])
            req_any = mode.get('requires_any', [])
            forbidden = mode.get('forbids', [])

            if not all(r in pipeline_prefixes for r in required):
                continue
            if req_any and not any(r in pipeline_prefixes for r in req_any):
                continue
            if any(f in pipeline_prefixes for f in forbidden):
                continue
            predicted_sm.add(mode['mode'])

        correct = actual_sm == predicted_sm
        predictions.append({
            'experiment': exp['experiment'],
            'actual': sorted(actual_sm),
            'predicted': sorted(predicted_sm),
            'match': correct,
            'missing': sorted(actual_sm - predicted_sm),
            'extra': sorted(predicted_sm - actual_sm),
        })

    n_correct = sum(1 for p in predictions if p['match'])
    accuracy = round(n_correct / max(len(predictions), 1) * 100, 1)

    # Mismatches reveal where modes use information beyond prefixes
    mismatches = [p for p in predictions if not p['match']]

    return {
        'n_experiments': len(predictions),
        'n_correct': n_correct,
        'accuracy_pct': accuracy,
        'mismatches': mismatches,
        'status': 'DERIVABLE' if accuracy > 95 else 'EMERGENT' if accuracy < 70 else 'MIXED',
    }


# ════════════════════════════════════════════════════════════
# METRIC 8: CROSS-DOMAIN MODE COHERENCE
# ════════════════════════════════════════════════════════════

def compute_mode_coherence(all_experiments):
    """Find structural archetypes — domains that share mode combinations."""
    # Build mode signature per experiment
    signatures = {}
    for exp in all_experiments:
        sm_codes = tuple(sorted(c['code'] for c in exp['codes'] if c['code'].startswith('SM-')))
        key = sm_codes if sm_codes else ('(none)',)
        if key not in signatures:
            signatures[key] = []
        signatures[key].append({
            'experiment': exp['experiment'],
            'domain': exp['domain'],
            'name': exp['name'],
        })

    # Convert to list for JSON
    archetypes = []
    for sig, members in sorted(signatures.items(), key=lambda x: -len(x[1])):
        domains = set(m['domain'] for m in members)
        archetypes.append({
            'signature': list(sig),
            'n_experiments': len(members),
            'n_domains': len(domains),
            'domains': sorted(domains),
            'experiments': [m['experiment'] for m in members],
            'cross_domain': len(domains) > 1,
        })

    cross_domain = [a for a in archetypes if a['cross_domain']]

    return {
        'n_archetypes': len(archetypes),
        'n_cross_domain': len(cross_domain),
        'archetypes': archetypes,
    }


# ════════════════════════════════════════════════════════════
# MASTER EVALUATION
# ════════════════════════════════════════════════════════════

def run_full_metrology():
    """Run all 8 metrology metrics and produce the instrument evaluation."""
    print("=" * 70)
    print("  Hˢ INSTRUMENT METROLOGY — META-EVALUATION REPORT")
    print("=" * 70)
    print(f"  Date: {datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}")
    print(f"  Code dictionary: {len(CODE_DICTIONARY)} codes")
    print(f"  Structural modes: {len(STRUCTURAL_MODES)} modes")
    print()

    # Load all experiments
    result_paths = find_all_results()
    print(f"  Scanning: {len(result_paths)} result files in {EXPERIMENTS_DIR}")

    all_experiments = []
    errors = []
    for path in result_paths:
        try:
            exp = load_and_generate_codes(path)
            all_experiments.append(exp)
        except Exception as e:
            errors.append({'path': path, 'error': str(e)})

    print(f"  Loaded: {len(all_experiments)} experiments ({len(errors)} errors)")
    if errors:
        for e in errors:
            print(f"    ERROR: {e['path']}: {e['error']}")
    print()

    # Run all metrics
    print("─" * 70)
    print("  METRIC 1: CODE COVERAGE")
    print("─" * 70)
    m1 = compute_code_coverage(all_experiments)
    print(f"  Defined: {m1['total_defined']} codes")
    print(f"  Fired:   {m1['total_fired']} codes ({m1['coverage_pct']}%)")
    if m1['never_fired']:
        print(f"  Never fired ({len(m1['never_fired'])}):")
        for c in m1['never_fired']:
            print(f"    {c}: {CODE_DICTIONARY.get(c, {}).get('short', '?')}")
    print()

    print("─" * 70)
    print("  METRIC 2: CODE DISTRIBUTION (Dynamic Range)")
    print("─" * 70)
    m2 = compute_code_distribution(all_experiments)
    print(f"  Total codes emitted: {m2['total_codes_emitted']} across {m2['n_experiments']} experiments")
    for lev, pct in sorted(m2['distribution_pct'].items()):
        stats = m2['level_stats'].get(lev, {})
        print(f"    {lev:4s}: {pct:5.1f}% (mean {stats.get('mean_per_exp',0):.1f}/exp, range {stats.get('min',0)}-{stats.get('max',0)})")
    print()

    print("─" * 70)
    print("  METRIC 3: STRUCTURAL MODE CONSISTENCY")
    print("─" * 70)
    m3 = compute_mode_consistency(all_experiments)
    print(f"  Defined: {m3['total_modes_defined']} modes")
    print(f"  Fired:   {m3['modes_fired']} modes")
    for mode, count in m3['mode_fire_counts'].items():
        exps = m3['mode_experiments'][mode]
        print(f"    {mode}: {count}× ({', '.join(exps[:4])}{'...' if len(exps)>4 else ''})")
    if m3['never_fired']:
        print(f"  Never fired: {', '.join(m3['never_fired'])}")
    print()

    print("─" * 70)
    print("  METRIC 4: IMPOSSIBILITY CHECK")
    print("─" * 70)
    m4 = compute_impossibility_check(all_experiments)
    print(f"  Pairs checked: {m4['pairs_checked']}")
    print(f"  Violations: {m4['violations_found']}")
    print(f"  Status: {m4['status']}")
    if m4['violations']:
        for v in m4['violations']:
            print(f"    ✗ {v['experiment']}: {v['code_a']} + {v['code_b']} — {v['reason']}")
    print()

    print("─" * 70)
    print("  METRIC 5: DYNAMIC RANGE")
    print("─" * 70)
    m5 = compute_dynamic_range(all_experiments)
    print(f"  Domains: {m5['n_domains']}")
    print(f"  Experiments: {m5['n_experiments']}")
    print(f"  Codes/experiment: {m5['codes_per_experiment']['min']}-{m5['codes_per_experiment']['max']} (mean {m5['codes_per_experiment']['mean']})")
    for cls, cnt in m5['classification_distribution'].items():
        label = cls.split('-')[1]
        print(f"    {label}: {cnt}")
    for shp, cnt in m5['shape_distribution'].items():
        label = 'bowl' if 'BWL' in shp else 'hill'
        print(f"    HVLD {label}: {cnt}")
    print()

    print("─" * 70)
    print("  METRIC 6: NOISE FLOOR")
    print("─" * 70)
    m6 = compute_noise_floor(all_experiments)
    print(f"  NATURAL: {m6['natural_count']} ({m6['natural_rate']}%)")
    print(f"  FLAG:    {m6['flag_count']}")
    if m6['flag_experiments']:
        print(f"  FLAG experiments: {', '.join(m6['flag_experiments'])}")
    print()

    print("─" * 70)
    print("  METRIC 7: STRUCTURAL MODE PREDICTABILITY")
    print("─" * 70)
    m7 = compute_mode_predictability(all_experiments)
    print(f"  Prediction accuracy: {m7['accuracy_pct']}% ({m7['n_correct']}/{m7['n_experiments']})")
    print(f"  Status: {m7['status']}")
    if m7['mismatches']:
        for mm in m7['mismatches'][:5]:
            print(f"    {mm['experiment']}: actual={mm['actual']}, predicted={mm['predicted']}")
            if mm['missing']: print(f"      missing: {mm['missing']}")
            if mm['extra']: print(f"      extra: {mm['extra']}")
    print()

    print("─" * 70)
    print("  METRIC 8: CROSS-DOMAIN MODE COHERENCE")
    print("─" * 70)
    m8 = compute_mode_coherence(all_experiments)
    print(f"  Structural archetypes: {m8['n_archetypes']}")
    print(f"  Cross-domain archetypes: {m8['n_cross_domain']}")
    for arch in m8['archetypes']:
        sig = ', '.join(arch['signature'])
        print(f"    [{sig}]")
        print(f"      {arch['n_experiments']} experiments, {arch['n_domains']} domains: {', '.join(arch['domains'])}")
    print()

    # ── SUMMARY VERDICT ──
    print("=" * 70)
    print("  INSTRUMENT QUALIFICATION SUMMARY")
    print("=" * 70)

    verdicts = []
    verdicts.append(('Code coverage', f"{m1['coverage_pct']}%", 'PASS' if m1['coverage_pct'] > 70 else 'REVIEW'))
    verdicts.append(('Impossibility check', f"{m4['violations_found']} violations", m4['status']))
    verdicts.append(('Mode predictability', f"{m7['accuracy_pct']}%", 'PASS' if m7['accuracy_pct'] > 80 else 'REVIEW'))
    verdicts.append(('Dynamic range', f"{m5['codes_per_experiment']['min']}-{m5['codes_per_experiment']['max']} codes/exp", 'PASS' if m5['codes_per_experiment']['max'] - m5['codes_per_experiment']['min'] > 10 else 'REVIEW'))
    verdicts.append(('Cross-domain coherence', f"{m8['n_cross_domain']} archetypes", 'PASS' if m8['n_cross_domain'] > 0 else 'REVIEW'))
    verdicts.append(('Mode coverage', f"{m3['modes_fired']}/{m3['total_modes_defined']}", 'PASS' if m3['modes_fired'] > m3['total_modes_defined'] * 0.5 else 'REVIEW'))

    all_pass = True
    for name, value, status in verdicts:
        symbol = '✓' if status == 'PASS' else '✗' if status == 'FAIL' else '◎'
        print(f"  {symbol} {name:30s} {value:25s} {status}")
        if status == 'FAIL':
            all_pass = False

    overall = 'QUALIFIED' if all_pass else 'REQUIRES REVIEW'
    print()
    print(f"  Overall: {overall}")
    print(f"  Experiments evaluated: {len(all_experiments)}")
    print(f"  Domains covered: {m5['n_domains']}")
    print(f"  Codes defined: {m1['total_defined']}")
    print(f"  Structural modes: {m3['total_modes_defined']}")
    print()

    # Build full report dict
    report = {
        'metrology_version': '1.0',
        'timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'pipeline_codes_defined': m1['total_defined'],
        'structural_modes_defined': m3['total_modes_defined'],
        'experiments_evaluated': len(all_experiments),
        'load_errors': len(errors),
        'metrics': {
            'code_coverage': m1,
            'code_distribution': m2,
            'mode_consistency': m3,
            'impossibility_check': m4,
            'dynamic_range': m5,
            'noise_floor': m6,
            'mode_predictability': m7,
            'mode_coherence': m8,
        },
        'verdicts': [{'metric': v[0], 'value': v[1], 'status': v[2]} for v in verdicts],
        'overall': overall,
    }

    return report


if __name__ == "__main__":
    report = run_full_metrology()

    # Save JSON report
    out_path = os.path.join(REPO_ROOT, "docs", "reference", "Hs_Instrument_Metrology.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    print(f"  Report saved: {out_path}")

    print()
    print("─" * 70)
    print("  Hˢ — The instrument reads. The metrology reads the instrument.")
    print("─" * 70)
