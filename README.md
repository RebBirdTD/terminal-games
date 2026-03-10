# Terminal Garden

A terminal-based garden simulator where you plant and watch seeds grow into flowers, trees, and grass — rendered with Unicode symbols and curses colors.

## Features

- **5 plant types**: Grass, Rose (❀), Tulip (⚘), Sunflower (✿), Tree — each with multi-stage growth (seed, sprout, bloom, wilt)
- **Multi-colored petals**: Flowers use different Unicode symbols per petal for varied colors
- **Sidebar**: Plant preview panel showing bloom-stage art and terrain legend
- **Terrain**: Organic water ponds (solid fill with sparse `~` waves) and rock clusters
- **Grass spreading**: Grass organically spreads to nearby empty ground over time
- **Plant override**: Flowers and trees grow over grass cells

## Quick Start

```bash
python -m terminal_garden
```

## Controls

| Key | Action |
|-----|--------|
| Arrow keys / `hjkl` | Move cursor |
| `1` `2` `3` `4` `5` | Select plant: Grass, Rose, Tulip, Sunflower, Tree |
| `Space` / `Enter` | Plant at cursor |
| `P` | Pause / Resume |
| `+` / `-` | Speed up / Slow down |
| `Q` | Quit |

## Project Structure

```
terminal_garden/
  config.py      # Plant type definitions, terrain types, growth stages
  grid.py        # 2D grid with terrain and plant cell management
  plants.py      # Plant lifecycle: growth, stage transitions, spreading
  renderer.py    # Curses rendering: sidebar, colors, Unicode support
  main.py        # Game loop, input handling, terrain generation
```

## Development

```bash
pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

## Requirements

- Python 3.10+
- A terminal with color and Unicode support (e.g., Terminal.app, iTerm2)
