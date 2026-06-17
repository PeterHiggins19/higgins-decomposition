#!/usr/bin/env python3
"""
Hˢ data‑prep — turn any data (zip / folder of zips / folder of CSVs / a CSV / an xlsx) into a
composition matrix the engine can consume, by STREAMING (never fully extracting big zips).

Generalises the Backblaze `huf_preparser.py` trick — stream zipped CSVs row by row and keep only
the tiny aggregated composition — so the same path works for trade zips, energy series, or any
compositional data. Output: an engine‑ready CSV (order column + carrier columns) + a manifest
(source, sha256, config, shape) — then `hs_kinematics_engine.run` / `hs_diagnosis.diagnose`.

TWO SHAPES:
  WIDE  — each row is one order‑point; the carriers are columns already (EMBER, sector weights).
  LONG  — rows are records; aggregate a value by (order, carrier), optionally filtered
          (e.g. trade: filter HS code ^2204, order=year, carrier=importer, value=trade value
          -> the wine export‑destination composition in motion).

CLI:
  python hs_data_prep.py SOURCE --mode long  --order year --carrier importer --value v \
                         --filter k:^2204 --top-k 20 -o wine_dest.csv [--run]
  python hs_data_prep.py SOURCE --mode wide  --order Year [--exclude World] [--run]

Streaming means a 4.5 GB zip is processed with O(orders×carriers) memory (kilobytes), so the
limit is wall‑time, not memory. Author: Peter Higgins (human authorship for claims); AI‑assisted
per HUF‑STD‑001. Honest‑broker.
"""
import argparse, csv, io, json, os, sys, zipfile, hashlib
from collections import defaultdict
from pathlib import Path


def _csv_streams(source):
    """Yield (label, text_stream) for every CSV in: a .zip, a folder of .zip, a folder of .csv,
    or a single .csv — streaming zip entries without extraction."""
    p = Path(source)
    if p.is_dir():
        zips = sorted(p.glob("*.zip")); csvs = sorted(p.glob("*.csv"))
        for z in zips:
            yield from _csv_streams(str(z))
        for c in csvs:
            yield (c.name, open(c, "r", encoding="utf-8", errors="replace"))
    elif p.suffix.lower() == ".zip":
        with zipfile.ZipFile(p) as zf:
            for info in zf.infolist():
                if info.filename.lower().endswith(".csv") and not info.filename.startswith("__MACOSX"):
                    with zf.open(info) as f:
                        yield (info.filename, io.TextIOWrapper(f, encoding="utf-8", errors="replace"))
    elif p.suffix.lower() == ".csv":
        yield (p.name, open(p, "r", encoding="utf-8", errors="replace"))
    elif p.suffix.lower() in (".xlsx", ".xls"):
        yield (p.name, _xlsx_as_csv_stream(p))
    else:
        raise ValueError(f"unsupported source: {source}")


def _xlsx_as_csv_stream(path):
    import openpyxl
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True).worksheets[0]
    buf = io.StringIO(); w = csv.writer(buf)
    for row in ws.iter_rows(values_only=True):
        w.writerow(["" if c is None else c for c in row])
    buf.seek(0); return buf


def _match(val, rule):
    if rule.startswith("^"):
        return str(val).startswith(rule[1:])
    return str(val) == rule


def prepare_long(source, order, carrier, value, filt=None, top_k=None, exclude=()):
    """Stream rows; accumulate comp[order][carrier] += float(value) for rows passing `filt`."""
    comp = defaultdict(lambda: defaultdict(float)); filt = filt or {}
    for _, st in _csv_streams(source):
        rd = csv.DictReader(st)
        for r in rd:
            if any(not _match(r.get(c, ""), rule) for c, rule in filt.items()):
                continue
            o = r.get(order); c = r.get(carrier)
            if o in (None, "") or c in (None, "") or c in exclude:
                continue
            try:
                comp[o][c] += float(r.get(value, 0) or 0)
            except ValueError:
                pass
    return _finish(comp, top_k)


def prepare_wide(source, order=None, exclude=(), top_k=None):
    """Each row = one order‑point; carriers = numeric columns (all except order/labels)."""
    comp = {}; carriers_seen = []
    for _, st in _csv_streams(source):
        rd = csv.reader(st); hdr = next(rd)
        oi = hdr.index(order) if order in hdr else 0
        cols = [(j, h) for j, h in enumerate(hdr) if j != oi and h not in exclude]
        for row in rd:
            if not row or len(row) <= oi:
                continue
            key = row[oi]; d = {}
            for j, h in cols:
                if j < len(row):
                    try:
                        d[h] = float(row[j])
                    except (ValueError, TypeError):
                        pass
            if d:
                comp[key] = d
                for h in d:
                    if h not in carriers_seen:
                        carriers_seen.append(h)
    return _finish(comp, top_k)


def _finish(comp, top_k):
    orders = sorted(comp.keys())
    means = defaultdict(float); cnt = defaultdict(int)
    for o in orders:
        for c, v in comp[o].items():
            means[c] += v; cnt[c] += 1
    carriers = sorted(means, key=lambda c: -means[c] / max(cnt[c], 1))
    if top_k:
        carriers = carriers[:top_k]
    import numpy as np
    M = np.array([[max(comp[o].get(c, 0.0), 0.0) for c in carriers] for o in orders], float)
    keep = M.sum(1) > 0
    return M[keep], carriers, [o for o, k in zip(orders, keep) if k]


def write_ready(M, names, order, source, cfg, out):
    import numpy as np
    with open(out, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["order"] + list(names))
        for o, row in zip(order, M):
            w.writerow([o] + [f"{v:.6g}" for v in row])
    man = {"source": str(source), "config": cfg, "shape": list(M.shape), "carriers": names,
           "order_range": [order[0], order[-1]] if order else [], "engine_ready": True,
           "sha256_of_output": hashlib.sha256(open(out, "rb").read()).hexdigest()}
    json.dump(man, open(out + ".manifest.json", "w"), indent=2)
    return man


def main():
    ap = argparse.ArgumentParser(description="Hˢ data‑prep: any data → engine‑ready composition (streaming).")
    ap.add_argument("source"); ap.add_argument("--mode", choices=["wide", "long"], required=True)
    ap.add_argument("--order"); ap.add_argument("--carrier"); ap.add_argument("--value")
    ap.add_argument("--filter", action="append", default=[], help="col:rule  (rule '^2204' = startswith)")
    ap.add_argument("--exclude", action="append", default=[]); ap.add_argument("--top-k", type=int)
    ap.add_argument("-o", "--out", default="engine_ready.csv"); ap.add_argument("--run", action="store_true")
    a = ap.parse_args()
    filt = dict(s.split(":", 1) for s in a.filter)
    if a.mode == "long":
        M, names, order = prepare_long(a.source, a.order, a.carrier, a.value, filt, a.top_k, set(a.exclude))
        cfg = {"mode": "long", "order": a.order, "carrier": a.carrier, "value": a.value, "filter": filt, "top_k": a.top_k}
    else:
        M, names, order = prepare_wide(a.source, a.order, set(a.exclude), a.top_k)
        cfg = {"mode": "wide", "order": a.order, "top_k": a.top_k}
    man = write_ready(M, names, order, a.source, cfg, a.out)
    print(f"engine‑ready: {a.out}  shape={man['shape']}  carriers={names[:6]}{'…' if len(names)>6 else ''}")
    if a.run:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import hs_kinematics_engine as eng, hs_diagnosis as dx
        print("DIAGNOSIS:", dx.diagnose(M, names)["narrative"])


if __name__ == "__main__":
    main()
