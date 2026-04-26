# Hs-20: Conversation Drift Detection
## Applying Hˢ to AI Safety and Conversation Quality

### Concept

Every conversation is a compositional system. At any point, the "state" of a conversation
can be decomposed into carriers — topics, intents, technical depth, terminology, direction —
and those carriers form a composition on the simplex. As the conversation evolves, the
composition drifts. If the user said "apple" and the system is heading toward "orange,"
that drift is detectable in the compositional trajectory before the final output reveals
the mismatch.

### The Problem This Solves

AI systems are experiencing backlash when conversations drift — sometimes through user
manipulation (adversarial prompt injection, deceptive reframing) and sometimes through
model tendencies (sycophancy, topic slide, mode collapse). In both cases, the drift
happens gradually across many turns, and neither the user nor the AI notices until the
output is wrong, harmful, or off-target.

Current approaches to this problem are largely reactive: content filters, output classifiers,
and retrospective audits. Hˢ offers a structural approach: monitor the compositional
trajectory of the conversation in real time and flag when the trajectory's character changes.

### How Hˢ Applies

The tool does not track goals — it tracks trajectory. The user doesn't set a target
composition; the tool watches the compositional evolution and reports when it changes
character:

- **HVLD bowl**: conversation is integrating (getting richer, exploring)
- **HVLD hill**: conversation is segregating (narrowing, converging)
- **Stalls**: conversation has stopped moving compositionally (stuck)
- **Spikes**: sudden topic change (possible injection or mode shift)
- **Reversals**: back-and-forth oscillation (indecision or adversarial probing)

The per-carrier contribution shows WHAT is changing. The drift trend shows WHETHER the
change is accelerating or decelerating. The transfer entropy shows WHO is driving the
change — user or AI.

### Safety Applications

1. **User drift detection**: Flag when a conversation's composition drifts from its
   established pattern. A user gradually steering toward harmful content would show
   as a slow carrier shift — detectable before the content itself triggers filters.

2. **AI drift detection**: Flag when the AI's responses shift compositional character
   without user prompting. Sycophancy shows as the AI's carrier distribution converging
   toward the user's. Mode collapse shows as decreasing entropy.

3. **Adversarial detection**: Deliberate manipulation typically produces specific
   compositional signatures: rapid carrier shifts (spikes), reversals (probing for
   boundaries), or engineered stalls followed by sudden direction changes.

4. **Quality assurance**: In long conversations, the ratio-pair lattice reveals which
   aspects of the discussion remain coupled and which drift independently. A technical
   conversation where the formality/informality ratio becomes volatile may indicate
   the AI is losing calibration.

### This Experiment

We applied Hˢ to the Higgins Unity Framework project milestones — 18 timestamped text
entries spanning 2025 to April 2026. Each milestone was decomposed into 4 carriers:
Theory (mathematical concepts), Engineering (code/tools), Documentation (tracking/reporting),
and Discovery (findings/domains).

Results:
- Classification: NATURAL (the research process has the same transcendental fingerprint
  as the physical systems it studies)
- HVLD: hill, R² = 0.93 (project is segregating — narrowing toward delivery)
- Nearest constant: 1/(2π) at δ = 0.000197
- Dominant carrier: Theory (29.4%)
- Drift: increasing, driven by Engineering growth
- Most stable pair: ln(Documentation/Discovery) — every discovery gets documented
- Least stable pair: ln(Theory/Engineering) — the natural oscillation of research

### Implications

If Hˢ can detect the compositional trajectory of a research project and classify it
NATURAL, it can detect the compositional trajectory of any AI conversation and flag
when that trajectory deviates from natural conversational structure. A conversation
that classifies as INVESTIGATE or FLAG under the Transcendental Naturalness Hypothesis
may be structurally anomalous — either the user or the AI is behaving in a way that
natural conversations do not.

This is not content filtering. It is structural monitoring. The tool doesn't know what
the conversation is about — it reads the compositional balance of the discussion and
reports when that balance changes character. That distinction matters for privacy,
interpretability, and the separation between monitoring structure and monitoring content.

### Citation

Peter Higgins, April 2026. Higgins Decomposition applied to conversation drift detection.
First demonstrated on HUF project milestones. Proposed for AI safety applications.
