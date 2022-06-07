"""Tray to hold a single 9V and AA battery on your desk"""

import cadquery as cq

width = 65
height = 60
thickness = 15
chamfer = 3

offset_9v = 5.0
depth_9v = 17.0
width_9v = 26.5
height_9v = 48.5

offset_aa = 40
diameter_aa = 14.5
length_aa = 50.5

result = (
    cq.Workplane("XY").tag("base_plane")
    # Base geometry
    .rect(width, height, centered=[True, False]).extrude(thickness)
    # External chamfers
    .edges("|Z").chamfer(chamfer)
    .faces(">Z").chamfer(chamfer)
    # 9V pocket
    .faces(">Z").workplane().center(0, offset_9v)
    .rect(height_9v, width_9v, centered=[True, False]).cutBlind(-depth_9v/2)
    # AA pocket
    .faces(">X").workplane().workplane(offset=-(width + length_aa)/2).center(offset_aa, 0)
    .circle(radius=diameter_aa/2).cutBlind(length_aa)
)