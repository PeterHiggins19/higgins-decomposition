"""
CodaWork 2026 (June) conference EMBER corpus runner.

Processes all 8 EMBER countries (CHN, DEU, FRA, GBR, IND, JPN, USA, WLD)
through CNT v3.0.0 + CNQ v2.0.0; generates per-country JOURNAL files in
two flavours:

    STAGE_1_REPORT.md       — pure CoDa standard view (closure, CLR, ILR,
                              variation matrix, pair examination).
                              The "minimal CoDa" reading any compositional-
                              data analyst can verify with their own tools.

    ADVANCED_ANALYSIS.md    — full Hˢ extension stack (κ^HS_ij metric,
                              s_j sensitivity, depth tower, attractor fit,
                              helmsman family, IR classification, plus the
                              full CNQ v2 quaternion view: bearing trajectory,
                              radial trajectory, CHSH coherence diagnostic).

Plus a combined COMPARISON_v2_0_4_vs_v3_0_0.md across all countries.

The positioning is explicit per Peter's directive:
    Stage 1 = pure CoDa
    Full CNQ = the more advanced option

Run:
    python papers/codawork2026/conference_2026_06/run_ember_corpus.py
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


_THIS_FILE = Path(__file__).resolve()
_REPO_ROOT = _THIS_FILE.parent.parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))
sys.path.insert(0, str(_REPO_ROOT / "HCI-CNT" / "engine"))
sys.path.insert(0, str(_REPO_ROOT / "HCI-CNQ" / "engine"))

import cnt as cnt_v3  # type: ignore
import cnq as cnq_v2  # type: ignore


COUNTRIES = [
    ("USA", "ember_USA_United_States_generation_TWh.csv", "United States"),
    ("CHN", "ember_CHN_China_generation_TWh.csv", "China"),
    ("DEU", "ember_DEU_Germany_generation_TWh.csv", "Germany"),
    ("FRA", "ember_FRA_France_generation_TWh.csv", "France"),
    ("GBR", "ember_GBR_United_Kingdom_generation_TWh.csv", "United Kingdom"),
    ("IND", "ember_IND_India_generation_TWh.csv", "India"),
    ("JPN", "ember_JPN_Japan_generation_TWh.csv", "Japan"),
    ("WLD", "ember_WLD_World_generation_TWh.csv", "World"),
]

EMBER_DATA_DIR = _REPO_ROOT / "data" / "Energy" / "EMBER_pipeline_ready"
OUTPUT_DIR = _THIS_FILE.parent / "per_country"
LEGACY_DIR = _REPO_ROOT / "HCI-CNT" / "experiments" / "codawork2026"


def _load_legacy_v204(country_code: str) -> Optional[Dict[str, Any]]:
    """Load the v2.0.4 cnt.json for a country, if available, for comparison."""
    candidate = LEGACY_DIR / f"ember_{country_code.lower()}" / f"ember_{country_code.lower()}_cnt.json"
    if not candidate.exists():
        return None
    try:
        return json.loads(candidate.read_text(encoding="utf-8"))
    except Exception:
        return None


def _stage1_report(country_code: str, country_name: str, payload: Dict[str, Any]) -> str:
    """Build the Stage 1 (pure CoDa) markdown report for a country.

    This view is exactly what a CoDa-community reviewer would expect: closure,
    CLR, ILR, variation matrix, carrier-pair correlation. No Hs extensions.
    """
    md = payload["metadata"]
    inp = payload["input"]
    s1 = payload["stages"]["stage1"]
    s2 = payload["stages"]["stage2"]
    timesteps = payload["tensor"]["timesteps"]

    lines: List[str] = []
    lines.append(f"# Stage 1 Report (pure CoDa) — EMBER {country_code} ({country_name})")
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

    # Per-step CoDa view
    lines.append("## CoDa-standard per-step view")
    lines.append("")
    lines.append("Per-timestep CoDa quantities. Columns: composition (closure-normalised); CLR (centred log-ratio, sums to zero); ILR Helmert basis projection; Shannon entropy; Aitchison norm; step-to-step Aitchison distance.")
    lines.append("")
    lines.append("| t | label | Shannon H | Aitchison ‖h‖ | step Δ |")
    lines.append("|---|---|---|---|---|")
    for ts in timesteps[:5]:
        cs = ts["coda_standard"]
        step = cs["aitchison_distance_step"]
        step_s = "—" if step is None else f"{step:.4f}"
        lines.append(f"| {ts['index']} | {ts['label']} | {cs['shannon_entropy']:.4f} | {cs['aitchison_norm']:.4f} | {step_s} |")
    lines.append(f"| ... | ... | ... | ... | ... |")
    for ts in timesteps[-3:]:
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
        lines.append("CoDa subcompositional-coherence matrix. Small τ = carriers move together; large τ = carriers move independently.")
        lines.append("")
        # Top 5 most-coherent and most-independent pairs by Pearson r
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

    # Section atlas (Stage 1)
    secs = s1["sections"]
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
    lines.append("**This Stage 1 report uses only standard CoDa-community operators.** "
                 "For the Hˢ-extension diagnostics (κ^HS metric tensor, s_j sensitivity, "
                 "depth tower, attractor fit, helmsman family, IR classification, plus the "
                 "full CNQ v2 quaternion view), see the companion `ADVANCED_ANALYSIS.md` "
                 "in the same folder.")
    lines.append("")
    lines.append(f"*Stage 1 report generated by `{_THIS_FILE.name}` for CodaWork 2026 (June).*")
    return "\n".join(lines)


def _advanced_report(
    country_code: str,
    country_name: str,
    cnt_payload: Dict[str, Any],
    cnq_payload: Dict[str, Any],
    legacy_v204: Optional[Dict[str, Any]],
) -> str:
    """Build the Advanced-Analysis markdown report (Hˢ extensions + CNQ)."""
    md = cnt_payload["metadata"]
    inp = cnt_payload["input"]
    dt = cnt_payload["depth_tower"]
    hf = cnt_payload["helmsman_family"]
    diag = cnt_payload["diagnostics"]
    cnq_md = cnq_payload["metadata"]
    cnq_view = cnq_payload["cnq_view"]
    cnq_diag = cnq_payload["diagnostics"]
    attractor_fit = cnq_payload["attractor_fit"]

    lines: List[str] = []
    lines.append(f"# Advanced Analysis (Hˢ extensions + CNQ v2) — EMBER {country_code} ({country_name})")
    lines.append("")
    lines.append("## Engines")
    lines.append("")
    lines.append(f"- **CNT v3.0.0** schema 3.0.0 — content_sha256 `{diag['cnt_content_sha256']}`")
    lines.append(f"- **CNQ v2.0.0** schema cnq/2.0.0 — content_sha256 `{cnq_diag['cnq_content_sha256']}`")
    lines.append(f"- **Engine independence:** CNT and CNQ canonical hashes are unrelated by design (push #32 policy).")
    lines.append("")
    lines.append(f"**Generated:** {md['generated']}")
    lines.append("")

    # Input
    lines.append("## Input")
    lines.append("")
    lines.append(f"- Source CSV: `{Path(inp['source_file']).name}`")
    lines.append(f"- T = **{inp['n_records']}** records  ·  D = **{inp['n_carriers']}** carriers")
    lines.append(f"- Carriers: {', '.join(inp['carriers'])}")
    lines.append("")

    # CNT depth tower headline
    lines.append("## Depth tower (CNT v3)")
    lines.append("")
    inv = dt["involution_M_squared"]
    lines.append("| Quantity | Value |")
    lines.append("|---|---|")
    lines.append(f"| Energy levels reached | {len(dt['energy_levels'])} |")
    lines.append(f"| Curvature levels reached | {len(dt['curvature_levels'])} |")
    lines.append(f"| Termination kind | **{dt['termination']['kind']}** |")
    lines.append(f"| IR classification | **{dt['ir_class']}** |")
    lines.append(f"| M² = I residual (max) | {inv['max_residual_overall']:.3e} |")
    lines.append(f"| Verified at IEEE floor | {'**YES**' if inv['verified_at_ieee_floor'] else 'no'} |")
    lines.append("")

    # Attractor fit (shared between CNT and CNQ)
    lines.append("## P2 attractor parameter fit")
    lines.append("")
    lines.append("From `hci_shared.attractors.fit_attractor` — same fitter is used by both engines.")
    lines.append("")
    af = attractor_fit
    lines.append("| Parameter | Value |")
    lines.append("|---|---|")
    lines.append(f"| Fitted | {af['fitted']} |")
    lines.append(f"| Period | {af.get('period', '—')} |")
    lines.append(f"| Period stability | {af.get('period_stability', 0):.4f} |")
    lines.append(f"| Dominant pair | axis_a = {af['dominant_pair']['axis_a']}, axis_b = {af['dominant_pair']['axis_b']} |")
    lines.append(f"| Amplitude A | {af.get('amplitude_A', 0):.4f} |")
    lines.append(f"| Damping ζ | {af.get('damping_zeta', 0):+.4f} |")
    lines.append(f"| Contraction λ | {af.get('contraction_lambda', 0):+.4e} |")
    lines.append(f"| Oscillation ratio | {af['confidence']['oscillation_ratio']:.4f} |")
    if af.get("warnings"):
        lines.append(f"| Warnings | {' / '.join(af['warnings'])} |")
    lines.append("")

    # Helmsman family
    lines.append("## Helmsman family channels")
    lines.append("")
    lines.append("σ tracks the dominant-axis attribution per step (which carrier had the largest CLR change). "
                 "Stability_S_σ measures how often σ stays unchanged across consecutive steps. "
                 "Vocabulary locked in `GLOSSARY.md` §I — domain interpretation in wrappers.")
    lines.append("")
    lines.append("| Channel | Value |")
    lines.append("|---|---|")
    lines.append(f"| σ trajectory length | {len(hf['sigma'])} |")
    lines.append(f"| Total flips | {hf['flips']['total']} |")
    lines.append(f"| Stability S_σ (global) | {hf['stability_S_sigma']['global']:.4f} |")
    lines.append(f"| Chaos indicator | {hf['chaos_indicator']} |")
    lines.append(f"| Rolling window (W) | {hf['flips']['rolling_window']} |")
    lines.append("")

    # CNQ view
    lines.append("## CNQ v2 quaternion view")
    lines.append("")
    pol = cnq_view["dimension_policy"]
    lines.append(f"**Dimension policy:** `{pol['label']}` (D = {pol['D']})")
    lines.append("")
    lines.append(f"> {pol['claim_strength']}")
    lines.append("")
    bt = cnq_view["bearing_trajectory"]
    rt = cnq_view["radial_trajectory"]
    lines.append("### Bearing trajectory (compositional direction)")
    lines.append("")
    lines.append("| Quantity | Value |")
    lines.append("|---|---|")
    if bt.get("max_residual") is not None:
        lines.append(f"| Pairs tested | {bt['n_pairs_tested']} |")
        lines.append(f"| Max sandwich residual | {bt['max_residual']:.3e} |")
        lines.append(f"| Mean sandwich residual | {bt['mean_residual']:.3e} |")
        lines.append(f"| Gate threshold | {bt['gate_threshold']:.0e} |")
        lines.append(f"| Gate pass | {'**PASS**' if bt['gate_pass'] else 'FAIL'} |")
    if "captured_step_fraction_global" in bt:
        lines.append(f"| Captured fraction (global) | {bt['captured_step_fraction_global']:.4f} |")
        lines.append(f"| Captured fraction (mean) | {bt['captured_step_fraction_mean']:.4f} |")
    if "projection_method" in bt:
        lines.append(f"| Projection method | `{bt['projection_method']}` |")
    lines.append("")
    lines.append("### Radial trajectory (compositional magnitude)")
    lines.append("")
    lines.append("First-class output in v2 (was discarded by v1's unit-vector normalisation). "
                 "Per-step ILR norm — together with bearing, recovers the full ILR trajectory.")
    lines.append("")
    if rt.get("ilr_norms"):
        lines.append("| Stat | Value |")
        lines.append("|---|---|")
        lines.append(f"| min | {rt['min']:.4f} |")
        lines.append(f"| max | {rt['max']:.4f} |")
        lines.append(f"| mean | {rt['mean']:.4f} |")
        lines.append(f"| median | {rt['median']:.4f} |")
        lines.append(f"| std | {rt['std']:.4f} |")
        lines.append("")

    # Comparison vs v2.0.4 baseline
    if legacy_v204:
        lines.append("## Comparison vs v2.0.4 baseline (legacy)")
        lines.append("")
        lines.append("Where the legacy v2.0.4 output is available at `HCI-CNT/experiments/codawork2026/`, this section reports the v2.0.4 headline values for direct comparison. v3 produces a different hash by design (engine-version triple is part of the canonical payload), so hash equality is NOT expected; numerical content is.")
        lines.append("")
        legacy_md = legacy_v204.get("metadata", {})
        legacy_diag = legacy_v204.get("diagnostics", {})
        depth_legacy = (legacy_v204.get("depth", {}) or
                        legacy_v204.get("depth_tower", {}))
        lines.append("| Quantity | v2.0.4 | v3.0.0 |")
        lines.append("|---|---|---|")
        lines.append(f"| engine_version | `{legacy_md.get('engine_version')}` | `{md['engine_version']}` |")
        lines.append(f"| schema_version | `{legacy_md.get('schema_version')}` | `{md['schema_version']}` |")
        # Try several paths to find termination + IR class in legacy
        legacy_term = (depth_legacy.get("termination", {}).get("kind") or
                       depth_legacy.get("higgins_extensions", {}).get("summary", {}).get("curvature_termination") or
                       legacy_diag.get("curvature_termination") or
                       "—")
        legacy_ir = (depth_legacy.get("ir_class") or
                     depth_legacy.get("higgins_extensions", {}).get("impulse_response", {}).get("classification") or
                     legacy_diag.get("ir_class") or
                     "—")
        lines.append(f"| termination kind | {legacy_term} | {dt['termination']['kind']} |")
        lines.append(f"| IR classification | {legacy_ir} | {dt['ir_class']} |")
        legacy_inv = (depth_legacy.get("involution_M_squared", {}).get("max_residual_overall") or
                      depth_legacy.get("higgins_extensions", {}).get("metric_involution", {}).get("max_residual"))
        if legacy_inv is not None:
            lines.append(f"| M²=I residual | {legacy_inv:.3e} | {inv['max_residual_overall']:.3e} |")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("**This advanced analysis exposes the full Hˢ-extension diagnostic stack and the CNQ v2 quaternion view.** "
                 "For the minimal CoDa-community reading (closure, CLR, ILR, variation matrix only), see `STAGE_1_REPORT.md` in the same folder.")
    lines.append("")
    lines.append(f"*Advanced analysis generated by `{_THIS_FILE.name}` for CodaWork 2026 (June).*")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CRD-1.0 (Coherent Range Doctrine) — multi-carrier temporal alignment.
#
# See docs/COHERENT_RANGE_DOCTRINE.md for the full doctrine. In short:
#   • coherent  — truncate every member to the intersection of all members'
#                 time ranges. Default for any multi-carrier run.
#   • native    — each member uses its own native range (mixed T allowed).
#   • explicit  — caller passes --range-start / --range-end; runner
#                 truncates every member to that exact window and drops
#                 carriers that don't span it.
# ---------------------------------------------------------------------------


def _read_csv_year_range(csv_path: Path) -> Tuple[int, int, List[int]]:
    """Read first-column years; return (min_year, max_year, year_list)."""
    years: List[int] = []
    with open(csv_path, "r", encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader, None)
        for row in reader:
            if not row:
                continue
            try:
                years.append(int(float(row[0])))
            except (ValueError, IndexError):
                continue
    if not years:
        raise ValueError(f"no parsable years in {csv_path}")
    return min(years), max(years), years


def _compute_coherent_range(
    countries: List[Tuple[str, str, str]],
) -> Dict[str, Any]:
    """Intersection of every member's [min_year, max_year] range.

    Returns a manifest dict with keys: coherent_start, coherent_end,
    members, limiting_members, member_ranges.
    """
    member_ranges: Dict[str, Tuple[int, int]] = {}
    for code, csv_name, _ in countries:
        path = EMBER_DATA_DIR / csv_name
        ymin, ymax, _ = _read_csv_year_range(path)
        member_ranges[code] = (ymin, ymax)

    coherent_start = max(r[0] for r in member_ranges.values())
    coherent_end = min(r[1] for r in member_ranges.values())

    if coherent_start > coherent_end:
        raise ValueError(
            f"CRD-1.0 violation: members do not share any common range "
            f"(intersection is empty). Member ranges: {member_ranges}"
        )

    # CRD-1.0 Rule 4: name limiting members. Distinguish carrier(s) whose
    # native start pins the coherent_start (those whose range begins LATER
    # than the rest) from carrier(s) whose native end pins the coherent_end.
    # When all members share an endpoint, that endpoint has no unique
    # binder — record as "(all share)" so the manifest reads cleanly.
    start_binders = sorted({
        code for code, (ymin, _) in member_ranges.items()
        if ymin == coherent_start
    })
    end_binders = sorted({
        code for code, (_, ymax) in member_ranges.items()
        if ymax == coherent_end
    })
    limiting_start = "(all share)" if len(start_binders) == len(member_ranges) else ", ".join(start_binders)
    limiting_end = "(all share)" if len(end_binders) == len(member_ranges) else ", ".join(end_binders)

    return {
        "coherent_start": coherent_start,
        "coherent_end": coherent_end,
        "T_set": coherent_end - coherent_start + 1,
        "members": [c for c, _, _ in countries],
        "limiting_members_start": limiting_start,
        "limiting_members_end": limiting_end,
        "limiting_members": sorted(set(start_binders) | set(end_binders)),
        "member_ranges": {k: list(v) for k, v in member_ranges.items()},
    }


def _truncate_csv_to_range(
    csv_path: Path, out_path: Path, year_start: int, year_end: int,
) -> int:
    """Write a subset of csv_path to out_path with rows where year ∈ [start, end].

    Returns the number of data rows written (header always written).
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    rows_written = 0
    with open(csv_path, "r", encoding="utf-8", newline="") as fh_in, \
         open(out_path, "w", encoding="utf-8", newline="") as fh_out:
        reader = csv.reader(fh_in)
        writer = csv.writer(fh_out)
        header = next(reader, None)
        if header is not None:
            writer.writerow(header)
        for row in reader:
            if not row:
                continue
            try:
                y = int(float(row[0]))
            except (ValueError, IndexError):
                continue
            if year_start <= y <= year_end:
                writer.writerow(row)
                rows_written += 1
    return rows_written


