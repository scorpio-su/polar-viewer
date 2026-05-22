# Polar Viewer

Reads data files in `index=value` format, applies an offset formula, and displays a polar coordinate chart in a PyQt5 desktop application.

## Features

- Import `.txt` / `.N_uvcmp` data files
- Apply b_key offset formula (`OFFSET = 90`) to reorder values
- Display polar line chart via embedded Matplotlib canvas
- Export chart as PNG or SVG
- Auto-detect CJK fonts on Windows / macOS / Linux

## Project Structure

```
polar_app.py      - Entry point: Qt/Matplotlib init and main()
main_window.py    - MainWindow class (menu, toolbar, layout, event handlers)
polar_canvas.py   - PolarCanvas class (Matplotlib figure embedded in Qt)
data_utils.py     - Data loading and offset-shift logic
constants.py      - All constants (UI, colors, data, file filters)
```

## Requirements

- Python 3.10+
- PyQt5
- matplotlib
- numpy

```bash
pip install PyQt5 matplotlib numpy
```

## Run

```bash
python polar_app.py
```

## Usage

| Action | Method |
|--------|--------|
| Open data file | Toolbar `📂 Open` / Menu `File > Open` / `Ctrl+O` |
| Save image | Toolbar `💾 Save Image` / Menu `File > Save Image As` / `Ctrl+S` |
| Exit | Menu `File > Exit` / `Alt+F4` |

## Input Format

One entry per line in `index=value` format, where index is an angle from 0 to 359:

```
0=8.25
1=8.251
2=8.255
...
359=8.10
```

## Output

- Polar line chart rendered live in the application window
- Save as `PNG` (150 DPI) or `SVG` vector image

## Offset Formula

```
shifted[i] = raw[(OFFSET + i) % 360]
```

`OFFSET = 90`, with 360 data points total.