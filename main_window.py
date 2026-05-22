from pathlib import Path

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QLabel, QPushButton, QFileDialog,
    QFrame, QMessageBox, QToolBar, QAction,
)
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtCore import QSize

from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    TOOLBAR_ICON_SIZE, TOOLBAR_BTN_HEIGHT,
    COLOR_FILE_LABEL,
    FILE_FILTER_OPEN, FILE_FILTER_SAVE, DEFAULT_SAVE_NAME,
)
from data_utils import load_raw_values, apply_offset_shift
from polar_canvas import PolarCanvas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._current_file: str | None = None
        self._is_data_loaded = False

        self.setWindowTitle("Polar Viewer")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self._build_menu()
        self._build_toolbar()
        self._build_body()
        self.statusBar().showMessage("Ready")

    # ── Menu bar ──────────────────────────────────────────────────────
    def _build_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File(&F)")

        open_action = QAction("Open(&O)...", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.on_open)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        save_action = QAction("Save Image As(&S)...", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.on_save)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit(&X)", self)
        exit_action.setShortcut(QKeySequence("Alt+F4"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menubar.addMenu("Help(&H)")
        about_action = QAction("About(&A)", self)
        about_action.triggered.connect(self.on_about)
        help_menu.addAction(about_action)

    # ── Toolbar ───────────────────────────────────────────────────────
    def _build_toolbar(self):
        toolbar = QToolBar("Main Toolbar", self)
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(TOOLBAR_ICON_SIZE, TOOLBAR_ICON_SIZE))
        self.addToolBar(toolbar)

        toolbar.addWidget(self._make_toolbar_button("📂  Open", self.on_open))

        toolbar.addSeparator()

        self.save_button = self._make_toolbar_button("💾  Save Image", self.on_save, enabled=False)
        toolbar.addWidget(self.save_button)

    def _make_toolbar_button(self, label: str, slot, *, enabled: bool = True) -> QPushButton:
        button = QPushButton(label)
        button.setFixedHeight(TOOLBAR_BTN_HEIGHT)
        button.setEnabled(enabled)
        button.clicked.connect(slot)
        return button

    # ── Body ──────────────────────────────────────────────────────────
    def _build_body(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(8, 8, 8, 4)
        layout.setSpacing(6)

        self.file_path_label = QLabel("No file loaded")
        self.file_path_label.setFont(QFont("Consolas", 9))
        self.file_path_label.setStyleSheet(f"color: {COLOR_FILE_LABEL}; padding: 2px 4px;")
        layout.addWidget(self.file_path_label)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)

        self.canvas = PolarCanvas(self)
        layout.addWidget(self.canvas)

    # ── Event handlers ────────────────────────────────────────────────
    def on_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Data File", "", FILE_FILTER_OPEN)
        if not path:
            return
        try:
            raw_values = load_raw_values(path)
            shifted_values = apply_offset_shift(raw_values)
            self.canvas.plot_polar(shifted_values)
            self._update_ui_after_load(path)
        except Exception as e:
            self._show_error("Load Failed", f"Cannot read file:\n{e}")
            self.statusBar().showMessage("Load failed")

    def _update_ui_after_load(self, path: str):
        filename = Path(path).name
        self._current_file = path
        self._is_data_loaded = True
        self.save_button.setEnabled(True)
        self.file_path_label.setText(f"📄  {path}")
        self.setWindowTitle(f"Polar Viewer — {filename}")
        self.statusBar().showMessage(f"Loaded: {filename}")

    def on_save(self):
        if not self._is_data_loaded:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Image As", DEFAULT_SAVE_NAME, FILE_FILTER_SAVE
        )
        if not path:
            return
        try:
            self.canvas.save_figure(path)
            self.statusBar().showMessage(f"Saved: {path}")
        except Exception as e:
            self._show_error("Save Failed", f"Cannot save image:\n{e}")

    def on_about(self):
        QMessageBox.about(
            self, "About Polar Viewer",
            "Polar Viewer\n\n"
            "Reads data files in index=value format,\n"
            "applies the b_key formula, and plots a polar chart.\n\n"
            "Supported input: .txt, _uvcmp\n"
            "Supported output: PNG, SVG",
        )

    def _show_error(self, title: str, message: str):
        QMessageBox.critical(self, title, message)