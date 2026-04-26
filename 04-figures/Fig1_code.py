"""
Fig1_conceptual_framework.py
Sweet Trap v4 — eLife Research Advance
Figure 1: Theoretical cornerstone — Sweet Trap construct, Δ_ST axioms, and
four-part evidence architecture.

Layout: 2-row × 2-column grid
  [A — cross-phyla taxonomy]   [B — axiomatic wedge diagram]
  [C — four-part evidence architecture, spanning full width]

eLife specs:
  Width  = 180 mm (double-column)
  Height ≈ 170 mm (generous; eLife max = 225 mm per panel set)
  DPI    = 600 (print), 150 (screen preview)
  Font   = Arial / Helvetica (sans-serif fallback)
  Colour = Okabe-Ito (colour-blind safe)

Outputs saved to the same directory as this script:
  Fig1_conceptual_framework.pdf
  Fig1_conceptual_framework.png   (600 dpi)
  Fig1_conceptual_framework.svg

Run with the project's venv-phylo interpreter:
  /Users/andy/Desktop/Research/sweet-trap-multidomain/venv-phylo/bin/python \
      /Users/andy/Desktop/Research/sweet-trap-multidomain/04-figures/Fig1_code.py

Author: Figure Designer agent, 2026-04-24
"""

import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patches as mpatch
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Arc
from matplotlib.path import Path
from matplotlib.lines import Line2D
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
import scipy.stats as stats

# ── Output directory ────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PDF  = os.path.join(SCRIPT_DIR, "Fig1_conceptual_framework.pdf")
OUT_PNG  = os.path.join(SCRIPT_DIR, "Fig1_conceptual_framework.png")
OUT_SVG  = os.path.join(SCRIPT_DIR, "Fig1_conceptual_framework.svg")

# ── Okabe-Ito colour-blind-safe palette ────────────────────────────────────
OKI = {
    "black":   "#000000",
    "orange":  "#E69F00",
    "sky":     "#56B4E9",
    "green":   "#009E73",
    "yellow":  "#F0E442",
    "blue":    "#0072B2",
    "red":     "#D55E00",
    "pink":    "#CC79A7",
    "grey":    "#999999",
    "ltgrey":  "#DDDDDD",
    "white":   "#FFFFFF",
}

# Part colours (used in panel C)
PART_COLORS = {
    1: OKI["blue"],    # Human MR — cohort blue
    2: OKI["green"],   # Animal Phylogenetic — phylogeny green
    3: OKI["pink"],    # Molecular Convergence — molecular purple/pink
    4: OKI["red"],     # Genetic Causality — red
}

# ── Global matplotlib settings ──────────────────────────────────────────────
mpl.rcParams.update({
    "font.family":        "sans-serif",
    "font.sans-serif":    ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size":          8,
    "axes.linewidth":     0.6,
    "axes.labelsize":     8,
    "xtick.labelsize":    7,
    "ytick.labelsize":    7,
    "xtick.major.width":  0.6,
    "ytick.major.width":  0.6,
    "xtick.minor.width":  0.4,
    "ytick.minor.width":  0.4,
    "legend.fontsize":    7,
    "lines.linewidth":    1.0,
    "patch.linewidth":    0.6,
    "figure.dpi":         150,
    "savefig.dpi":        600,
    "savefig.bbox":       "tight",
    "savefig.pad_inches": 0.05,
    "pdf.fonttype":       42,   # embed fonts as TrueType in PDF
    "ps.fonttype":        42,
})

MM_TO_INCH = 1 / 25.4
FIG_W = 180 * MM_TO_INCH   # 7.087 in
FIG_H = 175 * MM_TO_INCH   # 6.890 in

# ═══════════════════════════════════════════════════════════════════════════
# Helper utilities
# ═══════════════════════════════════════════════════════════════════════════

def panel_label(ax, letter, x=-0.08, y=1.05, fontsize=11, fontweight="bold"):
    """Add bold panel label (a), (b), (c) at upper-left of axes."""
    ax.text(x, y, f"({letter})", transform=ax.transAxes,
            fontsize=fontsize, fontweight=fontweight,
            va="bottom", ha="left", color=OKI["black"])


