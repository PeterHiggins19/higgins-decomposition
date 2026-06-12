# Archive Note — Titration Movie Files

**Date:** 2026-05-01
**Status:** Archived — superseded by titration_projector.html

## Archived Files

- `titration_movie.html` — Slideshow-style polar stack animation
- `titration_movie_data.json` — 600-frame dataset (200 pH points x 3 systems)

## What Happened

These files were built as a self-contained HTML slideshow for animating polar stack
slices across pH for three polyprotic acid titration systems (H3PO4, Citric, H2CO3).

The JSON data file (52,958 bytes) contains all species fractions, CLR coordinates,
Aitchison norms, phases, and Shannon entropy values computed from closed-form
polyprotic acid equilibrium expressions.

## The Problem

The HTML file triggered a Chrome/Edge security origin error when opened from `file://`:

    Unsafe attempt to load URL file:///...titration_movie.html from frame with URL
    file:///...titration_movie.html. 'file:' URLs are treated as unique security origins.

This occurred despite:
- Removing all `fetch()` calls (data embedded inline)
- Stripping all non-ASCII characters (pure ASCII, zero non-ASCII bytes)
- Using `var` instead of `const`/`let`
- Using `window.onload` initialization
- Valid JavaScript (verified via Node.js)

Other HTML files in the same directory (including the projector) worked without issue.
Root cause was never definitively identified.

## Resolution

The titration_projector.html was built using the proven architecture from
Hs-M02_projector.html (3D manifold projector). This works reliably from file://
on Windows and provides a more powerful interactive experience:
- 3D stacked polar polygon manifold with perspective projection
- Mouse-drag rotation, zoom, orbit mode
- System tabs, pH slider, view presets, toggle controls
- All data embedded as JavaScript object literals (no JSON parsing)

A PowerPoint slideshow (titration_cinema.pptx) was also created for movie-like
playback of polar stack slices — 150 frames across all three systems.

## Future Solution

A user file selector approach using the standard File System API
(`<input type="file">` or `window.showOpenFilePicker()`) would allow the HTML
to load external JSON data without triggering file:// security restrictions.
This pattern lets users select their own data files at runtime, bypassing
the same-origin policy entirely while maintaining security.

This approach should be implemented as a universal data loader for all
Hs interactive tools, enabling any dataset to be examined through
the projector and cinema instruments.
