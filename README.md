# Terminal Garden

A terminal-based garden simulator where you plant and watch seeds grow into flowers, trees, cacti, and grass — all rendered in ASCII art with curses.

## Features

- **4 plant types**: Grass, Flower, Tree, Cactus — each with unique multi-stage ASCII art (seed, sprout, bloom, wilt)
- **Terrain**: Randomly generated water ponds (blue-filled with `~` waves) and scattered rocks
- **Grass spreading**: Grass organically spreads to nearby empty ground over time
- **Plant override**: Place flowers, trees, or cacti on top of grass to replace it
- **Controls**: Move cursor, select plant type, adjust simulation speed, pause/resume

## Quick Start

```bash
python -m terminal_garden
```

## Controls

| Key | Action |
|-----|--------|
| Arrow keys / `hjkl` | Move cursor |
| `1` `2` `3` `4` | Select plant: Grass, Flower, Tree, Cactus |
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
  renderer.py    # Curses rendering: colors, frame drawing
  main.py        # Game loop, input handling, terrain generation
```

## Development

```bash
pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

## Requirements

- Python 3.10+
- A terminal with color support
