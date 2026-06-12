"""CN-TT v4 — Pipeline: threads stages, hashes each, caches by (input,config,version)
so identical work is never repeated ('why repeat history at the cost of time and effort').
A config change recomputes only the changed section + everything downstream of it."""
from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
import provenance as prov

class Pipeline:
    def __init__(self, stages):
        self.stages = stages
        self.cache = {}

    def _digest(self, ctx):
        return prov.stable_hash({k: v for k, v in ctx.items() if not k.startswith("_")})

    def run(self, ctx0, configs=None, use_cache=True, controller=None):
        ctx = dict(ctx0); chain = []
        for st in self.stages:
            # lifecycle: respect a HALT command (stage-by-stage); blocks this + downstream
            if controller is not None and controller.is_halted(st.name):
                controller.set_state(st.name, "HALTED")
                chain.append({"stage": st.name, "state": "HALTED", "ran": False, "cached": False})
                ctx["_halted_at"] = st.name
                break
            cfg = st.configure((configs or {}).get(st.name))
            in_h = self._digest(ctx)
            key = prov.stable_hash({"s": st.name, "v": st.version, "c": cfg, "i": in_h})
            if controller is not None: controller.set_state(st.name, "RUNNING")
            try:
                if use_cache and key in self.cache:
                    out = self.cache[key]; cached = True
                else:
                    out = st.run(ctx, cfg)
                    if use_cache: self.cache[key] = out
                    cached = False
            except Exception as e:
                if controller is not None: controller.set_state(st.name, "ERROR")
                chain.append({"stage": st.name, "state": "ERROR", "error": str(e), "ran": False, "cached": False})
                ctx["_error_at"] = st.name; break
            if controller is not None: controller.set_state(st.name, "READY")
            ctx.update(out)
            chain.append({"stage": st.name, "version": st.version, "config": cfg,
                          "out_hash": prov.stable_hash(out)[:16], "cached": cached,
                          "state": "READY", "ran": True})
        ctx["_provenance"] = chain
        ctx["_chain_hash"] = prov.stable_hash([c.get("out_hash", "") for c in chain])
        if controller is not None: ctx["_stage_states"] = controller.snapshot()
        return ctx

    def test_all(self):
        results = []
        for st in self.stages:
            try:
                ok, detail = st.self_test()
            except Exception as e:
                ok, detail = False, f"exception: {e}"
            results.append((st.name, ok, detail))
        return results
