#!/usr/bin/env python3
"""
Hˢ SUBCOMPOSITIONAL RECURSION ENGINE — T2 Test Tool
====================================================
Amalgamation rerun: regroups carriers into every meaningful subcomposition,
reruns core pipeline diagnostics on each, and maps which attractors (black
holes) and repellers (white holes) appear, vanish, or persist at each
grouping level.

The black hole for one compositional group is invisible from inside
another group. This engine makes the invisible visible.

Author: Peter Higgins / Claude
Date: 2026-04-27
Version: 1.0

Tier: T2 test engine (independently verifiable, extends core pipeline)

Theory:
  Given D carriers, the engine generates all non-trivial amalgamations:
  - Level 0: Full D-carrier system (no amalgamation)
  - Level 1: All (D choose 2) pairwise merges → (D-1)-carrier systems
  - Level 2: All (D choose 3) triple merges → (D-2)-carrier systems
  - ...down to D=2 (minimum for simplex)

  For each subcomposition, the engine computes:
  1. Simplex closure
  2. CLR transform
  3. Aitchison variance trajectory
  4. HVLD shape (bowl/hill)
  5. Ratio-pair stability (CV for all pairs)
  6. Super squeeze (transcendental proximity)
  7. Shannon entropy + EITT invariance

  The duality map records:
  - BLACK HOLE: ratio pairs with CV < 0.01 (locked, attractor)
  - GREY ZONE:  ratio pairs with 0.01 ≤ CV < 0.50
  - WHITE HOLE: ratio pairs with CV ≥ 0.50 (volatile, repeller)

  Attractors that survive all levels of amalgamation are DEEP STRUCTURE.
  Attractors that vanish under amalgamation are SUBCOMPOSITIONAL.

Usage:
  from hs_amalgamation import SubcompositionalRecursion
  engine = SubcompositionalRecursion()
  result = engine.run("Hs-25", carriers, data, index_col=0)
  engine.print_report(result)

License: CC BY 4.0
"""

import numpy as np
import hashlib
import json
from itertools import combinations
from datetime import datetime


# ============================================================
# TRANSCENDENTAL CONSTANTS (shared with main pipeline)
# ============================================================
TRANSCENDENTAL_CONSTANTS = {
    "pi": np.pi,
    "1/pi": 1.0 / np.pi,
    "e": np.e,
    "1/e": 1.0 / np.e,
    "ln2": np.log(2),
    "1/ln2": 1.0 / np.log(2),
    "phi": (1 + np.sqrt(5)) / 2,
    "phi^2": ((1 + np.sqrt(5)) / 2) ** 2,
    "1/phi": 2.0 / (1 + np.sqrt(5)),
    "sqrt2": np.sqrt(2),
    "1/sqrt2": 1.0 / np.sqrt(2),
    "sqrt3": np.sqrt(3),
    "1/sqrt3": 1.0 / np.sqrt(3),
    "euler_gamma": 0.5772156649015329,
    "catalan": 0.9159655941772190,
    "ln10": np.log(10),
    "1/ln10": 1.0 / np.log(10),
    "pi/4": np.pi / 4,
    "2pi": 2.0 * np.pi,
    "e^pi": np.e ** np.pi,
    "pi^e": np.pi ** np.e,
    "sqrt5": np.sqrt(5),
    "1/sqrt5": 1.0 / np.sqrt(5),
    "ln_phi": np.log((1 + np.sqrt(5)) / 2),
    "pi^2/6": np.pi**2 / 6,
    "apery": 1.2020569031595942,
    "khinchin": 2.6854520010653064,
    "feigenbaum_delta": 4.6692016091029906,
    "feigenbaum_alpha": 2.5029078750958928,
    "1/(2pi)": 1.0 / (2.0 * np.pi),
    "1/(e^pi)": 1.0 / (np.e ** np.pi),
    "1/(pi^e)": 1.0 / (np.pi ** np.e),
    "omega_lambert": 0.5671432904097838,
    "dottie": 0.7390851332151607,
    "glaisher_kinkelin": 1.2824271291006226,
}

