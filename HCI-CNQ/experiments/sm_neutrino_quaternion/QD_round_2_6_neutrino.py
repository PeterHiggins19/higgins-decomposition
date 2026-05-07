#!/usr/bin/env python3
"""QD Round 2.6 - neutrino oscillation invariance test.

Computes the Standard Model 3-flavor numu oscillation probabilities
P(numu -> nue, numu -> numu, numu -> nutau) from published PMNS matrix
parameters as a function of distance L (km), at fixed energy E (MeV).
Hands the result to the canonical CNT engine. Asks whether the SM
prediction carries the universal compositional invariance signature.
"""
import csv
import json
import math
import subprocess
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
NU_DIR = HERE
NU_DIR.mkdir(exist_ok=True)
INPUT_CSV = NU_DIR / "sm_numu_oscillation_input.csv"
ENGINE_OUT = NU_DIR / "sm_numu_oscillation_cnt.json"
RESULTS = NU_DIR / "QD_round_2_6_results.json"

HS_ENGINE = Path("/sessions/epic-gracious-lovelace/mnt/Claude CoWorker/"
                 "Current-Repo/Hs/HCI-CNT/engine/cnt.py")

# PMNS parameters (PDG 2024 / NuFit 5.2 normal ordering)
THETA_12 = math.asin(math.sqrt(0.307))
THETA_13 = math.asin(math.sqrt(0.0218))
THETA_23 = math.asin(math.sqrt(0.546))
DELTA_CP = -math.pi / 2
DM21_SQ = 7.53e-5
DM31_SQ = 2.453e-3
ENERGY_MEV = 600.0
L_MIN_KM = 1.0
L_MAX_KM = 4000.0
N_POINTS = 1000


def pmns_matrix():
    s12, c12 = math.sin(THETA_12), math.cos(THETA_12)
    s13, c13 = math.sin(THETA_13), math.cos(THETA_13)
    s23, c23 = math.sin(THETA_23), math.cos(THETA_23)
    eid = complex(math.cos(DELTA_CP), math.sin(DELTA_CP))
    U = np.array([
        [c12*c13, s12*c13, s13*eid.conjugate()],
        [-s12*c23 - c12*s23*s13*eid, c12*c23 - s12*s23*s13*eid, s23*c13],
        [s12*s23 - c12*c23*s13*eid, -c12*s23 - s12*c23*s13*eid, c23*c13]
    ], dtype=complex)
    return U


def osc_prob(U, alpha, beta, L_km, E_MeV, masses_sq):
    """Standard 3-flavor vacuum oscillation probability.
    Uses the textbook formula with phase = 1.267 * Dm2(eV2) * L(km) / E(GeV)."""
    delta_ab = 1.0 if alpha == beta else 0.0
    E_GeV = E_MeV / 1000.0
    P = delta_ab
    for i in range(3):
        for j in range(i):
            uai_ubi = U[alpha, i].conjugate() * U[beta, i]
            uaj_ubj_conj = U[alpha, j] * U[beta, j].conjugate()
            term = uai_ubi * uaj_ubj_conj
            phase = 1.267 * (masses_sq[i] - masses_sq[j]) * L_km / E_GeV
            P -= 4 * term.real * math.sin(phase) ** 2
            P += 2 * term.imag * math.sin(2 * phase)
    return P


def step_1_compute():
    print("  PMNS parameters:")
    print(f"    theta_12 = {math.degrees(THETA_12):.2f} deg")
    print(f"    theta_13 = {math.degrees(THETA_13):.2f} deg")
    print(f"    theta_23 = {math.degrees(THETA_23):.2f} deg")
    print(f"    delta_CP = {math.degrees(DELTA_CP):.1f} deg ({DELTA_CP/math.pi:+.3f} pi)")
    print(f"    Dm2_21 = {DM21_SQ:.2e} eV2")
    print(f"    Dm2_31 = {DM31_SQ:.2e} eV2")
    print(f"    E = {ENERGY_MEV} MeV (T2K-like)")
    print(f"    L range: {L_MIN_KM} -> {L_MAX_KM} km, {N_POINTS} points")
    print()

    U = pmns_matrix()
    masses_sq = np.array([0.0, DM21_SQ, DM31_SQ])
    distances = np.linspace(L_MIN_KM, L_MAX_KM, N_POINTS)

    rows = []
    for L in distances:
        P_e = osc_prob(U, 1, 0, L, ENERGY_MEV, masses_sq)
        P_mu = osc_prob(U, 1, 1, L, ENERGY_MEV, masses_sq)
        P_tau = osc_prob(U, 1, 2, L, ENERGY_MEV, masses_sq)
        floor = 1e-12
        P_e = max(P_e, floor); P_mu = max(P_mu, floor); P_tau = max(P_tau, floor)
        s = P_e + P_mu + P_tau
        rows.append((L, P_e/s, P_mu/s, P_tau/s))

    arr = np.array([r[1:] for r in rows])
    print(f"  P(numu->nue)  range: [{arr[:, 0].min():.4f}, {arr[:, 0].max():.4f}]")
    print(f"  P(numu->numu) range: [{arr[:, 1].min():.4f}, {arr[:, 1].max():.4f}]")
    print(f"  P(numu->nutau)range: [{arr[:, 2].min():.4f}, {arr[:, 2].max():.4f}]")
    print(f"  Mean disappearance: 1 - <P(numu->numu)> = {1 - arr[:, 1].mean():.4f}")

    with INPUT_CSV.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["L_km", "P_nue", "P_numu", "P_nutau"])
        for L, p_e, p_mu, p_tau in rows:
            w.writerow([f"L{L:07.2f}", f"{p_e:.10e}", f"{p_mu:.10e}", f"{p_tau:.10e}"])
    print(f"  Wrote {len(rows)} rows to {INPUT_CSV.name}")
    return len(rows)


