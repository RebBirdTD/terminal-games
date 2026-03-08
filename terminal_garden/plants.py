import random
from terminal_garden.config import PLANT_TYPES, Stage

SPREAD_CHANCE = 0.03  # probability per tick at BLOOM stage
SPREAD_INTERVAL = 5   # only try spreading every N ticks


class Plant:
    def __init__(self, plant_type: str, root_x: int, root_y: int, plant_id: int):
        self.plant_type = plant_type
        self.root_x = root_x
        self.root_y = root_y
        self.plant_id = plant_id
        self.age = 0
        self.stage = Stage.SEED
        self._config = PLANT_TYPES[plant_type]
        self._stage_age = 0  # ticks in current stage
        self._occupied_cells: list[tuple[int, int]] = []

    def tick(self):
        self.age += 1
        self._stage_age += 1
        stage_info = self._config["stages"][self.stage]
        duration = stage_info["duration"]
        if duration != -1 and self._stage_age >= duration and self.stage < Stage.BLOOM:
            self.stage = Stage(self.stage + 1)
            self._stage_age = 0

    def get_template(self) -> list[str]:
        return self._config["stages"][self.stage]["template"]

    def get_color(self) -> str:
        return self._config["colors"][self.stage]

    def get_char_color(self, ch: str) -> str:
        """Get color for a specific character, falling back to stage color."""
        char_colors = self._config.get("char_colors", {})
        if ch in char_colors:
            return char_colors[ch]
        return self.get_color()

    def _compute_cells(self) -> list[tuple[int, int, str]]:
        """Compute (x, y, char) for current template."""
        template = self.get_template()
        cells = []
        for row_offset, row in enumerate(reversed(template)):
            y = self.root_y - row_offset
            x_start = self.root_x - len(row) // 2
            for col, ch in enumerate(row):
                if ch != " ":
                    cells.append((x_start + col, y, ch))
        return cells

    def place_on_grid(self, grid):
        """Place plant on grid for the first time."""
        self._clear_from_grid(grid)
        for x, y, ch in self._compute_cells():
            if grid.is_empty(x, y):
                grid.set(x, y, (self.plant_id, ch, self.get_char_color(ch)))
                self._occupied_cells.append((x, y))

    def update_grid(self, grid):
        """Update grid after stage change or growth."""
        self.place_on_grid(grid)

    def try_spread(self, grid):
        """Grass at BLOOM stage may spread to an adjacent empty cell.

        Returns (x, y) of new grass position, or None.
        """
        if self.plant_type != "grass" or self.stage != Stage.BLOOM:
            return None
        if self._stage_age % SPREAD_INTERVAL != 0:
            return None
        if random.random() > SPREAD_CHANCE:
            return None
        # Pick a random cardinal neighbor of root
        dx, dy = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        nx, ny = self.root_x + dx, self.root_y + dy
        if grid.is_empty(nx, ny):
            return (nx, ny)
        return None

    def _clear_from_grid(self, grid):
        """Remove all cells belonging to this plant from grid."""
        for x, y in self._occupied_cells:
            cell = grid.get(x, y)
            if cell is not None and isinstance(cell, tuple) and cell[0] == self.plant_id:
                grid.clear(x, y)
        self._occupied_cells = []
