from terminal_garden.renderer import color_name_to_pair, COLORS


def test_color_map_has_required_colors():
    required = ["white", "green", "bright_green", "dark_green", "yellow", "brown"]
    for c in required:
        assert c in COLORS, f"Missing color: {c}"


def test_color_pair_indices_are_unique():
    indices = list(COLORS.values())
    assert len(indices) == len(set(indices))


def test_color_name_to_pair():
    pair = color_name_to_pair("green")
    assert isinstance(pair, int)
