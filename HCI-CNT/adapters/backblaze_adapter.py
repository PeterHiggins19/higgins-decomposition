#!/usr/bin/env python3
"""
BackBlaze adapter — resumable. Streams quarterly zip files into a daily
fleet-mean composition CSV with the canonical Hs-17 carrier definition.

SMART -> carrier mapping (Hs-17 preparser v1.0):
    Mechanical = SMART 5  (Reallocated)
               + SMART 197 (Pending) * 10
               + SMART 198 (Offline Uncorrectable) * 10
    Thermal    = SMART 194 (Temperature, Celsius)
    Age        = SMART 9   (Power-On Hours) / 1000
    Errors     = SMART 1   (Read Error)  / 1e6
               + SMART 7   (Seek Error)  / 1e6
               + SMART 199 (UDMA CRC)

Aggregation: fleet MEAN per carrier per day across drives reporting that day.

Resumable: state saved to checkpoint.json after each daily CSV. Re-run
until done. Use --reset to start over.

Final output: backblaze_fleet_input.csv (Date, Mechanical, Thermal, Age, Errors)
"""
from __future__ import annotations
import sys, os, json, csv, zipfile, time, argparse
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[5]
ZIP_DIR = ROOT / "DATA" / "BackBlaze"
EXP_DIR = Path(__file__).resolve().parent.parent / "codawork2026" / "backblaze_fleet"
CHECKPOINT = EXP_DIR / "checkpoint.json"
OUT_CSV    = EXP_DIR / "backblaze_fleet_input.csv"

NEEDED = ["date","smart_1_raw","smart_5_raw","smart_7_raw","smart_9_raw",
          "smart_194_raw","smart_197_raw","smart_198_raw","smart_199_raw"]


def list_all_csvs() -> list[tuple[str, str]]:
    """List (zip_path, member_name) pairs for every daily CSV across all zips."""
    out = []
    for zp in sorted(ZIP_DIR.glob("data_Q*_*.zip")):
        with zipfile.ZipFile(zp) as z:
            for m in sorted(z.namelist()):
                if m.endswith(".csv") and "__MACOSX" not in m:
                    out.append((str(zp), m))
    return out


def process_one_csv(zp: str, member: str) -> tuple[str, float, float, float, float, int]:
    """Read one CSV from a zip, return (date, mech_sum, therm_sum, age_sum, errs_sum, n)."""
    with zipfile.ZipFile(zp) as z:
        with z.open(member) as f:
            df = pd.read_csv(f, usecols=NEEDED)
    s1   = df["smart_1_raw"].fillna(0)
    s5   = df["smart_5_raw"].fillna(0)
    s7   = df["smart_7_raw"].fillna(0)
    s9   = df["smart_9_raw"].fillna(0)
    s194 = df["smart_194_raw"].fillna(0)
    s197 = df["smart_197_raw"].fillna(0)
    s198 = df["smart_198_raw"].fillna(0)
    s199 = df["smart_199_raw"].fillna(0)

    mech  = s5 + 10.0 * s197 + 10.0 * s198
    therm = s194
    age   = s9 / 1000.0
    errs  = s1 / 1e6 + s7 / 1e6 + s199

    # drop drives reporting all zeros (sensor not populated for that drive)
    populated = (mech + therm + age + errs) > 0
    mech, therm, age, errs = mech[populated], therm[populated], age[populated], errs[populated]
    n = len(mech)

    date = df["date"].iloc[0] if len(df) else "unknown"
    return (date,
            float(mech.sum()),  float(therm.sum()),
            float(age.sum()),   float(errs.sum()), n)


def load_checkpoint() -> dict:
    if CHECKPOINT.exists():
        with CHECKPOINT.open() as f: return json.load(f)
    return {"processed": [], "day_accum": {}}


def save_checkpoint(state: dict):
    EXP_DIR.mkdir(parents=True, exist_ok=True)
    tmp = CHECKPOINT.with_suffix(".tmp")
    with tmp.open("w") as f: json.dump(state, f)
    tmp.replace(CHECKPOINT)


def write_final_csv(state: dict):
    rows = []
    for date in sorted(state["day_accum"].keys()):
        m_s, t_s, a_s, e_s, n = state["day_accum"][date]
        if n == 0: continue
        rows.append([date, m_s/n, t_s/n, a_s/n, e_s/n])
    EPS = 1e-9
    for r in rows:
        for k in (1, 2, 3, 4):
            if r[k] <= 0: r[k] = EPS
    with OUT_CSV.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Date", "Mechanical", "Thermal", "Age", "Errors"])
        for r in rows:
            w.writerow([r[0]] + [f"{v:.6g}" for v in r[1:]])
    return len(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-time", type=float, default=40.0,
                    help="Max wall-time in seconds before checkpointing and exiting (default 40).")
    ap.add_argument("--reset", action="store_true", help="Start over.")
    ap.add_argument("--write-csv", action="store_true", help="Just emit final CSV from checkpoint and exit.")
    args = ap.parse_args()

    if args.reset and CHECKPOINT.exists():
        CHECKPOINT.unlink()

    state = load_checkpoint()
    processed = set(state["processed"])

    if args.write_csv:
        n = write_final_csv(state)
        print(f"Wrote {n} rows to {OUT_CSV}")
        return

    all_csvs = list_all_csvs()
    remaining = [c for c in all_csvs if f"{c[0]}::{c[1]}" not in processed]
    print(f"BackBlaze adapter (resumable)")
    print(f"  Total daily CSVs: {len(all_csvs)}")
    print(f"  Already processed: {len(processed)}")
    print(f"  Remaining: {len(remaining)}")

    if not remaining:
        n = write_final_csv(state)
        print(f"All done. Wrote {n} rows to {OUT_CSV}")
        return

    t0 = time.time()
    n_processed = 0
    for zp, member in remaining:
        if time.time() - t0 > args.max_time:
            print(f"  Hitting max-time limit at {time.time()-t0:.0f}s, checkpointing...")
            break
        try:
            date, m_s, t_s, a_s, e_s, n = process_one_csv(zp, member)
        except Exception as e:
            print(f"  WARN: failed on {member}: {e}")
            processed.add(f"{zp}::{member}")
            continue
        slot = state["day_accum"].setdefault(date, [0.0, 0.0, 0.0, 0.0, 0])
        slot[0] += m_s; slot[1] += t_s; slot[2] += a_s; slot[3] += e_s; slot[4] += n
        processed.add(f"{zp}::{member}")
        n_processed += 1
        if n_processed % 20 == 0:
            print(f"  {n_processed}/{len(remaining)} this batch, "
                  f"{len(processed)}/{len(all_csvs)} total complete, "
                  f"latest date: {date} ({n} drives)")
            state["processed"] = list(processed)
            save_checkpoint(state)

    state["processed"] = list(processed)
    save_checkpoint(state)
    print(f"Batch done: {n_processed} CSVs in {time.time()-t0:.0f}s "
          f"({len(processed)}/{len(all_csvs)} total complete)")
    if len(processed) >= len(all_csvs):
        n_rows = write_final_csv(state)
        print(f"All done. Wrote {n_rows} rows to {OUT_CSV}")


if __name__ == "__main__":
    main()
