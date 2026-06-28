#!/usr/bin/env python3
"""
hs_probe.py -- THE INSTRUMENT: the Hs filter-injection differential probe (reusable module).

A general non-invasive probe: read a composition's STRUCTURE by differencing the RETURN against a
known REFERENCE in log-ratio (clr) space, so that a multiplicative common-mode (gain / coupling /
source level / dilution) is reciprocated away EXACTLY. Generalizes the ultrasonic probe to any
compositional return (gas blend, ion panel, spectral band power, ...).

RESEARCH / QA INSTRUMENT ONLY -- NOT a clinical or diagnostic device. Medical use requires validation
to medical standards (IEC 62304 / ISO 13485). Honest-broker tiered. Peter is the sole gate; nothing posted.
"""
import numpy as np, hashlib, json

def closure(v):
    v=np.asarray(v,float); return v/v.sum(axis=-1,keepdims=True)
def clr(v):
    v=closure(v); g=np.exp(np.mean(np.log(v),axis=-1,keepdims=True)); return np.log(v/g)

class HsProbe:
    """Set a known reference (the injection / healthy template); read returns against it."""
    def __init__(self, reference):
        self.ref = closure(np.asarray(reference,float))
        self.ref_clr = clr(self.ref)
    def read(self, ret):
        """Differential structure read: z = clr(return) - clr(reference). Multiplicative common-mode
        cancels exactly (clr(g*x)=clr(x)). Returns the structure deviation in clr space."""
        return clr(np.asarray(ret,float)) - self.ref_clr
    def lock(self, z):
        """Lock onto structure: the dominant deviating component (index) and its magnitude."""
        z=np.atleast_1d(z); i=int(np.argmax(np.abs(z))); return i,float(z.flat[i])
    def detect(self, ret, thresh=0.15):
        """Drift/flaw statistic = Aitchison distance of the return from the reference; flag if > thresh."""
        z=self.read(ret); d=float(np.sqrt(np.sum(z**2,axis=-1)).mean()); return d, bool(d>thresh)
    @staticmethod
    def receipt(obj):
        return hashlib.sha256(json.dumps(obj,sort_keys=True,default=str).encode()).hexdigest()[:16]

def self_test():
    """Known-hash conformance: a fixed composition + a 10x common-mode must read identically."""
    ref=np.array([5,3,2.0]); p=HsProbe(ref)
    x=np.array([4.0,4.0,2.0]); z1=p.read(x); z2=p.read(10.0*x)        # 10x common-mode
    cm_rej=float(np.max(np.abs(z1-z2)))                                # must be ~floor
    return {"common_mode_residual":float(f"{cm_rej:.2e}"),"pass":bool(cm_rej<1e-12),
            "fixture_receipt":HsProbe.receipt({"z":np.round(z1,8).tolist()})}

if __name__=="__main__":
    print(json.dumps(self_test(),indent=2))