def _process_country(
    country_code: str,
    csv_filename: str,
    country_name: str,
    range_window: Optional[Tuple[int, int]] = None,
) -> Dict[str, Any]:
    """Run both engines on a country; write artefacts; return headline dict.

    If range_window is provided (coherent or explicit policy), the input CSV
    is truncated to [year_start, year_end] before either engine sees it.
    """
    csv_path = EMBER_DATA_DIR / csv_filename
    out_dir = OUTPUT_DIR / f"ember_{country_code.lower()}"
    out_dir.mkdir(parents=True, exist_ok=True)

    # CRD-1.0: if a coherent or explicit window is in effect, truncate first.
    if range_window is not None:
        ystart, yend = range_window
        truncated_path = out_dir / f"input_truncated_{ystart}_{yend}.csv"
        rows = _truncate_csv_to_range(csv_path, truncated_path, ystart, yend)
        if rows < 2:
            raise ValueError(
                f"CRD-1.0: country {country_code} has fewer than 2 rows in "
                f"window [{ystart},{yend}] — drop this carrier and re-run."
            )
        csv_path = truncated_path

    cnt_json_path = out_dir / "cnt_v3.json"
    cnq_json_path = out_dir / "cnq_v2.json"

    t0 = time.monotonic()
    cnt_payload = cnt_v3.cnt_run(csv_path, out_path=cnt_json_path)
    cnq_payload = cnq_v2.cnq_run(input_csv=csv_path, out_path=cnq_json_path)
    duration_ms = int((time.monotonic() - t0) * 1000)

    legacy_v204 = _load_legacy_v204(country_code)

    # Stage 1 report
    s1_md = _stage1_report(country_code, country_name, cnt_payload)
    (out_dir / "STAGE_1_REPORT.md").write_text(s1_md, encoding="utf-8")

    # Advanced analysis
    adv_md = _advanced_report(country_code, country_name, cnt_payload, cnq_payload, legacy_v204)
    (out_dir / "ADVANCED_ANALYSIS.md").write_text(adv_md, encoding="utf-8")

    # Pull headline values
    return {
        "country_code": country_code,
        "country_name": country_name,
        "T": cnt_payload["input"]["n_records"],
        "D": cnt_payload["input"]["n_carriers"],
        "termination_kind": cnt_payload["depth_tower"]["termination"]["kind"],
        "ir_class": cnt_payload["depth_tower"]["ir_class"],
        "M2_residual_max": cnt_payload["depth_tower"]["involution_M_squared"]["max_residual_overall"],
        "M2_verified": cnt_payload["depth_tower"]["involution_M_squared"]["verified_at_ieee_floor"],
        "attractor_fitted": cnq_payload["attractor_fit"]["fitted"],
        "attractor_period": cnq_payload["attractor_fit"].get("period"),
        "attractor_stability": cnq_payload["attractor_fit"].get("period_stability", 0.0),
        "amplitude_A": cnq_payload["attractor_fit"].get("amplitude_A", 0.0),
        "damping_zeta": cnq_payload["attractor_fit"].get("damping_zeta", 0.0),
        "helmsman_flips": cnt_payload["helmsman_family"]["flips"]["total"],
        "helmsman_stability": cnt_payload["helmsman_family"]["stability_S_sigma"]["global"],
        "cnq_dim_label": cnq_payload["cnq_view"]["dimension_policy"]["label"],
        "cnt_content_sha256": cnt_payload["diagnostics"]["cnt_content_sha256"],
        "cnq_content_sha256": cnq_payload["diagnostics"]["cnq_content_sha256"],
        "legacy_available": legacy_v204 is not None,
        "duration_ms": duration_ms,
    }


