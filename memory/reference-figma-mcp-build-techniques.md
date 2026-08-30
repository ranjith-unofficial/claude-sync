---
name: reference-figma-mcp-build-techniques
description: "Working techniques for building real UI in Figma via use_figma — real icon sets, photos, segmented rings, and assembling animations from stage frames"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 32dcfc27-29c8-427f-8e82-f96c2295f2dd
  modified: 2026-08-30T10:32:11.556Z
---

Learned the hard way across ~26 rounds of building app screens via `use_figma`
(29-30 Aug 2026). These are the non-obvious ones that cost real debugging time.

**Real icons — use `figma.createNodeFromSvg(svgString)`, never `vectorPaths`.**
Figma's `vectorPaths` parser rejects both **commas** and **arc (`a`/`A`) commands**, so
pasting SVG path data from any real icon set fails with `Failed to convert path. Invalid
command at ,`. `createNodeFromSvg` parses full SVG properly. Fetch icons from a pinned CDN:
`https://unpkg.com/lucide-static@0.544.0/icons/<name>.svg` (Lucide is ISC-licensed; the
unversioned `@latest` URL returned empty). Then `node.rescale(size/24)` and centre with
`n.x = cx - n.width/2`. Hand-drawn icons are a false economy — a hand-built shopping bag
read as a **padlock** at 42px twice before being replaced with a parcel.

**Photos — `upload_assets` works and is the only supported path.**
`figma.createImageAsync` is explicitly unsupported in `use_figma`. Instead: call
`mcp__figma__upload_assets` with `count` and `nodeIds` (target nodes must already exist),
then `curl -X POST -F "file=@photo.jpg" "<submitUrl>"` for each returned URL. The image is
placed as a fill on the target node automatically. Multipart `file=` is preferred — the
filename becomes the layer name.

**Segmented rings (one arc per item) — `ellipse.arcData`.**
One ellipse per segment: `arcData = { startingAngle, endingAngle, innerRadius }` where
`innerRadius = (R - thickness) / R`, start at `-Math.PI/2` so segment one begins at 12
o'clock, and leave a small angular gap (~0.18 rad, ~0.09 when count > 5). This drives both
the week-streak ring and the per-sector story-count rings. Caps out visually around 6-7
segments — beyond that the arcs read as a solid ring.

**Animations — build stage frames, screenshot, assemble with PIL.**
There is no motion export. What works: clone the final frame N times, hide nodes per stage
(`n.visible = n.y < threshold` gives a clean top-down reveal), screenshot each stage, then
assemble a GIF in Python with `Image.blend(prev, cur, a)` tweens between states and a
per-frame `duration` list. Produced `~/ClaudeDocs/inc42/brief-card/inc42-streak-reveal.gif`.

**Layout gotchas that bit repeatedly**
- `use_figma` is **atomic** — a failed script changes nothing, so retrying after a fix is
  safe, but a syntax error loses the whole batch. Keep calls to a few frames.
- Text height is not known until render. Any headline over ~20px WILL wrap differently than
  expected — **screenshot after every build** and fix collisions; roughly one in three
  screens needed a spacing fix.
- Setting a line to ~50% opacity to de-emphasise it reads as **disabled**, not subtle. Use
  an accent colour at full opacity instead.
- A photo scrim needs a **three-stop** gradient (0 → 0.75 → 0.96) over ~70% of the frame;
  two stops left white text illegible over a bright sky.

Related: [[reference-figma-mcp-limits]] (seat/quota — a View seat is hard read-only),
[[project-inc42-app-brief-gratification-redesign]] (what this was built for).
