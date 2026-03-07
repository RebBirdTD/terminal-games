from terminal_garden.config import PLANT_TYPES, Stage


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
        if duration != -1 and self._stage_age >= duration and self.stage < Stage.WILT:
            self.stage = Stage(self.stage + 1)
            self._stage_age = 0

    def get_template(self) -> list[str]:
        return self._config["stages"][self.stage]["template"]

    def get_color(self) -> str:
        return self._config["colors"][self.stage]

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
                grid.set(x, y, (self.plant_id, ch, self.get_color()))
                self._occupied_cells.append((x, y))

    def update_grid(self, grid):
        """Update grid after stage change or growth."""
        self.place_on_grid(grid)

    def _clear_from_grid(self, grid):
        """Remove all cells belonging to this plant from grid."""
        for x, y in self._occupied_cells:
            cell = grid.get(x, y)
            if cell is not None and isinstance(cell, tuple) and cell[0] == self.plant_id:
                grid.clear(x, y)
        self._occupied_cells = []
