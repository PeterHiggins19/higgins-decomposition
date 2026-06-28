#!/usr/bin/env python3
"""
Illustrative VALUE ENVELOPE (Tier 3) for Hs-as-a-thin-analytical-layer if actually applied.
Method mirrors the constellation finance case: PUBLIC base x an EXPLICIT assumed small fraction = a range.
Every fraction is an ASSUMPTION (not measured); the crux (the yield/excursion fraction) can only be set by a
real pilot. NOT financial advice; modest by design. Author: Peter Higgins; AI-assisted per HUF-STD-001.
"""
import hashlib, json

YIELD_MGMT_MKT_2025_B    = 2.12     # semiconductor yield-management market, $B (2025)
ADV_PACKAGING_MKT_2025_B = 40.0     # advanced packaging market ~$33.5-45B (2025) -> ~40
OSAT_MKT_2025_B          = 52.6     # OSAT services market, $B (2025)
NA_PACKAGING_SHARE       = 0.228    # North America share of advanced packaging (2025)
CANADA_PKG_TEST_BASE_B   = 2.0      # ASSUMED Canadian packaging/test throughput touchpoint, $B/yr (T3)

def rng(base_B, lo, hi):
    return (base_B*1e3*lo, base_B*1e3*hi)   # -> $M/yr

scopes = {}
A_per_line_M = (0.5, 3.0)                                            # $M/yr per advanced line (ASSUMED)
scopes["A_single_line_pilot"] = A_per_line_M
scopes["B_canada_ecosystem"]  = rng(CANADA_PKG_TEST_BASE_B, 0.001, 0.005)
scopes["C_global_standard_upside_FLAGGED_NOT_SUMMED"] = rng(YIELD_MGMT_MKT_2025_B, 0.01, 0.04)

near_lo = A_per_line_M[0] + scopes["B_canada_ecosystem"][0]
near_hi = 3*A_per_line_M[1] + scopes["B_canada_ecosystem"][1]

out = {
  "framing": "Hs is a THIN analytical layer; value = public base x an EXPLICIT assumed small fraction. Modest by design. ALL Tier 3 (assumptions, not measured). NOT financial advice.",
  "public_anchors": {"yield_management_market_2025_$B": YIELD_MGMT_MKT_2025_B,
                     "advanced_packaging_market_2025_$B": ADV_PACKAGING_MKT_2025_B,
                     "OSAT_market_2025_$B": OSAT_MKT_2025_B, "north_america_packaging_share": NA_PACKAGING_SHARE,
                     "one_yield_point": "~ millions/yr per fab (public); small process variation swings yield 1-3%"},
  "scopes_$M_per_yr": {k: [round(v[0],2), round(v[1],2)] for k,v in scopes.items()},
  "realistic_near_term_envelope_$M_per_yr": [round(near_lo,1), round(near_hi,1)],
  "the_crux": "Every fraction is an ASSUMPTION. The yield/excursion fraction (does the ratio-read actually recover yield, and how much) is UNMEASURED -- only a real pilot sets it; it could be larger, smaller, or zero.",
  "strategic_value_note": "The larger value to Canada is likely NON-DOLLAR: a sovereignty/learning-rate asset + an auditable monitoring standard in a contested domain (a head start). The published science benefits the world (not an appropriable Canadian $).",
  "not_financial_advice": True
}
out["content_sha256"] = hashlib.sha256(json.dumps(out, sort_keys=True, default=str).encode()).hexdigest()
print(json.dumps(out, indent=2))
