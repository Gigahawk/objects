"""Cover to prevent SoundBot SB210 buttons from being pressed by a tight helmet"""

import cadquery as cq

bulk_width = 38
bulk_height = 11
bulk_thickness = 3

button_depth = 2.6
button_width = 6.2
button_distance = 13.75
button_chamfer1 = 0.2
button_chamfer2 = 1.0

fillet = 2

result = (
    cq.Workplane("XY").tag("base_plane")
    .rect(bulk_width, bulk_height, centered=True).extrude(bulk_thickness)
    .edges("|Z")
    .fillet(fillet)
    .faces(">Z").workplane()
    .rarray(button_distance, 0.1, 3, 1, center=True)
    .rect(button_width, button_width)
    .cutBlind(-button_depth)
    # Not sure why you can't do `and not()`
    .edges(">Z and #Z").edges("not(>Y or >X or <Y or <X)")
    .chamfer(button_chamfer1, button_chamfer2)
)