#!/usr/bin/env python3
"""
Hs Duplex — a complete bidirectional compositional communication system (the crowning jewel).

The whole loop is done by compositions, by Hs, deterministically:
  A: GENERATE a deep message (an INSTRUCTION + a PAYLOAD trajectory)
     -> ENCODE into compositions (each carries D-1 byte-symbols) -> TRANSMIT
  channel: +/-20 dB common-mode multiplicative gain (rejected EXACTLY by closure) + additive ILR noise
  B: DECODE -> OBSERVE the instruction -> RUN Hs on the payload (compute-in-the-loop)
     -> ENCODE the reading -> TRANSMIT back
  A: DECODE the result; verify end-to-end by re-deriving B's result hash.

Pure information theory: bits each way, capacity (= (D-1)*8 bits/composition) grows with D,
common-mode rejection exact, additive exact-decode margin measured, integrity by SHA-256 each hop.
No Shannon limit is beaten; the value is determinism + integrity + common-mode robustness + the
relational/dimensional encoding. Author: Peter Higgins; AI-assisted per HUF-STD-001. Honest-broker.
"""
import numpy as np, hashlib, json, math
rng = np.random.default_rng(2026)

def helmert(D):
    B = np.zeros((D - 1, D))
    for i in range(1, D):
        B[i-1, :i] = 1.0/i; B[i-1, i] = -1.0; B[i-1] *= math.sqrt(i/(i+1.0))
    return B
def clr(x): L = np.log(x); return L - L.mean()
def sha(b): return hashlib.sha256(b if isinstance(b, bytes) else json.dumps(b, sort_keys=True, default=str).encode()).hexdigest()[:16]

A_RANGE = 2.0; L = 256; DELTA = 2 * A_RANGE / (L - 1)      # ILR quantization step

def encode(msg, D):
    H = helmert(D); k = D - 1; syms = list(msg); syms += [0] * ((-len(syms)) % k); comps = []
    for i in range(0, len(syms), k):
        ilr = np.array([-A_RANGE + 2*A_RANGE*b/(L-1) for b in syms[i:i+k]])
        c = np.exp(ilr @ H); comps.append(c / c.sum())
    return np.array(comps), len(msg)

def transmit_receive(comps, D, nbytes, gain_dB, sigma_ilr):
    H = helmert(D); syms = []; cm = 0.0
    for c in comps:
        g = 10 ** (rng.uniform(-gain_dB, gain_dB) / 20)       # common-mode gain
        comp = (g * c) / (g * c).sum()                        # CLOSURE rejects g exactly
        cm = max(cm, float(np.max(np.abs(clr(comp) - clr(c)))))
        ilr = clr(comp) @ H.T + sigma_ilr * rng.standard_normal(D - 1)
        for v in ilr:
            syms.append(int(np.clip(round((v + A_RANGE) / (2*A_RANGE) * (L-1)), 0, L-1)))
    return bytes(syms[:nbytes]), cm


def main():
    D = 8
    # additive exact-decode margin (sweep)
    probe = bytes(rng.integers(0, 256, 140).tolist()); cp, n = encode(probe, D); margin = 0.0
    for s in [0, 0.05, 0.1, 0.2, 0.3, 0.5]:
        if all(transmit_receive(cp, D, n, 20.0, s * DELTA)[0] == probe for _ in range(20)):
            margin = s
    SIGMA = 0.03 * DELTA

    # the deep message: instruction + a 4-part payload trajectory drifting toward part 3
    T = 8; pay = []
    for t in range(T):
        w = np.array([3.0-0.3*t, 2.0, 1.5, 0.5+0.5*t]); w /= w.sum(); pay.append((w*255).round().astype(int))
    payload = bytes(int(b) for row in pay for b in row)
    instr = b"HUF-RPC/1 READ traj4 REPORT arrow,effdim,coh;"
    M_fwd = instr + payload

    cf, nf = encode(M_fwd, D); M_b, cm1 = transmit_receive(cf, D, nf, 20.0, SIGMA); fwd_ok = (M_b == M_fwd)
    pb = M_b[len(instr):]; traj = np.array([[pb[t*4+j] for j in range(4)] for t in range(T)], float)
    traj = traj / traj.sum(1, keepdims=True); H4 = helmert(4)
    ILR = np.array([clr(c) @ H4.T for c in traj]); arrow = int(np.argmax(clr(traj[-1]) - clr(traj[0])))
    Z = ILR - ILR.mean(0); lam = np.linalg.svd(Z, compute_uv=False) ** 2; eff = float((lam.sum()**2)/(lam**2).sum())
    V = np.diff(ILR, 0); coh = float(np.linalg.norm(V.sum(0)) / (np.linalg.norm(V, axis=1).sum() + 1e-12))
    result = f"RESULT arrow=part{arrow} effdim={eff:.2f} coh={coh:.2f}".encode(); res_hash = sha(result)
    crr, nr = encode(result, D); M_a, cm2 = transmit_receive(crr, D, nr, 20.0, SIGMA); ret_ok = (M_a == result)

    out = {
        "system": "Hs Duplex — bidirectional compositional communication, compute-in-the-loop",
        "channel": "composition codeword; +/-20 dB common-mode gain (closure-rejected) + additive ILR noise",
        "common_mode_rejection_residual": max(cm1, cm2), "D_parts": D, "bits_per_composition": (D-1)*8,
        "additive_exact_decode_margin_xDelta": margin, "operating_noise_xDelta": 0.03,
        "FORWARD": {"message": instr.decode() + "<payload 32B>", "bytes": nf, "compositions": len(cf),
                    "hash": sha(M_fwd), "decoded_exact_at_B": bool(fwd_ok)},
        "B_OBSERVE_AND_COMPUTE": {"instruction": instr.decode(), "ran": "Hs kinematic read on the payload trajectory",
                    "reading": result.decode(), "arrow_part": arrow, "effdim": round(eff, 2), "coherence": round(coh, 2),
                    "result_hash": res_hash},
        "RETURN": {"message": result.decode(), "bytes": nr, "compositions": len(crr), "hash": res_hash,
                    "decoded_exact_at_A": bool(ret_ok)},
        "ROUND_TRIP_EXACT": bool(fwd_ok and ret_ok),
        "END_TO_END_INTEGRITY": "MATCH" if (sha(M_a) == res_hash and ret_ok) else "MISMATCH",
        "capacity_bits_per_composition_vs_D": {str(d): (d-1)*8 for d in [3, 4, 8, 16, 48]},
    }
    out["content_sha256"] = hashlib.sha256(json.dumps(out, sort_keys=True, default=str).encode()).hexdigest()
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
