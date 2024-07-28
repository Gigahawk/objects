"""Spacers to keep a rolling pin at a set height
"""

from pathlib import Path
from build123d import *
from functools import cache
from itertools import product

spacer_thickness = 6
spacer_dia = 38
tolerance = 0.5
inner_chamfer = 1

dough_thicknesses = [
    10,  # 1/4in
    4
]


def build_spacer(d_t: float):
    with BuildPart() as spacer:
        Cylinder(
            radius=(spacer_dia + 2*d_t)/2, height=spacer_thickness,
            align=Align.CENTER
        )
        Cylinder(
            radius=(spacer_dia + tolerance)/2, height=spacer_thickness,
            align=Align.CENTER, mode=Mode.SUBTRACT
        )
        chamfer(spacer.edges(Select.LAST), length=inner_chamfer)
    return spacer


results = {
    f"{t}mm":
        build_spacer(t).part for
            t in dough_thicknesses
}


if __name__ == "__main__":
    if "show_object" in locals():
        show_object(None)

    try:
        from ocp_vscode import *
        show(*list(results.values()), names=list(results.keys()), measure_tools=True)
    except ImportError:
        pass
