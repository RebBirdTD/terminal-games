from terminal_garden.grid import Grid


def test_grid_creation():
    g = Grid(80, 24)
    assert g.width == 80
    assert g.height == 24


def test_grid_empty_by_default():
    g = Grid(10, 10)
    assert g.get(0, 0) is None
    assert g.get(5, 5) is None


def test_grid_set_and_get():
    g = Grid(10, 10)
    g.set(3, 4, "plant_id_1")
    assert g.get(3, 4) == "plant_id_1"


def test_grid_is_empty():
    g = Grid(10, 10)
    assert g.is_empty(5, 5) is True
    g.set(5, 5, "x")
    assert g.is_empty(5, 5) is False


def test_grid_out_of_bounds():
    g = Grid(10, 10)
    assert g.is_empty(-1, 0) is False  # out of bounds = not empty
    assert g.is_empty(10, 0) is False
    assert g.get(-1, 0) is None


def test_grid_clear_cell():
    g = Grid(10, 10)
    g.set(3, 3, "x")
    g.clear(3, 3)
    assert g.is_empty(3, 3) is True


def test_grid_can_place_template():
    g = Grid(20, 20)
    template = ["*", "|"]
    # template places from bottom up, centered on x
    assert g.can_place(10, 10, template) is True
    # Block one cell
    g.set(10, 10, "occupied")
    assert g.can_place(10, 10, template) is False


def test_set_terrain_stores_correctly():
    g = Grid(10, 10)
    g.set_terrain(3, 3, "~", "blue")
    cell = g.get(3, 3)
    assert cell == ("terrain", "~", "blue")


def test_is_terrain():
    g = Grid(10, 10)
    assert g.is_terrain(3, 3) is False
    g.set_terrain(3, 3, "~", "blue")
    assert g.is_terrain(3, 3) is True
    # Regular cell is not terrain
    g.set(5, 5, (1, "x", "green"))
    assert g.is_terrain(5, 5) is False


def test_terrain_blocks_plant_placement():
    g = Grid(10, 10)
    g.set_terrain(5, 5, "#", "white")
    assert g.is_empty(5, 5) is False
    assert g.can_place(5, 5, ["*"]) is False
