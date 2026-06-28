# Stewardship extension — language-agnostic pseudocode

*Companion to `hs_stewardship_extension.py` (self-test receipt `4c40932c30018925`). The extended language of the
engine — "know thy system, and thy is part of thy system; don't damage where you live" — as four operators that
sit on top of the exact core without touching it. The core read (closure → clr → effective dimension → helmsman
→ receipt) is unchanged; these add foresight and a conscience. Tier 1 for the geometry, Tier 2 for the cast /
gate / lever (designed, illustrative). The operator still chooses the destination (Breaker 16). Author: Peter
Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-27. Peter is the sole gate;
nothing posted.*

---

## Shared primitives (from the core)

```
function CLOSURE(v):            return v / sum(v)                       # parts of a conserved whole
function CLR(v):                v ← CLOSURE(clip(v, FLOOR, ∞))
                               g ← exp(mean(log(v)))                   # geometric mean
                               return log(v / g)                       # centered log-ratio
function SOFTMAX_CLR(z):        return exp(z − max(z)) / sum(exp(z − max(z)))   # clr⁻¹ back to shares
```

## 1. SELF_INCLUSION — "thy is part of thy system"

```
function SELF_INCLUSION(share, footprint, commons_idx):
    base ← CLOSURE(share)
    refl ← CLOSURE( concat( base · (1 − footprint),  [footprint] ) )   # append the operator as a carrier
    others_relative_shift ← sum(| CLOSURE(refl[0..D−1]) − base |)       # → 0  (scale invariance: you cannot
                                                                        #       rescale yourself out of the system)
    commons_without_you   ← sum( base[commons_idx] )
    commons_with_you      ← sum( refl[commons_idx] )                    # diluted by your own footprint
    whole_balance_shift   ← commons_without_you − commons_with_you      # > 0  (counting yourself moves the whole)
    return refl, {others_relative_shift, whole_balance_shift, ...}
```

Two truths, both exact: the **ratios among the rest are invariant** to adding yourself (the CoDa truth — you
cannot read yourself out by rescaling), yet **the commons balance of the whole moves**, because your footprint is
now one of the parts that must be stewarded.

## 2. FORWARD_CAST — the Ghost of Christmas Yet to Come (a what-if)

```
function FORWARD_CAST(trajectory, H, K):
    C   ← CLR(trajectory)                          # T × D path in log-ratio space
    dC  ← diff(C, axis=time)                        # step velocities
    vel ← mean( dC[last K steps] )                  # recent heading
    return SOFTMAX_CLR( C[last] + H · vel )          # where the mix lands IF the motion simply continues
```

A deterministic extrapolation of the recent heading — **a warning of what may come to pass, never a forecast.**

## 3. STEWARDSHIP_GATE — Breaker S, "don't damage where you live"

```
function STEWARDSHIP_GATE(now_share, cast_share, commons_idx, floor = 0.02):
    now   ← sum( now_share[commons_idx] )
    cast  ← sum( cast_share[commons_idx] )
    delta ← cast − now
    if delta ≥ −floor:  return CLEAR  ("on course")
    else:               return TRIP   ("fasten the belt")     # only trips when the cast LOWERS the commons share
```

A breaker that stays quiet unless the forward cast would **reduce the shared-good (commons) share** — a warning to
fasten the belt, never a verdict on what to do.

## 4. CORRECTIVE_LEVER — the seat belt works

```
function CORRECTIVE_LEVER(absolute_now, lever_idx, commons_idx, frac = 0.08):
    a ← copy(absolute_now);  add ← frac · sum(a)
    for j in lever_idx:  a[j] += add / count(lever_idx)        # a modest steer toward the commons
    recovered ← sum( CLOSURE(a)[commons_idx] )
    return {recovered, helps: recovered > commons_share(absolute_now)}
```

Proof that **the future the cast shows is a warning, not a sentence**: a modest steer bends the cast back. Change
the image, and the image changes.

## Order of use (non-invasive overlay)

```
core_read ← HS_KINEMATICS(trajectory)                          # the exact read, unchanged (Tier 1)
cast      ← FORWARD_CAST(trajectory, H, K)                     # the what-if (Tier 2)
gate      ← STEWARDSHIP_GATE(core_read.now_share, cast, commons)
if gate == TRIP:
    lever ← CORRECTIVE_LEVER(absolute_now, clean_parts, commons)   # show the belt works
refl      ← SELF_INCLUSION(core_read.now_share, operator_footprint, commons)
# report: the read, the cast, the gate, the lever, and the operator's own place in the system.
# DECISION: the operator chooses the destination (Breaker 16). The instrument only shows the play.
```

*Cross-refs: `hs_stewardship_extension.py` (`4c40932c30018925`), `hs_kinematics_engine.py` (the core),
`../experiments/foresight_stewardship_2026-06/foresight_run.py` (`f19cd3de451118f6`, the real EMBER+Backblaze
run), `../huf-gov/doctrine/DONT_DAMAGE_WHERE_YOU_LIVE.md` (the doctrine). Peter is the sole gate; nothing posted.*