ZERO_DELTA = 1e-6


class NumpyEncoder(json.JSONEncoder):
    """JSON encoder for numpy types."""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


# ============================================================
# CORE DIAGNOSTICS (standalone, no dependency on main pipeline)
# ============================================================

def close_to_simplex(data):
    """Close N×D matrix to simplex (rows sum to 1), with zero replacement."""
    data = data.copy().astype(np.float64)
    N, D = data.shape
    # Zero replacement
    mask = data <= 0
    if mask.any():
        data[mask] = ZERO_DELTA
        for i in range(N):
            if mask[i].any() and not mask[i].all():
                n_rep = mask[i].sum()
                total_delta = n_rep * ZERO_DELTA
                non_zero = ~mask[i]
                scale = (1.0 - total_delta) / data[i, non_zero].sum()
                data[i, non_zero] *= scale
                data[i, mask[i]] = ZERO_DELTA
    row_sums = data.sum(axis=1, keepdims=True)
    return data / row_sums


def clr_transform(simplex):
    """Centered log-ratio transform."""
    log_data = np.log(simplex)
    geo_mean_log = log_data.mean(axis=1, keepdims=True)
    return log_data - geo_mean_log


def aitchison_variance_trajectory(clr_data):
    """Cumulative Aitchison variance σ²_A."""
    N = clr_data.shape[0]
    sigma2 = np.zeros(N)
    for t in range(2, N):
        window = clr_data[:t+1]
        sigma2[t] = np.var(window, axis=0).sum()
    return sigma2


def hvld_shape(sigma2):
    """HVLD vertex lock: bowl or hill."""
    N = len(sigma2)
    valid = np.arange(2, N)
    if len(valid) < 3:
        return {"shape": "insufficient", "R2": 0.0, "a": 0.0}
    x = valid.astype(float)
    y = sigma2[valid]
    coeffs = np.polyfit(x, y, 2)
    a, b, c = coeffs
    y_pred = np.polyval(coeffs, x)
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    R2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return {
        "shape": "bowl" if a > 0 else "hill",
        "R2": float(R2),
        "a": float(a),
        "vertex_x": float(-b / (2 * a)) if abs(a) > 1e-15 else 0.0,
    }


def ratio_pair_analysis(simplex, carriers):
    """Compute pairwise log-ratio CV for all D*(D-1)/2 pairs."""
    N, D = simplex.shape
    pairs = {}
    for i in range(D):
        for j in range(i+1, D):
            log_ratio = np.log(simplex[:, i] / simplex[:, j])
            mean_lr = np.mean(log_ratio)
            std_lr = np.std(log_ratio)
            cv = abs(std_lr / mean_lr) if abs(mean_lr) > 1e-15 else float('inf')
            pair_name = f"{carriers[i]}/{carriers[j]}"
            pairs[pair_name] = {
                "cv": float(cv),
                "mean": float(mean_lr),
                "std": float(std_lr),
                "min": float(np.min(log_ratio)),
                "max": float(np.max(log_ratio)),
                "range": float(np.max(log_ratio) - np.min(log_ratio)),
            }
    return pairs


def classify_pairs(pairs):
    """Classify ratio pairs into black holes, grey zones, white holes."""
    black_holes = {}
    grey_zones = {}
    white_holes = {}
    for name, stats in pairs.items():
        cv = stats["cv"]
        rng = stats["range"]
        # Use both CV and range for classification
        # A truly locked pair has near-zero range in log-ratio space
        if rng < 0.01 or cv < 0.01:
            black_holes[name] = stats
        elif cv >= 0.50 or rng > 2.0:
            white_holes[name] = stats
        else:
            grey_zones[name] = stats
    return black_holes, grey_zones, white_holes


