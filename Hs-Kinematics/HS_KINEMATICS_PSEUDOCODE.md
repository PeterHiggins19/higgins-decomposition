# Hˢ Kinematics Engine — Language‑Agnostic Pseudocode (v1.0)

*A faithful, implementation‑independent transcription of `hs_kinematics_engine.py` + `hs_diagnosis.py`. Anyone can re‑implement the engine from this in any language and check conformance against the hash in the specification §11. Author: Peter Higgins; AI‑assisted per HUF‑STD‑001. Honest‑broker.*

---

## Notation
`M` = input matrix `[T rows × D carriers]`, real, non‑negative. `P` = closed `M`. `clr` = centered log‑ratio. `‖·‖` = Euclidean norm. `diff(X)` = row‑wise successive differences. All floats compared/serialized at 12 decimals.

## Primitives
```
function CLOSURE(M):
    M ← max(M, 0); for each row r: s ← sum(r); r ← r / (s if s>0 else 1)
    return M

function CLR(P):
    P ← max(P, 1e-12); L ← log(P)
    return L − rowmean(L)

function KEFF(P):                       # effective spread / entropy diversity
    P ← max(CLOSURE(P), 1e-12)
    return exp( − rowsum(P · log P) )

function SHANNON_MEAN(P):
    P ← CLOSURE(P); return mean over rows of ( − sum(P · log(max(P,1e-12))) )

function STABLE_HASH(payload):          # the determinism receipt
    round every float in payload to 12 decimals; canonicalize (sort keys)
    return SHA256( JSON(payload) )
```

## Stage 1 — carrier guard (E‑21) + zeros
```
function CARRIER_HEALTH(M):
    structural ← carriers that are 0 in EVERY row
    constant   ← carriers with zero range but not structural
    active     ← carriers not structural
    return structural, constant, active

GUARD: if structural or constant:
    report excluded(structural) [code GD-ZRC-CAL], flagged(constant) [code GD-CNC-CAL]
    if structural: drop structural carriers from M and names

sparsity ← fraction of entries ≤ 0          # if ≥ 0.5 → code GD-SPZ-WRN
function TREAT_ZEROS(M):                      # multiplicative replacement
    for each carrier j: pmin ← min positive in column j; set non‑positive entries ← 0.65·pmin
P ← CLOSURE(TREAT_ZEROS(M))
```

## Stage 2 — lossless reconstruction (exactness witness, P1)
```
function TILING_LOSSLESS(P):
    if D < 4: return (none, connected=true)
    charts ← every consecutive 4‑carrier window
    build rows A from within‑chart pairwise indicators (i→+1, j→−1) + one all‑ones closure row
    for each of up to 50 records t:
        b ← [ logP[t,i] − logP[t,j] for each chart pair (i,j) ] ++ [0]
        rec ← least_squares(A, b)
        err_t ← max| rec − CLR(P[t]) |
    return ( max_t err_t , connected=true )    # ≈1e‑15 on real data; exact if < 1e‑6
```

## Stage 3 — navigation reads
```
EFFECTIVE_SPREAD ← (KEFF(P)[0], KEFF(P)[last])           # start → end trend

function HELMSMAN_GUARD(P, names, floor=1e-6, tie=1e-3): # resolvability
    tot ← colsum(|diff(CLR(P))|); order ← argsort desc(tot)
    if tot[order[0]] < floor:           return (none, "HM-NUL-WRN")     # at rest
    if (tot[order0]−tot[order1]) ≤ tie·tot[order0]: return ("TIE","HM-TIE-WRN")
    return (names[order0], none)

function COHERENT_HELMSMAN(P, names):    # closure‑invariant steerer
    for each carrier i: m[i] ← mean over j≠i of sum| diff( logP[:,i] − logP[:,j] ) |
    return names[ argmax(m) ]

WAYPOINTS ← REGIMES(P):                  # candidate phase transitions
    s ← ‖diff(CLR(P))‖ per step; thr ← mean(s)+2·std(s); return indices where s>thr

SILENT_DRIFT ← DECEPTIVE(P):             # adiabatic / deceptive drift (P2)
    tv ← 0.5·rowsum|diff(CLOSURE(P))|; dk ← diff(KEFF(P))
    return count of steps where dk<0 AND tv ≤ median(tv)
```

## Stage 4 — guards: effective rank + hold‑lock
```
function EFFECTIVE_RANK(P):
    X ← CLR(P) − colmean; s ← singular_values(X); drop s ≤ s.max·1e‑9
    pr ← (sum s)² / sum(s²); maxr ← min(T−1, D−1)
    code ← "DG-RNK-WRN" if pr < 0.5·maxr else none
    return round(pr,2), maxr, code, s

function HOLD_LOCK(P, engine_floor=1e-9):     # discovered floor + hysteresis
    H ← CLR(P); st ← ‖diff(H)‖ per step
    md ← median(st); mad ← 1.4826·median|st−md|
    noise ← max(engine_floor, median(st)−mad, quantile(st,0.25), 1e-12)
    up ← 4·noise; lo ← 2·noise; state ← HOLD; ref ← 0; events ← []
    for t, m in st:
        if state=HOLD and m>up:  state ← MOVING
        elif state=MOVING and m<lo:
            if ‖H[t+1] − H[ref]‖ ≥ 3·noise: append t+1 to events; ref ← t+1
            state ← HOLD
    return round(noise,5), events
```

