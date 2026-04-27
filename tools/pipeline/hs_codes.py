#!/usr/bin/env python3
"""
Hˢ DIAGNOSTIC CODE SYSTEM
===========================
Lightweight code generation for the Higgins Decomposition pipeline.
The pipeline emits structured codes; a separate reporter reads them.

Code Format: SS-CCC-LLL
  SS  = Stage (2 chars): pipeline step or extended test
  CCC = Condition (3 chars): what was detected
  LLL = Level (3 chars): severity / information class

Stages:
  GD = Guard (input validation)
  S4 = Step 4 (simplex closure)
  S5 = Step 5 (CLR transform)
  S6 = Step 6 (Aitchison variance)
  S7 = Step 7 (HVLD vertex lock)
  S8 = Step 8 (super squeeze)
  S9 = Step 9 (EITT entropy)
  SA = Step 10 (ternary projection)
  SB = Step 11 (complex plane)
  SC = Step 12 (helix/polar)
  XU = Extended universal panel
  XC = Extended conditional panel
  RP = Report summary

Levels:
  INF = Information (normal operation)
  WRN = Warning (attention needed)
  ERR = Error (operation failed or invalid)
  DIS = Discovery (noteworthy finding)
  CAL = Calibration (instrument calibration signal)

Author: Peter Higgins / Claude
Version: 1.2 (added Component Power codes: CPM, DPC, PSC, CFR, PWR)
"""

# ════════════════════════════════════════════════════════════
# CODE DICTIONARY
# ════════════════════════════════════════════════════════════

