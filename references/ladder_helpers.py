"""Ladder-diagram drawing helpers — the McLeod house style (JIC/NEMA ladder, matplotlib).

This is the CANONICAL copy of the helpers used by every sheet in
docs/hardware/diagrams/sheet*.py. Each sheet script stays self-contained and
regenerable, so COPY the functions you need into the sheet (don't import across
files) — but keep this file the reference: if you improve a helper, update it
here AND in the sheets that use it.

Symbols follow the JIC / NMTBA EGP1-1967 chart (references/symbols.webp +
relay-symbols.png): NO contact -| |-, NC contact -|/|-, coil = circle, toggle =
two terminals + open lever. The blue DI box is OUR extension (not JIC): a
RevPi/DIO input channel — a high-impedance SENSE, never a current load.
"""
import matplotlib
matplotlib.use("Agg")           # headless render; NEVER the default GUI backend
import matplotlib.pyplot as plt

# ---- house constants --------------------------------------------------------------
LW = 1.6            # wire line width (1.6 ladder sheets, 1.7 power sheets — either OK)
BAR_H = 0.32        # contact bar half-height (0.30–0.32)
GAP = 0.16          # half-gap between contact bars (0.15–0.16)
BLUE = "#0a3ab5"    # net tags + DIO input boxes (RevPi = blue)
RED = "#b33"        # outputs / warnings ("#a33" for DROPPED notes)
GREEN = "#1b6b1b"   # new/changed feature callouts (band fill "#eef6ee")
AMBER = "#c08a00"   # mechanical-link dashes / one-relay highlight (band "#fff3c4")
GRAY = "#555"       # secondary explanatory text ("#777" for de-emphasized)


# ---- primitives -------------------------------------------------------------------
def wire(ax, x1, y1, x2, y2):
    """A conductor. zorder 1 so symbols (2-3) and dots (4) sit on top."""
    ax.plot([x1, x2], [y1, y2], color="k", lw=LW, solid_capstyle="round", zorder=1)


def label(ax, x, y, s, size=10, ha="center", va="center", weight="normal", color="k"):
    ax.text(x, y, s, fontsize=size, ha=ha, va=va, weight=weight, color=color, zorder=3)


def wnum(ax, x, y, num):
    """Net (wire) number tag — blue rounded box ON the wire, per DESIGN-RECORD §8."""
    ax.text(x, y, str(num), fontsize=8, ha="center", va="center", color=BLUE,
            weight="bold", zorder=6, bbox=dict(boxstyle="round,pad=0.14", fc="white",
                                               ec=BLUE, lw=0.7))


def dot(ax, x, y, r=0.07):
    """Junction dot — REQUIRED wherever a wire tees/branches (0.06–0.08)."""
    ax.add_patch(plt.Circle((x, y), r, color="k", zorder=4))


# ---- JIC symbols ------------------------------------------------------------------
def no_contact(ax, cx, cy, name, lblpos="above", nsize=9):
    """Normally-open relay contact  -| |-  centred at (cx, cy).
    Returns (left_x, right_x) — the caller wires up to these, leaving the gap open."""
    lx, rx = cx - GAP, cx + GAP
    ax.plot([lx, lx], [cy - BAR_H, cy + BAR_H], color="k", lw=LW, zorder=2)
    ax.plot([rx, rx], [cy - BAR_H, cy + BAR_H], color="k", lw=LW, zorder=2)
    if name:
        yy = cy + BAR_H + 0.24 if lblpos == "above" else cy - BAR_H - 0.34
        label(ax, cx, yy, name, size=nsize)
    return lx, rx


def nc_contact(ax, cx, cy, name, lblpos="above"):
    """Normally-closed relay contact  -|/|-  (NO bars + a diagonal slash)."""
    lx, rx = no_contact(ax, cx, cy, name, lblpos=lblpos)
    ax.plot([cx - GAP - 0.12, cx + GAP + 0.12], [cy - BAR_H - 0.05, cy + BAR_H + 0.05],
            color="k", lw=LW, zorder=2)
    return lx, rx