def super_squeeze(sigma2):
    """Test σ²_A against transcendental constants. Returns best match."""
    valid = sigma2[2:]
    if len(valid) == 0:
        return {"classification": "INSUFFICIENT", "matches": []}

    matches = []
    for name, const_val in TRANSCENDENTAL_CONSTANTS.items():
        if const_val <= 0:
            continue
        for idx, sv in enumerate(valid):
            if sv <= 0:
                continue
            for test_val, label in [(sv, "direct"), (1.0/sv if sv > 1e-15 else 0, "reciprocal")]:
                if test_val <= 0:
                    continue
                delta = abs(test_val - const_val)
                if delta < 0.01:
                    matches.append({
                        "time_index": int(idx + 2),
                        "constant": name,
                        "delta": float(delta),
                        "test_type": label,
                    })
    matches.sort(key=lambda m: m["delta"])
    if matches:
        best = matches[0]
        classification = "NATURAL" if best["delta"] < 0.01 else "INVESTIGATE"
    else:
        classification = "SYNTHETIC"
    return {
        "classification": classification,
        "matches": matches[:10],
        "closest_delta": matches[0]["delta"] if matches else None,
        "closest_constant": matches[0]["constant"] if matches else None,
        "match_count": len(matches),
    }


def shannon_entropy(simplex):
    """Shannon entropy per row, normalized."""
    N, D = simplex.shape
    H_max = np.log(D)
    H = np.zeros(N)
    for i in range(N):
        p = simplex[i]
        p = p[p > 0]
        H[i] = -np.sum(p * np.log(p))
    return H, H_max


def eitt_test(simplex, factors=[2, 4, 8]):
    """EITT: Shannon entropy invariance under geometric-mean decimation."""
    N, D = simplex.shape
    H_orig, H_max = shannon_entropy(simplex)
    H_mean_orig = np.mean(H_orig)

    results = {}
    for f in factors:
        n_blocks = N // f
        if n_blocks < 2:
            continue
        decimated = np.zeros((n_blocks, D))
        for b in range(n_blocks):
            block = simplex[b*f:(b+1)*f]
            # Geometric mean per carrier
            geo = np.exp(np.mean(np.log(block + 1e-30), axis=0))
            # Re-close
            decimated[b] = geo / geo.sum()
        H_dec, _ = shannon_entropy(decimated)
        H_mean_dec = np.mean(H_dec)
        variation = abs(H_mean_dec - H_mean_orig) / H_mean_orig if H_mean_orig > 1e-15 else 0
        results[f"{f}x"] = {
            "H_original": float(H_mean_orig),
            "H_decimated": float(H_mean_dec),
            "variation_pct": float(variation * 100),
            "preserved": variation < 0.05,
        }
    return results


def per_carrier_contribution(clr_data, carriers):
    """Per-carrier contribution to total Aitchison variance."""
    var_per_carrier = np.var(clr_data, axis=0)
    total_var = var_per_carrier.sum()
    contributions = {}
    for i, c in enumerate(carriers):
        contributions[c] = {
            "variance": float(var_per_carrier[i]),
            "fraction": float(var_per_carrier[i] / total_var) if total_var > 0 else 0,
        }
    dominant = carriers[np.argmax(var_per_carrier)]
    return contributions, dominant


# ============================================================
# AMALGAMATION ENGINE
# ============================================================

def generate_amalgamations(carriers):
    """Generate all meaningful amalgamation schemes.

    For D carriers, generate merges from 2-carrier merges up to (D-1)-carrier merges.
    Each scheme specifies which original carriers are merged and what remains separate.

    Returns list of dicts, each with:
      - groups: list of lists (each inner list = carriers in that group)
      - labels: list of strings (group labels)
      - level: amalgamation level (how many were merged in the largest group)
    """
    D = len(carriers)
    if D < 3:
        return []  # Cannot amalgamate a 2-carrier system

    schemes = []

    # Generate all subsets of size 2..D-1 to merge
    for merge_size in range(2, D):
        for combo in combinations(range(D), merge_size):
            merged_carriers = [carriers[i] for i in combo]
            remaining = [carriers[i] for i in range(D) if i not in combo]

            # The merged group becomes one carrier
            merged_label = "+".join(merged_carriers)
            groups = [list(combo)]  # indices of merged carriers
            labels = [merged_label]

            # Each remaining carrier is its own group
            for i in range(D):
                if i not in combo:
                    groups.append([i])
                    labels.append(carriers[i])

            # Only keep if result has ≥ 2 carriers (simplex requirement)
            if len(labels) >= 2:
                schemes.append({
                    "groups": groups,
                    "labels": labels,
                    "merge_size": merge_size,
                    "merged": merged_carriers,
                    "n_carriers": len(labels),
                })

    return schemes


