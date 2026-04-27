#!/usr/bin/env python3
"""
Hˢ COMPONENT POWER MAPPER — hs_sensitivity.py
================================================
Compositional sensitivity analysis for the Higgins Decomposition pipeline.

Measures component POWER (influence on system character), not component
FRACTION (share of composition). A carrier with 1% mass fraction can have
the highest power score if removing it changes the system's geometric
fingerprint.

Three analyses:
  1. Compositional Leverage Index (CLI) — perturbation sensitivity
  2. Phase Boundary Map (PBM) — where classification flips
  3. Component Power Score (CPS) — synthesised power ranking

The yeast problem: yeast is 1% of bread by mass but removing it changes
the system from bread to brick. The power mapper detects this by measuring
how much the system's geometric identity changes per unit perturbation of
each carrier, independent of that carrier's mass fraction.

Author: Peter Higgins / Claude
Date: 2026-04-27
Version: 1.0

Usage:
  from hs_sensitivity import ComponentPowerMapper
  mapper = ComponentPowerMapper(data, carriers, domain="FOOD")
  power_map = mapper.run_full_analysis()

  # Or CLI:
  python hs_sensitivity.py data.csv -o power_map.json
  python hs_sensitivity.py results.json --from-results -o power_map.json

License: CC BY 4.0
"""

import numpy as np
import json
import sys
import os
import hashlib
from datetime import datetime

# Add pipeline directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from higgins_decomposition_12step import HigginsDecomposition, NumpyEncoder