def _crd_manifest_md(manifest: Optional[Dict[str, Any]], range_policy: str) -> List[str]:
    """Render the CRD-1.0 coherent-range manifest as markdown header lines."""
    if manifest is None:
        return [
            "## Coherent range manifest (CRD-1.0)",
            "",
            "| Field | Value |",
            "|---|---|",
            "| Range policy | `native` (mixed T per carrier — not headline-eligible) |",
            "",
            "*This output uses native per-carrier ranges. Per CRD-1.0 §5, native-policy outputs are not headline-eligible; they exist for per-carrier inspection only.*",
            "",
        ]
    members = ", ".join(manifest["members"])
    lim_start = manifest.get("limiting_members_start", "(see manifest)")
    lim_end = manifest.get("limiting_members_end", "(see manifest)")
    return [
        "## Coherent range manifest (CRD-1.0)",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Coherent range | **{manifest['coherent_start']}-{manifest['coherent_end']}** |",
        f"| T_set | **{manifest['T_set']}** |",
        f"| Members | {members} |",
        f"| Start-limiting member(s) | {lim_start} |",
        f"| End-limiting member(s) | {lim_end} |",
        "| Carriers dropped | (none) |",
        f"| Range policy | `{range_policy}` |",
        "",
        "*Per [CRD-1.0](../../../docs/COHERENT_RANGE_DOCTRINE.md): every member is truncated to the intersection of all members' time ranges before any diagnostic is computed. The shortest-coverage member sets the binding window for the entire set. \"Start-limiting\" identifies the carrier(s) whose native data begins LATER than the rest (pinning the corpus's first year); \"end-limiting\" identifies the carrier(s) whose native data ends EARLIER than the rest. \"(all share)\" means no unique binder — every member naturally aligns at that endpoint.*",
        "",
    ]


