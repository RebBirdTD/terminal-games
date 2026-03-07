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

    # Draw all occupied cells from grid
    for (x, y), cell in grid._cells.items():
        if 0 <= y < max_y - 1 and 0 <= x < max_x:
            if isinstance(cell, tuple):
                plant_id, ch, color_name = cell
                try:
                    stdscr.addch(y, x, ch, get_color_attr(color_name))
                except curses.error:
                    pass  # ignore edge-of-screen errors

    # Draw cursor
    if 0 <= cursor_y < max_y - 1 and 0 <= cursor_x < max_x:
        try:
            stdscr.addch(cursor_y, cursor_x, ord("+"), curses.A_REVERSE | curses.A_BLINK)
        except curses.error:
            pass

    # Draw status bar
    status_line = status_text[:max_x - 1]
    try:
        stdscr.addstr(max_y - 1, 0, status_line, curses.A_REVERSE)
    except curses.error:
        pass

    stdscr.refresh()
