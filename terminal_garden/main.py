import curses
import math
import random
from terminal_garden.config import TERRAIN_TYPES
from terminal_garden.grid import Grid
from terminal_garden.plants import Plant
from terminal_garden.renderer import init_colors, render_frame, SIDEBAR_WIDTH

PLANT_NAMES = ["grass", "rose", "tulip", "sunflower", "tree"]
SPEED_LEVELS = [2, 5, 10, 20, 40]  # ticks per second (via halfdelay)


def _generate_blob(cx, cy, size, grid_width, grid_height):
    """Generate an organic blob shape using random-walk overlapping circles."""
    cells = set()
    # Start with a small circle at center
    for dy in range(-2, 3):
        for dx in range(-3, 4):
            if dx * dx / 9 + dy * dy / 4 <= 1:
                cells.add((cx + dx, cy + dy))

    # Random walk: place overlapping circles to form organic shape
    wx, wy = float(cx), float(cy)
    for _ in range(size):
        angle = random.uniform(0, 6.283)
        step = random.uniform(1.0, 2.5)
        wx += step * math.cos(angle)
        wy += step * math.sin(angle) * 0.5  # squash vertically
        # Keep walker near center
        wx = max(cx - 10, min(cx + 10, wx))
        wy = max(cy - 5, min(cy + 5, wy))
        r = random.uniform(1.5, 3.5)
        for dy in range(int(wy - r) - 1, int(wy + r) + 2):
            for dx in range(int(wx - r * 1.5) - 1, int(wx + r * 1.5) + 2):
                if (dx - wx) ** 2 / (r * 1.5) ** 2 + (dy - wy) ** 2 / r ** 2 <= 1:
                    if 0 <= dx < grid_width and 0 <= dy < grid_height:
                        cells.add((dx, dy))
    return cells


def generate_terrain(grid):
    """Place organic water ponds and rocks on the grid."""
    water_wave = TERRAIN_TYPES["water"]
    water_fill = TERRAIN_TYPES["water_fill"]

    # Water ponds: 1-2 organic blobs
    num_ponds = random.randint(1, 2)
    for _ in range(num_ponds):
        cx = random.randint(12, grid.width - 13)
        cy = random.randint(6, grid.height - 7)
        blob_size = random.randint(8, 15)
        all_water = _generate_blob(cx, cy, blob_size, grid.width, grid.height)

        # Find interior cells (all 4 neighbors also in water)
        interior = set()
        for px, py in all_water:
            if all((px + dx, py + dy) in all_water
                   for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]):
                interior.add((px, py))

        # Place all water cells as solid fill
        for px, py in all_water:
            if grid.is_empty(px, py):
                grid.set_terrain(px, py, water_fill["char"], water_fill["color"])

        # Add sparse wave bands: pick 2-4 y-levels, place short ~ runs
        if interior:
            y_values = sorted(set(py for _, py in interior))
            num_bands = min(random.randint(2, 4), len(y_values))
            band_ys = random.sample(y_values, num_bands)
            for by in band_ys:
                row_cells = sorted(px for px, py in interior if py == by)
                if len(row_cells) < 3:
                    continue
                # Pick a random starting x within the row, place 2-4 waves
                start_idx = random.randint(0, max(0, len(row_cells) - 3))
                wave_len = random.randint(2, min(4, len(row_cells) - start_idx))
                for i in range(start_idx, start_idx + wave_len):
                    wx = row_cells[i]
                    grid.set_terrain(wx, by, water_wave["char"], water_wave["color"])

    # Rocks: scattered in slightly bigger clusters
    rock = TERRAIN_TYPES["rock"]
    num_clusters = random.randint(3, 6)
    for _ in range(num_clusters):
        rx = random.randint(0, grid.width - 1)
        ry = random.randint(0, grid.height - 1)
        cluster_size = random.randint(2, 5)
        for _ in range(cluster_size):
            ox = rx + random.randint(-2, 2)
            oy = ry + random.randint(-1, 1)
            if grid.is_empty(ox, oy):
                grid.set_terrain(ox, oy, rock["char"], rock["color"])


