#!/usr/bin/env python3
"""
EUV stochastic "valley of death" read as a composition (physics-grounded, deterministic; T2, hash-receipted).

EUV at 13.5 nm => ~91.8 eV per photon. For a fixed dose, the photons hitting a feature are POISSON-distributed
(photon shot noise). The public imec picture is a TWO-SIDED stochastic cliff: too FEW photons -> missing/broken
contacts; too MANY -> bridging/merging. So the per-feature outcome is a composition {OK, missing, bridge}, and a
slow DOSE drift shifts the RATIOS (missing vs bridge) long before the total failure count crosses the yield spec.

Hs reads the silent ratio drift AND points the arrow at WHICH failure mode is rising -- and because the cliff is
two-sided, that arrow is a DIRECTIONAL helmsman: missing -> steer dose UP, bridge -> steer dose DOWN.

Deterministic: shares computed analytically from the Poisson CDF (no sampling noise). Requires scipy.
Author: Peter Higgins; AI-assisted per HUF-STD-001. Internal / planning. No vendor relationship implied.
"""
import hashlib, json
import numpy as np
from scipy.stats import poisson

def clr(p):
    L = np.log(p); return L - L.mean()

def shares(dose, N0, tl, th):
    lam = N0 * dose
    miss = float(poisson.cdf(tl-1, lam)); brg = float(poisson.sf(th, lam))
    p = np.clip(np.array([1-miss-brg, miss, brg]), 1e-15, None)
    return p / p.sum()

def main():
    N0, tl, th = 2000, 1740, 2260            # ~2000 photons/feature nominal; ~+/-5.8 sigma stochastic cliffs
    T = 100
    doses = 1.00 - 0.025 * (np.arange(T)/(T-1))      # slow downward dose drift 1.000 -> 0.975 over the lot
    P = np.array([shares(d, N0, tl, th) for d in doses])     # {OK, missing, bridge}
    total_nok = P[:, 1] + P[:, 2]

    NOK_SPEC = 0.1e-6                          # 0.1 ppm stochastic yield spec
    first_yield_alarm = next((t for t in range(T) if total_nok[t] > NOK_SPEC), None)

    ref = clr(P[:5].mean(0))
    drift = np.array([np.linalg.norm(clr(P[t]) - ref) for t in range(T)])
    band = drift[:5].mean() + 5*drift[:5].std() + 1e-9
    first_hs = next((t for t in range(5, T) if drift[t] > band), None)
    arrow = ["OK", "missing/broken -> steer dose UP", "bridge/merge -> steer dose DOWN"][int(np.argmax(clr(P[-1]) - clr(P[5])))]
    lead = (first_yield_alarm - first_hs) if (first_yield_alarm is not None and first_hs is not None) else None

    out = {
      "case": "EUV stochastic valley-of-death read as a {OK, missing, bridge} composition; dose drift shifts the ratios",
      "physics_anchor": {"wavelength_nm": 13.5, "photon_energy_eV": round(1239.84/13.5, 1),
                         "model": "photons/feature ~ Poisson(dose*N0) [photon shot noise]; analytic two-sided cliff (imec public)"},
      "nominal_photons_per_feature": N0,
      "Hs_silent_drift_flag_wafer": first_hs,
      "single_channel_yield_alarm_wafer": first_yield_alarm,
      "Hs_lead_time_wafers": lead,
      "arrow_points_to": arrow,
      "nominal_total_NOK_ppm": round(float(total_nok[0])*1e6, 4),
      "at_Hs_flag_total_NOK_ppm": (round(float(total_nok[first_hs])*1e6, 4) if first_hs is not None else None),
      "at_yield_alarm_total_NOK_ppm": (round(float(total_nok[first_yield_alarm])*1e6, 4) if first_yield_alarm is not None else None),
      "note": "Deterministic analytic Poisson model. Hs reads WHICH stochastic failure mode is rising (two-sided cliff = directional helmsman) and flags the ratio drift while total NOK is still far under spec. T2 physics-grounded; real validation (T3) on public imec/fab stochastic-defect datasets.",
      "maps_to": "dispense silent-drift (cf9bf72f); coherence/common-mode for drive-laser dose stability (a5ceab9e); dimension-is-the-message (bf24c615)."
    }
    out["content_sha256"] = hashlib.sha256(json.dumps(out, sort_keys=True, default=str).encode()).hexdigest()
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
