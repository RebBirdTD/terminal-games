from terminal_garden.plants import Plant
from terminal_garden.config import Stage
from terminal_garden.grid import Grid


def test_plant_creation():
    p = Plant(plant_type="grass", root_x=5, root_y=10, plant_id=1)
    assert p.plant_type == "grass"
    assert p.root_x == 5
    assert p.root_y == 10
    assert p.age == 0
    assert p.stage == Stage.SEED


def test_plant_tick_advances_age():
    p = Plant("grass", 5, 10, 1)
    p.tick()
    assert p.age == 1


def test_plant_stage_transitions():
    p = Plant("grass", 5, 10, 1)
    # Grass seed duration = 4
    for _ in range(4):
        p.tick()
    assert p.stage == Stage.SPROUT


def test_plant_stays_at_bloom():
    p = Plant("grass", 5, 10, 1)
    # seed=4, sprout=5 => bloom at tick 9, stays there
    for _ in range(100):
        p.tick()
    assert p.stage == Stage.BLOOM


def test_plant_get_template():
    p = Plant("grass", 5, 10, 1)
    assert p.get_template() == ["⋆"]
    for _ in range(4):
        p.tick()
    assert p.get_template() == ["v"]


def test_plant_get_color():
    p = Plant("grass", 5, 10, 1)
    assert p.get_color() == "white"
    for _ in range(4):
        p.tick()
    assert p.get_color() == "green"


def test_plant_place_on_grid():
    g = Grid(20, 20)
    p = Plant("grass", 5, 10, 1)
    p.place_on_grid(g)
    assert not g.is_empty(5, 10)


def test_plant_update_grid_on_stage_change():
    g = Grid(20, 20)
    p = Plant("rose", 5, 10, 1)
    p.place_on_grid(g)
    # Advance to sprout (rose seed duration = 5)
    for _ in range(5):
        p.tick()
    p.update_grid(g)
    # Rose sprout template is ["|"], so root cell should still be occupied
    assert not g.is_empty(5, 10)