def remove_spines(ax, which=("top", "right")):
    for sp in which:
        ax.spines[sp].set_visible(False)


def draw_arrow(ax, x0, y0, x1, y1, color=OKI["black"], lw=1.2,
               arrowstyle="-|>", mutation_scale=10, transform=None):
    tr = transform if transform is not None else ax.transData
    arr = FancyArrowPatch(
        (x0, y0), (x1, y1),
        arrowstyle=arrowstyle,
        color=color,
        lw=lw,
        mutation_scale=mutation_scale,
        transform=tr,
        zorder=5,
    )
    ax.add_patch(arr)


# ═══════════════════════════════════════════════════════════════════════════
# PANEL A — Cross-phyla taxonomy with iconic animals
# Six phyla, each with an iconic case drawn as a schematic path/polygon
# ═══════════════════════════════════════════════════════════════════════════

def draw_moth(ax, cx, cy, s=0.045, color=OKI["orange"]):
    """Simple geometric moth silhouette (bilateral wings + body)."""
    # Left forewing
    verts_lf = np.array([[0, 0], [-1.5, 0.4], [-1.8, 1.0],
                          [-0.8, 1.1], [-0.3, 0.7], [0, 0]]) * s
    # Right forewing (mirrored)
    verts_rf = verts_lf * np.array([-1, 1])
    # Left hindwing
    verts_lh = np.array([[0, 0], [-1.3, -0.3], [-1.5, -0.8],
                          [-0.7, -0.7], [-0.2, -0.3], [0, 0]]) * s
    verts_rh = verts_lh * np.array([-1, 1])
    # Body
    theta = np.linspace(0, np.pi, 12)
    body_x = 0.15 * s * np.cos(theta)
    body_y = 0.6 * s * np.sin(theta)
    body_xr = np.concatenate([body_x, -body_x[::-1]])
    body_yr = np.concatenate([body_y, body_y[::-1]])
    for verts in [verts_lf, verts_rf, verts_lh, verts_rh]:
        poly = plt.Polygon(verts + np.array([cx, cy]),
                           closed=True, color=color, alpha=0.85, zorder=4)
        ax.add_patch(poly)
    ax.fill(body_xr + cx, body_yr + cy, color=OKI["black"], zorder=5, alpha=0.9)


def draw_bird(ax, cx, cy, s=0.05, color=OKI["sky"]):
    """Simple bird silhouette — body ellipse + wing arc + tail."""
    # Body ellipse
    from matplotlib.patches import Ellipse
    body = Ellipse((cx, cy), width=1.8*s, height=0.7*s,
                   angle=-15, color=color, alpha=0.85, zorder=4)
    ax.add_patch(body)
    # Wing (curved patch)
    wing_x = np.array([cx, cx - 0.5*s, cx - 1.5*s, cx - 0.9*s, cx])
    wing_y = np.array([cy + 0.25*s, cy + 0.9*s, cy + 0.6*s, cy + 0.1*s, cy + 0.25*s])
    ax.fill(wing_x, wing_y, color=color, alpha=0.75, zorder=3)
    # Head circle
    head = plt.Circle((cx + 1.0*s, cy + 0.3*s), radius=0.28*s,
                       color=color, alpha=0.9, zorder=5)
    ax.add_patch(head)
    # Beak
    beak_x = [cx + 1.28*s, cx + 1.7*s, cx + 1.28*s]
    beak_y = [cy + 0.38*s, cy + 0.3*s, cy + 0.22*s]
    ax.fill(beak_x, beak_y, color=OKI["orange"], zorder=6)


