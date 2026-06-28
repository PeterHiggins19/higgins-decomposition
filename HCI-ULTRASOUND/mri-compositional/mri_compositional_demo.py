#!/usr/bin/env python3
"""
mri_compositional_demo.py -- is Hs useful for MRI? Yes, exactly where MRI data IS (or becomes) a COMPOSITION:
derived FRACTIONS / metabolite sets -- NOT raw k-space or raw image intensity. Demonstrated on published
glioma MR-spectroscopy ratios and on NODDI's sum-to-one compartment fractions.

Four measured points (all deterministic; receipt over the results):
  1. SCANNER/COIL-GAIN INVARIANCE. MRI intensity is non-quantitative; scanner effects are modelled as
     MULTIPLICATIVE + additive (ComBat). A compositional read EXACTLY cancels the MULTIPLICATIVE common-mode
     (clr(g.x)=clr(x), residual ~1e-15): a deterministic, no-training complement to statistical harmonization
     for the multiplicative component.
  2. GRADE SEPARATION. On published glioma metabolite signatures (high vs low grade, Cho/Cr ~2.44 vs 1.48,
     Cho/NAA ~2.05 vs 1.41), the compositional read separates grades (Aitchison) -- a locked discriminant on
     the metabolite simplex.
  3. CREATINE-DENOMINATOR CONFOUND. MRS commonly divides by Cr (assumed stable) -- a KNOWN confound when Cr
     itself shifts. The clr (geometric-mean reference) needs NO arbitrary denominator and is robust where the
     Cho/Cr ratio is misled.
  4. NODDI SUM-TO-ONE GEOMETRY. NODDI fractions sum to 1; raw-fraction correlation is a CLOSURE ARTIFACT
     (negative even for INDEPENDENT compartments); the principled measure -- LOG-RATIO VARIANCE -- correctly
     separates proportional (low) from independent (high).

MEDICAL FENCE (firm): RESEARCH / QA demonstrator on SYNTHETIC compositions from PUBLISHED ratios -- NOT a
clinical/diagnostic device, NOT a medical claim, NOT patient data. Cancels the MULTIPLICATIVE scanner component
only. Certification (IEC 62304 / ISO 13485) is the deploying company's (Southmedic); the offer stays OFF the
public repo. Raw k-space/intensity is NOT compositional. Deterministic; receipt. Sources in
THE_MRI_COMPOSITIONAL_STUDY.md. Author: Peter Higgins (human authorship for all claims); AI-assisted per
HUF-STD-001. 2026-06-26. Peter is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib

def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def clr(v): v=closure(np.clip(v,1e-12,None)); g=np.exp(np.mean(np.log(v),-1,keepdims=True)); return np.log(v/g)
def aitch(a,b): return float(np.linalg.norm(clr(a)-clr(b)))
rng=np.random.default_rng(20260626)

# metabolite composition [NAA, Cho, Cr, Lac/Lip], from published glioma ratios (relative to Cr=1)
HIGH=np.array([2.44/2.05,2.44,1.0,0.8]); LOW=np.array([1.48/1.41,1.48,1.0,0.1]); NORMAL=np.array([2.0,0.8,1.0,1e-3])
def cohort(sig,n=60,bio=0.08): return [closure(np.abs(sig*(1+bio*rng.standard_normal(4)))) for _ in range(n)]
hi=cohort(HIGH); lo=cohort(LOW); nm=cohort(NORMAL)

X=np.array(hi+lo+nm); g=rng.uniform(0.2,5.0,size=(X.shape[0],1))
gain_residual=float(np.max(np.abs(clr(g*X)-clr(X))))                # 1. scanner gain invariance

def centroid(c): return closure(np.exp(np.mean([clr(x) for x in c],0)))
d_hi_lo=aitch(centroid(hi),centroid(lo)); within_hi=float(np.mean([aitch(x,centroid(hi)) for x in hi]))
sep=round(d_hi_lo/within_hi,2)                                      # 2. grade separation

hi_true=centroid(hi)                                                # 3. creatine-denominator confound
def confound_Cr(x,f=1.35): y=x.copy(); y[2]*=f; return closure(y)
hi_conf=[confound_Cr(x) for x in hi]
cho_cr_true=float(np.mean([x[1]/x[2] for x in hi])); cho_cr_conf=float(np.mean([x[1]/x[2] for x in hi_conf]))
clr_drift_conf=float(np.mean([aitch(x,hi_true) for x in hi_conf])); clr_drift_low=aitch(centroid(lo),hi_true)

indepA=np.abs(rng.standard_normal((400,3)))+0.3                     # 4. NODDI sum-to-one geometry
propB=indepA.copy(); propB[:,2]=propB[:,0]*1.5+0.02*np.abs(rng.standard_normal(400))
FA=closure(indepA); FB=closure(propB)
raw_indep=float(np.corrcoef(FA[:,0],FA[:,2])[0,1]); raw_prop=float(np.corrcoef(FB[:,0],FB[:,2])[0,1])
lrv_indep=float(np.var(np.log(indepA[:,0]/indepA[:,2]))); lrv_prop=float(np.var(np.log(propB[:,0]/propB[:,2])))

checks={"scanner_gain_cancels_exactly":bool(gain_residual<1e-12),"grades_separate":bool(sep>2.0),
 "clr_robust_to_Cr_confound":bool(clr_drift_conf<0.25*clr_drift_low and cho_cr_conf<0.85*cho_cr_true),
 "raw_corr_is_a_closure_artifact":bool(raw_indep<-0.2),
 "logratio_variance_finds_the_real_relation":bool(lrv_prop<0.3*lrv_indep)}
verdict=("USEFUL FOR MRI WHERE THE DATA IS A COMPOSITION: clr cancels the multiplicative scanner gain exactly, "
   f"separates glioma grades ({sep}x), is robust to the creatine-denominator confound, and gives NODDI fractions "
   "the correct (log-ratio) geometry.") if all(checks.values()) else "CHECK FAILED"

results={
 "1_scanner_gain_invariance":{"max_clr_residual_under_random_gain":float(f"{gain_residual:.1e}"),
    "meaning":"compositional read EXACTLY cancels the multiplicative scanner/coil component; deterministic complement to ComBat"},
 "2_grade_separation":{"high_vs_low_Aitchison":round(d_hi_lo,3),"within_grade_scatter":round(within_hi,3),
    "separation_ratio":sep,"meaning":"locked discriminant on the metabolite simplex separates grades"},
 "3_creatine_denominator_confound":{"Cho_Cr_true":round(cho_cr_true,2),"Cho_Cr_after_35pct_Cr_rise":round(cho_cr_conf,2),
    "clr_drift_under_confound":round(clr_drift_conf,3),"clr_drift_for_a_real_grade_change":round(clr_drift_low,3),
    "meaning":"the Cho/Cr ratio is MISLED by a Cr shift; the clr (geometric-mean reference, no arbitrary denominator) stays put"},
 "4_noddi_sum_to_one":{"raw_corr_independent":round(raw_indep,3),"raw_corr_proportional":round(raw_prop,3),
    "logratio_var_independent":round(lrv_indep,3),"logratio_var_proportional":round(lrv_prop,3),
    "meaning":"raw fraction correlation is pushed negative by closure even when compartments are INDEPENDENT (a known artifact); LOG-RATIO VARIANCE correctly separates proportional (low) from independent (high)"},
 "checks":checks}
receipt=hashlib.sha256(json.dumps(results,sort_keys=True,default=str).encode()).hexdigest()[:16]
out={"_meta":{"tool":"mri_compositional_demo.py","what":"Hs for MRI -- on compositional MRI quantities (MRS, NODDI)",
              "verdict":verdict,"receipt_sha256":receipt},"results":results,
     "fence":("RESEARCH/QA demonstrator on SYNTHETIC compositions from PUBLISHED ratios -- NOT clinical/diagnostic, "
        "NOT patient data, NOT a medical claim. Cancels the MULTIPLICATIVE scanner component only. Certification is "
        "the deploying company's (Southmedic); offer OFF public repo. Raw k-space/intensity is NOT compositional. "
        "Peter is the sole gate; nothing posted.")}
if __name__=="__main__": print(json.dumps(out,indent=2))
