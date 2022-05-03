"""Replacement support pillars for a paper tray"""

import cadquery as cq

width = 17.1

insert_thickness = 3.8
insert_depth = 12

pillar_thickness = 8
pillar_height = 75

chamfer = 2

result = (
    cq.Workplane("XY").tag("base_plane")
    .rect(width, insert_thickness, centered=[True, False]).extrude(insert_depth)
    .faces(">Z").workplane()
    .rect(width, pillar_thickness, centered=[True, False]).extrude(pillar_height)
    .faces(">Z").workplane()
    .rect(width, insert_thickness, centered=[True, False]).extrude(insert_depth)
    .edges("|Y").chamfer(chamfer)
)