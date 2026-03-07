class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self._cells = {}  # (x, y) -> plant_id or char info

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get(self, x: int, y: int):
        return self._cells.get((x, y))

    def set(self, x: int, y: int, value):
        if self.in_bounds(x, y):
            self._cells[(x, y)] = value

    def clear(self, x: int, y: int):
        self._cells.pop((x, y), None)

    def is_empty(self, x: int, y: int) -> bool:
        if not self.in_bounds(x, y):
            return False
        return (x, y) not in self._cells

    def can_place(self, root_x: int, root_y: int, template: list[str]) -> bool:
        """Check if a template can be placed at root position.
        Template rows are bottom-to-top, each row centered on root_x.
        Root position is bottom-center of the template.
        """
        for row_offset, row in enumerate(reversed(template)):
            y = root_y - row_offset
            x_start = root_x - len(row) // 2
            for col, ch in enumerate(row):
                if ch != " ":
                    if not self.is_empty(x_start + col, y):
                        return False
        return True
