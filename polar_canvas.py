import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QSizePolicy

from constants import (
    FIGURE_SIZE, SAVE_DPI, RADIAL_TICK_COUNT, TOTAL_DEGREES,
    PLACEHOLDER_FONT_SIZE, TICK_FONT_SIZE,
    COLOR_BG, COLOR_PLACEHOLDER, COLOR_GRID, COLOR_TICK,
)


class PolarCanvas(FigureCanvas):
    """Polar coordinate canvas embeddable in a Qt window."""

    def __init__(self, parent=None):
        fig, self.ax = plt.subplots(figsize=FIGURE_SIZE, subplot_kw=dict(polar=True))
        super().__init__(fig)
        self.fig = self.figure  # FigureCanvas takes ownership of fig; access via self.figure
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._draw_placeholder()

    def _apply_base_style(self, bg_color: str):
        self.fig.patch.set_facecolor(bg_color)
        self.ax.set_facecolor(bg_color)

    def _draw_placeholder(self):
        self.ax.clear()
        self._apply_base_style(COLOR_BG)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.xaxis.grid(False)
        self.ax.yaxis.grid(False)
        self.ax.spines["polar"].set_visible(False)
        self.ax.text(
            0, 0, "Import a data file\n(.txt / _uvcmp)",
            ha="center", va="center",
            fontsize=PLACEHOLDER_FONT_SIZE, color=COLOR_PLACEHOLDER,
            transform=self.ax.transData,
        )
        self.draw()

    def plot_polar(self, values: list[float]):
        self.ax.clear()
        self._apply_base_style("white")

        degrees = np.arange(TOTAL_DEGREES)
        radians = degrees * np.pi / 180
        amplitudes = np.array(values, dtype=float)

        closed_radians = np.append(radians, radians[0])
        closed_amplitudes = np.append(amplitudes, amplitudes[0])

        self.ax.plot(closed_radians, closed_amplitudes, color="black", linewidth=1.0)

        v_min, v_max = amplitudes.min(), amplitudes.max()
        ticks = np.linspace(v_min, v_max, RADIAL_TICK_COUNT)
        self.ax.set_yticks(ticks)
        self.ax.set_yticklabels(
            [f"{t:.4g}" for t in ticks],
            color=COLOR_TICK, fontsize=TICK_FONT_SIZE, ha="left",
        )
        self.ax.set_rlabel_position(90)
        self.ax.yaxis.grid(True, color=COLOR_GRID, linestyle="--", linewidth=0.5)
        self.ax.set_xticks([])
        self.ax.xaxis.grid(False)
        self.ax.spines["polar"].set_visible(False)

        self.fig.tight_layout(pad=0)
        self.draw()

    def save_figure(self, path: str):
        self.fig.savefig(path, dpi=SAVE_DPI, bbox_inches="tight", facecolor="white")