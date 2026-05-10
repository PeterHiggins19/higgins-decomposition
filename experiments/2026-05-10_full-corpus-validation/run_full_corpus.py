"""
Full-corpus validation runner — CNT v3.0.0 + CNQ v2.0.0 + CRD-1.0.

Processes every dataset registered in MANIFEST.json through both engines,
producing per-dataset Stage 1 + Advanced reports plus per-domain summaries
and a master findings report.

These runs are the citation-grade reference suite for the latest engines.
No simulated data; every input CSV is a real-world dataset with documented
source.

Usage:
    python experiments/2026-05-10_full-corpus-validation/run_full_corpus.py
"""
from __future__ import annotations

import json
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional

_THIS_FILE = Path(__file__).resolve()
_REPO_ROOT = _THIS_FILE.parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))
sys.path.insert(0, str(_REPO_ROOT / "HCI-CNT" / "engine"))
sys.path.insert(0, str(_REPO_ROOT / "HCI-CNQ" / "engine"))
sys.path.insert(0, str(_THIS_FILE.parent))

import cnt as cnt_v3       # type: ignore
import cnq as cnq_v2       # type: ignore
from report_lib import stage1_report, advanced_report  # type: ignore

OUTPUT_DIR = _THIS_FILE.parent / "per_domain"
MANIFEST_PATH = _THIS_FILE.parent / "MANIFEST.json"


def _process_dataset(d: Dict[str, Any]) -> Dict[str, Any]:
    """Run both engines on a dataset; write artefacts; return headline dict."""
    csv_path = _REPO_ROOT / d["input_csv"]
    if not csv_path.exists():
        return {
            "id": d["id"],
            "domain": d["domain"],
            "status": "MISSING_INPUT",
            "input_csv": str(csv_path),
            "error": f"Pipeline-ready CSV not found at {csv_path}",
        }

    domain_dir = OUTPUT_DIR / d["domain"]
    out_dir = domain_dir / d["id"]
    out_dir.mkdir(parents=True, exist_ok=True)

    cnt_json_path = out_dir / "cnt_v3.json"
    cnq_json_path = out_dir / "cnq_v2.json"

    t0 = time.monotonic()
    try:
        cnt_payload = cnt_v3.cnt_run(csv_path, out_path=cnt_json_path)
    except Exception as exc:
        return {
            "id": d["id"], "domain": d["domain"], "status": "CNT_FAILED",
            "input_csv": str(csv_path),
            "error": f"{type(exc).__name__}: {exc}",
        }
    try:
        cnq_payload = cnq_v2.cnq_run(input_csv=csv_path, out_path=cnq_json_path)
    except Exception as exc:
        return {
            "id": d["id"], "domain": d["domain"], "status": "CNQ_FAILED",
            "input_csv": str(csv_path),
            "error": f"{type(exc).__name__}: {exc}",
        }
    duration_ms = int((time.monotonic() - t0) * 1000)

    s1_md = stage1_report(d["id"], d["domain"], d["description"], d["citation"], cnt_payload)
    (out_dir / "STAGE_1_REPORT.md").write_text(s1_md, encoding="utf-8")

    adv_md = advanced_report(
        d["id"], d["domain"], d["description"], d["citation"], cnt_payload, cnq_payload
    )
    (out_dir / "ADVANCED_ANALYSIS.md").write_text(adv_md, encoding="utf-8")

    headline = {
        "id": d["id"],
        "domain": d["domain"],
        "description": d["description"],
        "citation": d["citation"],
        "status": "OK",
        "T": cnt_payload["input"]["n_records"],
        "D": cnt_payload["input"]["n_carriers"],
        "termination": cnt_payload["depth_tower"]["termination"]["kind"],
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
        "cnq_D": cnq_payload["cnq_view"]["dimension_policy"]["D"],
        "cnt_content_sha256": cnt_payload["diagnostics"]["cnt_content_sha256"],
        "cnq_content_sha256": cnq_payload["diagnostics"]["cnq_content_sha256"],
        "duration_ms": duration_ms,
        "report_paths": {
            "stage1": str((out_dir / "STAGE_1_REPORT.md").relative_to(_REPO_ROOT)),
            "advanced": str((out_dir / "ADVANCED_ANALYSIS.md").relative_to(_REPO_ROOT)),
            "cnt_json": str(cnt_json_path.relative_to(_REPO_ROOT)),
            "cnq_json": str(cnq_json_path.relative_to(_REPO_ROOT)),
        },
    }
    return headline


