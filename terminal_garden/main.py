import curses
import random
from terminal_garden.config import TERRAIN_TYPES
from terminal_garden.grid import Grid
from terminal_garden.plants import Plant
from terminal_garden.renderer import init_colors, render_frame

PLANT_NAMES = ["grass", "flower", "tree", "cactus"]
SPEED_LEVELS = [2, 5, 10, 20, 40]  # ticks per second (via halfdelay)


def generate_terrain(grid):
    """Place random water ponds and rocks on the grid."""
    water = TERRAIN_TYPES["water"]
    all_water = set()

    # Water ponds: 2-3 solid ellipses with organic edges
    num_ponds = random.randint(2, 3)
    for _ in range(num_ponds):
        cx = random.randint(10, grid.width - 11)
        cy = random.randint(5, grid.height - 6)
        rx = random.randint(4, 8)   # horizontal radius
        ry = random.randint(2, 4)   # vertical radius
        for dy in range(-ry, ry + 1):
            for dx in range(-rx, rx + 1):
                # Ellipse equation + slight noise on the boundary
                dist = (dx / rx) ** 2 + (dy / ry) ** 2
                threshold = 1.0 + random.uniform(-0.12, 0.12)
                if dist <= threshold:
                    px, py = cx + dx, cy + dy
                    if grid.in_bounds(px, py):
                        all_water.add((px, py))

    # Place water cells
    for px, py in all_water:
        if grid.is_empty(px, py):
            grid.set_terrain(px, py, water["char"], water["color"])

    # Rocks: 5-10 scattered
    rock = TERRAIN_TYPES["rock"]
    num_rocks = random.randint(5, 10)
    for _ in range(num_rocks):
        rx = random.randint(0, grid.width - 1)
        ry = random.randint(0, grid.height - 1)
        if grid.is_empty(rx, ry):
            grid.set_terrain(rx, ry, rock["char"], rock["color"])


def main(stdscr):
    # Setup curses
    curses.curs_set(0)
    curses.start_color()
    init_colors()
    stdscr.nodelay(False)

    max_y, max_x = stdscr.getmaxyx()

    # Game state
    grid = Grid(max_x, max_y - 1)  # reserve bottom row for status
    plants: list[Plant] = []
    next_id = 1
    cursor_x = max_x // 2
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
            f"1-4:Plant  P:Pause  +/-:Speed  Q:Quit "
        )

        render_frame(stdscr, grid, plants, cursor_x, cursor_y, status)

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
            cursor_x = min(max_x - 1, cursor_x + 1)

        # Plant selection
        elif key in (ord("1"), ord("2"), ord("3"), ord("4")):
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
            cursor_x = min(cursor_x, max_x - 1)
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
