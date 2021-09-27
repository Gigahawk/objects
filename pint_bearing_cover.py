"""Clone of BadgerWheel OneWheel Pint Bearing Cover"""

import cadquery as cq
import numpy as np

nom_cavity_dia = 48.0
nom_shaft_dia = 40.0
nom_shaft_circ = np.pi*nom_shaft_dia
cavity_depth = 20

gap = 1
cavity_dia = nom_cavity_dia + gap
shaft_dia = nom_shaft_dia + gap
shaft_circ = np.pi*shaft_dia

cutout_arc = shaft_circ - nom_shaft_circ
cutout_angle = cutout_arc/(shaft_dia/2)
cutout_points = [
    (0, 0),
    (cavity_dia, 0),
    (cavity_dia, np.tan(cutout_angle)*cavity_dia)
]

result = (
    cq.Workplane("XY").tag("base_plane")
    .circle(cavity_dia/2).circle(shaft_dia/2)
    .extrude(10)
    .polyline(cutout_points).close().cutThruAll()
)