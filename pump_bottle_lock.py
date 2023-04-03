"""Lock for pump bottles"""

import cadquery as cq
import numpy as np
from math import sin, cos, pi

inner_diameter = 8.15
height = 9.3
handle_length = 8
handle_diameter = 4
thickness = 1.5
opening_angle = pi/2
fillet = 1.5

center_diameter = inner_diameter + thickness
rad = center_diameter/2
theta = pi/2 - opening_angle/2
pt1 = rad*np.array([cos(theta), sin(theta)])
_pt2 = rad*np.array([0, -1])
_pt3 = rad*np.array([-cos(theta), sin(theta)])
pt2 = _pt2 - pt1
pt3 = _pt3 - pt1
pt4 = _pt2 + handle_length/2*np.array([0, -1])
pt5 = _pt2 + handle_length*np.array([0, -1])


result = (
    cq.Workplane("XY").tag("base_plane")
    .center(*pt1)
    .threePointArc(pt2, pt3)
    .offset2D(thickness/2)
    .extrude(height)
    .workplaneFromTagged("base_plane")
    .center(*pt4)
    .slot2D(handle_length, thickness, -90)
    .extrude(height)
    .workplaneFromTagged("base_plane")
    .center(*pt5)
    .circle(handle_diameter/2).extrude(height)
    .edges("|Z")
    .fillet(1.5)
)
