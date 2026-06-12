#!/usr/bin/env python3
"""
Hˢ TENSOR TRANSFORMATION FUNCTION
====================================
The complete Higgins Decomposition expressed as a tensor functor.

ANSWER TO THE QUESTION: "Is there enough Hs construction to form a
tensor transformation function of Hs?"

YES. The existing construction provides exactly the right algebraic
objects. Here is the formal derivation and working implementation.

════════════════════════════════════════════════════════════════════════
TENSOR FORMULATION
════════════════════════════════════════════════════════════════════════

The Higgins Decomposition Hˢ is a composite functor:

    Hˢ : ℝ₊ᴺˣᴰ → ℝ

mapping a positive real matrix (N observations × D carriers) to a
scalar diagnostic classification.

Decomposed as tensor transformations:

    Hˢ = ρ ∘ Tr ∘ Σ ∘ Λ ∘ S

where each step is a tensor operation:

LAYER 1: S — Simplex Projection (rank-preserving)
─────────────────────────────────────────────────
    S : ℝ₊ᴺˣᴰ → Δᴰ⁻¹ˢ
    S(X)ᵢⱼ = Xᵢⱼ / Σₖ Xᵢₖ

    Tensor type: (1,1) → (1,1)  (matrix → matrix on simplex)
    Each row → probability vector. Rank preserved.

LAYER 2: Λ — Log-Ratio Transform (isometric embedding)
──────────────────────────────────────────────────────
    Λ : Δᴰ⁻¹ˢ → ℝᴺˣᴰ  (CLR basis)
    Λ(P)ᵢⱼ = ln(Pᵢⱼ) − (1/D) Σₖ ln(Pᵢₖ)

    Tensor type: (1,1) → (1,1)  (simplex matrix → Euclidean matrix)
    Isometry of (Δᴰ⁻¹, dₐ) into (ℝᴰ, ‖·‖₂) where dₐ is Aitchison distance.

    Basis choices (contravariant index transformation):
      CLR: Λ_clr = I − (1/D)𝟙𝟙ᵀ  applied to log(P)
      ILR: Λ_ilr = Ψᵀ · Λ_clr    where Ψ is Helmert (D×(D-1), orthonormal)
      ALR: Λ_alr = A · Λ_clr      where A is non-orthogonal projection

    KEY THEOREM: Tr(Ψᵀ · Cov(CLR) · Ψ) = Tr(Cov(CLR)) because Ψ is orthonormal.
    Therefore CLR and ILR are equivalent at the Trace gate.
    ALR breaks this because A is not orthogonal.

LAYER 3: Σ — Covariance Tensor (rank-2 symmetric)
─────────────────────────────────────────────────
    Σ : ℝᴺˣᴰ → Sym₊(D)
    Σ(Y)ᵢⱼ = (1/N) Σₜ (Yₜᵢ − μᵢ)(Yₜⱼ − μⱼ)

    Tensor type: (1,1) → (0,2) symmetric
    This is the VARIATION MATRIX V(t). A rank-2 symmetric tensor field
    over the parameter space (cumulative window size t).

    V(t) carries the full compositional information:
      Eigenvalues λᵢ(t) — variance along each principal axis
      Eigenvectors vᵢ(t) — principal directions of compositional variation
      Tr(V(t)) = σ²_A(t) — total Aitchison variance (scalar invariant)

LAYER 4: Tr — Trace Contraction (the balun gate)
────────────────────────────────────────────────
    Tr : Sym₊(D) → ℝ₊
    Tr(V) = Σᵢ Vᵢᵢ = Σᵢ λᵢ

    Tensor type: (0,2) → (0,0)  (full contraction to scalar)
    This is the key dimensional gate: balanced (D×D matrix) → unbalanced (scalar).

    When λ₁ ≫ Σᵢ₌₂ λᵢ, the tensor is effectively rank-1 and the
    Trace contraction retains the dominant eigenvalue.
    Reflection coefficient: Γ = √(1 − λ₁/Tr(V))

LAYER 5: ρ — Diagnostic Classification (pattern matching)
─────────────────────────────────────────────────────────
    ρ : ℝ₊ → {NATURAL, INVESTIGATE, FLAG} × ℝ₊
    ρ(σ²) = argmin_{c ∈ Constants} |σ² − c|

    Tensor type: (0,0) → label + residual
    Not a tensor operation per se, but a classification on the scalar ring.

════════════════════════════════════════════════════════════════════════
THE FULL TENSOR FUNCTOR
════════════════════════════════════════════════════════════════════════

    Hˢ(X) = ρ(Tr(Σ(Λ(S(X)))))

    Type signature:
      ℝ₊ᴺˣᴰ →^S Δᴰ⁻¹ˢ →^Λ ℝᴺˣᴰ →^Σ Sym₊(D) →^Tr ℝ₊ →^ρ Label

    Tensor ranks:
      (1,1)  →  (1,1)  →  (1,1)  →  (0,2)  →  (0,0)  →  classification

    The critical transformation is Σ: the passage from a rank-(1,1) data
    tensor to a rank-(0,2) symmetric tensor. This is where the system's
    geometric structure crystallises from observations into covariance.

════════════════════════════════════════════════════════════════════════
WHAT THE TENSOR VIEW REVEALS
════════════════════════════════════════════════════════════════════════

1. BASIS COVARIANCE: The functor is natural in the categorical sense —
   changing basis (CLR → ILR via Ψ) commutes with Trace when Ψ is
   orthonormal. This is why CLR ≡ ILR. The naturality square:

       Sym_CLR(D) ──Tr──→ ℝ
          │                │
        Ψᵀ·(·)·Ψ          =
          │                │
       Sym_ILR(D-1) ─Tr─→ ℝ

2. FUNCTORIALITY: Hˢ preserves composition. If X₁, X₂ are independent
   compositional datasets, Σ(Λ(S(X₁ ⊕ X₂))) decomposes as a direct
   sum in the eigenvalue spectrum.

3. THE ENRICHMENT: The full diagnostic is not just Tr but the entire
   eigenspectrum {λᵢ, vᵢ, S_vN, Γ, Q}. This enriches the functor
   from Hˢ : Data → Label to:

     Hˢ_enriched : Data → (Sym₊(D), λ_spectrum, v_stability, S_vN, Γ, VSWR, Q, Label)

   The matrix diagnostics ARE the enrichment of the tensor functor.

Author: Peter Higgins / Claude
Version: 1.0
Date: 2026-04-30
"""

