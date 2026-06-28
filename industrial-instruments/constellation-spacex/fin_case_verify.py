"""Deterministic verification of THE_FINANCIAL_CASE.md arithmetic.
Separates CITED PUBLIC BASES from STATED ASSUMPTIONS (fractions), computes each lever's
EV range and the conservative total, and emits a SHA-256 receipt. The data is the shield:
only the cited bases are load-bearing; the fractions are labelled guesses. Author: Peter Higgins;
AI-assisted per HUF-STD-001. Honest-broker; Tier-3 estimate; nothing posted."""
import json, hashlib

# ---- CITED PUBLIC BASES (verifiable; sources in the doc) ----
BASES = {
    "feb2022_sats_lost": 38,                 # Baruah 2024 / CIRES / SWSC 2022
    "persat_usd_low": 0.2e6,                  # V1 (New Space Economy/press)
    "persat_usd_avg": 0.4e6,                  # ~5/day average
    "persat_usd_high": 0.8e6,                 # V2-mini
    "fleet_active": 10400,                    # constellation study / SpaceNews / Wikipedia (mid-2026)
    "starlink_rev_2025_usd": 11.4e9,          # SpaceNews
    "sat_life_years_low": 5, "sat_life_years_high": 7,
}
# ---- STATED ASSUMPTIONS (MINE; NOT public; Tier-3) ----
ASSUME = {
    "L1_prevent_frac": (0.20, 0.50),         # fraction of a partial-loss event prevented
    "L1_events_per_year": (1/3, 1.0),        # one such minor-storm event every 1-3 years
    "L1_persat_today": (0.4e6, 0.8e6),       # today's per-sat cost band for the loss
    "L2_efficiency_frac": (0.003, 0.006),    # 0.3-0.6% on annual replacement
    "L3_maneuver_usd": (1e6, 5e6),           # judgement band (no formula)
    "L6_uptime_frac": 0.001,                 # 0.1% QoS/uptime attributable
    "L6_attributable": (0.20, 0.50),         # fraction of that 0.1% attributable to HUF
}

def rng(lo, hi): return (round(lo/1e6, 2), round(hi/1e6, 2))  # USD millions/yr

# Derived public base: annual fleet replacement value (shown, not asserted)
repl_lo = BASES["fleet_active"]*BASES["persat_usd_avg"]/BASES["sat_life_years_high"]
repl_hi = BASES["fleet_active"]*BASES["persat_usd_high"]/BASES["sat_life_years_low"]

# L1 — storm-loss early warning EV/yr
loss_lo = BASES["feb2022_sats_lost"]*ASSUME["L1_persat_today"][0]
loss_hi = BASES["feb2022_sats_lost"]*ASSUME["L1_persat_today"][1]
L1_lo = ASSUME["L1_prevent_frac"][0]*loss_lo*ASSUME["L1_events_per_year"][0]
L1_hi = ASSUME["L1_prevent_frac"][1]*loss_hi*ASSUME["L1_events_per_year"][1]
# L2 — pre-fault replacement efficiency
L2_lo = ASSUME["L2_efficiency_frac"][0]*repl_lo
L2_hi = ASSUME["L2_efficiency_frac"][1]*repl_hi
# L3 — maneuver/fuel (judgement)
L3_lo, L3_hi = ASSUME["L3_maneuver_usd"]
# L6 — QoS/revenue (fraction of 0.1% of revenue)
L6_full = ASSUME["L6_uptime_frac"]*BASES["starlink_rev_2025_usd"]
L6_lo = ASSUME["L6_attributable"][0]*L6_full
L6_hi = ASSUME["L6_attributable"][1]*L6_full

total_lo = L1_lo+L2_lo+L3_lo+L6_lo
total_hi = L1_hi+L2_hi+L3_hi+L6_hi

res = {
  "single_event_loss_usd_m": [round(loss_lo/1e6,1), round(loss_hi/1e6,1)],
  "derived_annual_replacement_usd_b": [round(repl_lo/1e9,2), round(repl_hi/1e9,2)],
  "levers_usd_m_per_year": {
     "L1_storm_warning": rng(L1_lo, L1_hi),
     "L2_prefault_replacement": rng(L2_lo, L2_hi),
     "L3_maneuver_fuel": rng(L3_lo, L3_hi),
     "L6_qos_revenue": rng(L6_lo, L6_hi),
  },
  "conservative_total_usd_m_per_year": [round(total_lo/1e6,1), round(total_hi/1e6,1)],
  "fraction_of_starlink_revenue": [round(total_lo/BASES["starlink_rev_2025_usd"]*100,3),
                                    round(total_hi/BASES["starlink_rev_2025_usd"]*100,3)],
  "note": "L4 (orbital-datacenter) and L5 (insurance) deliberately EXCLUDED as too speculative.",
}
res["inputs_hash"] = hashlib.sha256(json.dumps({"BASES":BASES,"ASSUME":ASSUME}, sort_keys=True, default=str).encode()).hexdigest()[:16]
res["result_hash"] = hashlib.sha256(json.dumps({k:res[k] for k in res if k!='note'}, sort_keys=True).encode()).hexdigest()[:16]
print(json.dumps(res, indent=2))
