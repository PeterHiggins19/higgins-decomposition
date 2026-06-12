"""
FAO SDMX wide-format -> CNT pipeline-ready CSV adapter.

The FAO indicators in DATA/World Bank Group Data/ (FAO_AS_WIDEF, FAO_IC_23068_WIDEF,
FAO_MK_22010/22016/22077_WIDEF) come in SDMX wide format where:
  - Each row is one (country REF_AREA, indicator) pair
  - Years are spread across columns 1961..2024 (or similar)
  - INDICATOR column identifies the metric

For a compositional reading we pick ONE indicator, treat the top-N countries
(by year-2020 value) as carriers, and pivot so each year becomes a row. The
resulting CSV is [Year, country_1, country_2, ..., country_N] with each row's
country-shares summing to closure (after closure-normalisation). This gives:
"the share of total <indicator> contributed by each top-N country, year by
year" — a meaningful global-redistribution time series.

For files where countries-by-year is sparse, we restrict to years where at
least N//2 of the top-N countries have data, and we use a small-fraction
positivity floor for any missing values (rather than dropping rows).
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_THIS = Path(__file__).resolve()


def _find_data_dir():
    cur = _THIS
    for _ in range(10):
        cand = cur / "DATA" / "World Bank Group Data"
        if cand.is_dir():
            return cand
        if cur.parent == cur:
            break
        cur = cur.parent
    raise FileNotFoundError("Could not locate DATA/World Bank Group Data folder")


WBG = _find_data_dir()
OUT_DIR = _THIS.parent.parent / "raw_inputs"


def adapt_widef(
    src_path: Path,
    indicator_id: str,
    top_n: int,
    out_name: str,
) -> Optional[Dict[str, Any]]:
    """Pivot a single WIDEF file's one indicator into a top-N-country composition."""
    with src_path.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
    if not rows:
        return None
    fieldnames = list(rows[0].keys())
    year_cols = [c for c in fieldnames if c.isdigit() and len(c) == 4]
    if not year_cols:
        return None
    # Filter to the chosen indicator
    matching = [r for r in rows if r.get("INDICATOR") == indicator_id]
    if not matching:
        return {"status": "no_rows_for_indicator", "indicator": indicator_id, "src": str(src_path)}

    # For each country, compute total value across all years; pick top N
    def _to_float(v):
        if v == "" or v is None:
            return None
        try:
            return float(v)
        except ValueError:
            return None

    totals: Dict[str, float] = {}
    country_label: Dict[str, str] = {}
    country_year_val: Dict[Tuple[str, str], float] = {}
    for r in matching:
        ref = r.get("REF_AREA", "").strip()
        label = r.get("REF_AREA_LABEL", "").strip() or ref
        if not ref:
            continue
        country_label[ref] = label
        total = 0.0
        for yc in year_cols:
            v = _to_float(r.get(yc))
            if v is not None and v > 0:
                country_year_val[(ref, yc)] = v
                total += v
        totals[ref] = total

    # Some countries are aggregates (e.g., "WLD", "EUU"). Skip 3-character ISO codes
    # that are not real countries — keep only entries that look like ISO-3 country.
    # Simple heuristic: aggregate codes start with 'X' or contain digits, or are
    # in known aggregate set.
    AGGREGATE_CODES = {"WLD", "EUU", "EMU", "OED", "AFE", "AFW", "ARB", "CEB", "EAP", "EAS",
                       "ECA", "ECS", "FCS", "HIC", "HPC", "IBD", "IBT", "IDA", "IDB", "IDX",
                       "LAC", "LCN", "LDC", "LIC", "LMC", "LMY", "LTE", "MEA", "MIC", "MNA",
                       "NAC", "OSS", "PRE", "PSS", "PST", "SAS", "SSA", "SSF", "TEA", "TEC",
                       "TLA", "TMN", "TSA", "TSS", "UMC", "EAR", "INX", "DTL"}
    real_countries = {k: v for k, v in totals.items() if k not in AGGREGATE_CODES and len(k) == 3 and k.isalpha()}
    if not real_countries:
        return {"status": "no_real_countries", "indicator": indicator_id}

    # Top N by total
    top_countries = sorted(real_countries.items(), key=lambda kv: kv[1], reverse=True)[:top_n]
    top_codes = [c for c, _ in top_countries]
    if not top_codes:
        return {"status": "no_top_countries"}

    # Year filter: keep years where at least half of top-N have positive data
    valid_years: List[str] = []
    for yc in year_cols:
        present = sum(1 for c in top_codes if (c, yc) in country_year_val)
        if present >= max(2, len(top_codes) // 2):
            valid_years.append(yc)
    if len(valid_years) < 5:
        return {"status": "too_few_valid_years", "valid_years": len(valid_years)}

    # Build the matrix
    out_rows: List[List[Any]] = []
    out_rows.append(["Year"] + top_codes)
    for yc in valid_years:
        row_vals = []
        row_total = 0.0
        for c in top_codes:
            v = country_year_val.get((c, yc), 0.0)
            row_vals.append(v)
            row_total += v
        if row_total <= 0:
            continue
        # Replace zeros with small floor to allow closure (no log(0))
        eps = row_total * 1e-6
        row_vals = [max(v, eps) for v in row_vals]
        # Re-normalise after floor  
        row_total = sum(row_vals)
        out_rows.append([yc] + [f"{v / row_total:.8f}" for v in row_vals])

    if len(out_rows) < 6:  # header + at least 5 data rows
        return {"status": "too_few_data_rows", "n": len(out_rows) - 1}

    out_path = OUT_DIR / out_name
    with out_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        for r in out_rows:
            writer.writerow(r)

    return {
        "status": "ok",
        "indicator": indicator_id,
        "out_path": str(out_path.relative_to(_THIS.parents[2])),
        "T": len(out_rows) - 1,
        "D": len(top_codes),
        "top_codes": top_codes,
        "top_country_labels": [country_label.get(c, c) for c in top_codes],
        "year_min": valid_years[0],
        "year_max": valid_years[-1],
    }


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    targets = [
        # (src, indicator_id, top_N, out_name, label)
        (WBG / "FAO_IC_23068_WIDEF.csv", "FAO_IC_23068", 10, "fao_credit_to_agriculture.csv", "Credit to Agriculture"),
        (WBG / "FAO_MK_22010_WIDEF.csv", "FAO_MK_22010", 10, "fao_value_added_agriculture.csv", "Value Added (Agriculture)"),
        (WBG / "FAO_MK_22016_WIDEF.csv", "FAO_MK_22016", 10, "fao_value_added_aff.csv", "Value Added (Agriculture, Forestry and Fishing)"),
        (WBG / "FAO_MK_22077_WIDEF.csv", "FAO_MK_22077", 10, "fao_value_added_food_mfg.csv", "Value Added (Manufacture of food and beverages)"),
    ]

    results = []
    for src, ind, n, out_name, label in targets:
        if not src.is_file():
            print(f"SKIP {ind}: src missing ({src})")
            continue
        r = adapt_widef(src, ind, n, out_name)
        if r is None:
            print(f"FAIL {ind}: empty source")
            continue
        if r.get("status") != "ok":
            print(f"FAIL {ind}: {r.get('status')} {r}")
            continue
        print(f"OK   {ind:18s} -> {out_name:40s}  T={r['T']:3d}  D={r['D']}  ({r['year_min']}-{r['year_max']})")
        print(f"     top countries: {', '.join(r['top_country_labels'])}")
        r["label"] = label
        results.append(r)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