def draw_human(ax, cx, cy, s=0.05, color=OKI["blue"]):
    """Stylised human figure (stick figure with filled body)."""
    # Head
    head = plt.Circle((cx, cy + 1.4*s), radius=0.28*s,
                       color=color, alpha=0.9, zorder=4)
    ax.add_patch(head)
    # Torso
    torso_x = [cx - 0.3*s, cx + 0.3*s, cx + 0.3*s, cx - 0.3*s]
    torso_y = [cy + 0.2*s, cy + 0.2*s, cy + 1.1*s, cy + 1.1*s]
    ax.fill(torso_x, torso_y, color=color, alpha=0.85, zorder=4)
    # Legs
    ax.plot([cx, cx - 0.25*s], [cy + 0.2*s, cy - 0.6*s],
            color=color, lw=3*s/0.05, solid_capstyle='round', zorder=4)
    ax.plot([cx, cx + 0.25*s], [cy + 0.2*s, cy - 0.6*s],
            color=color, lw=3*s/0.05, solid_capstyle='round', zorder=4)
    # Arms
    ax.plot([cx - 0.3*s, cx - 0.7*s], [cy + 0.9*s, cy + 0.5*s],
            color=color, lw=3*s/0.05, solid_capstyle='round', zorder=4)
    ax.plot([cx + 0.3*s, cx + 0.7*s], [cy + 0.9*s, cy + 0.5*s],
            color=color, lw=3*s/0.05, solid_capstyle='round', zorder=4)


def draw_worm(ax, cx, cy, s=0.05, color=OKI["green"]):
    """Sinusoidal worm body for C. elegans / Nematoda."""
    t = np.linspace(0, 2*np.pi, 100)
    wx = cx + s * 1.8 * (t / (2*np.pi) - 0.5)
    wy = cy + s * 0.5 * np.sin(t)
    ax.plot(wx, wy, color=color, lw=3*s/0.05, solid_capstyle='round', zorder=4)
    # Head blob
    head = plt.Circle((wx[0], wy[0]), radius=0.12*s, color=color, zorder=5)
    ax.add_patch(head)


def draw_snail(ax, cx, cy, s=0.05, color=OKI["pink"]):
    """Schematic Aplysia / Mollusca — coiled shell + body."""
    # Coiled shell
    for r_fac, alpha in [(1.0, 0.85), (0.7, 0.7), (0.4, 0.55)]:
        theta = np.linspace(0, 1.6*np.pi, 60)
        rx = cx + s * r_fac * np.cos(theta) * (0.6 + 0.25 * theta / (2*np.pi))
        ry = cy + s * r_fac * 0.5 * np.sin(theta) * (0.6 + 0.25 * theta / (2*np.pi))
        ax.plot(rx, ry, color=color, lw=2*s/0.05*r_fac, alpha=alpha,
                solid_capstyle='round', zorder=4)
    # Body
    body_x = [cx - 1.1*s, cx - 0.6*s, cx + 0.7*s, cx + 0.8*s]
    body_y = [cy - 0.35*s, cy - 0.55*s, cy - 0.5*s, cy - 0.25*s]
    ax.fill(body_x + [body_x[-1], body_x[0]],
            body_y + [cy - 0.1*s, cy - 0.1*s],
            color=color, alpha=0.75, zorder=3)


def draw_jellyfish(ax, cx, cy, s=0.05, color=OKI["grey"]):
    """Schematic jellyfish / Cnidaria — bell + tentacles."""
    # Bell (semi-ellipse)
    theta = np.linspace(0, np.pi, 80)
    bx = cx + s * 1.0 * np.cos(theta)
    by = cy + s * 0.6 * np.sin(theta)
    ax.fill(bx, by, color=color, alpha=0.7, zorder=4)
    ax.plot(bx, by, color=color, lw=1, zorder=5)
    # Tentacles
    for dx in np.linspace(-0.8*s, 0.8*s, 5):
        tet_x = cx + dx + 0.04*s * np.sin(np.linspace(0, 4*np.pi, 30))
        tet_y = cy + np.linspace(0, -0.9*s, 30)
        ax.plot(tet_x, tet_y, color=color, lw=0.8, alpha=0.7, zorder=3)


