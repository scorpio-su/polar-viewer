from __future__ import annotations

# ── Data parameters ───────────────────────────────────────────────────────
OFFSET: int = 90
TOTAL_DEGREES: int = 360

# ── UI constants ──────────────────────────────────────────────────────────
WINDOW_WIDTH: int = 640
WINDOW_HEIGHT: int = 620
TOOLBAR_ICON_SIZE: int = 16
TOOLBAR_BTN_HEIGHT: int = 28
FIGURE_SIZE: tuple[int, int] = (5, 5)
SAVE_DPI: int = 150
RADIAL_TICK_COUNT: int = 5

PLACEHOLDER_FONT_SIZE: int = 13
TICK_FONT_SIZE: int = 7

COLOR_BG: str = "#f8f8f8"
COLOR_PLACEHOLDER: str = "#aaaaaa"
COLOR_GRID: str = "#cccccc"
COLOR_TICK: str = "#888888"
COLOR_FILE_LABEL: str = "#555555"

FILE_FILTER_OPEN: str = "Data Files (*.txt *_uvcmp);;All Files (*)"
FILE_FILTER_SAVE: str = "PNG Image (*.png);;SVG Vector (*.svg);;All Files (*)"
DEFAULT_SAVE_NAME: str = "polar_output.png"