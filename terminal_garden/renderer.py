import curses
from terminal_garden.config import PLANT_TYPES, Stage

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
    "sidebar_bg": 10,
    "red": 11,
    "cyan": 12,
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
    "sidebar_bg": (10, curses.COLOR_WHITE, -1),
    "red": (11, curses.COLOR_RED, -1),  # + BOLD for bright red
    "cyan": (12, curses.COLOR_CYAN, -1),
}

# Sidebar config
SIDEBAR_WIDTH = 13  # total columns including borders
_SIDEBAR_INNER = SIDEBAR_WIDTH - 2  # usable inner width (excluding border chars)

# Plant display order matching PLANT_NAMES in main
_PLANT_ORDER = ["grass", "rose", "tulip", "sunflower", "tree"]


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
    if name == "red":
        attr |= curses.A_BOLD
    return attr


def _safe_addstr(stdscr, y, x, text, attr=0):
    """Write string, ignoring edge-of-screen errors."""
    max_y, max_x = stdscr.getmaxyx()
    if y < 0 or y >= max_y or x >= max_x:
        return
    if x + len(text) > max_x:
        text = text[:max_x - x]
    if not text:
        return
    try:
        stdscr.addstr(y, x, text, attr)
    except curses.error:
        pass


def _safe_addch(stdscr, y, x, ch, attr=0):
    """Write char (including Unicode), ignoring edge-of-screen errors."""
    max_y, max_x = stdscr.getmaxyx()
    if 0 <= y < max_y and 0 <= x < max_x:
        try:
            # Use addstr for Unicode support (addch only handles single-byte)
            stdscr.addstr(y, x, ch, attr)
        except curses.error:
            pass


def _draw_sidebar(stdscr, selected, max_y):
    """Draw the plant preview sidebar on the left."""
    border_attr = curses.color_pair(COLORS["white"]) | curses.A_DIM
    inner_w = _SIDEBAR_INNER

    # Top border
    _safe_addstr(stdscr, 0, 0, "┌" + "─" * inner_w + "┐", border_attr)

    # Title row
    title = "PLANTS"
    pad = (inner_w - len(title)) // 2
    _safe_addstr(stdscr, 1, 0, "│", border_attr)
    _safe_addstr(stdscr, 1, 1, " " * pad + title + " " * (inner_w - pad - len(title)), curses.A_BOLD)
    _safe_addstr(stdscr, 1, SIDEBAR_WIDTH - 1, "│", border_attr)

    # Separator
    _safe_addstr(stdscr, 2, 0, "├" + "─" * inner_w + "┤", border_attr)

    row = 3  # current drawing row

    for idx, plant_name in enumerate(_PLANT_ORDER):
        if row >= max_y - 1:
            break

        config = PLANT_TYPES[plant_name]
        bloom_template = config["stages"][Stage.BLOOM]["template"]
        char_colors = config.get("char_colors", {})
        bloom_color = config["colors"][Stage.BLOOM]
        is_selected = (idx == selected)

        # Label row
        label = f"{idx + 1} {plant_name.capitalize()}"
        label_padded = " " + label + " " * (inner_w - len(label) - 1)

        _safe_addstr(stdscr, row, 0, "│", border_attr)
        if is_selected:
            _safe_addstr(stdscr, row, 1, label_padded, curses.A_REVERSE | curses.A_BOLD)
        else:
            _safe_addstr(stdscr, row, 1, label_padded, curses.A_DIM)
        _safe_addstr(stdscr, row, SIDEBAR_WIDTH - 1, "│", border_attr)
        row += 1

        # Draw bloom template rows
        for tmpl_row in bloom_template:
            if row >= max_y - 1:
                break
            pad_left = (inner_w - len(tmpl_row)) // 2
            _safe_addstr(stdscr, row, 0, "│", border_attr)
            _safe_addstr(stdscr, row, 1, " " * inner_w, 0)
            _safe_addstr(stdscr, row, SIDEBAR_WIDTH - 1, "│", border_attr)
            for ci, ch in enumerate(tmpl_row):
                if ch != " ":
                    color = char_colors.get(ch, bloom_color)
                    _safe_addch(stdscr, row, 1 + pad_left + ci, ch, get_color_attr(color))
            row += 1

    # Terrain legend section
    if row < max_y - 1:
        _safe_addstr(stdscr, row, 0, "├" + "─" * inner_w + "┤", border_attr)
        row += 1

    if row < max_y - 1:
        title = "TERRAIN"
        pad = (inner_w - len(title)) // 2
        _safe_addstr(stdscr, row, 0, "│", border_attr)
        _safe_addstr(stdscr, row, 1, " " * pad + title + " " * (inner_w - pad - len(title)), curses.A_BOLD)
        _safe_addstr(stdscr, row, SIDEBAR_WIDTH - 1, "│", border_attr)
        row += 1

    # Water legend
    if row < max_y - 1:
        _safe_addstr(stdscr, row, 0, "│", border_attr)
        _safe_addstr(stdscr, row, 1, " " * inner_w, 0)
        _safe_addstr(stdscr, row, SIDEBAR_WIDTH - 1, "│", border_attr)
        _safe_addch(stdscr, row, 2, "~", get_color_attr("blue_fill"))
        _safe_addstr(stdscr, row, 4, "Water", curses.A_DIM)
        row += 1

    # Rock legend
    if row < max_y - 1:
        _safe_addstr(stdscr, row, 0, "│", border_attr)
        _safe_addstr(stdscr, row, 1, " " * inner_w, 0)
        _safe_addstr(stdscr, row, SIDEBAR_WIDTH - 1, "│", border_attr)
        _safe_addch(stdscr, row, 2, "#", get_color_attr("white"))
        _safe_addstr(stdscr, row, 4, "Rock", curses.A_DIM)
        row += 1

    # Bottom border
    if row < max_y - 1:
        _safe_addstr(stdscr, row, 0, "└" + "─" * inner_w + "┘", border_attr)
        row += 1

    # Fill remaining sidebar rows with border
    while row < max_y - 1:
        _safe_addstr(stdscr, row, 0, "│", border_attr)
        _safe_addstr(stdscr, row, 1, " " * inner_w, 0)
        _safe_addstr(stdscr, row, SIDEBAR_WIDTH - 1, "│", border_attr)
        row += 1