CODE_DICTIONARY = {
    # ── GUARDS ──
    "GD-D2M-ERR": {"short": "D < 2", "verbose": "Input rejected: D must be >= 2. The simplex requires at least 2 compositional parts."},
    "GD-N5M-ERR": {"short": "N < 5", "verbose": "Input rejected: N must be >= 5. The variance trajectory needs at least 3 non-zero points for a meaningful HVLD fit."},
    "GD-NAN-ERR": {"short": "NaN detected", "verbose": "Input rejected: data contains NaN values. Clean or impute before decomposition."},
    "GD-INF-ERR": {"short": "Inf detected", "verbose": "Input rejected: data contains Inf values. Check for division by zero or overflow."},
    "GD-SCL-ERR": {"short": "Scale disparity", "verbose": "Input rejected: max/min ratio exceeds 1e15. Normalise or partition before decomposition."},
    "GD-ALL-INF": {"short": "All guards pass", "verbose": "All 4 input guards passed. Data is valid for Hˢ pipeline processing."},

    # ── STEP 4: CLOSURE ──
    "S4-CLO-INF": {"short": "Closure OK", "verbose": "Simplex closure successful. All rows sum to 1.0 within tolerance 1e-12."},
    "S4-ZRP-INF": {"short": "Zero replacement", "verbose": "Multiplicative zero replacement applied. ZERO_DELTA = 1e-6."},
    "S4-ZRN-INF": {"short": "No zeros", "verbose": "No zero replacement needed. All input values are positive."},

    # ── STEP 5: CLR ──
    "S5-CLR-INF": {"short": "CLR complete", "verbose": "Centred log-ratio transform applied. All rows sum to zero in CLR space."},

    # ── STEP 6: VARIANCE ──
    "S6-VAR-INF": {"short": "Variance computed", "verbose": "Cumulative Aitchison variance trajectory σ²_A(t) computed for all time indices."},
    "S6-ZRO-WRN": {"short": "Zero variance", "verbose": "σ²_A is zero or near-zero. Data may be constant or degenerate."},
    "S6-RNG-INF": {"short": "Variance range", "verbose": "Variance trajectory range and final value recorded."},

    # ── STEP 7: HVLD ──
    "S7-BWL-INF": {"short": "HVLD bowl", "verbose": "HVLD vertex lock: bowl shape (a > 0). Variance is accelerating — system integrating."},
    "S7-HIL-INF": {"short": "HVLD hill", "verbose": "HVLD vertex lock: hill shape (a < 0). Variance is decelerating — system segregating."},
    "S7-HRQ-INF": {"short": "HVLD R² high", "verbose": "HVLD R² > 0.8. Quadratic fit describes the trajectory well."},
    "S7-LRQ-WRN": {"short": "HVLD R² low", "verbose": "HVLD R² < 0.5. Quadratic fit is poor — trajectory may be non-polynomial."},
    "S7-VTX-INF": {"short": "Vertex location", "verbose": "HVLD vertex (lock point) location recorded."},

    # ── STEP 8: SQUEEZE ──
    "S8-NAT-INF": {"short": "NATURAL", "verbose": "HTP classification: NATURAL. At least one transcendental match within δ < 1%."},
    "S8-INV-WRN": {"short": "INVESTIGATE", "verbose": "HTP classification: INVESTIGATE. Nearest match δ between 1% and 5%. Consider alternate decomposition."},
    "S8-FLG-WRN": {"short": "FLAG", "verbose": "HTP classification: FLAG. No match within 5%. System may be synthetic, adversarial, or improperly decomposed."},
    "S8-EUL-DIS": {"short": "Euler-family match", "verbose": "Nearest constant is from the Euler family (2π, e^π, π^e, or their reciprocals). Pipeline geometry resonates with system structure."},
    "S8-SQZ-INF": {"short": "Squeeze count", "verbose": "Number of transcendental proximity matches recorded."},
    "S8-TGT-DIS": {"short": "Tight match", "verbose": "Transcendental match tighter than δ < 0.001. Precision-level structural resonance."},

    # ── STEP 9: EITT ──
    "S9-ENT-INF": {"short": "Entropy computed", "verbose": "Shannon entropy H(t) computed for all observations. Normalised by H_max = ln(D)."},
    "S9-EIT-INF": {"short": "EITT pass", "verbose": "EITT invariance test passed at all tested compression ratios (variation < 5%)."},
    "S9-EIF-WRN": {"short": "EITT fail", "verbose": "EITT invariance test failed at one or more compression ratios."},
    "S9-CHS-INF": {"short": "Chaos low", "verbose": "Chaos detection: few deviations. System is compositionally smooth."},
    "S9-CHH-DIS": {"short": "Chaos high", "verbose": "Chaos detection: many deviations. System exhibits compositional turbulence — stalls, spikes, or reversals."},
    "S9-STL-DIS": {"short": "Stalls detected", "verbose": "Angular velocity stalls detected — entropy rate dropped below 15% of running mean."},
    "S9-SPK-DIS": {"short": "Spikes detected", "verbose": "Angular velocity spikes detected — entropy rate exceeded 3.5× running mean."},
    "S9-REV-DIS": {"short": "Reversals detected", "verbose": "Entropy reversals detected — ≥2 sign changes in 5 consecutive samples."},

    # ── STEPS 10-12: GEOMETRY ──
    "SA-TRN-INF": {"short": "Ternary OK", "verbose": "Ternary projection computed. Type: ternary (D=3), 1-simplex (D=2), or projected (D>3)."},
    "SB-CPX-INF": {"short": "Complex plane OK", "verbose": "Complex plane mapping computed. Centroid-relative coordinates."},
    "SC-HLX-INF": {"short": "Helix OK", "verbose": "3D helix/polar embedding computed. Radius, angle, angular velocity."},

    # ── EXTENDED UNIVERSAL ──
    "XU-PCC-INF": {"short": "Carrier decomposition", "verbose": "Per-carrier contribution computed. Shows which carrier drives the variance."},
    "XU-PCD-DIS": {"short": "Carrier dominance", "verbose": "One carrier contributes >60% of total variance. Strong structural signal."},
    "XU-MDN-INF": {"short": "Match density natural", "verbose": "Match density consistent with natural system (density >> synthetic baseline)."},
    "XU-MDS-CAL": {"short": "Match density low", "verbose": "Match density below natural baseline. May indicate synthetic data or sparse constant coverage."},
    "XU-DRI-INF": {"short": "Drift stable", "verbose": "Carrier drift trend: stable. Second half compositionally similar to first half."},
    "XU-DRU-DIS": {"short": "Drift increasing", "verbose": "Carrier drift trend: increasing. System is evolving — second half more dispersed."},
    "XU-DRD-DIS": {"short": "Drift decreasing", "verbose": "Carrier drift trend: decreasing. System is converging — second half more concentrated."},
    "XU-CDA-INF": {"short": "CoDa panel OK", "verbose": "CoDa structural panel computed: variation matrix, CLR summary, Aitchison distance."},
    "XU-CLM-INF": {"short": "Claim summary", "verbose": "Claim-status and envelope summary generated."},

    # ── EXTENDED CONDITIONAL ──
    "XC-PID-INF": {"short": "PID computed", "verbose": "Partial Information Decomposition computed. Redundant, unique, and synergistic carrier interactions quantified."},
    "XC-PIR-DIS": {"short": "PID redundancy", "verbose": "PID dominant mode: redundancy. Carriers share information — coupled dynamics."},
    "XC-PIU-DIS": {"short": "PID unique", "verbose": "PID dominant mode: unique. One carrier contributes information the others cannot — independent dynamics."},
    "XC-TEE-INF": {"short": "Transfer entropy", "verbose": "Transfer entropy matrix computed. Directed information flow between carriers quantified."},
    "XC-TEF-DIS": {"short": "TE dominant flow", "verbose": "Dominant directed information flow identified. One carrier informationally predicts another."},
    "XC-TEZ-CAL": {"short": "TE zero", "verbose": "Transfer entropy is zero across all pairs. System is compositionally memoryless at this aggregation level."},
    "XC-ORD-INF": {"short": "Order matters", "verbose": "Order sensitivity test: temporal/parametric order significantly affects the variance trajectory."},
    "XC-ORN-INF": {"short": "Order neutral", "verbose": "Order sensitivity test: shuffling order does not change the result. Structure is cross-sectional."},
    "XC-RPL-INF": {"short": "Ratio-pair lattice", "verbose": "Ratio-pair lattice computed. All pairwise log-ratios ranked by stability (CV)."},
    "XC-RPS-DIS": {"short": "Stable ratio found", "verbose": "A highly stable pairwise ratio detected (CV < 20%). These carriers are compositionally locked."},
    "XC-RPV-DIS": {"short": "Volatile ratio", "verbose": "A highly volatile pairwise ratio detected (CV > 50%). These carriers are compositionally independent."},
    "XC-ZCR-DIS": {"short": "Zero crossings", "verbose": "Carrier zero-crossing events detected. Compositions approaching simplex boundary — structural singularities."},

    # ── EXTENDED: HIERARCHY & FINGERPRINT ──
    "XU-HRC-INF": {"short": "Hierarchy moderate", "verbose": "Carrier hierarchy ratio (max/min of central values) is between 10³ and 10⁶. Moderate disparity — Dirichlet perturbation stable."},
    "XU-HRX-WRN": {"short": "Hierarchy extreme", "verbose": "Carrier hierarchy ratio exceeds 10⁶ (but below Guard 4 limit of 10¹⁵). Extreme disparity — perturbation methods may need alpha flooring. EITT failure is expected."},
    "XU-CSL-DIS": {"short": "Conservation signature", "verbose": "All carrier pairs show PID redundancy and at least 50% of ratio pairs are stable (CV < 20%). Strong signature of an underlying conservation law linking all carriers."},
    "XU-FPR-INF": {"short": "Fingerprint generated", "verbose": "Compositional fingerprint computed: hash of HVLD shape, R² band, classification, structural modes, and nearest constant family. Use for cross-database matching."},

    # ── COMPONENT POWER ──
    "XU-CPM-INF": {"short": "Power map computed", "verbose": "Component Power Mapper analysis completed. Leverage index, phase boundary map, and power scores computed for all carriers. Power rankings may differ from mass fraction rankings."},
    "XU-DPC-DIS": {"short": "Disproportionate carrier", "verbose": "One or more carriers have power-to-fraction ratios exceeding 2.0x, meaning their influence on system character is at least double what their mass fraction would predict. These are compositionally critical components."},
    "XU-PSC-WRN": {"short": "Phase-sensitive carrier", "verbose": "One or more carriers have criticality margins below 0.3, meaning small changes to their values can flip the system classification or HVLD shape. The system is sensitive to these components."},
    "XU-CFR-WRN": {"short": "Classification flip risk", "verbose": "Perturbation of one or more carriers caused the system classification to flip between NATURAL and FLAG (or between shapes). The system is near a phase boundary for these carriers."},
    "XU-PWR-DIS": {"short": "Power ≠ mass", "verbose": "The power ranking of carriers differs from the mass fraction ranking. Component influence on system character is not proportional to component fraction. This is the compositional leverage effect."},

    # ── REPORT ──
    "RP-CMP-INF": {"short": "Run complete", "verbose": "Hˢ extended pipeline run completed successfully. All results available for reporting."},
    "RP-DTM-INF": {"short": "Deterministic", "verbose": "Pipeline is deterministic. Repeated runs on identical data produce bit-identical results."},
    "RP-VER-INF": {"short": "Version", "verbose": "Pipeline version and configuration recorded."},

    # ── STRUCTURAL MODES (SM) ──
    # Detected from combinations of other codes. Not individual measurements —
    # structural diagnoses of the compositional geometry as a whole.
    # These are investigation prompts, not verdicts.

    "SM-BPO-DIS": {"short": "Bimodal population",
        "verbose": "Two or more distinct compositional populations detected on the simplex. "
                   "The variance trajectory shows mid-range peak (hill) with high turbulence "
                   "and EITT failure — entropy decimation mixes populations that should be separate. "
                   "INVESTIGATE: decompose by subpopulation, separate mechanism types, or add a carrier "
                   "that distinguishes the populations."},
    "SM-SCG-INF": {"short": "Smooth convergence",
        "verbose": "System converges smoothly to compositional equilibrium. Bowl HVLD with "
                   "low turbulence and EITT preservation indicates a single population evolving "
                   "continuously across the simplex. This is the expected mode for well-sampled "
                   "natural systems with a single dominant mechanism."},
    "SM-MCA-WRN": {"short": "Missing carrier",
        "verbose": "Compositional geometry suggests an incomplete decomposition. FLAG "
                   "classification combined with zero-crossings or degenerate vertices indicates "
                   "energy or information is leaking to an untracked carrier. "
                   "INVESTIGATE: what physical channel is absorbing the missing fraction? "
                   "Add the missing carrier and re-run. The FLAG should resolve."},
    "SM-DMR-DIS": {"short": "Domain resonance",
        "verbose": "System encodes deep geometric structure — Euler-family transcendental "
                   "detected with strong R². The constant is not accidental; the pipeline's "
                   "log-ratio geometry IS the structure. "
                   "INVESTIGATE: compare this constant to other decompositions in the same domain. "
                   "Do different decompositions lock to the same family? Does the specific constant "
                   "change with carrier choice?"},
    "SM-CPL-DIS": {"short": "Carrier coupling",
        "verbose": "Carriers are physically linked — PID shows redundancy and at least one "
                   "ratio pair is highly stable. The coupled carriers share a common driver. "
                   "INVESTIGATE: the stable ratio encodes a physical constraint (conservation law, "
                   "stoichiometry, momentum balance). Can the coupled carriers be merged or one "
                   "derived from the other?"},
    "SM-IND-DIS": {"short": "Carrier independence",
        "verbose": "Carriers are governed by independent mechanisms — all ratio pairs are volatile "
                   "and PID shows unique information in each. No carrier predicts another. "
                   "INVESTIGATE: this is typical of systems where each carrier represents a "
                   "different physical process. The decomposition may be maximally informative."},
    "SM-DGN-WRN": {"short": "Degenerate simplex",
        "verbose": "Data approaches the simplex boundary — zero-crossings detected with FLAG "
                   "or low N. One or more observations have a carrier at or near zero, creating "
                   "a degenerate vertex that distorts log-ratio geometry. "
                   "INVESTIGATE: is the zero physical (carrier genuinely absent) or artefactual "
                   "(measurement limit, missing data)? If physical, consider whether the carrier "
                   "definition should change."},
    "SM-RTR-DIS": {"short": "Regime transition",
        "verbose": "System undergoes compositional regime change — drift detected with stalls "
                   "and reversals. The composition is not stationary; it transitions between "
                   "structural states. "
                   "INVESTIGATE: the stall points mark regime boundaries. What physical parameter "
                   "changes at the transition? Consider splitting the data at the transition and "
                   "running each segment independently."},
    "SM-TNT-DIS": {"short": "Turbulent natural",
        "verbose": "System is NATURAL but turbulent — transcendental match found despite EITT "
                   "failure and high chaos. The turbulence is structural, not noise. The system "
                   "encodes real complexity that decimation destroys. "
                   "INVESTIGATE: the turbulence pattern contains information. What mechanisms "
                   "produce the oscillation? Alpha/beta alternation? Market cycles? Seasonal effects? "
                   "The oscillation frequency may be diagnostic."},
    "SM-OVC-CAL": {"short": "Overconstrained",
        "verbose": "System is highly constrained — near-perfect HVLD R², EITT pass, and "
                   "precision-level δ. This is either a mathematical function, a physical system "
                   "under tight constraints, or derived data. "
                   "INVESTIGATE: verify this is measured data, not model output. If derived, the "
                   "tight match is expected and calibrates the pipeline. If measured, this is a "
                   "precision-standard-grade result."},
}


