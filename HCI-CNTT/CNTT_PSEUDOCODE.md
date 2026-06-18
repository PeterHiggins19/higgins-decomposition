# CN‑TT v4 — language‑agnostic pseudocode (the replication reference)

*Every stage of the engine in plain pseudocode, so a designer can reimplement it in any language and verify against the Python/R ports (`tools/CNTT_single_cell.py`, `tools/cntt_single_cell.R`). Conventions: `M` is a matrix with rows = records (time/sample order) and columns = carriers (parts of a whole); `D` = number of carriers, `T` = number of records. All `log` are natural log. Author: Peter Higgins; AI‑assisted per HUF‑STD‑001. Honest‑broker; claim tiers in `CNTT_DESIGNER_SPECIFICATION.md`.*

---

```
INPUT:  M[T×D]  (counts or amounts ≥ 0),  names[D]
OUTPUT: payload  (reads + guard codes + deterministic content hash)

# ---------- 0. CARRIER GUARD (E-21) — admissibility before geometry ----------
structural ← columns j where M[:,j] has no positive value      # undefined under log-ratio
constant   ← columns j where max(M[:,j]) == min(M[:,j])         # admissible but degenerate
active     ← all columns except structural
if structural or constant:
    record carrier_guard{ excluded=names[structural], flagged=names[constant],
                          codes = ["GD-ZRC-CAL" if structural] + ["GD-CNC-CAL" if constant] }
    if structural: M ← M[:, active] ;  names ← names[active]    # drop only the undefined ones
sparsity ← fraction of entries of M that are ≤ 0

# ---------- 1. ZERO TREATMENT (multiplicative replacement of sporadic zeros) ----------
for each column j:
    p ← positive values of M[:,j]
    if p nonempty: replace every M[t,j] ≤ 0 with 0.65 · min(p)

# ---------- 2. GEOMETRY (closure → CLR → ILR) ----------
closure(M):  row r ↦ r / sum(r)                                 # onto the simplex
P ← closure(M)
clr(P):      L ← log(clip(P, 1e-12)) ;  return L − rowMean(L)   # centered log-ratio (sums to 0)
CLR ← clr(P)
helmert(D):  (D−1)×D orthonormal contrast basis B;  row i = ( 1/i,…,1/i, −1, 0,…,0 )·√(i/(i+1))
ILR ← CLR · Bᵀ                                                  # isometric log-ratio coords

# ---------- 3. LOSSLESS 4-PART TILING (the signature reconstruction) ----------
# Cover D carriers with overlapping 4-part charts; each chart's internal pairwise
# log-ratios are exact and closure-invariant. Stack them + the sum-zero constraint and
# solve for the full CLR. Connected overlap graph  ⇒  exact recovery (≈ machine floor).
charts ← all windows [s, s+1, s+2, s+3] for s = 0 … D−4        # overlap = 3
build linear system A · c = b:
    for each chart, for each pair (i,j) in the chart:
        row of A with +1 at i, −1 at j ;   b-entry = log P[t,i] − log P[t,j]
    append one row of all-ones with b-entry 0                  # sum-zero constraint
for t in a sample of records:
    solve least-squares A · rec = b ;   err[t] ← max| rec − CLR[t] |
reconstruction_max_err ← max(err) ;   lossless ← (graph connected AND err < 1e-6)

# ---------- 4. NAVIGATION FAMILY (per-series reads) ----------
k_eff(P)      ← exp( Shannon entropy of each row of P )         # effective # of active carriers
step[t]       ← ‖ CLR[t+1] − CLR[t] ‖                           # Aitchison step
helmsman_CLR  ← argmax_j  Σ_t | ΔCLR[t,j] |                     # which carrier steers the change
regime_bounds ← { t : step[t] > mean(step) + k·std(step) }     # k = 2  (old fixed-threshold)
TV[t]         ← ½ Σ | P[t+1] − P[t] |                           # total-variation step
deceptive     ← count of t where k_eff falls AND TV[t] ≤ median(TV)   # quiet concentration

# ---------- 5. GUARD LAYER (2026-06 — say what cannot be resolved) ----------
helmsman_guard(P):                                             # resolvability of the driver
    total_j ← Σ_t |ΔCLR[t,j]| ;  lead, runner ← top two j
    mag ← total[lead] ;  margin ← total[lead] − total[runner]
    if mag < motion_floor(1e-6):  return None, code "HM-NUL-WRN"   # at rest → no leader
    if margin ≤ tie_rel(1e-3)·mag: return "TIE", code "HM-TIE-WRN" # unseparated → tie
    return names[lead], no code

coherent_helmsman(P):                                          # carrier-set-robust driver
    score_j ← (1/(D−1)) Σ_{i≠j} Σ_t | Δ( log P[:,j] − log P[:,i] ) |   # pairwise log-ratio motion
    return names[argmax_j score]                              # invariant to adding/removing carriers

effective_rank(P):                                            # dimensionality of the motion
    s ← singular values of mean-centered CLR
    eff ← (Σs)² / Σs²   (participation ratio) ;  maxr ← min(T−1, D−1)
    code ← "DG-RNK-WRN" if eff < 0.5·maxr   # motion collapsed into a subspace

hold_lock(P):                                                 # self-calibrating structural change
    step[t] ← ‖ΔCLR[t]‖
    noise ← max( engine_floor 1e-9 , robust_quiet_level(step) )     # DISCOVER the trigger
            # robust_quiet_level = max( quantile(step,0.5) − 1.4826·MAD , quantile(step,0.25) )
    up ← 4·noise ;  lo ← 2·noise                              # hysteresis band (k_up > k_down)
    state ← HOLD ;  ref ← 0 ;  events ← []
    for t:
        if state==HOLD and step[t] > up:        state ← MOVING
        elif state==MOVING and step[t] < lo:
            if ‖CLR[t+1] − CLR[ref]‖ ≥ 3·noise: events.append(t+1) ; ref ← t+1   # structural + valid
            state ← HOLD
    return noise, events                                      # held drift is reported, never silent

sparsity_regime ← "GD-SPZ-WRN" if sparsity ≥ 0.5             # CLR geometry is replacement-dominated

# ---------- 6. DETERMINISTIC CONTENT HASH (the receipt) ----------
stable_hash(obj):
    round every float to 12 decimals ;  serialize canonically (keys sorted) ;  SHA-256
# same input → same output → same hash, on any platform (cross-platform value-determinism).

# ---------- 7. ASSEMBLE PAYLOAD ----------
payload ← { input{n_records,n_carriers,carriers,sparsity_pct, carrier_guard?},
            atlas{lossless, reconstruction_max_err},
            navigation{k_eff_start,k_eff_end, helmsman_CLR, coherent_helmsman,
                       regime_boundaries, deceptive_drift_steps},
            guards{resolvability, effective_rank, hold_lock, sparsity_regime, codes_fired} }
payload.cntt_content_sha256 ← stable_hash(payload)
return payload
```