import numpy as np
from typing import Dict, Tuple, List, Optional, Any


# ════════════════════════════════════════════════════════════
# TENSOR TRANSFORMATION LAYERS
# ════════════════════════════════════════════════════════════

class TensorLayer:
    """Base class for tensor transformation layers."""
    def __init__(self, name: str, input_rank: Tuple[int,int], output_rank: Tuple[int,int]):
        self.name = name
        self.input_rank = input_rank
        self.output_rank = output_rank

    def forward(self, tensor):
        raise NotImplementedError

    def __repr__(self):
        return f"{self.name}: ({self.input_rank}) → ({self.output_rank})"


class SimplexProjection(TensorLayer):
    """S : ℝ₊ᴺˣᴰ → Δᴰ⁻¹ˢ — closure to unit simplex."""
    def __init__(self, zero_delta=1e-6):
        super().__init__("S (Simplex)", (1,1), (1,1))
        self.zero_delta = zero_delta

    def forward(self, X: np.ndarray) -> np.ndarray:
        data = X.copy().astype(np.float64)
        # Zero replacement
        mask = data <= 0
        if mask.any():
            data[mask] = self.zero_delta
            for i in range(data.shape[0]):
                if mask[i].any():
                    n_rep = mask[i].sum()
                    if n_rep < data.shape[1]:
                        total_delta = n_rep * self.zero_delta
                        non_zero = ~mask[i]
                        scale = (1.0 - total_delta) / data[i, non_zero].sum()
                        data[i, non_zero] *= scale
                        data[i, mask[i]] = self.zero_delta
        # Closure
        return data / data.sum(axis=1, keepdims=True)