def _domain_summary_md(domain: str, headlines: List[Dict[str, Any]]) -> str:
    """Build a per-domain DOMAIN_SUMMARY.md aggregating that domain's datasets."""
    lines: List[str] = []
    lines.append(f"# Domain summary — {domain}")
    lines.append("")
    lines.append(f"**Datasets in this domain:** {len(headlines)}")
    lines.append("")
    lines.append("## Headline diagnostics")
    lines.append("")
    lines.append("| Dataset | Status | T | D | Termination | IR class | M²=I residual | A | ζ | flips | stability |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for h in headlines:
        if h["status"] != "OK":
            lines.append(f"| {h['id']} | **{h['status']}** | — | — | — | — | — | — | — | — | — |")
            continue
        lines.append(
            f"| {h['id']} "
            f"| OK "
            f"| {h['T']} "
            f"| {h['D']} "
            f"| `{h['termination']}` "
            f"| `{h['ir_class']}` "
            f"| {h['M2_residual_max']:.2e} "
            f"| {h['amplitude_A']:.3f} "
            f"| {h['damping_zeta']:+.3f} "
            f"| {h['helmsman_flips']} "
            f"| {h['helmsman_stability']:.3f} |"
        )
    lines.append("")
    lines.append("## Per-dataset detail")
    lines.append("")
    for h in headlines:
        if h["status"] != "OK":
            lines.append(f"- **{h['id']}** — {h['status']}: {h.get('error', '')}")
            continue
        rel_s1 = Path(h["report_paths"]["stage1"]).relative_to(Path("experiments") / _THIS_FILE.parent.name)
        rel_adv = Path(h["report_paths"]["advanced"]).relative_to(Path("experiments") / _THIS_FILE.parent.name)
        lines.append(f"- **{h['id']}** — {h['description']}")
        lines.append(f"  - [Stage 1 report]({rel_s1})  ·  [Advanced analysis]({rel_adv})")
    lines.append("")
    return "\n".join(lines)


def _master_findings_md(headlines: List[Dict[str, Any]], manifest_meta: Dict[str, Any]) -> str:
    """Cross-domain master findings report."""
    lines: List[str] = []
    lines.append("# Full-corpus validation — Master findings (2026-05-10)")
    lines.append("")
    lines.append(f"**Engines:** CNT v{manifest_meta['engines']['cnt']} + CNQ v{manifest_meta['engines']['cnq']}")
    lines.append(f"**Doctrines:** {', '.join(manifest_meta['doctrines'])}")
    lines.append(f"**Run date:** 2026-05-10")
    lines.append(f"**Datasets attempted:** {len(headlines)}")
    n_ok = sum(1 for h in headlines if h["status"] == "OK")
    lines.append(f"**Datasets that ran end-to-end:** {n_ok}")
    lines.append(f"**Datasets that failed or had missing inputs:** {len(headlines) - n_ok}")
    lines.append("")
    lines.append("This is the citation-grade reference suite for the latest CNT v3 + CNQ v2 engines applied across the entire DATA folder. **No simulated data** — every input CSV was a real-world dataset with a documented source. These runs are the canonical worked examples of compositional analysis using the Hs framework as of push #33.")
    lines.append("")

    # Cross-domain headline grid
    lines.append("## Cross-domain headline grid")
    lines.append("")
    lines.append("| Domain | Dataset | T | D | IR class | flips | stability | A | ζ | M²=I |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for h in sorted(headlines, key=lambda x: (x["domain"], x["id"])):
        if h["status"] != "OK":
            lines.append(f"| {h['domain']} | {h['id']} | (status: {h['status']}) | | | | | | | |")
            continue
        lines.append(
            f"| {h['domain']} | {h['id']} | {h['T']} | {h['D']} "
            f"| `{h['ir_class']}` | {h['helmsman_flips']} "
            f"| {h['helmsman_stability']:.3f} | {h['amplitude_A']:.3f} "
            f"| {h['damping_zeta']:+.3f} | {h['M2_residual_max']:.1e} |"
        )
    lines.append("")

    # Numerical anchors
    n_verified = sum(1 for h in headlines if h["status"] == "OK" and h["M2_verified"])
    worst_M2 = max((h["M2_residual_max"] for h in headlines if h["status"] == "OK"), default=0.0)
    lines.append("## Determinism + numerical anchors")
    lines.append("")
    lines.append(f"- **M² = I metric involution verified at IEEE floor (< 10⁻¹⁰) on {n_verified} of {n_ok} successful runs.** Worst residual across the corpus: **{worst_M2:.3e}**.")
    lines.append(f"- **Engine independence (push #32):** Each dataset produces two unrelated SHA-256 fingerprints — `cnt_content_sha256` and `cnq_content_sha256`. The fingerprints are independent by design; their non-identity is a feature, not a discrepancy.")
    lines.append("- **CRD-1.0:** This master report compares heterogeneous datasets across domains (different T, different D, different units). CRD-1.0 governs *intra-domain* multi-carrier comparisons (e.g., the 8-country EMBER corpus is run under CRD-1.0 coherent policy in `papers/codawork2026/conference_2026_06/`). Cross-domain comparisons are inherently heterogeneous and shown as-is.")
    lines.append("")

    # IR class distribution
    ir_classes = defaultdict(list)
    for h in headlines:
        if h["status"] == "OK":
            ir_classes[h["ir_class"]].append(h["id"])
    lines.append("## IR class distribution across the corpus")
    lines.append("")
    lines.append("| IR class | count | datasets |")
    lines.append("|---|---|---|")
    for ir_class in sorted(ir_classes.keys()):
        ds = ir_classes[ir_class]
        ds_s = ", ".join(ds[:5]) + (f" + {len(ds) - 5} more" if len(ds) > 5 else "")
        lines.append(f"| `{ir_class}` | {len(ds)} | {ds_s} |")
    lines.append("")
    lines.append("The IR class taxonomy describes the damping signature of each compositional trajectory — from `OVERDAMPED_EXTREME` (snap-to-attractor) through `LIGHTLY_DAMPED` to `LIMIT_CYCLE_P2` (the universal compositional invariance signature). Domain-domain comparisons in this column are scientifically meaningful: they reveal which compositional systems are dynamically locked, which are cycling, and which are diffusive.")
    lines.append("")

    # Per-domain table of contents
    lines.append("## Per-domain reports")
    lines.append("")
    by_domain = defaultdict(list)
    for h in headlines:
        by_domain[h["domain"]].append(h)
    for domain in sorted(by_domain.keys()):
        ds = by_domain[domain]
        lines.append(f"- **`{domain}`** ({len(ds)} datasets) — see [`per_domain/{domain}/DOMAIN_SUMMARY.md`](per_domain/{domain}/DOMAIN_SUMMARY.md)")
    lines.append("")

    # Anomalies and findings
    lines.append("## Anomalies and findings of interest")
    lines.append("")
    findings: List[str] = []
    for h in headlines:
        if h["status"] != "OK":
            findings.append(f"- **{h['id']}** failed: `{h['status']}` — {h.get('error', '(no detail)')}")
            continue
        if h["M2_residual_max"] > 1e-10:
            findings.append(f"- **{h['id']}** has unusually large M²=I residual ({h['M2_residual_max']:.3e}); investigate trajectory conditioning.")
        if h["attractor_fitted"] and h["attractor_stability"] > 0.9:
            findings.append(f"- **{h['id']}** has a strongly-locked period-{h['attractor_period']} attractor (stability {h['attractor_stability']:.3f}, A {h['amplitude_A']:.3f}); cycle-locked compositional dynamics.")
        if h["helmsman_stability"] > 0.95:
            findings.append(f"- **{h['id']}** has near-perfect helmsman stability ({h['helmsman_stability']:.3f}) — monotone or near-monotone compositional trajectory.")
        if h["helmsman_flips"] > h["T"] * 0.7:
            findings.append(f"- **{h['id']}** has unusually high flip density ({h['helmsman_flips']} flips in T={h['T']}) — chaotic or noisy dominant-axis structure.")
    if findings:
        lines.extend(findings)
    else:
        lines.append("(no anomalies surfaced by the standard heuristics)")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*Generated by `experiments/2026-05-10_full-corpus-validation/run_full_corpus.py`.*")
    return "\n".join(lines)


def main() -> int:
    print("=== Full-corpus validation — CNT v3.0.0 + CNQ v2.0.0 ===")
    print(f"Manifest: {MANIFEST_PATH}")
    print(f"Output:   {OUTPUT_DIR}")
    print()

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    datasets = manifest["datasets"]

    headlines: List[Dict[str, Any]] = []
    for d in datasets:
        print(f"  [{d['domain']}/{d['id']}] ... ", end="", flush=True)
        try:
            h = _process_dataset(d)
            headlines.append(h)
            if h["status"] == "OK":
                print(f"OK  T={h['T']}  D={h['D']}  ir={h['ir_class']}  ({h['duration_ms']} ms)")
            else:
                print(f"{h['status']}: {h.get('error', '')}")
        except Exception as exc:
            print(f"UNEXPECTED FAIL: {type(exc).__name__}: {exc}")
            headlines.append({
                "id": d["id"], "domain": d["domain"], "status": "UNEXPECTED_FAIL",
                "error": f"{type(exc).__name__}: {exc}",
            })

    # Per-domain summaries
    by_domain = defaultdict(list)
    for h in headlines:
        by_domain[h["domain"]].append(h)
    for domain, ds_list in by_domain.items():
        domain_dir = OUTPUT_DIR / domain
        domain_dir.mkdir(parents=True, exist_ok=True)
        (domain_dir / "DOMAIN_SUMMARY.md").write_text(
            _domain_summary_md(domain, ds_list), encoding="utf-8"
        )

    # Master findings
    master_md = _master_findings_md(headlines, manifest["_meta"])
    (_THIS_FILE.parent / "MASTER_FINDINGS.md").write_text(master_md, encoding="utf-8")

    # Combined headlines JSON
    json_blob = {
        "_meta": manifest["_meta"],
        "run_date": "2026-05-10",
        "headlines": headlines,
    }
    (_THIS_FILE.parent / "all_headlines.json").write_text(
        json.dumps(json_blob, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    n_ok = sum(1 for h in headlines if h["status"] == "OK")
    print()
    print(f"=== Summary ===")
    print(f"  Datasets attempted: {len(headlines)}")
    print(f"  Datasets OK:        {n_ok}")
    print(f"  Datasets failed:    {len(headlines) - n_ok}")
    print(f"  Master report:      {(_THIS_FILE.parent / 'MASTER_FINDINGS.md')}")
    return 0 if n_ok == len(headlines) else 1


if __name__ == "__main__":
    sys.exit(main())