## Notes for the implementer

- **Determinism rules:** no randomness in the science path; any sampling uses a fixed declared seed. Round floats to a declared precision (12 dp) before hashing so receipts match across platforms. The *values* are reproducible to the IEEE floor; byte‑identical cross‑*language* hashing additionally requires an agreed canonical serialization (Tier‑3 — the ports each hash within their own language).
- **Conditional, hash‑neutral guards:** `carrier_guard` and the resolvability block attach to the payload **only when a code fires**. On clean data nothing fires → identical payload → identical hash. This is the property that lets the guard layer be added without re‑basing the oracle.
- **Lossless requires connectivity:** the overlap graph of the charts must be connected; with overlap‑3 sliding windows it always is for D ≥ 4. A disjoint cover → reconstruction is rank‑deficient (emit `L3-DSJ-ERR`).
- **Conformance:** a correct reimplementation reproduces the numeric reads (lossless error ≈ machine floor, the helmsman, K_eff, effective rank, the hold‑lock events) on the shared demo data. See `CNTT_DESIGNER_SPECIFICATION.md` §Conformance.

*This pseudocode is the distilled engine — the core reads, the lossless tiling, and the guard layer. The frozen‑oracle binary additionally carries the full depth‑tower/IR‑class recursion, the CNQ quaternion bench, and EITT; see `CNTT_COMPLETE_SPECIFICATION.md`.*
