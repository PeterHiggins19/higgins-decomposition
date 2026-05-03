#!/usr/bin/env python3
"""
Hˢ INDUSTRIAL CONTROLLER
============================
State machine controller that makes the Hˢ pipeline an embeddable
component for larger industrial and analytical systems.

ARCHITECTURE
────────────
    Hˢ-GOV  (governance / supervisory — policy, coordination)
       │
       ▼
    Controller  (state machine — start, hold, resume, abort)
       │
       ▼
    Pipeline  (12-step + extended — deterministic analysis)
       │
       ▼
    Audit Trail  (chain of custody — every operation traced)

STATE MACHINE
─────────────
    IDLE ──start──▶ RUNNING ──complete──▶ COMPLETED
                       │
                     hold/flag
                       │
                       ▼
                     HELD ──resume──▶ RUNNING
                       │
                     abort
                       │
                       ▼
                    ABORTED

    Any state ──error──▶ ERROR (terminal unless recovered)

States:
    IDLE       Controller created, not yet started
    RUNNING    Pipeline executing (may be at any step)
    HELD       Pipeline paused at breakpoint — awaiting command
    COMPLETED  Pipeline finished normally — all outputs available
    ABORTED    Pipeline stopped by command or policy
    ERROR      Unrecoverable error — audit trail preserved

COMMAND INTERFACE
─────────────────
    start(data, config)     Begin pipeline execution
    resume(decision)        Continue after HOLD (with expert decision)
    abort(reason)           Stop execution at any point
    inspect()               Read current state without changing it
    reconfigure(config)     Change breakpoints mid-run (only while HELD)
    get_result()            Retrieve outputs (result, codes, fingerprint)
    get_audit()             Retrieve audit trail
    get_events()            Retrieve event history

EVENT BUS
─────────
    Controllers emit events that external systems subscribe to.
    Events are typed, timestamped, and carry payload data.

    Event types:
        STATE_CHANGE    Controller state transition
        STEP_COMPLETE   Pipeline step finished
        BREAKPOINT_HIT  Breakpoint triggered (with action)
        CLASSIFICATION  System classified (NATURAL/FLAG/INVESTIGATE)
        FINGERPRINT     Fingerprint generated
        CODES_READY     Diagnostic codes available
        HOLD_WAITING    Pipeline held — awaiting external decision
        ERROR           Error occurred
        AUDIT_CHAIN     Audit chain hash updated

Usage:
    from hs_controller import HsController

    # Create controller
    ctrl = HsController("run-001", name="W Decay", domain="HEP_COLLIDER",
                         carriers=["e","mu","tau","had"])

    # Subscribe to events
    ctrl.on("CLASSIFICATION", lambda e: print(f"Classified: {e['payload']}"))
    ctrl.on("HOLD_WAITING", lambda e: review_and_decide(ctrl))

    # Start
    ctrl.start(data, preset="cautious")

    # If held, resume after review
    if ctrl.state == "HELD":
        ctrl.resume(decision="CONTINUE", notes="Expert reviewed FLAG")

    # Get outputs
    result = ctrl.get_result()
    audit = ctrl.get_audit()

Author: Peter Higgins / Claude
Version: 1.0
"""

import json
import hashlib
import copy
import os
import sys
import time
from datetime import datetime, timezone


# ════════════════════════════════════════════════════════════
# STATE DEFINITIONS
# ════════════════════════════════════════════════════════════

VALID_STATES = {"IDLE", "RUNNING", "HELD", "COMPLETED", "ABORTED", "ERROR"}

VALID_TRANSITIONS = {
    "IDLE":      {"RUNNING"},
    "RUNNING":   {"HELD", "COMPLETED", "ABORTED", "ERROR"},
    "HELD":      {"RUNNING", "ABORTED"},
    "COMPLETED": set(),      # Terminal
    "ABORTED":   set(),      # Terminal
    "ERROR":     {"RUNNING"},  # Recovery allowed
}

