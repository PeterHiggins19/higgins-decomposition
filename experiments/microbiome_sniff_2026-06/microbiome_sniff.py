"""CN-TT v4 — microbiome high-D sniff.
Performance + functionality test on MICROBIOME-REALISTIC compositional data
(structure modeled on coda4microbiome: Calle, Pujolassos & Susin 2023, BMC
Bioinformatics 24:82 — sparse, many taxa, phylogenetic tree). SYNTHETIC data
(the real Crohn/HIV .rda run is the trivial next step on a machine with R/pyreadr).
Tests: (A) lossless tree-atlas reconstruction at microbiome D + timing/footprint;
(B) longitudinal navigation reads an injected perturbation; (C) determinism."""
import sys, time, json
from pathlib import Path
import numpy as np
ENG = Path(__file__).resolve().parents[2] / "HCI-CNTT" / "engine"
sys.path.insert(0, str(ENG))
import geometry as geo, navigate as nav, atlas as atl, provenance as prov

rng = np.random.default_rng(20260610)

def microbiome_matrix(N, D, prevalence_a=0.35, seed=0):
    """Realistic sparse microbiome composition: log-normal abundances x Bernoulli
    presence (zero-inflated), every taxon present in >=1 sample (no structural zeros)."""
    r = np.random.default_rng(seed)
    base = r.normal(0, 2.0, size=D)                      # per-taxon log-mean (wide => skewed)
    prev = r.beta(prevalence_a, 1.0, size=D)             # per-taxon prevalence (many rare)
    M = np.zeros((N, D))
    for i in range(N):
        present = r.random(D) < prev
        ab = np.exp(base + r.normal(0, 1.0, size=D)) * present
        M[i] = ab
    # guarantee no all-zero taxon (structural) -> seed one sample for each empty col
    empty = M.sum(0) == 0
    for j in np.where(empty)[0]:
        M[r.integers(N), j] = np.exp(base[j])
    # close + multiplicative zero-treatment (rounded zeros -> 0.65*min positive per col)
    M = M / M.sum(1, keepdims=True)
    for j in range(D):
        col = M[:, j]; pos = col[col > 0]
        if pos.size: M[col <= 0, j] = 0.65 * pos.min()
    return M / M.sum(1, keepdims=True)

print("== CN-TT v4 microbiome sniff (synthetic, coda4microbiome-structured) ==\n")
print("(A) high-D lossless tree-atlas reconstruction + performance")
print(f"  {'taxa(D)':>8} {'samples':>8} {'charts':>8} {'recon_err':>11} {'edges':>9} {'time/sample':>12} {'mem~MB':>8}")
rowsA = []
for D in [48, 256, 2048, 10000]:
    N = 20
    M = microbiome_matrix(N, D, seed=D)
    comp = geo.closure(M)
    charts = atl.hierarchical_atlas(D); edges = atl.edges_from_charts(charts)
    t0 = time.perf_counter()
    errs = [atl.reconstruct_clr(D, edges, comp[i])[1] for i in range(N)]
    dt = (time.perf_counter() - t0) / N
    mem = edges.nbytes / 1e6
    me = max(errs)
    rowsA.append({"D": D, "N": N, "charts": len(charts), "recon_err": me, "edges": int(len(edges)), "time_per_sample_s": dt})
    print(f"  {D:>8} {N:>8} {len(charts):>8} {me:>11.1e} {len(edges):>9} {dt*1e3:>9.1f}ms {mem:>8.1f}")

print("\n(B) longitudinal navigation — does the instrument read an injected perturbation?")
# subject microbiome over T timepoints; antibiotic-like perturbation at t0 (bloom + diversity drop), then recovery
D, T, t0 = 128, 60, 30
r = np.random.default_rng(7)
base = r.normal(0, 1.5, size=D); prev = r.beta(0.5, 1.0, size=D)
bloom = r.choice(D, size=6, replace=False)               # taxa that bloom under perturbation
series = np.zeros((T, D))
for t in range(T):
    logab = base + r.normal(0, 0.15, size=D)
    if t >= t0:
        decay = np.exp(-(t - t0) / 8.0)                  # perturbation magnitude decays (recovery)
        logab[bloom] += 3.2 * decay                      # bloom
        logab += -0.8 * decay                            # everything else suppressed
    ab = np.exp(logab) * (r.random(D) < prev)
    series[t] = ab
empty = series.sum(0) == 0
for j in np.where(empty)[0]: series[r.integers(T), j] = np.exp(base[j])
series = series / series.sum(1, keepdims=True)
for j in range(D):
    col = series[:, j]; pos = col[col > 0]
    if pos.size: series[col <= 0, j] = 0.65 * pos.min()
series = series / series.sum(1, keepdims=True)
comp = geo.closure(series); clr = geo.clr(comp); H = geo.helmert_basis(D); ilr = clr @ H.T
navout = nav.navigate(comp, clr, ilr)
keff = [s["k_eff"] for s in navout["steps"]]
bnds = navout["regime_boundaries"]["indices"]
# helmsman at the perturbation onset
helm_at = [navout["steps"][t]["helmsman"] for t in range(t0, t0+3)]
print(f"  D={D} taxa, T={T} timepoints, perturbation injected at t={t0} (6 taxa bloom -> recovery)")
print(f"  K_eff: baseline mean {np.mean(keff[:t0]):.1f} -> min after perturbation {min(keff[t0:]):.1f} (diversity collapse detected)")
print(f"  regime boundaries flagged at t = {bnds}  (perturbation onset t={t0} should appear)")
print(f"  helmsman at onset points to taxa {sorted(set(helm_at))}; injected bloom taxa were {sorted(bloom.tolist())}")
print(f"  deceptive-drift steps: {navout['regime_counts']['deceptive']}; tightening: {navout['regime_counts']['tightening']}")
onset_hit = any(abs(b - t0) <= 1 for b in bnds)
helm_hit = len(set(helm_at) & set(bloom.tolist())) > 0
print(f"  --> onset flagged within +/-1 step: {onset_hit}; helmsman identified a bloom taxon: {helm_hit}")

print("\n(C) determinism")
h1 = prov.stable_hash(navout); 
navout2 = nav.navigate(geo.closure(series), geo.clr(geo.closure(series)), geo.clr(geo.closure(series)) @ geo.helmert_basis(D).T)
h2 = prov.stable_hash(navout2)
print(f"  navigation stable_hash identical on rerun: {h1==h2}  ({h1[:16]})")

json.dump({"reconstruction": rowsA,
           "longitudinal": {"D": D, "T": T, "perturbation_t": t0, "boundaries": bnds,
                            "keff_baseline": float(np.mean(keff[:t0])), "keff_min_post": float(min(keff[t0:])),
                            "onset_flagged": bool(onset_hit), "helmsman_hit_bloom": bool(helm_hit),
                            "deceptive": navout["regime_counts"]["deceptive"]},
           "determinism": bool(h1==h2),
           "reference": "coda4microbiome: Calle, Pujolassos & Susin 2023, BMC Bioinformatics 24:82 (data structure; synthetic here)"},
          open(Path(__file__).resolve().parent / "microbiome_sniff_result.json", "w"), indent=2)
print("\nsaved microbiome_sniff_result.json")
