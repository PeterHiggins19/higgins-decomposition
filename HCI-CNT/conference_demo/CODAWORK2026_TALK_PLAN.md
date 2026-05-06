# CodaWork 2026 — Talk Plan
### Compositional Navigation Tensor: a hash-traceable instrument for compositional dynamics

**Speaker:** Peter Higgins
**Format:** 15-minute presentation + 5-minute Q&A
**Date:** 2026-05-05 (preparation)

---

## Timing budget

| Section | Time | Slides | Why |
|---|---:|---:|---|
| §A  CNT introduction | 4:30 | 10 | Set the framework. Get to the demo with cushion. |
| §B  PDF live walkthrough | 8:00 | (no slides, live PDF) | Demonstrate working software. The strongest moment. |
| §C  Closing — 3D projector | 2:30 | (live HTML viewer) | End on motion. The most memorable visual. |
| **Total presentation** | **15:00** | | 30-sec safety cushion built in |
| §D  Q&A | 5:00 | (no slides) | |

**One-line goal of the talk:** "Here is a deterministic, hash-chained
diagnostic instrument for compositional trajectories that ships
classical CoDa plates inside a single audit-grade report."

---

## §A  Slide deck (10 slides, 4:30 total)

Speaker-note convention: **bold = on slide**; plain text = spoken.

### Slide 1 — Title (~ 25 sec)
**Compositional Navigation Tensor**
*A hash-traceable instrument for compositional dynamics*
Peter Higgins  ·  CodaWork 2026

> "I'm going to show you an instrument my team built that takes the
> classical CoDa toolkit, wraps it in a deterministic engine, adds
> trajectory-native operators, and produces hash-chained reports.
> Every plate you'll see in the demo can be re-verified by anyone
> with the raw CSV in two minutes. That's the whole talk."

### Slide 2 — Value to the CoDa community (~ 30 sec)
**Three additions CNT brings to the established CoDa toolkit:**
- Trajectory-native operators (bearings, ω, helmsman, period-2 attractor, IR class)
- End-to-end determinism (raw CSV → JSON → PDF, byte-identical)
- Cross-dataset structural comparison (Stage 4 reports)

**These ship alongside the classical plates — both languages, one report.** Variation
matrix, biplot, balance dendrogram, SBP, ternary, scree are all
in the report — same engine.

> "The framing matters: this isn't a replacement for ILR or the
> classical biplot. It's an extension that ships those plates plus
> the trajectory-native ones in one report — both languages, one
> document."

### Slide 3 — Math step 1: Closure to the simplex (~ 25 sec)
**x ← x / Σx     (with δ-replacement for zeros)**

Diagram: dollar-share / mass-fraction / energy-share rows → simplex points.

> "Standard closure operator. The δ value is in the JSON's
> engine_config.DEFAULT_DELTA. Anyone re-running with a different
> δ produces a different content_sha256 — by design."

### Slide 4 — Math step 2: CLR transform (~ 25 sec)
**clr(x)_j = ln(x_j) − ⟨ln x⟩**

Diagram: simplex points → centred log-ratio space (zero-mean rows).

> "Aitchison's centred log-ratio. Dimension D, but constrained to
> Σ clr_j = 0, so D-1 degrees of freedom."

### Slide 5 — Math step 3: Helmert ILR basis (~ 30 sec)
**ilr(x) = V · clr(x)**

Diagram: D × D Helmert basis schematic; clr → ilr in (D-1) dims.

> "Egozcue's orthonormal Helmert basis. Same as classical CoDa.
> What's different is what we do next."

### Slide 6 — Math step 4: Bearing tensor (atan2 simplification) (~ 35 sec)
**θ_{i,j}(t) = atan2(y_{i,j}, x_{i,j})**

Side by side:
- arccos((u·v)/(|u||v|)) → 12 ops, sign loss, √ε noise floor near 0/π
- atan2 → 4 ops, [-π, π], machine precision

> "Pairwise bearings via atan2. Three-times-fewer ops, 10⁷-times
> better stability near locks. The bearing tensor is what makes
> trajectory-native operators tractable."

### Slide 7 — Math step 5: Metric tensor and M² = I (~ 35 sec)
**M(x) — D × D metric tensor**
**M² = I — verified per timestep, mean residual ≈ 1e-15**

Diagram: M ∘ M = I; residual histogram showing peak at IEEE floor.

> "The metric-dual involution. We compute M's dual, square it,
> verify it's the identity at IEEE floor. This is what lets the
> depth tower be Banach-contractive."

