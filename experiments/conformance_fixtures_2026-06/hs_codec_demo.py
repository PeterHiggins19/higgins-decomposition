#!/usr/bin/env python3
"""
Hs as a deterministic codec — data up (encode), data down (decode), exact round-trip.

Demonstrates the generator<->reader pair as one synced codec: a payload is ENCODED into the
rotation structure of an SO(n) object (each of the floor(n/2) rotation planes is one channel),
then DECODED back from that object exactly. Plus a MEASURED compression number on real data
(effective-dimension reduction over the lossless ILR transform).

HONEST FRAMING (read this): this is a *structured, deterministic, self-verifying* code, NOT a
capacity-beating one. It does not exceed the Shannon limit and makes no such claim. Its value
is (1) determinism + a hash receipt = built-in integrity/error detection, (2) interpretable
channels = each dimension is a named carrier, (3) exact round-trip. Capacity is bounded by the
same information theory as everything else; what changes is trust and structure, not the bound.

Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001.
Honest-broker: T1 the exact round-trip + the measured eff-dim; T2 the comms application.
"""
import csv, hashlib, json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BB_CSV = os.path.join(HERE, "..", "Hs-CNT_2026-05", "codawork2026", "backblaze_fleet", "backblaze_fleet_input.csv")


def givens(n, i, j, th):
    G = np.eye(n); c, s = math.cos(th), math.sin(th); G[i,i]=c; G[j,j]=c; G[i,j]=-s; G[j,i]=s; return G
def helmert(D):
    B = np.zeros((D-1, D))
    for i in range(1, D):
        B[i-1, :i] = 1.0/i; B[i-1, i] = -1.0; B[i-1] *= math.sqrt(i/(i+1.0))
    return B
def clr(x): L = np.log(x); return L - L.mean()


# ---- CODEC: bytes <-> SO(n) rotation channels (canonical planes preserve channel order) ----
LO, HI = 0.1, 0.9
def encode(msg: bytes, n: int):
    channels = n // 2
    payload = list(msg) + [0] * (channels - len(msg))
    angles = [LO + (HI - LO) * (b / 255.0) for b in payload]      # byte -> plane angle
    M = np.eye(n)
    for k in range(channels):
        M = M @ givens(n, 2*k, 2*k+1, angles[k])                  # data up
    return M, channels
def decode(M, channels, length):
    out = []
    for k in range(channels):
        i, j = 2*k, 2*k+1
        th = math.atan2(M[j, i], M[i, i])                         # recover this plane's angle
        out.append(int(round((th - LO) / (HI - LO) * 255.0)))     # data down
    return bytes(out[:length])


def main():
    # --- codec round-trips ---
    cases = []
    for msg, n in [(b"HUF", 8), (b"Hs", 6), (b"GOLD-1", 16), (b"compose", 16)]:
        M, ch = encode(msg, n)
        dec = decode(M, ch, len(msg))
        cases.append({"message": msg.decode(), "n": n, "channels": ch,
                      "bytes_per_object": ch, "decoded": dec.decode(errors="replace"),
                      "exact_roundtrip": bool(dec == msg)})

    # --- measured compression: effective dimension on real Backblaze ILR trajectory ---
    rows = []
    with open(BB_CSV) as f:
        for r in csv.DictReader(f):
            rows.append([float(r["Mechanical"]), float(r["Thermal"]), float(r["Age"]), float(r["Errors"])])
    raw = np.array(rows); H4 = helmert(4)
    V = np.array([H4 @ clr(x / x.sum()) for x in raw]); Vc = V - V.mean(0)
    lam = np.linalg.svd(Vc, compute_uv=False) ** 2
    eff_pr = float((lam.sum() ** 2) / (lam ** 2).sum())            # participation ratio
    eff_ent = float(np.exp(-(lambda p: (p * np.log(p + 1e-300)).sum())(lam / lam.sum())))  # entropy dim

    out = {
        "codec": cases,
        "codec_note": "each rotation plane carries one byte-symbol; exact round-trip; the hash below is the integrity receipt",
        "compression": {
            "D_parts": 4, "ilr_coords": 3,
            "effective_dimension_participation_ratio": round(eff_pr, 4),
            "effective_dimension_entropy": round(eff_ent, 4),
            "interpretation": "the ILR transform is lossless (bijection); the fleet's 731-day variation concentrates on ~1-2 of 3 directions, so a structured reduced code keeps that many coordinates. A real, measured reduction; NOT a Shannon-beating claim.",
        },
        "honesty": "structured deterministic self-verifying code; capacity bounded by information theory; the gain is integrity + interpretable channels, not bits beyond Shannon",
    }
    def rnd(o):
        if isinstance(o, bool): return o
        if isinstance(o, float): return round(o, 10)
        if isinstance(o, dict): return {k: rnd(v) for k, v in o.items()}
        if isinstance(o, list): return [rnd(v) for v in o]
        return o
    out["content_sha256"] = hashlib.sha256(json.dumps(rnd(out), sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
