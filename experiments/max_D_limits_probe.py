"""Maximum-D limits probe for Hs — measures the deterministic numerical ceilings.
Regenerates the anchors in papers/MAXIMUM_D_LIMITS.md. Author: Peter Higgins; AI-assisted per HUF-STD-001."""
import numpy as np, math
eps=np.finfo(np.float64).eps
print(f"float64 eps = {eps:.16e}")
print(f"int64 index ceiling 2^63 = {2**63:.6e} parts")
print(f"smallest positive normal double = {np.finfo(np.float64).tiny:.3e}")
print(f"{'D':>10} {'clr round-trip maxerr':>22} {'closure err':>14} {'mem (8B/part)':>14}")
rng=np.random.default_rng(0)
for D in [10**2,10**3,10**4,10**5,10**6,10**7]:
    x=rng.dirichlet(np.ones(D)*0.5); x/=x.sum()
    L=np.log(x); c=L-L.mean(); xr=np.exp(c); xr/=xr.sum()
    rt=float(np.max(np.abs(xr-x))); clo=abs(float(xr.sum())-1.0)
    mem=8*D; g=f"{mem/1e9:.2f} GB" if mem>=1e9 else (f"{mem/1e6:.1f} MB" if mem>=1e6 else f"{mem} B")
    print(f"{D:>10} {rt:>22.3e} {clo:>14.3e} {g:>14}")
print(f"\nD where D*eps ~ 1 (global log-sum precision floor): {1/eps:.3e}")
for D in [1e6,1e12,1e18]:
    diam=2*math.log(D)/math.log(3)
    print(f"  D={D:.0e}: tree diameter ~{diam:.0f}, diam^2*eps ~{diam*diam*eps:.2e}")