## Stage 5 — mechanics (jet to the noise floor, dynamics, integrals)
```
function MECHANICS(P, names, dt=1, noise_ratio=1.5):
    R ← CLR(P); d[0] ← R
    repeat up to 5×: if rows(d[last]) < 3 break; d.append( diff(d[last]) / dt )   # v,a,jerk,snap,crackle
    mag[k] ← mean‖d[k]‖
    order ← 1
    for k from 2:                                  # noise‑bounded max order
        ratio ← mag[k]/mag[k−1]; record ratio
        if ratio < noise_ratio: order ← k  else break
    v ← d[1]; a ← d[2]; mass ← (P[:-1]+P[1:])/2
    Tdir ← v/‖v‖
    curvature ← ‖a − (a·Tdir)Tdir‖ / ‖v‖²          # Frenet (median reported)
    p ← mass·v                                     # momentum
    net ← colsum(p)                                # arrow of intent
    coherence ← ‖net‖ / ( sum_t ‖p[t]‖ )           # 1 = ballistic, 0 = churn
    to   ← top carriers by net>0 ;  from ← top carriers by net<0
    force ← mean‖diff(p)/dt‖
    kinetic ← mean( 0.5·rowsum(mass·v²) ) ;  action ← sum over t of that
    angular ← mean_t ‖ outer(R[t],p[t]) − outer(p[t],R[t]) ‖ / √2
    pathlen ← sum‖v‖ ;  displacement ← ‖R[last]−R[0]‖ ;  efficiency ← displacement/pathlen
    return all of the above (dual‑named navigation/physics)
```

## Stage 6 — fringe / boundary (EITT, Tier 3)
```
function EITT_BOUNDARY(P, levels=(1,2,4), gate=0.01):
    for each level k with T//k ≥ 2:
        decimate P by geometric mean in blocks of k → Gk ; H[k] ← SHANNON_MEAN(Gk)
    drift ← (max H − min H) / |mean H|
    verdict ← "within-regime (EITT holds)" if drift<gate else "BOUNDARY" [code FR-BND-INF]
    return entropy_by_level, drift, verdict, tier="Tier 3 — a clue, never a claim"
```

## Stage 7 — assemble payload + hash
```
function RUN(M, names, dt=1):
    apply Stage 1 (guard, zeros, closure → P)
    recon ← TILING_LOSSLESS(P);  helm ← HELMSMAN_GUARD; er ← EFFECTIVE_RANK; (floor,events) ← HOLD_LOCK
    codes ← collect all fired guard codes
    payload ← { identity, input(records,carriers,names,sparsity[,carrier_guard]),
                lossless_reconstruction(exact, error=recon),
                navigation_reads(effective_spread, helmsman{raw,resolvable,coherent}, waypoints, silent_drift),
                kinematics_and_dynamics = MECHANICS(...),
                spectral_modes(singulars, effective_dimensionality),
                station_keeping(discovered_noise_floor=floor, structural_changes_at=events),
                guards_codes_fired = codes,
                fringe_boundary_TIER3 = EITT_BOUNDARY(P),
                computational_floors(ieee_reconstruction_floor, determinism_decimals=12,
                                     discovered_noise_floor, max_meaningful_derivative_order) }
    payload.content_hash ← STABLE_HASH(payload)
    return payload
```

## Diagnosis language (`hs_diagnosis.py`)
```
function DIAGNOSE(M, names):
    P ← CLOSURE(M); (Ks,Ke) ← (KEFF(P)[0], KEFF(P)[last]); (noise,events,maxstep) ← HOLD_LOCK‑variant
    rank ← participation ratio of CLR(P)
    if maxstep < 4·noise AND maxstep < 1e-6:           # honest rest gate
        return "The system is holding steady — at rest below its own noise floor. Nothing to report." (0 voices)
    movers ← carriers with |net momentum| ≥ 0.12·(max) ; each labelled gaining/shedding   # active voices
    trend ← concentrating if Ke<Ks−0.05 else diversifying if Ke>Ks+0.05 else steady
    build sentence: "<top mover> is steering (<dir>). Weight is moving toward <gaining>. It is moving away
        from <shedding>. The mixture is <trend> (effective spread Ks → Ke). It changed state N time(s).
        The motion runs in about <rank> independent directions. (<#movers> of D parts have something to say…)"
    voices scale with #movers (deterministic); same input → same words → same hash
```

*Conformance: implement the above and run the §11 reference; you should get `content_hash = fcae0ebe…a3d7ae7`. Any difference is a located deviation to explain, not noise (see `ADAPTIVE_ANTICIPATION.md`).*
