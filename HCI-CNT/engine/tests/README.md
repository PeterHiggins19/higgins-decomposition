# Engine tests

Determinism + parity tests for the CNT engine.

| Test | Purpose |
|---|---|
| `test_determinism.py` | 3-experiment fast gate — same input twice ⇒ same `content_sha256` |
| `test_full_corpus.py` | 25-experiment full gate — runs the entire reference corpus |
| `test_parity.sh`      | Cross-language parity — Python vs R produce identical SHAs |

Run from inside `HCI-CNT/`:

```bash
python -m pytest engine/tests/test_determinism.py
python -m pytest engine/tests/test_full_corpus.py
bash engine/tests/test_parity.sh
```

The full-corpus test is the canonical determinism gate. It must pass
**25 / 25** before any release; this is enforced in the
[`PREPARE_FOR_REPO.json`](../../ai-refresh/PREPARE_FOR_REPO.json) push
checklist.

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
