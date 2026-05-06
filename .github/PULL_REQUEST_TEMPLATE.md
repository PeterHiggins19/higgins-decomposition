## Summary

What does this pull request change, and why?

## Scope

- [ ] Documentation only
- [ ] Tooling / non-math code
- [ ] Adapter (new or updated pre-parser)
- [ ] Atlas plate or report
- [ ] Engine math (will shift `content_sha256` — requires version bump)
- [ ] Schema (additive — requires schema-version bump)
- [ ] Other (describe below)

## Verification

- [ ] `cd HCI-CNT && python tools/verify_package.py` → PACKAGE READY
- [ ] `cd HCI-CNT && python mission_command/mission_command.py` → all PASS
- [ ] If engine math changed: `cnt.R` parity test passes
- [ ] If a plate was added: it is tagged with its derivational order

## Issue link

Closes #

## Notes for reviewer

(anything specific to look at)