### Slide 8 — Math step 6: Depth tower (recursion) (~ 35 sec)
**Energy tower    ω(level), Hs(level)**
**Curvature tower ω(level), Hs(level)**

Diagram: trajectory of (ω, Hs) per level, each iteration one step deeper.

> "Recursive depth sounder. Two towers — energy and curvature.
> Each level applies the metric-dual; convergence shows up as ω
> dropping to the noise floor."

### Slide 9 — Math step 7: Period-2 attractor & IR classification (~ 35 sec)
**Convergence → period-2 attractor (c_even, c_odd, amplitude A)**
**Eight IR classes** (CRITICALLY / LIGHTLY / MODERATELY / OVERDAMPED + 4 edge cases)

Diagram: amplitude-A reference band with the 8 classes coloured.

> "The depth tower converges to a period-2 attractor whose amplitude
> A is the headline diagnostic. The eight-class taxonomy lives in
> the engine and the JSON. Every class has an interpretation rule."

### Slide 10 — One picture summary (~ 30 sec)
**raw CSV → JSON → 4 stages of PDF report**
**Stage 1: per-timestep | Stage 2: geometry+dynamics 28 plates**
**Stage 3: depth+attractor 11 plates | Stage 4: cross-dataset 11 plates**
**Every page footer carries: engine sig, content SHA, source SHA, date**

> "Here's what comes out the other end. Four stages. Hash chain on
> every page. Now I'm going to show you the actual PDFs."

---

## §B  PDF demo (8 min, no slides)

Open `codawork2026_conference/cnt_demo/02_per_country/ember_jpn/stage2_ember_jpn.pdf`
on the projector in full-screen mode. Have the file already open
and at page 1 to avoid fumbling.

### Walkthrough — choose 5 dwell pages (~ 90 sec each)

**Dwell 1 — Cover page (page 1)**
Talking points:
- "Compositional system geometry and dynamics for, Japan — EMBER electricity generation 2000-2025"
- Auto-generated title from dataset_id
- The traceability block: engine version, engine signature, source SHA, content SHA — all on this one page
- The reading-order map at the bottom: §A disclosure → §B geometry → §C dynamics → §D summary

**Dwell 2 — Data disclosure (page 2)**
Talking points:
- "This is what page 2 of every report looks like — before any analysis"
- Walk down the columns: source SHA, ordering, zero-replacement (δ value visible), units lineage, active engine_config_overrides, lock event count, EITT residuals
- "If any flag is non-empty, the analysis still ran but the reader knows to weight downstream plates accordingly"
- "This is the page that protects you, the author, from accusations later"

**Dwell 3 — Evolution of proportions + ternary (pages 3–4)**
Talking points:
- "Geometry first, basic to advanced"
- Page 3: top is per-carrier line plot, bottom is cumulative stacked area — same data, two views, both Order 1
- Page 4: top-3 ternary with colour-coded time trajectory — Japan's Solar/Wind/Hydro share trajectory through 2000-2025; the post-Fukushima shift is visible

**Dwell 4 — Biplot + balance dendrogram (pages 9 + 11)**
Talking points:
- Page 9: classical CoDa biplot — ray length = carrier importance, angle = log-ratio correlation
- "I'm showing this so the reviewers from the Pawlowsky-Egozcue tradition see we ship the standard plate, computed from the same engine"
- Page 11: Ward dendrogram on the variation matrix — data-driven SBP, not a hand-picked one

**Dwell 5 — System Course Plot + CBS (pages 16 + 25)**
Talking points:
- Page 16: System Course Plot from the Math Handbook Ch 15 — V_net (start → end vector), course directness, PCA path
- Page 25: Compositional Bearing Scope, three orthogonal faces (θ × d_A, θ × κ, d_A × κ)
- "These are the trajectory-native operators CNT adds on top of the established CoDa toolkit"

### Quick scroll through Stage 3 + Stage 4 (~ 60 sec total)

Open Stage 3 (`stage3_ember_jpn.pdf`) — 11 pages — flip through:
- Cover, depth-tower convergence, period-2 attractor card, IR classification card
- "This is Order 3 — the depth tower / IR / attractor view"

Open Stage 4 (`stage4_codawork2026_ember.pdf`) — 11 pages — flip through:
- Per-dataset summary table, cross-dataset amplitude A bar chart, IR-class distribution
- "This is Order 4 — comparing the 8 EMBER countries side by side in one report"

### Close the demo
- "Every PDF you've just seen was generated by `python tools/run_pipeline.py codawork2026_ember`"
- "The full corpus — 25 experiments — runs deterministic in 21 seconds"

