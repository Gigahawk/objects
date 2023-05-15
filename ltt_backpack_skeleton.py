"""Ribbing to prevent tipping of the LTT Store Backpack"""

from math import tan, pi
import cadquery as cq

thickness = 13
width = 20
height = 120
length = 145
fillet = 20
taper_angle = 15
taper_fillet = 5
face_chamfer = 3

taper_length = tan((90 - taper_angle)*pi/180)*thickness


main_rib_points = [
    (0, 0),
    (length, 0),
    (length, height),
    (length - thickness, height - taper_length),
    (length - thickness, thickness),
    (thickness, thickness),
    (thickness, height - taper_length),
    (0, height)
]

result = (
    cq.Workplane("XY").tag("base_plane")
    .polyline(main_rib_points).close().extrude(width)
    .edges("|Z and >Y").fillet(taper_fillet)
    .edges("|Z").fillet(fillet)
    .faces("|Z").chamfer(face_chamfer)
)
