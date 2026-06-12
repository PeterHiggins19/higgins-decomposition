# Pedagogical Tables — Deep-Explanation Backup for the CoDaWork 2026 Talk

**Purpose:** Two step-by-step tables that map the spoken oratory and the slide content back to specific functions and modules in the published code. Use these to answer Q&A depth questions or to give curious audience members a clean path from "what does it do" to "where exactly does it do it."

**Reading order:**
1. Read SPEAKER_BRIEF.md once for the strategic frame.
2. Read README.md (oratory) for the spoken talk.
3. Read STUDY_PAGE.md for the moot-round drill.
4. Read CHEAT_SHEET.md for the backstage scanner.
5. **Use this file** when someone asks a depth question that wants the full pipeline shown.

The two tables below were drafted by Grok in round 6 (2026-05-12) using the cross-AI coordination protocol, then verified and refined against the live `hci_shared/` module surface.

---

## Table 1 — From Aitchison Geometry to SU(2) Double Cover

**Question this answers:** *"You keep saying the rotation 'lives in SU(2). Can you show me exactly how?"*

| Step | Geometric / Algebraic Concept | Explanation | CNT / CNQ Function / Module | Primary Output |
|---|---|---|---|---|
| 1 | **Compositional data on the simplex** | Any compositional vector (e.g., yearly electricity mix) lives on the probability simplex Δ^(D-1). For D=4 (or D=8 with twin-factoring), this is the 3-simplex (or twin 3-simplices). | `closure()` in `hci_shared/validation.py` | Closed composition **x** with Σxᵢ = 1 |
| 2 | **ILR / CLR transform** | The isometric log-ratio (Helmert) transform maps the simplex to Euclidean space ℝ^(D-1). For D=4, this gives a 3-D vector space. The geometry is now Euclidean. | `compositions_to_ilr()` and `clr()` in `hci_shared/geometry.py` | ILR vector **v** ∈ ℝ^(D-1) |
| 3 | **Compositional change = rotation in ILR space** | The difference between two consecutive compositional points corresponds to a rotation in the ILR-Euclidean space. The CNT engine computes this rotation geometrically using the Aitchison metric. | Angular-velocity computation in the CNT tensor block (`cnt.py`) | Angular velocity ω(t) + change vector |
| 4 | **CNT engine computes the rotation** | The CNT pipeline (seven operators: S, V, T, C, E, M, R) calculates the rotation using Aitchison geometry tools (bearing, variance trajectory, transcendental squeeze, classification, entropy test, mode synthesis, report). | Full pipeline in `HCI-CNT/engine/cnt.py` | 4-channel tensor: θ(t), ω(t), κ^(Hˢ)(t), σ(t) |
| 5 | **SO(3) describes the rotation** | All 3-D rotations form the group SO(3). However, SO(3) is topologically non-trivial — it has a non-simply-connected fundamental group. This is invisible to standard linear algebra. | Implicit in geometric calculation | Rotation matrix equivalent (3×3) |
| 6 | **SU(2) is the universal cover of SO(3)** | The group SU(2) of unit quaternions is the **double cover** of SO(3). Every SO(3) rotation corresponds to two quaternions: q and −q. This is the topology that lets handedness emerge as a sign. | `classify_dimension()` + quaternion mapping in `HCI-CNQ/engine/cnq.py` | Unit quaternion q(t) on S³ |
| 7 | **Sandwich product realises the rotation** | The actual rotation is performed by the sandwich product: v' = q · v · q*. This is the quaternion version of the Aitchison rotation, and the residual between the geometric and quaternion versions stays at IEEE machine floor (~2ε ≈ 4.4 × 10⁻¹⁶). | `quaternion_sandwich_residuals()` in `hci_shared/geometry.py` | Rotated ILR vector v'; sandwich residual |
| 8 | **Double cover introduces handedness** | Because q and −q give the same rotation in SO(3), the *sign* of the quaternion lift encodes handedness (spinor parity). This information is invisible in pure SO(3) but appears naturally in compositional paths. **This is the source of helmsman flips.** | Helmsman computation in `hci_shared/helmsman.py` | Helmsman channel σ(t) = ±1 |
| 9 | **CNQ layer names the algebra** | The CNQ engine reveals that the rotation computed geometrically by CNT actually lives in SU(2), not just SO(3). This explains the three simultaneous invariances (rotation, handedness, time-reversal) within one algebraic object. | Full `cnq.py` engine + dimension policy table | Quaternion view JSON + spectral invariants |
| 10 | **Three invariances unified** | The SU(2) structure simultaneously captures: **rotation** (sandwich product), **handedness** (helmsman / spinor parity), **time reversal** (conjugation q → q*). This is the central thesis of Volume IV. | Combined CNT + CNQ output JSON + provenance hashes | Full invariant tensor + content_sha256 + cnq_content_sha256 |