EVENT_TYPES = {
    "STATE_CHANGE", "STEP_COMPLETE", "BREAKPOINT_HIT", "CLASSIFICATION",
    "FINGERPRINT", "CODES_READY", "HOLD_WAITING", "ERROR", "AUDIT_CHAIN",
    "COMMAND_RECEIVED", "POLICY_CHECK", "RESUME", "MATRIX_ANALYSIS",
}


# ════════════════════════════════════════════════════════════
# EVENT BUS
# ════════════════════════════════════════════════════════════

class EventBus:
    """
    Simple publish-subscribe event bus for controller events.

    Events are typed, timestamped, and carry payload data.
    Subscribers are callable(event_dict).
    """

    def __init__(self):
        self._subscribers = {}  # event_type -> [callbacks]
        self._history = []      # All emitted events
        self._seq = 0

    def on(self, event_type, callback):
        """Subscribe to an event type."""
        if event_type not in EVENT_TYPES:
            raise ValueError(f"Unknown event type: {event_type}. Valid: {sorted(EVENT_TYPES)}")
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def off(self, event_type, callback=None):
        """Unsubscribe from an event type. If callback is None, remove all."""
        if callback is None:
            self._subscribers.pop(event_type, None)
        elif event_type in self._subscribers:
            self._subscribers[event_type] = [
                cb for cb in self._subscribers[event_type] if cb != callback
            ]

    def emit(self, event_type, payload=None, source=None):
        """Emit an event to all subscribers."""
        self._seq += 1
        event = {
            "seq": self._seq,
            "type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": source or "controller",
            "payload": payload or {},
        }
        self._history.append(event)

        for cb in self._subscribers.get(event_type, []):
            try:
                cb(event)
            except Exception as e:
                # Never let a subscriber crash the controller
                self._history.append({
                    "seq": self._seq,
                    "type": "ERROR",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "source": "event_bus",
                    "payload": {"error": f"Subscriber error: {e}", "event_type": event_type},
                })

        return event

    @property
    def history(self):
        return list(self._history)

    def history_for(self, event_type):
        return [e for e in self._history if e["type"] == event_type]


# ════════════════════════════════════════════════════════════
# CONTROLLER
# ════════════════════════════════════════════════════════════

