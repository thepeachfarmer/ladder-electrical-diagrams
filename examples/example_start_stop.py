"""Example sheet — classic START/STOP seal-in rung, drawn in the house ladder style.

Shows most of the vocabulary in one small sheet: momentary switch, NO/NC contacts,
a relay coil with a parallel high-Z input-sense box (same node, same wire number),
a load rung, net tags, junction dots, and the NOTES block.

Run from the repo root:  python3 examples/example_start_stop.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "references"))
from ladder_helpers import *  # noqa: E402,F401,F403

fig, ax = plt.subplots(figsize=(12, 8))
ax.set_aspect("equal")
ax.axis("off")
label(ax, 5.6, 8.0, "EXAMPLE  —  START/STOP seal-in  (house ladder style)",
      size=14, weight="bold")

XL, XR = 0.8, 10.4
rails(ax, XL, XR, 1.6, 7.2)

# ---- Rung 1: (START momentary || R1 seal-in) -> STOP NC -> R1 coil + DI1 sense ----
y1 = 5.6
tA, tB = 1.4, 3.6                       # parallel block: START over the seal-in contact
wire(ax, XL, y1, tA, y1)
wire(ax, tA, y1 - 0.55, tA, y1 + 0.55)
wire(ax, tB, y1 - 0.55, tB, y1 + 0.55)
sl, sr = switch(ax, 2.5, y1 + 0.55, "START", momentary=True)
wire(ax, tA, y1 + 0.55, sl, y1 + 0.55); wire(ax, sr, y1 + 0.55, tB, y1 + 0.55)
cl, cr = no_contact(ax, 2.5, y1 - 0.55, "R1 (seal-in)", lblpos="below")
wire(ax, tA, y1 - 0.55, cl, y1 - 0.55); wire(ax, cr, y1 - 0.55, tB, y1 - 0.55)
dot(ax, tA, y1); dot(ax, tB, y1)

wire(ax, tB, y1, 4.3, y1)
wnum(ax, 3.95, y1 + 0.3, 10)
nl, nr = nc_contact(ax, 4.6, y1, "STOP")
wire(ax, 4.3, y1, nl, y1)
wire(ax, nr, y1, 5.6, y1)
wnum(ax, 5.3, y1 + 0.3, 11)

tC, tD = 5.6, 8.6                       # coil + its input sense ride the SAME node
wire(ax, tC, y1 - 0.5, tC, y1 + 0.5)
wire(ax, tD, y1 - 0.5, tD, y1 + 0.5)
kl, kr = coil(ax, 7.1, y1 + 0.5, "R1")
wire(ax, tC, y1 + 0.5, kl, y1 + 0.5); wire(ax, kr, y1 + 0.5, tD, y1 + 0.5)
dl, dr = di_box(ax, 7.1, y1 - 0.5, "DI1")
wire(ax, tC, y1 - 0.5, dl, y1 - 0.5); wire(ax, dr, y1 - 0.5, tD, y1 - 0.5)
dot(ax, tC, y1); dot(ax, tD, y1)
wire(ax, tD, y1, XR, y1)

# ---- Rung 2: R1 contact -> motor ------------------------------------------------
y2 = 2.8
ml, mr = no_contact(ax, 2.5, y2, "R1")
wire(ax, XL, y2, ml, y2)
wire(ax, mr, y2, 5.0, y2)
wnum(ax, 4.2, y2 + 0.3, 12)
ll, lr = circle_load(ax, 5.7, y2, "M1", r=0.6)
wire(ax, 5.0, y2, ll, y2)
wire(ax, lr, y2, XR, y2)
label(ax, 5.7, y2 - 0.95, "load (motor / lamp / valve)", size=8, color=GRAY)

notes(ax, 0.8, 1.1,
      "NOTES\n"
      "- Press START -> R1 energizes -> R1's own NO contact seals the rung in;\n"
      "  STOP (NC) breaks it.  R1's second contact drives the load on rung 2.\n"
      "- DI1 (blue box) = a controller input SENSING the coil node: same wire # (11),\n"
      "  high-impedance branch, NOT a load.  Contacts drawn de-energized.")

ax.set_xlim(-0.2, 12.4)
ax.set_ylim(-0.4, 8.6)
save_sheet(os.path.join(os.path.dirname(__file__), "example_start_stop.png"))