def draw_starfish(ax, cx, cy, s=0.05, color=OKI["yellow"]):
    """5-armed starfish / Echinodermata."""
    n_arms = 5
    angles_outer = np.array([np.pi/2 + 2*np.pi*i/n_arms for i in range(n_arms)])
    angles_inner = angles_outer + np.pi / n_arms
    r_outer = s * 1.2
    r_inner = s * 0.45
    pts_x, pts_y = [], []
    for ao, ai in zip(angles_outer, angles_inner):
        pts_x += [cx + r_outer * np.cos(ao), cx + r_inner * np.cos(ai)]
        pts_y += [cy + r_outer * np.sin(ao), cy + r_inner * np.sin(ai)]
    pts_x.append(pts_x[0])
    pts_y.append(pts_y[0])
    ax.fill(pts_x, pts_y, color=color, alpha=0.85, edgecolor=OKI["orange"], lw=0.5, zorder=4)


def draw_flame(ax, cx, cy, s=0.04, color=OKI["red"]):
    """Simple flame icon."""
    t = np.linspace(0, 2*np.pi, 60)
    fx = cx + s * 0.35 * np.sin(t)
    fy = cy + s * (0.8 * (1 - np.cos(t)/2) - 0.3)
    ax.fill(fx, fy, color=OKI["orange"], alpha=0.7, zorder=3)
    # Inner flame
    fx2 = cx + s * 0.18 * np.sin(t)
    fy2 = cy + s * (0.5 * (1 - np.cos(t)/2) - 0.2)
    ax.fill(fx2, fy2, color=OKI["yellow"], alpha=0.85, zorder=4)


def draw_panel_A(ax):
    """
    Panel A: Cross-phyla Sweet Trap cases.
    6 iconic animals arranged in a 2×3 grid with labels.
    Each shows: animal icon | arrow → reward signal → fitness cost text.
    """
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # ── Title ────────────────────────────────────────────────────────────────
    ax.text(0.5, 0.97, "Cross-phyla Sweet Trap instances",
            ha="center", va="top", fontsize=8, fontweight="bold",
            color=OKI["black"])

    # Layout: 2 columns × 3 rows
    # Reserve bottom 18% for legend; icons in top 82%
    # col_x: icon centres
    # row_y: row centres within the [0.20, 1.00] band
    cols = [0.25, 0.75]
    rows = [0.82, 0.58, 0.34]   # shifted up to leave room for legend

    # Animal specs: (draw_fn, cx, cy, colour, phylum_label)
    cases = [
        # Row 0
        (draw_moth,      cols[0], rows[0], OKI["orange"],
         "Arthropoda\n(Lepidoptera)"),
        (draw_bird,      cols[1], rows[0], OKI["sky"],
         "Chordata\n(Passeriformes)"),
        # Row 1
        (draw_human,     cols[0], rows[1], OKI["blue"],
         "Chordata\n(Homo sapiens)"),
        (draw_snail,     cols[1], rows[1], OKI["pink"],
         "Mollusca\n(Aplysia spp.)"),
        # Row 2
        (draw_worm,      cols[0], rows[2], OKI["green"],
         "Nematoda\n(C. elegans)"),
        (draw_jellyfish, cols[1], rows[2], OKI["grey"],
         "Cnidaria\n(Nematostella)"),
    ]

    s_icon = 0.060   # icon scale in axes-fraction units

    for (draw_fn, cx, cy, color, phylum) in cases:
        # Draw animal icon
        draw_fn(ax, cx, cy, s=s_icon, color=color)
        # Phylum label (below icon)
        ax.text(cx, cy - s_icon * 1.65, phylum,
                ha="center", va="top", fontsize=5.8,
                color=OKI["black"], style="italic",
                multialignment="center")

    # ── Legend row: reward signal → fitness cost ─────────────────────────────
    # Positioned in the bottom 18% of the axes
    y_leg = 0.10
    # Thin separator line
    ax.axhline(0.20, xmin=0.04, xmax=0.96,
               color=OKI["ltgrey"], lw=0.5, zorder=1)
    # Background highlight bar
    ax.axhspan(0.01, 0.19, xmin=0.04, xmax=0.96,
               color=OKI["red"], alpha=0.04, zorder=0)
    # Delta_ST label
    ax.text(0.50, 0.155, r"$\Delta_{ST} > 0$  across all 6 phyla",
            ha="center", va="center", fontsize=6.5,
            color=OKI["red"], fontweight="bold")
    # Arrow from "proximate reward" to "fitness cost"
    ax.annotate("", xy=(0.64, y_leg), xytext=(0.36, y_leg),
                arrowprops=dict(arrowstyle="-|>", color=OKI["red"],
                                lw=1.0, mutation_scale=7))
    ax.text(0.34, y_leg, "proximate reward",
            ha="right", va="center", fontsize=5.5, color=OKI["grey"])
    ax.text(0.66, y_leg, "fitness cost",
            ha="left", va="center", fontsize=5.5, color=OKI["red"])

    panel_label(ax, "a")


