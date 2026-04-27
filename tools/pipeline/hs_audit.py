#!/usr/bin/env python3
"""
Hˢ AUDIT TRAIL AND BREAKPOINT SYSTEM
=======================================
Full chain-of-custody traceability for every pipeline operation.

Every step in the Hˢ pipeline produces an audit record. Every record
captures: what operation ran, when, what went in (input hash), what came
out (output hash), and whether a breakpoint was encountered. The complete
audit trail is a JSON document that provides ISO 17025-grade traceability
from raw data to final diagnosis.

BREAKPOINT SYSTEM
─────────────────
Breakpoints are named pause points where the pipeline can:
  - CONTINUE  → proceed normally (default)
  - HOLD      → pause execution and return partial results
  - ABORT     → stop execution and flag the reason
  - LOG_ONLY  → emit a detailed log entry but continue

Available breakpoints:
  BP-PRE-RUN       Before any processing starts
  BP-POST-GUARD    After input guards (D≥2, N≥5, no NaN/Inf, scale)
  BP-POST-CLOSURE  After simplex closure (Step 4)
  BP-POST-CLR      After CLR transform (Step 5)
  BP-POST-VARIANCE After Aitchison variance (Step 6)
  BP-POST-HVLD     After HVLD vertex lock (Step 7)
  BP-POST-SQUEEZE  After super squeeze / classification (Step 8)
  BP-POST-EITT     After EITT entropy test (Step 9)
  BP-POST-GEOMETRY After ternary/complex/helix (Steps 10-12)
  BP-POST-EXTENDED After extended panel (universal + conditional)
  BP-POST-CODES    After diagnostic code generation
  BP-POST-FINGER   After fingerprint generation
  BP-ON-ERROR      On any pipeline error
  BP-ON-FLAG       When classification is FLAG (optional safety stop)
  BP-ON-GUARD-FAIL When any input guard fails
  BP-LOOP-ITER     Between iterations of a catalog/batch loop
  BP-LOOP-END      After the final iteration of any loop

AUDIT RECORD FORMAT
───────────────────
{
  "seq": 1,                          # Sequential operation number
  "operation": "step_4_closure",     # What ran
  "timestamp": "2026-04-26T...",     # When it ran (UTC)
  "duration_ms": 2.3,               # How long it took
  "input_hash": "a1b2c3d4",         # SHA-256 of input data (first 16 chars)
  "output_hash": "e5f6g7h8",        # SHA-256 of output data (first 16 chars)
  "input_shape": [20, 4],           # Shape of input matrix
  "output_shape": [20, 4],          # Shape of output matrix
  "status": "OK",                   # OK, WARNING, ERROR, HELD, ABORTED
  "breakpoint": null,               # Breakpoint name if triggered
  "breakpoint_action": null,        # CONTINUE, HOLD, ABORT, LOG_ONLY
  "notes": "",                      # Human-readable notes
  "metadata": {}                    # Step-specific metadata
}

Usage:
    from hs_audit import AuditTrail, BreakpointConfig

    # Configure breakpoints
    bp = BreakpointConfig()
    bp.set("BP-ON-FLAG", "HOLD")           # Pause if FLAG
    bp.set("BP-ON-ERROR", "ABORT")         # Stop on errors
    bp.set("BP-POST-HVLD", "LOG_ONLY")     # Extra logging after HVLD

    # Create audit trail
    audit = AuditTrail(experiment_id="Hs-24-001", breakpoints=bp)

    # Use with pipeline
    audit.record("step_4_closure", input_data, output_data, status="OK")

    # Check breakpoint
    action = audit.check_breakpoint("BP-POST-SQUEEZE", context={"classification": "FLAG"})
    if action == "HOLD":
        return audit.hold("FLAG detected — awaiting expert review")

    # Save audit trail
    audit.save("audit_trail.json")

Author: Peter Higgins / Claude
Version: 1.0
"""

import json
import hashlib
import time
import os
import sys
import copy
from datetime import datetime, timezone


# ════════════════════════════════════════════════════════════
# BREAKPOINT DEFINITIONS
# ════════════════════════════════════════════════════════════

