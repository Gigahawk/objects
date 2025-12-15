"""Catan number tiles compatible with Dakanzala/MATT makes Catan 2.0 set

https://www.thingiverse.com/thing:2525047
"""

from pathlib import Path
from build123d import *
from functools import cache
from itertools import product

tile_dia = 25
tile_thickness = 2

number_font = str(Path(__file__).parent / "res/LiberationSans-Bold.ttf")
number_size = 13
number_offset = 2
number_thickness = 0.6
number_cutout_clearance = 0.15
number_cutout_depth = 0.3
dot_dia = 2.5
dot_offset = 7
dot_spacing = 3.5

letter_size = 17
letter_depth = 0.3

# https://boardgames.stackexchange.com/a/2741
# 8 and 6 should have red text
numbers = {
    "A": 5,
    "B": 2,
    "C": 6,
    "D": 3,
    "E": 8,
    "F": 10,
    "G": 9,
    "H": 12,
    "I": 11,
    "J": 4,
    "K": 8,
    "L": 10,
    "M": 9,
    "N": 4,
    "O": 5,
    "P": 6,
    "Q": 3,
    "R": 11,
}


@cache
def get_dice_combos(val, dice=2, faces=6):
    @cache
    def get_dice_combos(d, f):
        dice_vals = [list(range(1, f + 1)) for _ in range(d)]
        return list(product(*dice_vals))

    combos = get_dice_combos(dice, faces)
    sums = [sum(c) for c in combos]
    count = sum(val == s for s in sums)
    return count


def build_tile(letter, number, dots, multipart=False):
    with BuildPart() as tile:
        Cylinder(
            radius=tile_dia / 2,
            height=tile_thickness,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        top_face = tile.faces().sort_by(Axis.Z)[-1]

        with BuildSketch(top_face) as number_sketch:
            with Locations((0, number_offset)):
                Text(
                    str(number),
                    font_size=number_size,
                    font_style=FontStyle.BOLD,
                    font_path=number_font,
                )
            with Locations((0, -dot_offset)):
                with GridLocations(
                    x_spacing=dot_spacing, y_spacing=0, x_count=dots, y_count=1
                ):
                    Circle(radius=dot_dia / 2)
        extrude(amount=number_thickness)

        with BuildSketch(Location((0, 0, 0), (0, 180, 0))) as letter_sketch:
            Text(
                str(letter),
                font_size=letter_size,
                font_style=FontStyle.BOLD,
                font_path=number_font,
            )
        extrude(amount=-letter_depth, mode=Mode.SUBTRACT)

        if multipart:
            with BuildSketch(top_face) as number_cutout_sketch:
                offset(objects=number_sketch.faces(), amount=number_cutout_clearance)
            extrude(amount=-number_cutout_depth, mode=Mode.SUBTRACT)
    return tile


results = {
    f"{letter}_{number}{'_multipart' if multipart else ''}": build_tile(
        letter, number, get_dice_combos(number), multipart=multipart
    ).part
    for (letter, number), multipart in product(numbers.items(), [True, False])
}


if __name__ == "__main__":
    if "show_object" in locals():
        show_object(None)

    try:
        from ocp_vscode import *

        show(*list(results.values()), names=list(results.keys()), measure_tools=True)
    except ImportError:
        pass
