from enum import IntEnum


class Stage(IntEnum):
    SEED = 0
    SPROUT = 1
    BLOOM = 2
    WILT = 3


# Each plant type defines 4 stages (seed, sprout, bloom, wilt).
# Each stage has:
#   - template: list of strings, each string is one row (relative to root at bottom-center)
#   - duration: ticks this stage lasts (-1 = permanent/final)
# Each plant type also has:
#   - colors: default color per stage (fallback)
#   - char_colors: per-character color overrides (char -> color name)

TERRAIN_TYPES = {
    "water": {"char": "~", "color": "blue_fill"},
    "rock": {"char": "#", "color": "white"},
}

PLANT_TYPES = {
    "grass": {
        "stages": [
            {"template": ["."], "duration": 4},
            {"template": ["v"], "duration": 5},
            {"template": ["w"], "duration": 6},
            {"template": [","], "duration": -1},
        ],
        "colors": {
            Stage.SEED: "white",
            Stage.SPROUT: "green",
            Stage.BLOOM: "bright_green",
            Stage.WILT: "brown",
        },
        "char_colors": {},
    },
    "flower": {
        "stages": [
            {"template": ["."], "duration": 5},
            {"template": ["'", "|"], "duration": 8},
            {
                "template": [
                    " @",
                    "@#@",
                    " @",
                    " |",
                    " |",
                ],
                "duration": 12,
            },
            {
                "template": [
                    " .",
                    ".,.",
                    " .",
                    " ;",
                    " ;",
                ],
                "duration": -1,
            },
        ],
        "colors": {
            Stage.SEED: "white",
            Stage.SPROUT: "green",
            Stage.BLOOM: "magenta",
            Stage.WILT: "brown",
        },
        "char_colors": {
            "@": "magenta",
            "#": "yellow",
            "|": "green",
            "'": "bright_green",
        },
    },
    "tree": {
        "stages": [
            {"template": ["."], "duration": 10},
            {"template": ["|", "|"], "duration": 15},
            {
                "template": [
                    "  %%%  ",
                    " %%%%% ",
                    "%%%*%%%",
                    "  |||  ",
                    "  |||  ",
                ],
                "duration": 25,
            },
            {
                "template": [
                    "  ...  ",
                    " ..... ",
                    "...:...",
                    "  |||  ",
                    "  |||  ",
                ],
                "duration": -1,
            },
        ],
        "colors": {
            Stage.SEED: "white",
            Stage.SPROUT: "green",
            Stage.BLOOM: "dark_green",
            Stage.WILT: "brown",
        },
        "char_colors": {
            "%": "green",
            "*": "yellow",
            "|": "brown",
            ":": "brown",
        },
    },
    "cactus": {
        "stages": [
            {"template": ["."], "duration": 8},
            {"template": ["|", "|"], "duration": 12},
            {
                "template": [
                    " | ",
                    "\\| ",
                    " |/",
                    " | ",
                    " | ",
                ],
                "duration": 20,
            },
            {
                "template": [
                    " . ",
                    "\\. ",
                    " ./",
                    " . ",
                    " . ",
                ],
                "duration": -1,
            },
        ],
        "colors": {
            Stage.SEED: "white",
            Stage.SPROUT: "green",
            Stage.BLOOM: "green",
            Stage.WILT: "brown",
        },
        "char_colors": {
            "/": "green",
            "\\": "green",
        },
    },
}
