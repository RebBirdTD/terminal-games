import curses

# Color name -> pair index mapping (initialized in init_colors)
COLORS = {
    "white": 1,
    "green": 2,
    "bright_green": 3,
    "dark_green": 4,
    "yellow": 5,
    "brown": 6,
    "magenta": 7,
    "blue": 8,
    "blue_fill": 9,
}

# Color definitions: (pair_index, fg, bg)
_COLOR_DEFS = {
    "white": (1, curses.COLOR_WHITE, -1),
    "green": (2, curses.COLOR_GREEN, -1),
    "bright_green": (3, curses.COLOR_GREEN, -1),  # + BOLD
    "dark_green": (4, curses.COLOR_GREEN, -1),
    "yellow": (5, curses.COLOR_YELLOW, -1),
    "brown": (6, curses.COLOR_RED, -1),  # closest to brown in basic curses
    "magenta": (7, curses.COLOR_MAGENTA, -1),
    "blue": (8, curses.COLOR_BLUE, -1),
    "blue_fill": (9, curses.COLOR_WHITE, curses.COLOR_CYAN),
}


def init_colors():
    """Initialize curses color pairs. Call after curses.start_color()."""
    curses.use_default_colors()
    for name, (idx, fg, bg) in _COLOR_DEFS.items():
        curses.init_pair(idx, fg, bg)


def color_name_to_pair(name: str) -> int:
    return COLORS.get(name, 0)


def get_color_attr(name: str) -> int:
    """Get the full curses attribute for a color name."""
    pair = color_name_to_pair(name)
    attr = curses.color_pair(pair)
    if name == "bright_green":
        attr |= curses.A_BOLD
    if name == "dark_green":
        attr |= curses.A_DIM
    return attr


def render_frame(stdscr, grid, plants, cursor_x, cursor_y, status_text):
    """Render one frame to the screen."""
    stdscr.erase()
    max_y, max_x = stdscr.getmaxyx()

    # Draw ground
    ground_attr = curses.color_pair(COLORS["brown"]) | curses.A_DIM
    for y in range(max_y - 1):
        for x in range(max_x):
            if grid.is_empty(x, y):
                try:
                    stdscr.addch(y, x, ".", ground_attr)
                except curses.error:
                    pass

    # Draw all occupied cells from grid
    for (x, y), cell in grid._cells.items():
        if 0 <= y < max_y - 1 and 0 <= x < max_x:
            if isinstance(cell, tuple):
                first, ch, color_name = cell
                try:
                    stdscr.addch(y, x, ch, get_color_attr(color_name))
                except curses.error:
                    pass  # ignore edge-of-screen errors

    # Draw cursor - show plant char underneath if occupied, otherwise "+"
    if 0 <= cursor_y < max_y - 1 and 0 <= cursor_x < max_x:
        cell = grid.get(cursor_x, cursor_y)
        if cell and isinstance(cell, tuple):
            _, ch, color_name = cell
            attr = get_color_attr(color_name) | curses.A_REVERSE
        else:
            ch = "+"
            attr = curses.A_REVERSE | curses.A_BLINK
        try:
            stdscr.addch(cursor_y, cursor_x, ch, attr)
        except curses.error:
            pass

    # Draw status bar
    status_line = status_text[:max_x - 1]
    try:
        stdscr.addstr(max_y - 1, 0, status_line, curses.A_REVERSE)
    except curses.error:
        pass

    stdscr.refresh()
