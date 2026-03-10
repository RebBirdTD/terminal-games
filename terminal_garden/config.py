from enum import IntEnum


class Stage(IntEnum):
    SEED = 0
    SPROUT = 1
    BLOOM = 2
    WILT = 3


TERRAIN_TYPES = {
    "water": {"char": "~", "color": "blue_fill"},       # sparse wave chars
    "water_fill": {"char": " ", "color": "blue_fill"},   # solid pond body
    "rock": {"char": "#", "color": "white"},
}

PLANT_TYPES = {
    "grass": {
        "stages": [
            {"template": ["⋆"], "duration": 4},
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
        "char_colors": {
            "⋆": "white",
        },
    },
    "rose": {
        "stages": [
            {"template": ["⋆"], "duration": 5},
            {"template": ["°", "|"], "duration": 8},
            {
                "template": [
                    " ✿",
                    "❀@❀",
                    " ✿",
                    " |~",
                    "~|",
                ],
                "duration": 12,
            },
            {
                "template": [
                    " °",
                    "°.°",
                    " °",
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
            "❀": "magenta",
            "✿": "red",
            "@": "yellow",
            "|": "green",
            "~": "bright_green",
            "°": "bright_green",
            "⋆": "white",
        },
    },
    "tulip": {
        "stages": [
            {"template": ["⋆"], "duration": 5},
            {"template": ["°", "|"], "duration": 8},
            {
                "template": [
                    " ❁",
                    "(⚘)",
                    " |~",
                    "~|",
                ],
                "duration": 14,
            },
            {
                "template": [
                    " °",
                    "°.°",
                    " ;",
                    " ;",
                ],
                "duration": -1,
            },
        ],
        "colors": {
            Stage.SEED: "white",
            Stage.SPROUT: "green",
            Stage.BLOOM: "red",
            Stage.WILT: "brown",
        },
        "char_colors": {
            "⚘": "magenta",
            "❁": "red",
            "(": "cyan",
            ")": "cyan",
            "|": "green",
            "~": "bright_green",
            "°": "bright_green",
            "⋆": "white",
        },
    },
    "sunflower": {
        "stages": [
            {"template": ["⋆"], "duration": 5},
            {"template": ["°", "|"], "duration": 10},
            {
                "template": [
                    "\\❁/",
                    "✿@✿",
                    "/❁\\",
                    " |~",
                    "~|",
                ],
                "duration": 15,
            },
            {
                "template": [
                    "...",
                    ".,.",
                    "...",
                    " ;",
                    " ;",
                ],
                "duration": -1,
            },
        ],
        "colors": {
            Stage.SEED: "white",
            Stage.SPROUT: "green",
            Stage.BLOOM: "yellow",
            Stage.WILT: "brown",
        },
        "char_colors": {
            "✿": "yellow",
            "❁": "red",
            "@": "brown",
            "\\": "yellow",
            "/": "yellow",
            "|": "green",
            "~": "bright_green",
            "°": "bright_green",
            "⋆": "white",
        },
    },
    "tree": {
        "stages": [
            {"template": ["⋆"], "duration": 10},
            {"template": ["|", "|"], "duration": 15},
            {
                "template": [
                    "    %    ",
                    "  %%%%%  ",
                    " %%%%%%% ",
                    "%%%%%%%%%",
                    " %%%*%%% ",
                    "%%%%%%%%%",
                    "  %%%%%  ",
                    "    |    ",
                    "    |    ",
                    "    |    ",
                ],
                "duration": 25,
            },
            {
                "template": [
                    "    .    ",
                    "  .....  ",
                    " ....... ",
                    ".........",
                    " ...:... ",
                    ".........",
                    "  .....  ",
                    "    |    ",
                    "    |    ",
                    "    |    ",
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
            "⋆": "white",
        },
    },
}