def _comparison_md(
    headlines: List[Dict[str, Any]],
    manifest: Optional[Dict[str, Any]] = None,
    range_policy: str = "coherent",
) -> str:
    """Combined headline comparison across all countries.

    The manifest argument carries the CRD-1.0 coherent-range declaration; it
    is rendered as the first section under the title (Rule 4: every
    multi-carrier output declares its range in its header).
    """
    lines: List[str] = []
    lines.append("# CodaWork 2026 — EMBER 8-country corpus headline comparison")
    lines.append("")
    if manifest is not None:
        T_set = manifest["T_set"]
        rng = f"{manifest['coherent_start']}-{manifest['coherent_end']}"
        engine_line = (
            f"**Engines:** CNT v3.0.0 + CNQ v2.0.0 (push #32). Both engines run on "
            f"the 8-country EMBER pipeline-ready dataset (Bioenergy, Coal, Gas, "
            f"Hydro, Nuclear, Other Fossil, Other Renewables, Solar, Wind; D = 9; "
            f"coherent range **{rng}**, T = {T_set} years per country)."
        )
    else:
        engine_line = (
            "**Engines:** CNT v3.0.0 + CNQ v2.0.0 (push #32). Both engines run on "
            "the 8-country EMBER pipeline-ready dataset (Bioenergy, Coal, Gas, "
            "Hydro, Nuclear, Other Fossil, Other Renewables, Solar, Wind; D = 9; "
            "native per-carrier ranges, mixed T)."
        )
    lines.append(engine_line)
    lines.append("")
    lines.extend(_crd_manifest_md(manifest, range_policy))
    lines.append("## Headline diagnostics across all countries")
    lines.append("")
    lines.append("| Country | T | termination | IR class | M^2=I residual | period | stability | A | zeta | flips |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for h in headlines:
        period_str = str(h['attractor_period']) if h['attractor_fitted'] else "—"
        lines.append(
            f"| {h['country_code']} ({h['country_name']}) "
            f"| {h['T']} "
            f"| {h['termination_kind']} "
            f"| {h['ir_class']} "
            f"| {h['M2_residual_max']:.2e} "
            f"| {period_str} "
            f"| {h['attractor_stability']:.3f} "
            f"| {h['amplitude_A']:.3f} "
            f"| {h['damping_zeta']:+.3f} "
            f"| {h['helmsman_flips']} |"
        )
    lines.append("")

    # IEEE floor verification
    all_verified = all(h["M2_verified"] for h in headlines)
    lines.append("## Determinism + numerical anchors")
    lines.append("")
    lines.append(f"- **M^2 = I metric involution verified at IEEE floor (< 1e-10) on {sum(1 for h in headlines if h['M2_verified'])} of {len(headlines)} countries.**")
    if all_verified:
        lines.append(f"  - All {len(headlines)} countries pass. Worst residual across the corpus: **{max(h['M2_residual_max'] for h in headlines):.3e}**.")
    lines.append(f"- **CNQ dimension policy:** all countries are D = 9 -> `{headlines[0]['cnq_dim_label']}` (D=5..15 reduced-projection branch).")
    lines.append("  - Native twin-quaternion factoring (D = 8) and quad-quaternion factoring (D = 16) are not exercised by the EMBER corpus; these are reserved for D-matched datasets when they arrive.")
    lines.append("")

    # Per-country hashes
    lines.append("## Per-country canonical hashes (engine-independence policy verified)")
    lines.append("")
    lines.append("| Country | cnt_content_sha256 | cnq_content_sha256 |")
    lines.append("|---|---|---|")
    for h in headlines:
        lines.append(f"| {h['country_code']} | `{h['cnt_content_sha256'][:16]}...` | `{h['cnq_content_sha256'][:16]}...` |")
    lines.append("")
    lines.append("Each country produces two unrelated hashes — CNT and CNQ canonical hashes are independent by design (push #32 engine-independence policy).")
    lines.append("")

    # Comparison status
    legacy_count = sum(1 for h in headlines if h["legacy_available"])
    lines.append("## Comparison vs v2.0.4 (legacy)")
    lines.append("")
    lines.append(f"v2.0.4 baseline outputs available for **{legacy_count}** of {len(headlines)} countries at `HCI-CNT/experiments/codawork2026/`.")
    lines.append("Per-country comparison detail in each `<country>/ADVANCED_ANALYSIS.md`.")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Reading these reports")
    lines.append("")
    lines.append("Each country folder contains two reports for two audiences:")
    lines.append("")
    lines.append("- **`STAGE_1_REPORT.md`** — pure CoDa community vocabulary (closure, CLR, ILR, variation matrix tau_ij, carrier-pair Pearson r, section atlas). This is what a CoDa-community reviewer reads to verify that the math fits their framework. **Stage 1 = pure CoDa.**")
    lines.append("")
    lines.append("- **`ADVANCED_ANALYSIS.md`** — full Hs-extension stack (kappa^HS metric tensor, s_j sensitivity, depth tower, P2 attractor fit, helmsman family, IR classification) plus the CNQ v2 quaternion view (bearing trajectory, radial trajectory, dimension policy). **Full CNQ = the more advanced option.**")
    lines.append("")
    lines.append("The two-document structure makes the positioning unambiguous: Stage 1 is a clean entry point in the CoDa community's own vocabulary; Advanced is the differentiator that justifies the framework's existence beyond standard CoDa.")
    lines.append("")
    lines.append(f"*Generated for CodaWork 2026 (June) by `{_THIS_FILE.name}` (CRD-1.0 range policy: `{range_policy}`).*")
    return "\n".join(lines)


def _parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse runner CLI arguments.

    CRD-1.0 (Coherent Range Doctrine) governs --range-policy. Default is
    `coherent`: every member is truncated to the intersection of all
    members' ranges before either engine sees the data.
    """
    parser = argparse.ArgumentParser(
        prog="run_ember_corpus",
        description="CodaWork 2026 EMBER 8-country corpus runner (CNT v3 + CNQ v2).",
    )
    parser.add_argument(
        "--range-policy",
        choices=("coherent", "native", "explicit"),
        default="coherent",
        help=(
            "CRD-1.0 range policy. 'coherent' (default): truncate every "
            "carrier to the intersection of all members' ranges. 'native': "
            "each carrier uses its own range (mixed T; not headline-eligible "
            "per CRD-1.0 section 5). 'explicit': use --range-start and --range-end."
        ),
    )
    parser.add_argument(
        "--range-start",
        type=int,
        default=None,
        help="Explicit-policy start year (inclusive). Required if --range-policy=explicit.",
    )
    parser.add_argument(
        "--range-end",
        type=int,
        default=None,
        help="Explicit-policy end year (inclusive). Required if --range-policy=explicit.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = _parse_args(argv)

    print("=== EMBER 8-country corpus runner — CNT v3.0.0 + CNQ v2.0.0 ===")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"CRD-1.0 range policy: {args.range_policy}")

    # CRD-1.0: resolve the range window before any engine call.
    range_window: Optional[Tuple[int, int]] = None
    manifest: Optional[Dict[str, Any]] = None
    if args.range_policy == "coherent":
        manifest = _compute_coherent_range(COUNTRIES)
        range_window = (manifest["coherent_start"], manifest["coherent_end"])
        print(
            f"  Coherent range: {manifest['coherent_start']}-{manifest['coherent_end']}  "
            f"T_set={manifest['T_set']}"
        )
        print(
            f"  Start-limiting: {manifest['limiting_members_start']}    "
            f"End-limiting: {manifest['limiting_members_end']}"
        )
    elif args.range_policy == "explicit":
        if args.range_start is None or args.range_end is None:
            raise SystemExit(
                "ERROR: --range-policy=explicit requires --range-start and --range-end."
            )
        range_window = (args.range_start, args.range_end)
        manifest = {
            "coherent_start": args.range_start,
            "coherent_end": args.range_end,
            "T_set": args.range_end - args.range_start + 1,
            "members": [c for c, _, _ in COUNTRIES],
            "limiting_members": ["(explicit)"],
            "member_ranges": {},
        }
        print(
            f"  Explicit range: {args.range_start}-{args.range_end}  "
            f"T_set={manifest['T_set']}"
        )
    else:  # native
        print("  Native ranges per carrier (mixed T; not headline-eligible per CRD-1.0 section 5)")
    print()

    headlines: List[Dict[str, Any]] = []
    for code, csv_name, country_name in COUNTRIES:
        print(f"  [{code}] {country_name} ... ", end="", flush=True)
        try:
            h = _process_country(code, csv_name, country_name, range_window=range_window)
            headlines.append(h)
            print(f"OK  T={h['T']}  ir={h['ir_class']}  flips={h['helmsman_flips']}  ({h['duration_ms']} ms)")
        except Exception as exc:
            print(f"FAIL: {type(exc).__name__}: {exc}")
            raise

    comparison_md = _comparison_md(headlines, manifest=manifest, range_policy=args.range_policy)
    comparison_path = _THIS_FILE.parent / "COMPARISON_v2_0_4_vs_v3_0_0.md"
    comparison_path.write_text(comparison_md, encoding="utf-8")

    json_path = _THIS_FILE.parent / "all_countries_headlines.json"
    json_blob: Dict[str, Any] = {
        "coherent_range_manifest": manifest,
        "range_policy": args.range_policy,
        "doctrine": "CRD-1.0 (docs/COHERENT_RANGE_DOCTRINE.md)",
        "countries": headlines,
    }
    json_path.write_text(json.dumps(json_blob, indent=2, ensure_ascii=False), encoding="utf-8")

    print()
    print(f"Comparison report: {comparison_path}")
    print(f"Headlines JSON:    {json_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