def main(stdscr):
    # Setup curses
    curses.curs_set(0)
    curses.start_color()
    init_colors()
    stdscr.nodelay(False)

    max_y, max_x = stdscr.getmaxyx()

    # Game state - grid excludes sidebar width
    grid_width = max_x - SIDEBAR_WIDTH
    grid = Grid(grid_width, max_y - 1)  # reserve bottom row for status
    plants: list[Plant] = []
    next_id = 1
    cursor_x = grid_width // 2
    cursor_y = max_y // 2
    selected = 0  # index into PLANT_NAMES
    paused = False
    speed_idx = 2  # default 10 ticks/sec
    tick_count = 0
    message = ""  # temporary status message
    message_timer = 0

    # Generate terrain
    generate_terrain(grid)

    # Frame timing
    frame_delay = 10  # curses halfdelay in tenths of seconds
    tick_accumulator = 0.0

    def set_speed():
        nonlocal frame_delay
        tps = SPEED_LEVELS[speed_idx]
        frame_delay = max(1, 10 // tps)  # halfdelay value
        curses.halfdelay(frame_delay)

    set_speed()

    while True:
        # Build status text
        plant_name = PLANT_NAMES[selected].capitalize()
        speed_label = f"{SPEED_LEVELS[speed_idx]}tps"
        pause_label = "PAUSED" if paused else "Running"
        if message and message_timer > 0:
            msg_display = f" >> {message} << |"
            message_timer -= 1
        else:
            msg_display = ""
        status = (
            f" [{plant_name}] | Tick: {tick_count} | {speed_label} | "
            f"Plants: {len(plants)} | {pause_label} |{msg_display} "
            f"1-5:Plant  P:Pause  +/-:Speed  Q:Quit "
        )

        render_frame(stdscr, grid, plants, cursor_x, cursor_y, status,
                     selected=selected)

        # Handle input
        try:
            key = stdscr.getch()
        except curses.error:
            key = -1

        if key == ord("q") or key == ord("Q"):
            break

        # Movement
        if key == curses.KEY_UP or key == ord("k"):
            cursor_y = max(0, cursor_y - 1)
        elif key == curses.KEY_DOWN or key == ord("j"):
            cursor_y = min(max_y - 2, cursor_y + 1)
        elif key == curses.KEY_LEFT or key == ord("h"):
            cursor_x = max(0, cursor_x - 1)
        elif key == curses.KEY_RIGHT or key == ord("l"):
            cursor_x = min(grid_width - 1, cursor_x + 1)

        # Plant selection (1-6)
        elif key in (ord("1"), ord("2"), ord("3"), ord("4"), ord("5")):
            selected = key - ord("1")

        # Place plant
        elif key in (ord("\n"), ord(" ")):
            plant_type = PLANT_NAMES[selected]
            can_plant = grid.is_empty(cursor_x, cursor_y)
            # Non-grass plants can override grass
            if not can_plant and plant_type != "grass" and grid.is_grass(cursor_x, cursor_y):
                # Remove the grass plant occupying this cell
                cell = grid.get(cursor_x, cursor_y)
                grass_id = cell[0]
                for gp in plants:
                    if gp.plant_id == grass_id:
                        gp._clear_from_grid(grid)
                        plants.remove(gp)
                        break
                can_plant = True
            if can_plant:
                p = Plant(plant_type, cursor_x, cursor_y, next_id)
                next_id += 1
                p.place_on_grid(grid)
                plants.append(p)
                message = f"Planted {plant_type}!"
                message_timer = 15
            else:
                message = "Occupied!"
                message_timer = 10

        # Pause
        elif key == ord("p") or key == ord("P"):
            paused = not paused

        # Speed
        elif key == ord("+") or key == ord("="):
            speed_idx = min(len(SPEED_LEVELS) - 1, speed_idx + 1)
            set_speed()
        elif key == ord("-"):
            speed_idx = max(0, speed_idx - 1)
            set_speed()

        # Handle terminal resize
        if key == curses.KEY_RESIZE:
            max_y, max_x = stdscr.getmaxyx()
            grid_width = max_x - SIDEBAR_WIDTH
            cursor_x = min(cursor_x, grid_width - 1)
            cursor_y = min(cursor_y, max_y - 2)

        # Update game state
        if not paused:
            tick_count += 1
            new_grass = []
            for plant in plants:
                old_stage = plant.stage
                plant.tick()
                if plant.stage != old_stage:
                    plant.update_grid(grid)
                # Grass spreading
                spread_pos = plant.try_spread(grid)
                if spread_pos:
                    gp = Plant("grass", spread_pos[0], spread_pos[1], next_id)
                    next_id += 1
                    gp.place_on_grid(grid)
                    new_grass.append(gp)
            plants.extend(new_grass)


def run():
    curses.wrapper(main)


if __name__ == "__main__":
    run()