class ComponentPowerMapper:
    """Component Power Mapper for compositional sensitivity analysis.

    Measures the POWER of each carrier in a compositional system:
    how much does the system's geometric identity change when this
    carrier is perturbed?

    Three analyses:
      1. Compositional Leverage Index (CLI)
      2. Phase Boundary Map (PBM)
      3. Component Power Score (CPS)
    """

    def __init__(self, data, carriers, experiment_id="CPM",
                 name="Power Analysis", domain="ANALYSIS",
                 perturbation_steps=10, perturbation_range=0.5,
                 phase_resolution=20):
        """
        Args:
            data: N×D numpy array of compositions
            carriers: list of D carrier names
            experiment_id: identifier for audit trail
            name: human-readable name
            domain: physical domain
            perturbation_steps: number of perturbation levels for CLI
            perturbation_range: max perturbation as fraction of carrier value
            phase_resolution: number of sweep points for phase boundary search
        """
        self.data = np.array(data, dtype=np.float64)
        self.carriers = list(carriers)
        self.experiment_id = experiment_id
        self.name = name
        self.domain = domain
        self.N, self.D = self.data.shape
        self.perturbation_steps = perturbation_steps
        self.perturbation_range = perturbation_range
        self.phase_resolution = phase_resolution

        # Validate
        assert self.D >= 2, f"Need D >= 2 carriers, got {self.D}"
        assert self.N >= 5, f"Need N >= 5 observations, got {self.N}"
        assert len(self.carriers) == self.D, \
            f"Carrier count {len(self.carriers)} != data columns {self.D}"

        # Compute actual mass fractions (mean simplex composition)
        closed = self.data.copy()
        row_sums = closed.sum(axis=1, keepdims=True)
        row_sums = np.where(row_sums > 0, row_sums, 1.0)
        closed /= row_sums
        self.mass_fractions = closed.mean(axis=0)  # true composition %

        # Store baseline run
        self._baseline = None
        self._baseline_fingerprint = None
        self._results = {}
        self._timestamp = datetime.utcnow().isoformat() + "Z"

    def _run_pipeline(self, data, tag=""):
        """Run the Hˢ pipeline on data, return key diagnostics."""
        hd = HigginsDecomposition(
            f"{self.experiment_id}_CPM{tag}",
            f"{self.name} (CPM{tag})",
            self.domain,
            carriers=self.carriers
        )
        hd.load_data(data)
        try:
            result = hd.run_full_extended()
        except Exception as e:
            return {
                "status": "FAILED",
                "error": str(e),
                "shape": None,
                "R2": 0.0,
                "classification": "ERROR",
                "sigma2_final": 0.0,
                "nearest_constant": None,
                "nearest_delta": float('inf'),
                "entropy_cv": float('inf'),
                "eitt_pass": False,
                "structural_modes": [],
            }

        steps = result.get("steps", {})
        ext = result.get("extended", {})
        universal = ext.get("universal", {})

        # HVLD uses legacy key names (step6_pll_*)
        shape = steps.get("step6_pll_shape", "unknown")
        R2 = float(steps.get("step6_pll_R2", 0))

        # Classification from extended claim_status
        claim = universal.get("claim_status", {})
        classification = claim.get("htp_classification", "UNKNOWN")

        # Sigma2_A final value
        sigma2_final = float(steps.get("step5_sigma2_final", 0))

        # Squeeze results
        squeeze_closest = steps.get("step7_squeeze_closest", {})
        if isinstance(squeeze_closest, dict):
            nearest_name = squeeze_closest.get("constant", None)
            nearest_delta = float(squeeze_closest.get("delta", float('inf')))
        else:
            nearest_name = None
            nearest_delta = float('inf')

        # Entropy
        entropy_cv = float(steps.get("step8_entropy_cv", float('inf')))
        eitt_data = steps.get("step8_eitt_invariance", {})
        eitt_pass = False
        if isinstance(eitt_data, dict):
            eitt_pass = eitt_data.get("invariant", False)
        elif isinstance(eitt_data, list) and eitt_data:
            # Check if all decimation levels pass
            eitt_pass = all(
                abs(e.get("H_ratio", 0) - 1.0) < 0.05
                for e in eitt_data if isinstance(e, dict))

        # Extract structural modes from conditional
        cond = ext.get("conditional", {})
        modes = []  # would need codes for this, simplified here

        # Per-carrier contribution
        pcc = universal.get("per_carrier_contribution", {})
        carrier_pct = pcc.get("carrier_pct", [0] * self.D)

        # Transfer entropy
        te = cond.get("transfer_entropy", {})
        te_matrix = te.get("te_matrix", {})

        # PID
        pid = cond.get("PID", {})

        return {
            "status": "OK",
            "shape": shape,
            "R2": R2,
            "classification": classification,
            "sigma2_final": sigma2_final,
            "nearest_constant": nearest_name,
            "nearest_delta": nearest_delta,
            "entropy_cv": entropy_cv,
            "eitt_pass": eitt_pass,
            "carrier_pct": carrier_pct,
            "te_matrix": te_matrix,
            "pid": pid,
            "structural_modes": modes,
        }

    def _fingerprint_vector(self, diag):
        """Extract a numeric fingerprint vector for comparison."""
        shape_val = {"bowl": 1.0, "hill": -1.0}.get(diag["shape"], 0.0)
        class_val = {"NATURAL": 1.0, "INVESTIGATE": 0.5,
                     "FLAG": 0.0, "ERROR": -1.0}.get(
                         diag["classification"], 0.0)
        eitt_val = 1.0 if diag["eitt_pass"] else 0.0

        return np.array([
            shape_val,
            diag["R2"],
            class_val,
            diag["sigma2_final"],
            diag["nearest_delta"],
            diag["entropy_cv"],
            eitt_val,
        ])

    def _fingerprint_distance(self, fp1, fp2):
        """Weighted distance between two fingerprint vectors.
        Higher weight on classification and shape (discrete changes)."""
        weights = np.array([
            3.0,   # shape change (bowl↔hill is major)
            1.0,   # R2 change
            5.0,   # classification change (NATURAL↔FLAG is critical)
            1.0,   # sigma2 change
            0.5,   # delta change
            0.5,   # entropy CV change
            2.0,   # EITT pass/fail change
        ])
        # Replace inf/nan with large values for safe comparison
        fp1_safe = np.where(np.isfinite(fp1), fp1, 1e6)
        fp2_safe = np.where(np.isfinite(fp2), fp2, 1e6)
        diff = np.abs(fp1_safe - fp2_safe)
        # Normalise each dimension by its scale
        scales = np.maximum(np.abs(fp1_safe) + np.abs(fp2_safe), 1e-10) / 2.0
        # For discrete variables (shape, class, eitt), use raw diff
        scales[0] = 1.0  # shape is already -1/0/1
        scales[2] = 1.0  # classification is already 0/0.5/1
        scales[6] = 1.0  # eitt is already 0/1
        normalised = diff / scales
        return float(np.sum(weights * normalised))

    def run_baseline(self):
        """Run the baseline (unperturbed) analysis."""
        self._baseline = self._run_pipeline(self.data, tag="_baseline")
        if self._baseline["status"] != "OK":
            raise RuntimeError(
                f"Baseline pipeline failed: {self._baseline.get('error')}")
        self._baseline_fingerprint = self._fingerprint_vector(self._baseline)
        return self._baseline

    def run_leverage_index(self):
        """Compositional Leverage Index (CLI).

        For each carrier j, perturb its value by ε (as fraction of current
        value), re-close to simplex, re-run pipeline, measure fingerprint
        change. The leverage is the ratio of fingerprint change to
        perturbation size.

        Returns dict with per-carrier leverage scores.
        """
        if self._baseline is None:
            self.run_baseline()

        leverage = {}
        epsilons = np.linspace(0.01, self.perturbation_range,
                               self.perturbation_steps)

        for j in range(self.D):
            carrier_name = self.carriers[j]
            carrier_mean = float(self.data.mean(axis=0)[j])

            # Perturbation in both directions
            responses_up = []
            responses_down = []
            eps_actual = []

            for eps in epsilons:
                # Upward perturbation: increase carrier j by eps fraction
                perturbed_up = self.data.copy()
                perturbed_up[:, j] *= (1.0 + eps)
                # Re-close to simplex
                row_sums = perturbed_up.sum(axis=1, keepdims=True)
                perturbed_up /= row_sums

                diag_up = self._run_pipeline(perturbed_up,
                                             tag=f"_up_{carrier_name}_{eps:.3f}")
                if diag_up["status"] == "OK":
                    fp_up = self._fingerprint_vector(diag_up)
                    dist_up = self._fingerprint_distance(
                        self._baseline_fingerprint, fp_up)
                    responses_up.append(dist_up)
                else:
                    responses_up.append(float('inf'))

                # Downward perturbation: decrease carrier j by eps fraction
                perturbed_down = self.data.copy()
                perturbed_down[:, j] *= max(1.0 - eps, 0.01)
                row_sums = perturbed_down.sum(axis=1, keepdims=True)
                perturbed_down /= row_sums

                diag_down = self._run_pipeline(
                    perturbed_down,
                    tag=f"_dn_{carrier_name}_{eps:.3f}")
                if diag_down["status"] == "OK":
                    fp_down = self._fingerprint_vector(diag_down)
                    dist_down = self._fingerprint_distance(
                        self._baseline_fingerprint, fp_down)
                    responses_down.append(dist_down)
                else:
                    responses_down.append(float('inf'))

                eps_actual.append(float(eps))

            # Compute leverage as mean response per unit perturbation
            valid_up = [(r, e) for r, e in zip(responses_up, eps_actual)
                        if r < float('inf') and e > 0]
            valid_down = [(r, e) for r, e in zip(responses_down, eps_actual)
                          if r < float('inf') and e > 0]

            if valid_up:
                leverage_up = np.mean([r / e for r, e in valid_up])
            else:
                leverage_up = 0.0

            if valid_down:
                leverage_down = np.mean([r / e for r, e in valid_down])
            else:
                leverage_down = 0.0

            # Asymmetry: is removal more dangerous than addition?
            leverage_mean = (leverage_up + leverage_down) / 2.0
            leverage_asymmetry = (leverage_down - leverage_up) / max(
                leverage_mean, 1e-10)

            # Did any perturbation flip the classification?
            classification_flipped_up = any(
                r > 4.0 for r in responses_up if r < float('inf'))
            classification_flipped_down = any(
                r > 4.0 for r in responses_down if r < float('inf'))

            leverage[carrier_name] = {
                "leverage_up": float(leverage_up),
                "leverage_down": float(leverage_down),
                "leverage_mean": float(leverage_mean),
                "leverage_asymmetry": float(leverage_asymmetry),
                "mass_fraction_pct": float(self.mass_fractions[j] * 100),
                "variance_contribution_pct": float(
                    self._baseline["carrier_pct"][j]
                    if j < len(self._baseline["carrier_pct"]) else 0),
                "carrier_mean_value": carrier_mean,
                "responses_up": [float(r) for r in responses_up],
                "responses_down": [float(r) for r in responses_down],
                "epsilons": eps_actual,
                "classification_flip_on_increase": classification_flipped_up,
                "classification_flip_on_decrease": classification_flipped_down,
            }

        # Rank by leverage
        ranked = sorted(leverage.items(),
                        key=lambda x: x[1]["leverage_mean"], reverse=True)
        rankings = {name: rank + 1 for rank, (name, _) in enumerate(ranked)}

        self._results["leverage_index"] = {
            "carriers": leverage,
            "rankings": rankings,
            "perturbation_steps": self.perturbation_steps,
            "perturbation_range": self.perturbation_range,
        }

        return self._results["leverage_index"]

    def run_phase_boundary_map(self):
        """Phase Boundary Map (PBM).

        For each carrier, sweep from current value toward zero and toward
        maximum, running the pipeline at each step. Record where the
        classification flips (NATURAL → FLAG, bowl → hill, etc.).
        The distance to the nearest phase boundary is the criticality margin.

        Returns dict with per-carrier phase boundaries and criticality margins.
        """
        if self._baseline is None:
            self.run_baseline()

        baseline_class = self._baseline["classification"]
        baseline_shape = self._baseline["shape"]

        phase_map = {}

        for j in range(self.D):
            carrier_name = self.carriers[j]
            carrier_mean = float(self.data.mean(axis=0)[j])

            # Sweep downward: scale carrier toward zero
            # Scale factors from 1.0 down to 0.01
            down_scales = np.linspace(1.0, 0.01, self.phase_resolution)
            down_boundary = None
            down_boundary_type = None

            for scale in down_scales[1:]:  # skip 1.0 (baseline)
                perturbed = self.data.copy()
                perturbed[:, j] *= scale
                # Prevent exact zeros
                perturbed[:, j] = np.maximum(perturbed[:, j], 1e-10)
                row_sums = perturbed.sum(axis=1, keepdims=True)
                perturbed /= row_sums

                diag = self._run_pipeline(
                    perturbed,
                    tag=f"_phase_dn_{carrier_name}_{scale:.3f}")

                if diag["status"] != "OK":
                    down_boundary = float(scale)
                    down_boundary_type = "pipeline_failure"
                    break

                if diag["classification"] != baseline_class:
                    down_boundary = float(scale)
                    down_boundary_type = (
                        f"classification_{baseline_class}_to_"
                        f"{diag['classification']}")
                    break

                if diag["shape"] != baseline_shape:
                    down_boundary = float(scale)
                    down_boundary_type = (
                        f"shape_{baseline_shape}_to_{diag['shape']}")
                    break

            # Sweep upward: scale carrier toward dominance
            # Scale factors from 1.0 up to 5.0 (carrier grows 5x)
            up_scales = np.linspace(1.0, 5.0, self.phase_resolution)
            up_boundary = None
            up_boundary_type = None

            for scale in up_scales[1:]:
                perturbed = self.data.copy()
                perturbed[:, j] *= scale
                row_sums = perturbed.sum(axis=1, keepdims=True)
                perturbed /= row_sums

                diag = self._run_pipeline(
                    perturbed,
                    tag=f"_phase_up_{carrier_name}_{scale:.3f}")

                if diag["status"] != "OK":
                    up_boundary = float(scale)
                    up_boundary_type = "pipeline_failure"
                    break

                if diag["classification"] != baseline_class:
                    up_boundary = float(scale)
                    up_boundary_type = (
                        f"classification_{baseline_class}_to_"
                        f"{diag['classification']}")
                    break

                if diag["shape"] != baseline_shape:
                    up_boundary = float(scale)
                    up_boundary_type = (
                        f"shape_{baseline_shape}_to_{diag['shape']}")
                    break

            # Criticality margin: distance to nearest boundary
            # (as fraction of current value)
            down_margin = (1.0 - down_boundary) if down_boundary else 1.0
            up_margin = (up_boundary - 1.0) if up_boundary else 4.0
            criticality_margin = min(down_margin, up_margin)

            phase_map[carrier_name] = {
                "carrier_mean_value": carrier_mean,
                "mass_fraction_pct": float(self.mass_fractions[j] * 100),
                "down_boundary_scale": down_boundary,
                "down_boundary_type": down_boundary_type,
                "down_margin": float(down_margin),
                "up_boundary_scale": up_boundary,
                "up_boundary_type": up_boundary_type,
                "up_margin": float(up_margin),
                "criticality_margin": float(criticality_margin),
                "phase_sensitive": criticality_margin < 0.3,
            }

        # Rank by criticality (smallest margin = most critical)
        ranked = sorted(phase_map.items(),
                        key=lambda x: x[1]["criticality_margin"])
        rankings = {name: rank + 1 for rank, (name, _) in enumerate(ranked)}

        self._results["phase_boundary_map"] = {
            "carriers": phase_map,
            "rankings": rankings,
            "baseline_classification": baseline_class,
            "baseline_shape": baseline_shape,
            "phase_resolution": self.phase_resolution,
        }

        return self._results["phase_boundary_map"]

    def run_component_power_score(self):
        """Component Power Score (CPS).

        Synthesises leverage index, phase boundary criticality, transfer
        entropy centrality, and PID synergistic contribution into a single
        power ranking per carrier.

        Power = w1 * leverage + w2 * (1/criticality_margin)
                + w3 * te_centrality + w4 * synergy_participation

        The power-to-fraction ratio reveals disproportionate influence:
        a ratio of 5.0 means the carrier has 5x the power of what its
        mass fraction would predict.

        Returns dict with per-carrier power scores and rankings.
        """
        if "leverage_index" not in self._results:
            self.run_leverage_index()
        if "phase_boundary_map" not in self._results:
            self.run_phase_boundary_map()
        if self._baseline is None:
            self.run_baseline()

        leverage_data = self._results["leverage_index"]["carriers"]
        phase_data = self._results["phase_boundary_map"]["carriers"]

        # Extract transfer entropy centrality from baseline
        te_matrix = self._baseline.get("te_matrix", {})
        te_out = {}  # outgoing TE per carrier
        te_in = {}   # incoming TE per carrier
        for key, val in te_matrix.items():
            parts = key.split("->")
            if len(parts) == 2:
                src, tgt = parts
                te_out[src] = te_out.get(src, 0) + val
                te_in[tgt] = te_in.get(tgt, 0) + val

        # Extract PID synergy participation
        pid = self._baseline.get("pid", {})
        pid_dominant = pid.get("dominant", "unknown")

        # Weights for power score components
        W_LEVERAGE = 0.35
        W_CRITICALITY = 0.30
        W_TRANSFER_ENTROPY = 0.20
        W_SYNERGY = 0.15

        power_scores = {}
        max_leverage = max(
            (d["leverage_mean"] for d in leverage_data.values()), default=1.0)
        max_leverage = max(max_leverage, 1e-10)

        for j, carrier_name in enumerate(self.carriers):
            # Normalised leverage (0-1)
            lev = leverage_data.get(carrier_name, {})
            norm_leverage = lev.get("leverage_mean", 0) / max_leverage

            # Normalised criticality (smaller margin = higher score)
            phase = phase_data.get(carrier_name, {})
            crit_margin = phase.get("criticality_margin", 1.0)
            # Transform: margin of 0 → score 1, margin of 1+ → score ~0
            norm_criticality = 1.0 / (1.0 + crit_margin)

            # Normalised transfer entropy centrality
            te_total = te_out.get(carrier_name, 0) + te_in.get(
                carrier_name, 0)
            max_te = max(
                (te_out.get(c, 0) + te_in.get(c, 0)
                 for c in self.carriers), default=1.0)
            max_te = max(max_te, 1e-10)
            norm_te = te_total / max_te

            # Synergy participation score
            # If PID available and this carrier is involved
            pid_sources = pid.get("sources", [])
            pid_target = pid.get("target", "")
            if carrier_name in pid_sources or carrier_name == pid_target:
                # Higher score if system is synergy-dominant
                # (carrier participates in non-decomposable information)
                if pid_dominant == "redundancy":
                    norm_synergy = 0.3  # participates but redundant
                else:
                    norm_synergy = 0.7  # participates and unique/synergistic
            else:
                norm_synergy = 0.0

            # If no PID available (D < 3), redistribute weight
            if not pid:
                # No PID data: redistribute synergy weight to other components
                adjusted_w_lev = W_LEVERAGE + W_SYNERGY * 0.4
                adjusted_w_crit = W_CRITICALITY + W_SYNERGY * 0.3
                adjusted_w_te = W_TRANSFER_ENTROPY + W_SYNERGY * 0.3
                adjusted_w_syn = 0.0
            else:
                adjusted_w_lev = W_LEVERAGE
                adjusted_w_crit = W_CRITICALITY
                adjusted_w_te = W_TRANSFER_ENTROPY
                adjusted_w_syn = W_SYNERGY

            # Composite power score
            power = (adjusted_w_lev * norm_leverage
                     + adjusted_w_crit * norm_criticality
                     + adjusted_w_te * norm_te
                     + adjusted_w_syn * norm_synergy)

            # Mass fraction for comparison (true composition, not variance)
            mass_frac = float(self.mass_fractions[j] * 100)
            # Normalise mass fraction to 0-1 scale
            max_mass = float(self.mass_fractions.max() * 100)
            max_mass = max(max_mass, 1e-10)
            norm_mass = mass_frac / max_mass

            # Power-to-fraction ratio
            # How much more powerful is this carrier than its mass predicts?
            power_to_fraction = (power / max(norm_mass, 1e-10)
                                 if norm_mass > 1e-10 else float('inf'))

            power_scores[carrier_name] = {
                "power_score": float(power),
                "norm_leverage": float(norm_leverage),
                "norm_criticality": float(norm_criticality),
                "norm_transfer_entropy": float(norm_te),
                "norm_synergy": float(norm_synergy),
                "mass_fraction_pct": float(mass_frac),
                "power_to_fraction_ratio": float(power_to_fraction),
                "leverage_rank": self._results[
                    "leverage_index"]["rankings"].get(carrier_name, 0),
                "criticality_rank": self._results[
                    "phase_boundary_map"]["rankings"].get(carrier_name, 0),
                "classification_flip_risk": (
                    lev.get("classification_flip_on_decrease", False)
                    or lev.get("classification_flip_on_increase", False)),
                "phase_sensitive": phase.get("phase_sensitive", False),
            }

        # Power ranking (highest power first)
        ranked = sorted(power_scores.items(),
                        key=lambda x: x[1]["power_score"], reverse=True)
        power_rankings = {name: rank + 1
                          for rank, (name, _) in enumerate(ranked)}

        # Detect disproportionate carriers (power >> mass)
        disproportionate = []
        for name, scores in power_scores.items():
            if scores["power_to_fraction_ratio"] > 2.0:
                disproportionate.append({
                    "carrier": name,
                    "power_to_fraction_ratio": scores[
                        "power_to_fraction_ratio"],
                    "mass_fraction_pct": scores["mass_fraction_pct"],
                    "power_rank": power_rankings[name],
                })

        # Sort disproportionate by ratio (most extreme first)
        disproportionate.sort(
            key=lambda x: x["power_to_fraction_ratio"], reverse=True)

        self._results["power_scores"] = {
            "carriers": power_scores,
            "rankings": power_rankings,
            "ranked_list": [name for name, _ in ranked],
            "disproportionate_carriers": disproportionate,
            "weights": {
                "leverage": W_LEVERAGE,
                "criticality": W_CRITICALITY,
                "transfer_entropy": W_TRANSFER_ENTROPY,
                "synergy": W_SYNERGY,
            },
        }

        return self._results["power_scores"]

    def run_full_analysis(self):
        """Run complete Component Power Mapping analysis.

        Returns comprehensive power map with all three analyses.
        """
        self.run_baseline()
        self.run_leverage_index()
        self.run_phase_boundary_map()
        self.run_component_power_score()

        # Build summary
        ps = self._results["power_scores"]
        summary = {
            "power_ranking": ps["ranked_list"],
            "mass_ranking": sorted(
                self.carriers,
                key=lambda c: ps["carriers"][c]["mass_fraction_pct"],
                reverse=True),
            "rankings_differ": (
                ps["ranked_list"] != sorted(
                    self.carriers,
                    key=lambda c: ps["carriers"][c]["mass_fraction_pct"],
                    reverse=True)),
            "disproportionate_count": len(ps["disproportionate_carriers"]),
            "most_powerful": ps["ranked_list"][0] if ps["ranked_list"] else None,
            "most_disproportionate": (
                ps["disproportionate_carriers"][0]["carrier"]
                if ps["disproportionate_carriers"] else None),
            "phase_sensitive_carriers": [
                c for c, s in ps["carriers"].items()
                if s["phase_sensitive"]],
            "classification_flip_risk_carriers": [
                c for c, s in ps["carriers"].items()
                if s["classification_flip_risk"]],
        }

        power_map = {
            "instrument": "Hˢ Component Power Mapper v1.0",
            "experiment_id": self.experiment_id,
            "name": self.name,
            "domain": self.domain,
            "timestamp": self._timestamp,
            "carriers": self.carriers,
            "D": self.D,
            "N": self.N,
            "baseline": {
                "classification": self._baseline["classification"],
                "shape": self._baseline["shape"],
                "R2": self._baseline["R2"],
                "sigma2_final": self._baseline["sigma2_final"],
                "nearest_constant": self._baseline["nearest_constant"],
            },
            "summary": summary,
            "leverage_index": self._results["leverage_index"],
            "phase_boundary_map": self._results["phase_boundary_map"],
            "power_scores": self._results["power_scores"],
        }

        return power_map

    def save_results(self, filepath):
        """Save power map to JSON."""
        power_map = self.run_full_analysis()
        with open(filepath, 'w') as f:
            json.dump(power_map, f, indent=2, cls=NumpyEncoder)
        return filepath

    def print_summary(self, power_map=None):
        """Print human-readable power map summary."""
        if power_map is None:
            power_map = self.run_full_analysis()

        summary = power_map["summary"]
        ps = power_map["power_scores"]
        baseline = power_map["baseline"]

        print("=" * 70)
        print(f"  Hˢ COMPONENT POWER MAP")
        print(f"  {power_map['name']} ({power_map['domain']})")
        print(f"  D={power_map['D']} carriers, N={power_map['N']} observations")
        print("=" * 70)
        print()
        print(f"  Baseline: {baseline['classification']} | "
              f"{baseline['shape']} | R²={baseline['R2']:.4f} | "
              f"σ²_A={baseline['sigma2_final']:.6f}")
        print()

        # Power ranking table
        print("  CARRIER POWER RANKING")
        print("  " + "-" * 66)
        print(f"  {'Rank':<5} {'Carrier':<15} {'Power':<8} "
              f"{'Mass%':<8} {'P/F Ratio':<10} {'Phase':<8} {'Flip?':<6}")
        print("  " + "-" * 66)

        for rank, carrier_name in enumerate(summary["power_ranking"], 1):
            scores = ps["carriers"][carrier_name]
            phase = "SENS" if scores["phase_sensitive"] else "safe"
            flip = "YES" if scores["classification_flip_risk"] else "no"
            print(f"  {rank:<5} {carrier_name:<15} "
                  f"{scores['power_score']:.4f}  "
                  f"{scores['mass_fraction_pct']:>6.1f}%  "
                  f"{scores['power_to_fraction_ratio']:>8.2f}x  "
                  f"{phase:<8} {flip:<6}")

        print("  " + "-" * 66)
        print()

        if summary["rankings_differ"]:
            print("  POWER ≠ MASS: Rankings differ from mass fraction order.")
            print(f"    Power ranking: {' > '.join(summary['power_ranking'])}")
            print(f"    Mass ranking:  {' > '.join(summary['mass_ranking'])}")
            print()

        if summary["disproportionate_count"] > 0:
            print(f"  DISPROPORTIONATE CARRIERS "
                  f"({summary['disproportionate_count']} found):")
            for dc in ps["disproportionate_carriers"]:
                print(f"    {dc['carrier']}: "
                      f"{dc['power_to_fraction_ratio']:.2f}x power vs mass "
                      f"(mass={dc['mass_fraction_pct']:.1f}%, "
                      f"power rank #{dc['power_rank']})")
            print()

        if summary["phase_sensitive_carriers"]:
            print(f"  PHASE-SENSITIVE CARRIERS: "
                  f"{', '.join(summary['phase_sensitive_carriers'])}")
            print("  (Small changes to these carriers can flip system state)")
            print()

        if summary["classification_flip_risk_carriers"]:
            print(f"  CLASSIFICATION FLIP RISK: "
                  f"{', '.join(summary['classification_flip_risk_carriers'])}")
            print("  (Perturbation caused NATURAL↔FLAG transition)")
            print()

        print("  " + "=" * 66)
        print("  The instrument reads power, not mass.")
        print("  The expert decides what matters.")
        print("  " + "=" * 66)