**Key insight (Peter's phrasing):** *In Aitchison geometry, a compositional change between two points on the 3-simplex corresponds to a rotation in the ILR space. The CNT engine computes this rotation geometrically. The CNQ layer reveals that this rotation lives naturally in SU(2) rather than just SO(3).*

This table makes that insight fully operational by showing exactly where and how each piece of the mathematics is implemented in the published code. The helmsman channel σ(t) is the practical manifestation of the double cover — it tells you which "sheet" of SU(2) the current compositional trajectory is travelling on, and when it flips sheets.

---

## Table 2 — Helmsman Attribution Logic (Step-by-Step)

**Question this answers:** *"Japan had 17 helmsman flips. What does that actually mean? Which carrier was steering when?"*

| Step | Operation | Explanation | Function / Module | Output |
|---|---|---|---|---|
| 1 | **Compute the instantaneous change vector** | After closure and ILR transform, the difference between consecutive points gives a vector in ℝ^(D-1). This is the raw "where did the composition just move" signal. | ILR transform + finite difference in `cnt.py` tensor block | Change vector Δv ∈ ℝ^(D-1) |
| 2 | **Identify the dominant axis of change** | The engine identifies the carrier (or linear combination) with the largest contribution to the current angular velocity ω(t). This is done via the sensitivity vector sⱼ produced inside the CNT tensor block. | Sensitivity-vector computation in `cnt.py` | Dominant-carrier identification |
| 3 | **Apply transcendental squeeze + entropy test** | These steps sharpen the attribution so that only the most influential carrier(s) receive credit. The squeeze is non-linear and the entropy test guards against spurious attribution when many carriers contribute equally. | `transcendental_squeeze()` + `entropy_test()` in `cnt.py` | Sharpened attribution scores |
| 4 | **Assign helmsman sign** | The sign of σ(t) is determined by the orientation of the change relative to the current basis. In the quaternion view, this is equivalent to the SU(2) lift sign — which sheet of the double cover the path is on. | `compute_helmsman_family()` in `hci_shared/helmsman.py` | σ(t) ∈ {−1, +1} |
| 5 | **Detect flips** | A flip is recorded whenever σ(t) ≠ σ(t−1) — a sign change. Total flips, rolling-window flips, and stability metric S_σ are reported. | Flip-counter logic in `helmsman.py` | flips.total, flips.rolling, stability_S_sigma |
| 6 | **Attribute flips to carriers** | Each flip is annotated with the dominant carrier (or carrier pair) at that timestep, giving carrier-level directional credit. | Attribution annotation in `cnt.py` output | Per-flip carrier label |

**Interpretation in the EMBERS country results:**

- **Japan (JPN): 17 helmsman flips after Fukushima.** Rapid switching between nuclear collapse and fossil-fuel surge — the "steering carrier" changes year by year as the post-2011 transition unfolds.

- **United Kingdom (GBR): 15 flips during coal exit.** Clear, repeated changes in which source was driving the transition as coal phased out and gas/renewables took up the slack.

- **Germany (DEU): 13 flips with high stability score (S_σ ≈ 0.43).** Fewer absolute flips but consistent handedness during the long deceptive drift — the same carriers (wind/solar) steadily steering the slow change. The stability score quantifies "are the flips concentrated in a small phase change, or spread evenly?"

The helmsman layer is what turns raw percentage changes into **attributed directional narratives** that policymakers can understand. The double-cover structure (Table 1, step 8) is the deep reason this attribution exists at all.

---

## How to use these tables at the lectern

If an audience member asks a deeper question than the slide deck covers, here is the cascade:

1. **"What is the helmsman?"** → Point at Table 2.
2. **"How does the rotation live in SU(2)?"** → Point at Table 1.
3. **"Where is this implemented?"** → Point at the function names in either table.
4. **"Show me a number."** → Sandwich residual at 4.4 × 10⁻¹⁶ for D=4, twin-factor coupling at ~5.9° for EMBER China D=8, CHSH S = 0.88 (independent verdict).
5. **"Can I reproduce it?"** → CCTT v1.0 + run_all_confirmations.py + verify_publication_results.py (REPRODUCIBILITY_CHECKLIST.md at the repo root).

These tables exist as backup. The talk is the priority. The tables are for the moment a sharp questioner wants to descend one more level. (Or, per Peter's correction in the ChatGPT session: *ascend* one more level.)

---

*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*