---

## §C  Closing — 3D projector (3 min, live HTML)

Open `codawork2026_conference/cnt_demo/03_combined/plate_time_projector_codawork2026_ember.html`
in the browser, full-screen.

Set the dropdown to "◆ ALL COMBINED (shared PCA frame)".

### Talking arc (~ 3 min)

Open with — "I want to leave you with one image."
Click and drag to start the orbit.

> *[Orbiting view, 30 sec]*
> "What you're looking at is 8 EMBER countries' 26-year electricity-mix
> trajectories projected into one shared PCA frame. The barycenter
> of the simplex is the z-axis spine running vertically through the
> middle. Each year is a horizontal slice. Each country is a coloured
> trajectory winding through that stack."

> *[Pause orbit; scrub year slider from 2000 → 2025, 60 sec]*
> "Watch what happens as I scrub forward in time. China climbs in
> coal. Germany drifts toward Solar/Wind. France stays anchored at
> Nuclear. Japan's pre-2011 trajectory is steady, then 2011 hits and
> Nuclear collapses; the trajectory makes a sharp right turn. The
> shape of each country's history is now a 3D curve."

> *[Toggle layers off/on — Trajectory, Carrier rays, Pair edges, 60 sec]*
> "Every line you see is one of five known relationships:
> consecutive-year trajectory, carrier rays from the barycenter,
> pair edges where Pearson r exceeds your threshold, helmsman links,
> lock events. Every one of them traces back to a specific JSON
> field. There are no fabricated connections."

> *[Lock back to ISO view, last 30 sec]*
> "This is the system. Engine 2.0.4, schema 2.1.0, twenty-five
> reference experiments, all reproducing byte-identically. The
> conference package — engine, per-country reports, combined views,
> calibration, doctrine — is one folder, fully self-contained.
> The papers, the engine, the reports, the determinism gate — all
> in the GitHub repo. The instrument reads. The expert decides.
> Thank you."

[Cue: pause for applause; transition to Q&A]

---

## §D  Q&A — 15-question study list

For each: a short answer (~ 20 sec spoken) and a one-line
"if pressed" follow-up. Prepare to answer in 30 seconds or less.

### Q1. "Is CNT a replacement for ILR or an extension?"
**Short:** Extension. The Helmert basis from Egozcue 2003 is the
foundational projection; CNT operates *on top* of ILR coordinates
to compute trajectory-native quantities (bearings, ω, helmsman).
**If pressed:** "Every CNT JSON contains the canonical ILR — you
could ignore everything Higgins-tagged and still use the report
as a classical CoDa pipeline output."

### Q2. "What does the Higgins scale add over the neper?"
**Short:** Nothing physically — it's measured in nepers by
default. The schema 2.1.0 `metadata.units` block just records
which unit (`ratio`, `bit`, `dB_power`, etc.) the input was in
and the conversion factor to neper.
**If pressed:** "The scale's value is in the unit lineage being
auditable, not in a different number space."

### Q3. "How is the bearing tensor different from log-ratio
differences?"
**Short:** Same information, different representation. The bearing
is the angle between two carriers' centred coordinates via atan2;
the log-ratio difference is the magnitude of the same vector. CNT
keeps both because the angular form is what makes period-2
attractor detection clean.
**If pressed:** "Bearing's distribution over carrier-pairs is the
'rose'; the log-ratio's distribution is what the variation matrix
shows. They're the polar and Cartesian readings of the same field."

### Q4. "Why integer orders only? Couldn't trajectory aggregates
be Order 1.5?"
**Short:** Doctrine choice. We round trajectory aggregates UP to
Order 2 because they aggregate across multiple timesteps.
Half-orders would be a category mistake — there's no such thing as
"half a recursion."
**If pressed:** "We considered fractional orders early on. They
made the doctrine harder to teach without buying any clarity in
the diagnostics."

### Q5. "What does the period-2 attractor mean physically?"
**Short:** It means the depth tower's recursion converges to two
alternating compositional states. The amplitude A is the gap
between them in Hs space. For most well-conditioned compositional
trajectories, A is small (CRITICALLY_DAMPED); for trajectories
with carrier phase-out, A is large (OVERDAMPED).
**If pressed:** "It's not a physical limit cycle of the original
data — it's the limit cycle of the metric-dual recursion. The
amplitude is structural."

### Q6. "How is zero-replacement handled differently from standard
practice?"
**Short:** The δ value is in `metadata.engine_config.DEFAULT_DELTA`
and any per-call override is in `active_overrides`. Different δ →
different content_sha256, by design. So the choice is auditable.
**If pressed:** "We don't claim to solve the zero problem; we
claim to disclose how we addressed it."

