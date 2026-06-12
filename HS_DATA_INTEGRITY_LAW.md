# Hˢ Data Integrity Law

## Instrument Status: Certified

The Hˢ Manifold Projector has been calibrated against five known geometric test objects (MC-4 series: cylinder, sphere, cube, cone, helix), each constructed from pure CoDa compositions and CLR-transformed using the standard Aitchison (1986) formula. The projected shapes match the expected geometry in every case. The instrument is certified.

From this point forward, the projector is not the subject of inquiry. The data is the Device Under Test.

## The Three Laws of Hˢ

### First Law — The Instrument Does Not Fabricate

The Hˢ Manifold Projector reveals the structure that exists within the data. It does not fabricate, adjust, or correct. If the projected shape does not match expectation, the data contains that structure. The instrument is not the source of error. The data is the anomaly. The anomaly is the finding.

### Second Law — Every Nibble Is Preserved

No data point is discarded, smoothed, interpolated, or suppressed by the instrument. Every carrier value at every timestep is projected, marked, or tagged. Where compositional structure exists, it is rendered as geometry. Where structure is absent (degenerate timesteps), a point marker shows the absence. Where a carrier is missing or suppressed, a marker tags the position. The projector conceals nothing. Every nibble of information reaches the output.

### Third Law — Confidence Is Stated

Every projection carries a certifiable chain of methodology:

1. **Closure** — Raw data is closed to constant sum (the simplex). Standard CoDa entry point. No methodological dispute exists.
2. **CLR Transform** — Centered Log-Ratio maps compositions to real coordinate space. Defined by Aitchison (1986), universally accepted in the CoDa community. No methodological dispute exists.
3. **Spline Assembly** — CLR trajectories across the time index are fitted to a cubic spline. Standard numerical interpolation. No data modification occurs.
4. **Per-Run Normalization** — CLR values are mapped to [0, 1] within each run using that run's own global min/max. This is a display scaling operation equivalent to choosing the zoom level on a microscope. It preserves within-timestep shape and between-timestep magnitude. It does not alter what the instrument observes.
5. **Projection** — Normalized CLR values are rendered as polar polygons stacked along the time axis. Vertex radius encodes CLR magnitude. Angle encodes carrier identity. This is direct geometric mapping with no fitting, filtering, or approximation.

At no point does any step modify, filter, or "improve" the data. The CoDa methodology chain is certifiable to CoDaWork standards. No known misstep exists in the data representation. The projection is Hˢ-certified and tested to this standard.

When the instrument is applied to real datasets, the confidence level is: **the methodology chain is sound, the instrument is calibrated, and the projection is a faithful geometric rendering of the compositional structure within the data.**

## The DUT Principle

In metrology, the Device Under Test is the object being measured. The measurement instrument is assumed correct once calibrated. The Hˢ projector has been calibrated. Therefore:

- The data is always the DUT. The projector is never the DUT.
- An unexpected shape is a finding about the data, not a defect of the instrument.
- An anomaly is the interesting part. It is the reason the instrument exists. The instrument exists to find what the data contains, especially what was not expected.
- The expert interprets the finding. The instrument does not interpret.

This is the operating posture for all Hˢ projections from this point forward. The question is never "is the projector showing the right thing?" The question is always "what is the data telling us?"

## Calibration Certificate

The MC-4 Shape Calibration series constitutes the instrument's type test:

| Test Object | Composition | Expected Projection | Result |
|-------------|-------------|---------------------|--------|
| Cylinder | Uniform at all timesteps | Constant circle through time | PASS |
| Sphere | CLR spread follows sin envelope | Circle expanding then contracting | PASS |
| Cube | Alternating high/low carrier quadrants | Square-like cross-section, constant | PASS |
| Cone | CLR spread linearly tapers | Circle shrinking from base to apex | PASS |
| Helix | Dominant carrier rotates over time | Polygon peak rotating around axis | PASS |

Each test object is constructed from legitimate compositions (proportions summing to 1), CLR-transformed, and projected without modification. All five pass. The instrument is calibrated.

## Boundary Condition Markers

The projector handles two boundary conditions that would otherwise produce misleading geometry:

**Degenerate Timesteps** — When all carriers at a given timestep have equal CLR values (spread below 1e-4), no compositional structure exists to project as a polygon. The projector renders a diamond-shaped point marker labeled DEGEN at the center axis. This occurs at mathematical singularities such as sphere poles where sin(0) = 0. The marker shows the singularity. It does not fabricate a polygon where no structure exists.

**Missing Carriers** — When a carrier's CLR value falls below -10 (indicating suppression or absence), the projector marks that vertex with a red X marker. The polygon is drawn using only the valid carriers. Hovering a missing carrier vertex displays "MISSING" instead of a CLR value. The absence is shown, not hidden.

These markers are diagnostic findings. A degenerate timestep in real data means the composition was uniform at that point — that is a finding. A missing carrier means a component was absent or below detection — that is a finding. The instrument shows what exists and marks what does not. Both are information. Neither is error.

## Carrier Lock Points

The transition from degenerate (no signal) to valid (signal present) defines the instrument's resolving boundary. This is not fabrication — it is standard metrological practice. Every measurement device has a noise floor and a signal acquisition threshold.

**Lock Acquisition (LOCK-ACQ)** — The first valid timestep following a degenerate timestep. The projector marks it with a green dashed ring and displays the exact CLR spread offset from zero. For the sphere standard, the lock acquisition at t=1 shows offset=0.125110. This is not zero. The instrument documents the exact distance from true zero where it first resolves compositional structure.

**Lock Loss (LOCK-LOSS)** — The last valid timestep before a degenerate timestep. The projector marks it with an amber dashed ring and displays the exact CLR spread offset. For the sphere standard, the lock loss at t=39 shows offset=0.125110 (symmetric with acquisition).

**The Out-of-Bounds Band** — The region between true zero (degenerate) and the lock point offset defines the instrument's resolving band. Within this band, compositional structure exists but is below the threshold where the projector can distinguish it from uniform. The offset value documents the width of this band. It is real data about the instrument's capability at that data point. It is not a correction, not an adjustment, not a fabrication. It is a measurement of the measurement boundary.

The lock point offset is always the actual computed CLR spread at that timestep. It is never rounded to 0 or 1. If it is 0.125110, it is displayed as 0.125110. The full positional documentation (timestep, carrier values, offset) is preserved.

## Standards Test Certificate

The Hs-STD Standards Test validates the complete instrument system on three known geometric objects:

| Test Object | Degenerate | Lock Points | Expected | Result |
|-------------|-----------|-------------|----------|--------|
| Cylinder | 41/41 | 0 | All DEGEN markers, no polygons | PASS |
| Sphere | 2/41 | 2 (ACQ t=1, LOSS t=39, offset=0.125110) | Expanding/contracting circle, DEGEN at poles | PASS |
| Cube | 0/41 | 0 | Square-like constant cross-section | PASS |

This supplements the MC-4 calibration (5/5 PASS) with boundary condition and lock point validation.

## Utility of Purpose

The Hˢ Manifold Projector exists to answer one question: **what structure does this compositional dataset contain?**

The methodology chain (closure, CLR, spline, projection) is built entirely from operations that the CoDa community has published, peer-reviewed, and accepted. The projection rendering is calibrated against known geometric objects. The degenerate and missing markers ensure that every data point, including the absence of data, reaches the output.

The instrument reads. The expert decides. The loop stays open.

This is the law of Hˢ.