# ═══════════════════════════════════════════════════════════════════════════
# PANEL B — Δ_ST axiomatic framework + wedge diagram
# ═══════════════════════════════════════════════════════════════════════════

def draw_panel_B(ax):
    """
    Panel B: two overlapping distributions (S_anc vs S_mod) with wedge shading
    showing Δ_ST. Annotated with A1-A4 axioms. No fabricated numerical values.
    """
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.05, 1.02)
    remove_spines(ax, which=("top", "right", "bottom", "left"))
    ax.set_xticks([])
    ax.set_yticks([])

    # Title
    ax.text(0.5, 1.00, r"Axiomatic framework & $\Delta_{ST}$ scalar",
            ha="center", va="top", fontsize=8, fontweight="bold")

    # ── Distributions ────────────────────────────────────────────────────────
    # S_anc: centred at 0.3
    # S_mod: centred at 0.7 (shifted = environmental decoupling)
    x = np.linspace(-0.1, 1.1, 500)
    mu_anc, sigma_anc = 0.30, 0.10
    mu_mod, sigma_mod = 0.65, 0.13

    y_anc = stats.norm.pdf(x, mu_anc, sigma_anc)
    y_mod = stats.norm.pdf(x, mu_mod, sigma_mod)

    # Normalize to same peak height for visual clarity
    y_anc = y_anc / y_anc.max() * 0.45
    y_mod = y_mod / y_mod.max() * 0.45

    y_bot = 0.08  # baseline y-coordinate in axes units

    # Shaded area — wedge between U_perc peak and E[U_fit] peak
    # Highlight the gap between the two distribution peaks as Δ_ST
    wedge_x = [mu_anc, mu_mod, mu_mod, mu_anc]
    wedge_y_top = 0.68
    wedge_y_bot = 0.40

    # Draw wedge as a trapezoid
    wedge_poly = plt.Polygon(
        [(mu_anc, wedge_y_bot), (mu_mod, wedge_y_bot),
         (mu_mod, wedge_y_top), (mu_anc, wedge_y_top)],
        closed=True, color=OKI["red"], alpha=0.12, zorder=1)
    ax.add_patch(wedge_poly)

    # Distribution curves
    ax.fill_between(x, y_bot, y_anc + y_bot,
                    alpha=0.25, color=OKI["grey"], zorder=2)
    ax.plot(x, y_anc + y_bot, color=OKI["grey"],
            lw=1.5, ls="--", zorder=3, label=r"$S_{anc}$")

    ax.fill_between(x, y_bot, y_mod + y_bot,
                    alpha=0.25, color=OKI["blue"], zorder=2)
    ax.plot(x, y_mod + y_bot, color=OKI["blue"],
            lw=1.8, ls="-", zorder=3, label=r"$S_{mod}$")

    # Baseline
    ax.axhline(y_bot, xmin=0.02, xmax=0.98,
               color=OKI["black"], lw=0.6, ls="-", zorder=1)

    # Peak lines
    y_anc_peak = y_anc.max() + y_bot
    y_mod_peak = y_mod.max() + y_bot
    ax.vlines(mu_anc, y_bot, y_anc_peak,
              colors=OKI["grey"], lw=0.8, ls=":", zorder=3)
    ax.vlines(mu_mod, y_bot, y_mod_peak,
              colors=OKI["blue"], lw=0.8, ls=":", zorder=3)

    # Horizontal brace arrow for Δ_ST
    brace_y = 0.64
    draw_arrow(ax, mu_anc, brace_y, mu_mod, brace_y,
               color=OKI["red"], lw=1.5, arrowstyle="<->", mutation_scale=9)
    ax.text((mu_anc + mu_mod) / 2, brace_y + 0.04,
            r"$\Delta_{ST} = U_{perc} - \mathbb{E}[U_{fit}|B]$",
            ha="center", va="bottom", fontsize=7.5,
            color=OKI["red"], fontweight="bold")

    # t_sep arrow
    ax.annotate("", xy=(mu_mod + 0.05, 0.12),
                xytext=(mu_anc + 0.02, 0.12),
                arrowprops=dict(arrowstyle="->", color=OKI["orange"],
                                lw=1.0, mutation_scale=8))
    ax.text((mu_anc + mu_mod)/2 + 0.04, 0.135,
            r"$t_{sep}$", ha="center", va="bottom",
            fontsize=6.5, color=OKI["orange"])

    # Labels on distributions
    ax.text(mu_anc - 0.02, y_anc_peak + 0.04, r"$S_{anc}$",
            ha="center", va="bottom", fontsize=7, color=OKI["grey"],
            style="italic")
    ax.text(mu_mod + 0.02, y_mod_peak + 0.04, r"$S_{mod}$",
            ha="center", va="bottom", fontsize=7, color=OKI["blue"],
            style="italic")

    ax.text(mu_anc - 0.02, y_bot - 0.025,
            r"$U_{fit}|S_{anc}$", ha="center", va="top",
            fontsize=6, color=OKI["grey"])
    ax.text(mu_mod + 0.02, y_bot - 0.025,
            r"$U_{perc}|S_{mod}$", ha="center", va="top",
            fontsize=6, color=OKI["blue"])

    # ── Axiom annotations (right side) ──────────────────────────────────────
    axiom_x = 0.755
    axiom_ys = [0.90, 0.75, 0.60, 0.44]
    axiom_labels = [
        ("A1", "Ancestral calibration:\n"
               r"$U_{perc} = \varphi(s,\mathbf{g})$ tracks $U_{fit}$ in $S_{anc}$"),
        ("A2", "Environmental decoupling:\n"
               r"$S_{anc} \to S_{mod}$; wedge $\Delta_{ST}$ emerges"),
        ("A3", "Endorsement inertia:\n"
               r"$B=(1-w)U_{perc}+w\mathbb{E}[U_{fit}|B]$"
               "\n" r"$w \in [0,\ w_{max} < 1/2]$"),
        ("A4", "Partial cost visibility:\n"
               r"$c_{eff}(\tau) = \delta(\tau)\cdot c,\ \delta' < 0$"),
    ]
    ax_colors = [OKI["green"], OKI["orange"], OKI["blue"], OKI["pink"]]

    for (tag, text), ypos, col in zip(axiom_labels, axiom_ys, ax_colors):
        # Coloured tag circle
        ax.text(axiom_x - 0.02, ypos, tag,
                ha="right", va="center",
                fontsize=7, fontweight="bold", color=col,
                bbox=dict(boxstyle="round,pad=0.15", fc=col,
                          ec="none", alpha=0.18))
        ax.text(axiom_x + 0.01, ypos, text,
                ha="left", va="center",
                fontsize=5.6, color=OKI["black"],
                linespacing=1.35)

    # Divider line between distribution plot and axioms
    ax.axvline(0.715, ymin=0.05, ymax=0.95,
               color=OKI["ltgrey"], lw=0.6, ls="-")

    panel_label(ax, "b")