def render_frame(stdscr, grid, plants, cursor_x, cursor_y, status_text,
                 selected=0):
    """Render one frame to the screen."""
    stdscr.erase()
    max_y, max_x = stdscr.getmaxyx()
    ox = SIDEBAR_WIDTH  # x offset for grid area

    # Draw sidebar
    _draw_sidebar(stdscr, selected, max_y)

    # Draw ground (offset by sidebar)
    ground_attr = curses.color_pair(COLORS["brown"]) | curses.A_DIM
    for y in range(max_y - 1):
        for x in range(grid.width):
            sx = ox + x
            if sx < max_x and grid.is_empty(x, y):
                try:
                    stdscr.addstr(y, sx, ".", ground_attr)
                except curses.error:
                    pass

    # Draw all occupied cells from grid (offset by sidebar)
    for (x, y), cell in grid._cells.items():
        sx = ox + x
        if 0 <= y < max_y - 1 and 0 <= sx < max_x:
            if isinstance(cell, tuple):
                first, ch, color_name = cell
                try:
                    stdscr.addstr(y, sx, ch, get_color_attr(color_name))
                except curses.error:
                    pass

    # Draw cursor (offset by sidebar)
    sx = ox + cursor_x
    if 0 <= cursor_y < max_y - 1 and 0 <= sx < max_x:
        cell = grid.get(cursor_x, cursor_y)
        if cell and isinstance(cell, tuple):
            _, ch, color_name = cell
            attr = get_color_attr(color_name) | curses.A_REVERSE
        else:
            ch = "+"
            attr = curses.A_REVERSE | curses.A_BLINK
        try:
            stdscr.addstr(cursor_y, sx, ch, attr)
        except curses.error:
            pass

    # Draw status bar (full width)
    status_line = status_text[:max_x - 1]
    try:
        stdscr.addstr(max_y - 1, 0, status_line, curses.A_REVERSE)
    except curses.error:
        pass

    stdscr.refresh()