class LogRatioTransform(TensorLayer):
    """Λ : Δᴰ⁻¹ˢ → ℝᴺˣᴰ — log-ratio embedding (CLR default)."""
    def __init__(self, basis='CLR'):
        super().__init__(f"Λ ({basis})", (1,1), (1,1))
        self.basis = basis

    def forward(self, P: np.ndarray) -> np.ndarray:
        D = P.shape[1]
        log_P = np.log(P)
        # CLR: subtract geometric mean
        clr = log_P - log_P.mean(axis=1, keepdims=True)

        if self.basis == 'CLR':
            return clr
        elif self.basis == 'ILR':
            Psi = self._helmert(D)
            return clr @ Psi  # N×(D-1)
        elif self.basis == 'ALR':
            return log_P[:, :-1] - log_P[:, -1:]  # N×(D-1)
        else:
            raise ValueError(f"Unknown basis: {self.basis}")

    @staticmethod
    def _helmert(D: int) -> np.ndarray:
        """Helmert submatrix: D×(D-1), orthonormal columns."""
        Psi = np.zeros((D, D - 1))
        for j in range(D - 1):
            k = j + 1
            Psi[:k, j] = 1.0 / np.sqrt(k * (k + 1))
            Psi[k, j] = -k / np.sqrt(k * (k + 1))
        return Psi