def coil(ax, cx, cy, name, r=0.42):
    """Relay coil — circle with the device tag (R9, RB-L …) inside.
    Returns (left_x, right_x)."""
    ax.add_patch(plt.Circle((cx, cy), r, fill=False, lw=LW, color="k", zorder=2))
    label(ax, cx, cy, name, size=9, weight="bold")
    return cx - r, cx + r


def switch(ax, cx, cy, name, momentary=False):
    """SPST toggle (JIC): two terminal dots + an OPEN lever (drawn de-actuated).
    momentary=True adds the small arc above the lever (spring return).
    Returns (left_x, right_x)."""
    lx, rx = cx - 0.34, cx + 0.34
    ax.add_patch(plt.Circle((lx, cy), 0.07, color="k", zorder=3))
    ax.add_patch(plt.Circle((rx, cy), 0.07, color="k", zorder=3))
    ax.plot([lx, rx - 0.02], [cy, cy + 0.38], color="k", lw=LW, zorder=2)   # open lever
    if momentary:
        ax.plot([cx - 0.16, cx, cx + 0.16], [cy + 0.52, cy + 0.60, cy + 0.52],
                color="k", lw=1.0, zorder=2)
    label(ax, cx, cy - 0.42, name, size=9)
    return lx, rx


def di_box(ax, cx, cy, name, w=1.05, h=0.52):
    """RevPi DIO INPUT channel (our extension, blue): a high-Z SENSE tapping a node.
    It rides the coil's own net — same wire #, no new number. Returns (left_x, right_x)."""
    ax.add_patch(plt.Rectangle((cx - w / 2, cy - h / 2), w, h, fill=False, lw=LW,
                               color=BLUE, zorder=2))
    label(ax, cx, cy, name, size=8, weight="bold", color=BLUE)
    return cx - w / 2, cx + w / 2


def box(ax, cx, cy, w, h, name, size=9):
    """Generic device box (Victron, FUSE, valve V-n …). Returns (left_x, right_x)."""
    ax.add_patch(plt.Rectangle((cx - w / 2, cy - h / 2), w, h, fill=False, lw=LW,
                               color="k", zorder=2))
    label(ax, cx, cy, name, size=size, weight="bold")
    return cx - w / 2, cx + w / 2


def circle_load(ax, cx, cy, name, r=0.5):
    """Round load (motor M1, FAN CLUTCH) — JIC motor symbol. Returns (left_x, right_x)."""
    ax.add_patch(plt.Circle((cx, cy), r, fill=False, lw=LW, color="k", zorder=2))
    label(ax, cx, cy, name, size=9, weight="bold")
    return cx - r, cx + r


# ---- sheet scaffolding ------------------------------------------------------------
def rails(ax, xl, xr, ybot, ytop, lname="+24 V", rname="0 V", lnet=102, rnet=400):
    """Vertical ladder rails: left = supply, right = return, each with its net tag."""
    wire(ax, xl, ybot, xl, ytop)
    wire(ax, xr, ybot, xr, ytop)
    label(ax, xl, ytop + 0.35, lname, size=13, weight="bold")
    label(ax, xr, ytop + 0.35, rname, size=13, weight="bold")
    wnum(ax, xl, ytop - 0.35, lnet)
    wnum(ax, xr, ytop - 0.35, rnet)


def notes(ax, x, y, text, size=9):
    """The NOTES block — monospace, boxed, bottom-left. Every sheet has one."""
    ax.text(x, y, text, fontsize=size, ha="left", va="top", family="monospace",
            bbox=dict(boxstyle="round", fc="white", ec="k", lw=1))


def highlight_band(ax, x0, y0, w, h, kind="new"):
    """Soft background band: kind='new' (green, changed feature) or
    'one-relay' (amber, poles of one physical relay drawn in a column)."""
    fc = {"new": "#eef6ee", "one-relay": "#fff3c4"}[kind]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, fc=fc, ec="none", alpha=0.7, zorder=0))


def save_sheet(out_png, dpi=140):
    """Standard save: PNG only (SVG chokes on text-heavy sheets), white, tight."""
    plt.tight_layout()
    plt.savefig(out_png, dpi=dpi, bbox_inches="tight", facecolor="white")
    print("wrote", out_png)
