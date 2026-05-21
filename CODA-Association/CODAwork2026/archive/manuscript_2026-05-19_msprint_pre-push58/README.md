# Archived manuscript renders — 2026-05-19 (kept for reference)

**Archived:** 2026-05-20 (then **restored to working copy 2026-05-20** — see Note below)
**Original purpose of the archive:** these two files (`.docx` + Microsoft Print To PDF rendered `.pdf`, 26 pp) were at one point thought to be stale renders that should be replaced by the LibreOffice canonical build at `papers/codawork2026/manuscript/output/`.

**Note (2026-05-20, second pass).** On closer inspection the Microsoft Print To PDF rendered `.pdf` is actually **superior** to the LibreOffice canonical export: it has a **fully populated Table of Contents** with section page numbers, while the LibreOffice headless export ships with the un-populated TOC placeholder text. Word populates the TOC fields on document open before printing; LibreOffice does not.

**Final policy:**
- `CODA-Association/CODAwork2026/Compositional_Monitoring_2026.pdf` ← the MS Print To PDF render with populated TOC (this is the conference distribution version).
- `CODA-Association/CODAwork2026/Compositional_Monitoring_2026.docx` ← byte-identical to `papers/codawork2026/manuscript/output/Compositional_Monitoring_2026.docx`.
- `papers/codawork2026/manuscript/output/Compositional_Monitoring_2026.pdf` ← LibreOffice canonical build artefact, retains the un-populated TOC. Acceptable for build-pipeline reproducibility records but **not for conference distribution**.
- `CODA-Association/CODAwork2026/archive/manuscript_2026-05-19_libreoffice_empty_toc/Compositional_Monitoring_2026.pdf` ← copy of the LibreOffice export, parked here for traceability.

**To-do post-conference.** Update `papers/codawork2026/manuscript/build/build_docx.js` (or the headless export pipeline) so the canonical PDF render also produces a populated TOC — closes the policy gap that lets the canonical artefact differ from the distribution artefact.

The original files in this folder are the same content as the current working copy; preserved as a fallback in case the working copy is accidentally overwritten.

---

*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*
