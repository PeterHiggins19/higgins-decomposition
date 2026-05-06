# Contributing to Higgins Decomposition (Hˢ)

Thank you for your interest in contributing to Hˢ. This project is a
deterministic compositional inference instrument with strict reproducibility
requirements; the contribution process reflects that.

## Quick orientation

* The Hˢ research line lives in the top-level folders (`HCI/`, `experiments/`,
  `data/`, `papers/`, `tools/`, `docs/`).
* The Compositional Navigation Tensor (CNT) subsystem lives in
  [`HCI-CNT/`](HCI-CNT/) and is documented across three handbook volumes
  in [`HCI-CNT/handbook/`](HCI-CNT/handbook/).
* Per-experiment audit records (input CSV → canonical JSON → journal) live
  under `experiments/` (Hˢ side) and `HCI-CNT/experiments/` (CNT side).

If you are unfamiliar with the project, please read these first:

1. [`README.md`](README.md) — entry point and project map.
2. [`HS_DATA_INTEGRITY_LAW.md`](HS_DATA_INTEGRITY_LAW.md) — the three laws
   that govern every change.
3. [`HCI-CNT/handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md`](HCI-CNT/handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md) —
   the math foundations.

## What kinds of contributions are welcome

* **Bug reports** — using the GitHub issue templates.
* **Reproducibility checks** — independent verification of any published
  result. The hash chain in every CNT JSON output makes this a two-minute
  exercise; we welcome reports either way (match or mismatch).
* **Adapter contributions** — new pre-parsers for compositional datasets.
  See [`HCI-CNT/handbook/VOLUME_2_PRACTITIONER_AND_OPERATIONS.md`](HCI-CNT/handbook/VOLUME_2_PRACTITIONER_AND_OPERATIONS.md)
  Part C for the disclosure requirements.
* **Documentation improvements** — clarifications, typo fixes, examples.
* **Math review** — corrections or extensions of the theory in Volume I.

## What changes need a heavier review

Anything that touches the engine math (`HCI-CNT/engine/cnt.py`,
`HCI-CNT/engine/cnt.R`), the schema, or the doctrine. These changes
shift `content_sha256` values across the corpus and break the
determinism gate, so they require:

* A justified explanation of why the change is needed.
* A version bump (engine and/or schema, depending on scope).
* A regenerated determinism gate run (25 PASS / 0 FAIL / 0 ERR).
* An updated entry in the appropriate volume of the handbook.

## How to submit a contribution

1. **Open an issue** describing the proposed change, *before* opening a
   pull request. This keeps coordination low-friction.
2. **Fork the repository** and make your change on a feature branch.
3. **Run the verifier** locally:
   ```bash
   cd HCI-CNT
   python tools/verify_package.py     # → PACKAGE READY
   python mission_command/mission_command.py    # → 25 PASS / 0 FAIL / 0 ERR
   ```
4. **Open a pull request** referencing the issue you opened in step 1.
   Use the PR template.

## What we look for in a pull request

* The local verifier passes.
* The change is consistent with the doctrine in Volume I §G
  (integer orders, round-up rule).
* If you added a plate, it is tagged with its derivational order.
* If you changed any engine constant, the change is reflected in
  every output JSON's `metadata.engine_config` block.
* If you wrote new prose, it follows the supportive-toward-classical-CoDa
  framing established in Volume I §I (the balance book).

## Licensing

The Hˢ research repository is licensed under **CC BY 4.0**. The
`HCI-CNT/` subsystem ships under **Apache-2.0** (allowing commercial
re-use of the engine and atlas). By submitting a contribution you
agree that your contribution is licensed under the same terms as the
file or folder you are modifying.

## Code of conduct

All contributors are expected to follow the
[Code of Conduct](CODE_OF_CONDUCT.md). Reports of unacceptable
behaviour go to **peterhiggins@roguewaveaudio.com**.

## Security

For security issues (vulnerabilities, data integrity concerns), please see
[SECURITY.md](SECURITY.md) — *do not* open public issues for these.

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
