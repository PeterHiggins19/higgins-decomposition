#!/usr/bin/env python3
"""
the_sniffer.py -- the data's own geometry tells you where to go next. A rover (or Matthew on the cliff) does not
hunt by random chance; at each station it takes a TETRODE of 4 samples, and the sniffer reads the local
COMPOSITIONAL GRADIENT and says "go this way" -- gradient ascent toward the signal, on the data itself, no
external map. Samples in TIME and LOCATION are part of the data (the station log is the map being built).

This realizes operators that were already seeded in the oldest archive (RWA V∞Core RMU index:
geodesic_equation_proxy, exterior_derivative, geodesic_deviation_proxy; "gradient descent on a unity-constrained
objective") -- now made concrete and receipted, in the same cohesive system as the ultrasonic probe (lock the
determinized object, PID-track) and the autonomous forager.

Mechanism, per station:
  1. take 4 samples at small offsets (the TETRODE; 4 points over-determine the 2-D gradient AND average the DUT
     noise -- the tetrode standard);
  2. read each as a composition; take the clr of the signal part;
  3. least-squares fit the spatial gradient of the signal-clr from the 4 points (exterior derivative / geodesic
     direction toward the richer ground);
  4. step that way. Repeat. The geometry of the data is the heading; the operator chooses to follow it (Breaker 16).

Measured against a random-walk searcher over many seeds: the sniffer reaches the target in far fewer stations.
HONEST: synthetic terrain; the gradient method is real; field deployment needs real survey/assay data + the
geologist's judgement. Deterministic; receipt. Author: Peter Higgins (human authorship for all claims);
AI-assisted per HUF-STD-001. 2026-06-27. Peter is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib
def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def clr_part0(comp):                      # clr of part 0 (the "signal"/ore part) of a 3-part composition
    c=closure(np.clip(comp,1e-9,None)); g=np.exp(np.mean(np.log(c))); return float(np.log(c[0]/g))
def sha(o): return hashlib.sha256(json.dumps(o,sort_keys=True,default=str).encode()).hexdigest()[:16]

FIELD=10.0; TARGET=np.array([8.0,7.0]); SCALE=40.0   # broad enough that a heading exists across the whole field
def ore_share(p):                          # signal part rises toward the target (the hidden ore body)
    d2=float(np.sum((np.asarray(p)-TARGET)**2)); return 0.10+0.80*np.exp(-d2/SCALE)
def composition_at(p):                      # {ore, gangue, other}
    o=ore_share(p); return closure([o, (1-o)*0.6, (1-o)*0.4])
# tetrode offsets: 4 points (a small cross) around the station -> gradient + noise averaging
OFF=np.array([[1,0],[-1,0],[0,1],[0,-1]],float)*0.5

def signal_clr_noisy(p, rng, sigma):
    c=composition_at(p)*np.exp(rng.normal(0,sigma,3))   # DUT noise (multiplicative)
    return clr_part0(c)

def sniff_gradient(p, rng, sigma):
    pts=OFF; vals=np.array([signal_clr_noisy(p+d,rng,sigma) for d in pts])
    # least squares: vals ~ a + g . d  ->  solve for g (2-vector)
    A=np.column_stack([np.ones(len(pts)),pts]); coef,*_=np.linalg.lstsq(A,vals,rcond=None)
    g=coef[1:]; n=np.linalg.norm(g); return (g/n if n>0 else np.zeros(2))

def run_sniffer(seed, sigma=0.08, step=0.7, maxst=120):
    rng=np.random.default_rng(seed); p=np.array([1.0,1.0]); align=[]
    for s in range(maxst):
        if np.linalg.norm(p-TARGET)<0.6: return s, float(np.mean(align)) if align else 0.0
        g=sniff_gradient(p,rng,sigma)
        true_dir=(TARGET-p)/np.linalg.norm(TARGET-p); align.append(float(np.dot(g,true_dir)))
        p=np.clip(p+step*g+rng.normal(0,0.05,2),0,FIELD)
    return maxst, float(np.mean(align)) if align else 0.0

def run_random(seed, step=0.7, maxst=120):
    rng=np.random.default_rng(seed+99999); p=np.array([1.0,1.0])
    for s in range(maxst):
        if np.linalg.norm(p-TARGET)<0.6: return s
        th=rng.uniform(0,2*np.pi); p=np.clip(p+step*np.array([np.cos(th),np.sin(th)]),0,FIELD)
    return maxst

M=300
sn=[run_sniffer(s) for s in range(M)]; sn_st=np.array([x[0] for x in sn]); sn_al=np.array([x[1] for x in sn])
rd_st=np.array([run_random(s) for s in range(M)])
res={"sniffer_mean_stations":round(float(sn_st.mean()),2),"random_mean_stations":round(float(rd_st.mean()),2),
     "sniffer_median":int(np.median(sn_st)),"random_median":int(np.median(rd_st)),
     "gradient_alignment_with_true_bearing":round(float(sn_al.mean()),3),
     "speedup_x":round(float(rd_st.mean()/sn_st.mean()),2),
     "sniffer_reached_rate":round(float((sn_st<120).mean()),3),"random_reached_rate":round(float((rd_st<120).mean()),3)}
checks={
 "sniffer_beats_random": bool(res["sniffer_mean_stations"]<res["random_mean_stations"]),
 "gradient_points_toward_signal": bool(res["gradient_alignment_with_true_bearing"]>0.3),
 "sniffer_reaches_reliably": bool(res["sniffer_reached_rate"]>0.9),
 "tetrode_of_4_used": bool(len(OFF)==4),
}
master=sha({"r":res,"c":checks})
verdict=(f"THE SNIFFER works: guided by the compositional gradient read from a TETRODE of 4 samples per station, "
   f"the rover reaches the signal in {res['sniffer_mean_stations']} stations vs {res['random_mean_stations']} for "
   f"random hunting ({res['speedup_x']}x fewer), with the gradient aligned to the true bearing "
   f"({res['gradient_alignment_with_true_bearing']}). The data's own geometry is the heading -- no external map, "
   "the same cohesive system as the ultrasonic probe and the forager. The operator chooses to follow it (Breaker 16).") if all(checks.values()) else "CHECK FAILED"
out={"_meta":{"tool":"the_sniffer.py","what":"compositional-gradient tetrode field guidance (the sniffer)","trials":M,
              "master_receipt":master,"verdict":verdict},
     "results":res,"checks":checks,"target":TARGET.tolist(),"tetrode_offsets":OFF.tolist(),
     "lineage":("realizes RWA V∞Core RMU operators (geodesic/exterior-derivative/geodesic-deviation; gradient "
        "descent on a unity-constrained objective) -- archive -> concrete + receipted; ties the tetrode standard, "
        "the ultrasonic probe (determinized-object lock + PID), and the autonomous forager into one system."),
     "fence":("Synthetic terrain; the gradient method is real, the field is illustrative. Real deployment needs "
        "real survey/assay compositions + the geologist's judgement; the sniffer gives the heading, the operator "
        "chooses the destination (Breaker 16). Peter is the sole gate; nothing posted.")}
if __name__=="__main__": print(json.dumps(out,indent=2))