# ════════════════════════════════════════════════════════════
# STRUCTURAL MODE DETECTION MATRIX
# ════════════════════════════════════════════════════════════
#
# Each mode is defined by a set of required and forbidden codes.
# The mode fires if ALL required codes are present and NO forbidden
# codes are present. Modes are evaluated in priority order.
#
# This is not a high-level analysis of the data — it is a structural
# analysis of the code pattern itself. The codes are geometric facts.
# The modes are geometric interpretations.

STRUCTURAL_MODES = [
    {
        "mode": "SM-OVC-CAL",
        "name": "Overconstrained",
        "requires": ["S7-HRQ", "S8-NAT", "S8-TGT", "S9-EIT"],
        "forbids": ["S9-CHH", "S8-FLG"],
        "priority": 1,
    },
    {
        "mode": "SM-MCA-WRN",
        "name": "Missing carrier",
        "requires": ["S8-FLG"],
        "requires_any": ["XC-ZCR", "S6-ZRO"],
        "forbids": [],
        "priority": 2,
    },
    {
        "mode": "SM-BPO-DIS",
        "name": "Bimodal population",
        "requires": ["S7-HIL", "S9-EIF", "S9-CHH"],
        "forbids": [],
        "priority": 3,
    },
    {
        "mode": "SM-TNT-DIS",
        "name": "Turbulent natural",
        "requires": ["S8-NAT", "S9-EIF", "S9-CHH"],
        "forbids": [],
        "priority": 4,
    },
    {
        "mode": "SM-RTR-DIS",
        "name": "Regime transition",
        "requires": ["S9-STL", "S9-REV"],
        "requires_any": ["XU-DRU", "XU-DRD"],
        "forbids": [],
        "priority": 5,
    },
    {
        "mode": "SM-DGN-WRN",
        "name": "Degenerate simplex",
        "requires": ["XC-ZCR"],
        "requires_any": ["S8-FLG", "S7-LRQ"],
        "forbids": [],
        "priority": 6,
    },
    {
        "mode": "SM-DMR-DIS",
        "name": "Domain resonance",
        "requires": ["S8-EUL", "S8-NAT"],
        "forbids": ["S8-FLG"],
        "priority": 7,
    },
    {
        "mode": "SM-CPL-DIS",
        "name": "Carrier coupling",
        "requires": ["XC-PIR", "XC-RPS"],
        "forbids": [],
        "priority": 8,
    },
    {
        "mode": "SM-IND-DIS",
        "name": "Carrier independence",
        "requires": ["XC-RPV"],
        "forbids": ["XC-RPS", "XC-PIR"],
        "priority": 9,
    },
    {
        "mode": "SM-SCG-INF",
        "name": "Smooth convergence",
        "requires": ["S7-BWL", "S9-EIT"],
        "forbids": ["S9-CHH", "S8-FLG", "S9-EIF"],
        "priority": 10,
    },
]


