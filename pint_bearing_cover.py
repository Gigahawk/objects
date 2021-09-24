"""Clone of BadgerWheel OneWheel Pint Bearing Cover"""

import cadquery as cq

cavity_dia = 48.0
shaft_dia = 40.0

result = (
    cq.Workplane("XY").tag("base_plane")
)