def amalgamate_data(data, scheme):
    """Amalgamate data according to a scheme.

    For merged groups, sum the original carrier columns (pre-closure).
    Returns N × D' matrix where D' = len(scheme['labels']).
    """
    N = data.shape[0]
    D_new = len(scheme["groups"])
    result = np.zeros((N, D_new))
    for g, group_indices in enumerate(scheme["groups"]):
        result[:, g] = data[:, group_indices].sum(axis=1)
    return result


class SubcompositionalRecursion:
    """Hˢ T2 Test Engine: Subcompositional Recursion.

    Runs core pipeline diagnostics on every meaningful amalgamation of
    a compositional dataset and builds a duality map showing which
    attractors (black holes) and repellers (white holes) appear, vanish,
    or persist at each grouping level.
    """

    def __init__(self, verbose=True):
        self.verbose = verbose

    def run(self, experiment_id, carriers, data, index_col=None):
        """Run subcompositional recursion on a dataset.

        Parameters
        ----------
        experiment_id : str
        carriers : list of str
        data : np.ndarray, shape (N, D) or (N, D+1) if index_col given
        index_col : int or None
            If not None, this column is the index (drop before analysis)

        Returns
        -------
        dict with full recursion results
        """
        if index_col is not None:
            data = np.delete(data, index_col, axis=1)

        D = len(carriers)
        N = data.shape[0]

        if self.verbose:
            print(f"\n{'='*72}")
            print(f"  Hˢ SUBCOMPOSITIONAL RECURSION ENGINE — T2")
            print(f"  Experiment: {experiment_id}")
            print(f"  Carriers: {carriers} (D={D})")
            print(f"  Observations: N={N}")
            print(f"{'='*72}\n")

        timestamp = datetime.utcnow().isoformat() + "Z"
        data_hash = hashlib.sha256(data.astype(np.float64).tobytes()).hexdigest()[:16]

        # ── LEVEL 0: Full system (no amalgamation) ──
        if self.verbose:
            print(f"── LEVEL 0: Full system ({D} carriers) ──")
        level0 = self._analyse_subcomposition(carriers, data, "FULL")

        # ── LEVELS 1+: All amalgamations ──
        schemes = generate_amalgamations(carriers)
        levels = {}

        for s_idx, scheme in enumerate(schemes):
            amal_data = amalgamate_data(data, scheme)
            label = f"MERGE({'+'.join(scheme['merged'])})"
            if self.verbose:
                print(f"  [{s_idx+1}/{len(schemes)}] {label} → {scheme['labels']} (D={scheme['n_carriers']})")
            analysis = self._analyse_subcomposition(scheme["labels"], amal_data, label)
            analysis["scheme"] = scheme
            levels[label] = analysis

        # ── BUILD DUALITY MAP ──
        duality_map = self._build_duality_map(level0, levels, carriers)

        # ── BUILD PERSISTENCE MAP ──
        persistence = self._build_persistence_map(level0, levels)

        result = {
            "experiment_id": experiment_id,
            "timestamp": timestamp,
            "data_hash": data_hash,
            "D": D,
            "N": N,
            "carriers": carriers,
            "level0": level0,
            "amalgamations": levels,
            "n_amalgamations": len(schemes),
            "duality_map": duality_map,
            "persistence": persistence,
        }

        if self.verbose:
            self.print_report(result)

        return result

    def _analyse_subcomposition(self, carriers, data, label):
        """Run core diagnostics on a single subcomposition."""
        simplex = close_to_simplex(data)
        clr = clr_transform(simplex)
        sigma2 = aitchison_variance_trajectory(clr)
        shape = hvld_shape(sigma2)
        pairs = ratio_pair_analysis(simplex, carriers)
        black_holes, grey_zones, white_holes = classify_pairs(pairs)
        squeeze = super_squeeze(sigma2)
        eitt = eitt_test(simplex)
        contributions, dominant = per_carrier_contribution(clr, carriers)
        H, H_max = shannon_entropy(simplex)

        return {
            "label": label,
            "carriers": carriers,
            "D": len(carriers),
            "shape": shape,
            "classification": squeeze["classification"],
            "closest_constant": squeeze.get("closest_constant"),
            "closest_delta": squeeze.get("closest_delta"),
            "match_count": squeeze.get("match_count", 0),
            "ratio_pairs": pairs,
            "black_holes": black_holes,
            "grey_zones": grey_zones,
            "white_holes": white_holes,
            "n_black_holes": len(black_holes),
            "n_white_holes": len(white_holes),
            "eitt": eitt,
            "contributions": contributions,
            "dominant_carrier": dominant,
            "entropy_mean": float(np.mean(H)),
            "entropy_std": float(np.std(H)),
            "sigma2_final": float(sigma2[-1]) if len(sigma2) > 0 else 0,
        }

    def _build_duality_map(self, level0, levels, original_carriers):
        """Build the black hole / white hole duality map.

        For each original carrier, determine:
        - Is it part of a black hole (locked pair) at level 0?
        - Is it part of a white hole (volatile pair) at level 0?
        - What happens when it is amalgamated with its partner?
        - What happens when it is amalgamated with its repeller?
        """
        duality = {}

        # Map each carrier to its black hole and white hole memberships
        for c in original_carriers:
            bh_partners = []
            wh_partners = []
            for pair_name, stats in level0["black_holes"].items():
                parts = pair_name.split("/")
                if c in parts:
                    partner = parts[1] if parts[0] == c else parts[0]
                    bh_partners.append(partner)
            for pair_name, stats in level0["white_holes"].items():
                parts = pair_name.split("/")
                if c in parts:
                    partner = parts[1] if parts[0] == c else parts[0]
                    wh_partners.append(partner)

            duality[c] = {
                "black_hole_partners": bh_partners,
                "white_hole_partners": wh_partners,
                "role": "attractor" if bh_partners else ("repeller" if wh_partners and not bh_partners else "mixed"),
            }

        return duality

    def _build_persistence_map(self, level0, levels):
        """Track which features persist vs vanish under amalgamation."""
        persistence = {
            "classification_changes": [],
            "shape_changes": [],
            "black_holes_vanished": [],
            "black_holes_emerged": [],
            "white_holes_vanished": [],
            "white_holes_emerged": [],
        }

        base_class = level0["classification"]
        base_shape = level0["shape"]["shape"]

        for label, analysis in levels.items():
            if analysis["classification"] != base_class:
                persistence["classification_changes"].append({
                    "amalgamation": label,
                    "from": base_class,
                    "to": analysis["classification"],
                })
            if analysis["shape"]["shape"] != base_shape:
                persistence["shape_changes"].append({
                    "amalgamation": label,
                    "from": base_shape,
                    "to": analysis["shape"]["shape"],
                })

            # Check for black holes that emerged in this amalgamation
            # (not present at level 0 between these same carrier groups)
            for pair_name in analysis["black_holes"]:
                # Check if this pair existed at level 0
                if pair_name not in level0["black_holes"]:
                    persistence["black_holes_emerged"].append({
                        "pair": pair_name,
                        "amalgamation": label,
                        "cv": analysis["black_holes"][pair_name]["cv"],
                    })

            for pair_name in analysis["white_holes"]:
                if pair_name not in level0["white_holes"]:
                    persistence["white_holes_emerged"].append({
                        "pair": pair_name,
                        "amalgamation": label,
                        "cv": analysis["white_holes"][pair_name]["cv"],
                    })

        # Count how many amalgamations preserved classification
        n_class_preserved = len(levels) - len(persistence["classification_changes"])
        persistence["classification_stability"] = {
            "preserved": n_class_preserved,
            "changed": len(persistence["classification_changes"]),
            "total": len(levels),
            "stability_pct": float(n_class_preserved / len(levels) * 100) if levels else 0,
        }

        n_shape_preserved = len(levels) - len(persistence["shape_changes"])
        persistence["shape_stability"] = {
            "preserved": n_shape_preserved,
            "changed": len(persistence["shape_changes"]),
            "total": len(levels),
            "stability_pct": float(n_shape_preserved / len(levels) * 100) if levels else 0,
        }

        return persistence

    def print_report(self, result):
        """Print human-readable report."""
        print(f"\n{'='*72}")
        print(f"  SUBCOMPOSITIONAL RECURSION REPORT")
        print(f"  {result['experiment_id']} · D={result['D']} · N={result['N']}")
        print(f"  {result['n_amalgamations']} amalgamations tested")
        print(f"{'='*72}\n")

        # Level 0
        L0 = result["level0"]
        print(f"── LEVEL 0: Full System ──")
        print(f"  Classification: {L0['classification']}")
        if L0["closest_constant"]:
            print(f"  Closest constant: {L0['closest_constant']} (δ = {L0['closest_delta']:.6e})")
        print(f"  Shape: {L0['shape']['shape']} (R² = {L0['shape']['R2']:.4f})")
        print(f"  Dominant carrier: {L0['dominant_carrier']}")
        print(f"  Black holes: {L0['n_black_holes']}")
        for name, stats in L0["black_holes"].items():
            print(f"    ⚫ {name}: CV = {stats['cv']:.6f}, range = {stats['range']:.6e}")
        print(f"  White holes: {L0['n_white_holes']}")
        for name, stats in L0["white_holes"].items():
            print(f"    ⚪ {name}: CV = {stats['cv']:.4f}, range = {stats['range']:.4f}")

        # Duality map
        print(f"\n── DUALITY MAP ──")
        for carrier, info in result["duality_map"].items():
            role = info["role"]
            marker = "⚫" if role == "attractor" else ("⚪" if role == "repeller" else "◐")
            bh = ", ".join(info["black_hole_partners"]) if info["black_hole_partners"] else "none"
            wh = ", ".join(info["white_hole_partners"]) if info["white_hole_partners"] else "none"
            print(f"  {marker} {carrier}: locked with [{bh}], decoupled from [{wh}]")

        # Persistence
        P = result["persistence"]
        print(f"\n── PERSISTENCE UNDER AMALGAMATION ──")
        print(f"  Classification stability: {P['classification_stability']['preserved']}/{P['classification_stability']['total']} "
              f"({P['classification_stability']['stability_pct']:.0f}%)")
        print(f"  Shape stability: {P['shape_stability']['preserved']}/{P['shape_stability']['total']} "
              f"({P['shape_stability']['stability_pct']:.0f}%)")

        if P["classification_changes"]:
            print(f"  Classification changes:")
            for ch in P["classification_changes"]:
                print(f"    {ch['amalgamation']}: {ch['from']} → {ch['to']}")

        if P["black_holes_emerged"]:
            print(f"  Black holes emerged under amalgamation:")
            for bh in P["black_holes_emerged"][:10]:
                print(f"    ⚫ {bh['pair']} in {bh['amalgamation']} (CV = {bh['cv']:.6f})")

        if P["white_holes_emerged"]:
            print(f"  White holes emerged under amalgamation:")
            for wh in P["white_holes_emerged"][:10]:
                print(f"    ⚪ {wh['pair']} in {wh['amalgamation']} (CV = {wh['cv']:.4f})")

        # Summary statistics across all amalgamations
        print(f"\n── AMALGAMATION SUMMARY ──")
        all_bh = set()
        all_wh = set()
        for label, analysis in result["amalgamations"].items():
            for pair_name in analysis["black_holes"]:
                all_bh.add(pair_name)
            for pair_name in analysis["white_holes"]:
                all_wh.add(pair_name)

        print(f"  Unique black holes across all levels: {len(all_bh)}")
        print(f"  Unique white holes across all levels: {len(all_wh)}")

        # Deep structure: black holes at level 0 that persist
        level0_bh = set(L0["black_holes"].keys())
        deep = []
        for bh_name in level0_bh:
            # Check if a related pair persists in any amalgamation
            parts = bh_name.split("/")
            persisted = False
            for label, analysis in result["amalgamations"].items():
                for pair_name in analysis["black_holes"]:
                    aparts = pair_name.split("/")
                    # Check if the merged group contains both parts
                    for ap in aparts:
                        if parts[0] in ap and parts[1] in ap:
                            # Both original carriers are in the same merged group
                            # — the lock is subcompositional (inside the group)
                            break
                    else:
                        # The pair survived as a visible pair
                        if any(parts[0] in ap or parts[1] in ap for ap in aparts):
                            persisted = True
            if persisted:
                deep.append(bh_name)

        if deep:
            print(f"\n  DEEP STRUCTURE (survives amalgamation):")
            for d in deep:
                print(f"    ⬛ {d}")

        print(f"\n{'='*72}")
        print(f"  Engine: Hˢ Subcompositional Recursion v1.0")
        print(f"  Hash: {result['data_hash']}")
        print(f"  Timestamp: {result['timestamp']}")
        print(f"{'='*72}\n")

    def save_results(self, result, filepath):
        """Save results to JSON."""
        with open(filepath, 'w') as f:
            json.dump(result, f, indent=2, cls=NumpyEncoder)
        if self.verbose:
            print(f"  Results saved to {filepath}")


