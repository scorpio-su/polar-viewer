"""
polar_app.py - Entry point

PyQt5 desktop GUI application
- Clean Windows Notepad-style UI
- Supports importing .txt / _uvcmp files
- Displays polar coordinate chart (embedded Matplotlib)
- Can save as image (PNG / SVG)

Install:
    pip install PyQt5 matplotlib numpy

Run:
    python polar_app.py
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib import font_manager

from PyQt5.QtWidgets import QApplication

from main_window import MainWindow

_CJK_FONT_CANDIDATES = [
    "Microsoft JhengHei",
    "Microsoft YaHei",
    "PingFang TC",
    "Noto Sans CJK TC",
    "Noto Sans TC",
    "SimHei",
]


def _set_cjk_font() -> None:
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in _CJK_FONT_CANDIDATES:
        if name in available:
            matplotlib.rcParams["font.family"] = name
            return


def _configure_qt_plugins() -> None:
    """Set Qt plugin path only when the local venv copy exists, to avoid overriding system environments."""
    import os
    plugin_path = (
        Path(__file__).resolve().parent
        / "venv" / "Lib" / "site-packages" / "PyQt5" / "Qt5" / "plugins" / "platforms"
    )
    if plugin_path.is_dir():
        os.environ.setdefault("QT_QPA_PLATFORM_PLUGIN_PATH", str(plugin_path))


def main() -> None:
    _configure_qt_plugins()
    _set_cjk_font()

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()