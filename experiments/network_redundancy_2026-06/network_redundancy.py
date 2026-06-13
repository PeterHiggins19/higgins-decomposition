#!/usr/bin/env python3
"""Network cross-verification — any Hs node can check any other connected system.

The capability that generalizes the triple-channel reader from one box to a network.
The primitive is DETERMINISM: the same composition produces the same content hash on
any node, anywhere. So a node verifies a peer's read by recomputing it and comparing
the receipt. Heterogeneous devices (a gas mask reading {O2,CO2,N2,agent}, a geo probe
reading {SiO2,Al2O3,...}) both emit hash-receipted reads in the same form, so any node
with spare capacity can lend redundancy to any other. With N nodes, a majority vote
isolates a faulty node (RC-ISO-WRN) or halts (RC-HLT-ERR) — FDIR across a network.

This is "all just part of the way the system handles compositions, including itself":
the instrument that reads compositions can read the composition of its own readers.

Run:  python experiments/network_redundancy_2026-06/network_redundancy.py
"""
import sys, numpy as np
from pathlib import Path
from collections import Counter
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "HCI-CNTT" / "engine"))
import cntt


def node_read(data, carriers):
    """An Hs processor: read a composition -> deterministic content hash (the receipt)."""
    p = cntt.cntt_run(np.asarray(data, float), carriers=carriers)
    return p["diagnostics"]["cntt_content_sha256"]


def network_vote(hashes):
    """N-node FDIR: consensus / isolate the minority / halt if no majority."""
    c = Counter(hashes); maj, n = c.most_common(1)[0]
    if len(set(hashes)) == 1:
        return "RC-CON-INF", "network consensus (all nodes agree)", []
    faulty = [i for i, h in enumerate(hashes) if h != maj]
    if n > len(hashes) // 2:
        return "RC-ISO-WRN", f"isolate node(s) {faulty}; majority agrees", faulty
    return "RC-HLT-ERR", "no network majority -> halt-and-report (Safe-Operations safe state)", []


if __name__ == "__main__":
    gas = [[78, 16, 5, 1], [77, 17, 5, 1], [76, 18, 5, 1]]                 # gas mask: N2,O2,CO2,agent
    geo = [[60, 18, 8, 7, 4, 3], [58, 19, 9, 7, 4, 3], [61, 17, 8, 7, 4, 3]]  # geo probe: 6 oxides

    hA = node_read(gas, list("ABCD"))
    hB = node_read(gas, list("ABCD"))
    print("1. determinism = cross-verify primitive:")
    print(f"   node A {hA[:20]} == node B recompute {hB[:20]} -> {hA == hB}")

    hGeo = node_read(geo, list("PQRSTU"))
    print("2. heterogeneous nodes (any checks any):")
    print(f"   gas-mask receipt {hA[:20]} | geo-probe receipt {hGeo[:20]}")
    print(f"   geo-probe verifies gas-mask (recompute its input): {node_read(gas, list('ABCD')) == hA}")

    print("3. N-node fault isolation:")
    reads = [node_read(gas, list("ABCD")) for _ in range(5)]
    reads[3] = node_read([[78, 16, 5, 2], [77, 17, 5, 1], [76, 18, 5, 1]], list("ABCD"))  # node 3 corrupted
    code, msg, faulty = network_vote(reads)
    print(f"   5 nodes, node 3 faulty -> {code}: {msg}")
    print(f"   5 nodes, all clean     -> {network_vote([node_read(gas, list('ABCD')) for _ in range(5)])[0]}")
