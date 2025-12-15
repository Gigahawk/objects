"""Tray to hold a single 9V and AA battery on your desk"""

import cadquery as cq

width = 65
height = 60
thickness = 12
chamfer = 3

depth_9v = 17.0
width_9v = 26.5
height_9v = 48.5

diameter_aa = 14.5
length_aa = 50.5

pocket_gap = 4
pocket_edge_to_edge = width_9v + pocket_gap + diameter_aa
offset_9v = (height - pocket_edge_to_edge) / 2
# For some reason AA cut plane origin is at offset_9v already
offset_aa = width_9v + pocket_gap + diameter_aa / 2

result = cq.Workplane("XY").tag("base_plane")

# Base geometry
result = result.rect(width, height, centered=[True, False]).extrude(thickness)

# External chamfers
result = result.edges("|Z").chamfer(chamfer)
result = result.faces(">Z").chamfer(chamfer)

# 9V pocket
result = result.faces(">Z").workplane().center(0, offset_9v)
result = result.rect(height_9v, width_9v, centered=[True, False]).cutBlind(
    -depth_9v / 2
)

# AA pocket
result = (
    result.faces(">X").workplane(offset=-(width + length_aa) / 2).center(offset_aa, 0)
)
result = result.circle(radius=diameter_aa / 2).cutBlind(length_aa)
