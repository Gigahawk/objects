"""LCD panel HYX-JX0701570D103A27"""

import cadquery as cq
from constants import (
    display_outer_height, display_outer_width, display_thickness)


def make_display():
    out = (
        cq.Workplane()
        .box(display_outer_width, display_outer_height, display_thickness)
    )

    out.faces("<Z").tag("display_back").end()

result = make_display()