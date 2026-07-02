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

## Wire-number tag placement (reviewer-set rules)

- **Tags sit IN LINE on the wire** — the white box breaks the wire. A tag floating
  above or beside its wire is wrong — bring it down onto the wire. (Reviewer's words on
  the reference sheet's in-line tag: *"That's perfect. That's how you should do it."*)
- **Every line really needs a number.** Both sides of every coil carry a tag. An
  unnumbered conductor means the net doesn't exist in the design record yet — STOP and
  assign it there first, then tag the drawing. (Applying this rule to a production sheet
  set flushed out a conductor that had no number anywhere — drawing, record, or
  schedules.)
- **No dot where there's no junction.** A straight-through connection point gets the
  wire tag, not a dot. Dots mark ONLY real tees (3+ wires joining) — and every real tee
  gets one: rail tees, parallel-tie feeds, snubber taps. (The same production sweep
  found both kinds of error: a phantom dot on a straight run, and real tees with no dot.)
- **A tag never covers a junction dot.** Extend the rail / shift the tag until both
  read clean.
- **Minimum clearance around connections:** a tag needs clear air to the connection
  points flanking it — a parallel-tie on one side, a symbol edge on the other, nothing
  sitting right on top of another.

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
| Junction | filled dot | `dot()` — REQUIRED at every tee, FORBIDDEN anywhere else |
| Net number | blue rounded tag IN LINE on the wire | `wnum()` — see tag-placement rules above |
| **Controller input** | **blue rectangle (our extension, not JIC)** | `di_box()` |

Contacts and switches are always drawn in the **de-energized / de-actuated** state
(standard practice). Where a sheet shows an energized path (e.g. an H-bridge), draw it
**dashed** and say so in the notes.

## Ladder layout rules

- **Rails:** supply left, return right, vertical, with net tags at the top — `rails()`.
- **Rungs** run left → right: switch/contact logic on the left, coil (or load) on the
  right, return to the right rail — and **supply-left / return-right applies to EVERY
  sub-drawing on a sheet**, not just the main ladder (a production sheet's motor section
  once used horizontal top/bottom rails and got rejected in review).
- **Wires land ON the element's edge** — always wire to the coordinates the helper
  returns (`coil()`/`di_box()`/`box()` edges), never to a hardcoded offset. A visible
  gap between a wire end and its coil is a defect (a real review catch: offsets sized
  for the wide input box left every coil's wires stopping short).
- **Element pitch inside a parallel block ≥ 1.05** (> the 0.84 coil diameter), and rung
  pitch sized so adjacent rungs' elements never touch (~0.5+ clear air). Reviewer's
  words: "space this stuff out so we can read where it's at."
- **A form-C (changeover) relay is drawn as its CONTACTS** — a real NO contact and a
  real NC contact (JIC bars/slash), never a pictorial pivot-lever with a dashed
  "energized" path. For a changeover feeding a load lead: NO from the supply rail and
  NC to the return rail meet at the lead's node, drawn de-energized so the rest state
  reads directly off the sheet.
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