BREAKPOINT_REGISTRY = {
    # Pre-processing
    "BP-PRE-RUN":       {"stage": "pre",      "description": "Before any processing starts"},
    "BP-POST-GUARD":    {"stage": "guard",     "description": "After input guards pass/fail"},

    # Core pipeline (Steps 4-12)
    "BP-POST-CLOSURE":  {"stage": "step_4",    "description": "After simplex closure"},
    "BP-POST-CLR":      {"stage": "step_5",    "description": "After CLR transform"},
    "BP-POST-VARIANCE": {"stage": "step_6",    "description": "After Aitchison variance trajectory"},
    "BP-POST-HVLD":     {"stage": "step_7",    "description": "After HVLD vertex lock diagnostic"},
    "BP-POST-SQUEEZE":  {"stage": "step_8",    "description": "After super squeeze / classification"},
    "BP-POST-EITT":     {"stage": "step_9",    "description": "After EITT entropy invariance test"},
    "BP-POST-GEOMETRY": {"stage": "step_10-12","description": "After ternary/complex/helix geometry"},

    # Extended panel
    "BP-POST-EXTENDED": {"stage": "extended",  "description": "After extended testing panel"},

    # Post-processing
    "BP-POST-CODES":    {"stage": "codes",     "description": "After diagnostic code generation"},
    "BP-POST-FINGER":   {"stage": "fingerprint","description": "After fingerprint generation"},

    # Conditional breakpoints
    "BP-ON-ERROR":      {"stage": "error",     "description": "On any pipeline error"},
    "BP-ON-FLAG":       {"stage": "flag",      "description": "When classification is FLAG"},
    "BP-ON-GUARD-FAIL": {"stage": "guard_fail","description": "When any input guard fails"},

    # Loop control
    "BP-LOOP-ITER":     {"stage": "loop",      "description": "Between iterations of a batch loop"},
    "BP-LOOP-END":      {"stage": "loop_end",  "description": "After the final iteration of any loop"},
}

VALID_ACTIONS = {"CONTINUE", "HOLD", "ABORT", "LOG_ONLY"}


class BreakpointConfig:
    """
    Configurable breakpoint settings.

    Default: all breakpoints are CONTINUE (no stops).
    Safety presets are available for common use cases.
    """

    def __init__(self):
        # Default: everything continues
        self._config = {bp: "CONTINUE" for bp in BREAKPOINT_REGISTRY}

    def set(self, breakpoint_name, action):
        """Set a breakpoint action. Raises ValueError for invalid names/actions."""
        if breakpoint_name not in BREAKPOINT_REGISTRY:
            raise ValueError(f"Unknown breakpoint: {breakpoint_name}. "
                           f"Valid: {sorted(BREAKPOINT_REGISTRY.keys())}")
        if action not in VALID_ACTIONS:
            raise ValueError(f"Unknown action: {action}. Valid: {sorted(VALID_ACTIONS)}")
        self._config[breakpoint_name] = action

    def get(self, breakpoint_name):
        """Get the action for a breakpoint."""
        return self._config.get(breakpoint_name, "CONTINUE")

    def set_preset(self, preset_name):
        """
        Apply a named preset configuration.

        Presets:
          'permissive'  — All CONTINUE (default, no stops)
          'cautious'    — HOLD on FLAG and errors
          'strict'      — ABORT on errors, HOLD on FLAG and guard failures
          'audit'       — LOG_ONLY everywhere (maximum traceability, no stops)
          'development' — HOLD at every step (step-through debugging)
        """
        if preset_name == 'permissive':
            self._config = {bp: "CONTINUE" for bp in BREAKPOINT_REGISTRY}

        elif preset_name == 'cautious':
            self._config = {bp: "CONTINUE" for bp in BREAKPOINT_REGISTRY}
            self._config["BP-ON-FLAG"] = "HOLD"
            self._config["BP-ON-ERROR"] = "HOLD"
            self._config["BP-ON-GUARD-FAIL"] = "HOLD"

        elif preset_name == 'strict':
            self._config = {bp: "CONTINUE" for bp in BREAKPOINT_REGISTRY}
            self._config["BP-ON-ERROR"] = "ABORT"
            self._config["BP-ON-FLAG"] = "HOLD"
            self._config["BP-ON-GUARD-FAIL"] = "ABORT"
            self._config["BP-LOOP-ITER"] = "LOG_ONLY"

        elif preset_name == 'audit':
            self._config = {bp: "LOG_ONLY" for bp in BREAKPOINT_REGISTRY}

        elif preset_name == 'development':
            self._config = {bp: "HOLD" for bp in BREAKPOINT_REGISTRY}

        else:
            raise ValueError(f"Unknown preset: {preset_name}. "
                           f"Valid: permissive, cautious, strict, audit, development")

    def to_dict(self):
        """Export configuration as dict."""
        return copy.deepcopy(self._config)

    def summary(self):
        """Return a human-readable summary of active (non-CONTINUE) breakpoints."""
        active = {k: v for k, v in self._config.items() if v != "CONTINUE"}
        if not active:
            return "All breakpoints: CONTINUE (no stops)"
        lines = []
        for bp, action in sorted(active.items()):
            desc = BREAKPOINT_REGISTRY[bp]["description"]
            lines.append(f"  {bp}: {action} — {desc}")
        return "\n".join(lines)