# ═══════════════════════════════════════════════════════════════════════════
# PANEL C — Four-part evidence architecture (full-width banner)
# ═══════════════════════════════════════════════════════════════════════════

def draw_panel_C(ax):
    """
    Panel C: Horizontal banner with 4 numbered evidence blocks linked by arrows.
    Each block: coloured header + method summary + key statistic.
    """
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.97,
            "Four-part evidence architecture testing the Sweet Trap thesis",
            ha="center", va="top", fontsize=8.5, fontweight="bold",
            color=OKI["black"])

    # Define 4 parts
    parts = [
        {
            "num": "1",
            "title": "Human\nSweet Trap",
            "color": PART_COLORS[1],
            "lines": [
                "Trans-ancestry MR",
                "5 ancestries × 6 cohorts",
                "NHANES · UKBiobank · FinnGen",
                "BBJ · MVP · AoU",
                "Key stat: pooled β ≥ 0.10",
                "(H1: behavioural + causal)",
            ],
        },
        {
            "num": "2",
            "title": "Animal\nPhylogenetic",
            "color": PART_COLORS[2],
            "lines": [
                "PRISMA meta-analysis",
                "≥ 50 cases × 6 phyla",
                "TimeTree + Open Tree of Life",
                "Blomberg K, Pagel λ, PGLS",
                "Key stat: K ≥ 0.30",
                "(H2 + H3 + H5)",
            ],
        },
        {
            "num": "3",
            "title": "Molecular\nConvergence",
            "color": PART_COLORS[3],
            "lines": [
                "Two-tier: H4a + H4b",
                "Ensembl / Ensembl Metazoa",
                "PAML codeml dN/dS",
                "InterPro Jaccard ≥ 0.70",
                "Key stat: cross-phyla identity",
                "30–50 % (convergence sig.)",
            ],
        },
        {
            "num": "4",
            "title": "Genetic\nCausality",
            "color": PART_COLORS[4],
            "lines": [
                "Branch-site Model A (PAML)",
                "15 genes × 4 eco-shift lineages",
                "+ lit. synthesis ≥ 30 expts",
                "hummingbird TAS1R1 control",
                "Key stat: ≥ 3/15 genes LRT",
                "p < 0.05 (H6a + H6f)",
            ],
        },
    ]

    n = len(parts)
    margin_x = 0.04
    gap = 0.015        # gap between boxes + arrows
    arrow_w = 0.03     # width consumed by arrows
    box_w = (1 - 2 * margin_x - (n - 1) * (gap + arrow_w)) / n
    box_y0 = 0.04
    box_y1 = 0.87
    header_h = 0.18   # fraction of box height for colour header

    # Draw each part box
    for i, part in enumerate(parts):
        x0 = margin_x + i * (box_w + gap + arrow_w)
        x1 = x0 + box_w
        y0 = box_y0
        y1 = box_y1
        col = part["color"]

        # Main box background
        bg = FancyBboxPatch((x0, y0), box_w, y1 - y0,
                            boxstyle="round,pad=0.005",
                            facecolor=col, alpha=0.08,
                            edgecolor=col, linewidth=1.0,
                            zorder=2)
        ax.add_patch(bg)

        # Coloured header band
        hdr = FancyBboxPatch((x0, y1 - header_h * (y1 - y0)), box_w,
                             header_h * (y1 - y0),
                             boxstyle="round,pad=0.005",
                             facecolor=col, alpha=0.75,
                             edgecolor=col, linewidth=0.8,
                             zorder=3)
        ax.add_patch(hdr)

        # Part number (large)
        ax.text(x0 + 0.018, (y1 - header_h * (y1 - y0) / 2),
                part["num"],
                ha="left", va="center",
                fontsize=13, fontweight="bold",
                color=OKI["white"], zorder=4)

        # Part title
        ax.text(x0 + box_w / 2, y1 - header_h * (y1 - y0) / 2,
                part["title"],
                ha="center", va="center",
                fontsize=7.2, fontweight="bold",
                color=OKI["white"], zorder=4,
                multialignment="center")

        # Body text lines
        line_h = (y1 - y0 - header_h * (y1 - y0) - 0.03) / len(part["lines"])
        for j, line in enumerate(part["lines"]):
            ty = y1 - header_h * (y1 - y0) - 0.025 - (j + 0.5) * line_h
            # Bold for "Key stat" line
            fw = "bold" if line.startswith("Key stat") else "normal"
            col_txt = col if line.startswith("Key stat") else OKI["black"]
            ax.text(x0 + box_w / 2, ty, line,
                    ha="center", va="center",
                    fontsize=5.8, fontweight=fw,
                    color=col_txt, zorder=4,
                    multialignment="center")

        # Arrow to next box
        if i < n - 1:
            ax_start = x1 + gap * 0.05
            ax_end = x1 + gap + arrow_w * 0.85
            ay = (y0 + y1) / 2
            draw_arrow(ax, ax_start, ay, ax_end, ay,
                       color=OKI["black"], lw=1.2,
                       arrowstyle="-|>", mutation_scale=9)

    # ── Bottom caption ───────────────────────────────────────────────────────
    ax.text(0.5, 0.005,
            "Coloured arrows: construct → operationalisation → empirical test   "
            "|   All predicted effect sizes and falsification criteria pre-registered (OSF)",
            ha="center", va="bottom",
            fontsize=5.5, color=OKI["grey"],
            style="italic")

    panel_label(ax, "c", x=-0.01, y=1.01)