### Q7. "Can the engine handle very high-D problems? Genomics
datasets are D > 100."
**Short:** The math scales. The bottleneck for high D is plate
clutter — at D > 8 the full biplot starts to crowd, which is why
we ship `p_biplot_topN`. We've tested up to D = 10 on financial
data; D > 50 hasn't been benchmarked but should run.
**If pressed:** "If you have a high-D problem we'd love a test
case to add to the corpus."

### Q8. "How does CNT compare to van den Boogaart's compositions
package in R?"
**Short:** Different scopes. compositions is the canonical R
toolkit for static-snapshot CoDa; CNT is built around trajectory
dynamics with a deterministic engine. They're complementary —
the cnt.R port is parity-tested against the Python engine and
honours the same schema.
**If pressed:** "For single-snapshot work, compositions is the simplest path. If it's trajectory-native, CNT is the differentiator."

### Q9. "What's the engine's computational cost?"
**Short:** Engine pass is ~120 ms per dataset for typical T = 26,
D = 8. Stage 1 + 2 + 3 atlas adds ~5 s rendering. Full 25-experiment
corpus runs in ~21 seconds with the determinism gate.
**If pressed:** "Memory peak is ~35 MB; not GPU-bound; trivially
parallelisable across datasets."

### Q10. "Is the R port at full parity with Python?"
**Short:** Yes — engine 2.0.4 / schema 2.1.0 in both. Parity test
in `tests/test_parity.sh` confirms identical content_sha256 from
the two implementations on the same inputs.
**If pressed:** "Some atlas modules are Python-only; the R port
covers the engine + JSON output."

### Q11. "Why use a SHA chain instead of just publishing the
script?"
**Short:** Because scripts mutate. The hash chain pins the bits.
A reviewer who has the raw CSV plus the published content_sha256
can verify in two minutes; reading and trusting a script takes
hours and assumes the script you read is the script that ran.
**If pressed:** "The chain doesn't replace the script — it
authenticates which version of the script ran, when, and on what."

### Q12. "Can I integrate it with my existing ILR pipeline?"
**Short:** Yes. The JSON's `coda_standard` block carries the
canonical ILR, CLR, variation matrix, etc. — read those into your
existing pipeline and ignore the `higgins_extensions`. The schema
is open and stable.
**If pressed:** "We've designed the dual-classification (CoDa
standard / Higgins extensions) precisely so the engine doesn't
force adoption of the extension layer."

### Q13. "When does the engine fail or refuse to produce output?"
**Short:** Three cases. (1) D = 2 — the depth tower can't exercise
off-diagonal metric structure; flagged D2_DEGENERATE. (2) Single
carrier > 60 % — flagged CURVATURE_VERTEX_FLAT. (3) M² ≠ I
beyond floating-point error — flagged in `involution_proof`. None
of these halt; all of them annotate.
**If pressed:** "The engine's discipline is annotate, never crash.
Disclosure trumps refusal."

### Q14. "Is the Helmert basis a fixed choice or can users pick
their own SBP?"
**Short:** The engine emits the Helmert basis as the canonical
ILR. The Stage 2 atlas separately computes a data-driven SBP via
Ward clustering on the variation matrix and shows it as a
balance dendrogram + SBP-table plate. So users see both: the
canonical ILR and the data-driven balance hierarchy.
**If pressed:** "User-supplied SBP is a v1.2 candidate; the
schema has the slot reserved."

### Q15. "What's the licence and how do I get the system?"
**Short:** Apache-2.0. GitHub repo at the URL on the title slide.
The conference package is one folder, fully self-contained:
engine source, per-country reports, combined views, calibration,
doctrine. `pip install -e .` runs the full demo.
**If pressed:** "Patent grant included. We want this used."

---

## Pre-talk preparation checklist

The morning of the talk:

- [ ] Test the projector with the full Stage 2 PDF in full-screen
- [ ] Test the HTML projector in browser; pre-set ISO view + scrub to year 2010
- [ ] Have backup copies on USB and on a cloud drive
- [ ] Print this plan as a single page for the lectern
- [ ] Check microphone before stepping up — practice voice level
- [ ] Drink water, breathe, remember: the work is solid; you're
      reporting on it, not auditioning

Practice once front-to-back the night before with a watch
running. Aim for 14:30. If you finish early, that's better than
running over.

---

*The instrument reads. The expert decides. The hashes hold the line.*
