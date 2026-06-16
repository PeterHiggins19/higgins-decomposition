# Hs kinematics + diagnosis on REAL OIV world wine data (production composition by country, 1995-2025).
# Data: DATA/Industrial Compositions/CN-TT 15June2026/world wine data.xlsx (OIV). Public, sector-level.
import openpyxl, numpy as np, sys
sys.path.insert(0,"../../Hs-Kinematics")
import hs_kinematics_engine as eng, hs_diagnosis as dx
XL="/sessions/sharp-sleepy-bell/mnt/Claude CoWorker/DATA/Industrial Compositions/CN-TT 15June2026/world wine data.xlsx"
ws=openpyxl.load_workbook(XL,read_only=True,data_only=True)['Export']; it=ws.iter_rows(values_only=True)
hdr=list(next(it)); I={h:i for i,h in enumerate(hdr)}
g=lambda r,h:(r[I[h]] if I[h]<len(r) else None)
data=[r for r in it if r and g(r,'Region/Country')]
AGG={'Global','World','Total','EU','European Union',None}
def comp(product='Wine',variable='Production',k=14):
    d={}
    for r in data:
        if g(r,'Product')==product and g(r,'Variable')==variable:
            try:q=float(g(r,'Quantity'))
            except:continue
            yr,c=g(r,'Year'),g(r,'Region/Country')
            if yr is None or c in AGG:continue
            d.setdefault(int(yr),{})[c]=max(q,0.0)
    yrs=sorted(d); mean={}
    for y in yrs:
        for c,q in d[y].items(): mean.setdefault(c,[]).append(q)
    top=sorted(mean,key=lambda c:-np.mean(mean[c]))[:k]
    Y=[y for y in yrs if sum(d[y].get(c,0) for c in top)>0]
    return np.array([[d[y].get(c,0.0) for c in top] for y in Y]),top,Y
M,top,Y=comp()
print(f"WORLD WINE PRODUCTION (OIV) {Y[0]}-{Y[-1]} | top {len(top)}: {top}")
out=eng.run(M,top); k=out['kinematics_and_dynamics']
print("arrow of intent:",k['arrow_of_intent_NAV__momentum_PHYS'])
print("efficiency:",k['course_directness_NAV__path_efficiency_PHYS'],"| eff-dim:",out['spectral_modes']['degrees_of_freedom_NAV__effective_dimensionality_PHYS'])
print("DIAGNOSIS:",dx.diagnose(M,top)['narrative'])
