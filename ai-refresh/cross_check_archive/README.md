# Cross-Check Archive

Audit-trail folder for completed AI cross-check rounds. Each session is preserved verbatim with explicit findings categorisation: actioned / deferred / false-positive.

| File | Date | Source | Outcome |
|---|---|---|---|
| `grok_round_2_session_2026-05-08.md` | 2026-05-08 | Grok | Mixed — 3 valid engineering items, 1 stale-cache false-positive ("cnq.py does not exist"), commercialisation pathway DEFERRED |

Active cross-check rounds (the productive seams that produced canonical pushes) are recorded directly in the corresponding `AI_REFRESH_*.md` files at `ai-refresh/`. This archive folder is for retrospective preservation when a session produced mixed or partial results that don't fit a single push narrative.

## When to add to this archive

- Cross-check session produced a mix of valid + false findings → archive verbatim
- AI platform exhibited a new failure mode worth cataloguing → archive + add to INV-031
- Substantive content needs preservation for future use even if not immediately actioned → archive

## When NOT to use this archive

- Session produced clean canonical contributions → goes in a regular `AI_REFRESH_*.md` push narrative
- Session was pure conversation without findings → no need to archive

The Investigation Catalog (`ai-refresh/INVESTIGATION_CATALOG.md`) is the master index of where each cross-check round landed.