# ============================================================
# CSV LOADER
# ============================================================

def load_csv(filepath, index_col=0):
    """Load a CSV file and return carriers + data.

    Parameters
    ----------
    filepath : str
    index_col : int or None
        Column index to treat as index (not a carrier). Set to None if no index.

    Returns
    -------
    carriers : list of str
    data : np.ndarray (N × D), without index column
    """
    import csv
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [row for row in reader]

    # Parse carriers
    if index_col is not None:
        carriers = [h for i, h in enumerate(header) if i != index_col]
    else:
        carriers = list(header)

    # Parse data
    data = np.array([[float(v) for v in row] for row in rows])
    if index_col is not None:
        data = np.delete(data, index_col, axis=1)

    return carriers, data


# ============================================================
# MAIN — Run across experiments
# ============================================================

if __name__ == "__main__":
    import sys
    import os

    # Default: run on all known experiment CSVs
    base = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.join(base, "..", "..")
    exp_dir = os.path.join(repo, "experiments")

    experiments = [
        ("Hs-25", "Hs-25_Cosmic_Energy_Budget/Hs-25_cosmic_energy_budget.csv", 0),
        ("Hs-16", "Hs-16_Planck_Cosmic/planck_cosmic_budget.csv", 0),
        ("Hs-17", "Hs-17_Backblaze/Hs-17_fleet_composition.csv", 0),
        ("Hs-20", "Hs-20_Conversation_Drift/Hs-20_milestone_compositions.csv", 0),
        ("Hs-23", "Hs-23_Radionuclides/Hs-23_decay_compositions.csv", None),
    ]

    engine = SubcompositionalRecursion(verbose=True)
    all_results = {}

    for exp_id, csv_path, idx_col in experiments:
        full_path = os.path.join(exp_dir, csv_path)
        if not os.path.exists(full_path):
            print(f"  SKIP: {full_path} not found")
            continue

        carriers, data = load_csv(full_path, index_col=idx_col)
        result = engine.run(exp_id, carriers, data)
        all_results[exp_id] = result

    # Save combined results
    out_path = os.path.join(repo, "tools", "pipeline", "amalgamation_results.json")
    with open(out_path, 'w') as f:
        json.dump(all_results, f, indent=2, cls=NumpyEncoder)
    print(f"\nAll results saved to {out_path}")
