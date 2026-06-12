#!/usr/bin/env python3
"""
Generate compositional titration datasets from first-principles equilibrium chemistry.

Three standard titration systems, each producing a simplex trajectory:

1. Phosphoric acid (H₃PO₄) titration with NaOH
   - 4-part simplex: [H₃PO₄, H₂PO₄⁻, HPO₄²⁻, PO₄³⁻]
   - pKa₁=2.148, pKa₂=7.198, pKa₃=12.375
   - Three equivalence points, two buffer regions
   - The gold standard polyprotic titration

2. Citric acid (C₆H₈O₇) titration with NaOH
   - 4-part simplex: [H₃Cit, H₂Cit⁻, HCit²⁻, Cit³⁻]
   - pKa₁=3.13, pKa₂=4.76, pKa₃=6.40
   - Closely spaced pKa values — overlapping equilibria
   - Common industrial/food chemistry standard

3. Carbonic acid (H₂CO₃) titration with NaOH
   - 3-part simplex: [H₂CO₃, HCO₃⁻, CO₃²⁻]
   - pKa₁=6.35, pKa₂=10.33
   - Environmental chemistry standard (ocean pH, blood buffering)

All species fractions are computed exactly from equilibrium constants.
No approximations, no numerical solving — closed-form alpha expressions.

Alpha (species fraction) for a polyprotic acid HₙA:
  α₀ = [H⁺]ⁿ / denominator
  α₁ = Ka₁·[H⁺]ⁿ⁻¹ / denominator
  α₂ = Ka₁·Ka₂·[H⁺]ⁿ⁻² / denominator
  ...
  denominator = [H⁺]ⁿ + Ka₁·[H⁺]ⁿ⁻¹ + Ka₁·Ka₂·[H⁺]ⁿ⁻² + ...

This is exact — no iterative solving needed.
"""

import csv
import numpy as np
import os


def alpha_polyprotic(pH_values, pKa_list):
    """
    Compute species fractions (alpha values) for a polyprotic acid.

    For an n-protic acid with pKa₁, pKa₂, ..., pKaₙ:
    Returns (n+1) alpha values at each pH, summing to 1.0.

    This is the exact closed-form expression — no approximations.
    """
    Ka = [10**(-pk) for pk in pKa_list]
    n = len(Ka)  # number of dissociation steps

    alphas = np.zeros((len(pH_values), n + 1))

    for i, pH in enumerate(pH_values):
        H = 10**(-pH)

        # Build denominator terms: [H⁺]ⁿ, Ka₁·[H⁺]ⁿ⁻¹, Ka₁·Ka₂·[H⁺]ⁿ⁻², ...
        terms = np.zeros(n + 1)
        terms[0] = H**n  # fully protonated

        Ka_product = 1.0
        for j in range(n):
            Ka_product *= Ka[j]
            terms[j + 1] = Ka_product * H**(n - j - 1)

        denom = np.sum(terms)
        alphas[i, :] = terms / denom

    return alphas


def generate_phosphoric_acid():
    """
    Phosphoric acid titration with NaOH.
    H₃PO₄ → H₂PO₄⁻ → HPO₄²⁻ → PO₄³⁻

    pKa values from NIST Critical Stability Constants:
      pKa₁ = 2.148 (25°C, I→0)
      pKa₂ = 7.198
      pKa₃ = 12.375
    """
    pKa = [2.148, 7.198, 12.375]
    carriers = ["H3PO4", "H2PO4_minus", "HPO4_2minus", "PO4_3minus"]

    # pH range covering all three equilibria: pH 0.5 to 14.0
    # 200 points for smooth compositional trajectory
    pH_values = np.linspace(0.5, 14.0, 200)

    alphas = alpha_polyprotic(pH_values, pKa)

    return pH_values, alphas, carriers, pKa


