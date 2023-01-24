"""Cover to prevent SoundBot SB210 buttons from being pressed by a tight helmet"""

import cadquery as cq

bulk_width = 38
bulk_height = 11
bulk_thickness = 3

button_depth = 2.6
button_width = 6
button_distance = 13.75

fillet = 3

result = (
    cq.Workplane("XY").tag("base_plane")
    .rect(bulk_width, bulk_height, centered=True).extrude(bulk_thickness)
    .edges("|Z")
    .fillet(fillet)
    .faces(">Z").workplane()
    .rarray(button_distance, 0.1, 3, 1, center=True)
    .rect(button_width, button_width)
    .cutBlind(-button_depth)
)