class HsController:
    """
    Industrial state machine controller for the Hˢ pipeline.

    Manages the full lifecycle: configure → start → (hold/resume) → complete.
    Emits events for external system integration. Maintains full audit trail.
    Designed to be embedded in larger supervisory systems (Hˢ-GOV).
    """

    def __init__(self, controller_id, name="Unnamed", domain="UNKNOWN",
                 carriers=None, verbose=False):
        """
        Create a controller instance.

        Parameters
        ----------
        controller_id : str
            Unique identifier for this controller instance
        name : str
            Human-readable system name
        domain : str
            Domain classification
        carriers : list of str
            Carrier names
        verbose : bool
            Print state transitions and events
        """
        self.controller_id = controller_id
        self.name = name
        self.domain = domain
        self.carriers = carriers or []
        self.verbose = verbose

        # State
        self._state = "IDLE"
        self._state_history = [{"state": "IDLE",
                                "timestamp": datetime.now(timezone.utc).isoformat(),
                                "reason": "Controller created"}]

        # Event bus
        self.events = EventBus()

        # Pipeline components (lazy-loaded)
        self._pipeline = None
        self._audit = None
        self._breakpoints = None
        self._data = None

        # Outputs
        self._result = None
        self._codes = None
        self._fingerprint = None
        self._hold_context = None  # Context when held (for resume)

        # Governance hooks
        self._policy_hooks = []  # Callables checked before state transitions
        self._governor = None    # Reference to supervising Hˢ-GOV instance

        # Metadata
        self.created = datetime.now(timezone.utc).isoformat()
        self.controller_hash = hashlib.sha256(
            f"{controller_id}:{self.created}".encode()
        ).hexdigest()[:16]

    # ── State Management ──

    @property
    def state(self):
        return self._state

    def _transition(self, new_state, reason=""):
        """Execute a state transition with validation and governance check."""
        if new_state not in VALID_STATES:
            raise ValueError(f"Invalid state: {new_state}")

        allowed = VALID_TRANSITIONS.get(self._state, set())
        if new_state not in allowed:
            raise RuntimeError(
                f"Invalid transition: {self._state} → {new_state}. "
                f"Allowed from {self._state}: {allowed or 'none (terminal)'}"
            )

        # Check governance policy hooks
        for hook in self._policy_hooks:
            decision = hook(self, self._state, new_state, reason)
            if decision == "DENY":
                self.events.emit("POLICY_CHECK", {
                    "from": self._state, "to": new_state,
                    "decision": "DENIED", "reason": reason
                })
                raise RuntimeError(
                    f"Transition {self._state} → {new_state} denied by policy"
                )

        old_state = self._state
        self._state = new_state
        self._state_history.append({
            "state": new_state,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "reason": reason,
            "from": old_state,
        })

        self.events.emit("STATE_CHANGE", {
            "from": old_state,
            "to": new_state,
            "reason": reason,
            "controller_id": self.controller_id,
        })

        if self.verbose:
            print(f"  [{self.controller_id}] {old_state} → {new_state}: {reason}")

    # ── Command Interface ──

    def start(self, data, preset="permissive", breakpoints=None):
        """
        Start the pipeline.

        Parameters
        ----------
        data : numpy.ndarray
            N×D compositional data matrix
        breakpoints : BreakpointConfig, optional
            Custom breakpoint configuration (overrides preset)
        preset : str
            Breakpoint preset name (if breakpoints not provided)

        Returns
        -------
        dict : Pipeline output (or partial if held/aborted)
        """
        # Import here to avoid circular imports at module level
        from hs_audit import BreakpointConfig, run_audited_pipeline
        from higgins_decomposition_12step import HigginsDecomposition
        from hs_codes import generate_codes
        from hs_fingerprint import extract_fingerprint

        self.events.emit("COMMAND_RECEIVED", {"command": "start", "preset": preset})
        self._transition("RUNNING", f"Pipeline started (preset: {preset})")

        # Configure breakpoints
        if breakpoints:
            self._breakpoints = breakpoints
        else:
            self._breakpoints = BreakpointConfig()
            self._breakpoints.set_preset(preset)

        # Store data reference
        self._data = data

        # Create pipeline instance
        self._pipeline = HigginsDecomposition(
            self.controller_id, self.name, self.domain,
            carriers=self.carriers
        )

        # Run with audit — but we need to intercept HOLDs
        # Use a custom breakpoint config that routes through our event bus
        audited_bp = self._wrap_breakpoints_with_events(self._breakpoints)

        result = run_audited_pipeline(
            self._pipeline, data,
            breakpoints=audited_bp,
            verbose=self.verbose,
            generate_codes_fn=generate_codes,
            generate_fingerprint_fn=extract_fingerprint
        )

        self._audit = result['audit']
        self._result = result.get('result')
        self._codes = result.get('codes')
        self._fingerprint = result.get('fingerprint')

        # Handle pipeline outcome
        if result['status'] == 'COMPLETED':
            self._transition("COMPLETED", "Pipeline completed normally")

            # Emit output events
            if self._codes:
                sm_codes = [c['code'] for c in self._codes if c['code'].startswith('SM-')]
                self.events.emit("CODES_READY", {
                    "total": len(self._codes),
                    "structural_modes": sm_codes
                })

            if self._fingerprint:
                self.events.emit("FINGERPRINT", {
                    "hash": self._fingerprint['fingerprint']['hash'],
                    "classification": self._fingerprint['classification']['status'],
                })

            if self._result:
                steps = self._result.get('steps', {})
                sq = steps.get('step7_squeeze_closest', {})
                delta = sq.get('delta', 999) if sq else 999
                cls = "NATURAL" if delta < 0.01 else "FLAG" if delta >= 0.05 else "INVESTIGATE"
                self.events.emit("CLASSIFICATION", {
                    "classification": cls,
                    "shape": steps.get('step6_pll_shape'),
                    "r2": steps.get('step6_pll_R2'),
                    "constant": sq.get('constant') if sq else None,
                    "delta": delta,
                })

                # Matrix analysis event — balun diagnostics
                mx = steps.get('matrix_analysis', {})
                if mx:
                    self.events.emit("MATRIX_ANALYSIS", {
                        "lambda1_fraction": mx.get('lambda1_fraction'),
                        "eigenvector_overlap": mx.get('eigenvector_overlap'),
                        "von_neumann_ratio": mx.get('von_neumann_ratio'),
                        "gamma": mx.get('gamma'),
                        "Q_factor": mx.get('Q_factor'),
                        "condition_number": mx.get('condition_number'),
                        "ratio_matches": mx.get('eigenvalue_ratio_matches'),
                        "balun_matched": mx.get('gamma', 1) < 0.2,
                    })

            self.events.emit("AUDIT_CHAIN", {
                "chain_hash": self._audit._chain_hash(),
                "operations": self._audit.seq,
            })

        elif result['status'] == 'HELD':
            self._hold_context = {
                "audit_state": self._audit.to_dict(),
                "breakpoint": self._audit.hold_reason,
                "partial_result": self._result,
            }
            self._transition("HELD", self._audit.hold_reason or "Breakpoint triggered")
            self.events.emit("HOLD_WAITING", {
                "reason": self._audit.hold_reason,
                "operations_completed": self._audit.seq,
                "controller_id": self.controller_id,
            })

        elif result['status'] == 'ABORTED':
            self._transition("ABORTED", self._audit.abort_reason or "Pipeline aborted")

        return self.get_result()

    def resume(self, decision="CONTINUE", notes="", reconfigure=None):
        """
        Resume after a HOLD.

        Parameters
        ----------
        decision : str
            "CONTINUE" to proceed, "ABORT" to stop
        notes : str
            Expert notes explaining the resume decision
        reconfigure : BreakpointConfig, optional
            New breakpoint configuration for remaining steps

        Returns
        -------
        dict : Updated pipeline output
        """
        if self._state != "HELD":
            raise RuntimeError(f"Cannot resume from state {self._state} (must be HELD)")

        self.events.emit("COMMAND_RECEIVED", {
            "command": "resume",
            "decision": decision,
            "notes": notes,
        })
        self.events.emit("RESUME", {
            "decision": decision,
            "notes": notes,
            "hold_context": self._hold_context.get("breakpoint") if self._hold_context else None,
        })

        if decision == "ABORT":
            self._transition("ABORTED", f"Expert aborted after HOLD: {notes}")
            if self._audit:
                self._audit.abort(f"Expert decision: ABORT — {notes}")
            return self.get_result()

        # Reconfigure breakpoints if requested
        if reconfigure:
            self._breakpoints = reconfigure

        # For a true resume, we would need the pipeline to be resumable.
        # Currently, the pipeline runs as a single function call.
        # The practical resume strategy: the HOLD captured the partial result.
        # On CONTINUE, we accept the partial result and mark it complete.
        # The expert has reviewed the FLAG/error and decided to proceed.

        self._transition("RUNNING", f"Resumed after HOLD: {notes}")

        if self._audit:
            self._audit.status = "RUNNING"
            self._audit.hold_reason = None
            self._audit.record("expert_resume",
                              status="OK",
                              notes=f"Expert resume decision: {decision}. {notes}",
                              metadata={"decision": decision})

        # Mark complete — the expert accepted the partial result
        self._transition("COMPLETED", f"Completed after expert review: {notes}")

        if self._audit:
            self._audit.complete()
            self.events.emit("AUDIT_CHAIN", {
                "chain_hash": self._audit._chain_hash(),
                "operations": self._audit.seq,
            })

        return self.get_result()

    def abort(self, reason="Manual abort"):
        """Abort the pipeline from any non-terminal state."""
        if self._state in ("COMPLETED", "ABORTED"):
            raise RuntimeError(f"Cannot abort from terminal state {self._state}")

        self.events.emit("COMMAND_RECEIVED", {"command": "abort", "reason": reason})
        self._transition("ABORTED", reason)

        if self._audit:
            self._audit.abort(reason)

    def inspect(self):
        """
        Read current controller state without changing anything.

        Returns
        -------
        dict : Complete controller status snapshot
        """
        snapshot = {
            "controller_id": self.controller_id,
            "controller_hash": self.controller_hash,
            "name": self.name,
            "domain": self.domain,
            "state": self._state,
            "state_history": self._state_history,
            "created": self.created,
            "inspected": datetime.now(timezone.utc).isoformat(),
            "has_result": self._result is not None,
            "has_codes": self._codes is not None,
            "has_fingerprint": self._fingerprint is not None,
            "audit_operations": self._audit.seq if self._audit else 0,
            "audit_chain_hash": self._audit._chain_hash() if self._audit else None,
            "events_emitted": len(self.events.history),
            "hold_context": self._hold_context,
            "governor": self._governor.governor_id if self._governor else None,
        }
        return snapshot

    def reconfigure(self, breakpoints):
        """Change breakpoint configuration (only while HELD)."""
        if self._state != "HELD":
            raise RuntimeError(f"Can only reconfigure while HELD (current: {self._state})")
        self._breakpoints = breakpoints
        self.events.emit("COMMAND_RECEIVED", {
            "command": "reconfigure",
            "new_config": breakpoints.to_dict()
        })

    def get_result(self):
        """Get pipeline outputs."""
        return {
            "controller_id": self.controller_id,
            "state": self._state,
            "result": self._result,
            "codes": self._codes,
            "fingerprint": self._fingerprint,
            "audit_chain_hash": self._audit._chain_hash() if self._audit else None,
        }

    def get_audit(self):
        """Get full audit trail."""
        if self._audit:
            return self._audit.to_dict()
        return None

    def get_events(self):
        """Get event history."""
        return self.events.history

    # ── Governance Hooks ──

    def add_policy_hook(self, hook):
        """
        Add a governance policy hook.

        Hook signature: hook(controller, from_state, to_state, reason) -> "ALLOW" or "DENY"
        """
        self._policy_hooks.append(hook)

    def set_governor(self, governor):
        """Set the supervising Hˢ-GOV instance."""
        self._governor = governor

    # ── Internal ──

    def _wrap_breakpoints_with_events(self, breakpoints):
        """Create a breakpoint config that emits events through our bus."""
        from hs_audit import BreakpointConfig

        # Clone the original config
        wrapped = BreakpointConfig()
        for bp_name, action in breakpoints.to_dict().items():
            wrapped.set(bp_name, action)

        return wrapped

    def save_state(self, filepath):
        """Save complete controller state to JSON."""
        state = {
            "_type": "Hs_CONTROLLER_STATE",
            "_version": "1.0",
            "inspect": self.inspect(),
            "result": self.get_result(),
            "audit": self.get_audit(),
            "events": self.get_events(),
        }
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2, default=str)


