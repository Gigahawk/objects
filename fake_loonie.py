import cadquery as cq
from math import sin, cos, floor, pi

def realeaux(self, w, n):
    rl = cq.Workplane()
    s = 2*w*sin(pi/(2*n))

    poly_dia = s/sin(pi/n)
    pts1 = cq.Workplane().polygon(n, poly_dia).vertices().vals()
    pts2 = pts1[1:] + [pts1[0]]

    for p1, p2 in zip(pts1, pts2):
        rl = rl.moveTo(p1.X, p1.Y)
        rl = rl.radiusArc((p2.X, p2.Y), -w)
    rl = rl.close()
    rl = rl.val()

    return self.eachpoint(lambda loc: rl.located(loc), True)

cq.Workplane.realeaux = realeaux

# A loonie is an 11 sided realeaux polygon
diameter = 26.5
thickness = 1.95
sides = 11

# Tab length from edge of coin
tab_length = 10.0
tab_width = 10.0

tab_dist = diameter/2 + tab_length

# Fillet radius of tab
fillet_rad = 3.0

# Width of tab cuts for grip
cut_width = 1.5

cut_depth = thickness/4
cut_count = floor(tab_length / cut_width)


result = (
    cq.Workplane("XY").tag("base_plane")
    .rect(tab_width, tab_dist, centered=[True, False]).extrude(thickness)
    .edges("|Z").fillet(fillet_rad)
    .workplaneFromTagged("base_plane")
    .realeaux(diameter, sides).extrude(thickness)
    .faces(">Z").workplane()
    .pushPoints([(0, diameter/2 + i*cut_width*2) for i in range(cut_count)])
    .rect(tab_width, cut_width, centered=[True, False]).cutBlind(-cut_depth)
)