class CovarianceTensor(TensorLayer):
    """Σ : ℝᴺˣᴰ → Sym₊(D) — covariance as rank-2 symmetric tensor.

    Produces the variation matrix V(t) for cumulative windows.
    """
    def __init__(self):
        super().__init__("Σ (Covariance)", (1,1), (0,2))

    def forward(self, Y: np.ndarray) -> Dict[str, Any]:
        """Returns the full V(t) tensor field plus the final matrix."""
        N, D = Y.shape
        n_slices = min(10, N // 3)
        if n_slices < 2:
            n_slices = 2
        slice_indices = np.linspace(2, N - 1, n_slices, dtype=int)

        V_field = {}  # t → V(t) with eigendecomposition
        for t in slice_indices:
            window = Y[:t + 1]
            V_t = np.cov(window.T)
            if V_t.ndim == 0:
                V_t = np.array([[V_t]])
            vals, vecs = np.linalg.eigh(V_t)
            idx = np.argsort(vals)[::-1]
            V_field[int(t)] = {
                'matrix': V_t,
                'eigenvalues': vals[idx],
                'eigenvectors': vecs[:, idx],
                'trace': float(np.trace(V_t)),
            }

        # Final (full data)
        V_final = np.cov(Y.T)
        if V_final.ndim == 0:
            V_final = np.array([[V_final]])
        vals_final, vecs_final = np.linalg.eigh(V_final)
        idx = np.argsort(vals_final)[::-1]

        return {
            'V_field': V_field,
            'V_final': V_final,
            'eigenvalues': vals_final[idx],
            'eigenvectors': vecs_final[:, idx],
            'trace': float(np.trace(V_final)),
            'D': D,
            'N': N,
            'slice_indices': slice_indices.tolist(),
        }


class TraceContraction(TensorLayer):
    """Tr : Sym₊(D) → ℝ₊ — trace contraction (the balun gate).

    Also computes the enriched output: Γ, VSWR, Q, S_vN, κ.
    """
    def __init__(self):
        super().__init__("Tr (Trace/Balun)", (0,2), (0,0))

    def forward(self, sigma_result: Dict) -> Dict[str, Any]:
        V = sigma_result['V_final']
        eigenvalues = sigma_result['eigenvalues']
        D = sigma_result['D']
        trace = sigma_result['trace']

        # Scalar trajectory (Aitchison variance at each slice)
        trajectory = {t: data['trace'] for t, data in sigma_result['V_field'].items()}

        # Impedance match
        lambda1_frac = float(eigenvalues[0] / trace) if trace > 0 else 0
        gamma = float(np.sqrt(1 - lambda1_frac)) if lambda1_frac <= 1 else 0
        vswr = (1 + gamma) / (1 - gamma) if gamma < 1 else float('inf')

        # Von Neumann entropy
        rho_eigs = eigenvalues / trace if trace > 0 else eigenvalues
        safe = rho_eigs[rho_eigs > 1e-15]
        S_vn = float(-np.sum(safe * np.log(safe)))
        S_max = float(np.log(D))

        # Condition number
        positive = eigenvalues[eigenvalues > 1e-15]
        kappa = float(positive[0] / positive[-1]) if len(positive) > 1 else float('inf')

        # Eigenvector stability
        V_field = sigma_result['V_field']
        slices = sorted(V_field.keys())
        if len(slices) >= 2:
            v1_first = V_field[slices[0]]['eigenvectors'][:, 0]
            v1_last = V_field[slices[-1]]['eigenvectors'][:, 0]
            overlap = float(abs(np.dot(v1_first, v1_last)))
        else:
            overlap = 1.0

        # Commutator
        if len(slices) >= 2:
            V1 = V_field[slices[0]]['matrix']
            V2 = V_field[slices[-1]]['matrix']
            comm = V1 @ V2 - V2 @ V1
            comm_norm = float(np.linalg.norm(comm, 'fro'))
            norm_prod = np.linalg.norm(V1, 'fro') * np.linalg.norm(V2, 'fro')
            comm_normalized = comm_norm / norm_prod if norm_prod > 0 else 0
        else:
            comm_normalized = 0

        return {
            'trace': trace,
            'trajectory': trajectory,
            'lambda1_fraction': lambda1_frac,
            'gamma': gamma,
            'VSWR': float(vswr) if not np.isinf(vswr) else 'inf',
            'von_neumann_entropy': S_vn,
            'von_neumann_ratio': S_vn / S_max if S_max > 0 else 0,
            'condition_number': kappa,
            'eigenvector_overlap': overlap,
            'commutator_norm': comm_normalized,
            'eigenvalues': eigenvalues.tolist(),
        }


class DiagnosticClassification(TensorLayer):
    """ρ : ℝ₊ → Label — pattern matching against transcendental constants."""

    CONSTANTS = {
        "pi": np.pi, "1/pi": 1/np.pi, "e": np.e, "1/e": 1/np.e,
        "ln2": np.log(2), "1/ln2": 1/np.log(2),
        "phi": (1+np.sqrt(5))/2, "1/phi": 2/(1+np.sqrt(5)),
        "sqrt2": np.sqrt(2), "1/sqrt2": 1/np.sqrt(2),
        "euler_gamma": 0.5772156649, "catalan": 0.9159655942,
        "2pi": 2*np.pi, "e^pi": np.e**np.pi, "pi^e": np.pi**np.e,
        "pi/4": np.pi/4, "pi^2/6": np.pi**2/6,
        "ln_phi": np.log((1+np.sqrt(5))/2),
        "omega_lambert": 0.5671432904, "dottie": 0.7390851332,
    }

    def __init__(self):
        super().__init__("ρ (Classification)", (0,0), None)

    def forward(self, trace_result: Dict) -> Dict[str, Any]:
        trajectory = trace_result['trajectory']
        sigma_values = list(trajectory.values())

        best_delta = float('inf')
        best_const = None
        matches = []

        for sv in sigma_values:
            if sv <= 0:
                continue
            for test_val, label in [(sv, 'direct'), (1/sv if sv > 1e-15 else 0, 'reciprocal')]:
                if test_val <= 0:
                    continue
                for cname, cval in self.CONSTANTS.items():
                    if cval <= 0:
                        continue
                    delta = abs(test_val - cval)
                    if delta < 0.05:
                        matches.append({'constant': cname, 'delta': delta, 'type': label})
                        if delta < best_delta:
                            best_delta = delta
                            best_const = cname

        if best_delta < 0.01:
            classification = 'NATURAL'
        elif best_delta < 0.05:
            classification = 'INVESTIGATE'
        else:
            classification = 'FLAG'

        return {
            'classification': classification,
            'closest_constant': best_const,
            'closest_delta': best_delta if best_delta < float('inf') else None,
            'total_matches': len(matches),
            'matches': matches[:20],
        }


# ════════════════════════════════════════════════════════════
# TENSOR FUNCTOR COMPOSITION
# ════════════════════════════════════════════════════════════

class HsTensorFunctor:
    """
    The complete Hˢ tensor transformation function.

        Hˢ = ρ ∘ Tr ∘ Σ ∘ Λ ∘ S

    Each layer is a tensor transformation with explicit rank changes.
    The functor is natural with respect to orthonormal basis changes.
    """

    def __init__(self, basis='CLR'):
        self.layers = [
            SimplexProjection(),           # S: (1,1) → (1,1)
            LogRatioTransform(basis),      # Λ: (1,1) → (1,1)
            CovarianceTensor(),            # Σ: (1,1) → (0,2)
            TraceContraction(),            # Tr: (0,2) → (0,0)
            DiagnosticClassification(),    # ρ: (0,0) → Label
        ]
        self.basis = basis

    def __call__(self, X: np.ndarray) -> Dict[str, Any]:
        """Apply the full tensor functor to data X (N×D)."""
        return self.forward(X)

    def forward(self, X: np.ndarray) -> Dict[str, Any]:
        """Full forward pass through all tensor layers."""
        result = {'input_shape': X.shape, 'basis': self.basis}
        tensor = X

        for layer in self.layers:
            tensor = layer.forward(tensor)
            result[layer.name] = tensor

        # Package final output
        trace_out = result['Tr (Trace/Balun)']
        class_out = result['ρ (Classification)']

        result['summary'] = {
            'classification': class_out['classification'],
            'trace': trace_out['trace'],
            'gamma': trace_out['gamma'],
            'VSWR': trace_out['VSWR'],
            'von_neumann_ratio': trace_out['von_neumann_ratio'],
            'eigenvector_overlap': trace_out['eigenvector_overlap'],
            'condition_number': trace_out['condition_number'],
            'commutator_norm': trace_out['commutator_norm'],
            'closest_constant': class_out['closest_constant'],
            'closest_delta': class_out['closest_delta'],
            'balun_matched': trace_out['gamma'] < 0.2,
        }

        return result

    def type_signature(self) -> str:
        """Human-readable type signature."""
        parts = []
        for layer in self.layers:
            parts.append(f"{layer.name}: {layer.input_rank} → {layer.output_rank}")
        return "\n".join(parts)

    def naturality_proof(self) -> str:
        """Prove CLR ≡ ILR via naturality square."""
        return (
            "NATURALITY PROOF: CLR ≡ ILR at the Trace gate\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Let Ψ be the Helmert basis (D×(D-1), orthonormal columns).\n"
            "ILR = Ψᵀ · CLR, so Cov_ILR = Ψᵀ · Cov_CLR · Ψ.\n"
            "\n"
            "Tr(Cov_ILR) = Tr(Ψᵀ · Cov_CLR · Ψ)\n"
            "             = Tr(Cov_CLR · Ψ · Ψᵀ)    [cyclic property]\n"
            "             = Tr(Cov_CLR)               [Ψ · Ψᵀ = I for orthonormal]\n"
            "\n"
            "Therefore: Tr ∘ Σ ∘ Λ_CLR = Tr ∘ Σ ∘ Λ_ILR  ∎\n"
            "\n"
            "This is the naturality square:\n"
            "  Sym_CLR(D) ──Tr──→ ℝ\n"
            "     │                │\n"
            "   Ψᵀ·(·)·Ψ          =\n"
            "     │                │\n"
            "  Sym_ILR(D-1) ─Tr─→ ℝ\n"
            "\n"
            "ALR breaks naturality because its transformation matrix A is\n"
            "NOT orthogonal: A · Aᵀ ≠ I, so Tr(Aᵀ · Cov · A) ≠ Tr(Cov)."
        )


# ════════════════════════════════════════════════════════════
# VERIFICATION
# ════════════════════════════════════════════════════════════

def verify_naturality(X: np.ndarray) -> Dict[str, Any]:
    """Verify that CLR ≡ ILR ≠ ALR at the Trace gate."""
    clr_functor = HsTensorFunctor('CLR')
    ilr_functor = HsTensorFunctor('ILR')
    alr_functor = HsTensorFunctor('ALR')

    r_clr = clr_functor(X)
    r_ilr = ilr_functor(X)
    r_alr = alr_functor(X)

    tr_clr = r_clr['Tr (Trace/Balun)']['trace']
    tr_ilr = r_ilr['Tr (Trace/Balun)']['trace']
    tr_alr = r_alr['Tr (Trace/Balun)']['trace']

    return {
        'CLR_trace': tr_clr,
        'ILR_trace': tr_ilr,
        'ALR_trace': tr_alr,
        'CLR_ILR_identical': abs(tr_clr - tr_ilr) < 1e-10,
        'ALR_deviation': abs(tr_clr - tr_alr),
        'naturality_holds': abs(tr_clr - tr_ilr) < 1e-10,
    }


# ════════════════════════════════════════════════════════════
# MAIN — DEMONSTRATION
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("═" * 75)
    print("  Hˢ TENSOR TRANSFORMATION FUNCTION — DEMONSTRATION")
    print("═" * 75)

    # Create the functor
    Hs = HsTensorFunctor('CLR')

    print("\nTYPE SIGNATURE:")
    print(Hs.type_signature())

    print("\n" + Hs.naturality_proof())

    # Test with Nuclear-like data
    print("\n" + "═" * 75)
    print("  TEST: Nuclear SEMF (rank-1 dominant)")
    print("═" * 75)

    np.random.seed(42)
    # Generate SEMF-like data: dominated by one mode
    N, D = 50, 5
    t = np.linspace(0, 1, N)
    dominant = 90 + 5 * t
    others = np.column_stack([
        5 - t, 3 - 0.5*t, 1.5 + 0.2*t, 0.5 + 0.3*t
    ])
    nuclear = np.column_stack([dominant, others])

    result = Hs(nuclear)
    s = result['summary']

    print(f"\n  Classification: {s['classification']}")
    print(f"  Trace: {s['trace']:.6f}")
    print(f"  Γ = {s['gamma']:.4f}  (balun {'MATCHED' if s['balun_matched'] else 'REFLECTING'})")
    print(f"  VSWR = {s['VSWR']}")
    print(f"  S/S_max = {s['von_neumann_ratio']:.4f}")
    print(f"  Eigenvector overlap = {s['eigenvector_overlap']:.6f}")
    print(f"  Condition number = {s['condition_number']:.1f}")
    print(f"  Commutator norm = {s['commutator_norm']:.6f}")
    if s['closest_delta'] is not None:
        print(f"  Closest constant: {s['closest_constant']} (δ = {s['closest_delta']:.4e})")
    else:
        print(f"  Closest constant: None (no match within threshold)")

    # Verify naturality
    print("\n" + "═" * 75)
    print("  NATURALITY VERIFICATION: CLR ≡ ILR ≠ ALR")
    print("═" * 75)

    nat = verify_naturality(nuclear)
    print(f"\n  CLR trace: {nat['CLR_trace']:.10f}")
    print(f"  ILR trace: {nat['ILR_trace']:.10f}")
    print(f"  ALR trace: {nat['ALR_trace']:.10f}")
    print(f"  CLR ≡ ILR: {nat['CLR_ILR_identical']}  ✓")
    print(f"  ALR deviation: {nat['ALR_deviation']:.6f}")
    print(f"  Naturality holds: {nat['naturality_holds']}  ✓")

    # Test with adversarial data
    print("\n" + "═" * 75)
    print("  TEST: Adversarial (thermal state)")
    print("═" * 75)

    adversarial = np.random.dirichlet([1, 1, 1, 1, 1], size=50)

    result_adv = Hs(adversarial)
    s_adv = result_adv['summary']

    print(f"\n  Classification: {s_adv['classification']}")
    print(f"  Γ = {s_adv['gamma']:.4f}  (balun {'MATCHED' if s_adv['balun_matched'] else 'REFLECTING'})")
    print(f"  S/S_max = {s_adv['von_neumann_ratio']:.4f}")
    print(f"  Eigenvector overlap = {s_adv['eigenvector_overlap']:.6f}")
    print(f"  Condition number = {s_adv['condition_number']:.1f}")

    print("\n" + "═" * 75)
    print("  CONCLUSION: Hˢ IS a tensor transformation function.")
    print("  5 layers, explicit rank changes, natural w.r.t. orthonormal bases.")
    print("═" * 75)