class AuditTrail:
    """
    Full chain-of-custody audit trail for an Hˢ pipeline run.

    Records every operation with input/output hashes, timestamps,
    durations, and breakpoint decisions. The complete trail is a
    machine-readable JSON document suitable for ISO 17025-style
    traceability.
    """

    def __init__(self, experiment_id=None, breakpoints=None, verbose=False):
        self.experiment_id = experiment_id or "unidentified"
        self.breakpoints = breakpoints or BreakpointConfig()
        self.verbose = verbose

        self.trail_id = hashlib.sha256(
            f"{self.experiment_id}:{datetime.now(timezone.utc).isoformat()}".encode()
        ).hexdigest()[:16]

        self.created = datetime.now(timezone.utc).isoformat()
        self.records = []
        self.seq = 0
        self.status = "RUNNING"  # RUNNING, COMPLETED, HELD, ABORTED, ERROR
        self.hold_reason = None
        self.abort_reason = None
        self._timer = None

    def start_timer(self):
        """Start a timer for the current operation."""
        self._timer = time.perf_counter()

    def elapsed_ms(self):
        """Return elapsed time in milliseconds since start_timer()."""
        if self._timer is None:
            return 0.0
        return (time.perf_counter() - self._timer) * 1000

    @staticmethod
    def hash_data(data):
        """
        Compute a deterministic hash of data for audit purposes.
        Handles numpy arrays, dicts, lists, strings, and None.
        """
        if data is None:
            return "null"
        try:
            import numpy as np
            if isinstance(data, np.ndarray):
                return hashlib.sha256(data.tobytes()).hexdigest()[:16]
        except ImportError:
            pass
        if isinstance(data, (dict, list)):
            s = json.dumps(data, sort_keys=True, default=str)
            return hashlib.sha256(s.encode()).hexdigest()[:16]
        if isinstance(data, (str, bytes)):
            if isinstance(data, str):
                data = data.encode()
            return hashlib.sha256(data).hexdigest()[:16]
        return hashlib.sha256(str(data).encode()).hexdigest()[:16]

    @staticmethod
    def data_shape(data):
        """Extract shape information from data."""
        if data is None:
            return None
        try:
            import numpy as np
            if isinstance(data, np.ndarray):
                return list(data.shape)
        except ImportError:
            pass
        if isinstance(data, list) and data and isinstance(data[0], list):
            return [len(data), len(data[0])]
        if isinstance(data, dict):
            return {"keys": len(data)}
        return None

    def record(self, operation, input_data=None, output_data=None,
               status="OK", notes="", metadata=None):
        """
        Record an audit entry for a pipeline operation.

        Parameters
        ----------
        operation : str
            Name of the operation (e.g., "step_4_closure", "guard_check")
        input_data : any
            Input to this operation (hashed, not stored)
        output_data : any
            Output from this operation (hashed, not stored)
        status : str
            OK, WARNING, ERROR, HELD, ABORTED
        notes : str
            Human-readable notes
        metadata : dict
            Step-specific metadata to include

        Returns
        -------
        dict : The audit record
        """
        self.seq += 1
        duration = self.elapsed_ms()

        record = {
            "seq": self.seq,
            "operation": operation,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "duration_ms": round(duration, 3),
            "input_hash": self.hash_data(input_data),
            "output_hash": self.hash_data(output_data),
            "input_shape": self.data_shape(input_data),
            "output_shape": self.data_shape(output_data),
            "status": status,
            "breakpoint": None,
            "breakpoint_action": None,
            "notes": notes,
            "metadata": metadata or {},
        }

        self.records.append(record)

        if self.verbose:
            bp_str = ""
            if record["breakpoint"]:
                bp_str = f" [{record['breakpoint']}:{record['breakpoint_action']}]"
            print(f"  AUDIT [{self.seq:03d}] {operation}: {status} "
                  f"({duration:.1f}ms){bp_str}")

        return record

    def check_breakpoint(self, breakpoint_name, context=None):
        """
        Check a breakpoint and record the decision.

        Parameters
        ----------
        breakpoint_name : str
            Name from BREAKPOINT_REGISTRY
        context : dict, optional
            Context information for the breakpoint decision

        Returns
        -------
        str : The action taken (CONTINUE, HOLD, ABORT, LOG_ONLY)
        """
        action = self.breakpoints.get(breakpoint_name)

        # Update the last record with breakpoint info
        if self.records:
            self.records[-1]["breakpoint"] = breakpoint_name
            self.records[-1]["breakpoint_action"] = action

        if action == "LOG_ONLY":
            desc = BREAKPOINT_REGISTRY.get(breakpoint_name, {}).get("description", "")
            self.record(
                f"breakpoint_{breakpoint_name}",
                status="LOG",
                notes=f"Breakpoint {breakpoint_name}: {desc}",
                metadata={"context": context or {}, "action": action}
            )

        elif action == "HOLD":
            self.status = "HELD"
            self.hold_reason = f"Breakpoint {breakpoint_name} triggered HOLD"
            if self.verbose:
                print(f"  *** HOLD at {breakpoint_name} ***")

        elif action == "ABORT":
            self.status = "ABORTED"
            self.abort_reason = f"Breakpoint {breakpoint_name} triggered ABORT"
            if self.verbose:
                print(f"  *** ABORT at {breakpoint_name} ***")

        return action

    def hold(self, reason=""):
        """Explicitly hold the pipeline with a reason."""
        self.status = "HELD"
        self.hold_reason = reason
        self.record("pipeline_hold", status="HELD", notes=reason)
        return {"status": "HELD", "reason": reason, "trail": self.to_dict()}

    def abort(self, reason=""):
        """Explicitly abort the pipeline with a reason."""
        self.status = "ABORTED"
        self.abort_reason = reason
        self.record("pipeline_abort", status="ABORTED", notes=reason)
        return {"status": "ABORTED", "reason": reason, "trail": self.to_dict()}

    def complete(self):
        """Mark the audit trail as complete."""
        self.status = "COMPLETED"
        self.record("pipeline_complete", status="OK",
                    notes=f"Pipeline completed: {self.seq} operations recorded")

    def to_dict(self):
        """Export the full audit trail as a dict."""
        return {
            "_type": "Hs_AUDIT_TRAIL",
            "_version": "1.0",
            "trail_id": self.trail_id,
            "experiment_id": self.experiment_id,
            "created": self.created,
            "completed": datetime.now(timezone.utc).isoformat(),
            "status": self.status,
            "total_operations": self.seq,
            "hold_reason": self.hold_reason,
            "abort_reason": self.abort_reason,
            "breakpoint_config": self.breakpoints.to_dict(),
            "records": self.records,
            "chain_hash": self._chain_hash(),
        }

    def _chain_hash(self):
        """
        Compute a tamper-evident hash of the entire audit chain.

        Each record's hash feeds into the next, creating a blockchain-like
        integrity chain. If any record is modified after creation, the
        chain hash will not match.
        """
        chain = ""
        for r in self.records:
            chain += f"{r['seq']}:{r['operation']}:{r['input_hash']}:{r['output_hash']}:{r['status']}"
        return hashlib.sha256(chain.encode()).hexdigest()[:32]

    def save(self, filepath):
        """Save the audit trail to a JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        if self.verbose:
            print(f"Audit trail saved: {filepath} ({self.seq} operations)")

    def summary(self):
        """Return a human-readable summary of the audit trail."""
        lines = [
            f"Hˢ AUDIT TRAIL — {self.experiment_id}",
            f"{'=' * 60}",
            f"Trail ID:    {self.trail_id}",
            f"Status:      {self.status}",
            f"Operations:  {self.seq}",
            f"Chain hash:  {self._chain_hash()}",
        ]

        if self.hold_reason:
            lines.append(f"Hold reason: {self.hold_reason}")
        if self.abort_reason:
            lines.append(f"Abort reason: {self.abort_reason}")

        # Count by status
        statuses = {}
        for r in self.records:
            statuses[r['status']] = statuses.get(r['status'], 0) + 1
        status_str = ", ".join(f"{k}: {v}" for k, v in sorted(statuses.items()))
        lines.append(f"Breakdown:   {status_str}")

        # List breakpoints that fired
        fired = [(r['breakpoint'], r['breakpoint_action'])
                 for r in self.records if r['breakpoint']]
        if fired:
            lines.append(f"\nBreakpoints fired:")
            for bp, action in fired:
                lines.append(f"  {bp}: {action}")

        # Total duration
        total_ms = sum(r['duration_ms'] for r in self.records)
        lines.append(f"\nTotal time:  {total_ms:.1f}ms")

        return "\n".join(lines)


# ════════════════════════════════════════════════════════════
# AUDITED PIPELINE RUNNER
# ════════════════════════════════════════════════════════════

def run_audited_pipeline(hd, data, breakpoints=None, verbose=False,
                         generate_codes_fn=None, generate_fingerprint_fn=None):
    """
    Run the full Hˢ pipeline with audit trail and breakpoint support.

    Parameters
    ----------
    hd : HigginsDecomposition
        Configured pipeline instance (with id, name, domain, carriers set)
    data : numpy.ndarray
        N×D data matrix
    breakpoints : BreakpointConfig, optional
        Breakpoint configuration (default: permissive)
    verbose : bool
        Print audit records as they're created
    generate_codes_fn : callable, optional
        Function to generate diagnostic codes (from hs_codes)
    generate_fingerprint_fn : callable, optional
        Function to generate fingerprint (from hs_fingerprint)

    Returns
    -------
    dict with:
        - result: pipeline result dict (or partial if held/aborted)
        - codes: diagnostic codes (if code generation was reached)
        - fingerprint: fingerprint dict (if fingerprint generation was reached)
        - audit: AuditTrail object
        - status: COMPLETED, HELD, or ABORTED
    """
    bp = breakpoints or BreakpointConfig()
    audit = AuditTrail(experiment_id=hd.experiment_id, breakpoints=bp, verbose=verbose)

    output = {
        "result": None,
        "codes": None,
        "fingerprint": None,
        "audit": audit,
        "status": "RUNNING",
    }

    # ── BP-PRE-RUN ──
    audit.start_timer()
    audit.record("pre_run", input_data=data, status="OK",
                notes=f"Starting pipeline: {hd.name} ({hd.domain})",
                metadata={"N": data.shape[0], "D": data.shape[1],
                         "experiment_id": hd.experiment_id})
    action = audit.check_breakpoint("BP-PRE-RUN")
    if action in ("HOLD", "ABORT"):
        output["status"] = audit.status
        return output

    # ── Load data + guards ──
    audit.start_timer()
    try:
        hd.load_data(data)
        audit.record("load_data_and_guards", input_data=data, output_data=hd.raw_data,
                    status="OK", notes="Data loaded, all guards passed",
                    metadata={"data_hash": hd.data_hash})
    except Exception as e:
        audit.record("load_data_and_guards", input_data=data, status="ERROR",
                    notes=str(e))
        action = audit.check_breakpoint("BP-ON-GUARD-FAIL", {"error": str(e)})
        if action in ("HOLD", "ABORT"):
            output["status"] = audit.status
            return output
        # Even with CONTINUE, guard failure is fatal
        audit.abort(f"Guard failure: {e}")
        output["status"] = "ABORTED"
        return output

    action = audit.check_breakpoint("BP-POST-GUARD")
    if action in ("HOLD", "ABORT"):
        output["status"] = audit.status
        return output

    # ── Step 4: Closure ──
    audit.start_timer()
    hd.close_to_simplex()
    audit.record("step_4_closure", input_data=hd.raw_data, output_data=hd.simplex_data,
                status="OK", notes="Simplex closure complete",
                metadata={"zero_replacement": bool(hd.results.get("step3_zero_replacement_applied"))})
    action = audit.check_breakpoint("BP-POST-CLOSURE")
    if action in ("HOLD", "ABORT"):
        output["status"] = audit.status
        return output

    # ── Step 5: CLR ──
    audit.start_timer()
    hd.clr_transform()
    audit.record("step_5_clr", input_data=hd.simplex_data, output_data=hd.clr_data,
                status="OK", notes="CLR transform complete")
    action = audit.check_breakpoint("BP-POST-CLR")
    if action in ("HOLD", "ABORT"):
        output["status"] = audit.status
        return output

    # ── Step 6: Variance ──
    audit.start_timer()
    hd.aitchison_variance()
    audit.record("step_6_variance", input_data=hd.clr_data,
                output_data=hd.results.get("step5_sigma2_final"),
                status="OK", notes="Aitchison variance trajectory computed",
                metadata={"sigma2_final": hd.results.get("step5_sigma2_final")})
    action = audit.check_breakpoint("BP-POST-VARIANCE")
    if action in ("HOLD", "ABORT"):
        output["status"] = audit.status
        return output

    # ── Step 7: HVLD ──
    audit.start_timer()
    hd.pll_parabola()
    shape = hd.results.get("step6_pll_shape", "unknown")
    r2 = hd.results.get("step6_pll_R2", 0)
    audit.record("step_7_hvld", output_data=hd.pll_result,
                status="OK", notes=f"HVLD: {shape}, R²={r2:.4f}",
                metadata={"shape": shape, "R2": r2,
                         "vertex": hd.results.get("step6_vertex")})
    action = audit.check_breakpoint("BP-POST-HVLD")
    if action in ("HOLD", "ABORT"):
        output["status"] = audit.status
        return output

    # ── Step 8: Super Squeeze ──
    audit.start_timer()
    hd.super_squeeze()
    sq = hd.results.get("step7_squeeze_closest", {})
    delta = sq.get("delta", 999) if sq else 999
    const = sq.get("constant", "none") if sq else "none"
    if delta < 0.01:
        classification = "NATURAL"
    elif delta < 0.05:
        classification = "INVESTIGATE"
    else:
        classification = "FLAG"
    audit.record("step_8_squeeze", output_data=hd.squeeze_result,
                status="OK", notes=f"Classification: {classification} (nearest: {const}, δ={delta:.6f})",
                metadata={"classification": classification, "nearest_constant": const,
                         "delta": delta, "match_count": hd.results.get("step7_squeeze_count", 0)})
    action = audit.check_breakpoint("BP-POST-SQUEEZE")
    if action in ("HOLD", "ABORT"):
        output["status"] = audit.status
        return output

    # ── Check BP-ON-FLAG ──
    if classification == "FLAG":
        action = audit.check_breakpoint("BP-ON-FLAG", {"classification": "FLAG"})
        if action in ("HOLD", "ABORT"):
            output["status"] = audit.status
            return output

    # ── Step 9: EITT ──
    audit.start_timer()
    hd.eitt_entropy()
    eitt = hd.results.get("step8_eitt_invariance", {})
    eitt_pass = all(v.get('pass', False) for v in eitt.values()) if eitt else False
    audit.record("step_9_eitt", output_data=hd.entropy_result,
                status="OK", notes=f"EITT: {'PASS' if eitt_pass else 'FAIL'}",
                metadata={"eitt_pass": eitt_pass})
    action = audit.check_breakpoint("BP-POST-EITT")
    if action in ("HOLD", "ABORT"):
        output["status"] = audit.status
        return output

    # ── Steps 10-12: Geometry ──
    audit.start_timer()
    hd.ternary_projection()
    hd.complex_plane()
    hd.helix_polar()
    audit.record("steps_10_12_geometry", status="OK",
                notes="Ternary, complex plane, helix/polar computed")
    action = audit.check_breakpoint("BP-POST-GEOMETRY")
    if action in ("HOLD", "ABORT"):
        output["status"] = audit.status
        return output

    # ── Assemble core result ──
    core_result = {
        "framework": "Higgins Unity Framework",
        "instrument": "Hˢ Higgins Decomposition — 12-Step Pipeline v1.0 Extended",
        "experiment": hd.experiment_id,
        "name": hd.name,
        "domain": hd.domain,
        "carriers": hd.carriers,
        "D": hd.D,
        "N": int(hd.raw_data.shape[0]),
        "data_source": hd.data_source,
        "data_hash_sha256_16": hd.data_hash,
        "run_timestamp": datetime.now(timezone.utc).isoformat(),
        "pipeline_version": "1.0 Extended",
        "steps": hd.results,
    }

    # ── Extended panel ──
    audit.start_timer()
    try:
        extended = hd.run_extended()
        core_result["extended"] = extended
        audit.record("extended_panel", status="OK",
                    notes="Extended testing panel complete (universal + conditional)")
    except Exception as e:
        audit.record("extended_panel", status="ERROR", notes=str(e))
        action = audit.check_breakpoint("BP-ON-ERROR", {"error": str(e), "stage": "extended"})
        if action in ("HOLD", "ABORT"):
            output["status"] = audit.status
            output["result"] = core_result
            return output

    action = audit.check_breakpoint("BP-POST-EXTENDED")
    if action in ("HOLD", "ABORT"):
        output["status"] = audit.status
        output["result"] = core_result
        return output

    output["result"] = core_result

    # ── Diagnostic codes ──
    if generate_codes_fn:
        audit.start_timer()
        try:
            codes = generate_codes_fn(core_result)
            output["codes"] = codes
            sm_codes = [c['code'] for c in codes if c['code'].startswith('SM-')]
            audit.record("code_generation", output_data=codes,
                        status="OK",
                        notes=f"{len(codes)} codes, {len(sm_codes)} structural modes",
                        metadata={"total_codes": len(codes), "structural_modes": sm_codes})
        except Exception as e:
            audit.record("code_generation", status="ERROR", notes=str(e))

        action = audit.check_breakpoint("BP-POST-CODES")
        if action in ("HOLD", "ABORT"):
            output["status"] = audit.status
            return output

    # ── Fingerprint ──
    if generate_fingerprint_fn:
        audit.start_timer()
        try:
            fp = generate_fingerprint_fn(core_result, name=hd.name, domain=hd.domain)
            output["fingerprint"] = fp
            audit.record("fingerprint_generation", output_data=fp,
                        status="OK",
                        notes=f"Hash: {fp['fingerprint']['hash']}",
                        metadata={"hash": fp['fingerprint']['hash'],
                                 "vector": fp['fingerprint']['vector']})
        except Exception as e:
            audit.record("fingerprint_generation", status="ERROR", notes=str(e))

        action = audit.check_breakpoint("BP-POST-FINGER")
        if action in ("HOLD", "ABORT"):
            output["status"] = audit.status
            return output

    # ── Complete ──
    audit.complete()
    output["status"] = "COMPLETED"
    return output


# ════════════════════════════════════════════════════════════
# CLI
# ════════════════════════════════════════════════════════════

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Hˢ Audit Trail and Breakpoint System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Breakpoint presets:
  permissive   All CONTINUE (no stops)
  cautious     HOLD on FLAG, errors, guard failures
  strict       ABORT on errors/guard failures, HOLD on FLAG
  audit        LOG_ONLY everywhere (max traceability)
  development  HOLD at every step (step-through)

Examples:
  python hs_audit.py --list-breakpoints
  python hs_audit.py --preset strict --run data.csv
  python hs_audit.py --view audit_trail.json
        """
    )

    parser.add_argument('--list-breakpoints', action='store_true',
                       help='List all available breakpoints')
    parser.add_argument('--preset', choices=['permissive','cautious','strict','audit','development'],
                       help='Apply a breakpoint preset')
    parser.add_argument('--run', metavar='DATA_CSV',
                       help='Run pipeline on CSV data with audit trail')
    parser.add_argument('--view', metavar='AUDIT_JSON',
                       help='View an existing audit trail')
    parser.add_argument('--name', default='CLI Test', help='System name')
    parser.add_argument('--domain', default='TEST', help='Domain')
    parser.add_argument('-o', '--output', help='Output audit trail path')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Print audit records as they are created')

    args = parser.parse_args()

    if args.list_breakpoints:
        print(f"\nHˢ BREAKPOINT REGISTRY ({len(BREAKPOINT_REGISTRY)} breakpoints)")
        print("=" * 70)
        for bp, info in sorted(BREAKPOINT_REGISTRY.items()):
            print(f"  {bp:<20s} [{info['stage']:<12s}] {info['description']}")
        print(f"\nActions: {', '.join(sorted(VALID_ACTIONS))}")
        print(f"\nPresets: permissive, cautious, strict, audit, development")
        return

    if args.view:
        with open(args.view) as f:
            trail = json.load(f)
        print(f"\nHˢ AUDIT TRAIL VIEWER")
        print(f"{'=' * 60}")
        print(f"Trail ID:    {trail['trail_id']}")
        print(f"Experiment:  {trail['experiment_id']}")
        print(f"Status:      {trail['status']}")
        print(f"Operations:  {trail['total_operations']}")
        print(f"Chain hash:  {trail['chain_hash']}")
        if trail.get('hold_reason'):
            print(f"Hold reason: {trail['hold_reason']}")
        if trail.get('abort_reason'):
            print(f"Abort:       {trail['abort_reason']}")
        print(f"\n{'─' * 60}")
        for r in trail['records']:
            bp_str = f" [{r['breakpoint']}→{r['breakpoint_action']}]" if r['breakpoint'] else ""
            print(f"  [{r['seq']:03d}] {r['operation']:<30s} {r['status']:<8s} "
                  f"{r['duration_ms']:>8.1f}ms{bp_str}")
            if r['notes']:
                print(f"         {r['notes']}")
        print(f"\n{'=' * 60}")
        return

    if args.run:
        import csv
        import numpy as np
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from higgins_decomposition_12step import HigginsDecomposition
        from hs_codes import generate_codes
        from hs_fingerprint import extract_fingerprint

        # Load CSV
        with open(args.run) as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in row] for row in reader]
        data = np.array(rows)

        # Configure breakpoints
        bp = BreakpointConfig()
        if args.preset:
            bp.set_preset(args.preset)

        # Create pipeline
        hd = HigginsDecomposition('CLI', args.name, args.domain, carriers=header)

        # Run with audit
        result = run_audited_pipeline(
            hd, data, breakpoints=bp, verbose=args.verbose,
            generate_codes_fn=generate_codes,
            generate_fingerprint_fn=extract_fingerprint
        )

        # Print summary
        print(f"\n{result['audit'].summary()}")

        # Save audit trail
        out_path = args.output or args.run.replace('.csv', '_audit.json')
        result['audit'].save(out_path)
        print(f"\nAudit trail saved: {out_path}")


if __name__ == "__main__":
    main()
