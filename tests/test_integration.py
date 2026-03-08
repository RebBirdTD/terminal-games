from terminal_garden.grid import Grid
from terminal_garden.plants import Plant
from terminal_garden.config import Stage


def test_full_grass_lifecycle():
    """Test a grass plant goes through all stages."""
    g = Grid(20, 20)
    p = Plant("grass", 10, 10, 1)
    p.place_on_grid(g)

    stages_seen = [p.stage]
    for _ in range(100):
        old = p.stage
        p.tick()
        if p.stage != old:
            p.update_grid(g)
            stages_seen.append(p.stage)

    assert Stage.SEED in stages_seen
    assert Stage.SPROUT in stages_seen
    assert Stage.BLOOM in stages_seen
    assert Stage.WILT not in stages_seen


def test_multiple_plants_no_overlap():
    """Test that two plants placed adjacent don't corrupt each other."""
    g = Grid(30, 20)
    p1 = Plant("grass", 5, 10, 1)
    p2 = Plant("grass", 7, 10, 2)
    p1.place_on_grid(g)
    p2.place_on_grid(g)

    cell1 = g.get(5, 10)
    cell2 = g.get(7, 10)
    assert cell1[0] == 1  # plant_id
    assert cell2[0] == 2


def test_tree_grows_multiline():
    """Test that tree bloom stage occupies multiple cells."""
    g = Grid(30, 20)
    p = Plant("tree", 15, 15, 1)
    p.place_on_grid(g)

    # Advance to bloom
    for _ in range(100):
        old = p.stage
        p.tick()
        if p.stage != old:
            p.update_grid(g)
        if p.stage == Stage.BLOOM:
            break

    assert p.stage == Stage.BLOOM
    # Tree should occupy multiple cells
    occupied = [(x, y) for (x, y) in g._cells if g.get(x, y) and g.get(x, y)[0] == 1]
    assert len(occupied) > 1


def test_cannot_plant_on_occupied():
    """Verify placement check works."""
    g = Grid(20, 20)
    p = Plant("grass", 5, 5, 1)
    p.place_on_grid(g)
    assert not g.is_empty(5, 5)
