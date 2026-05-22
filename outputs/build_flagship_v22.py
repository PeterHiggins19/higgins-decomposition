"""Build flagship v2.2 PDF (and docx via pandoc) from the consolidated markdown.

v2.2 folds the eight gaps surfaced by the RWA cross-check into v2.1. Rather
than reproduce the full styled docx-js builder for v2.1, this v2.2 builder
renders the consolidated markdown to a PDF that matches the Hˢ flagship
visual identity (navy headings, gold rules, cream equation blocks).

The v2.1 docx remains alongside as the styled reference; v2.2 supplies
the complete consolidated content as PDF + pandoc-built docx.
"""
import subprocess, os, re
from weasyprint import HTML, CSS
import markdown as md

MD_PATH = "/sessions/epic-gracious-lovelace/mnt/Claude CoWorker/Current-Repo/Hs/papers/flagship/GROUND_STATE_AND_TRACTION.md"
OUT_PDF = "/sessions/epic-gracious-lovelace/mnt/Claude CoWorker/Current-Repo/Hs/papers/flagship/GROUND_STATE_AND_TRACTION_v2.2.pdf"
OUT_DOCX = "/sessions/epic-gracious-lovelace/mnt/Claude CoWorker/Current-Repo/Hs/papers/flagship/GROUND_STATE_AND_TRACTION_v2.2.docx"

src = open(MD_PATH, 'r', encoding='utf-8').read()

# Convert markdown to HTML with table + fenced-code + footnotes support
md_extensions = ['tables', 'fenced_code', 'footnotes', 'attr_list', 'def_list']
body_html = md.markdown(src, extensions=md_extensions)

# Add wrapper + CSS
CSS_STR = """
@page {
    size: A4;
    margin: 18mm 18mm 18mm 18mm;
    @top-left { content: "Ground State and the Traction Engine"; font-family: Calibri, sans-serif; font-size: 9pt; font-style: italic; color: #555; }
    @top-right { content: "Hˢ Flagship · Master Standard v2.2"; font-family: Calibri, sans-serif; font-size: 9pt; color: #555; }
    @bottom-left { content: "Peter Higgins · Rogue Wave Audio · Binaural Test Lab"; font-family: Calibri, sans-serif; font-size: 9pt; color: #555; }
    @bottom-center { content: "page " counter(page); font-family: Calibri, sans-serif; font-size: 9pt; color: #555; }
    @bottom-right { content: "2026-05-22"; font-family: Calibri, sans-serif; font-size: 9pt; color: #555; }
}
@page :first {
    @top-left { content: ""; }
    @top-right { content: ""; }
    @bottom-left { content: ""; }
    @bottom-center { content: ""; }
    @bottom-right { content: ""; }
}
body { font-family: Calibri, "Helvetica", sans-serif; color: #1a1a1a; font-size: 11pt; line-height: 1.42; }
h1 { font-family: Calibri, sans-serif; color: #1f3a5f; font-size: 22pt; font-weight: bold; margin: 24pt 0 8pt 0; page-break-before: always; page-break-after: avoid; }
h1:first-of-type { page-break-before: avoid; font-size: 28pt; text-align: center; margin-top: 0; border-bottom: 2pt solid #9a7b3f; padding-bottom: 8pt; }
h2 { font-family: Calibri, sans-serif; color: #1f3a5f; font-size: 16pt; font-weight: bold; margin: 16pt 0 6pt 0; page-break-after: avoid; }
h3 { font-family: Calibri, sans-serif; color: #1f3a5f; font-size: 13pt; font-weight: bold; margin: 12pt 0 4pt 0; page-break-after: avoid; }
p { margin: 6pt 0; text-align: justify; hyphens: auto; }
blockquote { border-left: 3pt solid #9a7b3f; background: #f5f2ec; padding: 8pt 14pt; margin: 10pt 0; color: #1a1a1a; font-style: normal; }
blockquote p { margin: 4pt 0; }
strong { color: #1f3a5f; }
em { color: #444; }
code { font-family: Consolas, "Courier New", monospace; background: #f1f4f8; padding: 0 3pt; border-radius: 2pt; font-size: 9.5pt; color: #1a1a1a; }
pre { background: #f5f2ec; border-top: 2pt solid #9a7b3f; border-bottom: 2pt solid #9a7b3f; padding: 8pt 14pt; margin: 10pt 0; font-family: Consolas, "Courier New", monospace; font-size: 9pt; line-height: 1.35; overflow-x: auto; page-break-inside: avoid; }
pre code { background: none; padding: 0; font-size: 9pt; }
table { width: 100%; border-collapse: collapse; margin: 8pt 0; font-size: 10pt; page-break-inside: avoid; }
th { background: #1f3a5f; color: white; font-weight: bold; padding: 5pt 7pt; text-align: left; font-size: 9.5pt; }
td { padding: 4pt 7pt; border-bottom: 0.5pt solid #cfd8e0; vertical-align: top; }
tr:nth-child(even) td { background: #f9fbfd; }
hr { border: none; border-top: 1pt solid #9a7b3f; margin: 14pt 0; }
ul, ol { margin: 6pt 0; padding-left: 24pt; }
li { margin: 3pt 0; }
a { color: #1f3a5f; text-decoration: none; }
.subtitle { font-style: italic; color: #555; }
"""

# Wrap in proper HTML
html_doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>The Isotropic Radiation Ground State and the Traction Engine — v2.2</title>
<style>{CSS_STR}</style></head><body>{body_html}</body></html>"""

# Render PDF
doc = HTML(string=html_doc).render()
n_pages = len(doc.pages)
doc.write_pdf(OUT_PDF)
print(f"Wrote: {OUT_PDF}  ({n_pages} pages, {os.path.getsize(OUT_PDF)} B)")

# Build docx via pandoc
try:
    result = subprocess.run(
        ["pandoc", MD_PATH, "-o", OUT_DOCX,
         "--standalone",
         "--from=markdown+tables+pipe_tables+grid_tables+fenced_code_blocks+footnotes"],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode == 0:
        print(f"Wrote: {OUT_DOCX}  ({os.path.getsize(OUT_DOCX)} B)")
    else:
        print(f"pandoc failed: {result.stderr[:500]}")
except FileNotFoundError:
    print("pandoc not installed — docx skipped, PDF only")
except subprocess.TimeoutExpired:
    print("pandoc timed out")
