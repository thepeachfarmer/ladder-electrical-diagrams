# House conventions — naming, nets, symbols, layout

These rules were established drawing a real 16-relay control system (McLeod Farms
orchard sprayers), with every sheet reviewed by the person who wires the panels. The
symbol vocabulary is the **JIC standard (NMTBA specification EGP1-1967)** — the classic
"Electrical Diagram Symbols" chart most controls people learned from. This repo does not
redistribute the chart (it's third-party material); search "JIC ladder diagram symbols
EGP1-1967" for a copy. The helpers draw the subset you need for relay logic.

## Device naming

| Prefix | Device | Example |
|---|---|---|
| **R** | relay | R1–R6 loads, R7/R8 mode transfer, R9 master… |
| **S** | operator switch | S1 master, S2 mode, S6 dump (center-off momentary) |
| **M** | motor | M1 |
| **V** | valve | V1–V6 |

Adapt the prefixes to your project's standard, but be consistent, number everything,
and never let two naming generations coexist on the drawings — if a legacy tag survives
in a table somewhere, print the current tag alongside it.

## Net (wire) numbering

- **One number per electrical node.** Every point on a node shares the number; a supply
  rail is ONE number no matter how many things tap it.
- **A new number ONLY where a contact separates nodes.** A closed contact still
  separates nodes (it can open); a junction does not.
- **An input sense is a branch off an existing node → same wire #, never a new one.**
  A controller input (high-Z) sensing a coil's drive node reads operator intent without
  adding a wire number. (This rule came from a human reviewer deleting a whole band of
  redundant "sense nets" from an early draft.)
- **Group numbers in bands** so a number's neighborhood tells you what it is. The
  original project's bands: 100s = power rails · 200s = controller outputs and load
  drives · 300s = sensor inputs · 400s = operator/control wiring, with the 0 V return
  bus getting one memorable number (400). Last digit rhymes with the device where
  possible (output 7 → net 207, input 13 → net 313).
- **Every conductor gets a number** — if a wire has no number, the design record is
  incomplete. Fix the record, then the drawing.

## Symbols (JIC) and what draws them

| Thing | JIC symbol | Helper |
|---|---|---|
| NO relay contact | `-| |-` | `no_contact()` |
| NC relay contact | `-|/|-` (slash) | `nc_contact()` |
| Relay coil | circle with tag | `coil()` |
| SPST toggle | 2 terminal dots + open lever | `switch()` |
| Momentary | toggle + spring arc | `switch(momentary=True)` |
| Motor / clutch | circle with name | `circle_load()` |
| Valve, PSU, fuse… | rectangle | `box()` |
| Junction | filled dot | `dot()` — REQUIRED at every tee |
| Net number | blue rounded tag on the wire | `wnum()` |
| **Controller input** | **blue rectangle (our extension, not JIC)** | `di_box()` |

Contacts and switches are always drawn in the **de-energized / de-actuated** state
(standard practice). Where a sheet shows an energized path (e.g. an H-bridge), draw it
**dashed** and say so in the notes.

## Ladder layout rules

- **Rails:** supply left, return right, vertical, with net tags at the top — `rails()`.
- **Rungs** run left → right: switch/contact logic on the left, coil (or load) on the
  right, return to the right rail. Rung spacing ≥ ~1.9 units; parallel blocks need ~2.4.
- **Branches tie straight to the rail** when the rail is right there — don't add a
  gratuitous tie bar.
- **Parallel elements** (a coil + its input sense; two coils sharing a drive) hang
  between two short vertical ties with the rung entering/leaving at mid-height.
- **Input boxes ride the coil's node** — draw them as a parallel branch beside the
  coil, both ends on the same nets.
- **Multi-pole relays:** each pole may live on its own rung; when poles must be read as
  ONE device, align them in a column, tie with an amber dashed mechanical link, and put
  an amber `highlight_band(kind="one-relay")` behind the column.
- **New/changed features** get a soft green band + a green explainer box, so a
  reviewer's eye lands on what moved.
- **Every sheet ends with a boxed monospace NOTES block** (bottom-left, `notes()`):
  device legend, net legend, behavior summary, interlocks/warnings.
- **Colors:** black = wiring/symbols · blue `#0a3ab5` = net tags + controller I/O ·
  red `#b33` = warnings (`#a33` for DROPPED/superseded notes) · green `#1b6b1b` =
  new-feature callouts · amber `#c08a00` = mechanical links · gray `#555` = secondary
  prose.
- **Cross-reference other sheets by number** ("Sheet 1A", "→ Sheet 3, nets 411/412")
  instead of re-drawing the other sheet's content.

## Sheet set organization (one concern per sheet)

A working template from the original project:

| Sheet | Concern |
|---|---|
| 1 | Power chain + supply latch |
| 1A | Detail sheet (the "one relay, two poles" explainer) |
| 2 | Operator controls (switches → coils + input senses) |
| 3 | Main control ladder (coil side) |
| 4 | Controller I/O map (the module box, every channel + net) |
| 5–6 | Output stages (contacts → loads) |

A lettered detail sheet (1A) is the pattern for "this deserves its own explanation,
between 1 and 2." Superseded sheets are deleted, not archived in place.
