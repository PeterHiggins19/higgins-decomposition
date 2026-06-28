#!/usr/bin/env python3
"""
Oracle-parity check for run_cntt changes that touch the hashed path (E-21, guard-code wiring).

The rule: any change to run_cntt must reproduce the SAME cntt_content_sha256 on the
reference corpus, bit-for-bit. The guard attachments are conditional (only attach when a
guard fires), and the guards do NOT fire on the clean reference data — so the hashes MUST
be identical. This script proves it.

USAGE (run where the engine imports cleanly — not the torn sandbox mount):
  # 1) on the CURRENT committed main, record the baseline:
  python HCI-CNTT/verify_hash_parity.py --save baseline_hashes.json
  # 2) apply the wiring edit (see E21_AND_WIRING_TODO.md), then:
  python HCI-CNTT/verify_hash_parity.py --check baseline_hashes.json
  #    -> "ALL MATCH" = parity holds, safe to commit. Any MISMATCH = a guard changed clean
  #       output (a bug) -> the attach is not conditional enough; fix before commit.

Reference corpus: edit REFERENCE_CSVS to your canonical set (Backblaze parity + the CNT
experiment inputs). Author: Peter Higgins; AI-assisted per HUF-STD-001. Honest-broker.
"""
import sys, json, glob, argparse
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent          # Hs/
sys.path.insert(0, str(ROOT / "HCI-CNTT"))
import run_cntt

# The canonical reference set — the clean data the oracle hash is defined on.
REFERENCE_CSVS = sorted(
    glob.glob(str(ROOT / "experiments/backblaze_v4_parity_2026-06/*.csv")) +
    glob.glob(str(ROOT / "HCI-CNT/experiments/codawork2026/ember_*/*generation_TWh.csv")) +
    glob.glob(str(ROOT / "HCI-CNT/experiments/reference/*/*input.csv"))
)


def corpus_hashes():
    h = {}
    for p in REFERENCE_CSVS:
        try:
            payload = run_cntt.run(p)
            h[Path(p).name] = payload["diagnostics"]["cntt_content_sha256"]
        except Exception as e:
            h[Path(p).name] = f"ERROR: {e}"
    return h


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--save"); ap.add_argument("--check")
    a = ap.parse_args()
    cur = corpus_hashes()
    if a.save:
        json.dump(cur, open(a.save, "w"), indent=2)
        print(f"baseline saved: {len(cur)} reference runs -> {a.save}")
        return
    if a.check:
        base = json.load(open(a.check))
        ok = True
        for k, v in cur.items():
            b = base.get(k, "<absent>")
            tag = "MATCH" if v == b else "*** MISMATCH ***"
            if v != b:
                ok = False
            print(f"  [{tag}] {k}: {v[:16]}…")
        print("\nALL MATCH — parity holds; safe to commit." if ok
              else "\nMISMATCH — a guard changed clean output. Make the attach conditional / fix before commit.")
        sys.exit(0 if ok else 1)
    # no flag: just print current
    for k, v in cur.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