def generate_codes(result):
    """Generate diagnostic codes from an Hˢ pipeline result dict.
    
    Parameters
    ----------
    result : dict
        Output from HigginsDecomposition.run_full_extended()
    
    Returns
    -------
    list of dict, each with: code, short, verbose, value (optional)
    """
    codes = []
    
    def emit(code, value=None):
        entry = CODE_DICTIONARY.get(code, {"short": code, "verbose": "Unknown code"})
        codes.append({"code": code, "short": entry["short"], "verbose": entry["verbose"], "value": value})
    
    s = result.get('steps', {})
    ext = result.get('extended', {})
    u = ext.get('universal', {})
    c = ext.get('conditional', {})
    
    # Guards
    emit("GD-ALL-INF")
    
    # Closure
    if s.get('step3_zero_replacement_applied'):
        emit("S4-ZRP-INF")
    else:
        emit("S4-ZRN-INF")
    emit("S4-CLO-INF", s.get('step3_closure_check'))
    
    # CLR
    emit("S5-CLR-INF")
    
    # Variance
    sig_final = s.get('step5_sigma2_final', 0)
    emit("S6-VAR-INF", sig_final)
    if sig_final < 1e-10:
        emit("S6-ZRO-WRN")
    emit("S6-RNG-INF", s.get('step5_sigma2_range'))
    
    # HVLD
    shape = s.get('step6_pll_shape', 'unknown')
    r2 = s.get('step6_pll_R2', 0)
    if shape == 'bowl':
        emit("S7-BWL-INF", r2)
    else:
        emit("S7-HIL-INF", r2)
    if r2 > 0.8:
        emit("S7-HRQ-INF", r2)
    elif r2 < 0.5:
        emit("S7-LRQ-WRN", r2)
    emit("S7-VTX-INF", s.get('step6_vertex'))
    
    # Squeeze
    sq = s.get('step7_squeeze_closest')
    if sq:
        delta = sq.get('delta', 999)
        const = sq.get('constant', '')
        if delta < 0.01:
            emit("S8-NAT-INF", {"constant": const, "delta": delta})
        elif delta < 0.05:
            emit("S8-INV-WRN", {"constant": const, "delta": delta})
        else:
            emit("S8-FLG-WRN", {"constant": const, "delta": delta})
        
        euler_family = ['2pi', 'e^pi', 'pi^e', '1/(2pi)', '1/(e^pi)', '1/(pi^e)']
        if const in euler_family:
            emit("S8-EUL-DIS", {"constant": const, "delta": delta})
        
        if delta < 0.001:
            emit("S8-TGT-DIS", {"constant": const, "delta": delta})
    else:
        emit("S8-FLG-WRN")
    
    emit("S8-SQZ-INF", s.get('step7_squeeze_count', 0))
    
    # EITT
    emit("S9-ENT-INF", s.get('step8_entropy_mean'))
    eitt = s.get('step8_eitt_invariance', {})
    all_pass = all(v.get('pass', False) for v in eitt.values()) if eitt else False
    if all_pass:
        emit("S9-EIT-INF")
    elif eitt:
        emit("S9-EIF-WRN")
    
    chaos = s.get('step9_chaos_detection', {})
    total_dev = chaos.get('total_deviations', 0)
    if total_dev < 10:
        emit("S9-CHS-INF", total_dev)
    else:
        emit("S9-CHH-DIS", total_dev)
    if chaos.get('stalls', 0) > 0:
        emit("S9-STL-DIS", chaos['stalls'])
    if chaos.get('spikes', 0) > 0:
        emit("S9-SPK-DIS", chaos['spikes'])
    if chaos.get('reversals', 0) > 0:
        emit("S9-REV-DIS", chaos['reversals'])
    
    # Geometry
    emit("SA-TRN-INF")
    emit("SB-CPX-INF")
    emit("SC-HLX-INF")
    
    # Extended universal
    if u:
        pcc = u.get('per_carrier_contribution', {})
        emit("XU-PCC-INF", pcc)
        if pcc.get('dominant_pct', 0) > 60:
            emit("XU-PCD-DIS", {"carrier": pcc.get('dominant_carrier'), "pct": pcc.get('dominant_pct')})
        
        md = u.get('match_density', {})
        if md.get('density', 0) > 10:
            emit("XU-MDN-INF", md)
        else:
            emit("XU-MDS-CAL", md)
        
        drift = u.get('carrier_drift', {})
        direction = drift.get('drift_direction', 'stable')
        if direction == 'stable':
            emit("XU-DRI-INF", drift)
        elif direction == 'increasing':
            emit("XU-DRU-DIS", drift)
        else:
            emit("XU-DRD-DIS", drift)
        
        emit("XU-CDA-INF")
        emit("XU-CLM-INF")

        # Carrier hierarchy detection
        coda = u.get('coda_structural', {})
        var_matrix = coda.get('variation_matrix', {})
        # Check hierarchy from per-carrier contributions
        pcc_vals = pcc.get('contributions', {})
        if pcc_vals:
            vals = [v for v in pcc_vals.values() if isinstance(v, (int, float)) and v > 0]
            if len(vals) >= 2:
                ratio = max(vals) / min(vals)
                if ratio > 1e6:
                    emit("XU-HRX-WRN", {"ratio": ratio})
                elif ratio > 1e3:
                    emit("XU-HRC-INF", {"ratio": ratio})

    # Extended conditional
    if c.get('PID'):
        pid = c['PID']
        emit("XC-PID-INF", pid)
        if pid.get('dominant') == 'redundancy':
            emit("XC-PIR-DIS")
        else:
            emit("XC-PIU-DIS")
    
    if c.get('transfer_entropy'):
        te = c['transfer_entropy']
        emit("XC-TEE-INF")
        if te.get('dominant_te', 0) > 0.001:
            emit("XC-TEF-DIS", {"flow": te.get('dominant_flow'), "te": te.get('dominant_te')})
        else:
            emit("XC-TEZ-CAL")
    
    if c.get('order_sensitivity'):
        os_r = c['order_sensitivity']
        if os_r.get('order_matters'):
            emit("XC-ORD-INF", os_r)
        else:
            emit("XC-ORN-INF", os_r)
    
    if c.get('ratio_pair_lattice'):
        rpl = c['ratio_pair_lattice']
        emit("XC-RPL-INF", rpl)
        # Check for very stable or volatile pairs
        for pname, pdata in rpl.get('pairs', {}).items():
            if pdata.get('cv', 100) < 20:
                emit("XC-RPS-DIS", {"pair": pname, "cv": pdata['cv']})
            if pdata.get('cv', 0) > 50:
                emit("XC-RPV-DIS", {"pair": pname, "cv": pdata['cv']})
    
    if c.get('zero_crossing'):
        emit("XC-ZCR-DIS", c['zero_crossing'])

    # Conservation signature: PID redundancy + majority stable ratios
    pid_redundant = c.get('PID', {}).get('dominant') == 'redundancy'
    if pid_redundant and c.get('ratio_pair_lattice'):
        rpl_pairs = c['ratio_pair_lattice'].get('pairs', {})
        if rpl_pairs:
            total_pairs = len(rpl_pairs)
            stable_pairs = sum(1 for p in rpl_pairs.values() if p.get('cv', 100) < 20)
            if total_pairs > 0 and (stable_pairs / total_pairs) >= 0.5:
                emit("XU-CSL-DIS", {"stable_fraction": stable_pairs / total_pairs, "total_pairs": total_pairs})

    # ── COMPONENT POWER MAP ──
    # Power map results are stored at top level by the controller or
    # injected by hs_sensitivity.py after pipeline completion.
    power_map = result.get('power_map', {})
    if not power_map:
        # Also check inside extended panel (alternate integration point)
        power_map = ext.get('power_map', {})

    if power_map:
        summary_pm = power_map.get('summary', {})
        ps = power_map.get('power_scores', {})
        ps_carriers = ps.get('carriers', {})

        emit("XU-CPM-INF", {
            "carriers_analysed": len(ps_carriers),
            "most_powerful": summary_pm.get('most_powerful'),
        })

        # Disproportionate carriers (power >> mass fraction)
        disproportionate = ps.get('disproportionate_carriers', [])
        if disproportionate:
            emit("XU-DPC-DIS", {
                "count": len(disproportionate),
                "top": disproportionate[0].get('carrier'),
                "top_ratio": disproportionate[0].get('power_to_fraction_ratio'),
            })

        # Phase-sensitive carriers (criticality margin < 0.3)
        phase_sensitive = summary_pm.get('phase_sensitive_carriers', [])
        if phase_sensitive:
            emit("XU-PSC-WRN", {
                "count": len(phase_sensitive),
                "carriers": phase_sensitive,
            })

        # Classification flip risk
        flip_risk = summary_pm.get('classification_flip_risk_carriers', [])
        if flip_risk:
            emit("XU-CFR-WRN", {
                "count": len(flip_risk),
                "carriers": flip_risk,
            })

        # Power ranking differs from mass ranking
        if summary_pm.get('rankings_differ', False):
            emit("XU-PWR-DIS", {
                "power_ranking": summary_pm.get('power_ranking'),
                "mass_ranking": summary_pm.get('mass_ranking'),
            })

    # Report
    emit("RP-CMP-INF")
    emit("RP-DTM-INF")
    emit("RP-VER-INF", result.get('pipeline_version'))

    # ── STRUCTURAL MODE DETECTION ──
    # Scan all emitted codes and fire structural modes based on
    # the combination matrix. This is a second-order analysis:
    # the input is the code pattern, not the data.

    code_prefixes = set()
    for c in codes:
        # Extract prefix without level suffix (e.g., "S7-BWL" from "S7-BWL-INF")
        parts = c['code'].rsplit('-', 1)
        if len(parts) == 2:
            code_prefixes.add(parts[0])

    # Also track codes with level for specific matching
    code_set = set(c['code'] for c in codes)

    # Count volatile ratio pairs for independence detection
    volatile_count = sum(1 for c in codes if c['code'] == 'XC-RPV-DIS')
    stable_count = sum(1 for c in codes if c['code'] == 'XC-RPS-DIS')

    fired_modes = []
    for mode in sorted(STRUCTURAL_MODES, key=lambda m: m['priority']):
        # Check required codes (all must be present as prefixes)
        required = mode.get('requires', [])
        if not all(r in code_prefixes for r in required):
            continue

        # Check requires_any (at least one must be present)
        req_any = mode.get('requires_any', [])
        if req_any and not any(r in code_prefixes for r in req_any):
            continue

        # Check forbidden codes (none may be present)
        forbidden = mode.get('forbids', [])
        if any(f in code_prefixes for f in forbidden):
            continue

        # Special conditions for specific modes
        mode_code = mode['mode']

        # Carrier independence needs MULTIPLE volatile pairs and no stable pairs
        if mode_code == 'SM-IND-DIS' and (volatile_count < 3 or stable_count > 0):
            continue

        fired_modes.append(mode_code)

    # Emit fired structural modes
    for mode_code in fired_modes:
        emit(mode_code)

    return codes


