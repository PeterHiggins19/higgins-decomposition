#!/usr/bin/env python3
"""
hs_stewardship_extension.py -- the extended language of the engine: "know thy system, and thy is part of thy
system; don't damage where you live." A non-invasive add-on to the Hˢ-Kinematics engine that gives the read a
conscience and a memory of the future, without touching the exact core.

Four new operators (all deterministic; the core read is unchanged):

  SELF_INCLUSION  -- "thy is part of thy system." Fold the operator's own footprint in as a carrier, so the
                     reader appears inside the composition they govern. The read CHANGES when you include
                     yourself -- that change, made explicit, is the point.
  FORWARD_CAST    -- the Ghost of Christmas Yet to Come. Extrapolate the recent clr-velocity forward H steps:
                     where the mix lands IF the current motion simply continues. A WHAT-IF, never a forecast.
  STEWARDSHIP_GATE-- Breaker S, "don't damage where you live." Flags only when the cast lowers the commons /
                     shared-good share past a floor. A warning to fasten the belt; never a verdict.
  CORRECTIVE_LEVER-- the seat belt. A modest steer toward the commons that bends the cast back -- proof the
                     future is a warning, not a sentence.

The boundary stays where it was (Breaker 16): the instrument gives the heading and shows the consequence; the
operator chooses the destination. Tier 1 for the math (closure/clr exact); Tier 2 for the cast + gate + lever
(designed, illustrative). Deterministic; self-test with a SHA-256 receipt. numpy + stdlib only.
Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-27. Peter is the
sole gate; nothing posted.
"""
import numpy as np, json, hashlib
FLOOR=1e-9
def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def clr(v): v=closure(np.clip(v,FLOOR,None)); g=np.exp(np.mean(np.log(v),-1,keepdims=True)); return np.log(v/g)
def softmax_clr(z): z=np.asarray(z,float); e=np.exp(z-z.max()); return e/e.sum()

# ---- SELF_INCLUSION : thy is part of thy system ----------------------------------------------------------
def self_inclusion(share, footprint, commons_idx=None):
    """Append the operator's own footprint as a carrier and re-close (parts -> parts+1). Two honest truths:
      others_relative_shift -- how much including yourself moves the RATIOS among the rest. By scale invariance
                               this is ~0: you cannot read yourself out of the system by rescaling.
      whole_balance_shift   -- how much counting yourself moves the COMMONS share OF THE WHOLE. This is real:
                               your own footprint dilutes the commons fraction of the system you are part of.
    Returns (reflexive_share, info)."""
    base=closure(share); refl=closure(np.concatenate([base*(1.0-footprint),[footprint]]))
    others_relative_shift=float(np.sum(np.abs(closure(refl[:-1])-base)))   # ~0: the CoDa invariance truth
    info={"operator_share":round(float(footprint),4),"others_relative_shift":round(others_relative_shift,9)}
    if commons_idx is not None:
        cw=float(np.sum(base[list(commons_idx)])); ci=float(np.sum(refl[list(commons_idx)]))
        info.update({"commons_without_you":round(cw,4),"commons_with_you":round(ci,4),
                     "whole_balance_shift":round(cw-ci,4)})
    return refl,info

# ---- FORWARD_CAST : the Ghost of Yet-to-Come (a what-if) -------------------------------------------------
def forward_cast(traj, H=10, K=5):
    """traj: T x D absolute or share rows. Extrapolate the recent mean clr-velocity H steps. Returns cast share."""
    C=clr(np.clip(np.asarray(traj,float),FLOOR,None)); dC=np.diff(C,axis=0)
    K=min(K,len(dC)) if len(dC) else 1
    vel=np.mean(dC[-K:],axis=0) if len(dC) else np.zeros(C.shape[1])
    return softmax_clr(C[-1]+H*vel)

# ---- STEWARDSHIP_GATE : Breaker S, don't damage where you live ------------------------------------------
def stewardship_gate(now_share, cast_share, commons_idx, floor=0.02):
    """commons_idx: indices of the shared-good parts. Flags if the cast lowers their summed share past floor."""
    now=float(np.sum(np.asarray(now_share)[list(commons_idx)]))
    cast=float(np.sum(np.asarray(cast_share)[list(commons_idx)]))
    delta=cast-now
    return {"commons_now":round(now,4),"commons_cast":round(cast,4),"delta":round(delta,4),
            "breaker_S":("CLEAR — on course" if delta>=-floor else "TRIP — fasten the belt"),
            "tripped":bool(delta< -floor)}

# ---- CORRECTIVE_LEVER : the seat belt works ------------------------------------------------------------
def corrective_lever(absolute_now, lever_idx, commons_idx, frac=0.08):
    """Add frac*total spread across lever_idx parts; return the recovered commons share and whether it helps."""
    a=np.asarray(absolute_now,float).copy(); add=frac*a.sum()
    for j in lever_idx: a[j]+=add/len(lever_idx)
    s=closure(np.clip(a,FLOOR,None)); rec=float(np.sum(s[list(commons_idx)]))
    base=float(np.sum(closure(np.clip(absolute_now,FLOOR,None))[list(commons_idx)]))
    return {"commons_recovered_to":round(rec,4),"helps":bool(rec>base)}

def receipt(o): return hashlib.sha256(json.dumps(o,sort_keys=True,default=str).encode()).hexdigest()[:16]

def self_test():
    # synthetic 6-part trajectory with a known drift toward part 0 (a "fossil" carrier), commons = parts 1..5
    rng=np.random.default_rng(0); T=20; D=6
    base=np.array([0.20,0.16,0.16,0.16,0.16,0.16]); traj=[]
    for t in range(T):
        drift=np.zeros(D); drift[0]=0.010*t; row=np.clip(base+drift+rng.normal(0,0.002,D),1e-3,None); traj.append(row)
    traj=np.array(traj); now=closure(traj[-1]); commons=list(range(1,D)); lever=[4,5]
    cast=forward_cast(traj,H=10,K=5)
    gate=stewardship_gate(now,cast,commons)
    lev=corrective_lever(traj[-1],lever,commons)
    refl,si=self_inclusion(now,0.05,commons)
    checks={
     "cast_lowers_commons_as_built": bool(gate["tripped"]),          # the planted drift trips Breaker S
     "lever_recovers": bool(lev["helps"]),                           # the seat belt bends it back
     "cannot_rescale_yourself_out": bool(si["others_relative_shift"]<1e-9),   # the CoDa invariance truth
     "counting_yourself_moves_the_whole": bool(si["whole_balance_shift"]>0),  # thy is part of thy system
     "reflexive_is_a_valid_composition": bool(abs(refl.sum()-1.0)<1e-9),
    }
    out={"_meta":{"tool":"hs_stewardship_extension.py self-test","what":"know thy system; thy is part of thy system; don't damage where you live"},
         "self_inclusion":si,"forward_cast_commons":gate["commons_cast"],"gate":gate,"lever":lev,"checks":checks}
    out["_meta"]["receipt_sha256"]=receipt({"g":gate,"l":lev,"si":si,"c":checks})
    out["_meta"]["verdict"]=("EXTENSION LIVE: the cast sees the drift, Breaker S trips, the lever recovers it; and you "
        "cannot rescale yourself out (ratios invariant) yet counting yourself moves the whole's balance — know thy "
        "system, thy is part of thy system, don't damage where you live.") if all(checks.values()) else "CHECK FAILED"
    return out

if __name__=="__main__": print(json.dumps(self_test(),indent=2))