# ═══════════════════════════════════════════════════════════════════════════
# Compose full figure
# ═══════════════════════════════════════════════════════════════════════════

def build_figure():
    fig = plt.figure(figsize=(FIG_W, FIG_H), facecolor="white")

    # GridSpec: 2 rows × 2 cols for top; 1 row for bottom banner
    # Row heights: top row = 55 %, bottom banner = 45 %
    gs_outer = GridSpec(
        2, 1,
        figure=fig,
        height_ratios=[1.0, 0.85],
        hspace=0.06,
        left=0.02, right=0.98,
        top=0.97, bottom=0.02,
    )

    # Top row: A (left) + B (right)
    gs_top = GridSpecFromSubplotSpec(
        1, 2,
        subplot_spec=gs_outer[0],
        wspace=0.06,
        width_ratios=[1, 1.45],
    )

    ax_A = fig.add_subplot(gs_top[0])
    ax_B = fig.add_subplot(gs_top[1])
    ax_C = fig.add_subplot(gs_outer[1])

    draw_panel_A(ax_A)
    draw_panel_B(ax_B)
    draw_panel_C(ax_C)

    # ── Thin separator line between top and bottom panels ────────────────
    line = Line2D([0.02, 0.98], [gs_outer.get_subplot_params().hspace / 2 + 0.02,
                                   gs_outer.get_subplot_params().hspace / 2 + 0.02],
                  transform=fig.transFigure,
                  color=OKI["ltgrey"], lw=0.5, zorder=0)
    # (skip drawing the line — hspace whitespace is clean enough)

    return fig


# ═══════════════════════════════════════════════════════════════════════════
# Save outputs
# ═══════════════════════════════════════════════════════════════════════════

def main():
    os.makedirs(SCRIPT_DIR, exist_ok=True)
    fig = build_figure()

    # PDF (vector, embed fonts)
    fig.savefig(OUT_PDF, format="pdf", dpi=600,
                bbox_inches="tight", pad_inches=0.05)
    print(f"Saved: {OUT_PDF}")

    # PNG (raster, 600 dpi)
    fig.savefig(OUT_PNG, format="png", dpi=600,
                bbox_inches="tight", pad_inches=0.05,
                facecolor="white")
    print(f"Saved: {OUT_PNG}")

    # SVG (editable vector)
    fig.savefig(OUT_SVG, format="svg",
                bbox_inches="tight", pad_inches=0.05)
    print(f"Saved: {OUT_SVG}")

    plt.close(fig)
    print("Done.")


if __name__ == "__main__":
    main()
