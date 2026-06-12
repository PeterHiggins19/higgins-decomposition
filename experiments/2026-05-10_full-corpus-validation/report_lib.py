"""
Report generation library for the full-corpus validation suite.

Produces two markdown reports per dataset:
  STAGE_1_REPORT.md      — pure-CoDa view (closure, CLR, ILR, variation matrix,
                           carrier-pair correlation, section atlas).
  ADVANCED_ANALYSIS.md   — full Hs extension stack (kappa^HS, s_j, depth tower,
                           P2 attractor, helmsman family, IR class) plus the
                           CNQ v2 quaternion view (bearing, radial, dimension
                           policy, CHSH).

These are deliberately verbose reports — each is a self-contained scientific
record suitable for citation in future papers.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List


def stage1_report(
    dataset_id: str,
    domain: str,
    description: str,
    citation: str,
    payload: Dict[str, Any],
) -> str:
    """Build the Stage 1 (pure CoDa) markdown report."""
    md = payload["metadata"]
    inp = payload["input"]
    s1 = payload["stages"]["stage1"]
    s2 = payload["stages"]["stage2"]
    timesteps = payload["tensor"]["timesteps"]

    lines: List[str] = []
    lines.append(f"# Stage 1 Report (pure CoDa) — {dataset_id}")
    lines.append("")
    lines.append(f"**Domain:** {domain}")
    lines.append(f"**Description:** {description}")
    lines.append(f"**Citation / source:** {citation}")
    lines.append("")
    lines.append(f"**Engine:** {md['engine']} v{md['engine_version']} (schema {md['schema_version']})")
    lines.append(f"**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*")
    lines.append(f"**Generated:** {md['generated']}")
    lines.append(f"**cnt_content_sha256:** `{payload['diagnostics']['cnt_content_sha256']}`")
    lines.append("")

    # Input header
    lines.append("## Input")
    lines.append("")
    lines.append(f"- Source CSV: `{Path(inp['source_file']).name}`")
    lines.append(f"- Source SHA-256: `{inp['source_file_sha256'][:16]}...`")
    lines.append(f"- Records (T): **{inp['n_records']}**")
    lines.append(f"- Carriers (D): **{inp['n_carriers']}**")
    lines.append(f"- Carriers: " + ", ".join(inp['carriers']))
    lines.append(f"- Closed-data SHA-256: `{inp['closed_data_sha256'][:16]}...`")
    lines.append("")

    # Per-step CoDa view (head + tail)
    lines.append("## CoDa-standard per-step view")
    lines.append("")
    lines.append("Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).")
    lines.append("")
    lines.append("| t | label | Shannon H | Aitchison ‖h‖ | step Δ |")
    lines.append("|---|---|---|---|---|")
    head_n = min(5, len(timesteps))
    tail_n = min(3, max(0, len(timesteps) - head_n))
    for ts in timesteps[:head_n]:
        cs = ts["coda_standard"]
        step = cs["aitchison_distance_step"]
        step_s = "—" if step is None else f"{step:.4f}"
        lines.append(f"| {ts['index']} | {ts['label']} | {cs['shannon_entropy']:.4f} | {cs['aitchison_norm']:.4f} | {step_s} |")
    if tail_n > 0 and len(timesteps) > head_n + tail_n:
        lines.append("| ... | ... | ... | ... | ... |")
        for ts in timesteps[-tail_n:]:
            cs = ts["coda_standard"]
            step = cs["aitchison_distance_step"]
            step_s = "—" if step is None else f"{step:.4f}"
            lines.append(f"| {ts['index']} | {ts['label']} | {cs['shannon_entropy']:.4f} | {cs['aitchison_norm']:.4f} | {step_s} |")
    lines.append("")

    # Variation matrix and pair examination
    pairs = s2["carrier_pair_examination"]
    if pairs:
        lines.append("## Variation matrix τ_ij = var(log x_i / x_j)")
        lines.append("")
        lines.append("Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.")
        lines.append("")
        sorted_pairs = sorted(pairs, key=lambda p: p["pearson_r"], reverse=True)
        lines.append("### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)")
        lines.append("")
        lines.append("| i | j | Pearson r | bearing spread (deg) | locked? |")
        lines.append("|---|---|---|---|---|")
        for p in sorted_pairs[:5]:
            lines.append(f"| {p['i']} | {p['j']} | {p['pearson_r']:+.4f} | {p['bearing_spread_deg']:.1f}° | {'YES' if p['locked_pair'] else 'no'} |")
        lines.append("")
        lines.append("### Top 5 most-opposed carrier pairs (lowest Pearson r)")
        lines.append("")
        lines.append("| i | j | Pearson r | bearing spread (deg) | locked? |")
        lines.append("|---|---|---|---|---|")
        for p in sorted_pairs[-5:]:
            lines.append(f"| {p['i']} | {p['j']} | {p['pearson_r']:+.4f} | {p['bearing_spread_deg']:.1f}° | {'YES' if p['locked_pair'] else 'no'} |")
        lines.append("")

    # Section atlas
    secs = s1["sections"]
    if secs:
        lines.append("## Section atlas (CLR-space pair ranges)")
        lines.append("")
        lines.append(f"All C(D, 2) = {len(secs)} pairwise (i, j) coordinate ranges across the trajectory.")
        lines.append("")
        lines.append("| i | j | i_min | i_max | j_min | j_max |")
        lines.append("|---|---|---|---|---|---|")
        for s in secs[:10]:
            lines.append(f"| {s['i']} | {s['j']} | {s['i_min']:.3f} | {s['i_max']:.3f} | {s['j_min']:.3f} | {s['j_max']:.3f} |")
        if len(secs) > 10:
            lines.append(f"| ... ({len(secs) - 10} more) | | | | | |")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*")
    return "\n".join(lines)


def advanced_report(
    dataset_id: str,
    domain: str,
    description: str,
    citation: str,
    cnt_payload: Dict[str, Any],
    cnq_payload: Dict[str, Any],
) -> str:
    """Build the advanced (full Hˢ + CNQ v2) markdown report."""
    cnt_md = cnt_payload["metadata"]
    cnq_md = cnq_payload["metadata"]
    inp = cnt_payload["input"]
    s2 = cnt_payload["stages"]["stage2"]
    s3 = cnt_payload["stages"]["stage3"]
    helmsman = cnt_payload["helmsman_family"]
    depth = cnt_payload["depth_tower"]
    attractor = cnq_payload["attractor_fit"]
    cnq_view = cnq_payload["cnq_view"]
    chsh = cnq_payload.get("chsh_diagnostic") or {}

    lines: List[str] = []
    lines.append(f"# Advanced Analysis (Hˢ + CNQ v2) — {dataset_id}")
    lines.append("")
    lines.append(f"**Domain:** {domain}")
    lines.append(f"**Description:** {description}")
    lines.append(f"**Citation / source:** {citation}")
    lines.append("")
    lines.append(f"**CNT engine:** {cnt_md['engine']} v{cnt_md['engine_version']} (schema {cnt_md['schema_version']})")
    lines.append(f"**CNQ engine:** {cnq_md['engine']} v{cnq_md['engine_version']} (schema {cnq_md['schema_version']})")
    lines.append(f"**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*")
    lines.append(f"**cnt_content_sha256:** `{cnt_payload['diagnostics']['cnt_content_sha256']}`")
    lines.append(f"**cnq_content_sha256:** `{cnq_payload['diagnostics']['cnq_content_sha256']}`")
    lines.append("")
    lines.append("**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.")
    lines.append("")

    # Headline diagnostics
    lines.append("## Headline diagnostics")
    lines.append("")
    lines.append("| Quantity | Value | Interpretation |")
    lines.append("|---|---|---|")
    lines.append(f"| T (records) | {inp['n_records']} | Trajectory length |")
    lines.append(f"| D (carriers) | {inp['n_carriers']} | Compositional dimension |")
    lines.append(f"| Termination | `{depth['termination']['kind']}` | How the depth tower closed |")
    lines.append(f"| IR class | **`{depth['ir_class']}`** | Imaginary-Radius class — the Hˢ damping signature |")
    lines.append(f"| M²=I residual (max) | {depth['involution_M_squared']['max_residual_overall']:.3e} | Metric involution check; should be at IEEE floor |")
    lines.append(f"| M²=I verified | {'YES' if depth['involution_M_squared']['verified_at_ieee_floor'] else 'NO'} | < 10⁻¹⁰ floor pass |")
    period = attractor.get("period")
    period_s = "—" if not attractor.get("fitted") else str(period)
    lines.append(f"| Attractor fitted | {'YES' if attractor.get('fitted') else 'no'} | Whether a P2 cycle could be identified |")
    lines.append(f"| Period | {period_s} | If fitted, the cycle length |")
    lines.append(f"| Period stability | {attractor.get('period_stability', 0.0):.4f} | 0 = unstable, 1 = locked |")
    lines.append(f"| Amplitude A | {attractor.get('amplitude_A', 0.0):.4f} | Cycle amplitude |")
    lines.append(f"| Damping ζ | {attractor.get('damping_zeta', 0.0):+.4f} | Sign and magnitude of the dominant-pair damping |")
    lines.append(f"| Helmsman flips | {helmsman['flips']['total']} | Dominant-axis transitions across the trajectory |")
    lines.append(f"| Helmsman stability S_σ | {helmsman['stability_S_sigma']['global']:.4f} | Global trend persistence (1 = monotone, 0 = pure noise) |")
    if chsh:
        lines.append(f"| CHSH S | {chsh.get('S_value', 0.0) if isinstance(chsh, dict) else 0.0:.4f} | Joint-coherence diagnostic; classical bound 2.0, Tsirelson 2√2 |")
    lines.append(f"| CNQ dimension policy | `{cnq_view['dimension_policy']['label']}` | How CNQ v2 routes this D-value |")
    lines.append("")

    # IR class explanation
    ir_class = depth["ir_class"]
    ir_meaning = {
        "OVERDAMPED_EXTREME": "Strong damping, the system snaps to its attractor without overshooting. Common in well-regulated, near-equilibrium dynamics.",
        "OVERDAMPED": "Damping dominates. Small perturbations decay quickly; cycles do not develop.",
        "CRITICALLY_DAMPED": "Critical damping — fastest possible non-oscillatory return to equilibrium. Theoretical knife-edge.",
        "MODERATELY_DAMPED": "Damping is present but cycles can develop. Intermediate regime.",
        "LIGHTLY_DAMPED": "Cycles develop but eventually decay. Underlying oscillatory dynamics with weak friction.",
        "UNDAMPED": "No damping detected — pure cycling, conservative system.",
        "LIMIT_CYCLE_P2": "A locked period-2 cycle. Universal compositional invariance signature.",
    }.get(ir_class, "(class meaning not in standard taxonomy)")
    lines.append(f"**IR class meaning:** {ir_meaning}")
    lines.append("")

    # Helmsman family
    lines.append("## Helmsman family")
    lines.append("")
    lines.append("The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).")
    lines.append("")
    lines.append("| Field | Value |")
    lines.append("|---|---|")
    lines.append(f"| Total flips | {helmsman['flips']['total']} |")
    lines.append(f"| Stability S_σ (global) | {helmsman['stability_S_sigma']['global']:.4f} |")
    chaos_block = helmsman.get("chaos_indicator") or {}
    chaos = chaos_block.get("value") if isinstance(chaos_block, dict) else None
    if chaos is not None:
        lines.append(f"| Chaos indicator | {chaos:.4f} |")
    torque_block = helmsman.get("torque_proxy") or {}
    torque = torque_block.get("global_mean") if isinstance(torque_block, dict) else None
    if torque is not None:
        lines.append(f"| Torque proxy (global mean) | {torque:.4f} |")
    lines.append("")

    # Depth tower
    lines.append("## Depth tower (Hˢ involution ladder)")
    lines.append("")
    lines.append("The depth tower iterates the M operator until convergence, with each level recording its M²=I residual. Termination signals the structure of the dynamics.")
    lines.append("")
    levels = depth.get("levels", [])
    if levels:
        lines.append("| level | M²=I residual | termination flag |")
        lines.append("|---|---|---|")
        for lev in levels[:5]:
            lines.append(f"| {lev.get('level', '—')} | {lev.get('M_squared_residual', 0.0):.3e} | {lev.get('terminated', False)} |")
        if len(levels) > 5:
            lines.append(f"| ... ({len(levels) - 5} more) | | |")
        lines.append("")
    lines.append(f"**Termination:** `{depth['termination']['kind']}`")
    if depth['termination'].get('reason'):
        lines.append(f"**Reason:** {depth['termination']['reason']}")
    lines.append("")

    # CNQ view
    lines.append("## CNQ v2 quaternion view")
    lines.append("")
    lines.append("CNQ v2 names the algebra the trajectory lives in. For each step it computes a bearing angle (direction in CLR space, mod 2π) and a radial amplitude. The dimension policy tells you which factoring branch CNQ took for this D.")
    lines.append("")
    lines.append("| Field | Value |")
    lines.append("|---|---|")
    lines.append(f"| Dimension policy | `{cnq_view['dimension_policy']['label']}` |")
    lines.append(f"| D | {cnq_view['dimension_policy']['D']} |")
    lines.append(f"| Branch | `{cnq_view['dimension_policy'].get('branch', '—')}` |")
    bearing = cnq_view.get("bearing_trajectory") or {}
    radial = cnq_view.get("radial_trajectory") or {}
    if isinstance(bearing, dict) and bearing.get("per_step"):
        per_step = bearing["per_step"]
        angles = [s.get("angle_rad", 0.0) for s in per_step if isinstance(s, dict)]
        if angles:
            lines.append(f"| Bearing angle range | {min(angles):.4f} to {max(angles):.4f} rad |")
            lines.append(f"| Bearing angle mean | {sum(angles) / len(angles):.4f} rad |")
            lines.append(f"| Bearing pairs tested | {bearing.get('n_pairs_tested', '—')} |")
            lines.append(f"| Bearing max residual | {bearing.get('max_residual', 0.0):.2e} |")
            lines.append(f"| Bearing gate pass | {'YES' if bearing.get('gate_pass') else 'NO'} |")
            lines.append(f"| Captured step fraction (mean) | {bearing.get('captured_step_fraction_mean', 0.0):.4f} |")
            lines.append(f"| Captured step fraction (global) | {bearing.get('captured_step_fraction_global', 0.0):.4f} |")
    if isinstance(radial, dict) and radial.get("per_step"):
        rad_per_step = radial["per_step"]
        radii = [s.get("radius", 0.0) for s in rad_per_step if isinstance(s, dict)]
        if radii:
            lines.append(f"| Radial range | {min(radii):.4f} to {max(radii):.4f} |")
            lines.append(f"| Radial mean | {sum(radii) / len(radii):.4f} |")
    if chsh:
        lines.append(f"| CHSH S | {chsh.get('S_value', 0.0):.4f} |")
        lines.append(f"| CHSH classical bound | {chsh.get('classical_bound', 2.0):.1f} |")
        lines.append(f"| CHSH Tsirelson bound | {chsh.get('tsirelson_bound', 2.0 * (2 ** 0.5)):.4f} |")
    lines.append("")

    # Carrier pair coherence
    pairs = s2.get("carrier_pair_examination", [])
    if pairs:
        sorted_pairs = sorted(pairs, key=lambda p: abs(p["pearson_r"]), reverse=True)
        lines.append("## Carrier-pair coherence ranking")
        lines.append("")
        lines.append("Pairs ranked by |Pearson r| on CLR.")
        lines.append("")
        lines.append("| i | j | Pearson r | bearing spread (deg) | locked? |")
        lines.append("|---|---|---|---|---|")
        for p in sorted_pairs[:8]:
            lines.append(f"| {p['i']} | {p['j']} | {p['pearson_r']:+.4f} | {p['bearing_spread_deg']:.1f}° | {'YES' if p['locked_pair'] else 'no'} |")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*")
    return "\n".join(lines)