def generate_citric_acid():
    """
    Citric acid titration with NaOH.
    H₃Cit → H₂Cit⁻ → HCit²⁻ → Cit³⁻

    pKa values (25°C):
      pKa₁ = 3.13
      pKa₂ = 4.76
      pKa₃ = 6.40

    Note: closely spaced pKa values create overlapping equilibria —
    multiple species coexist across a wide pH range.
    """
    pKa = [3.13, 4.76, 6.40]
    carriers = ["H3Cit", "H2Cit_minus", "HCit_2minus", "Cit_3minus"]

    pH_values = np.linspace(1.0, 10.0, 200)
    alphas = alpha_polyprotic(pH_values, pKa)

    return pH_values, alphas, carriers, pKa


def generate_carbonic_acid():
    """
    Carbonic acid titration with NaOH.
    H₂CO₃ → HCO₃⁻ → CO₃²⁻

    pKa values (25°C):
      pKa₁ = 6.35 (apparent, includes CO₂(aq) ⇌ H₂CO₃ equilibrium)
      pKa₂ = 10.33

    The carbonate system is the primary pH buffer of the ocean
    and the blood bicarbonate buffer system.
    """
    pKa = [6.35, 10.33]
    carriers = ["H2CO3", "HCO3_minus", "CO3_2minus"]

    pH_values = np.linspace(3.0, 13.0, 200)
    alphas = alpha_polyprotic(pH_values, pKa)

    return pH_values, alphas, carriers, pKa


def write_csv(filename, pH_values, alphas, carriers):
    """Write compositional data as pipeline-ready CSV."""
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(carriers)
        for i in range(len(pH_values)):
            row = [f"{alphas[i, j]:.10f}" for j in range(len(carriers))]
            writer.writerow(row)
    print(f"  Written: {filename} ({len(pH_values)} rows, {len(carriers)} carriers)")


def verify_closure(alphas, name):
    """Verify all rows sum to 1.0."""
    sums = np.sum(alphas, axis=1)
    max_dev = np.max(np.abs(sums - 1.0))
    print(f"  {name}: max closure deviation = {max_dev:.2e}")
    assert max_dev < 1e-12, f"Closure violation in {name}!"


def main():
    output_dir = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/Current-Repo/Hs/experiments/Hs-LAB01_Titration_Standards"
    data_dir = os.path.join(output_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    print("Generating titration standard compositional datasets...")
    print()

    # 1. Phosphoric acid
    print("1. Phosphoric acid (H₃PO₄) — 4-part simplex")
    pH, alphas, carriers, pKa = generate_phosphoric_acid()
    verify_closure(alphas, "H₃PO₄")
    write_csv(os.path.join(data_dir, "phosphoric_acid_titration.csv"), pH, alphas, carriers)
    print(f"   pKa: {pKa}")
    print(f"   pH range: {pH[0]:.1f} to {pH[-1]:.1f}")
    print()

    # 2. Citric acid
    print("2. Citric acid (H₃Cit) — 4-part simplex")
    pH, alphas, carriers, pKa = generate_citric_acid()
    verify_closure(alphas, "H₃Cit")
    write_csv(os.path.join(data_dir, "citric_acid_titration.csv"), pH, alphas, carriers)
    print(f"   pKa: {pKa}")
    print(f"   pH range: {pH[0]:.1f} to {pH[-1]:.1f}")
    print()

    # 3. Carbonic acid
    print("3. Carbonic acid (H₂CO₃) — 3-part simplex")
    pH, alphas, carriers, pKa = generate_carbonic_acid()
    verify_closure(alphas, "H₂CO₃")
    write_csv(os.path.join(data_dir, "carbonic_acid_titration.csv"), pH, alphas, carriers)
    print(f"   pKa: {pKa}")
    print(f"   pH range: {pH[0]:.1f} to {pH[-1]:.1f}")
    print()

    print("All datasets generated. Closure verified to machine precision.")
    print(f"Output directory: {data_dir}")


if __name__ == "__main__":
    main()