def main():
    """CLI interface for Component Power Mapper."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Hˢ Component Power Mapper — "
                    "compositional sensitivity analysis")
    parser.add_argument("input", help="CSV data file or JSON results file")
    parser.add_argument("-o", "--output",
                        help="Output JSON file for power map")
    parser.add_argument("--from-results", action="store_true",
                        help="Input is a pipeline results JSON, "
                             "not raw data CSV")
    parser.add_argument("--name", default="Power Analysis",
                        help="System name")
    parser.add_argument("--domain", default="ANALYSIS",
                        help="Physical domain")
    parser.add_argument("--steps", type=int, default=10,
                        help="Perturbation steps (default: 10)")
    parser.add_argument("--range", type=float, default=0.5,
                        help="Perturbation range (default: 0.5)")
    parser.add_argument("--resolution", type=int, default=20,
                        help="Phase boundary resolution (default: 20)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print detailed summary")

    args = parser.parse_args()

    if args.from_results:
        # Load from pipeline results JSON
        with open(args.input) as f:
            results = json.load(f)
        # Reconstruct data from results — need original data
        print("Error: --from-results requires the original data file.")
        print("Usage: python hs_sensitivity.py data.csv [options]")
        sys.exit(1)

    # Load CSV
    import csv
    with open(args.input) as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = []
        for row in reader:
            rows.append([float(x) for x in row])
    data = np.array(rows)
    carriers = headers

    mapper = ComponentPowerMapper(
        data, carriers,
        experiment_id="CPM",
        name=args.name,
        domain=args.domain,
        perturbation_steps=args.steps,
        perturbation_range=args.range,
        phase_resolution=args.resolution,
    )

    power_map = mapper.run_full_analysis()

    if args.verbose or not args.output:
        mapper.print_summary(power_map)

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(power_map, f, indent=2, cls=NumpyEncoder)
        print(f"\nPower map saved to {args.output}")


if __name__ == "__main__":
    main()
