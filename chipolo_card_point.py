"""Dummy part matching the dimensions of a Chipolo Card Point

https://chipolo.net/en-us/products/chipolo-card-point
"""

from build123d import *

thickness = 2.4
length = 85.1
width = 53.6

# Standard credit card dimensions per ISO/IEC 7810
corner_fillet = 3.18

# Best guess from pictures
edge_fillet = 0.5



with BuildPart() as part:
    Box(length, width, thickness)
    fillet(
        part.edges()
        .filter_by(Axis.Z),
        radius=corner_fillet
    )
    fillet(
        part.edges()
        .filter_by(Axis.Z, reverse=True),
        radius=edge_fillet
    )

result = part.part

if "show_object" in locals():
    show_object(result)