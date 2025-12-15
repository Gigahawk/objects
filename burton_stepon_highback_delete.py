"""Washer to delete the high back on Burton StepOn Bindings

For each binding:
- 2x this part
- 2x 3/8" stainless washers

Place the printed washer with the slanted side against the low back.
The metal washer should be on the flat face of the washer against the retaining
nut.

Recommended print settings:
- PETG
- 100% infill (concentric)
- Max layer height up to `min_thickness` mm (0.3mm for a 0.4mm nozzle)
- Min layer height above `min_thickness` mm (0.05mm on a Prusa MK3s)

TODO: actually test, also figure out model year
Tested on (Gen 1) StepOn bindings.
"""

import logging
from build123d import *
from math import tan, radians

outer_dia = 19
inner_dia = 9.3
washer_angle = 6.95  # deg
# Total thickness with metal washer
total_min_thickness_total = 3
metal_washer_thickness = 0.8  # mm, measure your washers

min_thickness = total_min_thickness_total - metal_washer_thickness
max_thickness = min_thickness + tan(radians(washer_angle)) * outer_dia

logging.critical(f"Washer minimum thickness: {min_thickness}mm")

with BuildPart() as washer:
    # Base part
    Cylinder(
        radius=outer_dia / 2,
        height=max_thickness,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    Cylinder(
        radius=inner_dia / 2,
        height=max_thickness,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
        mode=Mode.SUBTRACT,
    )
    with BuildSketch(Plane.YZ) as sketch:
        with BuildLine():
            Line((-outer_dia / 2, max_thickness), (outer_dia / 2, max_thickness))
            Line((outer_dia / 2, max_thickness), (outer_dia / 2, min_thickness))
            Line((outer_dia / 2, min_thickness), (-outer_dia / 2, max_thickness))
        make_face()
    extrude(until=Until.LAST, both=True, mode=Mode.SUBTRACT)

result = washer.part

if __name__ == "__main__":
    if "show_object" in locals():
        show_object(washer)

    try:
        from ocp_vscode import *

        show_all(measure_tools=True)
    except ImportError:
        pass
