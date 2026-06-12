"""CN-TT v4 — concrete processing-section stages (each = control point + test point).
Wraps the kernel (geometry/atlas/quaternion/navigate) so the math stays locked while
the sections become modular, adaptable, individually testable, and hash-cacheable."""
from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
import numpy as np
import geometry as geo
import atlas as atl
import navigate as nav
from stage import Stage

# ---- L0 Adapt: domain raw -> canonical (carriers, labels, matrix) ----
class AdaptStage(Stage):
    name = "adapt"; version = "0.1.0"
    def run(self, ctx, cfg):
        header = ctx["header"]; rows = ctx["raw_rows"]
        carriers = [str(c).strip() for c in header[1:]]
        labels = [str(r[0]) for r in rows]
        matrix = [[float(x) for x in r[1:]] for r in rows]
        return {"carriers": carriers, "labels": labels, "matrix": matrix}
    def self_test(self):
        out = self.run({"header": ["t","a","b"], "raw_rows": [["0","1","2"],["1","3","4"]]}, {})
        ok = out["carriers"] == ["a","b"] and out["matrix"] == [[1.0,2.0],[3.0,4.0]]
        return ok, f"carriers={out['carriers']}"

# ---- L1 Treat: zero-treatment (multiplicative replacement) ----
class TreatStage(Stage):
    name = "treat"; version = "0.1.0"
    default_config = {"frac": 0.65}; config_bounds = {"frac": (0.5, 0.8)}
    def _treat(self, M, frac):
        M = np.asarray(M, float); out = M.copy()
        for j in range(M.shape[1]):
            col = M[:, j]; pos = col[col > 0]
            if pos.size: out[col <= 0, j] = frac * pos.min()
        return out
    def run(self, ctx, cfg):
        M = self._treat(ctx["matrix"], cfg["frac"])
        nz = int((np.asarray(ctx["matrix"], float) <= 0).sum())
        return {"matrix": M.tolist(), "zeros_replaced": nz}
    def self_test(self):
        out = self.run({"matrix": [[1.0, 0.0],[2.0, 4.0]]}, {"frac": 0.65})
        m = out["matrix"]; ok = m[0][1] > 0 and abs(m[0][1] - 0.65*4.0) < 1e-12
        return ok, f"zero->%.4f (replaced %d)" % (m[0][1], out["zeros_replaced"])

# ---- L1 Calibrate: identity by default; bounded linear gain/offset per carrier ----
class CalibrateStage(Stage):
    name = "calibrate"; version = "0.1.0"
    default_config = {"gain": 1.0, "offset": 0.0}
    def run(self, ctx, cfg):
        M = np.asarray(ctx["matrix"], float)
        g = np.asarray(cfg["gain"], float); o = np.asarray(cfg["offset"], float)
        out = np.maximum(g * M + o, 1e-300)
        return {"matrix": out.tolist(), "calibrated": bool(not (np.all(g == 1.0) and np.all(o == 0.0)))}
    def self_test(self):
        a = self.run({"matrix": [[2.0, 3.0]]}, {"gain": 1.0, "offset": 0.0})
        b = self.run({"matrix": [[2.0, 3.0]]}, {"gain": 2.0, "offset": 0.0})
        ok = a["matrix"] == [[2.0, 3.0]] and abs(b["matrix"][0][0] - 4.0) < 1e-12
        return ok, f"identity preserved; gain2 -> {b['matrix'][0][0]}"

# ---- L2 Geometry: closure -> CLR -> Helmert ILR -> radial ----
class GeometryStage(Stage):
    name = "geometry"; version = "0.1.0"
    def run(self, ctx, cfg):
        M = np.asarray(ctx["matrix"], float)
        comp = geo.closure(M); clr = geo.clr(comp)
        H = geo.helmert_basis(M.shape[1]); ilr = clr @ H.T
        return {"comp": comp.tolist(), "clr": clr.tolist(), "ilr": ilr.tolist(),
                "radial": geo.radial(ilr).tolist()}
    def self_test(self):
        out = self.run({"matrix": [[1.0,2.0,3.0,4.0],[4.0,3.0,2.0,1.0]]}, {})
        rowsum = max(abs(sum(r)) for r in out["clr"])
        return rowsum < 1e-12, f"max|sum(clr_row)|={rowsum:.1e}"

# ---- L3 Atlas: sliding/hierarchical tiling + lossless reconstruction ----
class AtlasStage(Stage):
    name = "atlas"; version = "0.1.0"
    default_config = {"strategy": "hierarchical"}
    def run(self, ctx, cfg):
        comp = np.asarray(ctx["comp"], float); D = comp.shape[1]
        charts = atl.hierarchical_atlas(D) if cfg["strategy"] == "hierarchical" else atl.sliding_window_atlas(D)
        edges = atl.edges_from_charts(charts)
        conn, nc = atl.is_connected(D, edges)
        err = max(atl.reconstruct_clr(D, edges, comp[t])[1] for t in range(comp.shape[0])) if conn else None
        return {"atlas": {"strategy": cfg["strategy"], "n_charts": len(charts), "n_edges": int(len(edges)),
                          "connected": bool(conn), "n_components": nc,
                          "recon_max_err": err, "lossless": bool(conn and err is not None and err < 1e-6)}}
    def self_test(self):
        rng = np.random.default_rng(0); x = rng.dirichlet(np.ones(16)*0.3, size=4)
        out = self.run({"comp": (x/x.sum(1, keepdims=True)).tolist()}, {"strategy": "hierarchical"})
        a = out["atlas"]; return (a["lossless"] and a["connected"]), f"err={a['recon_max_err']:.1e} charts={a['n_charts']}"

# ---- L4 Navigate: the parity navigation family ----
class NavigateStage(Stage):
    name = "navigate"; version = "0.1.0"
    default_config = {"regime_k": 2.0, "regime_threshold": 0.05}
    config_bounds = {"regime_k": (1.5, 3.0), "regime_threshold": (0.02, 0.1)}
    def run(self, ctx, cfg):
        return {"navigation": nav.navigate(ctx["comp"], ctx["clr"], ctx["ilr"],
                                           cfg["regime_k"], cfg["regime_threshold"])}
    def self_test(self):
        comp = [[0.25,0.25,0.25,0.25],[0.4,0.3,0.2,0.1],[0.7,0.1,0.1,0.1]]
        import geometry as g
        c = np.asarray(comp, float); clr = g.clr(c); H = g.helmert_basis(4); ilr = clr @ H.T
        out = self.run({"comp": comp, "clr": clr.tolist(), "ilr": ilr.tolist()}, self.default_config)
        kf = out["navigation"]["k_eff"]
        return (3.9 < kf["max"] <= 4.0 and kf["final"] < kf["max"]), f"k_eff max={kf['max']:.3f} final={kf['final']:.3f}"
