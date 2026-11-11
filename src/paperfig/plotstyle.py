"""Estilo de gráficas matplotlib para publicación.

Convenciones inspiradas en las reglas de estilo descritas en figures4papers
(https://github.com/ChenLiu-1996/figures4papers); implementación propia.
"""
from dataclasses import dataclass
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

PALETTE = {"blue_main": "#0F4D92", "blue_secondary": "#3775BA",
           "green_1": "#DDF3DE", "green_2": "#AADCA9", "green_3": "#8BCF8B",
           "red_1": "#F6CFCB", "red_2": "#E9A6A1", "red_strong": "#B64342",
           "neutral": "#CFCECE", "gray": "#767676", "dark": "#272727",
           "teal": "#42949E", "violet": "#9A4D8E", "highlight": "#FFD700"}


@dataclass(frozen=True)
class FigureStyle:
    font_size: int = 16
    axes_linewidth: float = 2.0
    font_family: tuple = ("Arial", "Helvetica", "Liberation Sans", "DejaVu Sans", "sans-serif")


def apply_publication_style(s: FigureStyle = FigureStyle()):
    plt.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": list(s.font_family),
        "font.size": s.font_size, "axes.linewidth": s.axes_linewidth,
        "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False,
        "xtick.major.width": s.axes_linewidth, "ytick.major.width": s.axes_linewidth,
        "svg.fonttype": "none", "pdf.fonttype": 42, "savefig.facecolor": "white"})


def panel_labels(axes, x=-0.2, y=1.08, size=19, parentheses=True):
    for ax, l in zip(axes, "abcdefgh"):
        ax.text(x, y, f"({l})" if parentheses else l, transform=ax.transAxes,
                fontsize=size, fontweight="bold", va="bottom")


def finalize_figure(fig, out, formats=("png", "pdf", "svg"), dpi=300, pad=1.2):
    fig.tight_layout(pad=pad)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    for f in formats:
        fig.savefig(out.with_suffix("." + f), dpi=dpi)
    plt.close(fig)
