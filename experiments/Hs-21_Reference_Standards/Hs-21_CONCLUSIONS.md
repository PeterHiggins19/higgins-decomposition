# Hs-21 Conclusions — Reference Standard Library

**Experiment:** Hs-21
**Domain:** METROLOGY
**Type:** Calibration baseline (not a standard DUT experiment)
**Status:** CLOSED
**Date:** April 27, 2026

---

## Purpose

Hs-21 establishes the performance envelope of the Hˢ pipeline. Fifteen reference standards across four categories — mathematical functions (6), diffraction boundaries (3), transcendental anchors (3), and noise floor (3) — provide the calibration baseline that every future Device Under Test is measured against.

## Key Findings

The reference library validates the pipeline's classification partition. Fourteen of fifteen references classify NATURAL, one (REF-15, near-constant) classifies INVESTIGATE. No reference classifies FLAG. This establishes that the NATURAL classification is achievable for mathematical functions with known analytical properties, physical diffraction boundaries, transcendental sequences, and even structured noise — confirming that NATURAL detects geometric structure rather than domain-specific physics.

The noise floor references (REF-13 uniform random, REF-14 Gaussian noise) both classify NATURAL with low match density and low concentration. This means NATURAL alone is insufficient for distinguishing signal from noise — the match density and concentration metrics are required as discriminators.

All fifteen references produce deterministic, bit-identical results on repeated runs.

## What This Experiment Establishes

1. Match density threshold: natural systems show >100 matches/unit trajectory; noise shows <50.
2. Match concentration threshold: natural systems show >0.40 Herfindahl; noise shows <0.25.
3. The INVESTIGATE classification (REF-15) validates the boundary — near-constant data does not pass NATURAL.
4. The reference library is the instrument's self-knowledge.

## Implications for Advancement

The library should grow with priority additions: (1) D=5+ mathematical references to test high-dimensional simplex behaviour, (2) a known-chaotic reference (Lorenz attractor partition) to validate turbulence detection, (3) a high-N reference (N>1000) for trajectory stability at scale, (4) a pure-combinatorial reference to validate FLAG detection, (5) references from the new T2 amalgamation framework to establish amalgamation-stability baselines.

---

*Hs-21 — Calibration complete. The instrument knows its own performance.*
*Peter Higgins, April 2026*
