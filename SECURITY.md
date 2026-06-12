# Security Policy

## Scope

This security policy covers:

* The Compositional Navigation Tensor (CNT) engine and atlas in [`HCI-CNT/`](HCI-CNT/).
* The Hˢ research pipeline tooling in `tools/` and `docs/`.
* The published reference experiments and their hash chains.

It does *not* cover third-party data sources referenced by adapters or
data-pointer files, nor any user code that builds on this repository.

## Reporting a vulnerability

For security issues — including, but not limited to:

* Vulnerabilities in the engine that could compromise determinism.
* Hash-chain integrity issues in published JSONs.
* Cases where reproducing a published result yields a different
  `content_sha256` despite identical inputs and config.

please email **peterhiggins@roguewaveaudio.com** rather than opening a
public issue. Include:

* A description of the issue.
* Reproduction steps if applicable.
* The relevant `content_sha256` (canonical) and the `content_sha256`
  you observed.
* Engine version (`metadata.engine_version`) and engine signature
  (`metadata.engine_config.engine_signature` or footer of any plate).

We will acknowledge within 7 days and aim to provide an initial
analysis within 30 days.

## Hash-chain verification

Anyone can verify any published result. The procedure is documented in
[`HCI-CNT/handbook/VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md`](HCI-CNT/handbook/VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md)
Part B (the verification appendix). The recipe is:

1. Get the raw CSV.
2. `sha256sum input.csv` → compare against `inp.source_file_sha256` in the JSON.
3. Run the engine: `python HCI-CNT/mission_command/mission_command.py <id>`.
4. Compare the recomputed `content_sha256` to the published value.

If the recomputed SHA matches, the result reproduces. If it doesn't,
that's a finding worth reporting.

## Supported versions

The current supported version is **engine 2.0.4 / schema 2.1.0**, as
shipped in `HCI-CNT/`. Older versions (2.0.0–2.0.3) are preserved in
the git history for traceability but receive no security updates.

| Version | Status | Last security review |
|---|---|---|
| 2.0.4 / 2.1.0 | Supported | 2026-05-06 |
| 2.0.3 / 2.0.0 | Historical | 2026-05-05 |
| < 2.0.3       | Unsupported | n/a |

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
