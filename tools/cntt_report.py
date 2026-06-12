#!/usr/bin/env python3
"""CN-TT v4 report — the current general-purpose tool.

Run any composition CSV through the current engine (CN-TT v4, HCI-CNTT) and emit a
human-readable diagnostics + SS-CCC-LLL code report, or full JSON. Carrier-guard
(E-21) aware. This is the modern single-entry replacement for the pre-CN-TT
piecemeal pipeline (archived 2026-06-11). It adds no new science: it composes the
canonical runner (HCI-CNTT/run_cntt.py) and the code system (HCI-CNTT/engine/codes.py).

Usage:
    python tools/cntt_report.py <composition.csv>                 # human report
    python tools/cntt_report.py <composition.csv> --json -o out.json
"""
import sys, json, argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # Hs repo root
CNTT = ROOT / "HCI-CNTT"
sys.path.insert(0, str(CNTT)); sys.path.insert(0, str(CNTT / "engine"))
import run_cntt, codes                                  # canonical runner + code system


def report(csv_path, high_d_threshold=64):
    payload = run_cntt.run(csv_path, high_d_threshold)
    coded = codes.generate_codes(payload)
    return payload, coded


def human(payload, coded):
    inp, at = payload["input"], payload["atlas"]
    L = [f"CN-TT v4 report — {inp.get('source','(csv)')}",
         f"  records {inp['n_records']} x carriers {inp['n_carriers']}"]
    cg = inp.get("carrier_guard")
    if cg:
        L.append(f"  carrier guard (E-21): excluded structural-zero {cg['excluded_structural_zero']}"
                 f" | flagged constant {cg['flagged_constant']}")
    L.append(f"  atlas: lossless={at['lossless']}  reconstruction_max_err={at['reconstruction_max_err']}")
    hf = payload.get("helmsman_family", {})
    if hf:
        L.append(f"  helmsman flips: {hf.get('flips',{}).get('total')}")
    L.append(f"  content hash: {payload['diagnostics']['cntt_content_sha256'][:16]}")
    L.append("  diagnostic codes (SS-CCC-LLL):")
    for c in coded["codes"]:
        L.append(f"    {c['code']:12} [{c['level']}] {c['msg']}")
    if coded["structural_modes"]:
        L.append("  structural modes:")
        for m in coded["structural_modes"]:
            L.append(f"    {m['mode']:12} {m['msg']}")
    L.append(f"  level counts: {coded['level_counts']}")
    return "\n".join(L)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="CN-TT v4 report (current toolchain)")
    ap.add_argument("csv"); ap.add_argument("-o", "--out")
    ap.add_argument("--json", action="store_true", help="emit full JSON (payload + codes)")
    ap.add_argument("--high-d-threshold", type=int, default=64)
    a = ap.parse_args()
    payload, coded = report(a.csv, a.high_d_threshold)
    if a.json:
        blob = {"payload": payload, "codes": coded}
        if a.out:
            json.dump(blob, open(a.out, "w"), indent=2); print("wrote", a.out)
        else:
            print(json.dumps(blob, indent=2))
    else:
        text = human(payload, coded); print(text)
        if a.out:
            open(a.out, "w").write(text + "\n"); print("wrote", a.out)
