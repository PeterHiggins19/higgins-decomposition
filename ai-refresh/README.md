# Hs AI Refresh

Machine-readable configuration files that maintain the repository's self-awareness.

These files serve as the **memory** of the Hs repository. Any AI assistant or contributor can read them to understand the current state of the project -- its identity, structure, file inventory, and push history -- without crawling the entire directory tree. They are the maintenance backbone: when the repository changes, these files are updated so that downstream tools and collaborators always have an accurate, centralised reference.

---

## Files

| File | Purpose |
|---|---|
| [HS_ADMIN.json](HS_ADMIN.json) | Identity authority (RWA-001). Contact information, licensing terms, and administrative metadata for the project owner. |
| [HS_GITHUB_CONFIG.json](HS_GITHUB_CONFIG.json) | Repository metadata. Push history, remote configuration, and SEO notes for the GitHub-hosted repository. |
| [HS_MACHINE_MANIFEST.json](HS_MACHINE_MANIFEST.json) | Complete system map. Catalogues every pipeline file, interactive tool, notebook, and architectural component in the repository. |
| [HS_SYSTEM_INVENTORY.json](HS_SYSTEM_INVENTORY.json) | File counts, experiment registry, and tool inventory. A quantitative snapshot of everything the repository contains. |
| [PREPARE_FOR_REPO.json](PREPARE_FOR_REPO.json) | Pre-push readiness checklist. Delta tracking, file verification, and the checklist used before each commit reaches the remote. |
| [AI_REFRESH_2026-04-27.md](AI_REFRESH_2026-04-27.md) | Human-readable changelog. A narrative summary of the most recent refresh, written for quick orientation. |

---

## How to use these files

1. **New AI session** -- read `HS_MACHINE_MANIFEST.json` first. It gives the full directory map so you know where everything lives.
2. **Quick audit** -- read `HS_SYSTEM_INVENTORY.json` for counts and the experiment registry.
3. **Before pushing** -- consult `PREPARE_FOR_REPO.json` to verify that all tracked files are present and accounted for.
4. **Identity and licensing** -- `HS_ADMIN.json` is the single source of truth.
5. **Recent changes** -- `AI_REFRESH_2026-04-27.md` provides a plain-language summary of the latest update.

Keeping these files current ensures that the repository remains navigable, reproducible, and self-documenting across sessions and contributors.

---

Peter Higgins / Rogue Wave Audio / CC BY 4.0
