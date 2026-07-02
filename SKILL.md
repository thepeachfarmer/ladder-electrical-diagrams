---
name: ladder-electrical-diagrams
description: "Draw and maintain industrial control-wiring drawings as JIC/NEMA ladder diagrams rendered with plain matplotlib (NOT schemdraw). Use when: (1) creating or editing ladder-diagram sheets, (2) the user asks for a ladder diagram, relay/control wiring drawing, or an electrical schematic for panel/relay/switch logic, (3) a wiring design change needs the drawings re-synced, (4) regenerating schematic PDFs. Covers the symbol vocabulary (JIC / NMTBA EGP1-1967), net-numbering and sense-tap rules, sheet-per-concern organization, the render→look-at-it→human-review loop, and the doc-sync checklist. For electronic circuit schematics (ICs, opamps, passives) use a schematic tool like schemdraw instead — this skill is for relay/ladder control logic."
---

# Ladder Electrical Diagrams — the McLeod house style

A Claude Code skill for drawing **industrial ladder diagrams in JIC/NEMA symbols with
plain matplotlib**, matching how a controls person hand-sketches a rung. Distilled at
McLeod Farms while designing a 16-relay orchard-sprayer control system with Claude —
seven production sheets, reviewed rung-by-rung by a human who wires panels.

The canonical helper functions are in `references/ladder_helpers.py`; the
naming/net/symbol/layout rules are in `references/conventions.md` (read it before
drawing); a complete worked example is `examples/example_start_stop.py`. In a project
that already has approved sheets, **those sheets are the authority on the style** —
when a reference here and an approved sheet differ, the sheet wins.

## Why matplotlib, not schemdraw

- Ladder style is rails + rungs + a handful of symbols — exact coordinate control beats
  a chained-element DSL, and there's no fighting a layout engine over label placement.
- The sheets are text-heavy (notes blocks, explainer boxes, net tags). SVG backends
  choke on heavy text; matplotlib PNG at dpi=140 just works.
- Every symbol is ~10 lines of code you own — when the reviewer wants the lever drawn
  a little differently, you change it.

## Workflow

### 1. Start from the paper design, not the canvas

Write the **rung list** before drawing. For each rung: source rail → switches/contacts
(with device tags) → coil/load → return path, **with the net (wire) number of every
segment** from the project's net-numbering scheme. If a net number doesn't exist yet,
STOP and settle it in the design record first — the diagram documents the design; it
must never invent it.

### 2. One sheet per concern

Don't cram. Power chain, operator controls, the control ladder, the I/O map, and each
output stage get their own sheets. A change that doesn't fit an existing sheet gets a
new lettered detail sheet (Sheet 1 → Sheet 1A) rather than crowding one. Cross-reference
other sheets by number instead of re-drawing their content. Coil side and contact side
of the same relay may live on different sheets — say so in both notes blocks.

### 3. Write the sheet script

- One self-contained script per sheet: `sheetN_<name>.py`, writing `sheetN_<name>.png`
  beside it. Copy the helpers you need from `references/ladder_helpers.py` into the
  script (sheets stay standalone and regenerable; no cross-imports).
- Docstring at the top: what the sheet shows, the design facts it encodes, and the run
  command. Someone should understand the circuit from the docstring alone.
- `matplotlib.use("Agg")` before pyplot; `ax.set_aspect("equal")`; `ax.axis("off")`;
  title at top (`SHEET N — <what it is>`); NOTES block bottom-left; save PNG only
  (`dpi=140, bbox_inches="tight", facecolor="white"`). **No SVG** (chokes on heavy text).
- Run from the repo root if output paths are repo-relative.

### 4. Look at it, then fix everything at once

Render, then **read the PNG yourself**. Walk the rung list: trace every connection
end-to-end; every net tag sits **in line on its wire** (breaking it — never floating
beside it); **every segment carries a tag** (both sides of every coil); dots at **every
real junction and nowhere else** (a straight-through point gets the tag, not a dot); no
tag covers a dot; clear air between a tag and the connections flanking it; no label
touches a symbol or another label; contacts drawn de-energized. **List ALL problems
first, then fix them in one pass** — fixing one at a time makes you forget the rest.

### 5. Human review is the gate

An AI's visual check is necessary but NOT sufficient — a human reviewer catches real
errors that look fine to a machine (a device present in the text but never drawn; a
redundant sense net; a wrong tie to the rail — all real catches from this skill's
history). Show the PNG and **wait for approval before calling a sheet done**. When the
reviewer corrects you, use their exact words, apply the correction everywhere it occurs
(not just the instance they pointed at), and if it's a new *rule*, add it to
`references/conventions.md` so it sticks.

### 6. Sync the paper trail (a drawing change is a docs change)

- Regenerate any combined/print PDF built from the sheets.
- If nets/relays/switches changed: update the design record, the relay schedule, the
  field-wire schedule (if a conductor crosses an enclosure wall), and the BOM.
- If an I/O map changed: code-side channel maps must agree (code changes are a
  separate, tested task — flag them, don't sneak them in).
- Changelog entry. Superseded sheets get **deleted**, not left around — stale drawings
  in a repo a shop wires from are dangerous.

## Electrical house rules (details + rationale in conventions.md)

1. **One net number per electrical node; a new number only where a contact separates
   nodes.** A junction never creates a new number.
2. **Input senses ride the coil's net** — a controller input sensing a coil node is a
   high-impedance branch, never a new wire number.
3. **Branches tie straight to the rail** when the rail is adjacent — no gratuitous ties.
4. **Draw de-energized/de-actuated**; dashed = energized path (note it on the sheet).
5. Consistent device prefixes, numbered: **R**elays / **S**witches / **M**otors /
   **V**alves (adapt to the project's standard).
6. Put controller-I/O facts on the drawing where they matter (input common polarity,
   output drive limits, watchdog behavior) — the sheet is where the builder reads them.
7. **Net tags sit IN LINE on the wire** (breaking it) — never floating beside it;
   **every segment is tagged** (both sides of every coil); **dots only at real
   junctions** (a straight-through point gets the tag, not a dot) and a tag never
   covers a dot; keep clear air between a tag and the connections flanking it (full
   detail in conventions.md "Wire-number tag placement").

## Tooling gotchas (learned in production)

- Agg backend, PNG-only output, dpi=140 — see step 3.
- zorder discipline: highlight bands 0 · wires 1 · symbols 2–3 · junction dots 4 ·
  text 3–5 · net tags 6.
- `plt.Circle` / `plt.Rectangle` via `ax.add_patch`; no `with` context needed — build
  the figure top-to-bottom and save.
- Wires meet symbols at the returned edge coordinates (`no_contact` returns the bar
  positions; `coil`/`box` return edges) — never draw a wire *through* a symbol's gap.
- Momentary switches: the spring arc sits above the lever (`switch(momentary=True)`).
- Figure sizes that work: ~(12–16, 8–16) at these symbol scales; keep `set_xlim/ylim`
  a little generous so `bbox_inches="tight"` does the cropping.