def codes_to_summary(codes):
    """Generate a human-readable summary from diagnostic codes."""
    lines = []
    lines.append("Hˢ DIAGNOSTIC CODE REPORT")
    lines.append("=" * 60)
    
    errors = [c for c in codes if c['code'].endswith('-ERR')]
    warnings = [c for c in codes if c['code'].endswith('-WRN')]
    discoveries = [c for c in codes if c['code'].endswith('-DIS')]
    calibrations = [c for c in codes if c['code'].endswith('-CAL')]
    infos = [c for c in codes if c['code'].endswith('-INF')]
    
    lines.append(f"\nTotal codes: {len(codes)}")
    lines.append(f"  Errors:       {len(errors)}")
    lines.append(f"  Warnings:     {len(warnings)}")
    lines.append(f"  Discoveries:  {len(discoveries)}")
    lines.append(f"  Calibrations: {len(calibrations)}")
    lines.append(f"  Information:  {len(infos)}")
    
    if errors:
        lines.append("\n── ERRORS ──")
        for c in errors:
            lines.append(f"  [{c['code']}] {c['verbose']}")
    
    if warnings:
        lines.append("\n── WARNINGS ──")
        for c in warnings:
            lines.append(f"  [{c['code']}] {c['short']}")
    
    if discoveries:
        lines.append("\n── DISCOVERIES ──")
        for c in discoveries:
            val = f" → {c['value']}" if c['value'] else ""
            lines.append(f"  [{c['code']}] {c['short']}{val}")
    
    if calibrations:
        lines.append("\n── CALIBRATION SIGNALS ──")
        for c in calibrations:
            lines.append(f"  [{c['code']}] {c['short']}")
    
    return "\n".join(lines)


if __name__ == "__main__":
    print(f"Hˢ Diagnostic Code System v1.2")
    print(f"Total defined codes: {len(CODE_DICTIONARY)}")
    print(f"Stages: GD, S4-SC, XU, XC, RP")
    print(f"Levels: INF, WRN, ERR, DIS, CAL")