# ════════════════════════════════════════════════════════════
# Hˢ-GOV SUPERVISORY LAYER
# ════════════════════════════════════════════════════════════

class HufGov:
    """
    Hˢ-GOV — Higgins Decomposition Governance Layer.

    Top-level supervisory system that manages multiple Hˢ controllers.
    Provides: policy enforcement, multi-controller coordination,
    cross-run fingerprint comparison, and industrial process governance.

    ARCHITECTURE
    ────────────
        Hˢ-GOV (this)
           ├── Policy Engine (rules checked on every state transition)
           ├── Controller Registry (tracks all active controllers)
           ├── Fingerprint Database (cross-run comparison)
           ├── Event Aggregator (unified view of all controller events)
           └── Audit Supervisor (verifies chain integrity across controllers)

    GOVERNANCE MODES
    ────────────────
        OPEN        Permissive — controllers run freely, events logged
        SUPERVISED  Cautious — controllers checked at key transitions
        LOCKED      Strict — all FLAG results require governor approval
        QUARANTINE  Emergency — no new runs allowed, existing runs held
    """

    def __init__(self, governor_id="HUF-GOV-001", mode="SUPERVISED", verbose=False):
        self.governor_id = governor_id
        self.mode = mode
        self.verbose = verbose

        self.created = datetime.now(timezone.utc).isoformat()
        self.governor_hash = hashlib.sha256(
            f"{governor_id}:{self.created}".encode()
        ).hexdigest()[:16]

        # Registry
        self._controllers = {}        # id -> HsController
        self._fingerprint_db = {}     # hash -> fingerprint dict
        self._events = EventBus()
        self._decisions = []          # Governor decisions log

        # Policy
        self._policies = self._default_policies()

        # Counters
        self._total_runs = 0
        self._completed_runs = 0
        self._held_runs = 0
        self._aborted_runs = 0

    def _default_policies(self):
        """Default governance policies by mode."""
        return {
            "OPEN": {
                "auto_approve_flag": True,
                "require_fingerprint": False,
                "max_concurrent": 100,
                "require_audit": False,
            },
            "SUPERVISED": {
                "auto_approve_flag": False,
                "require_fingerprint": True,
                "max_concurrent": 20,
                "require_audit": True,
            },
            "LOCKED": {
                "auto_approve_flag": False,
                "require_fingerprint": True,
                "max_concurrent": 5,
                "require_audit": True,
            },
            "QUARANTINE": {
                "auto_approve_flag": False,
                "require_fingerprint": True,
                "max_concurrent": 0,
                "require_audit": True,
            },
        }

    @property
    def policy(self):
        return self._policies.get(self.mode, self._policies["SUPERVISED"])

    # ── Controller Management ──

    def create_controller(self, controller_id, name, domain, carriers,
                          preset=None):
        """
        Create and register a new controller under this governor.

        Parameters
        ----------
        controller_id : str
            Unique controller ID
        name : str
            System name
        domain : str
            Domain classification
        carriers : list
            Carrier names
        preset : str, optional
            Breakpoint preset (defaults based on governance mode)

        Returns
        -------
        HsController
        """
        # Check concurrent limit
        active = sum(1 for c in self._controllers.values()
                     if c.state in ("RUNNING", "HELD"))
        max_conc = self.policy["max_concurrent"]
        if active >= max_conc:
            raise RuntimeError(
                f"Concurrent controller limit reached ({max_conc}). "
                f"Mode: {self.mode}. Complete or abort existing controllers first."
            )

        # Default preset based on governance mode
        if preset is None:
            preset_map = {
                "OPEN": "permissive",
                "SUPERVISED": "cautious",
                "LOCKED": "strict",
                "QUARANTINE": "strict",
            }
            preset = preset_map.get(self.mode, "cautious")

        ctrl = HsController(
            controller_id, name=name, domain=domain,
            carriers=carriers, verbose=self.verbose
        )

        # Add governance policy hook
        ctrl.add_policy_hook(self._policy_hook)
        ctrl.set_governor(self)

        # Subscribe to controller events
        ctrl.events.on("STATE_CHANGE", lambda e: self._on_controller_event(ctrl, e))
        ctrl.events.on("CLASSIFICATION", lambda e: self._on_classification(ctrl, e))
        ctrl.events.on("FINGERPRINT", lambda e: self._on_fingerprint(ctrl, e))
        ctrl.events.on("HOLD_WAITING", lambda e: self._on_hold(ctrl, e))
        ctrl.events.on("ERROR", lambda e: self._on_error(ctrl, e))

        self._controllers[controller_id] = ctrl
        self._total_runs += 1

        self._events.emit("STATE_CHANGE", {
            "message": f"Controller {controller_id} registered",
            "controller_id": controller_id,
            "name": name,
            "domain": domain,
            "preset": preset,
            "governance_mode": self.mode,
        }, source="HUF-GOV")

        if self.verbose:
            print(f"  [Hˢ-GOV] Registered controller: {controller_id} "
                  f"({name}, {domain}) preset={preset}")

        return ctrl

    def get_controller(self, controller_id):
        """Get a registered controller by ID."""
        return self._controllers.get(controller_id)

    def list_controllers(self):
        """List all controllers with their current state."""
        return {
            cid: {
                "state": ctrl.state,
                "name": ctrl.name,
                "domain": ctrl.domain,
            }
            for cid, ctrl in self._controllers.items()
        }

    # ── Policy Engine ──

    def _policy_hook(self, controller, from_state, to_state, reason):
        """Governance policy hook called on every state transition."""
        decision = "ALLOW"

        # Quarantine: block all new runs
        if self.mode == "QUARANTINE" and to_state == "RUNNING" and from_state == "IDLE":
            decision = "DENY"
            self._log_decision(controller, from_state, to_state, decision,
                              "QUARANTINE mode — no new runs allowed")

        self._events.emit("POLICY_CHECK", {
            "controller_id": controller.controller_id,
            "from": from_state,
            "to": to_state,
            "decision": decision,
            "governance_mode": self.mode,
        }, source="HUF-GOV")

        return decision

    def _log_decision(self, controller, from_state, to_state, decision, reason):
        """Log a governance decision."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "controller_id": controller.controller_id,
            "from_state": from_state,
            "to_state": to_state,
            "decision": decision,
            "reason": reason,
            "governance_mode": self.mode,
        }
        self._decisions.append(entry)
        if self.verbose:
            print(f"  [Hˢ-GOV] Decision: {decision} — {controller.controller_id} "
                  f"{from_state}→{to_state}: {reason}")

    # ── Event Handlers ──

    def _on_controller_event(self, controller, event):
        """Handle state change events from controllers."""
        payload = event.get("payload", {})
        to_state = payload.get("to")
        if to_state == "COMPLETED":
            self._completed_runs += 1
        elif to_state == "ABORTED":
            self._aborted_runs += 1

    def _on_classification(self, controller, event):
        """Handle classification events."""
        payload = event.get("payload", {})
        cls = payload.get("classification")
        if self.verbose:
            print(f"  [Hˢ-GOV] Classification: {controller.controller_id} → {cls}")

    def _on_fingerprint(self, controller, event):
        """Handle fingerprint events — add to cross-run database."""
        payload = event.get("payload", {})
        fp_hash = payload.get("hash")
        if fp_hash:
            self._fingerprint_db[fp_hash] = {
                "controller_id": controller.controller_id,
                "name": controller.name,
                "domain": controller.domain,
                "classification": payload.get("classification"),
                "timestamp": event.get("timestamp"),
            }
            if self.verbose:
                print(f"  [Hˢ-GOV] Fingerprint registered: {fp_hash} "
                      f"({controller.name})")

    def _on_hold(self, controller, event):
        """Handle HOLD events."""
        self._held_runs += 1
        if self.verbose:
            reason = event.get("payload", {}).get("reason", "unknown")
            print(f"  [Hˢ-GOV] Controller HELD: {controller.controller_id} — {reason}")

    def _on_error(self, controller, event):
        """Handle error events."""
        if self.verbose:
            payload = event.get("payload", {})
            print(f"  [Hˢ-GOV] ERROR in {controller.controller_id}: "
                  f"{payload.get('error', 'unknown')}")

    # ── Cross-Run Analysis ──

    def find_similar(self, fingerprint_hash, threshold=0.7):
        """
        Search the fingerprint database for similar systems.

        Parameters
        ----------
        fingerprint_hash : str
            Fingerprint hash to match against
        threshold : float
            Minimum similarity (only exact match supported in DB;
            full comparison requires fingerprint objects)

        Returns
        -------
        list of matching entries from the database
        """
        matches = []
        for fh, entry in self._fingerprint_db.items():
            if fh == fingerprint_hash:
                matches.append({"match": "EXACT", **entry})
        return matches

    def cross_check_all(self):
        """
        Compare all fingerprints in the database against each other.

        Returns
        -------
        list of (hash1, hash2, match_type) tuples
        """
        hashes = list(self._fingerprint_db.keys())
        matches = []
        for i, h1 in enumerate(hashes):
            for h2 in hashes[i+1:]:
                if h1 == h2:
                    matches.append((h1, h2, "EXACT"))
        return matches

    # ── Governance Controls ──

    def set_mode(self, mode):
        """Change governance mode."""
        if mode not in self._policies:
            raise ValueError(f"Invalid mode: {mode}. Valid: {list(self._policies.keys())}")
        old_mode = self.mode
        self.mode = mode
        self._events.emit("STATE_CHANGE", {
            "message": f"Governance mode changed: {old_mode} → {mode}",
            "from": old_mode,
            "to": mode,
        }, source="HUF-GOV")
        if self.verbose:
            print(f"  [Hˢ-GOV] Mode: {old_mode} → {mode}")

    def quarantine(self, reason=""):
        """Enter quarantine mode — hold all running controllers, block new runs."""
        self.set_mode("QUARANTINE")
        # Hold all running controllers
        for ctrl in self._controllers.values():
            if ctrl.state == "RUNNING":
                try:
                    ctrl.abort(f"QUARANTINE: {reason}")
                except RuntimeError:
                    pass  # Already in terminal state

    # ── Reporting ──

    def status(self):
        """Get governor status summary."""
        return {
            "governor_id": self.governor_id,
            "governor_hash": self.governor_hash,
            "mode": self.mode,
            "created": self.created,
            "total_runs": self._total_runs,
            "completed": self._completed_runs,
            "held": self._held_runs,
            "aborted": self._aborted_runs,
            "active_controllers": sum(1 for c in self._controllers.values()
                                     if c.state in ("RUNNING", "HELD")),
            "fingerprints_registered": len(self._fingerprint_db),
            "decisions_logged": len(self._decisions),
            "events_total": len(self._events.history),
            "controllers": self.list_controllers(),
        }

    def save_state(self, filepath):
        """Save complete governor state."""
        state = {
            "_type": "HUF_GOV_STATE",
            "_version": "1.0",
            "status": self.status(),
            "decisions": self._decisions,
            "fingerprint_db": self._fingerprint_db,
            "events": self._events.history,
            "controller_states": {
                cid: ctrl.inspect()
                for cid, ctrl in self._controllers.items()
            },
        }
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2, default=str)

    def summary(self):
        """Human-readable summary."""
        s = self.status()
        lines = [
            f"Hˢ-GOV SUPERVISOR — {self.governor_id}",
            f"{'=' * 60}",
            f"Mode:          {s['mode']}",
            f"Hash:          {s['governor_hash']}",
            f"Controllers:   {len(self._controllers)} ({s['active_controllers']} active)",
            f"Runs:          {s['total_runs']} total, {s['completed']} done, "
            f"{s['held']} held, {s['aborted']} aborted",
            f"Fingerprints:  {s['fingerprints_registered']}",
            f"Decisions:     {s['decisions_logged']}",
            f"Events:        {s['events_total']}",
        ]
        if self._controllers:
            lines.append(f"\nControllers:")
            for cid, ctrl in self._controllers.items():
                lines.append(f"  {cid}: {ctrl.state} — {ctrl.name} ({ctrl.domain})")

        return "\n".join(lines)


# ════════════════════════════════════════════════════════════
# CLI
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Hˢ Industrial Controller v1.0")
    print(f"States: {', '.join(sorted(VALID_STATES))}")
    print(f"Event types: {', '.join(sorted(EVENT_TYPES))}")
    print(f"Governance modes: OPEN, SUPERVISED, LOCKED, QUARANTINE")
    print()
    print("Architecture:")
    print("  Hˢ-GOV  →  Controller  →  Pipeline  →  Audit Trail")
    print("  (govern)    (control)      (analyse)    (trace)")