def step_2_run_engine():
    # overwrite if exists
    cmd = ["python3", str(HS_ENGINE), str(INPUT_CSV),
           "-o", str(ENGINE_OUT), "--ordering-method", "by-time"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        print(f"  Engine FAILED: {r.stderr[-500:]}")
        return None
    for line in r.stdout.splitlines()[-12:]:
        print(f"    {line}")
    return ENGINE_OUT


def step_3_report():
    j = json.load(open(ENGINE_OUT))
    inp = j["input"]; diag = j["diagnostics"]
    sm = j["depth"]["higgins_extensions"]["summary"]
    ir = j["depth"]["higgins_extensions"]["impulse_response"]
    print()
    print("  ENGINE OUTPUT:")
    print(f"    engine_version:        {j['metadata']['engine_version']}")
    print(f"    schema_version:        {j['metadata']['schema_version']}")
    print(f"    T:                     {inp.get('n_records', '?')}")
    print(f"    D:                     {inp.get('n_carriers', '?')}")
    print(f"    source_sha256:         {inp['source_file_sha256']}")
    print(f"    content_sha256:        {diag['content_sha256']}")
    print()
    print("  CNT DYNAMICS:")
    print(f"    IR class:              {ir['classification']}")
    print(f"    amplitude A:           {ir['amplitude_A']:.6f}")
    print(f"    damping zeta:          {ir['damping_zeta']:.6f}")
    print(f"    curvature_depth:       {sm['curvature_depth']}")
    print(f"    energy_depth:          {sm['energy_depth']}")
    print(f"    curvature_termination: {sm['curvature_termination']}")
    print(f"    energy_termination:    {sm['energy_termination']}")
    print()
    print("  CENTRAL-CLAIM VERDICT:")
    term = sm["curvature_termination"]
    if "LIMIT_CYCLE_P2" in term:
        verdict = "CONSISTENT - universal compositional invariance signature CONFIRMED"
        msg = ("    PASS - The Standard Model 3-flavor neutrino oscillation prediction\n"
               "    carries the same invariance fingerprint as drive failures, energy\n"
               "    mixes, geochemistry, and cosmic microwave background. The SM is\n"
               "    internally consistent with the universal compositional invariance.")
    elif "LIMIT_CYCLE_P1" in term:
        verdict = "ANOMALOUS - vector-branch signature unexpected"
        msg = "    The SM neutrino prediction does NOT match universal invariance."
    else:
        verdict = f"UNDETERMINED - terminator {term}"
        msg = "    Likely degenerate or short-trajectory limit."
    print(msg)
    return j, verdict


if __name__ == "__main__":
    print("=" * 72)
    print("QD ROUND 2.6 - SM neutrino oscillation invariance test")
    print("=" * 72)
    print("\n[Step 1] Compute SM 3-flavor numu oscillation prediction")
    print("-" * 72)
    n = step_1_compute()
    print("\n[Step 2] Run canonical CNT engine on the SM prediction")
    print("-" * 72)
    step_2_run_engine()
    print("\n[Step 3] Report verdict on the central claim")
    print("-" * 72)
    j, verdict = step_3_report()

    summary = {
        "dataset": "Standard Model 3-flavor numu oscillation (PDG 2024 / NuFit 5.2 NO)",
        "pmns_parameters": {
            "sin2_theta_12": 0.307, "sin2_theta_13": 0.0218, "sin2_theta_23": 0.546,
            "delta_CP_pi_units": -0.5,
            "Dm2_21_eV2": 7.53e-5, "Dm2_31_eV2": 2.453e-3,
        },
        "energy_MeV": ENERGY_MEV,
        "L_range_km": [L_MIN_KM, L_MAX_KM],
        "T": n, "D": 3,
        "cnt_termination": j["depth"]["higgins_extensions"]["summary"]["curvature_termination"],
        "cnt_ir_class": j["depth"]["higgins_extensions"]["impulse_response"]["classification"],
        "cnt_amplitude_A": j["depth"]["higgins_extensions"]["impulse_response"]["amplitude_A"],
        "cnt_damping_zeta": j["depth"]["higgins_extensions"]["impulse_response"]["damping_zeta"],
        "cnt_content_sha256": j["diagnostics"]["content_sha256"],
        "verdict": verdict,
    }
    RESULTS.write_text(json.dumps(summary, indent=2))
    print(f"\nSummary saved: {RESULTS}")
